"""
uv run code/query_gsi.py
"""

import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = "database-index-lab-orders-gsi"
INDEX_NAME = "customer-orders-index"
CUSTOMER_ID = "CUST-015"


def query_orders(table, customer_id):
    result = {
        "matched_count": 0,
        "scanned_count": 0,
        "consumed_capacity": 0.0,
        "page_count": 0,
    }

    query_kwargs = {
        "IndexName": INDEX_NAME,
        "KeyConditionExpression": Key("customer_id").eq(customer_id),
        "ReturnConsumedCapacity": "INDEXES",
    }

    while True:
        response = table.query(**query_kwargs)

        result["matched_count"] += response["Count"]
        result["scanned_count"] += response["ScannedCount"]
        result["consumed_capacity"] += response["ConsumedCapacity"]["CapacityUnits"]
        result["page_count"] += 1

        last_evaluated_key = response.get("LastEvaluatedKey")
        if not last_evaluated_key:
            break

        query_kwargs["ExclusiveStartKey"] = last_evaluated_key

    return result


def main():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)

    result = query_orders(table, CUSTOMER_ID)

    print(f"Customer: {CUSTOMER_ID}")
    print(f"Pages read: {result['page_count']}")
    print(f"Matching orders: {result['matched_count']}")
    print(f"Orders evaluated: {result['scanned_count']}")
    print(f"Consumed capacity: {result['consumed_capacity']:.1f}")


if __name__ == "__main__":
    main()
