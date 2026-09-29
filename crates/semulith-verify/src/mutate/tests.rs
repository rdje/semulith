//! The validator mutation suite's arms — one per designated wrong behaviour (`RULES.md` EVD-09,
//! `docs/EVIDENCE_AND_GATES.md`'s enumeration), plus the data-crossing census the
//! extra-access arm instruments against and the comparison-suppression exhibit. Every arm
//! names its injection level (model-level through `step_over`, or observation-level where a
//! faithful model-level seam would be a second implementation — see the module docs) and its
//! detection instrument, and asserts the divergence at the designated step, naming the
//! designated field. Every guest arm first re-derives the pinned GUEST-GEN expectations
//! against the real model: the anchor cannot drift silently.

use super::*;
use crate::fixtures::FlatMemory;
use crate::guests::{Guest, GUESTS};
use crate::run::{
    compare, render, run, run_over, Crossing, Divergence, Step, Stop, Trace, Verdict,
};
use semulith_core::definition::{decode, FieldDef, InsnDef, FIELDS, INSNS};
use semulith_core::env::{AccessWidth, BoundaryError, Request};
use semulith_core::outcome::UndefinedCase;

const ENTRY: u64 = 0x8000_0000;

fn flat(words: &[u32]) -> FlatMemory {
    let mut env = FlatMemory::new(ENTRY, 0x10000);
    let mut image = Vec::with_capacity(words.len() * 4);
    for word in words {
        image.extend_from_slice(&word.to_le_bytes());
    }
    env.load_image(0, &image);
    env
}

fn find_guest(name: &str) -> &'static Guest {
    GUESTS
        .iter()
        .find(|g| g.name == name)
        .unwrap_or_else(|| panic!("guest {name} is in the generated fixture"))
}

/// The suite-local word encoder (the exec-test `enc` pattern): every word is built from the
/// definition's rows, then anchored — the real decoder must claim it decodes to the intended
/// instruction, so no arm ever runs a word its claim does not cover.
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
            let bits =
                ((value >> imm_lo) & if w >= 64 { u64::MAX } else { (1u64 << w) - 1 }) as u32;
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
                }
                // FENCE's fm/pred/succ carry no field ranges; the encoding takes them
                // from the fixed bits alone, so there is nothing to place.
            }
        }
    }
    assert_eq!(
        decode(word).map(|insn| insn.name),
        Some(name),
        "the suite only runs words the real decoder claims"
    );
    word
}

/// GREEN anchor: run a tracked guest under the real model and re-derive the pinned
/// specification-derived expectations (the same checks as the run suites' guest tests —
/// this copy keeps every arm self-contained).
fn assert_meets_pinned_expectations(name: &str, want_stop: Stop) -> (Trace, Vec<Crossing>) {
    let guest = find_guest(name);
    let mut env = flat(guest.words);
    let (trace, crossings) = run(&mut env, guest.entry, guest.executed_steps);
    assert_eq!(
        trace.steps.len(),
        guest.executed_steps,
        "{name}: the trace runs exactly the declared step count"
    );
    assert_eq!(trace.stop, want_stop, "{name}: stop reason");
    for (i, expected) in guest.expected.iter().enumerate() {
        assert_eq!(
            expected.step, i,
            "{name}: the fixture's expectations are in step order"
        );
        assert_eq!(
            trace.steps[i].writes, expected.writes,
            "{name}: step {i} writes match the specification-derived expectations"
        );
    }
    let mut written: Vec<u8> = trace
        .steps
        .iter()
        .flat_map(|s| s.writes.iter().map(|(r, _)| *r))
        .collect();
    written.sort_unstable();
    for reg in guest.never_written {
        assert!(
            !written.contains(reg),
            "{name}: x{reg} must never be written"
        );
    }
    let fetches = crossings
        .iter()
        .filter(|c| matches!(c.request, Request::Fetch { .. }))
        .count();
    assert_eq!(
        fetches, guest.executed_steps,
        "{name}: exactly one fetch per executed step (no extraneous fetch)"
    );
    (trace, crossings)
}

fn run_real(words: &[u32], budget: usize) -> (Trace, Vec<Crossing>) {
    let mut env = flat(words);
    run(&mut env, ENTRY, budget)
}

