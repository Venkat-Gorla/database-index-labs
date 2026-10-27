"""
uv run code/scan_orders.py
"""

import boto3

TABLE_NAME = "database-index-lab-orders-gsi"


def main():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)

    response = table.scan()

    print(f"Orders returned: {response['Count']}")
    print(f"Orders scanned: {response['ScannedCount']}")


if __name__ == "__main__":
    main()
