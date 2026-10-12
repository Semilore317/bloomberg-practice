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
