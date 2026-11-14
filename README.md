# bloomberg-practice

Interview-grade practice for Bloomberg's AI-assisted codebase rounds. Each pack is an
**unfamiliar codebase** under a codename that reveals nothing about the domain, with
real, deliberately planted bugs and **no tests**.

That last part is the point. The real skill is not running a green suite someone handed
you. It is reading code you did not write, taking a vague bug report, forming a
hypothesis, **writing your own test to confirm it**, fixing the code, and keeping your
test green. So these packs ship the service and the reported symptom, and you bring the
tests.

- `round-1/` — a focused service: one stateful domain object with a clear lifecycle and a
  few planted bugs. Target ~35 minutes. Each pack's `README.md` gives the system and the
  reported symptom; `AGENTS.md` and `prep/` set the investigation process.
- `round-2/` — a larger multi-module microservice with more surface area and a `tickets/`
  backlog of reported problems. Target ~45 minutes. Each pack also has its own `AGENTS.md`
  and `prep/` material.

The baseline packs ship no tests. The code, the README, and the tickets are all you get,
the same as walking into a real repository on your first day. Completed solutions, where
present, live under `solutions/` as answer keys; do not read them during a timed attempt.

## Languages

Every pack is implemented three times, once per language, with the **same bugs**. Pick the
language you want to interview in.

```text
round-1/python/<codename>/              round-2/python/<codename>/
  README.md          scope + symptom      README.md          service map + setup
  AGENTS.md          investigation rules  AGENTS.md          investigation rules
  prep/WORKFLOW.md   investigation loop   prep/WORKFLOW.md   investigation loop
  prep/AI_PROMPTS.md reusable prompts     prep/AI_PROMPTS.md reusable prompts
  conftest.py        test import path     conftest.py        test import path
  <module>.py        implementation       tickets/           reported problems
                                          <package>/         implementation
```

The same packs exist under `cpp/` and `java/` with the same defects. Each Python pack keeps
a `conftest.py` so the tests you write import the module cleanly. The C++ implementation is
header-only, so you write a `test.cpp` that includes it. For Java you write a small
`Check.java` with a `main`. See each pack's `README.md` for setup.

## Round 1 — one service, a few bugs (~35 min, Python / C++ / Java)

One stateful domain object with a lifecycle and invariants to protect. The brief gives you
the reported symptom; you find and confirm the bugs.

| Pack | Domain | What it is |
| --- | --- | --- |
| [halcyon](round-1/python/halcyon) | Order Lifecycle | Working orders placed, filled, and cancelled; open-quantity and over-fill invariants. |
| [marlin](round-1/python/marlin) | Inventory Reservations | TTL stock holds, commit versus release, expiry returns units automatically. |
| [zephyr](round-1/python/zephyr) | Subscription Entitlement | Trial, active, suspended, cancelled lifecycle with trial expiry. |
| [cobalt](round-1/python/cobalt) | Wallet Holds | Authorization holds, capture versus void, available equals balance minus holds. |
| [quasar](round-1/python/quasar) | Rate Limiter | Fixed-window per-key limiter with window reset and remaining quota. |
| [onyx](round-1/python/onyx) | Access Tokens | Short-lived tokens: issue, validate, refresh, revoke, with TTL expiry. |
| [pike](round-1/python/pike) | Approval Workflow | Documents go pending then approved, rejected, or withdrawn; terminal states. |
| [vesper](round-1/python/vesper) | Connection Pool | Fixed-capacity acquire, release, and close, with a capacity invariant. |
| [tundra](round-1/python/tundra) | LRU + TTL Cache | Capacity-bounded cache with per-entry TTL and least-recently-used eviction. |
| [lumen](round-1/python/lumen) | Job State Machine | Queued, running, done, failed, with retries and an attempt budget. |

## Round 2 — larger microservices (~45 min, Python / C++ / Java)

More modules, more surface area, a ticket backlog. Work ticket by ticket.

| Pack | Service | What it is |
| --- | --- | --- |
| [harbor](round-2/python/harbor) | Payments Service | Accounts, a double-entry ledger, holds, and idempotent transfers. |
| [meridian](round-2/python/meridian) | Calendar Service | Scored meeting requests scheduled in batches around protected events. |
| [cinder](round-2/python/cinder) | Market Data Service | A snapshot-plus-incremental quote cache with a subscription fan-out. |
| [drift](round-2/python/drift) | Fulfillment Service | A catalog, on-hand inventory, and reservations behind an availability view. |
| [aperture](round-2/python/aperture) | Job Orchestration | A ready queue, a registry, and a dispatcher with retries and dead-lettering. |
| [kestrel](round-2/python/kestrel) | Matching Engine | A single-symbol limit order book with price-time priority matching. |
| [basalt](round-2/python/basalt) | Risk Netting | Per-counterparty, per-symbol netting of signed trades. |
| [galena](round-2/python/galena) | Message Bus | Topic pub/sub with wildcard matching and isolated fan-out. |
| [saffron](round-2/python/saffron) | Session Service | A TTL session store with expiry, refresh, and cleanup. |
| [ridgeline](round-2/python/ridgeline) | Cache Tier | A capacity-bounded LRU cache. |

