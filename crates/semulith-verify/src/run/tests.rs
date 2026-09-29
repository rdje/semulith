//! Tests for the observation runner and the first-divergence comparator. The comparator's
//! RED/GREEN arms mirror `scripts/compare_traces.py`'s self-test: a comparator that has
//! only ever agreed is not known to disagree.

use super::*;
use crate::fixtures::FlatMemory;
use semulith_core::env::{AccessWidth, Request};

fn step(pc: u64, word: u32, writes: &[(u8, u64)], trap: Option<(u8, u64)>) -> Step {
    Step {
        pc,
        word: Some(word),
        writes: writes.to_vec(),
        trap,
    }
}

const A: &str = "model-a";
const B: &str = "model-b";

#[test]
fn identical_streams_agree_including_the_trap() {
    let a = [
        step(0x80000000, 0x00100513, &[(10, 1)], None),
        step(0x80000004, 0x40152083, &[], Some((0x04, 0x80000401))),
    ];
    let b = a.clone();
    let verdict = compare(&a, &b, (A, B)).unwrap();
    assert_eq!(verdict, Verdict::Agree { steps: 2 });
    assert!(render(&verdict, 2, 2, (A, B)).starts_with("AGREE over 2"));
}

#[test]
fn a_register_value_divergence_names_the_step_and_register() {
    let a = [
        step(0x80000000, 0x00100513, &[(10, 1)], None),
        step(0x80000004, 0x40152083, &[], Some((0x04, 0x80000401))),
    ];
    let mut b = a.clone();
    b[0].writes = vec![(10, 2)];
    let verdict = compare(&a, &b, (A, B)).unwrap();
    match &verdict {
        Verdict::Divergence(d) => {
            assert_eq!(d.at, 0);
            assert!(d.what.contains("x10"), "names the register: {}", d.what);
            assert!(d.what.contains("model-a") && d.what.contains("model-b"));
        }
        other => panic!("expected a divergence, got {other:?}"),
    }
    assert!(render(&verdict, 2, 2, (A, B)).contains("FIRST DIVERGENCE at aligned step 0"));
}

#[test]
fn a_trap_cause_divergence_is_found_at_the_trapping_step() {
    let a = [
        step(0x80000000, 0x00100513, &[(10, 1)], None),
        step(0x80000004, 0x40152083, &[], Some((0x06, 0x80000401))),
    ];
    let b = [
        step(0x80000000, 0x00100513, &[(10, 1)], None),
        step(0x80000004, 0x40152083, &[], Some((0x04, 0x80000401))),
    ];
    let verdict = compare(&a, &b, (A, B)).unwrap();
    match &verdict {
        Verdict::Divergence(d) => {
            assert_eq!(d.at, 1);
            assert!(d.what.contains("cause"), "names the trap cause: {}", d.what);
        }
        other => panic!("expected a divergence, got {other:?}"),
    }
}

#[test]
fn a_trap_tval_divergence_is_found() {
    let a = [
        step(0x80000000, 0x00100513, &[(10, 1)], None),
        step(0x80000004, 0x40152083, &[], Some((0x04, 0xdeadbeef))),
    ];
    let b = [
        step(0x80000000, 0x00100513, &[(10, 1)], None),
        step(0x80000004, 0x40152083, &[], Some((0x04, 0x80000401))),
    ];
    let verdict = compare(&a, &b, (A, B)).unwrap();
    match &verdict {
        Verdict::Divergence(d) => {
            assert_eq!(d.at, 1);
            assert!(d.what.contains("tval"), "names the tval: {}", d.what);
        }
        other => panic!("expected a divergence, got {other:?}"),
    }
}

#[test]
fn a_missing_write_is_a_divergence() {
    let a = [step(0x80000000, 0x00100513, &[(10, 1)], None)];
    let b = [step(0x80000000, 0x00100513, &[], None)];
    let verdict = compare(&a, &b, (A, B)).unwrap();
    match &verdict {
        Verdict::Divergence(d) => {
            assert_eq!(d.at, 0);
            assert!(
                d.what.contains("x10"),
                "names the missing write: {}",
                d.what
            );
        }
        other => panic!("expected a divergence, got {other:?}"),
    }
}

#[test]
fn a_length_mismatch_is_not_a_pass() {
    let a = [
        step(0x80000000, 0x00100513, &[(10, 1)], None),
        step(0x80000004, 0x40152083, &[], Some((0x04, 0x80000401))),
    ];
    let b = [a[0].clone()];
    let verdict = compare(&a, &b, (A, B)).unwrap();
    assert_eq!(
        verdict,
        Verdict::LengthMismatch {
            agreed: 1,
            longer: A.to_string(),
        }
    );
    let text = render(&verdict, 2, 1, (A, B));
    assert!(text.contains("LENGTH MISMATCH"), "{text}");
    assert!(text.contains("NOT a pass"), "{text}");
}

