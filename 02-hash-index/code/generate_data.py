"""
uv run code/generate_data.py
"""

from pathlib import Path
from index_core import generate_data
from getpass import getpass
import psycopg

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "hash_index_lab",
    "user": "postgres",
}


def main():
    schema_path = Path(__file__).resolve().parent.parent / "schema.sql"
    schema = schema_path.read_text(encoding="utf-8")
    orders = generate_data()

    password = getpass("PostgreSQL password: ")

    with psycopg.connect(**DB_CONFIG, password=password) as conn:
        with conn.cursor() as cur:
            cur.execute(schema)

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
                [
                    (
                        order_id,
                        customer_id,
                        created_at,
                        status,
                        description,
                        total_amount,
                    )
                    for (
                        order_id,
                        customer_id,
                        created_at,
                        status,
                        description,
                        total_amount,
                    ) in orders
                ],
            )

            cur.execute("SELECT COUNT(*) FROM orders")
            row_count = cur.fetchone()[0]

    print(f"Loaded {row_count} orders into hash_index_lab.orders.")


if __name__ == "__main__":
    main()
