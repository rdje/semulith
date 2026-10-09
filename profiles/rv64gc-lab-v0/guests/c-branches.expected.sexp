;; c-branches.expected.sexp — spec-side observations for `c-branches.s`.
;; Author: scripts/derive_rv64gc_expectations.py; explicit-budget parcel route (C-capable).
;; EVD-05: values derive from independent spec-side rules and the declared
;; laboratory policies; each step names its derivation and source.
;; This derivation makes no processor conformance or original-capture claim.
;; Validate with
;;   python3 scripts/check_sexp_schema.py c-branches.expected.sexp schema/expectations.sexp

(expectations (program "c-branches.s") (entry "0x0000000080000000") (instructions 8)
  (step (n 0) (insn "c.li x8, 0") (writes)
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 1) (insn "c.beqz x8, zero") (writes)
    (derivation "C.BEQZ uses its declared base operation at length 2: branch if equal — a taken branch writes no register.") (source "RVI-C §27.1.4; RVI-RV32I §1.1.5"))
  (step (n 2) (insn "c.li x9, 1") (writes (write (reg "x9") (value "0x0000000000000001")))
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 3) (insn "c.bnez x9, one") (writes)
    (derivation "C.BNEZ uses its declared base operation at length 2: branch if not equal — a taken branch writes no register.") (source "RVI-C §27.1.4; RVI-RV32I §1.1.5"))
  (step (n 4) (insn "c.bnez x8, finish") (writes)
    (derivation "C.BNEZ uses its declared base operation at length 2: branch if not equal — a taken branch writes no register.") (source "RVI-C §27.1.4; RVI-RV32I §1.1.5"))
  (step (n 5) (insn "c.beqz x9, finish") (writes)
    (derivation "C.BEQZ uses its declared base operation at length 2: branch if equal — a taken branch writes no register.") (source "RVI-C §27.1.4; RVI-RV32I §1.1.5"))
  (step (n 6) (insn "c.li x10, 7") (writes (write (reg "x10") (value "0x0000000000000007")))
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 7) (insn "c.nop") (writes)
    (derivation "C.NOP uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
)
