//! The `UNIT-BOOKS` doctrine's driver, ported from `scripts/check_unit_books.sh` (`XTASK.6` slice `6z`), which is now a
//! shim of `cargo xtask check-unit-books`.
//!
//! Every registered unit (`materials/units.sexp`) owns a model book under `docs/models/` that builds with `mdbook`, is
//! listed in the project book's catalogue with its kind, includes only what exists, and whose rendered hyperlinks all
//! resolve; a book no unit registers is an orphan. `scripts/unit_books.py`, the pinned Python judge, decides it over a
//! fresh bundle and is spawned exactly as the driver spawned it, not ported; its two probes run as the script ran them,
//! scored beside the arms. The controls write the script's synthetic registry, project book and unit books. Each
//! self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::path::Path;
use std::process::{Command, ExitCode};

use crate::harness::{combined, on_path, scratch};

/// `python3 scripts/unit_books.py <root>` from the repository, stdout and stderr together as `2>&1` joined them.
fn check_books(repo: &Path, root: &Path) -> (i32, String) {
    combined(
        Command::new("python3")
            .arg("scripts/unit_books.py")
            .arg(root)
            .current_dir(repo),
    )
}

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

fn write(path: &Path, text: &str) {
    if let Some(parent) = path.parent() {
        let _ = fs::create_dir_all(parent);
    }
    let _ = fs::write(path, text);
}

struct Tally<'a> {
    repo: &'a Path,
    root: &'a Path,
    pass: u32,
    fail: u32,
    verbose: bool,
    /// Every missed arm's report, kept so a quiet run's refusal can name what missed (`XTASK.12`).
    misses: Vec<String>,
}

impl Tally<'_> {
    /// One arm: judging the fixture tree must give `expected` and contain `want`.
    fn arm(&mut self, name: &str, expected: i32, want: &str) {
        let (rc, out) = check_books(self.repo, self.root);
        let out = captured(&out);
        if rc != expected {
            self.miss(format!(
                "UNIT-BOOKS self-test MISS: {name} expected rc={expected} got rc={rc}\n{out}"
            ));
        } else if !out.contains(want) {
            self.miss(format!(
                "UNIT-BOOKS self-test MISS: {name} right verdict, wrong reason (no {want})\n{out}"
            ));
        } else {
            self.pass += 1;
        }
    }

    /// One of the script's four probe runs, scored as it scored them: a pass is a pass, a failure prints the probe's
    /// output under the script's heading.
    fn probe(&mut self, heading: &str, optimized: bool, script: &str) {
        let mut command = Command::new("python3");
        if optimized {
            command.arg("-O");
        }
        let (rc, out) = combined(command.arg(script).current_dir(self.repo));
        if rc == 0 {
            self.pass += 1;
        } else {
            self.miss(format!("{heading}\n{}", captured(&out)));
        }
    }

    /// A missed arm: counted, printed at once in a verbose run, kept for a quiet run's refusal.
    fn miss(&mut self, report: String) {
        self.fail += 1;
        if self.verbose {
            eprintln!("{report}");
        }
        self.misses.push(report);
    }
}

