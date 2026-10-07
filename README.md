# E-Commerce Analytics Engineering System

## Overview

This project is a hands-on analytics engineering and SQL-driven business intelligence workflow for an e-commerce dataset. The goal is to model a realistic online retail database, validate data quality, compute core commerce KPIs, and produce exported datasets and charts for business analysis.

It is not a full customer-facing web application or a production SaaS product. Instead, it is a local, data-first project that uses PostgreSQL, SQLAlchemy, Python, Pandas, and Matplotlib to create a reproducible analytics pipeline from raw database tables to processed KPI outputs.

The repository combines:

- a PostgreSQL sample e-commerce schema
- SQL-based data validation checks
- reusable analytics queries for revenue and customer behavior
- chart generation for reporting
- CSV exports for downstream analysis
- automated tests for core KPI and validation logic

## Purpose

The project was built to answer practical e-commerce questions such as:

- How much revenue is generated each month?
- What is the average order value (AOV)?
- Which products drive the most revenue?
- How often do customers make repeat purchases?
- Are there data integrity issues in orders or transactions?
- Are there signs of inactive customers or malformed records?

Rather than focusing on a frontend or deployment, the project focuses on the analytics engineering pipeline: raw database -> validity checks -> metrics -> outputs.

## What the project does

At a high level, the system does the following:

1. Creates or connects to a PostgreSQL e-commerce database
2. Loads the schema from `data/raw/ecommerce.sql`
3. Connects Python to the database through `sqlalchemy.create_engine`
4. Executes SQL queries against the database using Pandas
5. Validates data quality and integrity rules
6. Calculates business metrics such as revenue, AOV, repeat purchase rate, retention, and product performance
7. Exports query results to CSV files in `data/processed/`
8. Generates visual reports under `reports/figures/`
9. Offers test coverage for the main analytics and validation functions

## Chronological project flow

### 1. Database setup and schema initialization

The project begins with a PostgreSQL e-commerce schema supplied in `data/raw/ecommerce.sql`.

This SQL file defines a modern online retail data model with tables including:

- `users`
- `addresses`
- `categories`
- `products`
- `product_variants`
- `product_images`
- `inventory`
- `carriers`
- `carts`
- `cart_items`
- `orders`
- `order_items`
- additional fulfillment and transaction-related tables

The notebook `notebooks/01_sql_analytics.ipynb` explicitly documents the setup approach:

```bash
createdb ecommerce
psql -d ecommerce -v ON_ERROR_STOP=1 -f ecommerce.sql
```

This indicates the project expects a PostgreSQL instance and a local database named `ecommerce`.

### 2. Application connection to PostgreSQL

The project uses a simple environment-driven database connection pattern.

- `.env.example` contains:

```env
DATABASE_URL=******localhost:5432/ecommerce
```

- `src/db.py` loads environment variables via `python-dotenv`
- it creates a SQLAlchemy engine from `DATABASE_URL`
- it exposes `run_sql(query)` which runs a SQL statement and returns a Pandas DataFrame

This makes the analysis layer SQL-first and easy to query without custom database client code.

### 3. Data quality validation

The project includes a validation module in `src/validate.py`.

This module checks that the transactional dataset is internally consistent before using it for product analytics.

The validation logic includes:

- `check_order_total_match_items()`
  - verifies that each order total matches the expected subtotal minus discount plus shipping
- `check_negative_values()`
  - flags invalid negative quantities or unit prices in `order_items`
- `check_null_foreign_keys()`
  - checks for orders without a valid parent user
- `check_sanity_date()`
  - finds dates that are impossible or out-of-range

The validation functions return DataFrames of offending records, and `run_all_checks()` prints pass/fail summaries.

This reflects an analytics engineering practice: data quality checks are part of the pipeline, not an afterthought.

### 4. Core analytics layer

The actual business logic is implemented in `src/analytics.py`.

The analytics functions are SQL queries against the PostgreSQL database and return DataFrames ready for export or visual exploration.

Key metrics include:

- `monthly_revenue()`
  - total revenue per month
- `average_order_value()`
  - overall average order value
- `repeat_purchase_rate()`
  - share of users with more than one order
- `customer_lifetime_value_proxy()`
  - total spend per user
- `return_rate()`
  - share of orders in a returned state
- `product_ranking()`
  - top products by quantity sold and revenue
- `revenue_by_country()`
  - revenue grouped by shipping country code
- `retention()`
  - customer cohort retention by cohort and order month
- `first_to_second_purchase_interval()`
  - average gap between first and second purchases
- `top_product_by_category()`
  - units sold by category and product
- `customer_inactivity(days=90)`
  - users whose last known order predates the threshold

These queries are classic e-commerce metrics used in analytics engineering and business reporting.

### 5. Automation and exports

The repository’s entry point is `main.py`.

It does the following:

```python
from src import analytics
analytics.monthly_revenue().to_csv("data/processed/monthly_revenue.csv", index=False)
analytics.average_order_value().to_csv("data/processed/aov.csv", index=False)
```

