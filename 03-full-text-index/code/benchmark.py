"""
uv run code/benchmark.py
"""

from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "orders.db"

QUERY = """
SELECT order_id, description
FROM orders
WHERE description LIKE ?
"""

SEARCH_PATTERN = "%keyboard%"

FTS_QUERY = """
SELECT rowid, description
FROM orders_fts
WHERE orders_fts MATCH ?
"""

FTS_SEARCH_TERM = "keyboard"


def print_baseline_results(orders, baseline_plan):
    print(f"Baseline matching rows: {len(orders)}")

    print("\nBaseline query results:")
    for row in orders:
        print(row)

    print("\nBaseline query plan:")
    for row in baseline_plan:
        print(row)


def print_fts_results(fts_orders, fts_plan):
    print("\n" + "-" * 30)
    print(f"FTS matching rows: {len(fts_orders)}")

    print("\nFTS query results:")
    for row in fts_orders:
        print(row)

    print("\nFTS query plan:")
    for row in fts_plan:
        print(row)


def main():
    with sqlite3.connect(DB_PATH) as conn:
        orders = conn.execute(QUERY, (SEARCH_PATTERN,)).fetchall()

        baseline_plan = conn.execute(
            f"EXPLAIN QUERY PLAN {QUERY}",
            (SEARCH_PATTERN,),
        ).fetchall()

        fts_orders = conn.execute(
            FTS_QUERY,
            (FTS_SEARCH_TERM,),
        ).fetchall()

        fts_plan = conn.execute(
            f"EXPLAIN QUERY PLAN {FTS_QUERY}",
            (FTS_SEARCH_TERM,),
        ).fetchall()

    print_baseline_results(orders, baseline_plan)
    print_fts_results(fts_orders, fts_plan)


if __name__ == "__main__":
    main()
