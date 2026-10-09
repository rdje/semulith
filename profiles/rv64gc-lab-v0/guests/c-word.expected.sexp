;; c-word.expected.sexp — spec-side observations for `c-word.s`.
;; Author: scripts/derive_rv64gc_expectations.py; explicit-budget parcel route (C-capable).
;; EVD-05: values derive from independent spec-side rules and the declared
;; laboratory policies; each step names its derivation and source.
;; This derivation makes no processor conformance or original-capture claim.
;; Validate with
;;   python3 scripts/check_sexp_schema.py c-word.expected.sexp schema/expectations.sexp

(expectations (program "c-word.s") (entry "0x0000000080000000") (instructions 10) (fetches 12)
  (step (n 0) (insn "lui x8, 524288") (writes (write (reg "x8") (value "0xffffffff80000000")))
    (derivation "the upper 20 bits land sign-extended in rd.") (source "RVI-RV64I §3.1.2.1"))
  (step (n 1) (insn "addi x8, x8, -1") (writes (write (reg "x8") (value "0xffffffff7fffffff")))
    (derivation "the 12-bit immediate adds into rd.") (source "RVI-RV32I §1.1.4"))
  (step (n 2) (insn "c.li x9, 1") (writes (write (reg "x9") (value "0x0000000000000001")))
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 3) (insn "c.addw x8, x9") (writes (write (reg "x8") (value "0xffffffff80000000")))
    (derivation "C.ADDW uses its declared base operation at length 2: the low 32 bits of the sum, sign-extended to 64 bits.") (source "RVI-C §27.1.5.3; RVI-RV64I §3.1.2.2"))
  (step (n 4) (insn "c.subw x8, x9") (writes (write (reg "x8") (value "0x000000007fffffff")))
    (derivation "C.SUBW uses its declared base operation at length 2: the low 32 bits of the difference, sign-extended to 64 bits.") (source "RVI-C §27.1.5.3; RVI-RV64I §3.1.2.2"))
  (step (n 5) (insn "c.addiw x8, 1") (writes (write (reg "x8") (value "0xffffffff80000000")))
    (derivation "C.ADDIW uses its declared base operation at length 2: the low 32 bits add, sign-extended (D-WSUFFIX).") (source "RVI-C §27.1.5.2; RVI-RV64I §3.1.2.1"))
  (step (n 6) (insn "c.addiw x8, 0") (writes)
    (derivation "C.ADDIW uses its declared base operation at length 2: the low 32 bits add, sign-extended (D-WSUFFIX).") (source "RVI-C §27.1.5.2; RVI-RV64I §3.1.2.1"))
  (step (n 7) (insn "c.addiw x8, -32") (writes (write (reg "x8") (value "0x000000007fffffe0")))
    (derivation "C.ADDIW uses its declared base operation at length 2: the low 32 bits add, sign-extended (D-WSUFFIX).") (source "RVI-C §27.1.5.2; RVI-RV64I §3.1.2.1"))
  (step (n 8) (insn "c.addw x9, x9") (writes (write (reg "x9") (value "0x0000000000000002")))
    (derivation "C.ADDW uses its declared base operation at length 2: the low 32 bits of the sum, sign-extended to 64 bits.") (source "RVI-C §27.1.5.3; RVI-RV64I §3.1.2.2"))
  (step (n 9) (insn "c.subw x9, x9") (writes (write (reg "x9") (value "0x0000000000000000")))
    (derivation "C.SUBW uses its declared base operation at length 2: the low 32 bits of the difference, sign-extended to 64 bits.") (source "RVI-C §27.1.5.3; RVI-RV64I §3.1.2.2"))
)
