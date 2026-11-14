;; lui-auipc-forms.expected.sexp — spec-side observations for `lui-auipc-forms.s`.
;; Author: scripts/derive_rv64gc_expectations.py; explicit-budget parcel route (C-capable).
;; EVD-05: values derive from independent spec-side rules and the declared
;; laboratory policies; each step names its derivation and source.
;; This derivation makes no processor conformance or original-capture claim.
;; Validate with
;;   python3 scripts/check_sexp_schema.py lui-auipc-forms.expected.sexp schema/expectations.sexp

(expectations (program "lui-auipc-forms.s") (entry "0x0000000080000000") (instructions 10) (fetches 20)
  (step (n 0) (insn "lui x5, 0x12345") (writes (write (reg "x5") (value "0x0000000012345000")))
    (derivation "LUI fills the low 12 bits with zeros: 0x0000000012345000.") (source "RVI-RV64I §3.1.2.1"))
  (step (n 1) (insn "lui x6, 0x80000") (writes (write (reg "x6") (value "0xffffffff80000000")))
    (derivation "bit 31 set: the 32-bit result sign-extends to 64 bits, 0xffffffff80000000.") (source "RVI-RV64I §3.1.2.1 (boundary: LUI sign-extends from bit 31)"))
  (step (n 2) (insn "lui x7, 0x7ffff") (writes (write (reg "x7") (value "0x000000007ffff000")))
    (derivation "bit 31 clear, the largest positive result: 0x000000007ffff000.") (source "RVI-RV64I §3.1.2.1 (boundary: LUI's largest positive result)"))
  (step (n 3) (insn "lui x8, 0xfffff") (writes (write (reg "x8") (value "0xfffffffffffff000")))
    (derivation "every U-immediate bit set: 0xfffffffffffff000.") (source "RVI-RV64I §3.1.2.1 (boundary: LUI with all its immediate bits set)"))
  (step (n 4) (insn "addi x13, x0, 77") (writes (write (reg "x13") (value "0x000000000000004d")))
    (derivation "a sentinel, so the 0 that follows is a change.") (source "RVI-RV32I §1.1.4"))
  (step (n 5) (insn "lui x13, 0") (writes (write (reg "x13") (value "0x0000000000000000")))
    (derivation "a zero immediate clears rd: 0x0000000000000000.") (source "RVI-RV64I §3.1.2.1 (boundary: LUI with a zero immediate)"))
  (step (n 6) (insn "auipc x9, 0") (writes (write (reg "x9") (value "0x0000000080000018")))
    (derivation "AUIPC with a zero offset reads this instruction's own address: 0x0000000080000018.") (source "RVI-RV64I §3.1.2.1"))
  (step (n 7) (insn "auipc x10, 1") (writes (write (reg "x10") (value "0x000000008000101c")))
    (derivation "AUIPC adds the 0x1000 offset to its own address: 0x000000008000101c.") (source "RVI-RV64I §3.1.2.1"))
  (step (n 8) (insn "auipc x11, 0x80000") (writes (write (reg "x11") (value "0x0000000000000020")))
    (derivation "the offset sign-extends to -2^31, so the 0x80000000 of the address cancels: 0x0000000000000020.") (source "RVI-RV64I §3.1.2.1 (boundary: AUIPC's offset sign-extends)"))
  (step (n 9) (insn "auipc x12, 0x7ffff") (writes (write (reg "x12") (value "0x00000000fffff024")))
    (derivation "the largest positive offset, 0x7ffff000, added: 0x00000000fffff024.") (source "RVI-RV64I §3.1.2.1 (boundary: AUIPC's largest positive offset)"))
)
