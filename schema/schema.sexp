;; schema.sexp — the schema language, written in itself.
;;
;; A schema declares the constructs a source-of-truth file may use. Adding a
;; domain construct — an encoding field, a fragment kind, a semantics form — is
;; data in this directory, never an edit to the validator (SOT-FORMAT.1). The
;; kernel of scripts/check_sexp_schema.py interprets (construct …) and
;; (field …) declarations; a new KIND of declaration changes the kernel —
;; the boundary the tree names deliberately, the same one a database draws
;; between adding a table and adding a column type.
;;
;; A schema file is a sequence of top-level forms: one (schema (id STRING))
;; of metadata, then one (construct …) per construct. A field instance is a
;; child list headed by its field's name. Atom fields take exactly one value,
;; `(name value)`; (empty yes) also allows the bare marker `(name)` — the
;; house corpus writes `(requires)` and `(extensions)` that way. Form fields
;; take the nested form: when the field name is one of the allowed heads the
;; whole child list IS the form (`(source (file …) …)`); otherwise the child
;; holds one form whose head must be allowed (`(effect (set …))`). Repetition
;; is sibling child lists with the same head, never extra elements in one
;; list — arity is uniform at every level. A repeated field may appear zero
;; times (an absent list is empty); (optional yes) is the 0-or-1 variant for
;; single-valued fields.
;;
;;   (construct (name SYMBOL)
;;     (field (name SYMBOL) (type symbol|string|integer|form) …)…)
;;
;; (type form) names its allowed heads with repeated (head SYM) pairs; a
;; symbol-typed field may restrict its spellings with repeated (values SYM)
;; pairs; (repeat yes) allows more than one occurrence.
;;
;; FACETS (SOT-FORMAT.3) refine a field without a new declaration kind:
;;   (pattern "regex")    — a string field's value must match (re.search, JSON-Schema semantics)
;;   (min-length N)       — a string field's value holds at least N characters
;;   (min N)              — a (repeat yes) field occurs at least N times — an empty list is
;;                          not a citation
;;   (unique yes)         — a (repeat yes) field writes no value twice
;;
;; ⭐ THE FIXPOINT: this file must validate under itself —
;;   python3 scripts/check_sexp_schema.py schema/schema.sexp schema/schema.sexp
;; — which is what proves "extensible by data" instead of asserting it.

(schema (id "schema"))

(construct (name schema)
  (field (name id) (type string)))

(construct (name construct)
  (field (name name) (type symbol))
  (field (name field) (type form) (head field) (repeat yes)))

(construct (name field)
  (field (name name) (type symbol))
  (field (name type) (type symbol)
         (values symbol) (values string) (values integer) (values form))
  (field (name head) (type symbol) (repeat yes) (optional yes))
  (field (name values) (type symbol) (repeat yes) (optional yes))
  (field (name repeat) (type symbol) (values yes) (values no) (optional yes))
  (field (name optional) (type symbol) (values yes) (values no) (optional yes))
  (field (name empty) (type symbol) (values yes) (values no) (optional yes))
  (field (name pattern) (type string) (optional yes))
  (field (name min-length) (type integer) (optional yes))
  (field (name min) (type integer) (optional yes))
  (field (name unique) (type symbol) (values yes) (values no) (optional yes)))
