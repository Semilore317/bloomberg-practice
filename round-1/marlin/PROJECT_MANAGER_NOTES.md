# Project Manager Notes - Inventory Reservations

Do not read this until after your first pass.

These are the questions a strong candidate asks before and during the fix. The
interviewer is playing the project manager, so some answers are judgement calls,
not facts in the code.

- What should releasing the same reservation twice do?
- Can an expired hold still be committed?
- Should an expired hold become EXPIRED or just RELEASED?
- Can a committed reservation be released back to stock?
- Should a read like reserved_units force expiry cleanup first?
- What invariant should always hold for available stock?
