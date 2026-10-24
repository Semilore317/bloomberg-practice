# Calendar Service

Welcome to the team responsible for Blike Moomberg's calendar. Requests arrive from employees, are
scored for relevance, and are scheduled in batches around protected commitments. Times are
timezone-free integer minutes since midnight.

This repository has four reported problems in `tickets/`. Your interviewer will tell you which
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


---

# Tickets

## CAL-TICKET-duplicate-request.md

# CAL-TICKET: duplicate request after retry

## Report

Occasionally the same meeting request appears twice. It is most common when the requester's
connection is unstable and the client retries before receiving a response. Slow, sequential
retries normally return the original request, so a naive sequential test can pass while the real
problem remains.

## Acceptance criteria

- one requester and idempotency key produce exactly one stored request;
- overlapping submissions return the same request id rather than an internal error;
- the same idempotency key may be used by two different requesters;
- the fast existing lookup may remain, but correctness cannot depend on its timing;
- add a test that sends overlapping submissions, not merely sequential calls.

Do not redesign scheduling or relevance scoring as part of this ticket.


## CAL-TICKET-overlap-arbitration.md

# CAL-TICKET: meetings booked over protected commitments

## Report

Employees are being double-booked: a scheduled meeting lands in a slot already held by a protected
calendar event. Requests are supposed to be scheduled in batches *around* protected commitments,
never on top of them.

## Acceptance criteria

- `schedule_batch` never accepts a request that overlaps a protected event;
- half-open intervals hold: a request ending when a protected block starts is fine;
- the invariant holds regardless of the order requests are considered;
- add a test with one protected event and a request that overlaps it.

State the overlap invariant in your own words before changing code. Do not change the scoring
model as part of this ticket.


## CAL-TICKET-scorer-failure.md

# CAL-TICKET: high-tier requests lose their slot

## Report

Executive assistants report that a STANDARD request sometimes wins a slot over an EXECUTIVE one.
Scheduling is meant to prefer the higher business tier, breaking ties in favour of the earlier
submission. The relevance scorer is a deterministic stand-in; the ranking it produces is what the
scheduler consumes.

## Acceptance criteria

- among requests contending for a slot, the higher `business_tier` is scheduled first;
- equal tiers are ordered by earlier `submitted_at`;
- the fix lives in the ranking, not in a special case inside the scheduler loop;
- add a test where an EXECUTIVE and a STANDARD request contend and the EXECUTIVE wins.

Do not change persistence or the request intake path as part of this ticket.


## CAL-TICKET-terminal-status.md

# CAL-TICKET: rejected requests can be re-accepted

## Report

Audit found requests that moved from REJECTED back to ACCEPTED with no error. A rejection is
final; once a request is rejected it must stay rejected.

## Acceptance criteria

- accepting a request that is already REJECTED raises a clear error;
- the request's status is left unchanged when the transition is refused;
- valid transitions (PENDING to ACCEPTED or REJECTED) still work;
- add a test that rejects a request and then asserts accept raises.

Do not change the scheduler or scorer as part of this ticket.




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
