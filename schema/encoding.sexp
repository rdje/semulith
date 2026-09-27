;; encoding.sexp — the schema for a unit's encoding composition (encoding.sexp).
;;
;; A unit does not carry a copy of any instruction; it names the fragments it
;; composes, and the fragments own the facts. The encoding file is one (encoding …):
;; the profile id, the instruction length, the composition — exactly one base plus an
;; extension list, EMPTY on purpose for rv64i-lab-v0 — and the fragment root the
;; fragment ids resolve against. The composition may also carry (status partial) and
;; (slot …) declarations: an unbound hole and what it must eventually provide
;; (MODEL-COMPOSE.4) — partial is declared, never inferred from silence.
;;
;; Records move only behind the schema layer: an undeclared construct, an unknown
;; field, a wrong arity or a wrong value type is refused by name, never ignored.

(schema (id "encoding"))

(construct (name encoding)
  (field (name profile) (type string))
  (field (name ilen) (type integer))
  (field (name compose) (type form) (head compose))
  (field (name fragment-root) (type string)))

(construct (name compose)
  (field (name base) (type string))
  (field (name extensions) (type string) (empty yes) (repeat yes))
  (field (name status) (type symbol) (values complete) (values partial) (optional yes))
  (field (name slot) (type form) (head slot) (repeat yes)))

(construct (name slot)
  (field (name id) (type symbol))
  (field (name requires) (type string) (repeat yes)))
