//! The `PORT-WEB` doctrine, ported from `scripts/check_wasm_build.sh` (`XTASK.6` slice `6a`), which is now
//! a shim of `cargo xtask check-wasm-build`.
//!
//! The director's portability decision (`decision_browser-wasm-target`, 2026-09-27) makes
//! `wasm32-unknown-unknown` a first-class target from the first crate: host-native is a build mode, not the
//! architecture. The check proves the workspace still builds for the wasm target, so a host-only API cannot
//! slip into the engine unnoticed: the build itself is the proof (`PORT-WEB.1`).
//!
//! A check with arms: `--self-test` builds four scratch crates (a sound lib, a host-only lib, a sound bin,
//! one broken for an unrelated reason) and asserts the verdict and the reason for each. The real run re-runs
//! them first and refuses (exit 2) when they no longer discriminate. Each arm is one `tally.arm(` call, the
//! idiom the `DERIVED-COUNTS` arm total counts in a shim's module.

use std::fs;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{combined, scratch};

/// The browser target the workspace must build for.
const TARGET: &str = "wasm32-unknown-unknown";

/// Runs the doctrine: `--self-test` as the first argument runs the arms; anything else (like the script,
/// which read only its first argument) runs the check. Exit 0 ok, 1 the workspace fails to build, 2 refused.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    // Preflight: the target must be installed. Refuse with the fix, never fail silently or pass vacuously.
    if !target_installed() {
        eprintln!("PORT-WEB: REFUSED — rustup target '{TARGET}' is not installed, this check cannot judge.");
        eprintln!("  Install it with: rustup target add {TARGET}");
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
        eprintln!("PORT-WEB: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let (code, out) = combined(
        Command::new("cargo")
            .args(["build", "--workspace", "--target", TARGET])
            .current_dir(root),
    );
    if code != 0 {
        eprintln!(
            "PORT-WEB: FAIL — the workspace must build for {TARGET} (decision_browser-wasm-target):\n{}",
            out.trim_end_matches('\n')
        );
        return ExitCode::from(1);
    }
    println!("PORT-WEB: ok (workspace builds for {TARGET})");
    ExitCode::SUCCESS
}

/// Whether `rustup target list --installed` lists the target as a whole line (the script's `grep -qx`).
fn target_installed() -> bool {
    Command::new("rustup")
        .args(["target", "list", "--installed"])
        .stderr(Stdio::null())
        .output()
        .is_ok_and(|output| {
            String::from_utf8_lossy(&output.stdout)
                .lines()
                .any(|line| line == TARGET)
        })
}

/// The self-test's pass and fail counts; `verbose` prints misses on stderr and the summary on stdout.
struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: the verdict `rc` must equal `expected`, and `want` must occur in `out` (`-` asserts no
    /// reason; a leading `!` asserts the rest is absent).
    fn arm(&mut self, name: &str, rc: i32, expected: i32, out: &str, want: &str) {
        let held = match want.strip_prefix('!') {
            Some(absent) => rc == expected && !out.contains(absent),
            None => rc == expected && (want == "-" || out.contains(want)),
        };
        if held {
            self.pass += 1;
            return;
        }
        self.fail += 1;
        if self.verbose {
            match want.strip_prefix('!') {
                Some(absent) => eprintln!(
                    "PORT-WEB self-test MISS: {name} — expected rc={expected} WITHOUT {absent}, got rc={rc}\n{out}"
                ),
                None => eprintln!(
                    "PORT-WEB self-test MISS: {name} — expected rc={expected} (reason: {want}), got rc={rc}\n{out}"
                ),
            }
        }
    }
}

/// Writes a one-file crate with its own `[workspace]`, so the repository's workspace does not claim it.
fn make_crate(dir: &Path, name: &str, bin: bool, source: &str) -> std::io::Result<()> {
    fs::create_dir_all(dir.join("src"))?;
    fs::write(
        dir.join("Cargo.toml"),
        format!("[package]\nname = \"{name}\"\nversion = \"0.1.0\"\nedition = \"2021\"\n\n[workspace]\n"),
    )?;
    let file = if bin { "src/main.rs" } else { "src/lib.rs" };
    fs::write(dir.join(file), format!("{source}\n"))
}

/// Builds a scratch crate for the target with its own target directory inside the scratch directory, so
/// the self-test never shares artifacts with the real run.
fn build_wasm(dir: &Path) -> (i32, String) {
    let target_dir = dir.join(".wt");
    combined(
        Command::new("cargo")
            .args(["build", "--offline", "--target", TARGET, "--target-dir"])
            .arg(target_dir)
            .current_dir(dir),
    )
}

/// The four arms. Returns whether every arm held.
fn self_test(root: &Path, verbose: bool) -> bool {
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    let t = match scratch(root, "target/doctrine-selftest", "port-web") {
        Ok(dir) => dir,
        Err(error) => {
            if verbose {
                eprintln!("PORT-WEB self-test: cannot create a scratch directory: {error}");
            }
            return false;
        }
    };
    let cases: [(&str, &str, bool, &str); 4] = [
        ("good", "probe-good", false, "pub fn probe() -> u32 { 42 }"),
        (
            "hostonly",
            "probe-hostonly",
            false,
            "use std::os::unix::ffi::OsStrExt as _; pub fn probe() -> u32 { 42 }",
        ),
        (
            "bingood",
            "probe-bingood",
            true,
            "fn main() { println!(\"ok\"); }",
        ),
        ("syntax", "probe-syntax", false, "pub fn broken( {"),
    ];
    let [good, hostonly, bingood, syntax] = cases.map(|(dir, name, bin, source)| {
        let path = t.join(dir);
        match make_crate(&path, name, bin, source) {
            Ok(()) => build_wasm(&path),
            Err(error) => (-1, format!("cannot write the scratch crate: {error}")),
        }
    });
    tally.arm(
        "GREEN a sound lib crate builds for wasm",
        good.0,
        0,
        &good.1,
        "-",
    );
    tally.arm(
        "RED a host-only unix import breaks the wasm build, naming the reason",
        hostonly.0,
        101,
        &hostonly.1,
        "unix",
    );
    tally.arm(
        "GREEN a sound bin crate builds for wasm",
        bingood.0,
        0,
        &bingood.1,
        "-",
    );
    tally.arm(
        "REFUSE a failure with an unrelated cause is not read as the host-only reason",
        syntax.0,
        101,
        &syntax.1,
        "!unix",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "PORT-WEB --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}
