;; rv64gc-no-pmp-v2.alternative.sexp — what selects otherwise, over this case's configuration (schema/alternative.sexp).
;; Rendered by scripts/prepare_div_inputs.py and run only by scripts/measure_config_effect.py: it selects no capture.
(alternative (case_id "rv64gc-no-pmp-v2")
  (reason "The specification's other choice: the hart implements 16 PMP entries, which the pinned binary offers, with none configured, so an access at S's or U's privilege matches none and fails.") (pmp_count 16))
