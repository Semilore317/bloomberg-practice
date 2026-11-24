# KES-106: One bad subscriber blocks the rest

## Report

Two handlers subscribe to quote events. The first raises an exception. The second never
receives the event, and the publishing call itself fails.

## Acceptance criteria

- every subscribed handler is invoked for one published event;
- an exception raised by one handler is contained so remaining handlers still run;
- the event is still recorded in the bus's published log.

## Scope

Do not change the subscription API or the event payload.
