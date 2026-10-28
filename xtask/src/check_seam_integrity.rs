//! The `SEAM-INTEGRITY` doctrine's driver, ported from `scripts/check_seam_integrity.sh` (`XTASK.6` slice `6au`), which
//! is now a shim of `cargo xtask check-seam-integrity`.
//!
//! Three defects of the neutral spine checks are fixed here through the `.doctrine/` seams, and a fix whose
//! disappearance is undetectable is not a fix. So the seams' BEHAVIOUR is asserted over the repository's own history:
//! R1 the neutral acceptance check still consumes both seam files; R2 every current tracked hard-gated acceptance box
//! still matches the effective signature set; R3 no prose file is classified as a code change; R4 every behaviour-
//! governing path family is; R5 every instrument the census gate accepts is accepted as evidence too. The effective
//! rules are asked of their owner (`scripts/check_task_acceptance.sh --print-sig`, `--print-code-re`), the built-in
//! defaults extracted from its text as the script's `sed` did, the census list from `scripts/check_gap_claims.sh`'s
//! text; the box scoper is the script's `awk` program, run verbatim per file, and every pattern test is the shell's own
//! `grep -E`, spawned as the script spawned it. Each self-test score is one `tally.score(` call, the idiom the
//! `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::io::Write;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::scratch;

const NEUTRAL: &str = "scripts/check_task_acceptance.sh";
const TOKENS: &str = ".doctrine/evidence_tokens.txt";
const PATHS: &str = ".doctrine/code_paths.txt";
/// Prose families that must never be classified as a code change here.
const PROSE_PATHS: &str = "^docs/book/src/";
/// Path families that MUST be classified as a code change: editing any of them alone changes what this repository does.
const MUST_BE_CODE: &[&str] = &[
    "^\\.githooks/",
    "^\\.github/workflows/",
    "^Cargo\\.(toml|lock)$",
    "^\\.doctrine/",
    "^doctrine/.*\\.tsv$",
    "^docs/tasks/artifacts/.*\\.sh$",
    "^scripts/.*\\.sh$",
    "^crates/",
];
/// The historical unanchored pattern, a regression fixture for the self-test only: the exact shape that classified 28
/// files of mdBook prose as a code change.
const HISTORICAL_OVERMATCH_RE: &str = "(^|/)(crates|src|scripts)/|\\.(rs|sh)$|(^|/)Makefile$";
/// `boxes_regression`'s scoper, verbatim: each hard-gated ticked box's own bullet, then `\036`.
const BOX_SCOPER: &str = r####"      BEGIN { inbox = 0 }
      {
        line = $0
        isbox = (line ~ /^[[:space:]]*-[[:space:]]*\[[xX]\]/)
        if (isbox) {
          low = tolower(line)
          if (low ~ /root.?cause/ || low ~ /addressed/ || low ~ /no.?regress/) {
            if (inbox) print "\036"
            inbox = 1; print; next
          }
          if (inbox) { print "\036"; inbox = 0 }
          next
        }
        if (inbox) {
          if (line ~ /^[[:space:]]+/ || line ~ /^[[:space:]]*$/) { print; next }
          print "\036"; inbox = 0
        }
      }
      END { if (inbox) print "\036" }
"####;
/// The verdict line's box count, verbatim.
const BOX_COUNT: &str = r####"git ls-files docs/tasks | grep -E '\.md$' | grep -v TEMPLATE | xargs grep -hcE '^[[:space:]]*-[[:space:]]*\[[xX]\]' 2>/dev/null | paste -sd+ - | bc 2>/dev/null || echo '?'"####;

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

/// A child in the working directory, stdin closed; its stdout, stderr and status.
fn run_in(cwd: &Path, program: &str, args: &[&str], stdin: Option<&str>) -> (i32, String, String) {
    let mut command = Command::new(program);
    command
        .args(args)
        .current_dir(cwd)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());
    command.stdin(if stdin.is_some() {
        Stdio::piped()
    } else {
        Stdio::null()
    });
    let Ok(mut child) = command.spawn() else {
        return (127, String::new(), String::new());
    };
    if let (Some(text), Some(mut pipe)) = (stdin, child.stdin.take()) {
        let _ = pipe.write_all(text.as_bytes());
    }
    match child.wait_with_output() {
        Ok(o) => (
            o.status.code().unwrap_or(-1),
            String::from_utf8_lossy(&o.stdout).into_owned(),
            String::from_utf8_lossy(&o.stderr).into_owned(),
        ),
        Err(_) => (127, String::new(), String::new()),
    }
}

