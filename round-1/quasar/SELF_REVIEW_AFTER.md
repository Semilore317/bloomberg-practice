# Self-review guide - Rate Limiter

This file is for AFTER the exercise. It lists what strong candidates tend to
notice. It is not a patch: there is no corrected code here, only the observations
that lead you to one.

Strong candidates often notice:

- allow never rolls an elapsed window, so a key stays blocked forever
- remaining ignores the elapsed window and reports a stale count
- reset does not actually clear the key's window
- the window boundary (>= window) decides when a fresh window starts
- the count is shared mutable state; concurrent allow calls would race
- a sliding-window version needs per-timestamp tracking, not a single counter

If you reproduced each issue with a test you wrote, fixed it, and can explain each
fix in terms of the invariant it protects, you did the exercise well.
