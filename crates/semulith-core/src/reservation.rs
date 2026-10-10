//! The hart's LR/SC reservation — `P4-SYSTEM.4` (decisions 2–4), the additive module the
//! state document's SEM-08 census pre-declared (`state.sexp`'s "reservation set (LR/SC)"
//! candidate, recorded so the reservation could never be smuggled in silently).
//!
//! One reservation = **(physical address, width, valid)** of the most recent LR — the
//! reservation SET is exactly the accessed word's or doubleword's bytes, the minimal
//! conformant set: "An implementation can register an arbitrarily large reservation set
//! … provided [it] includes all bytes of the addressed data word or doubleword" (RVI-A
//! §12.1.2). It is keyed on the PHYSICAL address: the spec's aliasing latitude — an SC
//! is "allowed to succeed … using an alias … also allowed to fail" — is resolved to the
//! exact-physical-match point (laboratory authority, decision 2), so a different virtual
//! address mapping the same physical address pairs, and nothing else does.
//!
//! The selected one-hart invalidation policy (decision 4) is:
//!
//! - **any completed LR REPLACES** the reservation (RVI-A §12.1.2 registers a
//!   reservation on the load); a faulting LR preserves the prior reservation
//!   under the declared trap-retention policy;
//! - **any completed SC CLEARS** it — "Regardless of success or failure, executing an
//!   SC.W instruction invalidates any reservation held by this hart" (§12.1.2); an SC
//!   that TRAPS preserves it under the declared trap-retention policy. The public
//!   a-lrsc-fault experiment observes a later aligned SC succeeding after a trapped
//!   misaligned SC; this supports the named cell, not reference implementation details;
//! - **nothing else touches it** — the context-switch scratch-SC guidance is software's
//!   duty, not machinery, and the external invalidation event (another hart's store, a
//!   device write) cannot arise at harts=1 with no devices — `rv64gc-lab-env-v1`'s
//!   `OB-GC-ENV-RESERVATION-EVENTS` states it (P4-SYSTEM.9); a multi-agent environment
//!   that delivers one is a later contract version (`MC-MULTICORE`).
//!
//! The deterministic SC policy is selected laboratory data (decision 3). After
//! alignment, translation and physical permission pass, SC succeeds when the
//! reservation is valid and both physical address and width match. Exact-width
//! matching and no spurious failure choose one permitted behavior; the predicate
//! alone does not authorize retirement or a memory store. The reservation is a
//! pure function of this laboratory hart's LR/SC history and cold reset, so the
//! same cold-restored execution retains the selected deterministic behavior.

/// The reservation itself: three fields, no allocation (RUST-03).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Reservation {
    physical_address: u64,
    width: u8,
    valid: bool,
}

impl Reservation {
    /// Cold state: NO reservation (RVP's reset rule — "For implementations with the 'A'
    /// standard extension, there is no valid load reservation" at reset).
    #[must_use]
    pub const fn new() -> Self {
        Self {
            physical_address: 0,
            width: 0,
            valid: false,
        }
    }

    /// An LR's act: register (physical address, width) of the just-completed load —
    /// any LR REPLACES whatever reservation the hart held (§12.1.2: an SC pairs only
    /// with the most recent LR in program order). `width` is the access width in BYTES
    /// (4 for `.W`, 8 for `.D` at XLEN=64).
    pub fn establish(&mut self, physical_address: u64, width: u8) {
        self.physical_address = physical_address;
        self.width = width;
        self.valid = true;
    }

    /// A completed SC's act: the reservation is gone, whatever it was (§12.1.2's own
    /// sentence — success or failure, any address).
    pub fn clear(&mut self) {
        self.valid = false;
    }

    /// The selected reservation condition: valid, equal physical address and
    /// equal byte width. Exact-width matching and no spurious failure are
    /// laboratory choices. The caller must separately validate alignment,
    /// translation and physical write permission before completing SC.
    #[must_use]
    pub fn matches(&self, physical_address: u64, width: u8) -> bool {
        self.valid && self.physical_address == physical_address && self.width == width
    }
}

impl Default for Reservation {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const A: u64 = 0x8000_1000;
    const B: u64 = 0x8000_2000;

    #[test]
    fn cold_reservation_is_invalid_and_never_matches() {
        let r = Reservation::new();
        assert_eq!(r.physical_address, 0, "the selected full-cold owner value");
        assert_eq!(
            r.width, 0,
            "cleared-but-retained width is not full cold state"
        );
        assert!(!r.valid);
        assert!(!r.matches(A, 4));
        assert!(!r.matches(0, 0));
    }

    #[test]
    fn establish_registers_and_matches_exactly() {
        let mut r = Reservation::new();
        r.establish(A, 4);
        assert!(r.matches(A, 4));
    }

    #[test]
    fn any_lr_replaces_the_reservation() {
        let mut r = Reservation::new();
        r.establish(A, 4);
        r.establish(B, 8);
        assert!(!r.matches(A, 4), "the older LR's reservation is gone");
        assert!(r.matches(B, 8), "the most recent LR pairs");
    }

    #[test]
    fn address_mismatch_fails() {
        let mut r = Reservation::new();
        r.establish(A, 4);
        assert!(!r.matches(B, 4));
    }

    #[test]
    fn width_mismatch_fails() {
        let mut r = Reservation::new();
        r.establish(A, 4);
        assert!(
            !r.matches(A, 8),
            "a .D SC cannot pair with a .W LR (the minimal set)"
        );
        let mut r = Reservation::new();
        r.establish(A, 8);
        assert!(!r.matches(A, 4));
    }

    #[test]
    fn a_completed_sc_clears_success_or_failure() {
        let mut r = Reservation::new();
        r.establish(A, 4);
        r.clear();
        assert!(!r.matches(A, 4));
        // and a second clear is a no-op — the empty reservation stays empty
        r.clear();
        assert!(!r.matches(A, 4));
    }

    #[test]
    fn determinism_same_history_same_reservation() {
        // The reservation is a pure function of the hart's own history: two cold
        // reservations driven by the same LR/SC sequence answer identically (the
        // TLB suite's cold-reset determinism argument, module level).
        let drive = |r: &mut Reservation| {
            r.establish(A, 4);
            r.establish(B, 8);
            r.clear();
            r.establish(A, 4);
        };
        let mut one = Reservation::new();
        let mut two = Reservation::new();
        drive(&mut one);
        drive(&mut two);
        assert_eq!(one, two);
        assert_eq!(one.matches(A, 4), two.matches(A, 4));
    }
}
