;; interactions.sexp — the declared fault × alias × boundary × legality × delegation ×
;; progress × restart interaction matrix of `rv64gc-lab-v0` (P4-SYSTEM.2 slice g).
;; Validate with:
;;   python3 scripts/check_sexp_schema.py interactions.sexp schema/interactions.sexp
;; Rehearse (staged; the gate's driver discovers tracked profiles/*/ at the flip):
;;   python3 scripts/check_interaction_matrix.py <this unit dir>
;;
;; DECLARED FIRST, THEN EXERCISED. The seven axes are the leaf's own vocabulary — the
;; four layers the mirrored base corpus already carries (fault, alias, boundary, progress,
;; from P2-SCALAR.2/.3) plus the three the privileged machinery adds (legality, delegation,
;; and restart REFRAMED): rv64i's event axis (requested traps) is absorbed — ecall/ebreak
;; are now the mode-cause and delegation story — and rv64i's mechanism-shaped restart axis
;; becomes GUEST-shaped here: the xret/xepc return discipline is observable by guests.
;;   fault      trap delivery: the cause/xtval/xepc vocabulary, fault priority, suppressed
;;              effects — every target-visible fault DELIVERED on this composition (the
;;              zicsr refinement), never merely reported
;;   alias      register aliasing: rd=rs overlaps, x0 hardwired in both directions — the
;;              base layer, plus CSR accesses with x0 destinations
;;   boundary   data-domain edges: wraps, sign edges, shift-amount domains, address
;;              extremes — mode-agnostic by construction
;;   legality   permission and refusal: mode-dependent legality of instructions and CSR
;;              accesses (M/S/U, the TW/TVM/TSR gates, read-only and WARL), and encoding
;;              validity (the reserved/refused forms)
;;   delegation interception routing: medeleg, mcounteren/scounteren, STCE — which agent
;;              (M or S) a trap or an access reaches
;;   progress   every step's effect visible; continuation PAST a delivered trap; wfi as a
;;              nop; the budget contract
;;   restart    the xret/xepc return discipline: resumption of preempted control flow at
;;              the recorded address and mode (mret/sret, SPP/MPP, the MPRV rule)
;; `P4-SYSTEM.6` slice (b) (`2026-10-05`): the fence.i bind rides the SAME seven axes —
;; the retiring fence.i and the reserved-fields word are the legality axis's
;; decode-vs-reject vocabulary (the shall-ignore rule), the re-derived fencei guests are
;; the fault axis's cause-2 vocabulary measured GONE by design (the trap that was),
;; and the rewrite-code acceptance pair (fencei-selfmod with, fault-selfmod and
;; dir-selfmod-fence without the synchronization) is progress — visibility observed
;; through the patched instruction's effects. No axis is added.
;; `P4-SYSTEM.5` slice (c) (`2026-10-05`): the wake family and mm-wfi's re-derivation
;; ride the SAME seven axes (decision 8 — no axis is added): the timer interrupt's
;; delivery shape (the Interrupt-bit cause, xepc = the WFI's pc + 4) is the fault
;; axis's vocabulary, the wake's individual-enable rule (globals and mideleg ignored)
;; is legality, the delegated-source wake is delegation, time observed passing through
;; the halt and the pc+4 continuations are progress (the axis's own wording names
;; wfi), and the handler's mret after a wake-trap is the restart axis's xRET
;; discipline.
;; `P4-SYSTEM.5` slice (b) (`2026-10-05`): the 7-guest interrupts corpus rides the SAME
;; seven axes (decision 3 — no axis is added): the delivered interrupt's Interrupt-bit /
;; cause / xepc shape and the synchronous-keeps-BASE vs vectored landing are the fault
;; axis's delivery vocabulary, the global enables' taken-rule and the vectored MODE's
;; WARL are legality, mideleg's mask (and the delegation-aware sip/mip views) is
;; delegation, the time-reaches-stimecmp equality edge is boundary, the pending
;; evaluation at every step head and continuation past a delivery are progress, and the
;; nested xRET stack's restoration is restart.
;; `P4-SYSTEM.4` slice (e) (`2026-10-05`): the 12-guest atomics corpus rides the SAME
;; seven axes (decision 9 — no axis is added): misaligned atomics are the fault axis's
;; cause 7 vocabulary, the AMO permission rules and the reserved encodings are
;; legality, the translated AMO's page fault routed to S is delegation, the .W sign
;; edges are boundary, the LR/SC sequences and the constrained loop are progress, the
;; trapped-resume discipline is restart, rd=rs overlaps are alias.
;; `P4-SYSTEM.3` slice (e) (`2026-10-04`): the 14-guest sv39 corpus rides the SAME seven
;; axes — page faults are the fault axis's cause 12/13/15 vocabulary, the walk's
;; permissions are legality, medeleg's page-fault bit is delegation, the superpage
;; sizes and the page-crossing fetch are boundary, MPRV/MPP and the xret returns are
;; restart, and translated continuation is progress. No axis is added: translation
;; composes the existing vocabulary.
;; The 7×7 upper triangle is 28 cells; the INTERACTION-MATRIX doctrine re-derives them from
;; the axes and refuses — by name — an omitted cell, a disposition that does not resolve, an
;; orphan guest no cell names, or a difference id references.sexp does not carry. Three
;; cells are REPORTED degenerate with their reasons (the corpus composes nothing there);
;; no cell names a difference id — the unit records none (the two fencei mirror files were
;; re-derived at this slice to drop rv64i's DIFF-FENCEI-EXECUTED pin, which this unit's
;; references.sexp does not and should not record: rv64gc DECLARES Zifencei, and the staged
;; encoding leaves its slot unbound).

(interactions (profile "rv64gc-lab-v0")

(axis (id "fault") (covers "trap delivery: the cause/xtval/xepc vocabulary, fault priority, suppressed effects — every target-visible fault delivered on this composition (zicsr's declared refinement), never merely reported"))
(axis (id "alias") (covers "register aliasing: rd=rs overlaps, x0 hardwired in both directions — the base layer, plus CSR accesses with x0 destinations"))
(axis (id "boundary") (covers "data-domain edges: wraps, sign edges, the 6-bit and 5-bit shift-amount domains, address extremes — mode-agnostic by construction"))
(axis (id "legality") (covers "permission and refusal: mode-dependent legality of instructions and CSR accesses (M/S/U, the TW/TVM/TSR gates, read-only and WARL), and encoding validity (the reserved/refused forms)"))
(axis (id "delegation") (covers "interception routing: medeleg, mcounteren/scounteren, STCE — which agent (M or S) a trap or an access reaches"))
(axis (id "progress") (covers "every step's effect visible; continuation past a delivered trap; wfi as a nop; the budget contract"))
(axis (id "restart") (covers "the xret/xepc return discipline: resumption of preempted control flow at the recorded address and mode (mret/sret, SPP/MPP, the MPRV clear-below-M / preserve-at-M rule)"))

;; ── fault × * ─────────────────────────────────────────────────────────────────────
(cell (axis "fault") (axis "fault") (guest "it-prio-jump") (guest "it-prio-load"))
(cell (axis "fault") (axis "alias") (guest "it-fault-alias") (guest "fault-ld-x0-mis") (guest "fault-ld-x0-fault"))
(cell (axis "fault") (axis "boundary") (guest "it-fault-wrap-ld") (guest "it-fault-wrap-sd") (guest "sv39-fault-canonical") (guest "sv39-fault-superpage") (guest "a-lrsc-fault"))
(cell (axis "fault") (axis "legality") (guest "fault-reserved") (guest "dir-runoff") (guest "it-fencei") (guest "min-fencei") (guest "mm-csr-legality-s") (guest "mm-csr-legality-u") (guest "sv39-fault-invalid") (guest "sv39-fault-reserved") (guest "sv39-perm-rwx") (guest "sv39-svade") (guest "sv39-mprv") (guest "a-lrsc-illegal") (guest "a-amo-sv39") (guest "i-vector") (guest "fencei-reserved"))
(cell (axis "fault") (axis "delegation") (guest "mm-ecall-deleg") (guest "mm-counters") (guest "mm-stimecmp") (guest "sv39-deleg") (guest "a-amo-sv39") (guest "i-deleg") (guest "w-deleg"))
(cell (axis "fault") (axis "progress") (guest "smoke-trap") (guest "guest-no-device") (guest "fault-jal-mis") (guest "fault-jalr-mis") (guest "fault-branch-nt") (guest "fault-fetch") (guest "fault-ld-mis-h") (guest "fault-ld-mis-d") (guest "fault-st-mis-h") (guest "fault-st-mis-w") (guest "fault-st-mis-d") (guest "fault-access-ld") (guest "fault-access-sd") (guest "fault-fence") (guest "fault-hints") (guest "fault-selfmod") (guest "dir-selfmod-fence") (guest "a-lrsc-fault") (guest "a-lrsc-mustfail") (guest "i-timer") (guest "w-timer") (guest "fencei-selfmod"))
(cell (axis "fault") (axis "restart") (guest "mm-ebreak") (guest "mm-mret") (guest "a-lrsc-fault") (guest "a-amo-sv39") (guest "i-nest") (guest "w-timer"))

;; ── alias × * ─────────────────────────────────────────────────────────────────────
(cell (axis "alias") (axis "alias") (guest "bound-alias") (guest "scope-mem") (guest "dir-chase") (guest "dir-ext-matrix") (guest "dir-x0-writes") (guest "a-amo-overlap"))
(cell (axis "alias") (axis "boundary") (guest "it-alias-bound") (guest "smoke-arith"))
(cell (axis "alias") (axis "legality") (guest "mm-csr-rw") (guest "mm-readonly"))
(cell (axis "alias") (axis "delegation") (guest "mm-ecall-deleg") (guest "mm-counters"))
(cell (axis "alias") (axis "progress") (guest "bound-alias") (guest "it-progress-loop"))
(cell (axis "alias") (axis "restart") (degenerate "the staged corpus composes no x0/aliasing case with an xret return: the restart cells observe control state (xepc, xPP, MPRV) through CSR reads by design, and the alias layer's x0 discipline is exercised against CSR access (alias x legality) and loop progress (alias x progress) — reported, not omitted"))

;; ── boundary × * ──────────────────────────────────────────────────────────────────
(cell (axis "boundary") (axis "boundary") (guest "bound-arith") (guest "bound-shift") (guest "bound-shiftw") (guest "bound-ext") (guest "dir-ext-matrix") (guest "scope-alu") (guest "a-amo-arith-w") (guest "a-amo-arith-d") (guest "a-amo-minmax-w") (guest "a-amo-minmax-d"))
(cell (axis "boundary") (axis "legality") (guest "bound-shiftw") (guest "fault-shiftw-res"))
(cell (axis "boundary") (axis "delegation") (degenerate "delegation routing is a function of the cause and the current mode, never of a data-domain edge: no staged guest composes them — the boundary layer is mode-agnostic and every delegation cell keys on cause and mode — reported, not omitted"))
(cell (axis "boundary") (axis "progress") (guest "bound-shift") (guest "bound-shiftw") (guest "dir-memwalk") (guest "dir-chain") (guest "scope-branch") (guest "dir-cmp-branch") (guest "sv39-translate-2m") (guest "sv39-translate-1g") (guest "sv39-straddle") (guest "i-timer"))
(cell (axis "boundary") (axis "restart") (degenerate "no staged guest composes a data-domain edge with an xret return: the restart cells' observations are control state, and an xret to a domain-edge target (a 2-mod-4 mepc under IALIGN=16) is semantics this slice has not derived — reported, not omitted"))

;; ── legality × * ──────────────────────────────────────────────────────────────────
(cell (axis "legality") (axis "legality") (guest "mm-csr-legality-s") (guest "mm-csr-legality-u") (guest "mm-readonly") (guest "mm-wfi") (guest "mm-sfence") (guest "mm-sret") (guest "sv39-perm-usr") (guest "a-lrsc-illegal") (guest "i-prio"))
(cell (axis "legality") (axis "delegation") (guest "mm-ecall-deleg") (guest "mm-counters") (guest "mm-stimecmp"))
(cell (axis "legality") (axis "progress") (guest "mm-wfi") (guest "mm-ebreak") (guest "scope-ecall") (guest "scope-ebreak") (guest "fault-fetch") (guest "sv39-tlb-fence") (guest "a-amo-aqrl") (guest "a-lrsc-mustfail") (guest "i-accept") (guest "i-enable") (guest "w-sw"))
(cell (axis "legality") (axis "restart") (guest "mm-sret") (guest "mm-mret") (guest "mm-ecall-deleg") (guest "sv39-mprv") (guest "sv39-perm-usr"))

;; ── delegation × * ────────────────────────────────────────────────────────────────
(cell (axis "delegation") (axis "delegation") (guest "mm-ecall-deleg") (guest "mm-counters") (guest "mm-stimecmp") (guest "i-deleg") (guest "w-deleg"))
(cell (axis "delegation") (axis "progress") (guest "mm-ecall-deleg") (guest "mm-counters"))
(cell (axis "delegation") (axis "restart") (guest "mm-ecall-deleg") (guest "sv39-deleg"))

;; ── progress × *, restart × restart ───────────────────────────────────────────────
(cell (axis "progress") (axis "progress") (guest "it-progress-loop") (guest "dir-memwalk") (guest "dir-chain") (guest "guest-control") (guest "scope-alu") (guest "scope-mem") (guest "mm-ecall-modes") (guest "sv39-translate-4k") (guest "a-lrsc-pair") (guest "a-lrsc-loop") (guest "a-lrsc-mustfail") (guest "i-prio") (guest "w-notrap") (guest "mm-wfi") (guest "fencei-selfmod"))
(cell (axis "progress") (axis "restart") (guest "mm-ebreak") (guest "mm-ecall-modes") (guest "mm-sret"))
(cell (axis "restart") (axis "restart") (guest "mm-mret") (guest "mm-sret") (guest "mm-ecall-deleg") (guest "i-nest")))
