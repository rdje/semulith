//! The performance-baseline harness — `P1-LAB.11`, RUST-04: measure arithmetic,
//! control-flow, memory and fault-heavy mixes separately, on a named host, with allocation
//! counts, in ARCHITECTURE §6's three modes — **untraced**, **instrumented**, **diagnostic** —
//! and characterize the measurement noise BEFORE any regression threshold exists. No MIPS
//! target is invented anywhere in this module: the deliverable is the noise table a future
//! threshold must cite, not a verdict.
//!
//! ## Workload mixes
//!
//! [`Mix::program`] generates each mix's guest words programmatically. The encoders are
//! harness-local data construction — the same standing as the mutation suite's mutated
//! trees (`P1-LAB.9`): they feed the ONE generated definition and are pinned to it by a
//! test that decode-round-trips every generated word against `definition::decode`, so the
//! encoder cannot drift from the definition it feeds. Each mix is a counted loop ending in
//! EBREAK, so a run terminates on a requested trap and the step budget is only a safety
//! bound:
//!
//! - **arithmetic** — the ALU vocabulary (reg/imm, shifts, word ops, LUI/AUIPC) with no
//!   data-memory traffic and one loop branch;
//! - **control** — alternating taken/not-taken branches plus jal/jalr call/return, a
//!   transfer on roughly every other step;
//! - **memory** — sd/sw/sh/sb stores and ld/lw/lh/lb/lwu/lhu/lbu loads over a scratch area
//!   inside the region;
//! - **fault** — the exception paths as the common case: per iteration a model-side
//!   misaligned load (raised BEFORE the boundary, `exec`'s own alignment rule), a
//!   model-side misaligned store, and an environment-side out-of-region load (the
//!   boundary's AccessFault answer).
//!
//! The fault mix runs under the stated harness policy ([`apply_outcome`]): a delivered
//! exception is observed and execution resumes at pc+4 (delivery-continues, ARCHITECTURE
//! §5); a requested trap (EBREAK) stops the run; a fetch access-fault stops without an
//! observation (run.rs's rule — a failed fetch supplied no word).
//!
//! ## The three modes
//!
//! - [`run_untraced`] — the bare `exec::step` loop; no observation is constructed.
//! - [`run_instrumented`] — the `(pc, word, writes, trap)` Step stream, built with
//!   `run`'s own snapshot/diff and trap mapping (shared `pub(crate)`, so the measured mode
//!   IS the production observation construction). The executed word comes from the
//!   harness's own image — never a second fetch, which would corrupt the census. The
//!   runner is generic over [`Observer`], so this tree's static-vs-dynamic dispatch
//!   question is measured: one function instantiated with [`VecObserver`] and with
//!   `dyn Observer` is two cells of the same report.
//! - [`run_diagnostic`] — the Step stream plus the full boundary-crossing log (`run`'s
//!   own `Recording` wrapper).
//!
//! All modes run under one counting environment wrapper ([`Census`]), so the crossing
//! census is comparable across modes without being recorded. RUST-02 is CHECKED, not
//! assumed: [`agree`] requires all modes to agree on step count, stop classification,
//! final architectural state and census, and every recorded Step stream to be identical.
//!
//! ## Allocation counts and noise
//!
//! [`alloc`] is a `GlobalAlloc` wrapper over `System` (std-only, RUST-01) installed by the
//! CLI binary and by this crate's test binary; the wasm cdylib is untouched. Allocations
//! and bytes per step are reported per mix per mode — RUST-03's "no mandatory
//! per-instruction allocation" as a number. [`stats`] reduces each cell's repeated samples
//! to min/median/mean/max and the (max−min)/median spread; the report exists so a
//! threshold can be set FROM the noise, never before it.

use semulith_core::env::{BoundaryError, Environment, Request, Response};
use semulith_core::exec;
use semulith_core::outcome::{ExceptionCause, StepOutcome, TargetEvent};
use semulith_core::state::ArchitecturalState;

use crate::fixtures::FlatMemory;
use crate::run::{self, Crossing, Recording, Step, Stop};

/// The laboratory platform anchor every benchmark mix runs at (the tracked guests' entry).
pub const ENTRY: u64 = 0x8000_0000;
/// The one declared memory region's size (64 KiB) — small enough that the fault mix's
/// out-of-region address is a short, honest constant.
pub const REGION_SIZE: usize = 0x1_0000;
/// The scratch area offset (within the region) the memory mix walks and the fault mix
/// misaligns against.
pub const DATA_OFFSET: u64 = 0x8000;
/// The fault mix's environment-side fault address: aligned, and outside every declared
/// region, so the boundary answers AccessFault.
pub const OOB_ADDR: u64 = ENTRY + REGION_SIZE as u64 + 0x1000;

/// The harness sanity bound on the iteration count (a workload is meant to be measured
/// in seconds, not to run unbounded).
pub const MAX_ITERATIONS: u32 = 1_000_000;

// ---------------------------------------------------------------------------
// Instruction encoders — harness-local data construction, pinned to the
// generated definition by the decode round-trip test in `bench/tests.rs`.
// ---------------------------------------------------------------------------

