//! Literal JALR target/link/request witnesses (RV32I 1.1.5.1; C 27.1).

use semulith_core::definition_rv64gc::{InsnDef, INSNS};
use semulith_core::env::{BoundaryError, Environment, Request, Response};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_MCAUSE, CSR_MCYCLE, CSR_MEPC, CSR_MINSTRET, CSR_MTVAL,
    CSR_MTVEC,
};

use crate::fixtures::FlatMemory;

const ENTRY: u64 = 0x1000;
const HANDLER: u64 = 0x1100;

#[derive(Clone, Copy)]
struct Case {
    name: &'static str,
    word: u32,
    rs: u8,
    base: u64,
    rd: u8,
    target: u64,
}

// Words and target values are literal specification-side observations, not
// values calculated from the processor's decoder or semantic table.
const POSITIVE: [Case; 3] = [
    Case {
        name: "even",
        word: 0x0003_02e7,
        rs: 6,
        base: 0x0000_0000_0000_1080,
        rd: 5,
        target: 0x0000_0000_0000_1080,
    },
    Case {
        name: "odd",
        word: 0x0003_02e7,
        rs: 6,
        base: 0x0000_0000_0000_1081,
        rd: 5,
        target: 0x0000_0000_0000_1080,
    },
    Case {
        name: "positive-limit",
        word: 0x7ff3_02e7,
        rs: 6,
        base: 0x0000_0000_0000_1080,
        rd: 5,
        target: 0x0000_0000_0000_187e,
    },
];

const NEGATIVE: [Case; 10] = [
    Case {
        name: "retain-bit1",
        word: 0x0003_02e7,
        rs: 6,
        base: 0x0000_0000_0000_1083,
        rd: 5,
        target: 0x0000_0000_0000_1082,
    },
    Case {
        name: "carry-before-mask",
        word: 0x0013_02e7,
        rs: 6,
        base: 0x0000_0000_0000_1081,
        rd: 5,
        target: 0x0000_0000_0000_1082,
    },
    Case {
        name: "odd-immediate",
        word: 0x0013_02e7,
        rs: 6,
        base: 0x0000_0000_0000_1080,
        rd: 5,
        target: 0x0000_0000_0000_1080,
    },
    Case {
        name: "negative-one",
        word: 0xfff3_02e7,
        rs: 6,
        base: 0x0000_0000_0000_1082,
        rd: 5,
        target: 0x0000_0000_0000_1080,
    },
    Case {
        name: "negative-limit",
        word: 0x8003_02e7,
        rs: 6,
        base: 0x0000_0000_0000_1881,
        rd: 5,
        target: 0x0000_0000_0000_1080,
    },
    Case {
        name: "wrap",
        word: 0x0033_02e7,
        rs: 6,
        base: 0xffff_ffff_ffff_ffff,
        rd: 5,
        target: 0x0000_0000_0000_0002,
    },
    Case {
        name: "high-bits",
        word: 0x0003_02e7,
        rs: 6,
        base: 0x0000_0001_0000_1083,
        rd: 5,
        target: 0x0000_0001_0000_1082,
    },
    Case {
        name: "alias",
        word: 0x0013_0367,
        rs: 6,
        base: 0x0000_0000_0000_1081,
        rd: 6,
        target: 0x0000_0000_0000_1082,
    },
    Case {
        name: "discard-link",
        word: 0x0003_0067,
        rs: 6,
        base: 0x0000_0000_0000_1083,
        rd: 0,
        target: 0x0000_0000_0000_1082,
    },
    Case {
        name: "zero-source",
        word: 0xfff0_02e7,
        rs: 0,
        base: 0x0000_0000_0000_0000,
        rd: 5,
        target: 0xffff_ffff_ffff_fffe,
    },
];

const FETCH_FAULTS: [Case; 2] = [
    Case {
        name: "fault-low",
        word: 0x0003_02e7,
        rs: 6,
        base: 0x0000_0000_0000_0003,
        rd: 5,
        target: 0x0000_0000_0000_0002,
    },
    Case {
        name: "fault-region",
        word: 0x0003_02e7,
        rs: 6,
        base: 0x0000_0000_4000_0003,
        rd: 5,
        target: 0x0000_0000_4000_0002,
    },
];

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

