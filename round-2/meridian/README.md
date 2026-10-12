# Calendar Service

Welcome to the team responsible for Blike Moomberg's calendar. Requests arrive from employees, are
scored for relevance, and are scheduled in batches around protected commitments. Times are
timezone-free integer minutes since midnight.

This repository has four reported problems in `tickets/`. Your interviewer will tell you which
ticket to start with. You are not expected to finish every ticket.

You may use the available AI assistant and normal repository tools. Treat the assistant like a
junior developer: establish a plan, inspect its work, run the tests, and retain ownership of the
result.

## Reproduce and test it yourself

This pack ships no tests. The code is the same in `python/`, `cpp/`, and `java/`;
pick one (see [SETUP.md](SETUP.md)). Work from the tickets in `tickets/`: for each,
write a test that reproduces the reported behaviour, confirm it fails, fix the
code, and keep your own test green.

## Repository map

## Repository map

```text
blike_calendar/
  database.py    SQLite persistence (requests + events), find_by_idempotency_key
  directory.py   internal employee lookup
  models.py      domain types (BusinessTier, MeetingRequest, CalendarEvent, RequestStatus)
  scheduler.py   scheduling around protected events; conflict arbitration
  scorer.py      deterministic stand-in for an opaque relevance model
  service.py     request intake (SchedulingService: submit_request, accept, reject)
tests/           shipped regression tests
tickets/         reported work
```

## Product rules already agreed

- intervals are half-open: a meeting ending at 10:00 does not conflict with one starting at 10:00;
- protected calendar commitments cannot be displaced;
- when requests contend, the higher business tier wins; ties go to the earlier submission;
- `submit_request` is idempotent on `(requester_key, idempotency_key)`;
- status flow is PENDING to ACCEPTED or REJECTED, and REJECTED is terminal.