fn run_under(words: &[u32], budget: usize, table: &[InsnDef]) -> (Trace, Vec<Crossing>) {
    let mut env = flat(words);
    run_over(&mut env, ENTRY, budget, table)
}

fn divergence(a: &[Step], b: &[Step], names: (&str, &str)) -> Divergence {
    let verdict = compare(a, b, names).unwrap_or_else(|e| panic!("comparison refused: {e:?}"));
    match verdict {
        Verdict::Divergence(d) => d,
        other => panic!(
            "expected a divergence, got {}",
            render(&other, a.len(), b.len(), names)
        ),
    }
}

fn must_agree(a: &[Step], b: &[Step], names: (&str, &str)) {
    let verdict = compare(a, b, names).unwrap_or_else(|e| panic!("comparison refused: {e:?}"));
    match verdict {
        Verdict::Agree { .. } => {}
        other => panic!(
            "expected agreement, got {}",
            render(&other, a.len(), b.len(), names)
        ),
    }
}

/// Partition the crossing log by the one-fetch-per-step invariant (a fetch opens its step's
/// group) and return the data crossings — every non-fetch request — tagged with the index
/// of the executing step.
fn data_crossings_by_step(crossings: &[Crossing]) -> Vec<(usize, Crossing)> {
    let mut out = Vec::new();
    let mut step = 0usize;
    for crossing in crossings {
        if matches!(crossing.request, Request::Fetch { .. }) {
            step += 1;
        } else {
            out.push((step - 1, *crossing));
        }
    }
    out
}

// ---- the instrument itself: the census pin -----------------------------------------------------

#[test]
fn the_data_crossing_census_pins_every_tracked_guest() {
    // The extra-access arm detects through this census; the census itself is pinned here so
    // the instrument cannot drift silently either. The table itself lives with the suite's
    // public surface (`super::pinned_census`) — this test pins its CONTENT against the runs.
    let want_stop = |name: &str| match name {
        "smoke-trap" | "guest-no-device" | "scope-ecall" | "scope-ebreak" => Stop::Trap,
        // The P2-SCALAR.3 fault guests: a contained trap ends most; the fetch fault keeps
        // its own stop reason, the two reserved guests keep their source classification,
        // and the four suppressed-effect/nop guests retire into the budget.
        "fault-fetch" => Stop::FetchFault { at: 0x4000_0000 },
        "fault-reserved" | "fault-shiftw-res" => {
            Stop::Undefined(UndefinedCase::ReservedDecode { at: 0x8000_0004 })
        }
        "fault-branch-nt" | "fault-fence" | "fault-hints" | "fault-selfmod" => Stop::Budget,
        n if n.starts_with("fault-") => Stop::Trap,
        _ => Stop::Budget,
    };
    for guest in GUESTS {
        let (_, crossings) = assert_meets_pinned_expectations(guest.name, want_stop(guest.name));
        let data = data_crossings_by_step(&crossings);
        let pinned = pinned_census(guest.name);
        assert_eq!(
            data.len(),
            pinned.len(),
            "{}: the real run's data crossings are exactly the pinned census",
            guest.name
        );
        for ((step, crossing), (want_step, want_request, want_fault)) in data.iter().zip(pinned) {
            assert_eq!(step, want_step, "{}: crossing at its step", guest.name);
            assert_eq!(
                &crossing.request, want_request,
                "{}: the crossing the source declares",
                guest.name
            );
            let faulted = matches!(crossing.response, Err(BoundaryError::Target(_)));
            assert_eq!(faulted, *want_fault, "{}: the answer's class", guest.name);
        }
    }
}

// ---- designated class: wrong sign extension ----------------------------------------------------

