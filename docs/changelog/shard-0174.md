# CHANGELOG shard — SEMULITH-P5-0019 … SEMULITH-P5-0019

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P5-0019 (leaf P5-BOARD.6) — the platform capability manifest: derived, schema-gated, drift-gated by PLATFORM-GEN; the dossier pin load-bearing; endianness a data owner

- The board's read-only export for a compatibility checker landed:
  `profiles/netboard-lab-v0/platform.sexp` (export version 0) — OWN-06: derived, never
  handwritten, so a consumer imports facts rather than becoming a second hardware
  implementation. One generator (`scripts/gen_platform.py`, boards discovered by
  declaration) derives it from three fingerprinted canonical inputs — the board
  definition, the pinned processor's profile dossier, the composed contract
  obligations — through the one board reader, the one dossier mapping, the one record
  mapping. Schema-gated by `schema/platform.sexp`; drift-gated by the 34th project
  doctrine PLATFORM-GEN (`scripts/check_platform_gen.sh`, self-test 11/11, every RED
  arm asserting its reason on copies of the real board).
- The document mirrors `docs/ARCHOGEN_INTEGRATION.md` §3's six bullets: processor/ISA
  facts (endianness included — prose-only until this leaf gave it a data owner in the
  CPU dossier), the resolved memory map, the device pins, the declared absences, the
  composition dispositions, the newly declared boot contract and test-control surface
  (`boot`/`test-control` blocks in board.sexp), the time/event/ordering facts derived
  from the composed obligations' parameters, explicit per-facility `presence` markers,
  and the limitations and non-claims as data — including the recorded boundary that
  archogen is actively developed and has no functional eADL interface today, so the
  export is validated by derivation freshness, schema conformance and §3 coverage,
  never by archogen acceptance.
- The board's `dossier-sha256` pin is load-bearing now: measured display-only (rendered,
  re-derived by nothing), it is verified against the live dossier at every derivation
  (`gate_report.dossier_digest`, factored out of `build_cpulab` — byte-identical
  measured). The leaf's own endianness edit exercised the cascade for real: GC-REPORT
  regenerated, the pin re-pinned `1879ba18…` → `95ebca2f…`.
- Measured and fixed at root: a planned edit to ARCHOGEN_INTEGRATION.md was reverted —
  the file is a frozen-in-place delivered input and DELIVERY-PROVENANCE fired as
  designed; the announcement lives in the books and the DOSSIER. TOOLBOX.md's missing
  `.3`/`.4` board-tooling rows were backfilled. FACT-OWNERSHIP +3 rows (57 kinds) with
  the corpus census's three platform pairs; REGEN_GOVERNORS grew per the `.12` ruling;
  DERIVED-COUNTS re-derived (34 doctrines, 376 arms). The board book gained the
  manifest chapter (the generated file included — one owner, two readers).
- Validation: `gen_platform.py --check` byte-exact; PLATFORM-GEN green (self-test
  11/11); schema validation on all touched documents incl. the schema fixpoint;
  BOARD-GEN / BOARD-VERDICT / GATE-REPORT / MATERIALS-BILL / UNIT-BOOKS green;
  `make gate` → all doctrines green; both books build; the book index regenerated.

