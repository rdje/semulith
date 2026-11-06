;; rv64gc-fault-priority-v1.overlay.sexp — this case's reference configuration, over the profile override (schema/overlay.sexp).
;; Applied by scripts/prepare_div_inputs.py; the case pins the result as its prepared reference-config.json.
(overlay (case_id "rv64gc-fault-priority-v1")
  (reason "A misaligned AMO is judged before translation, as the statement says: the binary's default judges it after, under the same access fault.") (misaligned_amo AccessFault))
