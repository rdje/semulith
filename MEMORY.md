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
- **Active tree:** `SEMULITH-PKG` — 5 leaves done; `.6` open to fix this project's code-path declaration.
- **Frontier leaf:** `SEMULITH-PKG.6` — declare `.doctrine/code_paths.txt`.
- **Next action:** the default code-path pattern matches `docs/book/src/*.md` (prose) and
  misses `doctrine/*.tsv` (real gate data) — declare `.doctrine/code_paths.txt`, then fire
  `TASK-ACCEPTANCE` RED to prove it still catches a real code change. Then open
  `SEMULITH-TREES` to convert `ROADMAP.md` P0–P7 into task-trees.
- **Latest commit:** see `git log -1` — `SEMULITH-PKG-0006 (leaf SEMULITH-PKG.5)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
