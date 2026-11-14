//! The read-once guarantee (`OB-GC-READ-ONCE`, `rv64gc-lab-env-v4`), realized as a census
//! over the tracked corpus (`P4-SYSTEM.20` slice e).
//!
//! A side-effecting device region is safe only if the hart reads it exactly as often as the
//! program does. The census runs every step of every tracked guest through the tracked
//! engine, counts each data crossing by kind, and classifies the step from its own fetched
//! bits: a load issues at most one `Load`, an LR at most one `AtomicLoad`, an AMO at most
//! one `AtomicLoad` and no store without it, and SC, every other instruction and an
//! unfetched step issue no data read at all. Zero reads is legal for any class: an access
//! that faults before its read never reads.
//!
//! The negative cannot rebuild the engine, so it models each defect as the boundary sees
//! it: an adapter on the engine's side of the recorder issues what a defective engine would
//! — every data read repeated, or an atomic read sent as a plain `Load`, as the engine did
//! before version 4 — and the census must name exactly the steps the defect touches. Main
//! memory reads have no side effect, so neither adapter changes what the run observes, and
//! each count is predicted from the positive census before the defect runs.
//!
//! Finite: the corpus's guests and the forms they reach, not every program.

use std::collections::BTreeMap;

use semulith_core::env::{BoundaryError, Environment, Request, Response};
use semulith_core::exec_rv64gc::{self, StepRv64gc};
use semulith_core::privilege;
use semulith_core::state_rv64gc::ArchitecturalState;

use crate::fixtures::FlatMemory;
use crate::guests_rv64gc::GUESTS;
use crate::run_rv64gc::Refusing;

/// What a step's own fetched bits name, as far as data reads are concerned.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
enum Class {
    /// An integer, FP or compressed load.
    Load,
    /// LR.W or LR.D.
    Lr,
    /// SC.W or SC.D.
    Sc,
    /// One of the nine AMOs, at either width.
    Amo,
    /// Any other instruction.
    Other,
    /// No instruction bits arrived: the fetch faulted, or the hart waited.
    Unfetched,
}

/// One step's crossings, by kind, and the instruction bits it fetched.
#[derive(Default)]
struct Crossings {
    loads: u32,
    atomic_loads: u32,
    stores: u32,
    word: Option<u32>,
    parcels: Vec<u16>,
}

/// Counts every crossing that reaches it, then forwards it unchanged.
struct Recording<'a, E> {
    inner: &'a mut E,
    seen: Crossings,
}

impl<E: Environment> Environment for Recording<'_, E> {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        let answer = self.inner.request(request);
        match (request, &answer) {
            (Request::Load { .. }, _) => self.seen.loads += 1,
            (Request::AtomicLoad { .. }, _) => self.seen.atomic_loads += 1,
            (Request::Store { .. }, _) => self.seen.stores += 1,
            (Request::Fetch { .. }, Ok(Response::Fetch(word))) => self.seen.word = Some(*word),
            (Request::FetchParcel { .. }, Ok(Response::FetchParcel(parcel))) => {
                self.seen.parcels.push(*parcel);
            }
            _ => {}
        }
        answer
    }
}

/// A modelled engine defect, placed between the engine and the recorder.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Defect {
    /// The tracked engine, unmodified.
    Absent,
    /// Every data read crosses twice; the second answer is the one used.
    RepeatedRead,
    /// An atomic read crosses as a plain `Load`, as LR and the AMOs did before version 4.
    AtomicAsLoad,
}

/// What the engine issues, as a defective engine would issue it.
struct Defective<'a, E> {
    inner: &'a mut E,
    defect: Defect,
}

impl<E: Environment> Environment for Defective<'_, E> {
    fn request(&mut self, request: Request) -> Result<Response, BoundaryError> {
        match (self.defect, request) {
            (Defect::RepeatedRead, Request::Load { .. } | Request::AtomicLoad { .. }) => {
                let _first = self.inner.request(request);
                self.inner.request(request)
            }
            (Defect::AtomicAsLoad, Request::AtomicLoad { width, addr }) => {
                self.inner.request(Request::Load { width, addr })
            }
            _ => self.inner.request(request),
        }
    }
}

