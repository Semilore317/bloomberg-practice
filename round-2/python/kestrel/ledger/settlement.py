from __future__ import annotations

from matching.models import Trade


def cash_delta(trade: Trade, account: str) -> int:
    """Signed cash movement for an account on a trade."""
    if account == trade.taker_account:
        return -trade.price * trade.qty
    if account == trade.maker_account:
        return trade.price * trade.qty
    return 0
