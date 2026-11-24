# KES-104: Retrying a fill duplicates it

## Report

When an upstream client retries an order submission with the same event id, the trade is
captured twice. Downstream position and settlement figures are overstated.

## Acceptance criteria

- submitting the same event id twice records exactly one ledger entry;
- a distinct event id still records a new entry;
- the ledger's deduplication key is the event id supplied to the submission.

## Scope

Do not change the trade model or the submission signature; the event id is already passed
through to trade capture.
