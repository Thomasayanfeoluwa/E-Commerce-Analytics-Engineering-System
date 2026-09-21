from src.db import run_sql

def monthly_revenue():
    return run_sql("""
    SELECT DATA_TRUNC('month', 'created_at') AS month,
        SUM('total') AS revenue
    FROM orders
    GROUP BY 1
    ORDER BY 1
    """)