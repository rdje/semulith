# MEMORY — resume pointer (layer A; overwrite-only, keep ≤ ~50 lines)

> The bounded layer-A resume pointer (see `MEMORY_ARCHITECTURE.md`). OVERWRITE the
> "Current state" block each update — never append history here.

## How to resume

1. Read `README.md`, `MEMORY_ARCHITECTURE.md`, `TOOLBOX.md`, `DOCTRINE_ENFORCEMENT.md`.
2. Open the active task-tree below → its Current Frontier → continue from the next action.
3. Durable facts: `docs/decisions/INDEX.md`. Retrievable lessons: `docs/knowledge/INDEX.md`.

## Current state

- **Project:** semulith — trustworthy CPU/DSP software models in Rust; planning package v0.2
  is the design input, `ROADMAP.md` v0.3 is the plan. No CPU code exists yet.
- **Active trees:** `UPSTREAM-TRACK` (3/4), `PUSH-DISCIPLINE` (1/3), `SOT-FORMAT` (5/10), `MODEL-METHOD` (6/13), `MODEL-COMPOSE` (2/6), `MODEL-BOOKS` (0/6), `ARTIFACT-CLEANUP` (1/1 — recurring §8).
- **Frontier leaf:** `SOT-FORMAT.3` — the records (`requirements.jsonl` 26, `contract-obligations.jsonl` 34) to the format; round-trip proves losslessness field-by-field.
- **Schema layer:** `schema/` now declares `encoding`, `fragment`, `semantics` (+ the language itself). The semantics' 32 forms are data; `check_semantics.py` loads them. Adding a construct/operator = a schema edit; a new declaration KIND changes the kernel (`operator` is the fourth kind).
- **Direction (director, 2026-09-14):** every source of truth is **one format**, S-expression, composable and extensible to new constructs in the same format — composition is a merge, and three formats are three merge semantics (`decision_one-format-every-source-of-truth`).
- **Direction (delegated, 2026-09-27):** `ROADMAP.md` **v0.3** adopted ("sota, signoff and
  production-grade") — P1's start condition is `SOT-FORMAT.2` + `MODEL-METHOD.10`; the semantics
  **data** is the execution authority (`decision_interpreter-before-compiler`); every lane names
  its consuming milestone (`decision_lane-consumption`). After `.2`: `P1-LAB.1` (crate skeleton).
- **Materials:** 36 primary sources in `materials/catalog.sexp` (corpus pinned `3c45e81`). Cached
  in gitignored `.materials/` by `scripts/materials.py --fetch`; the corpus location comes from
  `$SEMULITH_CHIPDOC_ROOT`, never from a tracked file.
- **Citations:** `check_citations.py` resolves 52 of 52, offline from the cache. The pin is
  docs.riscv.org, NOT github.com/riscv/riscv-isa-manual — different chapter numbering; read
  `docs/knowledge/a-version-string-is-not-an-identity.md` first.
- **Next action:** `SOT-FORMAT.3` — records to the format. P1's v0.3 start condition is now
  half-met (`.2` done; `MODEL-METHOD.10` still open — the extraction contract). ⛔ Records move
  only behind the schema layer, never before.
- ⚠️ `52 of 52` semantics means well-formed, complete and **cited** — not **correct**. Proving
  correctness is a differential experiment against a reference model.
- **Also open:** `MODEL-METHOD.10` (is the definition sufficient for an engine), `MODEL-COMPOSE.3`
  (assumption/guarantee discharge — needs `SOT-FORMAT.5`'s record merge), `MODEL-BOOKS.1`.
- **Read first:** `docs/decisions/INDEX.md` — the last five records define the current direction.
- **Latest commit:** see `git log -1`. **In-flight uncommitted work:** none.
- ⛔ **Do not push.** Cadence is 300 commits — `scripts/check_push_cadence.sh --status` says where
  we stand. Below cadence a push is exceptional and **only the director may approve it** —
  `decision_push-cadence`. The pre-push hook refuses; `SEMULITH_PUSH_APPROVED` carries the
  director's reason and is never set on an agent's own judgement.
- **Blockers:** none — `SOT-FORMAT.9` unblocked `2026-09-26`: upstream shipped the LS-001 fix,
  the pin moved to `a8d34c845`, our repro re-ran 8/0. ⛔ Never patch the submodule; adopt by
  moving the pin.
- **LinkedSpec:** pinned `a8d34c845` (LS-001 fix `8259719f8` shipped; RGX `8763a0e6` unchanged).
  `compare_readers.py` sweeps every tracked `.sexp`: Lispish (carries the two CLASS families as
  the LS-guard) and SExprDocumentV1 via `sexpr_file` (the engine's read path).
