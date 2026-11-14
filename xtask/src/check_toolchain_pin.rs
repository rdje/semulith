//! The `TOOLCHAIN-PIN` doctrine (`XTASK.19` slice b): the Rust toolchain is chosen, never floated.
//!
//! Twice a Rust release turned hosted CI red with no code change, because every workflow installed that day's
//! stable while this host built with its own: 1.99's clippy on 2026-10-08 (`CI-RECOVERY.1`), then 1.100.0's on
//! 2026-11-14 (`XTASK.19`). `rust-toolchain.toml` now names one exact release, and every workflow step that
//! installs or selects Rust names that same release, so local and hosted builds judge with the same compiler and
//! the same clippy, and moving to a newer release is a unit of its own (`decision_the-toolchain-is-pinned.md`).
//!
//! The probe reads text on purpose, because what it holds is text: the `channel` line of the toolchain file and
//! the toolchain argument of each workflow step, in the forms a workflow selects Rust with: `RUSTUP_TOOLCHAIN=`,
//! `rustup toolchain install`, `rustup default`, `rustup override set`, and `cargo +` or `rustc +`. Prose that
//! merely says "stable", a step name or a comment, selects nothing and is not read. The one sanctioned
//! indirection is the Miri leg's dated nightly: `scripts/check_portability.sh --print-toolchain` owns that pin, and
//! a step may select a variable only if the same workflow assigns it from that command. Each self-test arm is one
//! `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts in a shim's module.

use std::fs;
use std::path::Path;
use std::process::ExitCode;

use crate::harness::scratch;

/// The file that names the toolchain for every local build.
const PIN_FILE: &str = "rust-toolchain.toml";
/// The directory whose workflows the hosted builds run.
const WORKFLOWS: &str = ".github/workflows";
/// The command that prints the Miri leg's pinned nightly; a toolchain variable may be assigned only from it.
const NIGHTLY_PRINTER: &str = "bash scripts/check_portability.sh --print-toolchain";
/// The text that introduces a toolchain argument in a workflow line.
const SELECTORS: [&str; 6] = [
    "RUSTUP_TOOLCHAIN=",
    "rustup toolchain install ",
    "rustup default ",
    "rustup override set ",
    "cargo +",
    "rustc +",
];

/// Runs the doctrine: `--self-test` as the first argument runs the arms; anything else runs the check.
/// Exit 0 ok, 1 a floating or mismatched toolchain, 2 refused.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !self_test(root, false) {
        eprintln!("TOOLCHAIN-PIN: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let verdict = probe(root);
    if !verdict.findings.is_empty() {
        eprintln!("TOOLCHAIN-PIN: the Rust toolchain floats, or a workflow names another release.");
        for finding in &verdict.findings {
            eprintln!("  {finding}");
        }
        eprintln!("  Name one exact release in {PIN_FILE} and the same release in every workflow step that");
        eprintln!("  installs or selects Rust; a newer release is a unit of its own (decision_the-toolchain-is-pinned).");
        return ExitCode::from(1);
    }
    println!(
        "TOOLCHAIN-PIN: ok ({PIN_FILE} pins {}; {} workflow step(s) in {} workflow(s) name it, {} take the Miri nightly from scripts/check_portability.sh)",
        verdict.pin, verdict.pinned_sites, verdict.workflows, verdict.nightly_sites
    );
    ExitCode::SUCCESS
}

/// What one probe found under a root.
struct Verdict {
    /// The pinned release, or the empty string when there is none.
    pin: String,
    /// The workflow files read.
    workflows: usize,
    /// The steps that name the pinned release.
    pinned_sites: usize,
    /// The steps that take the Miri nightly from its printer.
    nightly_sites: usize,
    /// One line per breach; empty when the doctrine holds.
    findings: Vec<String>,
}

/// Whether `text` is one exact release, `MAJOR.MINOR.PATCH`: `1.95` floats to its newest patch, and a channel
/// name floats to that day's release.
fn exact_release(text: &str) -> bool {
    let parts: Vec<&str> = text.split('.').collect();
    parts.len() == 3
        && parts
            .iter()
            .all(|part| !part.is_empty() && part.bytes().all(|b| b.is_ascii_digit()))
}

