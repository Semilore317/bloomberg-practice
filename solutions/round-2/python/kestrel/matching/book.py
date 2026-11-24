from __future__ import annotations

from typing import List, Optional

from .models import Order, Trade
from .priority import ask_key, bid_key


class OrderBook:
    def __init__(self, risk=None) -> None:
        self._asks: List[Order] = []
        self._bids: List[Order] = []
        self._orders: dict = {}
        self._seq = 0
        self._risk = risk

    def _next_seq(self) -> int:
        self._seq += 1
        return self._seq

    def add(self, order: Order) -> None:
        order.seq = self._next_seq()
        self._orders[order.order_id] = order
        (self._bids if order.side == "buy" else self._asks).append(order)

    def cancel(self, order_id: str) -> bool:
        order = self._orders.get(order_id)
        if order is None:
            return False
        book = self._bids if order.side == "buy" else self._asks
        if order in book:
            book.remove(order)
        return True

    def best_bid(self) -> Optional[int]:
        if not self._bids:
            return None
        return max(o.price for o in self._bids)

    def best_ask(self) -> Optional[int]:
        if not self._asks:
            return None
        return min(o.price for o in self._asks)

    def depth(self, levels: int) -> tuple:
        bids = sorted(self._bids, key=bid_key)[:levels]
        asks = sorted(self._asks, key=ask_key)[:levels]
        return (
            [(o.price, o.qty) for o in bids],
            [(o.price, o.qty) for o in asks],
        )

    def _consume(self, maker: Order, fill: int) -> None:
        maker.qty -= fill
        if maker.order_type == "iceberg" and maker.qty == 0 and maker.reserve:
            maker.qty = min(maker.display_qty, maker.reserve)
            maker.reserve -= maker.qty

    def limit(self, order: Order) -> List[Trade]:
        trades: List[Trade] = []
        remaining = order.qty
        opposite = self._asks if order.side == "buy" else self._bids
        opposite.sort(key=ask_key if order.side == "buy" else bid_key)
        i = 0
        while remaining > 0 and i < len(opposite):
            maker = opposite[i]
            crosses = (
                maker.price <= order.price
                if order.side == "buy"
                else maker.price >= order.price
            )
            if not crosses:
                break
            if self._risk is not None:
                self._risk.check_self_trade(maker.account, order.account)
            fill = min(remaining, maker.qty)
            if fill <= 0:
                break
            trades.append(
                Trade(
                    maker.order_id,
                    order.order_id,
                    maker.price,
                    fill,
                    maker.account,
                    order.account,
                )
            )
            remaining -= fill
            self._consume(maker, fill)
            if maker.qty <= 0:
                opposite.pop(i)
            else:
                i += 1
        if remaining > 0:
            order.qty = remaining
            if order.order_type == "iceberg" and order.display_qty:
                order.reserve = max(0, remaining - order.display_qty)
                order.qty = min(order.display_qty, remaining)
            self.add(order)
        return trades
