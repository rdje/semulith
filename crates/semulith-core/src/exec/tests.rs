//! Tests for the definitional interpreter. Every expectation here is derived from the pinned
//! specification rules the outcomes name (see the module docs), not from any model's output;
//! the tracked guests carry the same expectations as data on the verify side, and the
//! live reference comparison is the experiment, not the commit gate.

use super::*;
use crate::definition::INSNS;
use crate::env::ContractViolation;

const ENTRY: u64 = 0x1000;

/// A small scripted environment: one little-endian region, fault-injection flags, and a
/// request log a test can assert on (e.g. that a misaligned load never crossed the boundary).
struct TestEnv {
    base: u64,
    mem: Vec<u8>,
    fetch_fault: bool,
    access_fault: bool,
    violate: bool,
    requests: Vec<Request>,
}

impl TestEnv {
    fn new(base: u64, size: usize) -> Self {
        Self {
            base,
            mem: vec![0; size],
            fetch_fault: false,
            access_fault: false,
            violate: false,
            requests: Vec::new(),
        }
    }

    fn load(&mut self, offset: usize, image: &[u8]) {
        self.mem[offset..offset + image.len()].copy_from_slice(image);
    }

    fn contains(&self, addr: u64, width: AccessWidth) -> bool {
        let start = u128::from(addr);
        let end = start + u128::from(width.bytes());
        start >= u128::from(self.base) && end <= u128::from(self.base) + self.mem.len() as u128
    }

    fn read(&self, addr: u64, width: AccessWidth) -> u64 {
        let off = (addr - self.base) as usize;
        let mut value = 0u64;
        for (i, byte) in self.mem[off..off + width.bytes() as usize]
            .iter()
            .enumerate()
        {
            value |= u64::from(*byte) << (8 * i);
        }
        value
    }
}

impl Environment for TestEnv {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        self.requests.push(request);
        if self.violate {
            return Err(BoundaryError::Violation(ContractViolation::ScriptExhausted));
        }
        match request {
            Request::Fetch { addr } => {
                if self.fetch_fault {
                    return Err(Failure::AccessFault.into());
                }
                Ok(Response::Fetch(self.read(addr, AccessWidth::W) as u32))
            }
            Request::Load { width, addr } => {
                if addr % width.bytes() != 0 {
                    return Err(Failure::Misaligned.into());
                }
                if self.access_fault || !self.contains(addr, width) {
                    return Err(Failure::AccessFault.into());
                }
                Ok(Response::Load(self.read(addr, width)))
            }
            Request::Store { width, addr, data } => {
                if addr % width.bytes() != 0 {
                    return Err(Failure::Misaligned.into());
                }
                if self.access_fault || !self.contains(addr, width) {
                    return Err(Failure::AccessFault.into());
                }
                let off = (addr - self.base) as usize;
                for (i, byte) in data.to_le_bytes()[..width.bytes() as usize]
                    .iter()
                    .enumerate()
                {
                    self.mem[off + i] = *byte;
                }
                Ok(Response::StoreDone)
            }
        }
    }
}

