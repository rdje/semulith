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
- **Active trees:** `UPSTREAM-TRACK` (3/4), `PUSH-DISCIPLINE` (1/3), `SOT-FORMAT` (7/10), `MODEL-METHOD` (6/13), `MODEL-COMPOSE` (2/6), `MODEL-BOOKS` (0/6), `ARTIFACT-CLEANUP` (1/1 — recurring §8).
- **Frontier leaf:** `SOT-FORMAT.5` — record merge across a composition boundary (the thing the split made impossible). `.4` is done: the whole dossier moved — `profile.sexp`, `state.sexp`, `sources.sexp`, `references.sexp`, the matched override and the four guest expectations — round-trip field-for-field with the comment census exact, `PROFILE-CONSISTENCY`'s 39 arms re-fired, the kernel carries one reserved `(comment …)` head, and the Sail JSON derives from the tracked `.sexp` byte-identically. `schema/` declares twelve families; ceiling re-derived to 24 with grounds in the registry.
- **Direction (director, 2026-09-14):** every source of truth is **one format**, S-expression, composable and extensible to new constructs in the same format — composition is a merge, and three formats are three merge semantics (`decision_one-format-every-source-of-truth`).
- **Direction (delegated, 2026-09-27):** `ROADMAP.md` **v0.3** adopted — P1's start condition is `SOT-FORMAT.2` (now done) + `MODEL-METHOD.10`; the semantics **data** is the execution authority (`decision_interpreter-before-compiler`); every lane names its consuming milestone (`decision_lane-consumption`).
- **Direction (director, 2026-09-27):** everything must also run in the **browser** — JS + Wasm is a first-class target from the first crate (`decision_browser-wasm-target`); lane `PORT-WEB` (proposed, consumed by `P1-LAB`) owns it, leaf `.1` activates with `P1-LAB.1`.
- **Materials:** 36 primary sources in `materials/catalog.sexp` (corpus pinned `3c45e81`). Cached
  in gitignored `.materials/` by `scripts/materials.py --fetch`; the corpus location comes from
  `$SEMULITH_CHIPDOC_ROOT`, never from a tracked file.
- **Citations:** `check_citations.py` resolves 52 of 52, offline from the cache. The pin is
  docs.riscv.org, NOT github.com/riscv/riscv-isa-manual — read `docs/knowledge/a-version-string-is-not-an-identity.md` first.
- **Next action:** `SOT-FORMAT.5` — define and check the union of two units' records across a
  composition boundary, feeding `MODEL-COMPOSE.3`'s assumption/guarantee discharge; the
  `SOURCE-FORMAT` gate (`.6`) follows. P1's start condition stays half-met (`MODEL-METHOD.10`
  open). ⛔ Everything moves only behind the schema layer, never before.
- ⚠️ `52 of 52` semantics means well-formed, complete and **cited** — not **correct**. Proving
  correctness is a differential experiment against a reference model.
- **Also open:** `MODEL-METHOD.10` (is the definition sufficient for an engine), `MODEL-COMPOSE.3`
  (assumption/guarantee discharge — needs `SOT-FORMAT.5`'s record merge), `MODEL-BOOKS.1`.
  `DOC-SHARDING` closed 2026-09-27 (shard tool + `SHARD-FREEZE`; headroom restored).
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
