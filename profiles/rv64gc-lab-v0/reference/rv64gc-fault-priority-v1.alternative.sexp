;; rv64gc-fault-priority-v1.alternative.sexp — what selects otherwise, over this case's configuration (schema/alternative.sexp).
;; Rendered by scripts/prepare_div_inputs.py and run only by scripts/measure_config_effect.py: it selects no capture.
(alternative (case_id "rv64gc-fault-priority-v1")
  (reason "The table's other choice: misaligned loads and stores proceed to translation.") (misaligned_load_store None))
