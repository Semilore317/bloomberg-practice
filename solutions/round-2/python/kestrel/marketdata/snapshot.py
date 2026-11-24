from __future__ import annotations

from typing import Dict, List, Tuple


def depth_snapshot(book, levels: int) -> Dict[str, List[Tuple[int, int]]]:
    bids, asks = book.depth(levels)
    return {"bids": bids, "asks": asks}
