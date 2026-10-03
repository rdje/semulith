;; zicntr.sem.sexp — what the Zicntr counter reads DO.
;;
;; ⛔ HAND-WRITTEN FROM THE PINNED SPECIFICATION. The pseudo-semantics mechanism, measured at
;; P4-SYSTEM.2 slice b: rdcycle/rdtime/rdinstret exist upstream only as $pseudo_op rows of
;; csrrs (the rv_zicntr pin), so the fragment carries them as `(pseudo …)` — no encodings —
;; and a pseudo has its OWN name. The composition's refinement rule keys on names, so no
;; `(refines …)` is needed or possible: this rule IS the specialization of csrrs with
;; rs1=x0 (no write — RVI-ZICSR §5.1.1's discipline) and the row's fixed csr address, and it
;; is exact because the counter-enable gating is not repeated here — it lives in csr-read's
;; uniform permission model (RVP-MACHINE §2.1.1.11, RVP-SUPERVISOR §11.1.1.5), which the
;; csrrs rule these specialize uses identically. The decoder matches the word as csrrs (the
;; pseudo adds no encoding — definitions/riscv/zicntr.sexp); what THIS file records is what
;; the architectural spelling means, and the counter semantics (rate, wrap, progress) are
;; the environment contract's (P4-SYSTEM.5/.9), not this slice's.

(semantics
  (fragment "riscv/zicntr")
  (xlen 64)

  (sem (insn rdcycle) (source "RVI-ZICNTR §6.1.1 — reads the cycle counter (csr 0xC00, the pinned rv_zicntr row); counter-enable gating is csr-read's (RVP-MACHINE §2.1.1.11, RVP-SUPERVISOR §11.1.1.5)")
       (effect (set (reg rd) (csr-read (lit 3072)))))
  (sem (insn rdtime) (source "RVI-ZICNTR §6.1.1 — reads the time counter (csr 0xC01, the pinned rv_zicntr row); counter-enable gating is csr-read's (RVP-MACHINE §2.1.1.11, RVP-SUPERVISOR §11.1.1.5)")
       (effect (set (reg rd) (csr-read (lit 3073)))))
  (sem (insn rdinstret) (source "RVI-ZICNTR §6.1.1 — reads the instret counter (csr 0xC02, the pinned rv_zicntr row); counter-enable gating is csr-read's (RVP-MACHINE §2.1.1.11, RVP-SUPERVISOR §11.1.1.5)")
       (effect (set (reg rd) (csr-read (lit 3074)))))
)
