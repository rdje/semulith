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
- **Active tree:** none. `SEMULITH-PKG` and `SEMULITH-TREES` are both `done`.
- **Next tree:** `P0-PROFILE` — frontier leaf `.1`, the `rv64i-lab-v0` profile dossier.
- **Next action:** execute `P0-PROFILE.1` — pin the RV64I specification revision by exact
  locator and write the `rv64i-lab-v0` dossier: instruction scope, entry state, memory
  boundaries, access/misalignment policy, fetch rules, environment-trap reporting; every field
  source-linked or a recorded open question with an owner.
- **Latest commit:** see `git log -1` — `SEMULITH-TREES-0012 (leaf SEMULITH-TREES.4)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
