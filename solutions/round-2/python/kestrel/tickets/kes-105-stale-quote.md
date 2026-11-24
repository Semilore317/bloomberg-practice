# KES-105: Best quote is stale after a cancel

## Report

A client asks for the best bid/ask, then a resting order is cancelled. The quote returned
after the cancellation still shows the cancelled price. A fresh subscriber receiving the
first published quote sees the same stale value.

## Acceptance criteria

- the best quote reflects the book after a cancellation;
- the best quote reflects the book after a match;
- calling the quote getter repeatedly without book changes is stable.

## Scope

Do not change the book's price computation or the shape of the quote tuple.
