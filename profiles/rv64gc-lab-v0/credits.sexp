;; credits.sexp — the credited dispositions of profile rv64gc-lab-v0 (schema/credits.sexp).
;; A credit is a record the derivation authenticates on every read (decision_credit-is-a-catalogue-record.md):
;; its pins must still describe the tree, its case's receipt must be a complete capture carrying no verdict,
;; and its policy measurement must be satisfied; otherwise it is lapsed and the status falls back.
;; CR-GC-M-2 re-issues CR-GC-M-1 (a42az, retired at P4-SYSTEM.14 a44-2b) against the M case's v4 capture through the
;; same crediting act (decision_req-gc-m-credited-implemented.md, Retirement; decision_case-declarations-as-data.md).
(credit (id "CR-GC-M-2") (profile_ids "rv64gc-lab-v0") (requirement_id "REQ-GC-M") (obligation_ids "OB-GC-M")
  (case_id "rv64gc-m-forms-v4")
  (measured (pin (path "evidence/rv64gc-m-forms-v4/measured-experiment.sexp") (sha256 "aadb5ef3360f1d14a79258522eea098802d492889a747d5be41eeed69e106e08") (byte_size 16942)))
  (receipt (pin (path "evidence/rv64gc-m-forms-v4/verification.json") (sha256 "1d4b1b5d5472a85b0c47ba2a835c04aec314ae4d5ed1d5ca872754a771f91e16") (byte_size 7017)))
  (policy (pin (path "profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md") (sha256 "85296cf7ae694f0d40e08ed398989d32f20f4720d4a798bf46a18caf22825071") (byte_size 9230)))
  (retained_sources "RVI-M-DIV-STATEMENT") (retained_sources "RVI-M-STATEMENTS")
  (authority review) (date "2026-10-29") (decision "decision_req-gc-m-credited-implemented.md") (legs 10)
  (limitations "one finite case: 25 witnesses, the 13 M forms and the 12 Table 1 cells, one each")
  (limitations "the receipt's own limitation: not all M or CPU acceptance")
  (limitations "credits implemented only, under the director's delegation of 2026-10-26 (decision_four-rulings-delegated.md) and ruling 1 of 2026-10-28 (decision_case-declarations-as-data.md: the credit re-issued against the new capture); no claim about other extensions or about acceptance"))
;; CR-D-XLEN-1 credits REQ-D-XLEN through the XLEN case's one capture (P4-SYSTEM.14 a43a-3), by the same act and on the
;; same rulings as the M case's (decision_req-d-xlen-credited-implemented.md); the first `state` requirement credited.
(credit (id "CR-D-XLEN-1") (profile_ids "rv64gc-lab-v0") (requirement_id "REQ-D-XLEN") (obligation_ids "OB-XLEN")
  (case_id "rv64gc-xlen-forms-v1")
  (measured (pin (path "evidence/rv64gc-xlen-forms-v1/measured-experiment.sexp") (sha256 "d39825b0b4d7ccbada20d4d0545f26bb5fce1a79b5003b16dd99997cce041e41") (byte_size 14958)))
  (receipt (pin (path "evidence/rv64gc-xlen-forms-v1/verification.json") (sha256 "72413fdfc829b75fa6144b1405d39eed459ffc72dda7bcc93c62dc3e4c317fd2") (byte_size 7055)))
  (policy (pin (path "profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md") (sha256 "85296cf7ae694f0d40e08ed398989d32f20f4720d4a798bf46a18caf22825071") (byte_size 9230)))
  (retained_sources "RVI-RV64I-STATEMENTS")
  (authority review) (date "2026-10-29") (decision "decision_req-d-xlen-credited-implemented.md") (legs 10)
  (limitations "one finite case: 17 witnesses, one each - bit 63 and the 2^64 wrap, the shift amounts, RV64 LUI, the *W family, and a 64-bit address reported whole through mtval")
  (limitations "the receipt's own limitation, written by the producer for every case at the time: 'not all M or CPU acceptance'; read as not all REQ-D-XLEN or CPU acceptance (P4-SYSTEM.14 a43a-2e)")
  (limitations "the measured record's control prose and control-run id ('wrong quotient must diverge', 'wrong-quotient') are the pinned producer's fixed M text; the control-run's reason states this case's control, the address truncated to 32 bits")
  (limitations "credits implemented only, under the director's delegation of 2026-10-26 (decision_four-rulings-delegated.md); no claim about the address space's regions, other privilege modes, or acceptance"))
