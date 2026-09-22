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


def repeat_purchase_rate():
    return run_sql("""
    WITH order_counts AS (
        SELECT user_id, COUNT(*) AS n_order
        FROM orders
        WHERE status NOT IN ('cancelled')
        GROUP BY user_id
    )
    SELECT 
        COUNT(*) FILTER (WHERE n_order > 1)::float / COUNT(*) AS repeat_rate
    FROM order_counts;
    """)

def customer_lifetime_value_proxy():
    return run_sql("""
    SELECT user_id, 
        SUM(grand_total) AS total_spent,
        COUNT(*) AS orders
    FROM orders
    WHERE status NOT IN ('cancelled')
    GROUP BY user_id
    ORDER BY total_spent DESC;
    """)

def return_rate():
    return run_sql("""
    SELECT 
        COUNT(*) FILTER (WHERE status = 'returned')::float / COUNT(*) AS returned_rate
    FROM orders
    """)