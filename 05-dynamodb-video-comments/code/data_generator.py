"""
uv run code/data_generator.py
"""

from datetime import datetime, timedelta, timezone
import ulid
from sample_data_output import (
    print_summary,
    print_comment_tree,
)

BASE_TIME = datetime(2026, 10, 31, 8, 0, tzinfo=timezone.utc)
INTERVAL_MINUTES = 30


def node(label, *replies):
    """Create a comment node with its direct replies."""
    return {
        "label": label,
        "replies": list(replies),
    }


# 25 comments per video, including nested replies.
VIDEO_TREES = {
    "V001": [
        node(
            "R01",
            node("R01-A"),
            node("R01-B", node("R01-B1", node("R01-B1a"))),
            node("R01-C"),
            node("R01-D"),
            node("R01-E"),
            node("R01-F"),
            node("R01-G"),
        ),
        node(
            "R02",
            node("R02-A", node("R02-A1"), node("R02-A2")),
            node("R02-B"),
        ),
        node("R03", node("R03-A", node("R03-A1"))),
        node("R04", node("R04-A")),
        node("R05", node("R05-A")),
        node("R06"),
        node("R07"),
        node("R08"),
    ],
    "V002": [
        node(
            "S01",
            node("S01-A", node("S01-A1")),
            node("S01-B", node("S01-B1")),
            node("S01-C"),
            node("S01-D"),
            node("S01-E"),
            node("S01-F"),
        ),
        node(
            "S02",
            node("S02-A", node("S02-A1"), node("S02-A2")),
            node("S02-B"),
        ),
        node(
            "S03",
            node("S03-A"),
            node("S03-B", node("S03-B1")),
        ),
        node("S04", node("S04-A")),
        node("S05", node("S05-A")),
        node("S06"),
        node("S07"),
        node("S08"),
    ],
}


def generate_ulid(timestamp: datetime, sequence: int) -> str:
    """
    Generate a deterministic ULID.

    First 6 bytes: timestamp in milliseconds.
    Remaining 10 bytes: deterministic sequence.
    """
    timestamp_ms = int(timestamp.timestamp() * 1000)

    ulid_bytes = (
        timestamp_ms.to_bytes(6, byteorder="big")
        + sequence.to_bytes(10, byteorder="big")
    )

    return str(ulid.from_bytes(ulid_bytes))


def generate_comments() -> list[dict]:
    """Generate DynamoDB-ready comment items for both videos."""

    comments = []
    sequence = 0

    def add_comment(video_id, spec, parent_id, root_id, depth):
        nonlocal sequence

        comment_time = BASE_TIME + timedelta(
            minutes=INTERVAL_MINUTES * sequence
        )

        raw_id = generate_ulid(comment_time, sequence)

        # A root comment is its own RootId.
        current_root_id = raw_id if depth == 0 else root_id

        item = {
            "VideoId": f"VIDEO#{video_id}",
            "CommentId": f"COMMENT#{raw_id}",
            "RootId": current_root_id,
            "Depth": depth,
            "CreatedAt": comment_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "Label": spec["label"],
            "Text": f"Sample comment {spec['label']} on {video_id}",
            "LikeCount": (sequence * 7) % 100,
            "ReplyCount": len(spec["replies"]),
            "VideoIdDepth": (
                f"VIDEO#{video_id}#DEPTH#{depth:03d}"
            ),
        }

        # Root comments have no ParentId.
        if parent_id is not None:
            item["ParentId"] = parent_id

        comments.append(item)
        sequence += 1

        # Recursively generate direct replies and nested replies.
        for reply in spec["replies"]:
            add_comment(
                video_id=video_id,
                spec=reply,
                parent_id=raw_id,
                root_id=current_root_id,
                depth=depth + 1,
            )

    for video_id, roots in VIDEO_TREES.items():
        for root in roots:
            add_comment(
                video_id=video_id,
                spec=root,
                parent_id=None,
                root_id=None,
                depth=0,
            )

    return comments


if __name__ == "__main__":
    comments = generate_comments()

    # Basic sanity checks.
    assert len(comments) == 50

    for video_id in VIDEO_TREES:
        video_items = [
            item for item in comments
            if item["VideoId"] == f"VIDEO#{video_id}"
        ]
        assert len(video_items) == 25

    print_summary(VIDEO_TREES, comments)
    print_comment_tree(comments, "V001")
