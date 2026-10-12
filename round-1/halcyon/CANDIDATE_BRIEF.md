# Candidate Brief — Order Lifecycle

You are joining an existing project late in development.

`OrderService` tracks working orders for a trading desk. An order is placed OPEN, filled in one or more executions until it is FILLED, and may be cancelled while it still has open quantity. Users report orders that over-fill, cancelled orders that still show open quantity, and cancels that go through twice.

The intended high-level lifecycle is:

```
OPEN -> PARTIAL -> FILLED
   \-> CANCELLED
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

`python/orders.py` (OrderService, Order), `cpp/orders.hpp`, and `java/Orders.java`.

## Be ready to explain

- your invariants
- the state transitions
- why a bug occurs, and why your fix belongs where you put it
- whether each operation should be idempotent
- the time and space complexity
- what changes in a concurrent or distributed version
