;; config-effect.sexp — the schema for what ran to observe one case's reference configuration
;; (profiles/<profile>/reference/<case-id>.effect.sexp, beside its raw .effect.trace).
;;
;; The policy's `implementation-defined` row asks for a pinned matching reference configuration with a behavior-changing
;; control, and calls a configuration without an observed effect insufficient (decision_reference-config-per-case.md).
;; scripts/measure_config_effect.py runs a case's guest through the same binary under the profile override, once. The record
;; names what ran by digest and carries no verdict: the policy review re-derives the first difference from the retained trace
;; and the case's own baseline expectation, on every read.

(schema (id "config-effect"))

(construct (name config_effect)
  (field (name case_id) (type string) (pattern "^[a-z0-9][a-z0-9-]*-v[0-9]+\\Z"))
  (field (name binary_sha256) (type string) (pattern "^[0-9a-f]{64}\\Z"))
  (field (name guest_sha256) (type string) (pattern "^[0-9a-f]{64}\\Z"))
  (field (name case_config_sha256) (type string) (pattern "^[0-9a-f]{64}\\Z"))
  (field (name alternative_config_sha256) (type string) (pattern "^[0-9a-f]{64}\\Z"))
  (field (name instructions) (type integer))
  (field (name trace_sha256) (type string) (pattern "^[0-9a-f]{64}\\Z"))
  (field (name trace_bytes) (type integer)))