#[test]
fn an_empty_stream_is_refused_not_a_match() {
    let a = [step(0x80000000, 0x00100513, &[(10, 1)], None)];
    assert!(compare(&[], &a, (A, B)).is_err());
    assert!(compare(&a, &[], (A, B)).is_err());
}

// ---- the runner ---------------------------------------------------------------------------------

const ENTRY: u64 = 0x80000000;

fn flat(words: &[u32]) -> FlatMemory {
    let mut env = FlatMemory::new(ENTRY, 0x1000);
    let mut image = Vec::with_capacity(words.len() * 4);
    for word in words {
        image.extend_from_slice(&word.to_le_bytes());
    }
    env.load_image(0, &image);
    env
}

#[test]
fn runner_records_observations_and_crossings() {
    // addi x1, x0, 5 ; addi x2, x1, -1 — a budget of 2 stops the run after both steps
    // (past them lies zeroed memory, whose words are reserved decodes).
    let mut env = flat(&[0x0050_0093, 0xfff0_8113]);
    let (trace, crossings) = run(&mut env, ENTRY, 2);
    assert_eq!(trace.stop, Stop::Budget);
    assert_eq!(trace.steps.len(), 2);
    assert_eq!(trace.steps[0].pc, ENTRY);
    assert_eq!(trace.steps[0].word, Some(0x0050_0093));
    assert_eq!(trace.steps[0].writes, vec![(1, 5)]);
    assert_eq!(trace.steps[1].writes, vec![(2, 4)]);
    // one fetch per step, no more (OB-ENV-FETCH-SUPPLY's no-extraneous-fetch clause).
    let fetches = crossings
        .iter()
        .filter(|c| matches!(c.request, Request::Fetch { .. }))
        .count();
    assert_eq!(fetches, 2);
    assert_eq!(env.fetch_count(), 2);
}

#[test]
fn runner_stops_at_a_trap_with_the_trapping_step_last() {
    // addi x1, x0, 5 ; lw x3, 2(x1) — effective address 7, misaligned.
    let mut env = flat(&[0x0050_0093, 0x0020_a183]);
    let (trace, crossings) = run(&mut env, ENTRY, 16);
    assert_eq!(trace.stop, Stop::Trap);
    assert_eq!(trace.steps.len(), 2);
    let last = &trace.steps[1];
    assert_eq!(last.pc, ENTRY + 4);
    assert_eq!(last.word, Some(0x0020_a183));
    assert_eq!(last.writes, vec![]);
    assert_eq!(last.trap, Some((0x04, 7)));
    // The misaligned load never crossed the boundary: the only load-class crossing is
    // absent; the fetch count proves nothing else happened either.
    assert!(!crossings
        .iter()
        .any(|c| matches!(c.request, Request::Load { .. })));
}

#[test]
fn runner_never_records_an_x0_write() {
    // addi x0, x0, 5 — the write is architecturally discarded, so the observation shows none.
    let mut env = flat(&[0x0050_0013]);
    let (trace, _) = run(&mut env, ENTRY, 16);
    assert_eq!(trace.steps[0].writes, vec![]);
}

#[test]
fn runner_observes_stores_in_the_crossing_log() {
    // addi x1, x0, 5 ; addi x2, x0, 1 ; slli x2, x2, 31 (x2 = ENTRY) ; sb x1, 16(x2).
    // Budget 4 stops the run exactly at the program's end: past it lies zeroed memory,
    // whose words are reserved decodes — which the runner now converts and RECORDS
    // (D-RESERVED-DECODE's policy step), so an over-generous budget would add a step.
    let mut env = flat(&[0x0050_0093, 0x0010_0113, 0x01F1_1113, 0x0011_0823]);
    let (trace, crossings) = run(&mut env, ENTRY, 4);
    assert_eq!(trace.steps.len(), 4);
    let stored = crossings.iter().any(|c| {
        matches!(
            c.request,
            Request::Store {
                width: AccessWidth::B,
                addr: 0x8000_0010,
                data: 5,
            }
        )
    });
    assert!(stored, "the store crossing is recorded: {crossings:x?}");
    assert_eq!(env.bytes()[0x10], 5);
}

#[test]
fn fetch_fault_records_the_word_less_step() {
    // Entry just past the region's top: the very first fetch faults. The observation is
    // the honest step — the pc, the trap the rule reports, and NO word (a fetch that
    // failed supplied none; inventing one would put a fiction in the vocabulary).
    let mut env = FlatMemory::new(ENTRY, 0x1000);
    let (trace, crossings) = run(&mut env, ENTRY + 0x1000, 4);
    assert_eq!(
        trace.steps,
        vec![Step {
            pc: ENTRY + 0x1000,
            word: None,
            writes: Vec::new(),
            trap: Some((0x01, ENTRY + 0x1000)),
        }]
    );
    assert_eq!(trace.stop, Stop::FetchFault { at: ENTRY + 0x1000 });
    assert!(crossings
        .iter()
        .any(|c| matches!(c.request, Request::Fetch { addr } if addr == ENTRY + 0x1000)));
}

