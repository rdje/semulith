//! Exact mid-execution snapshots of the RV64GC flat-memory laboratory (P4-SYSTEM.16).
//!
//! The state inventory is the generated state's SEM-08 census: integer and FP
//! registers, PC, privilege, all CSR storage, TLB slots/FIFO position, reservation,
//! wait state and memory. Typed laboratory fault regions travel with the environment.
//! This format supplies no board/device or external-event snapshot contract.

use semulith_core::definition_rv64gc::MANIFEST;
use semulith_core::privilege::{PrivilegeMode, PrivilegedHart};
use semulith_core::reservation::Reservation;
use semulith_core::state_rv64gc::{ArchitecturalState, CSR_COUNT};
use semulith_core::translation::{Tlb, TlbEntry, TLB_CAPACITY};

use crate::fixtures::FlatMemory;
use crate::guests_rv64gc::{Refusal, RefusalKind};
use crate::json::{self, Json};
use crate::replay::{self, Algorithm};
use crate::run_rv64gc::{self, Trace};
use crate::sha256::sha256_hex;
use crate::snapshot::Snapshot;

const FORMAT: &str = "semulith-rv64gc-snapshot-v1";
/// First snapshot surface's explicit memory bound; the CPU's address width is unchanged.
pub const MAX_MEMORY_BYTES: u64 = 64 * 1024 * 1024;
/// At most one million boundaries per captured run, including its continuation.
pub const MAX_STEPS: usize = 1_000_000;
/// Fixed 4 KiB chunks keep sparse encoding overhead bounded even for alternating bytes.
pub const MAX_JSON_BYTES: usize = 2 * MAX_MEMORY_BYTES as usize + 1024 * 1024;

/// A complete CPU and laboratory environment checkpoint. Fields stay private so every
/// externally supplied record passes the same structural validation before restoration.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct SnapshotRv64gc {
    common: Snapshot,
    runtime_sha256: String,
    mode: PrivilegeMode,
    fregs: [u64; 32],
    csrs: [u64; CSR_COUNT],
    tlb: Tlb,
    reservation: Reservation,
    waiting: bool,
    refusals: Vec<Refusal>,
}

/// Continuation observations, final CPU state and final memory for further checkpoints.
pub struct Resumed {
    pub trace: Trace,
    pub state: ArchitecturalState,
    pub memory: FlatMemory,
}

fn algorithm() -> Algorithm {
    Algorithm {
        harness: concat!("semulith-verify ", env!("CARGO_PKG_VERSION")).into(),
        model: "production".into(),
        profile: MANIFEST.profile.into(),
        ilen: MANIFEST.ilen,
        generator: (
            MANIFEST.generator.name.into(),
            MANIFEST.generator.sha256.into(),
        ),
        inputs: MANIFEST
            .inputs
            .iter()
            .map(|p| (p.path.into(), p.sha256.into()))
            .collect(),
    }
}