/// The `channel` value under `[toolchain]` in the toolchain file's text, if any.
fn channel(text: &str) -> Option<String> {
    let mut section = String::new();
    for line in text.lines() {
        let line = line.split('#').next().unwrap_or("").trim();
        if let Some(name) = line
            .strip_prefix('[')
            .and_then(|rest| rest.strip_suffix(']'))
        {
            section = name.trim().to_owned();
        } else if section == "toolchain" {
            if let Some((key, value)) = line.split_once('=') {
                if key.trim() == "channel" {
                    return Some(value.trim().trim_matches('"').trim_matches('\'').to_owned());
                }
            }
        }
    }
    None
}

/// The toolchain argument after each selector in `line`: the run of characters up to a quote, whitespace or a
/// shell operator, with one leading quote dropped.
fn selections(line: &str) -> Vec<String> {
    let mut found = Vec::new();
    for selector in SELECTORS {
        let mut rest = line;
        while let Some(at) = rest.find(selector) {
            let tail = rest[at + selector.len()..].trim_start_matches(['"', '\'']);
            let value: String = tail
                .chars()
                .take_while(|c| {
                    !c.is_whitespace()
                        && !matches!(c, '"' | '\'' | ';' | '&' | '|' | '>' | '<' | ')')
                })
                .collect();
            if !value.is_empty() {
                found.push(value);
            }
            rest = &rest[at + selector.len()..];
        }
    }
    found
}

/// Whether `text` assigns `variable` from the nightly printer, as `variable="$(bash scripts/check_portability.sh
/// --print-toolchain)"`.
fn assigned_from_printer(text: &str, variable: &str) -> bool {
    let assignment = format!("{variable}=\"$({NIGHTLY_PRINTER})\"");
    text.lines().any(|line| line.trim() == assignment)
}

/// Reads the toolchain file and every workflow under `root` and judges them.
fn probe(root: &Path) -> Verdict {
    let mut verdict = Verdict {
        pin: String::new(),
        workflows: 0,
        pinned_sites: 0,
        nightly_sites: 0,
        findings: Vec::new(),
    };
    match fs::read_to_string(root.join(PIN_FILE)) {
        Err(error) => verdict.findings.push(format!(
            "NO PIN FILE: {PIN_FILE} cannot be read ({error}); every local build would take rustup's default"
        )),
        Ok(text) => match channel(&text) {
            None => verdict.findings.push(format!(
                "NO CHANNEL: {PIN_FILE} names no `channel` under [toolchain]"
            )),
            Some(value) if !exact_release(&value) => verdict.findings.push(format!(
                "FLOATING CHANNEL: {PIN_FILE} names `{value}`, which moves when Rust releases; name one exact release (MAJOR.MINOR.PATCH)"
            )),
            Some(value) => verdict.pin = value,
        },
    }
    let mut files: Vec<_> = match fs::read_dir(root.join(WORKFLOWS)) {
        Ok(entries) => entries
            .filter_map(Result::ok)
            .map(|entry| entry.path())
            .filter(|path| {
                path.extension()
                    .is_some_and(|ext| ext == "yml" || ext == "yaml")
            })
            .collect(),
        Err(error) => {
            verdict.findings.push(format!(
                "NO WORKFLOWS: {WORKFLOWS} cannot be read ({error}); nothing hosted is held"
            ));
            return verdict;
        }
    };
    files.sort();
    if files.is_empty() {
        verdict.findings.push(format!(
            "NO WORKFLOWS: {WORKFLOWS} holds no workflow; nothing hosted is held"
        ));
    }
    for path in files {
        let shown = format!(
            "{WORKFLOWS}/{}",
            path.file_name().unwrap_or_default().to_string_lossy()
        );
        let text = match fs::read_to_string(&path) {
            Ok(text) => text,
            Err(error) => {
                verdict
                    .findings
                    .push(format!("UNREADABLE: {shown} ({error})"));
                continue;
            }
        };
        verdict.workflows += 1;
        for (number, line) in text.lines().enumerate() {
            let at = format!("{shown}:{}", number + 1);
            for value in selections(line) {
                if let Some(variable) = value
                    .strip_prefix('$')
                    .map(|name| name.trim_start_matches('{').trim_end_matches('}'))
                {
                    if assigned_from_printer(&text, variable) {
                        verdict.nightly_sites += 1;
                    } else {
                        verdict.findings.push(format!(
                            "UNDERIVED: {at} selects `{value}`, which this workflow assigns from nothing but `{NIGHTLY_PRINTER}`'s pin would justify; name the pinned release"
                        ));
                    }
                } else if !verdict.pin.is_empty() && value == verdict.pin {
                    verdict.pinned_sites += 1;
                } else if exact_release(&value) {
                    verdict.findings.push(format!(
                        "NOT THE PIN: {at} names {value}, but {PIN_FILE} pins {}; local and hosted builds would judge with different compilers",
                        if verdict.pin.is_empty() { "nothing exact" } else { &verdict.pin }
                    ));
                } else {
                    verdict.findings.push(format!(
                        "FLOATING TOOLCHAIN: {at} selects `{value}`, which moves when Rust releases; name the pinned release"
                    ));
                }
            }
        }
    }
    verdict
}

