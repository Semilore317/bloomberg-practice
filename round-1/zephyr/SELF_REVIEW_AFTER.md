# Self-review guide — Subscription Entitlement

This file is for AFTER the exercise. It lists what strong candidates tend to
notice. It is not a patch: there is no corrected code here, only the observations
that lead you to one.

Strong candidates often notice:

- a cancelled subscription can be reactivated (activate has no guard)
- an expired trial can be activated without paying (activate skips cleanup)
- is_entitled ignores expiry, so an expired trial still reads as entitled
- cancel can run twice (no terminal-state guard)
- ACTIVE and unexpired TRIAL are entitled; everything else is not
- EXPIRED and CANCELLED are terminal and distinct

If you reproduced each issue with a test you wrote, fixed it, and can explain each
fix in terms of the invariant it protects, you did the exercise well.
