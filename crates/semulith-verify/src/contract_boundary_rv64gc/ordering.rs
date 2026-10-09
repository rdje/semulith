//! Independent conversations for one-hart data order and coherent instruction reads.

use semulith_core::env::{
    AccessWidth, BoundaryError, ContractViolation, Environment, Failure, Request, Response,
};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::outcome::ModelError;
use semulith_core::state_rv64gc::{
    ArchitecturalState, CSR_MCAUSE, CSR_MCYCLE, CSR_MEPC, CSR_MINSTRET, CSR_MTVAL,
};

use crate::fixtures::{FlatMemory, ScriptedEnv};

const ENTRY: u64 = 0x1000;
const DATA: u64 = 0x1040;
type Conversation = Vec<(Request, Result<Response, Failure>)>;

#[derive(Clone, Copy, PartialEq, Eq)]
enum Mode {
    Exact,
    DiscardStores,
    StaleParcels,
}

struct AuditedMemory {
    memory: FlatMemory,
    script: ScriptedEnv,
    cached: Vec<u8>,
    mode: Mode,
    audit_values: bool,
}

impl AuditedMemory {
    fn new(words: &[u32], script: Conversation, mode: Mode, audit_values: bool) -> Self {
        let mut memory = FlatMemory::with_fetch_align(ENTRY, 128, 2);
        for (i, word) in words.iter().enumerate() {
            memory.load_image(i * 4, &word.to_le_bytes());
        }
        let cached = memory.bytes().to_vec();
        Self {
            memory,
            script: ScriptedEnv::new(script),
            cached,
            mode,
            audit_values,
        }
    }
}

impl Environment for AuditedMemory {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        // ScriptedEnv owns exact request-order validation; expected response
        // values come from the independent literal conversation below.
        let expected = self.script.request(request)?;
        let arrived = match (self.mode, request) {
            (Mode::DiscardStores, Request::Store { .. }) => Response::StoreDone,
            (Mode::StaleParcels, Request::FetchParcel { addr }) => {
                let i = (addr - ENTRY) as usize;
                Response::FetchParcel(u16::from_le_bytes([self.cached[i], self.cached[i + 1]]))
            }
            _ => self.memory.request(request)?,
        };
        if self.audit_values {
            super::response_matches(request, expected, arrived)
        } else {
            Ok(arrived)
        }
    }
}

fn fetch(script: &mut Conversation, addr: u64, word: u32) {
    script.push((
        Request::FetchParcel { addr },
        Ok(Response::FetchParcel(word as u16)),
    ));
    script.push((
        Request::FetchParcel { addr: addr + 2 },
        Ok(Response::FetchParcel((word >> 16) as u16)),
    ));
}

fn steps(hart: &mut ArchitecturalState, env: &mut AuditedMemory, count: usize) -> StepRv64gc {
    for _ in 0..count {
        let outcome = exec_rv64gc::step(hart, env);
        if outcome != StepRv64gc::Executed {
            return outcome;
        }
    }
    StepRv64gc::Executed
}

fn data_order(
    aqrl: u32,
    mode: Mode,
    audit: bool,
    count: usize,
) -> (ArchitecturalState, AuditedMemory, StepRv64gc) {
    // SW x6,0(x5); LWU x7,0(x5); SB x8,1(x5); LWU x9,0(x5);
    // AMOADD.W x10,x11,(x5), with the four independently selected aq/rl bits.
    let words = [
        0x0062_a023,
        0x0002_e383,
        0x0082_80a3,
        0x0002_e483,
        0x00b2_a52f | aqrl,
    ];
    let data: [Vec<(Request, Response)>; 5] = [
        vec![(
            Request::Store {
                width: AccessWidth::W,
                addr: DATA,
                data: 0x1122_3344,
            },
            Response::StoreDone,
        )],
        vec![(
            Request::Load {
                width: AccessWidth::W,
                addr: DATA,
            },
            Response::Load(0x1122_3344),
        )],
        vec![(
            Request::Store {
                width: AccessWidth::B,
                addr: DATA + 1,
                data: 0xaa,
            },
            Response::StoreDone,
        )],
        vec![(
            Request::Load {
                width: AccessWidth::W,
                addr: DATA,
            },
            Response::Load(0x1122_aa44),
        )],
        vec![
            (
                Request::Load {
                    width: AccessWidth::W,
                    addr: DATA,
                },
                Response::Load(0x1122_aa44),
            ),
            (
                Request::Store {
                    width: AccessWidth::W,
                    addr: DATA,
                    data: 0x1122_aa45,
                },
                Response::StoreDone,
            ),
        ],
    ];
    let mut script = vec![];
    for (i, word) in words.iter().enumerate() {
        fetch(&mut script, ENTRY + 4 * i as u64, *word);
        script.extend(
            data[i]
                .iter()
                .map(|(request, response)| (*request, Ok(*response))),
        );
    }
    let mut env = AuditedMemory::new(&words, script, mode, audit);
    let mut hart = ArchitecturalState::zeroed_at(ENTRY);
    hart.write_x(5, DATA);
    hart.write_x(6, 0x1122_3344);
    hart.write_x(8, 0xaa);
    hart.write_x(11, 1);
    let outcome = steps(&mut hart, &mut env, count);
    (hart, env, outcome)
}

