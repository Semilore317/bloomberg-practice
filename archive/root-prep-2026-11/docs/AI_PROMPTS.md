# AI Prompts

Use these with [`AGENTS.md`](../AGENTS.md). `AGENTS.md` wins on permissions: no edits, test
runs, or state changes without your approval. The prompts keep the investigation yours.

## Non-negotiables

- Read the code first and state a hypothesis before asking the assistant to investigate.
- Never ask the assistant to "find all the bugs".
- Require a `file:line` reference for every claim.
- Ask the assistant to challenge the hypothesis and produce a counterexample.
- Do not let the assistant edit files or run tests without explicit approval.
- Run the focused check yourself and report only observed results.

## Reconnaissance

> Read these files and explain the system's purpose, entry points, important state, data flow,
> and invariants. Do not suggest bugs or fixes yet. Cite `file:line` for each claim.

## Hypothesis verification

> My hypothesis is that `<invariant>` is violated when `<sequence>`. Trace the actual execution
> path from `<entry point>` through the relevant state changes. Cite `file:line`. Then challenge
> the hypothesis: what alternative explanation or counterexample would disprove it?

## Root-cause analysis

> I have a failing test that demonstrates `<symptom>`. Identify the root cause, not the symptom.
> Trace all callers and affected invariants. Propose the smallest safe fix and explain what
> behaviour must remain unchanged. Do not edit files or run tests.

## Fix review

> Review this diff as a senior reviewer. Does it preserve the public API and every documented
> invariant? Which boundary, idempotency, ordering, or partial-failure cases does it miss? Is the
> change broader than necessary? Do not edit anything.

## Test generation

> Given the public API and the invariant `<invariant>`, propose edge cases worth testing. Do not
> reveal or infer any hidden defects. Keep the tests behaviour-focused and minimal.

## Performance analysis

> For `<operation>`, derive the current time and space complexity from the implementation.
> Identify the hot path and the dominant cost. Compare at least two alternative data structures or
> algorithms, including trade-offs. Do not implement anything yet.

## Triage review

> Here is my findings list. Classify each by severity and dependency order. Challenge my ranking:
> which high-severity issue am I underestimating, and which low-severity issue am I over-investing
> in?

## After approval

Once you approve a specific fix, restate the root cause and intended change, then ask the
assistant for the smallest diff. Review it against the prompt above before accepting it.
See [`PREP_WORKFLOW.md`](./PREP_WORKFLOW.md) for the surrounding loop.
