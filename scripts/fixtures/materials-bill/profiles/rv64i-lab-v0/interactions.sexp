;; interactions.sexp — the declared fault × alias × boundary × event × progress × restart
;; interaction matrix of `rv64i-lab-v0` (P2-SCALAR.4, `G-INTERACTIONS`).
;; Validate with:
;;   python3 scripts/check_sexp_schema.py interactions.sexp schema/interactions.sexp
;;
;; DECLARED FIRST, THEN EXERCISED. The six axes are grounded in the tree's own layers:
;;   fault    the P2-SCALAR.3 layer (fetch/access faults, suppressed effects, reserved cases)
;;   alias    the .2 alias layer (register aliasing, x0, overlap, the same cell twice)
;;   boundary the .2 boundary layer (domain edges, wraps, sign edges, shift-amount domains)
;;   event    OB-ENV-EVENT-DELIVERY — synchronous exceptions and requested traps only
;;   progress OB-ENV-PARTIAL-PROGRESS + the budget contract
;;   restart  the state.sexp census admits no restartable suboperation, so restartability is
;;            DETERMINISM OF RE-EXECUTION FROM COLD RESET — a mechanism property, not a guest
;;            shape (the smoke runner's reproduce leg + the offline determinism suite)
;; The 6×6 upper triangle is 21 cells; the INTERACTION-MATRIX doctrine re-derives them from
;; the axes and refuses — by name — an omitted cell, a disposition that does not resolve, an
;; orphan guest no cell names, or a difference id references.sexp does not carry. Unexercised
;; cells are REPORTED (a disposition of mechanism or degenerate-with-reason), never omitted.

(interactions (profile "rv64i-lab-v0")

(axis (id "fault") (covers "the P2-SCALAR.3 layer: fetch and access faults, suppressed effects, reserved encodings, controlled event boundaries (SEM-06, SEM-07)"))
(axis (id "alias") (covers "the P2-SCALAR.2 alias layer: register aliasing (rd = rs1 = rs2), x0 hardwired in both directions, overlap composition, a load over its own base"))
(axis (id "boundary") (covers "the P2-SCALAR.2 boundary layer: signed-extreme wraps, sign/zero-extension edges, the 6-bit and 5-bit shift-amount domains, D-ADDR-WRAP"))
(axis (id "event") (covers "OB-ENV-EVENT-DELIVERY: synchronous exceptions and requested traps (ecall/ebreak) — the only events this laboratory delivers"))
(axis (id "progress") (covers "OB-ENV-PARTIAL-PROGRESS plus the budget contract: every step's effect is visible, and a non-terminating guest ends at Stop::Budget"))
(axis (id "restart") (covers "the state.sexp census admits no restartable suboperation, so restartability is determinism of re-execution from cold reset — a mechanism property, not a guest shape"))

;; ── fault × * ─────────────────────────────────────────────────────────────────────
(cell (axis "fault") (axis "fault") (guest "it-prio-jump") (guest "it-prio-load"))
(cell (axis "fault") (axis "alias") (guest "it-fault-alias") (guest "fault-ld-x0-mis") (guest "fault-ld-x0-fault"))
(cell (axis "fault") (axis "boundary") (guest "it-fault-wrap-ld") (guest "it-fault-wrap-sd") (difference "DIFF-TVAL-PHYS-MASK"))
(cell (axis "fault") (axis "event") (guest "it-fencei") (guest "min-fencei") (guest "fault-reserved") (guest "dir-runoff") (guest "fault-shiftw-res") (guest "scope-ecall") (guest "scope-ebreak") (difference "DIFF-FENCEI-EXECUTED"))
(cell (axis "fault") (axis "progress") (guest "fault-st-mis-h") (guest "fault-st-mis-w") (guest "fault-st-mis-d") (guest "fault-jal-mis") (guest "fault-jalr-mis") (guest "fault-branch-nt") (guest "smoke-trap") (guest "guest-no-device") (guest "fault-ld-mis-h") (guest "fault-ld-mis-d") (guest "fault-access-ld") (guest "fault-access-sd") (guest "fault-fence") (guest "fault-hints") (guest "fault-selfmod") (guest "dir-selfmod-fence"))
(cell (axis "fault") (axis "restart") (mechanism "smoke-reproduce") (mechanism "offline-determinism"))

;; ── alias × * ─────────────────────────────────────────────────────────────────────
(cell (axis "alias") (axis "alias") (guest "bound-alias") (guest "scope-mem") (guest "dir-chase") (guest "dir-ext-matrix") (guest "dir-x0-writes"))
(cell (axis "alias") (axis "boundary") (guest "it-alias-bound") (guest "smoke-arith"))
(cell (axis "alias") (axis "event") (guest "it-progress-loop"))
(cell (axis "alias") (axis "progress") (guest "bound-alias"))
(cell (axis "alias") (axis "restart") (mechanism "smoke-reproduce") (mechanism "offline-determinism"))

;; ── boundary × * ──────────────────────────────────────────────────────────────────
(cell (axis "boundary") (axis "boundary") (guest "bound-arith") (guest "bound-shift") (guest "bound-shiftw") (guest "bound-ext") (guest "dir-ext-matrix") (guest "scope-alu"))
(cell (axis "boundary") (axis "event") (guest "scope-branch") (guest "fault-branch-nt") (guest "dir-cmp-branch"))
(cell (axis "boundary") (axis "progress") (guest "bound-shift") (guest "bound-shiftw"))
(cell (axis "boundary") (axis "restart") (mechanism "smoke-reproduce") (mechanism "offline-determinism"))

;; ── event × * ─────────────────────────────────────────────────────────────────────
(cell (axis "event") (axis "event") (degenerate "the contained-trap contract (the harness stops the run at the first reported event) makes a SECOND in-run event unreachable — no single run can exhibit event × event; the event KINDS are exercised across guests (misalignment, access faults, the fetch fault, the reserved-decode conversions, ecall, ebreak), which is what the F×E and E×P cells enumerate"))
(cell (axis "event") (axis "progress") (guest "scope-ecall") (guest "scope-ebreak") (guest "fault-fetch") (guest "fault-reserved") (guest "dir-runoff"))
(cell (axis "event") (axis "restart") (mechanism "smoke-reproduce") (mechanism "offline-determinism"))

;; ── progress × *, restart × restart ───────────────────────────────────────────────
(cell (axis "progress") (axis "progress") (guest "it-progress-loop") (guest "dir-memwalk") (guest "dir-chain") (guest "guest-control") (guest "scope-alu") (guest "scope-mem"))
(cell (axis "progress") (axis "restart") (mechanism "smoke-reproduce") (mechanism "offline-determinism"))
(cell (axis "restart") (axis "restart") (mechanism "smoke-reproduce") (mechanism "offline-determinism")))
