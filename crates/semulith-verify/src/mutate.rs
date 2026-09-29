//! The validator mutation suite — `P1-LAB.9`, task card T007 (`EVD-09`): proof that the
//! laboratory's differential can *detect* each designated wrong behaviour, not only agree
//! with correct models. `RULES.md` EVD-09: "Keep a validator mutation suite that verifies
//! detection of known-wrong behaviors and unjustified comparison suppression." A suite that
//! has never seen a broken implementation is not known to detect anything — so every arm
//! below runs a broken model (or a broken comparison configuration) through the real
//! instruments and asserts the divergence is reported at the designated step, naming the
//! designated field.
//!
//! Two injection levels, chosen by fidelity (the per-arm tests document which level they
//! use and why):
//!
//! - **Model-level, through the `step_over`/`run_over` seam.** `semulith-core::exec` and
//!   `semulith-verify::run` take the instruction table they execute as a parameter; the
//!   production paths pass the generated `definition::INSNS`. A mutated model is then exactly
//!   what it should be — *data the one evaluator consumes*: a table copied from `INSNS` with
//!   one row swapped, either its decode row (`mask`/`value`) or its effect pointer, the
//!   latter to a mutated copy of the instruction's real effect tree rebuilt by [`rebuild`]
//!   and leaked into the suite's bounded test arena. OWN-01 is untouched: no rule has a
//!   second implementation; the suite never writes semantics, it perturbs data.
//! - **Observation/outcome-level, where a faithful model-level seam would require a second
//!   implementation of a rule** (e.g. an outcome-mapping mutation). There the suite applies
//!   the named wrong behaviour to the observation stream itself — the stream the designated
//!   wrong model would emit — and asserts the differential rejects it. This is the honest
//!   maximum: a mutation that can only exist as harness code is tested at the harness
//!   boundary, never smuggled into the semantics data.
//!
//! Detection instruments are all real and already gated: the first-divergence comparator
//! ([`crate::run::compare`]/[`crate::run::render`]) naming step and field, the run's
//! boundary-crossing census (an access the architectural observation vocabulary cannot see
//! is still a recorded crossing), and the pinned GUEST-GEN expectations as the GREEN anchor —
//! every guest arm first asserts the real model still meets the specification-derived
//! expectations, so an arm can only pass by detecting the mutant, not by a drifting anchor.
//!
//! No new doctrine guards this module: the suite is Rust tests under `make check`, the same
//! standing as the run suites. It guards discriminating power, not drift, so there is no
//! generated artifact to refuse.

use semulith_core::definition::{InsnDef, Sem, INSNS};
use semulith_core::env::{AccessWidth, Request};

/// Leak one rebuilt tree node into the suite's test arena. The suite mutates at most a
/// handful of small trees per test run; leaking them (rather than threading lifetimes
/// through the generated `&'static Sem` shape) keeps the production types unchanged.
fn leak(sem: Sem) -> &'static Sem {
    Box::leak(Box::new(sem))
}

