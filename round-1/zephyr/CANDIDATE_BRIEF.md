# Candidate Brief — Subscription Entitlement

You are joining an existing project late in development.

`SubscriptionService` is the entitlement lifecycle for a SaaS product. A subscription starts as a TRIAL with a TTL, becomes ACTIVE once paid, can be SUSPENDED and resumed, and can be CANCELLED. An unpaid trial that runs out of time EXPIRES. Users report cancelled accounts coming back to life, expired trials that still have access, and cancels that run twice.

The intended high-level lifecycle is:

```
TRIAL -> ACTIVE <-> SUSPENDED
   |        \-> CANCELLED
   \--TTL--> EXPIRED
```

Some requirements are intentionally incomplete. Treat the interviewer as the
project manager: ask clarifying questions where behaviour is ambiguous (there is
a list to start from in `PROJECT_MANAGER_NOTES.md`).

You may inspect the source, run and add tests, and modify the implementation. The
same system exists in Python, C++, and Java; pick one (see `SETUP.md`). Most of
the test suite passes. The failing tests are the reported bugs.

## Where the code lives

The same system is implemented three times, once per language:

`python/subscriptions.py` (SubscriptionService), `cpp/subscriptions.hpp`, and `java/Subscriptions.java`.

Shared tests ship with each language. The acceptance tests are the specification.

## Be ready to explain

- your invariants
- the state transitions
- why a bug occurs, and why your fix belongs where you put it
- whether each operation should be idempotent
- the time and space complexity
- what changes in a concurrent or distributed version
