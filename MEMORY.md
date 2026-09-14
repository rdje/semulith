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
- **Active trees:** `MODEL-COMPOSE` (2/6), `MODEL-METHOD` (2/10), `MODEL-BOOKS` (0/6).
- **Frontier leaf:** `MODEL-COMPOSE.3` — assumption/guarantee discharge.
- **Next action:** `MODEL-COMPOSE.3`, the inter-unit operator. Its first input already exists: the
  **8 environment-assumptions** `rv64i-lab-v0` carries, written before any board did. Every
  sub-unit assumption must be matched by a named guarantee or the composition is REJECTED
  (`CPU_ENVIRONMENT` §5, made mechanical). `.1` built the intra-unit operator (union, decidable);
  `.2` gave fragments a form and a home under `definitions/`, reusable across units.
- **Also open:** `MODEL-METHOD.9` (semantics — nothing machine-executable exists), `.10` (is the
  definition sufficient for an engine — the precondition for writing model code), `MODEL-BOOKS.1`.
- **Read first:** `docs/decisions/INDEX.md` — the last five records define the current direction.
- **Latest commit:** see `git log -1` — `SEMULITH-MC-0038 (leaf MODEL-COMPOSE.1)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