/// Rebuild a tree, bottom-up, applying `f` to every node; a node `f` replaces is final —
/// `f` decides what its replacement's children are by rebuilding them itself. `f` returns
/// `None` to keep the node (rebuilt recursively, children mapped) and `Some(sem)` to swap
/// it. Only the swapped spine is new; untouched subtrees are reused by reference.
fn rebuild(sem: &Sem, f: &impl Fn(&Sem) -> Option<Sem>) -> Sem {
    if let Some(replacement) = f(sem) {
        return replacement;
    }
    let map = |child: &'static Sem| leak(rebuild(child, f));
    match sem {
        Sem::Lit(value) => Sem::Lit(*value),
        Sem::Reg(name) => Sem::Reg(name),
        Sem::Imm(name) => Sem::Imm(name),
        Sem::Pc => Sem::Pc,
        Sem::Xlen => Sem::Xlen,
        Sem::Add(a, b) => Sem::Add(map(a), map(b)),
        Sem::Sub(a, b) => Sem::Sub(map(a), map(b)),
        Sem::And(a, b) => Sem::And(map(a), map(b)),
        Sem::Or(a, b) => Sem::Or(map(a), map(b)),
        Sem::Xor(a, b) => Sem::Xor(map(a), map(b)),
        Sem::Shl(a, b) => Sem::Shl(map(a), map(b)),
        Sem::Shr(a, b) => Sem::Shr(map(a), map(b)),
        Sem::Sar(a, b) => Sem::Sar(map(a), map(b)),
        Sem::Slt(a, b) => Sem::Slt(map(a), map(b)),
        Sem::Sltu(a, b) => Sem::Sltu(map(a), map(b)),
        Sem::Eq(a, b) => Sem::Eq(map(a), map(b)),
        Sem::Ne(a, b) => Sem::Ne(map(a), map(b)),
        Sem::Lt(a, b) => Sem::Lt(map(a), map(b)),
        Sem::Ltu(a, b) => Sem::Ltu(map(a), map(b)),
        Sem::Ge(a, b) => Sem::Ge(map(a), map(b)),
        Sem::Geu(a, b) => Sem::Geu(map(a), map(b)),
        Sem::Trunc(width, v) => Sem::Trunc(*width, map(v)),
        Sem::Sext(width, v) => Sem::Sext(*width, map(v)),
        Sem::Zext(width, v) => Sem::Zext(*width, map(v)),
        Sem::Bits(hi, lo, v) => Sem::Bits(*hi, *lo, map(v)),
        Sem::Load(width, signed, addr) => Sem::Load(map(width), map(signed), map(addr)),
        Sem::Store(width, addr, value) => Sem::Store(map(width), map(addr), map(value)),
        Sem::Set(target, value) => Sem::Set(map(target), map(value)),
        Sem::SetPc(target) => Sem::SetPc(map(target)),
        Sem::Seq(steps) => {
            let rebuilt: Vec<&'static Sem> =
                steps.iter().map(|step| leak(rebuild(step, f))).collect();
            Sem::Seq(Box::leak(rebuilt.into_boxed_slice()))
        }
        Sem::Nop => Sem::Nop,
        Sem::If(cond, then, else_) => Sem::If(map(cond), map(then), map(else_)),
        Sem::Trap(cause, tval) => Sem::Trap(map(cause), map(tval)),
    }
}

/// The whole generated table with one row's effect replaced by `f`'s rebuild of that row's
/// real tree. `f` sees every node of the real tree and returns `Some` to swap a node.
#[must_use]
pub fn table_with_effect(name: &str, f: impl Fn(&Sem) -> Option<Sem>) -> Vec<InsnDef> {
    let mut table: Vec<InsnDef> = INSNS.iter().map(|insn| InsnDef { ..*insn }).collect();
    let pos = table
        .iter()
        .position(|insn| insn.name == name)
        .unwrap_or_else(|| panic!("the generated definition has an `{name}` row"));
    table[pos] = InsnDef {
        effect: leak(rebuild(table[pos].effect, &f)),
        ..table[pos]
    };
    table
}

/// The whole generated table with one row replaced wholesale (decode-row mutations: masks).
#[must_use]
pub fn table_with_row(name: &str, f: impl Fn(&InsnDef) -> InsnDef) -> Vec<InsnDef> {
    let mut table: Vec<InsnDef> = INSNS.iter().map(|insn| InsnDef { ..*insn }).collect();
    let pos = table
        .iter()
        .position(|insn| insn.name == name)
        .unwrap_or_else(|| panic!("the generated definition has an `{name}` row"));
    table[pos] = f(&table[pos]);
    table
}

/// The whole generated table with one row removed — a model limitation: the instruction is
/// declared by the profile but this model does not implement it.
#[must_use]
pub fn table_without(name: &str) -> Vec<InsnDef> {
    let mut table: Vec<InsnDef> = INSNS.iter().map(|insn| InsnDef { ..*insn }).collect();
    let pos = table
        .iter()
        .position(|insn| insn.name == name)
        .unwrap_or_else(|| panic!("the generated definition has an `{name}` row"));
    table.remove(pos);
    table
}

/// Swap every sign extension for a zero extension of the same width — "the immediate is
/// sign-extended" (RVI-RV32I §1.1.4) read as zero-extended.
#[must_use]
pub fn sext_to_zext(sem: &Sem) -> Option<Sem> {
    match sem {
        Sem::Sext(width, v) => Some(Sem::Zext(*width, v)),
        _ => None,
    }
}

/// The named mutations the demo and the browser bench expose — `(name, one-line story)`. `none`
/// is the real model; the rest are the `.9` suite's arms chosen for how visible they are.
pub const MUTATIONS: &[(&str, &str)] = &[
    ("none", "the real model — the reference trace"),
    (
        "zext-addi",
        "addi zero-extends its immediate instead of sign-extending",
    ),
    (
        "jal-no-link",
        "jal transfers but suppresses the pc+4 link write",
    ),
    (
        "jalr-odd-bit",
        "jalr keeps the odd target bit (D-JALR-LSB dropped)",
    ),
    (
        "phantom-load",
        "addi performs a discarded extra byte load (the census arm)",
    ),
];

