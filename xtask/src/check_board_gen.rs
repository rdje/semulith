//! The `BOARD-GEN` doctrine's driver, ported from `scripts/check_board_gen.sh` (`XTASK.6` slice `6v`), which is now a
//! shim of `cargo xtask check-board-gen`.
//!
//! A board's manifest, composed catalogues, hardware description and map are GENERATED from the canonical definition
//! (`profiles/*/board.sexp`) by `scripts/gen_board.py`; this check regenerates them in memory and refuses the day a
//! committed artifact stops byte-matching its derivation — a hand-edited or stale artifact is a running total. The
//! generator is spawned exactly as the driver spawned it and is not ported; the controls run over a scratch copy of the
//! real definition (the generator's part resolution falls back to the repository's units): the seven artifacts emitted,
//! two derivations byte-identical, a faithful generation in sync, three hand-edited artifacts and a moved definition
//! named as DRIFT, an overlapping region and an undeclared device refused at generation. HONEST LIMIT, the script's: it
//! says nothing about whether the definition is TRUE. Each self-test arm is one `tally.arm(` call, the idiom the
//! `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{combined, locale_sorted, scratch};

const BOARD: &str = "profiles/netboard-lab-v0";

/// `python3 scripts/gen_board.py <args>` from the root, stdout and stderr together as `2>&1` joined them.
fn generator(repo: &Path, args: &[&str]) -> (i32, String) {
    combined(
        Command::new("python3")
            .arg("scripts/gen_board.py")
            .args(args)
            .current_dir(repo),
    )
}

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

/// `cp -r src dst`: a directory tree copied, files and directories.
fn copy_tree(src: &Path, dst: &Path) {
    let _ = fs::create_dir_all(dst);
    let Ok(entries) = fs::read_dir(src) else {
        return;
    };
    for entry in entries.flatten() {
        let target = dst.join(entry.file_name());
        if entry.path().is_dir() {
            copy_tree(&entry.path(), &target);
        } else {
            let _ = fs::copy(entry.path(), target);
        }
    }
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

/// `printf '\n;; hand edit\n' >> file`.
fn hand_edit(path: &Path) {
    let mut text = fs::read(path).unwrap_or_default();
    text.extend_from_slice(b"\n;; hand edit\n");
    let _ = fs::write(path, text);
}

/// `p.write_text(p.read_text().replace(a, b))`: every occurrence, as Python's `str.replace` replaces.
fn replace_in(path: &Path, from: &str, to: &str) {
    if let Ok(text) = fs::read_to_string(path) {
        let _ = fs::write(path, text.replace(from, to));
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
            self.report(format!("BOARD-GEN self-test MISS: {name} — expected rc={expected} and no output, got rc={rc}\n{out}"));
            return;
        }
        if rc == expected && out.contains(want) {
            self.pass += 1;
        } else {
            self.fail += 1;
            self.report(format!("BOARD-GEN self-test MISS: {name} — expected rc={expected} (reason: {want}), got rc={rc}\n{out}"));
        }
    }
}

