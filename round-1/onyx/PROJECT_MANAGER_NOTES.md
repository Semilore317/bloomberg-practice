# Project Manager Notes — Access Token Store

Do not read this until after your first pass.

These are the questions a strong candidate asks before and during the fix. The
interviewer is playing the project manager, so some answers are judgement calls,
not facts in the code.

- Should an expired token pass validation?
- Can an expired token be refreshed back to life?
- What should a second revoke do?
- Is revoke idempotent, or an error the second time?
- Does refresh extend from now, or from the original expiry?
- Should validation force cleanup of expired tokens, or just report them invalid?
