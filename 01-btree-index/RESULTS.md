# B-tree Index — Experiment Results

## Query

Find orders for `CUST-007`, newest first.

- Dataset: 200 orders
- Matching orders: 12
- Database: SQLite
- Index: `(customer_id, created_at DESC)`

## Before Index

```text
SCAN orders
USE TEMP B-TREE FOR ORDER BY
```

SQLite scans the table to find matching orders and uses a temporary B-tree to sort them.

## After Index

```text
SEARCH orders USING INDEX idx_orders_customer_created (customer_id=?)
```

SQLite uses the index to locate the customer's orders. The plan no longer reports a temporary B-tree for sorting.

## Verification

After dropping the index, the original query plan returned. All runs returned the same 12 orders in the same order.

## Conclusion

The composite B-tree index supports both customer filtering and timestamp ordering.

`EXPLAIN QUERY PLAN` confirms the access strategy, but does not report exact rows examined. No numerical efficiency improvement is claimed.
