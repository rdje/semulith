//! Tests for the recorded input bundle and its replay — `P1-LAB.10`'s first half
//! (G-REPLAY). The acceptance under test: the bundle replays the same result, and a seed
//! is accompanied by algorithm/version and the actual relevant event choices — every
//! tamper and omission arm below must be refused by name, never silently re-run.

use super::*;
use crate::guests::GUESTS;

fn spec(model: &str, entry: u64, budget: usize) -> CaseSpec {
    CaseSpec {
        model: model.to_string(),
        entry,
        base: entry,
        size: 0x1_0000,
        budget,
    }
}

fn round_trip(bundle: &Bundle) -> Bundle {
    Bundle::parse(&bundle.to_json()).expect("the serialized bundle parses")
}

#[test]
fn every_tracked_guest_replays_identically_under_the_production_model() {
    for guest in GUESTS {
        let bundle = Bundle::record(
            &spec("production", guest.entry, guest.executed_steps),
            guest.words,
        )
        .unwrap_or_else(|why| panic!("record {}: {why}", guest.name));
        let parsed = round_trip(&bundle);
        assert_eq!(bundle, parsed, "{}: serialization round-trips", guest.name);
        match parsed.replay() {
            Ok(Replay::Identical) => {}
            other => panic!(
                "{}: expected an identical replay, got {other:?}",
                guest.name
            ),
        }
        assert_eq!(
            bundle.recorded.steps.len(),
            guest.executed_steps,
            "{}: the recorded result is the executed trace",
            guest.name
        );
    }
}

#[test]
fn a_mutant_bundle_replays_and_the_divergence_reproduces() {
    let guest = GUESTS.iter().find(|g| g.name == "guest-control").unwrap();
    let bundle = Bundle::record(
        &spec("mutant:zext-addi", guest.entry, guest.executed_steps),
        guest.words,
    )
    .unwrap();
    let parsed = round_trip(&bundle);
    assert_eq!(parsed.algorithm.model, "mutant:zext-addi");
    assert_eq!(
        parsed.replay(),
        Ok(Replay::Identical),
        "the mutant's recorded trace re-derives"
    );
    // The divergence against the reference model falls out of the recorded inputs.
    let mut env = FlatMemory::new(guest.entry, 0x1_0000);
    env.load_image(0, &image_bytes(guest.words));
    let (reference, _) = run::run(&mut env, guest.entry, guest.executed_steps);
    let divergence = match run::compare(
        &reference.steps,
        &parsed.recorded.steps,
        ("reference", "model"),
    ) {
        Ok(run::Verdict::Divergence(d)) => d,
        other => panic!("expected the reproduced divergence, got {other:?}"),
    };
    assert_eq!(divergence.at, 1, "the `.9` suite's designated step");
    assert!(
        divergence.what.contains("x1"),
        "names the designated field: {}",
        divergence.what
    );
}

#[test]
fn an_empty_recorded_run_replays() {
    let guest = GUESTS.iter().find(|g| g.name == "smoke-arith").unwrap();
    let bundle = Bundle::record(&spec("production", guest.entry, 0), guest.words).unwrap();
    assert!(bundle.recorded.steps.is_empty());
    assert_eq!(bundle.recorded.stop, "Budget");
    assert_eq!(round_trip(&bundle).replay(), Ok(Replay::Identical));
}

#[test]
fn a_tampered_image_is_refused_by_name() {
    let guest = GUESTS.iter().find(|g| g.name == "smoke-arith").unwrap();
    let mut bundle = Bundle::record(
        &spec("production", guest.entry, guest.executed_steps),
        guest.words,
    )
    .unwrap();
    bundle.image.words[0] ^= 0x1;
    let why = bundle
        .replay()
        .expect_err("a tampered image must not replay");
    assert!(
        why.contains("image digest mismatch"),
        "names the refusal: {why}"
    );
}

#[test]
fn a_tampered_entry_replays_to_a_named_mismatch() {
    let guest = GUESTS.iter().find(|g| g.name == "smoke-arith").unwrap();
    let mut bundle = Bundle::record(
        &spec("production", guest.entry, guest.executed_steps),
        guest.words,
    )
    .unwrap();
    bundle.entry += 4;
    match bundle.replay() {
        Ok(Replay::Mismatch(d)) => {
            assert_eq!(d.at, 0, "the moved program diverges at the first step");
            assert!(d.what.contains("pc"), "names the field: {}", d.what);
        }
        other => panic!("expected a named mismatch, got {other:?}"),
    }
}

#[test]
fn an_overrunning_image_is_refused_by_name() {
    let guest = GUESTS.iter().find(|g| g.name == "smoke-arith").unwrap();
    let err = Bundle::record(
        &CaseSpec {
            model: "production".to_string(),
            entry: guest.entry,
            base: guest.entry,
            size: 8,
            budget: guest.executed_steps,
        },
        guest.words,
    )
    .expect_err("a 12-word image cannot fit an 8-byte region");
    assert!(err.contains("overruns"), "names the refusal: {err}");
}

