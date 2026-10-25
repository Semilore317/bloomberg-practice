# Acceptance criteria

- `apply_delta` for a symbol with no snapshot raises `LookupError`;
- a delta applied after a snapshot still works and carries forward unset fields;
- no fabricated 0/0 quote ever enters the store;
- add a test that applies a delta with no prior snapshot and asserts it raises.

Do not change the subscription code as part of this ticket.
