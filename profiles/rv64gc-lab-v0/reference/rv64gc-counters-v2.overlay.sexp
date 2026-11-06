;; rv64gc-counters-v2.overlay.sexp — this case's reference configuration, over the profile override (schema/overlay.sexp).
;; Applied by scripts/prepare_div_inputs.py; the case pins the result as its prepared reference-config.json.
(overlay (case_id "rv64gc-counters-v2")
  (reason "The profile selects Zicntr, and these reads need a reference that implements it. The pinned binary does, given a source of time in a defined memory region (its one such source is a CLINT), and at one tick per instruction.")
  (extension "Zicntr")
  (clint (base 0x2000000) (size 0xC000))
  (instructions_per_tick 1))
