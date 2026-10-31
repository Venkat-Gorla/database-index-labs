from collections import Counter


def print_summary(video_trees, comments):
    print(f"\nTotal comments generated: {len(comments)}")

    for video_id in video_trees:
        video_comments = [
            item for item in comments
            if item["VideoId"] == f"VIDEO#{video_id}"
        ]

        depth_counts = Counter(
            item["Depth"] for item in video_comments
        )

        print(f"\n{video_id}: {len(video_comments)} comments")
        for depth, count in sorted(depth_counts.items()):
            print(f"  Depth {depth}: {count}")


def print_comment_tree(comments, video_id):
    video_comments = {
        item["CommentId"].removeprefix("COMMENT#"): item
        for item in comments
        if item["VideoId"] == f"VIDEO#{video_id}"
    }

    children = {}
    roots = []

    for raw_id, item in video_comments.items():
        parent_id = item.get("ParentId")

        if parent_id:
            children.setdefault(parent_id, []).append(raw_id)
        else:
            roots.append(raw_id)

    def print_branch(raw_id, prefix=""):
        item = video_comments[raw_id]

        print(
            f"{prefix}{item['Label']} "
            f"[Depth={item['Depth']}, "
            f"Replies={item['ReplyCount']}]"
        )

        for child_id in children.get(raw_id, []):
            print_branch(child_id, prefix + "  ")

    print(f"\nVideo {video_id} Comments Tree")
    print("-" * 30)
    for root_id in roots:
        print_branch(root_id)
