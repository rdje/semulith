//! Tests for the observation runner and the first-divergence comparator. The comparator's
//! RED/GREEN arms mirror `scripts/compare_traces.py`'s self-test: a comparator that has
//! only ever agreed is not known to disagree.

use super::*;
use crate::fixtures::FlatMemory;
use semulith_core::env::{AccessWidth, Request};

fn step(pc: u64, word: u32, writes: &[(u8, u64)], trap: Option<(u8, u64)>) -> Step {
    Step {
        pc,
        word,
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
    assert_eq!(trace.steps[0].word, 0x0050_0093);
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
    assert_eq!(last.word, 0x0020_a183);
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
    let mut env = flat(&[0x0050_0093, 0x0010_0113, 0x01F1_1113, 0x0011_0823]);
    let (trace, crossings) = run(&mut env, ENTRY, 8);
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
fn fetch_fault_stops_without_a_fiction_step() {
    // Empty memory region: the very first fetch is outside it... an empty region cannot be
    // built, so place no image and fetch from the region's end via entry just past the top.
    let mut env = FlatMemory::new(ENTRY, 0x1000);
    let (trace, crossings) = run(&mut env, ENTRY + 0x1000, 4);
    assert_eq!(trace.steps, vec![]);
    assert_eq!(trace.stop, Stop::FetchFault { at: ENTRY + 0x1000 });
    assert!(crossings
        .iter()
        .any(|c| matches!(c.request, Request::Fetch { addr } if addr == ENTRY + 0x1000)));
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
    assert_eq!(last.word, 0x4015_2083);
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
    assert_eq!(last.word, 0x0000_0073);
    assert_eq!(last.writes, vec![]);
    assert_eq!(last.trap, Some((0x0B, 0x0)));
}

#[test]
fn scope_ebreak_reports_the_requested_trap_and_stops() {
    // D-ECALL-EBREAK: cause 0x03 (breakpoint), tval = the ebreak's own address.
    assert_guest_observations("scope-ebreak", Stop::Trap);
    let (trace, _, _) = run_guest("scope-ebreak");
    let last = &trace.steps[1];
    assert_eq!(last.word, 0x0010_0073);
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