#[test]
fn reserved_decode_is_converted_by_policy_and_keeps_its_classification() {
    // addi x1, x0, 5, then a word no row matches (zeroed memory): the interpreter reports
    // the reserved case; the laboratory's D-RESERVED-DECODE policy — the harness's act,
    // never the interpreter's — converts it to the illegal-instruction observation with
    // the reserved word as tval, and the stop reason keeps the source classification.
    let mut env = flat(&[0x0050_0093]);
    let (trace, _) = run(&mut env, ENTRY, 4);
    assert_eq!(trace.steps.len(), 2);
    assert_eq!(
        trace.steps[1],
        Step {
            pc: ENTRY + 4,
            word: Some(0),
            writes: Vec::new(),
            trap: Some((0x02, 0)),
        }
    );
    assert!(matches!(
        trace.stop,
        Stop::Undefined(UndefinedCase::ReservedDecode { at }) if at == ENTRY + 4
    ));
}

// ---- the tracked guests: the offline differential, commitment-gated ----------------------------

use crate::guests::{Guest, GUESTS};

/// Run one tracked guest under the laboratory fixture. The region is declared 64 KiB at the
/// entry: every observation the tracked guests make (stores at +0x400, faults at 0x0200_BFF8,
/// misaligned accesses judged before region membership) is identical under any region size
/// from there up to the platform's declared 2 GiB — the size is not what any of them probes.
fn run_guest(name: &str) -> (Trace, Vec<Crossing>, &'static Guest) {
    let guest = GUESTS
        .iter()
        .find(|g| g.name == name)
        .unwrap_or_else(|| panic!("guest {name} is in the generated fixture"));
    let mut env = FlatMemory::new(guest.entry, 0x10000);
    let mut image = Vec::with_capacity(guest.words.len() * 4);
    for word in guest.words {
        image.extend_from_slice(&word.to_le_bytes());
    }
    env.load_image(0, &image);
    let (trace, crossings) = run(&mut env, guest.entry, guest.executed_steps);
    (trace, crossings, guest)
}

fn assert_guest_observations(name: &str, want_stop: Stop) {
    let (trace, crossings, guest) = run_guest(name);
    assert_eq!(
        trace.steps.len(),
        guest.executed_steps,
        "{name}: the trace runs exactly the declared step count"
    );
    assert_eq!(trace.stop, want_stop, "{name}: stop reason");
    for (i, expected) in guest.expected.iter().enumerate() {
        assert_eq!(
            expected.step, i,
            "{name}: the fixture's expectations are declared in step order"
        );
        assert_eq!(
            trace.steps[i].writes, expected.writes,
            "{name}: step {i} writes match the specification-derived expectations"
        );
    }
    let mut written: Vec<u8> = trace
        .steps
        .iter()
        .flat_map(|s| s.writes.iter().map(|(r, _)| *r))
        .collect();
    written.sort_unstable();
    for reg in guest.never_written {
        assert!(
            !written.contains(reg),
            "{name}: x{reg} must never be written, but the trace wrote it"
        );
    }
    let fetches = crossings
        .iter()
        .filter(|c| matches!(c.request, Request::Fetch { .. }))
        .count();
    assert_eq!(
        fetches, guest.executed_steps,
        "{name}: exactly one fetch per executed step (no extraneous fetch)"
    );
}

#[test]
fn smoke_arith_matches_its_specification_derived_expectations() {
    // 12 steps, then the budget is spent (the program retires into the run bound exactly
    // as the references' instruction limits bound theirs).
    assert_guest_observations("smoke-arith", Stop::Budget);
    let (trace, crossings, _) = run_guest("smoke-arith");
    // The access observation: step 11's SD commits x9 = 0xFFFFFFFF00000001 (the step-8
    // expectation value) to 0x80000400 — the only data crossing the whole run.
    let stores: Vec<_> = crossings
        .iter()
        .filter(|c| matches!(c.request, Request::Store { .. }))
        .collect();
    assert_eq!(stores.len(), 1, "smoke-arith: exactly one store crossing");
    assert!(matches!(
        stores[0].request,
        Request::Store {
            width: AccessWidth::D,
            addr: 0x8000_0400,
            data: 0xFFFF_FFFF_0000_0001,
        }
    ));
    assert!(trace.steps[11].trap.is_none());
}

#[test]
fn guest_control_matches_its_specification_derived_expectations() {
    // 13 executed steps from 12 instructions: the loop body runs three times. The
    // never_written registers (x6, x13) are the negative observations — a control
    // transfer that failed to skip would write them.
    assert_guest_observations("guest-control", Stop::Budget);
}

