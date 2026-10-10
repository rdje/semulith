//! Bit transfers and literal rule/refusal cases completing the F witness.
use super::*;
use semulith_core::env::AccessWidth;
const LOW: [u64; 12] = [
    0,
    0x8000_0000,
    1,
    0x8000_0001,
    0x0080_0000,
    0x3f80_0000,
    0xbf80_0000,
    0x7f80_0000,
    0xff80_0000,
    0x7fc1_2345,
    0x7fa1_2345,
    0xffff_ffff,
];
const UPPER: [u64; 3] = [0xffff_ffff, 0x1234_5678, 0];
const DEST: [u32; 6] = [0, 5, 6, 7, 8, 31];
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
        return Err(format!("matrix extent {actual}, expected {expected}"));
    }
    Ok(())
}
fn write_float(expected: &mut Observation, rd: u32, bits: u64) {
    expected.f[rd as usize] = boxed(bits);
    expected.csrs[CSR_MSTATUS] |= 3 << 13;
}
fn sign_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
    for a in LOW {
        for b in LOW {
            for invalid in 0..4 {
                for kind in 0..3 {
                    each(|mode, rd, flags| {
                        let word =
                            (0x10 << 25) | (7 << 20) | (6 << 15) | (kind << 12) | (rd << 7) | 0x53;
                        let (mut h, mut o) = seed(word, mode, 2, 7, flags);
                        h.write_f(
                            6,
                            if invalid & 1 != 0 {
                                0x1234_5678_0000_0000 | a
                            } else {
                                boxed(a)
                            },
                        );
                        h.write_f(
                            7,
                            if invalid & 2 != 0 {
                                0x1234_5678_0000_0000 | b
                            } else {
                                boxed(b)
                            },
                        );
                        let aa = if invalid & 1 != 0 { 0x7fc0_0000 } else { a };
                        let bb = if invalid & 2 != 0 { 0x7fc0_0000 } else { b };
                        let sign = match kind {
                            0 => bb,
                            1 => !bb,
                            _ => aa ^ bb,
                        } & 0x8000_0000;
                        let mut expected = retired(&mut h, &o);
                        write_float(&mut expected, rd, (aa & 0x7fff_ffff) | sign);
                        execute(&mut h, &mut o, table, &expected).map_err(|e| format!("sign kind={kind} a={a:x} b={b:x} invalid={invalid} {mode:?} rd={rd} flags={flags}: {e}"))?;
                        count += 1;
                        Ok(())
                    })?;
                }
            }
        }
    }
    extent(count, 62208)
}
fn moves_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
    for low in LOW {
        for upper in UPPER {
            for into_float in [false, true] {
                each(|mode, rd, flags| {
                    let raw = (upper << 32) | low;
                    let word = ((if into_float { 0x78 } else { 0x70 }) << 25)
                        | (6 << 15)
                        | (rd << 7)
                        | 0x53;
                    let (mut h, mut o) = seed(word, mode, 2, 7, flags);
                    h.write_x(6, raw);
                    h.write_f(6, raw);
                    let mut expected = retired(&mut h, &o);
                    if into_float {
                        write_float(&mut expected, rd, low);
                    } else if rd != 0 {
                        expected.x[rd as usize] = low as u32 as i32 as i64 as u64;
                    }
                    execute(&mut h, &mut o, table, &expected).map_err(|e| {
                        format!("move float={into_float} raw={raw:x} {mode:?} rd={rd}: {e}")
                    })?;
                    count += 1;
                    Ok(())
                })?;
            }
        }
    }
    extent(count, 2592)
}
fn memory_word(load: bool, register: u32, offset: u32) -> u32 {
    if load {
        (offset << 20) | (6 << 15) | (2 << 12) | (register << 7) | 7
    } else {
        ((offset >> 5) << 25)
            | (register << 20)
            | (6 << 15)
            | (2 << 12)
            | ((offset & 31) << 7)
            | 0x27
    }
}
fn memory_over(table: &[InsnDef]) -> Result<(), String> {
    let mut loads = 0;
    let mut stores = 0;
    for low in LOW {
        for offset in [0, 4, 8] {
            each(|mode, rd, flags| {
                let (mut h, mut o) = seed(memory_word(true, rd, offset), mode, 2, 7, flags);
                h.write_x(6, DATA);
                o.memory.load_image(0x80, &[0x69; 16]);
                o.memory
                    .load_image(0x80 + offset as usize, &(low as u32).to_le_bytes());
                let mut expected = retired(&mut h, &o);
                expected.requests.push(Request::Load {
                    width: AccessWidth::W,
                    addr: DATA + u64::from(offset),
                });
                write_float(&mut expected, rd, low);
                execute(&mut h, &mut o, table, &expected)?;
                loads += 1;
                Ok(())
            })?;
            for upper in UPPER {
                for mode in [PrivilegeMode::M, PrivilegeMode::S, PrivilegeMode::U] {
                    for source in [0, 6, 31] {
                        for flags in [0, 31] {
                            let (mut h, mut o) =
                                seed(memory_word(false, source, offset), mode, 2, 7, flags);
                            h.write_x(6, DATA);
                            h.write_f(source as u8, (upper << 32) | low);
                            o.memory.load_image(0x80, &[0x69; 16]);
                            let mut expected = retired(&mut h, &o);
                            expected.requests.push(Request::Store {
                                width: AccessWidth::W,
                                addr: DATA + u64::from(offset),
                                data: low,
                            });
                            expected.memory[0x80 + offset as usize..0x84 + offset as usize]
                                .copy_from_slice(&(low as u32).to_le_bytes());
                            execute(&mut h, &mut o, table, &expected)?;
                            stores += 1;
                        }
                    }
                }
            }
        }
    }
    extent(loads, 1296)?;
    extent(stores, 1944)
}
fn identical_writes_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
    for load in [false, true] {
        each(|mode, rd, flags| {
            let low = 0x7fa1_2345;
            let word = if load {
                memory_word(true, rd, 0)
            } else {
                (0x78 << 25) | (6 << 15) | (rd << 7) | 0x53
            };
            let (mut h, mut o) = seed(word, mode, 2, 7, flags);
            h.write_f(rd as u8, boxed(low));
            h.write_x(6, if load { DATA } else { low });
            o.memory.load_image(0x80, &(low as u32).to_le_bytes());
            let mut expected = retired(&mut h, &o);
            if load {
                expected.requests.push(Request::Load {
                    width: AccessWidth::W,
                    addr: DATA,
                });
            }
            write_float(&mut expected, rd, low);
            execute(&mut h, &mut o, table, &expected)?;
            count += 1;
            Ok(())
        })?;
    }
    extent(count, 72)
}
fn invalid_boxes_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
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
    ] {
        let masks: &[u32] = if op == Op::Fma {
            &[1, 2, 4, 7]
        } else if matches!(
            op,
            Op::Sqrt | Op::Class | Op::ToI32 | Op::ToU32 | Op::ToI64 | Op::ToU64
        ) {
            &[1]
        } else {
            &[1, 2, 3]
        };
        for &invalid in masks {
            for fused in 0..if op == Op::Fma { 4 } else { 1 } {
                for rm in 0..if op.rounded() { 5 } else { 1 } {
                    for dynamic in [false, true]
                        .into_iter()
                        .take(if op.rounded() { 2 } else { 1 })
                    {
                        each(|mode, rd, flags| {
                            let word = op.word(32, rd, if dynamic { 7 } else { rm }, fused);
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
                                    if invalid & (1 << i) != 0 {
                                        0x1234_5678_3f80_0000
                                    } else {
                                        boxed(0x3f80_0000)
                                    },
                                );
                            }
                            let mut expected = retired(&mut h, &o);
                            let (bits, raised) = match op {
                                Op::Min | Op::Max => (
                                    if invalid == 3 {
                                        0x7fc0_0000
                                    } else {
                                        0x3f80_0000
                                    },
                                    0,
                                ),
                                Op::Eq => (0, 0),
                                Op::Lt | Op::Le => (0, 16),
                                Op::Class => (512, 0),
                                Op::ToI32 => (0x7fff_ffff, 16),
                                Op::ToU32 => (u64::MAX, 16),
                                Op::ToI64 => (0x7fff_ffff_ffff_ffff, 16),
                                Op::ToU64 => (u64::MAX, 16),
                                _ => (0x7fc0_0000, 0),
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
                            execute(&mut h, &mut o, table, &expected).map_err(|e| format!("invalid box {op:?} mask={invalid} fused={fused} rm={rm}/{dynamic} rd={rd}: {e}"))?;
                            count += 1;
                            Ok(())
                        })?;
                    }
                }
            }
        }
    }
    extent(count, 12456)
}
// Literal IEEE/RVI cases, independently re-derived with specfp in the slice audit.
// No production FP helper is used in any expected value.
fn directed_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
    for rm in 0..5 {
        for dynamic in [false, true] {
            for (op, a, b, c, bits, raised) in [
                (
                    Op::Add,
                    0x3f80_0000,
                    0x3380_0000,
                    0,
                    if rm == 3 || rm == 4 {
                        0x3f80_0001
                    } else {
                        0x3f80_0000
                    },
                    1,
                ),
                (
                    Op::Add,
                    0xbf80_0000,
                    0xb380_0000,
                    0,
                    if rm == 2 || rm == 4 {
                        0xbf80_0001
                    } else {
                        0xbf80_0000
                    },
                    1,
                ),
                (
                    Op::Mul,
                    0x0080_0000,
                    0x3f7f_ffff,
                    0,
                    if rm == 1 || rm == 2 {
                        0x007f_ffff
                    } else {
                        0x0080_0000
                    },
                    3,
                ),
                (Op::Mul, 0x0080_0000, 0x3f7f_fffe, 0, 0x007f_ffff, 0),
                (
                    Op::Fma,
                    0x3f80_0001,
                    0x3f7f_fffe,
                    0xbf80_0000,
                    0xa880_0000,
                    0,
                ),
            ] {
                for fused in 0..if op == Op::Fma { 4 } else { 1 } {
                    each(|mode, rd, flags| {
                        Cell {
                            vector: Vector {
                                format: 32,
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
                0x7f80_0000,
                0xff80_0000,
                0x7fc1_2345,
                0x7fa1_2345,
                0x5f80_0000,
                0xdf80_0000,
            ] {
                for op in [Op::ToI32, Op::ToU32, Op::ToI64, Op::ToU64] {
                    let negative = a & 0x8000_0000 != 0;
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
                                format: 32,
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
fn f_rows() -> Result<Vec<&'static InsnDef>, String> {
    let rows: Vec<_> = INSNS
        .iter()
        .filter(|r| matches!(r.from, "rv_f" | "rv64_f"))
        .collect();
    extent(rows.len(), 30)?;
    extent(
        rows.iter().filter(|r| r.operands.contains(&"rm")).count(),
        17,
    )?;
    Ok(rows)
}
fn form_word(row: &InsnDef, register: u32, rm: u32) -> u32 {
    let mut word = row.value;
    for (field, value, shift) in [
        ("rd", register, 7),
        ("rs1", 6, 15),
        ("rs2", if row.name == "fsw" { register } else { 7 }, 20),
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
    for row in f_rows()? {
        each(|mode, reg, flags| {
            let word = form_word(row, reg, 0);
            let (mut h, mut o) = seed(word, mode, 0, 0, flags);
            // Gate must win over either data misalignment or an unmapped data address.
            h.write_x(6, if reg.is_multiple_of(2) { DATA + 1 } else { 0 });
            let expected = trapped(&mut h, &o, 2, u64::from(word));
            execute(&mut h, &mut o, table, &expected)
                .map_err(|e| format!("FS Off {} {mode:?} reg={reg}: {e}", row.name))?;
            count += 1;
            Ok(())
        })?;
    }
    extent(count, 1080)
}
fn rounding_refusals_over(table: &[InsnDef]) -> Result<(), String> {
    let mut count = 0;
    let settings: Vec<_> = [5, 6]
        .into_iter()
        .flat_map(|rm| (0..8).map(move |frm| (rm, frm)))
        .chain([5, 6, 7].into_iter().map(|frm| (7, frm)))
        .collect();
    extent(settings.len(), 19)?;
    for row in f_rows()?.into_iter().filter(|r| r.operands.contains(&"rm")) {
        for &(rm, frm) in &settings {
            each(|mode, rd, flags| {
                let word = form_word(row, rd, rm);
                let (mut h, mut o) = seed(word, mode, 2, frm, flags);
                for reg in [6, 7, 8] {
                    h.write_f(reg, boxed(0x3f80_0000));
                }
                let expected = trapped(&mut h, &o, 2, u64::from(word));
                execute(&mut h, &mut o, table, &expected).map_err(|e| {
                    format!(
                        "reserved {} rm={rm} frm={frm} {mode:?} rd={rd}: {e}",
                        row.name
                    )
                })?;
                count += 1;
                Ok(())
            })?;
        }
    }
    extent(count, 11628)
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
                            width: AccessWidth::W,
                            addr,
                        }
                    } else {
                        Request::Store {
                            width: AccessWidth::W,
                            addr,
                            data: expected.f[reg as usize] & 0xffff_ffff,
                        }
                    });
                }
                execute(&mut h, &mut o, table, &expected).map_err(|e| {
                    format!("memory fault load={load} addr={addr:x} {mode:?} reg={reg}: {e}")
                })?;
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
    invalid_boxes_over(table)?;
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
    fn f_transfer_sign_boxing_and_directed_rules() {
        assert_eq!(positive_over(INSNS), Ok(()));
    }
    #[test]
    fn every_f_form_refuses_fs_off_and_every_rounded_form_refuses_reserved_modes() {
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
    fn wrong_transfer_sign_and_memory_effects_are_rejected() {
        use semulith_core::definition_rv64gc::Sem;
        for (name, replacement) in [
            ("fsgnj.s", "fsgnjn.s"),
            ("fsgnjn.s", "fsgnjx.s"),
            ("fsgnjx.s", "fsgnj.s"),
        ] {
            let effect = INSNS.iter().find(|r| r.name == replacement).unwrap().effect;
            assert!(sign_over(&wrong_table(name, effect))
                .unwrap_err()
                .contains("floating registers differ"));
        }
        for effect in [
            &Sem::Set(&Sem::Reg("rd"), &Sem::Bits(31, 0, &Sem::FReg("rs1"))),
            &Sem::Set(&Sem::Reg("rd"), &Sem::FReg("rs1")),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Sext(64, &Sem::FUnbox(32, &Sem::FReg("rs1"))),
            ),
        ] {
            assert!(moves_over(&wrong_table("fmv.x.w", effect))
                .unwrap_err()
                .contains("integer registers differ"));
        }
        assert!(moves_over(&wrong_table(
            "fmv.w.x",
            &Sem::Set(&Sem::FReg("rd"), &Sem::Reg("rs1"))
        ))
        .unwrap_err()
        .contains("floating registers differ"));
        const ADDRESS: &Sem = &Sem::Add(&Sem::Reg("rs1"), &Sem::Sext(64, &Sem::Imm("imm12")));
        for effect in [
            &Sem::Set(
                &Sem::FReg("rd"),
                &Sem::FBox(32, &Sem::Load(&Sem::Lit(64), &Sem::Lit(0), ADDRESS)),
            ),
            &Sem::Set(
                &Sem::FReg("rd"),
                &Sem::Load(&Sem::Lit(32), &Sem::Lit(0), ADDRESS),
            ),
        ] {
            assert!(memory_over(&wrong_table("flw", effect)).is_err());
        }
        for effect in [
            &Sem::Store(&Sem::Lit(64), ADDRESS, &Sem::FReg("rs2")),
            &Sem::Store(&Sem::Lit(32), ADDRESS, &Sem::FUnbox(32, &Sem::FReg("rs2"))),
            &Sem::Nop,
        ] {
            assert!(memory_over(&wrong_table("fsw", effect)).is_err());
        }
    }
}
