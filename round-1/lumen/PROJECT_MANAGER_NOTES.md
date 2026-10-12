# Project Manager Notes - Job State Machine

Do not read this until after your first pass.

These are the questions a strong candidate asks before and during the fix. The
interviewer is playing the project manager, so some answers are judgement calls,
not facts in the code.

- What should starting an already-running job do?
- Can a job be completed while it is not running?
- After how many attempts should a job become FAILED?
- Does the attempt count increment on start, or on fail?
- Is start idempotent if a worker retries it?
- Should a DONE or FAILED job be truly terminal?