fn r_type(funct7: u32, rs2: u32, rs1: u32, funct3: u32, rd: u32, opcode: u32) -> u32 {
    (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
}

fn i_type(imm: i32, rs1: u32, funct3: u32, rd: u32, opcode: u32) -> u32 {
    ((imm as u32 & 0xFFF) << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
}

fn s_type(imm: i32, rs2: u32, rs1: u32, funct3: u32) -> u32 {
    let imm = imm as u32 & 0xFFF;
    ((imm >> 5) << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | ((imm & 0x1F) << 7) | 0x23
}

fn b_type(offset: i32, rs2: u32, rs1: u32, funct3: u32) -> u32 {
    let imm = offset as u32;
    ((imm >> 12 & 1) << 31)
        | ((imm >> 5 & 0x3F) << 25)
        | (rs2 << 20)
        | (rs1 << 15)
        | (funct3 << 12)
        | ((imm >> 1 & 0xF) << 8)
        | ((imm >> 11 & 1) << 7)
        | 0x63
}

fn u_type(imm20: u32, rd: u32, opcode: u32) -> u32 {
    (imm20 << 12) | (rd << 7) | opcode
}

fn j_type(offset: i32, rd: u32) -> u32 {
    let imm = offset as u32;
    ((imm >> 20 & 1) << 31)
        | ((imm >> 12 & 0xFF) << 12)
        | ((imm >> 11 & 1) << 20)
        | ((imm >> 1 & 0x3FF) << 21)
        | (rd << 7)
        | 0x6F
}

fn addi(rd: u32, rs1: u32, imm: i32) -> u32 {
    i_type(imm, rs1, 0, rd, 0x13)
}
fn andi(rd: u32, rs1: u32, imm: i32) -> u32 {
    i_type(imm, rs1, 7, rd, 0x13)
}
fn ori(rd: u32, rs1: u32, imm: i32) -> u32 {
    i_type(imm, rs1, 6, rd, 0x13)
}
fn xori(rd: u32, rs1: u32, imm: i32) -> u32 {
    i_type(imm, rs1, 4, rd, 0x13)
}
fn slti(rd: u32, rs1: u32, imm: i32) -> u32 {
    i_type(imm, rs1, 2, rd, 0x13)
}
fn slli(rd: u32, rs1: u32, shamt: u32) -> u32 {
    i_type(shamt as i32, rs1, 1, rd, 0x13)
}
fn srli(rd: u32, rs1: u32, shamt: u32) -> u32 {
    i_type(shamt as i32, rs1, 5, rd, 0x13)
}
fn srai(rd: u32, rs1: u32, shamt: u32) -> u32 {
    i_type((0x400 | shamt) as i32, rs1, 5, rd, 0x13)
}
fn addiw(rd: u32, rs1: u32, imm: i32) -> u32 {
    i_type(imm, rs1, 0, rd, 0x1B)
}
fn slliw(rd: u32, rs1: u32, shamt: u32) -> u32 {
    i_type(shamt as i32, rs1, 1, rd, 0x1B)
}
fn srliw(rd: u32, rs1: u32, shamt: u32) -> u32 {
    i_type(shamt as i32, rs1, 5, rd, 0x1B)
}
fn sraiw(rd: u32, rs1: u32, shamt: u32) -> u32 {
    i_type((0x400 | shamt) as i32, rs1, 5, rd, 0x1B)
}
fn add(rd: u32, rs1: u32, rs2: u32) -> u32 {
    r_type(0, rs2, rs1, 0, rd, 0x33)
}
fn sub(rd: u32, rs1: u32, rs2: u32) -> u32 {
    r_type(0x20, rs2, rs1, 0, rd, 0x33)
}
fn sll(rd: u32, rs1: u32, rs2: u32) -> u32 {
    r_type(0, rs2, rs1, 1, rd, 0x33)
}
fn slt(rd: u32, rs1: u32, rs2: u32) -> u32 {
    r_type(0, rs2, rs1, 2, rd, 0x33)
}
fn sltu(rd: u32, rs1: u32, rs2: u32) -> u32 {
    r_type(0, rs2, rs1, 3, rd, 0x33)
}
fn xor_(rd: u32, rs1: u32, rs2: u32) -> u32 {
    r_type(0, rs2, rs1, 4, rd, 0x33)
}
fn srl(rd: u32, rs1: u32, rs2: u32) -> u32 {
    r_type(0, rs2, rs1, 5, rd, 0x33)
}
fn sra(rd: u32, rs1: u32, rs2: u32) -> u32 {
    r_type(0x20, rs2, rs1, 5, rd, 0x33)
}
fn or_(rd: u32, rs1: u32, rs2: u32) -> u32 {
    r_type(0, rs2, rs1, 6, rd, 0x33)
}
fn and_(rd: u32, rs1: u32, rs2: u32) -> u32 {
    r_type(0, rs2, rs1, 7, rd, 0x33)
}
fn addw(rd: u32, rs1: u32, rs2: u32) -> u32 {
    r_type(0, rs2, rs1, 0, rd, 0x3B)
}
fn subw(rd: u32, rs1: u32, rs2: u32) -> u32 {
    r_type(0x20, rs2, rs1, 0, rd, 0x3B)
}
fn lui(rd: u32, imm20: u32) -> u32 {
    u_type(imm20, rd, 0x37)
}
fn auipc(rd: u32, imm20: u32) -> u32 {
    u_type(imm20, rd, 0x17)
}
fn jal(rd: u32, offset: i32) -> u32 {
    j_type(offset, rd)
}
fn jalr(rd: u32, rs1: u32, imm: i32) -> u32 {
    i_type(imm, rs1, 0, rd, 0x67)
}
fn beq(rs1: u32, rs2: u32, offset: i32) -> u32 {
    b_type(offset, rs2, rs1, 0)
}
fn bne(rs1: u32, rs2: u32, offset: i32) -> u32 {
    b_type(offset, rs2, rs1, 1)
}
fn lb(rd: u32, rs1: u32, imm: i32) -> u32 {
    i_type(imm, rs1, 0, rd, 0x03)
}
fn lh(rd: u32, rs1: u32, imm: i32) -> u32 {
    i_type(imm, rs1, 1, rd, 0x03)
}
fn lw(rd: u32, rs1: u32, imm: i32) -> u32 {
    i_type(imm, rs1, 2, rd, 0x03)
}
fn ld(rd: u32, rs1: u32, imm: i32) -> u32 {
    i_type(imm, rs1, 3, rd, 0x03)
}
fn lbu(rd: u32, rs1: u32, imm: i32) -> u32 {
    i_type(imm, rs1, 4, rd, 0x03)
}
fn lhu(rd: u32, rs1: u32, imm: i32) -> u32 {
    i_type(imm, rs1, 5, rd, 0x03)
}
fn lwu(rd: u32, rs1: u32, imm: i32) -> u32 {
    i_type(imm, rs1, 6, rd, 0x03)
}
fn sb(rs2: u32, rs1: u32, imm: i32) -> u32 {
    s_type(imm, rs2, rs1, 0)
}
fn sh(rs2: u32, rs1: u32, imm: i32) -> u32 {
    s_type(imm, rs2, rs1, 1)
}
fn sw(rs2: u32, rs1: u32, imm: i32) -> u32 {
    s_type(imm, rs2, rs1, 2)
}
fn sd(rs2: u32, rs1: u32, imm: i32) -> u32 {
    s_type(imm, rs2, rs1, 3)
}
const EBREAK: u32 = 0x0010_0073;

/// One program point: the instruction name the generator intends, and the word it emitted.
/// The names ride along so the decode round-trip test pins EVERY word to the instruction
/// the generated definition decodes it to — the encoder cannot drift silently.
type NamedWords = Vec<(&'static str, u32)>;

/// zext-by-shifts idiom: `lui` sign-extends from bit 31, so a 0x8000_xxxx address is
/// assembled as lui + slli 32 + srli 32. Returns the three named words setting `rd`.
fn zext_address(rd: u32, imm20: u32) -> [(&'static str, u32); 3] {
    [
        ("lui", lui(rd, imm20)),
        ("slli", slli(rd, rd, 32)),
        ("srli", srli(rd, rd, 32)),
    ]
}

/// The four workload mixes, measured separately per ARCHITECTURE §6.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Mix {
    /// ALU vocabulary only: no data-memory traffic, one loop branch.
    Arithmetic,
    /// Taken/not-taken branches plus jal/jalr call-return; a transfer every other step.
    Control,
    /// Stores and loads at all four widths over a scratch area.
    Memory,
    /// The exception paths as the common case: model-side misaligned load and store,
    /// environment-side out-of-region load, every iteration.
    Fault,
}

impl Mix {
    /// Every mix, in report order.
    pub const ALL: [Mix; 4] = [Mix::Arithmetic, Mix::Control, Mix::Memory, Mix::Fault];

    /// The mix's report name.
    #[must_use]
    pub fn name(self) -> &'static str {
        match self {
            Mix::Arithmetic => "arithmetic",
            Mix::Control => "control",
            Mix::Memory => "memory",
            Mix::Fault => "fault",
        }
    }

    /// The mix's guest words: a counted loop of `iterations` rounds ending in EBREAK.
    ///
    /// # Panics
    /// Refuses an iteration count outside `1..=MAX_ITERATIONS` — a generator that guesses
    /// is a second definition.
    #[must_use]
    pub fn program(self, iterations: u32) -> Vec<u32> {
        self.named_program(iterations)
            .into_iter()
            .map(|(_, word)| word)
            .collect()
    }

    /// The program with the intended instruction name riding on every word (the decode
    /// round-trip test's pin).
    #[must_use]
    pub fn named_program(self, iterations: u32) -> NamedWords {
        assert!(
            (1..=MAX_ITERATIONS).contains(&iterations),
            "iterations {iterations} outside 1..={MAX_ITERATIONS} (the harness sanity bound)"
        );
        match self {
            Mix::Arithmetic => arithmetic_program(iterations),
            Mix::Control => control_program(iterations),
            Mix::Memory => memory_program(iterations),
            Mix::Fault => fault_program(iterations),
        }
    }
}

/// The loop counter x28's initialization: a bare addi inside its signed-12-bit range, else
/// the canonical lui+addiw pair (the addi immediate's sign is pre-compensated in hi).
fn counter(iterations: u32) -> NamedWords {
    if iterations <= 2047 {
        vec![("addi", addi(28, 0, iterations as i32))]
    } else {
        let hi = (iterations + 0x800) >> 12;
        let lo = iterations as i32 - (hi << 12) as i32;
        vec![("lui", lui(28, hi)), ("addiw", addiw(28, 28, lo))]
    }
}

/// The backward branch closing a counted loop: `bne x28, x0, loop_start`.
fn loop_back(body: &NamedWords, loop_start: usize) -> (&'static str, u32) {
    let offset = -4 * (body.len() - loop_start) as i32;
    ("bne", bne(28, 0, offset))
}

fn arithmetic_program(iterations: u32) -> NamedWords {
    let mut p: NamedWords = counter(iterations);
    let loop_start = p.len();
    p.push(("add", add(1, 2, 3)));
    p.push(("sub", sub(2, 1, 4)));
    p.push(("and", and_(3, 1, 2)));
    p.push(("or", or_(4, 3, 5)));
    p.push(("xor", xor_(5, 4, 6)));
    p.push(("sll", sll(6, 5, 7)));
    p.push(("srl", srl(7, 6, 8)));
    p.push(("sra", sra(8, 7, 9)));
    p.push(("slt", slt(9, 8, 10)));
    p.push(("sltu", sltu(10, 9, 11)));
    p.push(("addi", addi(11, 11, 7)));
    p.push(("xori", xori(12, 11, 0x5A5)));
    p.push(("ori", ori(13, 12, 0x33)));
    p.push(("andi", andi(14, 13, 0x7F)));
    p.push(("slti", slti(15, 14, 100)));
    p.push(("slli", slli(16, 15, 3)));
    p.push(("srli", srli(17, 16, 2)));
    p.push(("srai", srai(18, 17, 1)));
    p.push(("lui", lui(19, 0x12345)));
    p.push(("auipc", auipc(20, 0x1)));
    p.push(("addw", addw(21, 1, 2)));
    p.push(("subw", subw(22, 21, 3)));
    p.push(("addiw", addiw(23, 22, -3)));
    p.push(("slliw", slliw(24, 23, 2)));
    p.push(("srliw", srliw(25, 24, 1)));
    p.push(("sraiw", sraiw(26, 25, 1)));
    p.push(("addi", addi(28, 28, -1)));
    p.push(loop_back(&p, loop_start));
    p.push(("ebreak", EBREAK));
    p
}

fn control_program(iterations: u32) -> NamedWords {
    // Layout (indices relative to loop_start L):
    //   L+0  beq  x28, x0, end      (taken only on the final pass)
    //   L+1  addi x28, x28, -1
    //   L+2  andi x6, x28, 1
    //   L+3  beq  x6, x0, even      (alternates taken / not-taken)
    //   L+4  addi x7, x7, 1         (odd path)
    //   L+5  jal  x0, tail
    //   L+6  addi x8, x8, 1         (even path)
    //   L+7  jal  x9, sub           (call)
    //   L+8  jal  x0, loop
    //   L+9  addi x10, x10, 1       (sub)
    //   L+10 jalr x0, 0(x9)         (return — the bit-clearing path)
    //   L+11 ebreak                 (end)
    let mut p: NamedWords = counter(iterations);
    let l = p.len();
    p.push(("beq", beq(28, 0, 4 * 11))); // L+0 -> L+11
    p.push(("addi", addi(28, 28, -1)));
    p.push(("andi", andi(6, 28, 1)));
    p.push(("beq", beq(6, 0, 4 * 3))); // L+3 -> L+6
    p.push(("addi", addi(7, 7, 1)));
    p.push(("jal", jal(0, 4 * 2))); // L+5 -> L+7
    p.push(("addi", addi(8, 8, 1)));
    p.push(("jal", jal(9, 4 * 2))); // L+7 -> L+9
    p.push(("jal", jal(0, -4 * 8))); // L+8 -> L+0
    p.push(("addi", addi(10, 10, 1)));
    p.push(("jalr", jalr(0, 9, 0)));
    p.push(("ebreak", EBREAK));
    debug_assert_eq!(p.len(), l + 12, "control layout drifted from its offsets");
    p
}

fn memory_program(iterations: u32) -> NamedWords {
    let mut p: NamedWords = zext_address(30, 0x80008).to_vec(); // x30 = ENTRY + DATA_OFFSET
    p.extend(counter(iterations));
    let loop_start = p.len();
    p.push(("andi", andi(5, 28, 0xF)));
    p.push(("slli", slli(5, 5, 3)));
    p.push(("add", add(5, 30, 5))); // x5 = scratch + (iteration & 0xF) * 8
    p.push(("sd", sd(1, 5, 0)));
    p.push(("sw", sw(2, 5, 4)));
    p.push(("sh", sh(3, 5, 2)));
    p.push(("sb", sb(4, 5, 1)));
    p.push(("ld", ld(11, 5, 0)));
    p.push(("lwu", lwu(12, 5, 0)));
    p.push(("lw", lw(13, 5, 4)));
    p.push(("lhu", lhu(14, 5, 2)));
    p.push(("lh", lh(15, 5, 0)));
    p.push(("lbu", lbu(16, 5, 1)));
    p.push(("lb", lb(17, 5, 3)));
    p.push(("add", add(1, 11, 12)));
    p.push(("addi", addi(28, 28, -1)));
    p.push(loop_back(&p, loop_start));
    p.push(("ebreak", EBREAK));
    p
}

fn fault_program(iterations: u32) -> NamedWords {
    // OOB_ADDR = 0x8002_1000 -> lui imm20 0x80021; DATA_OFFSET + 2 is the misaligned cell.
    let mut p: NamedWords = zext_address(30, 0x80021).to_vec(); // x30 = OOB_ADDR
    p.extend(zext_address(29, 0x80008)); // x29 = ENTRY + DATA_OFFSET
    p.push(("addi", addi(29, 29, 2))); // x29 misaligned for W/D accesses
    p.extend(counter(iterations));
    let loop_start = p.len();
    p.push(("addi", addi(28, 28, -1)));
    p.push(("lw", lw(11, 29, 0))); // LoadAddressMisaligned — model-side, before the boundary
    p.push(("sw", sw(13, 29, 0))); // StoreAddressMisaligned — model-side
    p.push(("ld", ld(12, 30, 0))); // LoadAccessFault — the boundary's answer
    p.push(loop_back(&p, loop_start));
    p.push(("ebreak", EBREAK));
    p
}

// ---------------------------------------------------------------------------
// The harness: census, outcome policy, and the three modes.
// ---------------------------------------------------------------------------

/// The per-kind boundary-crossing census every mode records identically: requests by
/// kind, target-facing failure answers, contract violations. Comparable across modes
/// because it counts without recording — the diagnostic mode's crossing LOG is the cost
/// being measured, the census is not.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct Census {
    /// Fetch requests.
    pub fetches: u64,
    /// Load requests.
    pub loads: u64,
    /// Store requests.
    pub stores: u64,
    /// Page-table walk-access requests (P4-SYSTEM.3 — always zero on the rv64i bench;
    /// the boundary vocabulary gained the kind with the translation machinery).
    pub walks: u64,
    /// Target-facing failure answers (access fault / misaligned).
    pub faults: u64,
    /// Contract violations (the environment broke a rule).
    pub violations: u64,
}

struct Counting<'a, E: Environment> {
    inner: &'a mut E,
    census: &'a mut Census,
}

impl<E: Environment> Environment for Counting<'_, E> {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        match request {
            Request::Fetch { .. } | Request::FetchParcel { .. } => self.census.fetches += 1,
            Request::Load { .. } => self.census.loads += 1,
            Request::Store { .. } => self.census.stores += 1,
            Request::WalkAccess { .. } => self.census.walks += 1,
        }
        let response = self.inner.request(request);
        match response {
            Err(BoundaryError::Target(_)) => self.census.faults += 1,
            Err(BoundaryError::Violation(_)) => self.census.violations += 1,
            Ok(_) => {}
        }
        response
    }
}

