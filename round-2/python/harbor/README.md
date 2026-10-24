# Payments Service

Welcome to the team that runs money movement for the platform. Accounts hold balances in a
double-entry ledger; funds can be reserved with holds and moved between accounts with idempotent
transfers. Every amount is an integer number of cents.

This repository has four reported problems in `tickets/`. Your interviewer will tell you which
ticket to start with. You are not expected to finish every ticket.

You may use the available AI assistant and normal repository tools. Treat the assistant like a
junior developer: establish a plan, inspect its work, run the tests, and retain ownership of the
result.

## Scope

In scope: work the tickets in `tickets/`, fixing the defects they report and
confirming each with a test you write. Keep all existing, correct behaviour working.

Out of scope: redesigning the services, changing public APIs, or adding features no
ticket asks for.

Time budget: about 45 minutes.

## Reproduce and test it yourself

This pack ships no tests. The code is the same in `python/`, `cpp/`, and `java/`;
pick one (see [SETUP.md](SETUP.md)). Work from the tickets in `tickets/`: for each,
write a test that reproduces the reported behaviour, confirm it fails, fix the
code, and keep your own test green.

## Repository map

## Repository map

```text
payments/
  models.py      domain types (Account, LedgerEntry, Hold)
  errors.py      ValidationError, UnknownAccount, InsufficientFunds
  accounts.py    the account store (open / exists / require)
  ledger.py      append-only double-entry ledger; balance = debits - credits
  holds.py       funds reserved against an account but not yet moved
  transfers.py   available() and the idempotent transfer() with a funds check
  service.py     PaymentsService: deposit, place_hold, release_hold, transfer, balance, available
tests/           shipped regression tests
tickets/         reported work
```

## Product rules already agreed

- all amounts are integer cents; floating point must not enter the ledger;
- the ledger is double-entry: every posting debits one account and credits another, and the sum
  of all balances is always zero;
- available funds are the ledger balance minus active holds;
- transfers are idempotent on `transfer_id`;
- a rejected transfer writes no ledger entry.


---

# Tickets

## HARBOR-134-double-charge.md

# HARBOR-134: Retried transfers move money twice

## Report

A client that retries `transfer` with the same `transfer_id` moves the funds again. It is most
common when the caller's connection is unstable and it retries before receiving our response. A
slow, sequential retry should simply return without moving money a second time.

## Acceptance criteria

- a transfer with a previously seen `transfer_id` is a no-op after the first application;
- the retried call does not raise; it returns as if the original had succeeded;
- balances reflect exactly one application of the transfer;
- add a test that applies the same transfer twice and asserts the funds moved once.

Do not change the ledger or the hold model as part of this ticket.


## HARBOR-141-overdraft.md

# HARBOR-141: Accounts can be overdrawn past their holds

## Report

Transfers go through even when the amount is larger than the funds actually available on the
source account. Available funds are the ledger balance minus any active holds; a transfer above
that should be refused and leave the ledger untouched.

## Acceptance criteria

- a transfer greater than `available(src)` raises `InsufficientFunds`;
- a rejected transfer writes no ledger entry and moves no money;
- active holds reduce the amount that can be transferred;
- add a test that places a hold, then attempts a transfer that only fails once the hold is counted.

Do not redesign the ledger or the hold model as part of this ticket.


## HARBOR-150-stuck-holds.md

# HARBOR-150: Released holds still reserve funds

## Report

After a hold is released the reserved funds do not come back: `available` stays low. Merchants
report that a cancelled authorization keeps blocking a customer's balance.

## Acceptance criteria

- after `release_hold`, the hold no longer counts toward `held` or `available`;
- releasing an unknown hold id is a no-op, not an error;
- available funds return to the balance minus the remaining active holds;
- add a test that reserves, releases, and asserts availability is restored.

Do not change the transfer path as part of this ticket.


## HARBOR-158-ledger-imbalance.md

# HARBOR-158: The ledger does not balance

## Report

Account balances do not reconcile. The sum of all balances drifts away from zero, and a transfer
appears to increase the sender's balance instead of decreasing it. In a double-entry ledger the
debit side increases while the credit side decreases by the same amount.

## Acceptance criteria

- a transfer decreases the sender and increases the receiver by the same amount;
- after any sequence of postings the sum of all account balances is zero;
- deposits and transfers both preserve this invariant;
- add a test that asserts conservation after a deposit and a transfer.

Do not change the public API of the ledger as part of this ticket.




---

# Setup and Test Instructions

# Setup

This pack ships no tests, on purpose. Read the tickets, form a hypothesis about
what is wrong, and write your own tests to confirm it before you change anything.
The same service exists in Python, C++, and Java; pick one.

## Python 3.9+

Write test files named `test_*.py` under `python/` (a `conftest.py` is already
there so your imports resolve), then:

```bash
cd python && pytest -q
```

## C++ (g++ with -std=c++17)

The implementation is header-only. Write your own `test.cpp` that includes the
headers, then:

```bash
cd cpp && g++ -std=c++17 test.cpp -o test && ./test
```

## Java (JDK 11+)

Write your own `Check.java` with a `main` that exercises the classes, then:

```bash
cd java && javac *.java && java Check
```
