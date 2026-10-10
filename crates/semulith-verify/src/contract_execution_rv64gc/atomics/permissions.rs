//! Failed SC checks physical permission without issuing a data read or write.
use super::*;
#[cfg(test)]
use semulith_core::env::ContractViolation;
#[cfg(test)]
use semulith_core::outcome::ModelError;

fn seed(fixture: &mut Fixture, prior: usize, n: u32) {
    let reservation = fixture.hart.reservation();
    *reservation = Reservation::new();
    match prior {
        1 => {
            reservation.establish(DATA, n as u8);
            reservation.clear();
        }
        2 => reservation.establish(DATA + 32, n as u8),
        3 => reservation.establish(DATA, if n == 4 { 8 } else { 4 }),
        _ => {}
    }
    fixture.expected = Observation::capture(&mut fixture.hart, &fixture.observer, true);
}

fn expect_permission(fixture: &mut Fixture, n: u32, pa: u64) {
    fixture.expected.requests.push(Request::StorePermission {
        width: width(n),
        addr: pa,
    });
}

fn expect_fault(fixture: &mut Fixture, va: u64) {
    // The parent translated-AMO fixture pins MPRV. Here use this scenario's raw
    // initial status and mode: a Bare trap must not invent MPRV.
    let mode = match fixture.expected.mode {
        PrivilegeMode::M => 3,
        PrivilegeMode::S => 1,
        PrivilegeMode::U => 0,
    };
    let old = fixture.expected.csrs[CSR_MSTATUS];
    fixture.trap(7, va);
    fixture.expected.csrs[CSR_MSTATUS] =
        (old & !((3 << 11) | (1 << 7) | (1 << 3))) | (mode << 11) | ((old & 8) << 4);
}

fn bare_permissions() -> Result<(), String> {
    let mut count = 0;
    for n in [4, 8] {
        for order in 0..4 {
            for mode in MODES {
                for rd in [0, 6, 7, 9] {
                    for prior in 0..4 {
                        for access in 0..3 {
                            let address = if access == 1 { 0 } else { DATA };
                            let mut fixture =
                                Fixture::new(word(3, n, order, rd, 9), mode, &VECTORS[7], address);
                            seed(&mut fixture, prior, n);
                            if access == 2 {
                                fixture.observer.fail = Some(Request::StorePermission {
                                    width: width(n),
                                    addr: address,
                                });
                            }
                            fixture.fetch();
                            expect_permission(&mut fixture, n, address);
                            if access == 0 {
                                fixture.retire(rd, 1);
                                fixture.expected.reservation.clear();
                            } else {
                                expect_fault(&mut fixture, address);
                            }
                            judge(&fixture.observe(INSNS), &fixture.expected).map_err(|e| {
                                format!("permission W{n} order{order} {mode:?} rd{rd} prior{prior} access{access}: {e}")
                            })?;
                            count += 1;
                        }
                    }
                }
            }
        }
    }
    if count != 1152 {
        return Err(format!(
            "Bare permission matrix extent {count}, expected 1152"
        ));
    }
    Ok(())
}

fn translated_permissions() -> Result<(), String> {
    let mut count = 0;
    for n in [4, 8] {
        for order in 0..4 {
            for rd in [0, 6, 7, 9] {
                for prior in 0..4 {
                    for access in 0..3 {
                        let pa = if access == 1 { 0 } else { PA };
                        let mut fixture = Fixture::new(
                            word(3, n, order, rd, 9),
                            PrivilegeMode::M,
                            &VECTORS[7],
                            VA,
                        );
                        fixture.hart.write_csr(CSR_MSTATUS, 0xa_0002_6808);
                        fixture.hart.write_csr(CSR_SATP, 0x8000_0000_0000_0002);
                        for (address, value) in [
                            (0x2000_u64, 0xc01_u64),
                            (0x3000, 0x1001),
                            (0x4080, ((pa >> 12) << 10) | 0xc7),
                        ] {
                            fixture
                                .observer
                                .memory
                                .load_image((address - ENTRY) as usize, &value.to_le_bytes());
                        }
                        seed(&mut fixture, prior, n);
                        if access == 2 {
                            fixture.observer.fail = Some(Request::StorePermission {
                                width: width(n),
                                addr: pa,
                            });
                        }
                        fixture.fetch();
                        fixture.expected.requests.extend([
                            Request::WalkAccess { addr: 0x2000 },
                            Request::WalkAccess { addr: 0x3000 },
                            Request::WalkAccess { addr: 0x4080 },
                        ]);
                        fixture.expected.tlb.install(TlbEntry {
                            valid: true,
                            global: false,
                            asid: 0,
                            vpn: VA >> 12,
                            pa_base: pa,
                            r: true,
                            w: true,
                            x: false,
                            u: false,
                            a: true,
                            d: true,
                            level: 0,
                        });
                        expect_permission(&mut fixture, n, pa);
                        if access == 0 {
                            fixture.retire(rd, 1);
                            fixture.expected.reservation.clear();
                        } else {
                            expect_fault(&mut fixture, VA);
                        }
                        judge(&fixture.observe(INSNS), &fixture.expected).map_err(|e| {
                            format!("translated permission W{n} order{order} rd{rd} prior{prior} access{access}: {e}")
                        })?;
                        count += 1;
                    }
                }
            }
        }
    }
    if count != 384 {
        return Err(format!(
            "translated permission matrix extent {count}, expected 384"
        ));
    }
    Ok(())
}

