;; c-immediates.expected.sexp — spec-side observations for `c-immediates.s`.
;; Author: scripts/derive_rv64gc_expectations.py; explicit-budget parcel route (C-capable).
;; EVD-05: values derive from independent spec-side rules and the declared
;; laboratory policies; each step names its derivation and source.
;; This derivation makes no processor conformance or original-capture claim.
;; Validate with
;;   python3 scripts/check_sexp_schema.py c-immediates.expected.sexp schema/expectations.sexp

(expectations (program "c-immediates.s") (entry "0x0000000080000000") (instructions 15) (fetches 16)
  (step (n 0) (insn "c.li x1, -32") (writes (write (reg "x1") (value "0xffffffffffffffe0")))
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 1) (insn "c.addi x1, 31") (writes (write (reg "x1") (value "0xffffffffffffffff")))
    (derivation "C.ADDI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
  (step (n 2) (insn "c.addi x1, 1") (writes (write (reg "x1") (value "0x0000000000000000")))
    (derivation "C.ADDI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
  (step (n 3) (insn "c.li x3, 31") (writes (write (reg "x3") (value "0x000000000000001f")))
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 4) (insn "c.addi x3, -32") (writes (write (reg "x3") (value "0xffffffffffffffff")))
    (derivation "C.ADDI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
  (step (n 5) (insn "c.lui x4, -32") (writes (write (reg "x4") (value "0xfffffffffffe0000")))
    (derivation "C.LUI uses its declared base operation at length 2: the upper 20 bits land sign-extended in rd.") (source "RVI-C §27.1.5.1; RVI-RV64I §3.1.2.1"))
  (step (n 6) (insn "c.lui x5, 31") (writes (write (reg "x5") (value "0x000000000001f000")))
    (derivation "C.LUI uses its declared base operation at length 2: the upper 20 bits land sign-extended in rd.") (source "RVI-C §27.1.5.1; RVI-RV64I §3.1.2.1"))
  (step (n 7) (insn "c.li x2, 16") (writes (write (reg "x2") (value "0x0000000000000010")))
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 8) (insn "c.addi16sp -512") (writes (write (reg "x2") (value "0xfffffffffffffe10")))
    (derivation "C.ADDI16SP uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
  (step (n 9) (insn "c.addi16sp 496") (writes (write (reg "x2") (value "0x0000000000000000")))
    (derivation "C.ADDI16SP uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
  (step (n 10) (insn "c.addi4spn x8, 1020") (writes (write (reg "x8") (value "0x00000000000003fc")))
    (derivation "C.ADDI4SPN uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
  (step (n 11) (insn "addi x2, x0, -1") (writes (write (reg "x2") (value "0xffffffffffffffff")))
    (derivation "the 12-bit immediate adds into rd.") (source "RVI-RV32I §1.1.4"))
  (step (n 12) (insn "c.addi16sp 16") (writes (write (reg "x2") (value "0x000000000000000f")))
    (derivation "C.ADDI16SP uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
  (step (n 13) (insn "c.addi4spn x15, 4") (writes (write (reg "x15") (value "0x0000000000000013")))
    (derivation "C.ADDI4SPN uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
  (step (n 14) (insn "c.nop") (writes)
    (derivation "C.NOP uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
)