/// The RED/GREEN controls over the script's synthetic registry, project book and unit books, then its four probe runs.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "unitbooks") else {
        eprintln!("UNIT-BOOKS self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    let registry = |text: &str| write(&t.join("materials/units.sexp"), &format!("{text}\n"));
    let book = |name: &str| {
        let dir = t.join("docs/models").join(name);
        write(
            &dir.join("book.toml"),
            &format!("[book]\ntitle = \"{name}\"\nsrc = \"src\"\n"),
        );
        write(
            &dir.join("src/SUMMARY.md"),
            "# Summary\n\n[Intro](intro.md)\n",
        );
        write(&dir.join("src/intro.md"), "# Intro\n");
    };
    let models = |text: &str| write(&t.join("docs/book/src/models.md"), text);
    let intro = |text: &str| write(&t.join("docs/models/u1/src/intro.md"), text);
    let mut tally = Tally {
        repo,
        root: &t,
        pass: 0,
        fail: 0,
        verbose,
        misses: Vec::new(),
    };
    tally.arm("REFUSE no registry at all", 2, "REFUSED");
    registry("(unit (id \"u1\") (kind processor) (layer processor) (book \"docs/models/u1\"))");
    tally.arm("RED   a unit whose book does not exist", 1, "NO BOOK u1");
    write(
        &t.join("docs/book/book.toml"),
        "[book]\ntitle = \"project\"\nsrc = \"src\"\n",
    );
    write(
        &t.join("docs/book/src/SUMMARY.md"),
        "# Summary\n\n[Models](models.md)\n",
    );
    models("# Models\n\n- **`u1`** (kind: processor)\n");
    book("u1");
    tally.arm(
        "GREEN a registered unit with a building book",
        0,
        "__CHECKED__ 1",
    );
    book("stray");
    tally.arm("RED   a book no unit registers", 1, "ORPHAN BOOK");
    let _ = fs::remove_dir_all(t.join("docs/models/stray"));
    let _ = fs::remove_file(t.join("docs/models/u1/src/SUMMARY.md"));
    tally.arm("RED   a book without its SUMMARY", 1, "INCOMPLETE BOOK u1");
    write(
        &t.join("docs/models/u1/src/SUMMARY.md"),
        "# Summary\n\n[Intro](intro.md)\n",
    );
    write(&t.join("docs/models/u1/book.toml"), "not toml at all [[[\n");
    tally.arm(
        "RED   a book that does not build (a malformed book.toml)",
        1,
        "BOOK DOES NOT BUILD u1",
    );
    write(
        &t.join("docs/models/u1/book.toml"),
        "[book]\ntitle = \"u1\"\nsrc = \"src\"\n",
    );
    models("# Models\n");
    tally.arm(
        "RED   missing registered catalogue entry",
        1,
        "MODEL-CATALOGUE missing u1",
    );
    models("# Models\n\n- **`u1`** (kind: board)\n");
    tally.arm("RED   wrong catalogue kind", 1, "MODEL-CATALOGUE kind u1");
    models("# Models\n\n- **`u1`** (kind: processor)\n");
    let fragment = "// ANCHOR: selected\ncontract\n// ANCHOR_END: selected\n";
    write(&t.join("docs/book/src/fragment.txt"), fragment);
    write(&t.join("docs/models/u1/src/fragment.txt"), fragment);
    models("# Models\n\n- **`u1`** (kind: processor)\n\n{{#include absent.txt}}\n");
    tally.arm("RED   project include file missing", 1, "DEFECT");
    models("# Models\n\n- **`u1`** (kind: processor)\n\n{{#include fragment.txt:absent}}\n");
    tally.arm("RED   project include anchor missing", 1, "DEFECT");
    // `cat fragment >> duplicate` twice, then `mv`: the fragment doubled.
    write(
        &t.join("docs/book/src/fragment.txt"),
        &format!("{fragment}{fragment}"),
    );
    models("# Models\n\n- **`u1`** (kind: processor)\n\n{{#include fragment.txt:selected}}\n");
    tally.arm("RED   project include anchor duplicate", 1, "DEFECT");
    models("# Models\n\n- **`u1`** (kind: processor)\n");
    intro("# Intro\n\n{{#include absent.txt}}\n");
    tally.arm("RED   unit include file missing", 1, "DEFECT");
    intro("# Intro\n\n{{#include fragment.txt:absent}}\n");
    tally.arm("RED   unit include anchor missing", 1, "DEFECT");
    let _ = fs::copy(
        t.join("docs/book/src/fragment.txt"),
        t.join("docs/models/u1/src/fragment.txt"),
    );
    intro("# Intro\n\n{{#include fragment.txt:selected}}\n");
    tally.arm("RED   unit include anchor duplicate", 1, "DEFECT");
    intro("# Intro\n\n[Missing](missing.md)\n");
    tally.arm(
        "RED   rendered local path is absent",
        1,
        "BOOK-LINK missing-path",
    );
    intro("# Intro\n\n[Missing](intro.md#absent)\n");
    tally.arm(
        "RED   rendered HTML anchor is absent",
        1,
        "BOOK-LINK missing-anchor",
    );
    intro("# Intro\n");
    registry(&format!(
        "(unit (id \"u1\") (kind processor) (layer processor) (book \"{}/docs/models/u1\"))",
        t.display()
    ));
    tally.arm(
        "REFUSE absolute registry book path before build",
        2,
        "UNSAFE BOOK PATH",
    );
    registry("");
    tally.arm("REFUSE an empty registry", 2, "registry is empty");
    tally.probe(
        "UNIT-BOOKS probe failed",
        false,
        "scripts/probe_unit_books.py",
    );
    tally.probe(
        "UNIT-BOOKS optimized probe failed",
        true,
        "scripts/probe_unit_books.py",
    );
    tally.probe(
        "UNIT-BOOKS navigation probe failed",
        false,
        "scripts/probe_book_navigation.py",
    );
    tally.probe(
        "UNIT-BOOKS optimized navigation probe failed",
        true,
        "scripts/probe_book_navigation.py",
    );
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "UNIT-BOOKS --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    } else {
        // A quiet run that misses names every missed arm before the caller's refusal line (`XTASK.12`): a hosted
        // refusal that said only "self-test failed" could not be diagnosed from its log (run 40746652030).
        for report in &tally.misses {
            eprintln!("{report}");
        }
    }
    tally.fail == 0
}

