;; rv64gc-sc-deterministic-v2.overlay.sexp — this case's reference configuration, over the profile override (schema/overlay.sexp).
;; Applied by scripts/prepare_div_inputs.py; the case pins the result as its prepared reference-config.json.
(overlay (case_id "rv64gc-sc-deterministic-v2")
  (reason "The profile selects an SC that pairs only at its LR's own address: the binary's default pairs anywhere in an eight-byte set.") (require_exact_reservation_addr true))
