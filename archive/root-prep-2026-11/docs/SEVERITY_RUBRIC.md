# Severity and Triage Rubric

Use this to order findings, not to label every line of code. Correctness and data integrity
always come before performance.

| Level | Criterion | Typical signal |
| --- | --- | --- |
| **Critical** | Data corruption, lost updates, or money/quantity becomes incorrect | Wrong balances, totals, fills, or inventory; invariant can be broken by ordinary use |
| **High** | Invalid state transition or clearly incorrect result | Terminal state can be re-entered; operation returns the wrong value; duplicate action changes state |
| **Medium** | Boundary or idempotency gap with limited blast radius | Expiry edge, retry edge, repeated call after a partial failure |
| **Low** | Maintainability or performance concern | Avoidable work on a cold path; unclear code with no current correctness impact |
| **Deferred** | Real issue, not worth the remaining time | Broad refactor, public API redesign, speculative improvement |

## Triage order

1. Critical data and accounting failures.
2. Invalid lifecycle or state-machine transitions.
3. Incorrect return values and observable behaviour.
4. Boundary, ordering, and idempotency gaps.
5. Performance and maintainability.

## Dependency check

Before fixing an issue, ask:

- Is the broken invariant enforced here, or only observed here?
- Which callers depend on the current behaviour?
- Does one fix expose or mask another issue?
- Is the smallest safe fix local, or does the contract itself need to change?

## Communication

For each finding, be ready to state: the invariant, the concrete failing sequence, the
evidence, the severity, and the smallest safe fix. If time runs out, explain the unresolved
findings and your ranking instead of starting a broad rewrite.
