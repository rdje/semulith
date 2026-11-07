;; dispositions.sexp — the schema for a profile's declared source-specific dispositions (profiles/<profile>/dispositions.sexp).
;;
;; EVIDENCE_POLICY.md: "Any alternative disposition needs an explicit source-grounded argument and its own controls before
;; execution." Its `source-specific` row asks the same: "A disposition declared for that precise source category and constraints
;; before its qualification run." So each record states why the requirement's row cannot be met, and names the controls that
;; stand for it. A requirement keeps the category its source gives it: an `implementation-defined` one takes a record only where
;; the pinned reference offers nothing to select otherwise. `kind case`: it closes through a matched case, whose declared control it names.
;; `kind record`: nothing runs, and it closes through a retained record of its checks. `walk_record yes`: the case also
;; retains a comparison of its page-table reads (scripts/measure_walk_trace.py). scripts/dispositions.py reads this; a
;; requirement with no record stays `planned` (decision_the-seventeen-called.md; P4-SYSTEM.14 a51-7).

(schema (id "dispositions"))

(construct (name disposition)
  (field (name id) (type string) (pattern "^DS-[A-Z0-9-]+\\Z"))
  (field (name requirement_id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name kind) (type symbol) (values case) (values record))
  (field (name source_id) (type string) (min-length 1))
  (field (name source_locator) (type string) (min-length 1))
  (field (name argument) (type string) (min-length 1))
  (field (name controls) (type string) (repeat yes) (min 1) (min-length 1))
  (field (name control_property) (type string) (min-length 1) (optional yes))
  (field (name walk_record) (type symbol) (values yes) (optional yes)))
