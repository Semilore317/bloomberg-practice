# Open-Audit Drill

Use this to rehearse the open-ended shape: an unfamiliar codebase, no ticket list, independent
discovery. The goal is not to find every defect. It is to demonstrate a disciplined
investigation, a defensible priority order, and a few well-proven fixes.

## Target

Start with [`round-2/python/kestrel`](../round-2/python/kestrel/). It is the closest domain
match available, though smaller than a full Round 1 system. Any pack works if you ignore its
tickets and symptom list.

## Setup

1. Pick a pack and language. Start a 60–90 minute timer.
2. Read only the pack `README.md` for system context and how to run code.
3. **Ignore the tickets.** Do not open `tickets/`, `report.md`, or any acceptance criteria
   before or during the attempt. Treat any reported-problem summary in the README as out of
   scope.
4. Do not read `solutions/`.
5. Work from the source. Write your own tests.

## Rules

- Discover issues independently. Do not ask the assistant to find all bugs.
- State a hypothesis before asking for a trace, and require `file:line` evidence.
- Ask the assistant to challenge your hypothesis rather than confirm it.
- Classify findings and prioritise correctness and data integrity.
- Fix only the highest-impact confirmed issues. Defer the rest explicitly.
- Stop at time. Do not start a broad rewrite.

## Suggested sequence

Use [`docs/PREP_WORKFLOW.md`](../docs/PREP_WORKFLOW.md) and
[`docs/SEVERITY_RUBRIC.md`](../docs/SEVERITY_RUBRIC.md).

- **A. Reconnaissance (5–8 min)** — purpose, entry points, state, invariants.
- **B. Investigation (20–30 min)** — read the implementation, list suspicious behaviour, form
  hypotheses, confirm the strongest ones with focused tests.
- **C. Triage (5 min)** — rank by severity and dependency; name what you are deferring.
- **D. Implementation (20–30 min)** — fix one root cause at a time with a regression test.
- **E. Performance (only if correctness is stable and time remains)** — see
  [`performance-review.md`](./performance-review.md).
- **F. Review (5–8 min)** — run your tests, review the diff, summarise what remains.

## Deliverable

A short findings log, not an exhaustive document. Use
[`docs/SESSION_TEMPLATE.md`](../docs/SESSION_TEMPLATE.md) if it helps.

- system map and key invariants;
- findings with location, evidence, and confidence;
- triage order and deferred items;
- fixes with observed test results;
- a two-minute verbal summary.

## Success criteria

- Issues were found independently from the code.
- Each fixed issue has a failing-then-passing test you wrote.
- The priority order is justified by impact and dependencies.
- No speculative fixes or unrelated refactors.
- Unresolved work is named clearly.
