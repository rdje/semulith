;; rv64gc-composition-v1.overlay.sexp — this case's reference configuration, over the profile override (schema/overlay.sexp).
;; Applied by scripts/prepare_div_inputs.py; the case pins the result as its prepared reference-config.json.
(overlay (case_id "rv64gc-composition-v1")
  (reason "The composition includes Zicntr, and the pinned binary implements it given a source of time in a defined memory region. At one tick per instruction its counters agree with the laboratory's.") (extension "Zicntr")
  (clint (base 0x2000000) (size 0xC000))
  (instructions_per_tick 1))