#[test]
fn smoke_trap_reports_the_misaligned_load_and_stops() {
    let (trace, _, _) = run_guest("smoke-trap");
    assert_eq!(trace.steps.len(), 3);
    assert_eq!(trace.stop, Stop::Trap);
    // The pinned derivation: cause 0x04 (misaligned load), tval 0x80000401; x1 never
    // written (checked by the shared assertion helper's caller via never_written data).
    let last = &trace.steps[2];
    assert_eq!(last.word, Some(0x4015_2083));
    assert_eq!(last.writes, vec![]);
    assert_eq!(last.trap, Some((0x04, 0x8000_0401)));
}

#[test]
fn guest_no_device_faults_instead_of_finding_a_device() {
    let (trace, _, guest) = run_guest("guest-no-device");
    assert_eq!(trace.steps.len(), 6);
    assert_eq!(trace.stop, Stop::Trap);
    // D-PLATFORM: 0x0200_BFF8 is outside every region the laboratory declares, so the load
    // raises a load access-fault (cause 0x05) instead of reading a counter — the defect
    // P0-PROFILE.10 fixed and this fixture exists to prevent recurring.
    let last = &trace.steps[5];
    assert_eq!(last.trap, Some((0x05, 0x0200_BFF8)));
    assert!(!guest.never_written.is_empty());
}

// ---- the P2-SCALAR.1 scope-completion guests ---------------------------------------------------

#[test]
fn scope_alu_matches_its_specification_derived_expectations() {
    // 31 steps covering the 21 remaining ALU forms plus FENCE: the logical/compare/shift
    // pairs, the *W sign-extension pins, the rs2[4:0] vs rs2[5:0] shift-amount pin, and the
    // two 1→0 transitions that make the 0-results of SLTU/SLTIU visible in the trace.
    assert_guest_observations("scope-alu", Stop::Budget);
}

#[test]
fn scope_mem_matches_its_specification_derived_expectations() {
    // 29 steps covering the 8 remaining load/store forms: the sign/zero-extension pairs at
    // one address, the D-LOAD-X0 discarded load, and the three store widths with read-back.
    assert_guest_observations("scope-mem", Stop::Budget);
}

#[test]
fn scope_branch_matches_its_specification_derived_expectations() {
    // 19 executed steps from 24 instructions: each of the five branches taken once (the
    // skipped addi's register is never written — the negative observations) and not taken
    // once (the fall-through write happens).
    assert_guest_observations("scope-branch", Stop::Budget);
}

#[test]
fn scope_ecall_reports_the_requested_trap_and_stops() {
    // D-ECALL-EBREAK: cause 0x0B (environment call from M-mode), tval 0, reported ON the
    // ecall — then the run stops; there is no guest handler to continue into.
    assert_guest_observations("scope-ecall", Stop::Trap);
    let (trace, _, _) = run_guest("scope-ecall");
    let last = &trace.steps[1];
    assert_eq!(last.word, Some(0x0000_0073));
    assert_eq!(last.writes, vec![]);
    assert_eq!(last.trap, Some((0x0B, 0x0)));
}

#[test]
fn scope_ebreak_reports_the_requested_trap_and_stops() {
    // D-ECALL-EBREAK: cause 0x03 (breakpoint), tval = the ebreak's own address.
    assert_guest_observations("scope-ebreak", Stop::Trap);
    let (trace, _, _) = run_guest("scope-ebreak");
    let last = &trace.steps[1];
    assert_eq!(last.word, Some(0x0010_0073));
    assert_eq!(last.writes, vec![]);
    assert_eq!(last.trap, Some((0x03, 0x8000_0004)));
}

// ---- the P2-SCALAR.2 boundary guests ------------------------------------------------------------

#[test]
fn bound_shift_matches_its_specification_derived_expectations() {
    // 89 steps: the 6-bit shamt domain exhausted by one srli sweep over all 64 amounts of
    // 0x8000000000000001, srai/slli pinned at {0,1,2,4,8,16,32,63} (every amount bit on
    // every form), and the register-amount corners rs2 = 64 (reads as 0 — a pre-written
    // identity) and rs2 = -1 (reads as 63).
    assert_guest_observations("bound-shift", Stop::Budget);
}

#[test]
fn bound_shiftw_matches_its_specification_derived_expectations() {
    // 55 steps: the 5-bit shamt domain exhausted by one sraiw sweep over all 32 amounts,
    // slliw/srliw pinned at {0,1,2,4,8,16,31}, and the 5-vs-6-bit discriminator rs2 = 96 as
    // the srl/srlw pair on identical operands (srl shifts by 32, srlw is the identity).
    assert_guest_observations("bound-shiftw", Stop::Budget);
}

#[test]
fn bound_arith_matches_its_specification_derived_expectations() {
    // 31 steps: the signed-extreme wraps modulo 2^64 on the register AND immediate paths,
    // the *W wraps sign-extending from bit 31 with a garbage upper half ignored, slt/sltu
    // at the extremes, the 12-bit immediate extremes, and the U-immediate sign edges —
    // auipc 0x80000 wraps the address sum to exactly 4*n (D-ADDR-WRAP).
    assert_guest_observations("bound-arith", Stop::Budget);
}

