from __future__ import annotations

from typing import List, Optional

from infra.config import EngineConfig
from infra.events import EventBus
from ledger.positions import PositionBook
from ledger.trade_log import TradeLedger
from marketdata.quote_cache import QuoteCache
from marketdata.publisher import QuotePublisher
from risk.checks import RiskGateway

from .book import OrderBook
from .errors import ValidationError
from .models import Order, Trade


class MatchingService:
    def __init__(
        self,
        config: Optional[EngineConfig] = None,
        bus: Optional[EventBus] = None,
    ) -> None:
        self.config = config or EngineConfig()
        self.bus = bus or EventBus()
        self.risk = RiskGateway(self.config)
        self.book = OrderBook(risk=self.risk)
        self.positions = PositionBook()
        self.ledger = TradeLedger()
        self.quotes = QuoteCache(self.book)
        self.publisher = QuotePublisher(self.quotes, self.bus)

    def submit(
        self,
        order_id: str,
        account: str,
        side: str,
        price: int,
        qty: int,
        order_type: str = "limit",
        display_qty: Optional[int] = None,
        event_id: Optional[str] = None,
    ) -> List[Trade]:
        if side not in ("buy", "sell"):
            raise ValidationError("side must be 'buy' or 'sell'")
        if order_type not in ("limit", "iceberg", "post_only"):
            raise ValidationError("unsupported order type")
        if price <= 0 or qty <= 0:
            raise ValidationError("price and qty must be positive")
        order = Order(
            order_id,
            account,
            side,
            price,
            qty,
            order_type=order_type,
            display_qty=display_qty or self.config.default_display_qty,
        )
        self.risk.pre_trade(account, side, price, qty, self.positions)
        trades = self.book.limit(order)
        captured = []
        for trade in trades:
            if self.ledger.record(trade, event_id=event_id):
                self.positions.apply(trade)
                captured.append(trade)
        self.quotes.invalidate()
        self.publisher.publish_quote()
        return captured

    def cancel(self, order_id: str) -> bool:
        cancelled = self.book.cancel(order_id)
        self.quotes.invalidate()
        return cancelled

    def best_quote(self):
        return self.quotes.best()