// Definition pins cover declarative inputs; these compiled source pins additionally
// reject a checkpoint against changed runtime, state, environment or decoding machinery.
fn runtime_identity() -> &'static str {
    static IDENTITY: std::sync::OnceLock<String> = std::sync::OnceLock::new();
    IDENTITY.get_or_init(|| {
        let sources = [
            include_str!("snapshot_rv64gc.rs"),
            include_str!("snapshot.rs"),
            include_str!("replay.rs"),
            include_str!("report.rs"),
            include_str!("json.rs"),
            include_str!("sha256.rs"),
            include_str!("run_rv64gc.rs"),
            include_str!("model_rv64gc.rs"),
            include_str!("fixtures.rs"),
            include_str!("../../../Cargo.lock"),
            include_str!("../../semulith-core/src/lib.rs"),
            include_str!("../../semulith-core/src/exec_rv64gc.rs"),
            include_str!("../../semulith-core/src/exec_rv64gc/counter_writes.rs"),
            include_str!("../../semulith-core/src/exec_rv64gc/satp_writes.rs"),
            include_str!("../../semulith-core/src/exec.rs"),
            include_str!("../../semulith-core/src/arith.rs"),
            include_str!("../../semulith-core/src/fp.rs"),
            include_str!("../../semulith-core/src/muldiv.rs"),
            include_str!("../../semulith-core/src/privilege.rs"),
            include_str!("../../semulith-core/src/translation.rs"),
            include_str!("../../semulith-core/src/interrupts.rs"),
            include_str!("../../semulith-core/src/timekeeping.rs"),
            include_str!("../../semulith-core/src/reservation.rs"),
            include_str!("../../semulith-core/src/wait.rs"),
            include_str!("../../semulith-core/src/env.rs"),
            include_str!("../../semulith-core/src/outcome.rs"),
            include_str!("../../semulith-core/src/definition.rs"),
            include_str!("../../semulith-core/src/state.rs"),
            include_str!("../../semulith-core/src/state_rv64gc.rs"),
            include_str!("../../semulith-core/src/definition_rv64gc.rs"),
        ];
        let pins: String = sources.iter().map(|s| sha256_hex(s.as_bytes())).collect();
        sha256_hex(pins.as_bytes())
    })
}

impl SnapshotRv64gc {
    /// Capture without changing CPU state. The mutable borrow is required by the
    /// existing PrivilegedHart inspection surface for TLB/reservation/wait owners.
    pub fn capture(
        env: &FlatMemory,
        state: &mut ArchitecturalState,
        entry: u64,
        at_step: usize,
        budget: usize,
        refusals: &[Refusal],
    ) -> Result<Self, String> {
        let (base, size) = env.region();
        check_layout(base, size as u64, entry, at_step, budget)?;
        check_refusals(refusals)?;
        let (entries, cursor) = state.tlb().snapshot();
        let tlb = Tlb::restore(entries, cursor)?;
        let (address, width, valid) = state.reservation().snapshot();
        let reservation = Reservation::restore(address, width, valid)?;
        let runs = env
            .bytes()
            .chunks(4096)
            .enumerate()
            .filter(|(_, bytes)| bytes.iter().any(|b| *b != 0))
            .map(|(i, bytes)| ((i * 4096) as u64, bytes.to_vec()))
            .collect();
        Ok(Self {
            common: Snapshot {
                algorithm: algorithm(),
                base,
                size: size as u64,
                entry,
                at_step,
                budget,
                regs: std::array::from_fn(|i| state.read_x(i as u8)),
                pc: state.pc(),
                memory_sha256: sha256_hex(env.bytes()),
                runs,
            },
            runtime_sha256: runtime_identity().into(),
            mode: state.mode(),
            fregs: std::array::from_fn(|i| state.read_f(i as u8)),
            csrs: std::array::from_fn(|i| state.read_csr(i)),
            tlb,
            reservation,
            waiting: state.hart_state().is_waiting(),
            refusals: refusals.to_vec(),
        })
    }

    #[must_use]
    pub fn at_step(&self) -> usize {
        self.common.at_step
    }

    pub(crate) fn remaining_steps(&self) -> usize {
        self.common.budget - self.common.at_step
    }

    /// Bind the complete final owners with the same canonical checkpoint encoding.
    pub(crate) fn result_sha256(&self, result: &mut Resumed) -> Result<String, String> {
        let final_snapshot = Self::capture(
            &result.memory,
            &mut result.state,
            self.common.entry,
            self.common.at_step + result.trace.steps.len(),
            self.common.budget,
            &self.refusals,
        )?;
        Ok(sha256_hex(final_snapshot.to_json().as_bytes()))
    }