/// `printf '%s' "$text" | grep -qE "$re"`.
fn matches(cwd: &Path, re: &str, text: &str) -> bool {
    run_in(cwd, "grep", &["-qE", re], Some(text)).0 == 0
}

/// `printf '%s\n' "$all" | grep -E "$re"` (or `-vE`): the selected lines.
fn select(cwd: &Path, re: &str, lines: &str, invert: bool) -> Vec<String> {
    let flag = if invert { "-vE" } else { "-E" };
    let (_, out, _) = run_in(cwd, "grep", &[flag, re], Some(&format!("{lines}\n")));
    out.lines().map(str::to_owned).collect()
}

/// `sed -n "s/^NAME='\(.*\)'$/\1/p" FILE | head -1`.
fn extract(cwd: &Path, file: &str, name: &str) -> String {
    let text = fs::read_to_string(cwd.join(file)).unwrap_or_default();
    let head = format!("{name}='");
    text.lines()
        .find_map(|l| {
            l.strip_prefix(&head)
                .and_then(|rest| rest.strip_suffix('\''))
                .map(str::to_owned)
        })
        .unwrap_or_default()
}

/// `"$NEUTRAL" <flag> 2>/dev/null`, captured: the owner's own effective rule.
fn effective(cwd: &Path, flag: &str) -> String {
    let (_, out, _) = run_in(cwd, &cwd.join(NEUTRAL).display().to_string(), &[flag], None);
    captured(&out).to_owned()
}

/// R2 — `boxes_regression <signature> <dir>`, run in `cwd`: every ticked hard-gated box must match the signature set.
fn boxes_regression(cwd: &Path, sig: &str, dir: &str) -> (i32, String) {
    let mut out = String::new();
    let mut bad = 0;
    let (_, listed, _) = run_in(cwd, "git", &["ls-files", dir], None);
    for f in listed.lines().filter(|l| l.ends_with(".md")) {
        if f.ends_with("/TEMPLATE.md") {
            continue;
        }
        if fs::File::open(cwd.join(f)).is_err() {
            continue;
        }
        let (_, scoped, _) = run_in(cwd, "awk", &[BOX_SCOPER, f], None);
        let mut boxed = String::new();
        for l in scoped.lines() {
            if l == "\u{1e}" {
                if !boxed.is_empty() && !matches(cwd, sig, &boxed) {
                    out.push_str(&format!(
                        "  REGRESSED {f}: a current tracked acceptance box lacks a declared evidence signature\n"
                    ));
                    let first = boxed.lines().next().unwrap_or("");
                    let cut: String = first.chars().take(96).collect();
                    out.push_str(&format!("    {cut}\n"));
                    bad = 1;
                }
                boxed.clear();
            } else {
                boxed.push_str(l);
                boxed.push('\n');
            }
        }
    }
    (bad, out)
}

/// R5 — `vocabulary_agreement <signature> <census gate>`: every literal alternative of the census list, as a sample
/// evidence line, must match the acceptance signature.
fn vocabulary_agreement(cwd: &Path, sig: &str, gate: &str) -> (i32, String) {
    if !cwd.join(gate).is_file() {
        return (
            1,
            format!("  NO CENSUS GATE {gate} is missing; the vocabularies cannot be compared\n"),
        );
    }
    let census = extract(cwd, gate, "CENSUS_RE");
    if census.is_empty() {
        return (
            1,
            format!("  NO CENSUS LIST {gate} no longer defines CENSUS_RE in the expected shape\n"),
        );
    }
    // `sed 's/([^)]*)//g'`: every parenthesised group stripped before the split.
    let mut stripped = String::new();
    let mut rest = census.as_str();
    while let Some(open) = rest.find('(') {
        let after = &rest[open + 1..];
        match after.find(')') {
            Some(close) => {
                stripped.push_str(&rest[..open]);
                rest = &after[close + 1..];
            }
            None => {
                stripped.push_str(rest);
                rest = "";
            }
        }
    }
    stripped.push_str(rest);
    let mut out = String::new();
    let mut missed = 0;
    // `IFS='|'; for alt in $census`: a trailing separator ends the last field rather than opening an empty one.
    let mut fields: Vec<&str> = stripped.split('|').collect();
    if stripped.ends_with('|') {
        fields.pop();
    }
    for alt in fields {
        if alt.is_empty() || alt.contains(['(', ')', '[', ']', '?', '+', '*']) {
            continue;
        }
        if matches!(alt, "a search of" | "searched " | "census:") {
            continue;
        }
        if !matches(cwd, sig, &format!("evidence: {alt} foo")) {
            out.push_str(&format!(
                "  VOCABULARY GAP the census gate accepts '{alt}' but the acceptance gate does not\n"
            ));
            missed += 1;
        }
    }
    if missed > 0 {
        out.push_str(&format!(
            "  ({missed} instrument(s) an author could be told to use and then refused for using)\n"
        ));
        return (1, out);
    }
    (0, out)
}

