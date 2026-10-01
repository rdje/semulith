# CHANGELOG shard — SEMILITH-PS-0007 … SEMILITH-PS-0007

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMILITH-PS-0007 (leaf P2-SCALAR.4) — the interaction matrix: declared, exercised, gated

- The 21-cell fault × alias × boundary × event × progress × restart matrix is tracked
  data (`profiles/rv64i-lab-v0/interactions.sexp` over the new `schema/interactions.sexp`),
  declared first and then exercised; the 25th project doctrine `INTERACTION-MATRIX`
  re-derives the cells from the axes and refuses by name an omitted cell, an unresolved
  disposition, an orphan guest, or an unrecorded difference id — fired RED against the
  real corpus (`NO MATRIX`) before registration; self-test 12/0; mirrored per the
  registry rules.
- Eight new EVD-05 guests, every behavior probed before authoring: `it-prio-jump` /
  `it-prio-load` (misaligned AND unmapped → the misaligned cause wins, three-way),
  `it-fault-alias` (a misaligned load over its own base preserves the base),
  `it-fault-wrap-ld` / `it-fault-wrap-sd` (the address wraps mod 2^64 INTO the access
  fault, tval 0 — kept below 2^56 after the probes found sail's 56-bit tval masking,
  recorded as the new `DIFF-TVAL-PHYS-MASK`), `it-alias-bound` (self-aliased ops at
  boundary values), `it-progress-loop` (an unbounded loop under the budget contract, the
  x0 link discarded, `Stop::Budget`), `it-fencei` (the `DIFF-FENCEI-EXECUTED` pin).
- The comparator learned the EXPECTED divergence: `expect_divergence` on the expectation
  document (schema + dossier round-trip), `check_expected_divergence` in
  `compare_traces.py` (self-test 16/0 — an AGREE at the declared step is RED), and the
  smoke run's four-step protocol (own expectations; first divergence at exactly the
  declared step against each reference; sail vs spike agree over their full length; the
  difference id recorded). `cross_model` stays a comparison DISABLE.
- The restart axis is a mechanism, commit-gated: the new offline determinism suite runs
  every guest twice from `zeroed_at(entry)` and asserts identical traces and crossing
  logs, beside the smoke's reproduce leg.
- Validation: 166 verify suites (+8 guest suites, +1 determinism suite), 65 core;
  `make gate` green with 25 doctrines; smoke-bench 44 arms (40 clean guests);
  `EXERCISE-COVERAGE` 52/52 (self-test 7/0); live three-way: **40 guests, 492/492
  aligned steps** plus the one declared divergence, byte-identical reproduction.
- Reviewed ceiling expansion: `profiles/` 78 → 95 files / 402,967 B (registry 82 → 99
  files, 471,040 → 516,096 B; per-part 32,768 untouched — it bit on `references.sexp`,
  so the difference record was tightened rather than the ceiling moved); the 25th
  doctrine row also re-based the TOOLBOX.md / DOCTRINE_ENFORCEMENT.md caps to
  20 KiB / 28 KiB (the SEMILITH-PL-0001 precedent).

