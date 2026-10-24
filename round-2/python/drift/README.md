# Fulfillment Service

Welcome to the team that promises stock to orders. A catalog of SKUs, physical on-hand inventory,
and a reservation book combine into an availability view: what can still be promised is the
on-hand count minus what is already reserved.

This repository has three reported problems in `tickets/`. Your interviewer will tell you which
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
fulfillment/
  models.py        domain types (Sku, Reservation)
  errors.py        ValidationError, UnknownSku, OutOfStock
  catalog.py       the SKU catalog (add / exists / require)
  inventory.py     physical on-hand counts per SKU
  reservations.py  the reservation book (place / release / reserved)
  service.py       FulfillmentService: available(), reserve(), release()
tests/             shipped regression tests
tickets/           reported work
```

## Product rules already agreed

- availability is on-hand minus active reservations;
- a reservation is never granted beyond availability;
- releasing a reservation returns its stock to availability;
- an unknown SKU is rejected at the boundary.


---

# Tickets

## DRIFT-101-stuck-reservations.md

# DRIFT-101: Released reservations keep holding stock

## Report

`release` does not actually free a reservation, so availability never recovers after a hold is
cancelled. Stock stays locked away from new orders.

## Acceptance criteria

- after `release`, the reservation no longer counts toward `reserved` or `available`;
- releasing an unknown reservation id is a no-op, not an error;
- availability returns to on-hand minus the remaining active reservations;
- add a test that reserves, releases, and asserts availability is restored.

Do not change the oversell check as part of this ticket.


## DRIFT-88-availability.md

# DRIFT-88: Availability ignores reservations

## Report

The same stock is being promised twice. `available(sku)` returns the physical on-hand count and
ignores reservations that are already holding some of it, so two orders can each be told the stock
is free.

## Acceptance criteria

- `available(sku)` equals on-hand minus active reservations for that SKU;
- reserving stock immediately lowers availability by the reserved amount;
- availability for other SKUs is unaffected;
- add a test that reserves part of the stock and asserts availability drops.

Do not change the inventory or catalog modules as part of this ticket.


## DRIFT-92-oversell.md

# DRIFT-92: Reservations can oversell

## Report

A reservation larger than what is available succeeds and drives availability negative. Warehouses
are getting orders they cannot fill.

## Acceptance criteria

- reserving more than `available(sku)` raises `OutOfStock`;
- a rejected reservation leaves availability unchanged;
- a reservation exactly equal to availability is allowed;
- add a test that attempts to reserve beyond availability and asserts it raises.

Do not change the reservation-release path as part of this ticket.




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
