from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List

Handler = Callable[["Event"], None]


@dataclass(frozen=True)
class Event:
    topic: str
    payload: Dict[str, Any] = field(default_factory=dict)


class EventBus:
    def __init__(self) -> None:
        self._handlers: Dict[str, List[Handler]] = {}
        self._published: List[Event] = []

    def subscribe(self, topic: str, handler: Handler) -> None:
        self._handlers.setdefault(topic, []).append(handler)

    def handlers(self, topic: str) -> List[Handler]:
        return list(self._handlers.get(topic, []))

    def publish(self, event: Event) -> None:
        self._published.append(event)
        for handler in self.handlers(event.topic):
            try:
                handler(event)
            except Exception:
                pass

    def published(self) -> List[Event]:
        return list(self._published)
