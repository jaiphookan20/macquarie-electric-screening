# Pre-Interview Screening Test
Welcome and thanks for your interest in joining Macquarie Electric!
We’re really excited to have you move forward in our hiring process. Before the interview, we’d
love for you to take a quick screening test. Please take your time to read through the instructions
carefully. We’re looking forward to seeing how you tackle this!

## Question
You're working with three datasets: customers, their transactions, and a product catalog. The goal
is to build a complete pipeline; from uploading the data to generating reports—that helps make
sense of all this information.

# Phase 1: Data Upload and Validation
### 1. A Simple Web App
Create a simple python Flask-based web application where users can upload an Excel file
containing all three sheets: Transactions, Customers, and Products.

### 2. File Validation
Once the file is uploaded, check that it’s structured correctly and contains the expected
data.

# Phase 2: Data Processing and Analysis

### 3. Data Processing with Pandas
After validation, use Pandas to:
a. Detect changes in customer addresses over time and keep a history of those
changes.
b. Calculate total transaction amount of each customer for each product category.
c. Identify the top spender in each category.
d. Rank all customers based on their total purchase value across all products.

# Phase 3: Data Enrichment and Storage
### 4. Geolocation Enrichment
Use any external API to fetch latitude and longitude for each unique customer address.
Add this location data to the customer records.
Note: It’s okay if fetched geolocation is not entirely accurate, since the addresses in the
dataset are not accurate.

### 5. Logging Uploads
Save metadata about each upload (i.e. upload timestamp, file name, and row count of
each sheet) into SQLite database for maintaining a log.

### 6. Downloadable Output
Let users download the cleaned and processed Excel file with different sheets.

# Phase 4: Reporting
### 7. Summary Report
Create a short Word document summarizing the entire process and key insights.

## Pre-Interview Screening Test
Submission Instructions
Please submit your completed pre-screening test as either:
• A ZIP file containing your project, or
• A Git repository link
You may choose whichever format is more convenient for you. Once ready, please email your
submission back to us.