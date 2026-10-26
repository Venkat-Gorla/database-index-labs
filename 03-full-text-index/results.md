# Lab 03 — Full-Text Search (SQLite FTS5)

## Objective

Understand full-text search in SQLite using FTS5 and compare its matching behavior with a regular `LIKE` query.

## Experiment

- Dataset: 200 synthetic orders
- Search field: `description`
- Baseline: `LIKE '%board%'`
- FTS5: `MATCH 'board'`

## Results

|               | Baseline (`LIKE`) | FTS5 (`MATCH`)                             |
| ------------- | ----------------- | ------------------------------------------ |
| Matching rows | 13                | 0                                          |
| Query plan    | `SCAN orders`     | `SCAN orders_fts VIRTUAL TABLE INDEX 0:M1` |

## Key Learnings

- **Substring search:** `LIKE '%board%'` matches `board` inside `keyboard`.
- **Token search:** FTS5 `MATCH 'board'` searches for the token `board`, not a substring within `keyboard`.

_Note: This experiment demonstrates matching behavior and query-plan evidence, not a measured performance improvement._
