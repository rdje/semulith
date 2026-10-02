# Task-Tree Workflow

This document defines the repo-local task-tree workflow. A step-by-step setup guide is in
[TASK_TREE_README.md](TASK_TREE_README.md). Individual trees live under
[`tasks/`](tasks/); the leaf template is [`tasks/TEMPLATE.md`](tasks/TEMPLATE.md).

## Purpose

Use a task tree when a top-level task is too broad to finish safely as one signoff-quality
slice, or when it is expected to discover subtasks over time. The tree owns the recursive
breakdown, current frontier, acceptance criteria, blockers, decisions, validation, and
completion evidence for one top-level task — so the project survives a lost session and
continuity holds across sessions, machines, and harness switches.

The tree is not a second roadmap. `ROADMAP.md` states the high-level direction; a task tree
owns the disciplined execution of one lane of it.

## Code-change doctrine (binding, non-negotiable)

**It is strictly forbidden to make any code change unless it is first tracked/owned by a
task-tree leaf.** "Code change" = any edit to Rust sources, `Cargo.toml`/build scripts,
generated artifacts, or anything altering behavior. Before touching code, a leaf must exist
that owns the change (create/extend a tree, or add a leaf). The leaf — its goal, acceptance,
verification, and commit — is the unit of traceability. Enforced by
`scripts/check_task_tree_ownership.sh`.

## Leaf lifecycle (statuses)

`proposed` → `pending` → `active`/`in_progress` → `done`. A leaf is `done` only when its
acceptance criteria are met, verification is recorded, and it is committed via `COMMIT.md`.
Mark `blocked` (with the blocker named) rather than leaving a stalled leaf `active`.

## The pivot rule

**Do not pivot to a different task-tree while the repo is dirty.** The repo is
handoff-ready only when the tree is clean (no modified/untracked work except the task-tree
file itself). Finish the current leaf and get the repo clean before switching — even if
asked to pivot immediately. The guarantor of repo integrity holds this line.

## Commit traceability

Each slice uses a work-unit id in the commit subject (e.g. `MYPROJ-AREA-0007`). When the
slice belongs to a leaf, the subject or first body line also names the leaf ID
(e.g. `MYPROJ-AREA-0007 (leaf FEATURE-X.2): …`), so the slice id and the tree node coexist
on the same commit. One commit per completed leaf.

## Active Task Trees

