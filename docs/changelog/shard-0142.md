# CHANGELOG shard — SEMULITH-BR-0011 … SEMULITH-BR-0011

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-BR-0011 (leaf P3-BREADTH.4) — the model crate stands; the first differential case AGREEs

- `crates/semulith-dsp56300` (lib + runner): the full canonical register set + 16-level
  hardware stack + three bounded memory windows (`machine.rs` — named per the
  FACT-OWNERSHIP generated-mirror convention), FM-cited decode for the nine demo-path
  forms, semantics with the FM Table 5-1 CCR rules and the DO loop machinery, the
  canonical-dump emitter (NO `cyc` line — timing is never emitted), the `.lod`/`.meta`
  dialects with fill headers refused by name; every out-of-subset word is a typed
  `ModelStop`.
- `scripts/compare_dumps.py` — the checkpoint-level comparator (field-exact; a missing
  key is a mismatch; `cyc` skipped by recorded rule; 4-arm self-test) and
  `scripts/run_dsp56300_smoke.py` — the campaign driver (not a commit gate; refuses
  unbuilt references).
- **The micro guest AGREES over 53 fields** (registers + X/Y deviations + stack slots) —
  the Semulith dump is byte-identical to the reference's. The 10 unit tests carry
  manual-derived expectations (EVD-05); `make check` + `make gate` green.
- Owned findings (§15): the FM's U-bit equation is an extraction INVERSION of its own
  prose (the reference's `sr c00310` is the arbiter — XNOR, recorded in `exec.rs`).

