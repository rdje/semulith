//! GENERATED — do not edit (OWN-03). Regenerate with `python3 scripts/gen_guests.py --encoding scripts/fixtures/def-gen/profiles/rv64gc-lab-v0/encoding.sexp --guests-dir scripts/fixtures/guest-gen/rv64gc --out crates/semulith-verify/src/guests_rv64gc.rs --image-format bytes`; drift between this fixture and the tracked guest sources is refused by the GUEST-GEN doctrine (`scripts/check_guest_gen.sh`). This module lowers the tracked assembly guests and their specification-derived expectations into data for the verify-side execution tests (`P1-LAB.8`): every expectation value was derived from the pinned specification prose before any model ran (EVD-05), so the commit gate re-runs the first-execution-slice differential offline.
//!
//! Canonical inputs (sha256):
//!   `scripts/fixtures/def-gen/profiles/rv64gc-lab-v0/encoding.sexp`  `8b77378df968f9687c370f0f9128c31531853b11bccc9a68abdbe8b91e3df5a0`
//!   `scripts/fixtures/guest-gen/rv64gc/bound-arith.expected.sexp`  `5c487858898481a9e0a04abbdac97328b39cbdad6a3225ee71087dd4c0c6da92`
//!   `scripts/fixtures/guest-gen/rv64gc/bound-arith.s`  `13b3be6d77489ae88564a00c0b8d57800e488a1104ad5df04bbaad15618a4e3b`
//!   `scripts/fixtures/guest-gen/rv64gc/c-alu.expected.sexp`  `3f944d1a2febe803443518b366d91f1f315128d93b2a985c7c0a137f69bd14e6`
//!   `scripts/fixtures/guest-gen/rv64gc/c-alu.s`  `5245738e7eba27e9e16ec4064aa0477336f3f918c36b3ea8e31c5a93cbe1f59a`
//!   `scripts/fixtures/guest-gen/rv64gc/smoke-arith.expected.sexp`  `2003aec0844fdff64e5a5da93166132461f3e9530c5d969d70b5c1d2dcd87284`
//!   `scripts/fixtures/guest-gen/rv64gc/smoke-arith.s`  `00e86c26cf8a113499fc2c3f3abaf96953347efb620a031771147001018fd84b`
//! Generator: `scripts/gen_guests.py` (sha256 `cefce8dfb55619694bb4420affbe8f8951ee32ae810834015616127979b45de3`)
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
static IMAGE_SMOKE_ARITH: &[u8] = &[
    0xB7, 0x00, 0x00, 0x80, 0x1B, 0x81, 0x10, 0x00, 0x93, 0x01, 0xF0, 0xFF, 0x13, 0x92, 0xF1, 0x03,
    0x93, 0x52, 0xF2, 0x03, 0x13, 0x53, 0xF2, 0x43, 0x9B, 0x83, 0x01, 0x00, 0x1B, 0x94, 0xF1, 0x01,
    0xB3, 0x84, 0x20, 0x00, 0x13, 0x05, 0x10, 0x00, 0x13, 0x15, 0xF5, 0x01, 0x23, 0x30, 0x95, 0x40,
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
static IMAGE_BOUND_ARITH: &[u8] = &[
    0x93, 0x00, 0xF0, 0xFF, 0x93, 0xD0, 0x10, 0x00, 0x13, 0x01, 0x10, 0x00, 0x13, 0x11, 0xF1, 0x03,
    0x13, 0x02, 0x10, 0x00, 0xB3, 0x81, 0x40, 0x00, 0xB3, 0x02, 0x41, 0x40, 0x33, 0x83, 0x10, 0x00,
    0x93, 0x03, 0xF1, 0xFF, 0x13, 0x04, 0x00, 0x80, 0x93, 0x04, 0xF0, 0x7F, 0x37, 0xB5, 0xAD, 0xDE,
    0x13, 0x05, 0xF5, 0x7E, 0x13, 0x15, 0x05, 0x02, 0x93, 0x05, 0xF0, 0xFF, 0x93, 0xD5, 0x15, 0x02,
    0x33, 0x65, 0xB5, 0x00, 0x1B, 0x06, 0x15, 0x00, 0x9B, 0x06, 0xF1, 0xFF, 0x3B, 0x07, 0x45, 0x00,
    0xBB, 0x07, 0x41, 0x40, 0x3B, 0x08, 0xA2, 0x40, 0xB3, 0x28, 0x11, 0x00, 0x13, 0x09, 0x10, 0x00,
    0x33, 0x39, 0x11, 0x00, 0xB3, 0x39, 0x20, 0x00, 0x13, 0x2A, 0x01, 0x80, 0x93, 0x3A, 0xF0, 0xFF,
    0x37, 0xFB, 0xFF, 0x7F, 0x97, 0x0B, 0x00, 0x80, 0x17, 0xFC, 0xFF, 0x7F,
];
#[rustfmt::skip]
static EXPECTED_BOUND_ARITH: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 1, writes: &[(1, 0x7FFFFFFFFFFFFFFF)] },
    Expectation { step: 2, writes: &[(2, 0x0000000000000001)] },
    Expectation { step: 3, writes: &[(2, 0x8000000000000000)] },
    Expectation { step: 4, writes: &[(4, 0x0000000000000001)] },
    Expectation { step: 5, writes: &[(3, 0x8000000000000000)] },
    Expectation { step: 6, writes: &[(5, 0x7FFFFFFFFFFFFFFF)] },
    Expectation { step: 7, writes: &[(6, 0xFFFFFFFFFFFFFFFE)] },
    Expectation { step: 8, writes: &[(7, 0x7FFFFFFFFFFFFFFF)] },
    Expectation { step: 9, writes: &[(8, 0xFFFFFFFFFFFFF800)] },
    Expectation { step: 10, writes: &[(9, 0x00000000000007FF)] },
    Expectation { step: 11, writes: &[(10, 0xFFFFFFFFDEADB000)] },
    Expectation { step: 12, writes: &[(10, 0xFFFFFFFFDEADB7EF)] },
    Expectation { step: 13, writes: &[(10, 0xDEADB7EF00000000)] },
    Expectation { step: 14, writes: &[(11, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 15, writes: &[(11, 0x000000007FFFFFFF)] },
    Expectation { step: 16, writes: &[(10, 0xDEADB7EF7FFFFFFF)] },
    Expectation { step: 17, writes: &[(12, 0xFFFFFFFF80000000)] },
    Expectation { step: 18, writes: &[(13, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 19, writes: &[(14, 0xFFFFFFFF80000000)] },
    Expectation { step: 20, writes: &[(15, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 21, writes: &[(16, 0xFFFFFFFF80000002)] },
    Expectation { step: 22, writes: &[(17, 0x0000000000000001)] },
    Expectation { step: 23, writes: &[(18, 0x0000000000000001)] },
    Expectation { step: 24, writes: &[(18, 0x0000000000000000)] },
    Expectation { step: 25, writes: &[(19, 0x0000000000000001)] },
    Expectation { step: 26, writes: &[(20, 0x0000000000000001)] },
    Expectation { step: 27, writes: &[(21, 0x0000000000000001)] },
    Expectation { step: 28, writes: &[(22, 0x000000007FFFF000)] },
    Expectation { step: 29, writes: &[(23, 0x0000000000000074)] },
    Expectation { step: 30, writes: &[(24, 0x00000000FFFFF078)] },
];

#[rustfmt::skip]
static IMAGE_C_ALU: &[u8] = &[
    0x7D, 0x54, 0x7D, 0x90, 0x7E, 0x14, 0x7D, 0x94, 0x01, 0x98, 0x85, 0x44, 0x26, 0x94, 0x05, 0x8C,
    0x65, 0x8C, 0x45, 0x8C, 0x25, 0x8C, 0x26, 0x85, 0x2A, 0x95, 0x02, 0x05, 0x01, 0x80, 0x01, 0x84,
    0x8D, 0x45, 0x0D, 0x8C,
];
#[rustfmt::skip]
static EXPECTED_C_ALU: &[Expectation] = &[
    Expectation { step: 0, writes: &[(8, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 1, writes: &[(8, 0x0000000000000001)] },
    Expectation { step: 2, writes: &[(8, 0x8000000000000000)] },
    Expectation { step: 3, writes: &[(8, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 4, writes: &[(8, 0xFFFFFFFFFFFFFFE0)] },
    Expectation { step: 5, writes: &[(9, 0x0000000000000001)] },
    Expectation { step: 6, writes: &[(8, 0xFFFFFFFFFFFFFFE1)] },
    Expectation { step: 7, writes: &[(8, 0xFFFFFFFFFFFFFFE0)] },
    Expectation { step: 8, writes: &[(8, 0x0000000000000000)] },
    Expectation { step: 9, writes: &[(8, 0x0000000000000001)] },
    Expectation { step: 10, writes: &[(8, 0x0000000000000000)] },
    Expectation { step: 11, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 12, writes: &[(10, 0x0000000000000002)] },
    Expectation { step: 13, writes: &[] },
    Expectation { step: 14, writes: &[] },
    Expectation { step: 15, writes: &[] },
    Expectation { step: 16, writes: &[(11, 0x0000000000000003)] },
    Expectation { step: 17, writes: &[(8, 0xFFFFFFFFFFFFFFFD)] },
];

/// The kind of boundary request a refusal region answers with an access fault
/// (P4-SYSTEM.8 slice c — typed fault injection, environment-shaped).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum RefusalKind {
    /// The implicit instruction read.
    Fetch,
    /// An explicit read.
    Load,
    /// An explicit write or a side-effect-free store-permission check.
    Store,
    /// A page-table-walk read.
    Walk,
}

/// One refusal region of a guest's experiment: requests of `kind` whose bytes
/// intersect `[base, base + size)` are answered with an access fault.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Refusal {
    /// The request kind refused.
    pub kind: RefusalKind,
    /// The region's first byte.
    pub base: u64,
    /// The region's length in bytes.
    pub size: u64,
}

/// A tracked guest program (assembled bytes) and the specification-derived
/// observations it must produce under the definitional interpreter.
pub struct Guest {
    /// The guest's name — the basename of its tracked sources.
    pub name: &'static str,
    /// The declared entry address (the reset vector of the laboratory).
    pub entry: u64,
    /// The exact little-endian program bytes, with no padding between units.
    pub image: &'static [u8],
    /// How many steps the program executes (the expectations declare it).
    pub executed_steps: usize,
    /// How many fetch requests the run must make (the expectations
    /// declare actual boundary requests, faulted ones included). A C-enabled
    /// table reads one parcel for C, two for a word; walk faults, interrupts
    /// and waiting can prevent requests (P4-SYSTEM.12).
    pub expected_fetches: usize,
    /// The expected register writes, one entry per executed step.
    pub expected: &'static [Expectation],
    /// Registers a correct execution must never write (the negative
    /// observations; a control transfer that failed to skip is invisible to
    /// positive checks alone).
    pub never_written: &'static [u8],
    /// The experiment's refusal regions (typed fault injection; empty for
    /// every guest that injects nothing).
    pub refusals: &'static [Refusal],
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
        image: IMAGE_SMOKE_ARITH,
        executed_steps: 12,
        expected_fetches: 24,
        expected: EXPECTED_SMOKE_ARITH,
        never_written: &[],
        refusals: &[],
        cross_model: true,
    },
    Guest {
        name: "bound-arith",
        entry: 0x0000000080000000,
        image: IMAGE_BOUND_ARITH,
        executed_steps: 31,
        expected_fetches: 62,
        expected: EXPECTED_BOUND_ARITH,
        never_written: &[],
        refusals: &[],
        cross_model: true,
    },
    Guest {
        name: "c-alu",
        entry: 0x0000000080000000,
        image: IMAGE_C_ALU,
        executed_steps: 18,
        expected_fetches: 18,
        expected: EXPECTED_C_ALU,
        never_written: &[],
        refusals: &[],
        cross_model: true,
    },
];
