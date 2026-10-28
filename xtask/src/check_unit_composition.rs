//! The `UNIT-COMPOSITION` doctrine, ported from `scripts/check_unit_composition.sh` (`XTASK.6` slice `6n`), which is
//! now a shim of `cargo xtask check-unit-composition`.
//!
//! `MODEL-COMPOSE.1` made a unit's encoding union a verdict and `MODEL-COMPOSE.2` moved the instructions into reusable
//! fragments — and the verdict silently stopped running on the unit (measured, `MODEL-COMPOSE.4`). This check reads every
//! tracked `profiles/*/encoding.sexp` through the ONE disjointness judge (`disjoint.rs`, validating through `schema.rs`
//! and resolving through `composition.rs`): a unit whose composed union collides, duplicates a name or carries a pseudo
//! problem is REJECTED; one the judge cannot read is REFUSED by name; a declared slot is reported partial. The script's
//! inline Python is ported line for line; each self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS`
//! arm total counts.

use std::collections::BTreeSet;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode};

use crate::disjoint::{
    check_slot_rules, composition_slots, judge_overlaps, load_fragment, load_specializations,
    pseudo_problems,
};
use crate::harness::scratch;
use crate::sexp;

#[derive(Clone, Copy, PartialEq, Eq)]
enum Mode {
    Git,
    Fs,
}

struct Verdict {
    rc: i32,
    lines: Vec<String>,
}

impl Verdict {
    fn text(&self) -> String {
        self.lines.join("\n")
    }
}

fn documents(root: &Path, mode: Mode) -> Vec<PathBuf> {
    match mode {
        Mode::Git => Command::new("git")
            .args(["ls-files", "--", "profiles/*/encoding.sexp"])
            .current_dir(root)
            .output()
            .map(|o| {
                String::from_utf8_lossy(&o.stdout)
                    .lines()
                    .filter(|l| !l.trim().is_empty())
                    .map(|l| root.join(l))
                    .collect()
            })
            .unwrap_or_default(),
        Mode::Fs => {
            let mut found: Vec<PathBuf> = fs::read_dir(root.join("profiles"))
                .map(|entries| {
                    entries
                        .flatten()
                        .map(|e| e.path().join("encoding.sexp"))
                        .filter(|p| p.is_file())
                        .collect()
                })
                .unwrap_or_default();
            found.sort();
            found
        }
    }
}

/// The inline Python, line for line: every unit composition decided through the one judge.
fn check_units(root: &Path, mode: Mode) -> Verdict {
    let mut out: Vec<String> = Vec::new();
    let docs = documents(root, mode);
    if docs.is_empty() {
        out.push("UNIT-COMPOSITION: REFUSED — no unit composition document found; this check cannot judge an empty corpus".to_owned());
        out.push("__CHECKED__ 0".to_owned());
        return Verdict { rc: 2, lines: out };
    }
    let mut findings: Vec<String> = Vec::new();
    let mut checked = 0u32;
    for doc in &docs {
        checked += 1;
        let shown = doc.display().to_string();
        let loaded: Result<_, String> = (|| {
            let (insns, pseudos) = load_fragment(root, doc).map_err(|e| e.0)?;
            let forms = sexp::read_file(doc).map_err(|e| e.0)?;
            let first = forms
                .first()
                .ok_or_else(|| "list index out of range".to_owned())?;
            let slots = composition_slots(first)?.1;
            check_slot_rules(doc, first).map_err(|e| e.0)?;
            Ok((insns, pseudos, slots))
        })();
        let (insns, pseudos, slots) = match loaded {
            Ok(v) => v,
            Err(e) => {
                findings.push(format!("REFUSED {shown}: {e}"));
                continue;
            }
        };
        let specs = match load_specializations(doc) {
            Ok(s) => s,
            Err(e) => {
                findings.push(format!("REFUSED {shown}: {}", e.0));
                continue;
            }
        };
        let (bad, _accepted, spec_problems) = judge_overlaps(&insns, &specs);
        let names: Vec<&str> = insns
            .iter()
            .map(|i| i.name.as_str())
            .chain(pseudos.iter().map(|p| p.name.as_str()))
            .collect();
        let dupes: BTreeSet<&str> = names
            .iter()
            .copied()
            .filter(|n| names.iter().filter(|m| m == &n).count() > 1)
            .collect();
        let mut problems = pseudo_problems(&insns, &pseudos);
        problems.extend(spec_problems);
        if !bad.is_empty() || !dupes.is_empty() || !problems.is_empty() {
            findings.push(format!(
                "REJECTED {shown}: {} collision(s), {} duplicate name(s), {} pseudo problem(s) — a decoder cannot be generated from a set in which one word matches two instructions",
                bad.len(),
                dupes.len(),
                problems.len()
            ));
            continue;
        }
        let suffix = if slots.is_empty() {
            String::new()
        } else {
            format!("; partial: {} slot(s) unbound", slots.len())
        };
        let pseudo = if pseudos.is_empty() {
            String::new()
        } else {
            format!(" (+ {} pseudo-instruction(s))", pseudos.len())
        };
        out.push(format!(
            "  {shown}: {} instruction(s){pseudo} compose{suffix}",
            insns.len()
        ));
    }
    out.extend(findings.iter().cloned());
    out.push(format!("__CHECKED__ {checked}"));
    Verdict {
        rc: i32::from(!findings.is_empty()),
        lines: out,
    }
}

