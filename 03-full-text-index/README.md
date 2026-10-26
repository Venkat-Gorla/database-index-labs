# Full-Text Index

```text
                Search Query
              MATCH 'keyboard'
                      │
             ┌────────▼────────┐
             │ Inverted Index  │
             └────────┬────────┘
                      │
             Find matching terms
               and their rows
                      │
             ┌────────▼────────┐
             │ Matching Rows   │
             └─────────────────┘


       Without Index         With Index
       ─────────────         ──────────
       Scan text             Search terms
       Check descriptions    Locate matches
```

> Explore full-text search with SQLite FTS5.
