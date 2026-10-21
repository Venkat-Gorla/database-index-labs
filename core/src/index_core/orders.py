import random
from datetime import datetime, timedelta

ORDER_COUNT = 200
CUSTOMER_COUNT = 20
RANDOM_SEED = 42

STATUSES = ("pending", "shipped", "delivered", "cancelled")

PRODUCTS = [
    "Wireless keyboard",
    "Blue running shoes",
    "Stainless steel bottle",
    "Cotton bedsheet set",
    "USB-C charging cable",
    "Ceramic coffee mug",
    "Laptop stand",
    "Travel backpack",
    "Desk lamp",
    "Notebook set",
]


def generate_data(
    order_count: int = ORDER_COUNT,
    customer_count: int = CUSTOMER_COUNT,
    random_seed: int = RANDOM_SEED,
) -> list[tuple[str, str, str, str, str, float]]:
    """Generate deterministic synthetic customer orders."""

    if order_count < 0:
        raise ValueError("order_count must be non-negative")

    if customer_count <= 0:
        raise ValueError("customer_count must be positive")

    rng = random.Random(random_seed)
    start = datetime(2025, 1, 1)
    orders = []

    for i in range(1, order_count + 1):
        created_at = start + timedelta(
            days=rng.randint(0, 179),
            minutes=rng.randint(0, 1439),
        )

        orders.append(
            (
                f"ORD-{i:03d}",
                f"CUST-{rng.randint(1, customer_count):03d}",
                created_at.isoformat(timespec="seconds"),
                rng.choice(STATUSES),
                f"{rng.choice(PRODUCTS)} - order {i:03d}",
                round(rng.uniform(10, 500), 2),
            )
        )

    return orders
