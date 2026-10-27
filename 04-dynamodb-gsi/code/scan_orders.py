"""
uv run code/scan_orders.py
"""

import boto3
from boto3.dynamodb.conditions import Attr

TABLE_NAME = "database-index-lab-orders-gsi"
CUSTOMER_ID = "CUST-015"


def scan_orders(table, customer_id):
    result = {
        "matched_count": 0,
        "scanned_count": 0,
        "consumed_capacity": 0.0,
        "page_count": 0,
    }

    scan_kwargs = {
        "FilterExpression": Attr("customer_id").eq(customer_id),
        "ReturnConsumedCapacity": "TOTAL",
    }

    while True:
        response = table.scan(**scan_kwargs)

        result["matched_count"] += response["Count"]
        result["scanned_count"] += response["ScannedCount"]
        result["consumed_capacity"] += response["ConsumedCapacity"]["CapacityUnits"]
        result["page_count"] += 1

        last_evaluated_key = response.get("LastEvaluatedKey")
        if not last_evaluated_key:
            break

        scan_kwargs["ExclusiveStartKey"] = last_evaluated_key

    return result


def main():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)

    result = scan_orders(table, CUSTOMER_ID)

    print(f"Customer: {CUSTOMER_ID}")
    print(f"Pages read: {result['page_count']}")
    print(f"Matching orders: {result['matched_count']}")
    print(f"Orders scanned: {result['scanned_count']}")
    print(f"Consumed capacity: {result['consumed_capacity']:.1f}")


if __name__ == "__main__":
    main()