struct Tally<'a> {
    root: &'a Path,
    pass: u32,
    fail: u32,
    verbose: bool,
    /// Every missed arm's report, for a quiet run's refusal (`XTASK.12`).
    misses: Vec<String>,
}

impl Tally<'_> {
    /// A missed arm's report: printed at once in a verbose run, kept for a quiet run's refusal (`XTASK.12`).
    fn report(&mut self, report: String) {
        if self.verbose {
            eprintln!("{report}");
        }
        self.misses.push(report);
    }
    /// One arm: judging the fixture tree must give `expected` and contain `want`.
    fn arm(&mut self, name: &str, expected: i32, want: &str) {
        let verdict = check_units(self.root, Mode::Fs);
        let out = verdict.text();
        if verdict.rc != expected {
            self.fail += 1;
            self.report(format!(
                "UNIT-COMPOSITION self-test MISS: {name} expected rc={expected} got rc={}\n{out}",
                verdict.rc
            ));
        } else if !out.contains(want) {
            self.fail += 1;
            self.report(format!("UNIT-COMPOSITION self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}"));
        } else {
            self.pass += 1;
        }
    }
}

fn write(path: &Path, text: &str) {
    if let Some(parent) = path.parent() {
        let _ = fs::create_dir_all(parent);
    }
    let _ = fs::write(path, text);
}

