"""
uv run code/load_data.py
"""

from decimal import Decimal
import boto3
from index_core import generate_data

TABLE_NAME = "database-index-lab-orders-gsi"
ORDER_COUNT = 500


def main():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)

    orders = generate_data(order_count=ORDER_COUNT)

    with table.batch_writer() as batch:
        for order in orders:
            (
                order_id,
                customer_id,
                created_at,
                status,
                description,
                total_amount,
            ) = order

            batch.put_item(
                Item={
                    "order_id": order_id,
                    "customer_id": customer_id,
                    "created_at": created_at,
                    "status": status,
                    "description": description,
                    "total_amount": Decimal(str(total_amount)),
                }
            )

    print(f"Loaded {len(orders)} orders into {TABLE_NAME}")


if __name__ == "__main__":
    main()
