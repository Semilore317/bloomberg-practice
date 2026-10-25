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
write a test that reproduces the reported behaviour, confirm it fails, fix the
code, and keep your own test green.

## Product rules already agreed

- intervals are half-open: a meeting ending at 10:00 does not conflict with one starting at 10:00;
- protected calendar commitments cannot be displaced;
- when requests contend, the higher business tier wins; ties go to the earlier submission;
- `submit_request` is idempotent on `(requester_key, idempotency_key)`;
- status flow is PENDING to ACCEPTED or REJECTED, and REJECTED is terminal.


## How to run

This pack ships no tests. Pick one language and write your own tests to reproduce and verify fixes. See instructions below.

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


## Running tests

Write your own `test.cpp` that includes the headers, then:

```bash
g++ -std=c++17 test.cpp -o test && ./test
```