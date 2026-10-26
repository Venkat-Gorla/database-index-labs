# Lab 02: PostgreSQL B-tree vs. Hash Index

## Objective

Compare PostgreSQL B-tree and hash indexes for an equality lookup on the same dataset. Use `EXPLAIN (ANALYZE, BUFFERS)` to observe index selection, query execution time, and buffer activity.

## 1. Experiment Setup

| Property           | Value                    |
| ------------------ | ------------------------ |
| Database           | PostgreSQL               |
| Table              | `orders`                 |
| Dataset size       | 10,000 rows              |
| Distinct customers | 20                       |
| Lookup column      | `customer_id`            |
| Query type         | Equality lookup          |
| Rows returned      | 526                      |
| Selected columns   | All columns (`SELECT *`) |

The dataset was generated using the shared `index_core` package. The same query and data were used for both index configurations.

### Indexes tested

| Index  | Definition                                   |
| ------ | -------------------------------------------- |
| B-tree | `idx_orders_customer_btree` on `customer_id` |
| Hash   | `idx_orders_customer_hash` on `customer_id`  |

The primary-key B-tree index on `order_id` remained in place throughout the experiment.

## 2. Query Under Test

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM orders
WHERE customer_id = 'CUST-001';
```

Both indexes support this equality lookup. PostgreSQL's planner chooses a query plan based on its cost estimates and available indexes.

## 3. Results

### Execution measurements

| Metric                    |       B-tree |     Hash |
| ------------------------- | -----------: | -------: |
| Execution time            | **0.380 ms** | 0.512 ms |
| Actual rows returned      |          526 |      526 |
| Estimated rows            |          526 |      526 |
| Index scan time           |     0.085 ms | 0.066 ms |
| Shared buffer hits        |          132 |      136 |
| Shared buffer reads       |            2 |        0 |
| Estimated total plan cost |       152.94 |   168.65 |

_Measurements are from one execution per index configuration._

### Query plan shape

| B-tree plan                        | Hash plan                         |
| ---------------------------------- | --------------------------------- |
| Bitmap Index Scan                  | Bitmap Index Scan                 |
| Bitmap Heap Scan                   | Bitmap Heap Scan                  |
| Index: `idx_orders_customer_btree` | Index: `idx_orders_customer_hash` |

Both plans used a bitmap index scan to locate matching rows, followed by a bitmap heap scan to retrieve the table data.

## 4. Key Learnings

1. **Both index types support equality lookups.** PostgreSQL successfully used the B-tree and hash indexes for the same predicate.
2. **Creating an index does not guarantee its selection.** When both indexes were available, PostgreSQL chose the B-tree-based plan because its estimated cost was lower.
3. **Index lookup time is not total query time.** Fetching the matching table rows also contributes to execution time.
4. **Measure actual execution, not just estimates.** `EXPLAIN (ANALYZE, BUFFERS)` provided observed timings and buffer activity in addition to the planner's estimates.

## 5. Conclusion

For this dataset and equality query, the B-tree plan had both the lower estimated total cost and the lower observed execution time.

This is a useful proof of concept demonstrating index selection and execution-plan analysis in PostgreSQL. It does **not** establish that B-tree indexes are universally faster than hash indexes.

### Limitations

- One measured execution per index configuration.
- Results may vary with caching, system activity, and data distribution.
- The experiment used a small synthetic dataset and one equality predicate.
- Execution times are sub-millisecond, so individual measurements are sensitive to measurement conditions.

## 6. Reproduction

Check the table size:

```sql
SELECT COUNT(*) FROM orders;
```

Check the indexes:

```sql
\d orders
```

Run the benchmark query:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM orders
WHERE customer_id = 'CUST-001';
```

To compare index configurations, ensure that the intended index is available and record the actual plan selected by PostgreSQL.
