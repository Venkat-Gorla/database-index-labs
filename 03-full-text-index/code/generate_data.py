"""
uv run code/generate_data.py
"""

from pathlib import Path
import sqlite3
from index_core import generate_data

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "orders.db"
SCHEMA_PATH = ROOT / "schema.sql"


def main():
    if DB_PATH.exists():
        raise FileExistsError(
            f"Database already exists: {DB_PATH}. "
            "Remove it explicitly before regenerating the dataset."
        )

    orders = generate_data()

    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

        conn.executemany(
            """
            INSERT INTO orders (
                order_id,
                customer_id,
                created_at,
                status,
                description,
                total_amount
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            orders,
        )

    print(f"Created database: {DB_PATH}")
    print(f"Inserted {len(orders)} orders.")


if __name__ == "__main__":
    main()
