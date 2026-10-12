# Self-review guide — Access Token Store

This file is for AFTER the exercise. It lists what strong candidates tend to
notice. It is not a patch: there is no corrected code here, only the observations
that lead you to one.

Strong candidates often notice:

- validate ignores expiry, so an expired token still validates
- refresh does not check expiry, so an expired token can be revived
- revoke can run twice (no terminal-state guard)
- a valid token is ACTIVE and now < expires_at
- refresh should only extend a token that is still valid
- whether revoke is idempotent is a product decision worth asking about

If you found and fixed the failing tests and can explain each fix in terms of the
invariant it protects, you did the exercise well.
