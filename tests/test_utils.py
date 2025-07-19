"""
Unit tests for utility functions.
Run with: python -m pytest tests/ or python -m unittest discover tests/
"""

import unittest
import tempfile
import os
import pandas as pd
from unittest.mock import patch, mock_open

# Add the app directory to the path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from utils import validate_excel_file


class TestValidateExcelFile(unittest.TestCase):
    """Test cases for the validate_excel_file function."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up after each test method."""
        # Clean up temp files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def create_test_excel_file(self, filename, sheets_data):
        """Helper method to create test Excel files."""
        filepath = os.path.join(self.temp_dir, filename)
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            for sheet_name, data in sheets_data.items():
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        return filepath

    def test_valid_file_passes_validation(self):
        """Test that a properly formatted file passes validation."""
        valid_data = {
            'Transactions': {
                'transaction_id': ['TXN001'],
                'customer_id': ['C001'],
                'transaction_date': ['2023-01-01'],
                'product_code': ['P001'],
                'amount': [100.0],
                'payment_type': ['Credit Card']
            },
            'Customers': {
                'customer_id-name-email-dob-address-created-date': ['C001_John_john@test.com_1990-01-01_123 Main St_2023-01-01']
            },
            'Products': {
                'product_code': ['P001'],
                'product_name': ['Test Product'],
                'category': ['Test Category'],
                'unit_price': [50.0]
            }
        }
        
        filepath = self.create_test_excel_file('valid.xlsx', valid_data)
        is_valid, message = validate_excel_file(filepath)
        
        self.assertTrue(is_valid)
        self.assertEqual(message, "File validated successfully.")

    def test_missing_sheet_fails(self):
        """Test that missing required sheet causes validation to fail."""
        invalid_data = {
            'Customers': {
                'customer_id-name-email-dob-address-created-date': ['C001_John_john@test.com_1990-01-01_123 Main St_2023-01-01']
            },
            'Products': {
                'product_code': ['P001'],
                'product_name': ['Test Product'],
                'category': ['Test Category'],
                'unit_price': [50.0]
            }
            # Missing Transactions sheet
        }
        
        filepath = self.create_test_excel_file('missing_sheet.xlsx', invalid_data)
        is_valid, message = validate_excel_file(filepath)
        
        self.assertFalse(is_valid)
        self.assertIn("Missing required sheet", message)

    def test_missing_column_fails(self):
        """Test that missing required column causes validation to fail."""
        invalid_data = {
            'Transactions': {
                'transaction_id': ['TXN001'],
                'customer_id': ['C001']
                # Missing other required columns
            },
            'Customers': {
                'customer_id-name-email-dob-address-created-date': ['C001_John_john@test.com_1990-01-01_123 Main St_2023-01-01']
            },
            'Products': {
                'product_code': ['P001'],
                'product_name': ['Test Product'],
                'category': ['Test Category'],
                'unit_price': [50.0]
            }
        }
        
        filepath = self.create_test_excel_file('missing_column.xlsx', invalid_data)
        is_valid, message = validate_excel_file(filepath)
        
        self.assertFalse(is_valid)
        self.assertIn("Missing columns", message)

    def test_invalid_file_fails(self):
        """Test that invalid file causes validation to fail."""
        is_valid, message = validate_excel_file('/nonexistent/path/file.xlsx')
        
        self.assertFalse(is_valid)
        self.assertIn("Failed to read Excel file", message)


if __name__ == '__main__':
    unittest.main()
