;; credits.sexp — the credited dispositions of profile rv64gc-lab-v0 (schema/credits.sexp).
;; A credit is a record the derivation authenticates on every read (decision_credit-is-a-catalogue-record.md):
;; its pins must still describe the tree, its case's receipt must be a complete capture carrying no verdict,
;; and its policy measurement must be satisfied; otherwise it is lapsed and the status falls back.
(credit (id "CR-GC-M-1") (profile_ids "rv64gc-lab-v0") (requirement_id "REQ-GC-M") (obligation_ids "OB-GC-M")
  (case_id "rv64gc-m-forms-v3")
  (measured (pin (path "evidence/rv64gc-m-forms-v3/measured-experiment.sexp") (sha256 "fb22d5e5554a0e132c231e5551ed8314ab4be35ff93e7f086fceeacb6235a152") (byte_size 16942)))
  (receipt (pin (path "evidence/rv64gc-m-forms-v3/verification.json") (sha256 "91a90d9c56487af1a6b4306e9007d771e17246ddf41b358185374680090a5a5d") (byte_size 7017)))
  (policy (pin (path "profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md") (sha256 "85296cf7ae694f0d40e08ed398989d32f20f4720d4a798bf46a18caf22825071") (byte_size 9230)))
  (retained_sources "RVI-M-DIV-STATEMENT") (retained_sources "RVI-M-STATEMENTS")
  (authority review) (date "2026-10-26") (decision "decision_req-gc-m-credited-implemented.md") (legs 10)
  (limitations "one finite case: 25 witnesses, the 13 M forms and the 12 Table 1 cells, one each")
  (limitations "the receipt's own limitation: not all M or CPU acceptance")
  (limitations "credits implemented only, under the director's delegation of 2026-10-26 (decision_four-rulings-delegated.md); no claim about other extensions or about acceptance"))
