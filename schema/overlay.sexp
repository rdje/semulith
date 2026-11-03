;; overlay.sexp — the schema for one matched case's reference-configuration overlay
;; (profiles/<profile>/reference/<case-id>.overlay.sexp).
;;
;; A case may carry its own reference configuration (decision_reference-config-per-case.md; P4-SYSTEM.14 a43b-3c): the
;; overlay is applied over the mapped profile override by scripts/prepare_div_inputs.py, and the result is the case's
;; prepared reference-config.json, pinned as every case's is. It holds only what the pinned binary's public configuration
;; needs for the case and says why; the profile override does not move. Its closed vocabulary is deliberate: a new knob is
;; a schema change a reviewer sees, not a free-form patch of the configuration.

(schema (id "overlay"))

;; `extension`: extensions the profile selects and its override leaves off. `clint`: the reference's device, in its own
;; region, the one source of time the pinned binary accepts for Zicntr. `instructions_per_tick`: the reference's tick rate.
(construct (name overlay)
  (field (name case_id) (type string) (min-length 1))
  (field (name reason) (type string) (min-length 1))
  (field (name extension) (type string) (repeat yes) (min 1) (unique yes) (min-length 1))
  (field (name clint) (type form) (head clint))
  (field (name instructions_per_tick) (type integer)))

(construct (name clint)
  (field (name base) (type integer))
  (field (name size) (type integer)))
