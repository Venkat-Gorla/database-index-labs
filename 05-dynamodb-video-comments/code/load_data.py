"""
uv run code/load_data.py
"""

import boto3
from data_generator import generate_comments

TABLE_NAME = "database-index-lab-video-comments"


def load_data():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)

    comments = generate_comments()

    print(f"Loading {len(comments)} comments into {TABLE_NAME}...")

    with table.batch_writer() as batch:
        for comment in comments:
            batch.put_item(Item=comment)

    print(f"Successfully loaded {len(comments)} comments.")


if __name__ == "__main__":
    load_data()
