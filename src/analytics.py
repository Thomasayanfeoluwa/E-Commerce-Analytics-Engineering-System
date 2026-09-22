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
        SELECT AVG(grand_total) AS aov
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

def product_ranking():
    return run_sql("""
        SELECT product_name, SUM(qty) AS unit_sold,
            SUM(qty * unit_price) AS revenue
        FROM order_items
        GROUP BY product_name
        ORDER BY revenue DESC;
        """)


def revenue_by_country():
    return run_sql("""
        SELECT 
            ship_country_code AS country_code,
            SUM(grand_total) AS revenue
        FROM orders 
        WHERE status <> 'cancelled'
        GROUP BY ship_country_code
        ORDER BY revenue DESC;
        """)

def retention():
    return run_sql("""
        WITH first_orders AS (
            SELECT user_id,
                MIN(DATE_TRUNC('month', created_at)) AS cohort_month
            FROM orders
            WHERE status <> 'cancelled'
            GROUP BY user_id
        ),
        activity AS (
            SELECT
                o.user_id,
                f.cohort_month,
                DATE_TRUNC('month', o.created_at) AS order_month
            FROM orders AS o
            JOIN first_orders AS f
                ON f.user_id = o.user_id
            WHERE o.status <> 'cancelled'
        )
        SELECT 
            cohort_month,
            order_month,
            COUNT (DISTINCT user_id) AS active_user
        FROM activity
        GROUP BY cohort_month, order_month
        ORDER BY cohort_month, order_month;
        """)

def first_to_second_purchase_interval():
    return run_sql("""
        WITH ranked AS (
            SELECT user_id, created_at,
                ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY created_at) AS rn
                FROM orders
                )
        SELECT AVG(r2.created_at - r1.created_at) AS average_interval
        FROM ranked r1
        JOIN ranked r2
            ON r1.user_id = r2.user_id
        WHERE r1.rn = 1 AND r2.rn = 2;
    """)

def top_product_by_category():
    return run_sql("""
    SELECT 
        c.name AS category,
        p.name AS product_name,
        SUM(oi.qty) AS units_sold
    FROM order_items AS oi
    JOIN product_variants AS v
        ON v.variant_id = oi.variant_id
    JOIN products AS p
        ON p.product_id = v.product_id
    JOIN categories AS c
        ON c.category_id = p.category_id
    GROUP BY c.name, p.name
    ORDER BY c.name, units_sold DESC;
    """)

def customer_inactivity(days: int = 90):
    return run_sql(f"""
    SELECT
        user_id,
        MAX(ordered_at) AS last_order
    FROM orders
    WHERE status NOT IN ('cancelled')
    GROUP BY user_id
    HAVING MAX(ordered_at) < NOW() - INTERVAL '{days} days';
    """)