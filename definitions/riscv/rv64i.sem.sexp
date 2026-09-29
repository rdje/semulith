;; rv64i.sem.sexp — what each RV64I instruction DOES.
;;
;; ⛔ HAND-WRITTEN FROM THE PINNED SPECIFICATION, and deliberately NOT in the same file as the
;; encodings. `rv64i.sexp` is GENERATED from a machine-readable table and is regenerated whenever
;; that table moves; regenerating a file that also held hand-derived semantics would destroy them.
;; Generated and authored content have different provenance and must not share a file.
;;
;; Every rule carries the locator it was derived from, so a reviewer can check the expression
;; against the sentence. That is the whole evidence argument: a semantics nobody can trace back to
;; a document is a semantics nobody can dispute.
;;
;; ⚠️ WIDTHS ARE ALWAYS EXPLICIT. `(sext 64 (trunc 32 v))` says what it means; an implicit width is
;; where two models silently disagree. XLEN is 64 throughout this fragment.
;;
;; ⚠️ NOT VERIFIED CORRECT by existing here. `scripts/check_semantics.py` proves these are
;; well-formed, complete and cited. Proving them RIGHT is a differential experiment against a
;; reference model, which is what P0-PROFILE.6 does and what P1-LAB will do at scale.

(semantics
  (fragment "riscv/rv64i")
  (xlen 64)

  ;; ---- upper immediates -------------------------------------------------------------------
  (sem (insn lui)   (source "RVI-RV64I §3.1.2.1 — D-LUI-AUIPC")
       (effect (set (reg rd) (sext 64 (shl (imm imm20) (lit 12))))))
  (sem (insn auipc) (source "RVI-RV64I §3.1.2.1 — D-LUI-AUIPC; the offset is added to the address OF THIS INSTRUCTION")
       (effect (set (reg rd) (add (pc) (sext 64 (shl (imm imm20) (lit 12)))))))

  ;; ---- control transfer -------------------------------------------------------------------
  ;; ⛔ set-pc FIRST, the link write SECOND (P2-SCALAR.3, DEFECT-B): the target's alignment
  ;; check raises ON the jump (D-IALIGN/D-MISALIGN-REPORT), and an instruction that raises a
  ;; synchronous exception retires no architectural write — both references suppress the link
  ;; write on a misaligned target (measured). `(pc)` reads the frame's constant instruction
  ;; address, so the reorder is exact on the success path.
  (sem (insn jal)  (source "RVI-RV32I §1.1.5.1 — JAL adds the offset to THIS instruction's address and stores pc+4 in rd; the misaligned-target check precedes the link write (§1.1.5.2)")
       (effect (seq (set-pc (add (pc) (sext 64 (imm jimm20))))
                    (set (reg rd) (add (pc) (lit 4))))))
  (sem (insn jalr) (source "RVI-RV32I §1.1.5.1 — D-JALR-LSB: add, THEN set the least-significant bit to zero; the misaligned-target check precedes the link write (§1.1.5.2)")
       (effect (seq (set-pc (and (add (reg rs1) (sext 64 (imm imm12))) (lit -2)))
                    (set (reg rd) (add (pc) (lit 4))))))

  ;; ---- conditional branches; the offset is added to the BRANCH's address ------------------
  (sem (insn beq)  (source "RVI-RV32I §1.1.5.2")
       (effect (if (eq  (reg rs1) (reg rs2)) (set-pc (add (pc) (sext 64 (imm bimm12)))) (nop))))
  (sem (insn bne)  (source "RVI-RV32I §1.1.5.2")
       (effect (if (ne  (reg rs1) (reg rs2)) (set-pc (add (pc) (sext 64 (imm bimm12)))) (nop))))
  (sem (insn blt)  (source "RVI-RV32I §1.1.5.2 — signed comparison")
       (effect (if (lt  (reg rs1) (reg rs2)) (set-pc (add (pc) (sext 64 (imm bimm12)))) (nop))))
  (sem (insn bge)  (source "RVI-RV32I §1.1.5.2 — signed comparison")
       (effect (if (ge  (reg rs1) (reg rs2)) (set-pc (add (pc) (sext 64 (imm bimm12)))) (nop))))
  (sem (insn bltu) (source "RVI-RV32I §1.1.5.2 — unsigned comparison")
       (effect (if (ltu (reg rs1) (reg rs2)) (set-pc (add (pc) (sext 64 (imm bimm12)))) (nop))))
  (sem (insn bgeu) (source "RVI-RV32I §1.1.5.2 — unsigned comparison")
       (effect (if (geu (reg rs1) (reg rs2)) (set-pc (add (pc) (sext 64 (imm bimm12)))) (nop))))

  ;; ---- loads; D-LOAD-EXT gives the extension per width ------------------------------------
  (sem (insn lb)  (source "RVI-RV64I §3.1.3 — D-LOAD-EXT: LB sign-extends")
       (effect (set (reg rd) (sext 64 (load (lit 8)  (lit 1) (add (reg rs1) (sext 64 (imm imm12))))))))
  (sem (insn lh)  (source "RVI-RV64I §3.1.3 — D-LOAD-EXT: LH sign-extends")
       (effect (set (reg rd) (sext 64 (load (lit 16) (lit 1) (add (reg rs1) (sext 64 (imm imm12))))))))
  (sem (insn lw)  (source "RVI-RV64I §3.1.3 — D-LOAD-EXT: LW sign-extends its 32-bit result to 64 bits")
       (effect (set (reg rd) (sext 64 (load (lit 32) (lit 1) (add (reg rs1) (sext 64 (imm imm12))))))))
  (sem (insn lbu) (source "RVI-RV64I §3.1.3 — D-LOAD-EXT: LBU zero-extends")
       (effect (set (reg rd) (zext 64 (load (lit 8)  (lit 0) (add (reg rs1) (sext 64 (imm imm12))))))))
  (sem (insn lhu) (source "RVI-RV64I §3.1.3 — D-LOAD-EXT: LHU zero-extends")
       (effect (set (reg rd) (zext 64 (load (lit 16) (lit 0) (add (reg rs1) (sext 64 (imm imm12))))))))
  (sem (insn lwu) (source "RVI-RV64I §3.1.3 — D-LOAD-EXT: LWU zero-extends, and exists only at RV64")
       (effect (set (reg rd) (zext 64 (load (lit 32) (lit 0) (add (reg rs1) (sext 64 (imm imm12))))))))
  (sem (insn ld)  (source "RVI-RV64I §3.1.3 — a full XLEN load needs no extension")
       (effect (set (reg rd) (load (lit 64) (lit 0) (add (reg rs1) (sext 64 (imm imm12)))))))

  ;; ---- stores; each writes the LOW bits of rs2 --------------------------------------------
  (sem (insn sb) (source "RVI-RV64I §3.1.3 — SB stores the low 8 bits of rs2")
       (effect (store (lit 8)  (add (reg rs1) (sext 64 (imm imm12))) (trunc 8  (reg rs2)))))
  (sem (insn sh) (source "RVI-RV64I §3.1.3 — SH stores the low 16 bits of rs2")
       (effect (store (lit 16) (add (reg rs1) (sext 64 (imm imm12))) (trunc 16 (reg rs2)))))
  (sem (insn sw) (source "RVI-RV64I §3.1.3 — SW stores the low 32 bits of rs2")
       (effect (store (lit 32) (add (reg rs1) (sext 64 (imm imm12))) (trunc 32 (reg rs2)))))
  (sem (insn sd) (source "RVI-RV64I §3.1.3 — SD stores the low 64 bits of rs2")
       (effect (store (lit 64) (add (reg rs1) (sext 64 (imm imm12))) (reg rs2))))

  ;; ---- register-immediate ------------------------------------------------------------------
  (sem (insn addi)  (source "RVI-RV32I §1.1.4 — the immediate is sign-extended; overflow is ignored")
       (effect (set (reg rd) (add (reg rs1) (sext 64 (imm imm12))))))
  (sem (insn slti)  (source "RVI-RV32I §1.1.4 — signed comparison, result 0 or 1")
       (effect (set (reg rd) (slt  (reg rs1) (sext 64 (imm imm12))))))
  (sem (insn sltiu) (source "RVI-RV32I §1.1.4 — the immediate is still SIGN-extended, then compared UNSIGNED")
       (effect (set (reg rd) (sltu (reg rs1) (sext 64 (imm imm12))))))
  (sem (insn xori)  (source "RVI-RV32I §1.1.4") (effect (set (reg rd) (xor (reg rs1) (sext 64 (imm imm12))))))
  (sem (insn ori)   (source "RVI-RV32I §1.1.4") (effect (set (reg rd) (or  (reg rs1) (sext 64 (imm imm12))))))
  (sem (insn andi)  (source "RVI-RV32I §1.1.4") (effect (set (reg rd) (and (reg rs1) (sext 64 (imm imm12))))))
  (sem (insn slli)  (source "RVI-RV64I §3.1.2.1 — D-SHAMT: a 6-bit shift amount at XLEN=64")
       (effect (set (reg rd) (shl (reg rs1) (imm shamt)))))
  (sem (insn srli)  (source "RVI-RV64I §3.1.2.1 — D-SHAMT; logical, zeros shifted in")
       (effect (set (reg rd) (shr (reg rs1) (imm shamt)))))
  (sem (insn srai)  (source "RVI-RV64I §3.1.2.1 — D-SHAMT; arithmetic, the sign bit is replicated")
       (effect (set (reg rd) (sar (reg rs1) (imm shamt)))))

  ;; ---- register-register -------------------------------------------------------------------
  (sem (insn add)  (source "RVI-RV32I §1.1.4 — overflow ignored; the result wraps modulo 2^XLEN")
       (effect (set (reg rd) (add (reg rs1) (reg rs2)))))
  (sem (insn sub)  (source "RVI-RV32I §1.1.4") (effect (set (reg rd) (sub (reg rs1) (reg rs2)))))
  (sem (insn sll)  (source "RVI-RV64I §3.1.2.2 — D-SHAMT: only the low 6 bits of rs2 at XLEN=64")
       (effect (set (reg rd) (shl (reg rs1) (bits 5 0 (reg rs2))))))
  (sem (insn slt)  (source "RVI-RV32I §1.1.4") (effect (set (reg rd) (slt  (reg rs1) (reg rs2)))))
  (sem (insn sltu) (source "RVI-RV32I §1.1.4") (effect (set (reg rd) (sltu (reg rs1) (reg rs2)))))
  (sem (insn xor)  (source "RVI-RV32I §1.1.4") (effect (set (reg rd) (xor (reg rs1) (reg rs2)))))
  (sem (insn srl)  (source "RVI-RV64I §3.1.2.2 — D-SHAMT")
       (effect (set (reg rd) (shr (reg rs1) (bits 5 0 (reg rs2))))))
  (sem (insn sra)  (source "RVI-RV64I §3.1.2.2 — D-SHAMT")
       (effect (set (reg rd) (sar (reg rs1) (bits 5 0 (reg rs2))))))
  (sem (insn or)   (source "RVI-RV32I §1.1.4") (effect (set (reg rd) (or  (reg rs1) (reg rs2)))))
  (sem (insn and)  (source "RVI-RV32I §1.1.4") (effect (set (reg rd) (and (reg rs1) (reg rs2)))))

  ;; ---- the *W family: 32-bit result, SIGN-extended to 64 regardless of the operation -------
  ;; D-WSUFFIX. Every one of these truncates its inputs to 32, operates, and sign-extends.
  (sem (insn addiw) (source "RVI-RV64I §3.1.2 — D-WSUFFIX: overflow ignored, low 32 bits sign-extended")
       (effect (set (reg rd) (sext 64 (trunc 32 (add (trunc 32 (reg rs1)) (sext 32 (imm imm12))))))))
  (sem (insn slliw) (source "RVI-RV64I §3.1.2.1 — D-SHAMT: a 5-bit amount for the *W shifts")
       (effect (set (reg rd) (sext 64 (trunc 32 (shl (trunc 32 (reg rs1)) (imm shamt)))))))
  (sem (insn srliw) (source "RVI-RV64I §3.1.2.1 — logical, on the low 32 bits")
       (effect (set (reg rd) (sext 64 (trunc 32 (shr (trunc 32 (reg rs1)) (imm shamt)))))))
  (sem (insn sraiw) (source "RVI-RV64I §3.1.2.1 — arithmetic, on the low 32 bits")
       (effect (set (reg rd) (sext 64 (trunc 32 (sar (trunc 32 (reg rs1)) (imm shamt)))))))
  (sem (insn addw)  (source "RVI-RV64I §3.1.2.2 — D-WSUFFIX")
       (effect (set (reg rd) (sext 64 (trunc 32 (add (trunc 32 (reg rs1)) (trunc 32 (reg rs2))))))))
  (sem (insn subw)  (source "RVI-RV64I §3.1.2.2 — D-WSUFFIX")
       (effect (set (reg rd) (sext 64 (trunc 32 (sub (trunc 32 (reg rs1)) (trunc 32 (reg rs2))))))))
  (sem (insn sllw)  (source "RVI-RV64I §3.1.2.2 — the *W shifts use rs2[4:0], not rs2[5:0]")
       (effect (set (reg rd) (sext 64 (trunc 32 (shl (trunc 32 (reg rs1)) (bits 4 0 (reg rs2))))))))
  (sem (insn srlw)  (source "RVI-RV64I §3.1.2.2 — rs2[4:0]")
       (effect (set (reg rd) (sext 64 (trunc 32 (shr (trunc 32 (reg rs1)) (bits 4 0 (reg rs2))))))))
  (sem (insn sraw)  (source "RVI-RV64I §3.1.2.2 — rs2[4:0]")
       (effect (set (reg rd) (sext 64 (trunc 32 (sar (trunc 32 (reg rs1)) (bits 4 0 (reg rs2))))))))

  ;; ---- memory ordering and environment ----------------------------------------------------
  (sem (insn fence)  (source "RVI-RV32I §1.1.7 — D-FENCE: one hart, no devices, in-order; decoded, must not trap, no observable effect")
       (effect (nop)))
  (sem (insn ecall)  (source "RVI-RV32I §1.1.8 — D-ECALL-EBREAK: a precise REQUESTED trap to the execution environment")
       (effect (trap (lit 11) (lit 0))))
  (sem (insn ebreak) (source "RVI-RV32I §1.1.8 — D-ECALL-EBREAK: a precise REQUESTED trap; cause 3 is breakpoint")
       (effect (trap (lit 3) (pc)))))
