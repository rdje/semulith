//! The `SCOPE-COVERAGE` doctrine, ported from `scripts/check_scope_coverage.sh` (`XTASK.6` slice `6p`), which is now
//! a shim of `cargo xtask check-scope-coverage`.
//!
//! The director's rule, mechanized (`MODEL-METHOD.6`): no model implementation for a profile while a category its
//! DECLARED SCOPE requires is `missing`. The unit registry (`materials/units.sexp`) declares, per unit, the categories
//! its scope REQUIRES; the census (`materials/category-needs.sexp`) declares what each category's disposition is. This
//! gate refuses the day a required category is `missing` — or has no census row at all — because model code built on
//! a category whose facts are not extractable is code built on an intention. It composes with `EXTRACTION`
//! (`MODEL-METHOD.10`) and does not duplicate it: coverage says the category's facts are OWNED, extraction says they
//! are EXTRACTABLE. The script's inline Python is ported line for line over the one record mapping (`records.rs`);
//! each self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode};

use crate::harness::scratch;
use crate::records::{self, Value};

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

/// The unit registries: the tracked one under `git`, the one on disk under `fs` (the self-test's fixture tree).
fn registries(root: &Path, mode: Mode) -> Vec<PathBuf> {
    match mode {
        Mode::Git => Command::new("git")
            .args(["ls-files", "--", "materials/units.sexp"])
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
            let registry = root.join("materials/units.sexp");
            if registry.exists() {
                vec![registry]
            } else {
                Vec::new()
            }
        }
    }
}

/// Python's `str()` of a field the mapping read: the text of a string, `None` for an absent one.
fn shown(value: Option<&Value>) -> String {
    match value {
        None | Some(Value::Null) => "None".to_owned(),
        Some(Value::Str(s)) => s.clone(),
        Some(Value::Int(n)) => n.to_string(),
        Some(Value::Bool(true)) => "True".to_owned(),
        Some(Value::Bool(false)) => "False".to_owned(),
        Some(other) => records::json_dumps(other),
    }
}

fn relative(path: &Path, root: &Path) -> String {
    path.strip_prefix(root)
        .unwrap_or(path)
        .display()
        .to_string()
}

fn file_name(path: &Path) -> String {
    path.file_name()
        .map(|n| n.to_string_lossy().into_owned())
        .unwrap_or_default()
}

/// A census row's key, `(unit, category)` as the mapping read them — absent fields stay absent, as Python's `None`.
type NeedKey = (Option<Value>, Option<Value>);

/// The dispositions the gate can judge besides `missing`.
const JUDGED: [&str; 4] = ["covered", "partial", "out-of-scope", "deferred-to-board"];

/// The inline Python, line for line: every unit's declared scope against the census beside its registry.
fn check_coverage(root: &Path, mode: Mode) -> Verdict {
    let regs = registries(root, mode);
    if regs.is_empty() {
        return Verdict {
            rc: 2,
            lines: vec![
                "SCOPE-COVERAGE: REFUSED — no unit registry found; this check cannot judge"
                    .to_owned(),
                "__CHECKED__ 0".to_owned(),
            ],
        };
    }
    let mut findings: Vec<String> = Vec::new();
    let mut checked = 0u32;
    for reg in &regs {
        let units = match records::load(reg, root) {
            Ok(units) => units,
            Err(e) => {
                findings.push(format!("UNREADABLE {}: {e}", relative(reg, root)));
                continue;
            }
        };
        let needs_path = reg.parent().unwrap_or(root).join("category-needs.sexp");
        // (unit, category) → the row; a later row replaces an earlier one, as the dict comprehension did.
        let mut needs: Vec<(NeedKey, Value)> = Vec::new();
        if needs_path.is_file() {
            match records::load(&needs_path, root) {
                Ok(rows) => {
                    for n in rows {
                        let key = (n.get("unit").cloned(), n.get("category").cloned());
                        needs.retain(|(k, _)| k != &key);
                        needs.push((key, n));
                    }
                }
                Err(_) => findings.push(format!(
                    "UNREADABLE {}: the census beside the registry does not map — coverage against a census nobody can read proves nothing",
                    relative(&needs_path, root)
                )),
            }
        } else {
            findings.push(format!(
                "NO CENSUS {}: no category-needs.sexp beside the registry — required categories cannot be checked without it",
                relative(reg, root)
            ));
        }
        let name = file_name(reg);
        for u in &units {
            checked += 1;
            let uid = u.get("id");
            let required: &[Value] = match u.get("requires") {
                Some(Value::List(items)) => items,
                _ => &[],
            };
            if required.is_empty() {
                findings.push(format!(
                    "UNDECLARED SCOPE {name} [{}]: the unit declares no required categories — model code may not start against a scope that was never declared",
                    shown(uid)
                ));
                continue;
            }
            for cat in required {
                let key = (uid.cloned(), Some(cat.clone()));
                let Some((_, row)) = needs.iter().find(|(k, _)| k == &key) else {
                    findings.push(format!(
                        "UNCOVERED REQUIRED {name} [{} requires {}]: no census row at all — the declared scope is uncovered",
                        shown(uid),
                        shown(Some(cat))
                    ));
                    continue;
                };
                match row.get("disposition") {
                    Some(Value::Str(d)) if d == "missing" => findings.push(format!(
                        "MISSING REQUIRED {name} [{} requires {}]: the census disposition is 'missing' — model code may not start against a category the unit's scope requires and the catalogue lacks. Close the gap or shrink the declaration.",
                        shown(uid),
                        shown(Some(cat))
                    )),
                    Some(Value::Str(d)) if JUDGED.contains(&d.as_str()) => {}
                    other => findings.push(format!(
                        "UNKNOWN DISPOSITION {name} [{} requires {}]: '{}' is not a disposition the gate can judge",
                        shown(uid),
                        shown(Some(cat)),
                        shown(other)
                    )),
                }
            }
        }
    }
    let mut lines = findings.clone();
    lines.push(format!("__CHECKED__ {checked}"));
    Verdict {
        rc: i32::from(!findings.is_empty()),
        lines,
    }
}