/// R3/R4 — `code_class_properties <code regex>` over a list of paths.
fn code_class_properties(
    cwd: &Path,
    re: &str,
    paths: &str,
    prose: &str,
    must_be_code: &[&str],
) -> (i32, String) {
    let all = captured(paths);
    let mut out = String::new();
    let mut bad = 0;
    let prose_lines = select(cwd, prose, all, false).join("\n");
    let over = if prose_lines.is_empty() {
        Vec::new()
    } else {
        select(cwd, re, &prose_lines, false)
    };
    if !over.is_empty() {
        out.push_str(&format!(
            "  OVER-MATCH {} prose file(s) under {prose} classified as a code change\n",
            over.len()
        ));
        for l in over.iter().take(3) {
            out.push_str(&format!("    {l}\n"));
        }
        bad = 1;
    }
    for fam in must_be_code {
        let present = select(cwd, fam, all, false);
        if present.is_empty() {
            continue;
        }
        let missing = select(cwd, re, &present.join("\n"), true);
        if !missing.is_empty() {
            out.push_str(&format!(
                "  UNDER-MATCH {} file(s) matching {fam} are NOT classified as a code change\n",
                missing.len()
            ));
            for l in missing.iter().take(3) {
                out.push_str(&format!("    {l}\n"));
            }
            bad = 1;
        }
    }
    (bad, out)
}

struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// `score <name> <expected rc> <expected substring> <rc> <output>`.
    fn score(&mut self, name: &str, expected: i32, want: &str, (rc, raw): (i32, String)) {
        let out = captured(&raw);
        if rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!("SEAM-INTEGRITY self-test MISS: {name} expected rc={expected} got rc={rc}\n{out}");
            }
        } else if !want.is_empty() && !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("SEAM-INTEGRITY self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
        } else {
            self.pass += 1;
        }
    }
}

/// `python3 [env] "$ROOT/scripts/probe_temporary_locality.py" --mode <mode> 2>&1`.
fn locality(root: &Path, mode: &str, optimize: bool) -> (i32, String) {
    let mut command = Command::new("python3");
    command
        .arg(root.join("scripts/probe_temporary_locality.py"))
        .args(["--mode", mode])
        .current_dir(root)
        .stdin(Stdio::null());
    if optimize {
        command.env("PYTHONOPTIMIZE", "1");
    }
    merged(&mut command)
}

/// A command's `2>&1` (through `bash -c`, which joins the two streams in write order).
fn merged(command: &mut Command) -> (i32, String) {
    let program = command.get_program().to_owned();
    let args: Vec<std::ffi::OsString> = command.get_args().map(ToOwned::to_owned).collect();
    let mut shell = Command::new("bash");
    shell
        .arg("-c")
        .arg("\"$@\" 2>&1")
        .arg("bash")
        .arg(program)
        .args(args);
    if let Some(dir) = command.get_current_dir() {
        shell.current_dir(dir);
    }
    for (k, v) in command.get_envs() {
        if let Some(v) = v {
            shell.env(k, v);
        }
    }
    shell.stdin(Stdio::null());
    match shell.output() {
        Ok(o) => (
            o.status.code().unwrap_or(-1),
            String::from_utf8_lossy(&o.stdout).into_owned(),
        ),
        Err(e) => (-1, e.to_string()),
    }
}

