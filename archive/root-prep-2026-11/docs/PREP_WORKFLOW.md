# Preparation Workflow

One loop for every drill. [`AGENTS.md`](../AGENTS.md) is authoritative for how the assistant
behaves; this document covers how you run the exercise. Keep written output minimal during a
timed attempt. The session log is a thinking aid, not a deliverable.

## Modes

- **Open audit** — no ticket list. Discover issues independently from the code. See
  [`drills/open-audit.md`](../drills/open-audit.md).
- **Ticket-driven** — work the reported problems in a pack's `tickets/`.
- **Performance review** — only after correctness is investigated and established. See
  [`drills/performance-review.md`](../drills/performance-review.md).

## The loop

| Phase | Time | Minimum output |
| --- | --- | --- |
| A. Reconnaissance | 5–8 min | Purpose, entry points, state, invariants |
| B. Investigation | 15–25 min | Findings with evidence and confidence |
| C. Triage | 5 min | Ranked order and deferred items |
| D. Implementation | 20–35 min | One fix and one regression test per issue |
| E. Optimisation | 10–15 min | Complexity note, only if correctness is stable |
| F. Verification | 5–8 min | Observed tests, diff review, open issues |

The timeboxes fit a 60–90 minute open audit. Ticket-driven runs usually spend less time on
reconnaissance and more on implementation.

## A. Reconnaissance

Read the README and the source before asking the assistant anything. Map the public API to
internal state. List the invariants the system must preserve: valid state transitions,
resource or money conservation, ordering, idempotency, and boundary behaviour. Identify which
operations mutate state and which only read it.

## B. Investigation

State a hypothesis before asking the assistant to investigate:

> I think `<invariant>` breaks when `<sequence>` because `<reason>`.

Then ask the assistant to trace that path and challenge the hypothesis, not to agree with it.
Every claim needs a `file:line` reference. Separate confirmed findings (reproduced by a
failing test) from suspicions. Do not ask the assistant to "find all the bugs".

## C. Triage

Use [`SEVERITY_RUBRIC.md`](./SEVERITY_RUBRIC.md). Put correctness and data integrity first,
then invalid state transitions and incorrect return values, then lower-impact edge cases.
Check dependencies: fixing a caller may hide a broken invariant deeper in the system. Record
what you are deliberately deferring and why.

## D. Implementation

Fix one logical issue at a time. Read the callers before changing behaviour. Write or update a
focused regression test, run it with approval, and record the observed result. Keep the
public API stable unless the defect is in the API contract. Do not refactor unrelated code.

## E. Optimisation

Do not start performance work until correctness is stable and your regression tests pass. If
an optimisation breaks a test, revert it before investigating further. See
[`drills/performance-review.md`](../drills/performance-review.md).

## F. Verification and review

Run the focused tests you wrote. Review the full diff. Name unresolved issues and deferred
improvements. Practise a two-minute verbal summary: what was broken, how you proved it, what
you changed, and what remains.

## Documentation discipline

Use [`SESSION_TEMPLATE.md`](./SESSION_TEMPLATE.md) only as much as it helps. During a timed
attempt, a short findings table and a fix log are usually enough. Do not let logging consume
the exercise.

Use [`AI_PROMPTS.md`](./AI_PROMPTS.md) for prompts that keep the investigation yours.
