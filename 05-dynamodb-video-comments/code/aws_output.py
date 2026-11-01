from datetime import datetime


def format_created_at(timestamp):
    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    return dt.strftime("%d %b %Y, %I:%M %p UTC")


def print_root_comments(video_id, items, page_number, has_more):
    print(f"\nVideo {video_id} - Root Comments (Page {page_number})")
    print("-" * 40)

    for item in items:
        print(
            f"{item['Text']} "
            f"[CreatedAt={format_created_at(item['CreatedAt'])}, "
            f"Depth={item['Depth']}, "
            f"Replies={item['ReplyCount']}]"
        )

    print(f"\nItems returned: {len(items)}")
    print(f"More pages available: {has_more}")


def print_replies(parent_id, items):
    print(f"\nReplies for parent: {parent_id}")
    print("-" * 60)

    for item in items:
        print(
            f"{item['Text']} "
            f"[CreatedAt={format_created_at(item['CreatedAt'])}, "
            f"Depth={item['Depth']}]"
        )

    print(f"\nReplies returned: {len(items)}")
