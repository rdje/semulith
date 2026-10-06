//! GENERATED — do not edit (OWN-03). Regenerate with `python3 scripts/gen_definition.py`;
//! drift between this module and the canonical definition it derives from is refused
//! by the DEF-GEN doctrine (`scripts/check_definition_gen.sh`). These tables are the
//! executable skeleton of the unit's canonical definition (`docs/ARCHITECTURE.md` §2):
//! the decode metadata, the operand-field table, and the semantics effect trees,
//! lowered from rv64gc-lab-v0's composition (base riscv/rv64i + the Zicsr, Zicntr
//! and privileged-system fragments, P4-SYSTEM.2) — including the privileged operator
//! surface of `schema/semantics.sexp`. This module landed tracked at the route
//! flip (P4-SYSTEM.2 slice h, decision_generated-mirror-needs-tracked-input: a
//! tracked generated module needs its canonical inputs tracked in the same commit).
//!
//! OWN-01: every semantic rule has exactly one executable owner — the semantics
//! DATA. This module is its lowered mirror; there is no handwritten second copy of
//! any rule, and the interpreter slice (`P1-LAB.8`) evaluates exactly these trees.
//!
//! Canonical inputs (sha256):
//!   `definitions/riscv/a.sem.sexp`  `929f7d11f11856e303460d4f4c9f5094314a8090ce7ce710efe83fb5dfb9c306`
//!   `definitions/riscv/a.sexp`  `f5e99591cadc1500bbc8333c95cd0c4548aae0d7aa007dfb9fd6bdfeb56ebe1b`
//!   `definitions/riscv/rv64i.sem.sexp`  `c3065957307cc3fe1d58005a533e0d7291fe66ae7b05d6f8be4747e18a3aa29e`
//!   `definitions/riscv/rv64i.sexp`  `f45071eef9894463259482191cc464fa79df59af04b16e5c10f6c3a7342e0278`
//!   `definitions/riscv/system.sem.sexp`  `cb25de97e2197c5d443779f28579589dd1384bf9eb1ae0028166678bdd94692b`
//!   `definitions/riscv/system.sexp`  `c89d687d7a52c8e1cb19e8d87633c0f3bc70a7e7819f3ba8e2c3e895f20518e9`
//!   `definitions/riscv/zicntr.sem.sexp`  `9308b046ae1213e4302a2258c55e17e4f12f2d81f7e10c9a2e248646084b7570`
//!   `definitions/riscv/zicntr.sexp`  `f0c483e24e2515c12f32d2a95ac55be3a663e2c7ca355cc804890a2f2c3bc675`
//!   `definitions/riscv/zicsr.sem.sexp`  `823278a9ab48c7f95005998d183e5127f76d6c8c276f70f74a58e4cf22b64975`
//!   `definitions/riscv/zicsr.sexp`  `f2cd1ab3c64e343a6456b2ce81f506e097d1e25de523522f2577dc377b6e78e2`
//!   `definitions/riscv/zifencei.sem.sexp`  `048555ac8a792789fb534d37d05c0f099a658f822520689e214265ecd2afcd5c`
//!   `definitions/riscv/zifencei.sexp`  `7e3c6eebb4cffe383504979c83098cd2807bf90ee23c254ab4f94cad139a5003`
//!   `profiles/rv64gc-lab-v0/encoding.sexp`  `3dd1ab658eed1a72e95b9a13108e7701d0fc59c9c8e9605c631bcaebfcabfe33`
//!   `profiles/rv64gc-lab-v0/state.sexp`  `ea6c4ef14b592100f3c691ea64e71bf6851928a076b1628c95570ab372736e4b`
//! Generator: `scripts/gen_definition.py` (sha256 `11244266f1e953d5d71243027dbf890c90853b129f0ade99e94f469e170757a9`)

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
    profile: "rv64gc-lab-v0",
    ilen: 32,
    fragments: &[
        "riscv/rv64i",
        "riscv/zicsr",
        "riscv/zicntr",
        "riscv/system",
        "riscv/a",
        "riscv/zifencei",
    ],
    generator: GeneratorPin {
        name: "scripts/gen_definition.py",
        sha256: "11244266f1e953d5d71243027dbf890c90853b129f0ade99e94f469e170757a9",
    },
    inputs: &[
        InputPin {
            path: "definitions/riscv/a.sem.sexp",
            sha256: "929f7d11f11856e303460d4f4c9f5094314a8090ce7ce710efe83fb5dfb9c306",
        },
        InputPin {
            path: "definitions/riscv/a.sexp",
            sha256: "f5e99591cadc1500bbc8333c95cd0c4548aae0d7aa007dfb9fd6bdfeb56ebe1b",
        },
        InputPin {
            path: "definitions/riscv/rv64i.sem.sexp",
            sha256: "c3065957307cc3fe1d58005a533e0d7291fe66ae7b05d6f8be4747e18a3aa29e",
        },
        InputPin {
            path: "definitions/riscv/rv64i.sexp",
            sha256: "f45071eef9894463259482191cc464fa79df59af04b16e5c10f6c3a7342e0278",
        },
        InputPin {
            path: "definitions/riscv/system.sem.sexp",
            sha256: "cb25de97e2197c5d443779f28579589dd1384bf9eb1ae0028166678bdd94692b",
        },
        InputPin {
            path: "definitions/riscv/system.sexp",
            sha256: "c89d687d7a52c8e1cb19e8d87633c0f3bc70a7e7819f3ba8e2c3e895f20518e9",
        },
        InputPin {
            path: "definitions/riscv/zicntr.sem.sexp",
            sha256: "9308b046ae1213e4302a2258c55e17e4f12f2d81f7e10c9a2e248646084b7570",
        },
        InputPin {
            path: "definitions/riscv/zicntr.sexp",
            sha256: "f0c483e24e2515c12f32d2a95ac55be3a663e2c7ca355cc804890a2f2c3bc675",
        },
        InputPin {
            path: "definitions/riscv/zicsr.sem.sexp",
            sha256: "823278a9ab48c7f95005998d183e5127f76d6c8c276f70f74a58e4cf22b64975",
        },
        InputPin {
            path: "definitions/riscv/zicsr.sexp",
            sha256: "f2cd1ab3c64e343a6456b2ce81f506e097d1e25de523522f2577dc377b6e78e2",
        },
        InputPin {
            path: "definitions/riscv/zifencei.sem.sexp",
            sha256: "048555ac8a792789fb534d37d05c0f099a658f822520689e214265ecd2afcd5c",
        },
        InputPin {
            path: "definitions/riscv/zifencei.sexp",
            sha256: "7e3c6eebb4cffe383504979c83098cd2807bf90ee23c254ab4f94cad139a5003",
        },
        InputPin {
            path: "profiles/rv64gc-lab-v0/encoding.sexp",
            sha256: "3dd1ab658eed1a72e95b9a13108e7701d0fc59c9c8e9605c631bcaebfcabfe33",
        },
        InputPin {
            path: "profiles/rv64gc-lab-v0/state.sexp",
            sha256: "ea6c4ef14b592100f3c691ea64e71bf6851928a076b1628c95570ab372736e4b",
        },
    ],
    sources: &[
        SourcePin {
            file: "rv64_a",
            sha256: "819e0487131bc97cfc0b6f3de62390f2f9936b43e80aef7c6cec14fbe7c7a1b6",
        },
        SourcePin {
            file: "rv64_i",
            sha256: "262cbd0884fe1383fcb7c42070cbc73e309d0452ff8d00b38452a4dee7cfa7f5",
        },
        SourcePin {
            file: "rv_a",
            sha256: "d9eaa988c4779ca352d9da9eabacf6c71771d0b81e04b234302627f69e0863d9",
        },
        SourcePin {
            file: "rv_i",
            sha256: "146e297ddbe346f325d993aaf56d7006f1bfde39df584b888b221543def17b97",
        },
        SourcePin {
            file: "rv_s",
            sha256: "e9d509a3a46de9024547fa75f76bf3c2839910ebc9af81d106cc46bc0ac6eb78",
        },
        SourcePin {
            file: "rv_system",
            sha256: "4a58b5f0c908d7b748abbeb9df8335dbc53650ea284b738e4351afd49755e646",
        },
        SourcePin {
            file: "rv_zicntr",
            sha256: "34ed6bb1cf98448c7c40abbd6f67cbccee0788bd42429a2b1a9538952f6cca8c",
        },
        SourcePin {
            file: "rv_zicsr",
            sha256: "dd8cc0e2c32fb5658d4aa719cef6ab1b714e2145ba071c9aeb382d9963e4901f",
        },
        SourcePin {
            file: "rv_zifencei",
            sha256: "be2d8f7286e06fadafffbde14656e6adb3f923ce704ea0829229d3a3b5f35758",
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

/// The 19 operand fields the composed fragments declare, sorted by
/// name: what the decoder extracts, and how the scrambled immediates unscramble.
/// Every declared operand names a field — this generator refuses one that does not,
/// because extraction for it would be silent (ARCHITECTURE §2: an unsupported
/// construct is a model-generation failure, never a guessed translation).
pub static FIELDS: &[FieldDef] = &[
    FieldDef {
        name: "aq",
        hi: 26,
        lo: 26,
        scatter: &[],
    },
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
        name: "csr",
        hi: 31,
        lo: 20,
        scatter: &[],
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
        name: "rl",
        hi: 25,
        lo: 25,
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
    FieldDef {
        name: "zimm5",
        hi: 19,
        lo: 15,
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

/// The 85 instructions of the composed definition, sorted by name. Every
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
        name: "amoadd.d",
        mask: 0xf800707f,
        value: 0x0000302f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv64_a",
        source: "RVI-A §12.1.4 — AMOADD.D atomically adds rs2's 64 bits to the memory doubleword at rs1's address and writes the OLD doubleword to rd (op 0x00, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Amo(
                0,
                &Sem::Lit(0x0000000000000040),
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "amoadd.w",
        mask: 0xf800707f,
        value: 0x0000202f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv_a",
        source: "RVI-A §12.1.4 — AMOADD.W atomically adds rs2's low 32 bits to the memory word at rs1's address and writes the OLD word, sign-extended, to rd (op 0x00, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Amo(
                    0,
                    &Sem::Lit(0x0000000000000020),
                    &Sem::Reg("rs1"),
                    &Sem::Trunc(
                        32,
                        &Sem::Reg("rs2"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "amoand.d",
        mask: 0xf800707f,
        value: 0x6000302f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv64_a",
        source: "RVI-A §12.1.4 — AMOAND.D atomically ANDs rs2's 64 bits into the memory doubleword at rs1's address and writes the OLD doubleword to rd (op 0x0c, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Amo(
                12,
                &Sem::Lit(0x0000000000000040),
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "amoand.w",
        mask: 0xf800707f,
        value: 0x6000202f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv_a",
        source: "RVI-A §12.1.4 — AMOAND.W atomically ANDs rs2's low 32 bits into the memory word at rs1's address and writes the OLD word, sign-extended, to rd (op 0x0c, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Amo(
                    12,
                    &Sem::Lit(0x0000000000000020),
                    &Sem::Reg("rs1"),
                    &Sem::Trunc(
                        32,
                        &Sem::Reg("rs2"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "amomax.d",
        mask: 0xf800707f,
        value: 0xa000302f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv64_a",
        source: "RVI-A §12.1.4 — AMOMAX.D atomically takes the signed maximum of the memory doubleword at rs1's address and rs2's 64 bits, and writes the OLD doubleword to rd (op 0x14, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Amo(
                20,
                &Sem::Lit(0x0000000000000040),
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "amomax.w",
        mask: 0xf800707f,
        value: 0xa000202f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv_a",
        source: "RVI-A §12.1.4 — AMOMAX.W atomically takes the signed maximum of the memory word at rs1's address and rs2's low 32 bits, and writes the OLD word, sign-extended, to rd (op 0x14, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Amo(
                    20,
                    &Sem::Lit(0x0000000000000020),
                    &Sem::Reg("rs1"),
                    &Sem::Trunc(
                        32,
                        &Sem::Reg("rs2"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "amomaxu.d",
        mask: 0xf800707f,
        value: 0xe000302f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv64_a",
        source: "RVI-A §12.1.4 — AMOMAXU.D atomically takes the unsigned maximum of the memory doubleword at rs1's address and rs2's 64 bits, and writes the OLD doubleword to rd (op 0x1c, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Amo(
                28,
                &Sem::Lit(0x0000000000000040),
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "amomaxu.w",
        mask: 0xf800707f,
        value: 0xe000202f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv_a",
        source: "RVI-A §12.1.4 — AMOMAXU.W atomically takes the unsigned maximum of the memory word at rs1's address and rs2's low 32 bits, and writes the OLD word, sign-extended, to rd (op 0x1c, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Amo(
                    28,
                    &Sem::Lit(0x0000000000000020),
                    &Sem::Reg("rs1"),
                    &Sem::Trunc(
                        32,
                        &Sem::Reg("rs2"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "amomin.d",
        mask: 0xf800707f,
        value: 0x8000302f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv64_a",
        source: "RVI-A §12.1.4 — AMOMIN.D atomically takes the signed minimum of the memory doubleword at rs1's address and rs2's 64 bits, and writes the OLD doubleword to rd (op 0x10, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Amo(
                16,
                &Sem::Lit(0x0000000000000040),
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "amomin.w",
        mask: 0xf800707f,
        value: 0x8000202f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv_a",
        source: "RVI-A §12.1.4 — AMOMIN.W atomically takes the signed minimum of the memory word at rs1's address and rs2's low 32 bits, and writes the OLD word, sign-extended, to rd (op 0x10, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Amo(
                    16,
                    &Sem::Lit(0x0000000000000020),
                    &Sem::Reg("rs1"),
                    &Sem::Trunc(
                        32,
                        &Sem::Reg("rs2"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "amominu.d",
        mask: 0xf800707f,
        value: 0xc000302f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv64_a",
        source: "RVI-A §12.1.4 — AMOMINU.D atomically takes the unsigned minimum of the memory doubleword at rs1's address and rs2's 64 bits, and writes the OLD doubleword to rd (op 0x18, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Amo(
                24,
                &Sem::Lit(0x0000000000000040),
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "amominu.w",
        mask: 0xf800707f,
        value: 0xc000202f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv_a",
        source: "RVI-A §12.1.4 — AMOMINU.W atomically takes the unsigned minimum of the memory word at rs1's address and rs2's low 32 bits, and writes the OLD word, sign-extended, to rd (op 0x18, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Amo(
                    24,
                    &Sem::Lit(0x0000000000000020),
                    &Sem::Reg("rs1"),
                    &Sem::Trunc(
                        32,
                        &Sem::Reg("rs2"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "amoor.d",
        mask: 0xf800707f,
        value: 0x4000302f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv64_a",
        source: "RVI-A §12.1.4 — AMOOR.D atomically ORs rs2's 64 bits into the memory doubleword at rs1's address and writes the OLD doubleword to rd (op 0x08, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Amo(
                8,
                &Sem::Lit(0x0000000000000040),
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "amoor.w",
        mask: 0xf800707f,
        value: 0x4000202f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv_a",
        source: "RVI-A §12.1.4 — AMOOR.W atomically ORs rs2's low 32 bits into the memory word at rs1's address and writes the OLD word, sign-extended, to rd (op 0x08, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Amo(
                    8,
                    &Sem::Lit(0x0000000000000020),
                    &Sem::Reg("rs1"),
                    &Sem::Trunc(
                        32,
                        &Sem::Reg("rs2"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "amoswap.d",
        mask: 0xf800707f,
        value: 0x0800302f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv64_a",
        source: "RVI-A §12.1.4 — AMOSWAP.D atomically writes rs2's 64 bits to the memory doubleword at rs1's address and writes the OLD doubleword to rd (op 0x01, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Amo(
                1,
                &Sem::Lit(0x0000000000000040),
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "amoswap.w",
        mask: 0xf800707f,
        value: 0x0800202f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv_a",
        source: "RVI-A §12.1.4 — AMOSWAP.W atomically writes rs2's low 32 bits to the memory word at rs1's address and writes the OLD word, sign-extended, to rd (op 0x01, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Amo(
                    1,
                    &Sem::Lit(0x0000000000000020),
                    &Sem::Reg("rs1"),
                    &Sem::Trunc(
                        32,
                        &Sem::Reg("rs2"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "amoxor.d",
        mask: 0xf800707f,
        value: 0x2000302f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv64_a",
        source: "RVI-A §12.1.4 — AMOXOR.D atomically XORs rs2's 64 bits into the memory doubleword at rs1's address and writes the OLD doubleword to rd (op 0x04, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Amo(
                4,
                &Sem::Lit(0x0000000000000040),
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "amoxor.w",
        mask: 0xf800707f,
        value: 0x2000202f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv_a",
        source: "RVI-A §12.1.4 — AMOXOR.W atomically XORs rs2's low 32 bits into the memory word at rs1's address and writes the OLD word, sign-extended, to rd (op 0x04, the encoding's own funct5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Amo(
                    4,
                    &Sem::Lit(0x0000000000000020),
                    &Sem::Reg("rs1"),
                    &Sem::Trunc(
                        32,
                        &Sem::Reg("rs2"),
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
        name: "csrrc",
        mask: 0x0000707f,
        value: 0x00003073,
        operands: &["rd", "rs1", "csr"],
        from: "rv_zicsr",
        source: "RVI-ZICSR §5.1.1 — atomic read and clear bits; if rs1=x0 the instruction shall not write the CSR",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Field("rs1"),
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::CsrRead(
                    &Sem::Field("csr"),
                ),
            ),
            &Sem::Seq(&[
                &Sem::Set(
                    &Sem::Reg("rd"),
                    &Sem::CsrRead(
                        &Sem::Field("csr"),
                    ),
                ),
                &Sem::CsrWrite(
                    &Sem::Field("csr"),
                    &Sem::And(
                        &Sem::CsrRead(
                            &Sem::Field("csr"),
                        ),
                        &Sem::Xor(
                            &Sem::Reg("rs1"),
                            &Sem::Lit(0xffffffffffffffff),
                        ),
                    ),
                ),
            ]),
        )
    },
    InsnDef {
        name: "csrrci",
        mask: 0x0000707f,
        value: 0x00007073,
        operands: &["rd", "csr", "zimm5"],
        from: "rv_zicsr",
        source: "RVI-ZICSR §5.1.1 — CSRRC with a zero-extended 5-bit immediate; if uimm=0 the instruction shall not write the CSR",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Field("zimm5"),
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::CsrRead(
                    &Sem::Field("csr"),
                ),
            ),
            &Sem::Seq(&[
                &Sem::Set(
                    &Sem::Reg("rd"),
                    &Sem::CsrRead(
                        &Sem::Field("csr"),
                    ),
                ),
                &Sem::CsrWrite(
                    &Sem::Field("csr"),
                    &Sem::And(
                        &Sem::CsrRead(
                            &Sem::Field("csr"),
                        ),
                        &Sem::Xor(
                            &Sem::Zext(
                                64,
                                &Sem::Field("zimm5"),
                            ),
                            &Sem::Lit(0xffffffffffffffff),
                        ),
                    ),
                ),
            ]),
        )
    },
    InsnDef {
        name: "csrrs",
        mask: 0x0000707f,
        value: 0x00002073,
        operands: &["rd", "rs1", "csr"],
        from: "rv_zicsr",
        source: "RVI-ZICSR §5.1.1 — atomic read and set bits; if rs1=x0 the instruction shall not write the CSR",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Field("rs1"),
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::CsrRead(
                    &Sem::Field("csr"),
                ),
            ),
            &Sem::Seq(&[
                &Sem::Set(
                    &Sem::Reg("rd"),
                    &Sem::CsrRead(
                        &Sem::Field("csr"),
                    ),
                ),
                &Sem::CsrWrite(
                    &Sem::Field("csr"),
                    &Sem::Or(
                        &Sem::CsrRead(
                            &Sem::Field("csr"),
                        ),
                        &Sem::Reg("rs1"),
                    ),
                ),
            ]),
        )
    },
    InsnDef {
        name: "csrrsi",
        mask: 0x0000707f,
        value: 0x00006073,
        operands: &["rd", "csr", "zimm5"],
        from: "rv_zicsr",
        source: "RVI-ZICSR §5.1.1 — CSRRS with a zero-extended 5-bit immediate; if uimm=0 the instruction shall not write the CSR",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Field("zimm5"),
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::CsrRead(
                    &Sem::Field("csr"),
                ),
            ),
            &Sem::Seq(&[
                &Sem::Set(
                    &Sem::Reg("rd"),
                    &Sem::CsrRead(
                        &Sem::Field("csr"),
                    ),
                ),
                &Sem::CsrWrite(
                    &Sem::Field("csr"),
                    &Sem::Or(
                        &Sem::CsrRead(
                            &Sem::Field("csr"),
                        ),
                        &Sem::Zext(
                            64,
                            &Sem::Field("zimm5"),
                        ),
                    ),
                ),
            ]),
        )
    },
    InsnDef {
        name: "csrrw",
        mask: 0x0000707f,
        value: 0x00001073,
        operands: &["rd", "rs1", "csr"],
        from: "rv_zicsr",
        source: "RVI-ZICSR §5.1.1 — atomic read/write CSR; if rd=x0 the instruction shall not read the CSR",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Field("rd"),
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::CsrWrite(
                &Sem::Field("csr"),
                &Sem::Reg("rs1"),
            ),
            &Sem::Seq(&[
                &Sem::Set(
                    &Sem::Reg("rd"),
                    &Sem::CsrRead(
                        &Sem::Field("csr"),
                    ),
                ),
                &Sem::CsrWrite(
                    &Sem::Field("csr"),
                    &Sem::Reg("rs1"),
                ),
            ]),
        )
    },
    InsnDef {
        name: "csrrwi",
        mask: 0x0000707f,
        value: 0x00005073,
        operands: &["rd", "csr", "zimm5"],
        from: "rv_zicsr",
        source: "RVI-ZICSR §5.1.1 — CSRRW with a zero-extended 5-bit immediate; if rd=x0 the instruction shall not read the CSR",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Field("rd"),
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::CsrWrite(
                &Sem::Field("csr"),
                &Sem::Zext(
                    64,
                    &Sem::Field("zimm5"),
                ),
            ),
            &Sem::Seq(&[
                &Sem::Set(
                    &Sem::Reg("rd"),
                    &Sem::CsrRead(
                        &Sem::Field("csr"),
                    ),
                ),
                &Sem::CsrWrite(
                    &Sem::Field("csr"),
                    &Sem::Zext(
                        64,
                        &Sem::Field("zimm5"),
                    ),
                ),
            ]),
        )
    },
    InsnDef {
        name: "ebreak",
        mask: 0xffffffff,
        value: 0x00100073,
        operands: &[],
        from: "rv_i",
        source: "RVP-MACHINE §2.1.3.1 — cause 3 (breakpoint); xtval is the instruction's own address (measured tval=pc on both reference models)",
        effect: &Sem::TrapDeliver(
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
        source: "RVP-MACHINE §2.1.3.1 — the cause names the ORIGINATING mode (U=8, S=9, M=11); xtval is 0 (measured on both reference models)",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Mode,
                &Sem::Lit(0x0000000000000003),
            ),
            &Sem::TrapDeliver(
                &Sem::Lit(0x000000000000000b),
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::If(
                &Sem::Eq(
                    &Sem::Mode,
                    &Sem::Lit(0x0000000000000001),
                ),
                &Sem::TrapDeliver(
                    &Sem::Lit(0x0000000000000009),
                    &Sem::Lit(0x0000000000000000),
                ),
                &Sem::TrapDeliver(
                    &Sem::Lit(0x0000000000000008),
                    &Sem::Lit(0x0000000000000000),
                ),
            ),
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
        name: "fence.i",
        mask: 0x0000707f,
        value: 0x0000100f,
        operands: &["imm12", "rs1", "rd"],
        from: "rv_zifencei",
        source: "RVI-ZIFENCEI §4.1 — the declared nop: the coherent/uncached-RAM latitude ('just the fetch pipeline needs to be flushed at a FENCE.I') meets a re-read-per-fetch machine (nothing to flush, D-CODE-VISIBILITY); funct12/rs1/rd decoded-and-ignored per the chapter's shall-ignore rule, never legalization-rejected",
        effect: &Sem::Nop
    },
    InsnDef {
        name: "jal",
        mask: 0x0000007f,
        value: 0x0000006f,
        operands: &["rd", "jimm20"],
        from: "rv_i",
        source: "RVI-RV32I §1.1.5.1 — JAL adds the offset to THIS instruction's address and stores pc+4 in rd; the misaligned-target check precedes the link write (§1.1.5.2)",
        effect: &Sem::Seq(&[
            &Sem::SetPc(
                &Sem::Add(
                    &Sem::Pc,
                    &Sem::Sext(
                        64,
                        &Sem::Imm("jimm20"),
                    ),
                ),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Add(
                    &Sem::Pc,
                    &Sem::Lit(0x0000000000000004),
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
        source: "RVI-RV32I §1.1.5.1 — D-JALR-LSB: add, THEN set the least-significant bit to zero; the misaligned-target check precedes the link write (§1.1.5.2)",
        effect: &Sem::Seq(&[
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
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Add(
                    &Sem::Pc,
                    &Sem::Lit(0x0000000000000004),
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
        name: "lr.d",
        mask: 0xf9f0707f,
        value: 0x1000302f,
        operands: &["rd", "rs1", "aq", "rl"],
        from: "rv64_a",
        source: "RVI-A §12.1.2 — LR.D loads a doubleword from rs1's address into rd and registers a reservation on the addressed bytes; a full XLEN load needs no extension",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::LoadReserved(
                &Sem::Lit(0x0000000000000040),
                &Sem::Lit(0x0000000000000000),
                &Sem::Reg("rs1"),
            ),
        )
    },
    InsnDef {
        name: "lr.w",
        mask: 0xf9f0707f,
        value: 0x1000202f,
        operands: &["rd", "rs1", "aq", "rl"],
        from: "rv_a",
        source: "RVI-A §12.1.2 — LR.W loads a word from rs1's address, sign-extends it into rd, and registers a reservation on the addressed bytes (the reservation contract is the operators', schema/semantics.sexp)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::LoadReserved(
                    &Sem::Lit(0x0000000000000020),
                    &Sem::Lit(0x0000000000000001),
                    &Sem::Reg("rs1"),
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
        name: "mret",
        mask: 0xffffffff,
        value: 0x30200073,
        operands: &[],
        from: "rv_system",
        source: "RVP-MACHINE §2.1.3.2 — xRET executes in mode x or higher; in a less-privileged mode it raises illegal-instruction (xtval = the instruction word)",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Mode,
                &Sem::Lit(0x0000000000000003),
            ),
            &Sem::Xret(
                &Sem::Lit(0x0000000000000003),
            ),
            &Sem::TrapDeliver(
                &Sem::Lit(0x0000000000000002),
                &Sem::Inst,
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
        name: "sc.d",
        mask: 0xf800707f,
        value: 0x1800302f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv64_a",
        source: "RVI-A §12.1.2 — SC.D conditionally stores rs2's 64 bits to rs1's address and writes the code to rd (0 success / 1 failure); success or failure, the reservation is cleared — the section's own sentence",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::StoreConditional(
                &Sem::Lit(0x0000000000000040),
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "sc.w",
        mask: 0xf800707f,
        value: 0x1800202f,
        operands: &["rd", "rs1", "rs2", "aq", "rl"],
        from: "rv_a",
        source: "RVI-A §12.1.2 — SC.W conditionally stores rs2's low 32 bits to rs1's address and writes the code to rd (0 success / 1 failure; the deterministic never-spurious policy is decision 3's, stated at the operator); success or failure, the reservation is cleared — the section's own sentence",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::StoreConditional(
                &Sem::Lit(0x0000000000000020),
                &Sem::Reg("rs1"),
                &Sem::Trunc(
                    32,
                    &Sem::Reg("rs2"),
                ),
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
        name: "sfence.vma",
        mask: 0xfe007fff,
        value: 0x12000073,
        operands: &["rs1", "rs2"],
        from: "rv_s",
        source: "RVP-SUPERVISOR §11.1.2.1 — the translation fence; illegal in U (§11.1.9's shared-permission sentence) and in S with mstatus.TVM=1 (RVP-MACHINE §2.1.1.6.6; TVM is bit 20); the invalidation effect is the four specified cases over the modelled TLB (P4-SYSTEM.3 decision 2; the header records the superseded time-scoped nop)",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Mode,
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::TrapDeliver(
                &Sem::Lit(0x0000000000000002),
                &Sem::Inst,
            ),
            &Sem::If(
                &Sem::And(
                    &Sem::Eq(
                        &Sem::Mode,
                        &Sem::Lit(0x0000000000000001),
                    ),
                    &Sem::Ne(
                        &Sem::Bits(
                            20,
                            20,
                            &Sem::CsrState(
                                &Sem::Lit(0x0000000000000300),
                            ),
                        ),
                        &Sem::Lit(0x0000000000000000),
                    ),
                ),
                &Sem::TrapDeliver(
                    &Sem::Lit(0x0000000000000002),
                    &Sem::Inst,
                ),
                &Sem::TlbInvalidate(
                    &Sem::Reg("rs1"),
                    &Sem::Reg("rs2"),
                ),
            ),
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
        name: "sret",
        mask: 0xffffffff,
        value: 0x10200073,
        operands: &[],
        from: "rv_s",
        source: "RVP-MACHINE §2.1.3.2 — legal in M and in S, illegal in U; in S with mstatus.TSR=1 it raises illegal-instruction (§2.1.1.6.6; TSR is bit 22, mstatus is 0x300 — the pinned encoding.h masks)",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Mode,
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::TrapDeliver(
                &Sem::Lit(0x0000000000000002),
                &Sem::Inst,
            ),
            &Sem::If(
                &Sem::And(
                    &Sem::Eq(
                        &Sem::Mode,
                        &Sem::Lit(0x0000000000000001),
                    ),
                    &Sem::Ne(
                        &Sem::Bits(
                            22,
                            22,
                            &Sem::CsrState(
                                &Sem::Lit(0x0000000000000300),
                            ),
                        ),
                        &Sem::Lit(0x0000000000000000),
                    ),
                ),
                &Sem::TrapDeliver(
                    &Sem::Lit(0x0000000000000002),
                    &Sem::Inst,
                ),
                &Sem::Xret(
                    &Sem::Lit(0x0000000000000001),
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
        name: "wfi",
        mask: 0xffffffff,
        value: 0x10500073,
        operands: &[],
        from: "rv_system",
        source: "RVP-MACHINE §2.1.3.3 — legality: illegal in U with S present, illegal in S with mstatus.TW=1 (§2.1.1.6.6; TW is bit 21), always legal in M; a LEGAL wfi enters the wait state — the halt entry is the step machinery's (P4-SYSTEM.5 decision 4; the nop latitude recorded-not-taken, the header)",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Mode,
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::TrapDeliver(
                &Sem::Lit(0x0000000000000002),
                &Sem::Inst,
            ),
            &Sem::If(
                &Sem::And(
                    &Sem::Lt(
                        &Sem::Mode,
                        &Sem::Lit(0x0000000000000003),
                    ),
                    &Sem::Ne(
                        &Sem::Bits(
                            21,
                            21,
                            &Sem::CsrState(
                                &Sem::Lit(0x0000000000000300),
                            ),
                        ),
                        &Sem::Lit(0x0000000000000000),
                    ),
                ),
                &Sem::TrapDeliver(
                    &Sem::Lit(0x0000000000000002),
                    &Sem::Inst,
                ),
                &Sem::Nop,
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
/// language (`schema/semantics.sexp`, the 43 forms `scripts/check_semantics.py`
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
    /// `(field NAME)` — the RAW numeric value of an operand field (a register
    /// index, a csr address, a zimm5), not the register the field names.
    Field(&'static str),
    /// `(inst)` — the instruction word (illegal-instruction xtval carries it).
    Inst,
    /// `(mode)` — the current privilege mode (0=U, 1=S, 3=M).
    Mode,
    /// `(csr-state a)` — the machine's own read of CSR state (no permission model).
    CsrState(&'static Sem),
    /// `(csr-read a)` — an architectural CSR read under the uniform permission model.
    CsrRead(&'static Sem),
    /// `(csr-write a v)` — an architectural CSR write, legalized per the state
    /// document's declared per-field tables.
    CsrWrite(&'static Sem, &'static Sem),
    /// `(trap-deliver cause tval)` — synchronous trap delivery: delegation,
    /// the xPIE/xIE/xPP stack, xepc/xcause/xtval, pc <- xtvec.
    TrapDeliver(&'static Sem, &'static Sem),
    /// `(xret x)` — the privilege-stack pop and pc <- xepc.
    Xret(&'static Sem),
    /// `(tlb-invalidate va asid)` — SFENCE.VMA's four specified invalidation
    /// cases over the modelled TLB (RVP-SUPERVISOR §11.1.2.1; P4-SYSTEM.3).
    TlbInvalidate(&'static Sem, &'static Sem),
    /// `(load-reserved width signed? addr)` — LR's load: translates under the
    /// load rules, sets/replaces the hart's reservation (physical address,
    /// width, valid), yields the loaded value (RVI-A §12.1.2).
    LoadReserved(&'static Sem, &'static Sem, &'static Sem),
    /// `(store-conditional width addr value)` — SC: success (reservation valid
    /// ∧ physical address ∧ width match) writes and yields 0; failure writes
    /// nothing and yields 1; the reservation is cleared either way (the
    /// deterministic policy, P4-SYSTEM.4 decision 3).
    StoreConditional(&'static Sem, &'static Sem, &'static Sem),
    /// `(amo op width addr value)` — one of the closed Zaamo nine (op the
    /// funct5 encoding): one store/AMO-rules translation, the old value read,
    /// op applied at width, the result written, the old value yielded —
    /// never a seq(load, op, store) (P4-SYSTEM.4 decision 5).
    Amo(u64, &'static Sem, &'static Sem, &'static Sem),
}

/// Decode a 32-bit word to its instruction definition by the fixed bits: the first
/// entry whose `mask`ed bits equal its `value`. Linear over the 85
/// entries — no allocation, and no failure family of its own: a word no entry
/// matches is the reserved-decode case (`outcome::UndefinedCase::ReservedDecode`,
/// REQ-D-RESERVED-DECODE), and that classification is the caller's, not this
/// table's. Operand extraction and evaluation land with the interpreter slice
/// (`P1-LAB.8`).
#[must_use]
pub fn decode(word: u32) -> Option<&'static InsnDef> {
    INSNS.iter().find(|insn| word & insn.mask == insn.value)
}

/// One pseudo-instruction of the composition (Zicntr's counter reads): an
/// assembler spelling whose encoding SPECIALIZES a real instruction's — it adds
/// nothing to the decode space (check_encoding_disjoint's specialization rule),
/// so it never appears in INSNS; the row exists so the coverage census maps the
/// architectural spelling to the realizing instruction (P4-SYSTEM.2 slice f).
pub struct PseudoDef {
    pub name: &'static str,
    /// The realizing instruction (the pinned table's `of` base).
    pub of: &'static str,
    pub mask: u32,
    pub value: u32,
    pub operands: &'static [&'static str],
    /// The specification locator the pseudo's semantics rule cites.
    pub source: &'static str,
}

/// The 3 pseudo-instructions, sorted by name.
pub static PSEUDOS: &[PseudoDef] = &[
    PseudoDef {
        name: "rdcycle",
        of: "rv_zicsr::csrrs",
        mask: 0xfffff07f,
        value: 0xc0002073,
        operands: &["rd"],
        source: "RVI-ZICNTR §6.1.1 — reads the cycle counter (csr 0xC00, the pinned rv_zicntr row); counter-enable gating is csr-read's (RVP-MACHINE §2.1.1.11, RVP-SUPERVISOR §11.1.1.5)",
    },
    PseudoDef {
        name: "rdinstret",
        of: "rv_zicsr::csrrs",
        mask: 0xfffff07f,
        value: 0xc0202073,
        operands: &["rd"],
        source: "RVI-ZICNTR §6.1.1 — reads the instret counter (csr 0xC02, the pinned rv_zicntr row); counter-enable gating is csr-read's (RVP-MACHINE §2.1.1.11, RVP-SUPERVISOR §11.1.1.5)",
    },
    PseudoDef {
        name: "rdtime",
        of: "rv_zicsr::csrrs",
        mask: 0xfffff07f,
        value: 0xc0102073,
        operands: &["rd"],
        source: "RVI-ZICNTR §6.1.1 — reads the time counter (csr 0xC01, the pinned rv_zicntr row); counter-enable gating is csr-read's (RVP-MACHINE §2.1.1.11, RVP-SUPERVISOR §11.1.1.5)",
    },
];
