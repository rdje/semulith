# CHANGELOG shard — SEMULITH-P4-0013 … SEMULITH-P4-0013

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P4-0013 (leaf P4-SYSTEM.2, slice h part 2) — the Sail privileged matched experiment (11/12 AGREE, the TW cell named, mm-counters not matchable); the leaf closes

- The Sail privileged matched experiment (decision 8), attempted and honestly
  recorded. The matched override lands tracked at
  `profiles/rv64gc-lab-v0/reference/sail-rv64gc-lab-v0.override.sexp` (the .sexp is
  the truth, the JSON derived by `materialize_sail_override`): privileged ISA 1.13,
  misa held (WARL), FS four-state / VS off, the declared selection (M/A/F/D/C,
  Zicsr, Zifencei, Sstc, Sv39, S, U) minus Zicntr, no devices, no PMP, WFI a nop
  except in U, medeleg 0x3FF — Sail's own validator confirming the corpus's claims
  (cause 10 is reserved with H off; bit 11, ecall from M, is undelegatable by law;
  the matched mask derived by bisection).
- The evidence chain closes end to end: the tracked .sexp derives the JSON, Sail
  0.14 (git 29e6158) runs the mode-matrix guests under it, and **11 of 12 AGREE
  step-for-step against the specification-derived expectations** — the zicsr rw
  semantics, per-mode CSR legality with mtval = the word, delivered breakpoints and
  resumes, ecall causes 11/9/8 and medeleg delegation (the M-ecall never
  delegating), mret's MPRV clear-below-M / preserve-at-M, the mstatus all-ones
  WARL read-back bit-exact (`0x8000000A007E79AA`), stimecmp's TM then STCE gating,
  the TVM gates, sret and TSR. The comparison normalizes Sail's trace to the
  corpus's own change-observation rule — the reference's execution, the
  specification's values.
- The two honest boundaries, each with its evidence: mm-wfi's TW=1-in-S legality
  cell is a NAMED DIVERGENCE — Sail 0.14 does not implement mstatus.TW's effect on
  WFI legality (the wfi retires as a nop with `wfi_is_nop=true`, waits forever
  with it false; the bit is provably writable — mm-readonly's all-ones read-back
  AGREEs bit-exact, bit 21 included; no config knob exists). Our expectation
  stands on RVP-INSNS; the finding is routed to P4-SYSTEM.5 (the wfi/wake leaf)
  with the measurement recorded. mm-counters is NOT MATCHABLE — Sail requires a
  CLINT time source when Zicntr is enabled and D-PLATFORM declares no devices;
  the counter rate is the environment's own declaration (our laboratory holds
  zero). Spike stayed platform-conflicted, no attempt.
- The dossier-format owners learned the override's new keys:
  `schema/override.sexp` (optional fields — rv64i's override re-validated) and
  `dossier_sexp`'s mapping both directions (self-test 13→14; the round-trip
  field-for-field exact). `make check` and `make gate` fully green
  (DERIVED-COUNTS 419 unchanged).
- **Leaf P4-SYSTEM.2 is done** — the acceptance criterion "the same instruction's
  behaviour is tested in each supported mode" is the mode matrix itself: 13
  guests, every cell a mode crossing, falsified by the tracked engine (62/62) and
  differentially confirmed (11 full AGREE + 1 partial). Frontier: `.3` — Sv39
  translation and protection.