    /// Restore the exact checkpoint without advancing a boundary.
    pub fn restore(&self) -> Result<(ArchitecturalState, FlatMemory), String> {
        if self.common.algorithm != algorithm() || self.runtime_sha256 != runtime_identity() {
            return Err("RV64GC snapshot: definition/runtime identity mismatch".into());
        }
        check_layout(
            self.common.base,
            self.common.size,
            self.common.entry,
            self.common.at_step,
            self.common.budget,
        )?;
        let mut memory =
            FlatMemory::with_fetch_align(self.common.base, self.common.size as usize, 2);
        let mut previous_end = 0;
        for (offset, bytes) in &self.common.runs {
            let end = offset
                .checked_add(bytes.len() as u64)
                .filter(|end| *end <= self.common.size)
                .ok_or("RV64GC snapshot: memory run exceeds region")?;
            if bytes.is_empty() || *offset < previous_end {
                return Err("RV64GC snapshot: empty, overlapping or unordered memory run".into());
            }
            memory.bytes_mut()[*offset as usize..end as usize].copy_from_slice(bytes);
            previous_end = end;
        }
        if sha256_hex(memory.bytes()) != self.common.memory_sha256 {
            return Err("RV64GC snapshot: memory digest mismatch".into());
        }
        let mut state = ArchitecturalState::zeroed_at(self.common.entry);
        for i in 0..32u8 {
            state.write_x(i, self.common.regs[i as usize]);
            state.write_f(i, self.fregs[i as usize]);
        }
        for (i, value) in self.csrs.iter().enumerate() {
            state.write_csr(i, *value);
        }
        state.set_pc(self.common.pc);
        state.set_mode(self.mode);
        *state.tlb() = self.tlb.clone();
        *state.reservation() = self.reservation;
        if self.waiting {
            state.hart_state().enter();
        }
        Ok((state, memory))
    }

    /// Identity and memory integrity are checked before executing a continuation.
    pub fn resume(&self) -> Result<Resumed, String> {
        self.resume_with_model(crate::model_rv64gc::Model::Production)
    }

    /// A bundle records this additional choice; the checkpoint pins base-state compatibility.
    pub(crate) fn resume_with_model(
        &self,
        model: crate::model_rv64gc::Model,
    ) -> Result<Resumed, String> {
        let (mut state, mut memory) = self.restore()?;
        let trace = run_rv64gc::run_from_with_model(
            &mut memory,
            &mut state,
            self.common.budget - self.common.at_step,
            &self.refusals,
            model,
        )?;
        Ok(Resumed {
            trace,
            state,
            memory,
        })
    }

    /// Deterministic JSON; fixed memory chunks bound the output to MAX_JSON_BYTES.
    #[must_use]
    pub fn to_json(&self) -> String {
        let mut out = format!("{{\"format\":\"{FORMAT}\",\"runtime_sha256\":\"");
        crate::report::push_escaped(&mut out, &self.runtime_sha256);
        out.push_str(&format!(
            "\",\"common\":{},\"mode\":{},\"waiting\":{},\"fregs\":[",
            self.common.to_json(),
            self.mode.code(),
            self.waiting
        ));
        push_words(&mut out, &self.fregs);
        out.push_str("],\"csrs\":[");
        push_words(&mut out, &self.csrs);
        let (entries, cursor) = self.tlb.snapshot();
        out.push_str(&format!("],\"tlb\":{{\"cursor\":{cursor},\"entries\":["));
        for (i, e) in entries.iter().enumerate() {
            if i != 0 {
                out.push(',');
            }
            out.push_str(&format!("{{\"valid\":{},\"global\":{},\"asid\":{},\"vpn\":\"0x{:016x}\",\"pa_base\":\"0x{:016x}\",\"r\":{},\"w\":{},\"x\":{},\"u\":{},\"a\":{},\"d\":{},\"level\":{}}}",
                                  e.valid,e.global,e.asid,e.vpn,e.pa_base,e.r,e.w,e.x,e.u,e.a,e.d,e.level));
        }
        let (address, width, valid) = self.reservation.snapshot();
        out.push_str(&format!("]}},\"reservation\":{{\"address\":\"0x{address:016x}\",\"width\":{width},\"valid\":{valid}}},\"refusals\":["));
        for (i, r) in self.refusals.iter().enumerate() {
            if i != 0 {
                out.push(',');
            }
            let kind = match r.kind {
                RefusalKind::Fetch => "fetch",
                RefusalKind::Load => "load",
                RefusalKind::Store => "store",
                RefusalKind::Walk => "walk",
            };
            out.push_str(&format!(
                "{{\"kind\":\"{kind}\",\"base\":\"0x{:016x}\",\"size\":\"0x{:016x}\"}}",
                r.base, r.size
            ));
        }
        out.push_str("]}");
        out
    }

