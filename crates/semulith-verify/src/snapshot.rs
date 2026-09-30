//! The mid-execution snapshot and its resume — `P2-SCALAR.7` (`G-REPLAY`'s second half:
//! `P1-LAB.10`'s bundle/replay reproduces a run from COLD reset; this module reproduces a
//! run from a recorded MID-EXECUTION state).
//!
//! The completeness claim is the pinned dossier's own census, not a hope:
//! `state.sexp`'s `hidden_state_census` (SEM-08) measured every hidden-state candidate
//! absent from this profile — no CSRs, no reservation set, no FP/vector state, no
//! privilege/trap state, no fetch-cache state, no partially committed effects — so a
//! snapshot of THIS profile is complete if and only if it carries the register file, the
//! pc, and the memory content. Anything beyond those is deliberately **not offered at
//! all** (the leaf acceptance's second arm): there is no device state to save because the
//! platform declares no devices.
//!
//! A [`Snapshot`] carries the [`Algorithm`] identity pins (the `P1-LAB.10` bundle
//! discipline: replaying against a different definition is refused BY NAME), the region
//! declaration, the entry, the step index, the registers and pc, and the memory content
//! sparse-encoded as non-zero runs — a two-gibibyte region of zeros is not data. The
//! region digest guards the whole: a corrupted or dropped run is refused on resume,
//! structurally.

use semulith_core::state::ArchitecturalState;

use crate::fixtures::FlatMemory;
use crate::json;
use crate::replay::{self, Algorithm};
use crate::run::{self, Crossing, Trace};
use crate::sha256::sha256_hex;

/// Everything a mid-execution state needs to resume from — see the module documentation.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Snapshot {
    /// The tool and definition identity (reused from the bundle vocabulary; a snapshot
    /// only exists for the production model — mutant runs are not offered).
    pub algorithm: Algorithm,
    /// The region the memory content belongs to.
    pub base: u64,
    /// Region length in bytes.
    pub size: u64,
    /// The image entry the run started at (the snapshot does not restart there — it
    /// rides as provenance).
    pub entry: u64,
    /// The step index the snapshot was taken at (steps executed before it).
    pub at_step: usize,
    /// The total step budget the original run was bounded by.
    pub budget: usize,
    /// The 32 integer registers (x0 rides as 0, architecturally discarded on restore).
    pub regs: [u64; 32],
    /// The program counter at the snapshot.
    pub pc: u64,
    /// sha256 over the whole region's bytes — the tamper check for the sparse encoding.
    pub memory_sha256: String,
    /// The memory content, sparse: (offset from base, the non-zero run's bytes).
    pub runs: Vec<(u64, Vec<u8>)>,
}

/// The outcome of resuming from a snapshot: the continuation trace and its crossings.
#[derive(Debug)]
pub struct Resumed {
    /// Steps executed after the snapshot.
    pub trace: Trace,
    /// The continuation's boundary crossings.
    pub crossings: Vec<Crossing>,
}

impl Snapshot {
    /// Capture the state mid-run: the register file and pc from `state`, the memory
    /// content from `env`. The identity pins are read from the live manifest at capture
    /// time — a snapshot records what it WAS taken against, and resume re-checks it.
    #[must_use]
    pub fn capture(
        env: &FlatMemory,
        state: &ArchitecturalState,
        base: u64,
        size: u64,
        entry: u64,
        at_step: usize,
        budget: usize,
    ) -> Self {
        let bytes = env.bytes();
        let mut regs = [0u64; 32];
        for (i, r) in regs.iter_mut().enumerate() {
            *r = state.read_x(i as u8);
        }
        let mut runs = Vec::new();
        let mut i = 0;
        while i < bytes.len() {
            if bytes[i] == 0 {
                i += 1;
                continue;
            }
            let start = i;
            while i < bytes.len() && bytes[i] != 0 {
                i += 1;
            }
            runs.push((start as u64, bytes[start..i].to_vec()));
        }
        Self {
            algorithm: replay::algorithm_for("production"),
            base,
            size,
            entry,
            at_step,
            budget,
            regs,
            pc: state.pc(),
            memory_sha256: sha256_hex(bytes),
            runs,
        }
    }

    /// Resume from the snapshot: identity first (definition pins — a mismatch refuses by
    /// name), then the sparse encoding's integrity (the region is rebuilt zero-filled and
    /// its digest recomputed — a corrupted or dropped run is a different memory, refused
    /// by name), then the continuation from the recorded state.
    pub fn resume(&self) -> Result<Resumed, String> {
        if self.algorithm.model != "production" {
            return Err(format!(
                "snapshot: model '{}' is not offered — snapshots record the production \
                 model only (a mutant's mid-run state is not a replay contract)",
                self.algorithm.model
            ));
        }
        check_identity(&self.algorithm)?;
        if self.at_step > self.budget {
            return Err(format!(
                "snapshot: at_step {} exceeds the recorded budget {} — the record is \
                 incoherent",
                self.at_step, self.budget
            ));
        }
        if self.entry < self.base || self.entry >= self.base.saturating_add(self.size) {
            return Err(format!(
                "snapshot: entry {:#x} lies outside the declared region [{:#x}, +{:#x})",
                self.entry, self.base, self.size
            ));
        }
        let mut env = FlatMemory::new(self.base, self.size as usize);
        for (offset, run_bytes) in &self.runs {
            let end = (*offset as usize)
                .checked_add(run_bytes.len())
                .filter(|e| *e <= env.bytes().len())
                .ok_or_else(|| {
                    format!(
                        "snapshot: a memory run at +{offset:#x} ({} bytes) overruns the \
                         declared region — the record is corrupt",
                        run_bytes.len()
                    )
                })?;
            env.bytes_mut()[*offset as usize..end].copy_from_slice(run_bytes);
        }
        let digest = sha256_hex(env.bytes());
        if digest != self.memory_sha256 {
            return Err(format!(
                "snapshot: memory digest mismatch — the record's {} vs the rebuilt \
                 region's {}: a run was corrupted, dropped, or added",
                self.memory_sha256, digest
            ));
        }
        let mut state = ArchitecturalState::zeroed_at(self.entry);
        for (i, value) in self.regs.iter().enumerate() {
            state.write_x(i as u8, *value);
        }
        state.set_pc(self.pc);
        let (trace, crossings) = run::run_from(&mut env, state, self.budget - self.at_step);
        Ok(Resumed { trace, crossings })
    }