/// What one run established, independent of any tracing: how many steps produced an
/// observation, why the run stopped, the final architectural state, and the census.
/// This is the cross-mode comparable residue — an untraced run has nothing else BY
/// DESIGN, so agreement is stated over these facts plus any recorded streams.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct RunFacts {
    /// Steps that produced an observation (a fetch fault produces none — run.rs's rule).
    pub steps: usize,
    /// Why the run stopped.
    pub stop: Stop,
    /// The 32 architectural registers at the stop.
    pub regs: [u64; 32],
    /// The pc at the stop.
    pub pc: u64,
    /// The boundary-crossing census.
    pub census: Census,
}

/// One mode's run: the facts, plus the Step stream where the mode records one.
#[derive(Clone, Debug)]
pub struct ModeRun {
    /// The mode-independent facts.
    pub facts: RunFacts,
    /// The observation stream — `Some` for instrumented and diagnostic, `None` for
    /// untraced (which constructs no observations at all; that absence is the point).
    pub steps: Option<Vec<Step>>,
}

/// The bench harness's own failure: a traced mode needed the word at a pc outside the
/// guest image. The tracked mixes never do this (a runaway pc is caught by the agreement
/// check instead); a refusal is named, never an invented word.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct HarnessError(pub String);

/// The outcome policy the benchmark harness states and every mode applies identically:
/// a delivered exception (other than a fetch fault) is observed and execution resumes at
/// pc+4 (delivery-continues, ARCHITECTURE §5); a requested trap is observed and stops the
/// run; a fetch fault, a model error and an undefined case stop without an observation.
enum Disposition {
    /// A step observation exists; keep running.
    Observed,
    /// A step observation exists; then stop with this reason.
    StopAfterObservation(Stop),
    /// No observation; stop with this reason.
    StopSilent(Stop),
}

