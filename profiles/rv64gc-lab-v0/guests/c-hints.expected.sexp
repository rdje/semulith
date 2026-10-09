;; c-hints.expected.sexp — spec-side observations for `c-hints.s`.
;; Author: scripts/derive_rv64gc_expectations.py; explicit-budget parcel route (C-capable).
;; EVD-05: values derive from independent spec-side rules and the declared
;; laboratory policies; each step names its derivation and source.
;; This derivation makes no processor conformance or original-capture claim.
;; Validate with
;;   python3 scripts/check_sexp_schema.py c-hints.expected.sexp schema/expectations.sexp

(expectations (program "c-hints.s") (entry "0x0000000080000000") (instructions 11)
  (step (n 0) (insn "c.li x1, 7") (writes (write (reg "x1") (value "0x0000000000000007")))
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 1) (insn "c.li x8, 9") (writes (write (reg "x8") (value "0x0000000000000009")))
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 2) (insn "c.addi x1, 0") (writes)
    (derivation "C.ADDI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
  (step (n 3) (insn "c.li x0, 31") (writes)
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 4) (insn "c.lui x0, 1") (writes)
    (derivation "C.LUI uses its declared base operation at length 2: the upper 20 bits land sign-extended in rd.") (source "RVI-C §27.1.5.1; RVI-RV64I §3.1.2.1"))
  (step (n 5) (insn "c.slli x0, 1") (writes)
    (derivation "C.SLLI uses its declared base operation at length 2: logical left shift.") (source "RVI-C §27.1.5.2; RVI-RV64I §3.1.2.1"))
  (step (n 6) (insn "c.mv x0, x1") (writes)
    (derivation "C.MV uses its declared base operation at length 2: rd = rs1 + rs2, wrapping.") (source "RVI-C §27.1.5.3; RVI-RV32I §1.1.4"))
  (step (n 7) (insn "c.add x0, x1") (writes)
    (derivation "C.ADD uses its declared base operation at length 2: rd = rs1 + rs2, wrapping.") (source "RVI-C §27.1.5.3; RVI-RV32I §1.1.4"))
  (step (n 8) (insn "c.srli x8, 0") (writes)
    (derivation "C.SRLI uses its declared base operation at length 2: logical right shift.") (source "RVI-C §27.1.5.2; RVI-RV64I §3.1.2.1"))
  (step (n 9) (insn "c.srai x8, 0") (writes)
    (derivation "C.SRAI uses its declared base operation at length 2: arithmetic right shift.") (source "RVI-C §27.1.5.2; RVI-RV64I §3.1.2.1"))
  (step (n 10) (insn "c.nop 1") (writes)
    (derivation "C.NOP uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
)
