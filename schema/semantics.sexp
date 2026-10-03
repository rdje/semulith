;; semantics.sexp — the schema for a semantics fragment (rv64i.sem.sexp's grammar).
;;
;; A semantics file is one (semantics …) holding the fragment id, the XLEN, and one
;; (sem …) per instruction: the instruction name, the specification locator the rule
;; was derived from, and the effect. The effect is an expression of the operator
;; language declared below — the 40 forms `scripts/check_semantics.py` checks against,
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
         (head csr-write) (head trap-deliver) (head xret)))

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
