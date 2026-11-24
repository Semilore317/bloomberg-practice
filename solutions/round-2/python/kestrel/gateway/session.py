from __future__ import annotations

from typing import Dict, List


class SessionLimiter:
    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit = limit
        self.window = window_seconds
        self._hits: Dict[str, List[int]] = {}

    def allow(self, key: str, now: int) -> bool:
        hits = [t for t in self._hits.get(key, []) if now - t < self.window]
        self._hits[key] = hits
        if len(hits) >= self.limit:
            return False
        hits.append(now)
        return True
