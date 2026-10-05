;; a-lrsc-loop.expected.sexp — the expected observations for `a-lrsc-loop.s` (P4-SYSTEM.4
;; slice d, the atomics corpus). EVD-05: every value below was derived from the pinned
;; chapters and the declared deterministic SC policy (state.sexp) by the spec-side
;; authoring model BEFORE any engine run; the corpus runner falsifies against it.
;; Validate with
;;   python3 scripts/check_sexp_schema.py a-lrsc-loop.expected.sexp schema/expectations.sexp

(expectations (program "a-lrsc-loop.s") (entry "0x0000000080000000") (instructions 11)
  (never_written "x28")
  (never_written "x29")
  (step (n 0) (insn "addi x10, x0, 1") (writes (write (reg "x10") (value "0x0000000000000001")))
    (derivation "raw material for the region base.") (source "RVI-RV32I §1.1.4"))
  (step (n 1) (insn "slli x10, x10, 31") (writes (write (reg "x10") (value "0x0000000080000000")))
    (derivation "x10 = 0x8000_0000.") (source "RVI-RV64I §3.1.2.1"))
  (step (n 2) (insn "addi x1, x10, 256") (writes (write (reg "x1") (value "0x0000000080000100")))
    (derivation "the counter's address.") (source "RVI-RV32I §1.1.4"))
  (step (n 3) (insn "addi x7, x0, 41") (writes (write (reg "x7") (value "0x0000000000000029")))
    (derivation "the initial count.") (source "RVI-RV32I §1.1.4"))
  (step (n 4) (insn "sw x7, 0, x1") (writes)
    (derivation "mem = 41.") (source "RVI-RV64I §3.1.3"))
  (step (n 5) (insn "lr.w x5, (x1)") (writes (write (reg "x5") (value "0x0000000000000029")))
    (derivation "the sequence begins: reserve and load 41.") (source "RVI-A §12.1.3"))
  (step (n 6) (insn "addi x5, x5, 1") (writes (write (reg "x5") (value "0x000000000000002a")))
    (derivation "the critical section: 42 — base-I only, same address and size, well under 16 instructions.") (source "RVI-A §12.1.3"))
  (step (n 7) (insn "sc.w x6, x5, (x1)") (writes)
    (derivation "the FIRST SC succeeds under the declared never-spurious policy: rd <- 0, mem <- 42.") (source "RVI-A §12.1.3; state.sexp's reservation candidate (decision 3)"))
  (step (n 8) (insn "bne x6, x0, retry") (writes)
    (derivation "code 0: the retry branch is NOT taken — the degenerate one-hart eventuality, recorded.") (source "RVI-A §12.1.3"))
  (step (n 9) (insn "sw x5, 8, x1") (writes)
    (derivation "the landing marker: 42 stored beside the counter — proof the flow arrived past the loop.") (source "RVI-RV64I §3.1.3"))
  (step (n 10) (insn "lw x8, x1, 0") (writes (write (reg "x8") (value "0x000000000000002a")))
    (derivation "read-back of the counter: 42.") (source "RVI-RV64I §3.1.3"))
)
