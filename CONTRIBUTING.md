# Contributing

Thanks for adding to the question bank. Each "pack" is a self-contained practice codebase
with deliberately planted bugs and **no tests**. The candidate writes the tests; you ship
the broken code and the story around it. Keep that contract and new packs will fit right in.

## The two round shapes

- `round-1/<language>/<codename>/` — one stateful domain object with a clear lifecycle and
  **3 to 5 planted bugs**. Target ~35 minutes.
- `round-2/<language>/<codename>/` — a larger multi-module microservice with more bugs and a
  ticket backlog. Target ~45 minutes.

Use a **codename** that reveals nothing about the domain (for example `halcyon`, `kestrel`).
The documents tell the story; the folder name does not.

## No tests in baseline packs

Packs do not ship tests. This is deliberate: confirming a bug with a test you wrote is the
skill being practised. What a pack ships instead:

- the implementation, with the bugs in it, one folder per language;
- a `conftest.py` in each `python/` so a candidate's own `test_*.py` imports the module;
- the story: round 1 ships a `README.md` with the reported symptom, round 2 ships a
  `README.md` and `tickets/` with one reported problem each.

The baseline under `round-1/` and `round-2/` contains no tests. Completed answers, where
present, live under `solutions/` and are answer keys, not part of the candidate-facing pack.

## Languages and layout

A pack is implemented three times with the **same bugs**, one folder per language.

```text
round-1/<language>/<codename>/           round-2/<language>/<codename>/
  README.md                                 README.md
  AGENTS.md                                 AGENTS.md
  prep/WORKFLOW.md                          prep/WORKFLOW.md
  prep/AI_PROMPTS.md                        prep/AI_PROMPTS.md
  conftest.py                               conftest.py
  implementation                            tickets/
                                            implementation
```

- **python/** — the module(s) plus a `conftest.py` that puts the pack on the path. No tests.
- **cpp/** — a header-only implementation (`.hpp`). No test file and no Makefile; a candidate
  writes `test.cpp`.
- **java/** — the classes only. No `Tests.java`; a candidate writes `Check.java`.

## Preparation documents

Every candidate-facing pack, in every language, must be self-contained and ship:

- `AGENTS.md` — the investigation-first assistant contract. Reconcile it with the shared
  root `AGENTS.md`; do not overwrite unique pack instructions with a blind copy.
- `prep/WORKFLOW.md` — the A–F loop, triage rubric, findings log, and both ticket-driven
  and open-ended modes.
- `prep/AI_PROMPTS.md` — phase-gated prompts that keep the investigation with the candidate.

Keep these files generic. Do not name the pack, its round, or its language, and do not link
to another pack's files. Any relative link must resolve from inside the pack directory. A
pack must not depend on root-level preparation files. Do not add a separate session
template; the findings log belongs in `prep/WORKFLOW.md`.

## Verify with a private holdout

Write a full acceptance suite while you build the pack, in all three languages, and use it to
prove two things: every planted bug is independently reproducible with a failing test, and
applying the intended fix turns the whole suite green. Keep it out of the baseline. If you
commit the answer, place it under `solutions/<round>/<language>/<codename>/` with its tests,
clearly separated from the candidate-facing pack.

## The rules (please keep these)

1. **Bugs that a written test can catch.** Each planted bug must be reproducible by a small,
   obvious test a candidate could write from the symptom. If you cannot write that test, the
   bug is too obscure.
2. **Fixable cleanly.** The intended fix is the narrowest change that restores the invariant,
   in all three languages.
3. **Realistic lifecycle bugs.** Missing state guards, idempotency gaps, off-by-ones at a
   boundary, stale reads that skip expiry cleanup, broken invariants. No syntax errors and no
   giveaway comments in the code.
4. **No external dependencies, services, API keys, or network calls.** Standard library only.
5. **Integer money.** If a pack handles money, use integer cents; no floats in a ledger.
6. **Determinism.** Anything time-based takes an injected clock, so a candidate's expiry tests
   are exact.
7. **Shipped code must compile and import on its own**, with no test files present.
8. **Self-contained packs.** Every candidate-facing pack ships its own `README.md`,
   `AGENTS.md`, and `prep/` material, so it works when opened directly without root-level
   setup docs.

## Round 1 document set

- `README.md` — joining the codebase late, the system, the intended lifecycle, the
  **reported symptom** (not a bug location), scope, time budget, and how to run the tests
  the candidate writes.
- `AGENTS.md` — the investigation-first assistant contract.
- `prep/WORKFLOW.md` and `prep/AI_PROMPTS.md` — the investigation process and prompts.
- `conftest.py` — Python import path only; the candidate supplies the tests.

## Round 2 document set

- `README.md` — "Welcome to the team that ...", a repository map, the product rules as
  bullets, setup, time budget, and a note that the candidate writes the tests.
- `tickets/` — one `.md` per reported problem: a Report, Acceptance criteria, and a scope
  boundary. The tickets are the symptoms; they do not name the buggy line.
- `AGENTS.md`, `prep/WORKFLOW.md`, `prep/AI_PROMPTS.md`, and `conftest.py` — as in round 1.

## Opening a change

Create a branch, add your pack (or language port), and open a pull request. In the PR
description (not in the baseline pack), list the codename, the round, the languages, the
planted bugs, and confirm that your private holdout went red-to-green in all three. Also
confirm that each pack's `README.md`, `AGENTS.md`, and `prep/` links resolve from inside the
pack. Keep the holdout out of the baseline; committed answers belong under `solutions/`.
