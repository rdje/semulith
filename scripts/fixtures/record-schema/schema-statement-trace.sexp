;; statement-trace.sexp — the schema for a profile's statement trace (statement-trace.sexp).
;;
;; EVIDENCE_POLICY.md "Statement trace": each traced requirement's statement, split into clauses in order,
;; with the declared properties that witness each clause and the limits its case names for what none does.
;; The review (scripts/review_div_policy.py, through scripts/statement_trace.py) holds the clauses to the
;; statement's own words on every read. It makes an omission visible; it proves no semantics (RULES EVD-06).

(schema (id "statement-trace"))

(construct (name trace)
  (field (name requirement_id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name clause) (type form) (head clause) (repeat yes) (min 1)))

(construct (name clause)
  (field (name text) (type string) (min-length 1))
  (field (name properties) (type string) (repeat yes) (unique yes) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name limits) (type string) (repeat yes) (unique yes) (min-length 1)))