fn check_case(table: &[InsnDef], case: Case, fetch_fault: bool) -> Result<(), String> {
    let mut memory = FlatMemory::with_fetch_align(ENTRY, 0x200, 2);
    memory.load_image(0, &case.word.to_le_bytes());
    let before_memory = memory.bytes().to_vec();
    let mut observer = Observer {
        memory,
        requests: Vec::new(),
    };
    let mut hart = ArchitecturalState::zeroed_at(ENTRY);
    for reg in 1..32 {
        hart.write_x(reg, 0x100 + u64::from(reg));
    }
    hart.write_x(case.rs, case.base);
    hart.write_csr(CSR_MTVEC, HANDLER);
    let mut expected_x: [u64; 32] = std::array::from_fn(|r| hart.read_x(r as u8));
    if case.rd != 0 {
        expected_x[usize::from(case.rd)] = 0x1004;
    }
    let mut requests = vec![
        Request::FetchParcel { addr: 0x1000 },
        Request::FetchParcel { addr: 0x1002 },
    ];
    for boundary in 1..=if fetch_fault { 2 } else { 1 } {
        let fault = boundary == 2;
        if fault {
            requests.push(Request::FetchParcel { addr: case.target });
        }
        let outcome = exec_rv64gc::step_over(&mut hart, &mut observer, table);
        if observer.requests != requests {
            return Err(format!(
                "{} boundary {boundary}: requests differ: {:?}, required {requests:?}",
                case.name, observer.requests
            ));
        }
        let expected_pc = if fault { HANDLER } else { case.target };
        if hart.pc() != expected_pc {
            return Err(format!(
                "{} boundary {boundary}: target differs: {:#x}, required {expected_pc:#x}",
                case.name,
                hart.pc()
            ));
        }
        if outcome != StepRv64gc::Executed
            || hart.mode() != PrivilegeMode::M
            || hart.read_csr(CSR_MCAUSE) != u64::from(fault)
            || hart.read_csr(CSR_MEPC) != if fault { case.target } else { 0 }
            || hart.read_csr(CSR_MTVAL) != if fault { case.target } else { 0 }
            || hart.read_csr(CSR_MCYCLE) != boundary
            || hart.read_csr(CSR_MINSTRET) != 1
            // FlatMemory counts accepted fetches; the request log above also
            // includes the refused target parcel at the second boundary.
            || observer.memory.fetch_count() != 2
            || observer.memory.bytes() != before_memory
            || expected_x.iter().enumerate().any(|(r, value)| hart.read_x(r as u8) != *value)
        {
            return Err(format!(
                "{} boundary {boundary}: link/state differs: {outcome:?}",
                case.name
            ));
        }
    }
    Ok(())
}

pub(super) fn positive() -> Result<(), String> {
    for case in POSITIVE {
        check_case(INSNS, case, false)?;
    }
    Ok(())
}

