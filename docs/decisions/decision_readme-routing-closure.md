# The landing page's caps are owned by a destination registry, not by a script

- **Type:** `decision`
- **Date:** `2026-09-13`
- **Status:** `active`
- **Owner / source:** director standing policy (README policy); adopted by leaf `SEMULITH-PKG.4`

## The fact / decision

`README_POLICY.md` is project-owned, refreshed to the director's current revision, and its
neutral body is imported unedited under a fenced local-adoption note. This project's reviewed
caps — **85 lines and 4,864 bytes**, derived from a 67-line / 3,719-byte trimmed landing page —
and every destination the README routes to are held as **data** in `doctrine/readme_routes.tsv`
and enforced by `scripts/check_readme_routes.sh`.

Each destination carries a route class (`reader_navigation` / `author_overflow` / `both`), a
lifecycle class (`hot_live` / `partitioned` / `generated_index` / `append_history` / `frozen` /
`normative`), a named owner, and the pressure control its class requires. A *health target*
prints; a *ceiling* blocks.

## Why

A README cap alone does not remove append pressure, it relocates it. Measured in the policy's
reference adoption: README status/history guidance routed overflow into an unchecked
neighbouring status file which reached **1,547,057 bytes**, 94.7% of it dated changelog
content — while the README guard stayed green the whole time. A repository with this shape
(a hot `LIVE_STATUS.md`, an append-only `CHANGELOG.md` and `DEV_NOTES.md`, growing `docs/tasks/`
and `docs/decisions/` families) is the exact configuration in which that happens.

Holding the numbers in the registry rather than in the check keeps one derived source instead
of N synchronized copies: the checker re-runs the neutral README guard **with the registry's
values**, so there is no second place a cap can be written.

## How to apply

- Adding a link to `README.md` that points somewhere ungoverned fails the commit. Add the row,
  with a class, an owner and a bound — or do not route readers there.
- **Never raise a ceiling to land content.** A raise requires a reviewed decision, recorded in
  a task leaf, that the surface's *contract* expanded.
- When an `append_history` ceiling fires (`CHANGELOG.md` at 64 KiB, `DEV_NOTES.md` at 48 KiB),
  the remedy is to shard, and the sharding tool does not exist yet. That is **recorded debt
  with an owner**, not an exemption: the firing ceiling is what opens the leaf that builds it.
- Full live-document-size containment is deliberately **not** adopted yet — the largest live
  surface is 16,228 bytes and there is no measured pressure. The registry's ceilings are the
  trigger; when one fires, adopt the containment doctrine rather than widen the number.

Related: [[decision_claim-verification-adopted]], [[decision_delivery-provenance-is-frozen]].
