import pytest
from wallet import WalletService, HoldStatus


def acct():
    s = WalletService()
    s.open_account("a1", 500)
    return s


def test_open_sets_balance():
    s = acct()
    assert s.balance("a1") == 500
    assert s.available("a1") == 500


def test_authorize_reduces_available():
    s = acct()
    s.authorize("a1", 300)
    assert s.balance("a1") == 500
    assert s.available("a1") == 200


def test_authorize_keeps_balance():
    s = acct()
    s.authorize("a1", 300)
    assert s.balance("a1") == 500


def test_capture_reduces_balance():
    s = acct()
    h = s.authorize("a1", 300)
    s.capture(h.hold_id)
    assert s.balance("a1") == 200


def test_capture_frees_hold():
    s = acct()
    h = s.authorize("a1", 300)
    s.capture(h.hold_id)
    assert s.available("a1") == 200


def test_void_restores_available():
    s = acct()
    h = s.authorize("a1", 300)
    s.void(h.hold_id)
    assert s.available("a1") == 500
    assert s.balance("a1") == 500


def test_void_non_held_rejected():
    s = acct()
    h = s.authorize("a1", 300)
    s.void(h.hold_id)
    with pytest.raises(ValueError):
        s.void(h.hold_id)                 # double void
    h2 = s.authorize("a1", 100)
    s.capture(h2.hold_id)
    with pytest.raises(ValueError):
        s.void(h2.hold_id)                # void a captured hold


def test_capture_non_held_rejected():
    s = acct()
    h = s.authorize("a1", 300)
    s.void(h.hold_id)
    with pytest.raises(ValueError):
        s.capture(h.hold_id)              # capture a voided hold


def test_unknown_hold_raises():
    s = acct()
    with pytest.raises(ValueError):
        s.void("nope")


def test_authorize_rejects_nonpositive():
    s = acct()
    with pytest.raises(ValueError):
        s.authorize("a1", 0)
