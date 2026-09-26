;; semantics.sexp — the schema for a semantics fragment (rv64i.sem.sexp's grammar).
;;
;; A semantics file is one (semantics …) holding the fragment id, the XLEN, and one
;; (sem …) per instruction: the instruction name, the specification locator the rule
;; was derived from, and the effect. The effect is an expression of the operator
;; language declared below — the 32 forms `scripts/check_semantics.py` checks against,
;; AS DATA (SOT-FORMAT.2): a new semantic form is a line here, zero lines of Python.
;;
;; Operators are positional: `(add (reg rs1) (reg rs2))` is not made of (name value)
;; field pairs. `(fixed N)` is exactly N arguments; `(variadic)` is N-or-more with
;; `(min N)` (default 1); `(arg SPEC)` types each argument — `symbol`, `integer`,
;; `string`, `expr` (an atom or a nested operator form; the default), or a
;; fixed-length tuple of those for one positional argument. Whether a bare symbol is
;; an operand the instruction actually HAS is a cross-file fact (the encoding provides
;; the operands) — it stays in check_semantics.py, not here.

(schema (id "semantics"))

(construct (name semantics)
  (field (name fragment) (type string))
  (field (name xlen) (type integer))
  (field (name sem) (type form) (head sem) (repeat yes)))

(construct (name sem)
  (field (name insn) (type symbol))
  (field (name source) (type string))
  (field (name effect) (type form)
         (head set) (head set-pc) (head seq) (head nop) (head if) (head store) (head trap)))

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
;; ---- effects --------------------------------------------------------------------------------
(operator (name set) (fixed 2))
(operator (name set-pc) (fixed 1))
(operator (name seq) (variadic))
(operator (name nop) (fixed 0))
(operator (name if) (fixed 3))
(operator (name trap) (fixed 2))                ; (trap cause tval)
