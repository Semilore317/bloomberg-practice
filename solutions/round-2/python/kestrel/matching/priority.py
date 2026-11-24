from __future__ import annotations

from .models import Order


def ask_key(order: Order):
    return (order.price, order.seq)


def bid_key(order: Order):
    return (-order.price, order.seq)
