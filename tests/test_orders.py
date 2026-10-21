"""
uv run pytest -v
"""

from index_core import generate_data


def test_order_schema():
    orders = generate_data()
    assert len(orders) == 200

    for order in orders:
        assert isinstance(order, tuple)
        assert len(order) == 6

        order_id, customer_id, created_at, status, description, total_amount = order

        assert isinstance(order_id, str)
        assert isinstance(customer_id, str)
        assert isinstance(created_at, str)
        assert isinstance(status, str)
        assert isinstance(description, str)
        assert isinstance(total_amount, float)


def test_default_seed_is_deterministic():
    assert generate_data() == generate_data()
