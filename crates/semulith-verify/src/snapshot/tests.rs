//! The snapshot proof suite (`P2-SCALAR.7`): mid-execution replay demonstrated for the
//! state boundaries actually implemented — and refused honestly beyond them.

use super::*;
use crate::guests::GUESTS;

const REGION: u64 = 0x10000;

fn guest_facts(name: &str) -> (u64, Vec<u32>, usize) {
    let guest = GUESTS
        .iter()
        .find(|g| g.name == name)
        .unwrap_or_else(|| panic!("guest {name} is in the generated fixture"));
    (guest.entry, guest.words.to_vec(), guest.executed_steps)
}

fn env_with(base: u64, words: &[u32]) -> FlatMemory {
    let mut env = FlatMemory::new(base, REGION as usize);
    let mut image = Vec::with_capacity(words.len() * 4);
    for word in words {
        image.extend_from_slice(&word.to_le_bytes());
    }
    env.load_image(0, &image);
    env
}

/// The split run: head to `k`, snapshot THROUGH the JSON round-trip (the record is the
/// artifact, not the in-memory value), resume — versus the uninterrupted reference.
fn assert_split_equals_reference(name: &str, k: usize) {
    let (entry, words, steps) = guest_facts(name);
    assert!(k <= steps, "{name}: snapshot point past the run");
    let (reference, ref_crossings) = run::run(&mut env_with(entry, &words), entry, steps);

    let mut env = env_with(entry, &words);
    let (head, head_crossings, state) =
        run::run_state(&mut env, ArchitecturalState::zeroed_at(entry), k);
    assert_eq!(
        head.steps.len(),
        k,
        "{name}: the head run is exactly k steps"
    );
    let snap = Snapshot::capture(&env, &state, entry, REGION, entry, k, steps);
    let restored = Snapshot::parse(&snap.to_json()).expect("the record round-trips");
    assert_eq!(restored, snap, "{name}: the JSON round-trip is exact");
    let resumed = restored.resume().expect("{name}: the snapshot resumes");

    let mut split = head.steps.clone();
    split.extend(resumed.trace.steps.iter().cloned());
    assert_eq!(
        split, reference.steps,
        "{name}: the split run's steps equal the uninterrupted run's at k = {k}"
    );
    let mut split_crossings = head_crossings;
    split_crossings.extend(resumed.crossings.iter().cloned());
    assert_eq!(
        split_crossings, ref_crossings,
        "{name}: the crossing logs agree too at k = {k}"
    );
}

#[test]
fn every_guest_resumes_identically_from_a_mid_execution_snapshot() {
    // The acceptance's positive arm: for every tracked guest, at an early, a middle and
    // the penultimate step, snapshot + resume reproduces the uninterrupted run EXACTLY —
    // steps and crossing logs. The memory-state guests (dir-memwalk's walk, dir-chase's
    // chase) are the load-bearing cases: their future behavior lives in MEMORY, not in
    // the register file, so a snapshot that silently dropped memory content fails HERE.
    for guest in GUESTS {
        let steps = guest.executed_steps;
        for k in [1, steps / 2, steps.saturating_sub(1)] {
            assert_split_equals_reference(guest.name, k);
        }
    }
}

#[test]
fn a_corrupted_memory_run_is_refused_by_its_digest() {
    // RED: flip one byte inside a recorded run — the sparse encoding still parses, and
    // the resume MUST refuse (the rebuilt region no longer hashes to the recorded
    // digest). A snapshot that silently dropped future-relevant state is exactly this
    // failure with the byte removed rather than altered; both are caught.
    let (entry, words, steps) = guest_facts("dir-memwalk");
    let mut env = env_with(entry, &words);
    let (_, _, state) = run::run_state(&mut env, ArchitecturalState::zeroed_at(entry), 13);
    let snap = Snapshot::capture(&env, &state, entry, REGION, entry, 13, steps);
    let mut json = snap.to_json();
    // flip one hex digit inside the first run's bytes
    let i = json.find("\"bytes\":\"").expect("the run exists") + "\"bytes\":\"".len();
    let b = json.as_bytes()[i];
    let flipped = if b == b'0' { b'1' } else { b'0' };
    json.replace_range(i..=i, &(flipped as char).to_string());
    let restored = Snapshot::parse(&json).expect("the corrupted record still parses");
    let err = restored
        .resume()
        .expect_err("a corrupted run must be refused");
    assert!(
        err.contains("memory digest mismatch"),
        "the refusal names the digest: {err}"
    );
}

