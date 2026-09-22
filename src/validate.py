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
            o.grand_total -
            )
                
    """)