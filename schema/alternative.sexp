;; alternative.sexp — the schema for the configuration a matched case declares to select otherwise
;; (profiles/<profile>/reference/<case-id>.alternative.sexp).
;;
;; The policy's `implementation-defined` row asks for a pinned matching reference configuration with a behavior-changing
;; control. When the profile override is itself the selection, there is nothing to compare it with: a case states the other
;; choice here (decision_declared-alternative-configuration.md; P4-SYSTEM.14 a50-1). It is applied over the case's own
;; configuration by scripts/prepare_div_inputs.py, and scripts/measure_config_effect.py runs the same guest under the result.
;; Nothing else reads it: it selects no case's capture, and neither the override nor any case's reference-config.json moves.
;; Its closed vocabulary holds each knob a requirement was measured to need against the pinned binary. A new knob is a schema
;; change a reviewer sees, not a free-form patch of the configuration.

(schema (id "alternative"))

;; `extension_off`, `extension_on`: `extensions.<name>.supported`; the binary refuses some alone (S, U, or Sv39 with S on), so a
;; set is declared together. `misaligned_*`: `memory.misaligned.exceptions.<kind>`, the checks made before address translation;
;; the region's own attribute changes nothing while these hold. `reservation_set_size_exp`, `invalidate_on_same_hart_store`:
;; `platform.reservation.<knob>`.
(construct (name alternative)
  (field (name case_id) (type string) (min-length 1))
  (field (name reason) (type string) (min-length 1))
  (field (name extension_off) (type string) (repeat yes) (unique yes) (min-length 1))
  (field (name extension_on) (type string) (repeat yes) (unique yes) (min-length 1))
  (field (name misaligned_load_store) (type symbol) (values None) (values AccessFault) (values AlignmentException) (optional yes))
  (field (name misaligned_lrsc) (type symbol) (values None) (values AccessFault) (values AlignmentException) (optional yes))
  (field (name misaligned_amo) (type symbol) (values None) (values AccessFault) (values AlignmentException) (optional yes))
  (field (name reservation_set_size_exp) (type integer) (optional yes))
  (field (name invalidate_on_same_hart_store) (type symbol) (values true) (optional yes)))