#[test]
fn bound_ext_matches_its_specification_derived_expectations() {
    // 47 steps: the sign edge at each width (0x7F/0x80, 0x7FFF/0x8000, 0x7FFFFFFF/
    // 0x80000000) through the sign/zero load pair at one address, the all-ones values, the
    // 0x00 byte observed through a pre-write, and store truncation at non-clamping values.
    assert_guest_observations("bound-ext", Stop::Budget);
}

#[test]
fn bound_alias_matches_its_specification_derived_expectations() {
    // 37 steps: the little-endian lane proof (one sd, eight lbu lane reads — D-ENDIAN),
    // overlap composition (sd + sb + sh + one ld), register aliasing (rd = rs1 = rs2, a
    // self-referential shift, a load overwriting its own base register), and x0 hardwired
    // in both directions (a discarded write, a zero store read back through ld).
    assert_guest_observations("bound-alias", Stop::Budget);
}

// ---- the P2-SCALAR.3 fault, suppression and reserved guests ---------------------------------------

#[test]
fn fault_jal_mis_traps_on_the_jump_and_never_writes_the_link() {
    // D-IALIGN + D-MISALIGN-REPORT: jal to 0x80000006 raises ON THE JUMP, tval = the
    // target — and the DEFECT-B pin: the link write is suppressed (never_written x5),
    // exactly as both references were measured to behave.
    assert_guest_observations("fault-jal-mis", Stop::Trap);
    let (trace, _, _) = run_guest("fault-jal-mis");
    let last = &trace.steps[1];
    assert_eq!(last.word, Some(0x0020_02EF));
    assert_eq!(last.writes, vec![]);
    assert_eq!(last.trap, Some((0x00, 0x8000_0006)));
}

#[test]
fn fault_jalr_mis_traps_on_the_jump_and_never_writes_the_link() {
    // D-JALR-LSB clears only bit 0: x1 = 3 yields target 2 — misaligned under IALIGN=32,
    // raised ON THE JUMP, tval = 2, link write suppressed (never_written x5).
    assert_guest_observations("fault-jalr-mis", Stop::Trap);
    let (trace, _, _) = run_guest("fault-jalr-mis");
    let last = &trace.steps[1];
    assert_eq!(last.word, Some(0x0000_82E7));
    assert_eq!(last.writes, vec![]);
    assert_eq!(last.trap, Some((0x00, 0x2)));
}

#[test]
fn fault_branch_nt_raises_nothing_on_not_taken_misaligned_targets() {
    // The suppressed-effect guest (SEM-06): six branches point at misaligned targets and
    // none is taken, so nothing is raised; the fall-through writes all happen, and the
    // taken aligned branch at the end proves the branches were live (never_written x8).
    assert_guest_observations("fault-branch-nt", Stop::Budget);
    let (trace, _, _) = run_guest("fault-branch-nt");
    assert!(
        trace.steps.iter().all(|s| s.trap.is_none()),
        "no step raises anything: the whole point of the guest"
    );
}

#[test]
fn fault_fetch_reports_the_word_less_step_on_the_target() {
    // D-FETCH-FAULT-REPORT: the fetch at the jump's target 0x40000000 faults, reported
    // ON THE TARGET — the vocabulary's word-less step: no word was fetched, so none is
    // recorded, and the run stops with Stop::FetchFault.
    assert_guest_observations("fault-fetch", Stop::FetchFault { at: 0x4000_0000 });
    let (trace, _, _) = run_guest("fault-fetch");
    let last = &trace.steps[2];
    assert_eq!(last.pc, 0x4000_0000);
    assert_eq!(last.word, None);
    assert_eq!(last.writes, vec![]);
    assert_eq!(last.trap, Some((0x01, 0x4000_0000)));
}

#[test]
fn fault_ld_mis_h_reports_the_misaligned_halfword_load() {
    // D-MISALIGN-DATA, the 2-byte case at an odd address: cause 0x04, x1 never written.
    assert_guest_observations("fault-ld-mis-h", Stop::Trap);
    let (trace, _, _) = run_guest("fault-ld-mis-h");
    assert_eq!(trace.steps[2].trap, Some((0x04, 0x8000_0401)));
}

#[test]
fn fault_ld_mis_d_reports_the_half_aligned_doubleword_load() {
    // The width rule: 0x80000404 passes a 4-byte test and fails the 8-byte one.
    assert_guest_observations("fault-ld-mis-d", Stop::Trap);
    let (trace, _, _) = run_guest("fault-ld-mis-d");
    assert_eq!(trace.steps[2].trap, Some((0x04, 0x8000_0404)));
}

