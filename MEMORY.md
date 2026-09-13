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
- **Active tree:** `P0-PROFILE` (gate `G0`) — 5 of 9 leaves done.
- **Frontier leaf:** `P0-PROFILE.3` — the requirements catalog seed.
- **Next action:** `P0-PROFILE.3`. Turn the 25 sourced decisions in `profile.toml` into
  `requirement.schema.json` records: `source_semantics` must distinguish defined /
  implementation-defined / unspecified / reserved, and `research_status` stays separate from
  `implementation_status`. No record may claim `resolved` research without a real `source_refs`
  locator. `.4` (the environment contract) needs `.3`'s obligation IDs.
- **Re-run the evidence path any time:** `scripts/fetch_references.sh --verify-only` then
  `scripts/run_smoke.py` (both need `target/refs/`, untracked).
- **Latest commit:** see `git log -1` — `SEMULITH-MIR-0025 (leaf MIRROR-DRIFT.4)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
