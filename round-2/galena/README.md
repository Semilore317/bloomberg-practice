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
