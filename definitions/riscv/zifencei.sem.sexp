;; zifencei.sem.sexp — what the Zifencei instruction DOES (fence.i, the one form the
;; pinned table carries).
;;
;; ⛔ HAND-WRITTEN FROM THE PINNED SPECIFICATION. The stated, dated decisions (2026-10-05),
;; each with its authority:
;;
;; - FENCE.I'S EFFECT IS THE DECLARED NOP (authority: laboratory, the chapter's own
;;   implementation latitude). The chapter's contract is three sentences (zifencei.html,
;;   Version 2.0 measured from the page title): "RISC-V does not guarantee that stores to
;;   instruction memory will be made visible to instruction fetches on a RISC-V hart until
;;   that hart executes a FENCE.I instruction"; "A FENCE.I instruction ensures that a
;;   subsequent instruction fetch on a RISC-V hart will see any previous data stores
;;   already visible to the same RISC-V hart"; "A FENCE.I instruction orders all explicit
;;   memory accesses that precede the FENCE.I in program order before all instruction
;;   fetches that follow the FENCE.I in program order. An instruction fetch is always
;;   ordered before any explicit memory accesses that instruction gives rise to." The
;;   latitude that sanctions the nop: "if instruction and data caches are kept coherent
;;   in this way, or if the memory system consists of only uncached RAMs, then just the
;;   fetch pipeline needs to be flushed at a FENCE.I" — and this machine re-reads memory
;;   on every fetch (D-CODE-VISIBILITY: no instruction-fetch cache state exists, the state
;;   document's `present false` census candidate), so there is nothing to flush. The
;;   synchronization is therefore ALREADY provided; the fence's retirement is the whole
;;   contract. Sail 0.14 lands identically ("fence.i is a nop for the memory model",
;;   extensions/Zifencei/zifencei_insts.sail) — the matched experiment can AGREE rather
;;   than recorded-diverge (P4-SYSTEM.6 decision 2).
;;
;; - THE RESERVED FIELDS ARE DECODED-AND-IGNORED, NEVER REJECTED. "The unused fields in
;;   the FENCE.I instruction, funct12, rs1, and rd, are reserved for finer-grain fences in
;;   future extensions. For forward compatibility, base implementations shall ignore these
;;   fields, and standard software shall zero these fields." So a fence.i word with
;;   NONZERO funct12/rs1/rd EXECUTES (the forward-compatibility rule — the
;;   reserved-fields cell is P4-SYSTEM.6 decision 5's, slice b), and the zero-operand
;;   `fence.i` spelling is the standard-software spelling the assembler accepts (the
;;   ecall/ebreak zero-operand precedent). No legalization arm exists or is needed: the
;;   chapter names no illegal encoding.

(semantics
  (fragment "riscv/zifencei")
  (xlen 64)

  (sem (insn fence.i) (source "RVI-ZIFENCEI §4.1 — the declared nop: the coherent/uncached-RAM latitude ('just the fetch pipeline needs to be flushed at a FENCE.I') meets a re-read-per-fetch machine (nothing to flush, D-CODE-VISIBILITY); funct12/rs1/rd decoded-and-ignored per the chapter's shall-ignore rule, never legalization-rejected")
       (effect (nop))))
