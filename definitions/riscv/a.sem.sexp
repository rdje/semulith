;; a.sem.sexp — what each A-extension instruction DOES (Zaamo's nine AMOs and Zalrsc's
;; load-reserved/store-conditional pairs, each .W and .D — the fragment's 22 forms).
;;
;; ⛔ HAND-WRITTEN FROM THE PINNED SPECIFICATION, like rv64i.sem.sexp: every rule carries the
;; locator it was derived from, and generated encodings never share a file with authored
;; semantics.
;;
;; THE SHARED POLICIES ARE NOT IN THESE RULES, BY DESIGN. They are part of the operators'
;; meaning (schema/semantics.sexp's atomic block, P4-SYSTEM.4 slice b), so every A
;; instruction gets them once: the reservation contract (minimal exact set, physical-keyed;
;; any LR replaces, any SC clears, traps do not invalidate — decisions 2–4, RVI-A §12.1.2);
;; the deterministic SC policy (0 on success, 1 on failure, never spurious — decision 3,
;; laboratory authority); the AMO's store/AMO fault semantics (one translation, never a
;; load page fault — decision 5, RVP-SUPERVISOR); misaligned atomics taking the
;; access-fault cause 7 (decision 6, reference-matched to the pinned override's declared
;; PMAs). The failed SC's UNSPECIFIED translation side effects (§12.1.2) are DISCHARGED by
;; the profile's Svade: the named side effect is the PTE D-bit update Svade replaces with a
;; fault, so no side effect can exist. aq/rl decode and order nothing observable at one
;; hart (decision 1) — no rule below mentions them. The op literal in each AMO rule is the
;; operation's funct5 encoding, the value the instruction's own fixed bits carry
;; (definitions/riscv/a.sexp's 31..27 fields — derived, never typed).

(semantics
  (fragment "riscv/a")
  (xlen 64)

  ;; ---- Zalrsc: load-reserved / store-conditional (RVI-A §12.1.2) --------------------------
  (sem (insn lr.w) (source "RVI-A §12.1.2 — LR.W loads a word from rs1's address, sign-extends it into rd, and registers a reservation on the addressed bytes (the reservation contract is the operators', schema/semantics.sexp)")
       (effect (set (reg rd) (sext 64 (load-reserved (lit 32) (lit 1) (reg rs1))))))
  (sem (insn lr.d) (source "RVI-A §12.1.2 — LR.D loads a doubleword from rs1's address into rd and registers a reservation on the addressed bytes; a full XLEN load needs no extension")
       (effect (set (reg rd) (load-reserved (lit 64) (lit 0) (reg rs1)))))
  (sem (insn sc.w) (source "RVI-A §12.1.2 — SC.W conditionally stores rs2's low 32 bits to rs1's address and writes the code to rd (0 success / 1 failure; the deterministic never-spurious policy is decision 3's, stated at the operator); success or failure, the reservation is cleared — the section's own sentence")
       (effect (set (reg rd) (store-conditional (lit 32) (reg rs1) (trunc 32 (reg rs2))))))
  (sem (insn sc.d) (source "RVI-A §12.1.2 — SC.D conditionally stores rs2's 64 bits to rs1's address and writes the code to rd (0 success / 1 failure); success or failure, the reservation is cleared — the section's own sentence")
       (effect (set (reg rd) (store-conditional (lit 64) (reg rs1) (reg rs2)))))

  ;; ---- Zaamo: the nine atomic memory operations (RVI-A §12.1.4), .W and .D ----------------
  ;; One operator carries the read-modify-write with store/AMO fault semantics (decision 5);
  ;; rd gets the OLD memory value, sign-extended for .W (the section's own sentence: "and
  ;; places the value originally in memory, sign-extended, into register rd").
  (sem (insn amoadd.w) (source "RVI-A §12.1.4 — AMOADD.W atomically adds rs2's low 32 bits to the memory word at rs1's address and writes the OLD word, sign-extended, to rd (op 0x00, the encoding's own funct5)")
       (effect (set (reg rd) (sext 64 (amo (lit 0) (lit 32) (reg rs1) (trunc 32 (reg rs2)))))))
  (sem (insn amoadd.d) (source "RVI-A §12.1.4 — AMOADD.D atomically adds rs2's 64 bits to the memory doubleword at rs1's address and writes the OLD doubleword to rd (op 0x00, the encoding's own funct5)")
       (effect (set (reg rd) (amo (lit 0) (lit 64) (reg rs1) (reg rs2)))))
  (sem (insn amoswap.w) (source "RVI-A §12.1.4 — AMOSWAP.W atomically writes rs2's low 32 bits to the memory word at rs1's address and writes the OLD word, sign-extended, to rd (op 0x01, the encoding's own funct5)")
       (effect (set (reg rd) (sext 64 (amo (lit 1) (lit 32) (reg rs1) (trunc 32 (reg rs2)))))))
  (sem (insn amoswap.d) (source "RVI-A §12.1.4 — AMOSWAP.D atomically writes rs2's 64 bits to the memory doubleword at rs1's address and writes the OLD doubleword to rd (op 0x01, the encoding's own funct5)")
       (effect (set (reg rd) (amo (lit 1) (lit 64) (reg rs1) (reg rs2)))))
  (sem (insn amoxor.w) (source "RVI-A §12.1.4 — AMOXOR.W atomically XORs rs2's low 32 bits into the memory word at rs1's address and writes the OLD word, sign-extended, to rd (op 0x04, the encoding's own funct5)")
       (effect (set (reg rd) (sext 64 (amo (lit 4) (lit 32) (reg rs1) (trunc 32 (reg rs2)))))))
  (sem (insn amoxor.d) (source "RVI-A §12.1.4 — AMOXOR.D atomically XORs rs2's 64 bits into the memory doubleword at rs1's address and writes the OLD doubleword to rd (op 0x04, the encoding's own funct5)")
       (effect (set (reg rd) (amo (lit 4) (lit 64) (reg rs1) (reg rs2)))))
  (sem (insn amoand.w) (source "RVI-A §12.1.4 — AMOAND.W atomically ANDs rs2's low 32 bits into the memory word at rs1's address and writes the OLD word, sign-extended, to rd (op 0x0c, the encoding's own funct5)")
       (effect (set (reg rd) (sext 64 (amo (lit 12) (lit 32) (reg rs1) (trunc 32 (reg rs2)))))))
  (sem (insn amoand.d) (source "RVI-A §12.1.4 — AMOAND.D atomically ANDs rs2's 64 bits into the memory doubleword at rs1's address and writes the OLD doubleword to rd (op 0x0c, the encoding's own funct5)")
       (effect (set (reg rd) (amo (lit 12) (lit 64) (reg rs1) (reg rs2)))))
  (sem (insn amoor.w) (source "RVI-A §12.1.4 — AMOOR.W atomically ORs rs2's low 32 bits into the memory word at rs1's address and writes the OLD word, sign-extended, to rd (op 0x08, the encoding's own funct5)")
       (effect (set (reg rd) (sext 64 (amo (lit 8) (lit 32) (reg rs1) (trunc 32 (reg rs2)))))))
  (sem (insn amoor.d) (source "RVI-A §12.1.4 — AMOOR.D atomically ORs rs2's 64 bits into the memory doubleword at rs1's address and writes the OLD doubleword to rd (op 0x08, the encoding's own funct5)")
       (effect (set (reg rd) (amo (lit 8) (lit 64) (reg rs1) (reg rs2)))))
  (sem (insn amomin.w) (source "RVI-A §12.1.4 — AMOMIN.W atomically takes the signed minimum of the memory word at rs1's address and rs2's low 32 bits, and writes the OLD word, sign-extended, to rd (op 0x10, the encoding's own funct5)")
       (effect (set (reg rd) (sext 64 (amo (lit 16) (lit 32) (reg rs1) (trunc 32 (reg rs2)))))))
  (sem (insn amomin.d) (source "RVI-A §12.1.4 — AMOMIN.D atomically takes the signed minimum of the memory doubleword at rs1's address and rs2's 64 bits, and writes the OLD doubleword to rd (op 0x10, the encoding's own funct5)")
       (effect (set (reg rd) (amo (lit 16) (lit 64) (reg rs1) (reg rs2)))))
  (sem (insn amomax.w) (source "RVI-A §12.1.4 — AMOMAX.W atomically takes the signed maximum of the memory word at rs1's address and rs2's low 32 bits, and writes the OLD word, sign-extended, to rd (op 0x14, the encoding's own funct5)")
       (effect (set (reg rd) (sext 64 (amo (lit 20) (lit 32) (reg rs1) (trunc 32 (reg rs2)))))))
  (sem (insn amomax.d) (source "RVI-A §12.1.4 — AMOMAX.D atomically takes the signed maximum of the memory doubleword at rs1's address and rs2's 64 bits, and writes the OLD doubleword to rd (op 0x14, the encoding's own funct5)")
       (effect (set (reg rd) (amo (lit 20) (lit 64) (reg rs1) (reg rs2)))))
  (sem (insn amominu.w) (source "RVI-A §12.1.4 — AMOMINU.W atomically takes the unsigned minimum of the memory word at rs1's address and rs2's low 32 bits, and writes the OLD word, sign-extended, to rd (op 0x18, the encoding's own funct5)")
       (effect (set (reg rd) (sext 64 (amo (lit 24) (lit 32) (reg rs1) (trunc 32 (reg rs2)))))))
  (sem (insn amominu.d) (source "RVI-A §12.1.4 — AMOMINU.D atomically takes the unsigned minimum of the memory doubleword at rs1's address and rs2's 64 bits, and writes the OLD doubleword to rd (op 0x18, the encoding's own funct5)")
       (effect (set (reg rd) (amo (lit 24) (lit 64) (reg rs1) (reg rs2)))))
  (sem (insn amomaxu.w) (source "RVI-A §12.1.4 — AMOMAXU.W atomically takes the unsigned maximum of the memory word at rs1's address and rs2's low 32 bits, and writes the OLD word, sign-extended, to rd (op 0x1c, the encoding's own funct5)")
       (effect (set (reg rd) (sext 64 (amo (lit 28) (lit 32) (reg rs1) (trunc 32 (reg rs2)))))))
  (sem (insn amomaxu.d) (source "RVI-A §12.1.4 — AMOMAXU.D atomically takes the unsigned maximum of the memory doubleword at rs1's address and rs2's 64 bits, and writes the OLD doubleword to rd (op 0x1c, the encoding's own funct5)")
       (effect (set (reg rd) (amo (lit 28) (lit 64) (reg rs1) (reg rs2)))))
)
