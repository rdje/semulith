;; c-res-addi16sp.expected.sexp — spec-side observations for `c-res-addi16sp.s`.
;; Author: scripts/derive_rv64gc_expectations.py; explicit-budget parcel route (C-capable).
;; EVD-05: values derive from independent spec-side rules and the declared
;; laboratory policies; each step names its derivation and source.
;; This derivation makes no processor conformance or original-capture claim.
;; Validate with
;;   python3 scripts/check_sexp_schema.py c-res-addi16sp.expected.sexp schema/expectations.sexp

(expectations (program "c-res-addi16sp.s") (entry "0x0000000080000000") (instructions 13) (fetches 23)
  (step (n 0) (insn "auipc x1, 0") (writes (write (reg "x1") (value "0x0000000080000000")))
    (derivation "auipc writes the instruction's own address plus the U-immediate.") (source "RVI-RV32I §1.1.4 (D-LUI-AUIPC)"))
  (step (n 1) (insn "addi x1, x1, 20") (writes (write (reg "x1") (value "0x0000000080000014")))
    (derivation "the 12-bit immediate adds into rd.") (source "RVI-RV32I §1.1.4"))
  (step (n 2) (insn "csrrw x0, mtvec, x1") (writes)
    (derivation "atomic read/write CSR; rd=x0 discards the old value.") (source "RVI-ZICSR §5.1.1"))
  (step (n 3) (insn ".half 0x6101") (writes)
    (derivation "reserved compressed parcel 0x6101: C.LUI/C.ADDI16SP has zero immediate; cause 2, xtval the original 16 bits.") (source "RVI-C §27.1.5/§27.1.8; the laboratory illegal-instruction policy"))
  (step (n 4) (insn "csrrs x7, mcause, x0") (writes (write (reg "x7") (value "0x0000000000000002")))
    (derivation "atomic read and set bits; rs1=x0 does not write the CSR.") (source "RVI-ZICSR §5.1.1"))
  (step (n 5) (insn "csrrs x8, mtval, x0") (writes (write (reg "x8") (value "0x0000000000006101")))
    (derivation "atomic read and set bits; rs1=x0 does not write the CSR.") (source "RVI-ZICSR §5.1.1"))
  (step (n 6) (insn "csrrs x9, mepc, x0") (writes (write (reg "x9") (value "0x000000008000000c")))
    (derivation "atomic read and set bits; rs1=x0 does not write the CSR.") (source "RVI-ZICSR §5.1.1"))
  (step (n 7) (insn "addi x9, x9, 2") (writes (write (reg "x9") (value "0x000000008000000e")))
    (derivation "the 12-bit immediate adds into rd.") (source "RVI-RV32I §1.1.4"))
  (step (n 8) (insn "csrrw x0, mepc, x9") (writes)
    (derivation "atomic read/write CSR; rd=x0 discards the old value.") (source "RVI-ZICSR §5.1.1"))
  (step (n 9) (insn "mret") (writes)
    (derivation "the privilege stack pops per MPP and pc <- mepc.") (source "RVP-MACHINE §2.1.3.2"))
  (step (n 10) (insn "addi x20, x0, 7") (writes (write (reg "x20") (value "0x0000000000000007")))
    (derivation "the 12-bit immediate adds into rd.") (source "RVI-RV32I §1.1.4"))
  (step (n 11) (insn "c.j done") (writes)
    (derivation "C.J uses its declared base operation at length 2: JAL writes the return address.") (source "RVI-C §27.1.4; RVI-RV32I §1.1.5"))
  (step (n 12) (insn "c.nop") (writes)
    (derivation "C.NOP uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
)
