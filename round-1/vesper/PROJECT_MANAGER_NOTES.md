# Project Manager Notes — Connection Pool

Do not read this until after your first pass.

These are the questions a strong candidate asks before and during the fix. The
interviewer is playing the project manager, so some answers are judgement calls,
not facts in the code.

- What should acquiring from a closed pool do?
- Can the pool ever exceed its capacity?
- What should releasing an already-idle connection do?
- What invariant holds for in-use plus idle versus capacity?
- Should close drain or forcibly close in-use connections?
- Is acquire/release safe under concurrent callers?