pub(super) fn physical_permissions() -> Result<(), String> {
    bare_permissions()?;
    translated_permissions()
}

#[test]
fn failed_sc_checks_physical_permissions_before_retirement() {
    assert_eq!(bare_permissions(), Ok(()));
}

#[test]
fn translated_failed_sc_uses_physical_permission_and_virtual_fault_payload() {
    assert_eq!(translated_permissions(), Ok(()));
}

#[cfg(test)]
struct Answer<'a> {
    observer: &'a mut Observer,
    answer: Result<Response, BoundaryError>,
}
#[cfg(test)]
impl Environment for Answer<'_> {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        if matches!(request, Request::StorePermission { .. }) {
            self.observer.requests.push(request);
            self.answer
        } else {
            self.observer.request(request)
        }
    }
}

#[test]
fn malformed_permission_answers_are_model_errors_without_target_effects() {
    let mut count = 0;
    for n in [4, 8] {
        for rd in [0, 9] {
            for prior in 0..4 {
                for response in [
                    Response::Fetch(0),
                    Response::FetchParcel(0),
                    Response::Load(0),
                    Response::StoreDone,
                    Response::WalkAccess(0),
                ] {
                    let mut fixture =
                        Fixture::new(word(3, n, 0, rd, 9), PrivilegeMode::M, &VECTORS[7], DATA);
                    seed(&mut fixture, prior, n);
                    fixture.fetch();
                    fixture.expected.csrs[CSR_MCYCLE] = 41;
                    fixture.expected.executed = false;
                    expect_permission(&mut fixture, n, DATA);
                    let outcome = exec_rv64gc::step_over(
                        &mut fixture.hart,
                        &mut Answer {
                            observer: &mut fixture.observer,
                            answer: Ok(response),
                        },
                        INSNS,
                    );
                    assert_eq!(
                        outcome,
                        StepRv64gc::Failed(ModelError::ContractViolation(
                            ContractViolation::WrongResponseKind {
                                request: Request::StorePermission {
                                    width: width(n),
                                    addr: DATA
                                },
                                response,
                            },
                        ))
                    );
                    let actual = Observation::capture(&mut fixture.hart, &fixture.observer, false);
                    assert_eq!(judge(&actual, &fixture.expected), Ok(()));
                    count += 1;
                }
            }
        }
    }
    assert_eq!(count, 80);
}

#[test]
fn permission_misalignment_answer_is_a_store_access_fault() {
    for n in [4, 8] {
        for prior in 0..4 {
            let mut fixture =
                Fixture::new(word(3, n, 0, 7, 9), PrivilegeMode::M, &VECTORS[7], DATA);
            seed(&mut fixture, prior, n);
            fixture.fetch();
            expect_permission(&mut fixture, n, DATA);
            expect_fault(&mut fixture, DATA);
            let outcome = exec_rv64gc::step_over(
                &mut fixture.hart,
                &mut Answer {
                    observer: &mut fixture.observer,
                    answer: Err(BoundaryError::Target(Failure::Misaligned)),
                },
                INSNS,
            );
            assert_eq!(outcome, StepRv64gc::Executed);
            let actual = Observation::capture(&mut fixture.hart, &fixture.observer, true);
            assert_eq!(judge(&actual, &fixture.expected), Ok(()));
        }
    }
}

#[test]
fn nonmatching_sc_never_issues_the_refused_data_store() {
    let mut fixture = Fixture::new(word(3, 4, 0, 7, 9), PrivilegeMode::M, &VECTORS[7], DATA);
    seed(&mut fixture, 0, 4);
    fixture.observer.fail = Some(Request::Store {
        width: AccessWidth::W,
        addr: DATA,
        data: VECTORS[7].source & 0xffff_ffff,
    });
    fixture.fetch();
    expect_permission(&mut fixture, 4, DATA);
    fixture.retire(7, 1);
    fixture.expected.reservation.clear();
    assert_eq!(judge(&fixture.observe(INSNS), &fixture.expected), Ok(()));
}
