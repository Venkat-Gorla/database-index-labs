"""
"""

from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "orders.db"

QUERY = """
SELECT order_id, description
FROM orders
WHERE description LIKE '%keyboard%'
"""


def main():
    with sqlite3.connect(DB_PATH) as conn:
        orders = conn.execute(QUERY).fetchall()

        plan = conn.execute(
            "EXPLAIN QUERY PLAN " + QUERY
        ).fetchall()

    print(f"Matching rows: {len(orders)}")

    print("\nBaseline query results:")
    for row in orders:
        print(row)

    print("\nQuery plan:")
    for row in plan:
        print(row)


if __name__ == "__main__":
    main()
