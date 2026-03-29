# SQL Client Reporting System

## Overview
The SQL Client Reporting System is a lightweight, production-style reporting pipeline built on PostgreSQL and Python.  
It demonstrates how transactional data can be validated, aggregated, and exported into client-ready reports using SQL-first logic and minimal automation.

The project mirrors the type of reporting and validation work typically handled by a Software Associate or Data Engineer supporting business, finance, or operations teams.

---

## Business Context
Sales and finance stakeholders require:
- Consistent revenue reporting
- Visibility into top-performing customers
- Early detection of data issues such as failed payments or invalid transactions

This repository centralizes schema design, reporting queries, and validation logic to ensure that insights are **accurate, auditable, and reproducible**.

---

## System Architecture

### 1. Database Layer (PostgreSQL)
- Tables: `customers`, `orders`, `payments`
- Enforced via:
  - Primary and foreign keys
  - CHECK constraints for data integrity
  - Referential consistency between transactions

### 2. SQL Reporting Layer
- Monthly revenue aggregation
- Top customers by total spend
- Validation queries to detect:
  - Negative or zero-value orders
  - Failed or inconsistent payments

### 3. Python Automation Layer
- `db_connection.py`  
  Centralized PostgreSQL connection handling using environment variables.
- `data_validation.py`  
  Executes validation SQL and summarizes anomaly counts using pandas.
- `report_generator.py`  
  Orchestrates reporting queries and exports timestamped CSV files.

### 4. Reporting Outputs
- Reports are generated at runtime and written to the `reports/` directory.
- Output files are intentionally excluded from version control.

---

## Tech Stack
- PostgreSQL
- Python 3.x
- psycopg2
- pandas
- SQL
- Git & GitHub

---

## Local Setup & Execution

### 1. Install dependencies
```bash
pip install psycopg2 pandas
````

### 2. Initialize database schema and seed data

```bash
psql -f sql/schema.sql
psql -f sql/sample_data.sql
```

### 3. Configure environment variables

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=sql_reporting
export DB_USER=postgres
export DB_PASSWORD=postgres
```

### 4. Run the reporting pipeline

```bash
python -m python.report_generator
```

---

## Generated Reports

CSV files are created under `reports/` with UTC timestamps:

* `monthly_revenue_<timestamp>.csv`
  Monthly revenue aggregates used for KPI dashboards.
* `top_customers_<timestamp>.csv`
  Ranked customers by total spend.
* `validation_summary_<timestamp>.csv`
  Counts of invalid orders and failed payments for operational review.

---

## Git Workflow

* Logical commits reflect incremental development:

  * Schema definition
  * Sample data
  * Reporting queries
  * Validation logic
  * Automation scripts
* Runtime artifacts (`reports/`) are excluded from Git.
* The repository is designed for clarity, auditability, and easy onboarding.

---

## Notes

* No automated tests are included.
* To validate functionality, execute the report generator against a local PostgreSQL instance and review generated CSVs.

