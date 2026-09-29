//! GENERATED — do not edit (OWN-03). Regenerate with `python3 scripts/gen_guests.py`; drift between this fixture and the tracked guest sources is refused by the GUEST-GEN doctrine (`scripts/check_guest_gen.sh`). This module lowers the tracked assembly guests and their specification-derived expectations into data for the verify-side execution tests (`P1-LAB.8`): every expectation value was derived from the pinned specification prose before any model ran (EVD-05), so the commit gate re-runs the first-execution-slice differential offline.
//!
//! Canonical inputs (sha256):
//!   `profiles/rv64i-lab-v0/encoding.sexp`  `93a2d4718a50b60c23c3b5e64afa64499b09fcf41a906d46d83e63eebab2e5e9`
//!   `profiles/rv64i-lab-v0/guests/guest-control.expected.sexp`  `4caae2a18515bc4b479ca810df3edd2d23c534f19b8cb9afc081a97cb48485ac`
//!   `profiles/rv64i-lab-v0/guests/guest-control.s`  `497f63c79cd8e25918d845d5cc7d3430566b2f504a31cd33b2deb572f94694e6`
//!   `profiles/rv64i-lab-v0/guests/guest-no-device.expected.sexp`  `2be4382d503c302ed52b68335f6b52a4b8848aa80bfca4b96f503666305336b7`
//!   `profiles/rv64i-lab-v0/guests/guest-no-device.s`  `4f6d655d95eaf9e132a3c66ff71d65def1642ade2997f96f663829ce65db50a3`
//!   `profiles/rv64i-lab-v0/guests/scope-alu.expected.sexp`  `94ece6fd4a48a7ec096ae75a2ea7e5a416386001398b99d5b6d7bfba6bdd9014`
//!   `profiles/rv64i-lab-v0/guests/scope-alu.s`  `927382ca130c89032d35619086339e7afa7316ec7202ce947cc575e9717c3517`
//!   `profiles/rv64i-lab-v0/guests/scope-branch.expected.sexp`  `b43b2690339c94e03cd0114e6f7e09602d4da30c520a4350505fab1588697fb6`
//!   `profiles/rv64i-lab-v0/guests/scope-branch.s`  `856333d6109e300b0c68f050b183bd95fa1aff342fd8c76c9cfccf9c883eb7ab`
//!   `profiles/rv64i-lab-v0/guests/scope-ebreak.expected.sexp`  `b4b52ac8b1ee44af16bae685ac51ce6d8ba4df5c455ff886593a6c90ca976ab7`
//!   `profiles/rv64i-lab-v0/guests/scope-ebreak.s`  `0d2d4b6ee08a5120348887306c09029d20a35240cee44e42e2d2ac6fe06e6f10`
//!   `profiles/rv64i-lab-v0/guests/scope-ecall.expected.sexp`  `506b4697c318a5f13f94d60b55a62053399f3797e0f22deef38c2bafe743faa3`
//!   `profiles/rv64i-lab-v0/guests/scope-ecall.s`  `e35b711474b88ca35d593ff4227ed2129c22e8df7f2d5e75773bf2911272b23f`
//!   `profiles/rv64i-lab-v0/guests/scope-mem.expected.sexp`  `f2ea5a85940c9b779a15dd755136af75a4f5e8c4a34ae786a962a85bc28689de`
//!   `profiles/rv64i-lab-v0/guests/scope-mem.s`  `e30e3b0f9464a75e79fba148d6185acab64613b0a7ceffa3d7aa7fa4b56a6321`
//!   `profiles/rv64i-lab-v0/guests/smoke-arith.expected.sexp`  `d0c5b96125992bc58fb403173f8ff9839d827264a2cc39c70b87ac05b3f43f72`
//!   `profiles/rv64i-lab-v0/guests/smoke-arith.s`  `5bd4d210483ed8c7815e40acb1c113fadf815359a73dae5c3e944d34208760f9`
//!   `profiles/rv64i-lab-v0/guests/smoke-trap.expected.sexp`  `081ed9427c790df38822107188dd91b03847e92bcb0a722f420eb7e89a289e35`
//!   `profiles/rv64i-lab-v0/guests/smoke-trap.s`  `c9533287494eecf17ecd965070232331cfdefc2eb9af1fb36de644c9c819d216`
//! Generator: `scripts/gen_guests.py` (sha256 `8be0c03df24b7a159d10d0ade8cef409fe421992d55930801fa45fb1081f03b9`)
//!
//! Every data array below carries `#[rustfmt::skip]`: the emission is
//! byte-stable by construction (one entry per line), so regeneration and the
//! GUEST-GEN drift check compare bytes rustfmt never reorders.

