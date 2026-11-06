;; rv64gc-zicntr-v3.overlay.sexp — the ZICNTR case's reference configuration, over the profile override (schema/overlay.sexp).
;; Applied by scripts/prepare_div_inputs.py; the case pins the result as its prepared reference-config.json.
(overlay (case_id "rv64gc-zicntr-v3")
  (reason "The profile selects Zicntr, and REQ-D-ZICNTR's reads need a reference that implements it. The pinned binary does, given a source of time in a defined memory region (its one such source is a CLINT), and at one tick per instruction its cycle and time agree with the laboratory's one tick per step boundary. The CLINT is the reference's and this case claims nothing about it: the case's limitations say so.")
  (extension "Zicntr")
  (clint (base 0x2000000) (size 0xC000))
  (instructions_per_tick 1))
