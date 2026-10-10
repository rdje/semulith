//! Boundary type and response-validation controls, including independent request/answer
//! properties and real CPU propagation (`docs/CPU_ENVIRONMENT.md` §4.1). Concrete
//! memory and scripted-environment behavior is tested in `semulith-verify`.

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

struct OneAnswer {
    answer: Result<Response, BoundaryError>,
    seen: Vec<Request>,
}

impl Environment for OneAnswer {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        self.seen.push(request);
        self.answer
    }
}

#[test]
fn every_response_kind_is_paired_with_only_its_request_kind() {
    let requests = [
        Request::Fetch { addr: 0x1000 },
        Request::FetchParcel { addr: 0x1002 },
        Request::Load {
            width: AccessWidth::B,
            addr: 0x2003,
        },
        Request::Store {
            width: AccessWidth::D,
            addr: 0x2008,
            data: 0x1234,
        },
        Request::WalkAccess { addr: 0x3000 },
        Request::StorePermission {
            width: AccessWidth::W,
            addr: 0x2004,
        },
    ];
    let responses = [
        Response::Fetch(0x1234),
        Response::FetchParcel(0x5678),
        Response::Load(0xff),
        Response::StoreDone,
        Response::WalkAccess(u64::MAX),
        Response::StorePermitted,
    ];
    for (i, request) in requests.into_iter().enumerate() {
        for (j, response) in responses.into_iter().enumerate() {
            let mut env = OneAnswer {
                answer: Ok(response),
                seen: vec![],
            };
            let expected = if i == j {
                Ok(response)
            } else {
                Err(BoundaryError::Violation(
                    ContractViolation::WrongResponseKind { request, response },
                ))
            };
            assert_eq!(
                request_checked(&mut env, request),
                expected,
                "{request:?}, {response:?}"
            );
            assert_eq!(
                env.seen,
                [request],
                "exactly one unmodified request crosses"
            );
        }
    }
}

#[test]
fn raw_load_width_edges_are_checked_without_truncating_or_rejecting_full_width() {
    for (width, maximum, first_invalid) in [
        (AccessWidth::B, 0xff, Some(0x100)),
        (AccessWidth::H, 0xffff, Some(0x1_0000)),
        (AccessWidth::W, 0xffff_ffff, Some(0x1_0000_0000)),
        (AccessWidth::D, u64::MAX, None),
    ] {
        let request = Request::Load {
            width,
            addr: 0x4000,
        };
        for value in [0, maximum] {
            let mut env = OneAnswer {
                answer: Ok(Response::Load(value)),
                seen: vec![],
            };
            assert_eq!(
                request_checked(&mut env, request),
                Ok(Response::Load(value))
            );
        }
        if let Some(first) = first_invalid {
            for value in [first, u64::MAX] {
                let mut env = OneAnswer {
                    answer: Ok(Response::Load(value)),
                    seen: vec![],
                };
                assert_eq!(
                    request_checked(&mut env, request),
                    Err(BoundaryError::Violation(
                        ContractViolation::LoadValueOutOfWidth { width, value }
                    ))
                );
            }
        }
    }
}

#[test]
fn validation_preserves_target_failures_and_existing_violations_exactly() {
    let request = Request::Load {
        width: AccessWidth::B,
        addr: 0x4000,
    };
    for error in [
        BoundaryError::Target(Failure::AccessFault),
        BoundaryError::Target(Failure::Misaligned),
        BoundaryError::Violation(ContractViolation::ScriptExhausted),
    ] {
        let mut env = OneAnswer {
            answer: Err(error),
            seen: vec![],
        };
        assert_eq!(request_checked(&mut env, request), Err(error));
        assert_eq!(env.seen, [request]);
    }
}

#[test]
fn malformed_answers_fail_the_real_cpu_as_violations_without_traps_or_load_effects() {
    use crate::exec_rv64gc::{self, StepRv64gc};
    use crate::outcome::ModelError;
    use crate::state_rv64gc::{ArchitecturalState, CSR_MCAUSE};

    struct Provider(u8);
    impl Environment for Provider {
        fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
            if self.0 == 0 {
                return Ok(Response::StoreDone);
            }
            match request {
                // Hand-encoded LB x6, 0(x5) = 0x00028303.
                Request::FetchParcel { addr: 0x1000 } => Ok(Response::FetchParcel(0x8303)),
                Request::FetchParcel { addr: 0x1002 } => Ok(Response::FetchParcel(0x0002)),
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x2000,
                } => {
                    if self.0 == 1 {
                        Ok(Response::Load(0x1ff))
                    } else {
                        Err(Failure::AccessFault.into())
                    }
                }
                _ => panic!("unexpected request: {request:?}"),
            }
        }
    }
    for (mode, violation) in [
        (
            0,
            ContractViolation::WrongResponseKind {
                request: Request::FetchParcel { addr: 0x1000 },
                response: Response::StoreDone,
            },
        ),
        (
            1,
            ContractViolation::LoadValueOutOfWidth {
                width: AccessWidth::B,
                value: 0x1ff,
            },
        ),
    ] {
        let mut state = ArchitecturalState::zeroed_at(0x1000);
        state.write_x(5, 0x2000);
        assert_eq!(
            exec_rv64gc::step(&mut state, &mut Provider(mode)),
            StepRv64gc::Failed(ModelError::ContractViolation(violation))
        );
        assert_eq!(state.pc(), 0x1000);
        assert_eq!(state.read_x(6), 0);
        assert_eq!(state.read_csr(CSR_MCAUSE), 0);
    }
    let mut state = ArchitecturalState::zeroed_at(0x1000);
    state.write_x(5, 0x2000);
    assert_eq!(
        exec_rv64gc::step(&mut state, &mut Provider(2)),
        StepRv64gc::Executed
    );
    assert_eq!(state.read_csr(CSR_MCAUSE), 5);
    assert_eq!(state.read_x(6), 0);

    let request = Request::Fetch { addr: 0x1000 };
    let mut env = OneAnswer {
        answer: Ok(Response::StoreDone),
        seen: vec![],
    };
    let mut scalar = crate::state::ArchitecturalState::zeroed_at(0x1000);
    assert_eq!(
        crate::exec::step(&mut scalar, &mut env),
        crate::outcome::StepOutcome::Failed(ModelError::ContractViolation(
            ContractViolation::WrongResponseKind {
                request,
                response: Response::StoreDone
            }
        ))
    );
    assert_eq!(scalar.pc(), 0x1000);

    let mut state = ArchitecturalState::zeroed_at(0x0040_0000);
    state.set_mode(crate::privilege::PrivilegeMode::S);
    state.write_csr(crate::state_rv64gc::CSR_SATP, (8 << 60) | 1);
    let mut env = OneAnswer {
        answer: Ok(Response::Load(0)),
        seen: vec![],
    };
    assert_eq!(
        crate::translation::translate(
            &mut state,
            &mut env,
            0x0040_0000,
            crate::translation::AccessKind::Load
        ),
        crate::translation::Translate::Failed(ModelError::ContractViolation(
            ContractViolation::WrongResponseKind {
                request: Request::WalkAccess { addr: 0x1000 },
                response: Response::Load(0)
            }
        ))
    );
}
