//! The `DOSSIER-SCHEMA` doctrine's driver, ported from `scripts/check_dossier_schema.sh` (`XTASK.6` slice `6ao`), which
//! is now a shim of `cargo xtask check-dossier-schema`.
//!
//! Every tracked `profiles/*/*.sexp` whose basename (or suffix family) has a same-named `schema/*.sexp` validates against
//! it through the one checker, `scripts/check_sexp_schema.py`; a document with no schema is skipped and counted BY NAME.
//! The sweep is the driver's inline Python (`check_tree`, over the pinned `dossier_sexp`); it runs verbatim through
//! `python3 -`, as the script ran it, and is not ported — nor are the three probes the controls run (the experiment
//! verification cases, the expectation mapping and its mutation, the bounded-artifact suite plain and `-O` under its
//! ten omissions), each spawned as the script spawned them. Each self-test arm is one `tally.arm(` call, unrolled as the
//! script's were, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::io::Write;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{combined, on_path, scratch};

const CHECKER: &str = "scripts/check_sexp_schema.py";

/// The sweep, verbatim: `python3 - <root> <git|fs> <checker>` — the findings, then `__VALIDATED__ N __SKIPPED__ M (…)`;
/// exit 1 on a finding.
const SWEEP: &str = r####"import subprocess, sys
from pathlib import Path

root = Path(sys.argv[1]); mode = sys.argv[2]
checker = Path(sys.argv[3])
sys.path.insert(0, str(checker.parent))
import dossier_sexp as D
if mode == "git":
    out = subprocess.run(["git", "ls-files", "--", "profiles/*/*.sexp"],
                         capture_output=True, text=True, check=True).stdout
    docs = [root / p for p in out.splitlines() if p.strip()]
else:
    docs = sorted((root / "profiles").glob("*/*.sexp"))

findings, validated, skipped = [], [], []
# Suffixed documents map to their family schema: expectations, overrides and
# obligation-catalog parts. Everything else needs a
# same-named schema or it is skipped — and counted by name in the verdict.
SUFFIX_SCHEMAS = ((".expected.sexp", "expectations.sexp"),
                  (".override.sexp", "override.sexp"),
                  (".obligations.sexp", "contract-obligations.sexp"))
for doc in sorted(docs):
    schema_name = doc.name
    for suffix, family in SUFFIX_SCHEMAS:
        if doc.name.endswith(suffix):
            schema_name = family
            break
    schema = root / "schema" / schema_name
    tag = doc.relative_to(root).as_posix()
    if not schema.is_file():
        skipped.append(doc.name)
        continue
    r = subprocess.run([sys.executable, str(checker), str(doc), str(schema)],
                       capture_output=True, text=True)
    if r.returncode == 2:
        findings.append(f"CANNOT JUDGE {tag}: {(r.stderr or r.stdout).strip()}")
    elif r.returncode != 0:
        findings.append(f"REFUSED {tag}: {(r.stderr or r.stdout).strip().splitlines()[0]}")
    elif doc.name.endswith(".expected.sexp"):
        try:
            D.load_expectations(doc)  # Reject duplicate dynamic write keys before dict collapse.
        except D.DossierError as exc:
            findings.append(f"REFUSED {tag}: {exc}")
        else:
            validated.append(tag)
    else:
        validated.append(tag)
for f in findings:
    print(f)
print(f"__VALIDATED__ {len(validated)} __SKIPPED__ {len(skipped)} "
      f"({', '.join(sorted(set(skipped))) if skipped else 'none'})")
sys.exit(1 if findings else 0)
"####;

/// The self-test's minimal schema with one facet: `id` must match `^p[0-9]+$`.
const FACET_SCHEMA: &str = "(schema (id \"profile\"))\n(construct (name profile)\n  (field (name id) (type string) (pattern \"^p[0-9]+$\")))\n";

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

