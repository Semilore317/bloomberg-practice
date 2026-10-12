import pytest
from orders import OrderService, OrderStatus


def svc():
    return OrderService()


def test_place_creates_open_order():
    s = svc()
    o = s.place("AAPL", "buy", 10)
    assert o.status == OrderStatus.OPEN
    assert s.remaining(o.order_id) == 10


def test_partial_fill_sets_partial_and_remaining():
    s = svc()
    o = s.place("AAPL", "buy", 10)
    s.fill(o.order_id, 4)
    assert o.status == OrderStatus.PARTIAL
    assert s.remaining(o.order_id) == 6


def test_full_fill_sets_filled():
    s = svc()
    o = s.place("AAPL", "buy", 10)
    s.fill(o.order_id, 10)
    assert o.status == OrderStatus.FILLED
    assert s.remaining(o.order_id) == 0


def test_two_fills_accumulate():
    s = svc()
    o = s.place("AAPL", "buy", 10)
    s.fill(o.order_id, 4)
    s.fill(o.order_id, 6)
    assert o.status == OrderStatus.FILLED


def test_overfill_rejected():
    s = svc()
    o = s.place("AAPL", "buy", 10)
    with pytest.raises(ValueError):
        s.fill(o.order_id, 11)


def test_fill_cancelled_order_rejected():
    s = svc()
    o = s.place("AAPL", "buy", 10)
    s.cancel(o.order_id)
    with pytest.raises(ValueError):
        s.fill(o.order_id, 1)


def test_cancel_open_order():
    s = svc()
    o = s.place("AAPL", "buy", 10)
    s.cancel(o.order_id)
    assert o.status == OrderStatus.CANCELLED


def test_double_cancel_rejected():
    s = svc()
    o = s.place("AAPL", "buy", 10)
    s.cancel(o.order_id)
    with pytest.raises(ValueError):
        s.cancel(o.order_id)


def test_open_qty_excludes_cancelled():
    s = svc()
    o = s.place("AAPL", "buy", 10)
    s.cancel(o.order_id)
    assert s.open_qty_for("AAPL") == 0


def test_open_qty_sums_remaining():
    s = svc()
    a = s.place("AAPL", "buy", 10)
    s.place("AAPL", "buy", 5)
    s.fill(a.order_id, 4)
    assert s.open_qty_for("AAPL") == 11
