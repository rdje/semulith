# CHANGELOG shard — SEMULITH-DR-0094 … SEMULITH-DR-0094

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-DR-0094 (leaf DSP-REVIEW.7) — the interface findings report: six findings routed, the tree closed 8/8

- The tree's capstone: every candidate interface change classified and costed, routed to
  `P3-BREADTH` with per-finding `ROUTING EVIDENCE` (manual locator + executable
  demonstration + the scalar-profile reproduction check — the method the tree
  pre-committed to before the first finding existed).
- Three CANNOT-EXPRESS findings, each refused by name and pinned by the `.6` synth
  suite: **F1** nonstandard widths (24/56/80-bit; rc 2) and **F3** multiple address
  spaces (rc 1) route to `P3-BREADTH.5`; **F4** the execute packet and **F5** the
  delayed visible writeback (both rc 1) route to `.1` **with the `.8` scope condition**
  — TI-family-shaped, so a scalar-DSP slice does not need them.
- Three NEEDS-A-CHANGE findings: **F2** register grouping with fill semantics (TI's
  40-bit odd:even zero-fill; the one finding without a measured refusal — recorded as
  its honest limit) and **F6** the per-profile state census reopenings (accumulator
  extensions, AMR/MODE1, sticky flags, loop state, the pending-writes window).
- Five measured non-findings classified OUT of interface work (the per-instruction SAT
  side effect, the saturate/round ordering, circular/bit-reversed addressing, the
  SPLOOP drain asymmetry, MFENCE — semantics data + census state, not interface shape).
- The scalar controls measured: the real 64-bit state document generates rc 0,
  `DEF-GEN: ok`, the synth suite 4/0 — **no finding reproduces on `rv64i-lab-v0`**;
  nothing routed belongs to `P2-SCALAR`. Evidence:
  `docs/tasks/artifacts/dsp-review/2026-10-01-interface-findings.md`.

