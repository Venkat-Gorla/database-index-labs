# DynamoDB Schema Diagram — Video Comments

```text
              video-comments
          ┌────────────────────┐
          │ VideoId            │
          │ CommentId          │
          │ ParentId           │
          │ RootId             │
          │ Depth              │
          │ LikeCount          │
          └─────────┬──────────┘
                    │
          ┌─────────┴──────────┐
          ▼                    ▼
         GSI                  GSI
   VideoDepthIndex      ParentCommentIndex
     Comments             Direct replies
     by video/depth       by parent comment
```
