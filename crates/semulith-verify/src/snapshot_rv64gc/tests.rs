use super::*;
use crate::guests_rv64gc::{Guest, GUESTS};

fn environment(guest: &Guest) -> FlatMemory {
    let mut env = FlatMemory::with_fetch_align(guest.entry, 0x10000, 2);
    env.load_image(0, guest.image);
    env
}

fn checkpoint(guest: &Guest, at: usize) -> (Trace, SnapshotRv64gc) {
    let mut env = environment(guest);
    let mut state = ArchitecturalState::zeroed_at(guest.entry);
    let head = run_rv64gc::run_from_with_refusals(&mut env, &mut state, at, guest.refusals);
    assert!(head.failed.is_none(), "{}: {:?}", guest.name, head.failed);
    let snapshot = SnapshotRv64gc::capture(
        &env,
        &mut state,
        guest.entry,
        at,
        guest.executed_steps,
        guest.refusals,
    )
    .unwrap();
    (head, snapshot)
}

#[test]
fn every_gc_guest_resumes_through_json_with_identical_steps_state_memory_and_fetches() {
    for guest in GUESTS {
        let mut env = environment(guest);
        let mut state = ArchitecturalState::zeroed_at(guest.entry);
        let whole = run_rv64gc::run_from_with_refusals(
            &mut env,
            &mut state,
            guest.executed_steps,
            guest.refusals,
        );
        assert!(whole.failed.is_none(), "{}", guest.name);
        let final_state = SnapshotRv64gc::capture(
            &env,
            &mut state,
            guest.entry,
            guest.executed_steps,
            guest.executed_steps,
            guest.refusals,
        )
        .unwrap();
        for at in [
            1,
            guest.executed_steps / 2,
            guest.executed_steps.saturating_sub(1),
        ] {
            let (mut head, snapshot) = checkpoint(guest, at);
            let restored = SnapshotRv64gc::parse(&snapshot.to_json()).unwrap();
            assert_eq!(
                restored, snapshot,
                "{} at {at}: complete serialization",
                guest.name
            );
            let mut tail = restored.resume().unwrap();
            assert!(tail.trace.failed.is_none(), "{} at {at}", guest.name);
            head.steps.extend(tail.trace.steps);
            assert_eq!(
                head.steps, whole.steps,
                "{} at {at}: continuation",
                guest.name
            );
            assert_eq!(
                head.fetches + tail.trace.fetches,
                whole.fetches,
                "{} at {at}: fetches",
                guest.name
            );
            let actual = SnapshotRv64gc::capture(
                &tail.memory,
                &mut tail.state,
                guest.entry,
                guest.executed_steps,
                guest.executed_steps,
                guest.refusals,
            )
            .unwrap();
            assert_eq!(
                actual, final_state,
                "{} at {at}: final complete state",
                guest.name
            );
        }
    }
    println!(
        "{} RV64GC guests, {} JSON split continuations",
        GUESTS.len(),
        GUESTS.len() * 3
    );
}

#[test]
fn live_reservation_and_waiting_have_observable_continuation_effects() {
    for (name, owner) in [("a-lrsc-pair", "reservation"), ("w-timer", "waiting")] {
        let guest = run_rv64gc::guest(name);
        let mut witnessed = false;
        for at in 1..guest.executed_steps {
            let (_, snapshot) = checkpoint(guest, at);
            if (owner == "waiting" && !snapshot.waiting)
                || (owner == "reservation" && !snapshot.reservation.snapshot().2)
            {
                continue;
            }
            let expected = snapshot.resume().unwrap();
            let mut damaged = snapshot.clone();
            if owner == "waiting" {
                damaged.waiting = false;
            } else {
                damaged.reservation.clear();
            }
            let actual = damaged.resume().unwrap();
            if actual.trace != expected.trace {
                witnessed = true;
                break;
            }
        }
        assert!(
            witnessed,
            "{owner}: dropping this owner must change future observations"
        );
    }
}

#[test]
fn tlb_slots_and_fifo_cursor_survive_even_when_invalidated() {
    let guest = run_rv64gc::guest("sv39-tlb-fence");
    let mut env = environment(guest);
    let mut state = ArchitecturalState::zeroed_at(guest.entry);
    let mut warm = false;
    for at in 0..guest.executed_steps {
        let current = state.tlb().snapshot();
        if current.0.iter().any(|e| e.valid) {
            warm = true;
        }
        let snapshot = SnapshotRv64gc::capture(
            &env,
            &mut state,
            guest.entry,
            at,
            guest.executed_steps,
            guest.refusals,
        )
        .unwrap();
        let parsed = SnapshotRv64gc::parse(&snapshot.to_json()).unwrap();
        assert_eq!(parsed.tlb.snapshot(), current, "at {at}");
        let _ = run_rv64gc::run_from_with_refusals(&mut env, &mut state, 1, guest.refusals);
    }
    assert!(warm, "the fixture must exercise a populated TLB");
}

#[test]
fn a_warm_tlb_changes_future_walk_requests_so_cold_restore_is_not_exact() {
    use semulith_core::env::{BoundaryError, Environment, Request, Response};
    struct Observed {
        memory: FlatMemory,
        requests: Vec<Request>,
    }
    impl Environment for Observed {
        fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
            self.requests.push(request);
            self.memory.request(request)
        }
    }
    let guest = run_rv64gc::guest("sv39-tlb-fence");
    let mut witnessed = false;
    for at in 1..guest.executed_steps {
        let (_, snapshot) = checkpoint(guest, at);
        if snapshot.tlb.occupied() == 0 {
            continue;
        }
        let mut cold = snapshot.clone();
        cold.tlb = Tlb::new();
        let (mut warm_state, warm_memory) = snapshot.restore().unwrap();
        let (mut cold_state, cold_memory) = cold.restore().unwrap();
        let mut warm = Observed {
            memory: warm_memory,
            requests: Vec::new(),
        };
        let mut cold = Observed {
            memory: cold_memory,
            requests: Vec::new(),
        };
        let _ = semulith_core::exec_rv64gc::step(&mut warm_state, &mut warm);
        let _ = semulith_core::exec_rv64gc::step(&mut cold_state, &mut cold);
        if warm.requests != cold.requests {
            witnessed = true;
            break;
        }
    }
    assert!(
        witnessed,
        "dropping a warm TLB must change actual future environment requests"
    );
}

