import pytest

from wallet import HoldStatus, WalletService


def test_held_funds_are_not_spendable():
    wallet = WalletService()
    wallet.open_account("acct-1", 100)

    hold = wallet.authorize("acct-1", 30)

    assert hold.status == HoldStatus.HELD
    assert wallet.balance("acct-1") == 100
    assert wallet.available("acct-1") == 70

    with pytest.raises(ValueError, match="insufficient available funds"):
        wallet.authorize("acct-1", 80)


def test_void_on_already_voided_hold_raises():
    wallet = WalletService()
    wallet.open_account("acct-1", 100)
    hold = wallet.authorize("acct-1", 30)

    wallet.void(hold.hold_id)
    assert hold.status == HoldStatus.VOIDED
    assert wallet.balance("acct-1") == 100

    with pytest.raises(ValueError):
        wallet.void(hold.hold_id)

    assert wallet.balance("acct-1") == 100
    assert hold.status == HoldStatus.VOIDED


def test_capture_does_not_run_after_void():
    wallet = WalletService()
    wallet.open_account("acct-1", 100)
    hold = wallet.authorize("acct-1", 30)

    wallet.void(hold.hold_id)
    assert hold.status == HoldStatus.VOIDED

    try:
        result = wallet.capture(hold.hold_id)
    except ValueError:
        result = None

    assert wallet.balance("acct-1") == 100
    assert hold.status == HoldStatus.VOIDED
    if result is not None:
        assert result.status == HoldStatus.VOIDED
