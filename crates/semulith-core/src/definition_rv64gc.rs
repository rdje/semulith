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
//!   `definitions/riscv/d.sem.sexp`  `92e92f9242414c53f2297962a236e9318822318acb322cb65fe4969e63ac375e`
//!   `definitions/riscv/d.sexp`  `c0cdc058273c25ac636adb33761aac51956a534c161f17db51e5b34ebe6f0dc0`
//!   `definitions/riscv/f.sem.sexp`  `fea32f7229d98271567372e618838f725fe9acb66d5f355ee49caf7fc071e49e`
//!   `definitions/riscv/f.sexp`  `4d3232c6f9c9298c6814fce8c4865ae103a46f4308b7649d7b4a71be02c28a9a`
//!   `definitions/riscv/m.sem.sexp`  `9f53ca1642ed520be3bf0cd8adc6f13dc4ceb9663575bc95524145d230097df8`
//!   `definitions/riscv/m.sexp`  `0f48d4348b850b5fcfd296b220409a2a711d8b13075fdea9059b33d67544a386`
//!   `definitions/riscv/rv64i.sem.sexp`  `c3065957307cc3fe1d58005a533e0d7291fe66ae7b05d6f8be4747e18a3aa29e`
//!   `definitions/riscv/rv64i.sexp`  `f45071eef9894463259482191cc464fa79df59af04b16e5c10f6c3a7342e0278`
//!   `definitions/riscv/system.sem.sexp`  `cb25de97e2197c5d443779f28579589dd1384bf9eb1ae0028166678bdd94692b`
//!   `definitions/riscv/system.sexp`  `c89d687d7a52c8e1cb19e8d87633c0f3bc70a7e7819f3ba8e2c3e895f20518e9`
//!   `definitions/riscv/zicntr.sem.sexp`  `9308b046ae1213e4302a2258c55e17e4f12f2d81f7e10c9a2e248646084b7570`
//!   `definitions/riscv/zicntr.sexp`  `f0c483e24e2515c12f32d2a95ac55be3a663e2c7ca355cc804890a2f2c3bc675`
//!   `definitions/riscv/zicsr.sem.sexp`  `52a45e254513ea2b9ed6a224b5cfb17c2ae8bb2ddad711c7f9b9a02e926bc45d`
//!   `definitions/riscv/zicsr.sexp`  `f2cd1ab3c64e343a6456b2ce81f506e097d1e25de523522f2577dc377b6e78e2`
//!   `definitions/riscv/zifencei.sem.sexp`  `048555ac8a792789fb534d37d05c0f099a658f822520689e214265ecd2afcd5c`
//!   `definitions/riscv/zifencei.sexp`  `7e3c6eebb4cffe383504979c83098cd2807bf90ee23c254ab4f94cad139a5003`
//!   `profiles/rv64gc-lab-v0/encoding.sexp`  `1f5e1587e01c3bf7cc84d96f6c3b84c5ecde0ce0cf2eb9ff0e89e8742c3b98e9`
//!   `profiles/rv64gc-lab-v0/state.sexp`  `0d063715bce44cd265341d92b2fb4bf9b172901ab730de6198f9132cb52638ae`
//! Generator: `scripts/gen_definition.py` (sha256 `8827d20f555b51457b1e04335508187796cb96b879b2fffefe2a111b4e69484b`)

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
        "riscv/f",
        "riscv/d",
        "riscv/m",
    ],
    generator: GeneratorPin {
        name: "scripts/gen_definition.py",
        sha256: "8827d20f555b51457b1e04335508187796cb96b879b2fffefe2a111b4e69484b",
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
            path: "definitions/riscv/d.sem.sexp",
            sha256: "92e92f9242414c53f2297962a236e9318822318acb322cb65fe4969e63ac375e",
        },
        InputPin {
            path: "definitions/riscv/d.sexp",
            sha256: "c0cdc058273c25ac636adb33761aac51956a534c161f17db51e5b34ebe6f0dc0",
        },
        InputPin {
            path: "definitions/riscv/f.sem.sexp",
            sha256: "fea32f7229d98271567372e618838f725fe9acb66d5f355ee49caf7fc071e49e",
        },
        InputPin {
            path: "definitions/riscv/f.sexp",
            sha256: "4d3232c6f9c9298c6814fce8c4865ae103a46f4308b7649d7b4a71be02c28a9a",
        },
        InputPin {
            path: "definitions/riscv/m.sem.sexp",
            sha256: "9f53ca1642ed520be3bf0cd8adc6f13dc4ceb9663575bc95524145d230097df8",
        },
        InputPin {
            path: "definitions/riscv/m.sexp",
            sha256: "0f48d4348b850b5fcfd296b220409a2a711d8b13075fdea9059b33d67544a386",
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
            sha256: "52a45e254513ea2b9ed6a224b5cfb17c2ae8bb2ddad711c7f9b9a02e926bc45d",
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
            sha256: "1f5e1587e01c3bf7cc84d96f6c3b84c5ecde0ce0cf2eb9ff0e89e8742c3b98e9",
        },
        InputPin {
            path: "profiles/rv64gc-lab-v0/state.sexp",
            sha256: "0d063715bce44cd265341d92b2fb4bf9b172901ab730de6198f9132cb52638ae",
        },
    ],
    sources: &[
        SourcePin {
            file: "rv64_a",
            sha256: "819e0487131bc97cfc0b6f3de62390f2f9936b43e80aef7c6cec14fbe7c7a1b6",
        },
        SourcePin {
            file: "rv64_d",
            sha256: "883e668be4c536d0dfdb8c02bd1f3eb959801eb953f1fb7a4b4e5e623cbf19a9",
        },
        SourcePin {
            file: "rv64_f",
            sha256: "5c01c243ccd8a1c0e24a48a1ffcf62eecb10aa36fd6bdcedf7392e670cd46cf9",
        },
        SourcePin {
            file: "rv64_i",
            sha256: "262cbd0884fe1383fcb7c42070cbc73e309d0452ff8d00b38452a4dee7cfa7f5",
        },
        SourcePin {
            file: "rv64_m",
            sha256: "112bf223a31b7cc51761ce1572a8a35c2502ab2c5a6e318db80c0601b587480e",
        },
        SourcePin {
            file: "rv_a",
            sha256: "d9eaa988c4779ca352d9da9eabacf6c71771d0b81e04b234302627f69e0863d9",
        },
        SourcePin {
            file: "rv_d",
            sha256: "24bc7c6384f9a009dbafb3f177ec68b0d4f8fb1c2c2b7b07767320fdd7d4acbc",
        },
        SourcePin {
            file: "rv_f",
            sha256: "227e09504c0d758add114d5a77ac06d7e2ffab9c6a9509633c4f531db58b3e3e",
        },
        SourcePin {
            file: "rv_i",
            sha256: "146e297ddbe346f325d993aaf56d7006f1bfde39df584b888b221543def17b97",
        },
        SourcePin {
            file: "rv_m",
            sha256: "1a53ea03820b7044de4f0f04d207c1e4fc0ced46deb2c6ed4a3ca268fa37ddbe",
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

/// The 21 operand fields the composed fragments declare, sorted by
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
        name: "rm",
        hi: 14,
        lo: 12,
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
        name: "rs3",
        hi: 31,
        lo: 27,
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

/// The 160 instructions of the composed definition, sorted by name. Every
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
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::CsrRw(
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
            ),
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
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::CsrRw(
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
            ),
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
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::CsrRw(
                    &Sem::Field("csr"),
                    &Sem::Or(
                        &Sem::CsrRead(
                            &Sem::Field("csr"),
                        ),
                        &Sem::Reg("rs1"),
                    ),
                ),
            ),
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
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::CsrRw(
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
            ),
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
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::CsrRw(
                    &Sem::Field("csr"),
                    &Sem::Reg("rs1"),
                ),
            ),
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
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::CsrRw(
                    &Sem::Field("csr"),
                    &Sem::Zext(
                        64,
                        &Sem::Field("zimm5"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "div",
        mask: 0xfe00707f,
        value: 0x02004033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_m",
        source: "RVI-M §11.1.2 — signed division rounding towards zero; Table 1: a zero divisor yields a quotient with all bits set, overflow the dividend (the operator's wrap)",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Reg("rs2"),
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Lit(0xffffffffffffffff),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Div(
                    &Sem::Reg("rs1"),
                    &Sem::Reg("rs2"),
                ),
            ),
        )
    },
    InsnDef {
        name: "divu",
        mask: 0xfe00707f,
        value: 0x02005033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_m",
        source: "RVI-M §11.1.2 — unsigned division; Table 1: a zero divisor yields 2^XLEN − 1, all bits set",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Reg("rs2"),
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Lit(0xffffffffffffffff),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::DivU(
                    &Sem::Reg("rs1"),
                    &Sem::Reg("rs2"),
                ),
            ),
        )
    },
    InsnDef {
        name: "divuw",
        mask: 0xfe00707f,
        value: 0x0200503b,
        operands: &["rd", "rs1", "rs2"],
        from: "rv64_m",
        source: "RVI-M §11.1.2 — DIVUW as unsigned integers, the 32-bit quotient sign-extended; Table 1 at L = 32: 2^32 − 1",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Trunc(
                    32,
                    &Sem::Reg("rs2"),
                ),
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Sext(
                    64,
                    &Sem::Trunc(
                        32,
                        &Sem::Lit(0xffffffffffffffff),
                    ),
                ),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Sext(
                    64,
                    &Sem::Trunc(
                        32,
                        &Sem::DivU(
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
            ),
        )
    },
    InsnDef {
        name: "divw",
        mask: 0xfe00707f,
        value: 0x0200403b,
        operands: &["rd", "rs1", "rs2"],
        from: "rv64_m",
        source: "RVI-M §11.1.2 — DIVW divides the lower 32 bits of rs1 by the lower 32 bits of rs2 as signed integers, the 32-bit quotient sign-extended; Table 1 at L = 32",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Trunc(
                    32,
                    &Sem::Reg("rs2"),
                ),
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Sext(
                    64,
                    &Sem::Trunc(
                        32,
                        &Sem::Lit(0xffffffffffffffff),
                    ),
                ),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Sext(
                    64,
                    &Sem::Trunc(
                        32,
                        &Sem::Div(
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
            ),
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
        name: "fadd.d",
        mask: 0xfe00007f,
        value: 0x02000053,
        operands: &["rd", "rs1", "rs2", "rm"],
        from: "rv_d",
        source: "RVI-D §21.1.4 — FADD.S's addition at format 64, rounded by rm",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FAdd(
                64,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::FReg("rs1"),
                &Sem::FReg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "fadd.s",
        mask: 0xfe00007f,
        value: 0x00000053,
        operands: &["rd", "rs1", "rs2", "rm"],
        from: "rv_f",
        source: "RVI-F §20.1.6 — FADD.S performs 'single-precision floating-point addition' between rs1 and rs2, rounded by rm",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::FAdd(
                    32,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs1"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs2"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "fclass.d",
        mask: 0xfff0707f,
        value: 0xe2001053,
        operands: &["rd", "rs1"],
        from: "rv_d",
        source: "RVI-D §21.1.7 — 'FCLASS.D, is defined analogously to its single-precision counterpart, but operates on double-precision operands': FCLASS.S's 10-bit mask at format 64, no flag",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::FClass(
                64,
                &Sem::FReg("rs1"),
            ),
        )
    },
    InsnDef {
        name: "fclass.s",
        mask: 0xfff0707f,
        value: 0xe0001053,
        operands: &["rd", "rs1"],
        from: "rv_f",
        source: "RVI-F §20.1.9 — FCLASS.S 'writes to integer register rd a 10-bit mask that indicates the class of the floating-point number' (Table 6); 'FCLASS.S does not set the floating-point exception flags'",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::FClass(
                32,
                &Sem::FUnbox(
                    32,
                    &Sem::FReg("rs1"),
                ),
            ),
        )
    },
    InsnDef {
        name: "fcvt.d.l",
        mask: 0xfff0007f,
        value: 0xd2200053,
        operands: &["rd", "rs1", "rm"],
        from: "rv64_d",
        source: "RVI-D §21.1.5 — FCVT.D.L converts the signed 64-bit integer in rs1 to a double in rd, rounded by rm ('All floating-point to integer and integer to floating-point conversion instructions round according to the rm field')",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::IToF(
                64,
                64,
                true,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::Reg("rs1"),
            ),
        )
    },
    InsnDef {
        name: "fcvt.d.lu",
        mask: 0xfff0007f,
        value: 0xd2300053,
        operands: &["rd", "rs1", "rm"],
        from: "rv64_d",
        source: "RVI-D §21.1.5 — FCVT.D.LU converts the unsigned 64-bit integer in rs1 to a double in rd, rounded by rm (RV64-only)",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::IToF(
                64,
                64,
                false,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::Reg("rs1"),
            ),
        )
    },
    InsnDef {
        name: "fcvt.d.s",
        mask: 0xfff0007f,
        value: 0x42000053,
        operands: &["rd", "rs1", "rm"],
        from: "rv_d",
        source: "RVI-D §21.1.5 — 'FCVT.D.S will never round': the single in rs1 (unboxed) widened exactly; its rm is still resolved (the reserved-mode decode)",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FToF(
                64,
                32,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::FUnbox(
                    32,
                    &Sem::FReg("rs1"),
                ),
            ),
        )
    },
    InsnDef {
        name: "fcvt.d.w",
        mask: 0xfff0007f,
        value: 0xd2000053,
        operands: &["rd", "rs1", "rm"],
        from: "rv_d",
        source: "RVI-D §21.1.5 — FCVT.D.W converts the signed 32-bit integer in rs1 to a double in rd; 'Note FCVT.D.W[U] always produces an exact result and is unaffected by rounding mode' — its rm is still resolved (the reserved-mode decode)",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::IToF(
                64,
                32,
                true,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::Reg("rs1"),
            ),
        )
    },
    InsnDef {
        name: "fcvt.d.wu",
        mask: 0xfff0007f,
        value: 0xd2100053,
        operands: &["rd", "rs1", "rm"],
        from: "rv_d",
        source: "RVI-D §21.1.5 — FCVT.D.WU converts the unsigned 32-bit integer in rs1 to a double in rd, exactly",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::IToF(
                64,
                32,
                false,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::Reg("rs1"),
            ),
        )
    },
    InsnDef {
        name: "fcvt.l.d",
        mask: 0xfff0007f,
        value: 0xc2200053,
        operands: &["rd", "rs1", "rm"],
        from: "rv64_d",
        source: "RVI-D §21.1.5 — FCVT.L.D converts rs1 to a signed 64-bit integer; 'FCVT.L[U].D and FCVT.D.L[U] are RV64-only instructions'",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::FToI(
                64,
                64,
                true,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::FReg("rs1"),
            ),
        )
    },
    InsnDef {
        name: "fcvt.l.s",
        mask: 0xfff0007f,
        value: 0xc0200053,
        operands: &["rd", "rs1", "rm"],
        from: "rv64_f",
        source: "RVI-F §20.1.7 — FCVT.L.S converts rs1 to a signed 64-bit integer in rd (RV64-only), clipped with NV out of range (Table 5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::FToI(
                32,
                64,
                true,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::FUnbox(
                    32,
                    &Sem::FReg("rs1"),
                ),
            ),
        )
    },
    InsnDef {
        name: "fcvt.lu.d",
        mask: 0xfff0007f,
        value: 0xc2300053,
        operands: &["rd", "rs1", "rm"],
        from: "rv64_d",
        source: "RVI-D §21.1.5 — FCVT.LU.D converts rs1 to an unsigned 64-bit integer (RV64-only), clipped with NV out of range as FCVT.int.S",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::FToI(
                64,
                64,
                false,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::FReg("rs1"),
            ),
        )
    },
    InsnDef {
        name: "fcvt.lu.s",
        mask: 0xfff0007f,
        value: 0xc0300053,
        operands: &["rd", "rs1", "rm"],
        from: "rv64_f",
        source: "RVI-F §20.1.7 — FCVT.LU.S converts rs1 to an unsigned 64-bit integer in rd (RV64-only), clipped with NV out of range (Table 5)",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::FToI(
                32,
                64,
                false,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::FUnbox(
                    32,
                    &Sem::FReg("rs1"),
                ),
            ),
        )
    },
    InsnDef {
        name: "fcvt.s.d",
        mask: 0xfff0007f,
        value: 0x40100053,
        operands: &["rd", "rs1", "rm"],
        from: "rv_d",
        source: "RVI-D §21.1.5 — 'FCVT.S.D rounds according to the RM field': the double in rs1 narrowed to a single, NaN-boxed into rd",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::FToF(
                    32,
                    64,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::FReg("rs1"),
                ),
            ),
        )
    },
    InsnDef {
        name: "fcvt.s.l",
        mask: 0xfff0007f,
        value: 0xd0200053,
        operands: &["rd", "rs1", "rm"],
        from: "rv64_f",
        source: "RVI-F §20.1.7 — FCVT.S.L converts the signed 64-bit integer in rs1 to a single in rd, rounded by rm (RV64-only)",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::IToF(
                    32,
                    64,
                    true,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::Reg("rs1"),
                ),
            ),
        )
    },
    InsnDef {
        name: "fcvt.s.lu",
        mask: 0xfff0007f,
        value: 0xd0300053,
        operands: &["rd", "rs1", "rm"],
        from: "rv64_f",
        source: "RVI-F §20.1.7 — FCVT.S.LU converts the unsigned 64-bit integer in rs1 to a single in rd, rounded by rm (RV64-only)",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::IToF(
                    32,
                    64,
                    false,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::Reg("rs1"),
                ),
            ),
        )
    },
    InsnDef {
        name: "fcvt.s.w",
        mask: 0xfff0007f,
        value: 0xd0000053,
        operands: &["rd", "rs1", "rm"],
        from: "rv_f",
        source: "RVI-F §20.1.7 — FCVT.S.W converts the signed 32-bit integer in rs1 to a single in rd, rounded by rm ('All floating-point to integer and integer to floating-point conversion instructions round according to the rm field')",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::IToF(
                    32,
                    32,
                    true,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::Reg("rs1"),
                ),
            ),
        )
    },
    InsnDef {
        name: "fcvt.s.wu",
        mask: 0xfff0007f,
        value: 0xd0100053,
        operands: &["rd", "rs1", "rm"],
        from: "rv_f",
        source: "RVI-F §20.1.7 — FCVT.S.WU converts the unsigned 32-bit integer in rs1 to a single in rd, rounded by rm",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::IToF(
                    32,
                    32,
                    false,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::Reg("rs1"),
                ),
            ),
        )
    },
    InsnDef {
        name: "fcvt.w.d",
        mask: 0xfff0007f,
        value: 0xc2000053,
        operands: &["rd", "rs1", "rm"],
        from: "rv_d",
        source: "RVI-D §21.1.5 — 'FCVT.W.D or FCVT.L.D converts a double-precision floating-point number in floating-point register rs1 to a signed 32-bit or 64-bit integer'; 'For RV64, FCVT.W[U].D sign-extends the 32-bit result'; the invalid-input behavior is FCVT.int.S's",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::FToI(
                    64,
                    32,
                    true,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::FReg("rs1"),
                ),
            ),
        )
    },
    InsnDef {
        name: "fcvt.w.s",
        mask: 0xfff0007f,
        value: 0xc0000053,
        operands: &["rd", "rs1", "rm"],
        from: "rv_f",
        source: "RVI-F §20.1.7 — FCVT.W.S converts rs1 to a signed 32-bit integer in rd, rounded by rm, clipped with NV out of range (Table 5); 'For XLEN>32, FCVT.W[U].S sign-extends the 32-bit result to the destination register width'",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::FToI(
                    32,
                    32,
                    true,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs1"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "fcvt.wu.d",
        mask: 0xfff0007f,
        value: 0xc2100053,
        operands: &["rd", "rs1", "rm"],
        from: "rv_d",
        source: "RVI-D §21.1.5 — FCVT.WU.D converts rs1 to an unsigned 32-bit integer, 'the same as for FCVT.int.S' out of range; the 32-bit result sign-extended to XLEN",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::FToI(
                    64,
                    32,
                    false,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::FReg("rs1"),
                ),
            ),
        )
    },
    InsnDef {
        name: "fcvt.wu.s",
        mask: 0xfff0007f,
        value: 0xc0100053,
        operands: &["rd", "rs1", "rm"],
        from: "rv_f",
        source: "RVI-F §20.1.7 — FCVT.WU.S converts rs1 to an unsigned 32-bit integer, clipped with NV out of range (Table 5); the 32-bit result is sign-extended to XLEN like FCVT.W.S's",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::FToI(
                    32,
                    32,
                    false,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs1"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "fdiv.d",
        mask: 0xfe00007f,
        value: 0x1a000053,
        operands: &["rd", "rs1", "rs2", "rm"],
        from: "rv_d",
        source: "RVI-D §21.1.4 — FDIV.S's division of rs1 by rs2 at format 64, rounded by rm",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FDiv(
                64,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::FReg("rs1"),
                &Sem::FReg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "fdiv.s",
        mask: 0xfe00007f,
        value: 0x18000053,
        operands: &["rd", "rs1", "rs2", "rm"],
        from: "rv_f",
        source: "RVI-F §20.1.6 — 'FDIV.S performs the single-precision floating-point division of rs1 by rs2'",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::FDiv(
                    32,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs1"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs2"),
                    ),
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
        name: "feq.d",
        mask: 0xfe00707f,
        value: 0xa2002053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_d",
        source: "RVI-D §21.1.6 — the compares 'are defined analogously to their single-precision counterparts, but operate on double-precision operands': FEQ.S's quiet comparison at format 64",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::FEq(
                64,
                &Sem::FReg("rs1"),
                &Sem::FReg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "feq.s",
        mask: 0xfe00707f,
        value: 0xa0002053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_f",
        source: "RVI-F §20.1.8 — FEQ.S writes 1 to rd if rs1 = rs2, else 0; 'FEQ.S performs a quiet comparison'; 0 if either operand is NaN",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::FEq(
                32,
                &Sem::FUnbox(
                    32,
                    &Sem::FReg("rs1"),
                ),
                &Sem::FUnbox(
                    32,
                    &Sem::FReg("rs2"),
                ),
            ),
        )
    },
    InsnDef {
        name: "fld",
        mask: 0x0000707f,
        value: 0x00003007,
        operands: &["rd", "rs1", "imm12"],
        from: "rv_d",
        source: "RVI-D §21.1.3 — 'The FLD instruction loads a double-precision floating-point value from memory into floating-point register rd', base+offset like the integer loads; 'FLD and FSD do not modify the bits being transferred'",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
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
        name: "fle.d",
        mask: 0xfe00707f,
        value: 0xa2000053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_d",
        source: "RVI-D §21.1.6 — FLE.S's signaling comparison at format 64: NV for any NaN input",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::FLe(
                64,
                &Sem::FReg("rs1"),
                &Sem::FReg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "fle.s",
        mask: 0xfe00707f,
        value: 0xa0000053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_f",
        source: "RVI-F §20.1.8 — FLE.S writes 1 to rd if rs1 ≤ rs2, else 0; a signaling comparison: NV 'if either input is NaN'",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::FLe(
                32,
                &Sem::FUnbox(
                    32,
                    &Sem::FReg("rs1"),
                ),
                &Sem::FUnbox(
                    32,
                    &Sem::FReg("rs2"),
                ),
            ),
        )
    },
    InsnDef {
        name: "flt.d",
        mask: 0xfe00707f,
        value: 0xa2001053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_d",
        source: "RVI-D §21.1.6 — FLT.S's signaling comparison at format 64: NV for any NaN input",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::FLt(
                64,
                &Sem::FReg("rs1"),
                &Sem::FReg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "flt.s",
        mask: 0xfe00707f,
        value: 0xa0001053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_f",
        source: "RVI-F §20.1.8 — FLT.S writes 1 to rd if rs1 < rs2, else 0; a signaling comparison: NV 'if either input is NaN'",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::FLt(
                32,
                &Sem::FUnbox(
                    32,
                    &Sem::FReg("rs1"),
                ),
                &Sem::FUnbox(
                    32,
                    &Sem::FReg("rs2"),
                ),
            ),
        )
    },
    InsnDef {
        name: "flw",
        mask: 0x0000707f,
        value: 0x00002007,
        operands: &["rd", "rs1", "imm12"],
        from: "rv_f",
        source: "RVI-F §20.1.5 — 'The FLW instruction loads a single-precision floating-point value from memory into floating-point register rd', base+offset like the integer loads; the 32 loaded bits are NaN-boxed into FLEN (RVI-D §21.1.2's transfer rule) and 'FLW and FSW do not modify the bits being transferred'",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
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
        name: "fmadd.d",
        mask: 0x0600007f,
        value: 0x02000043,
        operands: &["rd", "rs1", "rs2", "rs3", "rm"],
        from: "rv_d",
        source: "RVI-D §21.1.4 — the computational instructions 'are defined analogously to their single-precision counterparts, but operate on double-precision operands and produce double-precision results': FMADD.S's (rs1×rs2)+rs3 with one rounding",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FMadd(
                64,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::FReg("rs1"),
                &Sem::FReg("rs2"),
                &Sem::FReg("rs3"),
            ),
        )
    },
    InsnDef {
        name: "fmadd.s",
        mask: 0x0600007f,
        value: 0x00000043,
        operands: &["rd", "rs1", "rs2", "rs3", "rm"],
        from: "rv_f",
        source: "RVI-F §20.1.6 — 'FMADD.S computes (rs1×rs2)+rs3' with one rounding; ∞×0 raises NV even with a quiet-NaN addend (the operator's contract)",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::FMadd(
                    32,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs1"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs2"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs3"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "fmax.d",
        mask: 0xfe00707f,
        value: 0x2a001053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_d",
        source: "RVI-D §21.1.4 — FMAX.S's maximumNumber at format 64 (−0.0 < +0.0, NaN handling and NV per the operator's contract)",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FMax(
                64,
                &Sem::FReg("rs1"),
                &Sem::FReg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "fmax.s",
        mask: 0xfe00707f,
        value: 0x28001053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_f",
        source: "RVI-F §20.1.6 — FMAX.S writes the larger of rs1 and rs2 to rd; −0.0 < +0.0, NaN handling and NV per the operator's contract (maximumNumber)",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::FMax(
                    32,
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs1"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs2"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "fmin.d",
        mask: 0xfe00707f,
        value: 0x2a000053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_d",
        source: "RVI-D §21.1.4 — FMIN.S's minimumNumber at format 64 (−0.0 < +0.0, NaN handling and NV per the operator's contract)",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FMin(
                64,
                &Sem::FReg("rs1"),
                &Sem::FReg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "fmin.s",
        mask: 0xfe00707f,
        value: 0x28000053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_f",
        source: "RVI-F §20.1.6 — FMIN.S writes the smaller of rs1 and rs2 to rd; −0.0 < +0.0, NaN handling and NV per the operator's contract (minimumNumber)",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::FMin(
                    32,
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs1"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs2"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "fmsub.d",
        mask: 0x0600007f,
        value: 0x02000047,
        operands: &["rd", "rs1", "rs2", "rs3", "rm"],
        from: "rv_d",
        source: "RVI-D §21.1.4 — FMSUB.S's (rs1×rs2)−rs3 at format 64: rs3's sign bit flipped into the one fused operation",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FMadd(
                64,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::FReg("rs1"),
                &Sem::FReg("rs2"),
                &Sem::Xor(
                    &Sem::FReg("rs3"),
                    &Sem::Lit(0x8000000000000000),
                ),
            ),
        )
    },
    InsnDef {
        name: "fmsub.s",
        mask: 0x0600007f,
        value: 0x00000047,
        operands: &["rd", "rs1", "rs2", "rs3", "rm"],
        from: "rv_f",
        source: "RVI-F §20.1.6 — 'FMSUB.S computes (rs1×rs2)−rs3': rs3's sign bit flipped into the one fused operation",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::FMadd(
                    32,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs1"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs2"),
                    ),
                    &Sem::Xor(
                        &Sem::FUnbox(
                            32,
                            &Sem::FReg("rs3"),
                        ),
                        &Sem::Lit(0x0000000080000000),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "fmul.d",
        mask: 0xfe00007f,
        value: 0x12000053,
        operands: &["rd", "rs1", "rs2", "rm"],
        from: "rv_d",
        source: "RVI-D §21.1.4 — FMUL.S's multiplication at format 64, rounded by rm",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FMul(
                64,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::FReg("rs1"),
                &Sem::FReg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "fmul.s",
        mask: 0xfe00007f,
        value: 0x10000053,
        operands: &["rd", "rs1", "rs2", "rm"],
        from: "rv_f",
        source: "RVI-F §20.1.6 — FMUL.S performs single-precision floating-point multiplication between rs1 and rs2, rounded by rm",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::FMul(
                    32,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs1"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs2"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "fmv.d.x",
        mask: 0xfff0707f,
        value: 0xf2000053,
        operands: &["rd", "rs1"],
        from: "rv64_d",
        source: "RVI-D §21.1.5 — 'FMV.D.X moves the double-precision value encoded in IEEE 754-2008 standard encoding from the integer register rs1 to the floating-point register rd'",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::Reg("rs1"),
        )
    },
    InsnDef {
        name: "fmv.w.x",
        mask: 0xfff0707f,
        value: 0xf0000053,
        operands: &["rd", "rs1"],
        from: "rv_f",
        source: "RVI-F §20.1.7 — FMV.W.X moves the single 'from the lower 32 bits of integer register rs1 to the floating-point register rd'; 'The bits are not modified in the transfer' — NaN-boxed into FLEN",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::Bits(
                    31,
                    0,
                    &Sem::Reg("rs1"),
                ),
            ),
        )
    },
    InsnDef {
        name: "fmv.x.d",
        mask: 0xfff0707f,
        value: 0xe2000053,
        operands: &["rd", "rs1"],
        from: "rv64_d",
        source: "RVI-D §21.1.5 — 'FMV.X.D moves the double-precision value in floating-point register rs1 to a representation in IEEE 754-2008 standard encoding in integer register rd'; 'FMV.X.D and FMV.D.X do not modify the bits being transferred'",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::FReg("rs1"),
        )
    },
    InsnDef {
        name: "fmv.x.w",
        mask: 0xfff0707f,
        value: 0xe0000053,
        operands: &["rd", "rs1"],
        from: "rv_f",
        source: "RVI-F §20.1.7 — FMV.X.W moves rs1's single to 'the lower 32 bits of integer register rd'; 'For RV64, the higher 32 bits of the destination register are filled with copies of the floating-point number’s sign bit'",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Bits(
                    31,
                    0,
                    &Sem::FReg("rs1"),
                ),
            ),
        )
    },
    InsnDef {
        name: "fnmadd.d",
        mask: 0x0600007f,
        value: 0x0200004f,
        operands: &["rd", "rs1", "rs2", "rs3", "rm"],
        from: "rv_d",
        source: "RVI-D §21.1.4 — FNMADD.S's −(rs1×rs2)−rs3 at format 64: rs1's and rs3's sign bits flipped",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FMadd(
                64,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::Xor(
                    &Sem::FReg("rs1"),
                    &Sem::Lit(0x8000000000000000),
                ),
                &Sem::FReg("rs2"),
                &Sem::Xor(
                    &Sem::FReg("rs3"),
                    &Sem::Lit(0x8000000000000000),
                ),
            ),
        )
    },
    InsnDef {
        name: "fnmadd.s",
        mask: 0x0600007f,
        value: 0x0000004f,
        operands: &["rd", "rs1", "rs2", "rs3", "rm"],
        from: "rv_f",
        source: "RVI-F §20.1.6 — 'FNMADD.S computes −(rs1×rs2)−rs3': rs1's and rs3's sign bits flipped",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::FMadd(
                    32,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::Xor(
                        &Sem::FUnbox(
                            32,
                            &Sem::FReg("rs1"),
                        ),
                        &Sem::Lit(0x0000000080000000),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs2"),
                    ),
                    &Sem::Xor(
                        &Sem::FUnbox(
                            32,
                            &Sem::FReg("rs3"),
                        ),
                        &Sem::Lit(0x0000000080000000),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "fnmsub.d",
        mask: 0x0600007f,
        value: 0x0200004b,
        operands: &["rd", "rs1", "rs2", "rs3", "rm"],
        from: "rv_d",
        source: "RVI-D §21.1.4 — FNMSUB.S's −(rs1×rs2)+rs3 at format 64: rs1's sign bit flipped, so the product is negated before the single rounding",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FMadd(
                64,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::Xor(
                    &Sem::FReg("rs1"),
                    &Sem::Lit(0x8000000000000000),
                ),
                &Sem::FReg("rs2"),
                &Sem::FReg("rs3"),
            ),
        )
    },
    InsnDef {
        name: "fnmsub.s",
        mask: 0x0600007f,
        value: 0x0000004b,
        operands: &["rd", "rs1", "rs2", "rs3", "rm"],
        from: "rv_f",
        source: "RVI-F §20.1.6 — 'FNMSUB.S computes −(rs1×rs2)+rs3': rs1's sign bit flipped, so the product is negated before the single rounding",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::FMadd(
                    32,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::Xor(
                        &Sem::FUnbox(
                            32,
                            &Sem::FReg("rs1"),
                        ),
                        &Sem::Lit(0x0000000080000000),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs2"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs3"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "fsd",
        mask: 0x0000707f,
        value: 0x00003027,
        operands: &["imm12hi", "rs1", "rs2", "imm12lo"],
        from: "rv_d",
        source: "RVI-D §21.1.3 — 'FSD stores a double-precision value from the floating-point registers to memory'; 'the payloads of non-canonical NaNs are preserved'",
        effect: &Sem::Store(
            &Sem::Lit(0x0000000000000040),
            &Sem::Add(
                &Sem::Reg("rs1"),
                &Sem::Sext(
                    64,
                    &Sem::Imm("imm12"),
                ),
            ),
            &Sem::FReg("rs2"),
        )
    },
    InsnDef {
        name: "fsgnj.d",
        mask: 0xfe00707f,
        value: 0x22000053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_d",
        source: "RVI-D §21.1.5 — 'Floating-point to floating-point sign-injection instructions, FSGNJ.D, FSGNJN.D, and FSGNJX.D are defined analogously to the single-precision sign-injection instruction': rs1's magnitude, rs2's sign",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::Or(
                &Sem::And(
                    &Sem::FReg("rs1"),
                    &Sem::Lit(0x7fffffffffffffff),
                ),
                &Sem::And(
                    &Sem::FReg("rs2"),
                    &Sem::Lit(0x8000000000000000),
                ),
            ),
        )
    },
    InsnDef {
        name: "fsgnj.s",
        mask: 0xfe00707f,
        value: 0x20000053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_f",
        source: "RVI-F §20.1.7 — the result 'takes all bits except the sign bit from rs1' and its sign bit is rs2's; 'Sign-injection instructions do not set floating-point exception flags, nor do they canonicalize NaNs'",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::Or(
                    &Sem::And(
                        &Sem::FUnbox(
                            32,
                            &Sem::FReg("rs1"),
                        ),
                        &Sem::Lit(0x000000007fffffff),
                    ),
                    &Sem::And(
                        &Sem::FUnbox(
                            32,
                            &Sem::FReg("rs2"),
                        ),
                        &Sem::Lit(0x0000000080000000),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "fsgnjn.d",
        mask: 0xfe00707f,
        value: 0x22001053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_d",
        source: "RVI-D §21.1.5 — FSGNJN.S's rule at format 64: rs1's magnitude, the opposite of rs2's sign",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::Or(
                &Sem::And(
                    &Sem::FReg("rs1"),
                    &Sem::Lit(0x7fffffffffffffff),
                ),
                &Sem::And(
                    &Sem::Xor(
                        &Sem::FReg("rs2"),
                        &Sem::Lit(0x8000000000000000),
                    ),
                    &Sem::Lit(0x8000000000000000),
                ),
            ),
        )
    },
    InsnDef {
        name: "fsgnjn.s",
        mask: 0xfe00707f,
        value: 0x20001053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_f",
        source: "RVI-F §20.1.7 — 'for FSGNJN, the result’s sign bit is the opposite of rs2's sign bit'; the magnitude is rs1's",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::Or(
                    &Sem::And(
                        &Sem::FUnbox(
                            32,
                            &Sem::FReg("rs1"),
                        ),
                        &Sem::Lit(0x000000007fffffff),
                    ),
                    &Sem::And(
                        &Sem::Xor(
                            &Sem::FUnbox(
                                32,
                                &Sem::FReg("rs2"),
                            ),
                            &Sem::Lit(0x0000000080000000),
                        ),
                        &Sem::Lit(0x0000000080000000),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "fsgnjx.d",
        mask: 0xfe00707f,
        value: 0x22002053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_d",
        source: "RVI-D §21.1.5 — FSGNJX.S's rule at format 64: rs1's magnitude, the XOR of the two signs",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::Xor(
                &Sem::FReg("rs1"),
                &Sem::And(
                    &Sem::FReg("rs2"),
                    &Sem::Lit(0x8000000000000000),
                ),
            ),
        )
    },
    InsnDef {
        name: "fsgnjx.s",
        mask: 0xfe00707f,
        value: 0x20002053,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_f",
        source: "RVI-F §20.1.7 — 'for FSGNJX, the sign bit is the XOR of the sign bits of rs1 and rs2'; the magnitude is rs1's",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::Xor(
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs1"),
                    ),
                    &Sem::And(
                        &Sem::FUnbox(
                            32,
                            &Sem::FReg("rs2"),
                        ),
                        &Sem::Lit(0x0000000080000000),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "fsqrt.d",
        mask: 0xfff0007f,
        value: 0x5a000053,
        operands: &["rd", "rs1", "rm"],
        from: "rv_d",
        source: "RVI-D §21.1.4 — FSQRT.S's square root of rs1 at format 64; the row's rs2 field is fixed 0",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FSqrt(
                64,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::FReg("rs1"),
            ),
        )
    },
    InsnDef {
        name: "fsqrt.s",
        mask: 0xfff0007f,
        value: 0x58000053,
        operands: &["rd", "rs1", "rm"],
        from: "rv_f",
        source: "RVI-F §20.1.6 — 'FSQRT.S computes the square root of rs1'; the row's rs2 field is fixed 0",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::FSqrt(
                    32,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs1"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "fsub.d",
        mask: 0xfe00007f,
        value: 0x0a000053,
        operands: &["rd", "rs1", "rs2", "rm"],
        from: "rv_d",
        source: "RVI-D §21.1.4 — FSUB.S's subtraction of rs2 from rs1 at format 64, rounded by rm",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FSub(
                64,
                &Sem::Rounding(
                    &Sem::Field("rm"),
                ),
                &Sem::FReg("rs1"),
                &Sem::FReg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "fsub.s",
        mask: 0xfe00007f,
        value: 0x08000053,
        operands: &["rd", "rs1", "rs2", "rm"],
        from: "rv_f",
        source: "RVI-F §20.1.6 — 'FSUB.S performs the single-precision floating-point subtraction of rs2 from rs1'",
        effect: &Sem::Set(
            &Sem::FReg("rd"),
            &Sem::FBox(
                32,
                &Sem::FSub(
                    32,
                    &Sem::Rounding(
                        &Sem::Field("rm"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs1"),
                    ),
                    &Sem::FUnbox(
                        32,
                        &Sem::FReg("rs2"),
                    ),
                ),
            ),
        )
    },
    InsnDef {
        name: "fsw",
        mask: 0x0000707f,
        value: 0x00002027,
        operands: &["imm12hi", "rs1", "rs2", "imm12lo"],
        from: "rv_f",
        source: "RVI-F §20.1.5 — 'FSW stores a single-precision value from floating-point register rs2 to memory': the register's low 32 bits, the upper FLEN-32 ignored (RVI-D §21.1.2's narrower-transfer rule), bits unmodified",
        effect: &Sem::Store(
            &Sem::Lit(0x0000000000000020),
            &Sem::Add(
                &Sem::Reg("rs1"),
                &Sem::Sext(
                    64,
                    &Sem::Imm("imm12"),
                ),
            ),
            &Sem::Bits(
                31,
                0,
                &Sem::FReg("rs2"),
            ),
        )
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
        name: "mul",
        mask: 0xfe00707f,
        value: 0x02000033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_m",
        source: "RVI-M §11.1.1 — MUL \"places the lower XLEN bits in the destination register\"",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Mul(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "mulh",
        mask: 0xfe00707f,
        value: 0x02001033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_m",
        source: "RVI-M §11.1.1 — the upper XLEN bits of the full 2×XLEN-bit product, signed×signed",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::MulH(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "mulhsu",
        mask: 0xfe00707f,
        value: 0x02002033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_m",
        source: "RVI-M §11.1.1 — the upper XLEN bits of the full 2×XLEN-bit product, signed rs1 × unsigned rs2",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::MulHsu(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "mulhu",
        mask: 0xfe00707f,
        value: 0x02003033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_m",
        source: "RVI-M §11.1.1 — the upper XLEN bits of the full 2×XLEN-bit product, unsigned×unsigned",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::MulHu(
                &Sem::Reg("rs1"),
                &Sem::Reg("rs2"),
            ),
        )
    },
    InsnDef {
        name: "mulw",
        mask: 0xfe00707f,
        value: 0x0200003b,
        operands: &["rd", "rs1", "rs2"],
        from: "rv64_m",
        source: "RVI-M §11.1.1 — MULW \"multiplies the lower 32 bits of the source registers, placing the sign extension of the lower 32 bits of the result into the destination register\"",
        effect: &Sem::Set(
            &Sem::Reg("rd"),
            &Sem::Sext(
                64,
                &Sem::Trunc(
                    32,
                    &Sem::Mul(
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
        name: "rem",
        mask: 0xfe00707f,
        value: 0x02006033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_m",
        source: "RVI-M §11.1.2 — \"For REM, the sign of a nonzero result equals the sign of the dividend\"; Table 1: a zero divisor yields the dividend, overflow 0 (the operator's wrap)",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Reg("rs2"),
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Reg("rs1"),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Rem(
                    &Sem::Reg("rs1"),
                    &Sem::Reg("rs2"),
                ),
            ),
        )
    },
    InsnDef {
        name: "remu",
        mask: 0xfe00707f,
        value: 0x02007033,
        operands: &["rd", "rs1", "rs2"],
        from: "rv_m",
        source: "RVI-M §11.1.2 — the unsigned remainder; Table 1: a zero divisor yields the dividend",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Reg("rs2"),
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Reg("rs1"),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::RemU(
                    &Sem::Reg("rs1"),
                    &Sem::Reg("rs2"),
                ),
            ),
        )
    },
    InsnDef {
        name: "remuw",
        mask: 0xfe00707f,
        value: 0x0200703b,
        operands: &["rd", "rs1", "rs2"],
        from: "rv64_m",
        source: "RVI-M §11.1.2 — \"Both REMW and REMUW always sign-extend the 32-bit result to 64 bits, including on a divide by zero\"",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Trunc(
                    32,
                    &Sem::Reg("rs2"),
                ),
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Sext(
                    64,
                    &Sem::Trunc(
                        32,
                        &Sem::Reg("rs1"),
                    ),
                ),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Sext(
                    64,
                    &Sem::Trunc(
                        32,
                        &Sem::RemU(
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
            ),
        )
    },
    InsnDef {
        name: "remw",
        mask: 0xfe00707f,
        value: 0x0200603b,
        operands: &["rd", "rs1", "rs2"],
        from: "rv64_m",
        source: "RVI-M §11.1.2 — \"Both REMW and REMUW always sign-extend the 32-bit result to 64 bits, including on a divide by zero\"",
        effect: &Sem::If(
            &Sem::Eq(
                &Sem::Trunc(
                    32,
                    &Sem::Reg("rs2"),
                ),
                &Sem::Lit(0x0000000000000000),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Sext(
                    64,
                    &Sem::Trunc(
                        32,
                        &Sem::Reg("rs1"),
                    ),
                ),
            ),
            &Sem::Set(
                &Sem::Reg("rd"),
                &Sem::Sext(
                    64,
                    &Sem::Trunc(
                        32,
                        &Sem::Rem(
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
/// language (`schema/semantics.sexp`, the 72 forms `scripts/check_semantics.py`
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
    /// `(csr-rw a v)` — the atomic CSR read-write: both judged first, v written,
    /// the OLD value yielded; a refusal delivers cause 2 before any effect.
    CsrRw(&'static Sem, &'static Sem),
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
    /// `(freg NAME)` — the f-register the operand field names: the raw FLEN = 64
    /// bits of the pre-instruction file; as a `set` target, a write that marks FS Dirty.
    FReg(&'static str),
    /// `(rounding rm)` — the effective rounding mode (0..4); DYN resolves to frm;
    /// a reserved mode raises illegal-instruction (cause 2).
    Rounding(&'static Sem),
    /// `(fbox n v)` — v's low n bits NaN-boxed into FLEN (all 1s above).
    FBox(u8, &'static Sem),
    /// `(funbox n v)` — the n-bit operand of an FLEN value: its low n bits when
    /// properly NaN-boxed, else the n-bit canonical NaN.
    FUnbox(u8, &'static Sem),
    /// `(fclass n a)` — the 10-bit class mask; raises no flag.
    FClass(u8, &'static Sem),
    /// `(min n a b)` — minimumNumber/maximumNumber as RVI-F
    /// §20.1.6 amends them (−0 < +0; NaN rules; NV on a signaling input).
    FMin(u8, &'static Sem, &'static Sem),
    /// `(max n a b)` — minimumNumber/maximumNumber as RVI-F
    /// §20.1.6 amends them (−0 < +0; NaN rules; NV on a signaling input).
    FMax(u8, &'static Sem, &'static Sem),
    /// `(eq n a b)` — 1 if a = b, quiet; 0 if either is NaN.
    FEq(u8, &'static Sem, &'static Sem),
    /// `(lt n a b)` — 1 if a < b, signaling; 0 if either is NaN.
    FLt(u8, &'static Sem, &'static Sem),
    /// `(le n a b)` — 1 if a ≤ b, signaling; 0 if either is NaN.
    FLe(u8, &'static Sem, &'static Sem),
    /// `(fsqrt n rm a)` — √a, rounded; flags accrued.
    FSqrt(u8, &'static Sem, &'static Sem),
    /// `(add n rm a b)` — a+b, rounded; flags accrued.
    FAdd(u8, &'static Sem, &'static Sem, &'static Sem),
    /// `(sub n rm a b)` — a-b, rounded; flags accrued.
    FSub(u8, &'static Sem, &'static Sem, &'static Sem),
    /// `(mul n rm a b)` — a×b, rounded; flags accrued.
    FMul(u8, &'static Sem, &'static Sem, &'static Sem),
    /// `(div n rm a b)` — a÷b, rounded; flags accrued.
    FDiv(u8, &'static Sem, &'static Sem, &'static Sem),
    /// `(fmadd n rm a b c)` — (a×b)+c with one rounding; ∞×0 raises NV.
    FMadd(u8, &'static Sem, &'static Sem, &'static Sem, &'static Sem),
    /// `(f2i n iw signed rm a)` — float to an iw-bit integer, clipped with NV.
    FToI(u8, u8, bool, &'static Sem, &'static Sem),
    /// `(i2f n iw signed rm v)` — v's low iw bits to an n-bit float, rounded.
    IToF(u8, u8, bool, &'static Sem, &'static Sem),
    /// `(f2f m n rm a)` — an n-bit float to an m-bit float: narrowing rounds,
    /// widening is exact; a signaling NaN raises NV, any NaN yields the canonical NaN.
    FToF(u8, u8, &'static Sem, &'static Sem),
    /// `(mul a b)` — the low w bits of a×b.
    Mul(&'static Sem, &'static Sem),
    /// `(mulh a b)` — the high w bits of the 2w-bit a×b, signed×signed.
    MulH(&'static Sem, &'static Sem),
    /// `(mulhsu a b)` — the high w bits of the 2w-bit a×b, signed×unsigned.
    MulHsu(&'static Sem, &'static Sem),
    /// `(mulhu a b)` — the high w bits of the 2w-bit a×b, unsigned×unsigned.
    MulHu(&'static Sem, &'static Sem),
    /// `(div a b)` — a÷b signed, truncating; overflow wraps; b ≠ 0 (guarded).
    Div(&'static Sem, &'static Sem),
    /// `(divu a b)` — a÷b unsigned; b ≠ 0 (guarded).
    DivU(&'static Sem, &'static Sem),
    /// `(rem a b)` — the signed remainder, the dividend's sign; b ≠ 0 (guarded).
    Rem(&'static Sem, &'static Sem),
    /// `(remu a b)` — the unsigned remainder; b ≠ 0 (guarded).
    RemU(&'static Sem, &'static Sem),
}

/// Decode a 32-bit word to its instruction definition by the fixed bits: the first
/// entry whose `mask`ed bits equal its `value`. Linear over the 160
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
