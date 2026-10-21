"""
uv run code/generate_data.py
uv run code/generate_data.py 10000
"""

from pathlib import Path
import argparse
from index_core import generate_data
from getpass import getpass
import psycopg

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema.sql"

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "hash_index_lab",
    "user": "postgres",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate and load synthetic orders into PostgreSQL."
    )
    parser.add_argument(
        "row_count",
        nargs="?",
        type=int,
        default=200,
        help="Number of orders to generate (default: 200)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.row_count <= 0:
        raise SystemExit("row_count must be a positive integer")

    row_count = args.row_count

    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    orders = generate_data(order_count=row_count)

    password = getpass("PostgreSQL password: ")

    with psycopg.connect(**DB_CONFIG, password=password) as conn:
        with conn.cursor() as cur:
            cur.execute(schema)

            # Clear existing rows while preserving the table and its indexes.
            cur.execute("DELETE FROM orders")

            cur.executemany(
                """
                INSERT INTO orders (
                    order_id,
                    customer_id,
                    created_at,
                    status,
                    description,
                    total_amount
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                orders,
            )

            cur.execute("ANALYZE orders")
            cur.execute("SELECT COUNT(*) FROM orders")
            loaded_count = cur.fetchone()[0]

    print(f"Loaded {loaded_count} orders into hash_index_lab.orders.")


if __name__ == "__main__":
    main()
