//! The hart's wait state — `P4-SYSTEM.5` decision 4 (ACTIVE/WAITING, Sail 0.14's
//! `HART_WAITING` precedent, `step.sail:11`), the additive module the state document's
//! SEM-08 census declares (the `hart wait state (ACTIVE/WAITING)` candidate — the TLB/
//! reservation discipline: hart state the census accounts for before the module carries
//! it).
//!
//! One bit: the hart is ACTIVE or WAITING. A legal WFI ENTERS waiting (the nop latitude
//! — "Implementations are permitted to resume execution for any reason … a legal
//! implementation is to simply implement the WFI instruction as a NOP", RVP-MACHINE
//! §2.1.3.3 — is recorded-not-taken: taking it would leave the leaf's acceptance
//! untestable, the `.3` over-fence precedent). While WAITING, a step retires nothing,
//! issues no fetch, advances the time domain one tick, and the step's HEAD evaluates
//! the wake: resume on a locally-enabled pending interrupt at any privilege level,
//! regardless of the global enables and of mideleg (§2.1.3.3's musts —
//! `crate::interrupts::wake_pending` is that evaluation). The step the wake fires on is
//! ordinary: the taken-rule decides whether the trap is taken (xepc is then the WFI's
//! pc + 4, the section's own rule — the WFI retired into the halt with pc advanced, so
//! the generic between-instructions delivery computes exactly that) or execution
//! continues at pc + 4.
//!
//! The bit is a pure function of the hart's own history — cold-ACTIVE at reset, changed
//! only by the hart's own WFI/wake — so cold-reset re-execution stays trace-identical
//! (the TLB/reservation determinism argument, `P4-SYSTEM.3` decision 2).

/// The wait state itself: one bit, no allocation (RUST-03).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum HartState {
    /// Executing instructions (the reset state — the hart starts running, §2.1.4).
    Active,
    /// Stalled by a legal WFI until the wake evaluates true (§2.1.3.3).
    Waiting,
}

impl Default for HartState {
    fn default() -> Self {
        Self::new()
    }
}

impl HartState {
    /// Cold state: ACTIVE (the hart starts executing at reset, never stalled).
    #[must_use]
    pub const fn new() -> Self {
        Self::Active
    }

    /// Whether the hart is stalled in WFI's wait.
    #[must_use]
    pub fn is_waiting(self) -> bool {
        self == Self::Waiting
    }

    /// A legal WFI's act: enter the wait.
    pub fn enter(&mut self) {
        *self = Self::Waiting;
    }

    /// The wake's act: resume — the caller's step head then runs the ordinary
    /// evaluation (the taken-rule decides trap-or-continue, §2.1.3.3).
    pub fn wake(&mut self) {
        *self = Self::Active;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn cold_active_at_reset() {
        assert!(!HartState::new().is_waiting(), "the hart starts ACTIVE");
    }

    #[test]
    fn enter_then_wake_round_trips() {
        let mut s = HartState::new();
        s.enter();
        assert!(s.is_waiting(), "a legal WFI stalls the hart");
        s.wake();
        assert!(!s.is_waiting(), "the wake resumes it");
    }
}
