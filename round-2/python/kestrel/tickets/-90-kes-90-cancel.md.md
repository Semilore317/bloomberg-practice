# KES-90: Cancelled order still matches

## Report

A trader cancels a resting order and receives a successful result. A later crossing order
still trades against the cancelled order.

## Acceptance criteria

- after `cancel(order_id)`, the order no longer rests on either side;
- a subsequent crossing order does not match the cancelled order;
- cancelling an unknown order id is a no-op, not an error;
- add a test that rests an order, cancels it, and asserts a crossing order produces no trade.

## Scope

Do not change the matching algorithm as part of this ticket.
