;; dispositions.sexp — the schema for a profile's declared source-specific dispositions (profiles/<profile>/dispositions.sexp).
;;
;; EVIDENCE_POLICY.md: "Any alternative disposition needs an explicit source-grounded argument and its own controls before
;; execution." Its `source-specific` row asks the same: "A disposition declared for that precise source category and constraints
;; before its qualification run." So each record states why the requirement's row cannot be met, and names the controls that
;; stand for it. A requirement keeps the category its source gives it: an `implementation-defined` one takes a record only where
;; the pinned reference offers nothing to select otherwise. `kind case`: it closes through a matched case, whose declared control it names.
;; `kind record`: nothing runs, and it closes through a retained record of its checks, the `selection` below, each fact held to
;; the value its `expect` declares (decision_a-credit-with-no-case.md). `walk_record yes`: the case also
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
  (field (name walk_record) (type symbol) (values yes) (optional yes))
  (field (name expect) (type form) (head expect) (repeat yes)))

(construct (name expect)
  (field (name fact) (type string) (pattern "^[a-z0-9][a-z0-9-]*\\Z"))
  (field (name value) (type string) (min-length 1)))

;; A selection's retained record: profiles/<profile>/selections/<id>.selection.sexp, taken once by scripts/selections.py --record.
(construct (name selection)
  (field (name id) (type string) (pattern "^SEL-[A-Z0-9-]+\\Z"))
  (field (name requirement_id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name obligation_ids) (type string) (repeat yes) (min 1) (unique yes) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name disposition) (type string) (pattern "^DS-[A-Z0-9-]+\\Z"))
  (field (name runner) (type string) (min-length 1))
  (field (name date) (type string) (pattern "^20[0-9]{2}-[0-9]{2}-[0-9]{2}\\Z"))
  (field (name input) (type form) (head input) (repeat yes) (min 1))
  (field (name run) (type form) (head run) (repeat yes) (min 1))
  (field (name fact) (type form) (head fact) (repeat yes) (min 1))
  (field (name limitation) (type string) (repeat yes) (min 1) (min-length 1)))

(construct (name input)
  (field (name path) (type string) (min-length 1))
  (field (name sha256) (type string) (pattern "^[0-9a-f]{64}\\Z"))
  (field (name byte_size) (type integer)))

(construct (name run)
  (field (name command) (type string) (min-length 1))
  (field (name serves) (type string) (repeat yes) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name rc) (type integer))
  (field (name output) (type string))
  (field (name repeated) (type symbol) (values identical) (values different)))

(construct (name fact)
  (field (name id) (type string) (pattern "^[a-z0-9][a-z0-9-]*\\Z"))
  (field (name observed) (type string) (min-length 1)))
