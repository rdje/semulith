//! Finite one-hart A-extension execution witnesses (RVI-A 12.1.2/12.1.4).
//! Literal arithmetic vectors and independently authored expectations precede CPU
//! execution. A Load/Store request pair does not prove multicore indivisibility.

use semulith_core::definition_rv64gc::{InsnDef, INSNS};
use semulith_core::env::{AccessWidth, BoundaryError, Environment, Failure, Request, Response};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::privilege::PrivilegedHart;
use semulith_core::reservation::Reservation;
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_COUNT, CSR_FFLAGS, CSR_FRM, CSR_MCAUSE, CSR_MCYCLE,
    CSR_MEPC, CSR_MINSTRET, CSR_MSCRATCH, CSR_MSTATUS, CSR_MTVAL, CSR_MTVEC, CSR_SATP,
    CSR_SSCRATCH,
};
use semulith_core::translation::{Tlb, TlbEntry};
use semulith_core::wait::HartState;

use crate::fixtures::FlatMemory;

const ENTRY: u64 = 0x1000;
const DATA: u64 = 0x1080;
const VA: u64 = 0x10000;
const PA: u64 = 0x5000;
const MODES: [PrivilegeMode; 3] = [PrivilegeMode::M, PrivilegeMode::S, PrivilegeMode::U];
// RVI-A 12.1.4: ADD, SWAP, XOR, AND, OR, signed MIN/MAX, unsigned MIN/MAX.
const FUNCTIONS: [u32; 9] = [0, 1, 4, 12, 8, 16, 20, 24, 28];

mod permissions;
mod reservation;

