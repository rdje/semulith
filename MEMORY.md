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
- **Active trees:** `MIRROR-DRIFT` (2 of 3 leaves) and `P0-PROFILE` (gate `G0`, 2 of 9 leaves).
- **Frontier leaf:** `MIRROR-DRIFT.3` — the live docs' derived numbers.
- **Next action:** `MIRROR-DRIFT.3`. Gate this file's active tree and frontier leaf, and every
  `N leaves` claim in `LIVE_STATUS.md`, against the trees. The `.1` census found NO drift here,
  so the leaf is prevention: say so, and fire the gate RED on an edited copy.
- **Then:** `P0-PROFILE.5` — the reference candidate dossier (Sail RISC-V, Spike, ACT4): actual
  availability, build, configuration, invocation, trace granularity, injection capability, terms
  and hashes. `SRC-03` means a candidate that cannot be obtained is recorded as such, with the
  attempt. It unblocks `OQ-2` and `OQ-3`. Run `scripts/fetch_sources.sh` first to restore
  `target/sources/` (untracked).
- **Latest commit:** see `git log -1` — `SEMULITH-MIR-0018 (leaf MIRROR-DRIFT.2)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
