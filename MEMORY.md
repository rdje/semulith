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
- **Active trees:** `MIRROR-DRIFT` (1 of 3 leaves) and `P0-PROFILE` (gate `G0`, 2 of 9 leaves).
- **Frontier leaf:** `MIRROR-DRIFT.2` — the doctrine documents mirror the enforcer registry.
- **Next action:** `MIRROR-DRIFT.2`. Measured drift to repair, AFTER firing the new gate RED on
  it: `docs/book/src/working/doctrines.md` lists 3 project doctrines where 5 are registered
  (`PROFILE-CONSISTENCY`, `SEAM-INTEGRITY` missing, and now `FRONTIER-SYNC` — deliberately left
  by `.1` so the drift could be fired RED rather than quietly patched). Its "Thirteen checks run
  today" sentence is a hand-typed derived number too.
- **Then:** `P0-PROFILE.5` — the reference candidate dossier (Sail RISC-V, Spike, ACT4): actual
  availability, build, configuration, invocation, trace granularity, injection capability, terms
  and hashes. `SRC-03` means a candidate that cannot be obtained is recorded as such, with the
  attempt. It unblocks `OQ-2` and `OQ-3`. Run `scripts/fetch_sources.sh` first to restore
  `target/sources/` (untracked).
- **Latest commit:** see `git log -1` — `SEMULITH-MIR-0017 (leaf MIRROR-DRIFT.1)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
