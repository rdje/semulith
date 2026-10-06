;; m.sem.sexp — what each M-extension instruction DOES (the fragment's 13 forms: MUL, MULH, MULHSU,
;; MULHU, DIV, DIVU, REM, REMU, and the RV64 word forms MULW, DIVW, DIVUW, REMW, REMUW).
;;
;; ⛔ HAND-WRITTEN FROM THE PINNED SPECIFICATION (RVI-M, the v20260120 snapshot's §11.1), like
;; rv64i.sem.sexp: every rule carries the locator it was derived from, and generated encodings
;; never share a file with authored semantics.
;;
;; THE ISA'S CHOICES ARE IN THESE RULES, BY DESIGN (P4-SYSTEM.11 slice a). The operators are
;; arithmetic only (schema/semantics.sexp's multiply/divide block), and a zero divisor is outside
;; their domain — so what RISC-V makes division by zero yield (RVI-M §11.1.2, Table 1: the
;; quotient has all bits set, the remainder equals the dividend; the word forms sign-extend both)
;; is stated HERE, by a guard on the divisor, and check_semantics refuses a division no guard
;; covers. Signed overflow needs no guard: the operators wrap, and the wrapped results ARE the
;; table's overflow row (quotient the dividend, remainder 0). The word forms follow addw's shape:
;; operate on (trunc 32 …), then (sext 64 (trunc 32 …)) the result.

(semantics (fragment "riscv/m") (xlen 64)
  (sem (insn mul)    (source "RVI-M §11.1.1 — MUL \"places the lower XLEN bits in the destination register\"")
       (effect (set (reg rd) (mul (reg rs1) (reg rs2)))))
  (sem (insn mulh)   (source "RVI-M §11.1.1 — the upper XLEN bits of the full 2×XLEN-bit product, signed×signed")
       (effect (set (reg rd) (mulh (reg rs1) (reg rs2)))))
  (sem (insn mulhsu) (source "RVI-M §11.1.1 — the upper XLEN bits of the full 2×XLEN-bit product, signed rs1 × unsigned rs2")
       (effect (set (reg rd) (mulhsu (reg rs1) (reg rs2)))))
  (sem (insn mulhu)  (source "RVI-M §11.1.1 — the upper XLEN bits of the full 2×XLEN-bit product, unsigned×unsigned")
       (effect (set (reg rd) (mulhu (reg rs1) (reg rs2)))))
  (sem (insn mulw)   (source "RVI-M §11.1.1 — MULW \"multiplies the lower 32 bits of the source registers, placing the sign extension of the lower 32 bits of the result into the destination register\"")
       (effect (set (reg rd) (sext 64 (trunc 32 (mul (trunc 32 (reg rs1)) (trunc 32 (reg rs2))))))))

  (sem (insn div)    (source "RVI-M §11.1.2 — signed division rounding towards zero; Table 1: a zero divisor yields a quotient with all bits set, overflow the dividend (the operator's wrap)")
       (effect (if (eq (reg rs2) (lit 0))
                   (set (reg rd) (lit -1))
                   (set (reg rd) (div (reg rs1) (reg rs2))))))
  (sem (insn divu)   (source "RVI-M §11.1.2 — unsigned division; Table 1: a zero divisor yields 2^XLEN − 1, all bits set")
       (effect (if (eq (reg rs2) (lit 0))
                   (set (reg rd) (lit -1))
                   (set (reg rd) (divu (reg rs1) (reg rs2))))))
  (sem (insn rem)    (source "RVI-M §11.1.2 — \"For REM, the sign of a nonzero result equals the sign of the dividend\"; Table 1: a zero divisor yields the dividend, overflow 0 (the operator's wrap)")
       (effect (if (eq (reg rs2) (lit 0))
                   (set (reg rd) (reg rs1))
                   (set (reg rd) (rem (reg rs1) (reg rs2))))))
  (sem (insn remu)   (source "RVI-M §11.1.2 — the unsigned remainder; Table 1: a zero divisor yields the dividend")
       (effect (if (eq (reg rs2) (lit 0))
                   (set (reg rd) (reg rs1))
                   (set (reg rd) (remu (reg rs1) (reg rs2))))))

  (sem (insn divw)   (source "RVI-M §11.1.2 — DIVW divides the lower 32 bits of rs1 by the lower 32 bits of rs2 as signed integers, the 32-bit quotient sign-extended; Table 1 at L = 32")
       (effect (if (eq (trunc 32 (reg rs2)) (lit 0))
                   (set (reg rd) (sext 64 (trunc 32 (lit -1))))
                   (set (reg rd) (sext 64 (trunc 32 (div (trunc 32 (reg rs1)) (trunc 32 (reg rs2)))))))))
  (sem (insn divuw)  (source "RVI-M §11.1.2 — DIVUW as unsigned integers, the 32-bit quotient sign-extended; Table 1 at L = 32: 2^32 − 1")
       (effect (if (eq (trunc 32 (reg rs2)) (lit 0))
                   (set (reg rd) (sext 64 (trunc 32 (lit -1))))
                   (set (reg rd) (sext 64 (trunc 32 (divu (trunc 32 (reg rs1)) (trunc 32 (reg rs2)))))))))
  (sem (insn remw)   (source "RVI-M §11.1.2 — \"Both REMW and REMUW always sign-extend the 32-bit result to 64 bits, including on a divide by zero\"")
       (effect (if (eq (trunc 32 (reg rs2)) (lit 0))
                   (set (reg rd) (sext 64 (trunc 32 (reg rs1))))
                   (set (reg rd) (sext 64 (trunc 32 (rem (trunc 32 (reg rs1)) (trunc 32 (reg rs2)))))))))
  (sem (insn remuw)  (source "RVI-M §11.1.2 — \"Both REMW and REMUW always sign-extend the 32-bit result to 64 bits, including on a divide by zero\"")
       (effect (if (eq (trunc 32 (reg rs2)) (lit 0))
                   (set (reg rd) (sext 64 (trunc 32 (reg rs1))))
                   (set (reg rd) (sext 64 (trunc 32 (remu (trunc 32 (reg rs1)) (trunc 32 (reg rs2))))))))))
