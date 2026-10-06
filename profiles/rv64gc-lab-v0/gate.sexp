;; gate.sexp — rv64gc-lab-v0's evidence manifest for the CPU-SYSTEM gate (P4-SYSTEM.10 slice b).
;; Validate with:
;;   python3 scripts/check_sexp_schema.py gate.sexp schema/gate.sexp
;; Read by scripts/gate_report.py --gate GS, which VERIFIES every declaration here against the
;; tree and holds the list of kinds each axis requires; GS-REPORT.md is its derived output.

(gate (id "CPU-SYSTEM") (profile "rv64gc-lab-v0")
  (statement "The processor gate over the complete declared profile, including its environment contract (ROADMAP.md P4). The open items below were measured by the P4-SYSTEM.10 design brief's census (2026-10-06) and each is owned by a leaf of P4-SYSTEM."))

(evidence (axis G-REGRESSION) (kind directed)
  (test (file "crates/semulith-verify/src/run_rv64gc/tests.rs") (fn "every_guest_matches_its_expectations"))
  (statement "The directed corpus: every tracked guest runs on the engine and its change-observations match the expectations derived spec-side before either engine ran (EVD-05)."))
(evidence (axis G-REGRESSION) (kind generated)
  (test (file "crates/semulith-core/src/fp/tests.rs") (fn "every_spec_side_fixture_holds"))
  (statement "The generated numeric fixtures: the seeded spec-side cases from scripts/gen_fp_vectors.py, each result and flag set derived by the exact-rational authority, held by the model layer (P4-SYSTEM.7)."))
(evidence (axis G-REPLAY) (kind determinism)
  (test (file "crates/semulith-verify/src/run_rv64gc/tests.rs") (fn "every_guest_re_executes_identically_from_cold_reset"))
  (statement "Every guest re-executes identically from cold reset: the run is a function of the definition and the program."))

(open (axis G-SCOPE) (owner "P4-SYSTEM.11")
  (statement "M is declared by the profile and not bound: the encoding's m slot is unfilled; definitions/riscv/m.sexp has no semantics fragment."))
(open (axis G-SCOPE) (owner "P4-SYSTEM.12")
  (statement "C is declared by the profile and not bound: the encoding's c slot is unfilled; no compressed fragment exists."))
(open (axis G-STATE) (owner "P4-SYSTEM.13")
  (statement "The hidden-state census's consequence still describes the P4-SYSTEM.2 snapshot (the integer file, pc, memory, mode and 33 CSRs); every later candidate is answered but the consequence was never re-answered."))
(open (axis G-STATE) (owner "P4-SYSTEM.14")
  (statement "The state requirements read planned: no requirement status is derived from evidence yet."))
(open (axis G-CONTRACT) (owner "P4-SYSTEM.13")
  (statement "v0's checks are declared and not realized; rv64i's base boundary assumptions are not restated for this unit; three frozen v0 statements are stale and not superseded (OB-FP-DEFER, OB-ROUTE-FLIP, OB-RESOLUTION-ROUTE)."))
(open (axis G-TRACE) (owner "P4-SYSTEM.14")
  (statement "The seven Sail matched experiments (P4-SYSTEM.2 to .8) are recorded as prose inside references.sexp's matched_scope, not as experiment records; no control or independence row is judged for them, and their comparators are scratch."))
(open (axis G-OBLIGATIONS) (owner "P4-SYSTEM.14")
  (statement "Every requirement reads planned; no predeclared verification policy exists for this unit; REQ-D-ECALL-EBREAK (an rv64i mirror) is partial on OQ-5."))
(open (axis G-REGRESSION) (owner "P4-SYSTEM.15")
  (statement "No external directed suite has run against this unit; the validator-mutation suite decodes rv64i's tables only; no workload suite."))
(open (axis G-REPLAY) (owner "P4-SYSTEM.16")
  (statement "Snapshots, replay bundles and the reducer are rv64i-only; the CLI refuses this unit for each by name."))
(open (axis G-PORTABILITY) (owner "P4-SYSTEM.17")
  (statement "No portability record for this unit: the instrument's manifest is built from rv64i's guests."))
(open (axis G-RELEASE) (owner "P4-SYSTEM.18")
  (statement "No release decision is recorded for this unit."))
