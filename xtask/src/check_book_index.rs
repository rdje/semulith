//! The `BOOK-INDEX` doctrine's driver, ported from `scripts/check_book_index.sh` (`XTASK.6` slice `6t`), which is now a
//! shim of `cargo xtask check-book-index`.
//!
//! `docs/book/src/index.md` is GENERATED from the book's own text by `scripts/gen_book_index.py` (`BOOK-APPARATUS.1`;
//! `OWN-03`: generated artifacts are changed by regeneration, never by direct editing). This check regenerates the index
//! in memory and refuses the day it stops byte-matching the committed file — a hand-edited or stale index is a running
//! total, a memory of a measurement. What it protects is the DERIVATION: the book's text is the authority, the index its
//! mirror. HONEST LIMIT, the script's: it says nothing about whether the chapters are true. The generator is spawned
//! exactly as the driver spawned it and is not ported; status 1 denotes its named drift verdict, every other failure
//! stays a refusal. Each self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.
//!
//! The controls judge a small frozen book, `scripts/fixtures/book-index/` (`XTASK.13`, ruling 5's rule): the real book's
//! damage is the real check's to name, and it must not read as a check that stopped discriminating. So a chapter or a
//! glossary deleted from the real tree fails below by its own name, and the self-test stays green.

use std::fs;
use std::path::Path;
use std::process::{Command, ExitCode};

use crate::harness::{combined, scratch};

const BOOK: &str = "docs/book";
const GLOSSARY: &str = "docs/GLOSSARY.md";
const OUT: &str = "docs/book/src/index.md";
/// The frozen book the controls judge: five chapters' worth of structure, its index generated and committed beside it.
const FROZEN: &str = "scripts/fixtures/book-index";

/// `python3 scripts/gen_book_index.py <args>` from the root, stdout and stderr together as `2>&1` joined them.
fn generator(repo: &Path, args: &[&str]) -> (i32, String) {
    generator_in(repo, repo, args)
}

/// The same generator with its relative paths read from `cwd`, so the real judgement runs over a frozen root unchanged.
fn generator_in(repo: &Path, cwd: &Path, args: &[&str]) -> (i32, String) {
    combined(
        Command::new("python3")
            .arg(repo.join("scripts/gen_book_index.py"))
            .args(args)
            .current_dir(cwd),
    )
}

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

/// `judge_generator <rc> <output>`: the verdict and what the shell function printed to stderr. Status 1 denotes the
/// generator's named drift verdict; other failures cannot establish drift and stay refusal 2, launch failures and
/// unknown exits included.
fn judge_generator(rc: i32, output: &str) -> (i32, String) {
    if rc == 0 {
        return (0, String::new());
    }
    let mut err = format!("{output}\n");
    if rc == 1
        && output
            .lines()
            .any(|l| l.starts_with("gen_book_index: DRIFT — "))
    {
        err.push_str(&format!(
            "BOOK-INDEX: FAIL — {OUT} is out of sync with the book. Regenerate — never edit:\n  python3 scripts/gen_book_index.py\n"
        ));
        return (1, err);
    }
    err.push_str(&format!(
        "BOOK-INDEX: REFUSED — the generator cannot judge {OUT} (exit{rc}).\n"
    ));
    (2, err)
}

/// The real judgement of the book under `root`: the verdict, and the line it prints on success or the report on failure.
/// `no project book yet` means there is no book directory at all: a book whose `SUMMARY.md` is gone is damage, and the
/// generator refuses it by name.
fn judge_book(repo: &Path, root: &Path) -> (i32, String) {
    if !root.join(BOOK).is_dir() {
        return (0, "BOOK-INDEX: ok (no project book yet)".to_owned());
    }
    let (rc, out) = generator_in(
        repo,
        root,
        &[
            "--check",
            "--book",
            BOOK,
            "--glossary",
            GLOSSARY,
            "--out",
            OUT,
        ],
    );
    let (verdict, err) = judge_generator(rc, captured(&out));
    if verdict != 0 {
        return (verdict, err);
    }
    let terms = fs::read_to_string(root.join(OUT))
        .map(|text| text.lines().filter(|l| l.starts_with("| ")).count())
        .unwrap_or(0);
    (
        0,
        format!(
            "BOOK-INDEX: ok ({OUT} matches the book, {} table rows)",
            terms as i64 - 2
        ),
    )
}

/// `cp -R src dst`: a directory tree copied, files and directories.
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

/// `find src -name '*.md' ! -name SUMMARY.md ! -name glossary.md ! -name index.md -exec sh -c ': > "$1"'`: every chapter's
/// text removed, the structure kept.
fn truncate_chapters(dir: &Path) {
    let Ok(entries) = fs::read_dir(dir) else {
        return;
    };
    for entry in entries.flatten() {
        let path = entry.path();
        if path.is_dir() {
            truncate_chapters(&path);
            continue;
        }
        let name = entry.file_name().to_string_lossy().into_owned();
        if name.ends_with(".md")
            && !matches!(name.as_str(), "SUMMARY.md" | "glossary.md" | "index.md")
        {
            let _ = fs::write(&path, "");
        }
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
            self.report(format!("BOOK-INDEX self-test MISS: {name} — expected rc={expected} and no output, got rc={rc}\n{out}"));
            return;
        }
        if rc == expected && out.contains(want) {
            self.pass += 1;
        } else {
            self.fail += 1;
            self.report(format!("BOOK-INDEX self-test MISS: {name} — expected rc={expected} (reason: {want}), got rc={rc}\n{out}"));
        }
    }
}

