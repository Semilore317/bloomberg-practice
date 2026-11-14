# Performance Review Drill

Run this only after correctness has been investigated and established. Optimising code whose
behaviour you have not verified hides defects and changes semantics you do not yet understand.

## Preconditions

Do not start unless all of these are true:

- you have a findings log and have triaged correctness issues;
- the correctness fixes you intend to keep have tests that you have run and observed passing;
- you can run a stable correctness check before and after a change;
- you have written down the operation and input size you want to measure.

If any precondition is missing, return to [`open-audit.md`](./open-audit.md) first.

## Target

Start with [`round-2/python/kestrel`](../round-2/python/kestrel/), or any pack with a clear hot
path. Choose one to three public operations that have a meaningful input size, such as book
updates, cancellation, or inspection under load. Do not try to optimise the whole service.

## Steps

1. Define a workload: input sizes, operation mix, and a repeatable setup.
2. Measure the baseline with `time.perf_counter`, `timeit`, or `cProfile` from the standard
   library.
3. Derive the current time and space complexity from the code, not from intuition.
4. Identify the dominant cost and confirm it with a measurement.
5. Propose one or two alternatives with trade-offs before changing anything.
6. Ask the assistant to review the analysis using the performance prompt in
   [`docs/AI_PROMPTS.md`](../docs/AI_PROMPTS.md). Do not let it implement yet.
7. After your approval, make the smallest change that tests the hypothesis.
8. Re-run the correctness tests you wrote. If any fail, revert the optimisation.
9. Measure again under the same workload.
10. Keep the change only if the improvement is real and correctness is preserved.

## Rules

- No micro-optimisation without a measurement.
- Preserve the public API and observable behaviour.
- Do not optimise a cold path.
- Keep the change reversible and separate from correctness fixes.
- Correctness wins. A faster wrong answer is still wrong.

## Deliverable

- current complexity and measured baseline;
- hot path and evidence;
- the change and its trade-off;
- before/after measurement;
- correctness tests run and observed;
- a decision to keep or revert.

## Timebox

10–15 minutes inside a full drill, or 20–40 minutes as a standalone exercise. Stop at time and
explain the analysis even if you do not implement the optimisation.
