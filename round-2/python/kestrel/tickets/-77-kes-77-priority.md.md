# KES-77: Time priority violated at a price level

## Report

Two resting bids sit at the same price. A new aggressive sell fills only part of the
quantity. Traders report that the newer bid trades first, so the older bid keeps its
place in the queue unexpectedly.

## Acceptance criteria

- at one price level, the oldest resting order is filled first;
- orders at better prices still trade before orders at worse prices;
- a partial fill leaves the older order ahead of the newer one for the next incoming order.

## Scope

Do not change the public `submit` signature or the representation of a resting order.
