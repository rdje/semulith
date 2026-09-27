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
- **Active trees:** `UPSTREAM-TRACK` (3/4), `PUSH-DISCIPLINE` (1/3), `MODEL-BOOKS` (0/6), `ARTIFACT-CLEANUP` (1/1 — recurring §8).
- **Closed `2026-09-27`:** `SOT-FORMAT` (10/10) and `DOC-SHARDING` earlier; `MODEL-COMPOSE`'s slots leaf joined them the same day — slots are data (zero kernel lines), the unit's composed encoding space is decided and gated as the 15th doctrine (`UNIT-COMPOSITION`), and partial is declared, never inferred. `MODEL-COMPOSE` joined them (6/6 — composition is a verdict, a discharge, and a materializable unit). `MODEL-METHOD` (13/13 — the method, the census, the acquisitions, the coding gate) joined them.
- **Frontier leaf:** `P1-LAB.1` — the crate skeleton (gate G1). `MODEL-METHOD` **closed 13/13**: the method in prose (`docs/METHOD.md`), the census, the acquisitions, and `SCOPE-COVERAGE` — the 19th doctrine — whose verdict reads `1 unit(s) may code`. Every P1 precondition is a gate now: format, sufficiency, coverage.
- **Direction (director, 2026-09-14):** every source of truth is **one format**, S-expression, composable and extensible to new constructs in the same format — composition is a merge, and three formats are three merge semantics (`decision_one-format-every-source-of-truth`).
- **Direction (delegated, 2026-09-27):** `ROADMAP.md` **v0.3** adopted — P1's start condition is `SOT-FORMAT.2` (now done) + `MODEL-METHOD.10`; the semantics **data** is the execution authority (`decision_interpreter-before-compiler`); every lane names its consuming milestone (`decision_lane-consumption`).
- **Direction (director, 2026-09-27):** everything must also run in the **browser** — JS + Wasm is a first-class target from the first crate (`decision_browser-wasm-target`); lane `PORT-WEB` (proposed, consumed by `P1-LAB`) owns it, leaf `.1` activates with `P1-LAB.1`.
- **Materials:** 36 primary sources in `materials/catalog.sexp` (corpus pinned `3c45e81`). Cached
  in gitignored `.materials/` by `scripts/materials.py --fetch`; the corpus location comes from
  `$SEMULITH_CHIPDOC_ROOT`, never from a tracked file.
- **Citations:** `check_citations.py` resolves 52 of 52, offline from the cache. The pin is
  docs.riscv.org, NOT github.com/riscv/riscv-isa-manual — read `docs/knowledge/a-version-string-is-not-an-identity.md` first.
- **Next action:** `P1-LAB.1` — the processor laboratory's crate skeleton: the first Rust crate shaped for the browser target too (`PORT-WEB.1` activates with it), consuming the canonical definition through the checked extraction path. ⛔ Everything moves only behind the schema layer, never before.
- ⚠️ `52 of 52` semantics means well-formed, complete and **cited** — not **correct**. Proving
  correctness is a differential experiment against a reference model.
- **Also open:** `MODEL-BOOKS.1` (the book structure and the complete materials bill). `MODEL-COMPOSE`'s discharge operator landed; its frontier is slots.
  (assumption/guarantee discharge — its merge input, `scripts/merge_records.py`, exists),
  `MODEL-BOOKS.1`.
  ⭐ Director input to schedule (no pivot taken): chipdoc's corpus carries a semulith feed
  (`$SEMULITH_CHIPDOC_ROOT/SEMULITH.md` → `catalog/semulith-proposals.sexp`: psABI, SBI, BRS,
  U-Boot, DT, FU540, virtio, ACT + a standing offer to fetch more); a MODEL-METHOD catalogue
  slice consumes it when that frontier opens.
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