#[test]
fn fault_st_mis_h_suppresses_the_store_before_the_boundary() {
    // D-MISALIGN-DATA on the store side (SEM-06): cause 0x06, and the store never
    // crosses the boundary — the crossing log carries no store at all.
    assert_guest_observations("fault-st-mis-h", Stop::Trap);
    let (trace, crossings, _) = run_guest("fault-st-mis-h");
    assert_eq!(trace.steps[3].trap, Some((0x06, 0x8000_0401)));
    assert!(!crossings
        .iter()
        .any(|c| matches!(c.request, Request::Store { .. } | Request::Load { .. })));
}

#[test]
fn fault_st_mis_w_suppresses_the_store_before_the_boundary() {
    // The 4-byte store at 2 mod 4: cause 0x06, no store crossing.
    assert_guest_observations("fault-st-mis-w", Stop::Trap);
    let (trace, crossings, _) = run_guest("fault-st-mis-w");
    assert_eq!(trace.steps[3].trap, Some((0x06, 0x8000_0402)));
    assert!(!crossings
        .iter()
        .any(|c| matches!(c.request, Request::Store { .. } | Request::Load { .. })));
}

#[test]
fn fault_st_mis_d_suppresses_the_store_before_the_boundary() {
    // The 8-byte store at 4 mod 8: cause 0x06, no store crossing.
    assert_guest_observations("fault-st-mis-d", Stop::Trap);
    let (trace, crossings, _) = run_guest("fault-st-mis-d");
    assert_eq!(trace.steps[3].trap, Some((0x06, 0x8000_0404)));
    assert!(!crossings
        .iter()
        .any(|c| matches!(c.request, Request::Store { .. } | Request::Load { .. })));
}

#[test]
fn fault_ld_x0_mis_still_raises_with_a_discarded_destination() {
    // D-LOAD-X0 on the misaligned path: the discarded destination suppresses NOTHING —
    // the misaligned load into x0 raises cause 0x04 exactly as an ordinary register's.
    assert_guest_observations("fault-ld-x0-mis", Stop::Trap);
    let (trace, _, _) = run_guest("fault-ld-x0-mis");
    assert_eq!(trace.steps[2].trap, Some((0x04, 0x8000_0402)));
}

#[test]
fn fault_ld_x0_fault_still_raises_with_a_discarded_destination() {
    // D-LOAD-X0 on the access-fault path: cause 0x05 at 0x40000000 — the crossing is
    // recorded and answered AccessFault (the census pins it).
    assert_guest_observations("fault-ld-x0-fault", Stop::Trap);
    let (trace, crossings, _) = run_guest("fault-ld-x0-fault");
    assert_eq!(trace.steps[1].trap, Some((0x05, 0x4000_0000)));
    assert!(crossings.iter().any(|c| matches!(
        c.request,
        Request::Load {
            width: AccessWidth::D,
            addr: 0x4000_0000
        }
    )));
}

#[test]
fn fault_access_ld_reports_the_load_access_fault() {
    // D-ADDRESS-SPACE, cross-model: 0x40000000 is no platform's device, so this guest
    // carries the access-fault rule into the three-way comparison; x1 never written.
    assert_guest_observations("fault-access-ld", Stop::Trap);
    let (trace, _, _) = run_guest("fault-access-ld");
    assert_eq!(trace.steps[1].trap, Some((0x05, 0x4000_0000)));
}

#[test]
fn fault_access_sd_reports_the_store_access_fault() {
    // D-ADDRESS-SPACE on the store side: cause 0x07; the boundary refuses the request
    // and nothing is modified (SEM-06, catalog C11).
    assert_guest_observations("fault-access-sd", Stop::Trap);
    let (trace, _, _) = run_guest("fault-access-sd");
    assert_eq!(trace.steps[2].trap, Some((0x07, 0x4000_0000)));
}

#[test]
fn fault_reserved_is_converted_by_policy_and_keeps_its_classification() {
    // D-RESERVED-DECODE (SEM-07): 0xFFFFFFFF decodes to nothing; the laboratory's
    // declared policy — the harness's act, never the interpreter's — converts the
    // reserved case to the illegal-instruction observation (tval = the word), and the
    // stop reason keeps the source classification: Stop::Undefined.
    assert_guest_observations(
        "fault-reserved",
        Stop::Undefined(UndefinedCase::ReservedDecode { at: 0x8000_0004 }),
    );
    let (trace, _, _) = run_guest("fault-reserved");
    let last = &trace.steps[1];
    assert_eq!(last.word, Some(0xFFFF_FFFF));
    assert_eq!(last.writes, vec![]);
    assert_eq!(last.trap, Some((0x02, 0xFFFF_FFFF)));
}