fn apply_outcome(state: &mut ArchitecturalState, pc: u64, outcome: &StepOutcome) -> Disposition {
    match outcome {
        StepOutcome::Advanced(_) => Disposition::Observed,
        StepOutcome::Event(TargetEvent::Exception {
            cause: ExceptionCause::InstructionAccessFault,
            ..
        }) => Disposition::StopSilent(Stop::FetchFault { at: pc }),
        StepOutcome::Event(TargetEvent::Exception { .. }) => {
            state.set_pc(pc.wrapping_add(4));
            Disposition::Observed
        }
        StepOutcome::Event(TargetEvent::RequestedTrap { .. }) => {
            Disposition::StopAfterObservation(Stop::Trap)
        }
        StepOutcome::Undefined(case) => Disposition::StopSilent(Stop::Undefined(*case)),
        StepOutcome::Failed(error) => Disposition::StopSilent(Stop::Failed(*error)),
    }
}

/// The executed word for one observed step, from the harness's own image — never a second
/// fetch, which the census would (correctly) count as extraneous.
fn image_word(image: &[u32], pc: u64) -> Result<u32, HarnessError> {
    let in_image = pc
        .checked_sub(ENTRY)
        .filter(|offset| offset.is_multiple_of(4))
        .map(|offset| (offset / 4) as usize)
        .and_then(|index| image.get(index));
    match in_image {
        Some(word) => Ok(*word),
        None => Err(HarnessError(format!(
            "pc {pc:#018x} lies outside the {}-word guest image at {ENTRY:#018x}",
            image.len()
        ))),
    }
}

