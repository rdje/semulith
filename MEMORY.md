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
- **Active tree:** `MODEL-BOOKS` (0 of 6 leaves) — blocked behind a defect, see below.
- **Just closed:** the P0 tree, 9/9. Gate `G0` has been RUN and reads **`incomplete`**: its three
  criteria are met, and 66 declared checks are unimplemented, which is the stated reason.
  `incomplete` is the deliverable, not a failure.
- **Frontier leaf:** `MODEL-BOOKS.1`, **blocked**. Fix `P0-PROFILE.10` first.
- ⛔ **Next action: reopen `P0-PROFILE` for `.10` — a measured defect in committed work.** The
  matched-profile override configures the **ISA only**; the platform and memory map were never
  touched, so the reference still provides a CLINT, an interrupt generator and two I/O regions.
  Measured: a guest reads CLINT `mtime` at `0x0200BFF8` with a plain `ld` and it **advances**
  (2→3). That refutes `OB-ENV-VIRTUAL-TIME` ("no time source"), `OB-ENV-EVENT-DELIVERY` ("no
  interrupt controller"), `D-MAIN-VS-IO` ("no I/O region is declared") and `privilege_modes = []`
  (every trace line reads `[M]`). **The repair is verified**: adding `platform.clint.supported =
  false`, the interrupt generator off and a MainMemory-only region list makes both probes fault
  with `load-access-fault` and leaves all three guests agreeing over 28 steps.
- **Then:** `MODEL-BOOKS.1`, then `P1-LAB.1` (the crate skeleton; where the 66 declared checks
  acquire fixtures).
- **Re-run the evidence path any time:** `scripts/fetch_references.sh --verify-only` then
  `scripts/run_smoke.py` (both need `target/refs/`, untracked).
- **Latest commit:** see `git log -1` — `SEMULITH-P0-0029 (leaf P0-PROFILE.9)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
