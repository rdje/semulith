# MEMORY — resume pointer (layer A; overwrite-only, keep ≤ ~50 lines)

> The bounded layer-A resume pointer (see `MEMORY_ARCHITECTURE.md`). OVERWRITE the
> "Current state" block each update — never append history here.

## How to resume

1. Read `README.md`, `MEMORY_ARCHITECTURE.md`, `TOOLBOX.md`, `DOCTRINE_ENFORCEMENT.md`.
2. Open the active task-tree below → its Current Frontier → continue from the next action.
3. Durable facts: `docs/decisions/INDEX.md`. Retrievable lessons: `docs/knowledge/INDEX.md`.

## Current state

- **Project:** semulith — trustworthy CPU/DSP software models in Rust; `ROADMAP.md` v0.3 is the plan. CPU work is at the laboratory crate skeleton; no instruction code exists yet.
- **Active trees:** `P1-LAB` (1/12), `UPSTREAM-TRACK` (3/4), `PUSH-DISCIPLINE` (1/3), `MODEL-BOOKS` (0/6), `ARTIFACT-CLEANUP` (1/1 — recurring §8).
- **Closed `2026-09-27`:** `PORT-WEB` (1/1 — the skeleton builds for wasm32 from its first slice, doctrine `PORT-WEB` fired RED); `MODEL-METHOD` (13/13), `MODEL-COMPOSE` (6/6), `SOT-FORMAT` (10/10), `DOC-SHARDING` (1/1).
- **Frontier leaf:** `P1-LAB.2` — target arithmetic primitives, in `semulith-core`.
- **Just landed:** `P1-LAB.1` — `semulith-core`/`semulith-verify`/`semulith-cli` replace the
  placeholder crate, wired per `docs/ARCHITECTURE.md` §4 (core depends on nothing; verify owns
  the fixtures home; cli calls both), `make check` green at `-D warnings`, and the workspace
  builds for `wasm32-unknown-unknown` on every commit (`scripts/check_wasm_build.sh`, 20th doctrine).
- **Direction (director, 2026-09-14):** every source of truth is **one format**, S-expression, composable and extensible in the same format (`decision_one-format-every-source-of-truth`).
- **Direction (delegated, 2026-09-27):** the semantics **data** is the execution authority (`decision_interpreter-before-compiler`); every lane names its consuming milestone.
- **Direction (director, 2026-09-27):** everything must also run in the **browser** — JS + Wasm first-class from the first crate; now a gate, not a hope (`PORT-WEB`).
- **Materials:** 36 primary sources in `materials/catalog.sexp` (corpus `3c45e81`), cached in gitignored `.materials/` by `scripts/materials.py --fetch`; the corpus root comes from `$SEMULITH_CHIPDOC_ROOT`, never a tracked file. Run-real-code set pinned at `.materials/run-real-code/` (psABI, ELF gABI, syscall header, compiler-rt inventory).
- **Citations:** `check_citations.py` resolves 52 of 52, offline from the cache. The pin is docs.riscv.org, NOT github.com/riscv/riscv-isa-manual — read `docs/knowledge/a-version-string-is-not-an-identity.md` first.
- **Next action:** `P1-LAB.2` — source-linked widths and operations: explicit intermediate precision, truncation, sign/zero extension, shift corner cases (`SEM-03`), in `semulith-core`. ⛔ Everything moves only behind the schema layer, never before.
- ⚠️ `52 of 52` semantics means well-formed, complete and **cited** — not **correct**; correctness is a differential experiment against a reference model.
- **Also open:** `MODEL-BOOKS.1` (book structure + the complete materials bill), `UPSTREAM-TRACK.3`, `PUSH-DISCIPLINE.2`. ⭐ Director input to schedule (no pivot taken): chipdoc's corpus carries a semulith feed (`$SEMULITH_CHIPDOC_ROOT/SEMULITH.md` → `catalog/semulith-proposals.sexp`: psABI, SBI, BRS, U-Boot, DT, FU540, virtio, ACT); a MODEL-METHOD catalogue slice consumes it when that frontier opens.
- **Read first:** `docs/decisions/INDEX.md` — the last five records define the current direction. **Latest commit:** `git log -1`. **In-flight uncommitted work:** none.
- ⛔ **Do not push.** Cadence is 300 commits — `scripts/check_push_cadence.sh --status` says where we stand; below it a push is exceptional and **only the director may approve it** (`decision_push-cadence`). `SEMULITH_PUSH_APPROVED` carries the director's reason, never an agent's judgement.
- **Blockers:** none. LinkedSpec pinned `a8d34c845` (LS-001 fix shipped; RGX `8763a0e6` unchanged); our repro re-ran 8/0. ⛔ Never patch the submodule; adopt by moving the pin. **Sanctioned standing process:** CHIPDOC's ChipdocWatcher watches the chipdoc catalog and `materials/catalog.sexp` (director ruling 2026-09-27: it stays; do not kill it, do not flag it — `doctrine/sanctioned_processes.tsv` exempts it, `ARTIFACT-CLEANUP.2`).
- **LinkedSpec readers:** `compare_readers.py` sweeps every tracked `.sexp` — Lispish (the two CLASS families as the LS-guard) and SExprDocumentV1 via `sexpr_file` (the read path).
