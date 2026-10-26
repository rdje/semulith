# LIVE_STATUS.md — authoritative live progress tracker

Rows use ONLY these four states: **Done · Mostly Done · In Progress · Not Started**.
Review and update before every commit whenever actual closure or remaining scope changes;
summarize the snapshot in every commit-workflow completion message.

## Foundation

| Area | Status | Notes |
| --- | --- | --- |
| Discipline spine (`bedrock` 0.6.1) | Done | memory · task-trees · commit workflow · doctrine enforcement · mdBook |
| Planning package v0.2 ingested | Done | [`SEMULITH-PKG`](docs/tasks/SEMULITH-PKG.md) |
| Claim-verification standard adopted | Done | `docs/CLAIM_VERIFICATION.md`; §5A tags and §7 constant sweep not mechanized |
| Project doctrines (41 registered) | Done | `scripts/check_doctrines.project.sh` — 1675 self-test arms, each fired RED before registration |
| Spine defects repaired at source | Done | fixed in `check_task_acceptance.sh`, watched by `SEAM-INTEGRITY` |
| README policy + routing closure | Done | 85 lines / 4,864 B; 44 destinations |
| mdBook is the review surface | Done | 50 chapters; the doctrine chapter is gated against the registry; the API reference is rustdoc, built with it |
| Hand-kept mirrors gated | Done | [`MIRROR-DRIFT`](docs/tasks/MIRROR-DRIFT.md) 4/4 |
| Roadmap converted to task-trees | Done | [`SEMULITH-TREES`](docs/tasks/SEMULITH-TREES.md) — all 11 lanes are trees |
| Reference models acquired | Done | Sail 0.14, Spike `1e05ddac`, QEMU 11.1.1 pinned; ACT located. `scripts/fetch_references.sh` |
| Matched-profile evidence path | Done | 4 guests, 2 models, 34 spec-derived values, 4 negative observations, 7 differences; `scripts/run_smoke.py` |
| Requirements catalogue seeded | Done | `P0-PROFILE.3` — 28 records, schema-validated |
| Profile dossier in the one format | Done | `SOT-FORMAT.4` — every dossier document behind the schema layer |
| Environment contract v0 | Done | `P0-PROFILE.4` — `rv64i-lab-env-v0`: 36 obligations; 72 checks **declared not implemented** |
| Reference independence inventoried | Done | Historical 6 rows; ancestry basis withdrawn; current record sweep: `P4-SYSTEM.14` |
| North star: model widely, start small | In Progress | `decision_one-definition-one-book` — 6 units today |
| Dual mandate: production + teaching | In Progress | `decision_dual-mandate-production-and-teaching` — mistakes stay in the record |
| Composition of models | Done | [`MODEL-COMPOSE`](docs/tasks/MODEL-COMPOSE.md) 6 of 6 leaves; closure qualifies no processor/board |
| Canonical definition (engine input) | Done | [`MODEL-METHOD`](docs/tasks/MODEL-METHOD.md) 19/19 — semantics 52/52, cited not verified |
| Modelling method + materials | Done | same tree — `docs/METHOD.md` |
| Per-unit books | Done | [`MODEL-BOOKS`](docs/tasks/MODEL-BOOKS.md) 8/8 — `UNIT-BOOKS` gates it |
| Rust-native tooling: rustdoc, cargo xtask | In Progress | [`RUSTDOC`](docs/tasks/RUSTDOC.md) 7/7 done (100% documented, gated); [`XTASK`](docs/tasks/XTASK.md) — xtask incrementally, nothing breaks |

## Roadmap milestones (`ROADMAP.md` §6)

| Milestone | Gate | Status | Notes |
| --- | --- | --- | --- |
| P0 — profile and evidence access | G0 | Done | [`P0-PROFILE`](docs/tasks/P0-PROFILE.md) 10/10 — **gate `G0` RUN, verdict `incomplete`**: 68 declared checks unimplemented; matched on the ISA, **not the platform** |
| P1 — processor laboratory | G1 | Done | [`P1-LAB`](docs/tasks/P1-LAB.md) 13/13 — **gate `G1` RUN, verdict `passed` (`2026-09-30`)** |
| P2 — validated RV64I profile | CPU-LAB | Done | [`P2-SCALAR`](docs/tasks/P2-SCALAR.md) 9/9 — CPU-LAB report `incomplete` (G-CONTRACT/G-OBLIGATIONS open); EXPERIMENTAL release decision recorded |
| DSP specification and stress review | — | Done | [`DSP-REVIEW`](docs/tasks/DSP-REVIEW.md) 8/8 — six findings routed to `P3-BREADTH.1`; no oracle claim |
| P3 — shared interfaces + real DSP slice | BREADTH | Done | [`P3-BREADTH`](docs/tasks/P3-BREADTH.md) 6 of 7 leaves done; gate `BREADTH` RUN, verdict **`passed`**; TI C6000 / SHARC unclaimed |
| P4 — Linux CPU profile | CPU-SYSTEM | In Progress | [`P4-SYSTEM`](docs/tasks/P4-SYSTEM.md) 14/18; `.14` open — the M case measures 10 of 10 policy legs and credits `REQ-GC-M` `implemented` (CR-GC-M-1, 2026-10-26) |
| P5 — board model | BOARD | In Progress | [`P5-BOARD`](docs/tasks/P5-BOARD.md) — 10/12; probes and gate report wait on the CPU |
| archogen OS integration | ARCHOGEN-OS | Not Started | [`AG-OS`](docs/tasks/AG-OS.md) — 8 leaves |
| P6 — Linux userspace | LINUX | Not Started | [`P6-LINUX`](docs/tasks/P6-LINUX.md) — 8 leaves; a banner is not a pass |
| P7 — useful headless computer | SYSTEM | Not Started | [`P7-COMPUTER`](docs/tasks/P7-COMPUTER.md) — 7 leaves; the declared suite is the claim |
| Separate multicore CPU work | multicore gate | Not Started | [`MC-MULTICORE`](docs/tasks/MC-MULTICORE.md) — 7 leaves; host threads are not multicore |

Every row above is project state, not a conformance claim — G1 `passed` (a laboratory gate); G0 ran `incomplete`.
