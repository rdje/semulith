# CHANGELOG shard — SEMULITH-BR-0013 … SEMULITH-BR-0013

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-BR-0013 (leaf P3-BREADTH.1) — the dsp56300-lab-v0 state census; the dump is complete

- The SEM-08 hidden-state census re-ran for the exercised DSP profile (F6's per-profile
  leg): 14 candidates answered with locators, never by silence — the record is
  `docs/tasks/artifacts/p3-breadth/2026-10-01-dsp56300-state-census.md`.
- PRESENT and declared: the A2/B2 sign-extended extension readout and A1/B1 raw reads
  (`.4`'s pins harvested), M0–M7 bounded at reset by typed stops, sticky L/S (S has no
  writer in subset v0), the DO loop's stacked levels, the observable stale popped stack
  slots. ABSENT: REP working state beyond the declared LC (restored before the
  instruction retires), the F5 pending-writes window (scalar issue), reservation/FP/vector
  state (none exist in the family), and the interrupt/mode/stack-extension state (named
  exclusions, each reopening its census row).
- Consequence: for subset v0 under its named exclusions, the canonical end-state dump is
  the COMPLETE architectural state — surface completeness argued (stack slot 0 unwritable,
  P-low constant, the harness window excluded by the harness's own contract) and measured
  (the 6/6 agreement re-run this leg). The record is `.5`'s measured input for the
  `state.sexp` cases; the DOSSIER's deferral row names it. `P3-BREADTH.1` stays
  slice-gated (F6 refires per profile; F2/F4/F5 stay TI/VLIW-conditional); the frontier
  moves to `.5`.

