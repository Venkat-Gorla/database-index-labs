"""
uv run code/inspect_data.py
"""

from collections import Counter
from index_core import generate_data

ORDER_COUNT = 500


def main():
    orders = generate_data(order_count=ORDER_COUNT)
    customer_counts = Counter(order[1] for order in orders)

    print(f"Total orders: {len(orders)}")
    print(f"Distinct customers: {len(customer_counts)}")
    print(
        f"Average orders per customer: {len(orders) / len(customer_counts):.1f}")

    print("\nTop 5 customers by order count:")
    for customer_id, count in customer_counts.most_common(5):
        print(f"{customer_id}: {count} orders")


if __name__ == "__main__":
    main()
