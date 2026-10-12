# Candidate Brief — Access Token Store

You are joining an existing project late in development.

`TokenStore` issues short-lived access tokens. A token is valid while it is ACTIVE and unexpired. It can be refreshed to extend its life, or revoked. Users report expired tokens that still pass validation, expired tokens that can be refreshed back to life, and revokes that run twice.

The intended high-level lifecycle is:

```
ACTIVE --refresh--> ACTIVE (new expiry)
   |--revoke--> REVOKED
   \--TTL--> expired (still ACTIVE status, but invalid)
```

Some requirements are intentionally incomplete. Treat the interviewer as the
project manager: ask clarifying questions where behaviour is ambiguous (there is
a list to start from in `PROJECT_MANAGER_NOTES.md`).

You may inspect the source, run and add tests, and modify the implementation. The
same system exists in Python, C++, and Java; pick one (see `SETUP.md`). Most of
the test suite passes. The failing tests are the reported bugs.

## Where the code lives

The same system is implemented three times, once per language:

`python/tokens.py` (TokenStore, Token), `cpp/tokens.hpp`, and `java/Tokens.java`.

Shared tests ship with each language. The acceptance tests are the specification.

## Be ready to explain

- your invariants
- the state transitions
- why a bug occurs, and why your fix belongs where you put it
- whether each operation should be idempotent
- the time and space complexity
- what changes in a concurrent or distributed version
