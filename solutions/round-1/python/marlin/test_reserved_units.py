from inventory import InventoryService


def test_reserved_units_reflects_expiry_without_other_calls():
    """reserved_units must not count a hold that has already expired."""
    now = [0.0]
    svc = InventoryService({"A": 5}, hold_ttl_seconds=10, clock=lambda: now[0])
    svc.reserve("A", 2)

    now[0] = 11.0  # hold expired at t=10

    # No available()/reserve() call in between: reserved_units alone must be correct.
    assert svc.reserved_units("A") == 0


def test_reserved_units_at_exact_expiry_is_zero():
    """Expiry is inclusive: at expires_at == now the hold is no longer reserved."""
    now = [0.0]
    svc = InventoryService({"A": 5}, hold_ttl_seconds=10, clock=lambda: now[0])
    svc.reserve("A", 2)

    now[0] = 10.0  # exactly expires_at

    assert svc.reserved_units("A") == 0


def test_reserved_units_counts_active_hold():
    """Control: a hold that has not expired is still counted as reserved."""
    now = [0.0]
    svc = InventoryService({"A": 5}, hold_ttl_seconds=10, clock=lambda: now[0])
    svc.reserve("A", 2)

    now[0] = 9.0

    assert svc.reserved_units("A") == 2
