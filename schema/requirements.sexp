;; requirements.sexp — the schema for a requirement catalogue (requirements.sexp).
;;
;; One (requirement …) per record, house style (materials/catalog.sexp): the JSON keys of
;; the retired requirement.schema.json are the field names verbatim, so the mapping in
;; scripts/records_sexp.py has no translation table to drift. Enums are symbols under
;; (values …) — a typo is refused by name, the power the JSON enum carried. The
;; discriminating detail the record grammar could not state is carried by FACETS
;; (SOT-FORMAT.3): (pattern …) on identifiers, (min-length 1) on prose, (min 1) and
;; (unique yes) on lists — an empty list is not a citation, and a repeated citation is
;; a contradiction. Records move only behind the schema layer: an undeclared field, a
;; wrong arity or a wrong value type is refused by name, never ignored.

(schema (id "requirements"))

(construct (name requirement)
  (field (name id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name profile_ids) (type string) (repeat yes) (min 1) (unique yes)
         (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name kind) (type symbol)
         (values instruction) (values decode) (values state) (values numeric)
         (values memory) (values event) (values environment) (values configuration)
         (values invariant) (values device) (values composition))
  (field (name statement) (type string) (min-length 1))
  (field (name insns) (type string) (repeat yes) (optional yes)
         (pattern "^[a-z0-9._]+$"))
  (field (name source_refs) (type form) (head source_refs) (repeat yes) (min 1) (unique yes))
  (field (name applicability) (type symbol) (values included) (values excluded)
         (values conditional))
  (field (name research_status) (type symbol) (values resolved) (values partial)
         (values unresolved))
  (field (name implementation_status) (type symbol) (values planned) (values partial)
         (values implemented) (values not-applicable))
  (field (name source_semantics) (type form) (head source_semantics))
  (field (name risk) (type symbol) (values low) (values medium) (values high)
         (values critical))
  (field (name obligation_ids) (type string) (repeat yes) (min 1) (unique yes)
         (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name dependencies) (type string) (repeat yes) (unique yes)
         (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name implementation_refs) (type form) (head implementation_refs)
         (repeat yes) (unique yes))
  (field (name evidence_ids) (type string) (repeat yes) (unique yes)
         (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$")))

(construct (name source_refs)
  (field (name source_id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name locator) (type string) (min-length 1)))

(construct (name source_semantics)
  (field (name category) (type symbol) (values defined) (values implementation-defined)
         (values unspecified) (values undefined) (values reserved) (values unpredictable)
         (values source-specific) (values not-applicable))
  (field (name detail) (type string) (min-length 1)))

(construct (name implementation_refs)
  (field (name artifact_id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name locator) (type string) (min-length 1)))
