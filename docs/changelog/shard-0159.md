# CHANGELOG shard — SEMULITH-P5-0005 … SEMULITH-P5-0005

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P5-0005 (leaf P5-BOARD.1) — the platform specified: `netboard-lab-v0` pins versions, not names; the 16550 label measured false and corrected

- The first board's canonical definition lands: [`profiles/netboard-lab-v0/board.sexp`](profiles/netboard-lab-v0/board.sexp)
  under the new [`schema/board.sexp`](schema/board.sexp) — the first non-processor
  source-of-truth schema (DOSSIER-SCHEMA pairs them by basename) — narrated by
  [`profiles/netboard-lab-v0/DOSSIER.md`](profiles/netboard-lab-v0/DOSSIER.md).
- Every pin is a version, never a name (OWN-05, the leaf's acceptance): the processor by
  unit id + version `0` + the GATE-REPORT-gated dossier content digest; each device by its
  datasheet's material id + revision + sha256. The memory map (2 GiB RAM at the harness's
  existing base, the UART at the sourced FU540 instance address, the NIC in the datasheet's
  256-byte direct-register span), cold-only reset, and the serial console are data.
- Timers and interrupt controllers are **absent by contract** — declared as data with their
  reasons and the obligations they satisfy (`OB-ENV-VIRTUAL-TIME`, `OB-ENV-EVENT-DELIVERY`);
  a CLINT/PLIC would be a composition rejection, not a feature. `satisfies` fields pre-wire
  `.4`'s composition verdict. Both devices' interrupt lines unconnected-and-declared;
  drivers poll. The NIC backend is recorded-trace replay RX / recording-sink TX.
- **Measured defect, found and fixed in execution:** the design brief's "16550-compatible
  UART" label is false against the pinned source — zero occurrences of "16550" in
  FU540-C000 v1p5 (`pdftotext` census); §13 documents the SiFive UART. The source pin was
  the intent: the board adopts the SiFive UART, `materials/catalog.sexp`'s supplies text is
  corrected, and the correction is recorded as `D-BOARD-UART-KIND`.
- Scope routing: board-unit registration (`materials/units.sexp`, the `kind` edit, the
  per-unit book) lands with `.3` — registration day carries the UNIT-BOOKS /
  MATERIALS-BILL / generator consequences, which are not a specification's to bear.
- The `profiles/` family's third unit directory: the bound re-derived to 3× by the standing
  arithmetic ([`docs/decisions/decision_profiles-family-three-units.md`](docs/decisions/decision_profiles-family-three-units.md));
  the board-definition fact kind registered in `doctrine/fact_ownership.tsv`.
- Validation: both schema validations ok; every pin re-derived from its source artifact;
  `make gate` green; `mdbook build docs/book` rc 0.

