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
(evidence (axis G-REGRESSION) (kind external) (record "profiles/rv64gc-lab-v0/act4.sexp")
  (statement "The pinned riscv-arch-test suites I, M, Zaamo, Zalrsc, Zca, F and D (318 generated test files, 316,016 signature slots) built with the laboratory's own DUT pieces for this unit and run on this unit's model: every HTIF verdict pass, every signature equal to the Sail-derived one, spike agreeing with Sail as the control pair (P4-SYSTEM.15 slices a–c; the F and D suites with F_SUPPORTED/D_SUPPORTED declared and each file's own TEST_FLEN, 32 or 64). External tests with Sail-derived expectations — one semantics answering twice, never a second independent semantics (EVD-04). Not run: the Misalign suites, whose tests need the framework's trap handler the DUT pieces do not instantiate."))
(evidence (axis G-REGRESSION) (kind validator-mutation)
  (test (file "crates/semulith-verify/src/mutate_rv64gc/tests.rs") (fn "every_designated_mutant_is_detected_by_the_corpus"))
  (statement "The validator-mutation campaign over the complete profile's tables (P4-SYSTEM.15 slice d, EVD-09): 30 designated wrong behaviours across I, M, A, F, D, C, Zicsr and the privileged architecture, each a copy of the generated table with one row changed (a sibling's effect, Nop, the row removed, or one of the two replay controls), run under every one of the 168 tracked guests and compared with the production trace in the corpus rule's own vocabulary. All 30 are detected by at least one guest. Slice d found two the corpus could not tell apart — fle.d exercised only where <= and = agree, c.sub only where - and ^ agree — and pinned them; slice e closed both with one discriminating instruction each (d-compare's fle.d 1.0 <= 2.0, c-alu's c.sub 0 - 3), and the pin is empty: a new gap fails the test. The comparison rule has no suppression knob to misuse (EVD-09's second half is the base profile's mutate suite arm)."))
(evidence (axis G-REGRESSION) (kind generated)
  (test (file "crates/semulith-core/src/fp/tests.rs") (fn "every_spec_side_fixture_holds"))
  (statement "The generated numeric fixtures: the seeded spec-side cases from scripts/gen_fp_vectors.py, each result and flag set derived by the exact-rational authority, held by the model layer (P4-SYSTEM.7)."))
(evidence (axis G-REGRESSION) (kind generated)
  (test (file "crates/semulith-verify/src/m_vectors/tests.rs") (fn "every_generated_vector_holds_through_the_engine"))
  (statement "The generated M vectors: every M instruction over edge and seeded operands, the expected rd from scripts/gen_m_vectors.py's exact-integer reference (RVI-M §11.1, Table 1 by name), run through the engine's decode, guard and operators (P4-SYSTEM.11); the table gated by M-VECTORS."))
(evidence (axis G-TRACE) (kind experiment) (experiment "rv64gc-m-forms-v3")
  (statement "The first qualified matched experiment: the M case's measured record (33 instructions, 25 finite witnesses — the 13 M forms and the 12 Table 1 cells) with its matched-gpr-v1 verification graph — baseline, byte-identical repeat, a wrong-quotient control observed diverging, every input and observation pinned, both producer pairs assessed — credited by CR-GC-M-1 (REQ-GC-M, implemented) and qualified in the dossier only while that credit is current (P4-SYSTEM.14 a42bc). The eight earlier Sail matched experiments (P4-SYSTEM.2 to .8, .12's C corpus) stay prose in matched_scope: history, not evidence, until each is re-run as a record under the same contract."))
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
(open (axis G-OBLIGATIONS) (owner "P4-SYSTEM.14")
  (statement "Requirement statuses remain planned. EVIDENCE_POLICY.md declares the forthcoming requalification policy after the existing implementation; document presence alone proves neither timing nor adequate evidence. P4-SYSTEM.14 still owns structured records, policy/status checks and mirror reconciliation; REQ-D-ECALL-EBREAK remains partial on OQ-5."))
(open (axis G-REGRESSION) (owner "P4-SYSTEM.15")
  (statement "Four of the five required kinds are evidenced (directed, external, generated, validator-mutation). The fifth, workload, has RUN and is RECORDED — profiles/rv64gc-lab-v0/workload.sexp (P4-SYSTEM.15 slice f): four compiled, self-checking C workloads, 4 pass / 0 fail three-way, RECORD-SCHEMA rule 15 — but is not yet declared here: the GS report generator's own self-test assumes an open workload kind and the generator (scripts/gate_report.py) is a pinned input of the credited M case's dependency manifest, so changing it lapses credit CR-GC-M-1. Declaring the kind is slice g: re-capture the M case against the changed generator (or rule on the pin), then declare. The pinned Misalign suites are not applicable (generated for MISALIGNED_LDST true; the profile traps misaligned data)."))
(open (axis G-PORTABILITY) (owner "P4-SYSTEM.17")
  (statement "No portability record for this unit: the instrument's manifest is built from rv64i's guests."))
(open (axis G-RELEASE) (owner "P4-SYSTEM.18")
  (statement "No release decision is recorded for this unit."))
