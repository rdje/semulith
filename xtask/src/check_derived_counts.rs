//! The `DERIVED-COUNTS` doctrine, ported from `scripts/check_derived_counts.sh` (`XTASK.6` slice `6ae`), which is now a
//! shim of `cargo xtask check-derived-counts`.
//!
//! A live document may state a repository count — routed destinations, registered project doctrines, book chapters,
//! self-test arms, open upstream issues — only as the number the repository re-derives today; a running total is a
//! memory of a measurement, and both of this doctrine's founding defects were running totals. Every claim is a
//! `label|pattern|enumerator` row: the pattern begins with its `([0-9]+)` group, the enumerator is the shell command
//! (run as the script ran it, `eval` from the root) or the arm total, which this module derives itself as the script's
//! function did — bash `arm "` and `score "` lines, and a shim module's `tally.arm(` and `tally.score(` lines. The
//! shell's own `grep -E` finds and extracts the claims, so the match is the script's. Each self-test arm is one
//! `tally.arm(` call, the idiom the arm total counts.

use std::fs;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::scratch;

/// The `count_claims` table, verbatim from the script (`label|pattern|enumerator`), and two rows added in `XTASK.6` slice
/// `6as` after a running total drifted through twelve slices: the shim count and the registry size of the live phrase
/// `N of M drivers through shims`, re-derived from the project registry and the shims' own `exec cargo xtask` line.
const CLAIMS: &str = "routed destinations|([0-9]+) destinations governed|grep -cv '^#\\|^$' doctrine/readme_routes.tsv
project doctrines|([0-9]+) registered|grep -cE '^  \"[A-Z]' scripts/check_doctrines.project.sh
book chapters|([0-9]+) chapters|grep -cE '^\\s*-? ?\\[' docs/book/src/SUMMARY.md
self-test arms|([0-9]+) self-test arms|arm_total
open upstream issues|([0-9]+) open upstream issues|python3 scripts/upstream_exposure.py --open-count
drivers through shims|([0-9]+) of [0-9]+ drivers through shims|grep -oE '[|]scripts/[a-z_]+[.]sh\"$' scripts/check_doctrines.project.sh | tr -d '|\"' | xargs grep -l '^exec cargo xtask' | grep -c .
drivers registered|([0-9]+) drivers through shims|grep -cE '^  \"[A-Z]' scripts/check_doctrines.project.sh
";

/// A parsed claim row.
struct Claim {
    label: String,
    pattern: String,
    enumerator: String,
}

fn parse_claims(text: &str) -> Vec<Claim> {
    text.lines()
        .filter(|l| !l.is_empty())
        .filter_map(|l| {
            let mut parts = l.splitn(3, '|');
            let label = parts.next()?.to_owned();
            if label.is_empty() {
                return None;
            }
            Some(Claim {
                label,
                pattern: parts.next().unwrap_or("").to_owned(),
                enumerator: parts.next().unwrap_or("").to_owned(),
            })
        })
        .collect()
}

/// `grep -cE '(^|[; ])arm "'` on a text: lines where `arm "` opens the line or follows `;` or a space.
fn bash_arm_lines(text: &str) -> usize {
    text.lines()
        .filter(|l| l.starts_with("arm \"") || l.contains("; arm \"") || l.contains(" arm \""))
        .count()
}

/// `grep -cE '^[[:space:]]+score "'`.
fn bash_score_lines(text: &str) -> usize {
    text.lines()
        .filter(|l| {
            let stripped = l.trim_start_matches([' ', '\t']);
            stripped.len() < l.len() && stripped.starts_with("score \"")
        })
        .count()
}

/// `sed -nE 's/^exec cargo xtask ([a-z][a-z-]*)( .*)?$/\1/p' | head -1`: the shim's subcommand, if any.
fn shim_subcommand(text: &str) -> Option<String> {
    text.lines().find_map(|l| {
        let rest = l.strip_prefix("exec cargo xtask ")?;
        let name: String = rest
            .chars()
            .take_while(|c| c.is_ascii_lowercase() || *c == '-')
            .collect();
        if name.is_empty() || !name.chars().next().is_some_and(|c| c.is_ascii_lowercase()) {
            return None;
        }
        let after = &rest[name.len()..];
        (after.is_empty() || after.starts_with(' ')).then_some(name)
    })
}

