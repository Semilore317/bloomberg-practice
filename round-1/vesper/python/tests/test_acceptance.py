import pytest
from pool import ConnectionPool, ConnStatus


def test_acquire_marks_in_use():
    p = ConnectionPool(2)
    p.acquire()
    assert p.in_use_count() == 1


def test_release_returns_to_idle():
    p = ConnectionPool(2)
    c = p.acquire()
    p.release(c.conn_id)
    assert p.idle_count() == 1
    assert p.in_use_count() == 0


def test_reacquire_reuses_idle():
    p = ConnectionPool(2)
    c = p.acquire()
    p.release(c.conn_id)
    p.acquire()
    assert p.size() == 1


def test_two_acquires_distinct():
    p = ConnectionPool(2)
    a = p.acquire()
    b = p.acquire()
    assert a.conn_id != b.conn_id
    assert p.in_use_count() == 2


def test_capacity_enforced():
    p = ConnectionPool(2)
    p.acquire()
    p.acquire()
    with pytest.raises(ValueError):
        p.acquire()


def test_release_requires_in_use():
    p = ConnectionPool(2)
    c = p.acquire()
    p.release(c.conn_id)
    with pytest.raises(ValueError):
        p.release(c.conn_id)


def test_no_acquire_after_close():
    p = ConnectionPool(2)
    p.close()
    with pytest.raises(ValueError):
        p.acquire()


def test_release_unknown_raises():
    p = ConnectionPool(2)
    with pytest.raises(ValueError):
        p.release("nope")


def test_release_frees_capacity():
    p = ConnectionPool(1)
    a = p.acquire()
    p.release(a.conn_id)
    p.acquire()
    assert p.in_use_count() == 1
