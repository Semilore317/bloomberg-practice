# Project Manager Notes - Subscription Entitlement

Do not read this until after your first pass.

These are the questions a strong candidate asks before and during the fix. The
interviewer is playing the project manager, so some answers are judgement calls,
not facts in the code.

- Can a cancelled subscription be reactivated?
- Can an expired trial be activated without the user paying?
- Should an expired trial still read as entitled?
- What should a second cancel do?
- Is EXPIRED a distinct state from CANCELLED?
- Should a read like is_entitled force expiry cleanup?
