//! The validator-mutation campaign over the RV64GC tables (`P4-SYSTEM.15` slice d, `EVD-09`):
//! proof that the unit's directed corpus *detects* each designated wrong behaviour of the
//! complete profile, not only that the production table agrees with its expectations.
//!
//! Every mutant is DATA the one production evaluator consumes (OWN-01 untouched): the
//! generated `definition_rv64gc::INSNS` table copied with one row changed — its effect
//! swapped for a sibling's, replaced by `Nop`, the row removed, or one node of its effect
//! tree perturbed in the shape `model_rv64gc` already uses for the two replay controls.
//! The detector is the corpus's own rule (`run_rv64gc::assert_guest_observations`'s
//! vocabulary — per-step pc, mode and x-register changes, and the run's failure): a mutant
//! is detected when at least one tracked guest's trace under the mutant differs from its
//! trace under the production table. The census names, per mutant, the guests that
//! detect it; a mutant no guest detects is a corpus gap the campaign REPORTS, never a pass.
//!
//! FP state is not in the trace's vocabulary (x registers only), so an FP mutant is
//! detected through the guests that move FP results, classes, comparisons or conversions
//! into x registers (`f-*`, `d-*`, `fp-*`) — the census shows which.

use semulith_core::definition_rv64gc::{InsnDef, Sem, INSNS};

use crate::guests_rv64gc::{Guest, GUESTS};
use crate::model_rv64gc::Model;
use crate::run_rv64gc::{run_guest, run_guest_over, Trace};

/// The family a mutant perturbs — the complete profile's extension letters and the
/// privileged architecture — so the census can show every family touched.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Family {
    /// The base integer instruction set.
    I,
    /// Integer multiplication and division.
    M,
    /// Atomics (Zaamo and Zalrsc).
    A,
    /// Single-precision floating point.
    F,
    /// Double-precision floating point.
    D,
    /// Compressed instructions.
    C,
    /// CSR access instructions.
    Zicsr,
    /// The privileged architecture (traps, returns, waits).
    Privileged,
}

