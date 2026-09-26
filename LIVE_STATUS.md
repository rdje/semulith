# LIVE_STATUS.md — authoritative live progress tracker

Rows use ONLY these four states: **Done · Mostly Done · In Progress · Not Started**.
Review and update before every commit whenever actual closure or remaining scope changes;
summarize the snapshot in every commit-workflow completion message.

## Foundation

| Area | Status | Notes |
| --- | --- | --- |
| Discipline spine (`bedrock` 0.6.1) | Done | memory · task-trees · commit workflow · doctrine enforcement · mdBook |
| Planning package v0.2 ingested | Done | `SEMULITH-PKG` — docs landed, fingerprints gated, routes closed, book grown |
| Claim-verification standard adopted | Done | `docs/CLAIM_VERIFICATION.md`; §5A tags and §7 constant sweep not mechanized |
| Project doctrines (12 registered) | Done | `DELIVERY-PROVENANCE`, `FIXTURE-FINGERPRINT`, `README-ROUTING-CLOSURE`, `PROFILE-CONSISTENCY`, `SEAM-INTEGRITY`, `FRONTIER-SYNC`, `REGISTRY-MIRROR`, `TREE-CLAIMS`, `DERIVED-COUNTS`, `RECORD-SCHEMA`, `GATE-REPORT`, `UPSTREAM-INDEX` — 156 self-test arms, all fired RED before registration |
| Spine defects repaired at source | Done | fixed in `check_task_acceptance.sh`, off the re-sync list, watched by `SEAM-INTEGRITY` |
| README policy + routing closure | Done | caps 85 lines / 4,864 B; 31 destinations governed; containment deferred with a trigger |
| mdBook is the review surface | Done | 27 chapters; contracts included verbatim; its doctrine chapter is gated against the registry |
| Hand-kept mirrors gated | Done | [`MIRROR-DRIFT`](docs/tasks/MIRROR-DRIFT.md) 4/4 — the index, the doctrine documents, task-tree facts, and every other derived count in the live docs |
| Roadmap converted to task-trees | Done | `SEMULITH-TREES` — all 11 lanes are trees, registered, bounded, and mapped in the book |

| Reference models acquired | Done | Sail 0.14, Spike `1e05ddac`, QEMU 11.1.1 pinned; ACT located. `scripts/fetch_references.sh` |
| Matched-profile evidence path | Done | 4 guests, 2 models, 34 spec-derived values, 4 negative observations, 6 differences; `scripts/run_smoke.py` |
| Requirements catalogue seeded | Done | `P0-PROFILE.3` — 26 machine-readable records, one per decision, validated by a tracked schema validator |
| Environment contract v0 | Done | `P0-PROFILE.4` — `rv64i-lab-env-v0`: 33 obligations, all 10 boundary items dispositioned (4 in scope, 6 out with reasons), 66 checks **declared not implemented** |
| Reference independence inventoried | Done | 6 pairs, 4 verdicts; FP **shared** (184/199 files identical), routed to `P4-SYSTEM.7` |

| North star: model widely, start small | In Progress | `decision_one-definition-one-book` — kind + layer decide what a unit owns; 1 unit today |
| Dual mandate: production + teaching | In Progress | `decision_dual-mandate-production-and-teaching` — mistakes stay in the record |
| Composition of models | In Progress | [`MODEL-COMPOSE`](docs/tasks/MODEL-COMPOSE.md) 2/6 — union decidable and built; fragments reusable under `definitions/` |
| Canonical definition (engine input) | In Progress | [`MODEL-METHOD`](docs/tasks/MODEL-METHOD.md) 3/10 — encodings owned; semantics 52/52, cited not verified |
| Modelling method + materials | In Progress | same tree — no category→material binding yet |
| Per-unit books | Not Started | [`MODEL-BOOKS`](docs/tasks/MODEL-BOOKS.md) 0/6 — one definition, one mdBook |

## Roadmap milestones (`ROADMAP.md` §6)

| Milestone | Gate | Status | Notes |
| --- | --- | --- | --- |
| P0 — profile and evidence access | G0 | Done | [`P0-PROFILE`](docs/tasks/P0-PROFILE.md) 10/10 — **gate `G0` RUN, verdict `incomplete`**: all three criteria met, 68 declared checks unimplemented. Reopened for `.10`: the profile had been matched on its ISA and **not its platform** |
| P1 — processor laboratory | G1 | Not Started | [`P1-LAB`](docs/tasks/P1-LAB.md) — 12 leaves; the three crates, graph checker, mutation suite. Where the 66 declared checks acquire fixtures |
| P2 — validated RV64I profile | CPU-LAB | Not Started | [`P2-SCALAR`](docs/tasks/P2-SCALAR.md) — 9 leaves; the full processor gate |
| DSP specification and stress review | — | Not Started | [`DSP-REVIEW`](docs/tasks/DSP-REVIEW.md) — 7 leaves; real-spec pressure, no oracle claim |
| P3 — shared interfaces + real DSP slice | BREADTH | Not Started | [`P3-BREADTH`](docs/tasks/P3-BREADTH.md) — 6 leaves |
| P4 — Linux CPU profile | CPU-SYSTEM | Not Started | [`P4-SYSTEM`](docs/tasks/P4-SYSTEM.md) — 10 leaves; FP gated on qualification |
| P5 — board model | BOARD | Not Started | [`P5-BOARD`](docs/tasks/P5-BOARD.md) — 7 leaves; composition against the CPU contract |
| archogen OS integration | ARCHOGEN-OS | Not Started | [`AG-OS`](docs/tasks/AG-OS.md) — 8 leaves; adapter designed against the real eADL interface |
| P6 — Linux userspace | LINUX | Not Started | [`P6-LINUX`](docs/tasks/P6-LINUX.md) — 8 leaves; a banner is not a pass |
| P7 — useful headless computer | SYSTEM | Not Started | [`P7-COMPUTER`](docs/tasks/P7-COMPUTER.md) — 7 leaves; the declared suite is the claim |
| Separate multicore CPU work | multicore gate | Not Started | [`MC-MULTICORE`](docs/tasks/MC-MULTICORE.md) — 7 leaves; host threads are not multicore |

No gate has been run. Every row above is project state, not a conformance claim.
