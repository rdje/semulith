;; category-needs.sexp — the schema for the category-needs catalogue (materials/category-needs.sexp).
;;
;; A CATEGORY-NEED binds one docs/INFORMATION_CATALOG.md category to the material kind that
;; supplies it, for one modelled unit, with the layer at which that category lives and an
;; honest disposition. The dispositions distinguish ABSENT from NEVER-NEEDED: `missing`
;; means the unit requires the category and the catalogue lacks the material (a reason is
;; owed); `out-of-scope` means the unit never owed it — the acceptance's rule is the
;; mechanical form, enforced by RECORD-SCHEMA: a board-layer category dispositioned
;; `missing` for a processor unit is a lie about what was required.
;;
;; Category ids: C01..C24 are the catalogue's own; D01..D15 are the DSP-specific questions
;; of its §5, carried as their own categories rather than folded into the CPU ones
;; (MODEL-METHOD.2). Nothing is pre-built for units that have never been exercised.
;;
;; Records move only behind the schema layer: an undeclared construct, an unknown field,
;; a wrong arity or a wrong value type is refused by name, never ignored.

(schema (id "category-needs"))

(construct (name category-need)
  (field (name category) (type string) (pattern "^(C|D)[0-9]{2}$"))
  (field (name layer) (type symbol) (values processor) (values board) (values system))
  (field (name kind) (type string) (min-length 1))
  (field (name unit) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name disposition) (type symbol) (values covered) (values partial)
         (values missing) (values out-of-scope))
  (field (name reason) (type string) (optional yes) (min-length 1))
  (field (name material) (type string) (optional yes)
         (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$")))
