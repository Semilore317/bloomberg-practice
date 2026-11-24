from __future__ import annotations

from typing import Dict

from matching.models import Trade


class PositionBook:
    def __init__(self) -> None:
        self._net: Dict[str, int] = {}

    def apply(self, trade: Trade) -> None:
        self._net[trade.maker_account] = (
            self._net.get(trade.maker_account, 0) - trade.qty
        )
        self._net[trade.taker_account] = (
            self._net.get(trade.taker_account, 0) + trade.qty
        )

    def net(self, account: str) -> int:
        return self._net.get(account, 0)

    def snapshot(self) -> Dict[str, int]:
        return dict(self._net)