/// `cargo xtask check-unit-books [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if !on_path("mdbook") {
        eprintln!("UNIT-BOOKS: REFUSED — mdbook is not on PATH; this check cannot judge.");
        eprintln!("  Install it with: cargo install mdbook");
        return ExitCode::from(2);
    }
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    if !self_test(root, false) {
        eprintln!("UNIT-BOOKS: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    // `out="$(check_books "$ROOT")"`: stdout alone, the judge's stderr passing through as the shell's did.
    let output = Command::new("python3")
        .arg("scripts/unit_books.py")
        .arg(root)
        .current_dir(root)
        .stdin(std::process::Stdio::null())
        .stderr(std::process::Stdio::inherit())
        .output();
    let (rc, out) = match output {
        Ok(o) => (
            o.status.code().unwrap_or(-1),
            String::from_utf8_lossy(&o.stdout).into_owned(),
        ),
        Err(e) => (-1, e.to_string()),
    };
    let out = captured(&out);
    let count = out
        .lines()
        .find_map(|l| l.strip_prefix("__CHECKED__ "))
        .unwrap_or("0");
    let links = out
        .lines()
        .find_map(|l| l.strip_prefix("__LINKS__ "))
        .unwrap_or("0");
    let body: Vec<&str> = out
        .lines()
        .filter(|l| !l.starts_with("__CHECKED__ ") && !l.starts_with("__LINKS__ "))
        .collect();
    match rc {
        2 => {
            eprintln!("UNIT-BOOKS: REFUSED — the unit corpus could not be read.");
            for line in &body {
                eprintln!("  {line}");
            }
            ExitCode::from(2)
        }
        0 => {
            println!("UNIT-BOOKS: ok ({count} units + project book; catalogue and {links} rendered hyperlinks checked in fresh bundle)");
            ExitCode::SUCCESS
        }
        _ => {
            eprintln!("UNIT-BOOKS: catalogue, source, build or rendered-navigation defect.");
            for line in &body {
                eprintln!("  {line}");
            }
            eprintln!(
                "  Inspect the named source and fresh bundle verdict; stale output cannot qualify."
            );
            ExitCode::from(1)
        }
    }
}
