# Job Orchestration Service

Welcome to the team that runs background work. Jobs enter a FIFO ready queue; a registry tracks
each job's status and attempt count; a dispatcher hands work out, retries failures, and
dead-letters anything that fails too many times.

This repository has three reported problems in `tickets/`. Your interviewer will tell you which
ticket to start with. You are not expected to finish every ticket.

You may use the available AI assistant and normal repository tools. Treat the assistant like a
junior developer: establish a plan, inspect its work, run the tests, and retain ownership of the
result.

## Scope

In scope: work the tickets in `tickets/`, fixing the defects they report and
confirming each with a test you write. Keep all existing, correct behaviour working.

Out of scope: redesigning the services, changing public APIs, or adding features no
ticket asks for.

Time budget: about 45 minutes.

## Reproduce and test it yourself

This pack ships no tests. The code is the same in `python/`, `cpp/`, and `java/`;
pick one (see [SETUP.md](SETUP.md)). Work from the tickets in `tickets/`: for each,
write a test that reproduces the reported behaviour, confirm it fails, fix the
code, and keep your own test green.

## Repository map

## Repository map

```text
orchestration/
  models.py      domain types (Job, JobStatus)
  errors.py      UnknownJob
  queue.py       the FIFO ready queue (push / pop / peek / remove)
  registry.py    per-job status and attempt tracking
  dispatcher.py  dequeue / ack / nack / dead_letters
  service.py     OrchestrationService: enqueue / dequeue / ack / nack
tests/           shipped regression tests
tickets/         reported work
```

## Product rules already agreed

- a dequeued job is removed from the ready queue and must not be handed out again while in flight;
- `ack` completes a job and takes it out of circulation;
- `nack` records a failed attempt and re-queues, until the job has been attempted `max_retries`
  times, at which point it is dead-lettered rather than re-queued.


---

# Tickets

## APT-410-redelivery.md

# APT-410: Jobs are handed out repeatedly

## Report

Workers keep processing the same job. `dequeue` returns a job but does not remove it from the
ready queue or mark it in flight, so several workers pick up the same work at once.

## Acceptance criteria

- a dequeued job is removed from the ready queue;
- the next `dequeue` returns a different job, or `None` when the queue is empty;
- the dequeued job is marked in flight in the registry;
- add a test that enqueues one job and asserts the second `dequeue` returns `None`.

Do not change the retry or dead-letter logic as part of this ticket.


## APT-415-ack-redelivery.md

# APT-415: Acked jobs can be handed out again

## Report

A completed job can still be dequeued. After `ack`, a job should be out of circulation; instead it
can be redelivered and processed twice.

## Acceptance criteria

- after `ack`, `dequeue` never returns that job again;
- the job's status reflects completion;
- acking a job that is not in flight does not corrupt the queue;
- add a test that enqueues, dequeues, acks, and asserts the next `dequeue` is `None`.

Do not change the retry or dead-letter logic as part of this ticket.


## APT-421-retries.md

# APT-421: Retry count never advances; nothing dead-letters

## Report

A failing job retries forever and never reaches the dead-letter list. `nack` does not advance the
attempt count, and the dead-letter threshold is off by one, so the limit is never hit.

## Acceptance criteria

- each `nack` advances the job's attempt count by one;
- with `max_retries=N`, the Nth `nack` moves the job to the dead-letter list instead of re-queueing;
- a job below the limit is re-queued and can be dispatched again;
- add tests at `max_retries=1` and `max_retries=2` asserting the job dead-letters on the Nth nack.

Do not change the dequeue path as part of this ticket.




---

# Setup and Test Instructions

# Setup

This pack ships no tests, on purpose. Read the tickets, form a hypothesis about
what is wrong, and write your own tests to confirm it before you change anything.
The same service exists in Python, C++, and Java; pick one.

## Python 3.9+

Write test files named `test_*.py` under `python/` (a `conftest.py` is already
there so your imports resolve), then:

```bash
cd python && pytest -q
```

## C++ (g++ with -std=c++17)

The implementation is header-only. Write your own `test.cpp` that includes the
headers, then:

```bash
cd cpp && g++ -std=c++17 test.cpp -o test && ./test
```

## Java (JDK 11+)

Write your own `Check.java` with a `main` that exercises the classes, then:

```bash
cd java && javac *.java && java Check
```
