# app/models.py

from . import db

class UploadLog(db.Model):
    """Model to log file uploads."""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    upload_time = db.Column(db.DateTime, server_default=db.func.now())
    transaction_rows = db.Column(db.Integer, nullable=False)
    customer_rows = db.Column(db.Integer, nullable=False)
    product_rows = db.Column(db.Integer, nullable=False)

class Customer(db.Model):
    """Model for storing customer data."""
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)

class CustomerAddress(db.Model):
    """Model for storing customer address history."""
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(10), db.ForeignKey('customer.id'), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    start_date = db.Column(db.DateTime, server_default=db.func.now())
    end_date = db.Column(db.DateTime)

class Product(db.Model):
    """Model for storing product data."""
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

class Transaction(db.Model):
    """Model for storing transaction data."""
    id = db.Column(db.String(10), primary_key=True)
    customer_id = db.Column(db.String(10), db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.String(10), db.ForeignKey('product.id'), nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_type = db.Column(db.String(50), nullable=False)