/// The pinned data-crossing census of the tracked guests: the load/store crossings each
/// `.s` source declares, with the answer's class (`faulted` = the boundary answered a target
/// failure), tagged with the executing step. The `.9` suite pins this table and detects the
/// extra-access arm against it; the demo and bench report against it. Justifications:
/// - `smoke-arith.s`: one `sd x9, 1024(x10)` — the program's single data access (step 11).
/// - `guest-control.s`: no load or store instruction exists in the program.
/// - `smoke-trap.s`: the misaligned `lw` raises before the boundary is crossed
///   (D-MISALIGN-DATA) — zero data crossings.
/// - `guest-no-device.s`: one `ld x1, 0(x10)` at 0x0200_BFF8 — outside every declared
///   region, so the crossing is recorded and answered AccessFault (step 5).
/// - `scope-alu.s`, `scope-branch.s`, `scope-ecall.s`, `scope-ebreak.s`: no load or store
///   instruction exists in these programs (`P2-SCALAR.1`).
/// - `scope-mem.s` (`P2-SCALAR.1`): seventeen crossings — the support `sd`, eight load
///   probes (the `lw x0` load crosses the boundary even though its value is discarded,
///   D-LOAD-X0), the three stores under test, and their four read-back `ld`s — every one
///   inside the declared region, naturally aligned, none faulted.
/// - `bound-shift.s`, `bound-shiftw.s`, `bound-arith.s` (`P2-SCALAR.2`): pure arithmetic —
///   no load or store instruction exists in these programs.
/// - `bound-ext.s` (`P2-SCALAR.2`): thirty-two crossings — thirteen stores (the nine edge
///   values, the x0 zero byte, and the three truncation probes) and nineteen loads (the
///   sign/zero pairs, the all-ones values, the pre-written 0x00 byte, and the three
///   truncation read-backs) — every one inside the declared region, aligned, none faulted.
/// - `bound-alias.s` (`P2-SCALAR.2`): sixteen crossings — the three `sd`s of X, the eight
///   `lbu` lane reads, the overlapping `sb`/`sh`, two `ld` read-backs, the base-overwriting
///   `lb`, and the `sw x0` zero store — every one inside the declared region, aligned,
///   none faulted.
pub fn pinned_census(guest: &str) -> &'static [(usize, Request, bool)] {
    match guest {
        "smoke-arith" => &[(
            11,
            Request::Store {
                width: AccessWidth::D,
                addr: 0x8000_0400,
                data: 0xFFFF_FFFF_0000_0001,
            },
            false,
        )],
        "guest-control" => &[],
        "smoke-trap" => &[],
        "guest-no-device" => &[(
            5,
            Request::Load {
                width: AccessWidth::D,
                addr: 0x0200_BFF8,
            },
            true,
        )],
        "scope-mem" => &[
            (
                11,
                Request::Store {
                    width: AccessWidth::D,
                    addr: 0x8000_0400,
                    data: 0x80FF_F7F0_80FF_F7F0,
                },
                false,
            ),
            (
                12,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0400,
                },
                false,
            ),
            (
                13,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0401,
                },
                false,
            ),
            (
                14,
                Request::Load {
                    width: AccessWidth::H,
                    addr: 0x8000_0402,
                },
                false,
            ),
            (
                15,
                Request::Load {
                    width: AccessWidth::H,
                    addr: 0x8000_0402,
                },
                false,
            ),
            (
                16,
                Request::Load {
                    width: AccessWidth::W,
                    addr: 0x8000_0400,
                },
                false,
            ),
            (
                17,
                Request::Load {
                    width: AccessWidth::W,
                    addr: 0x8000_0404,
                },
                false,
            ),
            (
                18,
                Request::Load {
                    width: AccessWidth::D,
                    addr: 0x8000_0400,
                },
                false,
            ),
            (
                19,
                Request::Load {
                    width: AccessWidth::W,
                    addr: 0x8000_0400,
                },
                false,
            ),
            (
                21,
                Request::Store {
                    width: AccessWidth::B,
                    addr: 0x8000_0410,
                    data: 0xFF,
                },
                false,
            ),
            (
                22,
                Request::Load {
                    width: AccessWidth::D,
                    addr: 0x8000_0410,
                },
                false,
            ),
            (
                23,
                Request::Store {
                    width: AccessWidth::H,
                    addr: 0x8000_0418,
                    data: 0xFFFF,
                },
                false,
            ),
            (
                24,
                Request::Load {
                    width: AccessWidth::D,
                    addr: 0x8000_0418,
                },
                false,
            ),
            (
                25,
                Request::Store {
                    width: AccessWidth::W,
                    addr: 0x8000_0420,
                    data: 0xFFFF_FFFF,
                },
                false,
            ),
            (
                26,
                Request::Load {
                    width: AccessWidth::D,
                    addr: 0x8000_0420,
                },
                false,
            ),
            (
                27,
                Request::Store {
                    width: AccessWidth::W,
                    addr: 0x8000_0428,
                    data: 0x80FF_F7F0,
                },
                false,
            ),
            (
                28,
                Request::Load {
                    width: AccessWidth::D,
                    addr: 0x8000_0428,
                },
                false,
            ),
        ],
        "scope-alu" | "scope-branch" | "scope-ecall" | "scope-ebreak" => &[],
        "bound-shift" | "bound-shiftw" | "bound-arith" => &[],
        "bound-ext" => &[
            (
                14,
                Request::Store {
                    width: AccessWidth::B,
                    addr: 0x8000_0400,
                    data: 0x7F,
                },
                false,
            ),
            (
                15,
                Request::Store {
                    width: AccessWidth::B,
                    addr: 0x8000_0401,
                    data: 0x80,
                },
                false,
            ),
            (
                16,
                Request::Store {
                    width: AccessWidth::B,
                    addr: 0x8000_0402,
                    data: 0xFF,
                },
                false,
            ),
            (
                17,
                Request::Store {
                    width: AccessWidth::H,
                    addr: 0x8000_0408,
                    data: 0x7FFF,
                },
                false,
            ),
            (
                18,
                Request::Store {
                    width: AccessWidth::H,
                    addr: 0x8000_040A,
                    data: 0x8000,
                },
                false,
            ),
            (
                19,
                Request::Store {
                    width: AccessWidth::H,
                    addr: 0x8000_040C,
                    data: 0xFFFF,
                },
                false,
            ),
            (
                20,
                Request::Store {
                    width: AccessWidth::W,
                    addr: 0x8000_0410,
                    data: 0x7FFF_FFFF,
                },
                false,
            ),
            (
                21,
                Request::Store {
                    width: AccessWidth::W,
                    addr: 0x8000_0414,
                    data: 0x8000_0000,
                },
                false,
            ),
            (
                22,
                Request::Store {
                    width: AccessWidth::W,
                    addr: 0x8000_0418,
                    data: 0xFFFF_FFFF,
                },
                false,
            ),
            (
                23,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0400,
                },
                false,
            ),
            (
                24,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0401,
                },
                false,
            ),
            (
                25,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0401,
                },
                false,
            ),
            (
                26,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0402,
                },
                false,
            ),
            (
                27,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0402,
                },
                false,
            ),
            (
                28,
                Request::Load {
                    width: AccessWidth::H,
                    addr: 0x8000_0408,
                },
                false,
            ),
            (
                29,
                Request::Load {
                    width: AccessWidth::H,
                    addr: 0x8000_040A,
                },
                false,
            ),
            (
                30,
                Request::Load {
                    width: AccessWidth::H,
                    addr: 0x8000_040A,
                },
                false,
            ),
            (
                31,
                Request::Load {
                    width: AccessWidth::H,
                    addr: 0x8000_040C,
                },
                false,
            ),
            (
                32,
                Request::Load {
                    width: AccessWidth::H,
                    addr: 0x8000_040C,
                },
                false,
            ),
            (
                33,
                Request::Load {
                    width: AccessWidth::W,
                    addr: 0x8000_0410,
                },
                false,
            ),
            (
                34,
                Request::Load {
                    width: AccessWidth::W,
                    addr: 0x8000_0414,
                },
                false,
            ),
            (
                35,
                Request::Load {
                    width: AccessWidth::W,
                    addr: 0x8000_0414,
                },
                false,
            ),
            (
                36,
                Request::Load {
                    width: AccessWidth::W,
                    addr: 0x8000_0418,
                },
                false,
            ),
            (
                37,
                Request::Load {
                    width: AccessWidth::W,
                    addr: 0x8000_0418,
                },
                false,
            ),
            (
                38,
                Request::Store {
                    width: AccessWidth::B,
                    addr: 0x8000_0403,
                    data: 0x00,
                },
                false,
            ),
            (
                40,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0403,
                },
                false,
            ),
            (
                41,
                Request::Store {
                    width: AccessWidth::B,
                    addr: 0x8000_0420,
                    data: 0x80,
                },
                false,
            ),
            (
                42,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0420,
                },
                false,
            ),
            (
                43,
                Request::Store {
                    width: AccessWidth::H,
                    addr: 0x8000_0428,
                    data: 0x8000,
                },
                false,
            ),
            (
                44,
                Request::Load {
                    width: AccessWidth::H,
                    addr: 0x8000_0428,
                },
                false,
            ),
            (
                45,
                Request::Store {
                    width: AccessWidth::W,
                    addr: 0x8000_0430,
                    data: 0xFFFF_8000,
                },
                false,
            ),
            (
                46,
                Request::Load {
                    width: AccessWidth::W,
                    addr: 0x8000_0430,
                },
                false,
            ),
        ],
        "bound-alias" => &[
            (
                8,
                Request::Store {
                    width: AccessWidth::D,
                    addr: 0x8000_0400,
                    data: 0x0807_0605_0403_0201,
                },
                false,
            ),
            (
                9,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0400,
                },
                false,
            ),
            (
                10,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0401,
                },
                false,
            ),
            (
                11,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0402,
                },
                false,
            ),
            (
                12,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0403,
                },
                false,
            ),
            (
                13,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0404,
                },
                false,
            ),
            (
                14,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0405,
                },
                false,
            ),
            (
                15,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0406,
                },
                false,
            ),
            (
                16,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0407,
                },
                false,
            ),
            (
                17,
                Request::Store {
                    width: AccessWidth::D,
                    addr: 0x8000_0408,
                    data: 0x0807_0605_0403_0201,
                },
                false,
            ),
            (
                19,
                Request::Store {
                    width: AccessWidth::B,
                    addr: 0x8000_040B,
                    data: 0xAA,
                },
                false,
            ),
            (
                21,
                Request::Store {
                    width: AccessWidth::H,
                    addr: 0x8000_040E,
                    data: 0x4CD,
                },
                false,
            ),
            (
                22,
                Request::Load {
                    width: AccessWidth::D,
                    addr: 0x8000_0408,
                },
                false,
            ),
            (
                32,
                Request::Load {
                    width: AccessWidth::B,
                    addr: 0x8000_0400,
                },
                false,
            ),
            (
                34,
                Request::Store {
                    width: AccessWidth::D,
                    addr: 0x8000_0410,
                    data: 0x0807_0605_0403_0201,
                },
                false,
            ),
            (
                35,
                Request::Store {
                    width: AccessWidth::W,
                    addr: 0x8000_0410,
                    data: 0x00,
                },
                false,
            ),
            (
                36,
                Request::Load {
                    width: AccessWidth::D,
                    addr: 0x8000_0410,
                },
                false,
            ),
        ],
        _ => &[],
    }
}

