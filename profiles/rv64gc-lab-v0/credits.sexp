;; credits.sexp — the credited dispositions of profile rv64gc-lab-v0 (schema/credits.sexp).
;; A credit is a record the derivation authenticates on every read (decision_credit-is-a-catalogue-record.md):
;; its pins must still describe the tree, its case's receipt must be a complete capture carrying no verdict,
;; and its policy measurement must be satisfied; otherwise it is lapsed and the status falls back.
;; Every record here credits implemented only, under the director's delegation of 2026-10-26 (decision_four-rulings-delegated.md) and ruling 1 of 2026-10-28 (decision_case-declarations-as-data.md: the credit re-issued against the new capture); no claim about other extensions or about acceptance: each record's `decision` says which step. It stood in each record's limitations until a51-7 moved it here, for the file's bound.
;; P4-SYSTEM.14 a49-3: the window that carries fetch faults retired the 19 earlier records (a49-1, recoverable from 82498e5e). Each case was
;; re-captured once, the unchanged ones' traces byte-identical (a49-2), and is credited again by the same act under 11 legs; Batch II-b's four join them
;; (decision_the-window-that-carries-fetch-faults.md, decision_batch-ii-b-credited-implemented.md).
;; P4-SYSTEM.14 a50-4: the seven with a switch join them, each measured against what selects otherwise (decision_seven-credited-implemented.md).
;; P4-SYSTEM.14 a51-3: the six `defined` of the last 17 (decision_six-defined-credited-implemented.md).
;; P4-SYSTEM.14 a51-6: the two with a switch of the last 17 (decision_the-two-with-a-switch-credited-implemented.md).
;; P4-SYSTEM.14 a51-10: the four with no switch of the last 17 (decision_the-four-with-no-switch-credited-implemented.md).
;; P4-SYSTEM.14 a51-14: the four with nothing to run, each on a selection's record (decision_the-four-with-nothing-to-run-credited-implemented.md).
;; P4-SYSTEM.20 slice a: version 1's window moved the version label out of profile.sexp, which every case pins, and
;; retired the 42 case-backed records it lapsed by removal, recoverable at a88b01a0; the four with nothing to run stand.
;; Slice f re-issues them against the new captures (decision_the-next-window-is-version-1.md, items 4 and 6).

(credit (id "CR-D-ABI-1") (profile_ids "rv64gc-lab-v0") (requirement_id "REQ-D-ABI") (obligation_ids "OB-ABI")
  (selection "SEL-ABI")
  (measured (pin (path "profiles/rv64gc-lab-v0/selections/SEL-ABI.selection.sexp") (sha256 "6d8cb0861b72c757922fa15f8459dcf2b88ee2f50ae2a0b8d6afde69584cdf21") (byte_size 2692)))
  (policy (pin (path "profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md") (sha256 "35d6667ad0b241a7f937b90bd42fdc12fc7401cf179dec02e98f46b9da5e108c") (byte_size 10085)))
  (retained_sources "RVI-PSABI")
  (authority review) (date "2026-11-07") (decision "decision_the-four-with-nothing-to-run-credited-implemented.md") (legs 8)
  (limitations "what was selected and how it is held, read from the tree on each read; its limits are the record's own, in SEL-ABI"))
(credit (id "CR-D-FP-DEFER-1") (profile_ids "rv64gc-lab-v0") (requirement_id "REQ-D-FP-DEFER") (obligation_ids "OB-GC-FP-QUALIFIED-V3")
  (selection "SEL-FP-DEFER")
  (measured (pin (path "profiles/rv64gc-lab-v0/selections/SEL-FP-DEFER.selection.sexp") (sha256 "5e34e9721685da40f573a3268acfd644ec32c1e72862dceb5f07758dc0fb5532") (byte_size 3389)))
  (policy (pin (path "profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md") (sha256 "35d6667ad0b241a7f937b90bd42fdc12fc7401cf179dec02e98f46b9da5e108c") (byte_size 10085)))
  (retained_sources "RVI-PSABI")
  (authority review) (date "2026-11-07") (decision "decision_the-four-with-nothing-to-run-credited-implemented.md") (legs 13)
  (limitations "what was selected and how it is held, read from the tree on each read; its limits are the record's own, in SEL-FP-DEFER"))
(credit (id "CR-D-ROUTE-FLIP-1") (profile_ids "rv64gc-lab-v0") (requirement_id "REQ-D-ROUTE-FLIP") (obligation_ids "OB-GC-DEFINITION-V3")
  (selection "SEL-ROUTE-FLIP")
  (measured (pin (path "profiles/rv64gc-lab-v0/selections/SEL-ROUTE-FLIP.selection.sexp") (sha256 "42ff668e076442d8c4ad9310c6e48e8f3e0c1bfbb15bd02c5e6fdf434513c605") (byte_size 2703)))
  (policy (pin (path "profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md") (sha256 "35d6667ad0b241a7f937b90bd42fdc12fc7401cf179dec02e98f46b9da5e108c") (byte_size 10085)))
  (retained_sources "RVI-INTRO")
  (authority review) (date "2026-11-07") (decision "decision_the-four-with-nothing-to-run-credited-implemented.md") (legs 8)
  (limitations "what was selected and how it is held, read from the tree on each read; its limits are the record's own, in SEL-ROUTE-FLIP"))
(credit (id "CR-D-SCOPE-CENSUS-1") (profile_ids "rv64gc-lab-v0") (requirement_id "REQ-D-SCOPE-CENSUS") (obligation_ids "OB-SCOPE-CENSUS")
  (selection "SEL-SCOPE-CENSUS")
  (measured (pin (path "profiles/rv64gc-lab-v0/selections/SEL-SCOPE-CENSUS.selection.sexp") (sha256 "52ab65bd53a52ba3566e1653654c1a05afd65ec56a68ee9a7f99dee39360257c") (byte_size 1941)))
  (policy (pin (path "profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md") (sha256 "35d6667ad0b241a7f937b90bd42fdc12fc7401cf179dec02e98f46b9da5e108c") (byte_size 10085)))
  (retained_sources "RVI-RV32I")
  (authority review) (date "2026-11-07") (decision "decision_the-four-with-nothing-to-run-credited-implemented.md") (legs 7)
  (limitations "what was selected and how it is held, read from the tree on each read; its limits are the record's own, in SEL-SCOPE-CENSUS"))
