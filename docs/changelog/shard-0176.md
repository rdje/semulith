# CHANGELOG shard — SEMULITH-P4-0002 … SEMULITH-P4-0002

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0002 (leaf P4-SYSTEM.1) — the profile resolved: rv64gc-lab-v0, every element source-located; the profile-resolution vehicle route

- The Linux-capable profile is selected and recorded as data: `profiles/rv64gc-lab-v0/`
  carries the resolution — RV64I + M/A/F/D/C + Zicntr + Zicsr + Zifencei (+ Sstc
  privileged), M/S/U modes, Sv39, IALIGN 16 with C, one hart, the 33-CSR committed
  minimum, LP64D ABI, SBI 2.0 as the P6 firmware contract. 18 decisions, each mirrored
  verbatim into a requirement and a contract obligation (`rv64gc-lab-env-v0` v0), every
  element with its source locator. The pinned v20260120 snapshot was measured to CARRY
  the privileged chapters (24 priv/ + 46 unpriv/ pages, 21/21 pins re-hashed against
  the tracked SHA256SUMS); the 2026-09-27 census's "privileged volume absent" phrasing
  is superseded. The closure is measured (G = IMAFDZicsr_Zifencei; D⇒F; F⇒Zicsr;
  C⇒Zca+Zcd at RV64). FP is in the profile; its model evidence is gated on `.7`'s
  backend qualification. The unit is deliberately unregistered.
- The machinery gained the `profile-resolution` vehicle route by declaration (the .2
  discipline): EXTRACTION / EXERCISE-COVERAGE / INTERACTION-MATRIX honor it, a
  definition-pipeline document beside the declaration is RED (self-tests 11/11, 21/21,
  15/15). check_citations.py learned subdirectory `file` fields and named non-snapshot
  skips; gen_platform.py's ISA derivation fixed to the canonical order. FACT-OWNERSHIP
  +4 rows (61 kinds), the obligations fixture re-pinned to six units.
- Validation: `make gate` green (DERIVED-COUNTS 376→383 arms re-derived);
  check_citations 52/52 for both RISC-V units offline; RECORD-SCHEMA 18 record files.

