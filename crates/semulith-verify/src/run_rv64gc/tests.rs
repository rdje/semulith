//! The rv64gc corpus proof on the TRACKED engine (`P4-SYSTEM.2` slice h): every tracked
//! guest — the 49 base-mirror guests and the 13 mode-matrix guests — executed through
//! `exec_rv64gc` and falsified against its specification-derived expectations (EVD-05),
//! with the same assertion family the base profile's offline differential uses.

use super::{assert_guest_observations, run_guest};
use crate::guests_rv64gc::GUESTS;

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

#[test]
fn parcel_injection_does_not_refuse_an_unrequested_next_parcel() {
    use super::{refused, Refusal, RefusalKind};
    use semulith_core::env::Request;
    let regions = [Refusal {
        kind: RefusalKind::Fetch,
        base: 0x1002,
        size: 2,
    }];
    assert!(!refused(&regions, &Request::FetchParcel { addr: 0x1000 }));
    assert!(refused(&regions, &Request::FetchParcel { addr: 0x1002 }));
    assert!(refused(&regions, &Request::Fetch { addr: 0x1000 }));
}

/// The injection carrier's predicate (`P4-SYSTEM.8` slice c): a request is refused exactly
/// when its kind matches and its bytes intersect the region — no more, no less.
#[test]
fn the_refusal_predicate_refuses_exactly_the_declared_bytes_and_kind() {
    use super::{refused, Refusal, RefusalKind};
    use semulith_core::env::{AccessWidth, Request};
    let regions = [Refusal {
        kind: RefusalKind::Store,
        base: 0x8000_0400,
        size: 8,
    }];
    let store = |addr| Request::Store {
        width: AccessWidth::W,
        addr,
        data: 0,
    };
    assert!(
        refused(&regions, &store(0x8000_0400)),
        "the first word inside"
    );
    assert!(
        refused(&regions, &store(0x8000_0404)),
        "the last word inside"
    );
    assert!(
        refused(&regions, &store(0x8000_03FE)),
        "straddling the start"
    );
    assert!(refused(&regions, &store(0x8000_0406)), "straddling the end");
    assert!(
        !refused(&regions, &store(0x8000_03FC)),
        "adjacent below: untouched"
    );
    assert!(
        !refused(&regions, &store(0x8000_0408)),
        "adjacent above: untouched"
    );
    let load = Request::Load {
        width: AccessWidth::W,
        addr: 0x8000_0400,
    };
    assert!(
        !refused(&regions, &load),
        "another kind on the same bytes: untouched"
    );
    let walk = [Refusal {
        kind: RefusalKind::Walk,
        base: 0x8000_3018,
        size: 8,
    }];
    assert!(
        refused(&walk, &Request::WalkAccess { addr: 0x8000_3018 }),
        "a PTE read"
    );
    assert!(
        !refused(&walk, &Request::WalkAccess { addr: 0x8000_3010 }),
        "the PTE before"
    );
}

/// `P4-SYSTEM.12` slice (a2): the rv64gc engine's JAL at the offset's sign boundary and both
/// extremes (the defect and its cause are stated at `exec::tests`' twin of this test).
#[test]
fn jal_offsets_at_the_sign_boundary_reach_their_targets() {
    use crate::fixtures::FlatMemory;
    use semulith_core::exec_rv64gc::{step, StepRv64gc};
    use semulith_core::state_rv64gc::ArchitecturalState;
    const ENTRY: u64 = 0x8000_0000;
    let cases: [(u32, i64); 5] = [
        // (word, offset): the words from the tracked assembler, not this file's encoder
        (0x7fd7f06f, 0x7fffc),  // the control: below the boundary, bit 19 clear
        (0x0008006f, 0x80000),  // +2^19: bit 19 set, bit 20 clear — a FORWARD jump
        (0xffd7f06f, -0x80004), // just past -2^19: bit 20 set, bit 19 clear — a BACKWARD jump
        (0x7fdff06f, 0xffffc),  // the largest forward offset
        (0x8000006f, -0x100000), // the most negative offset
    ];
    for (word, offset) in cases {
        let mut memory = FlatMemory::new(ENTRY, 4096);
        memory.load_image(0, &word.to_le_bytes());
        let mut state = ArchitecturalState::zeroed_at(ENTRY);
        assert_eq!(
            step(&mut state, &mut memory),
            StepRv64gc::Executed,
            "jal {offset:#x}"
        );
        assert_eq!(
            state.pc(),
            ENTRY.wrapping_add(offset as u64),
            "jal {offset:#x}: the target is the jump's address plus the SIGNED offset"
        );
    }
}
