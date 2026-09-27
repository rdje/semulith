;; composition.sexp — the schema for a composition manifest.
;;
;; A composition (a board, a computer) is not written by hand as a fourth record shape; it is
;; MATERIALIZED from its unit parts by scripts/compose_units.py (MODEL-COMPOSE.5), and the
;; result is an ordinary unit directory — the same three catalogues, the same encoding
;; document, checked by the same code at every level. The manifest names the parts, by
;; repository-relative path: one (composition …), its id, and one (part …) per unit.
;;
;; Records move only behind the schema layer: an undeclared construct, an unknown field,
;; a wrong arity or a wrong value type is refused by name, never ignored.

(schema (id "composition"))

(construct (name composition)
  (field (name id) (type string))
  (field (name part) (type string) (repeat yes) (min 1)))
