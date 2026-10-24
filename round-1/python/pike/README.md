# pike - Document Approval Workflow

`ApprovalService` is a document approval workflow.

You are joining this codebase late, and something in it is wrong. Users report documents that get approved after being rejected, documents withdrawn after a decision, and a pending count that never goes down. Your job is
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

# Candidate Brief - Document Approval Workflow

You are joining an existing project late in development.

`ApprovalService` is a document approval workflow. A submitted document is PENDING, and from there it can be approved, rejected, or withdrawn by its author. Those are terminal decisions. Users report documents that get approved after being rejected, documents withdrawn after a decision, and a pending count that never goes down.

The intended high-level lifecycle is:

```
PENDING -> APPROVED
   |-> REJECTED
   \-> WITHDRAWN
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

`python/approvals.py` (ApprovalService, Document), `cpp/approvals.hpp`, and `java/Approvals.java`.

## Be ready to explain

- your invariants
- the state transitions
- why a bug occurs, and why your fix belongs where you put it
- whether each operation should be idempotent
- the time and space complexity
- what changes in a concurrent or distributed version


---

# Project Manager Notes (questions to ask)

# Project Manager Notes - Document Approval Workflow

Do not read this until after your first pass.

These are the questions a strong candidate asks before and during the fix. The
interviewer is playing the project manager, so some answers are judgement calls,
not facts in the code.

- What should approving a rejected document do?
- Can a document be withdrawn after it is decided?
- Does the pending count include decided documents?
- Are approve, reject, and withdraw all terminal?
- What should a second approve do?
- Should reject and withdraw be guarded the same way as approve?


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
