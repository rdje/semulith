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