    /// Serialize as JSON — hand-rolled like the bundle's, both directions.
    #[must_use]
    pub fn to_json(&self) -> String {
        let mut out = String::with_capacity(1024);
        out.push_str("{\"algorithm\":");
        replay::push_algorithm(&mut out, &self.algorithm);
        out.push_str(",\"base\":\"");
        replay::push_hex64(&mut out, self.base);
        out.push_str("\",\"size\":\"");
        replay::push_hex64(&mut out, self.size);
        out.push_str("\",\"entry\":\"");
        replay::push_hex64(&mut out, self.entry);
        out.push_str(&format!(
            "\",\"at_step\":{},\"budget\":{},\"regs\":[",
            self.at_step, self.budget
        ));
        for (i, r) in self.regs.iter().enumerate() {
            if i > 0 {
                out.push(',');
            }
            out.push_str(&format!("\"0x{r:016x}\""));
        }
        out.push_str("],\"pc\":\"");
        replay::push_hex64(&mut out, self.pc);
        out.push_str("\",\"memory_sha256\":\"");
        out.push_str(&self.memory_sha256);
        out.push_str("\",\"runs\":[");
        for (i, (offset, bytes)) in self.runs.iter().enumerate() {
            if i > 0 {
                out.push(',');
            }
            out.push_str(&format!("{{\"offset\":\"0x{offset:016x}\",\"bytes\":\""));
            for b in bytes {
                out.push_str(&format!("{b:02x}"));
            }
            out.push_str("\"}");
        }
        out.push_str("]}");
        out
    }

    /// Parse a snapshot record. Every missing or malformed accompaniment is an error
    /// naming the field — a partial state is not a snapshot, structurally.
    pub fn parse(text: &str) -> Result<Self, String> {
        let doc = json::parse(text).map_err(|e| format!("not JSON: {e}"))?;
        let root = doc
            .as_obj()
            .ok_or("snapshot: the document is not an object")?;
        let algorithm = replay::parse_algorithm(replay::need(root, "algorithm", "snapshot")?)?;
        let base = replay::hex_u64(replay::need(root, "base", "snapshot")?, "base")?;
        let size = replay::hex_u64(replay::need(root, "size", "snapshot")?, "size")?;
        let entry = replay::hex_u64(replay::need(root, "entry", "snapshot")?, "entry")?;
        let at_step = replay::int_usize(replay::need(root, "at_step", "snapshot")?, "at_step")?;
        let budget = replay::int_usize(replay::need(root, "budget", "snapshot")?, "budget")?;
        let regs_node = replay::need(root, "regs", "snapshot")?
            .as_arr()
            .ok_or("snapshot.regs: wants an array of 32 hex strings")?;
        if regs_node.len() != 32 {
            return Err(format!(
                "snapshot.regs: {} entr(ies), wants exactly 32 — a partial register file \
                 is not a snapshot",
                regs_node.len()
            ));
        }
        let mut regs = [0u64; 32];
        for (i, node) in regs_node.iter().enumerate() {
            regs[i] = replay::hex_u64(node, "regs[]")?;
        }
        let pc = replay::hex_u64(replay::need(root, "pc", "snapshot")?, "pc")?;
        let memory_sha256 = replay::need(root, "memory_sha256", "snapshot")?
            .as_str()
            .ok_or("snapshot.memory_sha256: wants a string")?
            .to_string();
        let runs_node = replay::need(root, "runs", "snapshot")?
            .as_arr()
            .ok_or("snapshot.runs: wants an array of {offset, bytes}")?;
        let mut runs = Vec::with_capacity(runs_node.len());
        for node in runs_node {
            let obj = node.as_obj().ok_or("snapshot.runs[]: wants an object")?;
            let offset = replay::hex_u64(replay::need(obj, "offset", "runs")?, "offset")?;
            let hex = replay::need(obj, "bytes", "runs")?
                .as_str()
                .ok_or("runs[].bytes: wants a hex string")?;
            if hex.len() % 2 != 0 {
                return Err("runs[].bytes: an odd-length hex string is not bytes".to_string());
            }
            let mut bytes = Vec::with_capacity(hex.len() / 2);
            for pair in hex.as_bytes().chunks(2) {
                let s = std::str::from_utf8(pair).map_err(|_| "runs[].bytes: not hex")?;
                bytes.push(
                    u8::from_str_radix(s, 16)
                        .map_err(|_| format!("runs[].bytes: '{s}' is not hex"))?,
                );
            }
            runs.push((offset, bytes));
        }
        Ok(Self {
            algorithm,
            base,
            size,
            entry,
            at_step,
            budget,
            regs,
            pc,
            memory_sha256,
            runs,
        })
    }
}

/// The identity check: the recorded definition pins against the live manifest — the
/// bundle's own check, shared by construction.
fn check_identity(alg: &Algorithm) -> Result<(), String> {
    replay::check_definition_pins(alg)
}

#[cfg(test)]
mod tests;
