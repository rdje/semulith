# MEMORY — resume pointer (layer A; overwrite-only, keep ≤ ~50 lines)

> The bounded layer-A resume pointer (see `MEMORY_ARCHITECTURE.md`). OVERWRITE the
> "Current state" block each update — never append history here.

## How to resume

1. Read `README.md`, `MEMORY_ARCHITECTURE.md`, `TOOLBOX.md`, `DOCTRINE_ENFORCEMENT.md`.
2. Open the active task-tree below → its Current Frontier → continue from the next action.
3. Durable facts: `docs/decisions/INDEX.md`. Retrievable lessons: `docs/knowledge/INDEX.md`.

## Current state

- **Project:** semulith — trustworthy CPU/DSP software models in Rust; `ROADMAP.md` v0.3 is the plan. **The definition now executes**: `semulith-core::exec` runs the generated `Sem` trees, and the four tracked guests agree with sail-riscv and spike on all 34 aligned steps (`scripts/run_semulith_smoke.py`, `2026-09-28`). **The laboratory measures itself**: `semulith bench` runs the four workload mixes in the three ARCHITECTURE §6 modes on a named host (`2026-09-28`).
- **Active trees:** `P1-LAB` (11/12 — frontier `.12`, the `G1` gate report), `LAB-BENCH` (1/2 — frontier `.2`, stepping/register-view/live traces proposed), `UPSTREAM-TRACK` (3/4), `PUSH-DISCIPLINE` (1/3), `MODEL-BOOKS` (0/6), `ARTIFACT-CLEANUP` (1/1 — recurring §8; last run `2026-09-28`).
- **Closed `2026-09-28`:** `P1-LAB.11` — the performance baseline (RUST-04): `semulith-verify::bench` generates the four mixes (every word decode-round-trip-pinned to the definition), drives them untraced / instrumented (static + dyn) / diagnostic under one counting environment, and checks RUST-02 mode agreement as data (a disagreement is exit 1). Measured on Apple M4 Pro, Darwin 27.0.0, rustc 1.95.0: untraced 47–54 ns/step, instrumented +24–40%, diagnostic +4–8% further; 1.00 alloc/step untraced (the `extract_operands` Vec — RUST-03's measured departure), noise spread 1.7–7.4% (one 113% scheduler outlier); NO threshold set — the noise table is what a future threshold cites. The static-vs-dynamic observer question resolved by measurement (×0.974–1.002, within noise; static stays the default). The `.10` checklist archives per the per-part ceiling.
- **Closed (older):** `P1-LAB.10` — replay and reduction (bundle/replay/reduce); `P1-LAB.9` — the validator mutation suite: `step_over`/`run_over` + 11 arms, all eight EVD-09 classes plus the JALR odd-bit arm (fault at 0x80000029, as predicted); `LAB-BENCH.1` — `semulith demo` + the browser bench; `.8` — the first execution slice; `.7` — graph/report checker; `.6` — DEF-GEN; `.1`–`.5` — skeleton→outcomes.
- **Direction (director, 2026-09-14):** every source of truth is **one format**, S-expression (`decision_one-format-every-source-of-truth`).
- **Direction (delegated, 2026-09-27):** the semantics **data** is the execution authority (`decision_interpreter-before-compiler`); every lane names its consuming milestone.
- **Direction (director, 2026-09-27):** everything must also run in the **browser** — JS + Wasm first-class from the first crate; now a gate (`PORT-WEB`).
- **Frontier leaf:** `P1-LAB.12` — the `G1` gate report: generated from pinned inputs, reproducible from recorded definitions/tools/inputs/event choices, reading `passed` or `incomplete`. Every other G1 criterion has landed.
- ⚠️ The `.9` suite is the detector's proof, not the model's; the `.10` bundle/reducer inherit that standing — replay fidelity and retention are tested on the suite's arms, not the space. The `.11` baseline is one named host's measurement, not a portable constant.
- **Materials:** 36 primary sources in `materials/catalog.sexp` (corpus `3c45e81`), cached in gitignored `.materials/`; `$SEMULITH_CHIPDOC_ROOT` never tracked. Run-real-code set pinned at `.materials/run-real-code/`.
- **Citations:** `check_citations.py` resolves 52 of 52, offline from the cache. The pin is docs.riscv.org, NOT github.com/riscv/riscv-isa-manual — read `docs/knowledge/a-version-string-is-not-an-identity.md` first.
- **Next action:** `P1-LAB.12` — the `G1` gate report; then P1-LAB closes.
- **Also open:** `MODEL-BOOKS.1` (book structure + the complete materials bill), `UPSTREAM-TRACK.3`, `PUSH-DISCIPLINE.2`, `LAB-BENCH.2`. ⭐ Director input to schedule (no pivot taken): chipdoc's corpus carries a semulith feed (`$SEMULITH_CHIPDOC_ROOT/SEMULITH.md` → `catalog/semulith-proposals.sexp`); a MODEL-METHOD catalogue slice consumes it when that frontier opens.
- **Feel it now:** `cargo run -p semulith-cli -- demo --guest=guest-control --mutate=jalr-odd-bit` — the trace + the detector's verdict; `semulith bundle --guest=guest-control --mutate=zext-addi > c.json && semulith replay c.json` — a recorded result re-deriving; `make bench && (cd bench && python3 -m http.server 8000)` — the browser bench; `cargo run --release -p semulith-cli -- bench` — the performance baseline on this host.
- **Read first:** `docs/decisions/INDEX.md` — the last five records define the current direction. **Latest commit:** `git log -1`. **In-flight uncommitted work:** none.
- ⛔ **Do not push.** Cadence is 300 commits — `scripts/check_push_cadence.sh --status` says where we stand; below it a push is exceptional and **only the director may approve it** (`decision_push-cadence`). `SEMULITH_PUSH_APPROVED` carries the director's reason, never an agent's judgement.
- **Blockers:** none. LinkedSpec pinned `a8d34c845` (LS-001 fix shipped; RGX `8763a0e6` unchanged); our repro re-ran 8/0. ⛔ Never patch the submodule; adopt by moving the pin. **Sanctioned standing process:** CHIPDOC's ChipdocWatcher watches the chipdoc catalog and `materials/catalog.sexp` (director ruling 2026-09-27: it stays; do not kill it, do not flag it — `doctrine/sanctioned_processes.tsv` exempts it, `ARTIFACT-CLEANUP.2`).
- **LinkedSpec readers:** `compare_readers.py` sweeps every tracked `.sexp` — Lispish (the two CLASS families as the LS-guard) and SExprDocumentV1 via `sexpr_file` (the read path).
