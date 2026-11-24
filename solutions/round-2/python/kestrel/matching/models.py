from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Order:
    order_id: str
    account: str
    side: str
    price: int
    qty: int
    seq: int = 0
    order_type: str = "limit"
    display_qty: Optional[int] = None
    reserve: int = 0


@dataclass(frozen=True)
class Trade:
    maker_id: str
    taker_id: str
    price: int
    qty: int
    maker_account: str = ""
    taker_account: str = ""
