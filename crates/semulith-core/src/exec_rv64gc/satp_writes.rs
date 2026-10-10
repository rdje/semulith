//! RVP-SUPERVISOR 11.1.1.11: unsupported MODE ignores the whole satp write.
//! Literal expected transitions precede public CSR and instruction execution.

use super::*;
use crate::privilege::PrivilegedHart;
use crate::reservation::Reservation;
use crate::state_rv64gc::{
    CSR_COUNT, CSR_MCAUSE, CSR_MCYCLE, CSR_MEPC, CSR_MINSTRET, CSR_MSTATUS, CSR_MTVAL, CSR_MTVEC,
    CSR_SATP,
};
use crate::translation::{Tlb, TlbEntry};
use crate::wait::HartState;

const ENTRY: u64 = 0x1000;
const OLD: [u64; 2] = [0, 0x8abc_d123_4567_89ab];
const PAYLOAD: [u64; 3] = [0, 0x0123_4567_89ab_cdef, 0x0fff_ffff_ffff_ffff];

#[derive(Clone)]
struct Snapshot {
    x: [u64; 32],
    f: [u64; 32],
    csr: [u64; CSR_COUNT],
    pc: u64,
    mode: privilege::PrivilegeMode,
    tlb: Tlb,
    reservation: Reservation,
    wait: HartState,
}

impl Snapshot {
    fn capture(h: &mut ArchitecturalState) -> Self {
        Self {
            x: std::array::from_fn(|r| h.read_x(r as u8)),
            f: std::array::from_fn(|r| h.read_f(r as u8)),
            csr: std::array::from_fn(|i| h.read_csr(i)),
            pc: h.pc(),
            mode: h.mode(),
            tlb: h.tlb().clone(),
            reservation: *h.reservation(),
            wait: *h.hart_state(),
        }
    }

    fn check(&self, h: &mut ArchitecturalState) {
        let a = Self::capture(h);
        assert_eq!(a.csr[CSR_SATP], self.csr[CSR_SATP], "whole satp value");
        assert!(a.x == self.x, "GPRs differ");
        assert!(a.f == self.f, "FPRs differ");
        assert!(a.csr == self.csr, "CSR owners differ");
        assert_eq!((a.pc, a.mode), (self.pc, self.mode));
        assert_eq!(a.tlb, self.tlb);
        assert_eq!(a.reservation, self.reservation);
        assert_eq!(a.wait, self.wait);
    }
}

fn hart(before: u64) -> ArchitecturalState {
    let mut h = ArchitecturalState::zeroed_at(ENTRY);
    h.write_csr(CSR_SATP, before);
    h.write_csr(CSR_MSTATUS, 0xa_0000_6000);
    h.write_csr(CSR_MTVEC, 0x1100);
    h.write_csr(CSR_MCAUSE, 0x55);
    h.write_csr(CSR_MEPC, 0x1200);
    h.write_csr(CSR_MTVAL, 0x7788);
    h.write_csr(CSR_MCYCLE, 41);
    h.write_csr(CSR_MINSTRET, 17);
    for r in 1..32 {
        h.write_x(r, 0x1111_2222_3333_0000 + u64::from(r));
    }
    for r in 0..32 {
        h.write_f(r, 0x7ff8_0000_0000_1000 + u64::from(r));
    }
    h.reservation().establish(0x1080, 8);
    for i in 0_u64..5 {
        h.tlb().install(TlbEntry {
            valid: true,
            global: i.is_multiple_of(2),
            asid: 0x12,
            vpn: 0x40 + i,
            pa_base: 0x9000 + i * 0x1000,
            r: true,
            w: true,
            x: true,
            u: false,
            a: true,
            d: true,
            level: 0,
        });
    }
    h
}

fn accepted(value: u64) -> bool {
    matches!(value >> 60, 0 | 8)
}

fn word(op: u32, source: u32, rd: u32) -> u32 {
    0x1800_0073 | (source << 15) | (op << 12) | (rd << 7)
}

struct Program {
    words: [u32; 2],
    requests: Vec<Request>,
}

impl Environment for Program {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        self.requests.push(request);
        let Request::FetchParcel { addr } = request else {
            panic!("CSR instruction issued a non-fetch request: {request:?}");
        };
        let offset = (addr - ENTRY) as usize;
        assert!(offset < 8 && offset.is_multiple_of(2));
        Ok(Response::FetchParcel(
            (self.words[offset / 4] >> ((offset % 4) * 8)) as u16,
        ))
    }
}

