# Macquarie Electric - Pre-Interview Screening Test

This project is a Python-based web application for uploading, processing, and analyzing customer transaction data from an Excel file.

## Project Structure

```
macquarie-electric-screening/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── services.py
│   ├── templates/
│   │   └── index.html
│   └── utils.py
├── instance/
│   └── app.db
├── venv/
├── run.py
├── requirements.txt
└── README.md
```

## Implementation Plan

The project is divided into four phases, each implemented in its own Git branch.

### Branch: `project-setup`

*   **Task 1: Initialize Project Structure**: Create the directories and empty files.
*   **Task 2: Setup Virtual Environment & Dependencies**: Create a `venv` and a `requirements.txt` file with `Flask`, `Flask-SQLAlchemy`, `pandas`, `openpyxl`, `geopy`, and `python-dotenv`.
*   **Task 3: Basic Flask App**: Set up a minimal Flask application.
*   **Task 4: Initialize Git**: Initialize the repository and make the initial commit.

### Branch: `upload-validation` (Phase 1)

*   **Task 1: Define Data Models**: Create SQLAlchemy models for `UploadLog`, `Customer`, `CustomerAddress`, `Product`, and `Transaction`.
*   **Task 2: Create Upload UI**: Develop a simple `index.html` for file uploads.
*   **Task 3: Implement Upload Route**: Create a `/upload` endpoint to handle file submissions.
*   **Task 4: Implement File Validation**: Create a utility function to validate the uploaded Excel file's structure and content.

### Branch: `processing-analysis` (Phase 2)

*   **Task 1: Implement Data Loading**: Load data from the validated Excel file into Pandas DataFrames.
*   **Task 2: Address Change Detection**: Identify and record changes in customer addresses.
*   **Task 3: Perform Data Analysis**:
    *   Calculate total spending per customer per product category.
    *   Identify the top spender in each category.
    *   Rank customers by total purchase value.
*   **Task 4: Store Processed Data**: Save the results to the SQLite database.

### Branch: `enrichment-storage` (Phase 3)

*   **Task 1: Geolocation Enrichment**: Use `geopy` to fetch coordinates for unique customer addresses.
*   **Task 2: Logging Uploads**: Log metadata for each successful upload.
*   **Task 3: Implement Downloadable Output**: Create an endpoint to download the processed data as an Excel file.

### Branch: `reporting` (Phase 4)

*   **Task 1: Summary Report Endpoint**: Create a `/report/summary` endpoint to show total sales per product category.
*   **Task 2: Detailed Report Endpoint**: Create a `/report/customer/<customer_id>` endpoint to show a customer's transaction history.
