# KES-102: Self-trade is accepted

## Report

A single account can rest an order on one side and cross it with its own order on the other
side. The desk expects self-trades to be rejected before any trade is created.

## Acceptance criteria

- a crossing order from the same account as the resting order raises a risk error;
- no trade is recorded and no position is changed when a self-trade is rejected;
- orders from different accounts still match normally.

## Scope

Do not introduce a new public API; use the existing risk guard called during matching.
