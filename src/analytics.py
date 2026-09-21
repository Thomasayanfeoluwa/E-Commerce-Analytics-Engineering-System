from src.db import run_sql

def monthly_revenue():
    return run_sql("""
    SELECT 
        DATE_TRUNC('month', ordered_at) AS month,
        SUM(grand_total) AS revenue
    FROM orders
    WHERE status != 'cancelled' 
    GROUP BY 1
    ORDER BY 1;
    """)


def average_order_value():
    return run_sql("""
    SELECT AVG(grand_total)
    FROM orders
    WHERE status <> 'cancelled'
    ORDER BY grand_total;
    """)

def repeated_purchase_rate():
    return run_sql("""
    WITH order_count AS (
    SELECT
        user_id, COUNT(*) AS n_orders
    FROM orders
    WHERE status NOT IN ('cancelled')
    GROUP BY user_id
    )
    SELECT
        COUNT(*) FILTER (WHERE n_orders > 1)::float / COUNT(*) AS repeated_rate
    FROM orders;
    """)