#[test]
fn a_starved_budget_is_a_named_length_mismatch() {
    let guest = GUESTS.iter().find(|g| g.name == "smoke-arith").unwrap();
    let mut bundle = Bundle::record(
        &spec("production", guest.entry, guest.executed_steps),
        guest.words,
    )
    .unwrap();
    bundle.budget = 1;
    match bundle.replay() {
        Ok(Replay::LengthMismatch { agreed, .. }) => assert_eq!(agreed, 1),
        other => panic!("expected a length mismatch, got {other:?}"),
    }
}

#[test]
fn a_tampered_generator_pin_is_refused_by_name() {
    let guest = GUESTS.iter().find(|g| g.name == "smoke-arith").unwrap();
    let mut bundle = Bundle::record(
        &spec("production", guest.entry, guest.executed_steps),
        guest.words,
    )
    .unwrap();
    bundle.algorithm.generator.1 = "0".repeat(64);
    let why = bundle
        .replay()
        .expect_err("a stale generator pin must not replay");
    assert!(
        why.contains("definition pin mismatch") && why.contains("generator"),
        "names the pin: {why}"
    );
}

#[test]
fn a_tampered_input_pin_is_refused_naming_the_path() {
    let guest = GUESTS.iter().find(|g| g.name == "smoke-arith").unwrap();
    let mut bundle = Bundle::record(
        &spec("production", guest.entry, guest.executed_steps),
        guest.words,
    )
    .unwrap();
    bundle.algorithm.inputs[0].1 = "0".repeat(64);
    let path = bundle.algorithm.inputs[0].0.clone();
    let why = bundle
        .replay()
        .expect_err("a stale input pin must not replay");
    assert!(
        why.contains("definition pin mismatch") && why.contains(&path),
        "names the path: {why}"
    );
}

#[test]
fn a_dropped_input_pin_is_refused_naming_it() {
    let guest = GUESTS.iter().find(|g| g.name == "smoke-arith").unwrap();
    let mut bundle = Bundle::record(
        &spec("production", guest.entry, guest.executed_steps),
        guest.words,
    )
    .unwrap();
    let dropped = bundle.algorithm.inputs.pop().unwrap().0;
    let why = bundle
        .replay()
        .expect_err("a seed missing a pin must not replay");
    assert!(
        why.contains("does not carry") && why.contains(&dropped),
        "names the missing pin: {why}"
    );
}

#[test]
fn an_unknown_model_name_is_refused_by_name() {
    let guest = GUESTS.iter().find(|g| g.name == "smoke-arith").unwrap();
    let err = Bundle::record(
        &spec("mutant:bogus", guest.entry, guest.executed_steps),
        guest.words,
    )
    .expect_err("an unknown mutation has no table");
    assert!(err.contains("bogus"), "names the mutation: {err}");
}

#[test]
fn a_bare_seed_is_refused_naming_what_is_missing() {
    let doc = "{\"image\":{\"sha256\":\"x\",\"words\":[]}}";
    let why = Bundle::parse(doc).expect_err("a bare seed is not a bundle");
    assert!(
        why.contains("algorithm") && why.contains("bare seed"),
        "names the missing accompaniment: {why}"
    );
}

#[test]
fn a_seed_without_event_choices_is_refused_naming_them() {
    let guest = GUESTS.iter().find(|g| g.name == "smoke-arith").unwrap();
    let mut doc = round_trip(
        &Bundle::record(
            &spec("production", guest.entry, guest.executed_steps),
            guest.words,
        )
        .unwrap(),
    )
    .to_json();
    let start = doc.find(",\"events\":").unwrap();
    let end = doc.find("\"budget\":").unwrap();
    doc.replace_range(start..end, ",");
    let why = Bundle::parse(&doc).expect_err("a seed without event choices is not a bundle");
    assert!(
        why.contains("events") && why.contains("bare seed"),
        "names the missing accompaniment: {why}"
    );
}

#[test]
fn a_scripted_event_claim_is_refused_as_not_this_platform() {
    let guest = GUESTS.iter().find(|g| g.name == "smoke-arith").unwrap();
    let mut doc = round_trip(
        &Bundle::record(
            &spec("production", guest.entry, guest.executed_steps),
            guest.words,
        )
        .unwrap(),
    )
    .to_json();
    let start = doc.find("\"events\":").unwrap();
    let end = doc.find("\"budget\":").unwrap();
    doc.replace_range(
        start..end,
        "\"events\":{\"kind\":\"scripted\",\"obligation\":\"x\"},",
    );
    let why = Bundle::parse(&doc).expect_err("a scripted claim is not a recorded choice");
    assert!(
        why.contains("scripted") && why.contains(EVENT_OBLIGATION),
        "names the refusal: {why}"
    );
}

#[test]
fn the_recorded_event_choice_names_its_obligation() {
    let guest = GUESTS.iter().find(|g| g.name == "smoke-arith").unwrap();
    let bundle = Bundle::record(
        &spec("production", guest.entry, guest.executed_steps),
        guest.words,
    )
    .unwrap();
    assert_eq!(bundle.events, Events::DeclaredNone);
    let doc = bundle.to_json();
    assert!(doc.contains(EVENT_OBLIGATION));
}
