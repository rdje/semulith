# MEMORY.md exists solely to point at the next action

- **Type:** `decision`
- **Date:** `2026-10-02`
- **Status:** `active`
- **Owner / source:** director rulings `2026-10-02` (three in-session messages, one intent),
  executed by `MEMORY-POINTER.1`.

## The decision

`MEMORY.md` — the layer-A resume pointer — exists **solely to point at the next action**. It is
**overwrite-only, never appended to**, exactly as `MEMORY_ARCHITECTURE.md` §6 defines: latest
commit, active trees, the single next action, in-flight state, blockers. Everything else —
project state, directions, measurements, caveats — lives in its own layer (task-trees,
`docs/decisions/`, `docs/knowledge/`, git) and the pointer names it by reference only.

## Why (measured at the ruling)

The pointer had re-grown into a state digest: 34 lines / 7,031 bytes against a health target of
30 lines / 1,792 bytes — the §6 failure shape ("the 'Current state' block accumulating one entry
per session"). Two trims in one session had already landed it at 97% of its hard byte cap.

## Consequences

- The slimmed file carries the §6 template fields and the claims `TREE-CLAIMS` gates (the
  `Active trees:` line; leaf-count shapes), nothing else.
- Every line dropped was first verified to have a durable home; the audit found exactly one
  dangling ruling (`document EVERYTHING`, `2026-10-01`), backfilled as
  `decision_document-everything` in the same slice.
- Future MEMORY.md edits overwrite "Current state" wholesale. Growth past the health target is
  a signal to demote content, never to negotiate the cap.
