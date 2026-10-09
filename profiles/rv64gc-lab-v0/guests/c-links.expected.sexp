;; c-links.expected.sexp — spec-side observations for `c-links.s`.
;; Author: scripts/derive_rv64gc_expectations.py; explicit-budget parcel route (C-capable).
;; EVD-05: values derive from independent spec-side rules and the declared
;; laboratory policies; each step names its derivation and source.
;; This derivation makes no processor conformance or original-capture claim.
;; Validate with
;;   python3 scripts/check_sexp_schema.py c-links.expected.sexp schema/expectations.sexp

(expectations (program "c-links.s") (entry "0x0000000080000000") (instructions 10) (fetches 13)
  (step (n 0) (insn "auipc x1, 0") (writes (write (reg "x1") (value "0x0000000080000000")))
    (derivation "auipc writes the instruction's own address plus the U-immediate.") (source "RVI-RV32I §1.1.4 (D-LUI-AUIPC)"))
  (step (n 1) (insn "addi x1, x1, 14") (writes (write (reg "x1") (value "0x000000008000000e")))
    (derivation "the 12-bit immediate adds into rd.") (source "RVI-RV32I §1.1.4"))
  (step (n 2) (insn "c.jalr x1") (writes (write (reg "x1") (value "0x000000008000000a")))
    (derivation "C.JALR uses its declared base operation at length 2: JALR clears target bit zero and writes the following instruction address.") (source "RVI-C §27.1.4; RVI-RV32I §1.1.5"))
  (step (n 3) (insn "c.addi x10, 1") (writes (write (reg "x10") (value "0x0000000000000001")))
    (derivation "C.ADDI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
  (step (n 4) (insn "c.jr x1") (writes)
    (derivation "C.JR uses its declared base operation at length 2: JALR clears target bit zero and writes the following instruction address.") (source "RVI-C §27.1.4; RVI-RV32I §1.1.5"))
  (step (n 5) (insn "c.j after") (writes)
    (derivation "C.J uses its declared base operation at length 2: JAL writes the return address.") (source "RVI-C §27.1.4; RVI-RV32I §1.1.5"))
  (step (n 6) (insn "c.mv x11, x1") (writes (write (reg "x11") (value "0x000000008000000a")))
    (derivation "C.MV uses its declared base operation at length 2: rd = rs1 + rs2, wrapping.") (source "RVI-C §27.1.5.3; RVI-RV32I §1.1.4"))
  (step (n 7) (insn "addi x12, x0, 7") (writes (write (reg "x12") (value "0x0000000000000007")))
    (derivation "the 12-bit immediate adds into rd.") (source "RVI-RV32I §1.1.4"))
  (step (n 8) (insn "c.j finish") (writes)
    (derivation "C.J uses its declared base operation at length 2: JAL writes the return address.") (source "RVI-C §27.1.4; RVI-RV32I §1.1.5"))
  (step (n 9) (insn "c.nop") (writes)
    (derivation "C.NOP uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
)
