"""Regression tests for the three reported order-lifecycle defects.

Each test below is expected to FAIL against the current implementation and
pass once the corresponding defect is fixed. They cover only the symptoms
reported in the README:

1. orders that over-fill;
2. cancelled orders that still show open quantity;
3. cancels that go through twice.
"""

import pytest

from orders import OrderService, OrderStatus


@pytest.fixture
def service() -> OrderService:
    return OrderService()


# ---------------------------------------------------------------- overfill

def test_single_fill_cannot_exceed_remaining(service):
    """README issue 1: a fill larger than the open quantity must be rejected."""
    order = service.place("AAPL", "buy", 10)
    service.fill(order.order_id, 6)

    with pytest.raises(ValueError):
        service.fill(order.order_id, 5)

    assert order.filled == 6
    assert order.status == OrderStatus.PARTIAL
    assert service.remaining(order.order_id) == 4


def test_fill_after_fully_filled_cannot_exceed_quantity(service):
    """README issue 1: another fill after FILLED must not over-fill the order."""
    order = service.place("AAPL", "buy", 10)
    service.fill(order.order_id, 10)

    with pytest.raises(ValueError):
        service.fill(order.order_id, 1)

    assert order.filled == 10
    assert order.status == OrderStatus.FILLED
    assert service.remaining(order.order_id) == 0


# ----------------------- cancelled orders that still show open quantity

def test_cancelled_order_remaining_is_zero(service):
    """README issue 2: a cancelled order must not report residual open quantity."""
    order = service.place("AAPL", "buy", 10)
    service.fill(order.order_id, 3)

    service.cancel(order.order_id)

    assert service.remaining(order.order_id) == 0


def test_cancelled_open_qty_excluded_but_working_qty_retained(service):
    """README issue 2: cancelled residual must not count towards symbol open qty."""
    cancelled = service.place("AAPL", "buy", 10)
    service.fill(cancelled.order_id, 3)
    service.cancel(cancelled.order_id)

    working = service.place("AAPL", "buy", 4)

    assert service.open_qty_for("AAPL") == 4
    assert service.remaining(working.order_id) == 4


# ------------------------------------------------------- double cancels

def test_duplicate_cancel_is_rejected(service):
    """README issue 3: cancelling an already-cancelled order must not succeed."""
    order = service.place("AAPL", "buy", 5)
    service.cancel(order.order_id)

    with pytest.raises(ValueError):
        service.cancel(order.order_id)

    assert order.status == OrderStatus.CANCELLED
