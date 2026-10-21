
CREATE TABLE IF NOT EXISTS orders (
    order_id      TEXT PRIMARY KEY,
    customer_id   TEXT NOT NULL,
    created_at    TIMESTAMP NOT NULL,
    status        TEXT NOT NULL,
    description   TEXT NOT NULL,
    total_amount  NUMERIC(10, 2) NOT NULL
);
