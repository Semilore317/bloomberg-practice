# bloomberg-practice

Interview-grade practice for Bloomberg's AI-assisted codebase rounds. Each pack is an
**unfamiliar codebase** under a codename that reveals nothing about the domain. Read the pack, map
the code, find the deliberately planted bugs, make the suite green with the smallest honest
changes, and be ready to explain every change out loud.

The two rounds have deliberately different shapes:

- `round-1/` — mirrors the **real Bloomberg format**: you join a mostly-working service late in
  development, **most tests pass, and a few planted bugs fail**. One domain object, a clear state
  machine, subtle lifecycle and invariant bugs. Target ~35 minutes. The job is surgical debugging
  plus explaining your reasoning, not a rebuild.
- `round-2/` — a harder, **all-red stress drill**: a larger multi-module microservice where
  **every test fails by default**, tuned harder than the real round. Target ~45 minutes.

There are no solution files in the repository. For round 1 a green suite is the proof; for round 2
the acceptance tests are the only answer key.

## Languages

Every pack is implemented three times, once per language, with the **same spec and the same planted
bugs**. Pick the language you want to interview in.

```text
round-1/halcyon/                         round-2/harbor/
  CANDIDATE_BRIEF.md                       README.md
  PROJECT_MANAGER_NOTES.md                 SETUP.md
  SELF_REVIEW_AFTER.md                     tickets/
  SETUP.md                                 python/  cpp/  java/
  python/  cpp/  java/
```

Round 1 ships the real-interview document set: a candidate brief, a list of clarifying questions to
ask the interviewer (who plays the project manager), and a self-review guide to read afterwards.
Round 2 keeps a README and a ticket backlog.

Quick run (any pack, any language):

```bash
cd round-1/halcyon/python && pytest -q         # or: cd ../cpp && make test
cd round-1/halcyon/java   && javac *.java && java Tests
cd round-2/harbor/python  && pytest -q
```

To add your own packs or a language port, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Round 1 — mostly-green, join a service late (~35 min, Python / C++ / Java)

Most tests pass. The few that fail are the reported bugs. Each pack is one stateful domain object
with a lifecycle and invariants to protect.

| Pack | Domain | What it is |
| --- | --- | --- |
| [halcyon](round-1/halcyon) | Order Lifecycle | Working orders placed, filled, and cancelled; open-quantity and over-fill invariants. |
| [marlin](round-1/marlin) | Inventory Reservations | TTL stock holds, commit versus release, expiry returns units automatically. |
| [zephyr](round-1/zephyr) | Subscription Entitlement | Trial, active, suspended, cancelled lifecycle with trial expiry. |
| [cobalt](round-1/cobalt) | Wallet Holds | Authorization holds, capture versus void, available equals balance minus holds. |
| [quasar](round-1/quasar) | Rate Limiter | Fixed-window per-key limiter with window reset and remaining quota. |
| [onyx](round-1/onyx) | Access Tokens | Short-lived tokens: issue, validate, refresh, revoke, with TTL expiry. |
| [pike](round-1/pike) | Approval Workflow | Documents go pending then approved, rejected, or withdrawn; terminal states. |
| [vesper](round-1/vesper) | Connection Pool | Fixed-capacity acquire, release, and close, with a capacity invariant. |
| [tundra](round-1/tundra) | LRU + TTL Cache | Capacity-bounded cache with per-entry TTL and least-recently-used eviction. |
| [lumen](round-1/lumen) | Job State Machine | Queued, running, done, failed, with retries and an attempt budget. |

## Round 2 — all-red microservices (~45 min, Python / C++ / Java)

Every test fails by default. Larger codebases, more surface area, tuned harder than the real round.

| Pack | Service | What it is |
| --- | --- | --- |
| [harbor](round-2/harbor) | Payments Service | Accounts, a double-entry ledger, holds, and idempotent transfers. |
| [meridian](round-2/meridian) | Calendar Service | Scored meeting requests scheduled in batches around protected events. |
| [cinder](round-2/cinder) | Market Data Service | A snapshot-plus-incremental quote cache with a subscription fan-out. |
| [drift](round-2/drift) | Fulfillment Service | A catalog, on-hand inventory, and reservations behind an availability view. |
| [aperture](round-2/aperture) | Job Orchestration | A ready queue, a registry, and a dispatcher with retries and dead-lettering. |
| [kestrel](round-2/kestrel) | Matching Engine | A single-symbol limit order book with price-time priority matching. |
| [basalt](round-2/basalt) | Risk Netting | Per-counterparty, per-symbol netting of signed trades. |
| [galena](round-2/galena) | Message Bus | Topic pub/sub with wildcard matching and isolated fan-out. |
| [saffron](round-2/saffron) | Session Service | A TTL session store with expiry, refresh, and cleanup. |
| [ridgeline](round-2/ridgeline) | Cache Tier | A capacity-bounded LRU cache. |

## How to practice

### Round 1 (the real-interview drill)

1. Pick a pack and a language, start a ~35 minute timer.
2. Read `CANDIDATE_BRIEF.md`. Run the tests. Most pass; a few fail. Those failures are the bugs.
3. Treat the interviewer as the project manager. Before you change behaviour, ask the clarifying
   questions in `PROJECT_MANAGER_NOTES.md` (what should a double action do, can an expired thing
   still be used, and so on).
4. Isolate each failing test, fix the narrowest layer, and keep every passing test green.
5. Narrate the whole time: the invariant each bug breaks, the state transitions, time and space
   complexity, whether the operation should be idempotent, and what changes in a concurrent or
   distributed version.
6. Afterwards, read `SELF_REVIEW_AFTER.md` and check what you missed.

### Round 2 (the stress drill)

1. Pick a pack and a language, start a ~45 minute timer.
2. Read the pack `README.md` and the `tickets/`. Run the tests: all red.
3. Map the modules, isolate a bug with a failing test, patch the narrowest layer, turn the suite
   green, and keep ownership of anything an AI assistant writes.

## Practising with a local AI assistant

The real rounds let you use an AI assistant. If you do not have a paid AI subscription, a free,
offline option is the
[AIInterviewPrepChat](https://marketplace.visualstudio.com/items?itemName=samthemogul.ai-interview-prep-chat)
VS Code extension by Samuel Emeka. It runs a local model through [Ollama](https://ollama.com), so
your code and conversations stay on your machine, with no accounts, API keys, or internet
connection needed.

It has two interview settings that line up with these packs:

- **Guarded** — like a standard coding test (and Bloomberg's round shape): the AI explains errors,
  concepts, and code, and only writes code for an approach you describe yourself. Use it to drill
  the "map the code, then verify" loop.
- **Unguarded (Agent)** — like a code-repos round: the agent proposes file edits as diffs you
  review and accept or reject. Use it to practise reviewing AI output like a teammate's pull
  request.

It also keeps a local practice transcript so you can review how you used the assistant afterwards.
Requires VS Code 1.90 or later and Ollama.