/// `grep -cE '^[[:space:]]+tally\.(arm|score)\('`.
fn rust_arm_lines(text: &str) -> usize {
    text.lines()
        .filter(|l| {
            let stripped = l.trim_start_matches([' ', '\t']);
            stripped.len() < l.len()
                && (stripped.starts_with("tally.arm(") || stripped.starts_with("tally.score("))
        })
        .count()
}

/// The script's `arm_total`, over the registry at `base`: the arms of every registered project check — bash arms and
/// scores, and a shim module's `tally.arm(`/`tally.score(` — or nothing when a shim's module is missing.
fn arm_total(base: &Path) -> Option<usize> {
    let registry = fs::read_to_string(base.join("scripts/check_doctrines.project.sh")).ok()?;
    let mut paths: Vec<String> = Vec::new();
    let mut i = 0;
    while let Some(at) = registry[i..].find("scripts/check_") {
        let start = i + at;
        let end = start
            + registry[start..]
                .char_indices()
                .find(|(_, c)| !(c.is_ascii_lowercase() || *c == '_' || *c == '/' || *c == '.'))
                .map_or(registry.len() - start, |(k, _)| k);
        let candidate = &registry[start..end];
        // `scripts/check_[a-z_]+\.sh`: the stem, then `.sh`.
        if let Some(stem) = candidate
            .strip_prefix("scripts/check_")
            .and_then(|s| s.strip_suffix(".sh"))
        {
            if !stem.is_empty() && stem.chars().all(|c| c.is_ascii_lowercase() || c == '_') {
                paths.push(candidate.to_owned());
            }
        }
        i = start + "scripts/check_".len();
    }
    paths.sort();
    paths.dedup();
    let mut total = 0usize;
    for rel in paths {
        let Ok(text) = fs::read_to_string(base.join(&rel)) else {
            continue;
        };
        total += bash_arm_lines(&text) + bash_score_lines(&text);
        if let Some(sub) = shim_subcommand(&text) {
            let rs = base.join(format!("xtask/src/{}.rs", sub.replace('-', "_")));
            let module = fs::read_to_string(&rs).ok()?;
            total += rust_arm_lines(&module);
        }
    }
    Some(total)
}

/// `cd "$base" && eval "$enum" 2>/dev/null | tr -d '[:space:]'`: the enumerator's answer, or none when it fails or
/// says nothing; `arm_total` is derived here.
fn enumerate(base: &Path, enumerator: &str) -> Option<String> {
    if enumerator == "arm_total" {
        return arm_total(base).map(|n| n.to_string());
    }
    let output = Command::new("bash")
        .args(["-c", enumerator])
        .current_dir(base)
        .stdin(Stdio::null())
        .stderr(Stdio::null())
        .output()
        .ok()?;
    if !output.status.success() {
        return None;
    }
    let text: String = String::from_utf8_lossy(&output.stdout)
        .chars()
        .filter(|c| !c.is_whitespace())
        .collect();
    (!text.is_empty()).then_some(text)
}

/// `grep -E "$pat" file`: the lines that match, through the shell's grep.
fn matching_lines(pattern: &str, file: &Path) -> Vec<String> {
    Command::new("grep")
        .args(["-E", pattern])
        .arg(file)
        .stdin(Stdio::null())
        .stderr(Stdio::null())
        .output()
        .map(|o| {
            String::from_utf8_lossy(&o.stdout)
                .lines()
                .map(str::to_owned)
                .collect()
        })
        .unwrap_or_default()
}

/// `printf '%s' "$line" | grep -oE "$pat" | head -1 | grep -oE '^[0-9]+'`: the number off the front of the first match.
fn claimed_number(pattern: &str, line: &str) -> Option<String> {
    let mut child = Command::new("grep")
        .args(["-oE", pattern])
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::null())
        .spawn()
        .ok()?;
    if let Some(mut stdin) = child.stdin.take() {
        use std::io::Write;
        let _ = stdin.write_all(line.as_bytes());
    }
    let out = child.wait_with_output().ok()?;
    let first = String::from_utf8_lossy(&out.stdout)
        .lines()
        .next()?
        .to_owned();
    let digits: String = first.chars().take_while(char::is_ascii_digit).collect();
    (!digits.is_empty()).then_some(digits)
}

