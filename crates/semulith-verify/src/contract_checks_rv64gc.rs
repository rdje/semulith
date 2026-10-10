//! The rv64gc environment contract's CHECKS, realized (`P4-SYSTEM.9` slice b).
//!
//! Each obligation declares positive and negative checks. This registry binds exact
//! (obligation, check) pairs to evidence the normal test suite runs: tracked corpus
//! guests, direct boundary/architectural execution fixtures, or static scope predicates.
//! Scope checks validate selection and consistency, never instruction execution. Their negative
//! fixtures must violate a named predicate; guests retain their own comparison rule.

/// The evidence a declared contract check actually runs.
pub enum Evidence {
    /// Run the named tracked guests under the corpus comparison rule.
    Guests(&'static [&'static str]),
    /// Run this check id through the tracked scope predicate and its negative copies.
    Scope,
    /// Run the named direct fixture; provider violations are discriminated where relevant.
    Boundary(crate::contract_boundary_rv64gc::BoundaryCheck),
    /// Run the named architectural witness and its declared companion guests.
    Execution(crate::contract_execution_rv64gc::ExecutionCheck),
}

/// One declared check of a contract obligation, realized as executable evidence.
pub struct ContractCheck {
    /// The check id an obligation's `required_checks` names.
    pub id: &'static str,
    /// The obligation it belongs to.
    pub obligation: &'static str,
    /// The executable evidence that realizes it.
    pub evidence: Evidence,
}

