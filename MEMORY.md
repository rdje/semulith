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
- **Frontier leaf:** `SEMULITH-TREES.2` — the CPU lane (`P2-SCALAR`, `DSP-REVIEW`, `P3-BREADTH`, `P4-SYSTEM`).
- **Next action:** create `P2-SCALAR`, `DSP-REVIEW`, `P3-BREADTH`, `P4-SYSTEM` (`.2`), then the
  system lane (`.3`), then re-review `docs/tasks/` bounds and the book (`.4`). After that,
  execute `P0-PROFILE.1` — the `rv64i-lab-v0` dossier.
- **Latest commit:** see `git log -1` — `SEMULITH-TREES-0009 (leaf SEMULITH-TREES.1)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