/// `live_docs`: the routes registry's `hot_live` rows that name a file.
fn live_docs(base: &Path) -> Vec<String> {
    fs::read_to_string(base.join("doctrine/readme_routes.tsv"))
        .map(|t| {
            t.lines()
                .filter(|l| !l.starts_with('#'))
                .filter_map(|l| {
                    let f: Vec<&str> = l.split('\t').collect();
                    (f.len() > 3 && f[2] == "hot_live" && !f[0].ends_with('/'))
                        .then(|| f[0].to_owned())
                })
                .collect()
        })
        .unwrap_or_default()
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

/// `check_counts <base> <claims> <docs>`: every claim re-derived against every live document.
fn check_counts(base: &Path, claims: &[Claim], docs: &[String]) -> Verdict {
    let mut out: Vec<String> = Vec::new();
    let mut findings = 0u32;
    let mut checked = 0u32;
    for claim in claims {
        if !claim.pattern.starts_with("([0-9]+)") {
            out.push(format!(
                "BAD PATTERN {}: '{}' must BEGIN with its ([0-9]+) group — the number is taken off the front of the match",
                claim.label, claim.pattern
            ));
            findings += 1;
            continue;
        }
        let Some(want) = enumerate(base, &claim.enumerator) else {
            out.push(format!(
                "NO ENUMERATOR {}: '{}' produced nothing — the check cannot judge this claim",
                claim.label, claim.enumerator
            ));
            findings += 1;
            continue;
        };
        for doc in docs {
            let file = base.join(doc);
            if !file.is_file() {
                continue;
            }
            for line in matching_lines(&claim.pattern, &file) {
                let Some(got) = claimed_number(&claim.pattern, &line) else {
                    continue;
                };
                checked += 1;
                if got != want {
                    out.push(format!(
                        "COUNT DRIFT {doc}: claims '{got}' {}; the repository has {want}  [{}]",
                        claim.label, claim.enumerator
                    ));
                    findings += 1;
                }
            }
        }
    }
    out.push(format!("__CHECKED__ {checked}"));
    Verdict {
        rc: i32::from(findings != 0),
        lines: out,
    }
}

struct Tally<'a> {
    root: &'a Path,
    claims: Vec<Claim>,
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally<'_> {
    /// One arm: judging the fixture (`LIVE.md` against the fixture claims) must give `expected` and contain `want`.
    fn arm(&mut self, name: &str, expected: i32, want: &str) {
        let verdict = check_counts(self.root, &self.claims, &["LIVE.md".to_owned()]);
        let out = verdict.text();
        if verdict.rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!(
                    "DERIVED-COUNTS self-test MISS: {name} expected rc={expected} got rc={}\n{out}",
                    verdict.rc
                );
            }
        } else if !out.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("DERIVED-COUNTS self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}");
            }
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

