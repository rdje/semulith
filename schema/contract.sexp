;; contract.sexp — the schema of a unit's ENVIRONMENT CONTRACT document (P4-SYSTEM.9 slice a).
;;
;; A contract's obligations live one per record in contract-obligations.sexp, each naming its
;; contract_id and contract_version. Until this document, the VERSION was only that repeated
;; string — nothing said which records made up a version, and nothing stopped a version's
;; records from being edited after the fact. "Versioned, not edited in place" is made
;; mechanical here: each (contract …) form is ONE version, listing its members; a FROZEN
;; version carries the sha256 of each member's record line, and CONTRACT-FREEZE
;; (scripts/check_contract_freeze.sh) refuses any change to a frozen record. A statement that
;; later work made wrong is SUPERSEDED by a newer version's record (supersede …), never
;; rewritten; a version EXTENDS the one before it.

(schema (id "contract"))

(construct (name contract)
  (field (name id) (type string) (pattern "^[a-z0-9-]+-v[0-9]+$"))
  (field (name version) (type string) (pattern "^[0-9]+$"))
  (field (name profile_ids) (type string) (repeat yes) (min 1) (unique yes)
         (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name extends) (type string) (optional yes) (pattern "^[a-z0-9-]+-v[0-9]+$"))
  (field (name status) (type symbol) (values open) (values frozen))
  (field (name statement) (type string) (min-length 1))
  (field (name member) (type form) (head member) (repeat yes) (min 1))
  (field (name supersede) (type form) (head supersede) (repeat yes) (optional yes)))

;; A member: an obligation id this version ADDS (an extending version inherits its parent's
;; members, minus the ones it supersedes). `sha256` — of the record's line in
;; contract-obligations.sexp, exactly — is present once the version is frozen.
(construct (name member)
  (field (name id) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name sha256) (type string) (pattern "^[0-9a-f]{64}$") (optional yes)))

;; A supersession: an inherited record this version replaces, by one of its own members.
(construct (name supersede)
  (field (name record) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name by) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name why) (type string) (min-length 1)))

;; The unit's check REGISTRY (P4-SYSTEM.10 slice a): the one tracked file whose entries realize
;; this contract's declared checks, each bound to the fixtures that run it. The gate report counts
;; a check implemented for THIS unit exactly when this registry realizes it under the obligation
;; that declares it — never because an id appears somewhere in the tree (MIRROR-DERIVE makes ids
;; shared across units). At most one per document; a unit with none realizes nothing.
(construct (name registry)
  (field (name path) (type string) (pattern "^crates/[A-Za-z0-9_/-]+\\.rs$"))
  (field (name statement) (type string) (min-length 1)))
