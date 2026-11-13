//! The `PLATFORM-GEN` doctrine's driver, ported from `scripts/check_platform_gen.sh` (`XTASK.6` slice `6w`), which is
//! now a shim of `cargo xtask check-platform-gen`.
//!
//! A board's platform capability manifest (`platform.sexp`) is GENERATED from its canonical inputs — the definition, the
//! composed obligations and the processor dossier's pinned digest — by `scripts/gen_platform.py`; this check regenerates
//! it and refuses the day the committed manifest stops byte-matching its derivation, or the day the generator refuses
//! an input (a stale dossier pin, a profile without endianness, a load-region that is not executable RAM, a console
//! claim the wiring contradicts, a missing or invented time fact). The generator is spawned exactly as the driver
//! spawned it and is not ported. Since `XTASK.13` the controls judge a small frozen tree, never the real board or its
//! processor's dossier, so a damaged real one fails by its own name (ruling 5): `BOARD-VERDICT`'s frozen definition and
//! composed obligations, and a frozen profile the generator prefers to the repository's, pinned by the digest of an untracked
//! directory, with the script's mutations (its `sed` and Python edits as the same first-occurrence replacements), and "no
//! board" told apart from a board whose definition was deleted. Each self-test arm is one `tally.arm(` call,
//! the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{combined, locale_sorted, scratch};

/// The frozen definition and composed obligations the controls judge: the ones `BOARD-VERDICT`'s controls read.
const FROZEN_BOARD: &str = "scripts/fixtures/board-verdict";
/// The frozen processor profile: a board's sibling unit, which `gen_platform.read_processor` prefers to the repository's.
const FROZEN_PROFILE: &str = "scripts/fixtures/platform-gen/rv64i-lab-v0/profile.sexp";
/// The frozen unit's release identity (P4-SYSTEM.20 slice a2): the pin's version is held to it.
const FROZEN_IDENTITY: &str = "scripts/fixtures/platform-gen/rv64i-lab-v0/identity.sexp";
const EMPTY_DIGEST: &str = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";

/// `python3 scripts/gen_platform.py <args>` from the root, stdout and stderr together as `2>&1` joined them.
fn generator(repo: &Path, args: &[&str]) -> (i32, String) {
    combined(
        Command::new("python3")
            .arg("scripts/gen_platform.py")
            .args(args)
            .current_dir(repo),
    )
}

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

/// `diff -r a b` is silent: the same names with the same bytes on both sides, recursively.
fn same_tree(a: &Path, b: &Path) -> bool {
    let names = |dir: &Path| -> Option<Vec<std::ffi::OsString>> {
        let mut v: Vec<_> = fs::read_dir(dir)
            .ok()?
            .flatten()
            .map(|e| e.file_name())
            .collect();
        v.sort();
        Some(v)
    };
    let (Some(na), Some(nb)) = (names(a), names(b)) else {
        return false;
    };
    if na != nb {
        return false;
    }
    na.iter().all(|name| {
        let (pa, pb) = (a.join(name), b.join(name));
        match (pa.is_dir(), pb.is_dir()) {
            (true, true) => same_tree(&pa, &pb),
            (false, false) => fs::read(&pa).ok() == fs::read(&pb).ok(),
            _ => false,
        }
    })
}

/// `sed 's/PAT/REPL/' src > dst`: the first occurrence on every line, the pattern being literal text.
fn sed_literal(src: &Path, dst: &Path, pattern: &str, replacement: &str) {
    let text = fs::read_to_string(src).unwrap_or_default();
    let out: String = text
        .split_inclusive('\n')
        .map(|line| line.replacen(pattern, replacement, 1))
        .collect();
    let _ = fs::write(dst, out);
}

