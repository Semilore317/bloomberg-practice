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


---

# Tickets

## CACHE-14-recency.md

# CACHE-14: get does not refresh recency

## Report

Reading a key does not mark it as recently used, so a frequently-read key can be evicted while
keys that are never touched survive. Cache hit rates are worse than they should be.

## Acceptance criteria

- a key read with `get` is marked most-recently-used and survives the next eviction;
- an untouched key is evicted before a recently-read one;
- the value returned by `get` is unchanged;
- add a test that reads a key and then forces an eviction, asserting the read key survives.

Do not change the eviction direction as part of this ticket.


## CACHE-19-update.md

# CACHE-19: Updating a key does not refresh it

## Report

Re-putting an existing key updates its value but not its recency, so a freshly written key can be
evicted before older, untouched ones.

## Acceptance criteria

- updating an existing key makes it most-recently-used;
- updating an existing key does not grow the cache beyond capacity;
- the new value is the one returned on the next `get`;
- add a test that updates a key and then forces an eviction, asserting the updated key survives.

Do not change the eviction direction as part of this ticket.


## CACHE-9-eviction.md

# CACHE-9: Eviction drops the wrong entry

## Report

Under load the cache is evicting the entry that was just inserted instead of the
least-recently-used one. Hot data is being thrown away while cold data survives.

## Acceptance criteria

- on overflow, the least-recently-used key is the one evicted;
- the most-recently inserted key stays in the cache;
- capacity is never exceeded;
- add a test: capacity 2, put a, b, c, and assert `a` is gone while `b` and `c` remain.

Do not change the `get` recency behaviour as part of this ticket.




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
