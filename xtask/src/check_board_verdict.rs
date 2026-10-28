//! The `BOARD-VERDICT` doctrine's driver, ported from `scripts/check_board_verdict.sh` (`XTASK.6` slice `6u`), which is
//! now a shim of `cargo xtask check-board-verdict`.
//!
//! `P5-BOARD.4`: a board's composition verdict is DECIDED, not narrated (`docs/CPU_ENVIRONMENT.md` §5, `ENV-02`). For
//! every tracked board (`profiles/*/board.sexp`), `scripts/board_verdict.py` — the pinned Python judge, spawned exactly
//! as the driver spawned it and not ported — decides three legs over the board's own data: every CPU
//! environment-assumption discharged by named guarantees, every `satisfies` edge resolved, every deferred device
//! obligation answered by exactly one board decision. Any leg failing REJECTS the composition by name. The controls
//! run over scratch copies of the real board with the script's text mutations (an answer removed, an answer to a
//! ghost, an obligation answered twice, a `satisfies` edge to a ghost, a guarantee's line removed), each judged.
//! HONEST LIMIT, the script's: the verdict is decided against the DATA; the dossiers' own gates own whether the device
//! facts are true. Each self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::process::ExitCode;

use crate::harness::{combined, locale_sorted, scratch};

/// The controls' frozen copies of the board's four documents (`XTASK.11` slice b, ruling 5,
/// `decision_doctrine-controls-refuse-and-freeze.md`): copied from `profiles/netboard-lab-v0` on 2026-10-28, never refreshed by a corpus
/// edit, so a wrong live board fails by name in the real check instead of making the controls refuse.
const FIXTURE: &str = "scripts/fixtures/board-verdict";
const DOCS: [&str; 4] = [
    "board.sexp",
    "requirements.sexp",
    "contract-obligations.sexp",
    "sources.sexp",
];

/// `python3 scripts/board_verdict.py <dir>` from the root, stdout and stderr together as `2>&1` joined them.
fn verdict(repo: &Path, dir: &str) -> (i32, String) {
    combined(
        Command::new("python3")
            .arg("scripts/board_verdict.py")
            .arg(dir)
            .current_dir(repo),
    )
}

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: the judge's exit status must be `expected` and its output must contain `want`.
    fn arm(&mut self, name: &str, rc: i32, expected: i32, out: &str, want: &str) {
        if rc == expected && out.contains(want) {
            self.pass += 1;
        } else {
            self.fail += 1;
            if self.verbose {
                eprintln!("BOARD-VERDICT self-test MISS: {name} — expected rc={expected} (reason: {want}), got rc={rc}\n{out}");
            }
        }
    }
}

/// `cp "$t/board"/* "$t/<name>/"`: a fresh copy of the scratch board under another name.
fn copy_board(t: &Path, name: &str) -> PathBuf {
    let dir = t.join(name);
    let _ = fs::create_dir_all(&dir);
    for doc in DOCS {
        let _ = fs::copy(t.join("board").join(doc), dir.join(doc));
    }
    dir
}

/// `p.write_text(p.read_text().replace(a, b))`: every occurrence, as Python's `str.replace` replaces.
fn replace_in(path: &Path, from: &str, to: &str) {
    if let Ok(text) = fs::read_to_string(path) {
        let _ = fs::write(path, text.replace(from, to));
    }
}