/// A safety bound for a mix run: the mixes terminate on EBREAK by construction, so
/// reaching the budget means the program escaped — a bench defect, reported, never
/// silently measured.
#[must_use]
pub fn budget_for(mix: Mix, iterations: u32) -> usize {
    let per_iteration = match mix {
        Mix::Arithmetic => 32,
        Mix::Control => 16,
        Mix::Memory => 24,
        Mix::Fault => 8,
    };
    iterations as usize * per_iteration + 64
}

/// The untraced mode: the bare `exec::step` loop. No observation is constructed; what the
/// run established is readable only from the facts residue.
pub fn run_untraced(env: &mut impl Environment, budget: usize) -> RunFacts {
    let mut state = ArchitecturalState::zeroed_at(ENTRY);
    let mut census = Census::default();
    let mut steps = 0;
    let stop = loop {
        if steps >= budget {
            break Stop::Budget;
        }
        let pc = state.pc();
        let outcome = {
            let mut counted = Counting {
                inner: &mut *env,
                census: &mut census,
            };
            exec::step(&mut state, &mut counted)
        };
        match apply_outcome(&mut state, pc, &outcome) {
            Disposition::Observed => steps += 1,
            Disposition::StopAfterObservation(stop) => {
                steps += 1;
                break stop;
            }
            Disposition::StopSilent(stop) => break stop,
        }
    };
    RunFacts {
        steps,
        stop,
        regs: run::snapshot(&state),
        pc: state.pc(),
        census,
    }
}

