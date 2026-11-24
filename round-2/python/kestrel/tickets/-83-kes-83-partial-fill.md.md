# KES-83: Partial fill loses the resting remainder

## Report

A resting order is partially filled by an incoming order. The trade is booked, but the
unfilled portion of the resting order can no longer be seen in the book and will not
match later orders.

## Acceptance criteria

- after a partial fill, the resting order remains at its price with the reduced quantity;
- a later crossing order can fill the remaining quantity;
- an order that is fully filled is removed from the book.

## Scope

Do not change trade price or quantity arithmetic; focus on how a resting order is handled
when a fill is smaller than its quantity.
