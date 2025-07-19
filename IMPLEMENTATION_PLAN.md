# Implementation Plan

This document outlines the tasks for each phase of the project. Completed tasks are marked with `[x]`.

## Project Setup
- [x] Initialize project structure (directories and files)
- [x] Set up virtual environment
- [x] Create `requirements.txt` and install dependencies
- [x] Configure a basic Flask application
- [x] Initialize Git repository

## Phase 1: Data Upload and Validation (`upload-validation` branch)
- [x] Define SQLAlchemy data models (`UploadLog`, `Customer`, `Product`, etc.)
- [x] Create a simple HTML interface for file uploads
- [x] Implement a Flask route to handle file uploads
- [x] Implement file validation logic:
  - [x] Check for correct file type (`.xlsx` and `.xls`)
  - [x] Check for the presence of `Transactions`, `Customers`, and `Products` sheets
  - [x] Check for correct column headers in each sheet (including `unit_price`)
- [x] Add comprehensive error handling for all upload scenarios
- [x] Create and run validation tests to ensure correctness
- [x] **Phase 1 Complete and Ready for Commit**

## Phase 2: Data Processing and Analysis (`processing-analysis` branch)
- [ ] **Task 1: Data Loading & Cleaning**
  - [ ] Create a service function to load Excel data into Pandas DataFrames.
  - [ ] Clean and parse the `Customers` sheet data from its single-column format.
- [ ] **Task 2: Data Processing**
  - [ ] Implement logic to detect and store the history of customer address changes.
  - [ ] Persist core data (customers, products, transactions) to the SQLite database.
- [ ] **Task 3: Data Analysis**
  - [ ] Calculate the total transaction amount for each customer per product category.
  - [ ] Identify the top spender in each category.
  - [ ] Rank all customers based on their total purchase value.

## Phase 3: Data Enrichment and Storage (`enrichment-storage` branch)
- [ ] **Task 1: Geolocation Enrichment**
  - [ ] Create a utility function to fetch latitude and longitude for each unique customer address using an external API (`geopy`).
  - [ ] Add the fetched location data to the customer address records in the database.
- [ ] **Task 2: Logging Uploads**
  - [ ] After successful processing, save metadata (filename, timestamp, row counts) to the `UploadLog` table.
- [ ] **Task 3: Downloadable Output**
  - [ ] Create a new route (`/download/<upload_id>`).
  - [ ] Implement the logic to generate a processed Excel file with different sheets for the analysis results.

## Phase 4: Reporting (`reporting` branch)
- [ ] **Task 1: Summary Report**
  - [ ] Create a `/report/summary` endpoint.
  - [ ] Display the total sales per product category.
- [ ] **Task 2: Detailed Customer Report**
  - [ ] Create a `/report/customer/<customer_id>` endpoint.
  - [ ] Display a detailed transaction history for a specific customer.
