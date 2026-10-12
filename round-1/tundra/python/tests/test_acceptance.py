import pytest
from cache import LRUCache


class FakeClock:
    def __init__(self, v=1000.0):
        self.v = v
    def __call__(self):
        return self.v
    def advance(self, s):
        self.v += s


def cache(cap=2, ttl=60, clock=None):
    return LRUCache(cap, ttl, clock or FakeClock())


def test_put_get():
    c = cache()
    c.put("a", 1)
    assert c.get("a") == 1


def test_missing_returns_none():
    c = cache()
    assert c.get("x") is None


def test_update_existing():
    c = cache()
    c.put("a", 1)
    c.put("a", 2)
    assert c.get("a") == 2


def test_capacity_evicts_oldest():
    c = cache(cap=2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("c", 3)
    assert c.get("a") is None
    assert c.get("c") == 3


def test_size_counts_live():
    c = cache(cap=3)
    c.put("a", 1)
    c.put("b", 2)
    assert c.size() == 2


def test_lru_evicts_least_recently_used():
    c = cache(cap=2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1          # a is now most recently used
    c.put("c", 3)                   # should evict b, not a
    assert c.get("b") is None
    assert c.get("a") == 1


def test_expired_get_returns_none():
    clk = FakeClock()
    c = cache(ttl=60, clock=clk)
    c.put("a", 1)
    clk.advance(61)
    assert c.get("a") is None


def test_expired_not_counted_in_size():
    clk = FakeClock()
    c = cache(ttl=60, clock=clk)
    c.put("a", 1)
    clk.advance(61)
    assert c.size() == 0
