;; rv64gc-sstc-v3.overlay.sexp — the SSTC case's reference configuration, over the profile override (schema/overlay.sexp).
;; Applied by scripts/prepare_div_inputs.py; the case pins the result as its prepared reference-config.json.
(overlay (case_id "rv64gc-sstc-v3")
  (reason "REQ-D-SSTC's delivery and suppression need a reference with a source of time, since stimecmp is compared against time. The pinned binary has one in a defined memory region (a CLINT), and at one tick per instruction its time agrees with the laboratory's one tick per step boundary. Zicntr is on because time is its CSR. The CLINT is the reference's and this case claims nothing about it: the case's limitations say so.")
  (extension "Zicntr")
  (clint (base 0x2000000) (size 0xC000))
  (instructions_per_tick 1))
