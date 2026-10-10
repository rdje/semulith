//! The frozen atomic access-fault choice and pre-translation alignment priority.
//!
//! RVI-A 12.1.2/12.1.4 permit the selected access-fault family; RVP-MACHINE's
//! exception table assigns LR to loads and SC/AMO to stores. This is a finite
//! one-hart witness, not an exploration of every atomic or weak-memory outcome.

use semulith_core::definition_rv64gc::{InsnDef, INSNS};
use semulith_core::env::{AccessWidth, BoundaryError, Environment, Request, Response};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::privilege::PrivilegedHart;
use semulith_core::reservation::Reservation;
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_COUNT, CSR_FFLAGS, CSR_FRM, CSR_MCAUSE, CSR_MCYCLE,
    CSR_MEPC, CSR_MINSTRET, CSR_MSCRATCH, CSR_MSTATUS, CSR_MTVAL, CSR_MTVEC, CSR_SATP,
    CSR_SSCRATCH,
};

use crate::fixtures::FlatMemory;

const ENTRY: u64 = 0x1000;
const HANDLER: u64 = 0x1100;
const DATA: u64 = 0x1080;
const OLD: u64 = 0x1122_3344_8000_0001;
const NEW: u64 = 0x8877_6655_4433_2211;
// LR, SC, then the nine Zaamo funct5 values; these literals also encode the words.
const FUNCTIONS: [u32; 11] = [2, 3, 1, 0, 4, 12, 8, 16, 20, 24, 28];

#[derive(Clone, Copy, Debug)]
enum Context {
    Machine,
    Supervisor,
    User,
    InvalidRoot,
    Noncanonical,
}

impl Context {
    fn mode(self) -> PrivilegeMode {
        match self {
            Self::Supervisor => PrivilegeMode::S,
            Self::User => PrivilegeMode::U,
            _ => PrivilegeMode::M,
        }
    }

    fn initial_status(self) -> u64 {
        match self {
            Self::InvalidRoot | Self::Noncanonical => 0xa_0002_6808, // MPRV, MPP=S.
            _ => 0xa_0000_6008, // FS Dirty, MIE set; no interrupt source enabled.
        }
    }

    fn trap_status(self) -> u64 {
        match self {
            Self::Machine => 0xa_0000_7880,
            Self::Supervisor => 0xa_0000_6880,
            Self::User => 0xa_0000_6080,
            Self::InvalidRoot | Self::Noncanonical => 0xa_0002_7880,
        }
    }

    fn address(self) -> u64 {
        match self {
            Self::Noncanonical => 0x40_0000_1080,
            _ => DATA,
        }
    }
}

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

#[derive(Clone)]
struct Observation {
    requests: Vec<Request>,
    memory: Vec<u8>,
    x: [u64; 32],
    f: [u64; 32],
    csrs: [u64; CSR_COUNT],
    reservation: Reservation,
    pc: u64,
    mode: PrivilegeMode,
    parcels: u64,
    executed: bool,
}

impl Observation {
    fn capture(hart: &mut ArchitecturalState, observer: &Observer, executed: bool) -> Self {
        Self {
            requests: observer.requests.clone(),
            memory: observer.memory.bytes().to_vec(),
            x: std::array::from_fn(|r| hart.read_x(r as u8)),
            f: std::array::from_fn(|r| hart.read_f(r as u8)),
            csrs: std::array::from_fn(|i| hart.read_csr(i)),
            reservation: *hart.reservation(),
            pc: hart.pc(),
            mode: hart.mode(),
            parcels: observer.memory.fetch_count(),
            executed,
        }
    }
}

