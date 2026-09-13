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
| Project doctrines (10 registered) | Done | `DELIVERY-PROVENANCE`, `FIXTURE-FINGERPRINT`, `README-ROUTING-CLOSURE`, `PROFILE-CONSISTENCY`, `SEAM-INTEGRITY`, `FRONTIER-SYNC`, `REGISTRY-MIRROR`, `TREE-CLAIMS`, `DERIVED-COUNTS`, `RECORD-SCHEMA` — 137 self-test arms, all fired RED before registration |
| Spine defects repaired at source | Done | fixed in `check_task_acceptance.sh`, off the re-sync list, watched by `SEAM-INTEGRITY` |
| README policy + routing closure | Done | caps 85 lines / 4,864 B; 25 destinations governed; containment deferred with a trigger |
| mdBook is the review surface | Done | 27 chapters; contracts included verbatim; its doctrine chapter is gated against the registry |
| Hand-kept mirrors gated | Done | [`MIRROR-DRIFT`](docs/tasks/MIRROR-DRIFT.md) 4/4 — the index, the doctrine documents, task-tree facts, and every other derived count in the live docs |
| Roadmap converted to task-trees | Done | `SEMULITH-TREES` — all 11 lanes are trees, registered, bounded, and mapped in the book |

| Reference models acquired | Done | 3 obtained and pinned (Sail RISC-V 0.14, Spike `1e05ddac`, QEMU 11.1.1); ACT located, unacquired. `scripts/fetch_references.sh` re-derives every pin |
| Matched-profile evidence path | Done | `P0-PROFILE.6` — 2 models agree over 15 aligned steps incl. a trap; 12 spec-derived values; 4 differences; reproduces. `scripts/run_smoke.py` |
| Requirements catalogue seeded | Done | `P0-PROFILE.3` — 25 machine-readable records, one per decision, validated by a tracked schema validator |
| Environment contract v0 | Done | `P0-PROFILE.4` — `rv64i-lab-env-v0`: 33 obligations, all 10 boundary items dispositioned (4 in scope, 6 out with reasons), 66 checks **declared not implemented** |
| Reference independence inventoried | Done | `P0-PROFILE.7` — 6 pairs, 4 verdict classes. FP is **shared**: 184 of 199 SoftFloat files byte-identical, routed to `P4-SYSTEM.7`. Encoding is not shared. 2 QEMU pairs unexamined, recorded as such |

## Roadmap milestones (`ROADMAP.md` §6)

| Milestone | Gate | Status | Notes |
| --- | --- | --- | --- |
| P0 — profile and evidence access | G0 | In Progress | [`P0-PROFILE`](docs/tasks/P0-PROFILE.md) — 7 of 9 leaves; profile, state, a 25-record requirements catalogue and a 33-obligation environment contract; 2 models agree over 15 aligned steps with their independence inventoried; the gate is `incomplete` |
| P1 — processor laboratory | G1 | Not Started | [`P1-LAB`](docs/tasks/P1-LAB.md) — 12 leaves; the three crates, graph checker, mutation suite |
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
