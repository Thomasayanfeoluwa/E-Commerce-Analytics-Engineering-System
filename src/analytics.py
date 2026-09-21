from src.db import run_sql

def monthly_revenue():
    return run_sql("""
    SELECT DATE_TRUNC('month', 'created_at')
        SUM(total) AS revenue
    FROM ecommerce
    WHERE status NOT IN ('cancelled')
    GROUP BY 1
    ORDER BY 1;
    """)