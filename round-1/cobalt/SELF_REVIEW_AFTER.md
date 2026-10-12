# Self-review guide - Wallet Authorization Holds

This file is for AFTER the exercise. It lists what strong candidates tend to
notice. It is not a patch: there is no corrected code here, only the observations
that lead you to one.

Strong candidates often notice:

- available ignores active holds, so reserved funds can be spent twice
- a voided hold can still be captured (capture has no status guard)
- a hold can be voided twice (void has no status guard)
- available should always equal balance minus the sum of HELD amounts
- capture settles out of the balance exactly once
- money is integer cents; no floats in the ledger

If you reproduced each issue with a test you wrote, fixed it, and can explain each
fix in terms of the invariant it protects, you did the exercise well.
