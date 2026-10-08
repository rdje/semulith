//! Controlled test fixtures: memory responses, faults and events implementing
//! `semulith-core`'s environment request/response contract for tests
//! (`docs/ARCHITECTURE.md` §4 — the harness implements the boundary; the production
//! crates never do).
//!
//! - [`FlatMemory`] — the laboratory platform's one region: little-endian main memory
//!   (OB-MAIN-VS-IO), no side effects, re-read on every fetch (OB-CODE-VISIBILITY), with
//!   the misaligned/access-fault responses the contract specifies (OB-MISALIGN-DATA,
//!   OB-ADDRESS-SPACE).
//! - [`ScriptedEnv`] — a fixed request→response script for tests that must pin exactly
//!   what the environment does; a script that does not cover a request is a contract
//!   violation, never an invented answer (`docs/CPU_ENVIRONMENT.md` §4.1.4).
//!
//! Cold reset (`OB-ENV-RESET`) is construction plus image load: a fresh `FlatMemory` with
//! the guest image written is the declared entry state, and nothing retains state across
//! constructions.

use semulith_core::env::{
    AccessWidth, BoundaryError, ContractViolation, Environment, Failure, Request, Response,
};

/// One region of little-endian main memory at `[base, base + bytes)`.
///
/// The region is the whole declared memory map (OB-ADDRESS-SPACE): an access whose every
/// byte lies inside succeeds, anything else is `Failure::AccessFault`. There is no I/O
/// region and no side effecting byte (OB-MAIN-VS-IO) — that absence is the profile's
/// platform property, not a missing feature.
pub struct FlatMemory {
    base: u64,
    bytes: Vec<u8>,
    /// Count of fetches served — the no-extraneous-fetch clause of OB-ENV-FETCH-SUPPLY is
    /// structural (the fixture only fetches when asked), and the counter is the re-derivable
    /// witness a test can assert on.
    fetch_count: u64,
    /// The fetch alignment in bytes — the running profile's IALIGN as data (P4-SYSTEM.2:
    /// rv64i-lab-v0 declares 32 bits → 4 bytes; rv64gc-lab-v0 declares 16 with C → 2).
    /// Data-access alignment stays the access width's own rule in every profile.
    fetch_align: u64,
}

impl FlatMemory {
    /// Declare a region of `size` zeroed bytes at `base` — the laboratory platform's one
    /// memory region, cold-reset state, at the rv64i fetch alignment (4 bytes).
    #[must_use]
    pub fn new(base: u64, size: usize) -> Self {
        Self::with_fetch_align(base, size, 4)
    }

    /// [`new`] with the profile's fetch alignment explicit (`P4-SYSTEM.2` slice h — the
    /// rv64gc corpus fetches at any even address under IALIGN=16, so its fixture declares
    /// 2; rv64i's paths keep the 4-byte default byte-exact).
    #[must_use]
    pub fn with_fetch_align(base: u64, size: usize, fetch_align: u64) -> Self {
        assert!(
            fetch_align >= 2 && fetch_align.is_power_of_two() && fetch_align <= 4,
            "fetch alignment {fetch_align} is outside the declared IALIGN vocabulary"
        );
        Self {
            base,
            bytes: vec![0; size],
            fetch_count: 0,
            fetch_align,
        }
    }

    /// Write the guest image at `offset` from the region base (cold-reset image load,
    /// OB-ENV-RESET: memory outside the image is unwritten). Panics if the image does not
    /// fit — a mis-sized image is a test bug, and fixtures surface test bugs loudly rather
    /// than modeling them.
    pub fn load_image(&mut self, offset: usize, image: &[u8]) {
        let end = offset
            .checked_add(image.len())
            .expect("image offset overflows");
        assert!(
            end <= self.bytes.len(),
            "image does not fit the declared region"
        );
        self.bytes[offset..end].copy_from_slice(image);
    }

    /// How many fetches the fixture has served since construction.
    #[must_use]
    pub fn fetch_count(&self) -> u64 {
        self.fetch_count
    }

    /// Byte slice view of the region (test assertions read memory directly).
    #[must_use]
    pub fn bytes(&self) -> &[u8] {
        &self.bytes
    }

    /// Mutable byte view — the snapshot resume path (`P2-SCALAR.7`) rebuilds a region
    /// from a recorded sparse encoding. The writer must keep the region's length
    /// invariant; the digest check catches a content mismatch by name.
    pub fn bytes_mut(&mut self) -> &mut [u8] {
        &mut self.bytes
    }

    fn contains(&self, addr: u64, width: AccessWidth) -> bool {
        // u128 arithmetic: exact end computation, no wrap fuzz (a declared region is a
        // plain range; an access spanning the address-space wrap is outside every region
        // this fixture can declare, which the range check reports as AccessFault).
        let start = u128::from(addr);
        let end = start + u128::from(width.bytes());
        end <= u128::from(self.base) + self.bytes.len() as u128 && start >= u128::from(self.base)
    }

