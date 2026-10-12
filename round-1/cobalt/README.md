# cobalt - Wallet Authorization Holds

`WalletService` is a wallet with authorization holds.

You are joining this codebase late, and something in it is wrong. Users report wallets that let you spend reserved money, voids that run twice, and captures that fire after a void. Your job is
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

## Start here

1. `CANDIDATE_BRIEF.md`: the system, the lifecycle, and what to be ready to explain.
2. `PROJECT_MANAGER_NOTES.md`: questions to ask before you change behaviour.
3. `SETUP.md`: how to run the tests you write, in Python, C++, or Java.
4. `SELF_REVIEW_AFTER.md`: read only after you finish.
