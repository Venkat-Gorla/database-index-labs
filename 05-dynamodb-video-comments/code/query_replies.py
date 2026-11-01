"""
uv run code/query_replies.py
"""

import boto3
from aws_output import print_replies

TABLE_NAME = "database-index-lab-video-comments"

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def get_replies(parent_id):
    response = table.query(
        IndexName="ParentCommentIndex",
        KeyConditionExpression="ParentId = :parent_id",
        ExpressionAttributeValues={
            ":parent_id": parent_id
        },
        ScanIndexForward=False,
    )

    return response.get("Items", [])


if __name__ == "__main__":
    test_cases = {
        # Root comment with multiple direct replies
        "Test 1 - Root comment R01": "01M68FJ0000000000000000000",

        # Nested comment with a direct reply
        "Test 2 - Nested comment R01-B": "01M68JZVM00000000000000002",
    }

    for description, parent_id in test_cases.items():
        print(f"\n{description}")
        replies = get_replies(parent_id)
        print_replies(parent_id, items=replies)