struct Tally<'a> {
    root: &'a Path,
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally<'_> {
    /// One arm: judging the fixture tree must give `expected` and contain `want`.
    fn arm(&mut self, name: &str, expected: i32, want: &str) {
        let verdict = check_coverage(self.root, Mode::Fs);
        let out = verdict.text();
        if verdict.rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!(
                    "SCOPE-COVERAGE self-test MISS: {name} expected rc={expected} got rc={}\n{out}",
                    verdict.rc
                );
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("SCOPE-COVERAGE self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }
}

/// `printf '%s\n' "$1" > file`.
fn write(path: &Path, text: &str) {
    let _ = fs::write(path, format!("{text}\n"));
}

/// The RED/GREEN controls: a scratch registry and census, as the script wrote them.
fn self_test(root: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(root, "target/doctrine-selftest", "scopecov") else {
        eprintln!("SCOPE-COVERAGE self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    let _ = fs::create_dir_all(t.join("materials"));
    let units_path = t.join("materials/units.sexp");
    let needs_path = t.join("materials/category-needs.sexp");
    let units = |text: &str| write(&units_path, text);
    let needs = |text: &str| write(&needs_path, text);
    let mut tally = Tally {
        root: &t,
        pass: 0,
        fail: 0,
        verbose,
    };
    let _ = fs::remove_file(&units_path);
    let _ = fs::remove_file(&needs_path);
    tally.arm("REFUSE no unit registry at all", 2, "cannot judge");
    units("(unit (id \"p\") (kind processor) (layer processor) (book \"b\") (requires \"C01\"))");
    let _ = fs::remove_file(&needs_path);
    tally.arm("REFUSE a registry with no census beside it", 1, "NO CENSUS");
    needs("(category-need (category \"C01\") (layer processor) (kind k) (unit \"p\") (disposition covered) (material \"M\"))");
    tally.arm("GREEN a required category covered", 0, "__CHECKED__ 1");
    needs("(category-need (category \"C01\") (layer processor) (kind k) (unit \"p\") (disposition missing) (reason \"owed\"))");
    tally.arm(
        "RED   the acceptance's shape: a required category missing",
        1,
        "MISSING REQUIRED",
    );
    needs("(category-need (category \"C99\") (layer processor) (kind k) (unit \"p\") (disposition covered) (material \"M\"))");
    tally.arm(
        "RED   a required category with no census row",
        1,
        "UNCOVERED REQUIRED",
    );
    units("(unit (id \"p\") (kind processor) (layer processor) (book \"b\"))");
    tally.arm("RED   a unit that declares no scope", 1, "UNDECLARED SCOPE");
    units("(unit (id \"p\") (kind processor) (layer processor) (book \"b\") (requires \"C01\"))");
    needs("(category-need (category \"C01\") (layer processor) (kind k) (unit \"p\") (disposition covered) (material \"M\"))\n(category-need (category \"C07\") (layer processor) (kind k) (unit \"p\") (disposition missing) (reason \"excluded subsystem\"))");
    tally.arm(
        "GREEN a missing category the scope does NOT require is legal",
        0,
        "__CHECKED__ 1",
    );
    // Every repeated requires field participates, not only the first child.
    units("(unit (id \"p\") (kind processor) (layer processor) (book \"b\") (requires \"C01\") (requires \"C07\"))");
    needs("(category-need (category \"C01\") (layer processor) (kind k) (unit \"p\") (disposition covered) (material \"M\"))\n(category-need (category \"C07\") (layer processor) (kind k) (unit \"p\") (disposition covered) (material \"M\"))");
    tally.arm(
        "GREEN every repeated required category is covered",
        0,
        "__CHECKED__ 1",
    );
    needs("(category-need (category \"C01\") (layer processor) (kind k) (unit \"p\") (disposition covered) (material \"M\"))\n(category-need (category \"C07\") (layer processor) (kind k) (unit \"p\") (disposition missing) (reason \"owed\"))");
    tally.arm(
        "RED   later repeated required category is missing",
        1,
        "p requires C07",
    );
    needs("(category-need (category \"C01\") (layer processor) (kind k) (unit \"p\") (disposition covered) (material \"M\"))");
    tally.arm(
        "RED   later repeated required category has no census row",
        1,
        "p requires C07",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "SCOPE-COVERAGE --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// `cargo xtask check-scope-coverage [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !self_test(root, false) {
        eprintln!("SCOPE-COVERAGE: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let verdict = check_coverage(root, Mode::Git);
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
            eprintln!("SCOPE-COVERAGE: REFUSED — the unit corpus could not be read.");
            for line in &body {
                eprintln!("  {line}");
            }
            ExitCode::from(2)
        }
        0 => {
            println!(
                "SCOPE-COVERAGE: ok ({count} unit(s) may code — every required category covered)"
            );
            ExitCode::SUCCESS
        }
        _ => {
            eprintln!(
                "SCOPE-COVERAGE: model code may not start — the declared scope is uncovered."
            );
            for line in &body {
                eprintln!("  {line}");
            }
            eprintln!(
                "  The declaration is the authority. Close the gap or shrink the declaration."
            );
            ExitCode::from(1)
        }
    }
}
