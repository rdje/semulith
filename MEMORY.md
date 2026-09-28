# MEMORY — resume pointer (layer A; overwrite-only, keep ≤ ~50 lines)

> The bounded layer-A resume pointer (see `MEMORY_ARCHITECTURE.md`). OVERWRITE the
> "Current state" block each update — never append history here.

## How to resume

1. Read `README.md`, `MEMORY_ARCHITECTURE.md`, `TOOLBOX.md`, `DOCTRINE_ENFORCEMENT.md`.
2. Open the active task-tree below → its Current Frontier → continue from the next action.
3. Durable facts: `docs/decisions/INDEX.md`. Retrievable lessons: `docs/knowledge/INDEX.md`.

## Current state

- **Project:** semulith — trustworthy CPU/DSP software models in Rust; `ROADMAP.md` v0.3 is the plan. **The definition now executes**: `semulith-core::exec` runs the generated `Sem` trees, and the four tracked guests agree with sail-riscv and spike on all 34 aligned steps (`scripts/run_semulith_smoke.py`, `2026-09-28`).
- **Active trees:** `P1-LAB` (9/12 — frontier `.10`), `UPSTREAM-TRACK` (3/4), `PUSH-DISCIPLINE` (1/3), `MODEL-BOOKS` (0/6), `ARTIFACT-CLEANUP` (1/1 — recurring §8; last run `2026-09-28`).
- **Closed `2026-09-28`:** `P1-LAB.9` — the validator mutation suite: `exec::step_over`/`run::run_over` parameterize the single execution path over the instruction table; `semulith-verify::mutate` runs 11 arms — all eight EVD-09 wrong-behaviour classes detected (wrong sign extension, suppressed write, wrong trap cause, illegal-opcode substitution for a limitation, extra access via the crossing census, shifted delivery, overbroad mask, stale reference config) plus the JALR odd-bit arm the fixture note names (fault at 0x80000029, as predicted), the four-guest census pin, and the comparison-suppression exhibit. `.1`–`.8` checklists archived to `docs/tasks/archive/P1-LAB.md` (per-part ceiling obeyed, not raised).
- **Closed (older):** `P1-LAB.8` — the first execution slice: `semulith-core::exec`, the observation runner + first-divergence comparator + ELF loader (`semulith-verify::{run,elf}`), the generated guest fixture + 23rd doctrine `GUEST-GEN`, `semulith run`; `.7` — the graph and report checker; `.6` — the generated canonical definition (DEF-GEN); `.1`–`.5` — skeleton→outcomes.
- **Direction (director, 2026-09-14):** every source of truth is **one format**, S-expression (`decision_one-format-every-source-of-truth`).
- **Direction (delegated, 2026-09-27):** the semantics **data** is the execution authority (`decision_interpreter-before-compiler`); every lane names its consuming milestone.
- **Direction (director, 2026-09-27):** everything must also run in the **browser** — JS + Wasm first-class from the first crate; now a gate (`PORT-WEB`).
- **Frontier leaf:** `P1-LAB.10` — replay and reduction (T008): an input bundle that replays the same result, and a minimizer whose output retains the original divergence — a seed is accompanied by algorithm/version and the actual relevant event choices.
- ⚠️ The `.9` suite is the detector's proof, not the model's: the differential now demonstrably catches all eight designated wrong-behaviour classes, but coverage is the suite's arms, not the space — new semantics land with new arms beside them.
- **Materials:** 36 primary sources in `materials/catalog.sexp` (corpus `3c45e81`), cached in gitignored `.materials/`; `$SEMULITH_CHIPDOC_ROOT` never tracked. Run-real-code set pinned at `.materials/run-real-code/`.
- **Citations:** `check_citations.py` resolves 52 of 52, offline from the cache. The pin is docs.riscv.org, NOT github.com/riscv/riscv-isa-manual — read `docs/knowledge/a-version-string-is-not-an-identity.md` first.
- **Next action:** `P1-LAB.10` — replay and reduction; the `.9` suite produces the divergences a reducer must retain while minimizing.
- **Also open:** `MODEL-BOOKS.1` (book structure + the complete materials bill), `UPSTREAM-TRACK.3`, `PUSH-DISCIPLINE.2`. ⭐ Director input to schedule (no pivot taken): chipdoc's corpus carries a semulith feed (`$SEMULITH_CHIPDOC_ROOT/SEMULITH.md` → `catalog/semulith-proposals.sexp`); a MODEL-METHOD catalogue slice consumes it when that frontier opens. ⭐ Director-adjacent ask (user, 2026-09-28): make the tool *feelable* early — CLI demo polish + a browser bench page; lands as its own tree after the current leaf (`LAB-BENCH`).
- **Read first:** `docs/decisions/INDEX.md` — the last five records define the current direction. **Latest commit:** `git log -1`. **In-flight uncommitted work:** none.
- ⛔ **Do not push.** Cadence is 300 commits — `scripts/check_push_cadence.sh --status` says where we stand; below it a push is exceptional and **only the director may approve it** (`decision_push-cadence`). `SEMULITH_PUSH_APPROVED` carries the director's reason, never an agent's judgement.
- **Blockers:** none. LinkedSpec pinned `a8d34c845` (LS-001 fix shipped; RGX `8763a0e6` unchanged); our repro re-ran 8/0. ⛔ Never patch the submodule; adopt by moving the pin. **Sanctioned standing process:** CHIPDOC's ChipdocWatcher watches the chipdoc catalog and `materials/catalog.sexp` (director ruling 2026-09-27: it stays; do not kill it, do not flag it — `doctrine/sanctioned_processes.tsv` exempts it, `ARTIFACT-CLEANUP.2`).
- **LinkedSpec readers:** `compare_readers.py` sweeps every tracked `.sexp` — Lispish (the two CLASS families as the LS-guard) and SExprDocumentV1 via `sexpr_file` (the read path).