/// The instruction table for a named [`MUTATIONS`] entry.
#[must_use]
pub fn table_for(mutation: &str) -> Option<Vec<InsnDef>> {
    match mutation {
        "none" => Some(INSNS.iter().map(|insn| InsnDef { ..*insn }).collect()),
        "zext-addi" => Some(table_with_effect("addi", sext_to_zext)),
        "jal-no-link" => Some(table_with_effect("jal", |sem| match sem {
            Sem::Seq(steps)
                if steps.len() == 2
                    && matches!(steps[0], Sem::Set(..))
                    && matches!(steps[1], Sem::SetPc(..)) =>
            {
                Some(rebuild(steps[1], &|_| None))
            }
            _ => None,
        })),
        "jalr-odd-bit" => Some(table_with_effect("jalr", |sem| match sem {
            Sem::And(a, b) if matches!(&**b, Sem::Lit(v) if *v == (-2i64) as u64) => {
                Some(rebuild(a, &|_| None))
            }
            _ => None,
        })),
        "phantom-load" => Some(table_with_row("addi", |insn| {
            // The suite's phantom-load arm at the region base: a discarded byte load before
            // the real effect — invisible to the trace, visible only in the crossing census.
            let phantom = Sem::Seq(Box::leak(
                vec![
                    leak(Sem::Load(
                        leak(Sem::Lit(8)),
                        leak(Sem::Lit(0)),
                        leak(Sem::Lit(0x8000_0000)),
                    )),
                    leak(rebuild(insn.effect, &|_| None)),
                ]
                .into_boxed_slice(),
            ));
            InsnDef {
                effect: leak(phantom),
                ..*insn
            }
        })),
        _ => None,
    }
}

#[cfg(test)]
mod tests;