#[test]
fn satp_public_writes_ignore_all_unsupported_modes_after_permission_checks() {
    let mut count = 0;
    for mode in [
        privilege::PrivilegeMode::M,
        privilege::PrivilegeMode::S,
        privilege::PrivilegeMode::U,
    ] {
        for tvm in [0, 1 << 20] {
            for before in OLD {
                for incoming_mode in 0..16 {
                    for payload in PAYLOAD {
                        let value = (incoming_mode << 60) | payload;
                        let mut h = hart(before);
                        h.set_mode(mode);
                        h.write_csr(CSR_MSTATUS, 0xa_0000_6000 | tvm);
                        let mut expected = Snapshot::capture(&mut h);
                        let permitted = mode == privilege::PrivilegeMode::M
                            || (mode == privilege::PrivilegeMode::S && tvm == 0);
                        if permitted && accepted(value) {
                            expected.csr[CSR_SATP] = value;
                        }
                        let result = privilege::csr_write(&mut h, 0x180, value);
                        assert_eq!(
                            result.is_ok(),
                            permitted,
                            "mode/TVM permission must precede ignore"
                        );
                        expected.check(&mut h);
                        count += 1;
                    }
                }
            }
        }
    }
    assert_eq!(count, 576);
}

#[test]
fn satp_all_csr_forms_preserve_unsupported_writes_and_read_back_exactly() {
    let mut count = 0;
    for before in OLD {
        for op in [1, 2, 3, 5, 6, 7] {
            for source in [0, 6, 31] {
                for incoming_mode in 0..16 {
                    for payload in PAYLOAD {
                        // Immediate forms encode their entire input in the five-bit field.
                        if op >= 5 && (incoming_mode != 0 || payload != 0) {
                            continue;
                        }
                        let input = (incoming_mode << 60) | payload;
                        for rd in [0, 5, 6, 31] {
                            let mut h = hart(before);
                            h.write_x(6, input);
                            h.write_x(31, input);
                            let mut expected = Snapshot::capture(&mut h);
                            let operand = if op >= 5 {
                                u64::from(source)
                            } else {
                                expected.x[source as usize]
                            };
                            let writes = op == 1 || op == 5 || source != 0;
                            let value = match op {
                                1 | 5 => operand,
                                2 | 6 => before | operand,
                                3 | 7 => before & !operand,
                                _ => unreachable!(),
                            };
                            if writes && accepted(value) {
                                expected.csr[CSR_SATP] = value;
                            }
                            if rd != 0 {
                                expected.x[rd as usize] = before;
                            }
                            expected.pc = ENTRY + 4;
                            expected.csr[CSR_MCYCLE] = 42;
                            expected.csr[CSR_MINSTRET] = 18;
                            let mut p = Program {
                                words: [word(op, source, rd), word(2, 0, 7)],
                                requests: Vec::new(),
                            };
                            assert_eq!(step(&mut h, &mut p), StepRv64gc::Executed);
                            expected.check(&mut h);
                            expected.x[7] = expected.csr[CSR_SATP];
                            expected.pc = ENTRY + 8;
                            expected.csr[CSR_MCYCLE] = 43;
                            expected.csr[CSR_MINSTRET] = 19;
                            assert_eq!(step(&mut h, &mut p), StepRv64gc::Executed);
                            expected.check(&mut h);
                            assert_eq!(
                                p.requests,
                                (0..4)
                                    .map(|i| Request::FetchParcel {
                                        addr: ENTRY + i * 2
                                    })
                                    .collect::<Vec<_>>()
                            );
                            count += 1;
                        }
                    }
                }
            }
        }
    }
    assert_eq!(count, 3528);
}

#[test]
fn satp_instruction_refusals_precede_unsupported_mode_ignoring() {
    let mut count = 0;
    for mode in [privilege::PrivilegeMode::S, privilege::PrivilegeMode::U] {
        for op in [1, 2, 3, 5, 6, 7] {
            for source in [0, 6, 31] {
                for rd in [0, 5] {
                    let mut h = hart(0); // Bare fetch in S/U; TVM=1 gates S access.
                    h.set_mode(mode);
                    h.write_csr(CSR_MSTATUS, 0xa_0010_6000);
                    h.write_x(6, 0xfabc_dfff_ffff_ffff);
                    h.write_x(31, 0xfabc_dfff_ffff_ffff);
                    let mut expected = Snapshot::capture(&mut h);
                    let instruction = word(op, source, rd);
                    expected.csr[CSR_MCAUSE] = 2;
                    expected.csr[CSR_MEPC] = ENTRY;
                    expected.csr[CSR_MTVAL] = u64::from(instruction);
                    expected.csr[CSR_MSTATUS] = (expected.csr[CSR_MSTATUS]
                        & !((3 << 11) | (1 << 7) | (1 << 3)))
                        | (mode.code() << 11);
                    expected.csr[CSR_MCYCLE] = 42;
                    expected.pc = 0x1100;
                    expected.mode = privilege::PrivilegeMode::M;
                    let mut p = Program {
                        words: [instruction, 0],
                        requests: Vec::new(),
                    };
                    assert_eq!(step(&mut h, &mut p), StepRv64gc::Executed);
                    expected.check(&mut h);
                    assert_eq!(
                        p.requests,
                        vec![
                            Request::FetchParcel { addr: ENTRY },
                            Request::FetchParcel { addr: ENTRY + 2 }
                        ]
                    );
                    count += 1;
                }
            }
        }
    }
    assert_eq!(count, 72);
}
