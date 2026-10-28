# Orphan incremental sessions are removed whole, anchored to the cleanup record; other trees' leftover build directories go

- **Type:** `decision`
- **Date:** `2026-10-28`
- **Status:** `active`
- **Owner / source:** the director, 2026-10-28 (option C of `ARTIFACT-CLEANUP.29`; design
  target/artifact-cleanup/AC29/design.md; [`decision_director-rulings-2026-10-28.md`](decision_director-rulings-2026-10-28.md)).
  Authority `director`. Refines rule 2 of [`decision_orphan-incremental-sessions.md`](decision_orphan-incremental-sessions.md).
answers: What does the recorded class "orphan incremental session" remove, and what happens to the leftover build directories of older units?

## The fact / decision

1. The class removes whole sessions — every regular file under an orphan session directory, then the
   directory — but only in a crate-hash directory none of whose sessions is younger than the last recorded
   cleanup act. Live caches between two cleanups are never touched; the age rule is anchored to the record,
   not to a threshold.
2. The nested cargo target directories other trees' units left under `target/` (18 roots, 24,135,434,240 B
   on 2026-10-28, listed in target/artifact-cleanup/AC0086-all-nested-targets.txt) are removed once, each
   validated by shape and content before removal, as `XTASK.9` removed its own.

## Why

Option A would leave ~442 MB of skeletons forever; B would also take a cache a build is about to reuse. C
removes the orphans completely and keeps the live caches. The leftover directories are disposable builds of
closed units, and rule 1 already says the unit removes them.

## How to apply

- The class lives in the selection tool and its probes, with RED arms: a directory with a session younger
  than the last record is never approved; a file outside the cargo scope is never approved; the census still
  binds before the guarded core unlinks. Executed by `ARTIFACT-CLEANUP.29`.
