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
- **Active tree:** `SEMULITH-PKG` (ingest planning package v0.2 under the spine).
- **Frontier leaf:** `SEMULITH-PKG.2` — adopt the claim-verification standard.
- **Next action:** add `docs/CLAIM_VERIFICATION.md` with a fenced local-adoption note, link it
  from `README.md`, record the adoption decision; then `.3` (live-fingerprint gates) and
  `.4` (mdBook sync). Then open `SEMULITH-TREES` to convert `ROADMAP.md` P0–P7 into trees.
- **Latest commit:** see `git log -1` — `SEMULITH-PKG-0002 (leaf SEMULITH-PKG.1)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
