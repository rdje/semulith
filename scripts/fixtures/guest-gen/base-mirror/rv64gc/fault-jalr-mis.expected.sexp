;; fault-jalr-mis.expected.sexp — the expected observations for `fault-jalr-mis.s` (P2-SCALAR.3).
;; Validate with:
;;   python3 scripts/check_sexp_schema.py fault-jalr-mis.expected.sexp schema/expectations.sexp

(comment "GC IALIGN=16 re-derivation: the historical base-profile basename is retained. Current annotations describe the legal jump/link and declared budget; base IALIGN=32 trap/reference claims do not transfer.")
(expectations (program "fault-jalr-mis.s") (entry "0x80000000") (instructions 2) (fetches 4) (step (n 0) (insn "addi x1, x0, 3") (writes (write (reg "x1") (value "0x0000000000000003"))) (derivation "Target material x1=3 has bits 0 and 1 set. Clearing only bit 0 after adding the immediate must retain bit 1.") (source "RVI-RV32I §1.1.4")) (step (n 1) (insn "jalr x5, x1, 0") (writes (write (reg "x5") (value "0x0000000080000008"))) (derivation "JALR computes (3+0)&~1=2. IALIGN=16 permits that alignment, so the jump completes and x5 receives pc+4=0x80000008. The two-boundary budget does not fetch address 2 or independently judge final PC.") (source "RVI-RV32I §1.1.5.1; RVI-C §27.1")))
