;; mm-csr-rw.expected.sexp — the expected observations for `mm-csr-rw.s` (P4-SYSTEM.2
;; slice f, the mode-matrix corpus). EVD-05: every value below was derived from the
;; pinned chapters BEFORE any engine run; the corpus runner falsifies against it.
;; Validate with
;;   python3 scripts/check_sexp_schema.py mm-csr-rw.expected.sexp schema/expectations.sexp

(expectations (program "mm-csr-rw.s") (entry "0x0000000080000000") (instructions 9)
  (step (n 0) (insn "addi x1, x0, 42") (writes (write (reg "x1") (value "0x000000000000002a")))
    (derivation "an immediate load, so the CSR value is observable.") (source "RVI-RV32I §1.1.4"))
  (step (n 1) (insn "csrrw x2, mscratch, x1") (writes)
    (derivation "x2 receives the OLD mscratch, which resets to 0 — and x2 already holds 0, so no register change is observed; mscratch becomes 42.") (source "RVI-ZICSR §5.1.1"))
  (step (n 2) (insn "csrrs x3, mscratch, x0") (writes (write (reg "x3") (value "0x000000000000002a")))
    (derivation "csrrs with rs1=x0 reads and does NOT write the CSR: x3 observes 42.") (source "RVI-ZICSR §5.1.1"))
  (step (n 3) (insn "csrrc x4, mscratch, x1") (writes (write (reg "x4") (value "0x000000000000002a")))
    (derivation "x4 receives the old value 42; the clear makes mscratch = 42 & ~42 = 0.") (source "RVI-ZICSR §5.1.1"))
  (step (n 4) (insn "csrrwi x5, mscratch, 7") (writes)
    (derivation "x5 receives the old value 0 — no change observed; mscratch becomes the immediate 7.") (source "RVI-ZICSR §5.1.1"))
  (step (n 5) (insn "csrrsi x6, mscratch, 1") (writes (write (reg "x6") (value "0x0000000000000007")))
    (derivation "x6 receives 7; the set-bits write makes mscratch = 7 | 1 = 7.") (source "RVI-ZICSR §5.1.1"))
  (step (n 6) (insn "csrrci x7, mscratch, 1") (writes (write (reg "x7") (value "0x0000000000000007")))
    (derivation "x7 receives 7; the clear-bits write makes mscratch = 7 & ~1 = 6.") (source "RVI-ZICSR §5.1.1"))
  (step (n 7) (insn "csrrsi x8, mscratch, 0") (writes (write (reg "x8") (value "0x0000000000000006")))
    (derivation "uimm=0: no CSR write; x8 observes 6.") (source "RVI-ZICSR §5.1.1"))
  (step (n 8) (insn "csrrs x9, mscratch, x0") (writes (write (reg "x9") (value "0x0000000000000006")))
    (derivation "the read-back: mscratch holds 6.") (source "RVI-ZICSR §5.1.1")))