/// The instrumented mode's sink: one callback per observed step. Static vs dynamic
/// dispatch is the measured question — the runner is generic over `O`, so
/// `run_instrumented::<VecObserver>` and `run_instrumented::<dyn Observer>` are the two
/// cells of the report that answer it.
pub trait Observer {
    /// Record one observed step (taken by value; constructing it is the instrumented
    /// cost being measured).
    fn observe(&mut self, step: Step);
}

/// The collecting observer: the full Step stream, for comparison and reporting.
#[derive(Default)]
pub struct VecObserver {
    /// The observed steps, in order.
    pub steps: Vec<Step>,
}

impl Observer for VecObserver {
    fn observe(&mut self, step: Step) {
        self.steps.push(step);
    }
}

/// The instrumented mode: the observation stream (pc, word, writes, trap) built with
/// `run`'s own snapshot/diff and trap mapping, delivered to the observer.
pub fn run_instrumented<O: Observer + ?Sized>(
    env: &mut impl Environment,
    image: &[u32],
    budget: usize,
    observer: &mut O,
) -> Result<RunFacts, HarnessError> {
    let mut state = ArchitecturalState::zeroed_at(ENTRY);
    let mut census = Census::default();
    let mut steps = 0;
    let stop = loop {
        if steps >= budget {
            break Stop::Budget;
        }
        let pc = state.pc();
        let before = run::snapshot(&state);
        let outcome = {
            let mut counted = Counting {
                inner: &mut *env,
                census: &mut census,
            };
            exec::step(&mut state, &mut counted)
        };
        match apply_outcome(&mut state, pc, &outcome) {
            Disposition::Observed => {
                observer.observe(Step {
                    pc,
                    word: Some(image_word(image, pc)?),
                    writes: run::diff(before, &state),
                    trap: match &outcome {
                        StepOutcome::Event(event) => Some(run::trap_pair(event)),
                        _ => None,
                    },
                });
                steps += 1;
            }
            Disposition::StopAfterObservation(stop) => {
                observer.observe(Step {
                    pc,
                    word: Some(image_word(image, pc)?),
                    writes: run::diff(before, &state),
                    trap: match &outcome {
                        StepOutcome::Event(event) => Some(run::trap_pair(event)),
                        _ => None,
                    },
                });
                steps += 1;
                break stop;
            }
            Disposition::StopSilent(stop) => break stop,
        }
    };
    Ok(RunFacts {
        steps,
        stop,
        regs: run::snapshot(&state),
        pc: state.pc(),
        census,
    })
}

/// The diagnostic mode: the instrumented stream plus the full boundary-crossing log
/// (`run`'s own `Recording` wrapper — the measured overhead is the production
/// recording's overhead).
pub fn run_diagnostic(
    env: &mut impl Environment,
    image: &[u32],
    budget: usize,
) -> Result<(RunFacts, Vec<Step>, Vec<Crossing>), HarnessError> {
    let mut state = ArchitecturalState::zeroed_at(ENTRY);
    let mut census = Census::default();
    let mut crossings: Vec<Crossing> = Vec::new();
    let mut stream: Vec<Step> = Vec::new();
    let mut steps = 0;
    let stop = loop {
        if steps >= budget {
            break Stop::Budget;
        }
        let pc = state.pc();
        let before = run::snapshot(&state);
        let outcome = {
            let mut counted = Counting {
                inner: &mut *env,
                census: &mut census,
            };
            let mut recorded = Recording {
                inner: &mut counted,
                log: &mut crossings,
            };
            exec::step(&mut state, &mut recorded)
        };
        match apply_outcome(&mut state, pc, &outcome) {
            Disposition::Observed => {
                stream.push(Step {
                    pc,
                    word: Some(image_word(image, pc)?),
                    writes: run::diff(before, &state),
                    trap: match &outcome {
                        StepOutcome::Event(event) => Some(run::trap_pair(event)),
                        _ => None,
                    },
                });
                steps += 1;
            }
            Disposition::StopAfterObservation(stop) => {
                stream.push(Step {
                    pc,
                    word: Some(image_word(image, pc)?),
                    writes: run::diff(before, &state),
                    trap: match &outcome {
                        StepOutcome::Event(event) => Some(run::trap_pair(event)),
                        _ => None,
                    },
                });
                steps += 1;
                break stop;
            }
            Disposition::StopSilent(stop) => break stop,
        }
    };
    Ok((
        RunFacts {
            steps,
            stop,
            regs: run::snapshot(&state),
            pc: state.pc(),
            census,
        },
        stream,
        crossings,
    ))
}

