//! Literal Sv39 implicit-request witnesses (RVP-SUPERVISOR 11.1.3.2, Svade).

use semulith_core::env::{AccessWidth, BoundaryError, Environment, Failure, Request, Response};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_MCAUSE, CSR_MCYCLE, CSR_MEPC, CSR_MINSTRET, CSR_MSTATUS,
    CSR_MTVAL, CSR_MTVEC, CSR_SATP,
};

use crate::fixtures::FlatMemory;

const BASE: u64 = 0x8000_0000;
const CODE: u64 = 0x8000_1000;
const DATA: u64 = 0x8000_1080;
const HANDLER: u64 = BASE + 0x100;
const PAYLOAD: u64 = 0x0123_4567_89ab_cdef;
const STORES: [u64; 2] = [0x8877_6655_4433_2211, 0x1122_3344_5566_7788];

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Access {
    Fetch,
    Load,
    Store,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Fault {
    None,
    AccessedClear,
    DirtyClear,
    Invalid(usize),
    Denied(usize),
    Noncanonical,
}

#[derive(Clone, Copy, Debug)]
struct Case {
    access: Access,
    depth: usize,
    fault: Fault,
}

impl Case {
    const fn new(access: Access, depth: usize, fault: Fault) -> Self {
        Self {
            access,
            depth,
            fault,
        }
    }

    fn path(self) -> (&'static [u64], &'static [u64]) {
        // 1 GiB, 2 MiB and 4 KiB leaves map the declared VA to CODE/DATA.
        // Pointer PTEs have only V; leaves have V/R/W/X/A/D (U/G clear).
        match self.depth {
            1 => (&[0x8000_2000], &[0x2000_00cf]),
            2 => (&[0x8000_2000, 0x8000_3008], &[0x2000_0c01, 0x2000_00cf]),
            3 => (
                &[0x8000_2000, 0x8000_3008, 0x8000_4008],
                &[0x2000_0c01, 0x2000_1001, 0x2000_04cf],
            ),
            _ => unreachable!("finite literal walk depth"),
        }
    }
}

struct Observer {
    memory: FlatMemory,
    denied: Option<u64>,
    requests: Vec<Request>,
}

impl Environment for Observer {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        self.requests.push(request);
        if matches!(request, Request::WalkAccess { addr } if Some(addr) == self.denied) {
            return Err(Failure::AccessFault.into());
        }
        self.memory.request(request)
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct State {
    x: [u64; 32],
    pc: u64,
    mode: PrivilegeMode,
    status: u64,
    satp: u64,
    trap: (u64, u64, u64),
    cycles: u64,
    retired: u64,
    parcels: u64,
    executed: bool,
}

#[derive(Clone)]
struct Observation {
    requests: Vec<Request>,
    memory: Vec<u8>,
    state: State,
}

fn judge(actual: &Observation, expected: &Observation) -> Result<(), String> {
    if actual.requests != expected.requests {
        return Err(format!(
            "requests differ: {:?}, required {:?}",
            actual.requests, expected.requests
        ));
    }
    if actual.memory != expected.memory {
        return Err("memory differs (including PTE bytes)".into());
    }
    if actual.state != expected.state {
        return Err(format!(
            "state differs: {:?}, required {:?}",
            actual.state, expected.state
        ));
    }
    Ok(())
}

fn observations(case: Case) -> Vec<(Observation, Observation)> {
    let (path, values) = case.path();
    let mut values = values.to_vec();
    match case.fault {
        Fault::AccessedClear => values[case.depth - 1] &= !0x40,
        Fault::DirtyClear => values[case.depth - 1] &= !0x80,
        Fault::Invalid(n) => values[n - 1] = 0,
        _ => {}
    }
    let virtual_code = if case.depth == 1 { 0x1000 } else { 0x20_1000 };
    let virtual_data = if case.fault == Fault::Noncanonical {
        0x40_0000_0000
    } else {
        virtual_code + 0x80
    };
    let fetch = case.access == Access::Fetch;
    let entry = if fetch { virtual_code } else { BASE };
    let physical_code = if fetch { CODE } else { BASE };
    let words: [u32; 2] = match case.access {
        Access::Fetch => [0x0010_0393, 0x0020_0413], // ADDI x7,0,1; ADDI x8,0,2
        Access::Load => [0x0003_3383, 0x0003_3403],  // LD x7,0(x6); LD x8,0(x6)
        Access::Store => [0x0073_3023, 0x0083_3423], // SD x7,0(x6); SD x8,8(x6)
    };
    let mut memory = FlatMemory::with_fetch_align(BASE, 0x10000, 2);
    for (i, word) in words.iter().enumerate() {
        memory.load_image((physical_code - BASE) as usize + i * 4, &word.to_le_bytes());
    }
    for (addr, value) in path.iter().zip(values) {
        memory.load_image((addr - BASE) as usize, &value.to_le_bytes());
    }
    memory.load_image((DATA - BASE) as usize, &PAYLOAD.to_le_bytes());
    let mut expected_memory = memory.bytes().to_vec();
    let mut observer = Observer {
        memory,
        denied: if let Fault::Denied(n) = case.fault {
            Some(path[n - 1])
        } else {
            None
        },
        requests: Vec::new(),
    };
    let mut hart = ArchitecturalState::zeroed_at(entry);
    let initial_mode = if fetch {
        PrivilegeMode::S
    } else {
        PrivilegeMode::M
    };
    let initial_status = if fetch { 0xa_0000_0000 } else { 0xa_0002_0800 };
    hart.set_mode(initial_mode);
    hart.write_csr(CSR_SATP, 0x8000_0000_0008_0002);
    hart.write_csr(CSR_MTVEC, HANDLER);
    hart.write_csr(CSR_MSTATUS, initial_status);
    let mut x = [0; 32];
    for (r, value) in x.iter_mut().enumerate().skip(1) {
        *value = 0x0123_4567_0000_0000 + r as u64;
    }
    x[6] = virtual_data;
    if case.access == Access::Store {
        x[7..9].copy_from_slice(&STORES);
    }
    for (r, value) in x.iter().enumerate() {
        hart.write_x(r as u8, *value);
    }
    let success = case.fault == Fault::None;
    let boundaries = if success { 2 } else { 1 };
    let walk_length = match case.fault {
        Fault::Noncanonical => 0,
        Fault::Invalid(n) | Fault::Denied(n) => n,
        _ => case.depth,
    };
    let mut requests = Vec::new();
    let mut pairs = Vec::new();
    for i in 0..boundaries {
        let parcels = [
            Request::FetchParcel {
                addr: physical_code + 4 * i,
            },
            Request::FetchParcel {
                addr: physical_code + 4 * i + 2,
            },
        ];
        if !fetch {
            requests.extend(parcels);
        }
        if i == 0 {
            requests.extend(
                path[..walk_length]
                    .iter()
                    .map(|addr| Request::WalkAccess { addr: *addr }),
            );
        }
        if success {
            if fetch {
                requests.extend(parcels);
            }
            match case.access {
                Access::Fetch => x[7 + i as usize] = i + 1,
                Access::Load => {
                    x[7 + i as usize] = PAYLOAD;
                    requests.push(Request::Load {
                        width: AccessWidth::D,
                        addr: DATA,
                    });
                }
                Access::Store => {
                    let value = STORES[i as usize];
                    requests.push(Request::Store {
                        width: AccessWidth::D,
                        addr: DATA + i * 8,
                        data: value,
                    });
                    let offset = (DATA - BASE + i * 8) as usize;
                    expected_memory[offset..offset + 8].copy_from_slice(&value.to_le_bytes());
                }
            }
        }
        let cause = if matches!(case.fault, Fault::Denied(_)) {
            5
        } else {
            match case.access {
                Access::Fetch => 12,
                Access::Load => 13,
                Access::Store => 15,
            }
        };
        let expected = Observation {
            requests: requests.clone(),
            memory: expected_memory.clone(),
            state: State {
                x,
                pc: if success {
                    entry + 4 * (i + 1)
                } else {
                    HANDLER
                },
                mode: if success {
                    initial_mode
                } else {
                    PrivilegeMode::M
                },
                status: if success {
                    initial_status
                } else if fetch {
                    0xa_0000_0800
                } else {
                    0xa_0002_1800
                },
                satp: 0x8000_0000_0008_0002,
                trap: if success {
                    (0, 0, 0)
                } else {
                    (cause, entry, if fetch { entry } else { virtual_data })
                },
                cycles: i + 1,
                retired: if success { i + 1 } else { 0 },
                parcels: if fetch && !success { 0 } else { 2 * (i + 1) },
                executed: true,
            },
        };
        let outcome = exec_rv64gc::step(&mut hart, &mut observer);
        let actual = Observation {
            requests: observer.requests.clone(),
            memory: observer.memory.bytes().to_vec(),
            state: State {
                x: std::array::from_fn(|r| hart.read_x(r as u8)),
                pc: hart.pc(),
                mode: hart.mode(),
                status: hart.read_csr(CSR_MSTATUS),
                satp: hart.read_csr(CSR_SATP),
                trap: (
                    hart.read_csr(CSR_MCAUSE),
                    hart.read_csr(CSR_MEPC),
                    hart.read_csr(CSR_MTVAL),
                ),
                cycles: hart.read_csr(CSR_MCYCLE),
                retired: hart.read_csr(CSR_MINSTRET),
                parcels: observer.memory.fetch_count(),
                executed: outcome == StepRv64gc::Executed,
            },
        };
        pairs.push((actual, expected));
    }
    pairs
}

fn check(case: Case) -> Result<(), String> {
    for (i, (actual, expected)) in observations(case).iter().enumerate() {
        judge(actual, expected).map_err(|error| format!("{case:?} boundary {}: {error}", i + 1))?;
    }
    Ok(())
}

pub(super) fn positive() -> Result<(), String> {
    for depth in 1..=3 {
        for access in [Access::Fetch, Access::Load, Access::Store] {
            check(Case::new(access, depth, Fault::None))?;
        }
    }
    Ok(())
}

pub(super) fn negative() -> Result<(), String> {
    for access in [Access::Fetch, Access::Load, Access::Store] {
        check(Case::new(access, 3, Fault::AccessedClear))?;
    }
    check(Case::new(Access::Store, 3, Fault::DirtyClear))?;
    for n in 1..=3 {
        check(Case::new(Access::Fetch, 3, Fault::Invalid(n)))?;
        check(Case::new(Access::Load, 3, Fault::Denied(n)))?;
    }
    check(Case::new(Access::Load, 3, Fault::Noncanonical))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn literal_walk_paths_hits_and_fault_termination_hold() {
        assert_eq!(positive(), Ok(()));
        assert_eq!(negative(), Ok(()));
    }

    #[test]
    fn request_and_pte_observers_reject_corrupted_captures() {
        let (actual, expected) = observations(Case::new(Access::Load, 3, Fault::None)).remove(0);
        assert_eq!(judge(&actual, &expected), Ok(()));
        let index = actual
            .requests
            .iter()
            .position(|r| matches!(r, Request::WalkAccess { .. }))
            .unwrap();
        let addr = 0x8000_2000;
        let mut controls = Vec::new();
        let mut changed = actual.clone();
        changed.requests[index] = Request::Load {
            width: AccessWidth::D,
            addr,
        };
        controls.push(("walk disguised as data load", changed));
        let mut changed = actual.clone();
        changed.requests.remove(index);
        controls.push(("missing walk", changed));
        let mut changed = actual.clone();
        changed.requests.insert(index, Request::WalkAccess { addr });
        controls.push(("fourth walk", changed));
        let mut changed = actual.clone();
        changed.requests[index] = Request::WalkAccess { addr: addr + 8 };
        controls.push(("wrong PTE address", changed));
        let mut changed = actual.clone();
        changed.requests[index] = Request::Store {
            width: AccessWidth::D,
            addr,
            data: 0x2000_0c01,
        };
        controls.push(("implicit PTE write", changed));
        let mut changed = actual.clone();
        changed.requests[0] = Request::Load {
            width: AccessWidth::H,
            addr: BASE,
        };
        controls.push(("fetch disguised as data load", changed));
        for (name, changed) in controls {
            assert!(judge(&changed, &expected)
                .expect_err(name)
                .contains("requests differ"));
        }
        let (mut actual, expected) =
            observations(Case::new(Access::Load, 3, Fault::AccessedClear)).remove(0);
        actual.memory[0x4008] |= 0x40;
        assert!(judge(&actual, &expected)
            .expect_err("PTE A changed")
            .contains("memory differs"));
    }
}
