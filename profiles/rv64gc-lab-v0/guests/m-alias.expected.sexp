;; m-alias.expected.sexp — the expected observations for `m-alias.s` (P4-SYSTEM.11,
;; the M corpus). EVD-05: every value below was derived from the pinned chapter (RVI-M
;; §11.1, Table 1's rows by name) with exact integers by the spec-side authoring model
;; BEFORE any engine run; the corpus runner falsifies against it.
;; Validate with
;;   python3 scripts/check_sexp_schema.py m-alias.expected.sexp schema/expectations.sexp

(expectations (program "m-alias.s") (entry "0x0000000080000000") (instructions 14)
  (step (n 0) (insn "addi x5, x0, 6") (writes (write (reg "x5") (value "0x0000000000000006")))
    (derivation "6.") (source "RVI-RV32I §1.1.4"))
  (step (n 1) (insn "mul x5, x5, x5") (writes (write (reg "x5") (value "0x0000000000000024")))
    (derivation "rd = rs1 = rs2: the reads see the PRE-instruction value - 6 x 6 = 0x0000000000000024.") (source "RVI-M §11.1.1"))
  (step (n 2) (insn "addi x6, x0, -9") (writes (write (reg "x6") (value "0xfffffffffffffff7")))
    (derivation "-9.") (source "RVI-RV32I §1.1.4"))
  (step (n 3) (insn "div x6, x6, x6") (writes (write (reg "x6") (value "0x0000000000000001")))
    (derivation "-9 / -9 into its own source: 0x0000000000000001.") (source "RVI-M §11.1.2"))
  (step (n 4) (insn "addi x7, x0, 13") (writes (write (reg "x7") (value "0x000000000000000d")))
    (derivation "13.") (source "RVI-RV32I §1.1.4"))
  (step (n 5) (insn "rem x7, x7, x7") (writes (write (reg "x7") (value "0x0000000000000000")))
    (derivation "13 rem 13 into its own source: 0x0000000000000000.") (source "RVI-M §11.1.2"))
  (step (n 6) (insn "mul x0, x5, x5") (writes)
    (derivation "an x0 destination: the product is discarded - no register changes.") (source "RVI-RV32I §1.1.1 (x0 is hardwired to 0); RVI-M §11.1.1"))
  (step (n 7) (insn "div x0, x5, x0") (writes)
    (derivation "a division by zero into x0: no trap, and nothing is written.") (source "RVI-M §11.1.2 (Table 1)"))
  (step (n 8) (insn "mulhu x0, x5, x5") (writes)
    (derivation "the high half into x0: discarded.") (source "RVI-M §11.1.1"))
  (step (n 9) (insn "divu x8, x8, x0") (writes (write (reg "x8") (value "0xffffffffffffffff")))
    (derivation "x8 (still 0) / 0, written over its own source: all bits set, 0xffffffffffffffff.") (source "RVI-M §11.1.2 (Table 1)"))
  (step (n 10) (insn "remu x9, x5, x9") (writes (write (reg "x9") (value "0x0000000000000024")))
    (derivation "36 rem x9 (still 0): division by zero - the dividend, 0x0000000000000024.") (source "RVI-M §11.1.2 (Table 1)"))
  (step (n 11) (insn "addi x10, x0, 10") (writes (write (reg "x10") (value "0x000000000000000a")))
    (derivation "a sentinel the zero product must replace.") (source "RVI-RV32I §1.1.4"))
  (step (n 12) (insn "mulh x10, x6, x7") (writes (write (reg "x10") (value "0x0000000000000000")))
    (derivation "1 x 0 - a zero product: 0x0000000000000000.") (source "RVI-M §11.1.1"))
  (step (n 13) (insn "divw x11, x5, x6") (writes (write (reg "x11") (value "0x0000000000000024")))
    (derivation "36 / 1 as words: 0x0000000000000024.") (source "RVI-M §11.1.2"))
)
