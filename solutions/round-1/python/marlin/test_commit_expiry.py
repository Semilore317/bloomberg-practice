import pytest

from inventory import InventoryService, ResStatus


def test_commit_after_expiry_is_rejected_and_units_returned():
    """A hold past its TTL must not be committable; its units are already free."""
    now = [0.0]
    svc = InventoryService({"A": 5}, hold_ttl_seconds=10, clock=lambda: now[0])
    reservation = svc.reserve("A", 2)
    assert svc.available("A") == 3

    now[0] = 11.0  # hold expired at t=10

    with pytest.raises(ValueError):
        svc.commit(reservation.reservation_id)

    # Expired holds return their units automatically.
    assert svc.available("A") == 5
    assert svc.reserved_units("A") == 0


def test_commit_at_exact_expiry_is_rejected():
    """Expiry is inclusive: at expires_at == now the hold is already expired."""
    now = [0.0]
    svc = InventoryService({"A": 5}, hold_ttl_seconds=10, clock=lambda: now[0])
    reservation = svc.reserve("A", 2)

    now[0] = 10.0  # exactly expires_at

    with pytest.raises(ValueError):
        svc.commit(reservation.reservation_id)

    assert svc.available("A") == 5


def test_commit_before_expiry_still_succeeds():
    """Control: the fix must not block committing a still-valid hold."""
    now = [0.0]
    svc = InventoryService({"A": 5}, hold_ttl_seconds=10, clock=lambda: now[0])
    reservation = svc.reserve("A", 2)

    now[0] = 9.0

    committed = svc.commit(reservation.reservation_id)
    assert committed.status == ResStatus.COMMITTED
    # Shipped units stay deducted.
    assert svc.available("A") == 3
