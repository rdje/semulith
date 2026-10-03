# CHANGELOG shard — SEMULITH-AC-0055 … SEMULITH-BR-0001

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-AC-0055 (tree ARTIFACT-CLEANUP) — the 2026-10-01 §8 cleanup: 96 incremental caches, 248 MB

- Time-triggered run (the `2026-09-30` run was a full day old). Pre-delete census: 96
  cargo incremental `.bin` files / 248 MB, all under `*/incremental/*` (48
  `target/debug`, 18 x86_64, 12 wasm32, 9+9 the two miri profiles); 0 stray
  `.bin`/`.log` in the enumerated locations; no `target/refs/*.log` present; the 7
  cargo-home crate-source fixtures kept by policy (inputs, not artifacts).
- Post-delete re-census: 0 incremental `.bin`; `target` 3.7 G → 3.5 G, `.app-data`
  unchanged at 1.4 G. `docs/ARTIFACT_CLEANUP.md` overwritten with the one-line record.

## SEMULITH-BR-0005 (leaf P3-BREADTH.1) — F2 measured executably; the unconditional-change set is empty; `.1` slice-gates on `.3`

- Finding F2 (register grouping with fill semantics, TI C64x §2.2) was the one
  `DSP-REVIEW.7` finding classified from a document's shape, not a measured refusal.
  The report named the honest route and `.1` took it: synth probe 5
  (`state-groups.sexp` — the real scalar state document plus one synthetic
  `register_groups` form) refuses by name, `undeclared field "register_groups"`, rc 1;
  the synth suite is now 5/5.
- The findings' required-**unconditional** implementation set measured **empty**: F4/F5
  are conditional on a VLIW slice, F2's implementation idles unless the slice is TI
  (implementing grouping with no exercised target would be the speculative generality
  this tree exists to refuse), F6 fires per new profile. `.1` is `slice-gated` — not
  closed: `.3` naming a VLIW or TI slice reopens it by name. Frontier moves to `.2`.
- Scalar regression evidence preserved and re-run (`EVD-07`; no code changed):
  `make check` 180/180 + fmt + clippy clean; gen_state rc 0; DEF-GEN ok; the G1 gate
  verdict `passed` re-derived.

## SEMULITH-BR-0001 (leaf P3-BREADTH.1) — the composable-DSP design discussion, recorded for resumption

- The director's `[DBINP]` exchange recorded in the `P3-BREADTH` tree's new Design
  Discussions section: a DSP as composition — the fixed skeleton of problems, the measured
  per-axis menu of vendor-citable choices, the composition rules that make a selection
  coherent, and the ISA as the fabric moving data between the chosen parts ("lego into a
  coherent, functional whole"). Resume point for the hypothetical high-end DSP as this
  tree's ultimate stress fixture; the permanent bounds carried (citable per-axis; never
  evidence about a real DSP).
- The tree's blockers cleared on record: `DSP-REVIEW` closed 8/8 (`SEMULITH-DR-0094`).