/// Encode one instruction from operand-level arguments, the test-side mirror of the
/// assembler: fixed bits from the instruction's own decode row, operands placed per the
/// field table, composed immediates (`imm12` on an S-type, `bimm12`, `shamt`) scattered
/// per the piece tables the same way `exec`'s extractor unscrambles them.
fn enc(name: &str, args: &[(&str, u64)]) -> u32 {
    let insn = INSNS
        .iter()
        .find(|i| i.name == name)
        .unwrap_or_else(|| panic!("{name}"));
    let field = |n: &str| -> &FieldDef {
        FIELDS
            .iter()
            .find(|f| f.name == n)
            .unwrap_or_else(|| panic!("field {n}"))
    };
    let place = |word: u32, f: &FieldDef, value: u64| -> u32 {
        let width = u32::from(f.hi - f.lo + 1);
        let mask = if width >= 32 {
            u64::from(u32::MAX)
        } else {
            (1u64 << width) - 1
        };
        let mask = (mask as u32) << f.lo;
        (word & !mask) | (((value as u32) << f.lo) & mask)
    };
    // Scatter a composed immediate through one field's piece table, MSB-first.
    let scatter = |word: u32, f: &FieldDef, value: u64| -> u32 {
        let mut word = word;
        let mut done = 0u32;
        for &(imm_hi, imm_lo) in f.scatter {
            let w = u32::from(imm_hi - imm_lo + 1);
            let bits = ((value >> imm_lo) & mask_u64(w)) as u32;
            let sub_hi = u32::from(f.hi) - done;
            let sub_lo = sub_hi - w + 1;
            let mask = (1u32 << w) - 1;
            word &= !(mask << sub_lo);
            word |= (bits & mask) << sub_lo;
            done += w;
        }
        word
    };
    let mut word = insn.value;
    for &(arg, value) in args {
        match arg {
            "imm12" => {
                if insn.operands.contains(&"imm12hi") {
                    // S-type: the immediate is split across imm12hi/imm12lo.
                    word = place(word, field("imm12hi"), value >> 5);
                    word = place(word, field("imm12lo"), value & 0x1f);
                } else {
                    // I-type: one contiguous field.
                    word = place(word, field("imm12"), value);
                }
            }
            "bimm12" => {
                word = scatter(word, field("bimm12hi"), value);
                word = scatter(word, field("bimm12lo"), value);
            }
            "jimm20" => word = scatter(word, field("jimm20"), value),
            "shamt" => {
                let fname = if insn.operands.contains(&"shamtd") {
                    "shamtd"
                } else {
                    "shamtw"
                };
                word = place(word, field(fname), value);
            }
            _ => {
                if FIELDS.iter().any(|f| f.name == arg) {
                    word = place(word, field(arg), value);
                } else {
                    // The generator refuses an operand that names no field; a test that
                    // builds a word for one must fail loudly, not emit a wrong word.
                    panic!("{arg} names no field — the generator refuses such a table");
                }
            }
        }
    }
    word
}

fn setup(words: &[u32]) -> (ArchitecturalState, TestEnv) {
    let mut env = TestEnv::new(ENTRY, 0x1000);
    let mut image = Vec::with_capacity(words.len() * 4);
    for word in words {
        image.extend_from_slice(&word.to_le_bytes());
    }
    env.load(0, &image);
    (ArchitecturalState::zeroed_at(ENTRY), env)
}

#[test]
fn addi_writes_and_advances() {
    let (mut state, mut env) = setup(&[enc("addi", &[("rd", 1), ("rs1", 0), ("imm12", 5)])]);
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Advanced(Advance::Completed)
    );
    assert_eq!(state.read_x(1), 5);
    assert_eq!(state.pc(), ENTRY + 4);
}

#[test]
fn lui_sign_extends_the_shifted_value_from_bit_31() {
    // D-LUI-AUIPC: the 32-bit value 0x80000000 sign-extends to 0xFFFFFFFF80000000. This is the
    // width-algebra case: sext extends from the shl's width (32), not from 64.
    let (mut state, mut env) = setup(&[enc("lui", &[("rd", 1), ("imm20", 0x80000)])]);
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Advanced(Advance::Completed)
    );
    assert_eq!(state.read_x(1), 0xFFFF_FFFF_8000_0000);
}

#[test]
fn auipc_adds_the_offset_to_its_own_address() {
    let (mut state, mut env) = setup(&[enc("auipc", &[("rd", 1), ("imm20", 0)])]);
    step(&mut state, &mut env);
    assert_eq!(state.read_x(1), ENTRY);
}

#[test]
fn jal_links_pc_plus_4_and_transfers() {
    let (mut state, mut env) = setup(&[enc("jal", &[("rd", 5), ("jimm20", 8)])]);
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Advanced(Advance::Completed)
    );
    assert_eq!(state.read_x(5), ENTRY + 4);
    assert_eq!(state.pc(), ENTRY + 8);
}

#[test]
fn jalr_clears_the_target_lsb() {
    // D-JALR-LSB: x1 + imm is odd; the target lands with the low bit cleared.
    let words = [
        enc("lui", &[("rd", 1), ("imm20", 0x1)]), // x1 = 0x1000
        enc("addi", &[("rd", 1), ("rs1", 1), ("imm12", 4)]), // x1 = ENTRY + 4
        enc("jalr", &[("rd", 10), ("rs1", 1), ("imm12", 0x105)]), // (ENTRY+0x109) & !1
    ];
    let (mut state, mut env) = setup(&words);
    step(&mut state, &mut env);
    step(&mut state, &mut env);
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Advanced(Advance::Completed)
    );
    assert_eq!(state.read_x(10), ENTRY + 12); // pc+4 of the jalr
    assert_eq!(state.pc(), ENTRY + 0x108);
}

