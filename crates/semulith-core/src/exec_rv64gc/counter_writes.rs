//! RVI-ZICSR 5.1.1 and RVP-MACHINE 2.1.1.10: explicit counter writes
//! replace the instruction's implicit increment. Expectations precede execution.

use super::*;
use crate::state_rv64gc::{CSR_MCAUSE, CSR_MCYCLE, CSR_MINSTRET, CSR_MTVEC};

const ENTRY: u64 = 0x1000;

struct Program {
    words: [u32; 2],
    requests: Vec<Request>,
}

impl Environment for Program {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        self.requests.push(request);
        let Request::FetchParcel { addr } = request else {
            panic!("counter instruction issued a non-fetch request: {request:?}");
        };
        let offset = (addr - ENTRY) as usize;
        assert!(offset < 8 && offset.is_multiple_of(2));
        Ok(Response::FetchParcel(
            (self.words[offset / 4] >> ((offset % 4) * 8)) as u16,
        ))
    }
}

fn word(address: u32, op: u32, source: u32, rd: u32) -> u32 {
    (address << 20) | (source << 15) | (op << 12) | (rd << 7) | 0x73
}

fn hart(cycle: u64, retired: u64) -> ArchitecturalState {
    let mut h = ArchitecturalState::zeroed_at(ENTRY);
    h.write_csr(CSR_MCYCLE, cycle);
    h.write_csr(CSR_MINSTRET, retired);
    h.write_csr(CSR_MTVEC, 0x1100);
    for r in 1..32 {
        h.write_x(r, 0x1111_2222_3333_0000 + u64::from(r));
    }
    h
}

fn check_writes(address: u32, index: usize) {
    for before in [41, u64::MAX, 0x8000_0001_2345_6789] {
        for op in [1, 2, 3, 5, 6, 7] {
            for source in [0, 6, 31] {
                for input in [0, before, 47, u64::MAX] {
                    for rd in [0, 5, 6, 31] {
                        let mut h = hart(73, 17);
                        h.write_csr(index, before);
                        h.write_x(6, input);
                        h.write_x(31, input);
                        let mut expected_x = std::array::from_fn::<_, 32, _>(|r| h.read_x(r as u8));
                        // CSRRS/CSRRC suppress writes by source FIELD, not source VALUE.
                        let writes = op == 1 || op == 5 || source != 0;
                        let operand = if op >= 5 {
                            u64::from(source)
                        } else {
                            h.read_x(source as u8)
                        };
                        let value = match op {
                            1 | 5 => operand,
                            2 | 6 => before | operand,
                            3 | 7 => before & !operand,
                            _ => unreachable!(),
                        };
                        let final_value = if writes {
                            value
                        } else {
                            before.wrapping_add(1)
                        };
                        let mut cycle = h.read_csr(CSR_MCYCLE).wrapping_add(1);
                        let mut retired = h.read_csr(CSR_MINSTRET).wrapping_add(1);
                        if index == CSR_MCYCLE {
                            cycle = final_value;
                        } else {
                            retired = final_value;
                        }
                        if rd != 0 {
                            expected_x[rd as usize] = before;
                        }
                        let instruction = word(address, op, source, rd);
                        // The following read-only view must see the exact committed value.
                        let mut p = Program {
                            words: [instruction, word(address + 0x100, 2, 0, 7)],
                            requests: Vec::new(),
                        };
                        assert_eq!(step(&mut h, &mut p), StepRv64gc::Executed);
                        assert_eq!(h.pc(), ENTRY + 4);
                        assert_eq!(h.read_csr(CSR_MCAUSE), 0);
                        assert_eq!(h.mode(), privilege::PrivilegeMode::M);
                        assert_eq!(privilege::csr_read(&h, 0xc01), Ok(cycle));
                        assert_eq!(
                            h.read_csr(CSR_MCYCLE),
                            cycle,
                            "cycle after {instruction:#010x}, before {before:#x}, input {input:#x}"
                        );
                        assert_eq!(
                            h.read_csr(CSR_MINSTRET),
                            retired,
                            "instret after {instruction:#010x}, before {before:#x}, input {input:#x}",
                        );
                        assert_eq!(
                            std::array::from_fn::<_, 32, _>(|r| h.read_x(r as u8)),
                            expected_x
                        );
                        expected_x[7] = final_value;
                        assert_eq!(step(&mut h, &mut p), StepRv64gc::Executed);
                        assert_eq!(h.pc(), ENTRY + 8);
                        assert_eq!(h.read_csr(CSR_MCYCLE), cycle.wrapping_add(1));
                        assert_eq!(h.read_csr(CSR_MINSTRET), retired.wrapping_add(1));
                        assert_eq!(
                            std::array::from_fn::<_, 32, _>(|r| h.read_x(r as u8)),
                            expected_x
                        );
                        assert_eq!(
                            p.requests,
                            (0..4)
                                .map(|i| Request::FetchParcel {
                                    addr: ENTRY + i * 2
                                })
                                .collect::<Vec<_>>()
                        );
                    }
                }
            }
        }
    }
}

#[test]
fn mcycle_writes_override_the_writing_instruction_increment() {
    assert_eq!(word(0xb00, 1, 6, 5), 0xb003_12f3);
    check_writes(0xb00, CSR_MCYCLE);
}

#[test]
fn minstret_writes_override_the_writing_instruction_increment() {
    assert_eq!(word(0xb02, 1, 6, 5), 0xb023_12f3);
    check_writes(0xb02, CSR_MINSTRET);
}

#[test]
fn refused_counter_writes_keep_normal_nonretiring_progress() {
    for mode in [privilege::PrivilegeMode::S, privilege::PrivilegeMode::U] {
        for address in [0xb00, 0xb02] {
            for op in [1, 2, 3, 5, 6, 7] {
                for rd in [0, 5] {
                    let mut h = hart(73, 17);
                    h.set_mode(mode);
                    let old_x = std::array::from_fn::<_, 32, _>(|r| h.read_x(r as u8));
                    let mut p = Program {
                        words: [word(address, op, 6, rd), 0],
                        requests: Vec::new(),
                    };
                    assert_eq!(step(&mut h, &mut p), StepRv64gc::Executed);
                    assert_eq!(h.pc(), 0x1100);
                    assert_eq!(h.read_csr(CSR_MCAUSE), 2);
                    assert_eq!(h.read_csr(CSR_MCYCLE), 74);
                    assert_eq!(h.read_csr(CSR_MINSTRET), 17);
                    assert_eq!(
                        std::array::from_fn::<_, 32, _>(|r| h.read_x(r as u8)),
                        old_x
                    );
                    assert_eq!(
                        p.requests,
                        vec![
                            Request::FetchParcel { addr: ENTRY },
                            Request::FetchParcel { addr: ENTRY + 2 }
                        ]
                    );
                }
            }
        }
    }
}
