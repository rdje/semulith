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
(evidence (axis G-REGRESSION) (kind generated)
  (test (file "crates/semulith-verify/src/m_vectors/tests.rs") (fn "every_generated_vector_holds_through_the_engine"))
  (statement "The generated M vectors: every M instruction over edge and seeded operands, the expected rd from scripts/gen_m_vectors.py's exact-integer reference (RVI-M §11.1, Table 1 by name), run through the engine's decode, guard and operators (P4-SYSTEM.11); the table gated by M-VECTORS."))
(evidence (axis G-REPLAY) (kind determinism)
  (test (file "crates/semulith-verify/src/run_rv64gc/tests.rs") (fn "every_guest_re_executes_identically_from_cold_reset"))
  (statement "Every guest re-executes identically from cold reset: the run is a function of the definition and the program."))
(evidence (axis G-REPLAY) (kind snapshot)
  (test (file "crates/semulith-verify/src/snapshot_rv64gc/tests.rs") (fn "every_gc_guest_resumes_through_json_with_identical_steps_state_memory_and_fetches"))
  (statement "Every tracked guest is split at three boundaries through JSON snapshots; continued steps, fetch totals, complete final CPU state and memory equal uninterrupted execution, with the same typed laboratory refusals. Reservation/wait effects, TLB slots/FIFO and corrupted/foreign/missing-state refusals have additional controls. This is laboratory snapshot evidence, not board/device or independent ISA validation."))
(evidence (axis G-REPLAY) (kind replay-bundle)
  (test (file "crates/semulith-verify/src/replay_rv64gc/tests.rs") (fn "every_gc_guest_bundle_roundtrips_and_replays_all_recorded_receipts"))
  (statement "Every tracked guest records and replays a self-contained JSON bundle: complete CPU/memory/fault-policy input, explicit no-external-event policy, trace, fetch/model-error receipts and a digest of the complete final checkpoint. Additional controls discriminate trace fields, aggregate/final receipts, foreign identities, invalid states and bounds; four system cases use the real CLI. This demonstrates laboratory reproducibility, not independent ISA correctness or board/device replay."))

(evidence (axis G-REPLAY) (kind reduction)
  (test (file "crates/semulith-verify/src/reduce_rv64gc/tests.rs") (fn "both_controls_reduce_and_replay_the_exact_original_paired_difference"))
  (statement "Both declared full-profile control models reduce with the exact original paired-step difference retained, then replay the deterministic search and both complete reduced-run receipts from self-contained JSON. Mixed 16/32-bit images, a trailing data byte, typed faults, capped search, single-chunk minimality witnesses and damaged record controls have additional tests; both models and capped records use the real CLI. This is bounded laboratory reproducibility, not independent ISA correctness or board/device replay."))

(open (axis G-STATE) (owner "P4-SYSTEM.14")
  (statement "The state requirements read planned: no requirement status is derived from evidence yet."))
(open (axis G-TRACE) (owner "P4-SYSTEM.14")
  (statement "The nine Sail matched experiments (P4-SYSTEM.2 to .8, .11's M corpus and .12's C corpus) are recorded as prose inside references.sexp's matched_scope, not as experiment records; no control or independence row is judged for them. The spec-side author and live Sail adapter are now tracked, but their existence does not substitute for experiment records."))
(open (axis G-OBLIGATIONS) (owner "P4-SYSTEM.14")
  (statement "Requirement statuses remain planned. EVIDENCE_POLICY.md declares the forthcoming requalification policy after the existing implementation; document presence alone proves neither timing nor adequate evidence. P4-SYSTEM.14 still owns structured records, policy/status checks and mirror reconciliation; REQ-D-ECALL-EBREAK remains partial on OQ-5."))
(open (axis G-REGRESSION) (owner "P4-SYSTEM.15")
  (statement "No external directed or workload suite has run against this unit. Two deliberately wrong full-table GC models are available as detector controls, but the complete validator mutation campaign remains P4-SYSTEM.15 work."))
(open (axis G-PORTABILITY) (owner "P4-SYSTEM.17")
  (statement "No portability record for this unit: the instrument's manifest is built from rv64i's guests."))
(open (axis G-RELEASE) (owner "P4-SYSTEM.18")
  (statement "No release decision is recorded for this unit."))
