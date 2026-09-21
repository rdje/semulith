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
- **Active trees:** `UPSTREAM-TRACK` (1/3), `PUSH-DISCIPLINE` (1/3), `SOT-FORMAT` (1/9), `MODEL-METHOD` (6/13), `MODEL-COMPOSE` (2/6), `MODEL-BOOKS` (0/6).
- **Frontier leaf:** `SOT-FORMAT.8` — the book describes no part of the canonical definition.
- **Direction (director, 2026-09-14):** every source of truth is **one format**, S-expression,
  **composable and extensible to new constructs in the same format**. This **supersedes** the
  per-file format split in `decision_canonical-definition-input` — composition is a merge, and
  three formats are three merge semantics.
- **Materials:** 36 primary sources in `materials/catalog.sexp` (corpus pinned `3c45e81`). Cached
  in gitignored `.materials/` by `scripts/materials.py --fetch`; the corpus location comes from
  `$SEMULITH_CHIPDOC_ROOT`, never from a tracked file.
- **Citations:** `check_citations.py` resolves 52 of 52, offline from the cache. The pin is
  docs.riscv.org, NOT github.com/riscv/riscv-isa-manual — different chapter numbering; read
  `docs/knowledge/a-version-string-is-not-an-identity.md` before touching it.
- **Next action:** `SOT-FORMAT.8` (the book's canonical-definition chapter describes no part of the canonical
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
- ⛔ **Do not push.** Cadence is 300 commits — `scripts/check_push_cadence.sh --status` says where
  we stand, because a count typed here is wrong the next commit. Below cadence a push is exceptional
  and **only the director may approve it** — `decision_push-cadence`. The `pre-push` hook
  refuses; `SEMULITH_PUSH_APPROVED` carries the director's reason and is never set on an
  agent's own judgement.
- **Blockers:** `SOT-FORMAT.9` only — upstream defect `LS-001` in `docs/upstream/` (a multi-line
  quoted string is not one string to Lispish). ⛔ Do NOT patch the submodule; a validated one-line
  fix is reported and is theirs to apply.
- **LinkedSpec:** `vendor/linkedspec` pinned `ad290bdb4`; build needs the documented PGEN
  bootstrap; `.app-data/` holds cargo home + target. `compare_readers.py`: 4 of 5 files agree.
