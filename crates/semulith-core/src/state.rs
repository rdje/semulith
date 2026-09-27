//! GENERATED — do not edit (OWN-03). Regenerate with `python3 scripts/gen_state.py`;
//! drift between this module and the descriptor it derives from is refused by the
//! STATE-GEN doctrine (`scripts/check_state_gen.sh`). The state accessors and
//! inspection metadata derive from the state/alias descriptors (docs/ARCHITECTURE.md
//! §2), never maintained by hand.
//! Source: `profiles/rv64i-lab-v0/state.sexp` (sha256 `ff53fb04f3ed7ac25e4db78e6e92cc3e0caa086df438e221350627194cbea5a4`).
//!
//! Architectural state of `rv64i-lab-v0`: 32 × 64-bit integer registers
//! (x0 hardwired to zero) and the 64-bit program counter. — REQ-D-XLEN,
//! REQ-D-ENTRY-STATE (RVI-RV32I §1.1.1; RVI-RV64I §3.1.1)

/// Number of integer registers in the architectural register file. — REQ-D-XLEN
pub const INTEGER_COUNT: usize = 32;

/// x1 — alias view, "return address for a call" (software convention named
/// by the ISA chapter; authority software-convention — RVI-RV32I §1.1.1).
/// Aliases are views over ONE storage: a value written through one name is visible
/// through every other (catalog C02).
pub const RETURN_ADDRESS_FOR_A_CALL: u8 = 1;

/// x2 — alias view, "stack pointer" (software convention named
/// by the ISA chapter; authority software-convention — RVI-RV32I §1.1.1).
/// Aliases are views over ONE storage: a value written through one name is visible
/// through every other (catalog C02).
pub const STACK_POINTER: u8 = 2;

/// x5 — alias view, "alternate link register" (software convention named
/// by the ISA chapter; authority software-convention — RVI-RV32I §1.1.1).
/// Aliases are views over ONE storage: a value written through one name is visible
/// through every other (catalog C02).
pub const ALTERNATE_LINK_REGISTER: u8 = 5;

/// The architectural register file and program counter: one fixed-width storage,
/// every alias a view over it. 33 × 8 bytes inline, no heap — common scalar execution
/// takes no per-access allocation (RUST-03).
pub struct ArchitecturalState {
    regs: [u64; INTEGER_COUNT],
    pc: u64,
}

impl ArchitecturalState {
    /// Fresh state at the laboratory reset for `entry` (REQ-D-ENTRY-STATE).
    #[must_use]
    pub fn zeroed_at(entry: u64) -> Self {
        Self {
            regs: [0; INTEGER_COUNT],
            pc: entry,
        }
    }

    /// The laboratory reset (REQ-D-ENTRY-STATE, OB-ENV-RESET): x1..x31 = 0 — a harness
    /// declaration the base ISA leaves to the execution environment, not an
    /// architectural guarantee — and pc = the loaded image's declared entry address,
    /// supplied by the environment. x0 needs no action: it is hardwired to zero.
    pub fn reset(&mut self, entry: u64) {
        self.regs = [0; INTEGER_COUNT];
        self.pc = entry;
    }

    /// Architectural read of `x(index)`. x0 reads as 0, always — hardwired zero,
    /// "a write to it is discarded; a read of it yields 0" (RVI-RV32I §1.1.1).
    /// Contract: `index < INTEGER_COUNT`; an out-of-range index is a model error
    /// (SEM-01) and panics rather than silently reading another register.
    #[must_use]
    pub fn read_x(&self, index: u8) -> u64 {
        debug_assert!(
            index < INTEGER_COUNT as u8,
            "read_x: index {index} out of range"
        );
        if index == 0 {
            0
        } else {
            self.regs[index as usize]
        }
    }

    /// Architectural write of `x(index)`; a write to x0 is discarded (hardwired zero).
    /// Same index contract as [`Self::read_x`].
    pub fn write_x(&mut self, index: u8, value: u64) {
        debug_assert!(
            index < INTEGER_COUNT as u8,
            "write_x: index {index} out of range"
        );
        if index != 0 {
            self.regs[index as usize] = value;
        }
    }

    /// The program counter: the address of the current instruction (RVI-RV32I §1.1.1).
    /// Compositions that advance it (pc+4 sequencing, taken targets) are instruction-
    /// layer rules; they land with the interpreter slice (P1-LAB.8).
    #[must_use]
    pub fn pc(&self) -> u64 {
        self.pc
    }

