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
- **Active tree:** `P0-PROFILE` (gate `G0`) — 3 of 9 leaves done.
- **Frontier leaf:** `P0-PROFILE.6` — the matched-profile smoke test.
- **Next action:** `P0-PROFILE.6` — run a real experiment against a matched reference and
  reproduce it: independently encoded arithmetic **and** an access/trap case. Three models are
  obtained and configured (`scripts/fetch_references.sh --verify-only` re-derives all six pins);
  none is *usable* until this leaf passes. Needs `.8`-style guest programs — encode them by hand
  rather than with a toolchain, so expected values come from the specification, not a model.
  ⛔ Do not treat our default+override merge as Sail's own report: it will not emit its effective
  configuration. See [`decision_reference-acquisition-route`](docs/decisions/decision_reference-acquisition-route.md).
- **Latest commit:** see `git log -1` — `SEMULITH-P0-0020 (leaf P0-PROFILE.5)`.
- **In-flight uncommitted work:** none.
- **Blockers:** none.
