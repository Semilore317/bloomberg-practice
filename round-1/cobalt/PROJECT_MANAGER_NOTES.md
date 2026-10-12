# Project Manager Notes - Wallet Authorization Holds

Do not read this until after your first pass.

These are the questions a strong candidate asks before and during the fix. The
interviewer is playing the project manager, so some answers are judgement calls,
not facts in the code.

- Does authorizing reduce the balance, or only the available funds?
- Can a voided hold be captured?
- What should a second void on the same hold do?
- What invariant relates balance, available, and active holds?
- Are all amounts integer cents, with no floating point?
- Should capture ever let available go negative?