    /// Set the program counter (a control transfer's target).
    pub fn set_pc(&mut self, value: u64) {
        self.pc = value;
    }
}

/// Static inspection metadata for one architectural state element — what observers,
/// divergence reports and the gate report read. Values, not storage: reading this
/// table never touches architectural state and never allocates.
pub struct StateElement {
    pub name: &'static str,
    pub width_bits: u32,
    pub class: StateClass,
    /// Software-convention role the ISA chapter itself names; `None` where the
    /// descriptor records none (ABI names are a calling convention, not
    /// architecture — see the descriptor's note).
    pub role: Option<&'static str>,
    pub source: &'static str,
}

/// Which kind of state an element is; the class set is descriptor-driven, so it is
/// generated with the elements rather than hand-extended.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum StateClass {
    IntegerRegister,
    SpecialRegister,
}

/// The 32 integer registers followed by the special registers, in descriptor
/// order: one row per state element, the observer's whole view of the file.
pub const ELEMENTS: [StateElement; 33] = [
    StateElement {
        name: "x0",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1",
    },
    StateElement {
        name: "x1",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: Some("return address for a call"),
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x2",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: Some("stack pointer"),
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x3",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x4",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x5",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: Some("alternate link register"),
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x6",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x7",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x8",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x9",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x10",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x11",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x12",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x13",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x14",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x15",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x16",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x17",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x18",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x19",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x20",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x21",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x22",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x23",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x24",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x25",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x26",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x27",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x28",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x29",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x30",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "x31",
        width_bits: 64,
        class: StateClass::IntegerRegister,
        role: None,
        source: "RVI-RV32I §1.1.1; RVI-RV64I §3.1.1",
    },
    StateElement {
        name: "pc",
        width_bits: 64,
        class: StateClass::SpecialRegister,
        role: None,
        source: "RVI-RV32I §1.1.1",
    },
];

/// SEM-08: required state includes hidden or pending information that can influence
/// future supported observations. This profile's census answers NO — per candidate,
/// with the reason — and the answer is carried as data so the interpreter, the gate
/// report and the reviewer read the same sentence. Every extension added later
/// reopens the census (the descriptor's own consequence).
pub struct HiddenStateCandidate {
    pub candidate: &'static str,
    pub present: bool,
    pub why: &'static str,
}

pub struct HiddenStateCensus {
    pub question: &'static str,
    pub answer: &'static str,
    pub candidates: &'static [HiddenStateCandidate],
    pub consequence: &'static str,
}

pub const HIDDEN_STATE_CENSUS: HiddenStateCensus = HiddenStateCensus {
    question: "Is there any state, not listed above, that can influence a future supported observation? (SEM-08, catalog C02)",
    answer: "No — for this profile, and only because of what it excludes.",
    candidates: &[
        HiddenStateCandidate {
            candidate: "CSRs",
            present: false,
            why: "Zicsr is not in this profile; profile.toml declares csrs = []",
        },
        HiddenStateCandidate {
            candidate: "reservation set (LR/SC)",
            present: false,
            why: "the A extension is not in this profile",
        },
        HiddenStateCandidate {
            candidate: "floating-point registers and fcsr",
            present: false,
            why: "F and D are not in this profile",
        },
        HiddenStateCandidate {
            candidate: "vector state (vtype, vl, vstart)",
            present: false,
            why: "V is not in this profile",
        },
        HiddenStateCandidate {
            candidate: "privilege mode and trap state",
            present: false,
            why: "no privilege modes are modelled; ECALL/EBREAK are requested traps to the harness",
        },
        HiddenStateCandidate {
            candidate: "instruction-fetch cache state",
            present: false,
            why: "the model re-reads memory on every fetch (D-CODE-VISIBILITY). A caching implementation WOULD have hidden state here, and would still be architecturally legal without Zifencei — which is why this is recorded as a laboratory choice, not an absence of the possibility",
        },
        HiddenStateCandidate {
            candidate: "pending or partially committed effects",
            present: false,
            why: "every instruction in this scope completes or faults as a unit; no multi-step or restartable suboperation exists in RV64I base",
        },
    ],
    consequence: "A profile with no hidden state is why this is a good first experiment: snapshot and replay reduce to the register file, pc and memory, so P1-LAB.10 can demonstrate replay honestly rather than approximately. Every extension added later reopens this census.",
};

#[cfg(test)]
mod tests;
