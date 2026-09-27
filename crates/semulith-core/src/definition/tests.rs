//! Tests for the generated canonical definition (`P1-LAB.6`).
//!
//! The acceptance criteria, each re-derived against the generated DATA (the generator
//! refuses to emit a table that violates these invariants; the suites below re-check
//! them in the artifact a reader actually consumes, so a hand edit fails twice):
//!
//! 1. **OWN-03** — the generation manifest names the whole definition: every canonical
//!    input by path and sha256, the generator by name and hash, the configuration as
//!    data, and the upstream source fingerprints.
//! 2. **OWN-01 / EXTRACTION** — every declared instruction has exactly one entry and
//!    carries its semantics; the fixed-bit encodings are decidable (no two
//!    instructions claim the same word).
//! 3. **The schema layer's shape** — fields sit inside the 32-bit word; scatter pieces
//!    account exactly for their field.
//! 4. **The binding rule** — a semantics tree references only operands its instruction
//!    provides (`scripts/check_semantics.py`'s rule, restated as data); every declared
//!    operand is extractable or a documented FENCE decoration.

use std::collections::HashSet;

use super::*;

fn hex64(s: &str) -> bool {
    s.len() == 64 && s.bytes().all(|b| b.is_ascii_hexdigit())
}

fn field(name: &str) -> Option<&'static FieldDef> {
    FIELDS.iter().find(|f| f.name == name)
}

/// Collect every register/immediate name an effect tree references.
fn collect_symbols(sem: &Sem, regs: &mut Vec<&'static str>, imms: &mut Vec<&'static str>) {
    match sem {
        Sem::Reg(name) => regs.push(name),
        Sem::Imm(name) => imms.push(name),
        Sem::Lit(_) | Sem::Pc | Sem::Xlen | Sem::Nop => {}
        Sem::Add(a, b)
        | Sem::Sub(a, b)
        | Sem::And(a, b)
        | Sem::Or(a, b)
        | Sem::Xor(a, b)
        | Sem::Shl(a, b)
        | Sem::Shr(a, b)
        | Sem::Sar(a, b)
        | Sem::Slt(a, b)
        | Sem::Sltu(a, b)
        | Sem::Eq(a, b)
        | Sem::Ne(a, b)
        | Sem::Lt(a, b)
        | Sem::Ltu(a, b)
        | Sem::Ge(a, b)
        | Sem::Geu(a, b)
        | Sem::Set(a, b)
        | Sem::Trap(a, b) => {
            collect_symbols(a, regs, imms);
            collect_symbols(b, regs, imms);
        }
        Sem::Trunc(_, v) | Sem::Sext(_, v) | Sem::Zext(_, v) => collect_symbols(v, regs, imms),
        Sem::Bits(_, _, v) => collect_symbols(v, regs, imms),
        Sem::Load(a, b, c) | Sem::Store(a, b, c) | Sem::If(a, b, c) => {
            collect_symbols(a, regs, imms);
            collect_symbols(b, regs, imms);
            collect_symbols(c, regs, imms);
        }
        Sem::SetPc(a) => collect_symbols(a, regs, imms),
        Sem::Seq(steps) => {
            for step in *steps {
                collect_symbols(step, regs, imms);
            }
        }
    }
}

/// The operand names a semantics rule may reference — the binding rule of
/// `scripts/check_semantics.py`, restated as data: the encoding provides the fields;
/// a split store immediate reads as one `imm12`, a split branch immediate as one
/// `bimm12`, and either shift field reads as `shamt`. `pc` and `xlen` are implicit.
fn bound_names(insn: &InsnDef) -> HashSet<&'static str> {
    let mut names: HashSet<&'static str> = insn.operands.iter().copied().collect();
    if names.contains("imm12hi") {
        names.remove("imm12hi");
        names.remove("imm12lo");
        names.insert("imm12");
    }
    if names.contains("bimm12hi") {
        names.remove("bimm12hi");
        names.remove("bimm12lo");
        names.insert("bimm12");
    }
    if names.contains("shamtd") || names.contains("shamtw") {
        names.insert("shamt");
    }
    names
}

// ── 1: OWN-03's manifest names the whole definition ─────────────────────────────────────

#[test]
fn manifest_covers_the_canonical_definition() {
    assert_eq!(MANIFEST.profile, "rv64i-lab-v0");
    assert_eq!(MANIFEST.ilen, 32);
    assert_eq!(MANIFEST.fragments, &["riscv/rv64i"]);
    assert!(MANIFEST.generator.name.ends_with("gen_definition.py"));
    assert!(hex64(MANIFEST.generator.sha256));
    // Exactly the canonical inputs: the unit's composition, the fragment it composes,
    // the fragment's semantics, and the state descriptor — encodings, semantics and
    // state, the three legs of the definition this manifest covers.
    let paths: Vec<&str> = MANIFEST.inputs.iter().map(|pin| pin.path).collect();
    assert_eq!(
        paths,
        [
            "definitions/riscv/rv64i.sem.sexp",
            "definitions/riscv/rv64i.sexp",
            "profiles/rv64i-lab-v0/encoding.sexp",
            "profiles/rv64i-lab-v0/state.sexp",
        ]
    );
    for pin in MANIFEST.inputs {
        assert!(hex64(pin.sha256), "{}: not a sha256", pin.path);
    }
    // The upstream tables the fragments pin: both RV64I encoding files, named.
    let sources: HashSet<&str> = MANIFEST.sources.iter().map(|pin| pin.file).collect();
    assert_eq!(sources, ["rv_i", "rv64_i"].into_iter().collect());
    for pin in MANIFEST.sources {
        assert!(hex64(pin.sha256), "{}: not a sha256", pin.file);
    }
}

