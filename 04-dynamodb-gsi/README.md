# DynamoDB Global Secondary Index (GSI)

```text
          Base Table
     ┌──────────────────┐
     │ PK: order_id     │
     │ customer_id      │
     │ created_at       │
     │ status           │
     └────────┬─────────┘
              │
              ▼
     ┌──────────────────┐
     │       GSI        │
     │ PK: customer_id  │
     │ SK: created_at   │
     └────────┬─────────┘
              │
              ▼
     Query customer orders
        ordered by time
```

A GSI enables queries using an alternative partition key and optional sort key, without changing the base table's primary key.

The GSI is maintained separately and may be eventually consistent with the base table.
