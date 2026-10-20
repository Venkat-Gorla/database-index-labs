"""
uv run code/benchmark.py
"""

from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "orders.db"

CUSTOMER_ID = "CUST-007"

QUERY = """
SELECT order_id, customer_id, created_at, status, description, total_amount
FROM orders
WHERE customer_id = ?
ORDER BY created_at DESC
"""


def main():
    with sqlite3.connect(DB_PATH) as conn:
        plan = conn.execute(
            f"EXPLAIN QUERY PLAN {QUERY}",
            (CUSTOMER_ID,),
        ).fetchall()

        orders = conn.execute(QUERY, (CUSTOMER_ID,)).fetchall()

    print(f"Customer: {CUSTOMER_ID}")
    print(f"Matching orders: {len(orders)}")

    print("\nQuery plan:")
    for row in plan:
        print(row)

    print("\nMatching orders:")
    for order in orders:
        print(order)


if __name__ == "__main__":
    main()
