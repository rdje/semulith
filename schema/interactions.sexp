;; interactions.sexp — the schema for an interaction-matrix document (interactions.sexp).
;;
;; `P2-SCALAR.4` (`G-INTERACTIONS`): the declared fault × alias × boundary × event ×
;; progress × restart matrix is TRACKED DATA, declared first and then exercised. Each `axis`
;; names one declared axis; each `cell` names an unordered axis pair (the upper triangle,
;; diagonal included — with N axes there are N*(N+1)/2 cells, and the INTERACTION-MATRIX
;; doctrine re-derives them, so an omitted cell fails by name rather than silently leaving
;; the matrix). A cell's disposition is one or more of:
;;   (guest "…")      a tracked guest (source AND expectations) exercising the pair;
;;   (mechanism "…")  a named mechanism from the gate's closed registry (not a guest shape);
;;   (degenerate "…") the pair cannot arise in one run — the non-empty reason is the data.
;; A cell may also name the `(difference "…")` ids (references.sexp) its guests pin.

(schema (id "interactions"))

(construct (name interactions)
  (field (name profile) (type string) (min-length 1))
  (field (name axis) (type form) (head axis) (repeat yes) (min 2))
  (field (name cell) (type form) (head cell) (repeat yes) (min 1)))

(construct (name axis)
  (field (name id) (type string) (min-length 1))
  (field (name covers) (type string) (min-length 1)))

(construct (name cell)
  (field (name axis) (type string) (repeat yes) (min 2))
  (field (name guest) (type string) (repeat yes))
  (field (name mechanism) (type string) (repeat yes))
  (field (name difference) (type string) (repeat yes))
  (field (name degenerate) (type string) (min-length 1) (optional yes)))
