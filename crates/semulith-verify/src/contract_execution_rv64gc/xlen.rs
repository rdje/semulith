//! RV64 integer/user-address witnesses (RV64I 3.1.1; Sv39 11.1.4).

use semulith_core::definition_rv64gc::{InsnDef, INSNS};
use semulith_core::env::{AccessWidth, BoundaryError, Environment, Request, Response};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_MCAUSE, CSR_MCYCLE, CSR_MEPC, CSR_MINSTRET, CSR_MSTATUS,
    CSR_MTVAL, CSR_SATP,
};

use crate::fixtures::FlatMemory;

const BASE: u64 = 0x8000_0000;
const PC: u64 = 0x8000_1000;
const DATA: u64 = 0x8000_1080;
const WORDS: [u32; 4] = [0x0003_0393, 0x0003_3403, 0x0083_3423, 0x0000_0497];

#[derive(Clone, Copy)]
struct Case {
    name: &'static str,
    entry: u64,
    pte: u64,
    payload: u64,
}

const POSITIVE: Case = Case {
    name: "above32",
    entry: 0x0000_0001_0000_1000,
    pte: 0x8000_2020,
    payload: 0x0123_4567_89ab_cdef,
};
const NEGATIVE: Case = Case {
    name: "high-canonical",
    entry: 0xffff_ffff_8000_1000,
    pte: 0x8000_2ff0,
    payload: 0xfedc_ba98_7654_3210,
};

struct Observer {
    memory: FlatMemory,
    requests: Vec<Request>,
}

impl Environment for Observer {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        self.requests.push(request);
        self.memory.request(request)
    }
}

fn check_case(table: &[InsnDef], case: Case) -> Result<(), String> {
    let mut memory = FlatMemory::with_fetch_align(BASE, 0x4000, 2);
    for (i, word) in WORDS.iter().enumerate() {
        memory.load_image(0x1000 + i * 4, &word.to_le_bytes());
    }
    // One 1 GiB leaf maps this canonical VA to ordinary laboratory RAM.
    // V/R/W/X/U/A/D are set; other root entries stay invalid.
    memory.load_image((case.pte - BASE) as usize, &0x2000_00df_u64.to_le_bytes());
    memory.load_image(0x1080, &case.payload.to_le_bytes());
    let mut expected_memory = memory.bytes().to_vec();
    let mut observer = Observer {
        memory,
        requests: Vec::new(),
    };
    let mut hart = ArchitecturalState::zeroed_at(case.entry);
    hart.set_mode(PrivilegeMode::U);
    hart.write_csr(CSR_SATP, 0x8000_0000_0008_0002);
    // Expectations precede the writes: a narrow register file cannot supply
    // its own expected values through a read-back snapshot.
    let mut expected_x = [0; 32];
    for (reg, value) in expected_x.iter_mut().enumerate().skip(1) {
        *value = 0x0123_4567_0000_0000 + reg as u64;
        hart.write_x(reg as u8, *value);
    }
    expected_x[6] = case.entry + 0x80;
    hart.write_x(6, expected_x[6]);
    hart.write_x(0, u64::MAX);
    let mut requests = vec![Request::WalkAccess { addr: case.pte }];
    for i in 0..4 {
        let offset = i * 4;
        requests.extend([
            Request::FetchParcel { addr: PC + offset },
            Request::FetchParcel {
                addr: PC + offset + 2,
            },
        ]);
        match i {
            0 => expected_x[7] = case.entry + 0x80,
            1 => {
                expected_x[8] = case.payload;
                requests.push(Request::Load {
                    width: AccessWidth::D,
                    addr: DATA,
                });
            }
            2 => {
                requests.push(Request::Store {
                    width: AccessWidth::D,
                    addr: DATA + 8,
                    data: case.payload,
                });
                expected_memory[0x1088..0x1090].copy_from_slice(&case.payload.to_le_bytes());
            }
            3 => expected_x[9] = case.entry + 12,
            _ => unreachable!(),
        }
        let outcome = exec_rv64gc::step_over(&mut hart, &mut observer, table);
        if observer.requests != requests {
            return Err(format!(
                "{} boundary {}: requests differ: {:?}, required {requests:?}",
                case.name,
                i + 1,
                observer.requests
            ));
        }
        if outcome != StepRv64gc::Executed
            || hart.pc() != case.entry + offset + 4
            || hart.mode() != PrivilegeMode::U
            || hart.read_csr(CSR_MSTATUS) & (3 << 32) != 2 << 32
            || hart.read_csr(CSR_MCAUSE) != 0
            || hart.read_csr(CSR_MEPC) != 0
            || hart.read_csr(CSR_MTVAL) != 0
            || hart.read_csr(CSR_MCYCLE) != i + 1
            || hart.read_csr(CSR_MINSTRET) != i + 1
            || observer.memory.fetch_count() != (i + 1) * 2
            || observer.memory.bytes() != expected_memory
            || expected_x
                .iter()
                .enumerate()
                .any(|(r, value)| hart.read_x(r as u8) != *value)
        {
            return Err(format!(
                "{} boundary {}: full-width state differs: {outcome:?}",
                case.name,
                i + 1
            ));
        }
    }
    Ok(())
}

