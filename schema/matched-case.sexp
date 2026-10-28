;; matched-case.sexp — the schema for a matched GPR case's declaration (evidence/<case>/case.sexp).
;;
;; A matched case's declaration is data (decision_case-declarations-as-data.md; P4-SYSTEM.14 a44-1): its
;; guest program, its predeclared properties and their RV64 values, its control, its hand-reviewed steps,
;; its authority and its pinned inputs. scripts/matched_gpr_case.py reads it; a case without one is
;; refused by name. Values are integers (the reader takes 0x… spellings); every digest is lowercase hex.

(schema (id "matched-case"))

(construct (name case)
  (field (name id) (type string) (pattern "^[a-z0-9][a-z0-9-]*-v[0-9]+\\Z"))
  (field (name profile_id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name program) (type string) (pattern "^[a-z0-9][a-z0-9-]*\\.s\\Z"))
  (field (name instructions) (type integer))
  (field (name source_size) (type integer))
  (field (name source_sha256) (type string) (pattern "^[0-9a-f]{64}\\Z"))
  (field (name requirement_id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name obligation_ids) (type string) (repeat yes) (min 1) (unique yes)
         (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name contract_id) (type string) (min-length 1))
  (field (name contract_version) (type string) (min-length 1))
  (field (name control) (type form) (head control))
  (field (name limitation) (type string) (min-length 1))
  (field (name source_id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name source_locator) (type string) (min-length 1))
  (field (name category) (type string) (min-length 1))
  (field (name risk) (type string) (min-length 1))
  (field (name coverage) (type string) (min-length 1))
  (field (name authority) (type form) (head authority))
  (field (name required_input) (type form) (head required_input) (repeat yes) (min 1))
  (field (name prepared) (type form) (head prepared) (repeat yes) (min 4))
  (field (name property) (type form) (head property) (repeat yes) (min 1))
  (field (name step) (type form) (head step) (repeat yes) (min 1)))

;; The property the control expectation changes, and the wrong value it carries there.
(construct (name control)
  (field (name property_id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name value) (type integer))
  (field (name reason) (type string) (min-length 1)))

;; The selected authority beyond the case's own requirement and source: the catalogues' semantic digests.
(construct (name authority)
  (field (name requirement_semantic_sha256) (type string) (pattern "^[0-9a-f]{64}\\Z"))
  (field (name obligation_id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name obligation_semantic_sha256) (type string) (pattern "^[0-9a-f]{64}\\Z"))
  (field (name source_sha256) (type string) (pattern "^[0-9a-f]{64}\\Z")))

;; A curated normative input the review authenticates separately from publication authority.
(construct (name required_input)
  (field (name role) (type string) (min-length 1))
  (field (name id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name path) (type string) (min-length 1))
  (field (name sha256) (type string) (pattern "^[0-9a-f]{64}\\Z")))

;; A prepared input under the case directory, pinned when it was curated.
(construct (name prepared)
  (field (name role) (type string) (pattern "^(guest-image|reference-config|expectation)\\Z"))
  (field (name id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name name) (type string) (pattern "^[A-Za-z0-9][A-Za-z0-9._-]*\\Z"))
  (field (name byte_size) (type integer))
  (field (name sha256) (type string) (pattern "^[0-9a-f]{64}\\Z")))

;; One predeclared property: the policy cell it serves, its witness and its RV64 value.
(construct (name property)
  (field (name id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*\\Z"))
  (field (name cell) (type string) (pattern "^(form|table1):[A-Za-z0-9._-]+\\Z"))
  (field (name statement) (type string) (min-length 1))
  (field (name step_n) (type integer))
  (field (name register) (type string) (pattern "^x([1-9]|[12][0-9]|3[01])\\Z"))
  (field (name expected) (type integer)))

;; One hand-reviewed boundary: its instruction and the register writes it makes (possibly none).
(construct (name step)
  (field (name n) (type integer))
  (field (name pc) (type integer))
  (field (name word) (type integer))
  (field (name length) (type integer))
  (field (name fetches) (type integer))
  (field (name write) (type form) (head write) (repeat yes)))

(construct (name write)
  (field (name register) (type integer))
  (field (name value) (type integer)))
