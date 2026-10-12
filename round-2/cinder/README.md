# Market Data Service

Welcome to the team that distributes market data. The service keeps the latest quote per symbol,
built from a snapshot plus incremental updates, and fans quotes out to subscribers. Every update
carries a monotonically increasing sequence number (`seq`) per symbol.

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
market_data/
  models.py         domain types (Quote)
  store.py          latest quote per symbol
  sequencer.py      tracks the highest seq per symbol (gap / staleness detection)
  feed.py           applies snapshots and incremental deltas
  subscriptions.py  the subscription hub (subscribe / unsubscribe / publish)
  service.py        MarketDataService: ties store, feed, and the hub together
tests/              shipped regression tests
tickets/            reported work
```

## Product rules already agreed

- updates may arrive out of order; a quote with a lower-or-equal `seq` must not overwrite a newer one;
- a delta only makes sense on top of a base snapshot;
- unsubscribing stops delivery and frees the subscription;
- one subscriber's failure must not affect delivery to the others.
