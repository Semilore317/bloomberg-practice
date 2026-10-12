import pytest
from ratelimit import RateLimiter


class FakeClock:
    def __init__(self, v=1000.0):
        self.v = v
    def __call__(self):
        return self.v
    def advance(self, s):
        self.v += s


def lim(clock=None):
    return RateLimiter(limit=3, window_seconds=10, clock=clock or FakeClock())


def test_allows_under_limit():
    r = lim()
    assert [r.allow("k") for _ in range(3)] == [True, True, True]


def test_blocks_at_limit():
    r = lim()
    for _ in range(3):
        r.allow("k")
    assert r.allow("k") is False


def test_remaining_counts_down():
    r = lim()
    r.allow("k")
    assert r.remaining("k") == 2


def test_remaining_zero_at_limit():
    r = lim()
    for _ in range(3):
        r.allow("k")
    assert r.remaining("k") == 0


def test_separate_keys_independent():
    r = lim()
    for _ in range(3):
        r.allow("a")
    assert r.allow("b") is True


def test_window_resets_after_window():
    c = FakeClock()
    r = lim(c)
    for _ in range(3):
        r.allow("k")
    assert r.allow("k") is False
    c.advance(11)
    assert r.allow("k") is True


def test_remaining_resets_after_window():
    c = FakeClock()
    r = lim(c)
    r.allow("k")
    r.allow("k")
    c.advance(11)
    assert r.remaining("k") == 3


def test_reset_clears_the_window():
    r = lim()
    for _ in range(3):
        r.allow("k")
    r.reset("k")
    assert r.allow("k") is True
