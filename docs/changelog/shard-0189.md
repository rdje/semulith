# CHANGELOG shard — SEMULITH-P4-0010 … SEMULITH-P4-0010

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0010 (leaf P4-SYSTEM.2, slice f) — the base mirror executed (49/49), the mode-matrix corpus, the coverage rehearsal

- The rv64i guest corpus runs on the rv64gc engine: all 49 guests staged byte-identically
  (c-scope.c excluded — `scripts/build_c_guest.sh` hard-codes `-march=rv64i`; the rv64gc
  C-guest question is recorded for the flip) and executed by the scratch corpus runner
  (`target/p4-system-2/proof/corpus.rs`) — the declared MainMemory map, fault delivery on
  the pinned cause vocabulary, the per-step x-register-change comparison rule from the
  rv64i verify runner. The runner's trap-END discipline was a real bug it-fault-alias
  exposed: a delivered trap now aborts the step's remaining effects.
- 46 expectation files carry over byte-identically; fault-jal-mis, fault-jalr-mis and
  it-prio-jump were RE-DERIVED BY DESIGN — under D-IALIGN-16 their 2-mod-4 jump targets
  are legal (RVI-C 27.1), so the link write lands and no misaligned-fetch fault fires. A
  declared profile difference, measured and re-derived from the pinned chapters — never
  fitted to engine output (EVD-05).
- The mode matrix: 13 new guests with expectations derived BEFORE the run — the six
  zicsr forms' read/write/set/clear semantics; M-CSR legality in S and U (mtval = the
  faulting word); delivered breakpoints that resume; ecall causes 11/9/8 by mode and
  medeleg delegation to S with sret return (an M-mode ecall never delegates); mret mode
  pops with MPRV cleared when the target is below M and preserved at M; sret legal in
  M/S, illegal in U, and the TSR gate; wfi and the TW gate; sfence.vma and satp reads
  under TVM; counter reads under mcounteren then scounteren; stimecmp under TM then
  STCE; read-only CSR writes trapping while misa (WARL) ignores them; the mstatus
  all-ones WARL read-back (0x8000000A007E79AA, the state document's field table).
- Execution was the falsifier: it caught 14 stale auipc+addi vector deltas (labels
  assemble to no word — every vector target re-audited through the real assembler), two
  guest-design bugs (M-level CSR writes inline in S-mode in mm-mret and mm-ecall-modes —
  the drops moved before/inside the M handler), one hex-digit slip in the mstatus WARL
  constant and one no-change mis-derivation. Every mismatch was re-derived, never
  fitted. `corpus: 62 guest(s) PASS, 0 FAIL` (49 base + 13 mode matrix, deterministic
  re-run); the coverage rehearsal over the staged 65-form scope reads 65/65 (the base 52
  via the mirror, the 13 extension forms via mm-*, per-guest counts recorded). All
  untracked scratch — no gate arms this slice (the corpus's registry governor lands at
  the flip); `make gate` green (DERIVED-COUNTS unchanged at 408).
  Next: slice (g) — the interactions.sexp.

