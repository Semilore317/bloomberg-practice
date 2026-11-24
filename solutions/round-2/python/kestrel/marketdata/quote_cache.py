from __future__ import annotations

from typing import Optional, Tuple


class QuoteCache:
    def __init__(self, book) -> None:
        self._book = book
        self._best: Optional[Tuple[Optional[int], Optional[int]]] = None

    def _compute(self):
        return (self._book.best_bid(), self._book.best_ask())

    def best(self):
        if self._best is None:
            self._best = self._compute()
        return self._best

    def invalidate(self) -> None:
        self._best = None
