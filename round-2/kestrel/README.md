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