#[test]
fn a_foreign_definition_is_refused_by_name() {
    // RED: a snapshot recorded against a different definition must not resume against
    // this one — replaying against another definition is a different experiment.
    let (entry, words, steps) = guest_facts("smoke-arith");
    let mut env = env_with(entry, &words);
    let (_, _, state) = run::run_state(&mut env, ArchitecturalState::zeroed_at(entry), 2);
    let snap = Snapshot::capture(&env, &state, entry, REGION, entry, 2, steps);
    let json = snap.to_json().replace(
        &format!("\"profile\":\"{}\"", snap.algorithm.profile),
        "\"profile\":\"rv64i-elsewhere-v9\"",
    );
    assert!(json != snap.to_json(), "the tamper landed");
    let restored = Snapshot::parse(&json).expect("the tampered record parses");
    let err = restored
        .resume()
        .expect_err("a foreign definition must be refused");
    assert!(
        err.contains("definition pin mismatch") && err.contains("rv64i-elsewhere-v9"),
        "the refusal names the pin: {err}"
    );
}

#[test]
fn incoherent_and_overrunning_records_are_refused() {
    // RED: structural honesty — a step index beyond the budget, a run past the region,
    // and a partial register file are all refused by name, never replayed.
    let (entry, words, steps) = guest_facts("smoke-arith");
    let mut env = env_with(entry, &words);
    let (_, _, state) = run::run_state(&mut env, ArchitecturalState::zeroed_at(entry), 2);
    let snap = Snapshot::capture(&env, &state, entry, REGION, entry, 2, steps);
    let json = snap.to_json();

    let bad = json.replace(
        &format!("\"at_step\":{}", snap.at_step),
        &format!("\"at_step\":{}", snap.budget + 1),
    );
    let err = Snapshot::parse(&bad)
        .expect("parses")
        .resume()
        .expect_err("at_step > budget");
    assert!(err.contains("exceeds the recorded budget"), "{err}");

    let bad = json.replace(
        &format!("\"offset\":\"0x{:016x}\"", snap.runs[0].0),
        &format!("\"offset\":\"0x{:016x}\"", REGION), // one past the end: overruns for certain
    );
    let err = Snapshot::parse(&bad)
        .expect("parses")
        .resume()
        .expect_err("a run past the region");
    assert!(err.contains("overruns the declared region"), "{err}");

    let i = json.find("\"regs\":[").expect("regs exist");
    let j = json[i..].find(']').expect("regs end") + i;
    let bad = format!("{}\"regs\":[\"0x0\"]{}", &json[..i], &json[j + 1..]);
    assert!(Snapshot::parse(&bad)
        .expect_err("a partial register file")
        .contains("wants exactly 32"));
}

#[test]
fn the_round_trip_is_exact_and_the_encoding_is_deterministic() {
    // The record is the artifact: capture → JSON → parse → identical record, and two
    // captures of the same state serialize byte-identically (a replay artifact whose
    // bytes drift between writes cannot anchor a comparison).
    let (entry, words, steps) = guest_facts("dir-chase");
    let mut env = env_with(entry, &words);
    let (_, _, state) = run::run_state(&mut env, ArchitecturalState::zeroed_at(entry), 12);
    let a = Snapshot::capture(&env, &state, entry, REGION, entry, 12, steps);
    let b = Snapshot::parse(&a.to_json()).expect("round-trip");
    assert_eq!(a, b);
    assert_eq!(a.to_json(), b.to_json());
    assert!(
        !a.runs.is_empty(),
        "dir-chase's mid-run memory is not empty — the sparse encoding carries it"
    );
}
