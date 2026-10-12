# Project Manager Notes - Order Lifecycle

Do not read this until after your first pass.

These are the questions a strong candidate asks before and during the fix. The
interviewer is playing the project manager, so some answers are judgement calls,
not facts in the code.

- What should filling a cancelled order do?
- Can an order be filled past its original quantity?
- Should cancelling a filled order error, or be a no-op?
- Does open quantity for a symbol include cancelled orders?
- Is a fill idempotent if the same execution is delivered twice?
- What invariant always holds between filled and the original quantity?
