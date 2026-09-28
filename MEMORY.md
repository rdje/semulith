# MEMORY — resume pointer (layer A; overwrite-only, keep ≤ ~50 lines)

> The bounded layer-A resume pointer (see `MEMORY_ARCHITECTURE.md`). OVERWRITE the
> "Current state" block each update — never append history here.

## How to resume

1. Read `README.md`, `MEMORY_ARCHITECTURE.md`, `TOOLBOX.md`, `DOCTRINE_ENFORCEMENT.md`.
2. Open the active task-tree below → its Current Frontier → continue from the next action.
3. Durable facts: `docs/decisions/INDEX.md`. Retrievable lessons: `docs/knowledge/INDEX.md`.

## Current state

- **Project:** semulith — trustworthy CPU/DSP software models in Rust; `ROADMAP.md` v0.3 is the plan. **The definition now executes**: `semulith-core::exec` runs the generated `Sem` trees, and the four tracked guests agree with sail-riscv and spike on all 34 aligned steps (`scripts/run_semulith_smoke.py`, `2026-09-28`).
- **Active trees:** `P1-LAB` (10/12 — frontier `.11`), `LAB-BENCH` (1/2 — frontier `.2`, stepping/register-view/live traces proposed), `UPSTREAM-TRACK` (3/4), `PUSH-DISCIPLINE` (1/3), `MODEL-BOOKS` (0/6), `ARTIFACT-CLEANUP` (1/1 — recurring §8; last run `2026-09-28`).
- **Closed `2026-09-28`:** `P1-LAB.10` — replay and reduction (G-REPLAY + EVD-02): `semulith-verify::replay` records the input bundle (MANIFEST pins + harness + model, platform, entry, image+sha256, the recorded event choice `DeclaredNone`/OB-ENV-EVENT-DELIVERY, budget, recorded steps+stop) and `replay()` re-derives it — identity checked by name, drift named at the first differing observation; `semulith-verify::reduce` is the ddmin minimizer whose retention is the original first divergence exactly (same step, same field), every accepted removal preserving it structurally, each result 1-minimality-witnessed; phantom-load refused `NoDivergence` (the census class is not reducible on observations). `semulith bundle`/`replay`/`reduce` land in the CLI; the `.9` checklist archives per the per-part ceiling.
- **Closed (older):** `P1-LAB.9` — the validator mutation suite: `step_over`/`run_over` + 11 arms, all eight EVD-09 classes plus the JALR odd-bit arm (fault at 0x80000029, as predicted); `LAB-BENCH.1` — `semulith demo` + the browser bench; `.8` — the first execution slice; `.7` — graph/report checker; `.6` — DEF-GEN; `.1`–`.5` — skeleton→outcomes.
- **Direction (director, 2026-09-14):** every source of truth is **one format**, S-expression (`decision_one-format-every-source-of-truth`).
- **Direction (delegated, 2026-09-27):** the semantics **data** is the execution authority (`decision_interpreter-before-compiler`); every lane names its consuming milestone.
- **Direction (director, 2026-09-27):** everything must also run in the **browser** — JS + Wasm first-class from the first crate; now a gate (`PORT-WEB`).
- **Frontier leaf:** `P1-LAB.11` — the performance baseline: arithmetic/control/memory/fault mixes on a **named host**, allocation counts, noise characterized **before** any threshold (`RUST-04`); no invented MIPS target; traced and untraced executions must agree on observations (`RUST-02`).
- ⚠️ The `.9` suite is the detector's proof, not the model's; the `.10` bundle/reducer inherit that standing — replay fidelity and retention are tested on the suite's arms, not the space.
- **Materials:** 36 primary sources in `materials/catalog.sexp` (corpus `3c45e81`), cached in gitignored `.materials/`; `$SEMULITH_CHIPDOC_ROOT` never tracked. Run-real-code set pinned at `.materials/run-real-code/`.
- **Citations:** `check_citations.py` resolves 52 of 52, offline from the cache. The pin is docs.riscv.org, NOT github.com/riscv/riscv-isa-manual — read `docs/knowledge/a-version-string-is-not-an-identity.md` first.
- **Next action:** `P1-LAB.11` — the performance baseline; named host, allocation counts, noise first.
- **Also open:** `MODEL-BOOKS.1` (book structure + the complete materials bill), `UPSTREAM-TRACK.3`, `PUSH-DISCIPLINE.2`, `LAB-BENCH.2`. ⭐ Director input to schedule (no pivot taken): chipdoc's corpus carries a semulith feed (`$SEMULITH_CHIPDOC_ROOT/SEMULITH.md` → `catalog/semulith-proposals.sexp`); a MODEL-METHOD catalogue slice consumes it when that frontier opens.
- **Feel it now:** `cargo run -p semulith-cli -- demo --guest=guest-control --mutate=jalr-odd-bit` — the trace + the detector's verdict; `semulith bundle --guest=guest-control --mutate=zext-addi > c.json && semulith replay c.json` — a recorded result re-deriving; `make bench && (cd bench && python3 -m http.server 8000)` — the browser bench.
- **Read first:** `docs/decisions/INDEX.md` — the last five records define the current direction. **Latest commit:** `git log -1`. **In-flight uncommitted work:** none.
- ⛔ **Do not push.** Cadence is 300 commits — `scripts/check_push_cadence.sh --status` says where we stand; below it a push is exceptional and **only the director may approve it** (`decision_push-cadence`). `SEMULITH_PUSH_APPROVED` carries the director's reason, never an agent's judgement.
- **Blockers:** none. LinkedSpec pinned `a8d34c845` (LS-001 fix shipped; RGX `8763a0e6` unchanged); our repro re-ran 8/0. ⛔ Never patch the submodule; adopt by moving the pin. **Sanctioned standing process:** CHIPDOC's ChipdocWatcher watches the chipdoc catalog and `materials/catalog.sexp` (director ruling 2026-09-27: it stays; do not kill it, do not flag it — `doctrine/sanctioned_processes.tsv` exempts it, `ARTIFACT-CLEANUP.2`).
- **LinkedSpec readers:** `compare_readers.py` sweeps every tracked `.sexp` — Lispish (the two CLASS families as the LS-guard) and SExprDocumentV1 via `sexpr_file` (the read path).
