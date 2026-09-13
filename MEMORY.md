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
- **Active tree:** `P0-PROFILE` (gate `G0`) — 1 of 9 leaves done.
- **Frontier leaf:** `P0-PROFILE.2` — the state inventory.
- **Next action:** `P0-PROFILE.2` — the state inventory (x0..x31, pc, widths, aliases, reset
  values, and any pending state that can influence a future observation), each entry
  source-linked. The specification is already pinned: run `scripts/fetch_sources.sh` to restore
  `target/sources/riscv-v20260120/` (untracked) before reading locators.
- **Latest commit:** see `git log -1` — `SEMULITH-P0-0013 (leaf P0-PROFILE.1)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
