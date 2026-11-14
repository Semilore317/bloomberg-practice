# Preparation Workflow

Use this process for any exercise in this directory. It works for ticket-driven and
open-ended exercises. [`AGENTS.md`](../AGENTS.md) is authoritative for assistant permissions;
this document covers the investigation itself. Keep written output minimal during a timed
attempt.

## Modes

- **Ticket-driven** — if the exercise provides tickets, read them as reported symptoms. They
  may be incomplete. Do not assume they enumerate every defect.
- **Open-ended** — if there is no ticket list, inspect the implementation and discover issues
  independently.

Do not assume a mode, language, or bug count before reading the exercise README and code.

## The loop

| Phase | Time | Minimum output |
| --- | --- | --- |
| A. Reconnaissance | 5–8 min | Purpose, entry points, state, invariants |
| B. Investigation | 15–25 min | Findings with evidence and confidence |
| C. Triage | 5 min | Ranked order and deferred items |
| D. Implementation | 20–35 min | One fix and one regression test per issue |
| E. Optimisation | 10–15 min | Complexity note, only if correctness is stable |
| F. Verification | 5–8 min | Observed tests, diff review, open issues |

Adjust the timeboxes to the exercise. Do not let logging consume the exercise.

## A. Reconnaissance

Read the README and the source before asking the assistant anything. Map the public API to
internal state. List the invariants the system must preserve: valid state transitions,
resource or money conservation, ordering, idempotency, and boundary behavior. Identify which
operations mutate state and which only read it.

## B. Investigation

State a hypothesis before asking the assistant to investigate:

> I think `<invariant>` breaks when `<sequence>` because `<reason>`.

Then ask the assistant to trace that path and challenge the hypothesis, not to agree with it.
Every claim needs a `file:line` reference. Separate confirmed findings (reproduced by a
failing test) from suspicions. Do not ask the assistant to find all bugs. If tickets exist,
use them as starting points, then inspect adjacent behavior they do not mention.

## C. Triage

Use the rubric below to order findings. Correctness and data integrity come first.

| Level | Criterion | Typical signal |
| --- | --- | --- |
| **Critical** | Data corruption, lost updates, or money/quantity becomes incorrect | Wrong totals, fills, or inventory; ordinary use breaks an invariant |
| **High** | Invalid state transition or clearly incorrect result | Terminal state re-entered; wrong return value; duplicate action changes state |
| **Medium** | Boundary or idempotency gap with limited blast radius | Expiry edge, retry edge, repeated call after partial failure |
| **Low** | Maintainability or performance concern | Avoidable work on a cold path; unclear code with no current correctness impact |
| **Deferred** | Real issue, not worth the remaining time | Broad refactor, public API redesign, speculative improvement |

Triage order:

1. Critical data and accounting failures.
2. Invalid lifecycle or state-machine transitions.
3. Incorrect return values and observable behavior.
4. Boundary, ordering, and idempotency gaps.
5. Performance and maintainability.

Before fixing, ask: is the invariant enforced here or only observed here, which callers depend
on the current behavior, and does one fix expose or mask another issue? Record what you defer
and why.

## D. Implementation

Fix one logical issue at a time. Read the callers before changing behavior. Write or update a
focused regression test, run it with approval, and record the observed result. Keep the public
API stable unless the defect is in the API contract. Do not refactor unrelated code.

## E. Optimisation

Do not start performance work until correctness is stable and your regression tests pass.
Derive the current complexity from the code, measure the hot path, and compare alternatives
before changing anything. If an optimisation breaks a test, revert it before investigating
further. A faster wrong answer is still wrong.

## F. Verification and review

Run the focused tests you wrote. Review the full diff. Name unresolved issues and deferred
improvements. Practise a two-minute verbal summary: what was broken, how you proved it, what
you changed, and what remains.

## Findings log

Use this compact log if it helps. A short table plus a fix note is usually enough.

| ID | Symptom or invariant violated | Location | Evidence | Confidence | Status |
| --- | --- | --- | --- | --- | --- |
| F1 | | `file:line` | | low / medium / high | hypothesis / confirmed / fixed / deferred |

For each fixed item, note: root cause, minimal change, callers checked, regression test, and
observed result.

## AI prompts

Use [`AI_PROMPTS.md`](./AI_PROMPTS.md) for prompts that keep the investigation yours.