## How to practice

1. Pick a pack and a language, and start a timer (35 min for round 1, 45 min for round 2).
2. Read the pack `README.md`, then its `AGENTS.md` and `prep/WORKFLOW.md`. Round 1 gives
   the system and the reported symptom; round 2 gives the service map and a `tickets/`
   backlog. Note the symptom, not a bug location.
3. Map the code. Form a hypothesis about what is actually wrong.
4. **Write a test that reproduces it** and watch it fail. That failing test is your proof
   the bug is real, and the thing you will turn green.
5. Fix the narrowest layer. Keep every test you wrote green. Do not change behaviour the
   pack did not ask you to.
6. Narrate the whole time: the invariant each bug breaks, the state transitions, time and
   space complexity, whether the operation should be idempotent, and what changes in a
   concurrent or distributed version.

Every exercise carries its own preparation material. Start with that exercise's
`AGENTS.md`, then read `prep/WORKFLOW.md` for the A–F loop, triage rubric, findings log,
and open-ended mode. Use `prep/AI_PROMPTS.md` for prompts that keep the investigation
yours. The material is self-contained: it does not assume a ticket list, a particular
round, or a specific language, so an exercise works when opened on its own. When
`tickets/` is present, treat the tickets as reported symptoms, not a complete bug list.

Treat any AI assistant the way the round expects: use it to understand the code and
sanity-check your tests, write and own the fix yourself.

## Practising with a local AI assistant

The real rounds let you use an AI assistant. If you do not have a paid AI subscription, a
free, offline option is the
[AIInterviewPrepChat](https://marketplace.visualstudio.com/items?itemName=samthemogul.ai-interview-prep-chat)
VS Code extension by Samuel Emeka. It runs a local model through [Ollama](https://ollama.com),
so your code and conversations stay on your machine, with no accounts, API keys, or internet
connection needed.

It has two interview settings that line up with these packs:

- **Guarded** — like a standard coding test (and Bloomberg's round shape): the AI explains
  errors, concepts, and code, and only writes code for an approach you describe yourself.
  Use it to drill the "map the code, then verify" loop.
- **Unguarded (Agent)** — like a code-repos round: the agent proposes file edits as diffs
  you review and accept or reject. Use it to practise reviewing AI output like a teammate's
  pull request.

It also keeps a local practice transcript so you can review how you used the assistant
afterwards. Requires VS Code 1.90 or later and Ollama.

## Practising on real codebases in the browser

[Groundwork](https://groundwork-two-roan.vercel.app/) (beta) is a hosted version of this
same drill: "Every engineer gets a real codebase," nothing to install. You get a timed
ticket (a bug report, a failing test suite, or a small feature) pinned to a real repository,
an isolated browser-based VS Code editor and terminal with dependencies preinstalled and no
internet, and a 30 to 35 minute budget. Tasks are in TypeScript and Python (Node, Express,
Jest, pytest). On submit, hidden checks run against the behaviour the ticket describes and
the repo's existing tests run again; you get your diff, each check's pass or fail, and your
duration, with no composite score and no leaderboard.

It has a built-in AI assistant, **Pair**, that reads the repository and explains code. In
its default **guarded** mode it will not write the fix, which is exactly the Bloomberg
posture: use the assistant to understand the code, then write and own the change yourself.
You can switch it to an ordinary assistant, and that choice is recorded with the attempt.

It is free to start and needs an account. Use Groundwork for the "unfamiliar codebase under
time pressure" muscle in TypeScript and Python; use the packs in this repo when you want to
drill offline, or in C++ and Java, or rehearse the round-1 explain-out-loud flow.


## Baseline vs Solutions

- `round-1/` and `round-2/` contain the original unsolved exercises (READMEs, tickets, and
  source). These are preserved as the baseline.
- `solutions/` contains completed answers and regression tests for a subset of exercises.
  Coverage is intentionally partial. It currently includes Python solutions for
  `round-1` packs `cobalt`, `halcyon`, `lumen`, and `marlin`; there are no `round-2`
  solutions yet.
- Do not read `solutions/` during a timed attempt. Use it only for post-attempt review.
- To run a solution, use the same conventions as the baseline (e.g., `pytest -q` in the
  solution directory if tests are present).
