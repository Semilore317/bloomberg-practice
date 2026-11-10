import pytest

from inventory import InventoryService


def test_release_twice_does_not_double_credit():
    """Releasing the same reservation twice must not return its units twice."""
    svc = InventoryService({"A": 5})
    reservation = svc.reserve("A", 2)
    assert svc.available("A") == 3

    svc.release(reservation.reservation_id)
    assert svc.available("A") == 5

    # A reservation is terminal once released; a second release must be rejected.
    with pytest.raises(ValueError):
        svc.release(reservation.reservation_id)

    # The key regression: units must not exceed capacity / be credited twice.
    assert svc.available("A") == 5


def test_release_committed_reservation_is_rejected():
    """Units that have already shipped must not be returned to available stock."""
    svc = InventoryService({"A": 5})
    reservation = svc.reserve("A", 2)
    svc.commit(reservation.reservation_id)
    assert svc.available("A") == 3

    # A committed reservation was shipped, not held; it cannot be released.
    with pytest.raises(ValueError):
        svc.release(reservation.reservation_id)

    assert svc.available("A") == 3


def test_release_after_expiry_does_not_double_credit():
    """An expired hold has already returned its units; releasing it must not credit again."""
    now = [0.0]
    svc = InventoryService({"A": 5}, hold_ttl_seconds=10, clock=lambda: now[0])
    reservation = svc.reserve("A", 2)

    now[0] = 11.0
    # Expiry cleanup returns the units and marks the reservation RELEASED.
    assert svc.available("A") == 5

    with pytest.raises(ValueError):
        svc.release(reservation.reservation_id)

    assert svc.available("A") == 5