struct Vector {
    old: u64,
    source: u64,
    // Literal low-width results in FUNCTIONS order; W then D.
    new: [[u64; 9]; 2],
}
const VECTORS: [Vector; 10] = [
    Vector {
        old: 0x0000000000000000,
        source: 0x0000000000000000,
        new: [
            [
                0x0000000000000000,
                0x0000000000000000,
                0x0000000000000000,
                0x0000000000000000,
                0x0000000000000000,
                0x0000000000000000,
                0x0000000000000000,
                0x0000000000000000,
                0x0000000000000000,
            ],
            [
                0x0000000000000000,
                0x0000000000000000,
                0x0000000000000000,
                0x0000000000000000,
                0x0000000000000000,
                0x0000000000000000,
                0x0000000000000000,
                0x0000000000000000,
                0x0000000000000000,
            ],
        ],
    },
    Vector {
        old: 0xffffffffffffffff,
        source: 0x0000000000000001,
        new: [
            [
                0x0000000000000000,
                0x0000000000000001,
                0x00000000fffffffe,
                0x0000000000000001,
                0x00000000ffffffff,
                0x00000000ffffffff,
                0x0000000000000001,
                0x0000000000000001,
                0x00000000ffffffff,
            ],
            [
                0x0000000000000000,
                0x0000000000000001,
                0xfffffffffffffffe,
                0x0000000000000001,
                0xffffffffffffffff,
                0xffffffffffffffff,
                0x0000000000000001,
                0x0000000000000001,
                0xffffffffffffffff,
            ],
        ],
    },
    Vector {
        old: 0x1122334480000000,
        source: 0x998877667fffffff,
        new: [
            [
                0x00000000ffffffff,
                0x000000007fffffff,
                0x00000000ffffffff,
                0x0000000000000000,
                0x00000000ffffffff,
                0x0000000080000000,
                0x000000007fffffff,
                0x000000007fffffff,
                0x0000000080000000,
            ],
            [
                0xaaaaaaaaffffffff,
                0x998877667fffffff,
                0x88aa4422ffffffff,
                0x1100334400000000,
                0x99aa7766ffffffff,
                0x998877667fffffff,
                0x1122334480000000,
                0x1122334480000000,
                0x998877667fffffff,
            ],
        ],
    },
    Vector {
        old: 0x7fffffffffffffff,
        source: 0x8000000000000000,
        new: [
            [
                0x00000000ffffffff,
                0x0000000000000000,
                0x00000000ffffffff,
                0x0000000000000000,
                0x00000000ffffffff,
                0x00000000ffffffff,
                0x0000000000000000,
                0x0000000000000000,
                0x00000000ffffffff,
            ],
            [
                0xffffffffffffffff,
                0x8000000000000000,
                0xffffffffffffffff,
                0x0000000000000000,
                0xffffffffffffffff,
                0x8000000000000000,
                0x7fffffffffffffff,
                0x7fffffffffffffff,
                0x8000000000000000,
            ],
        ],
    },
    Vector {
        old: 0x8000000000000000,
        source: 0xffffffffffffffff,
        new: [
            [
                0x00000000ffffffff,
                0x00000000ffffffff,
                0x00000000ffffffff,
                0x0000000000000000,
                0x00000000ffffffff,
                0x00000000ffffffff,
                0x0000000000000000,
                0x0000000000000000,
                0x00000000ffffffff,
            ],
            [
                0x7fffffffffffffff,
                0xffffffffffffffff,
                0x7fffffffffffffff,
                0x8000000000000000,
                0xffffffffffffffff,
                0x8000000000000000,
                0xffffffffffffffff,
                0x8000000000000000,
                0xffffffffffffffff,
            ],
        ],
    },
    Vector {
        old: 0x0123456789abcdef,
        source: 0xfedcba9876543210,
        new: [
            [
                0x00000000ffffffff,
                0x0000000076543210,
                0x00000000ffffffff,
                0x0000000000000000,
                0x00000000ffffffff,
                0x0000000089abcdef,
                0x0000000076543210,
                0x0000000076543210,
                0x0000000089abcdef,
            ],
            [
                0xffffffffffffffff,
                0xfedcba9876543210,
                0xffffffffffffffff,
                0x0000000000000000,
                0xffffffffffffffff,
                0xfedcba9876543210,
                0x0123456789abcdef,
                0x0123456789abcdef,
                0xfedcba9876543210,
            ],
        ],
    },
    Vector {
        old: 0xa5a5a5a55a5a5a5a,
        source: 0x5a5a5a5aa5a5a5a5,
        new: [
            [
                0x00000000ffffffff,
                0x00000000a5a5a5a5,
                0x00000000ffffffff,
                0x0000000000000000,
                0x00000000ffffffff,
                0x00000000a5a5a5a5,
                0x000000005a5a5a5a,
                0x000000005a5a5a5a,
                0x00000000a5a5a5a5,
            ],
            [
                0xffffffffffffffff,
                0x5a5a5a5aa5a5a5a5,
                0xffffffffffffffff,
                0x0000000000000000,
                0xffffffffffffffff,
                0xa5a5a5a55a5a5a5a,
                0x5a5a5a5aa5a5a5a5,
                0x5a5a5a5aa5a5a5a5,
                0xa5a5a5a55a5a5a5a,
            ],
        ],
    },
    Vector {
        old: 0x1122334480000001,
        source: 0x8877665544332211,
        new: [
            [
                0x00000000c4332212,
                0x0000000044332211,
                0x00000000c4332210,
                0x0000000000000001,
                0x00000000c4332211,
                0x0000000080000001,
                0x0000000044332211,
                0x0000000044332211,
                0x0000000080000001,
            ],
            [
                0x99999999c4332212,
                0x8877665544332211,
                0x99555511c4332210,
                0x0022224400000001,
                0x99777755c4332211,
                0x8877665544332211,
                0x1122334480000001,
                0x1122334480000001,
                0x8877665544332211,
            ],
        ],
    },
    Vector {
        old: 0x1122334480000001,
        source: 0x0000000000001080,
        new: [
            [
                0x0000000080001081,
                0x0000000000001080,
                0x0000000080001081,
                0x0000000000000000,
                0x0000000080001081,
                0x0000000080000001,
                0x0000000000001080,
                0x0000000000001080,
                0x0000000080000001,
            ],
            [
                0x1122334480001081,
                0x0000000000001080,
                0x1122334480001081,
                0x0000000000000000,
                0x1122334480001081,
                0x0000000000001080,
                0x1122334480000001,
                0x0000000000001080,
                0x1122334480000001,
            ],
        ],
    },
    Vector {
        old: 0x1122334480000001,
        source: 0x0000000000000000,
        new: [
            [
                0x0000000080000001,
                0x0000000000000000,
                0x0000000080000001,
                0x0000000000000000,
                0x0000000080000001,
                0x0000000080000001,
                0x0000000000000000,
                0x0000000000000000,
                0x0000000080000001,
            ],
            [
                0x1122334480000001,
                0x0000000000000000,
                0x1122334480000001,
                0x0000000000000000,
                0x1122334480000001,
                0x0000000000000000,
                0x1122334480000001,
                0x0000000000000000,
                0x1122334480000001,
            ],
        ],
    },
];

