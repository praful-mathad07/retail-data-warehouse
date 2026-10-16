# Retail Data Warehouse & Sales Analytics

A retail analytics project built using PostgreSQL, Python, SQL, and Power BI to organize sales data, automate data loading, and analyze revenue and profitability.

## Project Overview

This project demonstrates an end-to-end retail data analytics workflow, from storing sales transactions in a relational database to generating business insights through a Power BI dashboard.

## Tech Stack

- **Database:** PostgreSQL
- **Programming:** Python
- **Database connectivity:** Psycopg
- **Data ingestion:** Python CSV processing
- **Analytics:** SQL and DAX
- **Visualization:** Power BI
- **Configuration:** Python dotenv

## Project Structure

```text
retail-data-warehouse/
├── data/
│   ├── customers.csv
│   ├── products.csv
│   └── sales.csv
├── scripts/
│   └── load_data.py
├── .gitignore
└── README.md
```

## Database Design

The PostgreSQL database uses a dimensional model with four tables:

- `dim_product` — product details, categories, costs, and prices
- `dim_customer` — customer details, cities, and regions
- `dim_date` — calendar attributes for date-based analysis
- `fact_sales` — sales transactions, quantities, and financial values

## Python ETL Pipeline

The Python pipeline:

1. Reads sales transactions from CSV files.
2. Connects to PostgreSQL using environment-based configuration.
3. Looks up products, customers, and dates.
4. Validates transaction details and positive quantities.
5. Inserts new transactions while skipping duplicate order IDs.

## Key Performance Indicators

The Power BI dashboard includes:

- Total Revenue
- Total Profit
- Units Sold
- Total Orders
- Revenue by Product Category
- Monthly Revenue Trend
- Revenue by Product

## Sample Results

Based on the current sample dataset:

| Metric        |   Result |
| ------------- | -------: |
| Total Revenue | ₹267,500 |
| Total Profit  |  ₹79,500 |
| Units Sold    |       20 |
| Total Orders  |       10 |

These results describe the project's sample data, not real-world retail performance.

## Run the Project

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Git Bash for Windows:

```bash
source .venv/Scripts/activate
```

### 2. Install dependencies

```bash
pip install "psycopg[binary]" python-dotenv
```

### 3. Configure database credentials

Create a `.env` file in the project root:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retail_dw
DB_USER=postgres
DB_PASSWORD=your_local_postgres_password
```

Replace the password placeholder with your own local PostgreSQL password. Never commit the `.env` file.

### 4. Prepare the database

Create the database and the four tables described above, and load the product, customer, and date dimension data into PostgreSQL before running the sales pipeline.

### 5. Run the pipeline

```bash
python scripts/load_data.py
```

The script reports how many transactions were inserted and how many were skipped.

## Future Improvements

- Add automated database schema and dimension-table setup scripts.
- Expand the sample dataset to support richer analysis.
- Add data-quality reports and automated tests.
- Include Power BI dashboard screenshots and SQL analytics queries.

## Author

**Praful Mathad**
