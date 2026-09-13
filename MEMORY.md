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
- **Active tree:** `P0-PROFILE` (gate `G0`) — 7 of 9 leaves done. Remaining: `.8`, `.9`.
- **Frontier leaf:** `P0-PROFILE.8` — three representative guest programs.
- **Next action:** `P0-PROFILE.8`, and it is **blocked on a source, not on effort**. The programs
  must exercise arithmetic, control flow and a memory/fault boundary — but control flow needs the
  B and J immediate layouts, and `.6` measured that the pinned specification does not contain
  them (the format diagrams are images; zero 7-bit patterns across all six artifacts).
  `scripts/riscv_asm.py` REFUSES those two formats rather than typing a layout from memory.
  Resolve the encoding source first, pin it, then write the programs.
- **Re-run the evidence path any time:** `scripts/fetch_references.sh --verify-only` then
  `scripts/run_smoke.py` (both need `target/refs/`, untracked).
- **Latest commit:** see `git log -1` — `SEMULITH-P0-0027 (leaf P0-PROFILE.4)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
