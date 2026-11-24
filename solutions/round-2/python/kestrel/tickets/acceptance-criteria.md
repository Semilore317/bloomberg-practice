# Acceptance criteria

Across all tickets:

- each fix is confirmed by a small test written from the reported symptom;
- existing correct behaviour stays green (price priority, validation, event publishing);
- public entry points keep their signatures;
- no fixture, clock, or configuration default is changed just to make a test pass;
- the test fails before the fix and passes after it.

See individual ticket files for the specific invariant each one protects.
