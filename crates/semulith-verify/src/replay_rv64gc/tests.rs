use super::*;
use crate::fixtures::FlatMemory;
use crate::guests_rv64gc::{Guest, GUESTS};
use crate::run_rv64gc;
use semulith_core::state_rv64gc::ArchitecturalState;

fn input(guest: &Guest, at: usize, budget: usize) -> SnapshotRv64gc {
    let mut memory = FlatMemory::with_fetch_align(guest.entry, 0x10000, 2);
    memory.load_image(0, guest.image);
    let mut state = ArchitecturalState::zeroed_at(guest.entry);
    let prefix = run_rv64gc::run_from_with_refusals(&mut memory, &mut state, at, guest.refusals);
    assert!(prefix.failed.is_none());
    SnapshotRv64gc::capture(&memory, &mut state, guest.entry, at, budget, guest.refusals).unwrap()
}

fn bundle() -> BundleRv64gc {
    let guest = run_rv64gc::guest("a-lrsc-pair");
    BundleRv64gc::record(input(guest, 0, guest.executed_steps)).unwrap()
}

#[test]
fn every_gc_guest_bundle_roundtrips_and_replays_all_recorded_receipts() {
    for guest in GUESTS {
        let bundle = BundleRv64gc::record(input(guest, 0, guest.executed_steps)).unwrap();
        assert_eq!(
            bundle.recorded,
            run_rv64gc::run_guest(guest).0,
            "{}",
            guest.name
        );
        let text = bundle.to_json();
        assert!(text.len() <= MAX_JSON_BYTES);
        let parsed = BundleRv64gc::parse(&text).unwrap();
        assert_eq!(parsed, bundle, "{}", guest.name);
        assert_eq!(parsed.to_json(), text);
        assert_eq!(
            parsed.replay().unwrap(),
            ReplayRv64gc::Identical,
            "{}",
            guest.name
        );
    }
    println!(
        "{} complete RV64GC guest bundle round trips/replays",
        GUESTS.len()
    );
}

#[test]
fn checkpoint_inputs_and_empty_continuations_replay() {
    for name in ["a-lrsc-pair", "w-timer", "sv39-tlb-fence", "fp-fcsr-view"] {
        let guest = run_rv64gc::guest(name);
        for at in [guest.executed_steps / 2, guest.executed_steps] {
            let bundle = BundleRv64gc::record(input(guest, at, guest.executed_steps)).unwrap();
            assert_eq!(bundle.recorded_steps(), guest.executed_steps - at);
            assert_eq!(
                BundleRv64gc::parse(&bundle.to_json())
                    .unwrap()
                    .replay()
                    .unwrap(),
                ReplayRv64gc::Identical
            );
        }
    }
}

#[test]
fn first_trace_differences_and_aggregate_receipts_are_distinct() {
    let original = bundle();
    for (field, kind) in [("PC", 0), ("privilege mode", 1), ("GPR changes", 2)] {
        let mut altered = original.clone();
        match kind {
            0 => altered.recorded.steps[0].pc ^= 2,
            1 => altered.recorded.steps[0].mode = PrivilegeMode::U,
            _ => altered.recorded.steps[0].writes = vec![(31, 1)],
        }
        let parsed = BundleRv64gc::parse(&altered.to_json()).unwrap();
        assert_eq!(
            parsed.replay().unwrap(),
            ReplayRv64gc::Mismatch {
                boundary: Some(0),
                what: field.into()
            }
        );
    }
    let mut short = original.clone();
    short.recorded.steps.pop();
    assert_eq!(
        short.replay().unwrap(),
        ReplayRv64gc::Mismatch {
            boundary: Some(short.recorded_steps()),
            what: "boundary count".into()
        }
    );
    for (field, kind) in [
        ("model error receipt", 0),
        ("fetch count receipt", 1),
        ("final CPU/environment receipt", 2),
    ] {
        let mut altered = original.clone();
        match kind {
            0 => altered.recorded.failed = Some("changed \"error\"\nreceipt".into()),
            1 => altered.recorded.fetches ^= 1,
            _ => altered.final_sha256 = "0".repeat(64),
        }
        let parsed = BundleRv64gc::parse(&altered.to_json()).unwrap();
        assert_eq!(
            parsed.replay().unwrap(),
            ReplayRv64gc::Mismatch {
                boundary: None,
                what: field.into()
            }
        );
    }
    let guest = run_rv64gc::guest("a-lrsc-pair");
    let mut mid = BundleRv64gc::record(input(guest, 2, guest.executed_steps)).unwrap();
    mid.recorded.steps[0].pc ^= 2;
    assert_eq!(
        mid.replay().unwrap(),
        ReplayRv64gc::Mismatch {
            boundary: Some(2),
            what: "PC".into()
        }
    );
}

