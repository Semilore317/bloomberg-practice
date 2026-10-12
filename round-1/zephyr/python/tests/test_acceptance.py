import pytest
from subscriptions import SubscriptionService, SubStatus


class FakeClock:
    def __init__(self, v=1000.0):
        self.v = v
    def __call__(self):
        return self.v
    def advance(self, s):
        self.v += s


def svc(clock=None):
    return SubscriptionService(trial_ttl_seconds=60, clock=clock or FakeClock())


def test_trial_is_entitled():
    s = svc()
    sub = s.start_trial("u1")
    assert sub.status == SubStatus.TRIAL
    assert s.is_entitled(sub.sub_id) is True


def test_activate_makes_active():
    s = svc()
    sub = s.start_trial("u1")
    s.activate(sub.sub_id)
    assert sub.status == SubStatus.ACTIVE
    assert s.is_entitled(sub.sub_id) is True


def test_suspend_removes_entitlement():
    s = svc()
    sub = s.start_trial("u1")
    s.activate(sub.sub_id)
    s.suspend(sub.sub_id)
    assert s.is_entitled(sub.sub_id) is False


def test_resume_restores_entitlement():
    s = svc()
    sub = s.start_trial("u1")
    s.activate(sub.sub_id)
    s.suspend(sub.sub_id)
    s.resume(sub.sub_id)
    assert s.is_entitled(sub.sub_id) is True


def test_cancel_removes_entitlement():
    s = svc()
    sub = s.start_trial("u1")
    s.activate(sub.sub_id)
    s.cancel(sub.sub_id)
    assert s.is_entitled(sub.sub_id) is False


def test_cancelled_cannot_be_reactivated():
    s = svc()
    sub = s.start_trial("u1")
    s.cancel(sub.sub_id)
    with pytest.raises(ValueError):
        s.activate(sub.sub_id)


def test_double_cancel_rejected():
    s = svc()
    sub = s.start_trial("u1")
    s.cancel(sub.sub_id)
    with pytest.raises(ValueError):
        s.cancel(sub.sub_id)


def test_expired_trial_not_entitled():
    c = FakeClock()
    s = svc(c)
    sub = s.start_trial("u1")
    c.advance(61)
    assert s.is_entitled(sub.sub_id) is False


def test_active_survives_trial_ttl():
    c = FakeClock()
    s = svc(c)
    sub = s.start_trial("u1")
    s.activate(sub.sub_id)
    c.advance(1000)
    assert s.is_entitled(sub.sub_id) is True


def test_expired_trial_cannot_be_activated():
    c = FakeClock()
    s = svc(c)
    sub = s.start_trial("u1")
    c.advance(61)
    with pytest.raises(ValueError):
        s.activate(sub.sub_id)