#[test]
fn misaligned_taken_target_raises_on_the_jump() {
    // REQ-D-IALIGN / REQ-D-MISALIGN-REPORT: a taken transfer to a 2-byte-aligned target
    // raises InstructionAddressMisaligned ON the jump, at the target value, and the pc
    // stays at the jump.
    let (mut state, mut env) = setup(&[enc("jal", &[("rd", 0), ("jimm20", 2)])]);
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Event(TargetEvent::Exception {
            cause: ExceptionCause::InstructionAddressMisaligned,
            at: ENTRY + 2,
        })
    );
    assert_eq!(state.pc(), ENTRY);
}

#[test]
fn branch_taken_writes_nothing() {
    // 0x1ffc is -4 as a 13-bit two's-complement bimm12: the branch at ENTRY+4 loops back
    // to the addi at ENTRY.
    let words = [
        enc("addi", &[("rd", 1), ("rs1", 0), ("imm12", 1)]),
        enc("bne", &[("bimm12", 0x1ffc), ("rs1", 1), ("rs2", 0)]),
    ];
    let (mut state, mut env) = setup(&words);
    step(&mut state, &mut env);
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Advanced(Advance::Completed)
    );
    assert_eq!(state.read_x(1), 1);
    assert_eq!(state.pc(), ENTRY); // looped back
}

#[test]
fn misaligned_load_raises_before_crossing_the_boundary() {
    // D-MISALIGN-DATA: the misalignment is the instruction layer's rule; the request log
    // proves the environment never saw the access. Addresses are absolute: x1 = 4, so the
    // effective address is 4 + 2 = 6.
    let words = [
        enc("addi", &[("rd", 1), ("rs1", 0), ("imm12", 4)]),
        enc("lw", &[("rd", 2), ("rs1", 1), ("imm12", 2)]),
    ];
    let (mut state, mut env) = setup(&words);
    step(&mut state, &mut env);
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Event(TargetEvent::Exception {
            cause: ExceptionCause::LoadAddressMisaligned,
            at: 6,
        })
    );
    assert!(!env
        .requests
        .iter()
        .any(|r| matches!(r, Request::Load { .. })));
}

#[test]
fn loads_extend_per_d_load_ext() {
    // D-LOAD-EXT: LB sign-extends, LBU zero-extends. The byte sits at ENTRY+0x100; x1 is
    // built to that absolute address.
    let mut env = TestEnv::new(ENTRY, 0x1000);
    env.load(0x100, &[0x80]);
    let mut image = Vec::new();
    for word in [
        enc("lui", &[("rd", 1), ("imm20", 0x1)]), // x1 = ENTRY
        enc("lb", &[("rd", 2), ("rs1", 1), ("imm12", 0x100)]),
        enc("lbu", &[("rd", 3), ("rs1", 1), ("imm12", 0x100)]),
    ] {
        image.extend_from_slice(&word.to_le_bytes());
    }
    env.load(0, &image);
    let mut state = ArchitecturalState::zeroed_at(ENTRY);
    step(&mut state, &mut env);
    step(&mut state, &mut env);
    assert_eq!(state.read_x(2), 0xFFFF_FFFF_FFFF_FF80);
    step(&mut state, &mut env);
    assert_eq!(state.read_x(3), 0x80);
}

#[test]
fn store_writes_the_low_bits_and_advances() {
    // x1 = ENTRY; the store lands at ENTRY + 0x80, inside the region.
    let words = [
        enc("lui", &[("rd", 1), ("imm20", 0x1)]),
        enc("addi", &[("rd", 2), ("rs1", 0), ("imm12", 0x55)]),
        enc("sb", &[("imm12", 0x80), ("rs1", 1), ("rs2", 2)]),
    ];
    let (mut state, mut env) = setup(&words);
    step(&mut state, &mut env);
    step(&mut state, &mut env);
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Advanced(Advance::Completed)
    );
    assert_eq!(env.read(ENTRY + 0x80, AccessWidth::B), 0x55);
    assert_eq!(state.pc(), ENTRY + 12);
}

#[test]
fn fetch_access_fault_is_reported_at_the_pc() {
    // REQ-D-FETCH-FAULT-REPORT: the fault is reported on the faulting fetch itself.
    let (mut state, mut env) = setup(&[enc("addi", &[("rd", 1), ("rs1", 0), ("imm12", 1)])]);
    env.fetch_fault = true;
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Event(TargetEvent::Exception {
            cause: ExceptionCause::InstructionAccessFault,
            at: ENTRY,
        })
    );
}