struct Observer {
    memory: FlatMemory,
    requests: Vec<Request>,
    fail: Option<Request>,
}

impl Environment for Observer {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        self.requests.push(request);
        if self.fail == Some(request) {
            return Err(BoundaryError::Target(Failure::AccessFault));
        }
        self.memory.request(request)
    }
}

#[derive(Clone)]
struct Observation {
    x: [u64; 32],
    f: [u64; 32],
    csrs: [u64; CSR_COUNT],
    reservation: Reservation,
    tlb: Tlb,
    wait: HartState,
    pc: u64,
    mode: PrivilegeMode,
    memory: Vec<u8>,
    requests: Vec<Request>,
    parcels: u64,
    executed: bool,
}

impl Observation {
    fn capture(hart: &mut ArchitecturalState, observer: &Observer, executed: bool) -> Self {
        Self {
            x: std::array::from_fn(|r| hart.read_x(r as u8)),
            f: std::array::from_fn(|r| hart.read_f(r as u8)),
            csrs: std::array::from_fn(|i| hart.read_csr(i)),
            reservation: *hart.reservation(),
            tlb: hart.tlb().clone(),
            wait: *hart.hart_state(),
            pc: hart.pc(),
            mode: hart.mode(),
            memory: observer.memory.bytes().to_vec(),
            requests: observer.requests.clone(),
            parcels: observer.memory.fetch_count(),
            executed,
        }
    }
}

fn judge(actual: &Observation, expected: &Observation) -> Result<(), String> {
    if actual.requests != expected.requests {
        return Err("requests differ".into());
    }
    if actual.memory != expected.memory {
        return Err("memory differs".into());
    }
    if actual.x != expected.x {
        return Err("integer registers differ".into());
    }
    if actual.f != expected.f {
        return Err("floating registers differ".into());
    }
    if actual.csrs != expected.csrs {
        return Err("CSR owners differ".into());
    }
    if actual.reservation != expected.reservation {
        return Err("reservation differs".into());
    }
    if actual.tlb != expected.tlb {
        return Err("TLB/cursor differs".into());
    }
    if actual.wait != expected.wait {
        return Err("wait state differs".into());
    }
    if actual.pc != expected.pc || actual.mode != expected.mode {
        return Err("PC/mode differs".into());
    }
    if actual.parcels != expected.parcels || actual.executed != expected.executed {
        return Err("boundary outcome/parcels differ".into());
    }
    Ok(())
}

struct Fixture {
    hart: ArchitecturalState,
    observer: Observer,
    expected: Observation,
}

