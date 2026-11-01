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
    # Test 1: Root comment with multiple direct replies
    parent_id = "REPLACE_WITH_R01_ULID"
    replies = get_replies(parent_id)

    print_replies(
        parent_id=parent_id,
        items=replies,
    )

    # Test 2: Nested comment with a direct reply
    parent_id = "REPLACE_WITH_R01_B_ULID"
    replies = get_replies(parent_id)

    print_replies(
        parent_id=parent_id,
        items=replies,
    )
