# Candidate Brief - Job State Machine

You are joining an existing project late in development.

`JobQueue` is a job state machine. A job is QUEUED, then RUNNING once started. From RUNNING it either completes (DONE) or fails. A failure retries (back to QUEUED) until the attempt budget is spent, then the job is FAILED. Users report jobs that start twice, jobs completed while not running, and jobs that retry one time too many.

The intended high-level lifecycle is:

```
QUEUED -> RUNNING -> DONE
   RUNNING --fail, budget left--> QUEUED
   RUNNING --fail, budget spent--> FAILED
```

Some requirements are intentionally incomplete. Treat the interviewer as the
project manager: ask clarifying questions where behaviour is ambiguous (there is
a list to start from in `PROJECT_MANAGER_NOTES.md`).

You may inspect the source, modify the implementation, and add your own tests. The
same system exists in Python, C++, and Java; pick one (see `SETUP.md`).

This pack ships no tests. Reproduce the reported symptom with a test you write,
confirm your hypothesis, then fix the code and keep your own tests green.

## Where the code lives

The same system is implemented three times, once per language:

`python/jobs.py` (JobQueue, Job), `cpp/jobs.hpp`, and `java/Jobs.java`.

## Be ready to explain

- your invariants
- the state transitions
- why a bug occurs, and why your fix belongs where you put it
- whether each operation should be idempotent
- the time and space complexity
- what changes in a concurrent or distributed version
