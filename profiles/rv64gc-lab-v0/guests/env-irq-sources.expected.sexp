;; env-irq-sources.expected.sexp — the expected observations for `env-irq-sources.s` (P4-SYSTEM.9,
;; the environment-contract fixtures). EVD-05: every value below was derived from the
;; pinned chapters and the contract v1 assumptions by the spec-side authoring model
;; BEFORE any engine run; the corpus runner falsifies against it.
;; Validate with
;;   python3 scripts/check_sexp_schema.py env-irq-sources.expected.sexp schema/expectations.sexp

(expectations (program "env-irq-sources.s") (entry "0x0000000080000000") (instructions 11)
  (never_written "x28")
  (never_written "x29")
  (step (n 0) (insn "addi x6, x0, 1") (writes (write (reg "x6") (value "0x0000000000000001")))
    (derivation "a sentinel the first mip read must REPLACE.") (source "RVI-RV32I §1.1.4"))
  (step (n 1) (insn "addi x8, x0, 1") (writes (write (reg "x8") (value "0x0000000000000001")))
    (derivation "another sentinel.") (source "RVI-RV32I §1.1.4"))
  (step (n 2) (insn "addi x5, x0, -1") (writes (write (reg "x5") (value "0xffffffffffffffff")))
    (derivation "all ones …") (source "RVI-RV32I §1.1.4"))
  (step (n 3) (insn "csrrw x0, stimecmp, x5") (writes)
    (derivation "stimecmp <- the maximum: STIP, the hart's own comparison, reads 0 (time is far below).") (source "RVP-SSTC 12.1"))
  (step (n 4) (insn "csrrs x6, mip, x0") (writes (write (reg "x6") (value "0x0000000000000000")))
    (derivation "mip before: no source has asserted anything — 0.") (source "RVP-MACHINE §2.1.1.9"))
  (step (n 5) (insn "csrrs x0, mip, x5") (writes)
    (derivation "software writes ONES to every mip bit, the M-level sources' MSIP (3), MTIP (7) and MEIP (11) among them.") (source "RVP-MACHINE §2.1.1.9"))
  (step (n 6) (insn "csrrs x7, mip, x0") (writes (write (reg "x7") (value "0x0000000000000202")))
    (derivation "only the software-writable SSIP and SEIP took (0x202): MSIP, MTIP and MEIP stay 0 — this environment supplies no source, and a write cannot be one.") (source "RVP-MACHINE §2.1.1.9; the contract v1's interrupt-source assumption"))
  (step (n 7) (insn "csrrc x0, mip, x5") (writes)
    (derivation "software clears what it can.") (source "RVP-MACHINE §2.1.1.9"))
  (step (n 8) (insn "csrrs x8, mip, x0") (writes (write (reg "x8") (value "0x0000000000000000")))
    (derivation "back to 0: nothing is pending that software did not set.") (source "RVP-MACHINE §2.1.1.9"))
  (step (n 9) (insn "csrrw x0, stimecmp, x0") (writes)
    (derivation "stimecmp <- 0: now time >= stimecmp …") (source "RVP-SSTC 12.1"))
  (step (n 10) (insn "csrrs x9, mip, x0") (writes (write (reg "x9") (value "0x0000000000000020")))
    (derivation "… so STIP (bit 5) reads 1 — the hart's own comparison, the one timer source v1 has.") (source "RVP-SSTC 12.1 #|end"))
)
