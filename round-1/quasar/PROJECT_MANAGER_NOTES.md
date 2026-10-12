# Project Manager Notes - Rate Limiter

Do not read this until after your first pass.

These are the questions a strong candidate asks before and during the fix. The
interviewer is playing the project manager, so some answers are judgement calls,
not facts in the code.

- Is this a fixed window or a sliding window?
- When exactly does the count reset?
- What should remaining report once the window has elapsed?
- Should reset take effect immediately on the next call?
- What happens at the exact window boundary (now - start == window)?
- Is allow safe if two threads call it for the same key at once?
