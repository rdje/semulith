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
- **Active tree:** `P0-PROFILE` (gate `G0`) — 2 of 9 leaves done.
- **Frontier leaf:** `P0-PROFILE.5` — the reference candidate dossier.
- **Next action:** `P0-PROFILE.5` — the reference candidate dossier (Sail RISC-V, Spike, ACT4):
  actual availability, build, configuration, invocation, trace granularity, injection
  capability, terms and hashes. `SRC-03` means a candidate that cannot be obtained is recorded
  as such, with the attempt. It unblocks `OQ-2` and `OQ-3` in the profile dossier.
  Run `scripts/fetch_sources.sh` first to restore `target/sources/` (untracked).
- **Latest commit:** see `git log -1` — `SEMULITH-PKG-0016 (leaf SEMULITH-PKG.8)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
