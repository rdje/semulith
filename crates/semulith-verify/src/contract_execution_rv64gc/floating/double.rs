//! Literal D transfers, mixed-format rules, enabled FS states and refusals.
use super::*;
use semulith_core::env::AccessWidth;
const RAW: [u64; 16] = [
    0,
    0x8000_0000_0000_0000,
    1,
    0x8000_0000_0000_0001,
    0x0010_0000_0000_0000,
    0x3ff0_0000_0000_0000,
    0xbff0_0000_0000_0000,
    0x7ff0_0000_0000_0000,
    0xfff0_0000_0000_0000,
    0x7ff8_1234_5678_9abc,
    0x7ff0_1234_5678_9abc,
    0xfff8_1234_5678_9abc,
    0xfff0_1234_5678_9abc,
    0xffff_ffff_3f80_0000,
    0xffff_ffff_7fa1_2345,
    0x1234_5678_3f80_0000,
];
const DEST: [u32; 6] = [0, 5, 6, 7, 8, 31];
const CANON: u64 = 0x7ff8_0000_0000_0000;
const ONE: u64 = 0x3ff0_0000_0000_0000;
fn each(
    mut check: impl FnMut(PrivilegeMode, u32, u64) -> Result<(), String>,
) -> Result<(), String> {
    for mode in [PrivilegeMode::M, PrivilegeMode::S, PrivilegeMode::U] {
        for rd in DEST {
            for flags in [0, 31] {
                check(mode, rd, flags)?;
            }
        }
    }
    Ok(())
}
fn extent(actual: usize, expected: usize) -> Result<(), String> {
    if actual != expected {
        return Err(format!("D matrix extent {actual}, expected {expected}"));
    }
    Ok(())
}
fn write_float(expected: &mut Observation, rd: u32, bits: u64) {
    expected.f[rd as usize] = bits;
    expected.csrs[CSR_MSTATUS] |= 3 << 13;
}
fn sign_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
    for a in RAW {
        for b in RAW {
            for kind in 0..3 {
                each(|mode, rd, flags| {
                    let word =
                        (0x11 << 25) | (7 << 20) | (6 << 15) | (kind << 12) | (rd << 7) | 0x53;
                    let (mut h, mut o) = seed(word, mode, 2, 7, flags);
                    h.write_f(6, a);
                    h.write_f(7, b);
                    let sign = match kind {
                        0 => b,
                        1 => !b,
                        _ => a ^ b,
                    } & (1 << 63);
                    let mut expected = retired(&mut h, &o);
                    write_float(&mut expected, rd, (a & 0x7fff_ffff_ffff_ffff) | sign);
                    execute(&mut h, &mut o, table, &expected).map_err(|e| {
                        format!("D sign kind={kind} a={a:x} b={b:x} {mode:?} rd={rd}: {e}")
                    })?;
                    count += 1;
                    Ok(())
                })?;
            }
        }
    }
    extent(count, 27648)
}
fn move_word(into_float: bool, rd: u32) -> u32 {
    ((if into_float { 0x79 } else { 0x71 }) << 25) | (6 << 15) | (rd << 7) | 0x53
}
fn moves_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
    for raw in RAW {
        for into_float in [false, true] {
            each(|mode, rd, flags| {
                let (mut h, mut o) = seed(move_word(into_float, rd), mode, 2, 7, flags);
                h.write_x(6, raw);
                h.write_f(6, raw);
                let mut expected = retired(&mut h, &o);
                if into_float {
                    write_float(&mut expected, rd, raw);
                } else if rd != 0 {
                    expected.x[rd as usize] = raw;
                }
                execute(&mut h, &mut o, table, &expected)?;
                count += 1;
                Ok(())
            })?;
        }
    }
    extent(count, 1152)
}
fn memory_word(load: bool, register: u32, offset: u32) -> u32 {
    if load {
        (offset << 20) | (6 << 15) | (3 << 12) | (register << 7) | 7
    } else {
        ((offset >> 5) << 25)
            | (register << 20)
            | (6 << 15)
            | (3 << 12)
            | ((offset & 31) << 7)
            | 0x27
    }
}
fn memory_over(table: &[InsnDef]) -> Result<(), String> {
    let mut loads = 0;
    let mut stores = 0;
    for raw in RAW {
        for offset in [0, 8, 16] {
            each(|mode, rd, flags| {
                let (mut h, mut o) = seed(memory_word(true, rd, offset), mode, 2, 7, flags);
                h.write_x(6, DATA);
                o.memory.load_image(0x80, &[0x69; 32]);
                o.memory
                    .load_image(0x80 + offset as usize, &raw.to_le_bytes());
                let mut expected = retired(&mut h, &o);
                expected.requests.push(Request::Load {
                    width: AccessWidth::D,
                    addr: DATA + u64::from(offset),
                });
                write_float(&mut expected, rd, raw);
                execute(&mut h, &mut o, table, &expected)?;
                loads += 1;
                Ok(())
            })?;
            for mode in [PrivilegeMode::M, PrivilegeMode::S, PrivilegeMode::U] {
                for source in [0, 6, 31] {
                    for flags in [0, 31] {
                        let (mut h, mut o) =
                            seed(memory_word(false, source, offset), mode, 2, 7, flags);
                        h.write_x(6, DATA);
                        h.write_f(source as u8, raw);
                        o.memory.load_image(0x80, &[0x69; 32]);
                        let mut expected = retired(&mut h, &o);
                        expected.requests.push(Request::Store {
                            width: AccessWidth::D,
                            addr: DATA + u64::from(offset),
                            data: raw,
                        });
                        expected.memory[0x80 + offset as usize..0x88 + offset as usize]
                            .copy_from_slice(&raw.to_le_bytes());
                        execute(&mut h, &mut o, table, &expected)?;
                        stores += 1;
                    }
                }
            }
        }
    }
    extent(loads, 1728)?;
    extent(stores, 864)
}
fn identical_writes_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
    for load in [false, true] {
        each(|mode, rd, flags| {
            let raw = 0x7ff0_1234_5678_9abc_u64;
            let word = if load {
                memory_word(true, rd, 0)
            } else {
                move_word(true, rd)
            };
            let (mut h, mut o) = seed(word, mode, 2, 7, flags);
            h.write_f(rd as u8, raw);
            h.write_x(6, if load { DATA } else { raw });
            o.memory.load_image(0x80, &raw.to_le_bytes());
            let mut expected = retired(&mut h, &o);
            if load {
                expected.requests.push(Request::Load {
                    width: AccessWidth::D,
                    addr: DATA,
                });
            }
            write_float(&mut expected, rd, raw);
            execute(&mut h, &mut o, table, &expected)?;
            count += 1;
            Ok(())
        })?;
    }
    extent(count, 72)
}
fn enabled_states_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
    let mut seen = Vec::new();
    for vector in vectors(64)? {
        if seen.contains(&vector.op) {
            continue;
        }
        seen.push(vector.op);
        for fused in 0..if vector.op == Op::Fma { 4 } else { 1 } {
            for fs in [1, 3] {
                each(|mode, rd, flags| {
                    let cell = Cell {
                        vector,
                        fused,
                        dynamic: false,
                        rd,
                        mode,
                        flags,
                    };
                    let (mut h, mut o, expected) = cell.fixture_fs(fs);
                    execute(&mut h, &mut o, table, &expected)?;
                    count += 1;
                    Ok(())
                })?;
            }
        }
    }
    extent(seen.len(), 22)?;
    // The other seven forms: three sign operations, two moves, load and store.
    for kind in 0..7 {
        for fs in [1, 3] {
            each(|mode, rd, flags| {
                let word = match kind {
                    0..=2 => (0x11 << 25) | (7 << 20) | (6 << 15) | (kind << 12) | (rd << 7) | 0x53,
                    3 | 4 => move_word(kind == 4, rd),
                    _ => memory_word(kind == 5, rd, 0),
                };
                let (mut h, mut o) = seed(word, mode, fs, 7, flags);
                h.write_f(6, ONE);
                h.write_f(7, ONE | (1 << 63));
                h.write_x(6, if kind >= 5 { DATA } else { ONE });
                if kind == 6 {
                    h.write_f(rd as u8, ONE);
                }
                o.memory.load_image(0x80, &ONE.to_le_bytes());
                let mut expected = retired(&mut h, &o);
                match kind {
                    0 | 2 => write_float(&mut expected, rd, ONE | (1 << 63)),
                    1 | 4 => write_float(&mut expected, rd, ONE),
                    3 => {
                        if rd != 0 {
                            expected.x[rd as usize] = ONE;
                        }
                    }
                    5 => {
                        expected.requests.push(Request::Load {
                            width: AccessWidth::D,
                            addr: DATA,
                        });
                        write_float(&mut expected, rd, ONE);
                    }
                    _ => {
                        expected.requests.push(Request::Store {
                            width: AccessWidth::D,
                            addr: DATA,
                            data: ONE,
                        });
                    }
                }
                execute(&mut h, &mut o, table, &expected)?;
                count += 1;
                Ok(())
            })?;
        }
    }
    extent(count, 2304)
}
fn boxed_single_as_double_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
    for low in [0, 0x3f80_0000, 0x7fa1_2345] {
        for op in [
            Op::Add,
            Op::Sub,
            Op::Mul,
            Op::Div,
            Op::Sqrt,
            Op::Fma,
            Op::Min,
            Op::Max,
            Op::Eq,
            Op::Lt,
            Op::Le,
            Op::Class,
            Op::ToI32,
            Op::ToU32,
            Op::ToI64,
            Op::ToU64,
            Op::ToSingle,
        ] {
            let masks: &[u32] = if op == Op::Fma {
                &[1, 2, 4, 7]
            } else if matches!(
                op,
                Op::Sqrt | Op::Class | Op::ToI32 | Op::ToU32 | Op::ToI64 | Op::ToU64 | Op::ToSingle
            ) {
                &[1]
            } else {
                &[1, 2, 3]
            };
            for &nan_mask in masks {
                for fused in 0..if op == Op::Fma { 4 } else { 1 } {
                    for rm in 0..if op.rounded() { 5 } else { 1 } {
                        for dynamic in
                            [false, true]
                                .into_iter()
                                .take(if op.rounded() { 2 } else { 1 })
                        {
                            each(|mode, rd, flags| {
                                let word = op.word(
                                    if op == Op::ToSingle { 32 } else { 64 },
                                    rd,
                                    if dynamic { 7 } else { rm },
                                    fused,
                                );
                                let (mut h, mut o) = seed(
                                    word,
                                    mode,
                                    2,
                                    if dynamic { u64::from(rm) } else { 7 },
                                    flags,
                                );
                                for (i, reg) in [6, 7, 8].into_iter().enumerate() {
                                    h.write_f(
                                        reg,
                                        if nan_mask & (1 << i) != 0 {
                                            boxed(low)
                                        } else {
                                            ONE
                                        },
                                    );
                                }
                                let mut expected = retired(&mut h, &o);
                                let (bits, raised) = match op {
                                    Op::Min | Op::Max => {
                                        (if nan_mask == 3 { CANON } else { ONE }, 0)
                                    }
                                    Op::Eq => (0, 0),
                                    Op::Lt | Op::Le => (0, 16),
                                    Op::Class => (512, 0),
                                    Op::ToI32 => (0x7fff_ffff, 16),
                                    Op::ToU32 => (u64::MAX, 16),
                                    Op::ToI64 => (0x7fff_ffff_ffff_ffff, 16),
                                    Op::ToU64 => (u64::MAX, 16),
                                    Op::ToSingle => (boxed(0x7fc0_0000), 0),
                                    _ => (CANON, 0),
                                };
                                if op.integer_destination() {
                                    if rd != 0 {
                                        expected.x[rd as usize] = bits;
                                    }
                                } else {
                                    write_float(&mut expected, rd, bits);
                                }
                                expected.csrs[CSR_FFLAGS] |= raised;
                                if flags | raised != flags {
                                    expected.csrs[CSR_MSTATUS] |= 3 << 13;
                                }
                                execute(&mut h, &mut o, table, &expected).map_err(|e| format!("boxed single as D {op:?} low={low:x} mask={nan_mask} fused={fused} rm={rm}/{dynamic} rd={rd}: {e}"))?;
                                count += 1;
                                Ok(())
                            })?;
                        }
                    }
                }
            }
        }
    }
    extent(count, 38448)
}
// Exact widening literals, independently re-derived with specfp before execution.
const WIDEN: [(u64, u64, u64); 12] = [
    (0, 0, 0),
    (0x8000_0000, 0x8000_0000_0000_0000, 0),
    (1, 0x36a0_0000_0000_0000, 0),
    (0x8000_0001, 0xb6a0_0000_0000_0000, 0),
    (0x0080_0000, 0x3810_0000_0000_0000, 0),
    (0x3f80_0000, ONE, 0),
    (0xbf80_0000, 0xbff0_0000_0000_0000, 0),
    (0x7f80_0000, 0x7ff0_0000_0000_0000, 0),
    (0xff80_0000, 0xfff0_0000_0000_0000, 0),
    (0x7fc1_2345, CANON, 0),
    (0x7fa1_2345, CANON, 16),
    (0xffff_ffff, CANON, 0),
];
fn widening_boxes_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
    for (low, bits, raised) in WIDEN {
        for upper in [0xffff_ffff, 0x1234_5678, 0] {
            for rm in 0..5 {
                for dynamic in [false, true] {
                    each(|mode, rd, flags| {
                        let word = Op::FromSingle.word(64, rd, if dynamic { 7 } else { rm }, 0);
                        let (mut h, mut o) = seed(
                            word,
                            mode,
                            2,
                            if dynamic { u64::from(rm) } else { 7 },
                            flags,
                        );
                        h.write_f(6, (upper << 32) | low);
                        let mut expected = retired(&mut h, &o);
                        write_float(
                            &mut expected,
                            rd,
                            if upper == 0xffff_ffff { bits } else { CANON },
                        );
                        expected.csrs[CSR_FFLAGS] |= if upper == 0xffff_ffff { raised } else { 0 };
                        execute(&mut h, &mut o, table, &expected)?;
                        count += 1;
                        Ok(())
                    })?;
                }
            }
        }
    }
    extent(count, 12960)
}
fn directed_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
    for rm in 0..5 {
        for dynamic in [false, true] {
            for (op, a, b, c, bits, raised) in [
                (
                    Op::Add,
                    ONE,
                    0x3ca0_0000_0000_0000,
                    0,
                    if rm == 3 || rm == 4 { ONE + 1 } else { ONE },
                    1,
                ),
                (
                    Op::Add,
                    0xbff0_0000_0000_0000,
                    0xbca0_0000_0000_0000,
                    0,
                    if rm == 2 || rm == 4 {
                        0xbff0_0000_0000_0001
                    } else {
                        0xbff0_0000_0000_0000
                    },
                    1,
                ),
                (
                    Op::Mul,
                    0x0010_0000_0000_0000,
                    0x3fef_ffff_ffff_ffff,
                    0,
                    if rm == 1 || rm == 2 {
                        0x000f_ffff_ffff_ffff
                    } else {
                        0x0010_0000_0000_0000
                    },
                    3,
                ),
                (
                    Op::Mul,
                    0x0010_0000_0000_0000,
                    0x3fef_ffff_ffff_fffe,
                    0,
                    0x000f_ffff_ffff_ffff,
                    0,
                ),
                (
                    Op::Fma,
                    ONE + 1,
                    0x3fef_ffff_ffff_fffe,
                    0xbff0_0000_0000_0000,
                    0xb970_0000_0000_0000,
                    0,
                ),
            ] {
                for fused in 0..if op == Op::Fma { 4 } else { 1 } {
                    each(|mode, rd, flags| {
                        Cell {
                            vector: Vector {
                                format: 64,
                                op,
                                rm,
                                a,
                                b,
                                c,
                                bits,
                                flags: raised,
                            },
                            fused,
                            dynamic,
                            rd,
                            mode,
                            flags,
                        }
                        .check(table)?;
                        count += 1;
                        Ok(())
                    })?;
                }
            }
            for a in [
                0x7ff0_0000_0000_0000,
                0xfff0_0000_0000_0000,
                0x7ff8_1234_5678_9abc,
                0x7ff0_1234_5678_9abc,
                0x43f0_0000_0000_0000,
                0xc3f0_0000_0000_0000,
            ] {
                for op in [Op::ToI32, Op::ToU32, Op::ToI64, Op::ToU64] {
                    let negative = a & (1 << 63) != 0;
                    let bits = match (op, negative) {
                        (Op::ToI32, true) => 0x8000_0000,
                        (Op::ToI32, false) => 0x7fff_ffff,
                        (Op::ToU32, true) | (Op::ToU64, true) => 0,
                        (Op::ToU32, false) => 0xffff_ffff,
                        (Op::ToI64, true) => 0x8000_0000_0000_0000,
                        (Op::ToI64, false) => 0x7fff_ffff_ffff_ffff,
                        (Op::ToU64, false) => u64::MAX,
                        _ => unreachable!(),
                    };
                    each(|mode, rd, flags| {
                        Cell {
                            vector: Vector {
                                format: 64,
                                op,
                                rm,
                                a,
                                b: 0,
                                c: 0,
                                bits,
                                flags: 16,
                            },
                            fused: 0,
                            dynamic,
                            rd,
                            mode,
                            flags,
                        }
                        .check(table)?;
                        count += 1;
                        Ok(())
                    })?;
                }
            }
        }
    }
    extent(count, 11520)
}
fn d_rows() -> Result<Vec<&'static InsnDef>, String> {
    let rows: Vec<_> = INSNS
        .iter()
        .filter(|r| matches!(r.from, "rv_d" | "rv64_d"))
        .collect();
    extent(rows.len(), 32)?;
    extent(
        rows.iter().filter(|r| r.operands.contains(&"rm")).count(),
        19,
    )?;
    Ok(rows)
}
fn form_word(row: &InsnDef, register: u32, rm: u32) -> u32 {
    let mut word = row.value;
    for (field, value, shift) in [
        ("rd", register, 7),
        ("rs1", 6, 15),
        ("rs2", if row.name == "fsd" { register } else { 7 }, 20),
        ("rs3", 8, 27),
        ("rm", rm, 12),
    ] {
        if row.operands.contains(&field) {
            word |= value << shift;
        }
    }
    word
}
fn fs_off_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
    for row in d_rows()? {
        each(|mode, reg, flags| {
            let word = form_word(row, reg, 0);
            let (mut h, mut o) = seed(word, mode, 0, 0, flags);
            h.write_x(6, if reg.is_multiple_of(2) { DATA + 1 } else { 0 });
            let expected = trapped(&mut h, &o, 2, u64::from(word));
            execute(&mut h, &mut o, table, &expected)
                .map_err(|e| format!("D FS Off {} {mode:?} reg={reg}: {e}", row.name))?;
            count += 1;
            Ok(())
        })?;
    }
    extent(count, 1152)
}
fn rounding_refusals_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
    let settings: Vec<_> = [5, 6]
        .into_iter()
        .flat_map(|rm| (0..8).map(move |frm| (rm, frm)))
        .chain([5, 6, 7].into_iter().map(|frm| (7, frm)))
        .collect();
    extent(settings.len(), 19)?;
    for row in d_rows()?.into_iter().filter(|r| r.operands.contains(&"rm")) {
        for &(rm, frm) in &settings {
            each(|mode, rd, flags| {
                let word = form_word(row, rd, rm);
                let (mut h, mut o) = seed(word, mode, 2, frm, flags);
                for reg in [6, 7, 8] {
                    h.write_f(reg, ONE);
                }
                let expected = trapped(&mut h, &o, 2, u64::from(word));
                execute(&mut h, &mut o, table, &expected).map_err(|e| {
                    format!(
                        "D reserved {} rm={rm} frm={frm} {mode:?} rd={rd}: {e}",
                        row.name
                    )
                })?;
                count += 1;
                Ok(())
            })?;
        }
    }
    extent(count, 12996)
}
fn memory_faults_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
    for load in [false, true] {
        for addr in [DATA + 1, 0] {
            each(|mode, reg, flags| {
                let word = memory_word(load, reg, 0);
                let (mut h, mut o) = seed(word, mode, 2, 7, flags);
                h.write_x(6, addr);
                let cause = match (load, addr == 0) {
                    (true, false) => 4,
                    (true, true) => 5,
                    (false, false) => 6,
                    (false, true) => 7,
                };
                let mut expected = trapped(&mut h, &o, cause, addr);
                if addr == 0 {
                    expected.requests.push(if load {
                        Request::Load {
                            width: AccessWidth::D,
                            addr,
                        }
                    } else {
                        Request::Store {
                            width: AccessWidth::D,
                            addr,
                            data: expected.f[reg as usize],
                        }
                    });
                }
                execute(&mut h, &mut o, table, &expected)?;
                count += 1;
                Ok(())
            })?;
        }
    }
    extent(count, 144)
}
pub(super) fn positive_over(table: &[InsnDef]) -> Result<(), String> {
    sign_over(table)?;
    moves_over(table)?;
    memory_over(table)?;
    identical_writes_over(table)?;
    enabled_states_over(table)?;
    boxed_single_as_double_over(table)?;
    widening_boxes_over(table)?;
    directed_over(table)
}
pub(super) fn negative_over(table: &[InsnDef]) -> Result<(), String> {
    fs_off_over(table)?;
    rounding_refusals_over(table)?;
    memory_faults_over(table)
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn d_transfer_sign_format_and_directed_rules() {
        assert_eq!(positive_over(INSNS), Ok(()));
    }
    #[test]
    fn every_d_form_refuses_fs_off_and_every_rounded_form_refuses_reserved_modes() {
        assert_eq!(negative_over(INSNS), Ok(()));
    }
    fn wrong_table(
        name: &str,
        effect: &'static semulith_core::definition_rv64gc::Sem,
    ) -> Vec<InsnDef> {
        INSNS
            .iter()
            .map(|r| InsnDef {
                from: r.from,
                name: r.name,
                mask: r.mask,
                value: r.value,
                operands: r.operands,
                source: r.source,
                effect: if r.name == name { effect } else { r.effect },
                length: r.length,
                expansion: r.expansion,
            })
            .collect()
    }
    #[test]
    fn wrong_double_transfer_sign_memory_and_format_effects_are_rejected() {
        use semulith_core::definition_rv64gc::Sem;
        for (name, replacement) in [
            ("fsgnj.d", "fsgnjn.d"),
            ("fsgnjn.d", "fsgnjx.d"),
            ("fsgnjx.d", "fsgnj.d"),
        ] {
            let effect = INSNS.iter().find(|r| r.name == replacement).unwrap().effect;
            assert!(sign_over(&wrong_table(name, effect))
                .unwrap_err()
                .contains("floating registers differ"));
        }
        for effect in [
            &Sem::Set(&Sem::Reg("rd"), &Sem::Bits(31, 0, &Sem::FReg("rs1"))),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Sext(64, &Sem::Bits(31, 0, &Sem::FReg("rs1"))),
            ),
            &Sem::Set(&Sem::Reg("rd"), &Sem::FUnbox(32, &Sem::FReg("rs1"))),
        ] {
            assert!(moves_over(&wrong_table("fmv.x.d", effect)).is_err());
        }
        for effect in [
            &Sem::Set(&Sem::FReg("rd"), &Sem::FBox(32, &Sem::Reg("rs1"))),
            &Sem::Set(&Sem::FReg("rd"), &Sem::Bits(31, 0, &Sem::Reg("rs1"))),
        ] {
            assert!(moves_over(&wrong_table("fmv.d.x", effect)).is_err());
        }
        const ADDRESS: &Sem = &Sem::Add(&Sem::Reg("rs1"), &Sem::Sext(64, &Sem::Imm("imm12")));
        for effect in [
            &Sem::Set(
                &Sem::FReg("rd"),
                &Sem::Load(&Sem::Lit(32), &Sem::Lit(0), ADDRESS),
            ),
            &Sem::Set(
                &Sem::FReg("rd"),
                &Sem::FBox(32, &Sem::Load(&Sem::Lit(64), &Sem::Lit(0), ADDRESS)),
            ),
        ] {
            assert!(memory_over(&wrong_table("fld", effect)).is_err());
        }
        for effect in [
            &Sem::Store(&Sem::Lit(32), ADDRESS, &Sem::FReg("rs2")),
            &Sem::Store(&Sem::Lit(64), ADDRESS, &Sem::FUnbox(32, &Sem::FReg("rs2"))),
            &Sem::Nop,
        ] {
            assert!(memory_over(&wrong_table("fsd", effect)).is_err());
        }
        assert!(widening_boxes_over(&wrong_table(
            "fcvt.d.s",
            &Sem::Set(
                &Sem::FReg("rd"),
                &Sem::FToF(64, 32, &Sem::Rounding(&Sem::Field("rm")), &Sem::FReg("rs1"))
            )
        ))
        .is_err());
        assert!(boxed_single_as_double_over(&wrong_table(
            "fcvt.s.d",
            &Sem::Set(
                &Sem::FReg("rd"),
                &Sem::FToF(32, 64, &Sem::Rounding(&Sem::Field("rm")), &Sem::FReg("rs1"))
            )
        ))
        .is_err());
    }
}
