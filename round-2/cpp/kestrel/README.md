# Matching Engine

Welcome to the team that runs the order book. A single-symbol limit order book matches incoming
orders against resting ones with price-time priority: best price first and, within a price level,
oldest order first. Partial fills reduce the resting quantity; the unfilled remainder of an
incoming order rests.

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
matching/
  models.py    domain types (Resting, Trade)
  errors.py    ValidationError
  book.py      the order book: limit() matching and cancel()
  service.py   MatchingService: submit() (validates) and cancel()
tests/         shipped regression tests
tickets/       reported work
```

## Product rules already agreed

- matching is price-time priority: best price first, then oldest resting order (FIFO) at a price;
- a partial fill reduces the resting order's quantity; it is not removed until fully filled;
- the unfilled remainder of an incoming order rests in the book;
- a cancelled order no longer rests and cannot match.


---

# Tickets

## KES-77-priority.md

# KES-77: Time priority violated at a price level

## Report

When two resting orders sit at the same price, an incoming order matches the newer one first.
Traders who posted earlier at a price are being skipped, which breaks the fairness guarantee of
the book.

## Acceptance criteria

- at equal price, the earliest-resting order fills first (FIFO);
- best-price priority across price levels is preserved;
- the fix is in how the resting side is ordered for matching, not a special case;
- add a test with two same-price asks where the earlier one must fill first.

Do not change validation or the cancel path as part of this ticket.


## KES-83-partial-fill.md

# KES-83: Partial fills discard the remainder

## Report

A partial fill removes the whole resting order instead of reducing its quantity, so the unfilled
remainder vanishes from the book. Liquidity disappears after a small incoming order.

## Acceptance criteria

- a partial fill leaves the resting order with its remaining quantity still available;
- a fully-filled resting order is removed;
- a later incoming order can match the remaining quantity;
- add a test: rest 10, fill 4, then fill 6 and assert both trades occur.

Do not change price-time ordering as part of this ticket.


## KES-90-cancel.md

# KES-90: Cancel does not remove resting orders

## Report

`cancel` is a no-op: a cancelled order still rests and still matches. Traders are getting fills on
orders they pulled.

## Acceptance criteria

- after `cancel(order_id)`, the order no longer rests on either side;
- a subsequent crossing order does not match the cancelled order;
- cancelling an unknown order id is a no-op, not an error;
- add a test that rests an order, cancels it, and asserts a crossing order produces no trade.

Do not change the matching algorithm as part of this ticket.




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
