# Self-review guide — Inventory Reservations

This file is for AFTER the exercise. It lists what strong candidates tend to
notice. It is not a patch: there is no corrected code here, only the observations
that lead you to one.

Strong candidates often notice:

- releasing twice returns the same units to stock twice (release is not guarded)
- a committed reservation can still be released (no status guard on release)
- commit does not clean up expiry first, so an expired hold can still be committed
- reserved_units does not clean up expiry, so it reports stale counts
- available should always equal capacity minus held minus committed units
- lazy expiry cleanup is O(n) over all reservations

If you found and fixed the failing tests and can explain each fix in terms of the
invariant it protects, you did the exercise well.
