# Message Bus

Welcome to the team that runs the internal message bus. Subscribers register a topic pattern and a
callback; publishing a message delivers it to every matching subscriber. A pattern is an exact
topic (`"px.AAPL"`), a trailing one-segment wildcard (`"px.*"`), or the match-all pattern (`"*"`).

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
bus/
  models.py         domain types (Subscription)
  errors.py         BusError
  topics.py         TopicMatcher: pattern/topic matching
  subscriptions.py  SubscriptionRegistry: add / remove / all
  router.py         Router: publish -> match -> deliver
  service.py        MessageBus: subscribe / unsubscribe / publish
tests/              shipped regression tests
tickets/            reported work
```

## Product rules already agreed

- patterns are exact, a trailing one-segment wildcard (`"a.*"`), or match-all (`"*"`);
- unsubscribing stops delivery and removes the subscription;
- one subscriber's failure must not stop delivery to the others.


---

# Tickets

## BUS-21-wildcards.md

# BUS-21: Wildcard subscriptions never match

## Report

Subscribers using `"px.*"` or `"*"` receive nothing. Only exact-topic subscriptions get messages,
so every wildcard consumer is silently broken.

## Acceptance criteria

- `"px.*"` matches `"px.AAPL"` and any single trailing segment under `px`;
- `"*"` matches every topic;
- an exact pattern still matches only its exact topic;
- add a test that subscribes with `"px.*"` and asserts delivery of a `"px.AAPL"` message.

Do not change the subscription registry or the router loop as part of this ticket.


## BUS-27-unsubscribe.md

# BUS-27: Unsubscribe does nothing

## Report

After a client unsubscribes it keeps receiving messages. The registry's remove path compares the
wrong fields, so nothing is ever removed and subscriptions leak.

## Acceptance criteria

- after `unsubscribe(token)`, that subscription no longer receives messages;
- the subscription is actually removed from the registry;
- other subscriptions are unaffected;
- add a test that subscribes, unsubscribes, publishes, and asserts no delivery.

Do not change topic matching or the router loop as part of this ticket.


## BUS-33-fanout.md

# BUS-33: A raising subscriber aborts delivery

## Report

If one subscriber's callback raises, the subscribers after it on the same topic receive nothing.
A single bad consumer is breaking fan-out for everyone.

## Acceptance criteria

- an exception in one callback does not stop delivery to the others;
- the handling of a failing callback is explicit rather than accidental;
- delivery to healthy subscribers still happens in order;
- add a test with one raising subscriber and one healthy subscriber that still receives the message.

Do not change topic matching or the subscription registry as part of this ticket.




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