/// The RED/GREEN controls over a scratch copy of the real board definition.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "boardgen") else {
        eprintln!(
            "BOARD-GEN self-test: cannot create a scratch directory under target/doctrine-selftest"
        );
        return false;
    };
    let _ = fs::create_dir_all(t.join("board"));
    let _ = fs::copy(
        repo.join(BOARD).join("board.sexp"),
        t.join("board/board.sexp"),
    );
    let p = |rel: &str| t.join(rel).display().to_string();
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
        misses: Vec::new(),
    };
    // GREEN: the generator emits all seven artifacts from the real definition.
    let (rc, out) = generator(repo, &["--board-dir", &p("board"), "--out-dir", &p("out")]);
    tally.arm(
        "GREEN the generator emits the artifacts from the real definition",
        rc,
        0,
        captured(&out),
        "7 artifact(s)",
    );
    // GREEN: determinism — a second derivation is byte-identical.
    let _ = Command::new("python3")
        .args([
            "scripts/gen_board.py",
            "--board-dir",
            &p("board"),
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
    // GREEN: a faithful generation is judged in sync.
    let (rc, out) = generator(
        repo,
        &[
            "--check",
            "--board-dir",
            &p("board"),
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
    // RED: a hand-edited hardware description is detected and named.
    copy_tree(&t.join("out"), &t.join("d1"));
    hand_edit(&t.join("d1/hardware.sexp"));
    let (rc, out) = generator(
        repo,
        &["--check", "--board-dir", &p("board"), "--out-dir", &p("d1")],
    );
    tally.arm(
        "RED a hand-edited hardware.sexp is refused, naming DRIFT",
        rc,
        1,
        captured(&out),
        "hardware.sexp: DRIFT",
    );
    // RED: a hand-edited composed catalogue is detected and named.
    copy_tree(&t.join("out"), &t.join("d2"));
    hand_edit(&t.join("d2/requirements.sexp"));
    let (rc, out) = generator(
        repo,
        &["--check", "--board-dir", &p("board"), "--out-dir", &p("d2")],
    );
    tally.arm(
        "RED a hand-edited composed catalogue is refused, naming DRIFT",
        rc,
        1,
        captured(&out),
        "requirements.sexp: DRIFT",
    );
    // RED: a hand-edited manifest is detected and named.
    copy_tree(&t.join("out"), &t.join("d3"));
    hand_edit(&t.join("d3/composition.sexp"));
    let (rc, out) = generator(
        repo,
        &["--check", "--board-dir", &p("board"), "--out-dir", &p("d3")],
    );
    tally.arm(
        "RED a hand-edited manifest is refused, naming DRIFT",
        rc,
        1,
        captured(&out),
        "composition.sexp: DRIFT",
    );
    // RED: a board.sexp edit against stale artifacts is drift, named — the definition moved, the map did not.
    let _ = fs::copy(t.join("board/board.sexp"), t.join("board-moved.sexp"));
    replace_in(
        &t.join("board/board.sexp"),
        "(base \"0x1002_0000\")",
        "(base \"0x1002_1000\")",
    );
    let (rc, out) = generator(
        repo,
        &[
            "--check",
            "--board-dir",
            &p("board"),
            "--out-dir",
            &p("out"),
        ],
    );
    tally.arm(
        "RED a moved definition against stale artifacts is refused, naming DRIFT",
        rc,
        1,
        captured(&out),
        "DRIFT",
    );
    let _ = fs::copy(t.join("board-moved.sexp"), t.join("board/board.sexp"));
    // RED: an overlapping region is refused by name, at generation, before any artifact.
    let _ = fs::create_dir_all(t.join("overlap"));
    let _ = fs::copy(t.join("board/board.sexp"), t.join("overlap/board.sexp"));
    replace_in(
        &t.join("overlap/board.sexp"),
        "(base \"0x1002_0000\")",
        "(base \"0x1001_0800\")",
    );
    let (rc, out) = generator(
        repo,
        &["--board-dir", &p("overlap"), "--out-dir", &p("ovo")],
    );
    tally.arm(
        "RED an overlapping region is refused, naming both regions",
        rc,
        2,
        captured(&out),
        "overlap",
    );
    // RED: an mmio region naming an undeclared device is refused by name.
    let _ = fs::create_dir_all(t.join("ghost"));
    let _ = fs::copy(t.join("board/board.sexp"), t.join("ghost/board.sexp"));
    replace_in(
        &t.join("ghost/board.sexp"),
        "(device \"eth0\")",
        "(device \"eth9\")",
    );
    let (rc, out) = generator(repo, &["--board-dir", &p("ghost"), "--out-dir", &p("gho")]);
    tally.arm(
        "RED an mmio region naming an undeclared device is refused by name",
        rc,
        2,
        captured(&out),
        "undeclared device",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "BOARD-GEN --self-test: {} pass / {} fail",
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

/// `cargo xtask check-board-gen [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    // Re-run the controls before judging: a check that no longer discriminates must refuse, not pass.
    if !self_test(root, false) {
        eprintln!("BOARD-GEN: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let defs = boards(root);
    if defs.is_empty() {
        println!("BOARD-GEN: ok (no board declares itself yet)");
        return ExitCode::SUCCESS;
    }
    let (rc, out) = generator(root, &["--check"]);
    if rc != 0 {
        eprintln!("{}", captured(&out));
        eprintln!("BOARD-GEN: FAIL — a generated board artifact is out of sync with its canonical definition.");
        return ExitCode::from(1);
    }
    println!(
        "BOARD-GEN: ok ({} board(s) — manifest, composed catalogues, hardware description and map all byte-exact functions of the canonical definition)",
        defs.len()
    );
    ExitCode::SUCCESS
}