/// `sed 's/(dossier-sha256 "[0-9a-f]…")/(dossier-sha256 "<digest>")/' src > dst`: the pin's hex digits — exactly 64 of
/// them, or any run of them — replaced on the first match of every line.
fn sed_pin(src: &Path, dst: &Path, exactly_64: bool, digest: &str) {
    const HEAD: &str = "(dossier-sha256 \"";
    let text = fs::read_to_string(src).unwrap_or_default();
    let mut out = String::with_capacity(text.len());
    for line in text.split_inclusive('\n') {
        let mut replaced = false;
        let mut from = 0;
        while let Some(at) = line[from..].find(HEAD) {
            let start = from + at + HEAD.len();
            let hex = line[start..]
                .chars()
                .take_while(char::is_ascii_hexdigit)
                .filter(|c| !c.is_ascii_uppercase())
                .count();
            let end = start + hex;
            if line[end..].starts_with("\")") && (!exactly_64 || hex == 64) {
                out.push_str(&line[..start]);
                out.push_str(digest);
                out.push_str(&line[end..]);
                replaced = true;
                break;
            }
            from = start;
        }
        if !replaced {
            out.push_str(line);
        }
    }
    let _ = fs::write(dst, out);
}

/// `grep -v 'PAT' src > dst`: every line not containing the text.
fn grep_v(src: &Path, dst: &Path, pattern: &str) {
    let text = fs::read_to_string(src).unwrap_or_default();
    let out: String = text
        .split_inclusive('\n')
        .filter(|line| !line.contains(pattern))
        .collect();
    let _ = fs::write(dst, out);
}

fn copy(from: &Path, to_dir: &Path, names: &[&str]) {
    let _ = fs::create_dir_all(to_dir);
    for name in names {
        let _ = fs::copy(from.join(name), to_dir.join(name));
    }
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
    /// One arm: the run's exit status must be `expected` and its output must contain `want` — or, with an empty
    /// `want`, there must be no output at all.
    fn arm(&mut self, name: &str, rc: i32, expected: i32, out: &str, want: &str) {
        if want.is_empty() {
            if rc == expected && out.is_empty() {
                self.pass += 1;
                return;
            }
            self.fail += 1;
            self.report(format!("PLATFORM-GEN self-test MISS: {name} — expected rc={expected} and no output, got rc={rc}\n{out}"));
            return;
        }
        if rc == expected && out.contains(want) {
            self.pass += 1;
        } else {
            self.fail += 1;
            self.report(format!("PLATFORM-GEN self-test MISS: {name} — expected rc={expected} (reason: {want}), got rc={rc}\n{out}"));
        }
    }
}

