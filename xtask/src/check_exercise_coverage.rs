//! The `EXERCISE-COVERAGE` doctrine, ported from `scripts/check_exercise_coverage.sh` (`XTASK.6` slice `6k`),
//! which is now a shim of `cargo xtask check-exercise-coverage`.
//!
//! `P2-SCALAR.1`'s acceptance, mechanized: every form a profile DECLARES in its `[scope]` is EXECUTED by at
//! least one tracked guest — coverage reported with its denominator, never as a bare count. The denominator
//! is re-derived from the scope's mnemonic lists (a `count_total` that disagrees with its own enumeration is a
//! DENOMINATOR LIE); the numerator is the union of mnemonics the tracked expectation documents declare
//! executed. SCP-02 rides the same verdict: the composition resolves through ONE resolver — the port of
//! `riscv_asm.resolve_composition`, refusing a missing fragment or an unmet `requires` by name — and every
//! declared form must exist in it. Units declaring a `checkpoint-end-state` comparison are measured against
//! their `.a56` corpus in both directions; `device-model` and `profile-resolution` routes make both legs n/a
//! by declaration, and a document that contradicts the declaration is a finding. The script's inline Python
//! is ported line for line (the first consumer of the Rust S-expression reader, `sexp.rs`); each self-test
//! arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::collections::BTreeSet;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode};

use crate::composition::resolve_composition;
use crate::harness::scratch;
use crate::sexp::{self, Sexp, SexpError};

/// Which profile dossiers a run judges: the tracked ones (the real run) or every one on disk (the fixtures).
#[derive(Clone, Copy, PartialEq, Eq)]
enum Mode {
    Git,
    Fs,
}

/// What the inline Python printed and returned: its stdout lines, in order, and its exit status.
struct Verdict {
    rc: i32,
    lines: Vec<String>,
}

impl Verdict {
    fn text(&self) -> String {
        self.lines.join("\n")
    }
}

/// Python's `str(x)` of a parsed atom.
fn py_str(v: &Sexp) -> String {
    match v {
        Sexp::Int(n) => n.to_string(),
        Sexp::Str(s) | Sexp::Symbol(s) => s.clone(),
        Sexp::List(_) => sexp::py_repr(v),
    }
}

/// The directories whose dossiers a run judges, in the Python's order.
fn profiles(root: &Path, mode: Mode) -> Vec<PathBuf> {
    match mode {
        Mode::Git => {
            let out = Command::new("git")
                .args(["ls-files", "--", "profiles/*/profile.sexp"])
                .current_dir(root)
                .output();
            match out {
                Ok(o) => String::from_utf8_lossy(&o.stdout)
                    .lines()
                    .filter(|l| !l.trim().is_empty())
                    .map(|l| root.join(l))
                    .collect(),
                Err(_) => Vec::new(),
            }
        }
        Mode::Fs => {
            let mut found: Vec<PathBuf> = fs::read_dir(root.join("profiles"))
                .map(|entries| {
                    entries
                        .flatten()
                        .map(|e| e.path().join("profile.sexp"))
                        .filter(|p| p.is_file())
                        .collect()
                })
                .unwrap_or_default();
            found.sort();
            found
        }
    }
}

fn rel(path: &Path, root: &Path) -> String {
    path.strip_prefix(root)
        .unwrap_or(path)
        .to_string_lossy()
        .replace('\\', "/")
}

/// The first top-level form whose head is `name`, as `next(f for f in forms if …)`; `None` is StopIteration.
fn first_form<'a>(forms: &'a [Sexp], name: &str) -> Option<&'a Sexp> {
    forms
        .iter()
        .find(|f| matches!(f, Sexp::List(l) if l.first().and_then(Sexp::text) == Some(name)))
}

fn second_text(form: &Sexp) -> String {
    match form {
        Sexp::List(l) if l.len() > 1 => py_str(&l[1]),
        _ => String::new(),
    }
}

fn dir_has_entries(dir: &Path) -> bool {
    dir.is_dir()
        && fs::read_dir(dir)
            .map(|mut d| d.next().is_some())
            .unwrap_or(false)
}

