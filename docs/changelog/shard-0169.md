# CHANGELOG shard — SEMULITH-P5-0013 … SEMULITH-P5-0013

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P5-0013 (leaf P5-BOARD.3) — the generated maps: one generator, seven artifacts, the BOARD-GEN freshness gate

- `scripts/gen_board.py` discovers boards by declaration (`profiles/*/board.sexp`) and
  generates everything downstream of the canonical definition (OWN-05): the composition
  manifest (the part list derived from the pins, never restated), the four composed
  catalogues (99 requirements, 107 obligations, 5 sources, the rv64i encoding —
  materialized by the factorized `compose_units.compose_resolved`, the ONE code path
  the verdicts consume), `hardware.sexp` under the new `schema/hardware.sexp`, and
  `map.md`. Every artifact carries the OWN-03 fingerprint header.
- The **BOARD-GEN** doctrine (`scripts/check_board_gen.sh`) is the freshness proof
  `compose_units.py` deferred to the first tracked board: `--check` re-derives all
  seven artifacts and refuses DRIFT by name (self-test 9/9, every RED arm asserting
  the reason); the generator refuses an inconsistent definition by name (region
  overlap, MMIO window without device, executable MMIO, ghost console).
- The census found exactly ONE handwritten duplicate map (the DOSSIER's table) —
  replaced by the generated map: the DOSSIER links it, the board book includes it
  (one owner, two readers, the include verified in the built HTML). The DOSSIER's
  stale post-`.11` status rows (the brief's logged defect) fixed in the same pass.
- FACT-OWNERSHIP gained 8 rows (54 kinds; the two measured corpus pairs registered,
  never weakened) and the fixture re-pinned to five units; DERIVED-COUNTS fired as
  designed (31→32 doctrines, 345→354 arms, re-derived in `LIVE_STATUS.md`).
- Measured and recorded at root: the brief's register-surface containment check is
  not implementable — the device dossiers carry register offsets in prose, never as
  machine-readable data; the generator's refusals are scoped to what board.sexp
  proves, and machine-readable offsets arrive with the device models. And the
  `profiles/` per-part bound bit a second time (the first DERIVED member class:
  the composed `contract-obligations.sexp`, 104,372 B) — the standing reviewed-raise
  rule applied (`decision_profiles-family-composed-units`: 64 → 128 KiB at 0.80×,
  aggregates unmoved).
- Validation: BOARD-GEN ok; RECORD-SCHEMA 16 record files; FACT-OWNERSHIP 54 kinds;
  UNIT-BOOKS 5/5; `make gate` → all doctrines green; `mdbook build` rc 0;
  `gen_book_index.py --check` rc 0. No Rust surface touched. The composed catalogues
  on disk are `P5-BOARD.4`'s pre-staged input.

