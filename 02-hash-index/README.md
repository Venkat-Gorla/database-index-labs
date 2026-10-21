# Hash Index

```text
                  Query
                    │
           WHERE customer_id = ?
                    │
          ┌─────────▼─────────┐
          │    Hash Index     │
          └─────────┬─────────┘
                    │
           Hash the search key
                    │
         Locate matching entries
                    │
          ┌─────────▼─────────┐
          │   Matching Rows   │
          └───────────────────┘


       B-tree Index           Hash Index
       ────────────           ──────────
       Equality lookup        Equality lookup
       Range queries          Not supported
       Ordered retrieval      Not supported

```

> Explore PostgreSQL hash indexes through equality lookups, query-plan inspection, and comparison with B-tree indexes.