fn code_visibility(
    fence: bool,
    mode: Mode,
    audit: bool,
) -> (ArchitecturalState, AuditedMemory, StepRv64gc) {
    // Warm the old target once, rewind to the writer, then reach the rewritten
    // target by normal fallthrough, with and without a real FENCE.I instruction.
    let target = ENTRY + if fence { 8 } else { 4 };
    let old = 0x0010_0613; // ADDI x12,x0,1
    let new = 0x0070_0613; // ADDI x12,x0,7
    let store = 0x0062_a023; // SW x6,0(x5)
    let words = if fence {
        vec![store, 0x0000_100f, old]
    } else {
        vec![store, old]
    };
    let mut script = vec![];
    fetch(&mut script, target, old);
    fetch(&mut script, ENTRY, store);
    script.push((
        Request::Store {
            width: AccessWidth::W,
            addr: target,
            data: u64::from(new),
        },
        Ok(Response::StoreDone),
    ));
    if fence {
        fetch(&mut script, ENTRY + 4, 0x0000_100f);
    }
    fetch(&mut script, target, new);
    let mut env = AuditedMemory::new(&words, script, mode, audit);
    let mut hart = ArchitecturalState::zeroed_at(target);
    hart.write_x(5, target);
    hart.write_x(6, u64::from(new));
    let warm = steps(&mut hart, &mut env, 1);
    if warm != StepRv64gc::Executed || hart.read_x(12) != 1 {
        return (hart, env, warm);
    }
    hart.set_pc(ENTRY);
    let outcome = steps(&mut hart, &mut env, if fence { 3 } else { 2 });
    (hart, env, outcome)
}

pub(super) fn positive() -> Result<(), String> {
    for aqrl in [0, 1 << 25, 1 << 26, 3 << 25] {
        let (hart, env, outcome) = data_order(aqrl, Mode::Exact, true, 5);
        if outcome != StepRv64gc::Executed
            || env.script.remaining() != 0
            || hart.pc() != ENTRY + 20
            || hart.read_x(7) != 0x1122_3344
            || hart.read_x(9) != 0x1122_aa44
            || hart.read_x(10) != 0x1122_aa44
            || env.memory.bytes()[64..68] != [0x45, 0xaa, 0x22, 0x11]
            || env.memory.fetch_count() != 10
            || hart.read_csr(CSR_MCYCLE) != 5
            || hart.read_csr(CSR_MINSTRET) != 5
            || hart.read_csr(CSR_MCAUSE) != 0
        {
            return Err(format!("one-hart data/AMO order {aqrl:#x}: {outcome:?}"));
        }
    }
    for fence in [false, true] {
        let (hart, env, outcome) = code_visibility(fence, Mode::Exact, true);
        let count = if fence { 4 } else { 3 };
        if outcome != StepRv64gc::Executed
            || env.script.remaining() != 0
            || hart.read_x(12) != 7
            || env.memory.fetch_count() != count * 2
            || hart.read_csr(CSR_MCYCLE) != count
            || hart.read_csr(CSR_MINSTRET) != count
            || hart.read_csr(CSR_MCAUSE) != 0
        {
            return Err(format!(
                "coherent rewritten code, fence={fence}: {outcome:?}"
            ));
        }
    }
    Ok(())
}

fn discarded_store(audit: bool) -> Result<(), String> {
    // Stop at the first wrong load. Otherwise its bad value can alter the
    // later AMO store and trigger request-order validation independently.
    let (hart, _, outcome) = data_order(0, Mode::DiscardStores, audit, 2);
    let violation = ContractViolation::ResponseValueMismatch {
        request: Request::Load {
            width: AccessWidth::W,
            addr: DATA,
        },
        expected: Response::Load(0x1122_3344),
        arrived: Response::Load(0),
    };
    if outcome != StepRv64gc::Failed(ModelError::ContractViolation(violation))
        || hart.pc() != ENTRY + 4
        || hart.read_x(7) != 0
        || hart.read_csr(CSR_MCAUSE) != 0
        || hart.read_csr(CSR_MEPC) != 0
        || hart.read_csr(CSR_MTVAL) != 0
        || hart.read_csr(CSR_MINSTRET) != 1
    {
        return Err(format!("discarded acknowledged store escaped: {outcome:?}"));
    }
    Ok(())
}

fn stale_code(fence: bool, audit: bool) -> Result<(), String> {
    let target = ENTRY + if fence { 8 } else { 4 };
    let (hart, _, outcome) = code_visibility(fence, Mode::StaleParcels, audit);
    let violation = ContractViolation::ResponseValueMismatch {
        request: Request::FetchParcel { addr: target + 2 },
        expected: Response::FetchParcel(0x0070),
        arrived: Response::FetchParcel(0x0010),
    };
    if outcome != StepRv64gc::Failed(ModelError::ContractViolation(violation))
        || hart.pc() != target
        || hart.read_x(12) != 1
        || hart.read_csr(CSR_MCAUSE) != 0
        || hart.read_csr(CSR_MEPC) != 0
        || hart.read_csr(CSR_MTVAL) != 0
        || hart.read_csr(CSR_MINSTRET) != if fence { 3 } else { 2 }
    {
        return Err(format!("stale code escaped, fence={fence}: {outcome:?}"));
    }
    Ok(())
}

pub(super) fn negative() -> Result<(), String> {
    discarded_store(true)?;
    stale_code(false, true)?;
    stale_code(true, true)
}

#[cfg(test)]
mod tests {
    #[test]
    fn disabling_value_auditing_loses_all_ordering_violations() {
        let mut results = vec![super::discarded_store(false)];
        results.extend([false, true].map(|fence| super::stale_code(fence, false)));
        for result in results {
            let error = result.expect_err("negative fixture must discriminate");
            assert!(error.contains("Executed"), "{error}");
        }
    }
}
