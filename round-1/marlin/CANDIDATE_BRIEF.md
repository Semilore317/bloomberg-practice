# Candidate Brief — Inventory Reservations

You are joining an existing project late in development.

`InventoryService` reserves stock for a fulfilment system. Units are reserved with a TTL hold, then either committed (shipped) or released back to available stock. Expired holds should return their units automatically. Users report stock counts that drift, holds that ship after they should have expired, and releases that free the same units twice.

The intended high-level lifecycle is:

```
HELD -> COMMITTED
   \-> RELEASED   (also: HELD --TTL expiry--> RELEASED)
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

`python/inventory.py` (InventoryService), `cpp/inventory.hpp`, and `java/Inventory.java`.

## Be ready to explain

- your invariants
- the state transitions
- why a bug occurs, and why your fix belongs where you put it
- whether each operation should be idempotent
- the time and space complexity
- what changes in a concurrent or distributed version
