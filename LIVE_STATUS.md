# LIVE_STATUS.md — authoritative live progress tracker

Rows use ONLY these four states: **Done · Mostly Done · In Progress · Not Started**.
Review and update before every commit whenever actual closure or remaining scope changes;
summarize the snapshot in every commit-workflow completion message.

## Foundation

| Area | Status | Notes |
| --- | --- | --- |
| Discipline spine (`bedrock` 0.6.1) | Done | memory architecture · task-trees · commit workflow · doctrine enforcement · mdBook skeleton |
| Planning package v0.2 ingested | Done | `SEMULITH-PKG` — docs landed, standard adopted, fingerprints gated, routes closed, book grown |
| Claim-verification standard adopted | Done | `docs/CLAIM_VERIFICATION.md`; §5A claim tags and §7 constant sweep not yet mechanized |
| Project doctrines (4 registered) | Done | `DELIVERY-PROVENANCE`, `FIXTURE-FINGERPRINT`, `README-ROUTING-CLOSURE`, `PROFILE-CONSISTENCY` — 36 self-test arms, all fired RED before registration |
| Doctrine seams declared | Done | `.doctrine/code_paths.txt` and `evidence_tokens.txt`, each measured against the tracked corpus and fired |
| README policy + routing closure | Done | reviewed caps 85 lines / 4,864 bytes; 24 destinations governed; containment doctrine deferred with a trigger |
| mdBook is the review surface | Done | 27 chapters; contracts included verbatim so the book cannot become a second owner |
| Roadmap converted to task-trees | Done | `SEMULITH-TREES` — all 11 lanes are trees, registered, bounded, and mapped in the book |

## Roadmap milestones (`ROADMAP.md` §6)

| Milestone | Gate | Status | Notes |
| --- | --- | --- | --- |
| P0 — profile and evidence access | G0 | In Progress | [`P0-PROFILE`](docs/tasks/P0-PROFILE.md) — 1 of 9 leaves; `rv64i-lab-v0` pinned and dossiered; the gate is `incomplete` |
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
