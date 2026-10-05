# DEV_NOTES shard — _(2026-10-03)_ … _(2026-10-03)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-03)_ — execution is the falsifier: 14 stale deltas, two design bugs, and the value of the byte-probe (P4-SYSTEM.2 slice f)

Execution of the `.2` brief's checkpoint (f) measured:

- **The runner's comparison rule re-derives expectations for you.** The corpus runner
  records per-step x-register CHANGES (diff before/after the effect), so an instruction
  that writes a register its current value is NO observation — `csrrw x2, mscratch, x1`
  reading the reset mscratch (0) into the reset x2 (0) leaves an empty writes row. Three
  of my hand-derived rows (and one in mm-stimecmp, where x10 already held the mepc
  value) assumed a write that the rule correctly refuses to see. The derivation
  discipline held: every mismatch was re-derived from the semantics, never fitted.
- **Labels assemble to no word — audit every auipc+addi pair through the real
  assembler.** Fourteen mtvec/mepc/sepc vector deltas across eight mode-matrix guests
  were stale because they had been computed against a line count that charged label
  lines four bytes; the trap vectors landed in `.word 0` pad. The audit that ended the
  class: assemble each guest and print every `auipc xN, 0` + `addi xN, xN, d` pair's
  target address with the instruction it names — the target must be the intended
  handler/cell's first instruction. mm-ebreak's variant was a pad-count slip (mtvec
  pointing three words into the handler's prologue). All fourteen fixed and re-audited
  green before the first corpus run.
- **Two guest-design bugs only execution could catch.** mm-mret programmed mtvec and
  mm-ecall-modes cleared mstatus INLINE after dropping to S-mode — M-level CSRs,
  illegal in S (RVP-CSR §2.1), so each guest trapped into an unprogrammed vector and
  spun writing nothing (the failure signature: every step from the drop onward
  `wrote []`). Fixes: mm-mret was re-laid-out to program mtvec before any drop;
  mm-ecall-modes' handler became stage-aware so the second mode drop happens in M,
  reached by an S-mode ecall. The rule now encoded in the corpus: M-level CSR writes
  happen before a mode drop or inside the M handler, never inline in S/U.
- **One constant, one digit.** The mstatus all-ones WARL read-back is
  0x8000000A007E79AA (SD from FS=11, UXL/SXL held at 2, the writable fields set) — my
  first transcription dropped a zero nibble and the runner's `wrote [(7, …)]` named
  the correct value, which matched the state document's field table on re-derivation.
- **The byte-probe IS the mirror's claim.** 49 `.s` files byte-identical, 46/49
  expectations byte-identical, and the three re-derived ones named (fault-jal-mis,
  fault-jalr-mis, it-prio-jump) — the D-IALIGN-16 divergence is a declared profile
  difference (RVI-C 27.1: 2-mod-4 targets are legal with C), re-derived from the
  pinned chapters with provenance comments, not a soundness contradiction and never
  an edit-to-match.
- **Validation:** `corpus: 62 guest(s) PASS, 0 FAIL` (deterministic re-run); the
  coverage rehearsal applies EXERCISE-COVERAGE's own numerator rule (the first token
  of each step's insn text) to the staged tree: denominator 65 consistent with
  count_total, exercised 65/65, the base 52 via the mirror and the 13 extension forms
  via the mm-* guests. `make gate` green with DERIVED-COUNTS unchanged at 408 — the
  corpus is untracked scratch, so no new arms; the guests' registry governor lands at
  the flip. Promotion: declined — the auipc-delta audit and the M-level-before-drop
  rule are recorded in the leaf's checklist and encoded in the guests themselves.

