from __future__ import annotations

from infra.config import EngineConfig
from matching.errors import RiskError

from .fatfinger import FatFingerCheck
from .limits import PositionLimits


class RiskGateway:
    def __init__(self, config: EngineConfig) -> None:
        self.config = config
        self.fatfinger = FatFingerCheck(config.max_order_qty, config.max_notional)
        self.limits = PositionLimits(config.max_position)

    def pre_trade(self, account: str, side: str, price: int, qty: int, positions) -> None:
        self.fatfinger.check(price, qty)
        self.limits.check(account, side, qty, positions)

    def check_self_trade(self, maker_account: str, taker_account: str) -> None:
        if maker_account and taker_account and maker_account == taker_account:
            raise RiskError("self-trade rejected")