#[test]
fn identity_memory_and_missing_state_are_refused() {
    let guest = &GUESTS[0];
    let (_, snapshot) = checkpoint(guest, 1);
    let mut wrong = snapshot.clone();
    wrong.runtime_sha256 = "0".repeat(64);
    assert!(wrong.resume().err().unwrap().contains("identity mismatch"));
    wrong = snapshot.clone();
    wrong.common.algorithm.inputs[0].1 = "0".repeat(64);
    assert!(wrong.resume().err().unwrap().contains("identity mismatch"));
    wrong = snapshot.clone();
    wrong.common.runs[0].1[0] ^= 1;
    assert!(wrong
        .resume()
        .err()
        .unwrap()
        .contains("memory digest mismatch"));
    let text = snapshot.to_json();
    for key in [
        "mode",
        "waiting",
        "fregs",
        "csrs",
        "tlb",
        "reservation",
        "refusals",
    ] {
        let changed = text.replacen(&format!("\"{key}\":"), &format!("\"omitted_{key}\":"), 1);
        assert!(SnapshotRv64gc::parse(&changed).is_err(), "missing {key}");
    }
    for key in ["fregs", "csrs"] {
        let mut changed = text.clone();
        let start = changed.find(&format!("\"{key}\":[")).unwrap() + key.len() + 4;
        let end = start + changed[start..].find(']').unwrap();
        changed.replace_range(start..end, "\"0x0\"");
        assert!(SnapshotRv64gc::parse(&changed).is_err(), "partial {key}");
    }
    assert!(SnapshotRv64gc::parse(&text.replace("\"cursor\":0", "\"cursor\":4")).is_err());
    assert!(SnapshotRv64gc::parse(&text.replace("\"mode\":3", "\"mode\":2")).is_err());
    assert!(SnapshotRv64gc::parse(&text.replace("\"waiting\":false", "\"waiting\":0")).is_err());
}

#[test]
fn non_ascii_memory_hex_is_refused_in_both_snapshot_formats() {
    let (_, snapshot) = checkpoint(&GUESTS[0], 1);
    for (mut text, gc) in [
        (snapshot.common.to_json(), false),
        (snapshot.to_json(), true),
    ] {
        let start = text.find("\"bytes\":\"").unwrap() + "\"bytes\":\"".len();
        let end = start + text[start..].find('"').unwrap();
        text.replace_range(start..end, "\\u20ac0");
        let result = if gc {
            SnapshotRv64gc::parse(&text).map(|_| ())
        } else {
            Snapshot::parse(&text).map(|_| ())
        };
        assert!(
            result.is_err(),
            "non-ASCII memory hex must be a named refusal"
        );
    }
}

#[test]
fn bounds_and_noncanonical_memory_are_refused_before_execution() {
    let guest = &GUESTS[0];
    let (_, snapshot) = checkpoint(guest, 1);
    for (size, at, budget) in [
        (0, 0, 0),
        (MAX_MEMORY_BYTES + 1, 0, 0),
        (65536, 2, 1),
        (65536, 0, MAX_STEPS + 1),
    ] {
        let mut wrong = snapshot.clone();
        wrong.common.size = size;
        wrong.common.at_step = at;
        wrong.common.budget = budget;
        assert!(wrong.resume().is_err());
    }
    let mut wrong = snapshot.clone();
    wrong.common.base = u64::MAX;
    assert!(wrong.resume().is_err());
    let mut wrong = snapshot.clone();
    wrong.common.runs.push(wrong.common.runs[0].clone());
    assert!(wrong.resume().err().unwrap().contains("overlapping"));
    assert!(SnapshotRv64gc::parse(&"[".repeat(13))
        .unwrap_err()
        .contains("nesting"));
    let wide = format!("[{}0]", "0,".repeat(131072));
    assert!(SnapshotRv64gc::parse(&wide)
        .unwrap_err()
        .contains("structure limit"));
}

#[test]
fn zero_and_final_boundaries_and_cleared_reservation_round_trip() {
    let guest = run_rv64gc::guest("a-lrsc-pair");
    for at in [0, guest.executed_steps] {
        let (_, snapshot) = checkpoint(guest, at);
        let restored = SnapshotRv64gc::parse(&snapshot.to_json()).unwrap();
        assert_eq!(restored, snapshot);
        assert_eq!(
            restored.resume().unwrap().trace.steps.len(),
            guest.executed_steps - at
        );
    }
    let mut state = ArchitecturalState::zeroed_at(guest.entry);
    state.reservation().establish(guest.entry, 8);
    state.reservation().clear();
    let env = environment(guest);
    let snapshot = SnapshotRv64gc::capture(&env, &mut state, guest.entry, 0, 0, &[]).unwrap();
    let mut resumed = SnapshotRv64gc::parse(&snapshot.to_json())
        .unwrap()
        .resume()
        .unwrap();
    assert_eq!(
        resumed.state.reservation().snapshot(),
        (guest.entry, 8, false)
    );
}
