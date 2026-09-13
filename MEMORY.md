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
- **Active tree:** `P0-PROFILE` (gate `G0`) — 6 of 9 leaves done.
- **Frontier leaf:** `P0-PROFILE.4` — the environment contract v0.
- **Next action:** `P0-PROFILE.4`. `.3` minted 25 `OB-*` obligation ids that nothing yet defines —
  `RECORD-SCHEMA` carries that as a named gap. Build the versioned assumption/guarantee set from
  `docs/CPU_ENVIRONMENT.md` §2–§3 (address units, access widths, virtual-time domain, permitted
  event-delivery points, ordering), each with its authority, and define those obligations with
  positive **and negative** fixtures. Laboratory policy may nowhere override an architectural rule.
- **Re-run the evidence path any time:** `scripts/fetch_references.sh --verify-only` then
  `scripts/run_smoke.py` (both need `target/refs/`, untracked).
- **Latest commit:** see `git log -1` — `SEMULITH-P0-0026 (leaf P0-PROFILE.3)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
