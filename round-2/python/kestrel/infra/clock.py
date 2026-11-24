from __future__ import annotations


class Clock:
    """Deterministic clock so time-based rules can be tested exactly."""

    def __init__(self, start: int = 0) -> None:
        self._now = start

    def now(self) -> int:
        return self._now

    def advance(self, seconds: int) -> None:
        self._now += seconds
