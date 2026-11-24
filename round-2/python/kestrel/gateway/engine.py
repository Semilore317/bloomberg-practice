from __future__ import annotations

from typing import List, Optional

from infra.clock import Clock
from infra.config import EngineConfig
from infra.events import EventBus
from matching.models import Trade
from matching.service import MatchingService

from .session import SessionLimiter


class Engine:
    def __init__(
        self,
        config: Optional[EngineConfig] = None,
        clock: Optional[Clock] = None,
        bus: Optional[EventBus] = None,
    ) -> None:
        self.config = config or EngineConfig()
        self.clock = clock or Clock()
        self.bus = bus or EventBus()
        self.service = MatchingService(self.config, self.bus)
        self.sessions = SessionLimiter(
            self.config.rate_limit, self.config.rate_window_seconds
        )

    def submit(
        self,
        session: str,
        order_id: str,
        account: str,
        side: str,
        price: int,
        qty: int,
        order_type: str = "limit",
        display_qty: Optional[int] = None,
        event_id: Optional[str] = None,
    ) -> List[Trade]:
        if not self.sessions.allow(session, self.clock.now()):
            return []
        return self.service.submit(
            order_id, account, side, price, qty, order_type, display_qty, event_id
        )

    def cancel(self, order_id: str) -> bool:
        return self.service.cancel(order_id)
