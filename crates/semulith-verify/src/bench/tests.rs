//! The performance-baseline harness's suite (Rust tests under `make check`; no generated
//! artifact, no new doctrine — the harness guards measurement honesty, not drift). The
//! counting allocator is installed for this test binary so the counting path itself is
//! exercised; assertions are `>=` because sibling tests allocate concurrently.

use super::*;
use crate::run::Stop;

#[global_allocator]
static COUNTING: alloc::Counting = alloc::Counting;

#[test]
fn every_generated_word_decodes_to_its_intended_instruction() {
    for mix in Mix::ALL {
        for (name, word) in mix.named_program(3) {
            let decoded = semulith_core::definition::decode(word);
            assert_eq!(
                decoded.map(|insn| insn.name),
                Some(name),
                "{} mix word {word:#010x}: the encoder and the generated definition disagree",
                mix.name()
            );
        }
    }
}

#[test]
fn program_generation_is_deterministic() {
    for mix in Mix::ALL {
        assert_eq!(mix.program(7), mix.program(7));
    }
}

#[test]
fn iteration_count_outside_the_counter_range_is_refused() {
    for mix in Mix::ALL {
        let refused = std::panic::catch_unwind(|| mix.program(MAX_ITERATIONS + 1));
        assert!(
            refused.is_err(),
            "{} accepted an unencodable count",
            mix.name()
        );
    }
}

#[test]
fn each_mix_exercises_its_own_class() {
    let iterations = 5;
    // arithmetic: no data-memory traffic at all
    let (mut env, words) = prepare(Mix::Arithmetic, iterations);
    let run = run_mode(
        Mode::InstrumentedStatic,
        &mut env,
        &words,
        budget_for(Mix::Arithmetic, iterations),
    )
    .expect("arithmetic run");
    assert_eq!(run.facts.stop, Stop::Trap);
    assert_eq!(run.facts.census.loads, 0);
    assert_eq!(run.facts.census.stores, 0);
    assert_eq!(run.facts.census.faults, 0);
    // memory: 4 stores and 7 loads per iteration, no faults
    let (mut env, words) = prepare(Mix::Memory, iterations);
    let run = run_mode(
        Mode::InstrumentedStatic,
        &mut env,
        &words,
        budget_for(Mix::Memory, iterations),
    )
    .expect("memory run");
    assert_eq!(run.facts.stop, Stop::Trap);
    assert_eq!(run.facts.census.stores, u64::from(iterations) * 4);
    assert_eq!(run.facts.census.loads, u64::from(iterations) * 7);
    assert_eq!(run.facts.census.faults, 0);
    // fault: three trap observations per iteration (causes 4, 6, 5 — the model-side
    // misaligned pair never crosses the boundary; the out-of-region load does), plus the
    // closing EBREAK (cause 3)
    let (mut env, words) = prepare(Mix::Fault, iterations);
    let run = run_mode(
        Mode::InstrumentedStatic,
        &mut env,
        &words,
        budget_for(Mix::Fault, iterations),
    )
    .expect("fault run");
    assert_eq!(run.facts.stop, Stop::Trap);
    let steps = run.steps.expect("instrumented records the stream");
    let causes: Vec<u8> = steps
        .iter()
        .filter_map(|s| s.trap.map(|(c, _)| c))
        .collect();
    let mut expected = Vec::new();
    for _ in 0..iterations {
        expected.extend([0x04, 0x06, 0x05]);
    }
    expected.push(0x03);
    assert_eq!(
        causes, expected,
        "the fault mix must raise its designated causes in order"
    );
    assert_eq!(
        run.facts.census.faults,
        u64::from(iterations),
        "only the out-of-region load crosses the boundary and faults"
    );
    // control: no data memory, and it terminates on its trap
    let (mut env, words) = prepare(Mix::Control, iterations);
    let run = run_mode(
        Mode::InstrumentedStatic,
        &mut env,
        &words,
        budget_for(Mix::Control, iterations),
    )
    .expect("control run");
    assert_eq!(run.facts.stop, Stop::Trap);
    assert_eq!(run.facts.census.loads, 0);
    assert_eq!(run.facts.census.stores, 0);
}

