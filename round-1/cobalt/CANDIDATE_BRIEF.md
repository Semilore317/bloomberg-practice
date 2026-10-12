# Candidate Brief — Wallet Authorization Holds

You are joining an existing project late in development.

`WalletService` is a wallet with authorization holds. Funds are authorized (reserved), then either captured (settled out of the balance) or voided (released). All amounts are integer cents. Available funds should be the balance minus active holds. Users report wallets that let you spend reserved money, voids that run twice, and captures that fire after a void.

The intended high-level lifecycle is:

```
HELD -> CAPTURED
   \-> VOIDED
```

Some requirements are intentionally incomplete. Treat the interviewer as the
project manager: ask clarifying questions where behaviour is ambiguous (there is
a list to start from in `PROJECT_MANAGER_NOTES.md`).

You may inspect the source, modify the implementation, and add your own tests. The
same system exists in Python, C++, and Java; pick one (see `SETUP.md`).

This pack ships no tests. Reproduce the reported symptom with a test you write,
confirm your hypothesis, then fix the code and keep your own tests green.

## Where the code lives

The same system is implemented three times, once per language:

`python/wallet.py` (WalletService, Hold), `cpp/wallet.hpp`, and `java/Wallet.java`.

## Be ready to explain

- your invariants
- the state transitions
- why a bug occurs, and why your fix belongs where you put it
- whether each operation should be idempotent
- the time and space complexity
- what changes in a concurrent or distributed version
