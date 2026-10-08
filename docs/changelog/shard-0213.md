# CHANGELOG shard — SEMULITH-P4-0035 … SEMULITH-P4-0035

> Sharded from `CHANGELOG.md` under its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0035 (leaf P4-SYSTEM.6, slice a) — the rv_zifencei re-pin, the one-form fragment, zifencei.sem.sexp, the zero-operand assembler acceptance

- The re-pin: `rv_zifencei` through the tracked `extensions/` fetch route — 73
  bytes, exactly one row (`fence.i imm12 rs1 14..12=1 rd 6..2=0x03 1..0=3`,
  sha256 be2d8f72…), recorded in references.sexp with the supplies amendment; a
  scripted fresh re-fetch byte-identical. The fetch leg gains the named
  zifencei exclusion (the M/A pattern — pinned for the fragment, not the scope,
  until slice (b)'s bind flips it): both profiles' `--verify-only` green,
  87==87 and 52==52, "owned fragments agree with the pinned upstream".
- The FRAGMENTS entry generates `definitions/riscv/zifencei.sexp` — owns NO
  operand fields (imm12/rs1/rd are the base's), requires rv64i, funct3=1
  against fence's 0; the six existing fragments re-derive byte-identical.
  `zifencei.sem.sexp` lands hand-written with `(effect (nop))`: the three
  normative sentences, the coherent/uncached-RAM latitude (a re-read-per-fetch
  machine has nothing to flush) and the shall-ignore rule, every sentence
  re-located in the pinned chapter (Version 2.0); citations resolve offline
  (RVI-ZIFENCEI §4.1 ×1; corpus 6 files / 8 resolutions).
- One brief claim measured FALSE as written: decision 1's "no assembler
  shapes" — the row's operand list refused the bare standard-software spelling,
  so the zero-operand acceptance lands as a named, cited special case in
  `riscv_asm.py` (the A-suffix precedent's shape): bare `fence.i` → 0x0000100f,
  the full spelling unchanged, 3 named RED refusals, the spike-dasm round-trip
  exact including the shall-ignore word 0x0011118f. The OTHER no-change claims
  measured TRUE: no Sem variant, no generator change — gen_definition emits
  fence.i with mask 0x0000707f (funct3+opcode only — the shall-ignore decode)
  over the existing `Sem::Nop`, rustc rc=0 over both trial compositions.
- check_encoding_disjoint COMPOSEs base+zifencei (53) and the profile's set
  +zifencei (85+3); check_semantics pair 1/1 and both --compose green; all 99
  guests re-assemble byte-identical. The slot STAYS declared, the census STAYS
  87, no corpus, no Rust. `make check` rc=0, `make gate` green (DERIVED-COUNTS
  430 unchanged).