#[test]
fn a_delivered_exception_is_observed_and_execution_continues() {
    // The fault-mix harness policy: after the misaligned lw at pc P, the next observed
    // step is at P+4 — delivery-continues, never a silent stop.
    let iterations = 2;
    let (mut env, words) = prepare(Mix::Fault, iterations);
    let run = run_mode(
        Mode::InstrumentedStatic,
        &mut env,
        &words,
        budget_for(Mix::Fault, iterations),
    )
    .expect("fault run");
    let steps = run.steps.expect("instrumented records the stream");
    let mut checked = 0;
    for pair in steps.windows(2) {
        if pair[0].trap == Some((0x04, ENTRY + DATA_OFFSET + 2)) {
            assert_eq!(
                pair[1].pc,
                pair[0].pc + 4,
                "after the misaligned load the next step must be at pc+4"
            );
            checked += 1;
        }
    }
    assert_eq!(
        checked, iterations as usize,
        "every misaligned load checked"
    );
}

#[test]
fn modes_agree_on_every_observable_at_small_budgets() {
    // RUST-02 exercised, not assumed: for every mix, all four cells agree on the facts,
    // and every recorded stream is identical.
    let iterations = 5;
    for mix in Mix::ALL {
        let budget = budget_for(mix, iterations);
        let mut runs = Vec::new();
        for mode in Mode::ALL {
            let (mut env, words) = prepare(mix, iterations);
            runs.push(
                run_mode(mode, &mut env, &words, budget)
                    .unwrap_or_else(|e| panic!("{} / {}: {}", mix.name(), mode.name(), e.0)),
            );
        }
        for (i, mode) in Mode::ALL.iter().enumerate().skip(1) {
            agree(&runs[0], &runs[i], (Mode::Untraced.name(), mode.name()))
                .unwrap_or_else(|why| panic!("{}: {why}", mix.name()));
        }
        agree(&runs[1], &runs[2], ("static", "dyn"))
            .unwrap_or_else(|why| panic!("{}: {why}", mix.name()));
        agree(&runs[2], &runs[3], ("dyn", "diagnostic"))
            .unwrap_or_else(|why| panic!("{}: {why}", mix.name()));
    }
}

#[test]
fn the_budget_is_a_real_stop() {
    let (mut env, words) = prepare(Mix::Arithmetic, 5);
    let run = run_mode(Mode::Untraced, &mut env, &words, 10).expect("untraced run");
    assert_eq!(run.facts.stop, Stop::Budget);
    assert_eq!(run.facts.steps, 10);
}

#[test]
fn a_pc_outside_the_image_is_refused_by_name() {
    assert_eq!(image_word(&[0x0000_0013], ENTRY), Ok(0x0000_0013));
    let refused = image_word(&[0x0000_0013], ENTRY + 8).expect_err("outside the one-word image");
    assert!(
        refused.0.contains("outside the 1-word guest image"),
        "the refusal must name what happened: {}",
        refused.0
    );
}

#[test]
fn the_counting_allocator_counts_a_known_allocation() {
    let before = alloc::counts();
    let block: Vec<u8> = Vec::with_capacity(4096);
    std::hint::black_box(&block);
    let after = alloc::counts();
    assert!(
        after.0 > before.0,
        "an allocation went uncounted ({before:?} -> {after:?})"
    );
    assert!(
        after.1 >= before.1 + 4096,
        "the 4096-byte allocation's bytes went uncounted ({before:?} -> {after:?})"
    );
}

#[test]
fn stats_are_pinned_on_known_inputs() {
    let s = stats(&[30, 10, 20]);
    assert_eq!(
        s,
        Stats {
            min: 10,
            median: 20,
            mean: 20,
            max: 30,
            spread_ppm: 1_000_000,
        }
    );
    // even count: the two middles' mean
    let s = stats(&[40, 10, 30, 20]);
    assert_eq!(s.median, 25);
    assert_eq!(s.min, 10);
    assert_eq!(s.max, 40);
    // a constant series has zero spread
    assert_eq!(stats(&[7, 7, 7]).spread_ppm, 0);
}

