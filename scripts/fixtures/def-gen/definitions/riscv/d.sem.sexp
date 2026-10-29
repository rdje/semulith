;; d.sem.sexp — what each D-extension instruction DOES (the fragment's 32 forms: the FLD/FSD
;; transfers, the four fused multiply-adds, add/sub/mul/div/sqrt, sign injection, min/max, the
;; two format conversions, the compares, fclass, the integer conversions, the FMV bit moves).
;;
;; ⛔ HAND-WRITTEN FROM THE PINNED SPECIFICATION, like f.sem.sexp: every rule carries the
;; locator it was derived from, and generated encodings never share a file with authored
;; semantics.
;;
;; THE SHARED POLICIES ARE NOT IN THESE RULES, BY DESIGN — the floating-point block's meaning
;; (schema/semantics.sexp, P4-SYSTEM.7 slice c3) gives every D instruction the Off gate, the
;; canonical-NaN result, IEEE rounding with subnormals, flag accrual with its Dirty rule, the
;; Dirty-on-f-write rule and the reserved-rounding-mode policy, exactly as it gives them to F.
;; The chapter defines most D instructions "analogously to their single-precision
;; counterparts" (RVI-D §21.1.4), so each rule below is its F counterpart at format 64.
;;
;; FLEN = 64, so a double IS the register: no (fbox 64 …)/(funbox 64 …) — both are the
;; identity at 64 (the operators' own contract) and a rule that wrote them would say nothing.
;; A D operation that reads a NaN-boxed single reads it as the 64-bit negative quiet NaN it
;; is (RVI-D §21.1.2: "Valid NaN-boxed n-bit values therefore appear as negative quiet NaNs").
;; The one operator D adds is the format conversion (f2f): FCVT.S.D boxes its single result,
;; FCVT.D.S unboxes its single operand — the narrower side follows the boxing rule.
;;
;; The negated fused forms negate an OPERAND by flipping its sign bit (XOR
;; 0x8000000000000000), as F's do at 32 bits; the sign-injection forms are bit operations —
;; they neither round, raise a flag, nor canonicalize a NaN.

(semantics
  (fragment "riscv/d")
  (xlen 64)

  ;; ---- loads and stores (RVI-D §21.1.3) — transfers: bits move unmodified ------------------
  (sem (insn fld) (source "RVI-D §21.1.3 — 'The FLD instruction loads a double-precision floating-point value from memory into floating-point register rd', base+offset like the integer loads; 'FLD and FSD do not modify the bits being transferred'")
       (effect (set (freg rd) (load (lit 64) (lit 0) (add (reg rs1) (sext 64 (imm imm12)))))))
  (sem (insn fsd) (source "RVI-D §21.1.3 — 'FSD stores a double-precision value from the floating-point registers to memory'; 'the payloads of non-canonical NaNs are preserved'")
       (effect (store (lit 64) (add (reg rs1) (sext 64 (imm imm12))) (freg rs2))))

  ;; ---- the fused multiply-adds (RVI-D §21.1.4: F's, at format 64) ---------------------------
  (sem (insn fmadd.d) (source "RVI-D §21.1.4 — the computational instructions 'are defined analogously to their single-precision counterparts, but operate on double-precision operands and produce double-precision results': FMADD.S's (rs1×rs2)+rs3 with one rounding")
       (effect (set (freg rd) (fmadd 64 (rounding (field rm)) (freg rs1) (freg rs2) (freg rs3)))))
  (sem (insn fmsub.d) (source "RVI-D §21.1.4 — FMSUB.S's (rs1×rs2)−rs3 at format 64: rs3's sign bit flipped into the one fused operation")
       (effect (set (freg rd) (fmadd 64 (rounding (field rm)) (freg rs1) (freg rs2)
                                     (xor (freg rs3) (lit 0x8000000000000000))))))
  (sem (insn fnmsub.d) (source "RVI-D §21.1.4 — FNMSUB.S's −(rs1×rs2)+rs3 at format 64: rs1's sign bit flipped, so the product is negated before the single rounding")
       (effect (set (freg rd) (fmadd 64 (rounding (field rm)) (xor (freg rs1) (lit 0x8000000000000000))
                                     (freg rs2) (freg rs3)))))
  (sem (insn fnmadd.d) (source "RVI-D §21.1.4 — FNMADD.S's −(rs1×rs2)−rs3 at format 64: rs1's and rs3's sign bits flipped")
       (effect (set (freg rd) (fmadd 64 (rounding (field rm)) (xor (freg rs1) (lit 0x8000000000000000))
                                     (freg rs2) (xor (freg rs3) (lit 0x8000000000000000))))))

  ;; ---- add, subtract, multiply, divide, square root (RVI-D §21.1.4) -----------------------
  (sem (insn fadd.d) (source "RVI-D §21.1.4 — FADD.S's addition at format 64, rounded by rm")
       (effect (set (freg rd) (fadd 64 (rounding (field rm)) (freg rs1) (freg rs2)))))
  (sem (insn fsub.d) (source "RVI-D §21.1.4 — FSUB.S's subtraction of rs2 from rs1 at format 64, rounded by rm")
       (effect (set (freg rd) (fsub 64 (rounding (field rm)) (freg rs1) (freg rs2)))))
  (sem (insn fmul.d) (source "RVI-D §21.1.4 — FMUL.S's multiplication at format 64, rounded by rm")
       (effect (set (freg rd) (fmul 64 (rounding (field rm)) (freg rs1) (freg rs2)))))
  (sem (insn fdiv.d) (source "RVI-D §21.1.4 — FDIV.S's division of rs1 by rs2 at format 64, rounded by rm")
       (effect (set (freg rd) (fdiv 64 (rounding (field rm)) (freg rs1) (freg rs2)))))
  (sem (insn fsqrt.d) (source "RVI-D §21.1.4 — FSQRT.S's square root of rs1 at format 64; the row's rs2 field is fixed 0")
       (effect (set (freg rd) (fsqrt 64 (rounding (field rm)) (freg rs1)))))

  ;; ---- sign injection (RVI-D §21.1.5) — bit operations ------------------------------------
  (sem (insn fsgnj.d) (source "RVI-D §21.1.5 — 'Floating-point to floating-point sign-injection instructions, FSGNJ.D, FSGNJN.D, and FSGNJX.D are defined analogously to the single-precision sign-injection instruction': rs1's magnitude, rs2's sign")
       (effect (set (freg rd) (or (and (freg rs1) (lit 0x7fffffffffffffff))
                                  (and (freg rs2) (lit 0x8000000000000000))))))
  (sem (insn fsgnjn.d) (source "RVI-D §21.1.5 — FSGNJN.S's rule at format 64: rs1's magnitude, the opposite of rs2's sign")
       (effect (set (freg rd) (or (and (freg rs1) (lit 0x7fffffffffffffff))
                                  (and (xor (freg rs2) (lit 0x8000000000000000)) (lit 0x8000000000000000))))))
  (sem (insn fsgnjx.d) (source "RVI-D §21.1.5 — FSGNJX.S's rule at format 64: rs1's magnitude, the XOR of the two signs")
       (effect (set (freg rd) (xor (freg rs1) (and (freg rs2) (lit 0x8000000000000000))))))

  ;; ---- minimum / maximum (RVI-D §21.1.4) ---------------------------------------------------
  (sem (insn fmin.d) (source "RVI-D §21.1.4 — FMIN.S's minimumNumber at format 64 (−0.0 < +0.0, NaN handling and NV per the operator's contract)")
       (effect (set (freg rd) (fmin 64 (freg rs1) (freg rs2)))))
  (sem (insn fmax.d) (source "RVI-D §21.1.4 — FMAX.S's maximumNumber at format 64 (−0.0 < +0.0, NaN handling and NV per the operator's contract)")
       (effect (set (freg rd) (fmax 64 (freg rs1) (freg rs2)))))

  ;; ---- the format conversions (RVI-D §21.1.5) — the one operator D adds --------------------
  (sem (insn fcvt.s.d) (source "RVI-D §21.1.5 — 'FCVT.S.D rounds according to the RM field': the double in rs1 narrowed to a single, NaN-boxed into rd")
       (effect (set (freg rd) (fbox 32 (f2f 32 64 (rounding (field rm)) (freg rs1))))))
  (sem (insn fcvt.d.s) (source "RVI-D §21.1.5 — 'FCVT.D.S will never round': the single in rs1 (unboxed) widened exactly; its rm is still resolved (the reserved-mode decode)")
       (effect (set (freg rd) (f2f 64 32 (rounding (field rm)) (funbox 32 (freg rs1))))))

  ;; ---- integer conversions (RVI-D §21.1.5) -------------------------------------------------
  (sem (insn fcvt.w.d) (source "RVI-D §21.1.5 — 'FCVT.W.D or FCVT.L.D converts a double-precision floating-point number in floating-point register rs1 to a signed 32-bit or 64-bit integer'; 'For RV64, FCVT.W[U].D sign-extends the 32-bit result'; the invalid-input behavior is FCVT.int.S's")
       (effect (set (reg rd) (sext 64 (f2i 64 32 1 (rounding (field rm)) (freg rs1))))))
  (sem (insn fcvt.wu.d) (source "RVI-D §21.1.5 — FCVT.WU.D converts rs1 to an unsigned 32-bit integer, 'the same as for FCVT.int.S' out of range; the 32-bit result sign-extended to XLEN")
       (effect (set (reg rd) (sext 64 (f2i 64 32 0 (rounding (field rm)) (freg rs1))))))
  (sem (insn fcvt.l.d) (source "RVI-D §21.1.5 — FCVT.L.D converts rs1 to a signed 64-bit integer; 'FCVT.L[U].D and FCVT.D.L[U] are RV64-only instructions'")
       (effect (set (reg rd) (f2i 64 64 1 (rounding (field rm)) (freg rs1)))))
  (sem (insn fcvt.lu.d) (source "RVI-D §21.1.5 — FCVT.LU.D converts rs1 to an unsigned 64-bit integer (RV64-only), clipped with NV out of range as FCVT.int.S")
       (effect (set (reg rd) (f2i 64 64 0 (rounding (field rm)) (freg rs1)))))
  (sem (insn fcvt.d.w) (source "RVI-D §21.1.5 — FCVT.D.W converts the signed 32-bit integer in rs1 to a double in rd; 'Note FCVT.D.W[U] always produces an exact result and is unaffected by rounding mode' — its rm is still resolved (the reserved-mode decode)")
       (effect (set (freg rd) (i2f 64 32 1 (rounding (field rm)) (reg rs1)))))
  (sem (insn fcvt.d.wu) (source "RVI-D §21.1.5 — FCVT.D.WU converts the unsigned 32-bit integer in rs1 to a double in rd, exactly")
       (effect (set (freg rd) (i2f 64 32 0 (rounding (field rm)) (reg rs1)))))
  (sem (insn fcvt.d.l) (source "RVI-D §21.1.5 — FCVT.D.L converts the signed 64-bit integer in rs1 to a double in rd, rounded by rm ('All floating-point to integer and integer to floating-point conversion instructions round according to the rm field')")
       (effect (set (freg rd) (i2f 64 64 1 (rounding (field rm)) (reg rs1)))))
  (sem (insn fcvt.d.lu) (source "RVI-D §21.1.5 — FCVT.D.LU converts the unsigned 64-bit integer in rs1 to a double in rd, rounded by rm (RV64-only)")
       (effect (set (freg rd) (i2f 64 64 0 (rounding (field rm)) (reg rs1)))))

  ;; ---- bit moves (RVI-D §21.1.5) — transfers: never canonicalized ---------------------------
  (sem (insn fmv.x.d) (source "RVI-D §21.1.5 — 'FMV.X.D moves the double-precision value in floating-point register rs1 to a representation in IEEE 754-2008 standard encoding in integer register rd'; 'FMV.X.D and FMV.D.X do not modify the bits being transferred'")
       (effect (set (reg rd) (freg rs1))))
  (sem (insn fmv.d.x) (source "RVI-D §21.1.5 — 'FMV.D.X moves the double-precision value encoded in IEEE 754-2008 standard encoding from the integer register rs1 to the floating-point register rd'")
       (effect (set (freg rd) (reg rs1))))

  ;; ---- compares (RVI-D §21.1.6) ------------------------------------------------------------
  (sem (insn feq.d) (source "RVI-D §21.1.6 — the compares 'are defined analogously to their single-precision counterparts, but operate on double-precision operands': FEQ.S's quiet comparison at format 64")
       (effect (set (reg rd) (feq 64 (freg rs1) (freg rs2)))))
  (sem (insn flt.d) (source "RVI-D §21.1.6 — FLT.S's signaling comparison at format 64: NV for any NaN input")
       (effect (set (reg rd) (flt 64 (freg rs1) (freg rs2)))))
  (sem (insn fle.d) (source "RVI-D §21.1.6 — FLE.S's signaling comparison at format 64: NV for any NaN input")
       (effect (set (reg rd) (fle 64 (freg rs1) (freg rs2)))))

  ;; ---- classify (RVI-D §21.1.7) ------------------------------------------------------------
  (sem (insn fclass.d) (source "RVI-D §21.1.7 — 'FCLASS.D, is defined analogously to its single-precision counterpart, but operates on double-precision operands': FCLASS.S's 10-bit mask at format 64, no flag")
       (effect (set (reg rd) (fclass 64 (freg rs1)))))
)