/// The RED/GREEN controls: a population file, a live document, and the shim-counting fixture.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "derivedcounts") else {
        eprintln!("DERIVED-COUNTS self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    let pop = |n: u32| {
        let text: String = (1..=n).map(|i| format!("{i}\n")).collect();
        write(&t.join("pop.txt"), &text);
    };
    let doc = |text: &str| write(&t.join("LIVE.md"), &format!("{text}\n"));
    let mut tally = Tally {
        root: &t,
        claims: parse_claims("widgets|([0-9]+) widgets|wc -l < pop.txt\n"),
        pass: 0,
        fail: 0,
        verbose,
    };
    pop(7);
    doc("the system has 7 widgets today.");
    tally.arm("GREEN the count matches the population", 0, "__CHECKED__ 1");
    doc("the system has 6 widgets today.");
    tally.arm("RED   the count is stale", 1, "COUNT DRIFT");
    doc("the system has 8 widgets today.");
    tally.arm("RED   the count is ahead", 1, "COUNT DRIFT");
    doc("no claim of that shape here at all.");
    tally.arm("GREEN a document making no claim", 0, "__CHECKED__ 0");
    doc("first says 7 widgets\nand a second line says 6 widgets.");
    tally.arm("RED   one of two claims drifts", 1, "COUNT DRIFT");
    pop(12);
    doc("the system has 7 widgets today.");
    tally.arm(
        "RED   the population changed under a fixed number",
        1,
        "COUNT DRIFT",
    );
    pop(12);
    doc("the system has 12 widgets today.");
    tally.arm(
        "GREEN re-derived after the change (two digits)",
        0,
        "__CHECKED__ 1",
    );
    pop(2);
    doc("the system has 12 widgets today.");
    tally.arm(
        "RED   a two-digit claim is not read as its last digit",
        1,
        "COUNT DRIFT",
    );
    pop(12);
    tally.claims = parse_claims("widgets|widgets: ([0-9]+)|wc -l < pop.txt\n");
    doc("widgets: 12");
    tally.arm(
        "REFUSE a pattern whose number is not first",
        1,
        "BAD PATTERN",
    );
    tally.claims = parse_claims("widgets|([0-9]+) widgets|cat no-such-file-here\n");
    tally.arm(
        "REFUSE an enumerator that produces nothing",
        1,
        "NO ENUMERATOR",
    );
    let _ = fs::create_dir_all(t.join("scripts"));
    let _ = fs::create_dir_all(t.join("xtask/src"));
    write(
        &t.join("scripts/check_doctrines.project.sh"),
        "PROJECT_DOCTRINES=(\"A|a|scripts/check_a.sh\" \"B|b|scripts/check_b.sh\")\n",
    );
    // Built in two pieces by the script so its own line is not an arm of the idiom it writes into the fixture.
    write(
        &t.join("scripts/check_a.sh"),
        &format!("#!/usr/bin/env bash\nx=1; {}\n", "arm \"one\" 0 \"-\""),
    );
    write(
        &t.join("scripts/check_b.sh"),
        "#!/usr/bin/env bash\nset -euo pipefail\nexec cargo xtask check-b \"$@\"\n",
    );
    write(
        &t.join("xtask/src/check_b.rs"),
        "fn t(tally: &mut T) {\n    tally.arm(\"two\", 0, 0, \"\", \"-\");\n    tally.arm(\n        \"three\",\n    );\n    tally.score(\"four\");\n}\n",
    );
    tally.claims = parse_claims("self-test arms|([0-9]+) self-test arms|arm_total\n");
    doc("the gate holds 4 self-test arms.");
    tally.arm(
        "GREEN a shim's xtask arms and scores are counted with the bash arms",
        0,
        "__CHECKED__ 1",
    );
    let _ = fs::remove_file(t.join("xtask/src/check_b.rs"));
    tally.arm(
        "REFUSE a shim whose xtask module is missing yields no total",
        1,
        "NO ENUMERATOR",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "DERIVED-COUNTS --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// `cargo xtask check-derived-counts [--self-test|--list]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    let claims = parse_claims(CLAIMS);
    if args.first().is_some_and(|arg| arg == "--list") {
        let (claim, enumerator, value) = ("CLAIM", "ENUMERATOR", "VALUE");
        println!("{claim:<22} {enumerator:<34} {value}");
        for claim in &claims {
            println!(
                "{:<22} {:<34} {}",
                claim.label,
                claim.enumerator,
                enumerate(root, &claim.enumerator).unwrap_or_default()
            );
        }
        return ExitCode::SUCCESS;
    }
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !root.join("doctrine/readme_routes.tsv").is_file() {
        println!("DERIVED-COUNTS: ok (no routes registry yet)");
        return ExitCode::SUCCESS;
    }
    if !self_test(root, false) {
        eprintln!("DERIVED-COUNTS: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let verdict = check_counts(root, &claims, &live_docs(root));
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
    if verdict.rc != 0 {
        eprintln!("DERIVED-COUNTS: a live document states a count the repository contradicts.");
        for line in &body {
            eprintln!("  {line}");
        }
        eprintln!(
            "  RE-DERIVE it with the command shown — never increment a running total, which is"
        );
        eprintln!("  how both of this doctrine's founding defects were introduced.");
        return ExitCode::from(1);
    }
    println!("DERIVED-COUNTS: ok ({count} derived count claim(s) re-derived)");
    ExitCode::SUCCESS
}