pub(super) fn negative() -> Result<(), String> {
    for case in NEGATIVE {
        check_case(INSNS, case, false)?;
    }
    for case in FETCH_FAULTS {
        check_case(INSNS, case, true)?;
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use semulith_core::definition_rv64gc::Sem;

    const SUM: Sem = Sem::Add(&Sem::Reg("rs1"), &Sem::Sext(64, &Sem::Imm("imm12")));
    const TARGET: Sem = Sem::And(&SUM, &Sem::Lit(0xffff_ffff_ffff_fffe));
    const LINK: Sem = Sem::Set(&Sem::Reg("rd"), &Sem::Add(&Sem::Pc, &Sem::Lit(4)));
    static BAD_TARGETS: [(&str, Sem, Case); 6] = [
        (
            "bit1 erased",
            Sem::And(&SUM, &Sem::Lit(0xffff_ffff_ffff_fffc)),
            NEGATIVE[0],
        ),
        ("absent mask", SUM, POSITIVE[1]),
        (
            "source masked first",
            Sem::Add(
                &Sem::And(&Sem::Reg("rs1"), &Sem::Lit(0xffff_ffff_ffff_fffe)),
                &Sem::Sext(64, &Sem::Imm("imm12")),
            ),
            NEGATIVE[1],
        ),
        (
            "immediate masked first",
            Sem::Add(
                &Sem::Reg("rs1"),
                &Sem::And(
                    &Sem::Sext(64, &Sem::Imm("imm12")),
                    &Sem::Lit(0xffff_ffff_ffff_fffe),
                ),
            ),
            NEGATIVE[1],
        ),
        (
            "unsigned immediate",
            Sem::And(
                &Sem::Add(&Sem::Reg("rs1"), &Sem::Imm("imm12")),
                &Sem::Lit(0xffff_ffff_ffff_fffe),
            ),
            NEGATIVE[3],
        ),
        (
            "32-bit target",
            Sem::And(&SUM, &Sem::Lit(0xffff_fffe)),
            NEGATIVE[6],
        ),
    ];

    fn effect(target: &'static Sem, link_first: bool) -> &'static Sem {
        let pc: &'static Sem = Box::leak(Box::new(Sem::SetPc(target)));
        let sequence = if link_first { [&LINK, pc] } else { [pc, &LINK] };
        Box::leak(Box::new(Sem::Seq(Box::leak(Box::new(sequence)))))
    }

    fn changed_table(effect: &'static Sem) -> Vec<InsnDef> {
        assert_eq!(INSNS.iter().filter(|row| row.name == "jalr").count(), 1);
        INSNS
            .iter()
            .map(|row| InsnDef {
                name: row.name,
                mask: row.mask,
                value: row.value,
                operands: row.operands,
                from: row.from,
                source: row.source,
                effect: if row.name == "jalr" {
                    effect
                } else {
                    row.effect
                },
                length: row.length,
                expansion: row.expansion,
            })
            .collect()
    }

    #[test]
    fn all_literal_targets_links_and_next_fetch_faults_hold() {
        assert_eq!(positive(), Ok(()));
        assert_eq!(negative(), Ok(()));
    }

    #[test]
    fn wrong_jalr_effects_fail_named_observations_at_the_public_table_seam() {
        for (name, target, case) in &BAD_TARGETS {
            let table = changed_table(effect(target, false));
            let error = check_case(&table, *case, false).expect_err(name);
            assert!(
                error.contains(case.name) && error.contains("target differs"),
                "{name}: {error}"
            );
        }
        let table = changed_table(&Sem::Seq(&[
            &Sem::SetPc(&TARGET),
            &Sem::Set(&Sem::Reg("rd"), &Sem::Add(&Sem::Pc, &Sem::Lit(2))),
        ]));
        let error = check_case(&table, POSITIVE[0], false).expect_err("wrong link");
        assert!(
            error.contains("even") && error.contains("link/state differs"),
            "{error}"
        );
        // Reordering alone is equivalent: register reads use pre-state.
        let reordered = changed_table(effect(&TARGET, true));
        assert_eq!(check_case(&reordered, NEGATIVE[7], false), Ok(()));
        // Explicitly model the wrong use of the new pc+4 link as the aliased base.
        let table = changed_table(&Sem::Seq(&[
            &Sem::If(
                &Sem::Eq(&Sem::Field("rd"), &Sem::Field("rs1")),
                &Sem::SetPc(&Sem::And(
                    &Sem::Add(
                        &Sem::Add(&Sem::Pc, &Sem::Lit(4)),
                        &Sem::Sext(64, &Sem::Imm("imm12")),
                    ),
                    &Sem::Lit(0xffff_ffff_ffff_fffe),
                )),
                &Sem::SetPc(&TARGET),
            ),
            &LINK,
        ]));
        let error =
            check_case(&table, NEGATIVE[7], false).expect_err("new link used as aliased source");
        assert!(
            error.contains("alias") && error.contains("target differs"),
            "{error}"
        );
    }
}
