;; fragment.sexp — the schema for a reusable definition fragment (rv64i.sexp, m.sexp).
;;
;; A fragment is one (fragment …): its id, its kind, what it requires, the pinned
;; sources it was generated from, the operand-field table, the scattered-immediate
;; layouts, and the instructions. Three fields are POSITIONAL mini-languages, declared
;; here as operators (SOT-FORMAT.2): `(fixed (31 25 0x0) …)` bit-field triples,
;; `(operands rd rs1 rs2)` bare-symbol lists, `(pieces (12 12) …)` integer pairs.
;;
;; Records move only behind the schema layer: an undeclared construct, an unknown
;; field, a wrong arity or a wrong value type is refused by name, never ignored.

(schema (id "fragment"))

(construct (name fragment)
  (field (name id) (type string))
  (field (name kind) (type symbol) (values isa-base) (values isa-extension))
  (field (name requires) (type string) (empty yes))
  (field (name source) (type form) (head source))
  (field (name field) (type form) (head field) (repeat yes) (optional yes))
  (field (name scatter) (type form) (head scatter) (repeat yes) (optional yes))
  (field (name insn) (type form) (head insn) (repeat yes)))

(construct (name source)
  (field (name file) (type form) (head file) (repeat yes))
  (field (name origin) (type string))
  (field (name license) (type string)))

(construct (name file)
  (field (name name) (type string))
  (field (name sha256) (type string)))

(construct (name field)
  (field (name name) (type symbol))
  (field (name hi) (type integer))
  (field (name lo) (type integer)))

(construct (name scatter)
  (field (name name) (type symbol))
  (field (name hi) (type integer))
  (field (name lo) (type integer))
  (field (name pieces) (type form) (head pieces)))

(construct (name insn)
  (field (name name) (type symbol))
  (field (name fixed) (type form) (head fixed))
  (field (name operands) (type form) (head operands))
  (field (name from) (type string)))

(operator (name fixed) (variadic) (arg (integer integer integer)))
(operator (name operands) (variadic) (min 0) (arg symbol))
(operator (name pieces) (variadic) (arg (integer integer)))
