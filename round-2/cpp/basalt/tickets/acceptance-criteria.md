# Acceptance criteria

- positions are isolated per `(counterparty, symbol)`;
- the same symbol under two counterparties yields two independent nets;
- a query for one counterparty never reflects another's trades;
- add a test with two counterparties in the same symbol and assert independence.

Do not change the sign handling or idempotency as part of this ticket.
