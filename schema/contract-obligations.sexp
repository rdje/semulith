;; contract-obligations.sexp — the schema for a CPU/environment contract catalogue
;; (contract-obligations.sexp).
;;
;; One (obligation …) per record; field names verbatim from the retired
;; contract-obligation.schema.json (see requirements.sexp for the shared design).
;;
;; ⭐ parameters is where the JSON contract lied and the schema layer tells the truth.
;; contract-obligation.schema.json declared `additionalProperties: {type: [string, number,
;; boolean, null]}` — which silently excludes the ARRAYS three obligations actually write
;; (legal_access_widths_bits, reset_kinds, target_visible_counters), and the tracked JSON
;; validator never descended into additionalProperties at all, so the lie went unmeasured.
;; Here each parameter is a (param …) with a NAME and one typed VALUE — (int N), (str "…"),
;; (true), (false), (null), (ints …), (strs …) — declared as operators below. A value the
;; corpus does not write (a float, a mixed list) is REFUSED, not guessed; the day one is
;; needed is a schema decision, not a silent widening.

(schema (id "contract-obligations"))

(construct (name obligation)
  (field (name id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name contract_id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name contract_version) (type string) (min-length 1))
  (field (name profile_ids) (type string) (repeat yes) (min 1) (unique yes)
         (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name direction) (type symbol) (values environment-assumption)
         (values cpu-guarantee))
  (field (name statement) (type string) (min-length 1))
  (field (name authority) (type symbol) (values architecture)
         (values implementation-profile) (values platform) (values laboratory))
  (field (name source_refs) (type form) (head source_refs) (repeat yes) (min 1) (unique yes))
  (field (name parameters) (type form) (head parameters))
  (field (name dependencies) (type string) (repeat yes) (unique yes)
         (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name required_checks) (type string) (repeat yes) (min 1) (unique yes)
         (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$")))

(construct (name source_refs)
  (field (name source_id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name locator) (type string) (min-length 1)))

(construct (name parameters)
  (field (name param) (type form) (head param) (repeat yes)))

(construct (name param)
  (field (name name) (type symbol))
  (field (name value) (type form)
         (head int) (head str) (head true) (head false) (head null)
         (head ints) (head strs)))

;; ---- parameter value types, as positional operators -----------------------------------------
(operator (name int) (fixed 1) (arg integer))
(operator (name str) (fixed 1) (arg string))
(operator (name true) (fixed 0))
(operator (name false) (fixed 0))
(operator (name null) (fixed 0))
(operator (name ints) (variadic) (min 0) (arg integer))
(operator (name strs) (variadic) (min 0) (arg string))
