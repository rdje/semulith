;; c-irq.expected.sexp — spec-side observations for `c-irq.s`.
;; Author: scripts/derive_rv64gc_expectations.py; explicit-budget parcel route (C-capable).
;; EVD-05: values derive from independent spec-side rules and the declared
;; laboratory policies; each step names its derivation and source.
;; This derivation makes no processor conformance or original-capture claim.
;; Validate with
;;   python3 scripts/check_sexp_schema.py c-irq.expected.sexp schema/expectations.sexp

(expectations (program "c-irq.s") (entry "0x0000000080000000") (instructions 17) (fetches 28)
  (step (n 0) (insn "auipc x1, 0") (writes (write (reg "x1") (value "0x0000000080000000")))
    (derivation "auipc writes the instruction's own address plus the U-immediate.") (source "RVI-RV32I §1.1.4 (D-LUI-AUIPC)"))
  (step (n 1) (insn "addi x1, x1, 40") (writes (write (reg "x1") (value "0x0000000080000028")))
    (derivation "the 12-bit immediate adds into rd.") (source "RVI-RV32I §1.1.4"))
  (step (n 2) (insn "csrrw x0, mtvec, x1") (writes)
    (derivation "atomic read/write CSR; rd=x0 discards the old value.") (source "RVI-ZICSR §5.1.1"))
  (step (n 3) (insn "addi x2, x0, 32") (writes (write (reg "x2") (value "0x0000000000000020")))
    (derivation "the 12-bit immediate adds into rd.") (source "RVI-RV32I §1.1.4"))
  (step (n 4) (insn "csrrw x0, mie, x2") (writes)
    (derivation "atomic read/write CSR; rd=x0 discards the old value.") (source "RVI-ZICSR §5.1.1"))
  (step (n 5) (insn "addi x3, x0, 9") (writes (write (reg "x3") (value "0x0000000000000009")))
    (derivation "the 12-bit immediate adds into rd.") (source "RVI-RV32I §1.1.4"))
  (step (n 6) (insn "csrrw x0, stimecmp, x3") (writes)
    (derivation "atomic read/write CSR; rd=x0 discards the old value.") (source "RVI-ZICSR §5.1.1"))
  (step (n 7) (insn "csrrsi x0, mstatus, 8") (writes)
    (derivation "read and set the uimm bits (uimm=0 writes nothing).") (source "RVI-ZICSR §5.1.1"))
  (step (n 8) (insn "c.li x10, 1") (writes (write (reg "x10") (value "0x0000000000000001")))
    (derivation "C.LI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.1; RVI-RV32I §1.1.4"))
  (step (n 9) (insn "c.addi x10, 1") (writes)
    (derivation "pending interrupt 5 delivers in M before instruction fetch; EPC is this boundary PC, no retirement.") (source "RVP-MACHINE §2.1.1.9; RVP-SUPERVISOR §11.1.1.3"))
  (step (n 10) (insn "csrrs x7, mcause, x0") (writes (write (reg "x7") (value "0x8000000000000005")))
    (derivation "atomic read and set bits; rs1=x0 does not write the CSR.") (source "RVI-ZICSR §5.1.1"))
  (step (n 11) (insn "csrrs x8, mepc, x0") (writes (write (reg "x8") (value "0x0000000080000022")))
    (derivation "atomic read and set bits; rs1=x0 does not write the CSR.") (source "RVI-ZICSR §5.1.1"))
  (step (n 12) (insn "csrrw x0, mie, x0") (writes)
    (derivation "atomic read/write CSR; rd=x0 discards the old value.") (source "RVI-ZICSR §5.1.1"))
  (step (n 13) (insn "mret") (writes)
    (derivation "the privilege stack pops per MPP and pc <- mepc.") (source "RVP-MACHINE §2.1.3.2"))
  (step (n 14) (insn "c.addi x10, 1") (writes (write (reg "x10") (value "0x0000000000000002")))
    (derivation "C.ADDI uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
  (step (n 15) (insn "c.j done") (writes)
    (derivation "C.J uses its declared base operation at length 2: JAL writes the return address.") (source "RVI-C §27.1.4; RVI-RV32I §1.1.5"))
  (step (n 16) (insn "c.nop") (writes)
    (derivation "C.NOP uses its declared base operation at length 2: the 12-bit immediate adds into rd.") (source "RVI-C §27.1.5.2; RVI-RV32I §1.1.4"))
)
