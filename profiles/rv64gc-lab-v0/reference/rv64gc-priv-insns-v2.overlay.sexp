;; rv64gc-priv-insns-v2.overlay.sexp — this case's reference configuration, over the profile override (schema/overlay.sexp).
;; Applied by scripts/prepare_div_inputs.py; the case pins the result as its prepared reference-config.json.
(overlay (case_id "rv64gc-priv-insns-v2")
  (reason "The profile's wfi waits, so the reference's must too: the override's no-op would agree with anything.") (wfi_is_nop false))
