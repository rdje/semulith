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
- **Active tree:** `P0-PROFILE` (gate `G0`) — 8 of 9 leaves done. `.9` is the last.
- **Frontier leaf:** `P0-PROFILE.9` — the evidence-obligation policy and the `G0` report.
- **Next action:** `P0-PROFILE.9`. Declare, per obligation class, what KIND of evidence it
  requires (`EVD-03`) — written before the implementation that would otherwise pick whatever
  evidence is easiest — then generate the `G0` report from pinned inputs. ⛔ It must name inputs,
  commands, actual results and limitations (`EVD-08`) and read **`incomplete`**: 66 checks are
  declared and none implemented, so `passed` is not available to it.
- **Re-run the evidence path any time:** `scripts/fetch_references.sh --verify-only` then
  `scripts/run_smoke.py` (both need `target/refs/`, untracked).
- **Latest commit:** see `git log -1` — `SEMULITH-P0-0028 (leaf P0-PROFILE.8)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
