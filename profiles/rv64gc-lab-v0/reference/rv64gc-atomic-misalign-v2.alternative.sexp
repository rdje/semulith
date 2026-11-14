;; rv64gc-atomic-misalign-v2.alternative.sexp — what selects otherwise, over this case's configuration (schema/alternative.sexp).
;; Rendered by scripts/prepare_div_inputs.py and run only by scripts/measure_config_effect.py: it selects no capture.
(alternative (case_id "rv64gc-atomic-misalign-v2")
  (reason "The specification's other choice: misaligned LR, SC and AMO raise the misaligned causes.") (misaligned_lrsc AlignmentException) (misaligned_amo AlignmentException))
