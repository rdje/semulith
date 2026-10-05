# CHANGELOG shard — SEMULITH-P4-0004 … SEMULITH-AC-0057

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0004 (leaf P4-SYSTEM.2, slice a) — the Zicsr/Zicntr/privileged-system fragments from the re-pinned riscv-opcodes; the csr operand field; IALIGN as profile data

- The upstream census (riscv-opcodes master, the fetch script's own route) measured what
  the design brief delegated: the six Zicsr instructions are real rows in
  `extensions/rv_zicsr`; mret/wfi live in `rv_system`, sret/sfence.vma in `rv_s`; and
  Zicntr's rdcycle/rdtime/rdinstret exist ONLY as `$pseudo_op` rows of csrrs — Zicntr adds
  no encodings. Upstream moved every table from the repository root to `extensions/`; the
  moved rv_i/rv64_i/rv_m/rv64_m hash byte-identical to the rv64i pins, so the fetch route's
  new `extensions/` mapping keeps both profiles' `--verify-only` green (a scripted fresh
  re-fetch of rv_s came back byte-identical).
- The re-pin landed as `profiles/rv64gc-lab-v0/references.sexp` (rv_zicsr, rv_zicntr,
  rv_system, rv_s, csrs.csv + the shared arg_lut.csv — sha256+bytes each; rv64i's ledger
  untouched; the pinned arg_lut already carried csr (31..20) and zimm5 (19..15), so no
  arg_lut re-pin). Three new generated fragments: `definitions/riscv/zicsr.sexp` (owns the
  csr/zimm5 fields), `zicntr.sexp` (the counter reads as `(pseudo …)` — a new fragment
  construct for assembler spellings that add nothing to the encoding space, decided by the
  disjointness gate under a specialization rule; requires rv64i AND zicsr, the pinned rows'
  own `rv_zicsr::csrrs`), `system.sexp` (the D-PRIV-INSNS four). rv64i.sexp/m.sexp
  re-derive byte-identical; the 62-instruction 4-fragment trial union is collision-free.
- The assembler gained the csr/zimm5 operand fields (positions always derived from the
  pinned arg_lut.csv), csr names resolved through the pinned csrs.csv, pseudo-op support
  through the canonical path, and profile-derived IALIGN (rv64i 32 / rv64gc 16 — the
  line-486 hard-code retired). All 13 new forms assemble and round-trip through spike-dasm
  exactly. Measured in execution, fixed at root: `resolve_composition` silently dropped
  every `(extensions …)` form after the first (latent since MODEL-COMPOSE.2), the
  disjointness checker's `DUPLICATE NAME(S)` was advisory-only, and the assembler's label
  pass ate csr names. No Rust surface touched.
- Validation: check_encoding_disjoint self-test 12/12 (the pseudo and dupes arms RED
  first), UNIT-COMPOSITION 9/9, EXERCISE-COVERAGE 21/21, the focused gates green,
  fetch_references `--verify-only` green for BOTH profiles, `make gate` green
  (DERIVED-COUNTS 383→384 self-test arms re-derived).

## SEMULITH-AC-0057 (tree ARTIFACT-CLEANUP) — the 2026-10-03 §8 run: 0 incremental caches present to delete; the reference evidence logs kept

- The ~24 h trigger fired (the `2026-10-02` record was a day old). The census found
  **zero** cargo incremental `.bin` caches — none accumulated since the previous run —
  and zero stray `.bin`/`.log` in `target/release`/`target/debug/deps`. 62
  `target/refs/*.log` (2.2 M, evidence trails of the last reference run) and the 7
  cargo-home crate fixtures (inputs) kept by standing policy. `docs/ARTIFACT_CLEANUP.md`
  overwritten with the dated one-line record; `target` 3.9 G, `.app-data` 1.4 G,
  unchanged.

