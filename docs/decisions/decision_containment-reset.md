# Containment reset: the review surface is not size-contained, the task family is not capped

- **Type:** `decision`
- **Date:** `2026-10-21`
- **Status:** `active`
- **Owner / source:** director ruling in session `2026-10-21`, recorded by `LIVE-CONTAINMENT.4`
  slice (m), `SEMULITH-LC-0052`; measurement at `2634e94` by `bash scripts/check_readme_routes.sh`
  and a per-family census (`git ls-files docs/tasks | xargs wc -c`)
answers: Which surfaces carry no size ceiling, why, and what keeps the task family readable without an aggregate cap?

## The fact / decision

Three rulings, verbatim in substance:

1. **The book is not size-contained.** "The book shall have ZERO containment doctrine applied,
   that's a book, that is the only user visible surface, it is used to explain thoroughly what the
   project, its codebase, I mean everything. It shall not be restricted in its size and in what it
   can contain." `docs/book/` carries no ceiling on any axis. The unit books under `docs/models/`
   are built by the same `make book` target as part of the same review surface and carry none
   either.
2. **The task family's aggregate and file-count ceilings are ungoverned (0).** The per-part ceiling
   stays at 131,072 B. When a tree file fills, its closed records move verbatim into a new ordinary
   archive part under `docs/tasks/archive/`; that is the standing mechanism and needs no seal.
   Approved by the director on `2026-10-21` in these words: "Set the total-bytes ceiling and the
   file-count ceiling on that row to 0, so the family can grow as the project does. Keep the
   per-file ceiling at 128 KiB, so no single tree file becomes a monolith. … Nothing else about
   the gate changes."
3. **A second task-history seal is rejected** ("I reject (1)"). Slice (m) of `LIVE-CONTAINMENT.4`,
   scheduled as that seal, is withdrawn; this record is what the slice lands instead.
4. **Per-unit duplication is cut** ("Ok for (4)"): the owning tree record is a unit's single
   narrative and names its verification and commit; the gated acceptance rows stay; the
   Verification Log and Commit Log sections stop growing; `CHANGELOG.md` takes one line per
   unit; `DEV_NOTES.md` takes a dated entry only for a real lesson; decision records only for
   cross-cutting facts; no more retention continuations with inverse scripts.

## Why

- Measured at `2634e94`: `docs/tasks/` held 3,143,298 of 3,145,728 B (108 of 116 files), 2,430 B
  from the ceiling, and `docs/book/` 524,247 of 524,288 B. A unit of work cost about 3.5 KB of
  task-family bytes, so the next commit of any work would have failed README-ROUTING-CLOSURE.
  Since `2026-10-10`, 66 of 170 commits were containment or cleanup housekeeping while the
  CPU-SYSTEM gate stayed `incomplete`.
- The registry's own rule is that a ceiling moves only by a reviewed decision in a task leaf.
  This is that decision. The director's words are quoted so the authority is the ruling, not an
  agent's reading of it.
- The book is the only surface the director reviews. A cap on it limits what the project can
  explain, which inverts the surface's purpose; the structural gates (BOOK-INDEX, REGISTRY-MIRROR,
  UNIT-BOOKS, the navigation qualifiers) keep it true without bounding its size.
- The per-part cap is what keeps one tree readable in a sitting; the aggregate cap only measured
  how much history the project carries, and sealing history to satisfy it cost sessions.
- Feedback recorded with the ruling: "I'm surprised you didn't complain loud enough sooner. We
  are a team remember, you should have raised such blocking issue way sooner." A blocker that
  stems from a rule is a team decision, raised first with numbers and options.

## How to apply

- `doctrine/readme_routes.tsv`: `docs/book/` and `docs/models/` rows all zero; `docs/tasks/`
  ceilings `0 / 0 / 131072`. A later ruling may set numbers again; nothing else in the gate changed.
- When a tree's per-part cap nears, cut its oldest closed records verbatim into
  `docs/tasks/archive/<TREE>-<name>.md` with a header naming the source commit, span bytes/LF and
  SHA256, leave the original headings as stubs linking there, and add the part to the book's
  archive list. No inverse scripts, no sealed terminals, no reader.
- Record a unit once: tree record (what, why, verification, commit id) + acceptance rows; one
  `CHANGELOG.md` line; `DEV_NOTES.md` only when there is a lesson, promoted or declined.
- Related: [[task-family-count-rederivation-retention]], [[decisions-family-second-rederivation]],
  [[models-family-five-books]], [[memory-next-action-pointer]].
