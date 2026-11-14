;; contract.sexp — a frozen subset of profiles/rv64gc-lab-v0/contract.sexp at commit 1fa19741, its version chain kept and its members and supersessions trimmed to the FP records (XTASK.13 slice k):
;; probe_experiment_graph.py judges the effective-contract scope on these records, so a damaged live dossier fails
;; PROFILE-CONSISTENCY's real check by name instead of refusing its self-test.

(contract (id "rv64gc-lab-env-v0") (version 0) (member (id "OB-FP-DEFER")))
(contract (id "rv64gc-lab-env-v1") (version 1) (extends "rv64gc-lab-env-v0"))
(contract (id "rv64gc-lab-env-v2") (version 2) (extends "rv64gc-lab-env-v1") (member (id "OB-GC-FP-QUALIFIED-V2"))
  (supersede (record "OB-FP-DEFER")))
(contract (id "rv64gc-lab-env-v3") (version 3) (extends "rv64gc-lab-env-v2") (member (id "OB-GC-FP-QUALIFIED-V3"))
  (supersede (record "OB-GC-FP-QUALIFIED-V2")))