/// The expected observations for one executed step of a guest: which register
/// writes the pinned specification-derived expectations declare, as
/// `(register index, value)` pairs ascending by index. An empty slice declares
/// the step writes nothing.
pub struct Expectation {
    /// The step's index in the executed trace.
    pub step: usize,
    /// The register writes the expectations declare for this step.
    pub writes: &'static [(u8, u64)],
}

#[rustfmt::skip]
static WORDS_SMOKE_ARITH: &[u32] = &[
    0x800000B7,
    0x0010811B,
    0xFFF00193,
    0x03F19213,
    0x03F25293,
    0x43F25313,
    0x0001839B,
    0x01F1941B,
    0x002084B3,
    0x00100513,
    0x01F51513,
    0x40953023,
];
#[rustfmt::skip]
static EXPECTED_SMOKE_ARITH: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0xFFFFFFFF80000000)] },
    Expectation { step: 1, writes: &[(2, 0xFFFFFFFF80000001)] },
    Expectation { step: 2, writes: &[(3, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 3, writes: &[(4, 0x8000000000000000)] },
    Expectation { step: 4, writes: &[(5, 0x0000000000000001)] },
    Expectation { step: 5, writes: &[(6, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 6, writes: &[(7, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 7, writes: &[(8, 0xFFFFFFFF80000000)] },
    Expectation { step: 8, writes: &[(9, 0xFFFFFFFF00000001)] },
    Expectation { step: 9, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 10, writes: &[(10, 0x0000000080000000)] },
    Expectation { step: 11, writes: &[] },
];

#[rustfmt::skip]
static WORDS_GUEST_CONTROL: &[u32] = &[
    0x00300093,
    0xFFF08093,
    0xFE009EE3,
    0x00C002EF,
    0x55500313,
    0x00130313,
    0x00700393,
    0x00000497,
    0x00D48567,
    0x3E700693,
    0x02A00593,
    0x00100613,
];
#[rustfmt::skip]
static EXPECTED_GUEST_CONTROL: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000003)] },
    Expectation { step: 1, writes: &[(1, 0x0000000000000002)] },
    Expectation { step: 2, writes: &[] },
    Expectation { step: 3, writes: &[(1, 0x0000000000000001)] },
    Expectation { step: 4, writes: &[] },
    Expectation { step: 5, writes: &[(1, 0x0000000000000000)] },
    Expectation { step: 6, writes: &[] },
    Expectation { step: 7, writes: &[(5, 0x0000000080000010)] },
    Expectation { step: 8, writes: &[(7, 0x0000000000000007)] },
    Expectation { step: 9, writes: &[(9, 0x000000008000001C)] },
    Expectation { step: 10, writes: &[(10, 0x0000000080000024)] },
    Expectation { step: 11, writes: &[(11, 0x000000000000002A)] },
    Expectation { step: 12, writes: &[(12, 0x0000000000000001)] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_GUEST_CONTROL: &[u8] = &[6, 13];

#[rustfmt::skip]
static WORDS_SMOKE_TRAP: &[u32] = &[
    0x00100513,
    0x01F51513,
    0x40152083,
];
#[rustfmt::skip]
static EXPECTED_SMOKE_TRAP: &[Expectation] = &[
    Expectation { step: 0, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(10, 0x0000000080000000)] },
    Expectation { step: 2, writes: &[] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_SMOKE_TRAP: &[u8] = &[1];

#[rustfmt::skip]
static WORDS_GUEST_NO_DEVICE: &[u32] = &[
    0x00100513,
    0x01951513,
    0x0000C5B7,
    0xFF858593,
    0x00B50533,
    0x00053083,
];
#[rustfmt::skip]
static EXPECTED_GUEST_NO_DEVICE: &[Expectation] = &[
    Expectation { step: 0, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(10, 0x0000000002000000)] },
    Expectation { step: 2, writes: &[(11, 0x000000000000C000)] },
    Expectation { step: 3, writes: &[(11, 0x000000000000BFF8)] },
    Expectation { step: 4, writes: &[(10, 0x000000000200BFF8)] },
    Expectation { step: 5, writes: &[] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_GUEST_NO_DEVICE: &[u8] = &[1];

#[rustfmt::skip]
static WORDS_SCOPE_ALU: &[u32] = &[
    0xFFF00093,
    0x65400113,
    0x47000193,
    0x80000237,
    0x02000293,
    0x00317333,
    0x003163B3,
    0x00314433,
    0xFFF27493,
    0x7FF26513,
    0xFFF24593,
    0x0020A633,
    0x00100693,
    0x0020B6B3,
    0x00122713,
    0x00100793,
    0x00123793,
    0xFFF23813,
    0x403108B3,
    0x40218933,
    0x002199B3,
    0x00225A33,
    0x40225AB3,
    0x00220B3B,
    0x40220BBB,
    0x00511C3B,
    0x00225CBB,
    0x40225D3B,
    0x01F25D9B,
    0x41F25E1B,
    0x0FF0000F,
];
#[rustfmt::skip]
static EXPECTED_SCOPE_ALU: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 1, writes: &[(2, 0x0000000000000654)] },
    Expectation { step: 2, writes: &[(3, 0x0000000000000470)] },
    Expectation { step: 3, writes: &[(4, 0xFFFFFFFF80000000)] },
    Expectation { step: 4, writes: &[(5, 0x0000000000000020)] },
    Expectation { step: 5, writes: &[(6, 0x0000000000000450)] },
    Expectation { step: 6, writes: &[(7, 0x0000000000000674)] },
    Expectation { step: 7, writes: &[(8, 0x0000000000000224)] },
    Expectation { step: 8, writes: &[(9, 0xFFFFFFFF80000000)] },
    Expectation { step: 9, writes: &[(10, 0xFFFFFFFF800007FF)] },
    Expectation { step: 10, writes: &[(11, 0x000000007FFFFFFF)] },
    Expectation { step: 11, writes: &[(12, 0x0000000000000001)] },
    Expectation { step: 12, writes: &[(13, 0x0000000000000001)] },
    Expectation { step: 13, writes: &[(13, 0x0000000000000000)] },
    Expectation { step: 14, writes: &[(14, 0x0000000000000001)] },
    Expectation { step: 15, writes: &[(15, 0x0000000000000001)] },
    Expectation { step: 16, writes: &[(15, 0x0000000000000000)] },
    Expectation { step: 17, writes: &[(16, 0x0000000000000001)] },
    Expectation { step: 18, writes: &[(17, 0x00000000000001E4)] },
    Expectation { step: 19, writes: &[(18, 0xFFFFFFFFFFFFFE1C)] },
    Expectation { step: 20, writes: &[(19, 0x0000000047000000)] },
    Expectation { step: 21, writes: &[(20, 0x00000FFFFFFFF800)] },
    Expectation { step: 22, writes: &[(21, 0xFFFFFFFFFFFFF800)] },
    Expectation { step: 23, writes: &[(22, 0xFFFFFFFF80000654)] },
    Expectation { step: 24, writes: &[(23, 0x000000007FFFF9AC)] },
    Expectation { step: 25, writes: &[(24, 0x0000000000000654)] },
    Expectation { step: 26, writes: &[(25, 0x0000000000000800)] },
    Expectation { step: 27, writes: &[(26, 0xFFFFFFFFFFFFF800)] },
    Expectation { step: 28, writes: &[(27, 0x0000000000000001)] },
    Expectation { step: 29, writes: &[(28, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 30, writes: &[] },
];

#[rustfmt::skip]
static WORDS_SCOPE_MEM: &[u32] = &[
    0x00100513,
    0x01F51513,
    0x80FFF0B7,
    0x7F000113,
    0x0020E0B3,
    0x02009093,
    0x80FFF1B7,
    0x0021E1B3,
    0x02019193,
    0x0201D193,
    0x0030E3B3,
    0x40753023,
    0x40050583,
    0x40154603,
    0x40251683,
    0x40255703,
    0x40052783,
    0x40456803,
    0x40053883,
    0x40052003,
    0xFFF00213,
    0x40450823,
    0x41053903,
    0x40451C23,
    0x41853983,
    0x42452023,
    0x42053A03,
    0x42752423,
    0x42853A83,
];
#[rustfmt::skip]
static EXPECTED_SCOPE_MEM: &[Expectation] = &[
    Expectation { step: 0, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(10, 0x0000000080000000)] },
    Expectation { step: 2, writes: &[(1, 0xFFFFFFFF80FFF000)] },
    Expectation { step: 3, writes: &[(2, 0x00000000000007F0)] },
    Expectation { step: 4, writes: &[(1, 0xFFFFFFFF80FFF7F0)] },
    Expectation { step: 5, writes: &[(1, 0x80FFF7F000000000)] },
    Expectation { step: 6, writes: &[(3, 0xFFFFFFFF80FFF000)] },
    Expectation { step: 7, writes: &[(3, 0xFFFFFFFF80FFF7F0)] },
    Expectation { step: 8, writes: &[(3, 0x80FFF7F000000000)] },
    Expectation { step: 9, writes: &[(3, 0x0000000080FFF7F0)] },
    Expectation { step: 10, writes: &[(7, 0x80FFF7F080FFF7F0)] },
    Expectation { step: 11, writes: &[] },
    Expectation { step: 12, writes: &[(11, 0xFFFFFFFFFFFFFFF0)] },
    Expectation { step: 13, writes: &[(12, 0x00000000000000F7)] },
    Expectation { step: 14, writes: &[(13, 0xFFFFFFFFFFFF80FF)] },
    Expectation { step: 15, writes: &[(14, 0x00000000000080FF)] },
    Expectation { step: 16, writes: &[(15, 0xFFFFFFFF80FFF7F0)] },
    Expectation { step: 17, writes: &[(16, 0x0000000080FFF7F0)] },
    Expectation { step: 18, writes: &[(17, 0x80FFF7F080FFF7F0)] },
    Expectation { step: 19, writes: &[] },
    Expectation { step: 20, writes: &[(4, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 21, writes: &[] },
    Expectation { step: 22, writes: &[(18, 0x00000000000000FF)] },
    Expectation { step: 23, writes: &[] },
    Expectation { step: 24, writes: &[(19, 0x000000000000FFFF)] },
    Expectation { step: 25, writes: &[] },
    Expectation { step: 26, writes: &[(20, 0x00000000FFFFFFFF)] },
    Expectation { step: 27, writes: &[] },
    Expectation { step: 28, writes: &[(21, 0x0000000080FFF7F0)] },
];

#[rustfmt::skip]
static WORDS_SCOPE_BRANCH: &[u32] = &[
    0x00500093,
    0x00500113,
    0xFFF00193,
    0x00208463,
    0x00100A13,
    0x00308463,
    0x00100213,
    0x0011C463,
    0x00100A93,
    0x0030C463,
    0x00100293,
    0x0030D463,
    0x00100B13,
    0x0011D463,
    0x00100313,
    0x0030E463,
    0x00100B93,
    0x0011E463,
    0x00100393,
    0x0011F463,
    0x00100C13,
    0x0030F463,
    0x00100413,
    0x00100493,
];
#[rustfmt::skip]
static EXPECTED_SCOPE_BRANCH: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000005)] },
    Expectation { step: 1, writes: &[(2, 0x0000000000000005)] },
    Expectation { step: 2, writes: &[(3, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 3, writes: &[] },
    Expectation { step: 4, writes: &[] },
    Expectation { step: 5, writes: &[(4, 0x0000000000000001)] },
    Expectation { step: 6, writes: &[] },
    Expectation { step: 7, writes: &[] },
    Expectation { step: 8, writes: &[(5, 0x0000000000000001)] },
    Expectation { step: 9, writes: &[] },
    Expectation { step: 10, writes: &[] },
    Expectation { step: 11, writes: &[(6, 0x0000000000000001)] },
    Expectation { step: 12, writes: &[] },
    Expectation { step: 13, writes: &[] },
    Expectation { step: 14, writes: &[(7, 0x0000000000000001)] },
    Expectation { step: 15, writes: &[] },
    Expectation { step: 16, writes: &[] },
    Expectation { step: 17, writes: &[(8, 0x0000000000000001)] },
    Expectation { step: 18, writes: &[(9, 0x0000000000000001)] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_SCOPE_BRANCH: &[u8] = &[20, 21, 22, 23, 24];

#[rustfmt::skip]
static WORDS_SCOPE_ECALL: &[u32] = &[
    0x00700093,
    0x00000073,
];
#[rustfmt::skip]
static EXPECTED_SCOPE_ECALL: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000007)] },
    Expectation { step: 1, writes: &[] },
];

#[rustfmt::skip]
static WORDS_SCOPE_EBREAK: &[u32] = &[
    0x00900093,
    0x00100073,
];
#[rustfmt::skip]
static EXPECTED_SCOPE_EBREAK: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000009)] },
    Expectation { step: 1, writes: &[] },
];