// ---------------------------------------------------------------------------
// The allocation pins (P1-LAB.13): the baseline's allocation figures are exact,
// attributed, and gated. The counters are THREAD-local (`alloc::thread_*`), so these
// pins are exact even with the test binary running suites in parallel. The mechanism
// the pins prove:
//   untraced     = 1 allocation per step, zero intercept — `extract_operands`' Vec
//                  (attribution: the only allocation on the untraced path; 128 B/step
//                  for a three-operand instruction);
//   instrumented = untraced + the writes Vec per step WITH A VISIBLE REGISTER CHANGE
//                  (`run::diff` diffs VALUES, so a write that changes nothing — the
//                  fixed-point iterations the mixes settle into — allocates nothing)
//                  + the step stream's amortized doubling;
//   diagnostic   = instrumented + exactly the crossing log's doubling growth.
// ---------------------------------------------------------------------------

#[test]
fn untraced_allocates_exactly_one_operands_vec_per_step() {
    for mix in Mix::ALL {
        let (mut env, words) = prepare(mix, 1);
        alloc::thread_reset();
        let run = run_mode(Mode::Untraced, &mut env, &words, 8).expect("untraced run");
        assert_eq!(run.facts.steps, 8);
        let (allocs, _) = alloc::thread_counts();
        assert_eq!(
            allocs,
            8,
            "{}: the untraced path must allocate exactly once per executed step",
            mix.name()
        );
    }
    // zero intercept: the count IS the step count, at full program length
    let (mut env, words) = prepare(Mix::Arithmetic, 4);
    alloc::thread_reset();
    let run = run_mode(Mode::Untraced, &mut env, &words, 1000).expect("untraced run");
    let (allocs, bytes) = alloc::thread_counts();
    assert_eq!(run.facts.steps, 114);
    assert_eq!(allocs, 114, "one operands Vec per step, nothing else");
    assert_eq!(
        bytes, 14368,
        "the operand Vec sizes are pinned (128 B x 3-operand steps)"
    );
}

#[test]
fn instrumented_static_and_dyn_allocate_identically() {
    // The dispatch-variants cell of the .11 report, pinned as exact equality.
    for mix in Mix::ALL {
        let mut counts = Vec::new();
        for mode in [Mode::InstrumentedStatic, Mode::InstrumentedDyn] {
            let (mut env, words) = prepare(mix, 1);
            alloc::thread_reset();
            let _run = run_mode(mode, &mut env, &words, 32).expect("instrumented run");
            counts.push(alloc::thread_counts());
        }
        assert_eq!(
            counts[0],
            counts[1],
            "{}: static and dyn dispatch must pay identical allocations",
            mix.name()
        );
    }
}

#[test]
fn diagnostic_over_instrumented_is_exactly_the_crossing_log_growth() {
    // The crossings Vec doubles: capacities 4, 8, 16, 32, 64, 128 — one allocation each.
    for (iterations, steps, growth) in [(1u32, 30usize, 4usize), (2, 58, 5), (4, 114, 6)] {
        let mut pair = Vec::new();
        for mode in [Mode::InstrumentedStatic, Mode::Diagnostic] {
            let (mut env, words) = prepare(Mix::Arithmetic, iterations);
            alloc::thread_reset();
            let run = run_mode(mode, &mut env, &words, 1000).expect("run");
            assert_eq!(run.facts.steps, steps);
            pair.push(alloc::thread_counts().0);
        }
        assert_eq!(
            pair[1] - pair[0],
            growth,
            "iterations={iterations}: diagnostic must add exactly the crossing log's \
             doubling allocations, no more"
        );
    }
}

#[test]
fn instrumented_allocates_the_writes_vec_only_on_a_visible_change() {
    // The mechanism behind the recorded traced figures (baseline.sexp's 1.19-1.42
    // allocs/step): the arithmetic mix settles into a fixed point where most iterations
    // change nothing observable, so the diff Vec allocates rarely. Pinned exactly at the
    // measured truth — if the diff policy or the mix changes, this pin says so.
    for (iterations, want_allocs) in [(1u32, 50usize), (2, 85), (4, 153)] {
        let (mut env, words) = prepare(Mix::Arithmetic, iterations);
        alloc::thread_reset();
        let _run = run_mode(Mode::InstrumentedStatic, &mut env, &words, 1000).expect("run");
        let (allocs, _) = alloc::thread_counts();
        assert_eq!(
            allocs, want_allocs,
            "iterations={iterations}: the operands+diff+stream allocation pattern changed"
        );
    }
}