    /// Parse all state owners. Size and nesting limits precede the shared JSON reader.
    pub fn parse(text: &str) -> Result<Self, String> {
        check_json_limits(text, MAX_JSON_BYTES, 131072, "RV64GC snapshot")?;
        let doc = json::parse(text).map_err(|e| format!("RV64GC snapshot: {e}"))?;
        Self::from_json(&doc)
    }

    pub(crate) fn from_json(doc: &Json) -> Result<Self, String> {
        let obj = object(doc)?;
        if field(obj, "format")?.as_str() != Some(FORMAT) {
            return Err("RV64GC snapshot: unsupported format".into());
        }
        let common = Snapshot::from_json(field(obj, "common")?)?;
        check_layout(
            common.base,
            common.size,
            common.entry,
            common.at_step,
            common.budget,
        )?;
        if common.regs[0] != 0 {
            return Err("RV64GC snapshot: x0 must be zero".into());
        }
        let mode = match number(field(obj, "mode")?, "mode")? {
            0 => PrivilegeMode::U,
            1 => PrivilegeMode::S,
            3 => PrivilegeMode::M,
            _ => return Err("RV64GC snapshot: invalid privilege mode".into()),
        };
        let tlb_obj = object(field(obj, "tlb")?)?;
        let slots = field(tlb_obj, "entries")?
            .as_arr()
            .filter(|a| a.len() == TLB_CAPACITY)
            .ok_or("RV64GC snapshot: exactly four TLB entries required")?;
        let mut entries = [TlbEntry::default(); TLB_CAPACITY];
        for (e, node) in entries.iter_mut().zip(slots) {
            let v = object(node)?;
            *e = TlbEntry {
                valid: boolean(field(v, "valid")?)?,
                global: boolean(field(v, "global")?)?,
                asid: u16::try_from(number(field(v, "asid")?, "asid")?)
                    .map_err(|_| "invalid TLB ASID")?,
                vpn: word(field(v, "vpn")?)?,
                pa_base: word(field(v, "pa_base")?)?,
                r: boolean(field(v, "r")?)?,
                w: boolean(field(v, "w")?)?,
                x: boolean(field(v, "x")?)?,
                u: boolean(field(v, "u")?)?,
                a: boolean(field(v, "a")?)?,
                d: boolean(field(v, "d")?)?,
                level: i64::try_from(number(field(v, "level")?, "level")?)
                    .map_err(|_| "invalid TLB level")?,
            };
        }
        let tlb = Tlb::restore(entries, number(field(tlb_obj, "cursor")?, "cursor")?)?;
        let r = object(field(obj, "reservation")?)?;
        let reservation = Reservation::restore(
            word(field(r, "address")?)?,
            u8::try_from(number(field(r, "width")?, "width")?)
                .map_err(|_| "invalid reservation width")?,
            boolean(field(r, "valid")?)?,
        )?;
        let mut refusals = Vec::new();
        let raw = field(obj, "refusals")?
            .as_arr()
            .filter(|a| a.len() <= 64)
            .ok_or("invalid refusal list")?;
        for node in raw {
            let r = object(node)?;
            let kind = match field(r, "kind")?.as_str() {
                Some("fetch") => RefusalKind::Fetch,
                Some("load") => RefusalKind::Load,
                Some("store") => RefusalKind::Store,
                Some("walk") => RefusalKind::Walk,
                _ => return Err("invalid refusal kind".into()),
            };
            refusals.push(Refusal {
                kind,
                base: word(field(r, "base")?)?,
                size: word(field(r, "size")?)?,
            });
        }
        check_refusals(&refusals)?;
        Ok(Self {
            common,
            runtime_sha256: field(obj, "runtime_sha256")?
                .as_str()
                .ok_or("runtime identity must be a string")?
                .into(),
            mode,
            fregs: words(field(obj, "fregs")?)?,
            csrs: words(field(obj, "csrs")?)?,
            tlb,
            reservation,
            waiting: boolean(field(obj, "waiting")?)?,
            refusals,
        })
    }
}