#[test]
fn load_access_fault_is_the_boundary_answer_converted() {
    // x1 = 4, so the effective address is 4 — the fault is reported at that address.
    let words = [
        enc("addi", &[("rd", 1), ("rs1", 0), ("imm12", 4)]),
        enc("lw", &[("rd", 2), ("rs1", 1), ("imm12", 0)]),
    ];
    let (mut state, mut env) = setup(&words);
    step(&mut state, &mut env);
    env.access_fault = true;
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Event(TargetEvent::Exception {
            cause: ExceptionCause::LoadAccessFault,
            at: 4,
        })
    );
}

#[test]
fn store_access_fault_is_reported_at_the_address() {
    let words = [enc("sw", &[("imm12", 0), ("rs1", 0), ("rs2", 0)])];
    let (mut state, mut env) = setup(&words);
    env.access_fault = true;
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Event(TargetEvent::Exception {
            cause: ExceptionCause::StoreAccessFault,
            at: 0,
        })
    );
}

#[test]
fn reserved_decode_is_undefined_never_a_trap() {
    // D-RESERVED-DECODE: the all-zero word matches no decode row; the model reports the
    // source-classified UNSPECIFIED case rather than inventing an illegal-instruction trap.
    let (mut state, mut env) = setup(&[0]);
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Undefined(UndefinedCase::ReservedDecode { at: ENTRY })
    );
    assert_eq!(state.pc(), ENTRY);
}

#[test]
fn ecall_is_a_requested_trap_with_cause_11() {
    let (mut state, mut env) = setup(&[enc("ecall", &[])]);
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Event(TargetEvent::RequestedTrap {
            kind: RequestedTrapKind::EnvironmentCall,
            at: 0,
        })
    );
    assert_eq!(state.pc(), ENTRY); // a requested trap does not advance the pc
}

#[test]
fn ebreak_is_a_requested_trap_at_the_pc() {
    let (mut state, mut env) = setup(&[enc("ebreak", &[])]);
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Event(TargetEvent::RequestedTrap {
            kind: RequestedTrapKind::Breakpoint,
            at: ENTRY,
        })
    );
}

#[test]
fn x0_discards_the_write_but_the_instruction_completes() {
    let (mut state, mut env) = setup(&[enc("addi", &[("rd", 0), ("rs1", 0), ("imm12", 5)])]);
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Advanced(Advance::Completed)
    );
    assert_eq!(state.read_x(0), 0);
}

#[test]
fn fence_decodes_and_does_nothing() {
    // D-FENCE: decoded, must not trap, no observable effect in this profile.
    let (mut state, mut env) = setup(&[enc(
        "fence",
        &[("fm", 0), ("pred", 3), ("succ", 3), ("rs1", 0), ("rd", 0)],
    )]);
    assert_eq!(
        step(&mut state, &mut env),
        StepOutcome::Advanced(Advance::Completed)
    );
    assert_eq!(state.pc(), ENTRY + 4);
}

#[test]
fn w_family_operates_on_the_low_32_bits() {
    // D-WSUFFIX / D-SHAMT: the *W instructions ignore the upper 32 bits, operate at 32
    // bits, and sign-extend the 32-bit result. x1 = 0xFFFFFFFF80000000: the low half
    // 0x80000000 carries bit 31 set, which is where the sign extension bites.
    let words = [
        enc("lui", &[("rd", 1), ("imm20", 0x80000)]), // x1 = 0xFFFFFFFF80000000
        enc("addiw", &[("rd", 2), ("rs1", 1), ("imm12", 1)]), // 0x80000001 -> sext
        enc("srliw", &[("rd", 3), ("rs1", 1), ("shamt", 4)]), // logical: 0x08000000
        enc("sraiw", &[("rd", 4), ("rs1", 1), ("shamt", 4)]), // arithmetic: 0xF8000000 -> sext
    ];
    let (mut state, mut env) = setup(&words);
    step(&mut state, &mut env);
    step(&mut state, &mut env);
    assert_eq!(state.read_x(2), 0xFFFF_FFFF_8000_0001);
    step(&mut state, &mut env);
    assert_eq!(state.read_x(3), 0x0800_0000);
    step(&mut state, &mut env);
    assert_eq!(state.read_x(4), 0xFFFF_FFFF_F800_0000);
}

