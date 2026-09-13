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
- **Active tree:** none — every tree is `done` or `proposed`.
- **Just closed:** the P0 tree, 9/9. Gate `G0` has been RUN and reads **`incomplete`**: its three
  criteria are met, and 66 declared checks are unimplemented, which is the stated reason.
  `incomplete` is the deliverable, not a failure.
- **Frontier leaf:** `P1-LAB.1` — the crate skeleton. Open `P1-LAB` next.
- **Next action:** `P1-LAB.1`. Create `semulith-core`, `semulith-verify`, `semulith-cli`
  (`docs/ARCHITECTURE.md` §4); `crates/app/` is still the scaffold's placeholder. Then `P1-LAB`
  is where the **66 declared checks acquire fixtures** — until they do, `G0` cannot read `passed`.
  Two findings are already routed in: the delivered `examples/` records are referentially
  inconsistent (a first corpus for the graph checker), and `D-JALR-LSB` needs a mutation-suite
  control because both references clear the bit.
- **Re-run the evidence path any time:** `scripts/fetch_references.sh --verify-only` then
  `scripts/run_smoke.py` (both need `target/refs/`, untracked).
- **Latest commit:** see `git log -1` — `SEMULITH-P0-0029 (leaf P0-PROFILE.9)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
