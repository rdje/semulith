//! Literal instruction/request witnesses for OB-LOAD-X0 (RV32I 1.1.6).

use semulith_core::definition_rv64gc::{InsnDef, INSNS};
use semulith_core::env::{AccessWidth, BoundaryError, Environment, Failure, Request, Response};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_MCAUSE, CSR_MCYCLE, CSR_MEPC, CSR_MINSTRET, CSR_MSTATUS,
    CSR_MTVAL, CSR_MTVEC, CSR_SATP,
};

use crate::fixtures::FlatMemory;

const ENTRY: u64 = 0x1000;
const DATA: u64 = 0x1080;
const HANDLER: u64 = 0x1100;
const ROOT: u64 = 0x2000;

// Literal encodings of each load into x0, with address in x5 and immediate zero.
const LOADS: [(&str, AccessWidth, u32); 7] = [
    ("lb", AccessWidth::B, 0x0002_8003),
    ("lh", AccessWidth::H, 0x0002_9003),
    ("lw", AccessWidth::W, 0x0002_a003),
    ("lbu", AccessWidth::B, 0x0002_c003),
    ("lhu", AccessWidth::H, 0x0002_d003),
    ("lwu", AccessWidth::W, 0x0002_e003),
    ("ld", AccessWidth::D, 0x0002_b003),
];

#[derive(Clone, Copy, Debug)]
enum Case {
    Success,
    AccessFault,
    Misaligned,
    PageFault,
}

/// Observe the actual CPU boundary; the log is harness instrumentation,
/// not a side-effecting memory region or another instruction implementation.
struct Observer {
    memory: FlatMemory,
    requests: Vec<Request>,
    deny_load: bool,
}

impl Environment for Observer {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        if !matches!(request, Request::Fetch { .. } | Request::FetchParcel { .. }) {
            self.requests.push(request);
        }
        if self.deny_load && matches!(request, Request::Load { .. }) {
            return Err(Failure::AccessFault.into());
        }
        self.memory.request(request)
    }
}

fn check_case(
    table: &[InsnDef],
    name: &str,
    width: AccessWidth,
    word: u32,
    case: Case,
    deny_load: bool,
) -> Result<(), String> {
    let mut memory = FlatMemory::with_fetch_align(ENTRY, 0x2000, 2);
    memory.load_image(0, &word.to_le_bytes());
    memory.load_image(0x80, &[0x88; 8]);
    let before_memory = memory.bytes().to_vec();
    let mut observer = Observer {
        memory,
        requests: Vec::new(),
        deny_load,
    };
    let mut hart = ArchitecturalState::zeroed_at(ENTRY);
    for reg in 1..32 {
        hart.write_x(reg, 0x100 + u64::from(reg));
    }
    let address = if matches!(case, Case::Misaligned) {
        DATA + 1
    } else {
        DATA
    };
    hart.write_x(5, address);
    hart.write_csr(CSR_MTVEC, HANDLER);
    if matches!(case, Case::PageFault) {
        // M fetch stays bare; MPRV/MPP=S translates the data access. The root
        // page at 0x2000 is explicitly zero, so its first PTE is invalid.
        let status = (hart.read_csr(CSR_MSTATUS) & !(3 << 11)) | (1 << 11) | (1 << 17);
        hart.write_csr(CSR_MSTATUS, status);
        hart.write_csr(CSR_SATP, (8 << 60) | 2);
    }
    let before_x: [u64; 32] = std::array::from_fn(|r| hart.read_x(r as u8));
    let (cause, requests) = match case {
        Case::Success => (0, vec![Request::Load { width, addr: DATA }]),
        Case::AccessFault => (5, vec![Request::Load { width, addr: DATA }]),
        Case::Misaligned => (4, vec![]),
        Case::PageFault => (13, vec![Request::WalkAccess { addr: ROOT }]),
    };
    let outcome = exec_rv64gc::step_over(&mut hart, &mut observer, table);
    if observer.requests != requests {
        return Err(format!(
            "{name} {case:?}: x0 load requests differ: {:?}, required {requests:?}",
            observer.requests
        ));
    }
    let success = matches!(case, Case::Success);
    if outcome != StepRv64gc::Executed
        || hart.pc() != if success { ENTRY + 4 } else { HANDLER }
        || hart.mode() != PrivilegeMode::M
        || hart.read_csr(CSR_MCAUSE) != cause
        || hart.read_csr(CSR_MEPC) != if success { 0 } else { ENTRY }
        || hart.read_csr(CSR_MTVAL) != if success { 0 } else { address }
        || hart.read_csr(CSR_MCYCLE) != 1
        || hart.read_csr(CSR_MINSTRET) != u64::from(success)
        || observer.memory.fetch_count() != 2
        || observer.memory.bytes() != before_memory
        || before_x
            .iter()
            .enumerate()
            .any(|(r, value)| hart.read_x(r as u8) != *value)
    {
        return Err(format!(
            "{name} {case:?}: x0 load state differs: {outcome:?}"
        ));
    }
    Ok(())
}

fn positive_over(table: &[InsnDef]) -> Result<(), String> {
    for (name, width, word) in LOADS {
        check_case(table, name, width, word, Case::Success, false)?;
    }
    Ok(())
}

fn negative_over(table: &[InsnDef], deny_load: bool) -> Result<(), String> {
    for (name, width, word) in LOADS {
        check_case(table, name, width, word, Case::AccessFault, deny_load)?;
        if width != AccessWidth::B {
            check_case(table, name, width, word, Case::Misaligned, false)?;
        }
        check_case(table, name, width, word, Case::PageFault, false)?;
    }
    Ok(())
}

pub(super) fn positive() -> Result<(), String> {
    positive_over(INSNS)
}

pub(super) fn negative() -> Result<(), String> {
    negative_over(INSNS, true)
}

#[cfg(test)]
mod tests {
    use super::*;
    use semulith_core::definition_rv64gc::Sem;

    fn changed_table(name: &str, effect: &'static Sem) -> Vec<InsnDef> {
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
    fn all_x0_load_requests_and_faults_hold() {
        assert_eq!(positive(), Ok(()));
        assert_eq!(negative(), Ok(()));
    }

    #[test]
    fn each_erased_or_duplicated_load_is_detected_at_the_public_table_seam() {
        for (name, width, word) in LOADS {
            let erased = changed_table(name, &Sem::Nop);
            let error = positive_over(&erased).expect_err("an erased x0 load must fail");
            assert!(error.contains(name) && error.contains("requests differ"));
            for case in [Case::AccessFault, Case::Misaligned, Case::PageFault] {
                if matches!(case, Case::Misaligned) && width == AccessWidth::B {
                    continue;
                }
                let error = check_case(&erased, name, width, word, case, true)
                    .expect_err("erasing any x0 load fault must fail");
                assert!(error.contains(name), "{error}");
            }

            let row = INSNS.iter().find(|row| row.name == name).unwrap();
            let twice = Box::leak(Box::new([row.effect, row.effect]));
            let effect = Box::leak(Box::new(Sem::Seq(twice)));
            let duplicated = changed_table(name, effect);
            let error = positive_over(&duplicated).expect_err("two accesses must fail");
            assert!(error.contains(name) && error.contains("requests differ"));
        }
    }

    #[test]
    fn disabling_load_fault_injection_is_detected() {
        let error = negative_over(INSNS, false).expect_err("a missing fault must fail");
        assert!(error.contains("lb") && error.contains("state differs"));
    }
}
