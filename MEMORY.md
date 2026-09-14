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
- **Active trees:** `MODEL-METHOD` (3/10), `MODEL-COMPOSE` (2/6), `MODEL-BOOKS` (0/6).
- **Frontier leaf:** `MODEL-METHOD.10` — the extraction contract.
- **Next action:** `MODEL-METHOD.10`. Both halves of the canonical definition now exist — encodings
  (`.8`, owned and tracked) and semantics (`.9`, 52 of 52, every rule cited) — so *"the engine can
  extract all it needs"* can become a **verdict**: every declared instruction has an encoding AND
  semantics AND a requirement; every state element a reset; every obligation its checks. That
  verdict is the precondition for writing any model code (`.6` mechanizes it).
- ⚠️ `52 of 52` means the semantics are well-formed, complete and **cited** — not **correct**.
  Proving correctness is a differential experiment against a reference model.
- **Also open:** `MODEL-METHOD.9` (semantics — nothing machine-executable exists), `.10` (is the
  definition sufficient for an engine — the precondition for writing model code), `MODEL-BOOKS.1`.
- **Read first:** `docs/decisions/INDEX.md` — the last five records define the current direction.
- **Latest commit:** see `git log -1` — `SEMULITH-MM-0040 (leaf MODEL-METHOD.9)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
