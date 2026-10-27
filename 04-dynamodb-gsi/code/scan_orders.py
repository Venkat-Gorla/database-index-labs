"""
uv run code/scan_orders.py
"""

import boto3

TABLE_NAME = "database-index-lab-orders-gsi"


def main():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)

    total_count = 0
    total_scanned = 0
    page_count = 0
    scan_kwargs = {}

    while True:
        response = table.scan(**scan_kwargs)

        total_count += response["Count"]
        total_scanned += response["ScannedCount"]
        page_count += 1

        last_evaluated_key = response.get("LastEvaluatedKey")
        if not last_evaluated_key:
            break

        scan_kwargs["ExclusiveStartKey"] = last_evaluated_key

    print(f"Pages read: {page_count}")
    print(f"Orders returned: {total_count}")
    print(f"Orders scanned: {total_scanned}")


if __name__ == "__main__":
    main()