/// One of ARCHITECTURE §6's three modes, with the instrumented mode's two dispatch
/// variants measured as separate cells.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Mode {
    /// No observation constructed.
    Untraced,
    /// The Step stream through a statically dispatched observer.
    InstrumentedStatic,
    /// The Step stream through a `dyn Observer` — the static-vs-dynamic measurement.
    InstrumentedDyn,
    /// The Step stream plus the boundary-crossing log.
    Diagnostic,
}

impl Mode {
    /// Every measured cell, in report order.
    pub const ALL: [Mode; 4] = [
        Mode::Untraced,
        Mode::InstrumentedStatic,
        Mode::InstrumentedDyn,
        Mode::Diagnostic,
    ];

    /// The mode's report name.
    #[must_use]
    pub fn name(self) -> &'static str {
        match self {
            Mode::Untraced => "untraced",
            Mode::InstrumentedStatic => "instrumented",
            Mode::InstrumentedDyn => "instrumented (dyn)",
            Mode::Diagnostic => "diagnostic",
        }
    }

    /// Does this mode record the Step stream?
    #[must_use]
    pub fn records_steps(self) -> bool {
        !matches!(self, Mode::Untraced)
    }
}

/// Prepare a mix run: the guest image and a cold-reset environment with the image loaded
/// (OB-ENV-RESET: construction plus image load). Setup is deliberately outside the timed
/// section — the subject is per-step cost, not image loading.
#[must_use]
pub fn prepare(mix: Mix, iterations: u32) -> (FlatMemory, Vec<u32>) {
    let words = mix.program(iterations);
    let bytes: Vec<u8> = words.iter().flat_map(|word| word.to_le_bytes()).collect();
    let mut env = FlatMemory::new(ENTRY, REGION_SIZE);
    env.load_image(0, &bytes);
    (env, words)
}

/// Run one mode over a prepared environment/image. The dispatch variants of the
/// instrumented mode are literally the same generic function, instantiated statically and
/// dynamically — the measurement the open question asked for.
pub fn run_mode(
    mode: Mode,
    env: &mut FlatMemory,
    image: &[u32],
    budget: usize,
) -> Result<ModeRun, HarnessError> {
    match mode {
        Mode::Untraced => Ok(ModeRun {
            facts: run_untraced(env, budget),
            steps: None,
        }),
        Mode::InstrumentedStatic => {
            let mut observer = VecObserver::default();
            let facts = run_instrumented(env, image, budget, &mut observer)?;
            Ok(ModeRun {
                facts,
                steps: Some(observer.steps),
            })
        }
        Mode::InstrumentedDyn => {
            let mut observer = VecObserver::default();
            let dyn_observer: &mut dyn Observer = &mut observer;
            let facts = run_instrumented(env, image, budget, dyn_observer)?;
            Ok(ModeRun {
                facts,
                steps: Some(observer.steps),
            })
        }
        Mode::Diagnostic => {
            let (facts, stream, _crossings) = run_diagnostic(env, image, budget)?;
            Ok(ModeRun {
                facts,
                steps: Some(stream),
            })
        }
    }
}

/// The RUST-02 check, stated as data: two modes' runs must agree on every fact — step
/// count, stop, final state, pc, census — and, where both record streams, on every
/// observation. The first disagreement is named; agreement is never assumed.
pub fn agree(a: &ModeRun, b: &ModeRun, names: (&str, &str)) -> Result<(), String> {
    let (fa, fb) = (&a.facts, &b.facts);
    if fa.steps != fb.steps {
        return Err(format!(
            "{} ran {} steps, {} ran {}",
            names.0, fa.steps, names.1, fb.steps
        ));
    }
    if fa.stop != fb.stop {
        return Err(format!(
            "{} stopped '{:?}', {} stopped '{:?}'",
            names.0, fa.stop, names.1, fb.stop
        ));
    }
    if fa.regs != fb.regs {
        let reg = fa
            .regs
            .iter()
            .zip(fb.regs.iter())
            .position(|(x, y)| x != y)
            .expect("regs differ, so some register differs");
        return Err(format!(
            "x{reg}: {} holds {:#018x}, {} holds {:#018x}",
            names.0, fa.regs[reg], names.1, fb.regs[reg]
        ));
    }
    if fa.pc != fb.pc {
        return Err(format!(
            "pc: {} holds {:#018x}, {} holds {:#018x}",
            names.0, fa.pc, names.1, fb.pc
        ));
    }
    if fa.census != fb.census {
        return Err(format!(
            "census: {} counted {:?}, {} counted {:?}",
            names.0, fa.census, names.1, fb.census
        ));
    }
    if let (Some(sa), Some(sb)) = (&a.steps, &b.steps) {
        if sa != sb {
            let at = sa
                .iter()
                .zip(sb.iter())
                .position(|(x, y)| x != y)
                .map_or(sa.len().min(sb.len()), |i| i);
            return Err(format!(
                "observation streams of {} and {} first differ at step {at} ({}: {} steps, {}: {} steps)",
                names.0,
                names.1,
                names.0,
                sa.len(),
                names.1,
                sb.len()
            ));
        }
    }
    Ok(())
}

