# Risk Netting Service

Welcome to the risk team. The service nets signed trades per counterparty and symbol: buys are
positive, sells are negative, and the net position is their signed sum, isolated per
`(counterparty, symbol)`.

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
risk/
  models.py     domain types (Trade, with signed qty)
  errors.py     LimitBreach
  positions.py  PositionBook: net per (counterparty, symbol)
  netting.py    NettingService: add_trade (idempotent), net_position
  service.py    RiskService: the public entry point
tests/          shipped regression tests
tickets/        reported work
```

## Product rules already agreed

- quantities are signed: a buy adds, a sell subtracts;
- a trade is idempotent on `trade_id`;
- positions are isolated per `(counterparty, symbol)` and never share across counterparties.


---

# Tickets

## RISK-51-sign.md

# RISK-51: Sells increase the net position

## Report

Risk numbers are wrong: a sell adds to the net position instead of reducing it. Positions are
being accumulated with the magnitude of each trade, ignoring its sign.

## Acceptance criteria

- a buy of +10 then a sell of -4 nets to 6;
- the net can be negative when sells exceed buys;
- the sign of each trade is respected as given;
- add a test that mixes a buy and a sell and asserts the signed net.

Do not change counterparty isolation as part of this ticket.


## RISK-57-idempotency.md

# RISK-57: Replayed trades are double-counted

## Report

The same trade sometimes arrives twice from the upstream feed, and the position counts it twice.
Trades must be idempotent on `trade_id`.

## Acceptance criteria

- adding the same `trade_id` twice counts the trade once;
- a genuinely new `trade_id` with the same fields still counts;
- the net reflects exactly one application of a replayed trade;
- add a test that adds the same `trade_id` twice and asserts a single application.

Do not change the sign handling as part of this ticket.


## RISK-63-counterparty-mix.md

# RISK-63: Counterparties share a position

## Report

Two counterparties trading the same symbol are being netted together, so one counterparty's
exposure bleeds into another's. Positions are keyed only by symbol.

## Acceptance criteria

- positions are isolated per `(counterparty, symbol)`;
- the same symbol under two counterparties yields two independent nets;
- a query for one counterparty never reflects another's trades;
- add a test with two counterparties in the same symbol and assert independence.

Do not change the sign handling or idempotency as part of this ticket.




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
