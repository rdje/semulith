;; identity.sexp — the schema of a unit's RELEASE IDENTITY (P4-SYSTEM.20 slice a).
;;
;; A unit's version and status are a label about its dossier, not part of what its evidence
;; was measured on. They sat in profile.sexp, which every matched case pins, so a new version
;; number lapsed every case credit even when no behaviour moved
;; (docs/decisions/decision_the-next-window-is-version-1.md, finding 1). They live here, in a
;; file no case pins. The dossier digest still covers this file, so a release decision, which
;; pins that digest, stops standing when the version moves, as it should.
;;
;; Read by scripts/gate_report.py, which refuses an identity whose unit is not the profile it
;; sits beside. Validated against this schema by DOSSIER-SCHEMA, by name.

(schema (id "identity"))

;; `version` is a release number, decimal digits. `status` is the unit's stage: `development` for a
;; unit on the release route, with its own gate manifest; `experimental` for a model whose
;; dossier makes no release claim. Whether a version is ACCEPTED is never stated here: that is
;; the named release decision's, verified by the unit's report.
(construct (name identity)
  (field (name unit) (type string) (pattern "^[a-z0-9-]+-v[0-9]+\\Z"))
  (field (name version) (type string) (pattern "^[0-9]+\\Z"))
  (field (name status) (type symbol) (values development) (values experimental)))
