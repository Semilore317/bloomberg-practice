"""Framework-free reproductions for the reported cases in tickets/.

Each test targets one ticket's symptom and is expected to fail against the
current implementation. No pytest, fixtures, clock, or config changes needed.
"""

from gateway.session import SessionLimiter
from infra.events import EventBus
from marketdata.publisher import QuotePublisher
from marketdata.quote_cache import QuoteCache
from matching.book import OrderBook
from matching.errors import RiskError
from matching.service import MatchingService


def test_kes_077_priority():
    """Two bids at one price: the older one must trade first."""
    svc = MatchingService()
    svc.submit("b1", "OLDER", "buy", 100, 10)
    svc.submit("b2", "NEWER", "buy", 100, 10)

    trades = svc.submit("s1", "TAKER", "sell", 100, 5)
    assert len(trades) == 1, trades
    assert trades[0].maker_id == "b1", trades[0]


def test_kes_083_partial_fill():
    """A partially filled maker must stay in the book for later fills."""
    svc = MatchingService()
    svc.submit("b1", "MAKER", "buy", 100, 10)

    first = svc.submit("s1", "TAKER1", "sell", 100, 4)
    assert len(first) == 1 and first[0].qty == 4, first
    assert svc.book.best_bid() == 100, svc.book.best_bid()

    second = svc.submit("s2", "TAKER2", "sell", 100, 6)
    assert len(second) == 1, second
    assert second[0].maker_id == "b1" and second[0].qty == 6, second[0]


def test_kes_090_cancel():
    """A cancelled order must not match a later crossing order."""
    svc = MatchingService()
    svc.submit("b1", "MAKER", "buy", 100, 10)

    assert svc.cancel("b1") is True
    trades = svc.submit("s1", "TAKER", "sell", 100, 10)
    assert trades == [], trades
    assert svc.cancel("missing") is False


def test_kes_101_iceberg_reserve():
    """An iceberg must replenish its display from reserve after a fill."""
    svc = MatchingService()
    svc.submit("ice", "MAKER", "buy", 100, 25,
               order_type="iceberg", display_qty=3)

    first = svc.submit("s1", "TAKER1", "sell", 100, 3)
    assert len(first) == 1 and first[0].qty == 3, first
    assert svc.book.best_bid() == 100, svc.book.best_bid()

    second = svc.submit("s2", "TAKER2", "sell", 100, 3)
    assert len(second) == 1, second
    assert second[0].maker_id == "ice" and second[0].qty == 3, second[0]


def test_kes_102_self_trade():
    """An account must not cross its own resting order."""
    svc = MatchingService()
    svc.submit("m1", "ACCT", "buy", 100, 10)

    try:
        svc.submit("t1", "ACCT", "sell", 100, 10)
    except RiskError:
        pass
    else:
        raise AssertionError("expected RiskError for self-trade")
    assert svc.ledger.trades() == [], svc.ledger.trades()
    assert svc.positions.net("ACCT") == 0, svc.positions.snapshot()


def test_kes_103_position_limit_before_fill():
    """A limit breach must be rejected before ledger/position mutation."""
    svc = MatchingService()
    for i, acct in enumerate(("A", "B", "C")):
        svc.submit(f"s{i}", acct, "sell", 1, 50)

    try:
        svc.submit("b1", "X", "buy", 1, 150)
    except RiskError:
        pass
    else:
        raise AssertionError("expected RiskError before execution")

    assert svc.ledger.trades() == [], svc.ledger.trades()
    assert svc.positions.net("X") == 0, svc.positions.snapshot()


def test_kes_104_event_id_dedupe():
    """Replaying an event id must not create a second ledger entry."""
    svc = MatchingService()
    svc.submit("s1", "MAKER", "sell", 100, 30)

    svc.submit("b1", "TAKER", "buy", 100, 10, event_id="E1")
    svc.submit("b2", "TAKER", "buy", 100, 10, event_id="E1")
    e1 = [entry for entry in svc.ledger.entries() if entry[0] == "E1"]
    assert len(e1) == 1, e1

    svc.submit("b3", "TAKER", "buy", 100, 10, event_id="E2")
    assert len(svc.ledger.trades()) == 2, svc.ledger.trades()


def test_kes_105_quote_freshness():
    """The cached best quote must reflect book changes."""
    svc = MatchingService()
    svc.submit("b1", "M1", "buy", 100, 10)
    svc.submit("b2", "M2", "buy", 90, 10)
    assert svc.best_quote() == (100, None), svc.best_quote()

    svc.submit("s1", "T", "sell", 100, 10)
    assert svc.best_quote() == (90, None), svc.best_quote()

    # Cancellation case from the same ticket. This also depends on KES-90
    # being fixed, because cancel currently leaves the book unchanged.
    svc.cancel("b2")
    assert svc.best_quote() == (None, None), svc.best_quote()


def test_kes_106_subscriber_fanout():
    """One throwing handler must not block other subscribers."""
    bus = EventBus()
    called = []

    def bad(event):
        called.append("bad")
        raise RuntimeError("handler failed")

    def good(event):
        called.append("good")

    bus.subscribe("quote", bad)
    bus.subscribe("quote", good)
    publisher = QuotePublisher(QuoteCache(OrderBook()), bus)

    try:
        publisher.publish_quote()
    except RuntimeError:
        pass

    assert called == ["bad", "good"], called
    assert len(bus.published()) == 1, bus.published()


def test_kes_107_rate_limit_boundary():
    """Exactly rate_limit orders are accepted per window."""
    limiter = SessionLimiter(3, 60)
    results = [limiter.allow("session-A", 0) for _ in range(4)]
    assert results == [True, True, True, False], results


_TESTS = [
    test_kes_077_priority,
    test_kes_083_partial_fill,
    test_kes_090_cancel,
    test_kes_101_iceberg_reserve,
    test_kes_102_self_trade,
    test_kes_103_position_limit_before_fill,
    test_kes_104_event_id_dedupe,
    test_kes_105_quote_freshness,
    test_kes_106_subscriber_fanout,
    test_kes_107_rate_limit_boundary,
]


if __name__ == "__main__":
    failures = []
    for test in _TESTS:
        try:
            test()
        except Exception as exc:
            failures.append((test.__name__, repr(exc)))

    for name, error in failures:
        print(f"FAIL {name}: {error}")
    print(f"{len(failures)}/{len(_TESTS)} reproductions failed (expected before fixes)")
    raise SystemExit(1 if failures else 0)
