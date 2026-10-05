;; min-fencei.expected.sexp — the expected observations for `min-fencei.s` (P2-SCALAR.6;
;; mirrored to rv64gc-lab-v0 at P4-SYSTEM.2 slice (f), RE-DERIVED at slice (g), and
;; RE-DERIVED to the legal fence.i at P4-SYSTEM.6 slice (b) — the pre-commit fulfilled).
;; Validate with:
;;   python3 scripts/check_sexp_schema.py min-fencei.expected.sexp schema/expectations.sexp

(comment "min-fencei.expected.sexp — the expected observations for `min-fencei.s`." "" "⛔ RE-DERIVATION (P4-SYSTEM.6 slice b, THE BIND): the slice-(g) pre-commit is fulfilled —" "the slot is bound, so the one word of the minimal case decodes as fence.i and retires as" "the declared nop (RVI-ZIFENCEI §4.1; D-CODE-VISIBILITY). The count stays 1: the minimal" "guest's whole flow is the single retiring step; the illegal-instruction delivery that closed" "the pre-bind expectation is gone. No difference id — both sides execute it legally.")
(expectations (program "min-fencei.s") (entry "0x80000000") (instructions 1) (step (n 0) (insn ".word 0x0000100F") (writes) (derivation "0x0000100F is fence.i. The slot is bound, so the word matches the generated decode table's funct3+opcode mask (0x0000707f — the fields decoded-and-ignored per the chapter's shall-ignore rule) and retires as the declared nop: this machine re-reads memory on every fetch, so the chapter's coherent/uncached-RAM latitude leaves nothing to flush (D-CODE-VISIBILITY). The program runs off the end after the one retiring step.") (source "RVI-ZIFENCEI §4.1 — the declared nop; D-CODE-VISIBILITY")))