fn change_string(text: &str, key: &str, old: &str, new: &str) -> String {
    let before = format!("\"{key}\":\"{old}\"");
    assert_eq!(text.matches(&before).count(), 1);
    text.replacen(&before, &format!("\"{key}\":\"{new}\""), 1)
}

#[test]
fn foreign_producer_runtime_definition_and_corrupt_memory_refuse_before_replay() {
    let original = bundle();
    let text = original.to_json();
    let doc = json::parse(&text).unwrap();
    let checkpoint = field(&doc, "input").unwrap();
    let common = field(checkpoint, "common").unwrap();
    for (key, value, error) in [
        (
            "producer_sha256",
            field(&doc, "producer_sha256").unwrap(),
            "producer identity",
        ),
        (
            "runtime_sha256",
            field(checkpoint, "runtime_sha256").unwrap(),
            "definition/runtime identity",
        ),
        (
            "memory_sha256",
            field(common, "memory_sha256").unwrap(),
            "memory digest",
        ),
    ] {
        let altered = change_string(&text, key, value.as_str().unwrap(), &"0".repeat(64));
        let parsed = BundleRv64gc::parse(&altered).unwrap();
        assert!(parsed.replay().unwrap_err().contains(error), "{key}");
    }
    let altered = text.replacen("rv64gc-lab-v0", "foreign-profile", 1);
    assert!(BundleRv64gc::parse(&altered)
        .unwrap()
        .replay()
        .unwrap_err()
        .contains("identity"));
}

#[test]
fn partial_malformed_and_unsupported_records_refuse_by_name() {
    let original = bundle();
    let text = original.to_json();
    for key in [
        "input",
        "recorded",
        "final_sha256",
        "producer_sha256",
        "environment",
        "fregs",
        "csrs",
        "tlb",
        "reservation",
        "waiting",
    ] {
        let altered = text.replacen(&format!("\"{key}\":"), "\"omitted\":", 1);
        assert!(
            BundleRv64gc::parse(&altered).unwrap_err().contains(key),
            "{key}"
        );
    }
    for writes in [
        vec![(0, 1)],
        vec![(32, 1)],
        vec![(1, 1), (1, 2)],
        vec![(2, 1), (1, 2)],
    ] {
        let mut altered = original.clone();
        altered.recorded.steps[0].writes = writes;
        assert!(BundleRv64gc::parse(&altered.to_json())
            .unwrap_err()
            .contains("ordered unique"));
    }
    let altered = text.replacen(ENVIRONMENT, "unrecorded-external-events", 1);
    assert!(BundleRv64gc::parse(&altered)
        .unwrap_err()
        .contains("environment/event policy"));
    let altered = text.replacen(FORMAT, "unknown-format", 1);
    assert!(BundleRv64gc::parse(&altered)
        .unwrap_err()
        .contains("format"));
    let mut altered = original.clone();
    altered.final_sha256 = "not a digest".into();
    assert!(BundleRv64gc::parse(&altered.to_json())
        .unwrap_err()
        .contains("SHA256"));
    assert!(BundleRv64gc::parse(&"[".repeat(13))
        .unwrap_err()
        .contains("nesting"));
}

#[test]
fn continuation_bound_is_checked_before_execution() {
    let guest = run_rv64gc::guest("a-lrsc-pair");
    assert!(BundleRv64gc::record(input(guest, 0, MAX_BOUNDARIES + 1))
        .unwrap_err()
        .contains("10000"));
    let original = bundle();
    let text = original.to_json().replacen(
        &format!("\"budget\":{}", guest.executed_steps),
        &format!("\"budget\":{}", MAX_BOUNDARIES + 1),
        1,
    );
    assert!(BundleRv64gc::parse(&text).unwrap_err().contains("10000"));
}
