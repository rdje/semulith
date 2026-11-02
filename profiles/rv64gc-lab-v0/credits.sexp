;; credits.sexp — the credited dispositions of profile rv64gc-lab-v0 (schema/credits.sexp).
;; A credit is a record the derivation authenticates on every read (decision_credit-is-a-catalogue-record.md):
;; its pins must still describe the tree, its case's receipt must be a complete capture carrying no verdict,
;; and its policy measurement must be satisfied; otherwise it is lapsed and the status falls back.
;; P4-SYSTEM.14 a43b-2e: the planned lapse that opens CSR-SET retired CR-GC-M-2 and CR-D-XLEN-1 with this file (a43b-2b);
;; both cases were re-captured once, their control declared, traces byte-identical (a43b-2d), and are credited again by
;; the same act (decision_req-gc-m-credited-implemented.md; decision_req-d-xlen-credited-implemented.md).
(credit (id "CR-GC-M-3") (profile_ids "rv64gc-lab-v0") (requirement_id "REQ-GC-M") (obligation_ids "OB-GC-M")
  (case_id "rv64gc-m-forms-v5")
  (measured (pin (path "evidence/rv64gc-m-forms-v5/measured-experiment.sexp") (sha256 "1530832dd74c83297543d5fb5d1d150633cc3deeb46df7afcac11802ff657f8f") (byte_size 16942)))
  (receipt (pin (path "evidence/rv64gc-m-forms-v5/verification.json") (sha256 "b5fb667a82a5f05a202890702f165463db44202cd56a595b82d58c4e2203e29b") (byte_size 7021)))
  (policy (pin (path "profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md") (sha256 "85296cf7ae694f0d40e08ed398989d32f20f4720d4a798bf46a18caf22825071") (byte_size 9230)))
  (retained_sources "RVI-M-DIV-STATEMENT") (retained_sources "RVI-M-STATEMENTS")
  (authority review) (date "2026-11-02") (decision "decision_req-gc-m-credited-implemented.md") (legs 10)
  (limitations "one finite case: 25 witnesses, the 13 M forms and the 12 Table 1 cells, one each")
  (limitations "the receipt's own limitation: not all REQ-GC-M or CPU acceptance")
  (limitations "credits implemented only, under the director's delegation of 2026-10-26 (decision_four-rulings-delegated.md) and ruling 1 of 2026-10-28 (decision_case-declarations-as-data.md: the credit re-issued against the new capture); no claim about other extensions or about acceptance"))
(credit (id "CR-D-XLEN-2") (profile_ids "rv64gc-lab-v0") (requirement_id "REQ-D-XLEN") (obligation_ids "OB-XLEN")
  (case_id "rv64gc-xlen-forms-v2")
  (measured (pin (path "evidence/rv64gc-xlen-forms-v2/measured-experiment.sexp") (sha256 "3e536d08b739ffd8a1ffd75d9dcf8ca438b4f7f77cb99475718cb41984f58fad") (byte_size 14979)))
  (receipt (pin (path "evidence/rv64gc-xlen-forms-v2/verification.json") (sha256 "fbbfb66f1f21c2e667b46fa06d4cd4a4d14fb32f0224e889770868522531a1c6") (byte_size 7064)))
  (policy (pin (path "profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md") (sha256 "85296cf7ae694f0d40e08ed398989d32f20f4720d4a798bf46a18caf22825071") (byte_size 9230)))
  (retained_sources "RVI-RV64I-STATEMENTS")
  (authority review) (date "2026-11-02") (decision "decision_req-d-xlen-credited-implemented.md") (legs 10)
  (limitations "one finite case: 17 witnesses, one each - bit 63 and the 2^64 wrap, the shift amounts, RV64 LUI, the *W family, and a 64-bit address reported whole through mtval")
  (limitations "the receipt's own limitation: not all REQ-D-XLEN or CPU acceptance")
  (limitations "credits implemented only, under the director's delegation of 2026-10-26 (decision_four-rulings-delegated.md); no claim about the address space's regions, other privilege modes, or acceptance"))