#[test]
fn wrong_sign_extension_is_detected() {
    // Injection (model-level): "the immediate is sign-extended" (RVI-RV32I §1.1.4) read as
    // zero-extended — every `(sext 64 …)` in addi's tree becomes `(zext 64 …)`. Detection:
    // the first-divergence comparator against the pinned guest-control expectations.
    let (reference, _) = assert_meets_pinned_expectations("guest-control", Stop::Budget);
    let table = table_with_effect("addi", sext_to_zext);
    let guest = find_guest("guest-control");
    let (mutant, _) = run_under(guest.words, guest.executed_steps, &table);
    // `addi x1, x1, -1` at step 1: 3 + 0xFFF = 0x1002 under the mutant, not 2.
    let d = divergence(
        &reference.steps,
        &mutant.steps,
        ("reference", "zext-mutant"),
    );
    assert_eq!(
        d.at, 1,
        "the negative immediate is where sign-extension bites"
    );
    assert!(d.what.contains("x1"), "names the register: {}", d.what);
}

#[test]
fn unjustified_comparison_suppression_would_hide_a_designated_mutant() {
    // EVD-09's second half: detection of unjustified comparison suppression. Exhibit: a
    // comparator blind to the register-write leg. The instance is the sign-extension mutant
    // on a straight-line program — the written value is the ONLY differing observation — so
    // the blind comparator's agreement IS the suppression demonstrated, next to the real
    // comparator's divergence on the same streams.
    let words = [enc("addi", &[("rd", 1), ("rs1", 0), ("imm12", 0xFFF)])];
    let (reference, _) = run_real(&words, 1);
    assert_eq!(
        reference.steps[0].writes,
        vec![(1, 0xFFFF_FFFF_FFFF_FFFF)],
        "GREEN: -1 sign-extends to all ones"
    );
    let table = table_with_effect("addi", sext_to_zext);
    let (mutant, _) = run_under(&words, 1, &table);
    assert_eq!(
        mutant.steps[0].writes,
        vec![(1, 0x0000_0000_0000_0FFF)],
        "the mutant zero-extends: the write is the only differing observation"
    );
    let d = divergence(
        &reference.steps,
        &mutant.steps,
        ("reference", "zext-mutant"),
    );
    assert_eq!(d.at, 0);
    assert!(
        d.what.contains("x1"),
        "the real comparator names the register: {}",
        d.what
    );
    assert!(
        agree_except_writes(&reference.steps, &mutant.steps),
        "suppression demonstrated: the writes-blind comparator cannot see the designated mutant"
    );
}

/// The unjustified-suppression exhibit: equality on every observation leg EXCEPT the
/// register writes — the comparison-weakening mutation the arm above proves is hiding.
fn agree_except_writes(a: &[Step], b: &[Step]) -> bool {
    a.len() == b.len()
        && a.iter()
            .zip(b)
            .all(|(x, y)| x.pc == y.pc && x.word == y.word && x.trap == y.trap)
}

// ---- designated class: suppressed register write -----------------------------------------------

#[test]
fn suppressed_register_write_is_detected() {
    // Injection (model-level): jal's link write dropped — the `(seq …)` keeps only its
    // `set-pc`, so the jump transfers but writes nothing. guest-control's step 7 is due
    // x5 = pc+4 (RVI-RV32I §1.1.5.1).
    let (reference, _) = assert_meets_pinned_expectations("guest-control", Stop::Budget);
    let table = table_with_effect("jal", |sem| match sem {
        Sem::Seq(steps)
            if steps.len() == 2
                && matches!(steps[0], Sem::SetPc(..))
                && matches!(steps[1], Sem::Set(..)) =>
        {
            Some(rebuild(steps[0], &|_| None)) // the transfer, without the link write
        }
        _ => None,
    });
    let guest = find_guest("guest-control");
    let (mutant, _) = run_under(guest.words, guest.executed_steps, &table);
    let d = divergence(
        &reference.steps,
        &mutant.steps,
        ("reference", "write-suppressing mutant"),
    );
    assert_eq!(d.at, 7, "jal's step is where the link write is due");
    assert!(
        d.what.contains("x5"),
        "names the unwritten register: {}",
        d.what
    );
}

// ---- the arm the fixture names: JALR keeping its odd bit ----------------------------------------

