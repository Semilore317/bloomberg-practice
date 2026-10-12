from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Callable
import time


class ResStatus(str, Enum):
    HELD = "held"
    COMMITTED = "committed"
    RELEASED = "released"


@dataclass
class Reservation:
    reservation_id: str
    sku: str
    qty: int
    status: ResStatus
    expires_at: float | None


class InventoryService:
    """Reserves stock for a fulfilment system. Units are reserved with a TTL hold,
    then either committed (shipped) or released back to available stock. Expired
    holds return their units automatically."""

    def __init__(self, stock: dict[str, int], hold_ttl_seconds: int = 60,
                 clock: Callable[[], float] = time.time) -> None:
        self._capacity = dict(stock)
        self._available = dict(stock)
        self._reservations: dict[str, Reservation] = {}
        self._ttl = hold_ttl_seconds
        self._clock = clock
        self._seq = 0

    def available(self, sku: str) -> int:
        self._cleanup_expired()
        return self._available[sku]

    def reserve(self, sku: str, qty: int) -> Reservation:
        self._cleanup_expired()
        if sku not in self._available:
            raise ValueError("unknown sku")
        if qty <= 0:
            raise ValueError("qty must be positive")
        if self._available[sku] < qty:
            raise ValueError("not enough stock")
        self._seq += 1
        rid = f"R{self._seq}"
        r = Reservation(rid, sku, qty, ResStatus.HELD, self._clock() + self._ttl)
        self._reservations[rid] = r
        self._available[sku] -= qty
        return r

    def commit(self, reservation_id: str) -> Reservation:
        # BUG: does not clean up expiry first, so an expired hold still looks HELD
        r = self._get(reservation_id)
        if r.status != ResStatus.HELD:
            raise ValueError("only held reservations can be committed")
        r.status = ResStatus.COMMITTED
        r.expires_at = None
        return r

    def release(self, reservation_id: str) -> Reservation:
        r = self._get(reservation_id)
        # BUG: no status guard, a released or committed reservation can be released again
        self._available[r.sku] += r.qty
        r.status = ResStatus.RELEASED
        r.expires_at = None
        return r

    def reserved_units(self, sku: str) -> int:
        # BUG: no cleanup, so expired holds still count as reserved
        return self._capacity[sku] - self._available[sku]

    def _get(self, reservation_id: str) -> Reservation:
        r = self._reservations.get(reservation_id)
        if r is None:
            raise ValueError("reservation not found")
        return r

    def _cleanup_expired(self) -> None:
        now = self._clock()
        for r in self._reservations.values():
            if r.status == ResStatus.HELD and r.expires_at is not None and r.expires_at <= now:
                self._available[r.sku] += r.qty
                r.status = ResStatus.RELEASED