#[test]
fn fault_shiftw_res_closes_oq2_with_the_reserved_iw_shift() {
    // D-SHIFTW-RESERVED: the word is slliw x2, x1, 1 with imm[5] = 1 — RESERVED in this
    // revision; OQ-2 measured both references raising illegal-instruction with tval =
    // the word, so the policy-converted observation agrees three-way while the stop
    // reason keeps the classification. x2 is never written.
    assert_guest_observations(
        "fault-shiftw-res",
        Stop::Undefined(UndefinedCase::ReservedDecode { at: 0x8000_0004 }),
    );
    let (trace, _, _) = run_guest("fault-shiftw-res");
    let last = &trace.steps[1];
    assert_eq!(last.word, Some(0x0210_911B));
    assert_eq!(last.writes, vec![]);
    assert_eq!(last.trap, Some((0x02, 0x210_911B)));
}

#[test]
fn fault_fence_retires_every_reserved_configuration_as_a_fence() {
    // The corrected D-FENCE: a reserved FENCE *configuration* is architecture-SPECIFIED
    // behavior (execute as FENCE fm=0000), not the reserved-decode case — none traps,
    // and the run retires into the budget.
    assert_guest_observations("fault-fence", Stop::Budget);
    let (trace, _, _) = run_guest("fault-fence");
    assert!(trace.steps.iter().all(|s| s.trap.is_none()));
    assert!(trace.steps.iter().all(|s| s.word.is_some()));
}

#[test]
fn fault_hints_retires_the_rv64i_hint_table_as_nops() {
    // D-HINTS: every code point executes as a no-op that must not trap; each HINT step
    // shows the empty writes table (a write to x0 is architecturally discarded) and the
    // run reaches the landing addi.
    assert_guest_observations("fault-hints", Stop::Budget);
    let (trace, _, _) = run_guest("fault-hints");
    assert!(trace.steps.iter().all(|s| s.trap.is_none()));
}

#[test]
fn fault_selfmod_makes_the_store_fetch_visible_immediately() {
    // D-CODE-VISIBILITY, pinned three-way (both references re-read too): the sw patches
    // step 5's word into `addi x2, x0, 7`, and the step executes the PATCHED encoding —
    // x2 = 7, not 2. The one store crossing is census-pinned.
    assert_guest_observations("fault-selfmod", Stop::Budget);
    let (trace, crossings, _) = run_guest("fault-selfmod");
    assert_eq!(trace.steps[5].word, Some(0x0070_0113));
    assert_eq!(trace.steps[5].writes, vec![(2, 7)]);
    assert!(crossings.iter().any(|c| matches!(
        c.request,
        Request::Store {
            width: AccessWidth::W,
            addr: 0x8000_0014,
            data: 0x0070_0113
        }
    )));
}

// ---- the P2-SCALAR.4 interaction-matrix guests -----------------------------------------------------

#[test]
fn it_prio_jump_reports_the_misaligned_cause_on_the_doubly_bad_target() {
    // F×F priority, measured three-way: the jalr target 0x40000002 is BOTH misaligned AND
    // unmapped; the misalignment is judged on the jump (cause 0x00, tval = the target)
    // before any fetch is attempted there, and the link write is suppressed
    // (never_written x5).
    assert_guest_observations("it-prio-jump", Stop::Trap);
    let (trace, _, _) = run_guest("it-prio-jump");
    let last = &trace.steps[2];
    assert_eq!(last.word, Some(0x0000_82E7));
    assert_eq!(last.writes, vec![]);
    assert_eq!(last.trap, Some((0x00, 0x4000_0002)));
}

#[test]
fn it_prio_load_reports_the_misaligned_cause_on_the_doubly_bad_address() {
    // F×F priority on the data path, measured three-way: the lw at 0x40000001 is BOTH
    // misaligned AND unmapped; D-MISALIGN-DATA is judged before the boundary is crossed,
    // so cause 0x04 wins and no data crossing exists (the census pins the empty arm).
    assert_guest_observations("it-prio-load", Stop::Trap);
    let (trace, _, _) = run_guest("it-prio-load");
    assert_eq!(trace.steps[2].trap, Some((0x04, 0x4000_0001)));
}

#[test]
fn it_fault_alias_preserves_the_base_of_its_own_faulting_load() {
    // F×A, measured three-way: `lw x5, x5, 1` — rd == rs1 — raises cause 0x04, and the
    // base register is PRESERVED through the fault: the trap step writes nothing, so x5
    // keeps the value step 0 gave it (the empty writes table on a pre-written base is
    // the observation).
    assert_guest_observations("it-fault-alias", Stop::Trap);
    let (trace, _, _) = run_guest("it-fault-alias");
    assert_eq!(trace.steps[0].writes, vec![(5, 0xFFFF_FFFF_8000_0000)]);
    assert_eq!(trace.steps[1].writes, vec![]);
    assert_eq!(trace.steps[1].trap, Some((0x04, 0xFFFF_FFFF_8000_0001)));
}

