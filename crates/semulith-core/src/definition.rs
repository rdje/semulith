//! GENERATED — do not edit (OWN-03). Regenerate with `python3 scripts/gen_definition.py`;
//! drift between this module and the canonical definition it derives from is refused
//! by the DEF-GEN doctrine (`scripts/check_definition_gen.sh`). These tables are the
//! executable skeleton of the unit's canonical definition (`docs/ARCHITECTURE.md` §2):
//! the decode metadata, the operand-field table, and the semantics effect trees,
//! lowered from `profiles/rv64i-lab-v0/encoding.sexp` composing `riscv/rv64i`, with
//! `definitions/riscv/rv64i.sem.sexp` the execution authority's semantics data.
//!
//! OWN-01: every semantic rule has exactly one executable owner — the semantics
//! DATA. This module is its lowered mirror; there is no handwritten second copy of
//! any rule, and the interpreter slice (`P1-LAB.8`) evaluates exactly these trees.
//!
//! Canonical inputs (sha256):
//!   `definitions/riscv/rv64i.sem.sexp`  `addbe19d047c9c01c30455a09ff402e7bb5a8ee8a723f229233270679ce39ee2`
//!   `definitions/riscv/rv64i.sexp`  `f45071eef9894463259482191cc464fa79df59af04b16e5c10f6c3a7342e0278`
//!   `profiles/rv64i-lab-v0/encoding.sexp`  `93a2d4718a50b60c23c3b5e64afa64499b09fcf41a906d46d83e63eebab2e5e9`
//!   `profiles/rv64i-lab-v0/state.sexp`  `ff53fb04f3ed7ac25e4db78e6e92cc3e0caa086df438e221350627194cbea5a4`
//! Generator: `scripts/gen_definition.py` (sha256 `9679df2458d66a6036293c04a1de1bc282709edae19b47875e837cef2008fb34`)

/// OWN-03's generation manifest: the canonical inputs, the generator, the
/// configuration, and the upstream source fingerprints this module derives from.
/// Values, not behaviour: reading the manifest never touches the filesystem — the
/// fingerprints were computed at generation time, and the DEF-GEN doctrine refuses
/// the day the bytes behind them change without regeneration.
pub struct DefinitionManifest {
    /// The unit this definition was generated for.
    pub profile: &'static str,
    /// The instruction length in bits (ILEN = 32 for this profile).
    pub ilen: u32,
    /// The fragments the composition resolves, base first, then extensions.
    pub fragments: &'static [&'static str],
    /// The generator that produced this module, named and content-hashed.
    pub generator: GeneratorPin,
    /// Every canonical input, by repository-relative path and content hash.
    pub inputs: &'static [InputPin],
    /// The upstream source fingerprints the composed fragments carry.
    pub sources: &'static [SourcePin],
}

/// The generator, identified by name and content — OWN-03's generator fingerprint.
pub struct GeneratorPin {
    pub name: &'static str,
    pub sha256: &'static str,
}

/// One canonical input: the path, and the sha256 of the exact bytes.
pub struct InputPin {
    pub path: &'static str,
    pub sha256: &'static str,
}

/// One upstream source the definition was generated from, pinned by the fragment.
pub struct SourcePin {
    pub file: &'static str,
    pub sha256: &'static str,
}

pub static MANIFEST: DefinitionManifest = DefinitionManifest {
    profile: "rv64i-lab-v0",
    ilen: 32,
    fragments: &["riscv/rv64i"],
    generator: GeneratorPin {
        name: "scripts/gen_definition.py",
        sha256: "9679df2458d66a6036293c04a1de1bc282709edae19b47875e837cef2008fb34",
    },
    inputs: &[
        InputPin {
            path: "definitions/riscv/rv64i.sem.sexp",
            sha256: "addbe19d047c9c01c30455a09ff402e7bb5a8ee8a723f229233270679ce39ee2",
        },
        InputPin {
            path: "definitions/riscv/rv64i.sexp",
            sha256: "f45071eef9894463259482191cc464fa79df59af04b16e5c10f6c3a7342e0278",
        },
        InputPin {
            path: "profiles/rv64i-lab-v0/encoding.sexp",
            sha256: "93a2d4718a50b60c23c3b5e64afa64499b09fcf41a906d46d83e63eebab2e5e9",
        },
        InputPin {
            path: "profiles/rv64i-lab-v0/state.sexp",
            sha256: "ff53fb04f3ed7ac25e4db78e6e92cc3e0caa086df438e221350627194cbea5a4",
        },
    ],
    sources: &[
        SourcePin {
            file: "rv64_i",
            sha256: "262cbd0884fe1383fcb7c42070cbc73e309d0452ff8d00b38452a4dee7cfa7f5",
        },
        SourcePin {
            file: "rv_i",
            sha256: "146e297ddbe346f325d993aaf56d7006f1bfde39df584b888b221543def17b97",
        },
    ],
};