fn sorted_glob(dir: &Path, suffix: &str) -> Vec<PathBuf> {
    let mut found: Vec<PathBuf> = fs::read_dir(dir)
        .map(|entries| {
            entries
                .flatten()
                .map(|e| e.path())
                .filter(|p| p.is_file() && p.to_string_lossy().ends_with(suffix))
                .collect()
        })
        .unwrap_or_default();
    found.sort();
    found
}

const A56_DIRECTIVES: &[&str] = &[
    "org", "end", "dc", "ds", "dsm", "equ", "set", "page", "sect", "endsec", "include", "define",
    "undefine", "macro", "endm", "if", "else", "endif", "dup", "enddup", "msg", "warn", "fail",
];

/// The inline Python, line for line: the census over every profile dossier under `root`.
fn check_coverage(root: &Path, mode: Mode) -> Verdict {
    let mut out: Vec<String> = Vec::new();
    let profiles = profiles(root, mode);
    if profiles.is_empty() {
        out.push("EXERCISE-COVERAGE: REFUSED — no tracked profile dossier found; this check cannot judge".to_owned());
        out.push("__CHECKED__ 0".to_owned());
        return Verdict { rc: 2, lines: out };
    }
    let mut findings: Vec<String> = Vec::new();
    let mut checked = 0u32;
    for prof_path in &profiles {
        let pdir = prof_path.parent().unwrap_or(Path::new(""));
        let tag = rel(prof_path, root);
        let forms = match sexp::read_file(prof_path) {
            Ok(f) => f,
            Err(SexpError(e)) => {
                findings.push(format!("UNREADABLE {tag}: {e}"));
                continue;
            }
        };
        let Some(form) = first_form(&forms, "profile") else {
            findings.push(format!("UNREADABLE {tag}: "));
            continue;
        };
        let scopes = sexp::children(form, "scope").unwrap_or_default();
        let Some(scope) = scopes.first() else {
            findings.push(format!(
                "UNDECLARED SCOPE {tag}: the dossier declares no [scope] — coverage against a scope that was \
                 never declared proves nothing"
            ));
            continue;
        };
        let vehicle = sexp::children(form, "vehicle").unwrap_or_default();
        let checkpoint = vehicle.iter().any(|v| {
            sexp::children(v, "comparison")
                .unwrap_or_default()
                .iter()
                .any(|c| second_text(c) == "checkpoint-end-state")
        });
        let routes: Vec<String> = vehicle
            .iter()
            .flat_map(|v| sexp::children(v, "route").unwrap_or_default())
            .map(second_text)
            .collect();
        let device = routes.first().map(String::as_str) == Some("device-model");
        let resolution = routes.first().map(String::as_str) == Some("profile-resolution");
        let mut denominator: BTreeSet<String> = BTreeSet::new();
        if let Sexp::List(items) = scope {
            for f in items.iter().skip(1) {
                if let Sexp::List(l) = f {
                    let head = l.first().and_then(Sexp::text).unwrap_or("");
                    if !l.is_empty()
                        && !matches!(
                            head,
                            "count_base"
                                | "count_rv64i_additions"
                                | "count_total"
                                | "authority"
                                | "source"
                                | "comment"
                        )
                    {
                        for v in l.iter().skip(1) {
                            denominator.insert(py_str(v).to_lowercase());
                        }
                    }
                }
            }
        }
        let totals = sexp::children(scope, "count_total").unwrap_or_default();
        let declared_total: Option<i128> = totals.first().and_then(|t| match t {
            Sexp::List(l) if l.len() > 1 => match &l[1] {
                Sexp::Int(n) => Some(*n),
                other => py_str(other).trim().parse::<i128>().ok(),
            },
            _ => None,
        });
        checked += 1;
        match declared_total {
            None => findings.push(format!(
                "DENOMINATOR ABSENT {tag}: [scope] carries no count_total — a denominator nobody states is a \
                 coverage claim nobody can check"
            )),
            Some(n) if n != denominator.len() as i128 => findings.push(format!(
                "DENOMINATOR LIE {tag}: count_total says {n} but the mnemonic lists enumerate {} — the \
                 declaration contradicts its own enumeration",
                denominator.len()
            )),
            Some(_) => {}
        }
        let enc_path = pdir.join("encoding.sexp");
        let mut resolved: BTreeSet<String> = BTreeSet::new();
        let mut closure = "unresolved".to_owned();
        if !enc_path.is_file() {
            if checkpoint {
                closure = "n/a (checkpoint-end-state declared; no encoding.sexp — measured against the guest corpus)".to_owned();
            } else if device {
                closure = "n/a (device-model declared; no encoding.sexp — a device composes no instruction encoding)".to_owned();
            } else if resolution {
                closure = "n/a (profile-resolution declared; no encoding.sexp — the definition pipeline has not started)".to_owned();
            } else {
                findings.push(format!(
                    "NO COMPOSITION {tag}: no encoding.sexp beside the dossier — the declared scope's dependency \
                     closure cannot be decided"
                ));
            }
        } else if device {
            findings.push(format!(
                "DECLARATION CONTRADICTION {tag}: device-model route declared but an encoding.sexp exists — the \
                 declaration contradicts the documents"
            ));
        } else if resolution {
            findings.push(format!(
                "DECLARATION CONTRADICTION {tag}: profile-resolution route declared but an encoding.sexp exists — \
                 the declaration contradicts the documents"
            ));
        } else {
            let attempt: Result<(), String> = (|| {
                let enc_forms = sexp::read_file(&enc_path).map_err(|e| e.0)?;
                let enc = enc_forms
                    .first()
                    .ok_or_else(|| "list index out of range".to_owned())?;
                let comp = sexp::children(enc, "compose").map_err(|e| e.0)?;
                let comp0 = comp
                    .first()
                    .ok_or_else(|| "list index out of range".to_owned())?;
                let shown = enc_path.display().to_string();
                let base = py_str(sexp::field(comp0, "base", &shown).map_err(|e| e.0)?);
                let mut names = vec![base];
                for e in sexp::children(comp0, "extensions").map_err(|e| e.0)? {
                    if let Sexp::List(items) = e {
                        names.extend(items.iter().skip(1).map(py_str));
                    }
                }
                let merged = resolve_composition(enc, &enc_path).map_err(|e| e.0)?;
                for i in sexp::children(&merged, "insn").map_err(|e| e.0)? {
                    resolved.insert(py_str(sexp::field(i, "name", "").map_err(|e| e.0)?));
                }
                for i in sexp::children(&merged, "pseudo").map_err(|e| e.0)? {
                    resolved.insert(py_str(sexp::field(i, "name", "").map_err(|e| e.0)?));
                }
                closure = format!("{{{}}}", names.join(", "));
                Ok(())
            })();
            if let Err(e) = attempt {
                findings.push(format!("UNMET DEPENDENCY {tag}: {e}"));
            }
        }
        if !closure.starts_with("n/a") && !device && !resolution {
            for m in denominator.difference(&resolved) {
                findings.push(format!(
                    "UNRESOLVED FORM {tag}: [scope] declares '{m}' but the resolved composition does not provide \
                     it — an included feature whose dependency is not closed (SCP-02)"
                ));
            }
        }
        let mut exercised: BTreeSet<String> = BTreeSet::new();
        let pdir_rel = rel(pdir, root);
        if device {
            let gdir = pdir.join("guests");
            if dir_has_entries(&gdir) {
                findings.push(format!(
                    "DECLARATION CONTRADICTION {tag}: device-model route declared but a guests/ corpus exists — \
                     the declaration and the documents disagree"
                ));
            } else {
                out.push(format!(
                    "{pdir_rel}: device-model route declared — {} declared registers, exercise n/a by declaration",
                    denominator.len()
                ));
            }
            continue;
        }
        if resolution {
            let gdir = pdir.join("guests");
            if dir_has_entries(&gdir) {
                findings.push(format!(
                    "DECLARATION CONTRADICTION {tag}: profile-resolution route declared but a guests/ corpus \
                     exists — the declaration and the documents disagree"
                ));
            } else {
                out.push(format!(
                    "{pdir_rel}: profile-resolution route declared — {} declared forms, exercise n/a by declaration",
                    denominator.len()
                ));
            }
            continue;
        }
        if checkpoint {
            let a56_files = sorted_glob(&pdir.join("guests"), ".a56");
            if a56_files.is_empty() {
                findings.push(format!(
                    "NO GUESTS {tag}: checkpoint-end-state declared but no guests/*.a56 — nothing is exercised"
                ));
            }
            for gf in &a56_files {
                let gtag = rel(gf, root);
                let text = fs::read_to_string(gf).unwrap_or_default();
                for raw in text.lines() {
                    let line = raw.split(';').next().unwrap_or("").trim();
                    if line.is_empty() {
                        continue;
                    }
                    let toks: Vec<&str> = line.split_whitespace().collect();
                    let mn = if raw.starts_with(' ') || raw.starts_with('\t') {
                        toks[0]
                    } else {
                        if toks.len() < 2 {
                            continue;
                        }
                        toks[1]
                    };
                    let mn = mn.to_lowercase();
                    if A56_DIRECTIVES.contains(&mn.as_str()) {
                        continue;
                    }
                    if denominator.contains(&mn) {
                        exercised.insert(mn);
                    } else {
                        findings.push(format!(
                            "UNDECLARED EXERCISE {gtag}: the guest executes '{mn}', which the declared scope does \
                             not name — the corpus and the declaration disagree"
                        ));
                    }
                }
            }
        } else {
            let expected_files = sorted_glob(&pdir.join("guests"), ".expected.sexp");
            if expected_files.is_empty() {
                findings.push(format!(
                    "NO GUESTS {tag}: no guests/*.expected.sexp — nothing is exercised"
                ));
            }
            for ef in &expected_files {
                let etag = rel(ef, root);
                let eforms = match sexp::read_file(ef) {
                    Ok(f) => f,
                    Err(SexpError(e)) => {
                        findings.push(format!("UNREADABLE {etag}: {e}"));
                        continue;
                    }
                };
                let Some(eform) = first_form(&eforms, "expectations") else {
                    findings.push(format!("UNREADABLE {etag}: "));
                    continue;
                };
                for step in sexp::children(eform, "step").unwrap_or_default() {
                    let insn = sexp::children(step, "insn").unwrap_or_default();
                    let Some(first) = insn.first() else {
                        findings.push(format!(
                            "UNNAMED STEP {etag}: a step declares no insn — an exercised form nobody names cannot \
                             be counted"
                        ));
                        continue;
                    };
                    let text = second_text(first);
                    let text = text.trim();
                    if !text.is_empty() {
                        if let Some(mn) = text.split_whitespace().next() {
                            exercised.insert(mn.to_lowercase());
                        }
                    }
                }
            }
        }
        let unexercised: Vec<&String> = denominator.difference(&exercised).collect();
        for m in &unexercised {
            findings.push(format!(
                "UNEXERCISED {tag}: '{m}' is in the declared scope but no tracked guest executes it — coverage is \
                 {}/{}, not complete",
                denominator.len() - unexercised.len(),
                denominator.len()
            ));
        }
        if findings.is_empty() {
            out.push(format!(
                "{pdir_rel}: exercised {}/{} declared forms; SCP-02 closure {closure} resolved",
                exercised.intersection(&denominator).count(),
                denominator.len()
            ));
        }
        out.push(format!(
            "__EXERCISED__ {}/{}",
            denominator.len() - unexercised.len(),
            denominator.len()
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
        let verdict = check_coverage(self.root, Mode::Fs);
        let out = verdict.text();
        if verdict.rc != expected {
            self.fail += 1;
            self.report(format!(
                "EXERCISE-COVERAGE self-test MISS: {name} expected rc={expected} got rc={}\n{out}",
                verdict.rc
            ));
        } else if !out.contains(want) {
            self.fail += 1;
            self.report(format!("EXERCISE-COVERAGE self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}"));
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

/// The RED/GREEN controls over a scratch unit: a two-form scope over the REAL rv64i fragment (copied),
/// exercised by synthetic expectation documents. The fixture writers rebuild the unit per arm.
fn self_test(root: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(root, "target/doctrine-selftest", "exercise") else {
        eprintln!("EXERCISE-COVERAGE self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    let p = t.join("profiles/p");
    let _ = fs::create_dir_all(p.join("guests"));
    let _ = fs::create_dir_all(t.join("definitions/riscv"));
    let _ = fs::copy(
        root.join("definitions/riscv/rv64i.sexp"),
        t.join("definitions/riscv/rv64i.sexp"),
    );
    let profile = |scope: &str| {
        write(
            &p.join("profile.sexp"),
            &format!(
                "(profile (id \"p\") (version \"0\") (status \"development\") (scope {scope}))\n"
            ),
        )
    };
    let encoding = || {
        write(
            &p.join("encoding.sexp"),
            "(encoding (profile \"p\") (ilen 32) (compose (base \"riscv/rv64i\") (extensions)) (fragment-root \"definitions\"))\n",
        )
    };
    let guest = |name: &str, mnemonics: &str| {
        let mut steps = String::new();
        let mut n = 0;
        for m in mnemonics.split_whitespace() {
            steps.push_str(&format!(
                " (step (n {n}) (insn \"{m} x1, x0, 1\") (writes) (derivation \"d\") (source \"s\"))"
            ));
            n += 1;
        }
        write(
            &p.join(format!("guests/{name}.expected.sexp")),
            &format!("(expectations (program \"{name}.s\") (entry \"0x80000000\") (instructions {n}){steps})\n"),
        )
    };
    let scope2 = "(count_total 2) (authority architecture) (source \"s\") (base_op \"ADD\") (base_op \"SUB\")";
    let mut tally = Tally {
        root: &t,
        pass: 0,
        fail: 0,
        verbose,
        misses: Vec::new(),
    };

    tally.arm("REFUSE no profile dossier at all", 2, "cannot judge");

    profile(scope2);
    encoding();
    guest("g1", "add sub");
    tally.arm(
        "GREEN every declared form exercised",
        0,
        "__EXERCISED__ 2/2",
    );

    profile("(comment \"a note, not a mnemonic\") (count_total 2) (authority architecture) (source \"s\") (base_op \"ADD\") (base_op \"SUB\")");
    tally.arm(
        "GREEN a comment inside scope does not poison the denominator",
        0,
        "__EXERCISED__ 2/2",
    );

    guest("g1", "add");
    tally.arm(
        "RED   a declared form no guest exercises, named",
        1,
        "UNEXERCISED",
    );

    profile("(count_total 3) (authority architecture) (source \"s\") (base_op \"ADD\") (base_op \"SUB\")");
    tally.arm(
        "RED   a count_total that contradicts the enumeration",
        1,
        "DENOMINATOR LIE",
    );

    profile(scope2);
    let _ = fs::remove_file(p.join("encoding.sexp"));
    tally.arm(
        "RED   a scope whose composition is absent",
        1,
        "NO COMPOSITION",
    );

    encoding();
    profile("((count_total 1) (authority architecture) (source \"s\") (base_op \"MUL\"))");
    guest("g1", "mul");
    tally.arm(
        "RED   a declared form the composition does not provide (SCP-02)",
        1,
        "UNRESOLVED FORM",
    );

    let _ = fs::copy(
        root.join("definitions/riscv/zicsr.sexp"),
        t.join("definitions/riscv/zicsr.sexp"),
    );
    let _ = fs::copy(
        root.join("definitions/riscv/zicntr.sexp"),
        t.join("definitions/riscv/zicntr.sexp"),
    );
    write(
        &p.join("encoding.sexp"),
        "(encoding (profile \"p\") (ilen 32) (compose (base \"riscv/rv64i\") (extensions \"riscv/zicsr\" \"riscv/zicntr\")) (fragment-root \"definitions\"))\n",
    );
    profile("(count_total 3) (authority architecture) (source \"s\") (base_op \"ADD\") (base_op \"SUB\") (zicntr_counters \"RDCYCLE\")");
    guest("g1", "add sub rdcycle");
    tally.arm(
        "GREEN a scope form the composition provides as a pseudo resolves",
        0,
        "__EXERCISED__ 3/3",
    );
    write(
        &t.join("definitions/riscv/zicntr.sexp"),
        "(fragment (id \"riscv/zicntr\") (kind extension))\n",
    );
    tally.arm(
        "RED   a pseudo-only form the composition no longer provides, named",
        1,
        "UNRESOLVED FORM",
    );
    let _ = fs::remove_file(t.join("definitions/riscv/zicsr.sexp"));
    let _ = fs::remove_file(t.join("definitions/riscv/zicntr.sexp"));
    encoding();

    let _ = fs::remove_dir_all(p.join("guests"));
    let _ = fs::create_dir_all(p.join("guests"));
    profile(scope2);
    tally.arm("RED   a unit with no guests at all", 1, "NO GUESTS");

    let profile_cp = |scope: &str| {
        write(
            &p.join("profile.sexp"),
            &format!("(profile (id \"p\") (version \"0\") (status \"experimental\") (vehicle (route sibling-crate) (comparison checkpoint-end-state) (authority laboratory) (source \"s\")) (scope {scope}))\n"),
        )
    };
    let guest_a56 = |name: &str, lines: &str| {
        write(
            &p.join(format!("guests/{name}.a56")),
            &format!("\torg\tp:$100\nstart\t{lines}\n"),
        )
    };
    let _ = fs::remove_file(p.join("encoding.sexp"));
    profile_cp(
        "(count_total 2) (authority architecture) (source \"s\") (moves \"move\") (flow \"nop\")",
    );
    guest_a56("g1", "move #$1,x0\n\tnop");
    tally.arm(
        "GREEN checkpoint unit: the .a56 corpus covers the declared scope",
        0,
        "__EXERCISED__ 2/2",
    );

    profile_cp("(count_total 3) (authority architecture) (source \"s\") (moves \"move\") (flow \"nop\") (flow \"jmp\")");
    tally.arm(
        "RED   a declared form no .a56 guest executes, named",
        1,
        "UNEXERCISED",
    );

    profile_cp(
        "(count_total 2) (authority architecture) (source \"s\") (moves \"move\") (flow \"nop\")",
    );
    guest_a56("g1", "move #$1,x0\n\tjmp done");
    tally.arm(
        "RED   a guest instruction the scope does not name",
        1,
        "UNDECLARED EXERCISE",
    );

    guest_a56("g1", "move #$1,x0\n\tnop");
    let _ = fs::remove_file(p.join("guests/g1.a56"));
    tally.arm(
        "RED   checkpoint declared but no .a56 guests",
        1,
        "NO GUESTS",
    );

    guest_a56("g1", "move #$1,x0\n\tnop");
    profile_cp(
        "(count_total 2) (authority architecture) (source \"s\") (moves \"move\") (flow \"nop\")",
    );
    tally.arm(
        "GREEN checkpoint with no encoding.sexp — the composition leg is n/a, not RED",
        0,
        "checkpoint-end-state declared",
    );

    let profile_dev = |scope: &str| {
        write(
            &p.join("profile.sexp"),
            &format!("(profile (id \"p\") (version \"0\") (status \"experimental\") (vehicle (route device-model) (comparison register-expectations) (authority laboratory) (source \"s\")) (scope {scope}))\n"),
        )
    };
    let _ = fs::remove_file(p.join("guests/g1.a56"));
    profile_dev("(count_total 2) (authority platform) (source \"s\") (mmio_registers \"UART_RXDATA\") (mmio_registers \"UART_TXDATA\")");
    tally.arm(
        "GREEN device-model route: exercise n/a by declaration, the unit named",
        0,
        "profiles/p: device-model route declared",
    );

    encoding();
    tally.arm(
        "RED   device-model contradicted by an encoding.sexp",
        1,
        "contradicts the documents",
    );

    let _ = fs::remove_file(p.join("encoding.sexp"));
    guest("g1", "add sub");
    tally.arm(
        "RED   device-model contradicted by a guests/ corpus (anti-drift)",
        1,
        "the declaration and the documents disagree",
    );

    let _ = fs::remove_file(p.join("guests/g1.expected.sexp"));
    profile_dev("(count_total 3) (authority platform) (source \"s\") (mmio_registers \"UART_RXDATA\") (mmio_registers \"UART_TXDATA\")");
    tally.arm(
        "RED   a device scope whose count contradicts its own enumeration",
        1,
        "DENOMINATOR LIE",
    );

    let profile_res = |scope: &str| {
        write(
            &p.join("profile.sexp"),
            &format!("(profile (id \"p\") (version \"0\") (status \"development\") (vehicle (route profile-resolution) (authority laboratory) (source \"s\")) (scope {scope}))\n"),
        )
    };
    profile_res("(count_total 1) (authority architecture) (source \"s\") (base_op \"add\")");
    tally.arm(
        "GREEN profile-resolution route: composition and exercise n/a by declaration",
        0,
        "profiles/p: profile-resolution route declared",
    );

    encoding();
    tally.arm(
        "RED   profile-resolution contradicted by an encoding.sexp",
        1,
        "contradicts the documents",
    );
    let _ = fs::remove_file(p.join("encoding.sexp"));

    guest("g1", "add sub");
    tally.arm(
        "RED   profile-resolution contradicted by a guests/ corpus (anti-drift)",
        1,
        "the declaration and the documents disagree",
    );
    let _ = fs::remove_file(p.join("guests/g1.expected.sexp"));

    profile_res("(count_total 2) (authority architecture) (source \"s\") (base_op \"add\")");
    tally.arm(
        "RED   a resolution scope whose count contradicts its own enumeration",
        1,
        "DENOMINATOR LIE",
    );

    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "EXERCISE-COVERAGE --self-test: {} pass / {} fail",
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

/// `cargo xtask check-exercise-coverage [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !crate::harness::on_path("git") {
        eprintln!("EXERCISE-COVERAGE: REFUSED — git is not on PATH; this check cannot judge.");
        return ExitCode::from(2);
    }
    if !self_test(root, false) {
        eprintln!(
            "EXERCISE-COVERAGE: REFUSED — the check does not discriminate (self-test failed)."
        );
        return ExitCode::from(2);
    }
    let verdict = check_coverage(root, Mode::Git);
    let count: Vec<&str> = verdict
        .lines
        .iter()
        .filter_map(|l| l.strip_prefix("__CHECKED__ "))
        .collect();
    let exercised: Vec<&str> = verdict
        .lines
        .iter()
        .filter_map(|l| l.strip_prefix("__EXERCISED__ "))
        .collect();
    let body: Vec<&str> = verdict
        .lines
        .iter()
        .filter(|l| !l.starts_with("__CHECKED__ ") && !l.starts_with("__EXERCISED__ "))
        .map(String::as_str)
        .collect();
    let exercised_text = if exercised.is_empty() {
        "?".to_owned()
    } else {
        exercised.join("\n")
    };
    match verdict.rc {
        2 => {
            eprintln!("EXERCISE-COVERAGE: REFUSED — the profile corpus could not be read.");
            for line in &body {
                eprintln!("  {line}");
            }
            ExitCode::from(2)
        }
        0 => {
            println!(
                "EXERCISE-COVERAGE: ok ({} profile(s) — every declared form exercised, {exercised_text})",
                count.first().copied().unwrap_or("0")
            );
            ExitCode::SUCCESS
        }
        rc => {
            eprintln!("EXERCISE-COVERAGE: the declared scope is not fully exercised (coverage {exercised_text}).");
            for line in &body {
                eprintln!("  {line}");
            }
            eprintln!("  Every declared form must run under the laboratory — exercise it or shrink the declaration.");
            ExitCode::from(u8::try_from(rc).unwrap_or(1))
        }
    }
}