impl Fixture {
    fn new(word: u32, mode: PrivilegeMode, vector: &Vector, address: u64) -> Self {
        let mut memory = FlatMemory::with_fetch_align(ENTRY, 0x5000, 2);
        memory.load_image(0, &word.to_le_bytes());
        memory.load_image(0x80, &vector.old.to_le_bytes());
        let mut hart = ArchitecturalState::zeroed_at(ENTRY);
        hart.set_mode(mode);
        hart.write_csr(CSR_MSTATUS, 0xa_0000_6008);
        hart.write_csr(CSR_MTVEC, 0x1100);
        hart.write_csr(CSR_MSCRATCH, 0x1234_5678_9abc_def0);
        hart.write_csr(CSR_SSCRATCH, 0xfedc_ba98_7654_3210);
        hart.write_csr(CSR_MCAUSE, 0x55);
        hart.write_csr(CSR_MEPC, 0x1200);
        hart.write_csr(CSR_MTVAL, 0x0123_4567_89ab_cdef);
        hart.write_csr(CSR_FFLAGS, 0x15);
        hart.write_csr(CSR_FRM, 3);
        hart.write_csr(CSR_MCYCLE, 41);
        hart.write_csr(CSR_MINSTRET, 17);
        for r in 1..32 {
            hart.write_x(r, 0x1111_2222_0000_0000 + u64::from(r));
        }
        hart.write_x(6, address);
        hart.write_x(9, vector.source);
        for r in 0..32 {
            hart.write_f(r, 0x7ff8_0000_0000_1000 + u64::from(r));
        }
        hart.reservation().establish(DATA + 0x20, 8);
        // Bare mode preserves valid mappings and the nonzero FIFO cursor.
        for i in 0..5 {
            hart.tlb().install(TlbEntry {
                valid: true,
                global: i % 2 == 0,
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
        let observer = Observer {
            memory,
            requests: Vec::new(),
            fail: None,
        };
        let expected = Observation::capture(&mut hart, &observer, true);
        Self {
            hart,
            observer,
            expected,
        }
    }

    fn fetch(&mut self) {
        self.expected.requests.extend([
            Request::FetchParcel { addr: ENTRY },
            Request::FetchParcel { addr: ENTRY + 2 },
        ]);
        self.expected.parcels = 2;
        self.expected.csrs[CSR_MCYCLE] = 42;
    }

    fn retire(&mut self, rd: u32, result: u64) {
        self.expected.pc = ENTRY + 4;
        self.expected.csrs[CSR_MINSTRET] = 18;
        if rd != 0 {
            self.expected.x[rd as usize] = result;
        }
    }

    fn store(&mut self, width: AccessWidth, address: u64, data: u64) {
        self.expected.requests.push(Request::Store {
            width,
            addr: address,
            data,
        });
        let start = (address - ENTRY) as usize;
        let n = width.bytes() as usize;
        self.expected.memory[start..start + n].copy_from_slice(&data.to_le_bytes()[..n]);
    }

    fn trap(&mut self, cause: u64, address: u64) {
        self.expected.pc = 0x1100;
        self.expected.mode = PrivilegeMode::M;
        self.expected.csrs[CSR_MSTATUS] = 0xa_0002_7880;
        self.expected.csrs[CSR_MCAUSE] = cause;
        self.expected.csrs[CSR_MEPC] = ENTRY;
        self.expected.csrs[CSR_MTVAL] = address;
    }

    fn observe(&mut self, table: &[InsnDef]) -> Observation {
        let outcome = exec_rv64gc::step_over(&mut self.hart, &mut self.observer, table);
        Observation::capture(
            &mut self.hart,
            &self.observer,
            outcome == StepRv64gc::Executed,
        )
    }

    fn check(&mut self, table: &[InsnDef]) -> Result<(), String> {
        judge(&self.observe(table), &self.expected)
    }
}

fn word(function: u32, n: u32, ordering: u32, rd: u32, rs2: u32) -> u32 {
    (function << 27)
        | (ordering << 25)
        | (rs2 << 20)
        | (6 << 15)
        | ((if n == 4 { 2 } else { 3 }) << 12)
        | (rd << 7)
        | 0x2f
}

fn width(n: u32) -> AccessWidth {
    if n == 4 {
        AccessWidth::W
    } else {
        AccessWidth::D
    }
}
fn old_value(vector: &Vector, n: u32) -> u64 {
    if n == 4 {
        u64::from(vector.old as u32).wrapping_add(if vector.old & 0x8000_0000 != 0 {
            0xffff_ffff_0000_0000
        } else {
            0
        })
    } else {
        vector.old
    }
}

fn ordinary(
    function: u32,
    n: u32,
    order: u32,
    rd: u32,
    mode: PrivilegeMode,
    vector_index: usize,
    success: bool,
) -> Fixture {
    let vector = &VECTORS[vector_index];
    let rs2 = if function == 2 || vector_index == 9 {
        0
    } else if vector_index == 8 {
        6
    } else {
        9
    };
    let mut f = Fixture::new(word(function, n, order, rd, rs2), mode, vector, DATA);
    if function == 3 && success {
        f.hart.reservation().establish(DATA, n as u8);
    }
    f.expected = Observation::capture(&mut f.hart, &f.observer, true);
    f.fetch();
    if function == 2 {
        f.expected.requests.push(Request::Load {
            width: width(n),
            addr: DATA,
        });
        f.expected.reservation.establish(DATA, n as u8);
        f.retire(rd, old_value(vector, n));
    } else if function == 3 {
        if success {
            f.store(
                width(n),
                DATA,
                if n == 4 {
                    vector.source & 0xffff_ffff
                } else {
                    vector.source
                },
            );
        } else {
            f.expected.requests.push(Request::StorePermission {
                width: width(n),
                addr: DATA,
            });
        }
        f.expected.reservation.clear();
        f.retire(rd, u64::from(!success));
    } else {
        let operation = FUNCTIONS
            .iter()
            .position(|v| *v == function)
            .expect("closed nine");
        f.expected.requests.push(Request::Load {
            width: width(n),
            addr: DATA,
        });
        f.store(width(n), DATA, vector.new[usize::from(n == 8)][operation]);
        f.retire(rd, old_value(vector, n));
    }
    f
}

// M-mode fetch is Bare; MPRV/MPP=S translates only this instruction's data.
// Three literal page-table reads, no implicit stores under Svade.
fn translated(function: u32, n: u32, order: u32, leaf_flags: u64, fail: u8) -> Fixture {
    let vector = &VECTORS[7];
    let mut f = Fixture::new(word(function, n, order, 7, 9), PrivilegeMode::M, vector, VA);
    f.hart.write_csr(CSR_MSTATUS, 0xa_0002_6808);
    f.hart.write_csr(CSR_SATP, 0x8000_0000_0000_0002);
    *f.hart.tlb() = Tlb::new();
    for (address, data) in [
        (0x2000_u64, 0xc01_u64),
        (0x3000, 0x1001),
        (0x4080, 0x1400 | leaf_flags),
        (PA, vector.old),
    ] {
        f.observer
            .memory
            .load_image((address - ENTRY) as usize, &data.to_le_bytes());
    }
    let load = Request::Load {
        width: width(n),
        addr: PA,
    };
    let operation = FUNCTIONS
        .iter()
        .position(|v| *v == function)
        .expect("closed nine");
    let new = vector.new[usize::from(n == 8)][operation];
    let store = Request::Store {
        width: width(n),
        addr: PA,
        data: new,
    };
    f.observer.fail = match fail {
        1 => Some(load),
        2 => Some(store),
        _ => None,
    };
    f.expected = Observation::capture(&mut f.hart, &f.observer, true);
    f.fetch();
    for address in [0x2000, 0x3000, 0x4080] {
        f.expected
            .requests
            .push(Request::WalkAccess { addr: address });
    }
    if leaf_flags != 0xc7 {
        f.trap(15, VA);
    } else {
        f.expected.tlb.install(TlbEntry {
            valid: true,
            global: false,
            asid: 0,
            vpn: 0x10,
            pa_base: PA,
            r: true,
            w: true,
            x: false,
            u: false,
            a: true,
            d: true,
            level: 0,
        });
        f.expected.requests.push(load);
        if fail == 1 {
            f.trap(7, VA);
        } else if fail == 2 {
            f.expected.requests.push(store);
            f.trap(7, VA);
        } else {
            f.store(width(n), PA, new);
            f.retire(7, old_value(vector, n));
        }
    }
    f
}

pub(super) fn reservation_positive() -> Result<(), String> {
    reservation::positive_over(INSNS)
}

pub(super) fn reservation_negative() -> Result<(), String> {
    reservation::negative_over(INSNS)?;
    permissions::physical_permissions()
}

pub(super) fn positive() -> Result<(), String> {
    for n in [4, 8] {
        for order in 0..4 {
            for mode in MODES {
                for rd in [0, 6, 7, 9] {
                    for vector in 0..VECTORS.len() {
                        for function in FUNCTIONS.into_iter().chain([2, 3]) {
                            ordinary(function, n, order, rd, mode, vector, true).check(INSNS)
                                .map_err(|e| format!("funct5={function} W{n} order{order} {mode:?} rd{rd} vector{vector}: {e}"))?;
                        }
                    }
                }
            }
        }
    }
    for function in FUNCTIONS {
        for n in [4, 8] {
            for order in 0..4 {
                translated(function, n, order, 0xc7, 0).check(INSNS)?;
            }
        }
    }
    Ok(())
}

pub(super) fn negative() -> Result<(), String> {
    for n in [4, 8] {
        for order in 0..4 {
            for mode in MODES {
                for rd in [0, 6, 7, 9] {
                    for vector in 0..VECTORS.len() {
                        ordinary(3, n, order, rd, mode, vector, false).check(INSNS)?;
                    }
                }
            }
        }
    }
    for function in FUNCTIONS {
        for n in [4, 8] {
            for order in 0..4 {
                // Invalid V, write-only, read-only, A=0, D=0, inaccessible U page.
                for flags in [0xc6, 0xc5, 0xc3, 0x87, 0x47, 0xd7] {
                    translated(function, n, order, flags, 0)
                        .check(INSNS)
                        .map_err(|e| {
                            format!("AMO fault {function}/{n}/{order}/flags{flags:#x}: {e}")
                        })?;
                }
                for fail in [1, 2] {
                    translated(function, n, order, 0xc7, fail)
                        .check(INSNS)
                        .map_err(|e| {
                            format!("AMO physical fault {function}/{n}/{order}/{fail}: {e}")
                        })?;
                }
            }
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use semulith_core::definition_rv64gc::Sem;

    fn changed_table(effect: &'static Sem) -> Vec<InsnDef> {
        assert_eq!(INSNS.iter().filter(|r| r.name == "amoadd.w").count(), 1);
        INSNS
            .iter()
            .map(|r| InsnDef {
                name: r.name,
                mask: r.mask,
                value: r.value,
                operands: r.operands,
                from: r.from,
                source: r.source,
                effect: if r.name == "amoadd.w" {
                    effect
                } else {
                    r.effect
                },
                length: r.length,
                expansion: r.expansion,
            })
            .collect()
    }

    #[test]
    fn literal_atomic_values_aliases_and_faults_hold() {
        assert_eq!(positive(), Ok(()));
        assert_eq!(negative(), Ok(()));
    }

    const CORRECT_ADD_W: &Sem = &Sem::Set(
        &Sem::Reg("rd"),
        &Sem::Sext(
            64,
            &Sem::Amo(
                0,
                &Sem::Lit(32),
                &Sem::Reg("rs1"),
                &Sem::Trunc(32, &Sem::Reg("rs2")),
            ),
        ),
    );

    #[test]
    fn wrong_public_atomic_effects_fail_named_observations() {
        let cases: [(&Sem, &str); 9] = [
            (
                &Sem::Seq(&[
                    CORRECT_ADD_W,
                    &Sem::Load(&Sem::Lit(64), &Sem::Lit(0), &Sem::Lit(DATA)),
                ]),
                "requests differ",
            ),
            (&Sem::Nop, "requests differ"),
            (
                &Sem::Set(
                    &Sem::Reg("rd"),
                    &Sem::Load(&Sem::Lit(32), &Sem::Lit(0), &Sem::Reg("rs1")),
                ),
                "requests differ",
            ),
            (
                &Sem::Set(
                    &Sem::Reg("rd"),
                    &Sem::Amo(
                        1,
                        &Sem::Lit(32),
                        &Sem::Reg("rs1"),
                        &Sem::Trunc(32, &Sem::Reg("rs2")),
                    ),
                ),
                "requests differ",
            ),
            (
                &Sem::Set(
                    &Sem::Reg("rd"),
                    &Sem::Amo(
                        0,
                        &Sem::Lit(32),
                        &Sem::Reg("rs1"),
                        &Sem::Trunc(32, &Sem::Reg("rs2")),
                    ),
                ),
                "integer registers differ",
            ),
            (
                &Sem::Seq(&[
                    CORRECT_ADD_W,
                    &Sem::CsrWrite(&Sem::Lit(0x340), &Sem::Lit(0)),
                ]),
                "CSR owners differ",
            ),
            (
                &Sem::Seq(&[
                    CORRECT_ADD_W,
                    &Sem::StoreConditional(&Sem::Lit(64), &Sem::Lit(DATA + 0x20), &Sem::Lit(0)),
                ]),
                "requests differ",
            ),
            (
                &Sem::Seq(&[
                    CORRECT_ADD_W,
                    &Sem::TlbInvalidate(&Sem::Lit(0), &Sem::Lit(0), &Sem::Lit(1), &Sem::Lit(1)),
                ]),
                "TLB/cursor differs",
            ),
            (
                &Sem::Seq(&[CORRECT_ADD_W, &Sem::SetPc(&Sem::Lit(ENTRY + 8))]),
                "PC/mode differs",
            ),
        ];
        for (effect, reason) in cases {
            let mut f = ordinary(0, 4, 0, 7, PrivilegeMode::M, 7, true);
            assert!(f
                .check(&changed_table(effect))
                .expect_err(reason)
                .contains(reason));
        }
    }

    #[test]
    fn corrupt_atomic_captures_fail_all_observer_families() {
        let mut f = ordinary(0, 4, 0, 7, PrivilegeMode::M, 7, true);
        let actual = f.observe(INSNS);
        assert_eq!(judge(&actual, &f.expected), Ok(()));
        for i in 0..14 {
            let mut bad = actual.clone();
            let reason = match i {
                0 => {
                    bad.requests.pop();
                    "requests differ"
                }
                1 => {
                    bad.requests.swap(2, 3);
                    "requests differ"
                }
                2 => {
                    bad.requests.push(Request::WalkAccess { addr: 0x2000 });
                    "requests differ"
                }
                3 => {
                    bad.memory[0x80] ^= 1;
                    "memory differs"
                }
                4 => {
                    bad.x[7] ^= 1;
                    "integer registers differ"
                }
                5 => {
                    bad.f[7] ^= 1;
                    "floating registers differ"
                }
                6 => {
                    bad.csrs[CSR_MSCRATCH] ^= 1;
                    "CSR owners differ"
                }
                7 => {
                    bad.reservation.clear();
                    "reservation differs"
                }
                8 => {
                    bad.reservation.establish(DATA, 4);
                    "reservation differs"
                }
                9 => {
                    bad.tlb.invalidate(None, None);
                    "TLB/cursor differs"
                }
                10 => {
                    bad.wait.enter();
                    "wait state differs"
                }
                11 => {
                    bad.pc += 4;
                    "PC/mode differs"
                }
                12 => {
                    bad.parcels += 1;
                    "boundary outcome/parcels differ"
                }
                _ => {
                    bad.executed = false;
                    "boundary outcome/parcels differ"
                }
            };
            assert_eq!(judge(&bad, &f.expected).expect_err(reason), reason);
        }
    }
}
