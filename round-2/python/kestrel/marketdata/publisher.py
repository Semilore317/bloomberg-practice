from __future__ import annotations

from infra.events import Event, EventBus


class QuotePublisher:
    def __init__(self, cache, bus: EventBus) -> None:
        self.cache = cache
        self.bus = bus

    def publish_quote(self) -> None:
        event = Event("quote", {"best": self.cache.best()})
        for handler in self.bus.handlers("quote"):
            handler(event)