/// A tracked guest program (assembled bytes) and the specification-derived
/// observations it must produce under the definitional interpreter.
pub struct Guest {
    /// The guest's name — the basename of its tracked sources.
    pub name: &'static str,
    /// The declared entry address (the reset vector of the laboratory).
    pub entry: u64,
    /// The guest's instruction words, little-endian sequence.
    pub words: &'static [u32],
    /// How many steps the program executes (the expectations declare it).
    pub executed_steps: usize,
    /// The expected register writes, one entry per executed step.
    pub expected: &'static [Expectation],
    /// Registers a correct execution must never write (the negative
    /// observations; a control transfer that failed to skip is invisible to
    /// positive checks alone).
    pub never_written: &'static [u8],
    /// Whether the cross-model comparison is enabled for this guest (a
    /// recorded platform difference may disable it; the skip is printed,
    /// never silent).
    pub cross_model: bool,
}

/// The tracked guests, in the experiment's run order.
pub static GUESTS: &[Guest] = &[
    Guest {
        name: "smoke-arith",
        entry: 0x0000000080000000,
        words: WORDS_SMOKE_ARITH,
        executed_steps: 12,
        expected: EXPECTED_SMOKE_ARITH,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "guest-control",
        entry: 0x0000000080000000,
        words: WORDS_GUEST_CONTROL,
        executed_steps: 13,
        expected: EXPECTED_GUEST_CONTROL,
        never_written: NEVER_WRITTEN_GUEST_CONTROL,
        cross_model: true,
    },
    Guest {
        name: "smoke-trap",
        entry: 0x0000000080000000,
        words: WORDS_SMOKE_TRAP,
        executed_steps: 3,
        expected: EXPECTED_SMOKE_TRAP,
        never_written: NEVER_WRITTEN_SMOKE_TRAP,
        cross_model: true,
    },
    Guest {
        name: "guest-no-device",
        entry: 0x0000000080000000,
        words: WORDS_GUEST_NO_DEVICE,
        executed_steps: 6,
        expected: EXPECTED_GUEST_NO_DEVICE,
        never_written: NEVER_WRITTEN_GUEST_NO_DEVICE,
        cross_model: false,
    },
    Guest {
        name: "scope-alu",
        entry: 0x0000000080000000,
        words: WORDS_SCOPE_ALU,
        executed_steps: 31,
        expected: EXPECTED_SCOPE_ALU,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "scope-mem",
        entry: 0x0000000080000000,
        words: WORDS_SCOPE_MEM,
        executed_steps: 29,
        expected: EXPECTED_SCOPE_MEM,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "scope-branch",
        entry: 0x0000000080000000,
        words: WORDS_SCOPE_BRANCH,
        executed_steps: 19,
        expected: EXPECTED_SCOPE_BRANCH,
        never_written: NEVER_WRITTEN_SCOPE_BRANCH,
        cross_model: true,
    },
    Guest {
        name: "scope-ecall",
        entry: 0x0000000080000000,
        words: WORDS_SCOPE_ECALL,
        executed_steps: 2,
        expected: EXPECTED_SCOPE_ECALL,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "scope-ebreak",
        entry: 0x0000000080000000,
        words: WORDS_SCOPE_EBREAK,
        executed_steps: 2,
        expected: EXPECTED_SCOPE_EBREAK,
        never_written: &[],
        cross_model: true,
    },
];
