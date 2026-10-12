import pytest
from jobs import JobQueue, JobStatus


def q():
    return JobQueue(max_attempts=2)


def test_enqueue_queued():
    j = q().enqueue("p")
    assert j.status == JobStatus.QUEUED


def test_start_runs():
    s = q()
    j = s.enqueue("p")
    s.start(j.job_id)
    assert s.status(j.job_id) == JobStatus.RUNNING
    assert j.attempts == 1


def test_complete_done():
    s = q()
    j = s.enqueue("p")
    s.start(j.job_id)
    s.complete(j.job_id)
    assert s.status(j.job_id) == JobStatus.DONE


def test_fail_requeues_under_budget():
    s = q()
    j = s.enqueue("p")
    s.start(j.job_id)
    s.fail(j.job_id)
    assert s.status(j.job_id) == JobStatus.QUEUED


def test_retry_then_succeed():
    s = q()
    j = s.enqueue("p")
    s.start(j.job_id)
    s.fail(j.job_id)
    s.start(j.job_id)
    s.complete(j.job_id)
    assert s.status(j.job_id) == JobStatus.DONE


def test_fails_after_budget():
    s = q()
    j = s.enqueue("p")
    s.start(j.job_id)
    s.fail(j.job_id)
    s.start(j.job_id)
    s.fail(j.job_id)
    assert s.status(j.job_id) == JobStatus.FAILED


def test_start_requires_queued():
    s = q()
    j = s.enqueue("p")
    s.start(j.job_id)
    with pytest.raises(ValueError):
        s.start(j.job_id)


def test_complete_requires_running():
    s = q()
    j = s.enqueue("p")
    with pytest.raises(ValueError):
        s.complete(j.job_id)


def test_unknown_job_raises():
    s = q()
    with pytest.raises(ValueError):
        s.start("nope")
