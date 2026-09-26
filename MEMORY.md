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
- **Active trees:** `UPSTREAM-TRACK` (2/3), `PUSH-DISCIPLINE` (1/3), `SOT-FORMAT` (4/9), `MODEL-METHOD` (6/13), `MODEL-COMPOSE` (2/6), `MODEL-BOOKS` (0/6), `ARTIFACT-CLEANUP` (1/1 — recurring §8 housekeeping).
- **Frontier leaf:** `SOT-FORMAT.2` — the constructs already in use, declared as data.
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
- **Next action:** `SOT-FORMAT.2` (the constructs already in `.sexp` — encoding, fragment,
  semantics — declared as data in `schema/`; `check_semantics.py`'s 32 forms move out of Python;
  the `52 of 52` verdict must reproduce byte-identically). ⚠️ One kernel question `.2` must answer
  first: integer-headed data tuples like `(pieces (12 12))` need a declared shape the four atom
  types don't cover — expect one small kernel extension, owned and armed in `.2` itself.
  ⛔ Then `.3`/`.4` (records and configuration move) — only behind the schema layer, never before.
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
- **Blockers:** none — `SOT-FORMAT.9` unblocked `2026-09-26`: upstream shipped the LS-001 fix, the
  pin moved to `a8d34c845`, our repro re-ran 8/0. ⛔ Never patch the submodule; adopt by moving the pin.
- **LinkedSpec:** pinned `a8d34c845` (ships LS-001 fix `8259719f8`; RGX `8763a0e6` unchanged).
  Build: documented RGX bootstrap; `.app-data/` holds cargo home + target. `compare_readers.py`:
  5 of 5 files agree; residue = two CLASS families (quoted-numeric = LS-002, escape-retention).
