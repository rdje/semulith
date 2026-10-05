# CHANGELOG shard — SEMULITH-P4-0008 … SEMULITH-P4-0008

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0008 (leaf P4-SYSTEM.2, slice d) — the generators parameterize to rv64gc, the privilege machinery lands, the scratch execution proof passes

- The two-profile shape, measured into existence: the tracked evaluator matches rv64i's
  byte-frozen generated `Sem` enum, so the slice-(b) operators' evaluation arms cannot
  compile tracked until the rv64gc definition module is tracked (the flip). The machinery
  doesn't wait: `crates/semulith-core/src/privilege.rs` (tracked, hand-authored) owns trap
  delivery (delegation selection, the xPIE/xIE/xPP stack, xepc/xcause/xtval, pc←xtvec),
  xret, the uniform CSR permission model (mode bits, read-only bits, counter-enables,
  TM/STCE, TVM) and WPRI/WARL/WLRL legalization — over a `PrivilegedHart` trait whose
  metadata vocabulary it owns; the generated rv64gc state module implements the trait with
  the descriptor's tables. The WARL seam closed: prose legalization became the structured
  `(legalize …)` mini-language, applied by the engine as a lookup. 11 machinery tests over
  a fixture hart.
- gen_definition's rv64gc branch lowers all 8 slice-(b) operators, emits pseudos as
  PSEUDOS metadata (the coverage mapping is slice (f)'s), and composes three separate
  `(extensions …)` forms correctly — its name list carried the THIRD copy of the
  dropped-form bug. gen_guests is directory-derived (the set is the directory; the run
  order is the tracked run-order.txt, cross-checked both directions; rv64i regenerates
  hash-only — the brief's "51-name list" measured 49). elf.rs's IALIGN is a parameter
  (the routed twin of slice a's assembler fix); the CLI passes the profile datum (32)
  explicitly. The dossier digest rotated on run-order.txt; the cascade re-derived
  (reports, the board's pin, the platform manifest, both books), and the PLATFORM-GEN
  stale-pin arm that assumed the digest's leading digit was fixed.
- Validation: the scratch execution proof — six guests assembled with the tracked
  assembler against the staged composition, run through the generated modules + the
  tracked machinery: the CSR disciplines (rs1=x0 never writes, the swap exact for
  rd==rs1), ecall delivered in M (cause 11, xepc=own address) and delegated to S (cause 9,
  the S handler, sret back), wfi legal-nop in M / illegal in U, sret illegal in U,
  sfence.vma under TVM, rdcycle gated then enabled — 26/26, catching two authoring defects
  on the way (an atomic CSR's write preserving everything; a wrong delegation bit). Both
  rv64i generated modules regenerate with only the embedded generator-hash lines changed.
  STATE-GEN 20/20, DEF-GEN 15/15, GUEST-GEN 10/10 (new arms RED-first); `make check` and
  `make gate` green (DERIVED-COUNTS 395→404). Next: slice (e) — the unit artifacts.

