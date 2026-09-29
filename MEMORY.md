# MEMORY — resume pointer (layer A; overwrite-only, keep ≤ ~50 lines)

> The bounded layer-A resume pointer (see `MEMORY_ARCHITECTURE.md`). OVERWRITE the
> "Current state" block each update — never append history here.

## How to resume

1. Read `README.md`, `MEMORY_ARCHITECTURE.md`, `TOOLBOX.md`, `DOCTRINE_ENFORCEMENT.md`.
2. Open the active task-tree below → its Current Frontier → continue from the next action.
3. Durable facts: `docs/decisions/INDEX.md`. Retrievable lessons: `docs/knowledge/INDEX.md`.

## Current state

- **Project:** semulith — trustworthy CPU/DSP software models in Rust; `ROADMAP.md` v0.3 is the plan. **Every declared RV64I form now executes under the laboratory**: 9 tracked guests cover all 52 forms of `rv64i-lab-v0`, agreeing with sail-riscv and spike on 117/117 aligned steps (`scripts/run_semulith_smoke.py`, `2026-09-29`), and coverage is gated with its denominator by the 24th doctrine `EXERCISE-COVERAGE` (52/52).
- **Active trees:** `P2-SCALAR` (1/9 — frontier `.2`, boundary arithmetic and state interactions), `LAB-BENCH` (1/2 — frontier `.2`), `UPSTREAM-TRACK` (3/4 — frontier `.3`), `PUSH-DISCIPLINE` (1/3 — frontier `.2`), `MODEL-BOOKS` (0/6 — frontier `.1`), `ARTIFACT-CLEANUP` (1/1 — recurring §8; last run `2026-09-29`).
- **Closed `2026-09-29`:** `P2-SCALAR.1` — the declared instruction scope completed: five scope-completion guests (`scope-alu` 31 steps, `scope-mem` 29, `scope-branch` 19/24, `scope-ecall`, `scope-ebreak`), every expectation derived from the pinned spec before any run (`EVD-05`). `EXERCISE-COVERAGE` fired RED against the real corpus at 15/52 (37 forms named) before registration, GREEN since. `fence` needed its `fm`/`pred`/`succ` fields — now derived from the pinned `arg_lut.csv` (fragment + assembler extended, `definition.rs` regenerated, no opcode typed by hand). The trace adapter learned sail/spike's measured `ecall`/`ebreak` spellings (unknown spellings raise — a dropped trap reads as agreement). Two 0-result comparisons pre-write 1, because the observation vocabulary is the VISIBLE register change. Defect logged + owned: reserved-`fm` FENCE executes as a nop where `D-FENCE` says illegal-instruction → `P2-SCALAR.3` (needs a legality constraint the format lacks).
- **Closed (older):** `P1-LAB` 13/13 — gate `G1` RUN, verdict `incomplete`: criteria 1–5 met; criterion 6 (the C guest) owned by `P2-SCALAR.5`. `G1-REPORT.md` regenerates from tracked inputs (now 9 guests, 117 steps).
- **Direction (director, 2026-09-14):** every source of truth is **one format**, S-expression (`decision_one-format-every-source-of-truth`).
- **Direction (delegated, 2026-09-27):** the semantics **data** is the execution authority (`decision_interpreter-before-compiler`); every lane names its consuming milestone.
- **Direction (director, 2026-09-27):** everything must also run in the **browser** — JS + Wasm first-class from the first crate; now a gate (`PORT-WEB`).
- **Frontier:** `P2-SCALAR.2` (boundary arithmetic and state interactions) is next by the tree's order. ⭐ Still awaiting director (recorded in `P1-LAB.12`'s ROUTING EVIDENCE): is the C guest allowed to land in P2, or must G1 read `passed` first? — does not block `.2`–`.4`.
- ⚠️ The `.9` mutation suite is the detector's proof, not the model's; the `.11` baseline is one named host's measurement, not a portable constant.
- **Materials:** 36 primary sources in `materials/catalog.sexp` (corpus `3c45e81`), cached in gitignored `.materials/`; `$SEMULITH_CHIPDOC_ROOT` never tracked. Run-real-code set pinned at `.materials/run-real-code/`.
- **Citations:** `check_citations.py` resolves 52 of 52, offline from the cache. The pin is docs.riscv.org, NOT github.com/riscv/riscv-isa-manual — read `docs/knowledge/a-version-string-is-not-an-identity.md` first.
- **Next action:** `P2-SCALAR.2` — boundary values, sign/zero extension, shift corner cases.
- **Also open:** `MODEL-BOOKS.1` (book structure + the complete materials bill), `UPSTREAM-TRACK.3`, `PUSH-DISCIPLINE.2`, `LAB-BENCH.2`. ⭐ Director input to schedule (no pivot taken): chipdoc's corpus carries a semulith feed (`$SEMULITH_CHIPDOC_ROOT/SEMULITH.md` → `catalog/semulith-proposals.sexp`); a MODEL-METHOD catalogue slice consumes it when that frontier opens.
- **Feel it now:** `bash scripts/check_exercise_coverage.sh` — the 52/52 verdict with its denominator; `cargo run -p semulith-cli -- demo --guest=scope-alu` — a scope-completion guest under the detector; `cargo run -p semulith-cli -- demo --guest=guest-control --mutate=jalr-odd-bit` — the trace + the detector's verdict; `make bench && (cd bench && python3 -m http.server 8000)` — the browser bench; `scripts/gate_report.py rv64i-lab-v0 --gate G1 --stdout` — the honest gate.
- **Read first:** `docs/decisions/INDEX.md` — the last five records define the current direction. **Latest commit:** `git log -1`. **In-flight uncommitted work:** none.
- ⛔ **Do not push.** Cadence is 300 commits — `scripts/check_push_cadence.sh --status` says where we stand; below it a push is exceptional and **only the director may approve it** (`decision_push-cadence`). `SEMULITH_PUSH_APPROVED` carries the director's reason, never an agent's judgement.
- **Blockers:** none. LinkedSpec pinned `a8d34c845` (LS-001 fix shipped; RGX `8763a0e6` unchanged); our repro re-ran 8/0. ⛔ Never patch the submodule; adopt by moving the pin. **Sanctioned standing process:** CHIPDOC's ChipdocWatcher watches the chipdoc catalog and `materials/catalog.sexp` (director ruling 2026-09-27: it stays; do not kill it, do not flag it — `doctrine/sanctioned_processes.tsv` exempts it, `ARTIFACT-CLEANUP.2`).
- **LinkedSpec readers:** `compare_readers.py` sweeps every tracked `.sexp` — Lispish (the two CLASS families as the LS-guard) and SExprDocumentV1 via `sexpr_file` (the read path).