#[test]
fn jalr_keeping_its_odd_bit_is_detected() {
    // Injection (model-level): the `(and … (lit -2))` LSB-clear in jalr's set-pc target is
    // dropped — the model keeps the odd target. This is the arm `guest-control.expected.sexp`'s
    // step-10 limit note names: both references clear the bit, so no live experiment can ever
    // observe the failing branch; only a mutation of OUR model can (D-JALR-LSB, RVI-RV32I
    // §1.1.5.1).
    let (reference, _) = assert_meets_pinned_expectations("guest-control", Stop::Budget);
    let table = table_with_effect("jalr", |sem| match sem {
        Sem::And(a, b) if matches!(&**b, Sem::Lit(v) if *v == (-2i64) as u64) => {
            Some(rebuild(a, &|_| None))
        }
        _ => None,
    });
    let guest = find_guest("guest-control");
    let (mutant, _) = run_under(guest.words, guest.executed_steps, &table);
    // The note's prediction: x9 + 13 = 0x80000029, kept odd, faults AT the target value.
    assert_eq!(mutant.stop, Stop::Trap, "the kept-odd-bit model faults");
    assert_eq!(
        mutant.steps[10].trap,
        Some((0x00, 0x8000_0029)),
        "InstructionAddressMisaligned raised on the jump, at the odd target"
    );
    let d = divergence(
        &reference.steps,
        &mutant.steps,
        ("reference", "odd-bit mutant"),
    );
    assert_eq!(d.at, 10);
    // The first differing field is the LINK WRITE: the honest model clears the bit,
    // transfers to the aligned 0x80000028 and writes x10 = pc+4; the mutant keeps the
    // odd bit and faults BEFORE the link write retires (the P2-SCALAR.3 ordering —
    // a synchronous exception retires no write), so its trap shows in the step pair
    // but the walk names the register first.
    assert!(
        d.what.contains("x10"),
        "names the link register: {}",
        d.what
    );
    assert_eq!(
        mutant.steps[10].writes,
        Vec::new(),
        "the mutant's trap retires no link write"
    );
}

// ---- designated class: wrong trap cause ----------------------------------------------------------

#[test]
fn wrong_requested_trap_cause_is_detected() {
    // Injection (model-level): ebreak's cause literal 3 (breakpoint) read as 11 (environment
    // call) — the tval is untouched, so the cause leg alone must carry the detection
    // (D-ECALL-EBREAK; the requested-trap vocabulary is 11/3).
    let ebreak = enc("ebreak", &[]);
    let (reference, _) = run_real(&[ebreak], 4);
    assert_eq!(reference.steps.len(), 1);
    assert_eq!(reference.stop, Stop::Trap);
    assert_eq!(
        reference.steps[0].trap,
        Some((0x03, ENTRY)),
        "GREEN: cause 3 is breakpoint"
    );
    let table = table_with_effect("ebreak", |sem| match sem {
        Sem::Lit(3) => Some(Sem::Lit(11)),
        _ => None,
    });
    let (mutant, _) = run_under(&[ebreak], 4, &table);
    assert_eq!(mutant.steps[0].trap, Some((0x0b, ENTRY)));
    let d = divergence(
        &reference.steps,
        &mutant.steps,
        ("reference", "wrong-cause mutant"),
    );
    assert_eq!(d.at, 0);
    assert!(d.what.contains("cause"), "names the trap cause: {}", d.what);
}

// ---- designated class: illegal-opcode substitution for a model limitation ------------------------

