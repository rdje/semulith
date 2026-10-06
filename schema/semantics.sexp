;; semantics.sexp — the schema for a semantics fragment (rv64i.sem.sexp's grammar).
;;
;; A semantics file is one (semantics …) holding the fragment id, the XLEN, and one
;; (sem …) per instruction: the instruction name, the specification locator the rule
;; was derived from, and the effect. The effect is an expression of the operator
;; language declared below — the forms `scripts/check_semantics.py` checks against,
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
;; ---- floating point (P4-SYSTEM.7 slice c3; the F bind, D at slice d) --------------------------
;; THE FLOATING-POINT STATE, stated once for every operator of this block (the reservation
;; block's precedent — the shared rules are the operators' meaning, so no rule restates them):
;;
;; - (freg x) in a value position denotes the PRE-INSTRUCTION f-register file — the
;;   READS-AND-WRITES contract above, as (reg x) — and yields the raw FLEN = 64 bits (D is
;;   selected; RVI-D §21.1.1). (set (freg rd) v) writes v's 64 bits and marks mstatus.FS
;;   Dirty UNCONDITIONALLY — a write is a write: the pinned FS section makes the
;;   unaltered-contents case implementation-defined ("If an instruction explicitly or
;;   implicitly writes a floating-point register or the fcsr but does not alter its
;;   contents, and FS=Initial or FS=Clean, it is implementation-defined whether FS
;;   transitions to Dirty", RVP-MACHINE §2.1.1.6.7), and the laboratory resolves it the way
;;   Sail 0.14's wF does (laboratory authority).
;; - THE OFF GATE: an instruction whose rule reads or writes the floating-point state — any
;;   (freg …), any operator of this block — is ILLEGAL at mstatus.FS = Off: illegal
;;   instruction (cause 2, xtval the instruction word), judged at the HEAD of the
;;   instruction, before ANY effect of its rule (an FLW at FS=Off raises 2, never its
;;   load's own fault). The spec quantifies over exactly that population — "any
;;   instruction that attempts to read or write the corresponding state will cause an
;;   illegal-instruction exception" (RVP-MACHINE §2.1.1.6.7) — so the gate is DERIVED from
;;   the rule, never a per-rule guard a rule could forget (P4-SYSTEM.7's split decision;
;;   Sail 0.14 judges it at decode, fdext_control.sail:19). The FP CSRs are gated by
;;   csr-read/csr-write's permission model (slice b), not here.
;; - THE ARITHMETIC: the value operators below take n-bit IEEE 754-2008 encodings (n = 32 or
;;   64, a literal: the format is data, like a width) and, where they round, the EFFECTIVE
;;   rounding mode of (rounding …); they yield the n-bit result, IEEE-correctly rounded —
;;   one rounding; subnormals per IEEE, no flush ("Operations on subnormal numbers are
;;   handled in accordance with the IEEE 754-2008 standard", tininess detected after
;;   rounding — RVI-F §20.1.4) — and any NaN result is the CANONICAL NaN ("if the result of
;;   a floating-point operation is NaN, it is the canonical NaN", RVI-F §20.1.3:
;;   0x7fc00000 single, 0x7ff8000000000000 double). Each ACCRUES its IEEE exception flags
;;   into fflags (NV DZ OF UF NX at bits 4..0) by OR — sticky, never cleared by an
;;   instruction (RVI-F §20.1.2) — and the accrual marks FS Dirty iff fflags CHANGES (the
;;   same implementation-defined latitude, resolved as Sail 0.14's default
;;   Fflags_Dirty_Precise; laboratory authority). The arithmetic is rustc_apfloat behind
;;   the model layer, which owns the target policy and the measured LLVM-vs-IEEE flag
;;   deviations — two: OF on a directed-mode clamp and UF at the smallest-normal
;;   boundary (decision_fp-backend-qualification, amended `2026-10-06` twice: the record's
;;   third, no NV on a signaling-NaN conversion, was the MPFR oracle's — P4-SYSTEM.7 slice
;;   d3): an evaluator arm never touches the backend directly.
;; - NaN-BOXING is the tree's, in bits (RVI-D §21.1.2): a narrower result is written
;;   through (fbox n v); a narrower operand is read through (funbox n v); the transfer
;;   instructions (FLW/FSW, FMV.X.W/FMV.W.X) move bits and never unbox — "A narrower n-bit
;;   transfer out of the floating-point registers will transfer the lower n bits of the
;;   register ignoring the upper FLEN-n bits".
;;
;; (freg x) — the f-register the operand field x names (RVI-F §20.1.1).
(operator (name freg) (fixed 1) (arg symbol))
;; (fbox n v) — v's low n bits NaN-boxed into FLEN: all 1s above ("Any operation that writes
;; a narrower result to an 'f' register must write all 1s to the uppermost FLEN-n bits",
;; RVI-D §21.1.2). n = 64 is the identity.
(operator (name fbox) (fixed 2))
;; (funbox n v) — the n-bit operand an FLEN-bit register value carries: its low n bits when
;; the upper FLEN-n bits are all 1s, else the n-bit canonical NaN ("otherwise the input value
;; is treated as an n-bit canonical NaN", RVI-D §21.1.2). n = 64 is the identity.
(operator (name funbox) (fixed 2))
;; (rounding rm) — the EFFECTIVE rounding mode of the instruction's rm field, 0..4
;; (RNE RTZ RDN RUP RMM — RVI-F §20.1.2's Table 2): 111 (DYN) resolves to frm's current
;; value. A RESERVED rounding mode — static 101/110, or DYN with frm holding 101–111 —
;; raises illegal-instruction (cause 2, xtval the word) and the step ends: the pinned
;; revision makes the behavior "reserved" and keeps the ratified illegal-instruction
;; mandate "still valid behavior"; the laboratory takes it (Sail 0.14's Fcsr_RM_Illegal;
;; P4-SYSTEM.7 slice c1). Its argument is the instruction's own (field rm), never a
;; computed value; an encoding that carries rm resolves it in its rule even where the
;; operation cannot round — "implementations must treat the rm field as usual (in
;; particular, with regard to decoding legal vs. reserved encodings)".
(operator (name rounding) (fixed 1))
;; (fadd n rm a b) (fsub n rm a b) (fmul n rm a b) (fdiv n rm a b) — a+b, a-b, a×b, a÷b
;; (RVI-F §20.1.6; division by zero raises DZ, 0/0 and ∞-∞ NV — IEEE 754-2008 §7).
(operator (name fadd) (fixed 4))
(operator (name fsub) (fixed 4))
(operator (name fmul) (fixed 4))
(operator (name fdiv) (fixed 4))
;; (fsqrt n rm a) — √a; a negative non-zero operand is invalid: NV, the canonical NaN
;; (RVI-F §20.1.6; IEEE 754-2008 §5.4.1, §7.2). The backend carries no square root: the
;; model layer computes it (the qualification record's one named gap).
(operator (name fsqrt) (fixed 3))
;; (fmadd n rm a b c) — (a×b)+c with ONE rounding (RVI-F §20.1.6). ∞×0 raises NV even when c
;; is a quiet NaN ("The fused multiply-add instructions must set the invalid operation
;; exception flag when the multiplicands are ∞ and zero, even when the addend is a quiet
;; NaN"). The negated forms negate an OPERAND in the tree (a sign-bit XOR), never the
;; result: -(a×b)+c is (fmadd n rm -a b c) exactly — negation is exact and the single
;; rounding then sees the true value in every rounding mode (Sail 0.14's negate_S shape).
(operator (name fmadd) (fixed 5))
;; (fmin n a b) (fmax n a b) — IEEE 754-201x minimumNumber/maximumNumber as RVI-F §20.1.6
;; amends them: −0.0 < +0.0; both NaN → the canonical NaN; one NaN → the other operand; a
;; signaling-NaN input raises NV "even when the result is not NaN". No rounding.
(operator (name fmin) (fixed 3))
(operator (name fmax) (fixed 3))
;; (feq n a b) (flt n a b) (fle n a b) — 1 if a=b / a<b / a≤b, else 0 (an XLEN value); 0 when
;; either operand is NaN. FEQ is QUIET (NV only for a signaling NaN); FLT and FLE are
;; SIGNALING (NV for any NaN) — RVI-F §20.1.8.
(operator (name feq) (fixed 3))
(operator (name flt) (fixed 3))
(operator (name fle) (fixed 3))
;; (fclass n a) — the 10-bit class mask of a, exactly one bit set (RVI-F §20.1.9, Table 6:
;; bit 0 −∞ … bit 7 +∞, bit 8 signaling NaN, bit 9 quiet NaN); raises no flag.
(operator (name fclass) (fixed 2))
;; (f2i n iw s rm a) — a (an n-bit float) converted to an iw-bit integer, signed when s is 1,
;; rounded by rm (RVI-F §20.1.7); n, iw and s are literals. A result outside the target
;; range is CLIPPED and raises NV (Table 5: out-of-range negative and −∞ → the minimum; out-of
;; -range positive, +∞ and NaN → the maximum); NX otherwise when the rounded value differs
;; from a ("All floating-point conversion instructions set the Inexact exception flag if the
;; rounded result differs from the operand value and the Invalid exception flag is not set").
;; The W forms' sign extension to XLEN is the rule's own (sext 64 …).
(operator (name f2i) (fixed 5))
;; (i2f n iw s rm v) — v's low iw bits as an integer (signed when s is 1) converted to an
;; n-bit float, rounded by rm; NX when inexact (RVI-F §20.1.7).
(operator (name i2f) (fixed 5))
;; (f2f m n rm a) — a (an n-bit float) converted to an m-bit float: FCVT.S.D and FCVT.D.S,
;; where "both the source and destination are floating-point registers" (RVI-D §21.1.5); m
;; and n are DISTINCT literals 32/64. Narrowing rounds by rm, with OF/UF/NX as for any
;; rounded result, and widening is exact: "FCVT.S.D rounds according to the RM field;
;; FCVT.D.S will never round" — yet a widening rule still resolves its rm (the reserved-mode
;; decode every rm-carrying encoding owes). A NaN input yields the canonical NaN (RVI-F
;; §20.1.3); a signaling-NaN input raises NV (IEEE 754-2008 §7.2 — an operation on a
;; signaling NaN is invalid) — the backend's own status, measured (P4-SYSTEM.7 slices
;; d2/d3; the record's "deviation (ii)" was the MPFR oracle's missing signaling NaN).
(operator (name f2f) (fixed 4))
