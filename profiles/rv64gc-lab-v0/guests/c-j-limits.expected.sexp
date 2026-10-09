;; c-j-limits.expected.sexp — spec-side observations for `c-j-limits.s`.
;; Author: scripts/derive_rv64gc_expectations.py; explicit-budget parcel route (C-capable).
;; EVD-05: values derive from independent spec-side rules and the declared
;; laboratory policies; each step names its derivation and source.
;; This derivation makes no processor conformance or original-capture claim.
;; Validate with
;;   python3 scripts/check_sexp_schema.py c-j-limits.expected.sexp schema/expectations.sexp

(expectations (program "c-j-limits.s") (entry "0x0000000080000000") (instructions 7)
  (step (n 0) (insn "c.li x8, 2") (writes (write (reg "x8") (value "0x0000000000000002")))
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 1) (insn "c.j 2046") (writes)
    (derivation "C.J uses its declared base operation at length 2: JAL writes the return address.") (source "RVI-C §27.1.4; RVI-RV32I §1.1.5"))
  (step (n 2) (insn "c.addi x8, -1") (writes (write (reg "x8") (value "0x0000000000000001")))
    (derivation "C.ADDI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
  (step (n 3) (insn "c.j -2048") (writes)
    (derivation "C.J uses its declared base operation at length 2: JAL writes the return address.") (source "RVI-C §27.1.4; RVI-RV32I §1.1.5"))
  (step (n 4) (insn "c.j 2046") (writes)
    (derivation "C.J uses its declared base operation at length 2: JAL writes the return address.") (source "RVI-C §27.1.4; RVI-RV32I §1.1.5"))
  (step (n 5) (insn "c.addi x8, -1") (writes (write (reg "x8") (value "0x0000000000000000")))
    (derivation "C.ADDI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
  (step (n 6) (insn "c.j -2048") (writes)
    (derivation "C.J uses its declared base operation at length 2: JAL writes the return address.") (source "RVI-C §27.1.4; RVI-RV32I §1.1.5"))
)