#[test]
fn illegal_instruction_substituted_for_a_limitation_is_detected() {
    // SEM-02: a target exception is emitted only under a source-linked target rule, never as
    // a substitute for missing supported behavior. Injection: the model limitation is
    // fence's row removed from the table; the violation is the limitation reported as an
    // IllegalInstruction trap (cause 2, tval = the word) — the observation the substituting
    // model emits. Observation-level by necessity: the substitution lives in an outcome
    // mapping a tree cannot name (exec refuses trap causes outside the requested-trap
    // vocabulary by construction), so a model-level seam for it would be a second
    // implementation of the exception mapping.
    let words = [
        enc("fence", &[]),
        enc("addi", &[("rd", 1), ("rs1", 0), ("imm12", 1)]),
    ];
    let (reference, _) = run_real(&words, 2);
    assert_eq!(
        reference.stop,
        Stop::Budget,
        "GREEN: fence is D-FENCE's nop and the program retires"
    );
    assert_eq!(reference.steps[1].writes, vec![(1, 1)]);
    // The limitation, honestly carried: the fence word is reserved for the limited model.
    // The interpreter reports the undefined case; the laboratory's declared D-RESERVED-DECODE
    // policy — an act of the HARNESS (run.rs), never of the model — then converts it to the
    // illegal-instruction observation, and the stop reason keeps the classification (SEM-01,
    // SEM-07). So at the observation level the honest limited model and the SEM-02-violating
    // substitute now produce the SAME step — the policy says so — and the distinction lives
    // exactly where SEM-02 put it: the model's own report (the stop reason), which the
    // substituting model has laundered into a target trap.
    let (honest, _) = run_under(&words, 2, &table_without("fence"));
    assert!(
        matches!(
            honest.stop,
            Stop::Undefined(UndefinedCase::ReservedDecode { .. })
        ),
        "the limitation is carried as the undefined case, not a trap: {:?}",
        honest.stop
    );
    assert_eq!(
        honest.steps,
        vec![Step {
            pc: ENTRY,
            word: Some(words[0]),
            writes: Vec::new(),
            trap: Some((0x02, u64::from(words[0]))),
        }],
        "the laboratory's declared policy conversion, and nothing else"
    );
    // The violation: the same limitation dressed as a target IllegalInstruction trap — the
    // observation is identical BY POLICY, so the detector reads the stop reason: a model
    // whose limitation surfaces as Stop::Trap fabricated the trap the honest model reported
    // as Undefined.
    let fabricated = Step {
        pc: ENTRY,
        word: Some(words[0]),
        writes: Vec::new(),
        trap: Some((0x02, u64::from(words[0]))),
    };
    let d = divergence(
        &reference.steps,
        &[fabricated],
        ("reference", "SEM-02-violating model"),
    );
    assert_eq!(
        d.at, 0,
        "the substitution is caught at the very step it fabricates"
    );
    assert!(
        d.what.contains("trap"),
        "names the fabricated trap: {}",
        d.what
    );
}

// ---- designated class: an extra memory access -----------------------------------------------------

#[test]
fn an_extra_memory_access_is_detected_by_the_crossing_census() {
    // Injection (model-level): every addi performs a discarded phantom byte load at the
    // region base before its real effect — an access the architectural observation
    // vocabulary cannot see. The trace comparison must still AGREE; the boundary-crossing
    // census is the instrument that catches it. (At the trace level the same injection would
    // surface only if the access faulted — which is the wrong-trap class, not this one.)
    let (reference, _) = assert_meets_pinned_expectations("guest-control", Stop::Budget);
    let table = table_with_row("addi", |insn| {
        let phantom = Sem::Seq(Box::leak(
            vec![
                leak(Sem::Load(
                    leak(Sem::Lit(8)),
                    leak(Sem::Lit(0)),
                    leak(Sem::Lit(ENTRY)),
                )),
                leak(rebuild(insn.effect, &|_| None)),
            ]
            .into_boxed_slice(),
        ));
        InsnDef {
            effect: leak(phantom),
            ..*insn
        }
    });
    let guest = find_guest("guest-control");
    let (mutant, crossings) = run_under(guest.words, guest.executed_steps, &table);
    must_agree(
        &reference.steps,
        &mutant.steps,
        ("reference", "extra-access mutant"),
    );
    let extra = data_crossings_by_step(&crossings);
    assert_eq!(
        extra.len(),
        7,
        "guest-control declares NO data access; each of its seven addis gained a phantom load: {extra:?}"
    );
    for (step, crossing) in &extra {
        assert!(
            matches!(
                crossing.request,
                Request::Load {
                    width: AccessWidth::B,
                    addr: ENTRY,
                    ..
                }
            ),
            "step {step}: the phantom access, named"
        );
    }
}

// ---- designated class: shifted event delivery ------------------------------------------------------

