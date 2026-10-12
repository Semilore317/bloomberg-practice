import pytest
from tokens import TokenStore, TokenStatus


class FakeClock:
    def __init__(self, v=1000.0):
        self.v = v
    def __call__(self):
        return self.v
    def advance(self, s):
        self.v += s


def store(clock=None):
    return TokenStore(ttl_seconds=60, clock=clock or FakeClock())


def test_issued_token_validates():
    s = store()
    t = s.issue("u1")
    assert s.validate(t.token_id) is True


def test_revoke_invalidates():
    s = store()
    t = s.issue("u1")
    s.revoke(t.token_id)
    assert s.validate(t.token_id) is False


def test_refresh_extends_lifetime():
    c = FakeClock()
    s = store(c)
    t = s.issue("u1")
    c.advance(40)
    s.refresh(t.token_id)
    c.advance(40)                 # 80 total: past original 60, within refreshed 100
    assert s.validate(t.token_id) is True


def test_unknown_token_invalid():
    s = store()
    assert s.validate("nope") is False


def test_refresh_returns_active():
    s = store()
    t = s.issue("u1")
    r = s.refresh(t.token_id)
    assert r.status == TokenStatus.ACTIVE


def test_revoked_cannot_refresh():
    s = store()
    t = s.issue("u1")
    s.revoke(t.token_id)
    with pytest.raises(ValueError):
        s.refresh(t.token_id)


def test_double_revoke_rejected():
    s = store()
    t = s.issue("u1")
    s.revoke(t.token_id)
    with pytest.raises(ValueError):
        s.revoke(t.token_id)


def test_expired_token_invalid():
    c = FakeClock()
    s = store(c)
    t = s.issue("u1")
    c.advance(61)
    assert s.validate(t.token_id) is False


def test_expired_token_cannot_refresh():
    c = FakeClock()
    s = store(c)
    t = s.issue("u1")
    c.advance(61)
    with pytest.raises(ValueError):
        s.refresh(t.token_id)