    fn read(&self, addr: u64, width: AccessWidth) -> u64 {
        let start = (addr - self.base) as usize;
        let mut value = 0u64;
        for (i, byte) in self.bytes[start..start + width.bytes() as usize]
            .iter()
            .enumerate()
        {
            value |= u64::from(*byte) << (8 * i);
        }
        value
    }

    fn write(&mut self, addr: u64, width: AccessWidth, data: u64) {
        let start = (addr - self.base) as usize;
        for (i, byte) in self.bytes[start..start + width.bytes() as usize]
            .iter_mut()
            .enumerate()
        {
            *byte = (data >> (8 * i)) as u8;
        }
    }
}

impl Environment for FlatMemory {
    /// Answer one request. Alignment is judged before region membership: misalignment is a
    /// property of the address alone, and where an address is both misaligned and outside
    /// the map this fixture reports `Misaligned`. The profile pins no priority between the
    /// two (the obligations are independent); the order is stated here so a test can rely
    /// on it.
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        let (addr, width) = match request {
            Request::Fetch { addr } => (addr, AccessWidth::W),
            Request::FetchParcel { addr } => (addr, AccessWidth::H),
            Request::Load { width, addr } | Request::Store { width, addr, .. } => (addr, width),
            Request::WalkAccess { addr } => (addr, AccessWidth::D),
        };
        // Alignment is judged before region membership (misalignment is a property of the
        // address alone). A FETCH aligns to the profile's IALIGN (the fixture's declared
        // fetch alignment); a data access aligns to its own width; a walk access aligns
        // to the PTE's 8 bytes.
        let align = match request {
            Request::Fetch { .. } => self.fetch_align,
            Request::FetchParcel { .. } => 2,
            _ => width.bytes(),
        };
        if !addr.is_multiple_of(align) {
            return Err(Failure::Misaligned.into());
        }
        if !self.contains(addr, width) {
            return Err(Failure::AccessFault.into());
        }
        match request {
            Request::Fetch { .. } => {
                // Re-read every time: OB-CODE-VISIBILITY — a store to a later-fetched
                // address is visible to the next fetch immediately.
                self.fetch_count += 1;
                Ok(Response::Fetch(self.read(addr, AccessWidth::W) as u32))
            }
            Request::FetchParcel { .. } => {
                self.fetch_count += 1;
                Ok(Response::FetchParcel(self.read(addr, AccessWidth::H) as u16))
            }
            Request::Load { .. } => Ok(Response::Load(self.read(addr, width))),
            Request::Store { data, .. } => {
                self.write(addr, width, data);
                Ok(Response::StoreDone)
            }
            Request::WalkAccess { .. } => {
                // A walk access is an 8-byte physical read; it is NOT a fetch (the
                // one-fetch-per-step census keeps its meaning) and never a store.
                Ok(Response::WalkAccess(self.read(addr, AccessWidth::D)))
            }
        }
    }
}

/// A scripted environment: an ordered list of (request, outcome) pairs the test pins in
/// advance, where the outcome may be a success response **or a scripted failure** — the
/// fault-injection carrier (OB-MISALIGN-DATA and OB-ADDRESS-SPACE faults are environment
/// answers, so a fixture must be able to script them). Every incoming request must equal
/// the next scripted request; a fixture that would answer anything else reports a
/// [`ContractViolation`] instead of inventing data.
///
/// This is the negative-fixture carrier of `docs/CPU_ENVIRONMENT.md` §4.1.4: the contract
/// violation channel is exercised for real, and the violation is a harness-side report,
/// never a target-facing failure. There is no asynchronous event to script
/// (OB-ENV-EVENT-DELIVERY: synchronous exceptions and requested traps only — those are
/// CPU-side outcomes, not environment responses).
pub struct ScriptedEnv {
    script: std::collections::VecDeque<(Request, Result<Response, Failure>)>,
}

impl ScriptedEnv {
    /// Pin the whole conversation in advance, successes and scripted faults alike.
    #[must_use]
    pub fn new(script: Vec<(Request, Result<Response, Failure>)>) -> Self {
        Self {
            script: script.into(),
        }
    }

    /// Requests not yet consumed — a test can assert the conversation ended exactly.
    #[must_use]
    pub fn remaining(&self) -> usize {
        self.script.len()
    }
}

impl Environment for ScriptedEnv {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        let Some((scripted, outcome)) = self.script.pop_front() else {
            return Err(ContractViolation::ScriptExhausted.into());
        };
        if scripted != request {
            return Err(ContractViolation::ResponseMismatch {
                scripted,
                arrived: request,
            }
            .into());
        }
        outcome.map_err(BoundaryError::Target)
    }
}

#[cfg(test)]
mod tests;