This means the project is designed to generate processed datasets automatically from the database. In other words, the pipeline is intentionally data-product oriented: metrics are turned into CSVs that can be used for dashboards, notebooks, or downstream workflows.

### 6. Visualization and reporting

The visualization layer is implemented in `src/charts.py`.

It creates plots for:

- monthly revenue trend
- top products by revenue

Generated outputs include:

- `reports/figures/monthly_revenue.png`
- `reports/figures/top_products.png`

These charts are simple but useful reports for stakeholders and for validating whether the underlying data and SQL logic look sensible.

### 7. Testing and quality assurance

The repository uses `pytest` with two test files:

- `tests/test_analytics.py`
- `tests/test_validate.py`

These tests check that:

- monthly revenue is non-empty and non-negative
- average order value is positive
- repeat purchase rate is bounded between 0 and 1
- product rankings are populated and sorted by revenue
- revenue by country has valid values
- retention has expected columns and positive activity counts
- no negative values, null foreign keys, or bad dates are present

This indicates the project is intended to be more than a one-off notebook—it is structured enough to have repeatable validation and regression checks.

## Project structure

```text
E-Commerce Analytics Engineering System/
├── .env.example
├── .gitignore
├── README.md
├── main.py
├── pyproject.toml
├── uv.lock
├── data/
│   ├── processed/
│   │   ├── aov.csv
│   │   └── monthly_revenue.csv
│   └── raw/
│       └── ecommerce.sql
├── notebooks/
│   └── 01_sql_analytics.ipynb
├── reports/
│   └── figures/
│       ├── monthly_revenue.png
│       └── top_products.png
├── SQLqueries/
│   └── analytics.sql
├── src/
│   ├── __init__.py
│   ├── analytics.py
│   ├── charts.py
│   ├── db.py
│   └── validate.py
├── tests/
│   ├── test_analytics.py
│   └── test_validate.py
└── .pytest_cache/
```

## Tools and technologies used

This project is built with a practical analytics stack:

- PostgreSQL as the data warehouse / source database
- SQL for data modeling and transformation logic
- Python 3.11+
- SQLAlchemy for database access
- Pandas for DataFrame work
- Matplotlib for reporting visuals
- `python-dotenv` for environment configuration
- `pytest` for automated verification
- Jupyter Notebook for exploratory SQL analysis

## Dependencies

From `pyproject.toml`, the project depends on:

- `pandas`
- `python-dotenv`
- `numpy`
- `matplotlib`
- `seaborn`
- `sqlalchemy`
- `psycopg[binary]`
- `pytest`
- `ipykernel`
- `tabulate`
- `python-dateutil>=2.9.0.post0`

This indicates the project is meant to run in a Python environment with PostgreSQL connectivity and typical analytics tooling installed.

## Setup instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd "E-Commerce Analytics Engineering System"
```

### 2. Create a PostgreSQL database

```bash
createdb ecommerce
psql -d ecommerce -v ON_ERROR_STOP=1 -f data/raw/ecommerce.sql
```

### 3. Configure environment variables

Copy the example file and set the database URL:

```bash
cp .env.example .env
```

Then update `.env` with your PostgreSQL connection string, matching your local host and database name.

### 4. Install dependencies

If you use `uv`:

```bash
uv sync
```

If you prefer `pip`:

```bash
pip install -e .
```

### 5. Run the analytics pipeline

```bash
python main.py
```

This creates processed CSV files in `data/processed/`.

### 6. Generate report charts

The plotting functions exist in `src/charts.py`, and they can be run as part of an analysis workflow or notebook session.

### 7. Run tests

```bash
pytest
```

## Current outputs in the repository

The repository already contains generated artifacts such as:

- `data/processed/monthly_revenue.csv`
- `data/processed/aov.csv`
- `reports/figures/monthly_revenue.png`
- `reports/figures/top_products.png`

These files show that the project has already been exercised to produce real revenue and reporting outputs.

## Important notes and truth about the repository

This repository is a realistic analytics engineering prototype, not a monolithic SaaS application.

A few important truths about the current state of the project:

- The main source of data is a PostgreSQL schema loaded from SQL, not a production cloud data warehouse.
- The project is primarily SQL + Python data processing rather than machine learning or a web app.
- The analytics are mostly descriptive business metrics and data quality checks.
- The `SQLqueries/analytics.sql` file currently contains only a minimal `SELECT` placeholder and is not yet a complete standalone query script.
- The project is designed for local analytical workflows and validation, not deployment to a production environment.

## Practical interpretation of the system

In practical terms, this project acts like a mini analytics engineering stack:

- raw database schema
- quality gates
- SQL KPI queries
- exported business data
- visual artifacts
- repeatable tests

This is exactly the kind of foundation a modern data team uses before building dashboards, BI layers, or more advanced predictive analytics.

## Summary

The E-Commerce Analytics Engineering System is a structured SQL and Python project for analyzing a realistic e-commerce dataset. It is built around PostgreSQL, data validation, KPI extraction, CSV exports, and visual reporting. The repository is a solid example of an analytics engineering workflow that turns raw transactional data into business insights and operational quality checks.
