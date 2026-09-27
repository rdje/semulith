;; units.sexp — the schema for the modelled-unit registry (materials/units.sexp).
;;
;; A UNIT is one thing this project models: a processor, a board, a computer. The registry is
;; deliberately small — one row per unit, id / kind / layer / book — and nothing is pre-built
;; for kinds that have never been exercised (MODEL-METHOD.2): `kind` admits exactly what the
;; corpus holds today, and a new kind is a `(values …)` edit the day a real unit needs one.
;;
;; Records move only behind the schema layer: an undeclared construct, an unknown field,
;; a wrong arity or a wrong value type is refused by name, never ignored.

(schema (id "units"))

(construct (name unit)
  (field (name id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name kind) (type symbol) (values processor))
  (field (name layer) (type symbol) (values processor) (values board) (values system))
  (field (name book) (type string) (min-length 1))
  (field (name requires) (type string) (repeat yes) (optional yes)
         (pattern "^(C|D)[0-9]{2}$")))