/// The RED/GREEN controls. Quiet unless `verbose` (the script ran them `>/dev/null 2>&1` before the real judgement).
fn self_test(root: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(root, "target/doctrine-selftest", "seamintegrity") else {
        if verbose {
            eprintln!("SEAM-INTEGRITY self-test: cannot create a scratch directory under target/doctrine-selftest");
        }
        return false;
    };
    let full = effective(root, "--print-sig");
    if full.is_empty() {
        if verbose {
            eprintln!("seam self-test: the owner printed no signature set");
        }
        let _ = fs::remove_dir_all(&t);
        return false;
    }
    let narrow = extract(root, NEUTRAL, "DEFAULT_SIG");
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };

    // ---- R2: a tracked box whose evidence is a plain census — the exact shape refused three times before the tokens
    // were declared.
    let _ = fs::write(
        t.join("leaf.md"),
        "- [x] **ROOT CAUSE (WHY + WHERE)** — census over the pinned chapters:\n  `grep -ci reset rv32.txt rv64.txt` -> `rv32.txt:0`, `rv64.txt:0`.\n\n- [x] **ADDRESSED (verified)** — `README-ROUTING-CLOSURE: ok (24 governed destination(s))`.\n",
    );
    let _ = run_in(&t, "git", &["init", "-q", "."], None);
    let _ = run_in(&t, "git", &["add", "leaf.md"], None);
    tally.score(
        "GREEN declared tokens accept a current tracked box",
        0,
        "",
        boxes_regression(&t, &full, "."),
    );
    tally.score(
        "RED   losing tokens rejects a current tracked box",
        1,
        "current tracked acceptance box lacks a declared evidence signature",
        boxes_regression(&t, &narrow, "."),
    );

    // ---- R3/R4: classification properties, with the families narrowed for the duration. The fixture is one path per
    // line, and its line count is ASSERTED — a fixture that silently collapses to one line is how an earlier arm lied.
    let fixture = "docs/book/src/claim-scope.md\n.githooks/pre-commit\ndoctrine/readme_routes.tsv\ncrates/app/src/main.rs\nCargo.toml\n";
    let _ = fs::write(t.join("paths.txt"), fixture);
    if fixture.lines().count() != 5 {
        tally.fail += 1;
        if verbose {
            eprintln!("SEAM-INTEGRITY self-test MISS: the path fixture is not 5 lines");
        }
    }
    let families: &[&str] = &[
        "^\\.githooks/",
        "^doctrine/.*\\.tsv$",
        "^Cargo\\.(toml|lock)$",
        "^crates/",
    ];
    let classify = |re: &str| code_class_properties(root, re, fixture, PROSE_PATHS, families);
    tally.score(
        "GREEN declared classification holds both properties",
        0,
        "",
        classify(&effective(root, "--print-code-re")),
    );
    tally.score(
        "RED   the historical unanchored pattern over-matches prose",
        1,
        "OVER-MATCH",
        classify(HISTORICAL_OVERMATCH_RE),
    );
    tally.score(
        "RED   a narrowed pattern under-matches behaviour files",
        1,
        "UNDER-MATCH",
        classify("^crates/"),
    );
    tally.score(
        "RED   a pattern matching everything over-matches prose",
        1,
        "OVER-MATCH",
        classify("."),
    );

    // ---- R5: vocabulary agreement
    tally.score(
        "GREEN the two gates agree on what an instrument is",
        0,
        "",
        vocabulary_agreement(root, &full, "scripts/check_gap_claims.sh"),
    );
    tally.score(
        "RED   an acceptance set that ignores the census list",
        1,
        "VOCABULARY GAP",
        vocabulary_agreement(
            root,
            "test result: (ok|FAILED)",
            "scripts/check_gap_claims.sh",
        ),
    );
    tally.score(
        "RED   the census gate is gone, so nothing can be compared",
        1,
        "NO CENSUS GATE",
        vocabulary_agreement(root, &full, &t.join("absent.sh").display().to_string()),
    );

    // R6: direct allocations and nested child defaults stay on volume.
    tally.score(
        "GREEN shell allocation sites are qualified and cleaned",
        0,
        "shell sites qualified and cleaned",
        locality(root, "shell", false),
    );
    tally.score(
        "GREEN Python fixture allocations are qualified and cleaned",
        0,
        "Python self-tests qualified and cleaned",
        locality(root, "python", false),
    );
    tally.score(
        "GREEN entrypoints constrain unset and foreign child defaults",
        0,
        "unset/foreign child environments constrained",
        locality(root, "children", false),
    );
    tally.score(
        "RED bare shell allocation refuses before a foreign write",
        1,
        "unqualified shell allocation",
        locality(root, "bare-shell", false),
    );
    tally.score(
        "RED Python optimization cannot disable the shell allocator guard",
        1,
        "unqualified shell allocation",
        locality(root, "bare-shell", true),
    );
    tally.score(
        "RED bare Python allocation refuses before a foreign write",
        1,
        "unqualified Python allocation",
        locality(root, "bare-python", false),
    );
    tally.score(
        "RED a qualified fixture still needs complete cleanup",
        1,
        "fixture residue",
        locality(root, "residue", false),
    );
    tally.score(
        "RED a child with a foreign default fails the locality contract",
        1,
        "child temporary root differs",
        locality(root, "unconstrained-child", false),
    );
    tally.score(
        "GREEN standalone synth creates its scratch parent before allocation",
        0,
        "scratch parent created before guarded allocation",
        locality(root, "parent", false),
    );

    tally.score(
        "GREEN custom-vocabulary fixture still needs the declared seam",
        0,
        "probes: 10 pass / 0 fail",
        merged(
            Command::new("bash")
                .arg(
                    root.join("docs/tasks/artifacts/task_acceptance/run_task_acceptance_probes.sh"),
                )
                .current_dir(root),
        ),
    );

    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "SEAM-INTEGRITY --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// `cargo xtask check-seam-integrity [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    let _ = fs::create_dir_all(root.join("target/tmp"));
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    // ── refuse rather than skip
    if !root.join(NEUTRAL).is_file() {
        eprintln!("SEAM-INTEGRITY: REFUSED — {NEUTRAL} is missing; the seams it consumes cannot be judged.");
        return ExitCode::from(2);
    }
    if extract(root, NEUTRAL, "DEFAULT_SIG").is_empty()
        || extract(root, NEUTRAL, "default_code_re").is_empty()
    {
        eprintln!(
            "SEAM-INTEGRITY: REFUSED — cannot extract the neutral check's built-in defaults from"
        );
        eprintln!("  {NEUTRAL}. Its shape changed, so this check's baseline is unknown and a green verdict");
        eprintln!("  would be a guess. Re-derive the extraction before trusting either gate.");
        return ExitCode::from(2);
    }
    if !self_test(root, false) {
        eprintln!("SEAM-INTEGRITY: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }

    let mut fail = false;
    let mut report = String::new();
    // R1 — the seams exist and are still CONSUMED by the neutral check.
    let neutral_text = fs::read_to_string(root.join(NEUTRAL)).unwrap_or_default();
    for f in [TOKENS, PATHS] {
        if fs::metadata(root.join(f)).map(|m| m.len()).unwrap_or(0) == 0 {
            report.push_str(&format!(
                "  MISSING {f} — the declaration that fixes a spine defect here is gone\n"
            ));
            fail = true;
            continue;
        }
        let base = f.rsplit('/').next().unwrap_or(f);
        if !neutral_text.contains(base) {
            report.push_str(&format!(
                "  INERT {f} — {NEUTRAL} no longer reads it, so the declaration protects nothing\n"
            ));
            fail = true;
        }
    }
    let sig = effective(root, "--print-sig");
    if sig.is_empty() {
        eprintln!(
            "SEAM-INTEGRITY: REFUSED — {NEUTRAL} --print-sig produced nothing; cannot judge."
        );
        return ExitCode::from(2);
    }
    let code_re = effective(root, "--print-code-re");
    if code_re.is_empty() {
        eprintln!(
            "SEAM-INTEGRITY: REFUSED — {NEUTRAL} --print-code-re produced nothing; cannot judge."
        );
        return ExitCode::from(2);
    }
    // R2 — current tracked acceptance boxes must match the declared signatures.
    let (rc, out) = boxes_regression(root, &sig, "docs/tasks");
    fail |= rc != 0;
    report.push_str(captured(&out));
    // R3/R4 — classification properties over the tracked tree.
    let (_, tracked, _) = run_in(root, "git", &["ls-files"], None);
    let (rc, out) = code_class_properties(root, &code_re, &tracked, PROSE_PATHS, MUST_BE_CODE);
    fail |= rc != 0;
    report.push_str(captured(&out));
    // R5 — the acceptance gate must accept every instrument the census gate blesses.
    let (rc, out) = vocabulary_agreement(root, &sig, "scripts/check_gap_claims.sh");
    fail |= rc != 0;
    report.push_str(captured(&out));

    if fail {
        eprintln!("SEAM-INTEGRITY: a declared seam no longer does the job it was declared for.");
        for line in report.split('\n') {
            if !line.is_empty() {
                eprintln!("{line}");
            }
        }
        eprintln!("  These declarations fix defects in the neutral spine checks (see");
        eprintln!(
            "  docs/decisions/reference_upstream-spine-defects.md). Restoring the file is the fix;"
        );
        eprintln!("  weakening this check is not.");
        return ExitCode::from(1);
    }
    let (_, count, _) = run_in(
        root,
        "bash",
        &["-c", &format!("set -o pipefail; {BOX_COUNT}")],
        None,
    );
    println!(
        "SEAM-INTEGRITY: ok ({} current tracked acceptance box(es) match declared signatures; classification properties hold)",
        captured(&count)
    );
    ExitCode::SUCCESS
}
