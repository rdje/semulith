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
- **Active trees:** `SOT-FORMAT` (1/9), `MODEL-METHOD` (3/10), `MODEL-COMPOSE` (2/6), `MODEL-BOOKS` (0/6).
- **Frontier leaf:** `SOT-FORMAT.8` — the book describes no part of the canonical definition.
- **Direction (director, 2026-09-14):** every source of truth is **one format**, S-expression,
  **composable and extensible to new constructs in the same format**. This **supersedes** the
  per-file format split in `decision_canonical-definition-input` — composition is a merge, and
  three formats are three merge semantics.
- **Next action:** ⚠️ **shard `CHANGELOG.md` first** — 64,210 B against a 65,536 B ceiling, so the
  next ordinary entry blocks a commit mid-work (procedure: `docs/changelog/`, already registered).
  Then `SOT-FORMAT.8` (the book's canonical-definition chapter describes no part of the canonical
  definition — measured drift), then `.1`, the schema language written in itself.
  ⛔ Order matters: the schema language lands **before** any record is converted, or the migration
  spends a window with `RECORD-SCHEMA`'s 15 fired arms replaced by "it parses".
- ⚠️ `52 of 52` semantics means well-formed, complete and **cited** — not **correct**. Proving
  correctness is a differential experiment against a reference model.
- **Also open:** `MODEL-METHOD.10` (is the definition sufficient for an engine), `MODEL-COMPOSE.3`
  (assumption/guarantee discharge — needs `SOT-FORMAT.5`'s record merge), `MODEL-BOOKS.1`.
- **Read first:** `docs/decisions/INDEX.md` — the last five records define the current direction.
- **Latest commit:** see `git log -1`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