/// `check_tree <root> <mode>`: the sweep on stdin, the checker's absolute path as its third argument, from the repository
/// root. `merge_stderr` is the arms' `2>&1`; without it the sweep's stderr passes through as the real run let it.
fn check_tree(repo: &Path, root: &Path, mode: &str, merge_stderr: bool) -> (i32, String) {
    let mut command = Command::new("python3");
    command
        .arg("-")
        .arg(root)
        .arg(mode)
        .arg(repo.join(CHECKER))
        .current_dir(repo)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(if merge_stderr {
            Stdio::piped()
        } else {
            Stdio::inherit()
        });
    let Ok(mut child) = command.spawn() else {
        return (-1, "cannot run python3".to_owned());
    };
    if let Some(mut stdin) = child.stdin.take() {
        let _ = stdin.write_all(SWEEP.as_bytes());
    }
    match child.wait_with_output() {
        Ok(o) => {
            let mut text = String::from_utf8_lossy(&o.stdout).into_owned();
            if merge_stderr {
                text.push_str(&String::from_utf8_lossy(&o.stderr));
            }
            (o.status.code().unwrap_or(-1), text)
        }
        Err(e) => (-1, e.to_string()),
    }
}

/// `python3 [-O] "$ROOT/scripts/<probe>" <args…> 2>&1`, captured with its exit status.
fn probe(repo: &Path, optimized: bool, script: &str, args: &[&str]) -> (i32, String) {
    let mut command = Command::new("python3");
    if optimized {
        command.arg("-O");
    }
    command
        .arg(repo.join("scripts").join(script))
        .args(args)
        .current_dir(repo);
    combined(&mut command)
}

/// `verification_case <case>`: `python3 "$ROOT/scripts/probe_experiment_verification.py" --case <case> 2>&1`.
fn verification_case(repo: &Path, case: &str) -> (i32, String) {
    probe(
        repo,
        false,
        "probe_experiment_verification.py",
        &["--case", case],
    )
}

/// `artifact_case <normal|optimized> [<mutation>]`: the bounded-artifact suite, `-O` when optimized.
fn artifact_case(repo: &Path, optimized: bool, mutation: Option<&str>) -> (i32, String) {
    match mutation {
        Some(m) => probe(
            repo,
            optimized,
            "probe_matched_gpr_artifacts.py",
            &["--mutation", m],
        ),
        None => probe(repo, optimized, "probe_matched_gpr_artifacts.py", &[]),
    }
}

/// `python3 "$ROOT/scripts/probe_expectation_mapping.py" --emit <kind> > <path>`: the emitted fixture written (the
/// redirection created the file before the probe ran); the probe's stderr through when the self-test is the command.
fn emit_fixture(repo: &Path, kind: &str, path: &Path, verbose: bool) {
    let output = Command::new("python3")
        .arg(repo.join("scripts/probe_expectation_mapping.py"))
        .arg("--emit")
        .arg(kind)
        .current_dir(repo)
        .stdin(Stdio::null())
        .stderr(if verbose {
            Stdio::inherit()
        } else {
            Stdio::null()
        })
        .output();
    let _ = fs::write(path, output.map(|o| o.stdout).unwrap_or_default());
}

struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
    /// Every missed arm's report, for a quiet run's refusal (`XTASK.12`).
    misses: Vec<String>,
}

impl Tally {
    /// A missed arm's report: printed at once in a verbose run, kept for a quiet run's refusal (`XTASK.12`).
    fn report(&mut self, report: String) {
        if self.verbose {
            eprintln!("{report}");
        }
        self.misses.push(report);
    }
    /// One arm: the exit status must be `expected` and the captured output must contain `want`.
    fn arm(&mut self, name: &str, rc: i32, expected: i32, out: &str, want: &str) {
        if rc == expected && out.contains(want) {
            self.pass += 1;
        } else {
            self.fail += 1;
            self.report(format!("DOSSIER-SCHEMA self-test MISS: {name} — expected rc={expected} (reason: {want}), got rc={rc}\n{out}"));
        }
    }
}

