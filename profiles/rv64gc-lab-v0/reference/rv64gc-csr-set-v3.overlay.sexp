;; rv64gc-csr-set-v3.overlay.sexp — the CSR-SET case's reference configuration, over the profile override (schema/overlay.sexp).
;; Applied by scripts/prepare_div_inputs.py; the case pins the result as its prepared reference-config.json.
(overlay (case_id "rv64gc-csr-set-v3")
  (reason "The profile selects Zicntr, so REQ-D-CSR-SET's five counter CSRs need a reference that implements it. The pinned binary does, given a source of time in a defined memory region (its one such source is a CLINT), and at one tick per instruction its counters read what the laboratory's do, one tick per step boundary. The CLINT is the reference's means of time, not a claim about a device: the laboratory declares none, and the reference's holds mip.MTIP, so the case compares mip's value only through sip (decision_reference-config-per-case.md).")
  (extension "Zicntr")
  (clint (base 0x2000000) (size 0xC000))
  (instructions_per_tick 1))
