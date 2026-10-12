# Candidate Brief — Document Approval Workflow

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
