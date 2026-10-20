"""
uv run code/generate_data.py
"""

from pathlib import Path
import random
import sqlite3
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "orders.db"
SCHEMA_PATH = ROOT / "schema.sql"

ORDER_COUNT = 200
CUSTOMER_COUNT = 20
RANDOM_SEED = 42

PRODUCTS = [
    "Wireless keyboard",
    "Blue running shoes",
    "Stainless steel bottle",
    "Cotton bedsheet set",
    "USB-C charging cable",
    "Ceramic coffee mug",
    "Laptop stand",
    "Travel backpack",
    "Desk lamp",
    "Notebook set",
]

STATUSES = ["pending", "shipped", "delivered", "cancelled"]


def generate_data():
    rng = random.Random(RANDOM_SEED)
    start = datetime(2025, 1, 1)

    orders = []

    for i in range(1, ORDER_COUNT + 1):
        created_at = start + timedelta(
            days=rng.randint(0, 179),
            minutes=rng.randint(0, 1439),
        )

        orders.append(
            (
                f"ORD-{i:03d}",
                f"CUST-{rng.randint(1, CUSTOMER_COUNT):03d}",
                created_at.isoformat(timespec="seconds"),
                rng.choice(STATUSES),
                f"{rng.choice(PRODUCTS)} - order {i:03d}",
                round(rng.uniform(10, 500), 2),
            )
        )

    return orders


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
