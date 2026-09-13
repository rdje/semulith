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
- **Active tree:** `P0-PROFILE` (gate `G0`) — 4 of 9 leaves done.
- **Frontier leaf:** `P0-PROFILE.7` — the independence inventory.
- **Next action:** `P0-PROFILE.7` (`EVD-04`). Two models now AGREE over 15 aligned steps — worth
  exactly as much as their independence, which is unexamined. Record per subsystem whether
  `sail-riscv`, `spike` and `qemu` share semantic code or expected-result derivation; ACT derives
  its results from a configured Sail model, so that pair is known-correlated. Record unknown
  ancestry as unknown. The `lineage` field on each candidate in `references.toml` is the input.
- **Re-run the evidence path any time:** `scripts/fetch_references.sh --verify-only` then
  `scripts/run_smoke.py` (both need `target/refs/`, untracked).
- **Latest commit:** see `git log -1` — `SEMULITH-P0-0021 (leaf P0-PROFILE.6)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
