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
| [`P4-SYSTEM`](tasks/P4-SYSTEM.md) | `active` | `.20` — the next pinned window, version 1 (`decision_the-next-window-is-version-1.md`): slice a done (`SEMULITH-P4-0403`): the label in `identity.sexp` in every profile, the 42 credits it lapsed retired, the live report `incomplete` with four axes owned; a2 done (`SEMULITH-P4-0404`): the board's processor version held to the unit's identity; b1 done (`SEMULITH-P4-0405`): the author writes `medeleg`, `mtvec` and `stvec` by the table, a probe holds it to the engine; b2's brief measured (`0406`); b2 done (`SEMULITH-P4-0407`): the author derives the reserved trap for what the profile leaves out; c done (`SEMULITH-P4-0408`): `medeleg` narrowed to `0xb3ff`, the engine moved; d done (`SEMULITH-P4-0409`): the override selects the misaligned AMO; e's brief measured (`0410`): the hart reads once, and an atomic read needs its own boundary kind; e done (`SEMULITH-P4-0412`): `AtomicLoad` in the boundary, the engine and every environment, contract version 4 frozen (device regions, the read-once guarantee); f's brief measured (`0413`): one batch, each predecessor retired in the unit that declares its successor; f1 done (`SEMULITH-P4-0414`): the 42 declared, 40 predecessors retired and listed, two kept until f3; f2 done (`SEMULITH-P4-0415`): each captured once, no behaviour moved; f3 done (`SEMULITH-P4-0416`): the 42 credits re-issued, the report 3 of 10 open; g next. The release decision landed 2026-11-10: `rv64gc-lab-v0` version 0 accepted (`decision_release-rv64gc-lab-v0.md`), CPU-SYSTEM `passed` at `194437d6`, 10 of 10 axes, eight declared limits; the scalar unit's recorded runs measured again and held to what they cover. 19/20 leaves done | repo-local |
| [`P5-BOARD`](tasks/P5-BOARD.md) | `active` | `.13` — blocked: the netboard re-bases onto `rv64gc-lab-v0` once a version of it admits device regions, since version 0's contract forbids MMIO; then `.5`, the firmware probes (10/13 leaves done; the platform capability manifest landed, drift-gated by PLATFORM-GEN) | repo-local |
| [`AG-OS`](tasks/AG-OS.md) | `proposed` | `.1` — inspect the real eADL interfaces (gate `ARCHOGEN-OS`) | repo-local |
| [`P6-LINUX`](tasks/P6-LINUX.md) | `proposed` | `.1` — pin the system (gate `LINUX`) | repo-local |
| [`P7-COMPUTER`](tasks/P7-COMPUTER.md) | `proposed` | `.1` — declare the workload suite (gate `SYSTEM`) | repo-local |
| [`MC-MULTICORE`](tasks/MC-MULTICORE.md) | `proposed` | `.1` — extend the CPU/environment contract | repo-local |
| [`LAB-BENCH`](tasks/LAB-BENCH.md) | `active` | `.2` — proposed: stepping, register view, live traces (1 of 2 leaves done; `semulith demo` + the browser bench land) | repo-local |
| [`ARTIFACT-CLEANUP`](tasks/ARTIFACT-CLEANUP.md) | `active` | `ARTIFACT-CLEANUP.42` — the next recurring cleanup (due 24 h after 2026-11-13T20:58Z), the orphan act before its four; the feature cycle resumes meanwhile | repo-local |
| [`LIVE-CONTAINMENT`](tasks/LIVE-CONTAINMENT.md) | `active` | `.4` — active: archive sealed, full doctrine adoption remains; `.5` pending, the toolbox family at its ceiling; `.6` pending, the decisions index at its part ceiling (3 of 6 leaves done) | repo-local |
| [`XTASK`](tasks/XTASK.md) | `active` | `XTASK.13` — ruling 5's rule for the eleven fragile doctrines (frozen copies; a damaged live source fails by name), one slice each between feature units: slices a (DEF-GEN) and b1 (GUEST-GEN census/surgical) done 2026-10-29, b2 (GUEST-GEN mirror/count) 2026-11-02, b3 (GUEST-GEN parcel author) 2026-11-03, b4 (the author probes' owned corpus, and a real-run step) 2026-11-04, b5 (their other corpus reads), b6 (the rest of its self-test: GUEST-GEN whole) c (BOOK-INDEX) 2026-11-05, d (BOARD-GEN), e (PLATFORM-GEN), f (MATERIALS-BILL) 2026-11-06, g (EXERCISE-COVERAGE), h (CONTRACT-FREEZE), i (RECORD-SCHEMA) and j (UNIT-BOOKS) 2026-11-07; PROFILE-CONSISTENCY's probes: k done 2026-11-14 (`probe_experiment_graph.py` judges a frozen subset), `probe_retained_sail_identity.py` next; XTASK.15 done 2026-11-10 (`cargo xtask commit-unit` lands a unit), and XTASK.16 (a check skips only on a ledger-only commit; the chain runs the tests); `XTASK.17` pending, the ledger probe at the push boundary; XTASK.18 done 2026-11-10 (the chain accepts a colon after the number, and its refusal says what it wants). Hosted CI green on cefb0d84 (XTASK.12 done); XTASK.4 done by ruling 2; the project registry's drivers in Rust behind held shims — 42 of 42 drivers through shims, the count re-derived by `DERIVED-COUNTS` (16 of 18 leaves done) | repo-local |
<!-- ANCHOR_END: trees -->
