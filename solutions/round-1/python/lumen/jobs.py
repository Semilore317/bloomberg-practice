from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


@dataclass
class Job:
    job_id: str
    payload: str
    status: JobStatus
    attempts: int


class JobQueue:
    """A job state machine. A job is QUEUED, then RUNNING once started. From
    RUNNING it either completes (DONE) or fails. A failure retries (back to
    QUEUED) until the attempt budget is spent, then the job is FAILED."""

    def __init__(self, max_attempts: int = 2) -> None:
        self._jobs: dict[str, Job] = {}
        self._max = max_attempts
        self._seq = 0

    def enqueue(self, payload: str) -> Job:
        self._seq += 1
        jid = f"J{self._seq}"
        job = Job(jid, payload, JobStatus.QUEUED, 0)
        self._jobs[jid] = job
        return job

    def start(self, job_id: str) -> Job:
        # Only a QUEUED job may start. This rejects duplicate starts of RUNNING
        # jobs and rejects reopening DONE or FAILED jobs. The guard runs before
        # attempts is incremented, so a rejected start consumes no attempt.
        job = self._get(job_id)
        if job.status != JobStatus.QUEUED:
            raise ValueError("only queued jobs can start")
        job.status = JobStatus.RUNNING
        job.attempts += 1
        return job

    def complete(self, job_id: str) -> Job:
        # Only a RUNNING job may complete; QUEUED, DONE, and FAILED jobs are
        # rejected. attempts is unchanged because it counts starts, not
        # completions.
        job = self._get(job_id)
        if job.status != JobStatus.RUNNING:
            raise ValueError("only running jobs can complete")
        job.status = JobStatus.DONE
        return job

    def fail(self, job_id: str) -> Job:
        # Only a RUNNING job may fail.
        job = self._get(job_id)
        if job.status != JobStatus.RUNNING:
            raise ValueError("only running jobs can fail")
        # attempts already includes the attempt that just failed. Retry while
        # attempts is below max_attempts; FAILED is reached when attempts equals
        # max_attempts. With the default max_attempts=2, the second failure
        # marks the job FAILED.
        if job.attempts < self._max:
            job.status = JobStatus.QUEUED
        else:
            job.status = JobStatus.FAILED
        return job

    def status(self, job_id: str) -> JobStatus:
        return self._get(job_id).status

    def _get(self, job_id: str) -> Job:
        job = self._jobs.get(job_id)
        if job is None:
            raise ValueError("job not found")
        return job
