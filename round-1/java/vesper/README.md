# vesper - Connection Pool

`ConnectionPool` is a fixed-capacity connection pool.

You are joining this codebase late, and something in it is wrong. Users report pools that grow past their capacity, connections released twice, and a closed pool that still hands out connections. Your job is
to find the bug or bugs behind that, fix them, and prove each fix with a test you
write yourself. This pack ships no tests.

## Scope

In scope:

- find and fix the defects behind the reported symptom;
- write your own tests to confirm each defect and each fix;
- keep all existing, correct behaviour working.

Out of scope:

- redesigning the component or changing its public API;
- adding features the brief did not ask for;
- performance work, unless a defect is itself a performance bug.

Time budget: about 35 minutes.

## Start here

1. `CANDIDATE_BRIEF.md`: the system, the lifecycle, and what to be ready to explain.
2. `PROJECT_MANAGER_NOTES.md`: questions to ask before you change behaviour.
3. `SETUP.md`: how to run the tests you write, in Python, C++, or Java.
4. `SELF_REVIEW_AFTER.md`: read only after you finish.


---

# Task Description (from brief)

# Candidate Brief - Connection Pool

You are joining an existing project late in development.

`ConnectionPool` is a fixed-capacity connection pool. acquire() hands out an idle connection or opens a new one up to the capacity; release() returns one to the idle set; a closed pool hands out nothing. Users report pools that grow past their capacity, connections released twice, and a closed pool that still hands out connections.

The intended high-level lifecycle is:

```
(new) -> IN_USE <-> IDLE
   close() -> pool refuses new acquires
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

`python/pool.py` (ConnectionPool, Connection), `cpp/pool.hpp`, and `java/Pool.java`.

## Be ready to explain

- your invariants
- the state transitions
- why a bug occurs, and why your fix belongs where you put it
- whether each operation should be idempotent
- the time and space complexity
- what changes in a concurrent or distributed version


---

# Project Manager Notes (questions to ask)

# Project Manager Notes - Connection Pool

Do not read this until after your first pass.

These are the questions a strong candidate asks before and during the fix. The
interviewer is playing the project manager, so some answers are judgement calls,
not facts in the code.

- What should acquiring from a closed pool do?
- Can the pool ever exceed its capacity?
- What should releasing an already-idle connection do?
- What invariant holds for in-use plus idle versus capacity?
- Should close drain or forcibly close in-use connections?
- Is acquire/release safe under concurrent callers?


---

# Setup and Test Instructions

# Setup

This pack ships no tests, on purpose. Read the reported symptom, form a hypothesis
about what is wrong, and write your own tests to confirm it before you change
anything. The same service exists in Python, C++, and Java; pick one. No external
dependencies, services, API keys, or network.

## Python 3.9+

Write test files named `test_*.py` in `python/` (a `conftest.py` is already there
so your imports resolve), then:

```bash
cd python && pytest -q
```

## C++ (g++ with -std=c++17)

The implementation is header-only. Write your own `test.cpp` that includes the
header, then:

```bash
cd cpp && g++ -std=c++17 test.cpp -o test && ./test
```

## Java (JDK 11+)

Write your own `Check.java` with a `main` that exercises the classes, then:

```bash
cd java && javac *.java && java Check
```
