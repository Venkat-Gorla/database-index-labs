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
