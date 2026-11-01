"""
uv run code/query_comments.py
"""

import boto3

TABLE_NAME = "database-index-lab-video-comments"
PAGE_SIZE = 5

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def get_root_comments(video_id, exclusive_start_key=None):
    query_kwargs = {
        "IndexName": "VideoDepthIndex",
        "KeyConditionExpression": "VideoIdDepth = :partition_key",
        "ExpressionAttributeValues": {
            ":partition_key": f"VIDEO#{video_id}#DEPTH#000"
        },
        "ScanIndexForward": False,
        "Limit": PAGE_SIZE,
    }

    if exclusive_start_key:
        query_kwargs["ExclusiveStartKey"] = exclusive_start_key

    response = table.query(**query_kwargs)

    return {
        "items": response.get("Items", []),
        "last_evaluated_key": response.get("LastEvaluatedKey"),
    }


if __name__ == "__main__":
    result = get_root_comments("V001")

    print("\nVideo V001 - Root Comments")
    print("-" * 40)

    for item in result["items"]:
        print(
            f"{item['Text']} "
            f"[CreatedAt={item['CreatedAt']}, "
            f"Depth={item['Depth']}, "
            f"Replies={item['ReplyCount']}]"
        )

    print(f"\nItems returned: {len(result['items'])}")
    print(f"More pages available: {result['last_evaluated_key'] is not None}")
