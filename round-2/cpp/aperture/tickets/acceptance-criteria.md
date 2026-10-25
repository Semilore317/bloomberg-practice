# Acceptance criteria

- each `nack` advances the job's attempt count by one;
- with `max_retries=N`, the Nth `nack` moves the job to the dead-letter list instead of re-queueing;
- a job below the limit is re-queued and can be dispatched again;
- add tests at `max_retries=1` and `max_retries=2` asserting the job dead-letters on the Nth nack.

Do not change the dequeue path as part of this ticket.
