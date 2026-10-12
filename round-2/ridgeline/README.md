# Cache Tier

Welcome to the team that owns the caching tier. A capacity-bounded LRU cache serves hot values;
both `get` and `put` count as using a key, and when capacity is exceeded the least-recently-used
entry is evicted.

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
cache/
  lru.py       LRUCache: get / put with LRU eviction
  errors.py    CacheError
  service.py   CacheService: get / put
tests/         shipped regression tests
tickets/       reported work
```

## Product rules already agreed

- the cache never exceeds its capacity;
- `get` and `put` both mark a key as most-recently-used;
- on overflow, the least-recently-used key is evicted;
- updating an existing key refreshes it and does not grow the cache.
