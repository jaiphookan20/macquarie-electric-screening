import unittest
import pandas as pd
from datetime import datetime
import tempfile
import os
import sys

# Add the parent directory to the path to import the app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db
from app.models import Customer, CustomerAddress
from app.services import store_data_to_db


class TestAddressHistory(unittest.TestCase):
    """Test cases for address change detection and history tracking."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with self.app.app_context():
            db.create_all()
            
        self.app_context = self.app.app_context()
        self.app_context.push()
        
    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_new_customer_address_creation(self):
        """Test that a new customer gets their first address record."""
        # Create test data
        customers_df = pd.DataFrame({
            'customer_id': ['C001'],
            'name': ['John Doe'],
            'email': ['john@example.com'],
            'dob': ['1990-01-01'],
            'address': ['123 Main St, Sydney NSW 2000']
        })
        
        transactions_df = pd.DataFrame()
        products_df = pd.DataFrame()
        
        # Store data
        address_history = store_data_to_db(transactions_df, customers_df, products_df)
        
        # Verify customer was created
        customer = Customer.query.filter_by(id='C001').first()
        self.assertIsNotNone(customer)
        self.assertEqual(customer.name, 'John Doe')
        
        # Verify address was created
        address = CustomerAddress.query.filter_by(customer_id='C001').first()
        self.assertIsNotNone(address)
        self.assertEqual(address.address, '123 Main St, Sydney NSW 2000')
        self.assertIsNotNone(address.start_date)
        self.assertIsNone(address.end_date)
        
        # Verify address history is returned
        self.assertIn('C001', address_history)
        self.assertEqual(len(address_history['C001']), 1)
        self.assertEqual(address_history['C001'][0]['address'], '123 Main St, Sydney NSW 2000')
        self.assertEqual(address_history['C001'][0]['end_date'], 'Present')
        
    def test_address_change_detection(self):
        """Test that address changes are properly detected and tracked."""
        # First upload - create customer with initial address
        customers_df1 = pd.DataFrame({
            'customer_id': ['C001'],
            'name': ['John Doe'],
            'email': ['john@example.com'],
            'dob': ['1990-01-01'],
            'address': ['123 Main St, Sydney NSW 2000']
        })
        
        transactions_df = pd.DataFrame()
        products_df = pd.DataFrame()
        
        # Store initial data
        store_data_to_db(transactions_df, customers_df1, products_df)
        
        # Verify initial address
        initial_address = CustomerAddress.query.filter_by(customer_id='C001', end_date=None).first()
        self.assertIsNotNone(initial_address)
        self.assertEqual(initial_address.address, '123 Main St, Sydney NSW 2000')
        
        # Second upload - same customer with new address
        customers_df2 = pd.DataFrame({
            'customer_id': ['C001'],
            'name': ['John Doe'],
            'email': ['john@example.com'],
            'dob': ['1990-01-01'],
            'address': ['456 Oak Ave, Melbourne VIC 3000']
        })
        
        # Store updated data
        address_history = store_data_to_db(transactions_df, customers_df2, products_df)
        
        # Verify old address was end-dated
        old_address = CustomerAddress.query.filter_by(
            customer_id='C001', 
            address='123 Main St, Sydney NSW 2000'
        ).first()
        self.assertIsNotNone(old_address)
        self.assertIsNotNone(old_address.end_date)
        
        # Verify new address was created
        new_address = CustomerAddress.query.filter_by(
            customer_id='C001', 
            end_date=None
        ).first()
        self.assertIsNotNone(new_address)
        self.assertEqual(new_address.address, '456 Oak Ave, Melbourne VIC 3000')
        
        # Verify address history shows both addresses
        self.assertIn('C001', address_history)
        self.assertEqual(len(address_history['C001']), 2)
        
        # History should be ordered by start_date desc (newest first)
        self.assertEqual(address_history['C001'][0]['address'], '456 Oak Ave, Melbourne VIC 3000')
        self.assertEqual(address_history['C001'][0]['end_date'], 'Present')
        self.assertEqual(address_history['C001'][1]['address'], '123 Main St, Sydney NSW 2000')
        self.assertNotEqual(address_history['C001'][1]['end_date'], 'Present')
        
    def test_no_address_change_when_same(self):
        """Test that no new address record is created when address hasn't changed."""
        # First upload
        customers_df = pd.DataFrame({
            'customer_id': ['C001'],
            'name': ['John Doe'],
            'email': ['john@example.com'],
            'dob': ['1990-01-01'],
            'address': ['123 Main St, Sydney NSW 2000']
        })
        
        transactions_df = pd.DataFrame()
        products_df = pd.DataFrame()
        
        # Store initial data
        store_data_to_db(transactions_df, customers_df, products_df)
        
        # Count initial addresses
        initial_count = CustomerAddress.query.filter_by(customer_id='C001').count()
        
        # Second upload with same address
        address_history = store_data_to_db(transactions_df, customers_df, products_df)
        
        # Count addresses after second upload
        final_count = CustomerAddress.query.filter_by(customer_id='C001').count()
        
        # Should still have only one address record
        self.assertEqual(initial_count, final_count)
        self.assertEqual(final_count, 1)
        
        # Verify address history shows only one address
        self.assertIn('C001', address_history)
        self.assertEqual(len(address_history['C001']), 1)
        self.assertEqual(address_history['C001'][0]['end_date'], 'Present')
        
    
        """Test address history tracking for multiple customers."""
        # Create test data with multiple customers
        customers_df = pd.DataFrame({
            'customer_id': ['C001', 'C002'],
            'name': ['John Doe', 'Jane Smith'],
            'email': ['john@example.com', 'jane@example.com'],
            'dob': ['1990-01-01', '1985-05-15'],
            'address': ['123 Main St, Sydney NSW 2000', '789 Pine Rd, Brisbane QLD 4000']
        })
        
        transactions_df = pd.DataFrame()
        products_df = pd.DataFrame()
        
        # Store data
        address_history = store_data_to_db(transactions_df, customers_df, products_df)
        
        # Verify both customers have address history
        self.assertIn('C001', address_history)
        self.assertIn('C002', address_history)
        
        # Verify each customer has one address record
        self.assertEqual(len(address_history['C001']), 1)
        self.assertEqual(len(address_history['C002']), 1)
        
        # Verify addresses are correct
        self.assertEqual(address_history['C001'][0]['address'], '123 Main St, Sydney NSW 2000')
        self.assertEqual(address_history['C002'][0]['address'], '789 Pine Rd, Brisbane QLD 4000')
        
    
        """Test that address history dates are properly formatted."""
        customers_df = pd.DataFrame({
            'customer_id': ['C001'],
            'name': ['John Doe'],
            'email': ['john@example.com'],
            'dob': ['1990-01-01'],
            'address': ['123 Main St, Sydney NSW 2000']
        })
        
        transactions_df = pd.DataFrame()
        products_df = pd.DataFrame()
        
        # Store data
        address_history = store_data_to_db(transactions_df, customers_df, products_df)
        
        # Verify date format
        start_date = address_history['C001'][0]['start_date']
        end_date = address_history['C001'][0]['end_date']
        
        # start_date should be in YYYY-MM-DD HH:MM:SS format
        try:
            datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            self.fail(f"start_date '{start_date}' is not in expected format")
            
        # end_date should be 'Present' for active address
        self.assertEqual(end_date, 'Present')


if __name__ == '__main__':
    unittest.main()