/// One operand field of the encoding: its bit range in the 32-bit word, and, for
/// the scattered B/J immediates, the immediate-bit pieces the field carries in
/// MSB-first order — `(12, 12)` first means the field's top bit holds imm[12].
/// Empty `scatter` marks a contiguous field.
pub struct FieldDef {
    pub name: &'static str,
    pub hi: u8,
    pub lo: u8,
    pub scatter: &'static [(u8, u8)],
}

/// The 15 operand fields the composed fragments declare, sorted by
/// name: what the decoder extracts, and how the scrambled immediates unscramble.
/// The `FENCE` decorations `fm`/`pred`/`succ` are declared as operands by the
/// encoding without field ranges — D-FENCE decodes them and reads none (the rule's
/// effect is `nop`), so no extraction is emitted for them.
pub static FIELDS: &[FieldDef] = &[
    FieldDef {
        name: "bimm12hi",
        hi: 31,
        lo: 25,
        scatter: &[(12, 12), (10, 5)],
    },
    FieldDef {
        name: "bimm12lo",
        hi: 11,
        lo: 7,
        scatter: &[(4, 1), (11, 11)],
    },
    FieldDef {
        name: "fm",
        hi: 31,
        lo: 28,
        scatter: &[],
    },
    FieldDef {
        name: "imm12",
        hi: 31,
        lo: 20,
        scatter: &[],
    },
    FieldDef {
        name: "imm12hi",
        hi: 31,
        lo: 25,
        scatter: &[],
    },
    FieldDef {
        name: "imm12lo",
        hi: 11,
        lo: 7,
        scatter: &[],
    },
    FieldDef {
        name: "imm20",
        hi: 31,
        lo: 12,
        scatter: &[],
    },
    FieldDef {
        name: "jimm20",
        hi: 31,
        lo: 12,
        scatter: &[(20, 20), (10, 1), (11, 11), (19, 12)],
    },
    FieldDef {
        name: "pred",
        hi: 27,
        lo: 24,
        scatter: &[],
    },
    FieldDef {
        name: "rd",
        hi: 11,
        lo: 7,
        scatter: &[],
    },
    FieldDef {
        name: "rs1",
        hi: 19,
        lo: 15,
        scatter: &[],
    },
    FieldDef {
        name: "rs2",
        hi: 24,
        lo: 20,
        scatter: &[],
    },
    FieldDef {
        name: "shamtd",
        hi: 25,
        lo: 20,
        scatter: &[],
    },
    FieldDef {
        name: "shamtw",
        hi: 24,
        lo: 20,
        scatter: &[],
    },
    FieldDef {
        name: "succ",
        hi: 23,
        lo: 20,
        scatter: &[],
    },
];

/// One instruction of the composed definition: the fixed bits a decoder matches on
/// (`mask`/`value` — a word decodes to this instruction iff `word & mask = value`),
/// the operands the encoding declares, the upstream table the encoding came from,
/// the specification locator the semantics rule cites, and the rule's effect tree.
pub struct InsnDef {
    pub name: &'static str,
    pub mask: u32,
    pub value: u32,
    /// The operand fields as the encoding declares them, in operand order. A split
    /// immediate appears as its two fields (`imm12hi`/`imm12lo`, `bimm12hi`/`bimm12lo`);
    /// the semantics trees read the composed `imm12`/`bimm12` (and `shamt` for either
    /// shift field) — the binding rule of `scripts/check_semantics.py`, which the
    /// generator re-derives and the tests below re-check as data.
    pub operands: &'static [&'static str],
    /// The upstream encoding table this instruction's fixed bits were generated from.
    pub from: &'static str,
    /// The specification locator the semantics rule was derived from.
    pub source: &'static str,
    /// The semantics rule's effect, lowered from the semantics data — the one
    /// executable owner of the behaviour (OWN-01).
    pub effect: &'static Sem,
}