#[test]
fn it_fault_wrap_ld_faults_at_the_wrapped_address() {
    // F×B, measured three-way: 0xFFFF_FFFF_FFFF_FFFC + 4 wraps mod 2^64 to address 0
    // (D-ADDR-WRAP on the load path), which no region covers: cause 0x05, tval 0 — and
    // 0 < 2^56, so DIFF-TVAL-PHYS-MASK cannot reach the comparison.
    assert_guest_observations("it-fault-wrap-ld", Stop::Trap);
    let (trace, _, _) = run_guest("it-fault-wrap-ld");
    assert_eq!(trace.steps[1].trap, Some((0x05, 0x0)));
}

#[test]
fn it_fault_wrap_sd_faults_at_the_wrapped_address_and_stores_nothing() {
    // F×B on the store path — the DIFF-TVAL-PHYS-MASK redesign: the wrap target is
    // address 0 (tval 0, exact on all three models), not the top of the space where
    // sail masks the tval. The boundary refuses the request: cause 0x07, tval 0, and
    // nothing is stored (SEM-06 — the refused crossing is census-pinned).
    assert_guest_observations("it-fault-wrap-sd", Stop::Trap);
    let (trace, crossings, _) = run_guest("it-fault-wrap-sd");
    assert_eq!(trace.steps[2].trap, Some((0x07, 0x0)));
    assert!(crossings.iter().any(|c| matches!(
        c.request,
        Request::Store {
            width: AccessWidth::D,
            addr: 0x0,
            data: 7,
        }
    ) && c.response.is_err()));
}

#[test]
fn it_alias_bound_runs_self_aliased_ops_at_boundary_values() {
    // A×B: rd = rs1 = rs2 at domain edges — the addw 32-bit wrap, the 6-bit amount read
    // of 65 (which is 1), the shamt-63 extreme, and slt/sub at -1. Every result is a
    // visible change; the run retires into the budget.
    assert_guest_observations("it-alias-bound", Stop::Budget);
    let (trace, _, _) = run_guest("it-alias-bound");
    assert!(trace.steps.iter().all(|s| s.trap.is_none()));
    assert_eq!(trace.steps[1].writes, vec![(5, 0xFFFF_FFFF_FFFF_FFFE)]);
    assert_eq!(trace.steps[5].writes, vec![(7, 0x8000_0000_0000_0000)]);
}

#[test]
fn it_progress_loop_makes_every_iteration_visible_until_the_budget() {
    // P×P (+ the x0-link alias): an unbounded counting loop under the budget contract —
    // 13 executed steps from 3 instructions, every count a visible write, the jal's link
    // to x0 architecturally discarded (empty writes on the jump steps), and the run ends
    // exactly when the budget is spent.
    assert_guest_observations("it-progress-loop", Stop::Budget);
    let (trace, _, _) = run_guest("it-progress-loop");
    assert_eq!(trace.steps.len(), 13);
    assert_eq!(trace.steps[11].writes, vec![(1, 7)]);
    assert!(trace.steps.iter().all(|s| s.trap.is_none()));
}

#[test]
fn it_fencei_reports_the_reserved_word_and_stops_undefined() {
    // F×E — the DIFF-FENCEI-EXECUTED pin. Zifencei is absent from this profile, so
    // 0x0000100F matches no decode row: the interpreter reports the reserved case and the
    // laboratory's declared D-RESERVED-DECODE policy converts it to the
    // illegal-instruction observation (cause 0x02, tval = the word) — while both
    // references nop it and continue (the expected divergence the smoke run checks).
    // Stop::Undefined keeps the source classification (SEM-07); x2 (the continuation
    // marker) is never written by semulith.
    assert_guest_observations(
        "it-fencei",
        Stop::Undefined(UndefinedCase::ReservedDecode { at: 0x8000_0004 }),
    );
    let (trace, _, _) = run_guest("it-fencei");
    let last = &trace.steps[1];
    assert_eq!(last.word, Some(0x0000_100F));
    assert_eq!(last.writes, vec![]);
    assert_eq!(last.trap, Some((0x02, 0x0000_100F)));
}

// ---- the restart axis: the offline determinism suite (P2-SCALAR.4) ---------------------------------

#[test]
fn every_guest_re_executes_identically_from_cold_reset() {
    // Restartability is determinism of re-execution from cold reset — a mechanism
    // property, not a guest shape (the interaction matrix's restart cells name THIS
    // suite plus the smoke runner's reproduce leg). Every tracked guest runs twice from
    // `zeroed_at(entry)` and must produce the identical trace AND crossing log: a model
    // whose re-execution drifts is a model whose restart claim is unfounded.
    for guest in GUESTS {
        let (first_trace, first_crossings, _) = run_guest(guest.name);
        let (second_trace, second_crossings, _) = run_guest(guest.name);
        assert_eq!(
            first_trace, second_trace,
            "{}: re-execution from cold reset produced a different trace",
            guest.name
        );
        assert_eq!(
            first_crossings, second_crossings,
            "{}: re-execution from cold reset produced a different crossing log",
            guest.name
        );
    }
}
