;; gate.sexp — the schema of a unit's GATE EVIDENCE MANIFEST (P4-SYSTEM.10 slice b).
;;
;; The processor gate (docs/EVIDENCE_AND_GATES.md §7) asks ten questions, and five of them are
;; answered by suites and records whose location is the unit's own business: which test runs the
;; directed corpus, where the external campaign's verdicts are recorded, which experiment records
;; the trace rests on. A report generator that hard-codes those locations reports one unit's facts
;; about another (measured: `build_cpulab` read rv64i's replay suites for rv64gc and read green).
;; So the UNIT declares where its evidence is, and the generator (scripts/gate_report.py --gate GS)
;; VERIFIES each declaration against the tree — a test function must exist in a tracked file, a
;; record must be tracked and carry a passing verdict, an experiment must be a record in
;; references.sexp. The KINDS each axis requires are the gate's definition, held by the generator,
;; never by the unit: a kind with no verified evidence reads open, whatever this file says.

(schema (id "gate"))

(construct (name gate)
  (field (name id) (type string) (pattern "^[A-Z][A-Z0-9-]*$"))
  (field (name profile) (type string) (pattern "^[A-Za-z][A-Za-z0-9._:/-]*$"))
  (field (name statement) (type string) (min-length 1)))

;; One piece of evidence for one required kind of one axis. Exactly one of test / record /
;; experiment locates it (the generator refuses none or several).
(construct (name evidence)
  (field (name axis) (type symbol) (values G-TRACE) (values G-REGRESSION) (values G-PORTABILITY)
         (values G-REPLAY) (values G-RELEASE))
  (field (name kind) (type symbol))
  (field (name test) (type form) (head test) (optional yes))
  (field (name record) (type string) (optional yes) (pattern "^[A-Za-z0-9_./-]+$"))
  (field (name experiment) (type string) (optional yes) (min-length 1))
  (field (name statement) (type string) (min-length 1)))

;; A test function in a tracked Rust file — run by `cargo test`, which `make check` runs before
;; every commit.
(construct (name test)
  (field (name file) (type string) (pattern "^crates/[A-Za-z0-9_/-]+\\.rs$"))
  (field (name fn) (type string) (pattern "^[a-z_][a-z0-9_]*$")))

;; A required kind this unit declares does not apply — printed in the report with its reason, so
;; the reader judges it; it is never silent.
(construct (name not-applicable)
  (field (name axis) (type symbol))
  (field (name kind) (type symbol))
  (field (name why) (type string) (min-length 1)))

;; Something the gate finds open, with the task-tree leaf that owns closing it (defect ownership:
;; nothing open without an owner). Informational: the MEASURE decides an axis, never this form.
(construct (name open)
  (field (name axis) (type symbol))
  (field (name owner) (type string) (pattern "^[A-Z][A-Z0-9-]*\\.[0-9]+$"))
  (field (name statement) (type string) (min-length 1)))