/// Classify a step from the bits it fetched — independently of the engine's decoder, from
/// the pinned opcode map: major opcodes 0x03 (LOAD) and 0x07 (LOAD-FP); 0x2f (AMO) with
/// funct5 0x02 (LR) and 0x03 (SC); and the six compressed loads (quadrants 0 and 2, funct3
/// 1 to 3: C.FLD, C.LW, C.LD and their SP-relative forms).
fn classify(seen: &Crossings) -> Class {
    let word = match (seen.word, seen.parcels.as_slice()) {
        (Some(word), _) => word,
        (None, [low]) => u32::from(*low),
        (None, [low, high, ..]) => u32::from(*low) | (u32::from(*high) << 16),
        (None, []) => return Class::Unfetched,
    };
    if word & 3 != 3 {
        return match (word & 3, (word >> 13) & 7) {
            (0 | 2, 1..=3) => Class::Load,
            _ => Class::Other,
        };
    }
    match word & 0x7f {
        0x03 | 0x07 => Class::Load,
        0x2f => match word >> 27 {
            0x02 => Class::Lr,
            0x03 => Class::Sc,
            _ => Class::Amo,
        },
        _ => Class::Other,
    }
}

/// The guarantee, judged for one step: `None` when it holds, the breach otherwise.
fn breach(class: Class, seen: &Crossings) -> Option<&'static str> {
    let (loads, atomic, stores) = (seen.loads, seen.atomic_loads, seen.stores);
    match class {
        Class::Load if loads > 1 => Some("a load read more than once"),
        Class::Load if atomic != 0 => Some("a load crossed as an atomic read"),
        Class::Lr | Class::Amo if loads != 0 => Some("an atomic read crossed as a plain Load"),
        Class::Lr | Class::Amo if atomic > 1 => Some("an atomic read crossed more than once"),
        Class::Amo if stores > atomic => Some("an AMO stored without its atomic read"),
        Class::Sc | Class::Other | Class::Unfetched if loads + atomic != 0 => {
            Some("a step that names no read issued one")
        }
        _ => None,
    }
}

/// What a census run found: steps by class and how many of them read, and each breach.
#[derive(Debug, Default)]
struct Census {
    /// Steps of each class, and how many of them issued a data read.
    steps: BTreeMap<Class, (u64, u64)>,
    /// Every breach, as `guest step n: class: reason`.
    breaches: Vec<String>,
}

impl Census {
    fn reading(&self, class: Class) -> u64 {
        self.steps.get(&class).map_or(0, |&(_, reading)| reading)
    }
}

/// Run every step of every tracked guest through the tracked engine, as the corpus runner
/// does — the same flat memory, the guest's declared refusals, the reserved-decode
/// conversion — with the given defect between the engine and the recorder.
fn census(defect: Defect) -> Census {
    let mut census = Census::default();
    for guest in GUESTS {
        let mut memory = FlatMemory::with_fetch_align(guest.entry, 0x10000, 2);
        memory.load_image(0, guest.image);
        let mut state = ArchitecturalState::zeroed_at(guest.entry);
        for n in 0..guest.executed_steps {
            let mut refusing = Refusing {
                inner: &mut memory,
                refusals: guest.refusals,
            };
            let mut recording = Recording {
                inner: &mut refusing,
                seen: Crossings::default(),
            };
            let mut engine_side = Defective {
                inner: &mut recording,
                defect,
            };
            let outcome = exec_rv64gc::step(&mut state, &mut engine_side);
            let seen = recording.seen;
            let class = classify(&seen);
            let entry = census.steps.entry(class).or_default();
            entry.0 += 1;
            entry.1 += u64::from(seen.loads + seen.atomic_loads != 0);
            if let Some(reason) = breach(class, &seen) {
                census
                    .breaches
                    .push(format!("{} step {n}: {class:?}: {reason}", guest.name));
            }
            match outcome {
                StepRv64gc::Executed => {}
                StepRv64gc::ReservedDecode { at, word } => {
                    let handler = privilege::trap_deliver(&mut state, 2, u64::from(word), at);
                    state.set_pc(handler);
                }
                StepRv64gc::Failed(error) => {
                    census.breaches.push(format!(
                        "{} step {n}: the run failed: {error:?}",
                        guest.name
                    ));
                    break;
                }
            }
        }
    }
    census
}