/// How a row is perturbed. Each is data: a copy of the table with one row changed.
#[derive(Clone, Copy, Debug)]
pub enum Perturbation {
    /// The row's effect is a sibling row's effect (operand names shared).
    EffectOf(&'static str),
    /// The row's effect is `Nop`: the instruction decodes and does nothing.
    Nop,
    /// The row is absent: the model does not implement a declared instruction.
    Remove,
    /// One of the two replay control models (`model_rv64gc`), whose effect-tree
    /// perturbation is the canonical shape.
    Control(Model),
}

/// One designated wrong behaviour: `(name, family, row, perturbation, story)`.
pub struct Mutation {
    /// The mutant's name, the campaign's spelling (`family-row-what`).
    pub name: &'static str,
    /// The extension family the perturbed row belongs to.
    pub family: Family,
    /// The generated definition's row the mutant changes.
    pub row: &'static str,
    /// How the row is changed.
    pub how: Perturbation,
    /// The wrong behaviour in one line.
    pub story: &'static str,
}

/// The campaign's inventory. `none` is deliberately absent: the production table is the
/// anchor every test runs first, not a member of the inventory.
pub const MUTATIONS: &[Mutation] = &[
    // I — the base, through the two canonical controls and two sibling swaps
    Mutation {
        name: "zext-addi",
        family: Family::I,
        row: "addi",
        how: Perturbation::Control(Model::ZextAddi),
        story: "addi zero-extends its immediate instead of sign-extending it",
    },
    Mutation {
        name: "jal-no-link",
        family: Family::I,
        row: "jal",
        how: Perturbation::Control(Model::JalNoLink),
        story: "jal transfers but does not write its link register",
    },
    Mutation {
        name: "slt-unsigned",
        family: Family::I,
        row: "slt",
        how: Perturbation::EffectOf("sltu"),
        story: "slt compares unsigned",
    },
    Mutation {
        name: "lw-zero-extends",
        family: Family::I,
        row: "lw",
        how: Perturbation::EffectOf("lwu"),
        story: "lw zero-extends the loaded word",
    },
    Mutation {
        name: "sraiw-as-srliw",
        family: Family::I,
        row: "sraiw",
        how: Perturbation::EffectOf("srliw"),
        story: "sraiw shifts in zeros",
    },
    // M
    Mutation {
        name: "mul-as-mulh",
        family: Family::M,
        row: "mul",
        how: Perturbation::EffectOf("mulh"),
        story: "mul writes the high half of the product",
    },
    Mutation {
        name: "divu-as-div",
        family: Family::M,
        row: "divu",
        how: Perturbation::EffectOf("div"),
        story: "divu divides signed",
    },
    Mutation {
        name: "remw-missing",
        family: Family::M,
        row: "remw",
        how: Perturbation::Remove,
        story: "the model does not implement remw",
    },
    // A
    Mutation {
        name: "amoadd-w-as-swap",
        family: Family::A,
        row: "amoadd.w",
        how: Perturbation::EffectOf("amoswap.w"),
        story: "amoadd.w stores the operand instead of the sum",
    },
    Mutation {
        name: "amomax-d-unsigned",
        family: Family::A,
        row: "amomax.d",
        how: Perturbation::EffectOf("amomaxu.d"),
        story: "amomax.d compares unsigned",
    },
    Mutation {
        name: "sc-d-nop",
        family: Family::A,
        row: "sc.d",
        how: Perturbation::Nop,
        story: "sc.d neither stores nor writes its success code",
    },
    // F
    Mutation {
        name: "fadd-s-as-fsub",
        family: Family::F,
        row: "fadd.s",
        how: Perturbation::EffectOf("fsub.s"),
        story: "fadd.s subtracts",
    },
    Mutation {
        name: "feq-s-as-flt",
        family: Family::F,
        row: "feq.s",
        how: Perturbation::EffectOf("flt.s"),
        story: "feq.s answers less-than",
    },
    Mutation {
        name: "fmv-x-w-nop",
        family: Family::F,
        row: "fmv.x.w",
        how: Perturbation::Nop,
        story: "fmv.x.w moves nothing",
    },
    Mutation {
        name: "fcvt-w-s-unsigned",
        family: Family::F,
        row: "fcvt.w.s",
        how: Perturbation::EffectOf("fcvt.wu.s"),
        story: "fcvt.w.s converts to unsigned",
    },
    Mutation {
        name: "fclass-s-missing",
        family: Family::F,
        row: "fclass.s",
        how: Perturbation::Remove,
        story: "the model does not implement fclass.s",
    },
    // D
    Mutation {
        name: "fadd-d-as-fmul",
        family: Family::D,
        row: "fadd.d",
        how: Perturbation::EffectOf("fmul.d"),
        story: "fadd.d multiplies",
    },
    Mutation {
        name: "fle-d-as-feq",
        family: Family::D,
        row: "fle.d",
        how: Perturbation::EffectOf("feq.d"),
        story: "fle.d answers equality",
    },
    Mutation {
        name: "fmv-x-d-nop",
        family: Family::D,
        row: "fmv.x.d",
        how: Perturbation::Nop,
        story: "fmv.x.d moves nothing",
    },
    Mutation {
        name: "fcvt-l-d-unsigned",
        family: Family::D,
        row: "fcvt.l.d",
        how: Perturbation::EffectOf("fcvt.lu.d"),
        story: "fcvt.l.d converts to unsigned",
    },
    // C — a compressed row's OWN effect (its expansion only binds operands)
    Mutation {
        name: "c-addi-nop",
        family: Family::C,
        row: "c.addi",
        how: Perturbation::Nop,
        story: "c.addi does nothing",
    },
    Mutation {
        name: "c-sub-as-xor",
        family: Family::C,
        row: "c.sub",
        how: Perturbation::EffectOf("c.xor"),
        story: "c.sub exclusive-ors",
    },
    Mutation {
        name: "c-ld-nop",
        family: Family::C,
        row: "c.ld",
        how: Perturbation::Nop,
        story: "c.ld loads nothing",
    },
    Mutation {
        name: "c-j-nop",
        family: Family::C,
        row: "c.j",
        how: Perturbation::Nop,
        story: "c.j falls through",
    },
    // Zicsr
    Mutation {
        name: "csrrw-as-csrrs",
        family: Family::Zicsr,
        row: "csrrw",
        how: Perturbation::EffectOf("csrrs"),
        story: "csrrw sets bits instead of writing the value",
    },
    Mutation {
        name: "csrrci-nop",
        family: Family::Zicsr,
        row: "csrrci",
        how: Perturbation::Nop,
        story: "csrrci neither reads nor clears",
    },
    // Privileged
    Mutation {
        name: "mret-nop",
        family: Family::Privileged,
        row: "mret",
        how: Perturbation::Nop,
        story: "mret returns nowhere and restores nothing",
    },
    Mutation {
        name: "sret-as-mret",
        family: Family::Privileged,
        row: "sret",
        how: Perturbation::EffectOf("mret"),
        story: "sret behaves as mret",
    },
    Mutation {
        name: "ecall-nop",
        family: Family::Privileged,
        row: "ecall",
        how: Perturbation::Nop,
        story: "ecall traps nowhere",
    },
    Mutation {
        name: "wfi-missing",
        family: Family::Privileged,
        row: "wfi",
        how: Perturbation::Remove,
        story: "the model does not implement wfi",
    },
];

/// The mutants the tracked corpus does NOT detect — the campaign's finding, pinned. Slice d found
/// two (`fle-d-as-feq`: d-compare exercised `fle.d` only where <= and = agree; `c-sub-as-xor`:
/// c-alu exercised `c.sub` only where - and ^ agree); slice e closed both with one discriminating
/// instruction each. The pin keeps the test honest in both directions — a new gap fails it, and
/// so does a gap a new guest closes, until the pin moves with the corpus.
pub const KNOWN_GAPS: &[&str] = &[];

fn canonical_row(table: &[InsnDef], name: &str) -> Result<usize, String> {
    table
        .iter()
        .position(|row| row.name == name)
        .ok_or_else(|| format!("RV64GC mutation: the generated definition has no `{name}` row"))
}

/// The mutant's instruction table — the production table with one row changed as the
/// inventory says. A row the generated definition no longer carries is a refusal, not a
/// silent pass: the inventory must follow the definition.
pub fn table_for(mutation: &Mutation) -> Result<Vec<InsnDef>, String> {
    if let Perturbation::Control(model) = mutation.how {
        return Ok(model
            .table()?
            .iter()
            .map(|row| InsnDef { ..*row })
            .collect());
    }
    let mut table: Vec<InsnDef> = INSNS.iter().map(|row| InsnDef { ..*row }).collect();
    let at = canonical_row(&table, mutation.row)?;
    match mutation.how {
        Perturbation::EffectOf(sibling) => {
            let from = canonical_row(&table, sibling)?;
            let effect = table[from].effect;
            table[at].effect = effect;
        }
        Perturbation::Nop => table[at].effect = &Sem::Nop,
        Perturbation::Remove => {
            table.remove(at);
        }
        Perturbation::Control(_) => unreachable!("handled above"),
    }
    Ok(table)
}

/// One guest's verdict on one mutant: the step at which its trace first departs from the
/// production trace, or `None` when the guest cannot tell the two apart.
#[must_use]
pub fn first_divergence(production: &Trace, mutant: &Trace) -> Option<usize> {
    if production.failed != mutant.failed {
        return Some(production.steps.len().min(mutant.steps.len()));
    }
    production
        .steps
        .iter()
        .zip(&mutant.steps)
        .position(|(a, b)| a != b)
        .or_else(|| {
            (production.steps.len() != mutant.steps.len())
                .then_some(production.steps.len().min(mutant.steps.len()))
        })
}

/// One detection: the guest's name and the step at which its trace first diverges.
pub type Detection = (&'static str, usize);

/// The campaign's census: every mutant with its detections, in inventory order.
pub type Census = Vec<(&'static Mutation, Vec<Detection>)>;

/// The guests that detect a mutant, each with the step of first divergence.
pub fn detectors(mutation: &Mutation) -> Result<Vec<Detection>, String> {
    let table = table_for(mutation)?;
    let mut found = Vec::new();
    for guest in GUESTS {
        let production = run_guest(guest).0;
        let under = run_guest_over(guest, &table).0;
        if let Some(at) = first_divergence(&production, &under) {
            found.push((guest.name, at));
        }
    }
    Ok(found)
}

/// The campaign's census: every mutant with its detectors, in inventory order.
pub fn census() -> Result<Census, String> {
    MUTATIONS
        .iter()
        .map(|m| detectors(m).map(|d| (m, d)))
        .collect()
}

/// The guest a name denotes (the campaign's own lookup, so a test reads as a name).
#[must_use]
pub fn guest(name: &str) -> &'static Guest {
    GUESTS
        .iter()
        .find(|g| g.name == name)
        .unwrap_or_else(|| panic!("guest {name} is in the generated fixture"))
}

#[cfg(test)]
mod tests;