/// The RED/GREEN controls over scratch copies of the real board — the definition plus the composed catalogues the
/// verdict reads (their freshness against the definition is `BOARD-GEN`'s).
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "boardverdict") else {
        eprintln!("BOARD-VERDICT self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    let _ = fs::create_dir_all(t.join("board"));
    for doc in DOCS {
        let _ = fs::copy(repo.join(FIXTURE).join(doc), t.join("board").join(doc));
    }
    let judge = |dir: &Path| verdict(repo, &dir.display().to_string());
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    // GREEN: the frozen board's composition is ACCEPTED, every edge printed.
    let (rc, out) = judge(&t.join("board"));
    tally.arm(
        "GREEN the frozen board's composition is ACCEPTED",
        rc,
        0,
        captured(&out),
        "composition ACCEPTED",
    );
    // RED: a marked obligation left unanswered is a rejection, named.
    let dir = copy_board(&t, "unanswered");
    replace_in(
        &dir.join("board.sexp"),
        "(answers \"OB-NIC-STRAP-RESETS\"))",
        ")",
    );
    let (rc, out) = judge(&dir);
    tally.arm(
        "RED a deferred obligation no decision answers",
        rc,
        1,
        captured(&out),
        "UNANSWERED COMPOSITION OBLIGATION 'OB-NIC-STRAP-RESETS'",
    );
    // RED: an answers edge naming nothing marked is a rejection, named.
    let dir = copy_board(&t, "ghost");
    replace_in(
        &dir.join("board.sexp"),
        "(answers \"OB-NIC-STRAP-RESETS\")",
        "(answers \"OB-NIC-GHOST\")",
    );
    let (rc, out) = judge(&dir);
    tally.arm(
        "RED an answers edge to nothing marked",
        rc,
        1,
        captured(&out),
        "ANSWERS NOTHING",
    );
    // RED: an obligation answered by two decisions is a rejection, named.
    let dir = copy_board(&t, "twice");
    replace_in(
        &dir.join("board.sexp"),
        "(answers \"OB-NIC-TIME-SOURCES\")",
        "(answers \"OB-NIC-TIME-SOURCES\") (answers \"OB-NIC-STRAP-RESETS\")",
    );
    let (rc, out) = judge(&dir);
    tally.arm(
        "RED a deferred obligation answered twice",
        rc,
        1,
        captured(&out),
        "ANSWERED TWICE",
    );
    // RED: a satisfies edge naming no environment-assumption is a rejection, named.
    let dir = copy_board(&t, "sghost");
    replace_in(
        &dir.join("board.sexp"),
        "(satisfies \"OB-ENV-RESET\")",
        "(satisfies \"OB-ENV-GHOST\")",
    );
    let (rc, out) = judge(&dir);
    tally.arm(
        "RED a satisfies edge to no environment-assumption",
        rc,
        1,
        captured(&out),
        "SATISFIES EDGE 'OB-ENV-GHOST'",
    );
    // RED: the discharge leg armed — a guarantee removed from the composed catalogue rejects the composition.
    let dir = copy_board(&t, "nog");
    let obligations = dir.join("contract-obligations.sexp");
    if let Ok(text) = fs::read_to_string(&obligations) {
        let kept: String = text
            .split_inclusive('\n')
            .filter(|l| !l.contains("(obligation (id \"OB-ENTRY-STATE\")"))
            .collect();
        let _ = fs::write(&obligations, kept);
    }
    let (rc, out) = judge(&dir);
    tally.arm(
        "RED a guarantee removed — the discharge rejects",
        rc,
        1,
        captured(&out),
        "DANGLING DEP",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "BOARD-VERDICT --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
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

/// `profiles/*` units holding `composition.sexp` (the board generator's manifest, derived from `board.sexp`) but no
/// `board.sexp`, in the shell glob's order.
fn orphaned_units(root: &Path) -> Vec<String> {
    let found: Vec<String> = fs::read_dir(root.join("profiles"))
        .map(|entries| {
            entries
                .flatten()
                .filter(|e| {
                    e.path().join("composition.sexp").is_file()
                        && !e.path().join("board.sexp").is_file()
                })
                .map(|e| format!("profiles/{}", e.file_name().to_string_lossy()))
                .collect()
        })
        .unwrap_or_default();
    locale_sorted(found)
}

/// `cargo xtask check-board-verdict [--self-test]`: the shell driver's verdict lines and exit statuses.
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
        eprintln!("BOARD-VERDICT: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let defs = boards(root);
    // A unit holding the board generator's manifest without the definition it derives from is a deleted board, not
    // "no board yet" (`XTASK.11` slice d, ruling 5: a wrong live board fails by name).
    let orphans = orphaned_units(root);
    if !orphans.is_empty() {
        for dir in &orphans {
            eprintln!("BOARD-VERDICT: FAIL — {dir}/composition.sexp is generated from a board definition, but {dir}/board.sexp is absent. Restore the definition, or remove its generated artifacts with it.");
        }
        return ExitCode::from(1);
    }
    if defs.is_empty() {
        println!("BOARD-VERDICT: ok (no board declares itself yet)");
        return ExitCode::SUCCESS;
    }
    let mut failed = false;
    for def in &defs {
        let dir = def.strip_suffix("/board.sexp").unwrap_or(def);
        let (rc, out) = verdict(root, dir);
        if rc != 0 {
            eprintln!("{}", captured(&out));
            eprintln!("BOARD-VERDICT: FAIL — the composition does not hold.");
            failed = true;
        }
    }
    if failed {
        return ExitCode::from(1);
    }
    println!(
        "BOARD-VERDICT: ok ({} board(s) — every CPU assumption discharged, every satisfies edge resolved, every composition disposition bound)",
        defs.len()
    );
    ExitCode::SUCCESS
}
