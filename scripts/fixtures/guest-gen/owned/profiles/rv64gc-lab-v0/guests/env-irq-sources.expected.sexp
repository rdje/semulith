;; env-irq-sources.expected.sexp — spec-side observations for `env-irq-sources.s`.
;; Author: scripts/derive_rv64gc_expectations.py; explicit-budget parcel route (C-capable).
;; EVD-05: values derive from independent spec-side rules and the declared
;; laboratory policies; each step names its derivation and source.
;; This derivation makes no processor conformance or original-capture claim.
;; Validate with
;;   python3 scripts/check_sexp_schema.py env-irq-sources.expected.sexp schema/expectations.sexp

(expectations (program "env-irq-sources.s") (entry "0x0000000080000000") (instructions 13) (fetches 26)
  (never_written "x28")
  (never_written "x29")
  (step (n 0) (insn "lui x31, 0x80000") (writes (write (reg "x31") (value "0xffffffff80000000")))
    (derivation "the upper 20 bits land sign-extended in rd.") (source "RVI-RV64I §3.1.2.1"))
  (step (n 1) (insn "csrrs x0, menvcfg, x31") (writes)
    (derivation "atomic read and set bits; rs1=x0 does not write the CSR.") (source "RVI-ZICSR §5.1.1"))
  (step (n 2) (insn "addi x6, x0, 1") (writes (write (reg "x6") (value "0x0000000000000001")))
    (derivation "the 12-bit immediate adds into rd.") (source "RVI-RV32I §1.1.4"))
  (step (n 3) (insn "addi x8, x0, 1") (writes (write (reg "x8") (value "0x0000000000000001")))
    (derivation "the 12-bit immediate adds into rd.") (source "RVI-RV32I §1.1.4"))
  (step (n 4) (insn "addi x5, x0, -1") (writes (write (reg "x5") (value "0xffffffffffffffff")))
    (derivation "the 12-bit immediate adds into rd.") (source "RVI-RV32I §1.1.4"))
  (step (n 5) (insn "csrrw x0, stimecmp, x5") (writes)
    (derivation "atomic read/write CSR; rd=x0 discards the old value.") (source "RVI-ZICSR §5.1.1"))
  (step (n 6) (insn "csrrs x6, mip, x0") (writes (write (reg "x6") (value "0x0000000000000000")))
    (derivation "atomic read and set bits; rs1=x0 does not write the CSR.") (source "RVI-ZICSR §5.1.1"))
  (step (n 7) (insn "csrrs x0, mip, x5") (writes)
    (derivation "atomic read and set bits; rs1=x0 does not write the CSR.") (source "RVI-ZICSR §5.1.1"))
  (step (n 8) (insn "csrrs x7, mip, x0") (writes (write (reg "x7") (value "0x0000000000000202")))
    (derivation "atomic read and set bits; rs1=x0 does not write the CSR.") (source "RVI-ZICSR §5.1.1"))
  (step (n 9) (insn "csrrc x0, mip, x5") (writes)
    (derivation "atomic read and clear bits; rs1=x0 does not write the CSR.") (source "RVI-ZICSR §5.1.1"))
  (step (n 10) (insn "csrrs x8, mip, x0") (writes (write (reg "x8") (value "0x0000000000000000")))
    (derivation "atomic read and set bits; rs1=x0 does not write the CSR.") (source "RVI-ZICSR §5.1.1"))
  (step (n 11) (insn "csrrw x0, stimecmp, x0") (writes)
    (derivation "atomic read/write CSR; rd=x0 discards the old value.") (source "RVI-ZICSR §5.1.1"))
  (step (n 12) (insn "csrrs x9, mip, x0") (writes (write (reg "x9") (value "0x0000000000000020")))
    (derivation "atomic read and set bits; rs1=x0 does not write the CSR.") (source "RVI-ZICSR §5.1.1"))
)
