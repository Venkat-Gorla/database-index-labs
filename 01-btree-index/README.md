# B-tree Index

```text
                 Query
                   │
            WHERE user_id = ?
                   │
          ┌────────▼────────┐
          │   B-tree Index  │
          └────────┬────────┘
                   │
          Navigate to matching
             index entries
                   │
          ┌────────▼────────┐
          │ Matching Rows   │
          └─────────────────┘


       Without Index         With Index
       ─────────────         ──────────
       Scan table            Search index
       Check each row        Locate matches
       More work             Less work*
```

> Explore B-tree indexes in SQLite through equality lookups, range queries, sorting, and query-plan inspection.

_Actual performance depends on the data, query, and index._