/// The RED/GREEN controls over a scratch copy of the real board: the definition and the composed obligations the export
/// derives from (the processor unit resolves to the repository's dossier, so the digest pin verifies live).
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "platformgen") else {
        eprintln!("PLATFORM-GEN self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    // Every board here sits beside the frozen profile. Its directory is untracked, so its dossier digest is the empty one,
    // and the frozen board is pinned to that: the pin stays load-bearing, and the real dossier is never read.
    let board = t.join("netboard-lab-v0");
    let _ = fs::create_dir_all(&board);
    let _ = fs::create_dir_all(t.join("rv64i-lab-v0"));
    let _ = fs::copy(
        repo.join(FROZEN_PROFILE),
        t.join("rv64i-lab-v0/profile.sexp"),
    );
    let _ = fs::copy(
        repo.join(FROZEN_IDENTITY),
        t.join("rv64i-lab-v0/identity.sexp"),
    );
    sed_pin(
        &repo.join(FROZEN_BOARD).join("board.sexp"),
        &board.join("board.sexp"),
        false,
        EMPTY_DIGEST,
    );
    copy(
        &repo.join(FROZEN_BOARD),
        &board,
        &["contract-obligations.sexp"],
    );
    let p = |rel: &str| t.join(rel).display().to_string();
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
        misses: Vec::new(),
    };
    // GREEN: the generator emits the manifest from the frozen inputs.
    let (rc, out) = generator(
        repo,
        &["--board-dir", &p("netboard-lab-v0"), "--out-dir", &p("out")],
    );
    tally.arm(
        "GREEN the generator emits the manifest from the frozen inputs",
        rc,
        0,
        captured(&out),
        "platform.sexp generated",
    );
    // GREEN: determinism — a second derivation is byte-identical.
    let _ = Command::new("python3")
        .args([
            "scripts/gen_platform.py",
            "--board-dir",
            &p("netboard-lab-v0"),
            "--out-dir",
            &p("out2"),
        ])
        .current_dir(repo)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status();
    let (rc, out) = if same_tree(&t.join("out"), &t.join("out2")) {
        (0, String::new())
    } else {
        (1, "nondeterministic".to_owned())
    };
    tally.arm("GREEN two derivations are byte-identical", rc, 0, &out, "");
    // GREEN: a faithful generation is judged in sync — derive, then re-derive against it.
    let (rc, out) = generator(
        repo,
        &[
            "--check",
            "--board-dir",
            &p("netboard-lab-v0"),
            "--out-dir",
            &p("out"),
        ],
    );
    tally.arm(
        "GREEN a faithful generation is judged in sync",
        rc,
        0,
        captured(&out),
        "byte-exact",
    );
    // RED: a hand-edited manifest is detected and named: the generation just judged in sync, with one comment added.
    copy(&t.join("out"), &t.join("d1"), &["platform.sexp"]);
    let mut edited = fs::read(t.join("d1/platform.sexp")).unwrap_or_default();
    edited.extend_from_slice(b"\n;; hand edit\n");
    let _ = fs::write(t.join("d1/platform.sexp"), edited);
    let (rc, out) = generator(
        repo,
        &[
            "--check",
            "--board-dir",
            &p("netboard-lab-v0"),
            "--out-dir",
            &p("d1"),
        ],
    );
    tally.arm(
        "RED a hand-edited platform.sexp is refused, naming DRIFT",
        rc,
        1,
        captured(&out),
        "platform.sexp: DRIFT",
    );
    // RED: a board.sexp edit against that same generation is drift, named: the definition moved, the export did not.
    let _ = fs::copy(board.join("board.sexp"), t.join("board-kept.sexp"));
    sed_literal(
        &t.join("board-kept.sexp"),
        &board.join("board.sexp"),
        "(id \"netboard-lab-v0\")",
        "(id \"netboard-lab-v9\")",
    );
    let (rc, out) = generator(
        repo,
        &[
            "--check",
            "--board-dir",
            &p("netboard-lab-v0"),
            "--out-dir",
            &p("out"),
        ],
    );
    tally.arm(
        "RED a moved definition against a stale export is refused, naming DRIFT",
        rc,
        1,
        captured(&out),
        "DRIFT",
    );
    let _ = fs::copy(t.join("board-kept.sexp"), board.join("board.sexp"));
    // RED: a stale dossier pin is refused by name — the pin is load-bearing, not display.
    copy(&board, &t.join("d3"), &["contract-obligations.sexp"]);
    sed_pin(
        &board.join("board.sexp"),
        &t.join("d3/board.sexp"),
        true,
        "0000000000000000000000000000000000000000000000000000000000000000",
    );
    let (rc, out) = generator(repo, &["--board-dir", &p("d3"), "--out-dir", &p("d3o")]);
    tally.arm(
        "RED a stale dossier-sha256 pin is refused, named",
        rc,
        2,
        captured(&out),
        "STALE",
    );
    // RED: the pin's version is held to the unit's identity (P4-SYSTEM.20 slice a2): a board pinning a version the unit
    // does not name is refused by name. Only the processor's version line is indented four spaces.
    copy(&board, &t.join("d5"), &["contract-obligations.sexp"]);
    sed_literal(
        &board.join("board.sexp"),
        &t.join("d5/board.sexp"),
        "    (version \"0\")",
        "    (version \"9\")",
    );
    let (rc, out) = generator(repo, &["--board-dir", &p("d5"), "--out-dir", &p("d5o")]);
    tally.arm(
        "RED a processor version the unit's identity does not name is refused, named",
        rc,
        2,
        captured(&out),
        "version pin DISAGREES",
    );
    // RED: a processor unit with no identity states no version to hold the pin to, and is refused by name.
    copy(
        &board,
        &t.join("d6/units/netboard-lab-v0"),
        &["board.sexp", "contract-obligations.sexp"],
    );
    let _ = fs::create_dir_all(t.join("d6/units/rv64i-lab-v0"));
    let _ = fs::copy(
        repo.join(FROZEN_PROFILE),
        t.join("d6/units/rv64i-lab-v0/profile.sexp"),
    );
    let (rc, out) = generator(
        repo,
        &[
            "--board-dir",
            &p("d6/units/netboard-lab-v0"),
            "--out-dir",
            &p("d6o"),
        ],
    );
    tally.arm(
        "RED a processor unit with no identity.sexp is refused, named",
        rc,
        2,
        captured(&out),
        "identity.sexp is missing",
    );
    // RED: a processor profile without endianness is refused by name — the untracked sibling unit hashes zero inputs,
    // so the pin is set to that digest and the arm isolates the endianness refusal from the pin refusal.
    copy(
        &board,
        &t.join("d4/units/netboard-lab-v0"),
        &["contract-obligations.sexp"],
    );
    let _ = fs::create_dir_all(t.join("d4/units/rv64i-lab-v0"));
    let _ = fs::copy(
        repo.join(FROZEN_IDENTITY),
        t.join("d4/units/rv64i-lab-v0/identity.sexp"),
    );
    if let Ok(src) = fs::read_to_string(repo.join(FROZEN_PROFILE)) {
        if src.contains("(endianness little) ") {
            let _ = fs::write(
                t.join("d4/units/rv64i-lab-v0/profile.sexp"),
                src.replace("(endianness little) ", ""),
            );
        }
    }
    sed_pin(
        &board.join("board.sexp"),
        &t.join("d4/units/netboard-lab-v0/board.sexp"),
        false,
        EMPTY_DIGEST,
    );
    let (rc, out) = generator(
        repo,
        &[
            "--board-dir",
            &p("d4/units/netboard-lab-v0"),
            "--out-dir",
            &p("d4o"),
        ],
    );
    tally.arm(
        "RED a profile without endianness is refused, naming the owner",
        rc,
        2,
        captured(&out),
        "'endianness' is absent",
    );
    // RED: a boot load-region that is not executable RAM is refused by name.
    copy(&board, &t.join("d5"), &["contract-obligations.sexp"]);
    sed_literal(
        &board.join("board.sexp"),
        &t.join("d5/board.sexp"),
        "(load-region \"ram0\")",
        "(load-region \"eth0\")",
    );
    let (rc, out) = generator(repo, &["--board-dir", &p("d5"), "--out-dir", &p("d5o")]);
    tally.arm(
        "RED a load-region that is not executable RAM is refused",
        rc,
        2,
        captured(&out),
        "executable RAM",
    );
    // RED: a test-control claim the wiring contradicts — console capture over a recording sink.
    copy(&board, &t.join("d6"), &["contract-obligations.sexp"]);
    if let Ok(src) = fs::read_to_string(board.join("board.sexp")) {
        let _ = fs::write(
            t.join("d6/board.sexp"),
            src.replace(
                "(serial-console\n    (device \"uart0\"))",
                "(serial-console\n    (device \"eth0\"))",
            ),
        );
    }
    let (rc, out) = generator(repo, &["--board-dir", &p("d6"), "--out-dir", &p("d6o")]);
    tally.arm(
        "RED console capture without a host-console backend is refused",
        rc,
        2,
        captured(&out),
        "host-console",
    );
    // RED: a composed unit missing the obligation the time facts derive from is refused by name.
    copy(&board, &t.join("d7"), &["board.sexp"]);
    grep_v(
        &board.join("contract-obligations.sexp"),
        &t.join("d7/contract-obligations.sexp"),
        "(id \"OB-ENV-VIRTUAL-TIME\")",
    );
    let (rc, out) = generator(repo, &["--board-dir", &p("d7"), "--out-dir", &p("d7o")]);
    tally.arm(
        "RED a missing time obligation is refused, named",
        rc,
        2,
        captured(&out),
        "OB-ENV-VIRTUAL-TIME",
    );
    // RED: a time source other than "none" is a shape the generator cannot emit.
    copy(&board, &t.join("d8"), &["board.sexp"]);
    sed_literal(
        &board.join("contract-obligations.sexp"),
        &t.join("d8/contract-obligations.sexp"),
        "(name time_source) (value (str \"none\"))",
        "(name time_source) (value (str \"host\"))",
    );
    let (rc, out) = generator(repo, &["--board-dir", &p("d8"), "--out-dir", &p("d8o")]);
    tally.arm(
        "RED a non-none time source is refused, named",
        rc,
        2,
        captured(&out),
        "other than",
    );
    // GREEN: a tree that declares no board reads as one, and says so.
    let _ = fs::create_dir_all(t.join("none/profiles/a-unit"));
    let (rc, out) = judge(repo, &t.join("none"));
    tally.arm(
        "GREEN a tree with no board reads as none",
        rc,
        0,
        &out,
        "no board declares itself yet",
    );
    // RED: a generated manifest with no definition beside it is a deleted board, not "no board", and it is named.
    let _ = fs::create_dir_all(t.join("gone/profiles/a-board"));
    let _ = fs::write(
        t.join("gone/profiles/a-board/platform.sexp"),
        "(platform)\n",
    );
    let (rc, out) = judge(repo, &t.join("gone"));
    tally.arm(
        "RED a manifest whose board.sexp is gone is refused by name",
        rc,
        1,
        &out,
        "profiles/a-board/board.sexp: missing",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "PLATFORM-GEN --self-test: {} pass / {} fail",
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

/// `profiles/*/board.sexp`, in the shell glob's order (the locale's collation).
fn boards(root: &Path) -> Vec<String> {
    let found: Vec<String> = fs::read_dir(root.join("profiles"))
        .map(|entries| {
            entries
                .flatten()
                .filter(|e| e.path().join("board.sexp").is_file())
                .map(|e| format!("profiles/{}/board.sexp", e.file_name().to_string_lossy()))
                .collect()
        })
        .unwrap_or_default();
    locale_sorted(found)
}

/// `profiles/*/platform.sexp` with no `board.sexp` beside it. The manifest is only ever generated from a board, so this is a
/// board whose definition was deleted, which must not read as "no board declares itself" (ruling 5: `XTASK.13`).
fn orphaned(root: &Path) -> Vec<String> {
    let found: Vec<String> = fs::read_dir(root.join("profiles"))
        .map(|entries| {
            entries
                .flatten()
                .filter(|e| {
                    e.path().join("platform.sexp").is_file()
                        && !e.path().join("board.sexp").is_file()
                })
                .map(|e| format!("profiles/{}/board.sexp", e.file_name().to_string_lossy()))
                .collect()
        })
        .unwrap_or_default();
    locale_sorted(found)
}

/// The real run's verdict over the units under `root`, as (status, what it prints); the generator runs from `repo`.
fn judge(repo: &Path, root: &Path) -> (i32, String) {
    let gone = orphaned(root);
    if !gone.is_empty() {
        let names: Vec<String> = gone
            .iter()
            .map(|path| format!("{path}: missing, though its generated platform.sexp is present"))
            .collect();
        return (
            1,
            format!(
                "{}\nPLATFORM-GEN: FAIL — a board's canonical definition is gone.",
                names.join("\n")
            ),
        );
    }
    let defs = boards(root);
    if defs.is_empty() {
        return (
            0,
            "PLATFORM-GEN: ok (no board declares itself yet)".to_owned(),
        );
    }
    let (rc, out) = generator(repo, &["--check"]);
    if rc != 0 {
        return (
            1,
            format!(
                "{}\nPLATFORM-GEN: FAIL — a platform capability manifest is out of sync with its canonical inputs.",
                captured(&out)
            ),
        );
    }
    (
        0,
        format!(
            "PLATFORM-GEN: ok ({} board(s) — the platform capability manifest is a byte-exact function of its canonical inputs, the dossier pin verified live)",
            defs.len()
        ),
    )
}

/// `cargo xtask check-platform-gen [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !self_test(root, false) {
        eprintln!("PLATFORM-GEN: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let (rc, out) = judge(root, root);
    if rc != 0 {
        eprintln!("{out}");
        return ExitCode::from(1);
    }
    println!("{out}");
    ExitCode::SUCCESS
}
