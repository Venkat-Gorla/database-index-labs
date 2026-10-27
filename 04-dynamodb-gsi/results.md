# Results: DynamoDB GSI

## Experiment

Compare a table `Scan` with `FilterExpression` against a `Query` using the `customer-orders-index` GSI.

- Table items: 500
- Customer queried: `CUST-015`
- Matching orders: 43

## Results

| Metric                | Scan + Filter | GSI Query |
| --------------------- | ------------: | --------: |
| **Items matched**     |            43 |        43 |
| **Items evaluated**   |           500 |        43 |
| **Pages read**        |             1 |         1 |
| **Consumed capacity** |           8.5 |       1.0 |

## Key takeaway

A `FilterExpression` filters results after a scan evaluates items. A GSI provides an alternate access path, allowing DynamoDB to query by `customer_id` instead of scanning the base table.

The GSI improves read efficiency for this access pattern, at the cost of additional index storage and write maintenance.
