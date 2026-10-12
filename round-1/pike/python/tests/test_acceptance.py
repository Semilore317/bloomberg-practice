import pytest
from approvals import ApprovalService, DocStatus


def svc():
    return ApprovalService()


def test_submit_is_pending():
    s = svc()
    d = s.submit("spec")
    assert d.status == DocStatus.PENDING


def test_approve_pending():
    s = svc()
    d = s.submit("spec")
    s.approve(d.doc_id)
    assert s.status(d.doc_id) == DocStatus.APPROVED


def test_reject_pending():
    s = svc()
    d = s.submit("spec")
    s.reject(d.doc_id)
    assert s.status(d.doc_id) == DocStatus.REJECTED


def test_withdraw_pending():
    s = svc()
    d = s.submit("spec")
    s.withdraw(d.doc_id)
    assert s.status(d.doc_id) == DocStatus.WITHDRAWN


def test_approve_requires_pending():
    s = svc()
    d = s.submit("spec")
    s.reject(d.doc_id)
    with pytest.raises(ValueError):
        s.approve(d.doc_id)               # approve a rejected doc
    d2 = s.submit("spec2")
    s.approve(d2.doc_id)
    with pytest.raises(ValueError):
        s.approve(d2.doc_id)              # double approve


def test_withdraw_requires_pending():
    s = svc()
    d = s.submit("spec")
    s.approve(d.doc_id)
    with pytest.raises(ValueError):
        s.withdraw(d.doc_id)


def test_reject_requires_pending():
    s = svc()
    d = s.submit("spec")
    s.approve(d.doc_id)
    with pytest.raises(ValueError):
        s.reject(d.doc_id)


def test_pending_count_counts_only_pending():
    s = svc()
    a = s.submit("a")
    s.submit("b")
    s.submit("c")
    s.approve(a.doc_id)
    assert s.pending_count() == 2


def test_unknown_doc_raises():
    s = svc()
    with pytest.raises(ValueError):
        s.approve("nope")
