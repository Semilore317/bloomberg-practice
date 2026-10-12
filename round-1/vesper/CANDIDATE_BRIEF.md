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