/// The self-test's pass and fail counts; `verbose` prints misses on stderr and the summary on stdout.
struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: probing the fixture root `fixture` must give the verdict `expected` (0 no finding, 1 a finding),
    /// and its findings, or for a green arm its summary, must contain `want`.
    fn arm(&mut self, fixture: &Path, name: &str, expected: i32, want: &str) {
        let verdict = probe(fixture);
        let rc = i32::from(!verdict.findings.is_empty());
        let text = if verdict.findings.is_empty() {
            format!(
                "pin {} / {} pinned / {} nightly",
                verdict.pin, verdict.pinned_sites, verdict.nightly_sites
            )
        } else {
            verdict.findings.join("\n")
        };
        if rc != expected {
            self.fail += 1;
            if self.verbose {
                eprintln!("TOOLCHAIN-PIN self-test MISS: {name} expected rc={expected} got rc={rc}\n{text}");
            }
        } else if !text.contains(want) {
            self.fail += 1;
            if self.verbose {
                eprintln!("TOOLCHAIN-PIN self-test MISS: {name} right verdict, wrong reason (no {want})\n{text}");
            }
        } else {
            self.pass += 1;
        }
    }
}

/// A pinned toolchain file.
const PIN_EXACT: &str =
    "[toolchain]\nchannel = \"1.95.0\"\ncomponents = [\"rustfmt\", \"clippy\"]\n";
/// A pinned workflow: the release in the environment and the install step, step names that say "stable", and
/// the Miri leg's nightly taken from its printer.
const WORKFLOW_PINNED: &str = r#"jobs:
  check:
    steps:
      - name: Provision the pinned stable Rust
        run: |
          echo "RUSTUP_TOOLCHAIN=1.95.0" >> "$GITHUB_ENV"
          rustup toolchain install 1.95.0 --profile minimal --component rustfmt,clippy --no-self-update
  miri:
    steps:
      - name: The pinned nightly
        run: |
          toolchain="$(bash scripts/check_portability.sh --print-toolchain)"
          rustup toolchain install "$toolchain" --profile minimal --component miri --no-self-update
          echo "RUSTUP_TOOLCHAIN=$toolchain" >> "$GITHUB_ENV"
"#;

/// Writes one fixture root under `base`: the toolchain file (unless `None`) and one workflow.
fn fixture(
    base: &Path,
    name: &str,
    pin: Option<&str>,
    workflow: &str,
) -> std::io::Result<std::path::PathBuf> {
    let dir = base.join(name);
    fs::create_dir_all(dir.join(WORKFLOWS))?;
    if let Some(text) = pin {
        fs::write(dir.join(PIN_FILE), text)?;
    }
    fs::write(dir.join(WORKFLOWS).join("ci.yml"), workflow)?;
    Ok(dir)
}