fn check_layout(base: u64, size: u64, entry: u64, at: usize, budget: usize) -> Result<(), String> {
    if size == 0 || size > MAX_MEMORY_BYTES || base.checked_add(size).is_none() {
        return Err(
            "RV64GC snapshot: memory region must fit 1..=64 MiB without address wrap".into(),
        );
    }
    if at > budget || budget > MAX_STEPS {
        return Err("RV64GC snapshot: invalid step index/budget (maximum 1000000)".into());
    }
    replay::check_layout(base, size, entry, 0)
}
fn check_refusals(refusals: &[Refusal]) -> Result<(), String> {
    if refusals.len() > 64
        || refusals
            .iter()
            .any(|r| r.size == 0 || r.base.checked_add(r.size).is_none())
    {
        return Err("RV64GC snapshot: invalid laboratory refusal regions".into());
    }
    Ok(())
}
fn object(value: &Json) -> Result<&[(String, Json)], String> {
    value
        .as_obj()
        .ok_or("RV64GC snapshot: expected object".into())
}
fn field<'a>(obj: &'a [(String, Json)], key: &str) -> Result<&'a Json, String> {
    replay::need(obj, key, "RV64GC snapshot")
}
fn word(value: &Json) -> Result<u64, String> {
    replay::hex_u64(value, "RV64GC state word")
}
fn number(value: &Json, name: &str) -> Result<usize, String> {
    replay::int_usize(value, name)
}
fn boolean(value: &Json) -> Result<bool, String> {
    if let Json::Bool(v) = value {
        Ok(*v)
    } else {
        Err("RV64GC snapshot: expected boolean".into())
    }
}
fn words<const N: usize>(value: &Json) -> Result<[u64; N], String> {
    let values = value
        .as_arr()
        .filter(|a| a.len() == N)
        .ok_or_else(|| format!("RV64GC snapshot: expected {N} state words"))?;
    let mut result = [0; N];
    for (out, value) in result.iter_mut().zip(values) {
        *out = word(value)?;
    }
    Ok(result)
}
fn push_words(out: &mut String, values: &[u64]) {
    for (i, value) in values.iter().enumerate() {
        if i != 0 {
            out.push(',');
        }
        out.push_str(&format!("\"0x{value:016x}\""));
    }
}
pub(crate) fn check_json_limits(
    text: &str,
    max_bytes: usize,
    max_structure: usize,
    kind: &str,
) -> Result<(), String> {
    if text.len() > max_bytes {
        return Err(format!("{kind}: JSON byte limit exceeded"));
    }
    let (mut depth, mut string, mut escaped, mut structure) = (0usize, false, false, 0usize);
    for byte in text.bytes() {
        if string {
            if escaped {
                escaped = false;
            } else if byte == b'\\' {
                escaped = true;
            } else if byte == b'"' {
                string = false;
            }
        } else {
            if matches!(byte, b'[' | b'{' | b',' | b':') {
                structure += 1;
                if structure > max_structure {
                    return Err(format!("{kind}: JSON structure limit exceeded"));
                }
            }
            match byte {
                b'"' => string = true,
                b'[' | b'{' => {
                    depth += 1;
                    if depth > 12 {
                        return Err(format!("{kind}: JSON nesting limit exceeded"));
                    }
                }
                b']' | b'}' => depth = depth.saturating_sub(1),
                _ => {}
            }
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests;
