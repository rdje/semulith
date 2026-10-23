;; credits.sexp — the schema for a profile's credited-disposition catalogue (credits.sexp).
;;
;; EVIDENCE_POLICY.md "Records, controls and currentness": each credited disposition links the
;; requirement, the effective obligation, the owner, the tracked runner and the structured evidence
;; record. A credit is a RECORD here, never a flag in a retained receipt (a42ay, 2026-10-2x): the
;; derivation (scripts/requirement_status.py) credits a case only through a record whose pins
;; authenticate against the retained bytes and whose policy measurement is satisfied at read time.

(schema (id "credits"))

(construct (name credit)
  (field (name id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name profile_ids) (type string) (repeat yes) (min 1) (unique yes)
         (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name requirement_id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name obligation_ids) (type string) (repeat yes) (min 1) (unique yes)
         (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name case_id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name measured) (type form) (head pin))
  (field (name receipt) (type form) (head pin))
  (field (name policy) (type form) (head pin))
  (field (name retained_sources) (type string) (repeat yes) (min 1) (unique yes)
         (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name authority) (type symbol) (values director) (values review))
  (field (name date) (type string) (pattern "^20[0-9]{2}-[0-9]{2}-[0-9]{2}\\Z"))
  (field (name decision) (type string) (pattern "^decision_[a-z0-9-]+\\.md\\Z"))
  (field (name legs) (type integer))
  (field (name limitations) (type string) (repeat yes) (min 1)))

(construct (name pin)
  (field (name path) (type string) (min-length 1))
  (field (name sha256) (type string) (pattern "^[0-9a-f]{64}\\Z"))
  (field (name byte_size) (type integer)))
