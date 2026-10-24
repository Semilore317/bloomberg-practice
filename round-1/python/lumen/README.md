# lumen - Job State Machine

`JobQueue` is a job state machine.

You are joining this codebase late, and something in it is wrong. Users report jobs that start twice, jobs completed while not running, and jobs that retry one time too many. Your job is
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


---

# Project Manager Notes (questions to ask)

# Project Manager Notes - Job State Machine

Do not read this until after your first pass.

These are the questions a strong candidate asks before and during the fix. The
interviewer is playing the project manager, so some answers are judgement calls,
not facts in the code.

- What should starting an already-running job do?
- Can a job be completed while it is not running?
- After how many attempts should a job become FAILED?
- Does the attempt count increment on start, or on fail?
- Is start idempotent if a worker retries it?
- Should a DONE or FAILED job be truly terminal?


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
