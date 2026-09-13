# Delivered-package provenance is frozen, and its live rows are declared

- **Type:** `decision`
- **Date:** `2026-09-13`
- **Status:** `active`
- **Owner / source:** task-tree leaf `SEMULITH-PKG.1`; measured while ingesting planning package v0.2

## The fact / decision

A supplied package's `MANIFEST.sha256` is a record of **what was delivered**, not a live
integrity check on the repository. It is stored under
`docs/provenance/<package>/` together with the other delivery artifacts, and every row is
given one of three dispositions in that directory's `DELIVERY.md`: `frozen-in-place`,
`relocated`, or `live`. Only the first two are mechanically re-derived.

## Why

The delivered manifest listed `README.md` and `ROADMAP.md`. This repository must evolve both
— the landing page is governed by `README_POLICY.md` and the roadmap is the source the
task-trees grow from. Left at the repository root, the manifest would have invited
`shasum -a 256 -c MANIFEST.sha256` while containing rows guaranteed to drift, so its only
stable outcome would be failure. A check whose failure is expected trains its reader to skip
it, and a skipped check silently stops covering the rows that *were* still meaningful.

Deleting the manifest was the other option and is worse: rules `SRC-01` and `EVD-08` require
recorded fingerprints, and the schema/example fixtures are exactly the artifacts a later
evidence claim will be built on.

## How to apply

- Supplied artifacts arrive under `docs/provenance/<package>/`, verbatim, with a `DELIVERY.md`
  recording date, contents, and the disposition of every manifest row.
- Never edit a frozen record to make it agree with the tree. Change the disposition table and
  say why, or fix the tree.
- A fingerprint that is supposed to hold is gated by a tracked script; a fingerprint that is
  expected to drift is named in the `live` row set. There is no third, unstated category.
- Hashes of inputs that are not present in this repository (see `DESIGN_INPUTS.json`) are kept
  as the author's record and are labelled unverifiable here rather than implying a check.

Related: [[decision_public-repository-no-confidential-content]].
