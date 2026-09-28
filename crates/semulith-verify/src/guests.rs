//! GENERATED — do not edit (OWN-03). Regenerate with `python3 scripts/gen_guests.py`; drift between this fixture and the tracked guest sources is refused by the GUEST-GEN doctrine (`scripts/check_guest_gen.sh`). This module lowers the tracked assembly guests and their specification-derived expectations into data for the verify-side execution tests (`P1-LAB.8`): every expectation value was derived from the pinned specification prose before any model ran (EVD-05), so the commit gate re-runs the first-execution-slice differential offline.
//!
//! Canonical inputs (sha256):
//!   `profiles/rv64i-lab-v0/encoding.sexp`  `93a2d4718a50b60c23c3b5e64afa64499b09fcf41a906d46d83e63eebab2e5e9`
//!   `profiles/rv64i-lab-v0/guests/guest-control.expected.sexp`  `4caae2a18515bc4b479ca810df3edd2d23c534f19b8cb9afc081a97cb48485ac`
//!   `profiles/rv64i-lab-v0/guests/guest-control.s`  `497f63c79cd8e25918d845d5cc7d3430566b2f504a31cd33b2deb572f94694e6`
//!   `profiles/rv64i-lab-v0/guests/guest-no-device.expected.sexp`  `2be4382d503c302ed52b68335f6b52a4b8848aa80bfca4b96f503666305336b7`
//!   `profiles/rv64i-lab-v0/guests/guest-no-device.s`  `4f6d655d95eaf9e132a3c66ff71d65def1642ade2997f96f663829ce65db50a3`
//!   `profiles/rv64i-lab-v0/guests/smoke-arith.expected.sexp`  `d0c5b96125992bc58fb403173f8ff9839d827264a2cc39c70b87ac05b3f43f72`
//!   `profiles/rv64i-lab-v0/guests/smoke-arith.s`  `5bd4d210483ed8c7815e40acb1c113fadf815359a73dae5c3e944d34208760f9`
//!   `profiles/rv64i-lab-v0/guests/smoke-trap.expected.sexp`  `081ed9427c790df38822107188dd91b03847e92bcb0a722f420eb7e89a289e35`
//!   `profiles/rv64i-lab-v0/guests/smoke-trap.s`  `c9533287494eecf17ecd965070232331cfdefc2eb9af1fb36de644c9c819d216`
//! Generator: `scripts/gen_guests.py` (sha256 `0805df6bee8d60519dc5ba2b8e72934984007c519c923cb6d0f4de49aa4a46cb`)
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
];
