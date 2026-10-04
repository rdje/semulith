//! The rv64gc corpus proof on the TRACKED engine (`P4-SYSTEM.2` slice h): every tracked
//! guest — the 49 base-mirror guests and the 13 mode-matrix guests — executed through
//! `exec_rv64gc` and falsified against its specification-derived expectations (EVD-05),
//! with the same assertion family the base profile's offline differential uses.

use super::{guest, run_guest};
use crate::guests_rv64gc::GUESTS;

fn assert_guest_observations(name: &str) {
    let g = guest(name);
    let (trace, _env) = run_guest(g);
    assert!(
        trace.failed.is_none(),
        "{name}: the run ended on a model error: {:?}",
        trace.failed
    );
    assert_eq!(
        trace.steps.len(),
        g.executed_steps,
        "{name}: the trace runs exactly the declared step count"
    );
    for (i, expected) in g.expected.iter().enumerate() {
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
    for reg in g.never_written {
        assert!(
            !written.contains(reg),
            "{name}: x{reg} must never be written, but the trace wrote it"
        );
    }
    assert_eq!(
        trace.fetches as usize, g.expected_fetches,
        "{name}: the fetch-request count matches the declared expectation (one per \
         step, minus every step whose fetch page-faults in the walk)"
    );
}

#[test]
fn corpus_base_mirror_smoke() {
    // the base mirror's first guests, named so a failure reads as a name, not a number
    for name in [
        "smoke-arith",
        "guest-control",
        "smoke-trap",
        "it-prio-jump",
        "min-fencei",
    ] {
        assert_guest_observations(name);
    }
}

#[test]
fn corpus_mode_matrix() {
    // the 13 mode-matrix guests: the leaf's acceptance criterion made executable — the
    // same instruction's behaviour tested in each supported mode (M/S/U)
    for name in [
        "mm-csr-rw",
        "mm-csr-legality-s",
        "mm-csr-legality-u",
        "mm-ebreak",
        "mm-ecall-modes",
        "mm-ecall-deleg",
        "mm-mret",
        "mm-readonly",
        "mm-counters",
        "mm-stimecmp",
        "mm-wfi",
        "mm-sfence",
        "mm-sret",
    ] {
        assert_guest_observations(name);
    }
}

#[test]
fn every_guest_matches_its_expectations() {
    for g in GUESTS {
        assert_guest_observations(g.name);
    }
}

#[test]
fn every_guest_re_executes_identically_from_cold_reset() {
    // Restartability is determinism of re-execution from cold reset — the interaction
    // matrix's restart cells' guest-shaped property. Every tracked guest runs twice from
    // `zeroed_at(entry)` and must produce the identical trace.
    for g in GUESTS {
        let (first, _) = run_guest(g);
        let (second, _) = run_guest(g);
        assert_eq!(
            first, second,
            "{}: re-execution from cold reset produced a different trace",
            g.name
        );
    }
}
