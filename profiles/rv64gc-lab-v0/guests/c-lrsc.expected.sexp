;; c-lrsc.expected.sexp — spec-side observations for `c-lrsc.s`.
;; Author: scripts/derive_rv64gc_expectations.py; explicit-budget parcel route (C-capable).
;; EVD-05: values derive from independent spec-side rules and the declared
;; laboratory policies; each step names its derivation and source.
;; This derivation makes no processor conformance or original-capture claim.
;; Validate with
;;   python3 scripts/check_sexp_schema.py c-lrsc.expected.sexp schema/expectations.sexp

(expectations (program "c-lrsc.s") (entry "0x0000000080000000") (instructions 9) (fetches 13)
  (step (n 0) (insn "auipc x8, 0") (writes (write (reg "x8") (value "0x0000000080000000")))
    (derivation "auipc writes the instruction's own address plus the U-immediate.") (source "RVI-RV32I §1.1.4 (D-LUI-AUIPC)"))
  (step (n 1) (insn "addi x8, x8, 1024") (writes (write (reg "x8") (value "0x0000000080000400")))
    (derivation "the 12-bit immediate adds into rd.") (source "RVI-RV32I §1.1.4"))
  (step (n 2) (insn "c.li x9, 5") (writes (write (reg "x9") (value "0x0000000000000005")))
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 3) (insn "c.sd x8, x9, 0") (writes)
    (derivation "C.SD uses its declared base operation at length 2: SD stores the low 64 bits of rs2 — no register observation.") (source "RVI-C §27.1.3.2; RVI-RV64I §3.1.3"))
  (step (n 4) (insn "lr.d x10, (x8)") (writes (write (reg "x10") (value "0x0000000000000005")))
    (derivation "LR.D loads the doubleword into rd and registers the reservation.") (source "RVI-A §12.1.2"))
  (step (n 5) (insn "c.addi x10, 1") (writes (write (reg "x10") (value "0x0000000000000006")))
    (derivation "C.ADDI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
  (step (n 6) (insn "c.li x11, -1") (writes (write (reg "x11") (value "0xffffffffffffffff")))
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 7) (insn "sc.d x11, x10, (x8)") (writes (write (reg "x11") (value "0x0000000000000000")))
    (derivation "sc.d: the reservation matches (valid ∧ PA equal ∧ width equal): the store lands, rd <- 0, the reservation clears (the deterministic policy: succeeds iff valid ∧ physical address equal ∧ width equal).") (source "RVI-A §12.1.2; state.sexp's reservation candidate (decision 3)"))
  (step (n 8) (insn "c.ld x12, x8, 0") (writes (write (reg "x12") (value "0x0000000000000006")))
    (derivation "C.LD uses its declared base operation at length 2: a full XLEN load needs no extension.") (source "RVI-C §27.1.3.2; RVI-RV64I §3.1.3"))
)
