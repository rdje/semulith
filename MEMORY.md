# MEMORY — resume pointer (layer A; overwrite-only, keep ≤ ~50 lines)

> The bounded layer-A resume pointer (see `MEMORY_ARCHITECTURE.md`). OVERWRITE the
> "Current state" block each update — never append history here.

## How to resume

1. Read `README.md`, `MEMORY_ARCHITECTURE.md`, `TOOLBOX.md`, `DOCTRINE_ENFORCEMENT.md`.
2. Open the active task-tree below → its Current Frontier → continue from the next action.
3. Durable facts: `docs/decisions/INDEX.md`. Retrievable lessons: `docs/knowledge/INDEX.md`.

## Current state

- **Project:** semulith — trustworthy CPU/DSP software models in Rust; planning package v0.2
  is the design input, `ROADMAP.md` is the plan. No CPU code exists yet.
- **Active tree:** `SEMULITH-TREES` — represent the whole roadmap as task-trees.
- **Frontier leaf:** `SEMULITH-TREES.4` — re-review `docs/tasks/` bounds; sync the book.
- **Next action:** all 11 lanes are trees. Re-review `docs/tasks/` health/ceiling against the
  final corpus (it is over its health target, written when three trees existed), add the book's
  task-tree map, then execute `P0-PROFILE.1` — the `rv64i-lab-v0` dossier.
- **Latest commit:** see `git log -1` — `SEMULITH-TREES-0011 (leaf SEMULITH-TREES.3)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
