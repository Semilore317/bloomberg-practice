from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ConnStatus(str, Enum):
    IN_USE = "in_use"
    IDLE = "idle"


@dataclass
class Connection:
    conn_id: str
    status: ConnStatus


class ConnectionPool:
    """A fixed-capacity connection pool. acquire() hands out an idle connection or
    opens a new one up to the capacity; release() returns one to the idle set.
    A closed pool hands out nothing."""

    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._conns: dict[str, Connection] = {}
        self._closed = False
        self._seq = 0

    def acquire(self) -> Connection:
        for c in self._conns.values():
            if c.status == ConnStatus.IDLE:
                c.status = ConnStatus.IN_USE
                return c
        self._seq += 1
        cid = f"C{self._seq}"
        c = Connection(cid, ConnStatus.IN_USE)
        self._conns[cid] = c
        return c

    def release(self, conn_id: str) -> Connection:
        c = self._get(conn_id)
        c.status = ConnStatus.IDLE
        return c

    def close(self) -> None:
        self._closed = True

    def in_use_count(self) -> int:
        return sum(1 for c in self._conns.values() if c.status == ConnStatus.IN_USE)

    def idle_count(self) -> int:
        return sum(1 for c in self._conns.values() if c.status == ConnStatus.IDLE)

    def size(self) -> int:
        return len(self._conns)

    def _get(self, conn_id: str) -> Connection:
        c = self._conns.get(conn_id)
        if c is None:
            raise ValueError("connection not found")
        return c
