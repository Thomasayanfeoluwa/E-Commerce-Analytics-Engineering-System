from src.db import run_sql

def check_order_total_match_items():
    mismatches = run_sql("""
        SELECT 
            o.order_id,
            o.grand_total,
            o.subtotal,
            o.discount_total,
            o.shipping_total,
            o.subtotal
                - o.discount_total
                + o.shipping_total AS computed_total
        FROM orders AS o
        WHERE ABS(
            o.grand_total -
            (o.subtotal - o.discount_total + o.shipping_total)
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
    WHERE created_at > NOW()
        OR created_at < '2026-08-26';
    """)

def run_all_checks():
    results = {
        "order_totals_mismatch": check_order_total_match_items(),
        "negative_values": check_negative_values(),
        "null_fks": check_null_foreign_keys(),
        "bad_dates": check_sanity_date(),
    }

    for name, df in results.items():
        status = "PASS" if df.empty else f"FAIL ({len(df)} rows)"
        print(f"{name}: {status}")

    return results