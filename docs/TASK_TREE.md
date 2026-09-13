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
| [`P0-PROFILE`](tasks/P0-PROFILE.md) | `active` | `.5` — reference candidate dossier (gate `G0`; 2 of 9 leaves done) | repo-local |
| [`P1-LAB`](tasks/P1-LAB.md) | `proposed` | `.1` — crate skeleton (gate `G1`, blocked on `G0`) | repo-local |
| [`P2-SCALAR`](tasks/P2-SCALAR.md) | `proposed` | `.1` — complete the declared scope (gate `CPU-LAB`) | repo-local |
| [`DSP-REVIEW`](tasks/DSP-REVIEW.md) | `proposed` | `.1` — width and accumulator semantics | repo-local |
| [`P3-BREADTH`](tasks/P3-BREADTH.md) | `proposed` | `.1` — apply the interface findings (gate `BREADTH`) | repo-local |
| [`P4-SYSTEM`](tasks/P4-SYSTEM.md) | `proposed` | `.1` — resolve the profile (gate `CPU-SYSTEM`) | repo-local |
| [`P5-BOARD`](tasks/P5-BOARD.md) | `proposed` | `.1` — platform specification (gate `BOARD`) | repo-local |
| [`AG-OS`](tasks/AG-OS.md) | `proposed` | `.1` — inspect the real eADL interfaces (gate `ARCHOGEN-OS`) | repo-local |
| [`P6-LINUX`](tasks/P6-LINUX.md) | `proposed` | `.1` — pin the system (gate `LINUX`) | repo-local |
| [`P7-COMPUTER`](tasks/P7-COMPUTER.md) | `proposed` | `.1` — declare the workload suite (gate `SYSTEM`) | repo-local |
| [`MC-MULTICORE`](tasks/MC-MULTICORE.md) | `proposed` | `.1` — extend the CPU/environment contract | repo-local |
| [`MIRROR-DRIFT`](tasks/MIRROR-DRIFT.md) | `active` | `.2` — the doctrine documents mirror the registry | repo-local |
| [`SEMULITH-PKG`](tasks/SEMULITH-PKG.md) | `done` | — (8/8 leaves complete) | repo-local |
| [`BOOTSTRAP`](tasks/BOOTSTRAP.md) | `done` | — | repo-local |

Milestone trees are `proposed` until their first leaf starts. Each names its gate, its
dependencies, and the `ROADMAP.md` section it derives from, so it can be checked against the
plan rather than trusted.
<!-- ANCHOR_END: trees -->
