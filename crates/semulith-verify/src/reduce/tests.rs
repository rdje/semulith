//! Tests for the minimizer — `P1-LAB.10`'s second half (EVD-02). Every minimized result
//! must retain the original divergence exactly, and must be witnessed 1-minimal: no
//! single-word deletion of the result retains. The named boundary — a wrong behaviour the
//! observation vocabulary cannot see is not reducible on observations — is asserted as
//! the phantom-load refusal.

use super::*;
use crate::guests::GUESTS;
use crate::mutate::table_for;
use semulith_core::definition::INSNS;

fn guest(name: &str) -> &'static crate::guests::Guest {
    GUESTS.iter().find(|g| g.name == name).unwrap()
}

fn case<'a>(model: &'a [InsnDef], entry: u64, budget: usize) -> Case<'a> {
    Case {
        model,
        reference: INSNS,
        entry,
        region_size: 0x1_0000,
        budget,
    }
}

fn reduce_guest(mutation: &str, guest_name: &str) -> Result<Reduction, ReduceError> {
    let guest = guest(guest_name);
    let table = table_for(mutation).unwrap();
    let case = case(&table, guest.entry, guest.executed_steps);
    reduce(&case, guest.words)
}

/// The witness that makes "minimized" a claim with evidence: deleting any single word of
/// the result loses the retained divergence.
fn assert_one_minimal(case: &Case, reduction: &Reduction) {
    for i in 0..reduction.words.len() {
        let candidate: Vec<u32> = reduction.words[..i]
            .iter()
            .chain(&reduction.words[i + 1..])
            .cloned()
            .collect();
        assert_ne!(
            divergence(case, &candidate),
            Some(reduction.retained.clone()),
            "deleting word {i} must not retain — the result would not be 1-minimal"
        );
    }
}

#[test]
fn zext_addi_minimizes_to_the_divergent_prefix() {
    let guest = guest("guest-control");
    let table = table_for("zext-addi").unwrap();
    let case = case(&table, guest.entry, guest.executed_steps);
    let reduction = reduce(&case, guest.words).unwrap();
    assert_eq!(
        reduction.words,
        guest.words[..2],
        "only the two words the divergence's prefix executes are load-bearing"
    );
    assert_eq!(reduction.retained.at, 1, "the `.9` suite's designated step");
    assert!(
        reduction.retained.what.contains("x1"),
        "names the designated field: {}",
        reduction.retained.what
    );
    assert!(
        reduction.evaluations < 1_000,
        "ddmin on 13 words is tens of evaluations, not {} — {}",
        reduction.evaluations,
        "the guard documents the expected shape"
    );
    assert_one_minimal(&case, &reduction);
}

#[test]
fn jal_no_link_minimizes_to_the_divergent_prefix() {
    let guest = guest("guest-control");
    let table = table_for("jal-no-link").unwrap();
    let case = case(&table, guest.entry, guest.executed_steps);
    let reduction = reduce(&case, guest.words).unwrap();
    assert_eq!(
        reduction.words,
        guest.words[..4],
        "the suppressed link write diverges at step 7 (the jal itself); everything the \
         divergence never reaches — the jal's own target region included — is not load-bearing"
    );
    assert_eq!(reduction.retained.at, 7);
    assert!(
        reduction.retained.what.contains("x5"),
        "names the link register: {}",
        reduction.retained.what
    );
    assert_one_minimal(&case, &reduction);
}

#[test]
fn jalr_odd_bit_minimizes_and_retains_the_fixture_notes_fault() {
    let guest = guest("guest-control");
    let table = table_for("jalr-odd-bit").unwrap();
    let case = case(&table, guest.entry, guest.executed_steps);
    let reduction = reduce(&case, guest.words).unwrap();
    assert_eq!(
        reduction.words,
        guest.words[..9],
        "the misaligned jalr is step 10 and the divergence is AT that step: the two words \
         behind it are never reached by the first-divergence walk"
    );
    assert_eq!(reduction.retained.at, 10);
    assert!(
        reduction.retained.what.contains("trap"),
        "names the divergence kind: {}",
        reduction.retained.what
    );
    // The retained trap is the fixture note's prediction, byte for byte.
    let mut env = FlatMemory::new(guest.entry, 0x1_0000);
    env.load_image(0, &image_bytes(&reduction.words));
    let (trace, _) = run::run_over(&mut env, guest.entry, guest.executed_steps, &table);
    assert_eq!(
        trace.steps[10].trap,
        Some((0x00, 0x80000029)),
        "InstructionAddressMisaligned at 0x80000029 — the fixture note's prediction, retained"
    );
    assert_one_minimal(&case, &reduction);
}

#[test]
fn the_clean_model_has_no_divergence_to_retain() {
    let err =
        reduce_guest("none", "guest-control").expect_err("the clean model agrees with itself");
    assert_eq!(err, ReduceError::NoDivergence);
}

#[test]
fn the_phantom_load_is_refused_the_census_catches_what_the_trace_cannot() {
    let err = reduce_guest("phantom-load", "smoke-arith")
        .expect_err("an agreeing trace has no first divergence");
    assert_eq!(
        err,
        ReduceError::NoDivergence,
        "the phantom load moves the crossing census, not the observations — observation \
         reduction cannot retain it, and the refusal says the census owns that class"
    );
}

#[test]
fn an_empty_input_has_no_divergence_to_retain() {
    let guest = guest("smoke-arith");
    let table = table_for("zext-addi").unwrap();
    let case = case(&table, guest.entry, guest.executed_steps);
    assert_eq!(
        reduce(&case, &[]).expect_err("empty input"),
        ReduceError::NoDivergence
    );
}
