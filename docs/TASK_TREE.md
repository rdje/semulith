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
| [`P4-SYSTEM`](tasks/P4-SYSTEM.md) | `active` | `.18` — the verdict and the release decision: recorded evidence is held to what it covers and portability is re-measured over 210 guests (slice a); next the hosted matrix on this tree, which needs a push the director approves, then the named decision. All 48 requirements are settled: 46 `implemented`, 2 `not-applicable` (a51-14). 17/18 leaves done; CPU-SYSTEM `incomplete`, 1 of 10 axes open, `G-RELEASE` | repo-local |
| [`P5-BOARD`](tasks/P5-BOARD.md) | `active` | `.5` — firmware probes, gated on the CPU's acceptance trajectory (10/12 leaves done; the platform capability manifest landed, drift-gated by PLATFORM-GEN) | repo-local |
| [`AG-OS`](tasks/AG-OS.md) | `proposed` | `.1` — inspect the real eADL interfaces (gate `ARCHOGEN-OS`) | repo-local |
| [`P6-LINUX`](tasks/P6-LINUX.md) | `proposed` | `.1` — pin the system (gate `LINUX`) | repo-local |
| [`P7-COMPUTER`](tasks/P7-COMPUTER.md) | `proposed` | `.1` — declare the workload suite (gate `SYSTEM`) | repo-local |
| [`MC-MULTICORE`](tasks/MC-MULTICORE.md) | `proposed` | `.1` — extend the CPU/environment contract | repo-local |
| [`LAB-BENCH`](tasks/LAB-BENCH.md) | `active` | `.2` — proposed: stepping, register view, live traces (1 of 2 leaves done; `semulith demo` + the browser bench land) | repo-local |
| [`ARTIFACT-CLEANUP`](tasks/ARTIFACT-CLEANUP.md) | `active` | `ARTIFACT-CLEANUP.40` — the next recurring cleanup (due 24 h after 2026-11-07T11:06Z), the orphan act before its four; the feature cycle resumes meanwhile | repo-local |
| [`LIVE-CONTAINMENT`](tasks/LIVE-CONTAINMENT.md) | `active` | `.4` — active: archive sealed, full doctrine adoption remains (3 of 4 leaves done) | repo-local |
| [`XTASK`](tasks/XTASK.md) | `active` | `XTASK.13` — ruling 5's rule for the eleven fragile doctrines (frozen copies; a damaged live source fails by name), one slice each between feature units: slices a (DEF-GEN) and b1 (GUEST-GEN census/surgical) done 2026-10-29, b2 (GUEST-GEN mirror/count) 2026-11-02, b3 (GUEST-GEN parcel author) 2026-11-03, b4 (the author probes' owned corpus, and a real-run step) 2026-11-04, b5 (their other corpus reads), b6 (the rest of its self-test: GUEST-GEN whole) c (BOOK-INDEX) 2026-11-05, d (BOARD-GEN), e (PLATFORM-GEN), f (MATERIALS-BILL) 2026-11-06, g (EXERCISE-COVERAGE), h (CONTRACT-FREEZE), i (RECORD-SCHEMA) and j (UNIT-BOOKS) 2026-11-07; PROFILE-CONSISTENCY's probes next. Hosted CI green on cefb0d84 (XTASK.12 done); XTASK.4 done by ruling 2; the project registry's drivers in Rust behind held shims — 42 of 42 drivers through shims, the count re-derived by `DERIVED-COUNTS` (13 of 14 leaves done) | repo-local |
<!-- ANCHOR_END: trees -->