pub(super) fn positive() -> Result<(), String> {
    check_case(INSNS, POSITIVE)
}

pub(super) fn negative() -> Result<(), String> {
    check_case(INSNS, NEGATIVE)
}

#[cfg(test)]
mod tests {
    use super::*;
    use semulith_core::definition_rv64gc::Sem;

    const MASK: Sem = Sem::Lit(0xffff_ffff);
    const ADDRESS: Sem = Sem::Add(&Sem::Reg("rs1"), &Sem::Sext(64, &Sem::Imm("imm12")));
    static BAD_EFFECTS: [(&str, &str, Sem, &str); 7] = [
        (
            "ADDI result32",
            "addi",
            Sem::Set(&Sem::Reg("rd"), &Sem::And(&ADDRESS, &MASK)),
            "state differs",
        ),
        (
            "LD address32",
            "ld",
            Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Load(&Sem::Lit(64), &Sem::Lit(1), &Sem::And(&ADDRESS, &MASK)),
            ),
            "requests differ",
        ),
        (
            "SD address32",
            "sd",
            Sem::Store(
                &Sem::Lit(64),
                &Sem::And(
                    &Sem::Add(&Sem::Reg("rs1"), &Sem::Sext(64, &Sem::Imm("imm12"))),
                    &MASK,
                ),
                &Sem::Reg("rs2"),
            ),
            "requests differ",
        ),
        (
            "LD value32",
            "ld",
            Sem::Set(
                &Sem::Reg("rd"),
                &Sem::And(&Sem::Load(&Sem::Lit(64), &Sem::Lit(1), &ADDRESS), &MASK),
            ),
            "state differs",
        ),
        (
            "SD value32",
            "sd",
            Sem::Store(
                &Sem::Lit(64),
                &Sem::Add(&Sem::Reg("rs1"), &Sem::Sext(64, &Sem::Imm("imm12"))),
                &Sem::And(&Sem::Reg("rs2"), &MASK),
            ),
            "requests differ",
        ),
        (
            "AUIPC result32",
            "auipc",
            Sem::Set(&Sem::Reg("rd"), &Sem::And(&Sem::Pc, &MASK)),
            "state differs",
        ),
        (
            "next PC32",
            "addi",
            Sem::Seq(&[
                &Sem::Set(&Sem::Reg("rd"), &ADDRESS),
                &Sem::SetPc(&Sem::And(&Sem::Add(&Sem::Pc, &Sem::Lit(4)), &MASK)),
            ]),
            "state differs",
        ),
    ];

    fn changed_table(name: &str, effect: &'static Sem) -> Vec<InsnDef> {
        assert_eq!(INSNS.iter().filter(|row| row.name == name).count(), 1);
        INSNS
            .iter()
            .map(|row| InsnDef {
                name: row.name,
                mask: row.mask,
                value: row.value,
                operands: row.operands,
                from: row.from,
                source: row.source,
                effect: if row.name == name { effect } else { row.effect },
                length: row.length,
                expansion: row.expansion,
            })
            .collect()
    }

    #[test]
    fn full_width_registers_and_canonical_user_addresses_hold() {
        assert_eq!(positive(), Ok(()));
        assert_eq!(negative(), Ok(()));
    }

    #[test]
    fn every_narrow_public_effect_is_detected_in_both_user_programs() {
        for (label, name, effect, reason) in &BAD_EFFECTS {
            let table = changed_table(name, effect);
            for case in [POSITIVE, NEGATIVE] {
                let error = check_case(&table, case).expect_err(label);
                assert!(
                    error.contains(case.name) && error.contains(reason),
                    "{label}: {error}"
                );
            }
        }
    }
}