/// The RED/GREEN controls against synthetic fixtures and the three probes. Quiet unless `verbose` (the script ran it
/// `>/dev/null 2>&1` before the real judgement).
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "dossierschema") else {
        if verbose {
            eprintln!("DOSSIER-SCHEMA self-test: cannot create a scratch directory under target/doctrine-selftest");
        }
        return false;
    };
    let _ = fs::create_dir_all(t.join("profiles/p"));
    let _ = fs::create_dir_all(t.join("schema"));
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
        misses: Vec::new(),
    };
    let profile = t.join("profiles/p/profile.sexp");
    let _ = fs::write(t.join("schema/profile.sexp"), FACET_SCHEMA);
    let _ = fs::write(&profile, "(profile (id \"p1\"))\n");
    let (rc, out) = check_tree(repo, &t, "fs", true);
    tally.arm(
        "GREEN a conforming document validates",
        rc,
        0,
        captured(&out),
        "__VALIDATED__ 1",
    );
    let _ = fs::write(&profile, "(profile (id \"nope\"))\n");
    let (rc, out) = check_tree(repo, &t, "fs", true);
    tally.arm(
        "RED a facet violation is refused, naming it",
        rc,
        1,
        captured(&out),
        "does not match",
    );
    let _ = fs::write(&profile, "(profile (id \"p1\"))\n");
    let _ = fs::write(
        t.join("profiles/p/baseline.sexp"),
        "(baseline (note \"no same-named schema\"))\n",
    );
    let (rc, out) = check_tree(repo, &t, "fs", true);
    tally.arm(
        "GREEN a document with no same-named schema is skipped BY NAME",
        rc,
        0,
        captured(&out),
        "__SKIPPED__ 1 (baseline.sexp)",
    );
    // The real references schema and single mapper, with memory-only synthetic data.
    let (rc, out) = verification_case(repo, "complete");
    tally.arm(
        "GREEN complete structured verification",
        rc,
        0,
        captured(&out),
        "VERIFICATION complete: ok",
    );
    let (rc, out) = verification_case(repo, "roundtrip");
    tally.arm(
        "GREEN nested verification roundtrip preserves every record and argv",
        rc,
        0,
        captured(&out),
        "VERIFICATION roundtrip: ok",
    );
    let (rc, out) = verification_case(repo, "legacy");
    tally.arm(
        "GREEN legacy references retain their dictionary shape",
        rc,
        0,
        captured(&out),
        "VERIFICATION legacy: ok",
    );
    let (rc, out) = verification_case(repo, "unknown");
    tally.arm(
        "RED verification unknown fields at every depth",
        rc,
        0,
        captured(&out),
        "VERIFICATION unknown: ok",
    );
    let (rc, out) = verification_case(repo, "type");
    tally.arm(
        "RED verification wrong scalar types at every depth",
        rc,
        0,
        captured(&out),
        "VERIFICATION type: ok",
    );
    let (rc, out) = verification_case(repo, "arity");
    tally.arm(
        "RED verification wrong scalar arity at every depth",
        rc,
        0,
        captured(&out),
        "VERIFICATION arity: ok",
    );
    let (rc, out) = verification_case(repo, "duplicate");
    tally.arm(
        "RED verification duplicate singular fields at every depth",
        rc,
        0,
        captured(&out),
        "VERIFICATION duplicate: ok",
    );
    let (rc, out) = verification_case(repo, "missing");
    tally.arm(
        "RED verification missing required fields at every depth",
        rc,
        0,
        captured(&out),
        "VERIFICATION missing: ok",
    );
    let (rc, out) = verification_case(repo, "collection");
    tally.arm(
        "RED verification empty required collections",
        rc,
        0,
        captured(&out),
        "VERIFICATION collection: ok",
    );
    let (rc, out) = verification_case(repo, "digest");
    tally.arm(
        "RED verification malformed input and observation digests",
        rc,
        0,
        captured(&out),
        "VERIFICATION digest: ok",
    );
    let (rc, out) = verification_case(repo, "version");
    tally.arm(
        "RED verification unsupported method version",
        rc,
        0,
        captured(&out),
        "VERIFICATION version: ok",
    );
    let (rc, out) = verification_case(repo, "unique");
    tally.arm(
        "RED verification repeated identity-list entries",
        rc,
        0,
        captured(&out),
        "VERIFICATION unique: ok",
    );
    let (rc, out) = verification_case(repo, "vocabulary");
    tally.arm(
        "RED verification unsupported closed vocabularies",
        rc,
        0,
        captured(&out),
        "VERIFICATION vocabulary: ok",
    );
    let (rc, out) = verification_case(repo, "mapper-refusal");
    tally.arm(
        "RED mapper unknown nested fields and duplicate blocks",
        rc,
        0,
        captured(&out),
        "VERIFICATION mapper-refusal: ok",
    );
    let (rc, out) = verification_case(repo, "locators");
    tally.arm(
        "GREEN typed witness and baseline roundtrip preserves values",
        rc,
        0,
        captured(&out),
        "VERIFICATION locators: ok",
    );
    let (rc, out) = verification_case(repo, "locator-shape");
    tally.arm(
        "RED malformed witness and baseline fields refuse by shape",
        rc,
        0,
        captured(&out),
        "VERIFICATION locator-shape: ok",
    );
    let (rc, out) = verification_case(repo, "locator-mapper");
    tally.arm(
        "RED mapper refuses unknown or repeated witness children",
        rc,
        0,
        captured(&out),
        "VERIFICATION locator-mapper: ok",
    );
    // Shape permits repeated write forms; the mapping boundary enforces key identity.
    let _ = fs::copy(
        repo.join("schema/expectations.sexp"),
        t.join("schema/expectations.sexp"),
    );
    let fixture = t.join("profiles/p/fixture.expected.sexp");
    emit_fixture(repo, "positive", &fixture, verbose);
    let (rc, out) = check_tree(repo, &t, "fs", true);
    tally.arm(
        "GREEN valid expectation keys pass shape and mapping",
        rc,
        0,
        captured(&out),
        "__VALIDATED__ 2",
    );
    emit_fixture(repo, "conflicting", &fixture, verbose);
    let (rc, out) = check_tree(repo, &t, "fs", true);
    tally.arm(
        "RED conflicting expectation keys refuse before dict collapse",
        rc,
        1,
        captured(&out),
        "duplicate write register 'x1'",
    );
    emit_fixture(repo, "identical", &fixture, verbose);
    let (rc, out) = check_tree(repo, &t, "fs", true);
    tally.arm(
        "RED identical repeated expectation keys also refuse",
        rc,
        1,
        captured(&out),
        "duplicate write register 'x1'",
    );
    let (rc, out) = probe(repo, false, "probe_expectation_mapping.py", &[]);
    tally.arm(
        "GREEN lossless expectation mapping and loader controls",
        rc,
        0,
        captured(&out),
        "EXPECTATION-MAPPING: 12 pass / 0 fail; fixture cleaned",
    );
    let (rc, out) = probe(
        repo,
        false,
        "probe_expectation_mapping.py",
        &["--mutation", "ignore-duplicate-writes"],
    );
    tally.arm(
        "RED removed expectation key guard exposes conflicting input",
        rc,
        1,
        captured(&out),
        "EXPECTATION MISS conflicting keys: duplicate write accepted",
    );
    // Bytes-only artifact checks. No canonical capture exists: these controls do not extend the one-level
    // tracked-dossier sweep into a future retention store.
    let (rc, out) = artifact_case(repo, false, None);
    tally.arm(
        "GREEN bounded artifacts normal",
        rc,
        0,
        captured(&out),
        "Ran 36 tests",
    );
    let (rc, out) = artifact_case(repo, false, Some("no-facets"));
    tally.arm(
        "RED normal artifact no-facets omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=3)",
    );
    let (rc, out) = artifact_case(repo, false, Some("no-root-count"));
    tally.arm(
        "RED normal artifact no-root-count omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=1)",
    );
    let (rc, out) = artifact_case(repo, false, Some("no-path"));
    tally.arm(
        "RED normal artifact no-path omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=2)",
    );
    let (rc, out) = artifact_case(repo, false, Some("no-manifest-limit"));
    tally.arm(
        "RED normal artifact no-manifest-limit omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=1)",
    );
    let (rc, out) = artifact_case(repo, false, Some("no-nested-manifest"));
    tally.arm(
        "RED normal artifact no-nested-manifest omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=1)",
    );
    let (rc, out) = artifact_case(repo, false, Some("no-byte-bound"));
    tally.arm(
        "RED normal artifact no-byte-bound omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=3)",
    );
    let (rc, out) = artifact_case(repo, false, Some("no-identity"));
    tally.arm(
        "RED normal artifact no-identity omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=4)",
    );
    let (rc, out) = artifact_case(repo, false, Some("no-manifest-edges"));
    tally.arm(
        "RED normal artifact no-manifest-edges omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=1)",
    );
    let (rc, out) = artifact_case(repo, false, Some("no-output-set"));
    tally.arm(
        "RED normal artifact no-output-set omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=1)",
    );
    let (rc, out) = artifact_case(repo, false, Some("no-collector-edge"));
    tally.arm(
        "RED normal artifact no-collector-edge omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=1)",
    );
    let (rc, out) = artifact_case(repo, true, None);
    tally.arm(
        "GREEN bounded artifacts optimized",
        rc,
        0,
        captured(&out),
        "Ran 36 tests",
    );
    let (rc, out) = artifact_case(repo, true, Some("no-facets"));
    tally.arm(
        "RED optimized artifact no-facets omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=3)",
    );
    let (rc, out) = artifact_case(repo, true, Some("no-root-count"));
    tally.arm(
        "RED optimized artifact no-root-count omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=1)",
    );
    let (rc, out) = artifact_case(repo, true, Some("no-path"));
    tally.arm(
        "RED optimized artifact no-path omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=2)",
    );
    let (rc, out) = artifact_case(repo, true, Some("no-manifest-limit"));
    tally.arm(
        "RED optimized artifact no-manifest-limit omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=1)",
    );
    let (rc, out) = artifact_case(repo, true, Some("no-nested-manifest"));
    tally.arm(
        "RED optimized artifact no-nested-manifest omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=1)",
    );
    let (rc, out) = artifact_case(repo, true, Some("no-byte-bound"));
    tally.arm(
        "RED optimized artifact no-byte-bound omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=3)",
    );
    let (rc, out) = artifact_case(repo, true, Some("no-identity"));
    tally.arm(
        "RED optimized artifact no-identity omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=4)",
    );
    let (rc, out) = artifact_case(repo, true, Some("no-manifest-edges"));
    tally.arm(
        "RED optimized artifact no-manifest-edges omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=1)",
    );
    let (rc, out) = artifact_case(repo, true, Some("no-output-set"));
    tally.arm(
        "RED optimized artifact no-output-set omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=1)",
    );
    let (rc, out) = artifact_case(repo, true, Some("no-collector-edge"));
    tally.arm(
        "RED optimized artifact no-collector-edge omission",
        rc,
        1,
        captured(&out),
        "FAILED (failures=1)",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "DOSSIER-SCHEMA --self-test: {} pass / {} fail",
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

/// `cargo xtask check-dossier-schema [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    // `command -v python3`
    if !on_path("python3") {
        eprintln!("DOSSIER-SCHEMA: REFUSED — python3 is not on PATH; this check cannot judge.");
        return ExitCode::from(2);
    }
    if !root.join(CHECKER).is_file() {
        eprintln!(
            "DOSSIER-SCHEMA: REFUSED — the schema checker is missing; this gate cannot judge."
        );
        return ExitCode::from(2);
    }
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    // Re-run the controls before judging: a check that no longer discriminates must refuse, not pass.
    if !self_test(root, false) {
        eprintln!("DOSSIER-SCHEMA: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    // `out="$(check_tree "$ROOT" git)"`: stdout captured, stderr through.
    let (rc, raw) = check_tree(root, root, "git", false);
    let out = captured(&raw);
    if rc != 0 {
        eprintln!("DOSSIER-SCHEMA: a dossier document violates its schema.");
        for line in out.lines().filter(|l| !l.starts_with("__VALIDATED__")) {
            eprintln!("  {line}");
        }
        eprintln!("  The SCHEMA is the contract: fix the document, or change the schema with the");
        eprintln!("  case named — never leave the two disagreeing.");
        return ExitCode::from(1);
    }
    let summary = out
        .lines()
        .filter_map(|l| l.strip_prefix("__VALIDATED__ "))
        .collect::<Vec<_>>()
        .join("\n");
    println!("DOSSIER-SCHEMA: ok ({})", captured(&summary));
    ExitCode::SUCCESS
}