/// The noise summary of one cell's repeated wall-clock samples (nanoseconds per run).
/// This is RUST-04's deliverable: the spread a future regression threshold must be set
/// FROM. Nothing here is a threshold.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Stats {
    /// Fastest sample.
    pub min: u64,
    /// The middle sample (even counts take the lower of the two middles' mean).
    pub median: u64,
    /// The arithmetic mean.
    pub mean: u64,
    /// Slowest sample.
    pub max: u64,
    /// (max − min) / median, in parts per million — the noise spread.
    pub spread_ppm: u64,
}

/// Reduce samples to their noise summary. Empty input is a caller bug and refuses loudly.
#[must_use]
pub fn stats(samples: &[u64]) -> Stats {
    assert!(
        !samples.is_empty(),
        "stats of no samples is not a measurement"
    );
    let mut sorted = samples.to_vec();
    sorted.sort_unstable();
    let n = sorted.len();
    let min = sorted[0];
    let max = sorted[n - 1];
    let median = if n % 2 == 1 {
        sorted[n / 2]
    } else {
        (sorted[n / 2 - 1] + sorted[n / 2]) / 2
    };
    let mean = sorted.iter().map(|s| u128::from(*s)).sum::<u128>() / n as u128;
    let spread_ppm = if median == 0 {
        0
    } else {
        u64::try_from((u128::from(max - min) * 1_000_000) / u128::from(median))
            .expect("a spread beyond 4e15% is not a measurement")
    };
    Stats {
        min,
        median,
        mean: u64::try_from(mean).expect("a mean beyond 584 years of nanoseconds"),
        max,
        spread_ppm,
    }
}

/// Global allocation counting (RUST-03 as a number). The wrapper is std-only; the CLI
/// binary and this crate's test binary install it as their process allocator, the wasm
/// cdylib never links it as one. Overhead when unread is two relaxed atomic adds per
/// allocation, identical for every CLI command.
///
/// Two counter scopes: process-global (`counts`/`reset` — what the CLI's benchmark cells
/// measure) and thread-local (`thread_counts`/`thread_reset` — what the pinning suite
/// measures, because a test binary runs suites in parallel and only a per-thread counter
/// gives an EXACT count under concurrency). The bench CLI is single-threaded, so the two
/// scopes agree there by construction.
pub mod alloc {
    use std::alloc::{GlobalAlloc, Layout, System};
    use std::cell::Cell;
    use std::sync::atomic::{AtomicUsize, Ordering};

    /// The counting allocator: delegates to `System`, counting allocations and bytes.
    pub struct Counting;

    static ALLOCATIONS: AtomicUsize = AtomicUsize::new(0);
    static BYTES: AtomicUsize = AtomicUsize::new(0);

    thread_local! {
        static THREAD_ALLOCATIONS: Cell<usize> = const { Cell::new(0) };
        static THREAD_BYTES: Cell<usize> = const { Cell::new(0) };
    }

    unsafe impl GlobalAlloc for Counting {
        unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
            ALLOCATIONS.fetch_add(1, Ordering::Relaxed);
            BYTES.fetch_add(layout.size(), Ordering::Relaxed);
            THREAD_ALLOCATIONS.with(|c| c.set(c.get() + 1));
            THREAD_BYTES.with(|c| c.set(c.get() + layout.size()));
            // SAFETY: delegates to the system allocator with the caller's layout.
            unsafe { System.alloc(layout) }
        }

        unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
            // SAFETY: delegates to the system allocator with the caller's pointer/layout.
            unsafe { System.dealloc(ptr, layout) }
        }
    }

    /// Zero the process-global counters (call between setup and the measured section).
    pub fn reset() {
        ALLOCATIONS.store(0, Ordering::Relaxed);
        BYTES.store(0, Ordering::Relaxed);
    }

    /// `(allocations, bytes)` process-wide since the last reset.
    #[must_use]
    pub fn counts() -> (usize, usize) {
        (
            ALLOCATIONS.load(Ordering::Relaxed),
            BYTES.load(Ordering::Relaxed),
        )
    }

    /// Zero the calling thread's counters.
    pub fn thread_reset() {
        THREAD_ALLOCATIONS.with(|c| c.set(0));
        THREAD_BYTES.with(|c| c.set(0));
    }

    /// `(allocations, bytes)` on the calling thread since the last `thread_reset` — exact
    /// under test-binary parallelism, which is what the pinning suite needs.
    #[must_use]
    pub fn thread_counts() -> (usize, usize) {
        (
            THREAD_ALLOCATIONS.with(Cell::get),
            THREAD_BYTES.with(Cell::get),
        )
    }
}

#[cfg(test)]
mod tests;
