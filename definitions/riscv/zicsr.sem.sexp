;; zicsr.sem.sexp — what each Zicsr instruction DOES, plus the ECALL/EBREAK refinement.
;;
;; ⛔ HAND-WRITTEN FROM THE PINNED SPECIFICATION, like rv64i.sem.sexp: every rule carries the
;; locator it was derived from, and generated encodings never share a file with authored
;; semantics.
;;
;; THE PERMISSION MODEL IS NOT IN THESE RULES, BY DESIGN. It is part of csr-read/csr-write's
;; meaning (schema/semantics.sexp), so every CSR instruction gets it once: the address-map
;; mode bits and read-only bits (RVP-CSR §1.1.1), the counter-enable gates (RVP-MACHINE
;; §2.1.1.11, RVP-SUPERVISOR §11.1.1.5), the STCE gate (§2.1.1.18, RVP-SSTC 12.1) and the
;; TVM gate on satp (§2.1.1.6.6). A refused access raises illegal-instruction there.
;;
;; THE WARL SEAM (stated, dated 2026-10-03): csr-write legalizes the written value under the
;; CSR's DECLARED per-field discipline (WPRI/WARL/WLRL). Those tables are P4-SYSTEM.2 slice
;; (c)'s state document, and the engine applies them at lowering time (slice d) — this file
;; does not change when a field's discipline is declared or refined.
;;
;; READS: `(reg x)` reads the PRE-INSTRUCTION register file (the language's READS AND WRITES
;; contract in schema/semantics.sexp) — the csrrw swap is exact even for rd==rs1 because of
;; it. A CSR value read twice inside one rule (csrrs/csrrc read, then modify) reads the same
;; pre-write value; CSR reads in this model are side-effect-free, which is exactly why the
;; "shall not read / shall not write" disciplines below are stated rather than emergent.

(semantics
  (fragment "riscv/zicsr")
  (xlen 64)

  (refines (insn "ecall"))
  (refines (insn "ebreak"))

  ;; ---- the six CSR access instructions (RVI-ZICSR §5.1.1) -----------------------------------
  (sem (insn csrrw) (source "RVI-ZICSR §5.1.1 — atomic read/write CSR; if rd=x0 the instruction shall not read the CSR")
       (effect (if (eq (field rd) (lit 0))
                   (csr-write (field csr) (reg rs1))
                   (seq (set (reg rd) (csr-read (field csr)))
                        (csr-write (field csr) (reg rs1))))))
  (sem (insn csrrs) (source "RVI-ZICSR §5.1.1 — atomic read and set bits; if rs1=x0 the instruction shall not write the CSR")
       (effect (if (eq (field rs1) (lit 0))
                   (set (reg rd) (csr-read (field csr)))
                   (seq (set (reg rd) (csr-read (field csr)))
                        (csr-write (field csr) (or (csr-read (field csr)) (reg rs1)))))))
  (sem (insn csrrc) (source "RVI-ZICSR §5.1.1 — atomic read and clear bits; if rs1=x0 the instruction shall not write the CSR")
       (effect (if (eq (field rs1) (lit 0))
                   (set (reg rd) (csr-read (field csr)))
                   (seq (set (reg rd) (csr-read (field csr)))
                        (csr-write (field csr) (and (csr-read (field csr))
                                                    (xor (reg rs1) (lit -1))))))))
  (sem (insn csrrwi) (source "RVI-ZICSR §5.1.1 — CSRRW with a zero-extended 5-bit immediate; if rd=x0 the instruction shall not read the CSR")
       (effect (if (eq (field rd) (lit 0))
                   (csr-write (field csr) (zext 64 (field zimm5)))
                   (seq (set (reg rd) (csr-read (field csr)))
                        (csr-write (field csr) (zext 64 (field zimm5)))))))
  (sem (insn csrrsi) (source "RVI-ZICSR §5.1.1 — CSRRS with a zero-extended 5-bit immediate; if uimm=0 the instruction shall not write the CSR")
       (effect (if (eq (field zimm5) (lit 0))
                   (set (reg rd) (csr-read (field csr)))
                   (seq (set (reg rd) (csr-read (field csr)))
                        (csr-write (field csr) (or (csr-read (field csr))
                                                   (zext 64 (field zimm5))))))))
  (sem (insn csrrci) (source "RVI-ZICSR §5.1.1 — CSRRC with a zero-extended 5-bit immediate; if uimm=0 the instruction shall not write the CSR")
       (effect (if (eq (field zimm5) (lit 0))
                   (set (reg rd) (csr-read (field csr)))
                   (seq (set (reg rd) (csr-read (field csr)))
                        (csr-write (field csr) (and (csr-read (field csr))
                                                    (xor (zext 64 (field zimm5)) (lit -1))))))))

  ;; ---- the refinement this composition exists for (MODEL-COMPOSE.6's anticipated case) ------
  ;; rv64i's ecall/ebreak REPORT a trap to the harness — that model has no privilege machinery.
  ;; Here the architecture DELIVERS the trap: delegation, the xPIE/xIE/xPP stack, xepc/xcause/
  ;; xtval and pc <- xtvec are trap-deliver's meaning; xepc gets the instruction's own address
  ;; (§2.1.3.1). The cause codes are the pinned causes.csv's.
  (sem (insn ecall) (source "RVP-MACHINE §2.1.3.1 — the cause names the ORIGINATING mode (U=8, S=9, M=11); xtval is 0 (measured on both reference models)")
       (effect (if (eq (mode) (lit 3))
                   (trap-deliver (lit 11) (lit 0))
                   (if (eq (mode) (lit 1))
                       (trap-deliver (lit 9) (lit 0))
                       (trap-deliver (lit 8) (lit 0))))))
  (sem (insn ebreak) (source "RVP-MACHINE §2.1.3.1 — cause 3 (breakpoint); xtval is the instruction's own address (measured tval=pc on both reference models)")
       (effect (trap-deliver (lit 3) (pc))))
)
