;; fencei-selfmod.expected.sexp — the expected observations for `fencei-selfmod.s` (P4-SYSTEM.5
;; slice b, the interrupts corpus). EVD-05: every value below was derived from the pinned
;; chapters and the .5 brief's declared delivery rule by the spec-side authoring model
;; BEFORE any engine run; the corpus runner falsifies against it.
;; Validate with
;;   python3 scripts/check_sexp_schema.py fencei-selfmod.expected.sexp schema/expectations.sexp

(expectations (program "fencei-selfmod.s") (entry "0x0000000080000000") (instructions 8)
  (never_written "x28")
  (never_written "x29")
  (step (n 0) (insn "lui   x1, 0x00700") (writes (write (reg "x1") (value "0x0000000000700000")))
    (derivation "x1 = 0x00700000.") (source "RVI-RV32I §1.1.4 (D-LUI-AUIPC)"))
  (step (n 1) (insn "addi  x1, x1, 0x113") (writes (write (reg "x1") (value "0x0000000000700113")))
    (derivation "x1 = 0x00700113 — the encoding of `addi x2, x0, 7`, assembled from the encoding rule, never read back from any model.") (source "RVI-RV32I §1.1.4; §1.1.2 (the I-format layout)"))
  (step (n 2) (insn "auipc x3, 0") (writes (write (reg "x3") (value "0x0000000080000008")))
    (derivation "x3 = this instruction's own address (entry+0x08).") (source "RVI-RV32I §1.1.4 (D-LUI-AUIPC)"))
  (step (n 3) (insn "sw    x1, 16, x3") (writes)
    (derivation "[entry+0x18] <- the patch: the word three steps down.") (source "RVI-RV32I §1.1.6"))
  (step (n 4) (insn "fence.i") (writes)
    (derivation "THE ARCHITECTURAL SYNCHRONIZATION, executed and legal (the slot bound at slice b): it orders the store before every later fetch — and on this machine it retires as the declared nop, the coherent-latitude landing (nothing to flush).") (source "RVI-ZIFENCEI §4.1; the .6 brief's decision 2"))
  (step (n 5) (insn "addi  x4, x0, 4") (writes (write (reg "x4") (value "0x0000000000000004")))
    (derivation "an ordinary write between the fence.i and the target.") (source "RVI-RV32I §1.1.4"))
  (step (n 6) (insn "addi  x2, x0, 2 (patched: the word now reads 0x00700113)") (writes (write (reg "x2") (value "0x0000000000000007")))
    (derivation "entry+0x18, fetched AFTER the store and the fence.i: executes as `addi x2, x0, 7` — the patched instruction observed through its effects (D-CODE-VISIBILITY — immediate visibility is the laboratory's declared choice, a legal subset of the chapter's may-or-may-not).") (source "RVI-ZIFENCEI §4.1; D-CODE-VISIBILITY"))
  (step (n 7) (insn "addi  x5, x0, 5") (writes (write (reg "x5") (value "0x0000000000000005")))
    (derivation "the landing: the patch, the synchronization and the patched fetch all retired.") (source "RVI-RV32I §1.1.4 #|end"))
)
