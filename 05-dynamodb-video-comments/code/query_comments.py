"""
uv run code/query_comments.py
"""

import boto3
from aws_output import (
    print_root_comments,
)

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
    video_id = "V001"
    result = get_root_comments(video_id)

    print_root_comments(
        video_id=video_id,
        items=result["items"],
        page_number=1,
        has_more=result["last_evaluated_key"] is not None,
    )
