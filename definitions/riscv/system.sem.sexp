;; system.sem.sexp — what the privileged system instructions DO (mret, sret, wfi, sfence.vma
;; — the D-PRIV-INSNS selection, RVP-INSNS 18.1).
;;
;; ⛔ HAND-WRITTEN FROM THE PINNED SPECIFICATION. The stated, dated decisions (2026-10-03),
;; each with its authority:
;;
;; - WFI IS A NOP WHEN LEGAL (authority: laboratory). The specification permits it ("WFI may
;;   be implemented as a NOP", RVP-MACHINE §2.1.3.3); the wake event is P4-SYSTEM.5's, never
;;   this slice's. Legality, with the spec's latitudes resolved and recorded: illegal in U
;;   with S present (§2.1.3.3 — the bounded-time latitude is resolved FOR trapping, the
;;   deterministic choice); illegal in S with mstatus.TW=1 (§2.1.1.6.6 — the "may always
;;   raise" latitude, resolved the same way); always legal in M.
;;
;; - SFENCE.VMA'S INVALIDATION EFFECT IS A NOP AT THIS STAGE (authority: laboratory). The
;;   model implements no translation scheme and no address-translation cache (Sv39 is
;;   P4-SYSTEM.3), so there is nothing to invalidate — stated here, not silent. Its LEGALITY
;;   is fully modelled: illegal in U (RVP-SUPERVISOR §11.1.9's shared-permission sentence
;;   names SFENCE.VMA's permissions) and in S with mstatus.TVM=1 (RVP-MACHINE §2.1.1.6.6);
;;   TVM does not gate M.
;;
;; - THE mstatus BIT POSITIONS are the pinned encoding.h's masks (the specification renders
;;   the layouts only as figure images — the same re-pin family as the instruction tables):
;;   TSR=bit 22, TW=bit 21, TVM=bit 20 (MPRV=bit 17 is xret's internal concern).
;;
;; - INTERNAL STATE READS use csr-state, never csr-read: sret's TSR check, wfi's TW check and
;;   sfence.vma's TVM check are the machine inspecting its own state, not the instruction
;;   performing a CSR access — routing them through the permission model would trap an
;;   S-mode sret on the M-level mstatus address, and would recurse inside the gates
;;   themselves (schema/semantics.sexp says so at the operator).

(semantics
  (fragment "riscv/system")
  (xlen 64)

  (sem (insn mret) (source "RVP-MACHINE §2.1.3.2 — xRET executes in mode x or higher; in a less-privileged mode it raises illegal-instruction (xtval = the instruction word)")
       (effect (if (eq (mode) (lit 3))
                   (xret (lit 3))
                   (trap-deliver (lit 2) (inst)))))
  (sem (insn sret) (source "RVP-MACHINE §2.1.3.2 — legal in M and in S, illegal in U; in S with mstatus.TSR=1 it raises illegal-instruction (§2.1.1.6.6; TSR is bit 22, mstatus is 0x300 — the pinned encoding.h masks)")
       (effect (if (eq (mode) (lit 0))
                   (trap-deliver (lit 2) (inst))
                   (if (and (eq (mode) (lit 1))
                            (ne (bits 22 22 (csr-state (lit 768))) (lit 0)))
                       (trap-deliver (lit 2) (inst))
                       (xret (lit 1))))))
  (sem (insn wfi) (source "RVP-MACHINE §2.1.3.3 — a NOP when legal (the spec's own latitude; the wake is P4-SYSTEM.5's); illegal in U with S present, illegal in S with mstatus.TW=1 (§2.1.1.6.6; TW is bit 21); the latitudes are laboratory choices, recorded in the header")
       (effect (if (eq (mode) (lit 0))
                   (trap-deliver (lit 2) (inst))
                   (if (and (lt (mode) (lit 3))
                            (ne (bits 21 21 (csr-state (lit 768))) (lit 0)))
                       (trap-deliver (lit 2) (inst))
                       (nop)))))
  (sem (insn sfence.vma) (source "RVP-SUPERVISOR §11.1.2.1 — the translation fence; illegal in U (§11.1.9's shared-permission sentence) and in S with mstatus.TVM=1 (RVP-MACHINE §2.1.1.6.6; TVM is bit 20); the invalidation effect is a NOP at this stage — no translation caches are modelled (Sv39 is P4-SYSTEM.3), stated in the header")
       (effect (if (eq (mode) (lit 0))
                   (trap-deliver (lit 2) (inst))
                   (if (and (eq (mode) (lit 1))
                            (ne (bits 20 20 (csr-state (lit 768))) (lit 0)))
                       (trap-deliver (lit 2) (inst))
                       (nop)))))
)