/// The tracked engine keeps the guarantee on every step of the corpus, and the corpus is
/// not vacuous: each read class issues a read somewhere, and SC runs.
pub(super) fn positive() -> Result<(), String> {
    let census = census(Defect::Absent);
    if let Some(first) = census.breaches.first() {
        return Err(format!(
            "{} breach(es) of the read-once guarantee; first: {first}",
            census.breaches.len()
        ));
    }
    for class in [Class::Load, Class::Lr, Class::Amo] {
        if census.reading(class) == 0 {
            return Err(format!("no {class:?} step read: the census is vacuous"));
        }
    }
    if census.steps.get(&Class::Sc).map_or(0, |&(steps, _)| steps) == 0 {
        return Err("no SC step ran: the census cannot see an SC read".into());
    }
    Ok(())
}

/// Each modelled defect is named on exactly the steps it touches: a repeated read on
/// every step that reads, an atomic read sent as a load on every LR and AMO that reads.
pub(super) fn negative() -> Result<(), String> {
    let clean = census(Defect::Absent);
    let reading = clean.reading(Class::Load) + clean.reading(Class::Lr) + clean.reading(Class::Amo);
    let atomic = clean.reading(Class::Lr) + clean.reading(Class::Amo);
    for (defect, predicted, reason) in [
        (Defect::RepeatedRead, reading, "more than once"),
        (
            Defect::AtomicAsLoad,
            atomic,
            "an atomic read crossed as a plain Load",
        ),
    ] {
        let found = census(defect);
        let named = found.breaches.iter().filter(|b| b.contains(reason)).count() as u64;
        if named != predicted || found.breaches.len() as u64 != predicted {
            return Err(format!(
                "{defect:?}: predicted {predicted} breach(es) naming {reason:?}, found {} ({named} naming it); first: {:?}",
                found.breaches.len(),
                found.breaches.first()
            ));
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn the_corpus_keeps_the_guarantee_and_both_defects_are_named() {
        assert_eq!(positive(), Ok(()));
        assert_eq!(negative(), Ok(()));
    }

    #[test]
    fn the_judge_names_each_breach() {
        let step = |loads, atomic_loads, stores| Crossings {
            loads,
            atomic_loads,
            stores,
            ..Crossings::default()
        };
        for (class, seen, reason) in [
            (Class::Load, step(2, 0, 0), "a load read more than once"),
            (
                Class::Load,
                step(0, 1, 0),
                "a load crossed as an atomic read",
            ),
            (
                Class::Lr,
                step(1, 0, 0),
                "an atomic read crossed as a plain Load",
            ),
            (
                Class::Amo,
                step(0, 2, 2),
                "an atomic read crossed more than once",
            ),
            (
                Class::Amo,
                step(0, 0, 1),
                "an AMO stored without its atomic read",
            ),
            (
                Class::Sc,
                step(0, 1, 1),
                "a step that names no read issued one",
            ),
            (
                Class::Other,
                step(1, 0, 0),
                "a step that names no read issued one",
            ),
            (
                Class::Unfetched,
                step(1, 0, 0),
                "a step that names no read issued one",
            ),
        ] {
            assert_eq!(breach(class, &seen), Some(reason), "{class:?}");
        }
        for (class, seen) in [
            (Class::Load, step(1, 0, 0)),
            (Class::Load, step(0, 0, 0)),
            (Class::Lr, step(0, 1, 0)),
            (Class::Amo, step(0, 1, 1)),
            (Class::Amo, step(0, 1, 0)),
            (Class::Sc, step(0, 0, 1)),
            (Class::Other, step(0, 0, 1)),
        ] {
            assert_eq!(breach(class, &seen), None, "{class:?}");
        }
    }

    #[test]
    fn the_classifier_reads_the_pinned_opcode_map() {
        let word = |w: u32| Crossings {
            word: Some(w),
            ..Crossings::default()
        };
        // LD x6,0(x5); FLD f6,0(x5); LR.W x6,(x5); SC.W x6,x0,(x5); AMOADD.W x10,x11,(x5);
        // ADDI x6,x0,1; then C.LW a0,0(a1) as one parcel, and a step with no bits.
        for (seen, class) in [
            (word(0x0002_b303), Class::Load),
            (word(0x0002_b307), Class::Load),
            (word(0x1002_a32f), Class::Lr),
            (word(0x1802_a32f), Class::Sc),
            (word(0x00b2_a52f), Class::Amo),
            (word(0x0010_0313), Class::Other),
            (
                Crossings {
                    parcels: vec![0x4188],
                    ..Crossings::default()
                },
                Class::Load,
            ),
            (Crossings::default(), Class::Unfetched),
        ] {
            assert_eq!(classify(&seen), class);
        }
    }
}
