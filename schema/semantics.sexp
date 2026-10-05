;; semantics.sexp — the schema for a semantics fragment (rv64i.sem.sexp's grammar).
;;
;; A semantics file is one (semantics …) holding the fragment id, the XLEN, and one
;; (sem …) per instruction: the instruction name, the specification locator the rule
;; was derived from, and the effect. The effect is an expression of the operator
;; language declared below — the 43 forms `scripts/check_semantics.py` checks against,
;; AS DATA (SOT-FORMAT.2): a new semantic form is a line here, zero lines of Python.
;;
;; Operators are positional: `(add (reg rs1) (reg rs2))` is not made of (name value)
;; field pairs. `(fixed N)` is exactly N arguments; `(variadic)` is N-or-more with
;; `(min N)` (default 1); `(arg SPEC)` types each argument — `symbol`, `integer`,
;; `string`, `expr` (an atom or a nested operator form; the default), or a
;; fixed-length tuple of those for one positional argument. Whether a bare symbol is
;; an operand the instruction actually HAS is a cross-file fact (the encoding provides
;; the operands) — it stays in check_semantics.py, not here.
;;
;; READS AND WRITES, stated once for the whole language (P4-SYSTEM.2 slice b — the CSR
;; instructions forced the question and no RV64I rule depends on the answer either way):
;; a `(reg x)` in a value position denotes the PRE-INSTRUCTION register file — csrrw
;; swaps a register with a CSR, and a threaded read would see the write. Effects apply
;; in sequence, and MEMORY and CSR reads see the state at their point of evaluation (a
;; load after a store in the same tree sees the store — the self-modifying-code
;; discipline). `(pc)` and `(inst)` are frame constants of the instruction.
;;
;; THE RESERVATION, stated once for the three atomic operators below (RVI-A §12.1.2;
;; P4-SYSTEM.4 decisions 2–4, 6). The hart holds at most ONE reservation: (physical
;; address, width, valid) of the most recent LR — the reservation SET is exactly the
;; accessed word's or doubleword's bytes, the minimal conformant set ("An implementation
;; can register an arbitrarily large reservation set … provided [it] includes all bytes
;; of the addressed data word or doubleword", §12.1.2), keyed on the PHYSICAL address
;; (the aliasing latitude — "allowed to succeed … using an alias … also allowed to
;; fail" — resolved to exact physical match, laboratory authority). Invalidation is
;; exactly the one-hart set the specification states: any LR REPLACES the reservation;
;; any SC — success or failure, any address — CLEARS it ("Regardless of success or
;; failure, executing an SC.W instruction invalidates any reservation held by this
;; hart", §12.1.2); NOTHING else touches it — a trap does NOT invalidate (the spec
;; gives no such rule; §12.1.3's trap is only a loop-exit event), and the
;; context-switch scratch-SC guidance is software's duty, not machinery. The external
;; invalidation event (another hart's store, a device write) cannot arise at harts=1
;; with no devices; the boundary vocabulary for an environment to DELIVER one is
;; P4-SYSTEM.9's contract item, never smuggled. Misaligned atomics take the
;; ACCESS-FAULT family by kind (5 for LR, 7 for SC/AMO): the spec offers
;; misaligned-or-access-fault (§12.1.2, §12.1.4) and the laboratory's pinned override
;; declares the atomic kinds AccessFault (decision 6, laboratory authority) — within
;; access-fault the cause follows RVP-MACHINE's exception table ("load and
;; load-reserved instructions generate load exceptions, whereas store,
;; store-conditional, and AMO instructions generate store/AMO exceptions"), judged
;; before translation (the P4-SYSTEM.3 decision-7 hand-off).

(schema (id "semantics"))

(construct (name semantics)
  (field (name fragment) (type string))
  (field (name xlen) (type integer))
  (field (name sem) (type form) (head sem) (repeat yes))
  (field (name refines) (type form) (head refines) (repeat yes) (optional yes)))

(construct (name refines)
  (field (name insn) (type string)))

(construct (name sem)
  (field (name insn) (type symbol))
  (field (name source) (type string))
  (field (name effect) (type form)
         (head set) (head set-pc) (head seq) (head nop) (head if) (head store) (head trap)
         (head csr-write) (head trap-deliver) (head xret) (head tlb-invalidate)))

;; ---- values ---------------------------------------------------------------------------------
(operator (name reg) (fixed 1) (arg symbol))
(operator (name pc) (fixed 0))
(operator (name imm) (fixed 1) (arg symbol))
(operator (name lit) (fixed 1) (arg integer))
;; ---- integer arithmetic and logic, all on XLEN-wide two's-complement values -----------------
(operator (name add) (fixed 2))
(operator (name sub) (fixed 2))
(operator (name and) (fixed 2))
(operator (name or) (fixed 2))
(operator (name xor) (fixed 2))
(operator (name shl) (fixed 2))
(operator (name shr) (fixed 2))                 ; shr logical, sar arithmetic
(operator (name sar) (fixed 2))
(operator (name slt) (fixed 2))                 ; set-less-than, signed and unsigned
(operator (name sltu) (fixed 2))
(operator (name eq) (fixed 2))
(operator (name ne) (fixed 2))
(operator (name lt) (fixed 2))
(operator (name ltu) (fixed 2))
(operator (name ge) (fixed 2))
(operator (name geu) (fixed 2))
;; ---- width manipulation — explicit, because implicit width is where models diverge ----------
(operator (name trunc) (fixed 2))
(operator (name sext) (fixed 2))
(operator (name zext) (fixed 2))
(operator (name bits) (fixed 3))                ; (bits hi lo v)
;; ---- memory ---------------------------------------------------------------------------------
(operator (name load) (fixed 3))                ; (load width signed? addr)
(operator (name store) (fixed 3))               ; (store width addr value)
;; ---- privilege values (P4-SYSTEM.2 slice b) ---------------------------------------------------
;; (field X) — the RAW numeric value of a named operand field: a register index, a csr
;; address, a zimm5. `(reg rd)` reads the register the field NAMES; `(field rd)` reads the
;; field itself — the csrrs "rs1=x0 shall not write" discipline is a fact about the field.
(operator (name field) (fixed 1) (arg symbol))
;; (inst) — the instruction word, a frame constant like (pc): illegal-instruction xtval
;; carries the faulting bits (the project's D-RESERVED-DECODE convention, measured on both
;; reference models).
(operator (name inst) (fixed 0))
;; (mode) — the current privilege mode, encoded as the architecture encodes it: 0=U, 1=S,
;; 3=M (RVP-INTRO). Mode-dependent legality (xRET, WFI, SFENCE.VMA, ECALL's cause) reads it.
(operator (name mode) (fixed 0))
;; (csr-state a) — the MACHINE's own read of its CSR state: no permission model, no
;; legalization. This is how an effect inspects hardware state (mstatus.TSR in sret's
;; legality, and internally the delegation/vector/enable reads of trap-deliver, xret and the
;; CSR operators) — an instruction-initiated access goes through csr-read/csr-write, and
;; routing an internal check through the trapping path would recurse (the counter-enable
;; gate reads mcounteren to judge a counter read).
(operator (name csr-state) (fixed 1))
;; (csr-read a) — an ARCHITECTURAL CSR read (the CSR instructions'), yielding an XLEN value.
;; The uniform permission model is part of its meaning, so every CSR instruction gets it
;; once: the address-map mode bits csr[9:8] (a lesser mode -> illegal instruction) and the
;; read-only bits csr[11:10] (RVP-CSR §1.1.1); the counter-enable gates for cycle/time/
;; instret (mcounteren, then scounteren for U — RVP-MACHINE §2.1.1.11, RVP-SUPERVISOR
;; §11.1.1.5); mcounteren.TM gating stimecmp and menvcfg.STCE gating it for modes below M
;; (RVP-SSTC 12.1, §2.1.1.18); and mstatus.TVM gating satp access in S (§2.1.1.6.6). A
;; refused access raises illegal-instruction (cause 2, xtval the instruction word).
(operator (name csr-read) (fixed 1))
;; ---- effects --------------------------------------------------------------------------------
(operator (name set) (fixed 2))
(operator (name set-pc) (fixed 1))
(operator (name seq) (variadic))
(operator (name nop) (fixed 0))
(operator (name if) (fixed 3))
(operator (name trap) (fixed 2))                ; (trap cause tval)
;; ---- privilege effects (P4-SYSTEM.2 slice b) ---------------------------------------------------
;; (csr-write a v) — an ARCHITECTURAL CSR write under the same permission model (a read-only
;; address refuses the write). The value is legalized per the CSR's DECLARED per-field
;; discipline (WPRI/WARL/WLRL): those tables are the state document's (P4-SYSTEM.2 slice
;; c), and the engine applies them at lowering time (slice d) — this slice's files do not
;; change when a field's discipline is declared or refined. That seam is deliberate: the
;; semantics say "the write happens under the declared discipline"; the document says what
;; the discipline IS.
(operator (name csr-write) (fixed 2))
;; (trap-deliver c t) — a SYNCHRONOUS trap delivered by the architecture (not reported to
;; the harness, rv64i's (trap …) vocabulary): the delegation selection (medeleg bit c and
;; the originating mode choose the S handler or the M handler — RVP-MACHINE §2.1.1.8), then
;; for the chosen x: xepc <- the trapping instruction's own address (§2.1.1.14, §11.1.1.7),
;; xcause <- c (§2.1.1.15, §11.1.1.8), xtval <- t (§2.1.1.16, §11.1.1.9), the xPIE/xIE/xPP
;; stack update (xPIE <- xIE; xIE <- 0; xPP <- the originating mode — §2.1.1.6.1), and
;; pc <- xtvec (§2.1.1.7, §11.1.1.2). Interrupt-caused delivery is P4-SYSTEM.5's; this
;; operator delivers synchronous exceptions only.
(operator (name trap-deliver) (fixed 2))
;; (xret x) — the trap return for privilege x, given as its architectural code (3=M, 1=S —
;; the xPP encoding itself): supposing xPP holds y, xIE <- xPIE; the privilege mode <- y;
;; xPIE <- 1; xPP <- the least-privileged supported mode; if y != M then MPRV <- 0; and
;; pc <- xepc (RVP-MACHINE §2.1.1.6.1, §2.1.3.2). LEGALITY stays in the instruction's own
;; rule (xRET in a mode less privileged than x is illegal, §2.1.3.2; sret under
;; mstatus.TSR=1 in S, §2.1.1.6.6) — the operator performs the return, the rule decides
;; whether it may.
(operator (name xret) (fixed 1))
;; (tlb-invalidate va asid) — the address-translation cache invalidation of SFENCE.VMA
;; (RVP-SUPERVISOR §11.1.2.1, P4-SYSTEM.3 decision 2): the four operand cases, as
;; specified — va=0 with asid=0 invalidates every entry (all address spaces); va=0 with
;; asid≠0 invalidates the non-global entries of that ASID; va≠0 with asid=0 invalidates
;; the entries of that virtual page in every address space, the global entries included;
;; va≠0 with asid≠0 invalidates the non-global entries of that virtual page in that
;; ASID. A non-canonical va has no effect and raises nothing (the spec's own sentence).
;; The over-fence latitude (an implementation may always invalidate more) is
;; recorded-not-taken: the effect is exactly the four cases, so the G-bit retention and
;; the per-ASID cases are genuinely testable. It writes no architectural register.
(operator (name tlb-invalidate) (fixed 2))
;; ---- atomic memory values (P4-SYSTEM.4 slice b; the reservation contract above) ---------
;; (load-reserved width signed? addr) — LR's load, shaped like (load …): translates
;; under the LOAD rules ("load and load-reserved instructions generate load
;; exceptions", RVP-MACHINE's exception table), reads width bytes, SETS/REPLACES the
;; reservation to (the translated physical address, width, valid), and yields the
;; loaded value.
(operator (name load-reserved) (fixed 3))
;; (store-conditional width addr value) — SC's conditional store, yielding THE CODE
;; for rd: 0 on success, 1 on failure — 1 is the "unspecified failure" code
;; ("Portable software should only assume the failure code will be non-zero",
;; §12.1.2). Under the declared deterministic policy (P4-SYSTEM.4 decision 3,
;; laboratory authority, stated beside the reservation in the state document): SC
;; succeeds iff the reservation is valid ∧ physical address equal ∧ width equal,
;; writing the low width bits of value; otherwise it fails with code 1, writing
;; NOTHING — a failed SC "does not give rise to any memory operations" (RVWMO
;; §17.1.1.1). It NEVER spuriously fails: one legal point of the architectural
;; nondeterminism, chosen so exact-value expectations stay derivable (EVD-05); under
;; it a constrained loop at one hart succeeds on its FIRST SC — the eventuality
;; guarantee's degenerate one-hart form (§12.1.3). It translates under the STORE/AMO
;; rules ("store, store-conditional, and AMO instructions generate store/AMO
;; exceptions", RVP-MACHINE) and CLEARS the reservation either way (the contract
;; above).
(operator (name store-conditional) (fixed 3))
;; (amo op width addr value) — one of the closed nine atomic memory operations
;; (RVI-A §12.1.4, Zaamo), NOT a seq(load, op, store) tree: the decomposition is
;; expressible but delivers cause 13 where the architecture demands a store/AMO
;; cause — "AMOs never raise load page-fault exceptions … attempting to perform an
;; AMO on an unreadable page always raises a store page-fault exception"
;; (RVP-SUPERVISOR). The operator translates ONCE under the store/AMO rules, reads
;; the old value, computes op(old, value) at width, writes the result, and yields
;; the OLD value — one instruction, completing or faulting as a unit (P4-SYSTEM.4
;; decision 5; P4-SYSTEM.8's discipline); at the environment boundary the operation
;; is a load followed by a store to the same address (a Request::Atomic variant was
;; weighed and rejected: it would push the nine operations' semantics into the
;; environment — the wrong layer — and at one hart the pair IS the single operation
;; of RVWMO §17.1.1.1). op is the operation's funct5 encoding — the value the
;; instruction's own fixed bits carry (the pinned tables' bits 31..27: add=0x00,
;; swap=0x01, xor=0x04, or=0x08, and=0x0c, min=0x10, max=0x14, minu=0x18,
;; maxu=0x1c); an op outside the closed nine is a refusal, named (gen_definition
;; re-derives the set from the composed encodings, never from a typed table). The
;; reservation is UNTOUCHED: an AMO is neither an LR nor an SC (the contract above).
;; The .W forms' rd value sign-extends the old word — written in the instruction's
;; own tree (sext, never implicit). aq/rl order nothing observable at one hart —
;; every effect is defined "as viewed by other RISC-V harts" (§12.1.1) — so they
;; decode (the fragment's fields) and carry no semantics here; all four combinations
;; assemble and execute identically, the "Software should not" of §12.1.2 being a
;; software rule, not a decode illegality (decision 1).
(operator (name amo) (fixed 4))
