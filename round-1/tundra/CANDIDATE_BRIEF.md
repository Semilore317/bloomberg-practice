# Candidate Brief — LRU Cache with TTL

You are joining an existing project late in development.

`LRUCache` is a capacity-bounded cache with per-entry TTL and least-recently-used eviction. A read should count as a use, expired entries should not be returned, and expired entries should not count toward size. Users report stale values served after expiry, the wrong key evicted under load, and a size that counts dead entries.

The intended high-level lifecycle is:

```
put -> live entry (expires at now+ttl)
   get -> value if live, and the entry becomes most-recently-used
   over capacity -> evict least-recently-used
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

`python/cache.py` (LRUCache), `cpp/cache.hpp`, and `java/Cache.java`.

## Be ready to explain

- your invariants
- the state transitions
- why a bug occurs, and why your fix belongs where you put it
- whether each operation should be idempotent
- the time and space complexity
- what changes in a concurrent or distributed version
