from __future__ import annotations

from matching.errors import RiskError


class FatFingerCheck:
    def __init__(self, max_order_qty: int, max_notional: int) -> None:
        self.max_order_qty = max_order_qty
        self.max_notional = max_notional

    def check(self, price: int, qty: int) -> None:
        if qty > self.max_order_qty:
            raise RiskError(f"order quantity {qty} exceeds {self.max_order_qty}")
        notional = price * qty
        if notional > self.max_notional:
            raise RiskError(f"notional {notional} exceeds {self.max_notional}")
