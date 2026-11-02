;; fault-jal-mis.expected.sexp — the expected observations for `fault-jal-mis.s` (P2-SCALAR.3).
;; Validate with:
;;   python3 scripts/check_sexp_schema.py fault-jal-mis.expected.sexp schema/expectations.sexp

(comment "GC IALIGN=16 re-derivation: the historical base-profile basename is retained. Current annotations describe the legal jump/link and declared budget; base IALIGN=32 trap/reference claims do not transfer.")
(expectations (program "fault-jal-mis.s") (entry "0x80000000") (instructions 2) (fetches 4) (step (n 0) (insn "addi x1, x0, 1") (writes (write (reg "x1") (value "0x0000000000000001"))) (derivation "An ordinary first write: x1=1. No trap occurs at either declared instruction boundary.") (source "RVI-RV32I §1.1.4")) (step (n 1) (insn "jal x5, 2") (writes (write (reg "x5") (value "0x0000000080000008"))) (derivation "JAL at 0x80000004 adds offset 2, reaching 0x80000006. IALIGN=16 permits this target. The jump completes and writes pc+4=0x80000008 to x5; the two-boundary budget ends before a target fetch.") (source "RVI-RV32I §1.1.5.1; RVI-C §27.1")))