/// The RED/GREEN controls: a scratch unit over a two-instruction base fragment.
fn self_test(root: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(root, "target/doctrine-selftest", "unitcomp") else {
        eprintln!("UNIT-COMPOSITION self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    let _ = fs::create_dir_all(t.join("definitions/riscv"));
    let _ = fs::create_dir_all(t.join("profiles/p"));
    let _ = fs::create_dir_all(t.join("schema"));
    for s in ["encoding.sexp", "fragment.sexp", "schema.sexp"] {
        let _ = fs::copy(root.join("schema").join(s), t.join("schema").join(s));
    }
    let base_frag = || {
        write(
            &t.join("definitions/riscv/t-base.sexp"),
            "(fragment (id \"riscv/t-base\") (kind extension)\n(insn (name \"add\") (fixed (31 25 0x0) (14 12 0x0) (6 2 0x13) (1 0 0x3)))\n(insn (name \"sub\") (fixed (31 25 0x0) (14 12 0x1) (6 2 0x13) (1 0 0x3))))\n",
        )
    };
    let enc = |extra: &str| {
        write(
            &t.join("profiles/p/encoding.sexp"),
            &format!("(encoding (profile \"p\") (ilen 32)\n  (compose (base \"riscv/t-base\"){extra})\n  (fragment-root \"definitions\"))\n"),
        )
    };
    let mut tally = Tally {
        root: &t,
        pass: 0,
        fail: 0,
        verbose,
        misses: Vec::new(),
    };
    base_frag();
    enc(" (extensions)");
    tally.arm(
        "GREEN a complete unit composes",
        0,
        "instruction(s) compose",
    );
    base_frag();
    enc(" (extensions) (status partial) (slot (id clint) (requires \"riscv/t-timer\"))");
    tally.arm(
        "GREEN a declared slot is reported partial",
        0,
        "1 slot(s) unbound",
    );
    base_frag();
    enc(" (extensions) (slot (id clint))");
    tally.arm(
        "RED   slots claiming completeness",
        1,
        "claiming completeness while a hole is open",
    );
    base_frag();
    enc(" (extensions) (status partial)");
    tally.arm(
        "RED   a partial declaration with nothing unbound",
        1,
        "a hole is declared that is not there",
    );
    base_frag();
    enc(" (extensions) (widget \"x\")");
    tally.arm(
        "RED   an undeclared compose field",
        1,
        "undeclared field \"widget\"",
    );
    enc(" (extensions \"riscv/t-ghost\")");
    tally.arm(
        "RED   a fragment the composition names but does not have",
        1,
        "does not exist",
    );
    write(
        &t.join("definitions/riscv/t-clash.sexp"),
        "(fragment (id \"riscv/t-clash\") (kind extension)\n(insn (name \"add\") (fixed (31 25 0x0) (14 12 0x0) (6 2 0x13) (1 0 0x3))))\n",
    );
    base_frag();
    enc(" (extensions \"riscv/t-clash\")");
    tally.arm("RED   a collision in the composed union", 1, "collision(s)");
    write(
        &t.join("definitions/riscv/t-ghost-pseudo.sexp"),
        "(fragment (id \"riscv/t-ghost-pseudo\") (kind extension)\n(pseudo (name \"ghost\") (of \"t::add\") (fixed (30 28 0x5) (14 12 0x4)) (operands) (from \"t\")))\n",
    );
    base_frag();
    enc(" (extensions \"riscv/t-ghost-pseudo\")");
    tally.arm(
        "RED   a pseudo no composed instruction realizes",
        1,
        "pseudo problem(s)",
    );
    let _ = fs::remove_file(t.join("profiles/p/encoding.sexp"));
    tally.arm("RED   no composition document at all", 2, "cannot judge");
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "UNIT-COMPOSITION --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    } else {
        // A quiet run names every missed arm before the caller's refusal line (`XTASK.12`).
        for report in &tally.misses {
            eprintln!("{report}");
        }
    }
    tally.fail == 0
}

/// `cargo xtask check-unit-composition [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !self_test(root, false) {
        eprintln!(
            "UNIT-COMPOSITION: REFUSED — the check does not discriminate (self-test failed)."
        );
        return ExitCode::from(2);
    }
    let verdict = check_units(root, Mode::Git);
    let count = verdict
        .lines
        .iter()
        .find_map(|l| l.strip_prefix("__CHECKED__ "))
        .unwrap_or("0");
    let body: Vec<&str> = verdict
        .lines
        .iter()
        .filter(|l| !l.starts_with("__CHECKED__ "))
        .map(String::as_str)
        .collect();
    match verdict.rc {
        2 => {
            eprintln!("UNIT-COMPOSITION: REFUSED — the unit composition corpus could not be read.");
            for line in &body {
                eprintln!("  {line}");
            }
            ExitCode::from(2)
        }
        0 => {
            println!("UNIT-COMPOSITION: ok ({count} unit composition(s) decided)");
            ExitCode::SUCCESS
        }
        _ => {
            eprintln!("UNIT-COMPOSITION: a unit's composition does not hold.");
            for line in &body {
                eprintln!("  {line}");
            }
            eprintln!("  The composition is authoritative. Fix the unit, or it does not compose.");
            ExitCode::from(1)
        }
    }
}
