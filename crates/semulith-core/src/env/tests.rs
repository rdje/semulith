//! Tests for the boundary contract types themselves — the properties that hold with no
//! fixture and no instruction handler (`docs/CPU_ENVIRONMENT.md` §4.1: requests and
//! responses are testable against contract properties independently of the CPU
//! instruction handler). Fixture behavior is tested in `semulith-verify`.

use super::*;

#[test]
fn widths_are_exactly_the_offered_set() {
    // OB-ENV-ACCESS-WIDTHS: 8/16/32/64 and nothing else — the enum's exhaustiveness is
    // the contract; a fifth width cannot be requested.
    assert_eq!(AccessWidth::B.bits(), 8);
    assert_eq!(AccessWidth::H.bits(), 16);
    assert_eq!(AccessWidth::W.bits(), 32);
    assert_eq!(AccessWidth::D.bits(), 64);
    assert_eq!(AccessWidth::B.bytes(), 1);
    assert_eq!(AccessWidth::H.bytes(), 2);
    assert_eq!(AccessWidth::W.bytes(), 4);
    assert_eq!(AccessWidth::D.bytes(), 8);
}

#[test]
fn fetch_width_is_pinned_by_construction() {
    // OB-ENV-FETCH-SUPPLY: fetch is exactly 32 bits. It cannot carry another width
    // because it carries no width at all — `Request::Fetch` has only an address.
    let request = Request::Fetch { addr: 0x1000 };
    let Request::Fetch { addr } = request else {
        panic!("Fetch is Fetch");
    };
    assert_eq!(addr, 0x1000);
}

#[test]
fn failures_and_violations_are_distinct_families() {
    // SEM-01 in embryo: a target-facing failure answer and a contract violation must not
    // be interchangeable, and `BoundaryError` keeps them apart by construction.
    let failure = BoundaryError::from(Failure::Misaligned);
    let violation = BoundaryError::from(ContractViolation::ScriptExhausted);
    assert!(matches!(
        failure,
        BoundaryError::Target(Failure::Misaligned)
    ));
    assert!(matches!(violation, BoundaryError::Violation(_)));
    assert_ne!(failure, violation);
}

#[test]
fn mismatch_reports_both_sides() {
    let scripted = Request::Load {
        width: AccessWidth::W,
        addr: 0x2000,
    };
    let arrived = Request::Store {
        width: AccessWidth::W,
        addr: 0x2000,
        data: 0,
    };
    let v = ContractViolation::ResponseMismatch { scripted, arrived };
    let BoundaryError::Violation(v) = BoundaryError::from(v) else {
        panic!("a violation is a violation");
    };
    assert_eq!(v, ContractViolation::ResponseMismatch { scripted, arrived });
}
