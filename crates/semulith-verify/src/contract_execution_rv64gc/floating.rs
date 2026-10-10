//! Finite F witnesses and the numeric D prerequisite (P4-SYSTEM.13 c32/c33a).
//! Expected bits/flags come from the existing FP-VECTORS-governed spec-side data.
//! The production arithmetic backend is never used to construct an expectation.
use crate::fixtures::FlatMemory;
use semulith_core::definition_rv64gc::{InsnDef, INSNS};
use semulith_core::env::{BoundaryError, Environment, Request, Response};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::privilege::PrivilegedHart;
use semulith_core::reservation::Reservation;
use semulith_core::state_rv64gc::{
    ArchitecturalState, PrivilegeMode, CSR_COUNT, CSR_FFLAGS, CSR_FRM, CSR_MCAUSE, CSR_MCYCLE,
    CSR_MEPC, CSR_MINSTRET, CSR_MSCRATCH, CSR_MSTATUS, CSR_MTVAL, CSR_MTVEC,
};
use semulith_core::translation::{Tlb, TlbEntry};
use semulith_core::wait::HartState;
const ENTRY: u64 = 0x1000;
const HANDLER: u64 = 0x1100;
const DATA: u64 = 0x1080;
// Explicit shared data contract: source and expected values are regenerated and
// byte-checked by FP-VECTORS. This is data reuse, not a call to core arithmetic.
const NUMERIC_DATA: &str = include_str!("../../../semulith-core/src/fp/tests/fixtures.txt");
fn boxed(v: u64) -> u64 {
    0xffff_ffff_0000_0000 | (v & 0xffff_ffff)
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

// Shared prestate only: callers derive their own effects before executing.
fn seed(
    word: u32,
    mode: PrivilegeMode,
    fs: u64,
    frm: u64,
    flags: u64,
) -> (ArchitecturalState, Observer) {
    let mut h = ArchitecturalState::zeroed_at(ENTRY);
    h.set_mode(mode);
    h.write_csr(CSR_MSTATUS, 0xa_0000_0000 | (fs << 13)); // Caller selects FS; no interrupt enables.
    h.write_csr(CSR_FFLAGS, flags);
    // Static rm must ignore a reserved frm. DYN must use the vector's legal mode.
    h.write_csr(CSR_FRM, frm);
    h.write_csr(CSR_MCYCLE, 41);
    h.write_csr(CSR_MINSTRET, 17);
    h.write_csr(CSR_MTVEC, HANDLER);
    h.write_csr(CSR_MCAUSE, 0x55);
    h.write_csr(CSR_MEPC, 0x1200);
    h.write_csr(CSR_MTVAL, 0x7788);
    h.write_csr(CSR_MSCRATCH, 0x1122_3344_5566_7788);
    for r in 1..32 {
        h.write_x(r, 0x1111_2222_3333_0000 + u64::from(r));
    }
    for r in 0..32 {
        h.write_f(r, 0x7ff8_0000_0000_1000 + u64::from(r));
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
    memory.load_image(0, &word.to_le_bytes());
    memory.load_image(0x80, &0x8877_6655_4433_2211_u64.to_le_bytes());
    let observer = Observer {
        memory,
        requests: Vec::new(),
    };
    (h, observer)
}
fn retired(h: &mut ArchitecturalState, observer: &Observer) -> Observation {
    let mut expected = Observation::capture(h, observer, true);
    expected.requests = vec![
        Request::FetchParcel { addr: ENTRY },
        Request::FetchParcel { addr: ENTRY + 2 },
    ];
    expected.parcels = 2;
    expected.pc = ENTRY + 4;
    expected.csrs[CSR_MCYCLE] = 42;
    expected.csrs[CSR_MINSTRET] = 18;
    expected
}
fn trapped(h: &mut ArchitecturalState, observer: &Observer, cause: u64, tval: u64) -> Observation {
    let mode = match h.mode() {
        PrivilegeMode::M => 3,
        PrivilegeMode::S => 1,
        PrivilegeMode::U => 0,
    };
    let mut expected = retired(h, observer);
    expected.pc = HANDLER;
    expected.mode = PrivilegeMode::M;
    expected.csrs[CSR_MINSTRET] = 17;
    expected.csrs[CSR_MCAUSE] = cause;
    expected.csrs[CSR_MEPC] = ENTRY;
    expected.csrs[CSR_MTVAL] = tval;
    expected.csrs[CSR_MSTATUS] =
        (expected.csrs[CSR_MSTATUS] & !((3 << 11) | (1 << 7) | (1 << 3))) | (mode << 11);
    expected
}
fn execute(
    h: &mut ArchitecturalState,
    observer: &mut Observer,
    table: &[InsnDef],
    expected: &Observation,
) -> Result<(), String> {
    let executed = exec_rv64gc::step_over(h, observer, table) == StepRv64gc::Executed;
    judge(&Observation::capture(h, observer, executed), expected)
}
mod single;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Op {
    Add,
    Sub,
    Mul,
    Div,
    Sqrt,
    Fma,
    Min,
    Max,
    Eq,
    Lt,
    Le,
    Class,
    ToI32,
    ToU32,
    ToI64,
    ToU64,
    FromI32,
    FromU32,
    FromI64,
    FromU64,
    ToSingle,
    FromSingle,
}
impl Op {
    fn parse(s: &str, format: u32) -> Result<Self, String> {
        Ok(match s {
            "f2f" if format == 32 => Self::ToSingle,
            "f2f" => Self::FromSingle,
            "add" => Self::Add,
            "sub" => Self::Sub,
            "mul" => Self::Mul,
            "div" => Self::Div,
            "sqrt" => Self::Sqrt,
            "fma" => Self::Fma,
            "min" => Self::Min,
            "max" => Self::Max,
            "feq" => Self::Eq,
            "flt" => Self::Lt,
            "fle" => Self::Le,
            "class" => Self::Class,
            "f2i32" => Self::ToI32,
            "f2u32" => Self::ToU32,
            "f2i64" => Self::ToI64,
            "f2u64" => Self::ToU64,
            "i2f32" => Self::FromI32,
            "u2f32" => Self::FromU32,
            "i2f64" => Self::FromI64,
            "u2f64" => Self::FromU64,
            _ => return Err(format!("unrecognized numeric operation {s}")),
        })
    }
    fn rounded(self) -> bool {
        !matches!(
            self,
            Self::Min | Self::Max | Self::Eq | Self::Lt | Self::Le | Self::Class
        )
    }
    fn integer_source(self) -> bool {
        matches!(
            self,
            Self::FromI32 | Self::FromU32 | Self::FromI64 | Self::FromU64
        )
    }
    fn integer_destination(self) -> bool {
        matches!(
            self,
            Self::ToI32
                | Self::ToU32
                | Self::ToI64
                | Self::ToU64
                | Self::Eq
                | Self::Lt
                | Self::Le
                | Self::Class
        )
    }
    fn word(self, format: u32, rd: u32, rm: u32, fused: u32) -> u32 {
        if self == Self::Fma {
            return (8 << 27)
                | (u32::from(format == 64) << 25)
                | (7 << 20)
                | (6 << 15)
                | (rm << 12)
                | (rd << 7)
                | [0x43, 0x47, 0x4b, 0x4f][fused as usize];
        }
        let (funct7, rs2, funct3) = match self {
            Self::Add => (0x00, 7, rm),
            Self::Sub => (0x04, 7, rm),
            Self::Mul => (0x08, 7, rm),
            Self::Div => (0x0c, 7, rm),
            Self::Sqrt => (0x2c, 0, rm),
            Self::Min => (0x14, 7, 0),
            Self::Max => (0x14, 7, 1),
            Self::Eq => (0x50, 7, 2),
            Self::Lt => (0x50, 7, 1),
            Self::Le => (0x50, 7, 0),
            Self::Class => (0x70, 0, 1),
            Self::ToI32 => (0x60, 0, rm),
            Self::ToU32 => (0x60, 1, rm),
            Self::ToI64 => (0x60, 2, rm),
            Self::ToU64 => (0x60, 3, rm),
            Self::FromI32 => (0x68, 0, rm),
            Self::FromU32 => (0x68, 1, rm),
            Self::FromI64 => (0x68, 2, rm),
            Self::FromU64 => (0x68, 3, rm),
            Self::ToSingle => (0x20, 1, rm),
            Self::FromSingle => (0x21, 0, rm),
            Self::Fma => unreachable!(),
        };
        let funct7 = if matches!(self, Self::ToSingle | Self::FromSingle) {
            funct7
        } else {
            funct7 + u32::from(format == 64)
        };
        (funct7 << 25) | (rs2 << 20) | (6 << 15) | (funct3 << 12) | (rd << 7) | 0x53
    }
}
#[derive(Clone, Copy, Debug)]
struct Vector {
    format: u32,
    op: Op,
    rm: u32,
    a: u64,
    b: u64,
    c: u64,
    bits: u64,
    flags: u64,
}
fn vectors(profile_format: u32) -> Result<Vec<Vector>, String> {
    let mut out = Vec::new();
    let mut total = 0;
    for line in NUMERIC_DATA
        .lines()
        .filter(|l| !l.starts_with('#') && !l.is_empty())
    {
        let fields: Vec<_> = line.split_whitespace().collect();
        let [op, n, rm, a, b, c, bits, flags]: [&str; 8] = fields
            .try_into()
            .map_err(|_| format!("numeric row must have8fields: {line}"))?;
        total += 1;
        let n = n
            .parse::<u32>()
            .map_err(|_| format!("invalid format: {line}"))?;
        if !matches!(n, 32 | 64) {
            return Err(format!("unsupported format: {line}"));
        }
        // Both format conversions belong to D, including the single result.
        if (op == "f2f" && profile_format == 32) || (op != "f2f" && n != profile_format) {
            continue;
        }
        let hex = |v: &str| u64::from_str_radix(v, 16).map_err(|_| format!("invalid hex: {line}"));
        let rm = hex(rm)?;
        let flags = hex(flags)?;
        if rm > 4 || flags > 31 {
            return Err(format!("invalid rounding/flag field: {line}"));
        }
        out.push(Vector {
            format: n,
            op: Op::parse(op, n)?,
            rm: rm as u32,
            a: hex(a)?,
            b: hex(b)?,
            c: hex(c)?,
            bits: hex(bits)?,
            flags,
        });
    }
    if total != 3168 || out.len() != if profile_format == 32 { 1504 } else { 1664 } {
        return Err(format!("numeric data extent {total}/{}", out.len()));
    }
    Ok(out)
}
#[derive(Clone, Copy, Debug)]
struct Cell {
    vector: Vector,
    fused: u32,
    dynamic: bool,
    rd: u32,
    mode: PrivilegeMode,
    flags: u64,
}
impl Cell {
    fn word(self) -> u32 {
        self.vector.op.word(
            self.vector.format,
            self.rd,
            if self.dynamic { 7 } else { self.vector.rm },
            self.fused,
        )
    }
    fn fixture(self) -> (ArchitecturalState, Observer, Observation) {
        let v = self.vector;
        let (mut h, observer) = seed(
            self.word(),
            self.mode,
            2,
            if self.dynamic { u64::from(v.rm) } else { 7 },
            self.flags,
        );
        // Fused variants receive sign-adjusted inputs so the existing independent
        // a*b+c vector remains the expected result under each instruction's algebra.
        let sign = if v.format == 32 {
            0x8000_0000
        } else {
            0x8000_0000_0000_0000
        };
        let a = if v.op == Op::Fma && self.fused >= 2 {
            v.a ^ sign
        } else {
            v.a
        };
        let c = if v.op == Op::Fma && self.fused % 2 == 1 {
            v.c ^ sign
        } else {
            v.c
        };
        let source_format = match v.op {
            Op::ToSingle => 64,
            Op::FromSingle => 32,
            _ => v.format,
        };
        let input = |bits| {
            if source_format == 32 {
                boxed(bits)
            } else {
                bits
            }
        };
        h.write_f(6, input(a));
        h.write_f(7, input(v.b));
        h.write_f(8, input(c));
        if v.op.integer_source() {
            h.write_x(6, v.a);
        }
        let mut expected = retired(&mut h, &observer);
        let accrued = self.flags | v.flags;
        expected.csrs[CSR_FFLAGS] = accrued;
        if v.op.integer_destination() {
            let bits = if matches!(v.op, Op::ToI32 | Op::ToU32) {
                v.bits as u32 as i32 as i64 as u64
            } else {
                v.bits
            };
            if self.rd != 0 {
                expected.x[self.rd as usize] = bits;
            }
        } else {
            expected.f[self.rd as usize] = if v.format == 32 {
                boxed(v.bits)
            } else {
                v.bits
            };
        }
        if !v.op.integer_destination() || accrued != self.flags {
            expected.csrs[CSR_MSTATUS] |= 3 << 13;
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
fn numeric_over(table: &[InsnDef], profile_format: u32) -> Result<(), String> {
    let mut count = 0;
    for vector in vectors(profile_format)? {
        for fused in 0..if vector.op == Op::Fma { 4 } else { 1 } {
            for dynamic in [false, true]
                .into_iter()
                .take(if vector.op.rounded() { 2 } else { 1 })
            {
                for mode in [PrivilegeMode::M, PrivilegeMode::S, PrivilegeMode::U] {
                    for rd in [0, 5, 6, 7, 8, 31] {
                        for flags in [0, 31] {
                            Cell {
                                vector,
                                fused,
                                dynamic,
                                rd,
                                mode,
                                flags,
                            }
                            .check(table)?;
                            count += 1;
                        }
                    }
                }
            }
        }
    }
    if count != if profile_format == 32 { 111744 } else { 123264 } {
        return Err(format!("numeric matrix extent {count}"));
    }
    Ok(())
}
pub(super) fn positive() -> Result<(), String> {
    numeric_over(INSNS, 32)?;
    single::positive_over(INSNS)
}
pub(super) fn negative() -> Result<(), String> {
    single::negative_over(INSNS)
}
#[cfg(test)]
mod tests {
    use super::*;
    use semulith_core::definition_rv64gc::Sem;
    use semulith_core::env::AccessWidth;
    fn cell(mode: PrivilegeMode) -> Cell {
        Cell {
            vector: Vector {
                format: 32,
                op: Op::Add,
                rm: 3,
                a: 0x3f80_0000,
                b: 0x3380_0000,
                c: 0,
                bits: 0x3f80_0001,
                flags: 1,
            },
            fused: 0,
            dynamic: true,
            rd: 5,
            mode,
            flags: 0,
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
    fn single_precision_numeric_instructions_match_independent_vectors() {
        assert_eq!(numeric_over(INSNS, 32), Ok(()));
    }
    #[test]
    fn wrong_numeric_effects_fail_named_observations() {
        let cases: [(&Sem, &str); 7] = [
            (&Sem::Nop, "floating registers differ"),
            (
                &Sem::Set(&Sem::Reg("rd"), &Sem::Lit(0x3f80_0001)),
                "integer registers differ",
            ),
            (
                &Sem::Set(&Sem::FReg("rd"), &Sem::Lit(0x3f80_0001)),
                "floating registers differ",
            ),
            (
                &Sem::Set(&Sem::FReg("rd"), &Sem::Lit(0xffff_ffff_7fc0_0000)),
                "floating registers differ",
            ),
            (
                &Sem::Set(&Sem::FReg("rd"), &Sem::Lit(0xffff_ffff_3f80_0001)),
                "CSR owners differ",
            ),
            (
                &Sem::Set(
                    &Sem::FReg("rd"),
                    &Sem::FBox(
                        32,
                        &Sem::FAdd(
                            32,
                            &Sem::Lit(0),
                            &Sem::FUnbox(32, &Sem::FReg("rs1")),
                            &Sem::FUnbox(32, &Sem::FReg("rs2")),
                        ),
                    ),
                ),
                "floating registers differ",
            ),
            (
                &Sem::Set(
                    &Sem::FReg("rd"),
                    &Sem::FBox(
                        32,
                        &Sem::FSub(
                            32,
                            &Sem::Rounding(&Sem::Field("rm")),
                            &Sem::FUnbox(32, &Sem::FReg("rs1")),
                            &Sem::FUnbox(32, &Sem::FReg("rs2")),
                        ),
                    ),
                ),
                "floating registers differ",
            ),
        ];
        for (effect, reason) in cases {
            let error = cell(PrivilegeMode::M)
                .check(&wrong_table("fadd.s", effect))
                .expect_err(reason);
            assert!(error.contains(reason), "{error}");
        }
    }
    #[test]
    fn wrong_numeric_instruction_routes_are_rejected() {
        for (name, replacement) in [
            ("fsub.s", "fadd.s"),
            ("fmul.s", "fdiv.s"),
            ("fsqrt.s", "fcvt.s.w"),
            ("fmin.s", "fmax.s"),
            ("feq.s", "flt.s"),
            ("fclass.s", "fmv.x.w"),
            ("fcvt.w.s", "fcvt.wu.s"),
            ("fcvt.l.s", "fcvt.w.s"),
            ("fcvt.s.lu", "fcvt.s.l"),
            ("fmadd.s", "fmsub.s"),
            ("fmsub.s", "fmadd.s"),
            ("fnmsub.s", "fmadd.s"),
            ("fnmadd.s", "fmadd.s"),
        ] {
            let effect = INSNS
                .iter()
                .find(|row| row.name == replacement)
                .unwrap()
                .effect;
            let error = numeric_over(&wrong_table(name, effect), 32).expect_err(name);
            assert!(
                error.contains("registers differ") || error.contains("CSR owners differ"),
                "{name} via {replacement}: {error}"
            );
        }
    }

    #[test]
    fn corrupted_numeric_captures_fail_every_auditor_component() {
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
        bad.csrs[CSR_FRM] ^= 1;
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
    #[test]
    fn double_precision_numeric_instructions_match_independent_vectors() {
        assert_eq!(numeric_over(INSNS, 64), Ok(()));
    }
    #[test]
    fn wrong_double_numeric_instruction_routes_are_rejected() {
        for (name, replacement) in [
            ("fadd.d", "fadd.s"),
            ("fsub.d", "fadd.d"),
            ("fmul.d", "fdiv.d"),
            ("fsqrt.d", "fcvt.d.w"),
            ("fmin.d", "fmax.d"),
            ("feq.d", "flt.d"),
            ("fclass.d", "fmv.x.d"),
            ("fcvt.w.d", "fcvt.wu.d"),
            ("fcvt.l.d", "fcvt.w.d"),
            ("fcvt.d.lu", "fcvt.d.l"),
            ("fmadd.d", "fmsub.d"),
            ("fmsub.d", "fmadd.d"),
            ("fnmsub.d", "fmadd.d"),
            ("fnmadd.d", "fmadd.d"),
            ("fcvt.s.d", "fcvt.d.s"),
            ("fcvt.d.s", "fcvt.s.d"),
        ] {
            let effect = INSNS
                .iter()
                .find(|row| row.name == replacement)
                .unwrap()
                .effect;
            let error = numeric_over(&wrong_table(name, effect), 64).expect_err(name);
            assert!(
                error.contains("registers differ") || error.contains("CSR owners differ"),
                "{name} via {replacement}: {error}"
            );
        }
    }
}
