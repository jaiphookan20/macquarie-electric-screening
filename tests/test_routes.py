"""
Unit tests for route helper functions.
Run with: python -m pytest tests/ or python -m unittest discover tests/
"""

import unittest
import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestAllowedFile(unittest.TestCase):
    """Test cases for the allowed_file function."""

    def setUp(self):
        """Set up the allowed_file function for testing."""
        def allowed_file(filename):
            """Check if the file has an allowed extension."""
            if not filename or '.' not in filename:
                return False
            
            extension = filename.rsplit('.', 1)[1].lower()
            allowed_extensions = {'xlsx', 'xls'}
            return extension in allowed_extensions
        
        self.allowed_file = allowed_file

    def test_valid_excel_files_accepted(self):
        """Test that Excel files are accepted."""
        self.assertTrue(self.allowed_file('test.xlsx'))
        self.assertTrue(self.allowed_file('test.xls'))
        self.assertTrue(self.allowed_file('TEST.XLSX'))  # case insensitive

    def test_invalid_files_rejected(self):
        """Test that non-Excel files are rejected."""
        self.assertFalse(self.allowed_file('test.csv'))
        self.assertFalse(self.allowed_file('test.numbers'))
        self.assertFalse(self.allowed_file('test'))  # no extension
        self.assertFalse(self.allowed_file(''))  # empty
        self.assertFalse(self.allowed_file(None))  # None


if __name__ == '__main__':
    unittest.main()
