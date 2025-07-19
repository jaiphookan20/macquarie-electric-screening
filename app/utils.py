# app/utils.py

import pandas as pd

EXPECTED_SHEETS = {
    'Transactions': ['transaction_id', 'customer_id', 'transaction_date', 'product_code', 'amount', 'payment_type'],
    'Customers': ['customer_id-name-email-dob-address-created-date'],
    'Products': ['product_code', 'product_name', 'category', 'unit_price']
}

def validate_excel_file(filepath):
    """Validate the structure and content of the uploaded Excel file."""
    try:
        xls = pd.ExcelFile(filepath)
    except Exception as e:
        return False, f"Failed to read Excel file: {e}"

    # Check for required sheets
    sheet_names = xls.sheet_names
    for sheet in EXPECTED_SHEETS:
        if sheet not in sheet_names:
            return False, f"Missing required sheet: {sheet}"

    # Check for required columns in each sheet
    for sheet, expected_columns in EXPECTED_SHEETS.items():
        try:
            df = pd.read_excel(xls, sheet_name=sheet)
            if not all(col in df.columns for col in expected_columns):
                return False, f"Missing columns in {sheet} sheet. Expected: {expected_columns}"
        except Exception as e:
            return False, f"Failed to read or validate sheet {sheet}: {e}"

    return True, "File validated successfully."
