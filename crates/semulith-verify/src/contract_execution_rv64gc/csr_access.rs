//! Zicsr 5.1.1, CSR 1.1.1, and selected privileged CSR access gates.
//! Full-state expectations are constructed literally before each instruction.

use crate::fixtures::FlatMemory;
use semulith_core::definition_rv64gc::{InsnDef, Sem, INSNS};
use semulith_core::env::{BoundaryError, Environment, Request, Response};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::privilege::PrivilegedHart;
use semulith_core::reservation::Reservation;
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_COUNT, CSR_FFLAGS, CSR_FRM, CSR_MCAUSE, CSR_MCOUNTEREN,
    CSR_MCYCLE, CSR_MENVCFG, CSR_MEPC, CSR_MINSTRET, CSR_MSCRATCH, CSR_MSTATUS, CSR_MTVAL,
    CSR_MTVEC, CSR_SATP, CSR_SCOUNTEREN, CSR_SSCRATCH, CSR_STIMECMP,
};
use semulith_core::translation::{Tlb, TlbEntry};
use semulith_core::wait::HartState;

const ENTRY: u64 = 0x1000;
const HANDLER: u64 = 0x1100;
const DATA: u64 = 0x1080;
const HIGH: u64 = 0x8000_0000_55aa_00ff;
const MODES: [PrivilegeMode; 3] = [PrivilegeMode::M, PrivilegeMode::S, PrivilegeMode::U];
const FORMS: [(u32, &str); 6] = [
    (1, "csrrw"),
    (2, "csrrs"),
    (3, "csrrc"),
    (5, "csrrwi"),
    (6, "csrrsi"),
    (7, "csrrci"),
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

#[derive(Clone)]
struct Observation {
    x: [u64; 32],
    f: [u64; 32],
    csrs: [u64; CSR_COUNT],
    pc: u64,
    mode: PrivilegeMode,
    reservation: Reservation,
    tlb: Tlb,
    wait: HartState,
    memory: Vec<u8>,
    requests: Vec<Request>,
    parcels: u64,
    executed: bool,
}

impl Observation {
    fn capture(h: &mut ArchitecturalState, o: &Observer, executed: bool) -> Self {
        Self {
            x: std::array::from_fn(|i| h.read_x(i as u8)),
            f: std::array::from_fn(|i| h.read_f(i as u8)),
            csrs: std::array::from_fn(|i| h.read_csr(i)),
            pc: h.pc(),
            mode: h.mode(),
            reservation: *h.reservation(),
            tlb: h.tlb().clone(),
            wait: *h.hart_state(),
            memory: o.memory.bytes().to_vec(),
            requests: o.requests.clone(),
            parcels: o.memory.fetch_count(),
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
    if actual.pc != expected.pc || actual.mode != expected.mode {
        return Err("PC/mode differs".into());
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
    if actual.parcels != expected.parcels || actual.executed != expected.executed {
        return Err("extent/outcome differs".into());
    }
    Ok(())
}

#[derive(Clone, Copy, Debug)]
struct Context {
    address: u32,
    m: u64,
    s: u64,
    stce: bool,
    tvm: bool,
    fs: bool,
}

impl Context {
    const fn plain(address: u32) -> Self {
        Self {
            address,
            m: 0,
            s: 0,
            stce: false,
            tvm: false,
            fs: true,
        }
    }
}

const CONTEXTS: [Context; 15] = [
    Context::plain(0x340),
    Context::plain(0x140),
    Context::plain(0xc00),
    Context {
        m: 1,
        ..Context::plain(0xc00)
    },
    Context {
        s: 1,
        ..Context::plain(0xc00)
    },
    Context {
        m: 1,
        s: 1,
        ..Context::plain(0xc00)
    },
    Context::plain(0x14d),
    Context {
        m: 2,
        ..Context::plain(0x14d)
    },
    Context {
        stce: true,
        ..Context::plain(0x14d)
    },
    Context {
        m: 2,
        stce: true,
        ..Context::plain(0x14d)
    },
    Context::plain(0x180),
    Context {
        tvm: true,
        ..Context::plain(0x180)
    },
    Context {
        fs: false,
        ..Context::plain(0x003)
    },
    Context::plain(0x003),
    Context::plain(0x7c0),
];

#[derive(Clone, Copy, Debug)]
struct Cell {
    context: Context,
    mode: PrivilegeMode,
    form: u32,
    source: u32,
    input: u64,
    rd: u32,
    high: bool,
}

impl Cell {
    fn writes(self) -> bool {
        self.form & 3 == 1 || self.source != 0
    }

    fn legal(self) -> bool {
        let c = self.context;
        if c.address == 0x7c0 || (self.mode as u32) < ((c.address >> 8) & 3) {
            return false;
        }
        if self.writes() && c.address >> 10 == 3 {
            return false;
        }
        match c.address {
            0xc00 => {
                self.mode == PrivilegeMode::M
                    || (c.m & 1 != 0 && (self.mode == PrivilegeMode::S || c.s & 1 != 0))
            }
            0x14d => self.mode == PrivilegeMode::M || (c.m & 2 != 0 && c.stce),
            0x180 => self.mode != PrivilegeMode::S || !c.tvm,
            0x003 => c.fs,
            _ => true,
        }
    }

    fn word(self) -> u32 {
        (self.context.address << 20)
            | (self.source << 15)
            | (self.form << 12)
            | (self.rd << 7)
            | 0x73
    }

    fn fixture(self) -> (ArchitecturalState, Observer, Observation) {
        let c = self.context;
        let mut h = ArchitecturalState::zeroed_at(ENTRY);
        h.set_mode(self.mode);
        h.write_csr(
            CSR_MSTATUS,
            0xa_0000_0000 | (u64::from(c.fs) << 13) | (u64::from(c.tvm) << 20),
        );
        h.write_csr(CSR_MCOUNTEREN, c.m);
        h.write_csr(CSR_SCOUNTEREN, c.s);
        h.write_csr(CSR_MENVCFG, u64::from(c.stce) << 63);
        h.write_csr(CSR_MCYCLE, if self.high { u64::MAX } else { 41 });
        h.write_csr(CSR_MINSTRET, if self.high { u64::MAX } else { 17 });
        h.write_csr(CSR_MTVEC, HANDLER);
        h.write_csr(CSR_MCAUSE, 0x55);
        h.write_csr(CSR_MEPC, 0x1200);
        h.write_csr(CSR_MTVAL, 0x7788);
        let initial = if self.high { HIGH } else { 0 };
        h.write_csr(CSR_MSCRATCH, initial);
        h.write_csr(CSR_SSCRATCH, initial);
        h.write_csr(CSR_STIMECMP, initial);
        // Bare for all S/U fetches; c31a separately covers old Sv39/unsupported MODE.
        h.write_csr(CSR_SATP, 0);
        h.write_csr(CSR_FFLAGS, if self.high { 0x15 } else { 0 });
        h.write_csr(CSR_FRM, if self.high { 3 } else { 0 });
        for r in 1..32 {
            h.write_x(r, 0x1111_2222_3333_0000 + u64::from(r));
        }
        for r in 0..32 {
            h.write_f(r, 0x7ff8_0000_0000_1000 + u64::from(r));
        }
        if self.form < 4 {
            h.write_x(self.source as u8, self.input);
        }
        h.reservation().establish(DATA, 8);
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
        let mut memory = FlatMemory::with_fetch_align(ENTRY, 0x200, 2);
        memory.load_image(0, &self.word().to_le_bytes());
        memory.load_image(0x80, &0x8877_6655_4433_2211_u64.to_le_bytes());
        let observer = Observer {
            memory,
            requests: Vec::new(),
        };
        let mut expected = Observation::capture(&mut h, &observer, true);
        expected.requests = vec![
            Request::FetchParcel { addr: ENTRY },
            Request::FetchParcel { addr: ENTRY + 2 },
        ];
        expected.parcels = 2;
        expected.csrs[CSR_MCYCLE] = expected.csrs[CSR_MCYCLE].wrapping_add(1);
        if self.legal() {
            let old = match c.address {
                0x340 | 0x140 | 0x14d => initial,
                0xc00 => h.read_csr(CSR_MCYCLE),
                0x180 => 0,
                0x003 => {
                    if self.high {
                        0x75
                    } else {
                        0
                    }
                }
                _ => unreachable!("only the six implemented addresses can be legal"),
            };
            // Source and old CSR are taken before any destination write, including aliases.
            let source = if self.form < 4 {
                h.read_x(self.source as u8)
            } else {
                u64::from(self.source)
            };
            if self.writes() {
                let value = match self.form & 3 {
                    1 => source,
                    2 => old | source,
                    3 => old & !source,
                    _ => unreachable!(),
                };
                match c.address {
                    0x340 => expected.csrs[CSR_MSCRATCH] = value,
                    0x140 => expected.csrs[CSR_SSCRATCH] = value,
                    0x14d => expected.csrs[CSR_STIMECMP] = value,
                    0x180 => {
                        if matches!(value >> 60, 0 | 8) {
                            expected.csrs[CSR_SATP] = value;
                        }
                    }
                    0x003 => {
                        expected.csrs[CSR_FFLAGS] = value & 31;
                        expected.csrs[CSR_FRM] = (value >> 5) & 7;
                        expected.csrs[CSR_MSTATUS] |= 3 << 13;
                    }
                    _ => unreachable!("read-only counters never accept a write"),
                }
            }
            if self.rd != 0 {
                expected.x[self.rd as usize] = old;
            }
            expected.csrs[CSR_MINSTRET] = expected.csrs[CSR_MINSTRET].wrapping_add(1);
            expected.pc = ENTRY + 4;
        } else {
            expected.csrs[CSR_MCAUSE] = 2;
            expected.csrs[CSR_MEPC] = ENTRY;
            expected.csrs[CSR_MTVAL] = u64::from(self.word());
            expected.csrs[CSR_MSTATUS] = (expected.csrs[CSR_MSTATUS]
                & !((3 << 11) | (1 << 7) | (1 << 3)))
                | ((self.mode as u64) << 11);
            expected.pc = HANDLER;
            expected.mode = PrivilegeMode::M;
        }
        (h, observer, expected)
    }

    fn observe(self, table: &[InsnDef]) -> (Observation, Observation) {
        let (mut h, mut observer, expected) = self.fixture();
        let executed = exec_rv64gc::step_over(&mut h, &mut observer, table) == StepRv64gc::Executed;
        (Observation::capture(&mut h, &observer, executed), expected)
    }

    fn check(self, table: &[InsnDef]) -> Result<(), String> {
        let (actual, expected) = self.observe(table);
        judge(&actual, &expected).map_err(|why| format!("{self:?}: {why}"))
    }
}

// There is no selected CSR read side effect to count at the Environment boundary.
// Inspect just the published rd=0 branch: a write whose address/data operands cannot read
// a CSR. This is table evidence, separately qualified from the dynamic state witness.
fn no_read_swap_branch(table: &[InsnDef]) -> Result<(), String> {
    for name in ["csrrw", "csrrwi"] {
        let effect = table
            .iter()
            .find(|r| r.name == name)
            .ok_or_else(|| format!("missing {name}"))?
            .effect;
        let valid = match effect {
            Sem::If(
                Sem::Eq(Sem::Field("rd"), Sem::Lit(0)),
                Sem::CsrWrite(Sem::Field("csr"), data),
                _,
            ) => {
                matches!(data, Sem::Reg("rs1"))
                    || matches!(data, Sem::Zext(64, Sem::Field("zimm5")))
            }
            _ => false,
        };
        if !valid {
            return Err(format!(
                "{name} rd0 branch is not a write without a CSR read"
            ));
        }
    }
    Ok(())
}

fn matrix(legal: bool) -> Result<usize, String> {
    let mut count = 0;
    for context in CONTEXTS {
        for mode in MODES {
            for (form, _) in FORMS {
                for source in [0, 6, 31] {
                    let inputs: &[u64] = if form < 4 { &[0, HIGH, u64::MAX] } else { &[0] };
                    for &input in inputs {
                        for rd in [0, 5, 6, 31] {
                            for high in [false, true] {
                                let cell = Cell {
                                    context,
                                    mode,
                                    form,
                                    source,
                                    input,
                                    rd,
                                    high,
                                };
                                if cell.legal() == legal {
                                    cell.check(INSNS)?;
                                    count += 1;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    Ok(count)
}

pub(super) fn positive() -> Result<(), String> {
    no_read_swap_branch(INSNS)?;
    let count = matrix(true)?;
    if count != 4480 {
        return Err(format!("positive matrix extent {count}"));
    }
    Ok(())
}
pub(super) fn negative() -> Result<(), String> {
    let count = matrix(false)?;
    if count != 8480 {
        return Err(format!("negative matrix extent {count}"));
    }
    Ok(())
}
#[cfg(test)]
mod tests {
    use super::*;
    use semulith_core::env::AccessWidth;

    fn cell(mode: PrivilegeMode) -> Cell {
        Cell {
            context: Context::plain(0x340),
            mode,
            form: 1,
            source: 6,
            input: HIGH,
            rd: 5,
            high: true,
        }
    }
    fn wrong_table(name: &str, effect: &'static Sem) -> Vec<InsnDef> {
        INSNS
            .iter()
            .map(|row| InsnDef {
                from: row.from,
                name: row.name,
                mask: row.mask,
                value: row.value,
                operands: row.operands,
                source: row.source,
                effect: if row.name == name { effect } else { row.effect },
                length: row.length,
                expansion: row.expansion,
            })
            .collect()
    }
    #[test]
    fn all_csr_access_cells_match_literal_states() {
        assert_eq!(positive(), Ok(()));
        assert_eq!(negative(), Ok(()));
    }
    #[test]
    fn extra_same_csr_read_is_dynamically_equivalent_but_table_check_rejects_it() {
        for (form, name) in [(1, "csrrw"), (5, "csrrwi")] {
            let effect = if form == 1 {
                &Sem::Set(
                    &Sem::Reg("rd"),
                    &Sem::CsrRw(&Sem::Field("csr"), &Sem::Reg("rs1")),
                )
            } else {
                &Sem::Set(
                    &Sem::Reg("rd"),
                    &Sem::CsrRw(&Sem::Field("csr"), &Sem::Zext(64, &Sem::Field("zimm5"))),
                )
            };
            let table = wrong_table(name, effect);
            for context in CONTEXTS {
                for mode in MODES {
                    for source in [0, 6, 31] {
                        for input in [0, HIGH, u64::MAX] {
                            for high in [false, true] {
                                let c = Cell {
                                    context,
                                    mode,
                                    form,
                                    source,
                                    input,
                                    rd: 0,
                                    high,
                                };
                                assert_eq!(c.check(&table), Ok(()));
                            }
                        }
                    }
                }
            }
            assert!(no_read_swap_branch(&table)
                .unwrap_err()
                .contains("rd0 branch"));
        }
    }
    #[test]
    fn wrong_csr_effects_fail_named_observations() {
        let base = Cell {
            input: HIGH ^ 0x55,
            ..cell(PrivilegeMode::M)
        };
        let cases: [(Cell, &str, &Sem, &str); 13] = [
            (base, "csrrw", &Sem::Nop, "integer registers differ"),
            (
                base,
                "csrrw",
                &Sem::Set(&Sem::Reg("rd"), &Sem::Reg("rs1")),
                "integer registers differ",
            ),
            (
                Cell { rd: 0, ..base },
                "csrrw",
                &Sem::CsrWrite(&Sem::Lit(0x140), &Sem::Reg("rs1")),
                "CSR owners differ",
            ),
            (
                Cell { rd: 0, ..base },
                "csrrw",
                &Sem::CsrWrite(&Sem::Field("csr"), &Sem::Trunc(32, &Sem::Reg("rs1"))),
                "CSR owners differ",
            ),
            (
                Cell { rd: 0, ..base },
                "csrrw",
                &Sem::Nop,
                "CSR owners differ",
            ),
            (
                Cell {
                    mode: PrivilegeMode::U,
                    ..base
                },
                "csrrw",
                &Sem::Set(&Sem::Reg("rd"), &Sem::CsrState(&Sem::Field("csr"))),
                "integer registers differ",
            ),
            (
                Cell {
                    form: 5,
                    source: 31,
                    rd: 0,
                    ..base
                },
                "csrrwi",
                &Sem::CsrWrite(&Sem::Field("csr"), &Sem::Sext(64, &Sem::Field("zimm5"))),
                "CSR owners differ",
            ),
            (
                Cell {
                    form: 2,
                    rd: 0,
                    high: false,
                    ..base
                },
                "csrrs",
                &Sem::CsrWrite(
                    &Sem::Field("csr"),
                    &Sem::And(&Sem::CsrRead(&Sem::Field("csr")), &Sem::Reg("rs1")),
                ),
                "CSR owners differ",
            ),
            (
                Cell {
                    form: 3,
                    rd: 0,
                    ..base
                },
                "csrrc",
                &Sem::CsrWrite(
                    &Sem::Field("csr"),
                    &Sem::Or(&Sem::CsrRead(&Sem::Field("csr")), &Sem::Reg("rs1")),
                ),
                "CSR owners differ",
            ),
            (
                Cell {
                    context: Context::plain(0xc00),
                    form: 2,
                    source: 0,
                    rd: 0,
                    ..base
                },
                "csrrs",
                &Sem::CsrWrite(&Sem::Field("csr"), &Sem::CsrRead(&Sem::Field("csr"))),
                "CSR owners differ",
            ),
            (
                Cell {
                    context: Context::plain(0xc00),
                    rd: 0,
                    ..base
                },
                "csrrw",
                &Sem::CsrRead(&Sem::Field("csr")),
                "CSR owners differ",
            ),
            (
                Cell {
                    context: Context::plain(0x003),
                    form: 2,
                    input: 0,
                    rd: 0,
                    ..base
                },
                "csrrs",
                &Sem::If(
                    &Sem::Eq(&Sem::Reg("rs1"), &Sem::Lit(0)),
                    &Sem::CsrRead(&Sem::Field("csr")),
                    &Sem::CsrWrite(
                        &Sem::Field("csr"),
                        &Sem::Or(&Sem::CsrRead(&Sem::Field("csr")), &Sem::Reg("rs1")),
                    ),
                ),
                "CSR owners differ",
            ),
            (
                Cell {
                    context: Context::plain(0xc00),
                    ..base
                },
                "csrrw",
                &Sem::Seq(&[
                    &Sem::Set(&Sem::Reg("rd"), &Sem::CsrRead(&Sem::Field("csr"))),
                    &Sem::CsrWrite(&Sem::Field("csr"), &Sem::Reg("rs1")),
                ]),
                "integer registers differ",
            ),
        ];
        for (c, name, effect, reason) in cases {
            let error = c.check(&wrong_table(name, effect)).expect_err(reason);
            assert!(error.contains(reason), "{name}: {error}");
        }
    }

    #[test]
    fn corrupted_csr_captures_fail_every_auditor_component() {
        let (actual, expected) = cell(PrivilegeMode::M).observe(INSNS);
        assert_eq!(judge(&actual, &expected), Ok(()));
        let check =
            |bad: Observation, reason| assert_eq!(judge(&bad, &expected).unwrap_err(), reason);
        for request in [
            Request::Load {
                width: AccessWidth::D,
                addr: DATA,
            },
            Request::Store {
                width: AccessWidth::D,
                addr: DATA,
                data: 0,
            },
            Request::WalkAccess { addr: DATA },
        ] {
            let mut bad = actual.clone();
            bad.requests.push(request);
            check(bad, "requests differ");
        }
        let mut bad = actual.clone();
        bad.memory[0x80] ^= 1;
        check(bad, "memory differs");
        let mut bad = actual.clone();
        bad.x[0] = 1;
        check(bad, "integer registers differ");
        let mut bad = actual.clone();
        bad.x[5] ^= 1;
        check(bad, "integer registers differ");
        let mut bad = actual.clone();
        bad.f[31] ^= 1;
        check(bad, "floating registers differ");
        let mut bad = actual.clone();
        bad.csrs[CSR_MCYCLE] ^= 1;
        check(bad, "CSR owners differ");
        let mut bad = actual.clone();
        bad.csrs[CSR_MCOUNTEREN] ^= 1;
        check(bad, "CSR owners differ");
        let mut bad = actual.clone();
        bad.pc += 4;
        check(bad, "PC/mode differs");
        let mut bad = actual.clone();
        bad.mode = PrivilegeMode::S;
        check(bad, "PC/mode differs");
        let mut bad = actual.clone();
        bad.reservation.clear();
        check(bad, "reservation differs");
        let mut bad = actual.clone();
        bad.tlb = Tlb::new();
        check(bad, "TLB/cursor differs");
        let mut bad = actual.clone();
        bad.wait.enter();
        check(bad, "wait state differs");
        let mut bad = actual.clone();
        bad.parcels += 1;
        check(bad, "extent/outcome differs");
        let mut bad = actual.clone();
        bad.executed = false;
        check(bad, "extent/outcome differs");
    }
}
