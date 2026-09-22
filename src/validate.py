from src.db import run_sql

def check_order_total_match_items():
    mismatches = run_sql("""
        SELECT 
            o.order_id,
            o.grand_total,
            SUM(oi.line_total) AS items_total
            o.discount_total,
            o.shipping_total,
            SUM(oi.line_total)
                - o.discount_total
                + o.shipping_total AS computed_total
        FROM orders AS o
        JOIN order_items AS oi
            ON oi.order_id = o.order_id
        GROUP BY
            o.order_id,
            o.grand_total,
            o.discount_total,
            o.shipping_total
        HAVING ABS(
            o.grand_total - (
                SUM(oi.line_total)
                - o.discount_total
                + o.shipping_total
            )
        ) > 0.01;
    """)
    return mismatches

def check_negative_values():
    return run_sql("""
        SELECT *
        FROM order_items
        WHERE qty < 0 OR unit_price < 0;
    """)

def check_null_foreign_keys():
    return run_sql("""
    SELECT *
    FROM orders
    WHERE user_id IS NULL;
    """)


def check_sanity_date():
    return run_sql("""
    SELECT *
    FROM orders
    WHERE created_at > NOW() OR created_at < '2015-01-01';
    """)

def run_all_checks():
    result = {
        ""
    }