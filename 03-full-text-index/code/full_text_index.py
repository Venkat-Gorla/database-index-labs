"""
Manage the SQLite FTS5 full-text index.

uv run code/full_text_index.py add
uv run code/full_text_index.py remove
"""

from pathlib import Path
import argparse
import sqlite3

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "orders.db"
FTS_TABLE = "orders_fts"


def add_index(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE VIRTUAL TABLE orders_fts USING fts5(
            description,
            content='orders',
            content_rowid='rowid'
        )
        """
    )
    conn.execute(
        "INSERT INTO orders_fts(orders_fts) VALUES ('rebuild')"
    )


def remove_index(conn: sqlite3.Connection) -> None:
    conn.execute("DROP TABLE orders_fts")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Add or remove the SQLite FTS5 index."
    )
    parser.add_argument("action", choices=("add", "remove"))
    return parser.parse_args()


def main():
    args = parse_args()

    with sqlite3.connect(DB_PATH) as conn:
        if args.action == "add":
            add_index(conn)
            print("Created and populated the FTS5 index.")
        else:
            remove_index(conn)
            print("Removed the FTS5 index.")


if __name__ == "__main__":
    main()
