import pytest
from inventory import InventoryService, ResStatus


class FakeClock:
    def __init__(self, v=1000.0):
        self.v = v
    def __call__(self):
        return self.v
    def advance(self, s):
        self.v += s


def svc(clock=None):
    return InventoryService({"A": 5, "B": 8}, hold_ttl_seconds=60, clock=clock or FakeClock())


def test_reserve_reduces_available():
    s = svc()
    r = s.reserve("A", 2)
    assert r.status == ResStatus.HELD
    assert s.available("A") == 3


def test_commit_keeps_stock_consumed():
    s = svc()
    r = s.reserve("A", 2)
    s.commit(r.reservation_id)
    assert s.available("A") == 3


def test_release_restores_stock():
    s = svc()
    r = s.reserve("A", 2)
    s.release(r.reservation_id)
    assert s.available("A") == 5


def test_release_non_held_rejected():
    s = svc()
    r = s.reserve("A", 2)
    s.release(r.reservation_id)
    with pytest.raises(ValueError):
        s.release(r.reservation_id)          # double release
    r2 = s.reserve("A", 2)
    s.commit(r2.reservation_id)
    with pytest.raises(ValueError):
        s.release(r2.reservation_id)          # release a committed reservation
    assert s.available("A") == 3


def test_expired_hold_restores_stock():
    c = FakeClock()
    s = svc(c)
    s.reserve("A", 2)
    c.advance(61)
    assert s.available("A") == 5


def test_expired_hold_cannot_be_committed():
    c = FakeClock()
    s = svc(c)
    r = s.reserve("A", 2)
    c.advance(61)
    with pytest.raises(ValueError):
        s.commit(r.reservation_id)


def test_committed_survives_ttl():
    c = FakeClock()
    s = svc(c)
    r = s.reserve("A", 2)
    s.commit(r.reservation_id)
    c.advance(1000)
    assert s.available("A") == 3
    assert s.reserved_units("A") == 2


def test_reserved_units_reflects_expiry():
    c = FakeClock()
    s = svc(c)
    s.reserve("A", 2)
    c.advance(61)
    assert s.reserved_units("A") == 0


def test_reserve_rejects_oversell():
    s = svc()
    with pytest.raises(ValueError):
        s.reserve("A", 6)


def test_reserve_sums_reduce():
    s = svc()
    s.reserve("A", 2)
    s.reserve("A", 1)
    assert s.available("A") == 2
