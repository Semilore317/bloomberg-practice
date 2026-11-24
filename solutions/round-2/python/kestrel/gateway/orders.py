from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class OrderRequest:
    account: str
    side: str
    price: int
    qty: int
    order_type: str = "limit"
    display_qty: Optional[int] = None