#[test]
fn shifted_event_delivery_is_detected_at_its_due_step() {
    // Injection (observation-level): the deferred-delivery model — smoke-trap's misaligned
    // load trapping one step late. The stream is what such a model emits: the trapping step
    // recorded WITHOUT its trap, and a fabricated following step carrying it. (A tree cannot
    // defer an exec-raised trap; the seam for it would be a second exception-mapping
    // implementation, so the arm applies the named behaviour to the observation stream.)
    let (reference, _) = assert_meets_pinned_expectations("smoke-trap", Stop::Trap);
    let trap = reference.steps[2]
        .trap
        .expect("the pinned trap: cause 4, tval 0x80000401");
    let mut deferred = reference.clone();
    deferred.steps[2].trap = None;
    deferred.steps.push(Step {
        pc: ENTRY + 12,
        word: Some(0),
        writes: Vec::new(),
        trap: Some(trap),
    });
    let d = divergence(
        &reference.steps,
        &deferred.steps,
        ("reference", "deferred-delivery model"),
    );
    assert_eq!(d.at, 2, "the due step is where the missing trap is named");
    assert!(
        d.what.contains("trap"),
        "names the missing trap: {}",
        d.what
    );
}

// ---- designated class: an overbroad mask hiding a changed defined bit -------------------------------

#[test]
fn an_overbroad_mask_hiding_a_changed_defined_bit_is_detected() {
    // Injection (model-level): srai's decode row stops covering bit 30 — the bit the
    // encoding's fixed ranges use to tell SRAI (`fixed (31 26 0x10)`) from SRLI (`0x0`). The
    // changed defined bit no longer discriminates: srli's canonical word now matches the
    // mutated srai row, and the table's name order (srai before srli) silently executes
    // srli as srai.
    const BIT_30: u32 = 1 << 30;
    let table = table_with_row("srai", |insn| InsnDef {
        mask: insn.mask & !BIT_30,
        value: insn.value & !BIT_30,
        ..*insn
    });
    let srli_word = enc("srli", &[("rd", 1), ("rs1", 1), ("shamt", 1)]);
    let resolved = table
        .iter()
        .find(|row| srli_word & row.mask == row.value)
        .map(|row| row.name);
    assert_eq!(
        resolved,
        Some("srai"),
        "the hidden-bit witness: an srli encoding resolves to srai under the overbroad mask"
    );
    assert_eq!(
        decode(srli_word).map(|row| row.name),
        Some("srli"),
        "GREEN: the real decoder discriminates the two encodings"
    );
    // The differential: with x1 = 1 << 63, srli brings in zeros and srai replicates the sign.
    let words = [
        enc("addi", &[("rd", 1), ("rs1", 0), ("imm12", 1)]),
        enc("slli", &[("rd", 1), ("rs1", 1), ("shamt", 63)]),
        srli_word,
    ];
    let (reference, _) = run_real(&words, 3);
    assert_eq!(
        reference.steps[2].writes,
        vec![(1, 0x4000_0000_0000_0000)],
        "GREEN: logical shift brings in zeros"
    );
    let (mutant, _) = run_under(&words, 3, &table);
    assert_eq!(
        mutant.steps[2].writes,
        vec![(1, 0xC000_0000_0000_0000)],
        "the mutant executed srai: the sign bit is replicated"
    );
    let d = divergence(
        &reference.steps,
        &mutant.steps,
        ("reference", "overbroad-mask model"),
    );
    assert_eq!(d.at, 2);
    assert!(d.what.contains("x1"), "names the register: {}", d.what);
}

// ---- designated class: a stale reference configuration ----------------------------------------------

#[test]
fn a_stale_reference_entry_configuration_is_detected_at_step_zero() {
    // Injection (observation-level): the reference side ran under a stale profile
    // configuration — the entry pinned one instruction late. The reference stream is the
    // real model over the same image from ENTRY+4; its very first observation differs in pc,
    // and the comparator must name it before anything else. (A wrong entry is configuration,
    // not semantics; there is no model-level seam to mutate.)
    let (reference, _) = assert_meets_pinned_expectations("guest-control", Stop::Budget);
    let guest = find_guest("guest-control");
    let mut env = flat(guest.words);
    let (stale, _) = run(&mut env, ENTRY + 4, guest.executed_steps);
    let d = divergence(
        &reference.steps,
        &stale.steps,
        ("reference", "stale-config reference"),
    );
    assert_eq!(
        d.at, 0,
        "a stale entry poisons every step; the first is the diagnosis"
    );
    assert!(d.what.contains("pc"), "names the pc: {}", d.what);
}
