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
- **Active trees:** `MODEL-METHOD` (2 of 10) and `MODEL-BOOKS` (0 of 6).
- **Frontier leaf:** `MODEL-METHOD.9` — `semantics.sexp`, what each instruction *does*.
- **Next action:** `MODEL-METHOD.9`. The canonical definition is the single source of truth a
  generator engine reads (`decision_canonical-definition-input`): a **set of format-fit files**,
  S-expressions for `encoding.sexp` and `semantics.sexp`, records staying JSON/TOML. `.8` closed
  the encoding half — the repo now owns its encodings and **builds with the untracked upstream
  hidden**. Semantics are the other half and **nothing machine-executable exists yet**: every
  instruction in the declared scope needs an expression carrying the source locator it was derived
  from, so a reviewer can check the expression against the sentence. Then `.7` (no duplicated
  fact), `.10` (is the definition SUFFICIENT for an engine — the precondition for writing model
  code), `.2`–`.4` (materials schema, census, acquisition), `.5`–`.6` (method, no-coding gate).
- **Just closed:** `P0-PROFILE` 10/10. Gate `G0` run, verdict **`incomplete`** (68 declared
  checks, 0 implemented — the deliverable, not a failure). ⛔ Reopened for `.10` after a measured
  defect the first nine leaves carried: the profile was matched on its **instruction set and not
  its platform**, so the reference kept a core-local interruptor a guest could read `mtime` from
  with a plain load. Corrected at source; held by the negative fixture `guest-no-device.s`.
  Spike's platform is **not** matchable and that is enumerated (`DIFF-PLATFORM-SPIKE`).
- **Then:** `P1-LAB.1` — the crate skeleton; where the 68 declared checks acquire fixtures.
- **Re-run the evidence path any time:** `scripts/fetch_references.sh --verify-only` then
  `scripts/run_smoke.py` (both need `target/refs/`, untracked).
- **Latest commit:** see `git log -1` — `SEMULITH-MM-0037 (leaf MODEL-METHOD.8)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