fn judge(actual: &Observation, expected: &Observation) -> Result<(), String> {
    if actual.requests != expected.requests {
        return Err(format!(
            "requests differ: {:?}, required {:?}",
            actual.requests, expected.requests
        ));
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
        let index = actual
            .csrs
            .iter()
            .zip(expected.csrs)
            .position(|(a, e)| *a != e)
            .expect("a CSR differs");
        return Err(format!(
            "CSR owners differ at {index}: {:#x}, required {:#x}",
            actual.csrs[index], expected.csrs[index]
        ));
    }
    if actual.reservation != expected.reservation {
        return Err("reservation differs".into());
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
    fn new(words: &[u32], context: Context, address: u64, prior: bool) -> Self {
        // Root PTE at 0x2000 remains zero: if alignment is bypassed, Sv39 faults.
        let mut memory = FlatMemory::with_fetch_align(ENTRY, 0x2000, 2);
        for (i, word) in words.iter().enumerate() {
            memory.load_image(i * 4, &word.to_le_bytes());
        }
        memory.load_image(0x80, &OLD.to_le_bytes());
        let mut hart = ArchitecturalState::zeroed_at(ENTRY);
        hart.set_mode(context.mode());
        hart.write_csr(CSR_MSTATUS, context.initial_status());
        if matches!(context, Context::InvalidRoot | Context::Noncanonical) {
            hart.write_csr(CSR_SATP, 0x8000_0000_0000_0002);
        }
        hart.write_csr(CSR_MTVEC, HANDLER);
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
        hart.write_x(9, NEW);
        for r in 0..32 {
            hart.write_f(r, 0x7ff8_0000_0000_1000 + u64::from(r));
        }
        if prior {
            hart.reservation().establish(DATA + 0x20, 8);
        }
        let observer = Observer {
            memory,
            requests: Vec::new(),
        };
        let expected = Observation::capture(&mut hart, &observer, true);
        Self {
            hart,
            observer,
            expected,
        }
    }

    fn fetch(&mut self, pc: u64) {
        self.expected.requests.extend([
            Request::FetchParcel { addr: pc },
            Request::FetchParcel { addr: pc + 2 },
        ]);
        self.expected.parcels += 2;
        self.expected.csrs[CSR_MCYCLE] += 1;
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
        let actual = self.observe(table);
        judge(&actual, &self.expected)
    }
}

fn word(function: u32, bytes: u32, ordering: u32, rd: u32) -> u32 {
    (function << 27)
        | (ordering << 25)
        | ((if function == 2 { 0 } else { 9 }) << 20)
        | (6 << 15)
        | ((if bytes == 4 { 2 } else { 3 }) << 12)
        | (rd << 7)
        | 0x2f
}

fn aligned(bytes: u32, ordering: u32, context: Context, rd: u32) -> Result<(), String> {
    let words = [word(2, bytes, ordering, rd), word(3, bytes, ordering, rd)];
    let mut fixture = Fixture::new(&words, context, DATA, true);
    let width = if bytes == 4 {
        AccessWidth::W
    } else {
        AccessWidth::D
    };
    for i in 0..2 {
        fixture.fetch(ENTRY + 4 * i);
        fixture.expected.pc += 4;
        fixture.expected.csrs[CSR_MINSTRET] += 1;
        if i == 0 {
            fixture
                .expected
                .requests
                .push(Request::Load { width, addr: DATA });
            fixture.expected.reservation.establish(DATA, bytes as u8);
            if rd != 0 {
                fixture.expected.x[rd as usize] = if bytes == 4 {
                    0xffff_ffff_8000_0001
                } else {
                    OLD
                };
            }
        } else {
            fixture.expected.requests.push(Request::Store {
                width,
                addr: DATA,
                data: if bytes == 4 { NEW & 0xffff_ffff } else { NEW },
            });
            fixture.expected.reservation.clear();
            fixture.expected.memory[0x80..0x80 + bytes as usize]
                .copy_from_slice(&NEW.to_le_bytes()[..bytes as usize]);
            if rd != 0 {
                fixture.expected.x[rd as usize] = 0;
            }
        }
        fixture.check(INSNS).map_err(|e| {
            format!("aligned {bytes}/{ordering}/{context:?}/x{rd} boundary {i}: {e}")
        })?;
    }
    Ok(())
}

fn fault_fixture(
    function: u32,
    bytes: u32,
    ordering: u32,
    rd: u32,
    offset: u64,
    context: Context,
    prior: bool,
) -> Fixture {
    let address = context.address() + offset;
    let mut fixture = Fixture::new(
        &[word(function, bytes, ordering, rd)],
        context,
        address,
        prior,
    );
    fixture.fetch(ENTRY);
    fixture.expected.pc = HANDLER;
    fixture.expected.mode = PrivilegeMode::M;
    fixture.expected.csrs[CSR_MSTATUS] = context.trap_status();
    fixture.expected.csrs[CSR_MCAUSE] = if function == 2 { 5 } else { 7 };
    fixture.expected.csrs[CSR_MEPC] = ENTRY;
    fixture.expected.csrs[CSR_MTVAL] = address;
    fixture
}

pub(super) fn positive() -> Result<(), String> {
    for bytes in [4, 8] {
        for ordering in 0..4 {
            for context in [Context::Machine, Context::Supervisor, Context::User] {
                for rd in [0, 7] {
                    aligned(bytes, ordering, context, rd)?;
                }
            }
        }
    }
    Ok(())
}

pub(super) fn negative() -> Result<(), String> {
    for function in FUNCTIONS {
        for bytes in [4, 8] {
            for ordering in 0..4 {
                for offset in 1..u64::from(bytes) {
                    for context in [
                        Context::Machine,
                        Context::Supervisor,
                        Context::User,
                        Context::InvalidRoot,
                        Context::Noncanonical,
                    ] {
                        for rd in [0, 7] {
                            for prior in [false, true] {
                                fault_fixture(function, bytes, ordering, rd, offset, context, prior)
                                    .check(INSNS).map_err(|e| format!("misaligned funct5={function}/{bytes}/{ordering}/{context:?}/x{rd}/offset{offset}/prior{prior}: {e}"))?;
                            }
                        }
                    }
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

    fn table(effect: &'static Sem) -> Vec<InsnDef> {
        assert_eq!(INSNS.iter().filter(|row| row.name == "lr.d").count(), 1);
        INSNS
            .iter()
            .map(|row| InsnDef {
                name: row.name,
                mask: row.mask,
                value: row.value,
                operands: row.operands,
                from: row.from,
                source: row.source,
                effect: if row.name == "lr.d" {
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
    fn aligned_pairs_and_all_misaligned_forms_hold() {
        assert_eq!(positive(), Ok(()));
        assert_eq!(negative(), Ok(()));
    }

    #[test]
    fn wrong_public_effects_fail_named_observations() {
        let cases: [(&Sem, &str); 7] = [
            (
                &Sem::TrapDeliver(&Sem::Lit(4), &Sem::Reg("rs1")),
                "CSR owners differ",
            ),
            (
                &Sem::TrapDeliver(&Sem::Lit(7), &Sem::Reg("rs1")),
                "CSR owners differ",
            ),
            (
                &Sem::TrapDeliver(&Sem::Lit(5), &Sem::Lit(DATA)),
                "CSR owners differ",
            ),
            (
                &Sem::Seq(&[
                    &Sem::Set(&Sem::Reg("rd"), &Sem::Lit(0)),
                    &Sem::TrapDeliver(&Sem::Lit(5), &Sem::Reg("rs1")),
                ]),
                "integer registers differ",
            ),
            (
                &Sem::Seq(&[
                    &Sem::CsrWrite(&Sem::Lit(0x340), &Sem::Lit(0)),
                    &Sem::TrapDeliver(&Sem::Lit(5), &Sem::Reg("rs1")),
                ]),
                "CSR owners differ",
            ),
            (
                &Sem::Seq(&[
                    &Sem::Load(&Sem::Lit(64), &Sem::Lit(0), &Sem::Lit(DATA)),
                    &Sem::TrapDeliver(&Sem::Lit(5), &Sem::Reg("rs1")),
                ]),
                "requests differ",
            ),
            (
                &Sem::Seq(&[
                    &Sem::StoreConditional(&Sem::Lit(64), &Sem::Lit(DATA + 0x30), &Sem::Lit(0)),
                    &Sem::TrapDeliver(&Sem::Lit(5), &Sem::Reg("rs1")),
                ]),
                "requests differ",
            ),
        ];
        for (effect, reason) in cases {
            let mut fixture = fault_fixture(2, 8, 0, 7, 1, Context::Machine, true);
            assert!(fixture
                .check(&table(effect))
                .expect_err(reason)
                .contains(reason));
        }
    }

    #[test]
    fn corrupted_captures_fail_each_auditor_family() {
        let mut fixture = fault_fixture(2, 8, 0, 7, 1, Context::InvalidRoot, true);
        let actual = fixture.observe(INSNS);
        assert_eq!(judge(&actual, &fixture.expected), Ok(()));
        for control in 0..13 {
            let mut bad = actual.clone();
            let reason = match control {
                0 => {
                    bad.requests.pop();
                    "requests differ"
                }
                1 => {
                    bad.requests.push(Request::WalkAccess { addr: 0x2000 });
                    "requests differ"
                }
                2 => {
                    bad.requests.push(Request::Load {
                        width: AccessWidth::D,
                        addr: DATA,
                    });
                    "requests differ"
                }
                3 => {
                    bad.requests.push(Request::Store {
                        width: AccessWidth::D,
                        addr: DATA,
                        data: NEW,
                    });
                    "requests differ"
                }
                4 => {
                    bad.memory[0x80] ^= 1;
                    "memory differs"
                }
                5 => {
                    bad.x[7] = 0;
                    "integer registers differ"
                }
                6 => {
                    bad.f[7] = 0;
                    "floating registers differ"
                }
                7 => {
                    bad.csrs[CSR_MCAUSE] = 4;
                    "CSR owners differ"
                }
                8 => {
                    bad.reservation.clear();
                    "reservation differs"
                }
                9 => {
                    bad.pc += 4;
                    "PC/mode differs"
                }
                10 => {
                    bad.mode = PrivilegeMode::U;
                    "PC/mode differs"
                }
                11 => {
                    bad.parcels += 1;
                    "boundary outcome/parcels differ"
                }
                _ => {
                    bad.executed = false;
                    "boundary outcome/parcels differ"
                }
            };
            let error = judge(&bad, &fixture.expected).expect_err("corrupted capture");
            assert!(error.contains(reason), "control {control}: {error}");
        }
    }
}