/// The realized checks: v1's four environment assumptions and its two superseding
/// guarantees, `.8`'s partial-progress guarantee (whose statement already named its
/// fixtures), and v2's guarantees as each binds — M at `.11`, C and exact parcel fetch at `.12` e2c.
/// `.13` adds eleven selection pairs, three current guarantees, five typed boundary pairs
/// and the existing privilege-mode, Sv39, Svade, halfword-alignment and counter witnesses;
/// remaining records stay uncredited.
pub static CHECKS: &[ContractCheck] = &[
    ContractCheck {
        id: "CHK-LOAD-EXT-POS",
        obligation: "OB-LOAD-EXT",
        evidence: Evidence::Guests(&["scope-mem"]),
    },
    ContractCheck {
        id: "CHK-LOAD-EXT-NEG",
        obligation: "OB-LOAD-EXT",
        evidence: Evidence::Guests(&["bound-ext", "dir-ext-matrix"]),
    },
    ContractCheck {
        id: "CHK-WSUFFIX-POS",
        obligation: "OB-WSUFFIX",
        evidence: Evidence::Guests(&["scope-alu", "bound-arith"]),
    },
    ContractCheck {
        id: "CHK-WSUFFIX-NEG",
        obligation: "OB-WSUFFIX",
        evidence: Evidence::Guests(&["bound-shiftw"]),
    },
    ContractCheck {
        id: "CHK-SHAMT-POS",
        obligation: "OB-SHAMT",
        evidence: Evidence::Guests(&["scope-alu"]),
    },
    ContractCheck {
        id: "CHK-SHAMT-NEG",
        obligation: "OB-SHAMT",
        evidence: Evidence::Guests(&["bound-shift", "bound-shiftw"]),
    },
    ContractCheck {
        id: "CHK-LUI-AUIPC-POS",
        obligation: "OB-LUI-AUIPC",
        evidence: Evidence::Guests(&["scope-alu", "dir-chase"]),
    },
    ContractCheck {
        id: "CHK-LUI-AUIPC-NEG",
        obligation: "OB-LUI-AUIPC",
        evidence: Evidence::Guests(&["bound-arith"]),
    },
    ContractCheck {
        id: "CHK-ALU-REG-POS",
        obligation: "OB-ALU-REG",
        evidence: Evidence::Guests(&["scope-alu", "bound-arith"]),
    },
    ContractCheck {
        id: "CHK-ALU-REG-NEG",
        obligation: "OB-ALU-REG",
        evidence: Evidence::Guests(&["bound-alias"]),
    },
    ContractCheck {
        id: "CHK-ALU-IMM-POS",
        obligation: "OB-ALU-IMM",
        evidence: Evidence::Guests(&["scope-alu"]),
    },
    ContractCheck {
        id: "CHK-ALU-IMM-NEG",
        obligation: "OB-ALU-IMM",
        evidence: Evidence::Guests(&["bound-arith"]),
    },
    ContractCheck {
        id: "CHK-SSTC-POS",
        obligation: "OB-SSTC",
        evidence: Evidence::Execution(
            crate::contract_execution_rv64gc::ExecutionCheck::SstcPositive,
        ),
    },
    ContractCheck {
        id: "CHK-SSTC-NEG",
        obligation: "OB-SSTC",
        evidence: Evidence::Execution(
            crate::contract_execution_rv64gc::ExecutionCheck::SstcNegative,
        ),
    },
    ContractCheck {
        id: "CHK-GC-ENV-INTERRUPT-SOURCES-V2-POS",
        obligation: "OB-GC-ENV-INTERRUPT-SOURCES-V2",
        evidence: Evidence::Boundary(
            crate::contract_boundary_rv64gc::BoundaryCheck::InterruptSourcesPositive,
        ),
    },
    ContractCheck {
        id: "CHK-GC-ENV-INTERRUPT-SOURCES-V2-NEG",
        obligation: "OB-GC-ENV-INTERRUPT-SOURCES-V2",
        evidence: Evidence::Boundary(
            crate::contract_boundary_rv64gc::BoundaryCheck::InterruptSourcesNegative,
        ),
    },
    ContractCheck {
        id: "CHK-ZICNTR-POS",
        obligation: "OB-ZICNTR",
        evidence: Evidence::Guests(&["mm-counters"]),
    },
    ContractCheck {
        id: "CHK-ZICNTR-NEG",
        obligation: "OB-ZICNTR",
        evidence: Evidence::Guests(&["mm-csr-ro-counters"]),
    },
    ContractCheck {
        id: "CHK-IALIGN-16-POS",
        obligation: "OB-IALIGN-16",
        evidence: Evidence::Guests(&["c-links", "c-page-end", "sv39-straddle"]),
    },
    ContractCheck {
        id: "CHK-IALIGN-16-NEG",
        obligation: "OB-IALIGN-16",
        evidence: Evidence::Guests(&["c-page-straddle"]),
    },
    ContractCheck {
        id: "CHK-SVADE-POS",
        obligation: "OB-SVADE",
        evidence: Evidence::Guests(&[
            "sv39-translate-4k",
            "sv39-translate-2m",
            "sv39-translate-1g",
        ]),
    },
    ContractCheck {
        id: "CHK-SVADE-NEG",
        obligation: "OB-SVADE",
        evidence: Evidence::Guests(&["sv39-svade"]),
    },
    ContractCheck {
        id: "CHK-SV39-POS",
        obligation: "OB-SV39",
        evidence: Evidence::Guests(&[
            "sv39-translate-4k",
            "sv39-translate-2m",
            "sv39-translate-1g",
            "sv39-mprv",
            "sv39-tlb-fence",
            "sv39-straddle",
        ]),
    },
    ContractCheck {
        id: "CHK-SV39-NEG",
        obligation: "OB-SV39",
        evidence: Evidence::Guests(&[
            "sv39-fault-canonical",
            "sv39-fault-invalid",
            "sv39-fault-reserved",
            "sv39-fault-superpage",
            "sv39-perm-rwx",
            "sv39-perm-usr",
            "sv39-svade",
            "sv39-deleg",
        ]),
    },
    ContractCheck {
        id: "CHK-PRIV-MODES-POS",
        obligation: "OB-PRIV-MODES",
        evidence: Evidence::Guests(&[
            "mm-csr-rw",
            "mm-ebreak",
            "mm-ecall-modes",
            "mm-ecall-deleg",
            "mm-counters",
        ]),
    },
    ContractCheck {
        id: "CHK-PRIV-MODES-NEG",
        obligation: "OB-PRIV-MODES",
        evidence: Evidence::Guests(&[
            "mm-csr-legality-s",
            "mm-csr-legality-u",
            "mm-mret",
            "mm-readonly",
            "mm-stimecmp",
            "mm-wfi",
            "mm-sfence",
            "mm-sret",
        ]),
    },
    ContractCheck {
        id: "CHK-GC-ENV-RESET-POS",
        obligation: "OB-GC-ENV-RESET",
        evidence: Evidence::Boundary(crate::contract_boundary_rv64gc::BoundaryCheck::ResetPositive),
    },
    ContractCheck {
        id: "CHK-GC-ENV-RESET-NEG",
        obligation: "OB-GC-ENV-RESET",
        evidence: Evidence::Boundary(crate::contract_boundary_rv64gc::BoundaryCheck::ResetNegative),
    },
    ContractCheck {
        id: "CHK-GC-ENV-ORDERING-POS",
        obligation: "OB-GC-ENV-ORDERING",
        evidence: Evidence::Boundary(
            crate::contract_boundary_rv64gc::BoundaryCheck::OrderingPositive,
        ),
    },
    ContractCheck {
        id: "CHK-GC-ENV-ORDERING-NEG",
        obligation: "OB-GC-ENV-ORDERING",
        evidence: Evidence::Boundary(
            crate::contract_boundary_rv64gc::BoundaryCheck::OrderingNegative,
        ),
    },
    ContractCheck {
        id: "CHK-GC-ENV-EVENT-DELIVERY-POS",
        obligation: "OB-GC-ENV-EVENT-DELIVERY",
        evidence: Evidence::Boundary(
            crate::contract_boundary_rv64gc::BoundaryCheck::EventDeliveryPositive,
        ),
    },
    ContractCheck {
        id: "CHK-GC-ENV-EVENT-DELIVERY-NEG",
        obligation: "OB-GC-ENV-EVENT-DELIVERY",
        evidence: Evidence::Boundary(
            crate::contract_boundary_rv64gc::BoundaryCheck::EventDeliveryNegative,
        ),
    },
    ContractCheck {
        id: "CHK-GC-ENV-DATA-ACCESS-POS",
        obligation: "OB-GC-ENV-DATA-ACCESS",
        evidence: Evidence::Boundary(
            crate::contract_boundary_rv64gc::BoundaryCheck::DataAccessPositive,
        ),
    },
    ContractCheck {
        id: "CHK-GC-ENV-DATA-ACCESS-NEG",
        obligation: "OB-GC-ENV-DATA-ACCESS",
        evidence: Evidence::Boundary(
            crate::contract_boundary_rv64gc::BoundaryCheck::DataAccessNegative,
        ),
    },
    ContractCheck {
        id: "CHK-GC-ENV-ADDRESS-UNITS-POS",
        obligation: "OB-GC-ENV-ADDRESS-UNITS",
        evidence: Evidence::Boundary(
            crate::contract_boundary_rv64gc::BoundaryCheck::AddressUnitsPositive,
        ),
    },
    ContractCheck {
        id: "CHK-GC-ENV-ADDRESS-UNITS-NEG",
        obligation: "OB-GC-ENV-ADDRESS-UNITS",
        evidence: Evidence::Boundary(
            crate::contract_boundary_rv64gc::BoundaryCheck::AddressUnitsNegative,
        ),
    },
    ContractCheck {
        id: "CHK-GC-FP-QUALIFIED-V2-POS",
        obligation: "OB-GC-FP-QUALIFIED-V2",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-GC-FP-QUALIFIED-V2-NEG",
        obligation: "OB-GC-FP-QUALIFIED-V2",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-GC-DEFINITION-V2-POS",
        obligation: "OB-GC-DEFINITION-V2",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-GC-DEFINITION-V2-NEG",
        obligation: "OB-GC-DEFINITION-V2",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-GC-FAULT-PRIORITY-V2-POS",
        obligation: "OB-GC-FAULT-PRIORITY-V2",
        evidence: Evidence::Guests(&["prio-sv39", "it-prio-load", "a-amo-sv39", "fault-fetch"]),
    },
    ContractCheck {
        id: "CHK-GC-FAULT-PRIORITY-V2-NEG",
        obligation: "OB-GC-FAULT-PRIORITY-V2",
        evidence: Evidence::Guests(&["f-fs-off", "d-fs-off", "c-breakpoint", "mm-ebreak"]),
    },
    ContractCheck {
        id: "CHK-ABI-POS",
        obligation: "OB-ABI",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-ABI-NEG",
        obligation: "OB-ABI",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-SBI-POS",
        obligation: "OB-SBI",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-SBI-NEG",
        obligation: "OB-SBI",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-RVWMO-POS",
        obligation: "OB-RVWMO",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-RVWMO-NEG",
        obligation: "OB-RVWMO",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-PRIV-INSNS-POS",
        obligation: "OB-PRIV-INSNS",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-PRIV-INSNS-NEG",
        obligation: "OB-PRIV-INSNS",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-EXT-CLOSURE-POS",
        obligation: "OB-EXT-CLOSURE",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-EXT-CLOSURE-NEG",
        obligation: "OB-EXT-CLOSURE",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-PRIV-REVISION-POS",
        obligation: "OB-PRIV-REVISION",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-PRIV-REVISION-NEG",
        obligation: "OB-PRIV-REVISION",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-CSR-SET-POS",
        obligation: "OB-CSR-SET",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-CSR-SET-NEG",
        obligation: "OB-CSR-SET",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-NO-PMP-POS",
        obligation: "OB-NO-PMP",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-NO-PMP-NEG",
        obligation: "OB-NO-PMP",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-NO-H-POS",
        obligation: "OB-NO-H",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-NO-H-NEG",
        obligation: "OB-NO-H",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-SCOPE-CENSUS-POS",
        obligation: "OB-SCOPE-CENSUS",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-SCOPE-CENSUS-NEG",
        obligation: "OB-SCOPE-CENSUS",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-GC-COMPOSITION-POS",
        obligation: "OB-GC-COMPOSITION",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-GC-COMPOSITION-NEG",
        obligation: "OB-GC-COMPOSITION",
        evidence: Evidence::Scope,
    },
    ContractCheck {
        id: "CHK-GC-C-POS",
        obligation: "OB-GC-C",
        evidence: Evidence::Guests(&[
            "c-immediates",
            "c-alu",
            "c-word",
            "c-hints",
            "c-memory",
            "c-links",
            "c-branches",
            "c-backward",
            "c-j-limits",
            "c-lrsc",
            "c-irq",
            "c-page-end",
        ]),
    },
    ContractCheck {
        id: "CHK-GC-C-NEG",
        obligation: "OB-GC-C",
        evidence: Evidence::Guests(&[
            "c-wide-illegal",
            "c-res-zero",
            "c-res-addi16sp",
            "c-res-lui",
            "c-res-addiw",
            "c-res-lwsp",
            "c-res-ldsp",
            "c-res-jr",
            "c-res-ca",
            "c-res-quadrant0",
            "c-breakpoint",
            "c-off-fld",
            "c-off-fldsp",
            "c-off-fsd",
            "c-off-fsdsp",
            "c-page-straddle",
        ]),
    },
    ContractCheck {
        id: "CHK-GC-ENV-FETCH-SUPPLY-POS",
        obligation: "OB-GC-ENV-FETCH-SUPPLY",
        evidence: Evidence::Guests(&["c-page-end", "c-links"]),
    },
    ContractCheck {
        id: "CHK-GC-ENV-FETCH-SUPPLY-NEG",
        obligation: "OB-GC-ENV-FETCH-SUPPLY",
        evidence: Evidence::Guests(&["c-page-straddle", "fault-fetch"]),
    },
    ContractCheck {
        id: "CHK-GC-M-POS",
        obligation: "OB-GC-M",
        evidence: Evidence::Guests(&["m-mul", "m-word"]),
    },
    ContractCheck {
        id: "CHK-GC-M-NEG",
        obligation: "OB-GC-M",
        evidence: Evidence::Guests(&["m-div", "m-alias"]),
    },
    ContractCheck {
        id: "CHK-GC-ENV-TRANSLATION-INPUTS-POS",
        obligation: "OB-GC-ENV-TRANSLATION-INPUTS",
        evidence: Evidence::Guests(&["sv39-translate-4k", "sv39-svade"]),
    },
    ContractCheck {
        id: "CHK-GC-ENV-TRANSLATION-INPUTS-NEG",
        obligation: "OB-GC-ENV-TRANSLATION-INPUTS",
        evidence: Evidence::Guests(&["inj-walk-l2", "inj-walk-l1", "inj-walk-l0"]),
    },
    ContractCheck {
        id: "CHK-GC-ENV-INTERRUPT-SOURCES-POS",
        obligation: "OB-GC-ENV-INTERRUPT-SOURCES",
        evidence: Evidence::Guests(&["i-timer", "w-sw"]),
    },
    ContractCheck {
        id: "CHK-GC-ENV-INTERRUPT-SOURCES-NEG",
        obligation: "OB-GC-ENV-INTERRUPT-SOURCES",
        evidence: Evidence::Guests(&["env-irq-sources"]),
    },
    ContractCheck {
        id: "CHK-GC-ENV-VIRTUAL-TIME-POS",
        obligation: "OB-GC-ENV-VIRTUAL-TIME",
        evidence: Evidence::Guests(&["mm-counters", "i-timer"]),
    },
    ContractCheck {
        id: "CHK-GC-ENV-VIRTUAL-TIME-NEG",
        obligation: "OB-GC-ENV-VIRTUAL-TIME",
        evidence: Evidence::Guests(&["w-timer"]),
    },
    ContractCheck {
        id: "CHK-GC-ENV-RESERVATION-EVENTS-POS",
        obligation: "OB-GC-ENV-RESERVATION-EVENTS",
        evidence: Evidence::Guests(&["a-lrsc-loop", "a-lrsc-pair"]),
    },
    ContractCheck {
        id: "CHK-GC-ENV-RESERVATION-EVENTS-NEG",
        obligation: "OB-GC-ENV-RESERVATION-EVENTS",
        evidence: Evidence::Guests(&["a-lrsc-mustfail"]),
    },
    ContractCheck {
        id: "CHK-GC-PARTIAL-PROGRESS-POS",
        obligation: "OB-GC-PARTIAL-PROGRESS",
        evidence: Evidence::Guests(&["inj-carrier", "inj-atomics", "inj-fp", "prio-sv39"]),
    },
    ContractCheck {
        id: "CHK-GC-PARTIAL-PROGRESS-NEG",
        obligation: "OB-GC-PARTIAL-PROGRESS",
        evidence: Evidence::Guests(&["mm-csr-ro-write", "inj-walk-l2"]),
    },
    ContractCheck {
        id: "CHK-GC-PRIV-INSNS-V1-POS",
        obligation: "OB-GC-PRIV-INSNS-V1",
        evidence: Evidence::Guests(&["mm-wfi", "w-timer", "sv39-tlb-fence"]),
    },
    ContractCheck {
        id: "CHK-GC-PRIV-INSNS-V1-NEG",
        obligation: "OB-GC-PRIV-INSNS-V1",
        evidence: Evidence::Guests(&["mm-csr-legality-u", "w-notrap"]),
    },
    ContractCheck {
        id: "CHK-GC-ECALL-EBREAK-V1-POS",
        obligation: "OB-GC-ECALL-EBREAK-V1",
        evidence: Evidence::Guests(&["mm-ecall-modes", "mm-ebreak"]),
    },
    ContractCheck {
        id: "CHK-GC-ECALL-EBREAK-V1-NEG",
        obligation: "OB-GC-ECALL-EBREAK-V1",
        evidence: Evidence::Guests(&["mm-ecall-deleg"]),
    },
];

#[cfg(test)]
mod tests;
