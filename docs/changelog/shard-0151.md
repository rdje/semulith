# CHANGELOG shard — SEMULITH-BR-0018 … SEMULITH-BR-0018

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-BR-0018 (leaf P3-BREADTH.7) — the dsp56300-lab-v0 dossier lands, governed

- The three schema-validated documents moved from
  `docs/tasks/artifacts/p3-breadth/dsp56300-dossier/` to `profiles/dsp56300-lab-v0/`
  (rename lineage kept; headers rewritten from "NOT LANDED" to the landed gate map):
  `profile.sexp` (the subset decisions + the vehicle declaration), `state.sexp` (the F6
  census as data), `interactions.sexp` (6 axes, 21 cells).
- Every attaching gate green WITH the documents landed: EXERCISE-COVERAGE (19/19 DSP,
  52/52 rv64), EXTRACTION (sibling-crate route reported), INTERACTION-MATRIX (2 units —
  the DSP's 21 cells re-derived and resolved), PROFILE-CONSISTENCY (2 dossiers),
  DOSSIER-SCHEMA (62 validated, 2 skipped by name), FACT-OWNERSHIP (23 kinds — the DSP's
  five rows landed; the two post-landing census arms prove same-unit pairing, 10/10).
- The DOSSIER's rows now read present/deferred with owners; the stale "lands with the
  model slice" wording for requirements and unit registration re-routed to
  `P3-BREADTH.6`. `.7` DONE 3/3; the frontier is `.6`, the BREADTH gate report.
- Bookkeeping: `.7` slice 1's checklist archived verbatim (the 64 KiB per-part held).

