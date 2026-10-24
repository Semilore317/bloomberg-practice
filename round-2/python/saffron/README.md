# Session Service

Welcome to the team that owns sessions. A session store keeps sessions keyed by id; an expiry
policy decides when a session is dead; sessions can be refreshed and expired ones cleaned up.
Times are integer ticks.

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
sessions/
  models.py    domain types (Session: sid, expiry, data)
  errors.py    SessionError
  expiry.py    ExpiryPolicy: is_expired(session, now)
  store.py     SessionStore: put / get / delete / all / size
  service.py   SessionService: create / get / touch / cleanup / size
tests/         shipped regression tests
tickets/       reported work
```

## Product rules already agreed

- a session is expired once the clock reaches its expiry tick: `now >= expiry`;
- a valid `get` returns the session data; an expired one returns nothing;
- `touch` extends a session's life to `now + ttl`;
- `cleanup` reclaims expired sessions so the store does not grow without bound.


---

# Tickets

## SESS-12-boundary.md

# SESS-12: Sessions live one tick too long

## Report

A session is still considered valid at exactly its expiry tick. The policy should treat a session
as expired once `now >= expiry`, but it uses a strict greater-than, so sessions survive one tick
past their deadline.

## Acceptance criteria

- a session created at 0 with ttl 10 is expired at `now == 10`;
- a session is still valid at `now == 9`;
- the boundary rule lives in the expiry policy, not scattered at call sites;
- add a test that asserts expiry at exactly the expiry tick.

Do not change `touch` or `cleanup` as part of this ticket.


## SESS-18-refresh.md

# SESS-18: touch does not extend a session

## Report

Active users are being logged out on schedule even though they are still using the app. `touch`
is a no-op, so a session never gets its life extended.

## Acceptance criteria

- after `touch(sid, now, ttl)`, the session is valid until `now + ttl`;
- touching an unknown session id is a no-op, not an error;
- a touched session that later passes its new expiry is still expired;
- add a test that touches a session and asserts it survives past its original expiry.

Do not change the expiry boundary rule as part of this ticket.


## SESS-24-cleanup.md

# SESS-24: Expired sessions are never reclaimed

## Report

The session store grows without bound. `cleanup` does nothing, so expired sessions accumulate and
leak memory over time.

## Acceptance criteria

- `cleanup(now)` removes every session with `now >= expiry`;
- sessions that are not yet expired are kept;
- the store size reflects only live sessions after cleanup;
- add a test that creates a session, cleans up at its expiry, and asserts it is gone and size is 0.

Do not change the expiry boundary rule as part of this ticket.




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
