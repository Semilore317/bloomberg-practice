# Candidate Brief — Rate Limiter

You are joining an existing project late in development.

`RateLimiter` is a fixed-window per-key rate limiter. Each key may be allowed up to `limit` times per window, and the count resets when the window elapses. Users report keys that stay blocked forever after their first burst, remaining counts that never recover, and a reset that does nothing.

The intended high-level lifecycle is:

```
window open -> count rises to limit -> blocked
   \--window elapses--> fresh window, count 0
```

Some requirements are intentionally incomplete. Treat the interviewer as the
project manager: ask clarifying questions where behaviour is ambiguous (there is
a list to start from in `PROJECT_MANAGER_NOTES.md`).

You may inspect the source, run and add tests, and modify the implementation. The
same system exists in Python, C++, and Java; pick one (see `SETUP.md`). Most of
the test suite passes. The failing tests are the reported bugs.

## Where the code lives

The same system is implemented three times, once per language:

`python/ratelimit.py` (RateLimiter), `cpp/ratelimit.hpp`, and `java/RateLimit.java`.

Shared tests ship with each language. The acceptance tests are the specification.

## Be ready to explain

- your invariants
- the state transitions
- why a bug occurs, and why your fix belongs where you put it
- whether each operation should be idempotent
- the time and space complexity
- what changes in a concurrent or distributed version
