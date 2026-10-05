;; fencei-reserved.expected.sexp — the expected observations for `fencei-reserved.s` (P4-SYSTEM.5
;; slice b, the interrupts corpus). EVD-05: every value below was derived from the pinned
;; chapters and the .5 brief's declared delivery rule by the spec-side authoring model
;; BEFORE any engine run; the corpus runner falsifies against it.
;; Validate with
;;   python3 scripts/check_sexp_schema.py fencei-reserved.expected.sexp schema/expectations.sexp

(expectations (program "fencei-reserved.s") (entry "0x0000000080000000") (instructions 2)
  (never_written "x28")
  (never_written "x29")
  (step (n 0) (insn ".word 0x0011118F") (writes)
    (derivation "fence.i with imm12=1, rs1=x2, rd=x3 — decoded-and-IGNORED (the mask covers funct3 and the opcode only): the word retires as the declared nop, never raises.") (source "RVI-ZIFENCEI §4.1; the .6 brief's decision 5"))
  (step (n 1) (insn "addi  x9, x0, 42") (writes (write (reg "x9") (value "0x000000000000002a")))
    (derivation "the continuation marker: execution passed the reserved-fields word — proof the fields were ignored, never legalization-rejected.") (source "RVI-RV32I §1.1.4 #|end"))
)