/// The RED/GREEN controls over a copy of the frozen book and glossary, the judge's four status readings, then the real
/// judgement over a frozen root.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "bookindex") else {
        eprintln!("BOOK-INDEX self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    let frozen = repo.join(FROZEN);
    copy_tree(&frozen.join("book"), &t.join("book"));
    let _ = fs::copy(frozen.join("GLOSSARY.md"), t.join("GLOSSARY.md"));
    let book = t.join("book").display().to_string();
    let glossary = t.join("GLOSSARY.md").display().to_string();
    let index = t.join("index.md").display().to_string();
    let check = |repo: &Path| {
        generator(
            repo,
            &[
                "--check",
                "--book",
                &book,
                "--glossary",
                &glossary,
                "--out",
                &index,
            ],
        )
    };
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
        misses: Vec::new(),
    };
    // GREEN: the generator emits an index from the frozen book.
    let (rc, out) = generator(
        repo,
        &["--book", &book, "--glossary", &glossary, "--out", &index],
    );
    tally.arm(
        "GREEN the generator emits an index from the frozen book",
        rc,
        0,
        captured(&out),
        "wrote",
    );
    // GREEN: the drift check passes on a faithful regeneration.
    let (rc, out) = check(repo);
    tally.arm(
        "GREEN a faithful regeneration is judged in sync",
        rc,
        0,
        captured(&out),
        "",
    );
    // RED: a hand-edit of the generated index is detected, named, and refused.
    let mut edited = fs::read_to_string(t.join("index.md")).unwrap_or_default();
    edited.push_str("\na hand edit\n");
    let _ = fs::write(t.join("index.md"), edited);
    let (rc, out) = check(repo);
    tally.arm(
        "RED a hand-edited index is refused, naming DRIFT",
        rc,
        1,
        captured(&out),
        "DRIFT",
    );
    // RED: a book edit the index must reflect (every chapter's text removed) regenerates to different bytes.
    truncate_chapters(&t.join("book/src"));
    let (rc, out) = check(repo);
    tally.arm(
        "RED a stale index behind edited chapters is refused, naming DRIFT",
        rc,
        1,
        captured(&out),
        "DRIFT",
    );
    // RED: a SUMMARY naming a missing chapter is refused BY NAME — new book structure is generator work.
    let _ = fs::remove_file(t.join("book/src/claim-scope.md"));
    let (rc, out) = check(repo);
    tally.arm(
        "RED a SUMMARY naming a missing chapter is refused by name",
        rc,
        2,
        captured(&out),
        "claim-scope.md",
    );
    // RED: a book without its SUMMARY is refused — an index over an undeclared population is a guess.
    let _ = fs::remove_file(t.join("book/src/SUMMARY.md"));
    let (rc, out) = check(repo);
    tally.arm(
        "RED a missing SUMMARY.md is refused, naming it",
        rc,
        2,
        captured(&out),
        "SUMMARY.md",
    );
    let (rc, err) = judge_generator(2, "gen_book_index: REFUSED — unreadable source");
    tally.arm(
        "RED typed generator refusal stays refusal2",
        rc,
        2,
        captured(&err),
        "BOOK-INDEX: REFUSED",
    );
    let (rc, err) = judge_generator(1, "generator launch failed");
    tally.arm(
        "RED untyped launch failure is not drift",
        rc,
        2,
        captured(&err),
        "BOOK-INDEX: REFUSED",
    );
    let (rc, err) = judge_generator(77, "unknown generator failure");
    tally.arm(
        "RED unknown generator status refuses",
        rc,
        2,
        captured(&err),
        "BOOK-INDEX: REFUSED",
    );
    let (rc, err) = judge_generator(1, "gen_book_index: DRIFT — changed index");
    tally.arm(
        "RED named drift stays defect1",
        rc,
        1,
        captured(&err),
        "BOOK-INDEX: FAIL",
    );
    // The real judgement over a frozen root: its committed index is the frozen pair of its text.
    let root = t.join("root");
    copy_tree(&frozen.join("book"), &root.join(BOOK));
    let _ = fs::copy(frozen.join("GLOSSARY.md"), root.join(GLOSSARY));
    let (rc, out) = judge_book(repo, &root);
    tally.arm(
        "GREEN the real judgement reads a faithful book, with its row count",
        rc,
        0,
        captured(&out),
        "matches the book, 5 table rows",
    );
    let _ = fs::remove_file(root.join(GLOSSARY));
    let (rc, out) = judge_book(repo, &root);
    tally.arm(
        "RED a deleted glossary is refused by name",
        rc,
        2,
        captured(&out),
        "the canonical glossary docs/GLOSSARY.md is missing",
    );
    let _ = fs::copy(frozen.join("GLOSSARY.md"), root.join(GLOSSARY));
    let _ = fs::remove_file(root.join(BOOK).join("src/SUMMARY.md"));
    let (rc, out) = judge_book(repo, &root);
    tally.arm(
        "RED a book whose SUMMARY is gone is refused by name, never `no project book yet`",
        rc,
        2,
        captured(&out),
        "no SUMMARY.md under docs/book/src",
    );
    let _ = fs::remove_dir_all(root.join(BOOK));
    let (rc, out) = judge_book(repo, &root);
    tally.arm(
        "GREEN a root with no book directory has no project book yet",
        rc,
        0,
        captured(&out),
        "no project book yet",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "BOOK-INDEX --self-test: {} pass / {} fail",
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

/// `cargo xtask check-book-index [--self-test]`: the shell driver's verdict lines and exit statuses.
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
        eprintln!("BOOK-INDEX: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    let (verdict, report) = judge_book(root, root);
    if verdict != 0 {
        eprint!("{report}");
        return ExitCode::from(u8::try_from(verdict).unwrap_or(2));
    }
    println!("{report}");
    ExitCode::SUCCESS
}
