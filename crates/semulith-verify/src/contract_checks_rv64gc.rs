//! The rv64gc environment contract's CHECKS, realized (`P4-SYSTEM.9` slice b).
//!
//! Every obligation names a positive and a negative check (`required_checks`, RECORD-SCHEMA
//! rule 6), but until this registry no check named a fixture: the ids were declared and
//! nothing ran them. Each entry here binds one check id to the tracked corpus guests that
//! realize it, and the tests run every one of them under the corpus's own comparison rule
//! — so a check is implemented exactly when it names guests that exist and pass. A POSITIVE
//! check exercises the assumption holding; a NEGATIVE one exercises what would falsify it
//! (a refusal, a software write that must not take, a counter that must not move) and shows
//! the hart's answer is the declared one.

/// One declared check of a contract obligation, realized as tracked guests.
pub struct ContractCheck {
    /// The check id an obligation's `required_checks` names.
    pub id: &'static str,
    /// The obligation it belongs to.
    pub obligation: &'static str,
    /// The corpus guests that realize it.
    pub guests: &'static [&'static str],
}

/// The realized checks: v1's four environment assumptions and its two superseding
/// guarantees, and `.8`'s partial-progress guarantee (whose statement already named its
/// fixtures).
pub static CHECKS: &[ContractCheck] = &[
    ContractCheck {
        id: "CHK-GC-ENV-TRANSLATION-INPUTS-POS",
        obligation: "OB-GC-ENV-TRANSLATION-INPUTS",
        guests: &["sv39-translate-4k", "sv39-svade"],
    },
    ContractCheck {
        id: "CHK-GC-ENV-TRANSLATION-INPUTS-NEG",
        obligation: "OB-GC-ENV-TRANSLATION-INPUTS",
        guests: &["inj-walk-l2", "inj-walk-l1", "inj-walk-l0"],
    },
    ContractCheck {
        id: "CHK-GC-ENV-INTERRUPT-SOURCES-POS",
        obligation: "OB-GC-ENV-INTERRUPT-SOURCES",
        guests: &["i-timer", "w-sw"],
    },
    ContractCheck {
        id: "CHK-GC-ENV-INTERRUPT-SOURCES-NEG",
        obligation: "OB-GC-ENV-INTERRUPT-SOURCES",
        guests: &["env-irq-sources"],
    },
    ContractCheck {
        id: "CHK-GC-ENV-VIRTUAL-TIME-POS",
        obligation: "OB-GC-ENV-VIRTUAL-TIME",
        guests: &["mm-counters", "i-timer"],
    },
    ContractCheck {
        id: "CHK-GC-ENV-VIRTUAL-TIME-NEG",
        obligation: "OB-GC-ENV-VIRTUAL-TIME",
        guests: &["w-timer"],
    },
    ContractCheck {
        id: "CHK-GC-ENV-RESERVATION-EVENTS-POS",
        obligation: "OB-GC-ENV-RESERVATION-EVENTS",
        guests: &["a-lrsc-loop", "a-lrsc-pair"],
    },
    ContractCheck {
        id: "CHK-GC-ENV-RESERVATION-EVENTS-NEG",
        obligation: "OB-GC-ENV-RESERVATION-EVENTS",
        guests: &["a-lrsc-mustfail"],
    },
    ContractCheck {
        id: "CHK-GC-PARTIAL-PROGRESS-POS",
        obligation: "OB-GC-PARTIAL-PROGRESS",
        guests: &["inj-carrier", "inj-atomics", "inj-fp", "prio-sv39"],
    },
    ContractCheck {
        id: "CHK-GC-PARTIAL-PROGRESS-NEG",
        obligation: "OB-GC-PARTIAL-PROGRESS",
        guests: &["mm-csr-ro-write", "inj-walk-l2"],
    },
    ContractCheck {
        id: "CHK-GC-PRIV-INSNS-V1-POS",
        obligation: "OB-GC-PRIV-INSNS-V1",
        guests: &["mm-wfi", "w-timer", "sv39-tlb-fence"],
    },
    ContractCheck {
        id: "CHK-GC-PRIV-INSNS-V1-NEG",
        obligation: "OB-GC-PRIV-INSNS-V1",
        guests: &["mm-csr-legality-u", "w-notrap"],
    },
    ContractCheck {
        id: "CHK-GC-ECALL-EBREAK-V1-POS",
        obligation: "OB-GC-ECALL-EBREAK-V1",
        guests: &["mm-ecall-modes", "mm-ebreak"],
    },
    ContractCheck {
        id: "CHK-GC-ECALL-EBREAK-V1-NEG",
        obligation: "OB-GC-ECALL-EBREAK-V1",
        guests: &["mm-ecall-deleg"],
    },
];

#[cfg(test)]
mod tests;
