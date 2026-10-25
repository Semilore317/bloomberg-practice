# Acceptance criteria

- accepting a request that is already REJECTED raises a clear error;
- the request's status is left unchanged when the transition is refused;
- valid transitions (PENDING to ACCEPTED or REJECTED) still work;
- add a test that rejects a request and then asserts accept raises.

Do not change the scheduler or scorer as part of this ticket.
