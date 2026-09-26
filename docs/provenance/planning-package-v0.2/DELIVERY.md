# Delivery record — Semulith planning package v0.2

This directory is a **frozen delivery record**. It states what was handed to this repository,
with what fingerprints, on what date. Nothing here is maintained against the live tree; the
live tree is maintained against the task-trees.

- Package version: `0.2`
- Delivery date: `2026-09-13`
- Ingested by: task-tree leaf [`SEMULITH-PKG.1`](../../tasks/SEMULITH-PKG.md)

## Contents of this directory

| File | What it is |
| --- | --- |
| `MANIFEST.sha256` | the delivered file manifest, **verbatim**, with the paths it carried at delivery |
| `DESIGN_INPUTS.json` | SHA-256 fingerprints of the three supplied design-input documents, **verbatim** |
| `PACKAGE_CHECKS.md` | the checks the package author reports having run on the package, **verbatim** |
| `dispositions.tsv` | **the machine-readable owner** of each manifest row's disposition — data, not prose |

## Why this is frozen and not a live check

`MANIFEST.sha256` lists `README.md` and `ROADMAP.md`. This repository must evolve both: the
landing page is governed by `README_POLICY.md`, and the roadmap is the source the task-trees
are grown from. A manifest at the repository root that invites `shasum -c` while containing
rows guaranteed to drift is not a control — it is a check whose only stable outcome is
failure, and a check that always fails teaches its reader to skip it.

So the rows are split by disposition, and the split is declared here rather than implied.

Every row of `MANIFEST.sha256` carries exactly **one** disposition, declared as data in
`dispositions.tsv`. There is no fourth, unstated category — a manifest row with no
disposition, or a disposition naming a path the manifest does not list, is a breach.

| Disposition | Meaning |
| --- | --- |
| `frozen-in-place` | still at the delivered path with the delivered bytes; changing one is a deliberate, task-tree-owned edit of a reviewed input |
| `relocated` | identical bytes, moved; the manifest row's path is the delivery path and `current_path` is where it lives now |
| `live` | owned by this repository from ingestion onward; the manifest row records the delivered bytes and is *expected* to disagree with the working tree |

`scripts/check_delivery_provenance.sh` re-derives the `frozen-in-place` and `relocated` rows
against the live tree on every commit, asserts that the manifest and the disposition ledger
cover exactly the same row set, and prints the per-disposition counts. **That script, not this
document, is the enforcement** — the counts are derived on every run rather than carried here,
because a number synchronized by hand is a number that goes stale silently.

## Design inputs

`DESIGN_INPUTS.json` fingerprints three documents that were supplied to the package author
and are **not reproduced in this repository**:

| Input id | File name | Status here |
| --- | --- | --- |
| `roadmap-v0.1` | `CPU_DSP_Software_Modeling_Roadmap_v0.1.md` | not present; superseded by `ROADMAP.md` v0.2 |
| `cpu-roadmap-review` | `Review_of_CPU_DSP_Modeling_Roadmap_v0_1.md` | not present; its disposition is `docs/REVIEW_DISPOSITION.md` |
| `archogen-roadmap-revision-2.0` | `os-generation-roadmap-revised-v2.md` | not present; its boundary is `docs/ARCHOGEN_INTEGRATION.md` |

Those hashes are unverifiable from this repository alone, and that is stated rather than
hidden: they are the author's record of the inputs, retained so a future reader can confirm
which revision a design document responded to if the input is ever produced.

## What `PACKAGE_CHECKS.md` does and does not establish

It reports schema validation performed with Python `jsonschema` 4.26.0 in the package
author's environment. That environment is not this one — `python3 -c "import jsonschema"`
here raises `ModuleNotFoundError`. The results are therefore **cited, not currently
re-derivable in this repository**. Rule `RUST-01` makes the re-derivation a Rust deliverable,
and the P1 checker lane owns it. Until then the package's schema claims carry that named gap.

## Ingestion changes

Exactly one delivered file was not ingested: `docs/SEMULITH_ARCHOGEN_INTEGRATION.md`, which
was byte-identical to `docs/ARCHOGEN_INTEGRATION.md`, absent from `MANIFEST.sha256`, and
referenced by nothing. Two files owning one document contradicts rule `OWN-01`, so the
unlisted copy was deleted and the manifest-named path kept.

## Disposition changes

- `2026-09-26` — `docs/ARCHITECTURE.md` reclassified `frozen-in-place` → `live`, owned by
  leaf `SOT-FORMAT.8`. The file is the architecture contract that the mdBook includes verbatim,
  and the codebase's format decision — one S-expression format, fragments, the composition
  operator, the schema layer — had landed in code while the contract still named no format at
  all (`grep -c 'S-expression'` → 0). A frozen architecture document that contradicts the tree
  it governs is the drift this ledger exists to record honestly, not to paper over. The
  delivered bytes remain in `MANIFEST.sha256` as the delivery record; from this date the file
  is owned by this repository and is expected to evolve with the format it describes.