// ── 2: the table is decidable, complete, and cited ──────────────────────────────────────

#[test]
fn the_table_is_alphabetical_and_complete() {
    assert_eq!(INSNS.len(), 52, "RV64I declares 52 instructions");
    for (prev, next) in INSNS.iter().zip(INSNS.iter().skip(1)) {
        assert!(
            prev.name < next.name,
            "{} then {}: not sorted",
            prev.name,
            next.name
        );
    }
}

#[test]
fn fixed_bits_do_not_collide() {
    // Two instructions conflict iff their fixed bits agree on the overlap — then some
    // word would decode to both, and a linear scan's answer would depend on order.
    for a in INSNS {
        for b in INSNS {
            if a.name >= b.name {
                continue;
            }
            let shared = a.mask & b.mask;
            assert_ne!(
                (a.value ^ b.value) & shared,
                0,
                "{} and {} both claim fixed bits {:08x} (shared mask {:08x})",
                a.name,
                b.name,
                a.value & shared,
                shared
            );
        }
    }
}

#[test]
fn every_instruction_matches_its_own_fixed_bits() {
    for insn in INSNS {
        assert_eq!(
            insn.value & !insn.mask,
            0,
            "{}: value outside its mask",
            insn.name
        );
        assert_eq!(decode(insn.value).map(|d| d.name), Some(insn.name));
    }
}

#[test]
fn a_word_no_instruction_claims_is_reserved_decode() {
    // All-zero fixed bits: no RV64I instruction matches, so the decode is the
    // reserved-decode case — `None` here, an `UndefinedCase` at the caller.
    assert!(decode(0).is_none());
}

#[test]
fn semantics_are_cited() {
    for insn in INSNS {
        assert!(
            !insn.source.is_empty(),
            "{}: no specification locator",
            insn.name
        );
    }
}

// ── 3: the fields the decoder extracts from ─────────────────────────────────────────────

#[test]
fn fields_are_well_formed() {
    assert_eq!(FIELDS.len(), 12);
    for f in FIELDS {
        assert!(
            f.hi <= 31 && f.lo <= f.hi,
            "{}: bad range [{}:{}]",
            f.name,
            f.hi,
            f.lo
        );
        if !f.scatter.is_empty() {
            // A scattered field's pieces must account for exactly the field's width —
            // a layout that does not reconcile is one the decoder must not use.
            let width = u32::from(f.hi - f.lo) + 1;
            let accounted: u32 = f
                .scatter
                .iter()
                .map(|(hi, lo)| u32::from(hi - lo) + 1)
                .sum();
            assert_eq!(
                accounted, width,
                "{}: scatter does not fill the field",
                f.name
            );
        }
    }
    // Names are unique.
    let mut names: Vec<&str> = FIELDS.iter().map(|f| f.name).collect();
    names.sort_unstable();
    names.dedup();
    assert_eq!(names.len(), FIELDS.len());
}

#[test]
fn every_operand_is_a_field_or_a_fence_decoration() {
    // The encoding declares exactly three operands with no field ranges: FENCE's
    // fm/pred/succ decorations (D-FENCE decodes them, reads none — the effect is nop).
    // A NEW unfielded operand fails this ratchet until it is consciously dispositioned.
    const FENCE_DECORATIONS: [&str; 3] = ["fm", "pred", "succ"];
    for insn in INSNS {
        for op in insn.operands {
            assert!(
                field(op).is_some() || FENCE_DECORATIONS.contains(op),
                "{}: operand {} has no field range and is not a FENCE decoration",
                insn.name,
                op
            );
        }
    }
}

// ── 4: the binding rule, re-derived on the emitted trees ────────────────────────────────

#[test]
fn semantics_reference_only_declared_operands() {
    for insn in INSNS {
        let bound = bound_names(insn);
        let mut regs = Vec::new();
        let mut imms = Vec::new();
        collect_symbols(insn.effect, &mut regs, &mut imms);
        for name in regs.iter().chain(imms.iter()) {
            assert!(
                bound.contains(name) || *name == "pc" || *name == "xlen",
                "{}: semantics reference {name}, which the encoding does not provide",
                insn.name
            );
        }
        // The register-writing heads write a register, never an immediate.
        if let Sem::Set(target, _) = insn.effect {
            assert!(
                matches!(target, Sem::Reg(_)),
                "{}: set writes a non-register",
                insn.name
            );
        }
    }
}

#[test]
fn split_immediates_are_bound_as_one_operand() {
    // The S-type and B-type splits: the encoding declares two fields, the semantics
    // read one composed immediate — the generator's binding rule in both directions.
    let sb = decode(0x00000023).expect("sb encoding"); // sb x0, 0(x0)
    assert!(bound_names(sb).contains("imm12"));
    let beq = decode(0x00000063).expect("beq encoding"); // beq x0, x0, 0
    assert!(bound_names(beq).contains("bimm12"));
    let slli = decode(0x00001013).expect("slli encoding"); // slli x0, x0, 0
    assert!(bound_names(slli).contains("shamt"));
}
