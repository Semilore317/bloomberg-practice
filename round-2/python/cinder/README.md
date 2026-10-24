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


---

# Tickets

## MD-312-stale-quotes.md

# MD-312: Stale updates overwrite fresh quotes

## Report

Quotes occasionally flicker back to an older price. Updates can arrive out of order because of
retransmits and multiple feed handlers. An update whose `seq` is not greater than the stored
quote's `seq` must be ignored.

## Acceptance criteria

- applying a quote whose `seq` is not greater than the stored one is a no-op;
- a genuinely newer `seq` still updates the quote;
- the rule is enforced in the store, the single source of truth, not at each call site;
- add a test that applies a newer then an older update and asserts the newer survives.

Do not change the subscription or feed code as part of this ticket.


## MD-318-ghost-subscriptions.md

# MD-318: Unsubscribe does not stop callbacks

## Report

After a client unsubscribes it still receives quote callbacks, and the subscription list grows
without bound. Clients that come and go are slowly leaking memory and getting data they no longer
want.

## Acceptance criteria

- after `unsubscribe(symbol, token)`, publishing to that symbol does not call the removed callback;
- the removed subscription is actually dropped from the registry;
- other subscriptions on the same symbol are unaffected;
- add a test that subscribes, unsubscribes, publishes, and asserts no delivery.

Do not change the store or the sequence logic as part of this ticket.


## MD-324-fanout-isolation.md

# MD-324: One bad subscriber blocks the rest

## Report

If one subscriber's callback raises, later subscribers for the same symbol receive nothing. A
single misbehaving client is taking down fan-out for everyone on that symbol.

## Acceptance criteria

- an exception in one callback does not stop delivery to the others;
- the policy for a failing callback is explicit (dropped) rather than accidental;
- delivery order for healthy subscribers is preserved;
- add a test with one raising subscriber and one healthy subscriber that still receives the quote.

Do not change the store or the sequence logic as part of this ticket.


## MD-330-delta-before-snapshot.md

# MD-330: Deltas applied without a base snapshot

## Report

A delta for a symbol that has no prior snapshot silently fabricates a 0/0 base quote instead of
failing. Downstream consumers then see a bogus zero price. A delta only makes sense on top of a
snapshot.

## Acceptance criteria

- `apply_delta` for a symbol with no snapshot raises `LookupError`;
- a delta applied after a snapshot still works and carries forward unset fields;
- no fabricated 0/0 quote ever enters the store;
- add a test that applies a delta with no prior snapshot and asserts it raises.

Do not change the subscription code as part of this ticket.




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
