# Risk Netting Service

Welcome to the risk team. The service nets signed trades per counterparty and symbol: buys are
positive, sells are negative, and the net position is their signed sum, isolated per
`(counterparty, symbol)`.

This repository has three reported problems in `tickets/`. Your interviewer will tell you which
ticket to start with. You are not expected to finish every ticket.

You may use the available AI assistant and normal repository tools. Treat the assistant like a
junior developer: establish a plan, inspect its work, run the tests, and retain ownership of the
result.

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
