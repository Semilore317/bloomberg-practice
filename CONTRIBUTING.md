# Contributing

Thanks for adding to the question bank. Each "pack" is a self-contained practice codebase with
deliberately planted bugs. Keep the contract for its round and new packs will fit right in.

## The two round shapes

- `round-1/<codename>/` — **mostly green**. One stateful domain object with a clear lifecycle.
  Most tests pass; **3 to 5 planted bugs** fail. This mirrors the real Bloomberg round, where you
  join a mostly-working service and debug it. Target ~35 minutes.
- `round-2/<codename>/` — **all red**. A larger multi-module microservice where **every test fails
  by default**, tuned harder than the real round. Target ~45 minutes.

Use a **codename** that reveals nothing about the domain (for example `halcyon`, `kestrel`). The
documents tell the story; the folder name does not.

## Languages and layout

A pack is implemented three times with the **same spec and the same planted bugs**, one folder per
language. The documents differ by round:

```text
round-1/<codename>/                       round-2/<codename>/
  CANDIDATE_BRIEF.md                         README.md
  PROJECT_MANAGER_NOTES.md                   SETUP.md
  SELF_REVIEW_AFTER.md                       tickets/
  SETUP.md                                   python/  cpp/  java/
  python/  cpp/  java/
```

- **python/** — module(s) plus `tests/` (pytest) and a `conftest.py` that puts the pack on the path.
- **cpp/** — header-only implementation (`.hpp`), `tests.cpp`, and a `Makefile` (`make test`).
- **java/** — the classes plus `Tests.java` with a `main` that runs the checks.

There is **no SOLUTION file** anywhere. The acceptance tests are the answer key. Round 1 ships a
`SELF_REVIEW_AFTER.md`, but that is a list of symptoms to notice after the exercise, not corrected
code.

### Test runners (dependency-free on purpose)

- **Python:** `cd python && pytest -q`.
- **C++:** `cd cpp && make test` (compiles `tests.cpp` with `g++ -std=c++17` and runs it). The
  runner prints `PASS`/`FAIL` per check and exits non-zero while any check fails.
- **Java:** `cd java && javac *.java && java Tests`. `Tests.java` runs checks and calls
  `System.exit(1)` while any fail.

In every language the runner exits zero only when all checks pass, so "all green" means the same
thing everywhere.

## The rules (please keep these)

1. **The right shipped split.** Round 1 ships mostly green with 3 to 5 failing tests. Round 2 ships
   all red. Verify the shipped split in **every language** before you submit.
2. **Each failing test isolates one bug**, for one clear reason.
3. **Fixable to green.** After the intended fixes, the whole suite passes in all three languages.
4. **Realistic lifecycle bugs.** Missing state guards, idempotency gaps, off-by-ones at a boundary,
   stale reads that skip expiry cleanup, broken invariants. No syntax errors or obviously broken
   code.
5. **No external dependencies, services, API keys, or network calls.** Standard library only (plus
   `pytest` for Python).
6. **Integer money.** If a pack handles money, use integer cents; no floats in a ledger.
7. **Determinism.** Anything time-based takes an injected clock, so TTL and expiry tests are exact.

## Round 1 document set

- `CANDIDATE_BRIEF.md` — "You are joining an existing project late in development", the system, the
  intended lifecycle, where the code lives, and a **be-ready-to-explain** list (invariants, state
  transitions, idempotency, complexity, the concurrent/distributed version).
- `PROJECT_MANAGER_NOTES.md` — the clarifying questions a strong candidate asks. The interviewer
  plays the project manager, so some answers are judgement calls.
- `SELF_REVIEW_AFTER.md` — what strong candidates notice, read after the exercise. Symptoms, not a
  patch.
- `SETUP.md` — how to run each language.

## Round 2 document set

- `README.md` — "Welcome to the team that ...", a run section, a repository map, and the product
  rules as bullets.
- `tickets/` — one `.md` per reported problem: a Report, Acceptance criteria, and a scope boundary.
- `SETUP.md` — how to run each language.

## Before you submit: verify the pack

For each language, the shipped pack must show the correct split (mostly green for round 1, all red
for round 2) and must go to all green once the intended fixes are applied. A pack that cannot make
that round trip is not ready. Keep the fixes out of the repository.

## Opening a change

Create a branch, add your pack (or language port), and open a pull request. In the PR description
(not in the repo), list the codename, the round, the languages, and the planted bugs, and confirm
the suite makes the red-to-green round trip. Keep the solution out of the repository.
