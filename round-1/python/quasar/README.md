# quasar - Rate Limiter

`RateLimiter` is a fixed-window per-key rate limiter.

You are joining this codebase late, and something in it is wrong. Users report keys that stay blocked forever after their first burst, remaining counts that never recover, and a reset that does nothing. Your job is
to find the bug or bugs behind that, fix them, and prove each fix with a test you
write yourself. This pack ships no tests.

## Scope

In scope:

- find and fix the defects behind the reported symptom;
- write your own tests to confirm each defect and each fix;
- keep all existing, correct behaviour working.

Out of scope:

- redesigning the component or changing its public API;
- adding features the brief did not ask for;
- performance work, unless a defect is itself a performance bug.

Time budget: about 35 minutes.




## Running tests

Write your own tests as `test_*.py` in this directory. A `conftest.py` is provided for local imports.

```bash
pytest -q
```