#[test]
fn shift_operations_use_the_low_6_bits_of_rs2() {
    // D-SHAMT: register shifts mask the amount to 6 bits at XLEN=64.
    let words = [
        enc("addi", &[("rd", 1), ("rs1", 0), ("imm12", 1)]), // x1 = 1
        enc("slli", &[("rd", 1), ("rs1", 1), ("shamt", 40)]), // x1 = 1 << 40
        enc("addi", &[("rd", 2), ("rs1", 0), ("imm12", 65)]), // x2 = 65
        enc("sll", &[("rd", 3), ("rs1", 1), ("rs2", 2)]),    // 1<<40 << (65 & 63 = 1)
    ];
    let (mut state, mut env) = setup(&words);
    step(&mut state, &mut env);
    step(&mut state, &mut env);
    step(&mut state, &mut env);
    step(&mut state, &mut env);
    assert_eq!(state.read_x(3), 1u64 << 41);
}

#[test]
fn a_load_to_x0_still_raises_its_exceptions() {
    // D-LOAD-X0: rd = x0 discards the value, not the exceptions.
    let words = [
        enc("addi", &[("rd", 1), ("rs1", 0), ("imm12", 4)]),
        enc("lw", &[("rd", 0), ("rs1", 1), ("imm12", 2)]),
    ];
    let (mut state, mut env) = setup(&words);
    step(&mut state, &mut env);
    assert!(matches!(
        step(&mut state, &mut env),
        StepOutcome::Event(TargetEvent::Exception {
            cause: ExceptionCause::LoadAddressMisaligned,
            ..
        })
    ));
}

#[test]
fn environment_contract_violation_is_a_model_error_not_a_trap() {
    // SEM-01/SEM-02: a harness contract violation is ModelError, never a target exception.
    let (mut state, mut env) = setup(&[enc("addi", &[("rd", 1), ("rs1", 0), ("imm12", 1)])]);
    env.violate = true;
    assert!(matches!(
        step(&mut state, &mut env),
        StepOutcome::Failed(ModelError::ContractViolation(_))
    ));
}

#[test]
fn stored_code_is_visible_to_a_later_fetch() {
    // D-CODE-VISIBILITY: the model re-reads memory for every fetch, so a store that
    // overwrites a later instruction changes what executes. The program materializes the
    // encoding of `addi x3, x0, 7`, stores it over the fourth slot, and jumps there.
    let addi_x3_x0_7: u64 = 0x0070_0193;
    let words = [
        enc("lui", &[("rd", 1), ("imm20", 0x00700)]), // x1 = 0x00700000
        enc(
            "addi",
            &[("rd", 1), ("rs1", 1), ("imm12", addi_x3_x0_7 & 0xfff)],
        ), // x1 = the word
        enc("lui", &[("rd", 2), ("imm20", 0x1)]),     // x2 = ENTRY
        enc("sw", &[("imm12", 0x0c), ("rs1", 2), ("rs2", 1)]), // mem[ENTRY+0x0c] = the word
        enc("jalr", &[("rd", 0), ("rs1", 2), ("imm12", 0x0c)]), // to ENTRY+0x0c
        0u32, // replaced by the store before it is ever fetched
    ];
    let (mut state, mut env) = setup(&words);
    for _ in 0..6 {
        assert_eq!(
            step(&mut state, &mut env),
            StepOutcome::Advanced(Advance::Completed)
        );
    }
    assert_eq!(state.read_x(3), 7);
    assert_eq!(state.pc(), ENTRY + 0x10);
}

#[test]
fn step_over_the_generated_table_resolves_exactly_what_decode_resolves() {
    // P1-LAB.9's seam: the table scan inside `step_over` must BE the production definition —
    // over every row's canonical word, operand-varied encodings, and words no row claims, it
    // resolves the identical instruction `definition::decode` (the same documented predicate,
    // `word & mask == value`) resolves.
    let mut probes: Vec<u32> = INSNS.iter().map(|insn| insn.value).collect();
    probes.extend([
        enc("addi", &[("rd", 1), ("rs1", 0), ("imm12", 1)]),
        enc("addi", &[("rd", 31), ("rs1", 31), ("imm12", 0xFFF)]),
        enc("srli", &[("rd", 1), ("rs1", 1), ("shamtd", 1)]),
        enc("srai", &[("rd", 1), ("rs1", 1), ("shamtd", 1)]),
        enc("jalr", &[("rd", 10), ("rs1", 9), ("imm12", 13)]),
        enc("ebreak", &[]),
        0x0000_0000, // reserved: no row claims it
        0xFFFF_FFFF, // reserved: no row claims it
    ]);
    for word in probes {
        let scan = INSNS
            .iter()
            .find(|insn| word & insn.mask == insn.value)
            .map(|insn| insn.name);
        assert_eq!(
            scan,
            crate::definition::decode(word).map(|insn| insn.name),
            "word {word:#010x}: the step_over scan and the generated decode disagree"
        );
    }
}
