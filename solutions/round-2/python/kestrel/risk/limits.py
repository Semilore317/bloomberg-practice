from __future__ import annotations

from matching.errors import RiskError


class PositionLimits:
    def __init__(self, max_position: int) -> None:
        self.max_position = max_position

    def check(self, account: str, side: str, qty: int, positions) -> None:
        current = positions.net(account)
        projected = current + qty if side == "buy" else current - qty
        if abs(projected) > self.max_position:
            raise RiskError(
                f"position limit breached for {account}: "
                f"{projected} exceeds {self.max_position}"
            )
