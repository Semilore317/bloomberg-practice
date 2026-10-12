from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Callable
import time


class TokenStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"


@dataclass
class Token:
    token_id: str
    user_id: str
    status: TokenStatus
    expires_at: float | None


class TokenStore:
    """Issues short-lived access tokens. A token is valid while it is ACTIVE and
    unexpired. It can be refreshed to extend its life, or revoked."""

    def __init__(self, ttl_seconds: int = 60, clock: Callable[[], float] = time.time) -> None:
        self._tokens: dict[str, Token] = {}
        self._ttl = ttl_seconds
        self._clock = clock
        self._seq = 0

    def issue(self, user_id: str) -> Token:
        self._seq += 1
        tid = f"T{self._seq}"
        tok = Token(tid, user_id, TokenStatus.ACTIVE, self._clock() + self._ttl)
        self._tokens[tid] = tok
        return tok

    def validate(self, token_id: str) -> bool:
        tok = self._tokens.get(token_id)
        if tok is None:
            return False
        # BUG: ignores expiry, so an expired token still validates
        return tok.status == TokenStatus.ACTIVE

    def refresh(self, token_id: str) -> Token:
        tok = self._get(token_id)
        if tok.status != TokenStatus.ACTIVE:
            raise ValueError("cannot refresh a revoked token")
        # BUG: does not check expiry, so an expired token can be refreshed back to life
        tok.expires_at = self._clock() + self._ttl
        return tok

    def revoke(self, token_id: str) -> Token:
        tok = self._get(token_id)
        # BUG: no terminal guard, a revoked token can be revoked again
        tok.status = TokenStatus.REVOKED
        tok.expires_at = None
        return tok

    def _get(self, token_id: str) -> Token:
        tok = self._tokens.get(token_id)
        if tok is None:
            raise ValueError("token not found")
        return tok
