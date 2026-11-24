from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EngineConfig:
    max_position: int = 100
    max_order_qty: int = 10_000
    max_notional: int = 10_000_000
    rate_limit: int = 3
    rate_window_seconds: int = 60
    default_display_qty: int = 10
    snapshot_levels: int = 5