/// The arms, each against a fixture root of frozen synthetic files. Returns whether every arm held.
fn self_test(root: &Path, verbose: bool) -> bool {
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    let base = match scratch(root, "target/doctrine-selftest", "toolchain-pin") {
        Ok(dir) => dir,
        Err(error) => {
            if verbose {
                eprintln!("TOOLCHAIN-PIN self-test: cannot create a scratch directory: {error}");
            }
            return false;
        }
    };
    let floating_env =
        WORKFLOW_PINNED.replacen("RUSTUP_TOOLCHAIN=1.95.0", "RUSTUP_TOOLCHAIN=stable", 1);
    let floating_install = WORKFLOW_PINNED.replacen("install 1.95.0", "install stable", 1);
    let other_release = WORKFLOW_PINNED.replacen("install 1.95.0", "install 1.100.0", 1);
    let underived = WORKFLOW_PINNED.replacen(
        "toolchain=\"$(bash scripts/check_portability.sh --print-toolchain)\"",
        "toolchain=stable",
        1,
    );
    let plus_floating = format!("{WORKFLOW_PINNED}      - run: cargo +nightly test\n");
    let fixtures = [
        fixture(&base, "pinned", Some(PIN_EXACT), WORKFLOW_PINNED),
        fixture(
            &base,
            "channel-stable",
            Some("[toolchain]\nchannel = \"stable\"\n"),
            WORKFLOW_PINNED,
        ),
        fixture(
            &base,
            "channel-minor",
            Some("[toolchain]\nchannel = \"1.95\"\n"),
            WORKFLOW_PINNED,
        ),
        fixture(
            &base,
            "no-channel",
            Some("[toolchain]\ncomponents = [\"clippy\"]\n"),
            WORKFLOW_PINNED,
        ),
        fixture(&base, "no-pin-file", None, WORKFLOW_PINNED),
        fixture(&base, "env-stable", Some(PIN_EXACT), &floating_env),
        fixture(&base, "install-stable", Some(PIN_EXACT), &floating_install),
        fixture(&base, "other-release", Some(PIN_EXACT), &other_release),
        fixture(&base, "underived", Some(PIN_EXACT), &underived),
        fixture(&base, "plus-nightly", Some(PIN_EXACT), &plus_floating),
    ];
    let paths: Vec<_> = match fixtures.into_iter().collect::<std::io::Result<Vec<_>>>() {
        Ok(paths) => paths,
        Err(error) => {
            if verbose {
                eprintln!("TOOLCHAIN-PIN self-test: cannot write the fixtures: {error}");
            }
            let _ = fs::remove_dir_all(&base);
            return false;
        }
    };
    let [pinned, channel_stable, channel_minor, no_channel, no_pin_file, env_stable, install_stable, other, underived, plus_nightly] =
        &paths[..]
    else {
        let _ = fs::remove_dir_all(&base);
        return false;
    };
    tally.arm(
        pinned,
        "GREEN the pin, its workflow steps and the printer's nightly",
        0,
        "pin 1.95.0 / 2 pinned / 2 nightly",
    );
    tally.arm(
        channel_stable,
        "RED   the toolchain file names a channel",
        1,
        "FLOATING CHANNEL",
    );
    tally.arm(
        channel_minor,
        "RED   the toolchain file names a minor release",
        1,
        "FLOATING CHANNEL",
    );
    tally.arm(
        no_channel,
        "RED   the toolchain file names no channel",
        1,
        "NO CHANNEL",
    );
    tally.arm(no_pin_file, "RED   no toolchain file", 1, "NO PIN FILE");
    tally.arm(
        env_stable,
        "RED   a workflow selects stable in its environment",
        1,
        "FLOATING TOOLCHAIN: .github/workflows/ci.yml:6",
    );
    tally.arm(
        install_stable,
        "RED   a workflow installs stable",
        1,
        "FLOATING TOOLCHAIN: .github/workflows/ci.yml:7",
    );
    tally.arm(
        other,
        "RED   a workflow installs another exact release",
        1,
        "NOT THE PIN: .github/workflows/ci.yml:7 names 1.100.0",
    );
    tally.arm(
        underived,
        "RED   a toolchain variable not from the nightly printer",
        1,
        "UNDERIVED",
    );
    tally.arm(
        plus_nightly,
        "RED   cargo +nightly in a step",
        1,
        "FLOATING TOOLCHAIN: .github/workflows/ci.yml:15 selects `nightly`",
    );
    let _ = fs::remove_dir_all(&base);
    if verbose {
        println!(
            "TOOLCHAIN-PIN --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn an_exact_release_has_three_numeric_parts() {
        assert!(exact_release("1.95.0"));
        assert!(exact_release("1.100.0"));
        for floating in ["stable", "1.95", "1.95.x", "nightly-2026-09-13", "", "1..0"] {
            assert!(!exact_release(floating), "{floating}");
        }
    }

    #[test]
    fn a_selection_is_the_argument_not_the_prose() {
        assert_eq!(
            selections(r#"echo "RUSTUP_TOOLCHAIN=1.95.0" >> "$GITHUB_ENV""#),
            ["1.95.0"]
        );
        assert_eq!(
            selections(r#"rustup toolchain install "$toolchain" --profile minimal"#),
            ["$toolchain"]
        );
        assert_eq!(selections("cargo +nightly miri test"), ["nightly"]);
        assert!(selections("- name: Provision stable Rust").is_empty());
    }

    #[test]
    fn the_channel_is_read_under_its_section() {
        assert_eq!(
            channel("[toolchain]\nchannel = \"1.95.0\" # pinned\n").as_deref(),
            Some("1.95.0")
        );
        assert_eq!(channel("[other]\nchannel = \"stable\"\n"), None);
    }
}