/// The 52 instructions of the composed definition, sorted by name. Every
/// declared instruction carries its semantics — completeness is a generation-time
/// refusal, not a hope (EXTRACTION).
pub static INSNS: &[InsnDef] = &[
    InsnDef {
        name: "add",
        mask: 0xfe00707f,
        value: 0x00000033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.4 — overflow ignored; the result wraps modulo 2^XLEN",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Add(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "addi",
        mask: 0x0000707f,
        value: 0x00000013,
        operands: &["rd", "rs1", "imm12"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.4 — the immediate is sign-extended; overflow is ignored",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Add(
                &Sem::Reg("rs1"),
                &Sem::Sext(
                    64,
                    &Sem::Imm("imm12"),
                ),
            ),
        )
    },
    InsnDef {
        name: "addiw",
        mask: 0x0000707f,
        value: 0x0000001b,
        operands: &["rd", "rs1", "imm12"],
        from: "rv64_i",
        source: "RVI-RV64I §3.1.2 — D-WSUFFIX: overflow ignored, low 32 bits sign-extended",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Trunc(
                    32,
                    &Sem::Add(
                        &Sem::Trunc(
                            32,
                            &Sem::Reg("rs1"),
                        ),
                        &Sem::Sext(
                            32,
                            &Sem::Imm("imm12"),
                        ),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "addw",
        mask: 0xfe00707f,
        value: 0x0000003b,
        operands: &["rd", "rs1", "rs2"],
        from: "rv64_i",
        source: "RVI-RV64I §3.1.2.2 — D-WSUFFIX",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Trunc(
                    32,
                    &Sem::Add(
                        &Sem::Trunc(
                            32,
                            &Sem::Reg("rs1"),
                        ),
                        &Sem::Trunc(
                            32,
                            &Sem::Reg("rs2"),
                        ),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "and",
        mask: 0xfe00707f,
        value: 0x00007033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.4",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::And(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "andi",
        mask: 0x0000707f,
        value: 0x00007013,
        operands: &["rd", "rs1", "imm12"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.4",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::And(
                &Sem::Reg("rs1"),
                &Sem::Sext(
                    64,
                    &Sem::Imm("imm12"),
                ),
            ),
        )
    },
    InsnDef {
        name: "auipc",
        mask: 0x0000007f,
        value: 0x00000017,
        operands: &["rd", "imm20"],
        from: "rv_i",
        source: "RVI-RV64I §3.1.2.1 — D-LUI-AUIPC; the offset is added to the address OF THIS INSTRUCTION",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Add(
                &Sem::Pc,
                &Sem::Sext(
                    64,
                    &Sem::Shl(
                        &Sem::Imm("imm20"),
                        &Sem::Lit(0x000000000000000c),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "beq",
        mask: 0x0000707f,
        value: 0x00000063,
        operands: &["bimm12hi", "rs1", "rs2", "bimm12lo"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.5.2",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
            &Sem::SetPc(
                &Sem::Add(
                    &Sem::Pc,
                    &Sem::Sext(
                        64,
                        &Sem::Imm("bimm12"),
                    ),
                ),
            ),
            &Sem::Nop,
        )
    },
    InsnDef {
        name: "bge",
        mask: 0x0000707f,
        value: 0x00005063,
        operands: &["bimm12hi", "rs1", "rs2", "bimm12lo"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.5.2 — signed comparison",
        effect: &Sem::If(
            &Sem::Ge(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
            &Sem::SetPc(
                &Sem::Add(
                    &Sem::Pc,
                    &Sem::Sext(
                        64,
                        &Sem::Imm("bimm12"),
                    ),
                ),
            ),
            &Sem::Nop,
        )
    },
    InsnDef {
        name: "bgeu",
        mask: 0x0000707f,
        value: 0x00007063,
        operands: &["bimm12hi", "rs1", "rs2", "bimm12lo"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.5.2 — unsigned comparison",
        effect: &Sem::If(
            &Sem::Geu(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
            &Sem::SetPc(
                &Sem::Add(
                    &Sem::Pc,
                    &Sem::Sext(
                        64,
                        &Sem::Imm("bimm12"),
                    ),
                ),
            ),
            &Sem::Nop,
        )
    },
    InsnDef {
        name: "blt",
        mask: 0x0000707f,
        value: 0x00004063,
        operands: &["bimm12hi", "rs1", "rs2", "bimm12lo"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.5.2 — signed comparison",
        effect: &Sem::If(
            &Sem::Lt(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
            &Sem::SetPc(
                &Sem::Add(
                    &Sem::Pc,
                    &Sem::Sext(
                        64,
                        &Sem::Imm("bimm12"),
                    ),
                ),
            ),
            &Sem::Nop,
        )
    },
    InsnDef {
        name: "bltu",
        mask: 0x0000707f,
        value: 0x00006063,
        operands: &["bimm12hi", "rs1", "rs2", "bimm12lo"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.5.2 — unsigned comparison",
        effect: &Sem::If(
            &Sem::Ltu(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
            &Sem::SetPc(
                &Sem::Add(
                    &Sem::Pc,
                    &Sem::Sext(
                        64,
                        &Sem::Imm("bimm12"),
                    ),
                ),
            ),
            &Sem::Nop,
        )
    },
    InsnDef {
        name: "bne",
        mask: 0x0000707f,
        value: 0x00001063,
        operands: &["bimm12hi", "rs1", "rs2", "bimm12lo"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.5.2",
        effect: &Sem::If(
            &Sem::Ne(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
            &Sem::SetPc(
                &Sem::Add(
                    &Sem::Pc,
                    &Sem::Sext(
                        64,
                        &Sem::Imm("bimm12"),
                    ),
                ),
            ),
            &Sem::Nop,
        )
    },
    InsnDef {
        name: "ebreak",
        mask: 0xffffffff,
        value: 0x00100073,
        operands: &[],
        from: "rv_i",
        source: "RVI-RV32I §1.1.8 — D-ECALL-EBREAK: a precise REQUESTED trap; cause 3 is breakpoint",
        effect: &Sem::Trap(
            &Sem::Lit(0x0000000000000003),
            &Sem::Pc,
        )
    },
    InsnDef {
        name: "ecall",
        mask: 0xffffffff,
        value: 0x00000073,
        operands: &[],
        from: "rv_i",
        source: "RVI-RV32I §1.1.8 — D-ECALL-EBREAK: a precise REQUESTED trap to the execution environment",
        effect: &Sem::Trap(
            &Sem::Lit(0x000000000000000b),
            &Sem::Lit(0x0000000000000000),
        )
    },
    InsnDef {
        name: "fence",
        mask: 0x0000707f,
        value: 0x0000000f,
        operands: &["fm", "pred", "succ", "rs1", "rd"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.7 — D-FENCE: one hart, no devices, in-order; decoded, must not trap, no observable effect",
        effect: &Sem::Nop
    },
    InsnDef {
        name: "jal",
        mask: 0x0000007f,
        value: 0x0000006f,
        operands: &["rd", "jimm20"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.5.1 — JAL stores pc+4 in rd, then adds the offset to THIS instruction's address",
        effect: &Sem::Seq(&[
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Add(
                    &Sem::Pc,
                    &Sem::Lit(0x0000000000000004),
                ),
            ),
            &Sem::SetPc(
                &Sem::Add(
                    &Sem::Pc,
                    &Sem::Sext(
                        64,
                        &Sem::Imm("jimm20"),
                    ),
                ),
            ),
        ])
    },
    InsnDef {
        name: "jalr",
        mask: 0x0000707f,
        value: 0x00000067,
        operands: &["rd", "rs1", "imm12"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.5.1 — D-JALR-LSB: add, THEN set the least-significant bit to zero",
        effect: &Sem::Seq(&[
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Add(
                    &Sem::Pc,
                    &Sem::Lit(0x0000000000000004),
                ),
            ),
            &Sem::SetPc(
                &Sem::And(
                    &Sem::Add(
                        &Sem::Reg("rs1"),
                        &Sem::Sext(
                            64,
                            &Sem::Imm("imm12"),
                        ),
                    ),
                    &Sem::Lit(0xfffffffffffffffe),
                ),
            ),
        ])
    },
    InsnDef {
        name: "lb",
        mask: 0x0000707f,
        value: 0x00000003,
        operands: &["rd", "rs1", "imm12"],
        from: "rv_i",
        source: "RVI-RV64I §3.1.3 — D-LOAD-EXT: LB sign-extends",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Load(
                    &Sem::Lit(0x0000000000000008),
                    &Sem::Lit(0x0000000000000001),
                    &Sem::Add(
                        &Sem::Reg("rs1"),
                        &Sem::Sext(
                            64,
                            &Sem::Imm("imm12"),
                        ),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "lbu",
        mask: 0x0000707f,
        value: 0x00004003,
        operands: &["rd", "rs1", "imm12"],
        from: "rv_i",
        source: "RVI-RV64I §3.1.3 — D-LOAD-EXT: LBU zero-extends",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Zext(
                64,
                &Sem::Load(
                    &Sem::Lit(0x0000000000000008),
                    &Sem::Lit(0x0000000000000000),
                    &Sem::Add(
                        &Sem::Reg("rs1"),
                        &Sem::Sext(
                            64,
                            &Sem::Imm("imm12"),
                        ),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "ld",
        mask: 0x0000707f,
        value: 0x00003003,
        operands: &["rd", "rs1", "imm12"],
        from: "rv64_i",
        source: "RVI-RV64I §3.1.3 — a full XLEN load needs no extension",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Load(
                &Sem::Lit(0x0000000000000040),
                &Sem::Lit(0x0000000000000000),
                &Sem::Add(
                    &Sem::Reg("rs1"),
                    &Sem::Sext(
                        64,
                        &Sem::Imm("imm12"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "lh",
        mask: 0x0000707f,
        value: 0x00001003,
        operands: &["rd", "rs1", "imm12"],
        from: "rv_i",
        source: "RVI-RV64I §3.1.3 — D-LOAD-EXT: LH sign-extends",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Load(
                    &Sem::Lit(0x0000000000000010),
                    &Sem::Lit(0x0000000000000001),
                    &Sem::Add(
                        &Sem::Reg("rs1"),
                        &Sem::Sext(
                            64,
                            &Sem::Imm("imm12"),
                        ),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "lhu",
        mask: 0x0000707f,
        value: 0x00005003,
        operands: &["rd", "rs1", "imm12"],
        from: "rv_i",
        source: "RVI-RV64I §3.1.3 — D-LOAD-EXT: LHU zero-extends",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Zext(
                64,
                &Sem::Load(
                    &Sem::Lit(0x0000000000000010),
                    &Sem::Lit(0x0000000000000000),
                    &Sem::Add(
                        &Sem::Reg("rs1"),
                        &Sem::Sext(
                            64,
                            &Sem::Imm("imm12"),
                        ),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "lui",
        mask: 0x0000007f,
        value: 0x00000037,
        operands: &["rd", "imm20"],
        from: "rv_i",
        source: "RVI-RV64I §3.1.2.1 — D-LUI-AUIPC",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Shl(
                    &Sem::Imm("imm20"),
                    &Sem::Lit(0x000000000000000c),
                ),
            ),
        )
    },
    InsnDef {
        name: "lw",
        mask: 0x0000707f,
        value: 0x00002003,
        operands: &["rd", "rs1", "imm12"],
        from: "rv_i",
        source: "RVI-RV64I §3.1.3 — D-LOAD-EXT: LW sign-extends its 32-bit result to 64 bits",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Load(
                    &Sem::Lit(0x0000000000000020),
                    &Sem::Lit(0x0000000000000001),
                    &Sem::Add(
                        &Sem::Reg("rs1"),
                        &Sem::Sext(
                            64,
                            &Sem::Imm("imm12"),
                        ),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "lwu",
        mask: 0x0000707f,
        value: 0x00006003,
        operands: &["rd", "rs1", "imm12"],
        from: "rv64_i",
        source: "RVI-RV64I §3.1.3 — D-LOAD-EXT: LWU zero-extends, and exists only at RV64",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Zext(
                64,
                &Sem::Load(
                    &Sem::Lit(0x0000000000000020),
                    &Sem::Lit(0x0000000000000000),
                    &Sem::Add(
                        &Sem::Reg("rs1"),
                        &Sem::Sext(
                            64,
                            &Sem::Imm("imm12"),
                        ),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "or",
        mask: 0xfe00707f,
        value: 0x00006033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.4",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Or(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "ori",
        mask: 0x0000707f,
        value: 0x00006013,
        operands: &["rd", "rs1", "imm12"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.4",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Or(
                &Sem::Reg("rs1"),
                &Sem::Sext(
                    64,
                    &Sem::Imm("imm12"),
                ),
            ),
        )
    },
    InsnDef {
        name: "sb",
        mask: 0x0000707f,
        value: 0x00000023,
        operands: &["imm12hi", "rs1", "rs2", "imm12lo"],
        from: "rv_i",
        source: "RVI-RV64I §3.1.3 — SB stores the low 8 bits of rs2",
        effect: &Sem::Store(
            &Sem::Lit(0x0000000000000008),
            &Sem::Add(
                &Sem::Reg("rs1"),
                &Sem::Sext(
                    64,
                    &Sem::Imm("imm12"),
                ),
            ),
            &Sem::Trunc(
                8,
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "sd",
        mask: 0x0000707f,
        value: 0x00003023,
        operands: &["imm12hi", "rs1", "rs2", "imm12lo"],
        from: "rv64_i",
        source: "RVI-RV64I §3.1.3 — SD stores the low 64 bits of rs2",
        effect: &Sem::Store(
            &Sem::Lit(0x0000000000000040),
            &Sem::Add(
                &Sem::Reg("rs1"),
                &Sem::Sext(
                    64,
                    &Sem::Imm("imm12"),
                ),
            ),
            &Sem::Reg("rs2"),
        )
    },
    InsnDef {
        name: "sh",
        mask: 0x0000707f,
        value: 0x00001023,
        operands: &["imm12hi", "rs1", "rs2", "imm12lo"],
        from: "rv_i",
        source: "RVI-RV64I §3.1.3 — SH stores the low 16 bits of rs2",
        effect: &Sem::Store(
            &Sem::Lit(0x0000000000000010),
            &Sem::Add(
                &Sem::Reg("rs1"),
                &Sem::Sext(
                    64,
                    &Sem::Imm("imm12"),
                ),
            ),
            &Sem::Trunc(
                16,
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "sll",
        mask: 0xfe00707f,
        value: 0x00001033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_i",
        source: "RVI-RV64I §3.1.2.2 — D-SHAMT: only the low 6 bits of rs2 at XLEN=64",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Shl(
                &Sem::Reg("rs1"),
                &Sem::Bits(
                    5,
                    0,
                    &Sem::Reg("rs2"),
                ),
            ),
        )
    },
    InsnDef {
        name: "slli",
        mask: 0xfc00707f,
        value: 0x00001013,
        operands: &["rd", "rs1", "shamtd"],
        from: "rv64_i",
        source: "RVI-RV64I §3.1.2.1 — D-SHAMT: a 6-bit shift amount at XLEN=64",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Shl(
                &Sem::Reg("rs1"),
                &Sem::Imm("shamt"),
            ),
        )
    },
    InsnDef {
        name: "slliw",
        mask: 0xfe00707f,
        value: 0x0000101b,
        operands: &["rd", "rs1", "shamtw"],
        from: "rv64_i",
        source: "RVI-RV64I §3.1.2.1 — D-SHAMT: a 5-bit amount for the *W shifts",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Trunc(
                    32,
                    &Sem::Shl(
                        &Sem::Trunc(
                            32,
                            &Sem::Reg("rs1"),
                        ),
                        &Sem::Imm("shamt"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "sllw",
        mask: 0xfe00707f,
        value: 0x0000103b,
        operands: &["rd", "rs1", "rs2"],
        from: "rv64_i",
        source: "RVI-RV64I §3.1.2.2 — the *W shifts use rs2[4:0], not rs2[5:0]",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Trunc(
                    32,
                    &Sem::Shl(
                        &Sem::Trunc(
                            32,
                            &Sem::Reg("rs1"),
                        ),
                        &Sem::Bits(
                            4,
                            0,
                            &Sem::Reg("rs2"),
                        ),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "slt",
        mask: 0xfe00707f,
        value: 0x00002033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.4",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Slt(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "slti",
        mask: 0x0000707f,
        value: 0x00002013,
        operands: &["rd", "rs1", "imm12"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.4 — signed comparison, result 0 or 1",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Slt(
                &Sem::Reg("rs1"),
                &Sem::Sext(
                    64,
                    &Sem::Imm("imm12"),
                ),
            ),
        )
    },
    InsnDef {
        name: "sltiu",
        mask: 0x0000707f,
        value: 0x00003013,
        operands: &["rd", "rs1", "imm12"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.4 — the immediate is still SIGN-extended, then compared UNSIGNED",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sltu(
                &Sem::Reg("rs1"),
                &Sem::Sext(
                    64,
                    &Sem::Imm("imm12"),
                ),
            ),
        )
    },
    InsnDef {
        name: "sltu",
        mask: 0xfe00707f,
        value: 0x00003033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.4",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sltu(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "sra",
        mask: 0xfe00707f,
        value: 0x40005033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_i",
        source: "RVI-RV64I §3.1.2.2 — D-SHAMT",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sar(
                &Sem::Reg("rs1"),
                &Sem::Bits(
                    5,
                    0,
                    &Sem::Reg("rs2"),
                ),
            ),
        )
    },
    InsnDef {
        name: "srai",
        mask: 0xfc00707f,
        value: 0x40005013,
        operands: &["rd", "rs1", "shamtd"],
        from: "rv64_i",
        source: "RVI-RV64I §3.1.2.1 — D-SHAMT; arithmetic, the sign bit is replicated",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sar(
                &Sem::Reg("rs1"),
                &Sem::Imm("shamt"),
            ),
        )
    },
    InsnDef {
        name: "sraiw",
        mask: 0xfe00707f,
        value: 0x4000501b,
        operands: &["rd", "rs1", "shamtw"],
        from: "rv64_i",
        source: "RVI-RV64I §3.1.2.1 — arithmetic, on the low 32 bits",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Trunc(
                    32,
                    &Sem::Sar(
                        &Sem::Trunc(
                            32,
                            &Sem::Reg("rs1"),
                        ),
                        &Sem::Imm("shamt"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "sraw",
        mask: 0xfe00707f,
        value: 0x4000503b,
        operands: &["rd", "rs1", "rs2"],
        from: "rv64_i",
        source: "RVI-RV64I §3.1.2.2 — rs2[4:0]",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Trunc(
                    32,
                    &Sem::Sar(
                        &Sem::Trunc(
                            32,
                            &Sem::Reg("rs1"),
                        ),
                        &Sem::Bits(
                            4,
                            0,
                            &Sem::Reg("rs2"),
                        ),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "srl",
        mask: 0xfe00707f,
        value: 0x00005033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_i",
        source: "RVI-RV64I §3.1.2.2 — D-SHAMT",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Shr(
                &Sem::Reg("rs1"),
                &Sem::Bits(
                    5,
                    0,
                    &Sem::Reg("rs2"),
                ),
            ),
        )
    },
    InsnDef {
        name: "srli",
        mask: 0xfc00707f,
        value: 0x00005013,
        operands: &["rd", "rs1", "shamtd"],
        from: "rv64_i",
        source: "RVI-RV64I §3.1.2.1 — D-SHAMT; logical, zeros shifted in",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Shr(
                &Sem::Reg("rs1"),
                &Sem::Imm("shamt"),
            ),
        )
    },
    InsnDef {
        name: "srliw",
        mask: 0xfe00707f,
        value: 0x0000501b,
        operands: &["rd", "rs1", "shamtw"],
        from: "rv64_i",
        source: "RVI-RV64I §3.1.2.1 — logical, on the low 32 bits",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Trunc(
                    32,
                    &Sem::Shr(
                        &Sem::Trunc(
                            32,
                            &Sem::Reg("rs1"),
                        ),
                        &Sem::Imm("shamt"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "srlw",
        mask: 0xfe00707f,
        value: 0x0000503b,
        operands: &["rd", "rs1", "rs2"],
        from: "rv64_i",
        source: "RVI-RV64I §3.1.2.2 — rs2[4:0]",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Trunc(
                    32,
                    &Sem::Shr(
                        &Sem::Trunc(
                            32,
                            &Sem::Reg("rs1"),
                        ),
                        &Sem::Bits(
                            4,
                            0,
                            &Sem::Reg("rs2"),
                        ),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "sub",
        mask: 0xfe00707f,
        value: 0x40000033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.4",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sub(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "subw",
        mask: 0xfe00707f,
        value: 0x4000003b,
        operands: &["rd", "rs1", "rs2"],
        from: "rv64_i",
        source: "RVI-RV64I §3.1.2.2 — D-WSUFFIX",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Trunc(
                    32,
                    &Sem::Sub(
                        &Sem::Trunc(
                            32,
                            &Sem::Reg("rs1"),
                        ),
                        &Sem::Trunc(
                            32,
                            &Sem::Reg("rs2"),
                        ),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "sw",
        mask: 0x0000707f,
        value: 0x00002023,
        operands: &["imm12hi", "rs1", "rs2", "imm12lo"],
        from: "rv_i",
        source: "RVI-RV64I §3.1.3 — SW stores the low 32 bits of rs2",
        effect: &Sem::Store(
            &Sem::Lit(0x0000000000000020),
            &Sem::Add(
                &Sem::Reg("rs1"),
                &Sem::Sext(
                    64,
                    &Sem::Imm("imm12"),
                ),
            ),
            &Sem::Trunc(
                32,
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "xor",
        mask: 0xfe00707f,
        value: 0x00004033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.4",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Xor(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "xori",
        mask: 0x0000707f,
        value: 0x00004013,
        operands: &["rd", "rs1", "imm12"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.4",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Xor(
                &Sem::Reg("rs1"),
                &Sem::Sext(
                    64,
                    &Sem::Imm("imm12"),
                ),
            ),
        )
    },
];

/// One node of a canonical semantics effect, lowered from the S-expression operator
/// language (`schema/semantics.sexp`, the 32 forms `scripts/check_semantics.py`
/// checks) by `scripts/gen_definition.py`. Literals are XLEN-wide two's-complement
/// constants, masked to 64 bits; widths are explicit data everywhere the language
/// states them (`Trunc`/`Sext`/`Zext`/`Bits`). Evaluation — what the forms DO — is
/// the interpreter slice's job (`P1-LAB.8`); this type is the data it evaluates.
#[derive(Clone, Copy, Debug)]
pub enum Sem {
    /// `(lit N)` — an XLEN-wide two's-complement constant.
    Lit(u64),
    /// `(reg NAME)` — an architectural register operand.
    Reg(&'static str),
    /// `(imm NAME)` — an immediate operand.
    Imm(&'static str),
    /// `(pc)` — the address of the executing instruction.
    Pc,
    /// `(xlen)` — the XLEN constant (64 for this profile).
    Xlen,
    /// `(add a b)` — see `schema/semantics.sexp` for the contract.
    Add(&'static Sem, &'static Sem),
    /// `(sub a b)` — see `schema/semantics.sexp` for the contract.
    Sub(&'static Sem, &'static Sem),
    /// `(and a b)` — see `schema/semantics.sexp` for the contract.
    And(&'static Sem, &'static Sem),
    /// `(or a b)` — see `schema/semantics.sexp` for the contract.
    Or(&'static Sem, &'static Sem),
    /// `(xor a b)` — see `schema/semantics.sexp` for the contract.
    Xor(&'static Sem, &'static Sem),
    /// `(shl a b)` — see `schema/semantics.sexp` for the contract.
    Shl(&'static Sem, &'static Sem),
    /// `(shr a b)` — see `schema/semantics.sexp` for the contract.
    Shr(&'static Sem, &'static Sem),
    /// `(sar a b)` — see `schema/semantics.sexp` for the contract.
    Sar(&'static Sem, &'static Sem),
    /// `(slt a b)` — see `schema/semantics.sexp` for the contract.
    Slt(&'static Sem, &'static Sem),
    /// `(sltu a b)` — see `schema/semantics.sexp` for the contract.
    Sltu(&'static Sem, &'static Sem),
    /// `(eq a b)` — see `schema/semantics.sexp` for the contract.
    Eq(&'static Sem, &'static Sem),
    /// `(ne a b)` — see `schema/semantics.sexp` for the contract.
    Ne(&'static Sem, &'static Sem),
    /// `(lt a b)` — see `schema/semantics.sexp` for the contract.
    Lt(&'static Sem, &'static Sem),
    /// `(ltu a b)` — see `schema/semantics.sexp` for the contract.
    Ltu(&'static Sem, &'static Sem),
    /// `(ge a b)` — see `schema/semantics.sexp` for the contract.
    Ge(&'static Sem, &'static Sem),
    /// `(geu a b)` — see `schema/semantics.sexp` for the contract.
    Geu(&'static Sem, &'static Sem),
    /// `(trunc N v)` — the low N bits of `v`.
    Trunc(u64, &'static Sem),
    /// `(sext N v)` — sign-extend the low N bits of `v` to XLEN.
    Sext(u64, &'static Sem),
    /// `(zext N v)` — zero-extend the low N bits of `v` to XLEN.
    Zext(u64, &'static Sem),
    /// `(bits hi lo v)` — the bits [hi:lo] of `v`.
    Bits(u8, u8, &'static Sem),
    /// `(load width signed? addr)` — `signed?` is `1` for sign extension, `0` for
    /// zero extension (D-LOAD-EXT).
    Load(&'static Sem, &'static Sem, &'static Sem),
    /// `(store width addr value)` — the low `width` bits of `value`.
    Store(&'static Sem, &'static Sem, &'static Sem),
    /// `(set (reg rd) value)` — write a register.
    Set(&'static Sem, &'static Sem),
    /// `(set-pc target)` — a control transfer.
    SetPc(&'static Sem),
    /// `(seq a b …)` — effects in order.
    Seq(&'static [&'static Sem]),
    /// `(nop)` — no observable effect (D-FENCE's rule for this profile).
    Nop,
    /// `(if cond then else)` — a semantic branch.
    If(&'static Sem, &'static Sem, &'static Sem),
    /// `(trap cause tval)` — a requested trap (D-ECALL-EBREAK).
    Trap(&'static Sem, &'static Sem),
}

/// Decode a 32-bit word to its instruction definition by the fixed bits: the first
/// entry whose `mask`ed bits equal its `value`. Linear over the 52
/// entries — no allocation, and no failure family of its own: a word no entry
/// matches is the reserved-decode case (`outcome::UndefinedCase::ReservedDecode`,
/// REQ-D-RESERVED-DECODE), and that classification is the caller's, not this
/// table's. Operand extraction and evaluation land with the interpreter slice
/// (`P1-LAB.8`).
#[must_use]
pub fn decode(word: u32) -> Option<&'static InsnDef> {
    INSNS.iter().find(|insn| word & insn.mask == insn.value)
}

#[cfg(test)]
mod tests;
