;; c-alu.expected.sexp — spec-side observations for `c-alu.s`.
;; Author: scripts/derive_rv64gc_expectations.py; explicit-budget parcel route (C-capable).
;; EVD-05: values derive from independent spec-side rules and the declared
;; laboratory policies; each step names its derivation and source.
;; This derivation makes no processor conformance or original-capture claim.
;; Validate with
;;   python3 scripts/check_sexp_schema.py c-alu.expected.sexp schema/expectations.sexp

(expectations (program "c-alu.s") (entry "0x0000000080000000") (instructions 16)
  (step (n 0) (insn "c.li x8, -1") (writes (write (reg "x8") (value "0xffffffffffffffff")))
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 1) (insn "c.srli x8, 63") (writes (write (reg "x8") (value "0x0000000000000001")))
    (derivation "C.SRLI uses its declared base operation at length 2: logical right shift.") (source "RVI-C §27.1.5.2; RVI-RV64I §3.1.2.1"))
  (step (n 2) (insn "c.slli x8, 63") (writes (write (reg "x8") (value "0x8000000000000000")))
    (derivation "C.SLLI uses its declared base operation at length 2: logical left shift.") (source "RVI-C §27.1.5.2; RVI-RV64I §3.1.2.1"))
  (step (n 3) (insn "c.srai x8, 63") (writes (write (reg "x8") (value "0xffffffffffffffff")))
    (derivation "C.SRAI uses its declared base operation at length 2: arithmetic right shift.") (source "RVI-C §27.1.5.2; RVI-RV64I §3.1.2.1"))
  (step (n 4) (insn "c.andi x8, -32") (writes (write (reg "x8") (value "0xffffffffffffffe0")))
    (derivation "C.ANDI uses its declared base operation at length 2: bitwise AND with the sign-extended immediate.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
  (step (n 5) (insn "c.li x9, 1") (writes (write (reg "x9") (value "0x0000000000000001")))
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 6) (insn "c.add x8, x9") (writes (write (reg "x8") (value "0xffffffffffffffe1")))
    (derivation "C.ADD uses its declared base operation at length 2: rd = rs1 + rs2, wrapping.") (source "RVI-C §27.1.5.3; RVI-RV32I §1.1.4"))
  (step (n 7) (insn "c.sub x8, x9") (writes (write (reg "x8") (value "0xffffffffffffffe0")))
    (derivation "C.SUB uses its declared base operation at length 2: rd = rs1 - rs2, wrapping.") (source "RVI-C §27.1.5.3; RVI-RV32I §1.1.4"))
  (step (n 8) (insn "c.and x8, x9") (writes (write (reg "x8") (value "0x0000000000000000")))
    (derivation "C.AND uses its declared base operation at length 2: bitwise AND.") (source "RVI-C §27.1.5.3; RVI-RV32I §1.1.4"))
  (step (n 9) (insn "c.or x8, x9") (writes (write (reg "x8") (value "0x0000000000000001")))
    (derivation "C.OR uses its declared base operation at length 2: bitwise OR.") (source "RVI-C §27.1.5.3; RVI-RV32I §1.1.4"))
  (step (n 10) (insn "c.xor x8, x9") (writes (write (reg "x8") (value "0x0000000000000000")))
    (derivation "C.XOR uses its declared base operation at length 2: bitwise XOR.") (source "RVI-C §27.1.5.3; RVI-RV32I §1.1.4"))
  (step (n 11) (insn "c.mv x10, x9") (writes (write (reg "x10") (value "0x0000000000000001")))
    (derivation "C.MV uses its declared base operation at length 2: rd = rs1 + rs2, wrapping.") (source "RVI-C §27.1.5.3; RVI-RV32I §1.1.4"))
  (step (n 12) (insn "c.add x10, x10") (writes (write (reg "x10") (value "0x0000000000000002")))
    (derivation "C.ADD uses its declared base operation at length 2: rd = rs1 + rs2, wrapping.") (source "RVI-C §27.1.5.3; RVI-RV32I §1.1.4"))
  (step (n 13) (insn "c.slli x10, 0") (writes)
    (derivation "C.SLLI uses its declared base operation at length 2: logical left shift.") (source "RVI-C §27.1.5.2; RVI-RV64I §3.1.2.1"))
  (step (n 14) (insn "c.srli x8, 0") (writes)
    (derivation "C.SRLI uses its declared base operation at length 2: logical right shift.") (source "RVI-C §27.1.5.2; RVI-RV64I §3.1.2.1"))
  (step (n 15) (insn "c.srai x8, 0") (writes)
    (derivation "C.SRAI uses its declared base operation at length 2: arithmetic right shift.") (source "RVI-C §27.1.5.2; RVI-RV64I §3.1.2.1"))
)
