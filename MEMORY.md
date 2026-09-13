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
- **Frontier leaf:** `SEMULITH-PKG.4` — refresh `README_POLICY.md`, set reviewed caps.
- **Next action:** adopt the director's current `README_POLICY.md` revision under a fenced
  adoption note, derive line/byte caps from the trimmed landing page, enforce them in
  `scripts/check_doctrines.project.sh`, and close the routing-destination inventory. Then `.5`
  (mdBook). Then open `SEMULITH-TREES` to convert `ROADMAP.md` P0–P7 into trees.
- **Latest commit:** see `git log -1` — `SEMULITH-PKG-0004 (leaf SEMULITH-PKG.3)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
