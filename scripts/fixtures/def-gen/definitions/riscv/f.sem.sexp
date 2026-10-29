;; f.sem.sexp — what each F-extension instruction DOES (the fragment's 30 forms: the FLW/FSW
;; transfers, the four fused multiply-adds, add/sub/mul/div/sqrt, sign injection, min/max, the
;; compares, fclass, the integer conversions, the FMV bit moves).
;;
;; ⛔ HAND-WRITTEN FROM THE PINNED SPECIFICATION, like rv64i.sem.sexp: every rule carries the
;; locator it was derived from, and generated encodings never share a file with authored
;; semantics.
;;
;; THE SHARED POLICIES ARE NOT IN THESE RULES, BY DESIGN. They are the floating-point block's
;; meaning (schema/semantics.sexp, P4-SYSTEM.7 slice c3), so every F instruction gets them
;; once: the Off gate (every rule below reads or writes the FP state, so every F instruction
;; is illegal at mstatus.FS = Off, judged before any effect); the canonical-NaN result; IEEE
;; rounding with subnormals and no flush; flag accrual into fflags with its Dirty rule; the
;; Dirty-on-f-write rule; the reserved-rounding-mode policy of (rounding …). What stays in
;; each rule is what the specification makes per-instruction: the operation, the operands'
;; register files, the NaN-boxing of a narrower value (FLEN = 64 — D is selected; RVI-D
;; §21.1.2), and the sign extensions the integer side requires.
;;
;; THE REGISTER FILE OF AN OPERAND is stated here and nowhere else: (freg x) names an
;; f-register, (reg x) an x-register. The pinned opcode rows name only the FIELD (rd/rs1/rs2/
;; rs3), so the assembler derives an operand's spelling (f0..f31 or x0..x31) from these rules
;; (scripts/riscv_asm.py) — derived, never typed.
;;
;; The negated fused forms negate an OPERAND by flipping its sign bit (XOR 0x80000000 on the
;; unboxed single): -(a×b)+c is fmadd(-a, b, c) with ONE rounding in every mode (the
;; operator's contract). The sign-injection forms are bit operations on the unboxed inputs —
;; they neither round, raise a flag, nor canonicalize a NaN.

(semantics
  (fragment "riscv/f")
  (xlen 64)

  ;; ---- loads and stores (RVI-F §20.1.5) — transfers: bits move unmodified, never unboxed ----
  (sem (insn flw) (source "RVI-F §20.1.5 — 'The FLW instruction loads a single-precision floating-point value from memory into floating-point register rd', base+offset like the integer loads; the 32 loaded bits are NaN-boxed into FLEN (RVI-D §21.1.2's transfer rule) and 'FLW and FSW do not modify the bits being transferred'")
       (effect (set (freg rd) (fbox 32 (load (lit 32) (lit 0) (add (reg rs1) (sext 64 (imm imm12))))))))
  (sem (insn fsw) (source "RVI-F §20.1.5 — 'FSW stores a single-precision value from floating-point register rs2 to memory': the register's low 32 bits, the upper FLEN-32 ignored (RVI-D §21.1.2's narrower-transfer rule), bits unmodified")
       (effect (store (lit 32) (add (reg rs1) (sext 64 (imm imm12))) (bits 31 0 (freg rs2)))))

  ;; ---- the fused multiply-adds (RVI-F §20.1.6) -------------------------------------------
  (sem (insn fmadd.s) (source "RVI-F §20.1.6 — 'FMADD.S computes (rs1×rs2)+rs3' with one rounding; ∞×0 raises NV even with a quiet-NaN addend (the operator's contract)")
       (effect (set (freg rd) (fbox 32 (fmadd 32 (rounding (field rm))
                                              (funbox 32 (freg rs1)) (funbox 32 (freg rs2)) (funbox 32 (freg rs3)))))))
  (sem (insn fmsub.s) (source "RVI-F §20.1.6 — 'FMSUB.S computes (rs1×rs2)−rs3': rs3's sign bit flipped into the one fused operation")
       (effect (set (freg rd) (fbox 32 (fmadd 32 (rounding (field rm))
                                              (funbox 32 (freg rs1)) (funbox 32 (freg rs2))
                                              (xor (funbox 32 (freg rs3)) (lit 0x80000000)))))))
  (sem (insn fnmsub.s) (source "RVI-F §20.1.6 — 'FNMSUB.S computes −(rs1×rs2)+rs3': rs1's sign bit flipped, so the product is negated before the single rounding")
       (effect (set (freg rd) (fbox 32 (fmadd 32 (rounding (field rm))
                                              (xor (funbox 32 (freg rs1)) (lit 0x80000000)) (funbox 32 (freg rs2))
                                              (funbox 32 (freg rs3)))))))
  (sem (insn fnmadd.s) (source "RVI-F §20.1.6 — 'FNMADD.S computes −(rs1×rs2)−rs3': rs1's and rs3's sign bits flipped")
       (effect (set (freg rd) (fbox 32 (fmadd 32 (rounding (field rm))
                                              (xor (funbox 32 (freg rs1)) (lit 0x80000000)) (funbox 32 (freg rs2))
                                              (xor (funbox 32 (freg rs3)) (lit 0x80000000)))))))

  ;; ---- add, subtract, multiply, divide, square root (RVI-F §20.1.6) ------------------------
  (sem (insn fadd.s) (source "RVI-F §20.1.6 — FADD.S performs 'single-precision floating-point addition' between rs1 and rs2, rounded by rm")
       (effect (set (freg rd) (fbox 32 (fadd 32 (rounding (field rm)) (funbox 32 (freg rs1)) (funbox 32 (freg rs2)))))))
  (sem (insn fsub.s) (source "RVI-F §20.1.6 — 'FSUB.S performs the single-precision floating-point subtraction of rs2 from rs1'")
       (effect (set (freg rd) (fbox 32 (fsub 32 (rounding (field rm)) (funbox 32 (freg rs1)) (funbox 32 (freg rs2)))))))
  (sem (insn fmul.s) (source "RVI-F §20.1.6 — FMUL.S performs single-precision floating-point multiplication between rs1 and rs2, rounded by rm")
       (effect (set (freg rd) (fbox 32 (fmul 32 (rounding (field rm)) (funbox 32 (freg rs1)) (funbox 32 (freg rs2)))))))
  (sem (insn fdiv.s) (source "RVI-F §20.1.6 — 'FDIV.S performs the single-precision floating-point division of rs1 by rs2'")
       (effect (set (freg rd) (fbox 32 (fdiv 32 (rounding (field rm)) (funbox 32 (freg rs1)) (funbox 32 (freg rs2)))))))
  (sem (insn fsqrt.s) (source "RVI-F §20.1.6 — 'FSQRT.S computes the square root of rs1'; the row's rs2 field is fixed 0")
       (effect (set (freg rd) (fbox 32 (fsqrt 32 (rounding (field rm)) (funbox 32 (freg rs1)))))))

  ;; ---- sign injection (RVI-F §20.1.7) — bit operations on the unboxed inputs ---------------
  (sem (insn fsgnj.s) (source "RVI-F §20.1.7 — the result 'takes all bits except the sign bit from rs1' and its sign bit is rs2's; 'Sign-injection instructions do not set floating-point exception flags, nor do they canonicalize NaNs'")
       (effect (set (freg rd) (fbox 32 (or (and (funbox 32 (freg rs1)) (lit 0x7fffffff))
                                           (and (funbox 32 (freg rs2)) (lit 0x80000000)))))))
  (sem (insn fsgnjn.s) (source "RVI-F §20.1.7 — 'for FSGNJN, the result’s sign bit is the opposite of rs2's sign bit'; the magnitude is rs1's")
       (effect (set (freg rd) (fbox 32 (or (and (funbox 32 (freg rs1)) (lit 0x7fffffff))
                                           (and (xor (funbox 32 (freg rs2)) (lit 0x80000000)) (lit 0x80000000)))))))
  (sem (insn fsgnjx.s) (source "RVI-F §20.1.7 — 'for FSGNJX, the sign bit is the XOR of the sign bits of rs1 and rs2'; the magnitude is rs1's")
       (effect (set (freg rd) (fbox 32 (xor (funbox 32 (freg rs1)) (and (funbox 32 (freg rs2)) (lit 0x80000000)))))))

  ;; ---- minimum / maximum (RVI-F §20.1.6) ---------------------------------------------------
  (sem (insn fmin.s) (source "RVI-F §20.1.6 — FMIN.S writes the smaller of rs1 and rs2 to rd; −0.0 < +0.0, NaN handling and NV per the operator's contract (minimumNumber)")
       (effect (set (freg rd) (fbox 32 (fmin 32 (funbox 32 (freg rs1)) (funbox 32 (freg rs2)))))))
  (sem (insn fmax.s) (source "RVI-F §20.1.6 — FMAX.S writes the larger of rs1 and rs2 to rd; −0.0 < +0.0, NaN handling and NV per the operator's contract (maximumNumber)")
       (effect (set (freg rd) (fbox 32 (fmax 32 (funbox 32 (freg rs1)) (funbox 32 (freg rs2)))))))

  ;; ---- conversions (RVI-F §20.1.7) ---------------------------------------------------------
  (sem (insn fcvt.w.s) (source "RVI-F §20.1.7 — FCVT.W.S converts rs1 to a signed 32-bit integer in rd, rounded by rm, clipped with NV out of range (Table 5); 'For XLEN>32, FCVT.W[U].S sign-extends the 32-bit result to the destination register width'")
       (effect (set (reg rd) (sext 64 (f2i 32 32 1 (rounding (field rm)) (funbox 32 (freg rs1)))))))
  (sem (insn fcvt.wu.s) (source "RVI-F §20.1.7 — FCVT.WU.S converts rs1 to an unsigned 32-bit integer, clipped with NV out of range (Table 5); the 32-bit result is sign-extended to XLEN like FCVT.W.S's")
       (effect (set (reg rd) (sext 64 (f2i 32 32 0 (rounding (field rm)) (funbox 32 (freg rs1)))))))
  (sem (insn fcvt.l.s) (source "RVI-F §20.1.7 — FCVT.L.S converts rs1 to a signed 64-bit integer in rd (RV64-only), clipped with NV out of range (Table 5)")
       (effect (set (reg rd) (f2i 32 64 1 (rounding (field rm)) (funbox 32 (freg rs1))))))
  (sem (insn fcvt.lu.s) (source "RVI-F §20.1.7 — FCVT.LU.S converts rs1 to an unsigned 64-bit integer in rd (RV64-only), clipped with NV out of range (Table 5)")
       (effect (set (reg rd) (f2i 32 64 0 (rounding (field rm)) (funbox 32 (freg rs1))))))
  (sem (insn fcvt.s.w) (source "RVI-F §20.1.7 — FCVT.S.W converts the signed 32-bit integer in rs1 to a single in rd, rounded by rm ('All floating-point to integer and integer to floating-point conversion instructions round according to the rm field')")
       (effect (set (freg rd) (fbox 32 (i2f 32 32 1 (rounding (field rm)) (reg rs1))))))
  (sem (insn fcvt.s.wu) (source "RVI-F §20.1.7 — FCVT.S.WU converts the unsigned 32-bit integer in rs1 to a single in rd, rounded by rm")
       (effect (set (freg rd) (fbox 32 (i2f 32 32 0 (rounding (field rm)) (reg rs1))))))
  (sem (insn fcvt.s.l) (source "RVI-F §20.1.7 — FCVT.S.L converts the signed 64-bit integer in rs1 to a single in rd, rounded by rm (RV64-only)")
       (effect (set (freg rd) (fbox 32 (i2f 32 64 1 (rounding (field rm)) (reg rs1))))))
  (sem (insn fcvt.s.lu) (source "RVI-F §20.1.7 — FCVT.S.LU converts the unsigned 64-bit integer in rs1 to a single in rd, rounded by rm (RV64-only)")
       (effect (set (freg rd) (fbox 32 (i2f 32 64 0 (rounding (field rm)) (reg rs1))))))

  ;; ---- bit moves (RVI-F §20.1.7) — transfers: never unboxed, never canonicalized ----------
  (sem (insn fmv.x.w) (source "RVI-F §20.1.7 — FMV.X.W moves rs1's single to 'the lower 32 bits of integer register rd'; 'For RV64, the higher 32 bits of the destination register are filled with copies of the floating-point number’s sign bit'")
       (effect (set (reg rd) (sext 64 (bits 31 0 (freg rs1))))))
  (sem (insn fmv.w.x) (source "RVI-F §20.1.7 — FMV.W.X moves the single 'from the lower 32 bits of integer register rs1 to the floating-point register rd'; 'The bits are not modified in the transfer' — NaN-boxed into FLEN")
       (effect (set (freg rd) (fbox 32 (bits 31 0 (reg rs1))))))

  ;; ---- compares (RVI-F §20.1.8) ------------------------------------------------------------
  (sem (insn feq.s) (source "RVI-F §20.1.8 — FEQ.S writes 1 to rd if rs1 = rs2, else 0; 'FEQ.S performs a quiet comparison'; 0 if either operand is NaN")
       (effect (set (reg rd) (feq 32 (funbox 32 (freg rs1)) (funbox 32 (freg rs2))))))
  (sem (insn flt.s) (source "RVI-F §20.1.8 — FLT.S writes 1 to rd if rs1 < rs2, else 0; a signaling comparison: NV 'if either input is NaN'")
       (effect (set (reg rd) (flt 32 (funbox 32 (freg rs1)) (funbox 32 (freg rs2))))))
  (sem (insn fle.s) (source "RVI-F §20.1.8 — FLE.S writes 1 to rd if rs1 ≤ rs2, else 0; a signaling comparison: NV 'if either input is NaN'")
       (effect (set (reg rd) (fle 32 (funbox 32 (freg rs1)) (funbox 32 (freg rs2))))))

  ;; ---- classify (RVI-F §20.1.9) ------------------------------------------------------------
  (sem (insn fclass.s) (source "RVI-F §20.1.9 — FCLASS.S 'writes to integer register rd a 10-bit mask that indicates the class of the floating-point number' (Table 6); 'FCLASS.S does not set the floating-point exception flags'")
       (effect (set (reg rd) (fclass 32 (funbox 32 (freg rs1))))))
)
