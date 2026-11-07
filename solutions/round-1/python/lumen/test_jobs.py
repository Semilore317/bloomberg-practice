import pytest

from jobs import JobQueue, JobStatus


def test_start_twice_is_rejected():
    """A job already RUNNING must not be started a second time."""
    q = JobQueue()
    job = q.enqueue("payload")

    q.start(job.job_id)

    with pytest.raises(ValueError):
        q.start(job.job_id)

    # The rejected start must not change state or consume another attempt.
    assert q.status(job.job_id) == JobStatus.RUNNING
    assert job.attempts == 1


def test_complete_without_start_is_rejected():
    """A QUEUED job that never ran must not be completed."""
    q = JobQueue()
    job = q.enqueue("payload")

    with pytest.raises(ValueError):
        q.complete(job.job_id)

    assert q.status(job.job_id) == JobStatus.QUEUED
    assert job.attempts == 0


def test_job_fails_after_exactly_max_attempts():
    """With max_attempts=2, the second failure must mark the job FAILED."""
    q = JobQueue(max_attempts=2)
    job = q.enqueue("payload")

    # First attempt fails and goes back to QUEUED.
    q.start(job.job_id)
    q.fail(job.job_id)
    assert q.status(job.job_id) == JobStatus.QUEUED

    # Second attempt fails; the budget is now spent.
    q.start(job.job_id)
    q.fail(job.job_id)

    assert job.attempts == 2
    assert q.status(job.job_id) == JobStatus.FAILED
