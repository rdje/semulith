# MC-MULTICORE: extend and revalidate the CPU for multiple cores

## Metadata

- Tree ID: `MC-MULTICORE`
- Status: `proposed`
- Roadmap lane: `ROADMAP.md` §6 and §"Separate multicore and optimization work"
- Gate: a separate multicore CPU gate
- Depends on: the CPU release gate
- Unlocks: the later SMP system, jointly with `P7-COMPUTER`
- Created: `2026-09-13`
- Owner: repo-local workflow

## Goal

Extend the CPU and environment contract to multiple cores — memory model, atomicity,
reservations, event delivery, fairness — and **revalidate**, so that multicore is a processor
milestone with its own evidence rather than a threading change.

## Non-Goals

- **Host threads are not multicore.** Host concurrency is an implementation mechanism only
  (`ENV-04`).
- No research-grade memory-model checker built as an incidental emulator feature. Weak-memory
  exploration uses a separately selected existing checker and a pinned litmus corpus
  (`ROADMAP.md`, multicore section).
- SMP Linux is a later **integration test**, not the evidence for this gate.

## Acceptance Criteria — the multicore CPU gate

Distinct obligations for atomicity, reservation invalidation, coherence and ordering, interrupt
delivery, and forward progress, each with evidence, before SMP integration.

## Task Tree

- ID: `MC-MULTICORE.1` — **extend the CPU/environment contract**
  Status: `pending`
  Goal: multi-core memory and progress rules, reservation invalidation events the environment must report, event delivery across cores (`docs/CPU_ENVIRONMENT.md` §6).
  Acceptance: a new contract **version**; the single-core contract is not edited in place.

- ID: `MC-MULTICORE.2` — **atomicity and reservations across cores**
  Status: `pending`
  Goal: atomic widths, mixed-size accesses, reservation success/failure, overlap, external write and context cases (catalog `C16`).
  Acceptance: external invalidation events are supplied by the environment and tested, not assumed absent.

- ID: `MC-MULTICORE.3` — **the execution model, stated honestly**
  Status: `pending`
  Goal: a deterministic sequentially consistent mode, if chosen, whose produced executions satisfy the selected architecture.
  Acceptance: the report states that producing only legal executions is **not** coverage of all allowed weak behaviour — that is a separate claim with its own method (`EVD-01`, `ROADMAP.md` multicore section).

- ID: `MC-MULTICORE.4` — **interrupt delivery and fairness**
  Status: `pending`
  Goal: per-core interrupt routing and acceptance; forward-progress obligations, including what "eventually" means and how it is evidenced.
  Acceptance: a source phrase such as "eventually" carries its chosen fairness assumption and evidence method, **not** an arbitrary test timeout (`docs/CPU_ENVIRONMENT.md` §3).

- ID: `MC-MULTICORE.5` — **weak-memory exploration, if claimed**
  Status: `pending`
  Goal: select an existing operational or axiomatic checker, pin a litmus corpus, and record configuration and coverage claims.
  Acceptance: if this leaf is not done, the project does **not** claim weak-memory coverage. Silence is the honest state, not an implied pass.

- ID: `MC-MULTICORE.6` — **revalidate the affected single-core evidence**
  Status: `pending`
  Goal: apply the conservative change-impact policy — shared memory-contract and event-scheduling changes default to broad affected-profile validation (`EVD-07`).
  Acceptance: previously passing evidence touched by these changes is marked stale and re-run, not inherited.

- ID: `MC-MULTICORE.7` — **the multicore gate report**
  Status: `pending`
  Goal: generate from pinned inputs.
  Acceptance: names exactly which obligations have evidence and which are unclaimed.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `MC-MULTICORE.1` | `pending` | the contract is what the rest of the leaves test against |

## Decisions

- `2026-09-13`: multicore is a **separate CPU extension and validation milestone**. It never
  arrives merely by adding host threads (`ROADMAP.md` §1).

## Open Questions

- Which existing weak-memory checker, if any. Unresolved until `.5` is actually scoped; until
  then the coverage claim does not exist.

## Blockers

- The CPU release gate.

## Acceptance Checklist (filled per leaf at execution time)

- [ ] **ROOT CAUSE (WHY + WHERE)** — <the command run and its real output>
- [ ] **ADDRESSED (verified)** — <measured before → after>
- [ ] **NO REGRESSION** — <the suite or gate re-run, and its result>
- [ ] **FIX** — <the change made>
- [ ] **LOCKSTEP** — <docs, contracts and indexes updated>

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| — | — | not started | — |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| — | `pending` | `pending` |

## Changelog

- `2026-09-13`: Created from `ROADMAP.md` §6 and the multicore section by `SEMULITH-TREES.3`.
