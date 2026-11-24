# KES-101: Iceberg reserve never comes back

## Report

An iceberg order shows a small display quantity with a larger hidden reserve. After the
displayed quantity is filled, the order disappears from the book even though the reserve
should still be available.

## Acceptance criteria

- once the display quantity is consumed, the reserve replenishes the displayed quantity;
- the order keeps its original time priority after replenishment;
- replenishment stops when the reserve is empty, and the order is then removed.

## Scope

Do not change how display/reserve sizes are derived from an order request; the defect is in
fill handling.
