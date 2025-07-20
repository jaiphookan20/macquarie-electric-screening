# app/services.py

import pandas as pd
from datetime import datetime
from . import db
from .models import Customer, Product, Transaction, CustomerAddress, UploadLog

def process_excel_file(filepath, filename):
    """Process uploaded Excel file and return analysis results."""
    try:
        # Load data from Excel file
        transactions_df, customers_df, products_df = load_excel_data(filepath)
        
        # Clean and parse customer data
        customers_df = clean_customer_data(customers_df)
        
        # Store data in database
        address_history = store_data_to_db(transactions_df, customers_df, products_df)
        
        # Perform analysis
        analysis_results = perform_data_analysis(transactions_df, customers_df, products_df)
        
        # Log the upload
        log_upload(filename, len(transactions_df), len(customers_df), len(products_df))
        
        # Include address history in results
        analysis_results['address_history'] = address_history
        
        return True, analysis_results
        
    except Exception as e:
        return False, str(e)

def load_excel_data(filepath):
    """Load data from Excel file into DataFrames."""
    # Read all sheets
    transactions_df = pd.read_excel(filepath, sheet_name='Transactions')
    customers_df = pd.read_excel(filepath, sheet_name='Customers')
    products_df = pd.read_excel(filepath, sheet_name='Products')
    
    return transactions_df, customers_df, products_df

def clean_customer_data(customers_df):
    """Parse the single-column customer data format."""
    # The customer data is in format: {C0001_Name_email_dob_address_created_date}
    cleaned_data = []
    
    for _, row in customers_df.iterrows():
        try:
            # Get the single column value
            customer_string = str(row.iloc[0])
            
            # Remove curly braces and split by underscore
            customer_string = customer_string.strip('{}')
            parts = customer_string.split('_')
            
            if len(parts) >= 6:
                customer_data = {
                    'customer_id': parts[0],
                    'name': parts[1],
                    'email': parts[2],
                    'dob': parts[3],
                    'address': parts[4],
                    'created_date': parts[5]
                }
                cleaned_data.append(customer_data)
        except Exception as e:
            print(f"Error parsing customer row: {e}")
            continue
    
    return pd.DataFrame(cleaned_data)

def store_data_to_db(transactions_df, customers_df, products_df):
    """Store processed data to SQLite database and track address changes."""
    address_history = {}
    try:
        # Store customers and handle address changes
        for _, row in customers_df.iterrows():
            try:
                customer_id = row['customer_id']
                # Merge customer data
                customer = Customer(
                    id=customer_id,
                    name=row['name'],
                    email=row['email'],
                    dob=datetime.strptime(row['dob'], '%Y-%m-%d').date(),
                    created_date=datetime.now()
                )
                db.session.merge(customer)

                # Address change detection
                new_address = row['address']
                current_address = CustomerAddress.query.filter_by(
                    customer_id=customer_id, end_date=None
                ).first()

                if current_address:
                    if current_address.address != new_address:
                        # End date the old address
                        current_address.end_date = datetime.now()
                        db.session.add(current_address)
                        
                        # Create a new address record
                        new_address_record = CustomerAddress(
                            customer_id=customer_id,
                            address=new_address,
                            start_date=datetime.now()
                        )
                        db.session.add(new_address_record)
                else:
                    # No current address, so create one
                    new_address_record = CustomerAddress(
                        customer_id=customer_id,
                        address=new_address,
                        start_date=datetime.now()
                    )
                    db.session.add(new_address_record)

            except Exception as e:
                print(f"Error storing customer {row.get('customer_id', 'unknown')}: {e}")
                continue
        
        # Store products
        for _, row in products_df.iterrows():
            try:
                product = Product(
                    id=row['product_code'],
                    name=row['product_name'],
                    category=row['category'],
                    unit_price=row['unit_price']
                )
                db.session.merge(product)
            except Exception as e:
                print(f"Error storing product {row.get('product_code', 'unknown')}: {e}")
                continue
        
        # Store transactions
        for _, row in transactions_df.iterrows():
            try:
                transaction_date = pd.to_datetime(row['transaction_date'], origin='1899-12-30', unit='D')
                
                transaction = Transaction(
                    id=row['transaction_id'],
                    customer_id=row['customer_id'],
                    product_id=row['product_code'],
                    transaction_date=transaction_date,
                    amount=row['amount'],
                    payment_type=row['payment_type']
                )
                db.session.merge(transaction)
            except Exception as e:
                print(f"Error storing transaction {row.get('transaction_id', 'unknown')}: {e}")
                continue
        
        db.session.commit()
        
        # Collect address history for all customers after commit
        for customer_id in customers_df['customer_id'].unique():
            history = CustomerAddress.query.filter_by(customer_id=customer_id).order_by(CustomerAddress.start_date.desc()).all()
            customer = Customer.query.filter_by(id=customer_id).first()
            address_history[customer_id] = [
                {
                    'address': h.address, 
                    'name': customer.name,
                    'start_date': h.start_date.strftime('%Y-%m-%d %H:%M:%S'), 
                    'end_date': h.end_date.strftime('%Y-%m-%d %H:%M:%S') if h.end_date else 'Present'
                } for h in history
            ]
        
        return address_history
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Database storage failed: {e}")

# Address change detection removed for simplicity - can be added later if needed

def perform_data_analysis(transactions_df, customers_df, products_df):
    """Perform required data analysis."""
    # Merge dataframes for analysis
    analysis_df = transactions_df.merge(products_df, left_on='product_code', right_on='product_code')
    analysis_df = analysis_df.merge(customers_df, left_on='customer_id', right_on='customer_id')
    
    # Calculate total transaction amount per customer per category
    customer_category_totals = analysis_df.groupby(['customer_id', 'name', 'category'])['amount'].sum().reset_index()
    
    # Identify top spender in each category
    category_totals = analysis_df.groupby(['category', 'customer_id', 'name'])['amount'].sum().reset_index()
    top_spenders_by_category = category_totals.loc[category_totals.groupby('category')['amount'].idxmax()]
    
    # Rank customers by total purchase value
    customer_rankings = analysis_df.groupby(['customer_id', 'name'])['amount'].sum().reset_index()
    customer_rankings = customer_rankings.sort_values('amount', ascending=False)
    customer_rankings['rank'] = range(1, len(customer_rankings) + 1)
    
    return {
        'customer_category_totals': customer_category_totals,
        'top_spenders_by_category': top_spenders_by_category,
        'customer_rankings': customer_rankings
    }

def log_upload(filename, transaction_count, customer_count, product_count):
    """Log upload metadata to database."""
    upload_log = UploadLog(
        filename=filename,
        transaction_rows=transaction_count,
        customer_rows=customer_count,
        product_rows=product_count
    )
    db.session.add(upload_log)
    db.session.commit()
