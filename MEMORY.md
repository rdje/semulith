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
- **Active tree:** none. `SEMULITH-PKG` is `done` (7/7 leaves).
- **Next tree:** `SEMULITH-TREES` — convert `ROADMAP.md` into task-trees.
- **Next action:** open `SEMULITH-TREES` — convert `ROADMAP.md` P0–P7, the DSP lane, the
  multicore lane and the archogen lane into task-trees registered in `docs/TASK_TREE.md`, then
  start P0 (`rv64i-lab-v0` profile dossier, and a reference smoke test that actually runs).
- **Latest commit:** see `git log -1` — `SEMULITH-PKG-0008 (leaf SEMULITH-PKG.7)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
