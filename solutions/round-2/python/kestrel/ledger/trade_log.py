from __future__ import annotations

from typing import Any, List, Tuple

from matching.models import Trade


class TradeLedger:
    def __init__(self) -> None:
        self._entries: List[Tuple[Any, Trade]] = []
        self._seen: set = set()

    def record(self, trade: Trade, event_id: Any = None) -> bool:
        if event_id is not None and event_id in self._seen:
            return False
        if event_id is not None:
            self._seen.add(event_id)
        self._entries.append((event_id, trade))
        return True

    def trades(self) -> List[Trade]:
        return [trade for _, trade in self._entries]

    def entries(self) -> List[Tuple[Any, Trade]]:
        return list(self._entries)
