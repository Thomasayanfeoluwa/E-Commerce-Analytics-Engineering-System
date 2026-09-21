from src.db import run_sql

def monthly_revenue():
    return run_sql("""
    SELECT DATE_TRUNC('month', ordered_at) AS month,
        SUM(grand_total) AS revenue
    FROM orders
    WHERE status NOT IN ('cancelled')
    GROUP BY 1
    ORDER BY 1;
    """)