<!-- ANCHOR: trees -->
| Tree | Status | Frontier (next leaf) | Owner |
| --- | --- | --- | --- |
| [`SEMULITH-TREES`](tasks/SEMULITH-TREES.md) | `done` | — (4/4 leaves complete) | repo-local |
| [`P0-PROFILE`](tasks/P0-PROFILE.md) | `done` (reopened once, for `.10` — a measured defect the first nine leaves carried) | — (10/10 leaves complete) | repo-local |
| [`P1-LAB`](tasks/P1-LAB.md) | `done` (reopened once, for `.13` — the `.11` allocation figures had to be proven, not reported) | — (13/13 leaves complete; gate G1 RUN, verdict `incomplete` — criterion 6 routed to the P2-SCALAR tree) | repo-local |
| [`P2-SCALAR`](tasks/P2-SCALAR.md) | `done` | — (9/9 leaves complete; the CPU-LAB report reads `incomplete` with G-CONTRACT/G-OBLIGATIONS named — the release decision is the EXPERIMENTAL release of the versioned artifact, `decision_release-rv64i-lab-v0`) | repo-local |
| [`DSP-REVIEW`](tasks/DSP-REVIEW.md) | `done` | — (8/8 leaves complete; six findings routed to P3-BREADTH's first leaf, each with its ROUTING EVIDENCE — none reproduces on the scalar profile) | repo-local |
| [`P3-BREADTH`](tasks/P3-BREADTH.md) | `done` | — (8/8 leaves complete; gate `BREADTH` RUN `2026-10-01`, verdict **`passed`** — the capability report published at `docs/BREADTH-REPORT.md`) | repo-local |
| [`P4-SYSTEM`](tasks/P4-SYSTEM.md) | `proposed` | `.1` — resolve the profile (gate `CPU-SYSTEM`) | repo-local |
| [`P5-BOARD`](tasks/P5-BOARD.md) | `active` | `.3` — generated maps and the hardware description (4/11 leaves done; the platform specified, both device dossiers gated, the three units registered) | repo-local |
| [`AG-OS`](tasks/AG-OS.md) | `proposed` | `.1` — inspect the real eADL interfaces (gate `ARCHOGEN-OS`) | repo-local |
| [`P6-LINUX`](tasks/P6-LINUX.md) | `proposed` | `.1` — pin the system (gate `LINUX`) | repo-local |
| [`P7-COMPUTER`](tasks/P7-COMPUTER.md) | `proposed` | `.1` — declare the workload suite (gate `SYSTEM`) | repo-local |
| [`MC-MULTICORE`](tasks/MC-MULTICORE.md) | `proposed` | `.1` — extend the CPU/environment contract | repo-local |
| [`MODEL-COMPOSE`](tasks/MODEL-COMPOSE.md) | `done` | — (6/6 leaves complete; a composition is a verdict, a discharge, and a materializable unit) | repo-local |
| [`MODEL-METHOD`](tasks/MODEL-METHOD.md) | `done` (reopened once, for the per-kind chapter) | — (19/19 leaves complete; the demand chapter landed and is a LIVE chapter `2026-10-01`) | repo-local |
| [`MODEL-BOOKS`](tasks/MODEL-BOOKS.md) | `done` | — (8/8 leaves complete; the per-unit book structure, the five-chapter arc, and the `UNIT-BOOKS` gate — every registered unit has a book that builds) | repo-local |
| [`SOT-FORMAT`](tasks/SOT-FORMAT.md) | `done` | — (10/10 leaves complete; the `SOURCE-FORMAT` gate registered, the format split cannot return) | repo-local |
| [`PUSH-DISCIPLINE`](tasks/PUSH-DISCIPLINE.md) | `done` | — (3/3 leaves complete; the cadence, the named suite at the boundary, and the append-only approval record gated by `PUSH-RECORD`) | repo-local |
| [`DOC-SHARDING`](tasks/DOC-SHARDING.md) | `done` | — (2/2 leaves complete; both append heads shard into `docs/changelog/` under one frozen manifest) | repo-local |
| [`PORT-WEB`](tasks/PORT-WEB.md) | `done` | — (1/1 leaves complete; the crate skeleton builds for `wasm32-unknown-unknown` from its first slice, gated by `PORT-WEB`) | repo-local |
| [`UPSTREAM-TRACK`](tasks/UPSTREAM-TRACK.md) | `done` | — (4/4 leaves complete; age and exposure derived by command, `blocks` gated, the tree closed) | repo-local |
| [`LAB-BENCH`](tasks/LAB-BENCH.md) | `active` | `.2` — proposed: stepping, register view, live traces (1 of 2 leaves done; `semulith demo` + the browser bench land) | repo-local |
| [`BOOK-APPARATUS`](tasks/BOOK-APPARATUS.md) | `done` | — (2/2 leaves complete; the index landed generated + gated by `BOOK-INDEX`, and the first reading-experience audit pass revised 13 of the 29 main-line chapters — the yield was factual drift) | repo-local |
| [`MEMORY-POINTER`](tasks/MEMORY-POINTER.md) | `done` | — (1/1 leaves complete; MEMORY.md is the §6 next-action pointer per the director's `2026-10-02` ruling — 34/7,031 → 29/1,865) | repo-local |
| [`MCU-DOCS`](tasks/MCU-DOCS.md) | `done` | — (2/2 leaves complete; the twelve answers reconciled same-day — twelve MCU documents adopted and digest-verified into `.materials/mcu/`) | repo-local |
| [`ARTIFACT-CLEANUP`](tasks/ARTIFACT-CLEANUP.md) | `active` | — (1/1 leaves done; next cleanup is time-triggered) | repo-local |
| [`PREFIX-DISCIPLINE`](tasks/PREFIX-DISCIPLINE.md) | `done` | — (1/1 leaves complete; the SEMULITH- prefix pinned in `commit-msg`, watched behaviourally by `COMMIT-PREFIX` #29 — history keeps both spellings, immutably) | repo-local |
| [`ROADMAP-V3`](tasks/ROADMAP-V3.md) | `done` | — (3/3 leaves complete; consumed by the v0.4 revision at P1 first slice) | repo-local |
| [`MIRROR-DRIFT`](tasks/MIRROR-DRIFT.md) | `done` (reopened once, for `.4` — a mirror class the first three leaves did not cover) | — (4/4 leaves complete) | repo-local |
| [`SEMULITH-PKG`](tasks/SEMULITH-PKG.md) | `done` | — (9/9 leaves complete) | repo-local |
| [`BOOTSTRAP`](tasks/BOOTSTRAP.md) | `done` | — | repo-local |

Milestone trees are `proposed` until their first leaf starts. Each names its gate, its
dependencies, and the `ROADMAP.md` section it derives from, so it can be checked against the
plan rather than trusted.
<!-- ANCHOR_END: trees -->
