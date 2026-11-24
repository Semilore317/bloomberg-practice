# KES-103: Position limit checked too late

## Report

An account above its position limit still gets a trade booked. The limit is supposed to stop
the order before it executes, but the order appears in the trade log.

## Acceptance criteria

- an order that would breach the configured position limit is rejected before matching;
- no trade is produced and no position is mutated for a rejected order;
- an order within the limit still executes normally.

## Scope

Keep the limit arithmetic as agreed (buy increases net, sell decreases net); only the point
at which the check runs is in question.
