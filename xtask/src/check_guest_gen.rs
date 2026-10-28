//! The `GUEST-GEN` doctrine's driver, ported from `scripts/check_guest_gen.sh` (`XTASK.6` slice `6aq`), which is now a
//! shim of `cargo xtask check-guest-gen`.
//!
//! `crates/semulith-verify/src/guests.rs` and `guests_rv64gc.rs` are GENERATED from the tracked assembly guests and their
//! specification-derived expectations by `scripts/gen_guests.py`; the check regenerates each in memory (`--check`) and
//! refuses the day it stops byte-matching the committed file, then judges the rv64gc base mirror through the tracked
//! governor (`scripts/check_gc_mirror.py`). The generator, the governor, the twenty-odd probe suites the controls run
//! (plain and `-O`, each under its mutations) and the controls' three inline Python edits are spawned as the script
//! spawned them; nothing of them is ported. The quiet run keeps the controls' output in `target/guest-gen/self-test.log`
//! as the script did, and shows its tail on a refusal. Each self-test arm is one `tally.arm(` call — the two mode loops
//! keep their one GREEN and one RED call each, as the script's did — the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{on_path, scratch};

const ENCODING: &str = "profiles/rv64i-lab-v0/encoding.sexp";
const GUESTS_DIR: &str = "profiles/rv64i-lab-v0/guests";
const OUT: &str = "crates/semulith-verify/src/guests.rs";
// P4-SYSTEM.2 slice h (the route flip): the census's rv64gc owner→mirror pair.
const ENCODING_GC: &str = "profiles/rv64gc-lab-v0/encoding.sexp";
const GUESTS_DIR_GC: &str = "profiles/rv64gc-lab-v0/guests";
const OUT_GC: &str = "crates/semulith-verify/src/guests_rv64gc.rs";
const SELF_TEST_LOG: &str = "target/guest-gen/self-test.log";

/// The expectations document with its last step dropped, verbatim: `python3 - <expected.sexp>`.
const DROP_STEP: &str = r####"import sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
i = text.find('(step (n 11)')
assert i > 0
# Step 11 is the last child of the outer (expectations …) form: drop it, then re-close
# the outer form with the file's final paren.
k = text.rfind(')')
open(path, "w", encoding="utf-8").write(text[:i] + text[k:])
"####;
/// The run order with the ghost guest dropped again, verbatim: `python3 - <run-order.txt>`.
const DROP_GHOST: &str = r####"import sys
path = sys.argv[1]
lines = open(path).read().splitlines()
assert lines[-1] == "ghost-guest"
open(path, "w").write("\n".join(lines[:-1]) + "\n")
"####;
/// A comment-only exception re-derived onto the mirror, verbatim: `python3 - <encoding> <owner> <mirror>`.
const STALE_RECORD: &str = r####"import sys
from pathlib import Path
sys.path.insert(0, 'scripts')
import dossier_sexp as D
from expectations_text import with_fetches
from riscv_asm import Assembler
encoding, owner, mirror = map(Path, sys.argv[1:])
text = owner.read_bytes().decode('utf-8')
if 'c.nop' in Assembler(encoding).insns:
    prior = D.load_expectations(mirror)
    text = with_fetches(text, prior.get('fetches', prior['instructions']))
mirror.write_bytes(text.encode('utf-8'))
"####;

/// The snapshot-author mutations and their failure counts (`SNAPSHOT_AUTHOR_CASES`).
const SNAPSHOT_AUTHOR_CASES: &[(&str, &str)] = &[
    ("budget", "6"),
    ("source-preflight", "15"),
    ("canonical-context", "1"),
    ("budget-forward", "12"),
    ("stock-notes", "1"),
    ("source-controls", "2"),
    ("complete-result", "2"),
    ("raw-bits", "2"),
    ("source-fingerprint", "2"),
    ("payload-fingerprint", "3"),
    ("writes-copy", "8"),
    ("result-frozen", "1"),
    ("step-frozen", "1"),
    ("program-label", "3"),
    ("source-reopen", "33"),
];
/// The source-derivation mutations and their failure counts (`SOURCE_EXPECTATION_CASES`).
const SOURCE_EXPECTATION_CASES: &[(&str, &str)] = &[
    ("source-preflight", "2"),
    ("expectation-bounds", "4"),
    ("witness-copy", "1"),
    ("program", "1"),
    ("fixed-entry", "1"),
    ("exclusions", "3"),
    ("declared-events", "3"),
    ("source-forward", "21"),
    ("budget-forward", "12"),
    ("source-reopen", "29"),
    ("context-program", "1"),
    ("unfetched", "2"),
    ("whole-budget", "2"),
    ("value-comparison", "6"),
    ("witness-change", "1"),
    ("zero-value", "1"),
    ("baseline-fingerprint", "1"),
    ("facts-frozen", "1"),
    ("check-frozen", "1"),
];

/// Where the controls' own chatter goes: the terminal when the self-test is the command, the script's log file when the
/// real run re-runs the controls (`self_test >"$SELF_TEST_LOG" 2>&1`).
enum Report {
    Terminal,
    Log(fs::File),
}

impl Report {
    /// A line of the self-test's stderr.
    fn line(&mut self, text: &str) {
        match self {
            Report::Terminal => eprintln!("{text}"),
            Report::Log(file) => {
                let _ = writeln!(file, "{text}");
            }
        }
    }

    /// A line of the self-test's stdout.
    fn out(&mut self, text: &str) {
        match self {
            Report::Terminal => println!("{text}"),
            Report::Log(file) => {
                let _ = writeln!(file, "{text}");
            }
        }
    }

    /// A child's inherited stream.
    fn stdio(&self) -> Stdio {
        match self {
            Report::Terminal => Stdio::inherit(),
            Report::Log(file) => file.try_clone().map_or_else(|_| Stdio::null(), Stdio::from),
        }
    }
}

/// The shell's `$(…)`: every trailing newline removed.
fn captured(text: &str) -> &str {
    text.trim_end_matches('\n')
}

/// A command with stdout and stderr merged and captured (`2>&1`), beside its exit status.
fn merged(command: &mut Command) -> (i32, String) {
    match command.stdin(Stdio::null()).output() {
        Ok(o) => {
            let mut text = String::from_utf8_lossy(&o.stdout).into_owned();
            text.push_str(&String::from_utf8_lossy(&o.stderr));
            (o.status.code().unwrap_or(-1), text)
        }
        Err(e) => (-1, e.to_string()),
    }
}

/// `python3 [-O] scripts/<probe> <args…> 2>&1` from the repository root, captured.
fn probe(repo: &Path, optimized: bool, script: &str, args: &[&str]) -> (i32, String) {
    let mut command = Command::new("python3");
    if optimized {
        command.arg("-O");
    }
    command.arg(script).args(args).current_dir(repo);
    merged(&mut command)
}

/// `judge_mirror <owner> <mirror>`: the tracked governor over the base mirror; `capture_stderr` is the arms' `2>&1`.
fn judge_mirror(repo: &Path, owner: &Path, mirror: &Path, capture_stderr: bool) -> (i32, String) {
    let mut command = Command::new("python3");
    command
        .arg("scripts/check_gc_mirror.py")
        .arg("--owner")
        .arg(owner)
        .arg("--mirror")
        .arg(mirror)
        .arg("--encoding")
        .arg(ENCODING_GC)
        .current_dir(repo)
        .stdin(Stdio::null());
    if capture_stderr {
        return merged(&mut command);
    }
    match command.stderr(Stdio::inherit()).output() {
        Ok(o) => (
            o.status.code().unwrap_or(-1),
            String::from_utf8_lossy(&o.stdout).into_owned(),
        ),
        Err(e) => (-1, e.to_string()),
    }
}

/// `python3 - <args…> <<'…'`: a program on stdin from the repository root, its own output to the report's streams.
fn python_program(repo: &Path, program: &str, args: &[&Path], report: &Report) {
    let mut command = Command::new("python3");
    command
        .arg("-")
        .args(args)
        .current_dir(repo)
        .stdin(Stdio::piped())
        .stdout(report.stdio())
        .stderr(report.stdio());
    let Ok(mut child) = command.spawn() else {
        return;
    };
    if let Some(mut stdin) = child.stdin.take() {
        let _ = stdin.write_all(program.as_bytes());
    }
    let _ = child.wait();
}

/// `sed 's/PAT/REPL/' src > dst`: the first occurrence on every line, the patterns being literal text.
fn sed_first(src: &Path, dst: &Path, pattern: &str, replacement: &str) {
    let text = fs::read_to_string(src).unwrap_or_default();
    let mut out = String::with_capacity(text.len());
    for line in text.split_inclusive('\n') {
        out.push_str(&line.replacen(pattern, replacement, 1));
    }
    let _ = fs::write(dst, out);
}

/// `printf '…' >> path`: the text appended.
fn append(path: &Path, text: &str) {
    if let Ok(mut file) = fs::OpenOptions::new().append(true).create(true).open(path) {
        let _ = file.write_all(text.as_bytes());
    }
}

/// `cp <dir>/* <dst>/ 2>/dev/null || cp -R <dir>/. <dst>/`: the directory's entries copied, trees recursively.
fn copy_entries(src: &Path, dst: &Path) {
    let _ = fs::create_dir_all(dst);
    let Ok(entries) = fs::read_dir(src) else {
        return;
    };
    for entry in entries.flatten() {
        let from = entry.path();
        let to = dst.join(entry.file_name());
        if from.is_dir() {
            copy_entries(&from, &to);
        } else {
            let _ = fs::copy(&from, &to);
        }
    }
}

struct Tally<'a> {
    pass: u32,
    fail: u32,
    report: &'a mut Report,
}

impl Tally<'_> {
    /// One arm: the exit status must be `expected` and the output must contain `want` — or, for an empty `want`, be
    /// empty.
    fn arm(&mut self, name: &str, (rc, raw): (i32, String), expected: i32, want: &str) {
        let out = captured(&raw);
        if want.is_empty() {
            if rc == expected && out.is_empty() {
                self.pass += 1;
                return;
            }
            self.fail += 1;
            self.report.line(&format!("GUEST-GEN self-test MISS: {name} — expected rc={expected} and no output, got rc={rc}\n{out}"));
            return;
        }
        if rc == expected && out.contains(want) {
            self.pass += 1;
        } else {
            self.fail += 1;
            self.report.line(&format!("GUEST-GEN self-test MISS: {name} — expected rc={expected} (reason: {want}), got rc={rc}\n{out}"));
        }
    }
}

/// The RED/GREEN controls: a surgical copy of the tracked guests, the census pair, the base-mirror governor and the probe
/// suites. The report carries the controls' chatter to the terminal or to the script's log.
fn self_test(repo: &Path, report: &mut Report) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "guestgen") else {
        report.line(
            "GUEST-GEN self-test: cannot create a scratch directory under target/doctrine-selftest",
        );
        return false;
    };
    // The surgical guests directory mirrors the real layout: <name>.s + <name>.expected.sexp + the run-order record
    // (P4-SYSTEM.2 slice d: the guest SET is directory-derived; the order is recorded data).
    let guests = t.join("guests");
    let _ = fs::create_dir_all(&guests);
    let real_guests = repo.join(GUESTS_DIR);
    if let Ok(entries) = fs::read_dir(&real_guests) {
        for entry in entries.flatten() {
            let name = entry.file_name();
            let n = name.to_string_lossy();
            if n.ends_with(".s") || n.ends_with(".expected.sexp") || n == "run-order.txt" {
                let _ = fs::copy(entry.path(), guests.join(&name));
            }
        }
    }
    let fixture: PathBuf = t.join("guests.rs");
    // `GEN`: the real encoding, the surgical guests directory, the scratch fixture, then the caller's flags.
    let gen = |check: bool| {
        let mut command = Command::new("python3");
        command
            .arg("scripts/gen_guests.py")
            .arg("--encoding")
            .arg(ENCODING)
            .arg("--guests-dir")
            .arg(&guests)
            .arg("--out")
            .arg(&fixture)
            .current_dir(repo);
        if check {
            command.arg("--check");
        }
        merged(&mut command)
    };
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        report: &mut *report,
    };
    // GREEN: the generator emits a fixture from the tracked guests.
    tally.arm(
        "GREEN the generator emits a fixture from the tracked guests",
        gen(false),
        0,
        "wrote",
    );
    // GREEN: the drift check passes on a faithful regeneration.
    tally.arm(
        "GREEN a faithful regeneration is judged in sync",
        gen(true),
        0,
        "matches",
    );
    // RED: a hand-edit of the generated fixture is detected, named, and refused.
    append(&fixture, "\n// hand edit\n");
    tally.arm(
        "RED a hand-edited fixture is refused, naming DRIFT",
        gen(true),
        1,
        "DRIFT",
    );
    let _ = gen(false); // restore a faithful fixture for the remaining arms
                        // RED: a guest that does not assemble is refused by name.
    append(&guests.join("smoke-arith.s"), "zzz9 x1, x2\n");
    tally.arm(
        "RED an unassemblable guest is refused, naming the mnemonic",
        gen(true),
        2,
        "zzz9",
    );
    let _ = fs::copy(
        real_guests.join("smoke-arith.s"),
        guests.join("smoke-arith.s"),
    );
    // RED: an expectations document whose step exceeds the declared count is refused.
    sed_first(
        &real_guests.join("smoke-arith.expected.sexp"),
        &guests.join("smoke-arith.expected.sexp"),
        "(instructions 12)",
        "(instructions 11)",
    );
    tally.arm(
        "RED an expectation step past the declared count is refused",
        gen(true),
        2,
        "exceeds",
    );
    let _ = fs::copy(
        real_guests.join("smoke-arith.expected.sexp"),
        guests.join("smoke-arith.expected.sexp"),
    );
    // RED: an expectations document missing steps is refused (a gap would read as 'writes nothing', which is a lie the
    // generator must not emit).
    python_program(
        repo,
        DROP_STEP,
        &[&guests.join("smoke-arith.expected.sexp")],
        tally.report,
    );
    tally.arm(
        "RED expectations missing a step are refused",
        gen(true),
        2,
        "carry no expectation",
    );
    let _ = fs::copy(
        real_guests.join("smoke-arith.expected.sexp"),
        guests.join("smoke-arith.expected.sexp"),
    );
    // RED: a register outside the x0..x31 vocabulary is refused by name.
    sed_first(
        &real_guests.join("guest-control.expected.sexp"),
        &guests.join("guest-control.expected.sexp"),
        "(reg \"x1\")",
        "(reg \"x99\")",
    );
    tally.arm(
        "RED a register outside x0..x31 is refused",
        gen(true),
        2,
        "x99",
    );
    let _ = fs::copy(
        real_guests.join("guest-control.expected.sexp"),
        guests.join("guest-control.expected.sexp"),
    );
    // RED: a fetch-count declaration outside the parcel bounds is refused (P4-SYSTEM.3 slice e).
    sed_first(
        &real_guests.join("smoke-arith.expected.sexp"),
        &guests.join("smoke-arith.expected.sexp"),
        "(instructions 12)",
        "(instructions 12) (fetches 25)",
    );
    tally.arm(
        "RED a fetches count outside the parcel bounds is refused",
        gen(true),
        2,
        "fetches",
    );
    let _ = fs::copy(
        real_guests.join("smoke-arith.expected.sexp"),
        guests.join("smoke-arith.expected.sexp"),
    );
    // ---- directory derivation (P4-SYSTEM.2 slice d) ---------------------------------------------
    // RED: the run-order record missing is refused — the order is data, never the directory's accident.
    let _ = fs::rename(
        guests.join("run-order.txt"),
        guests.join("run-order.txt.bak"),
    );
    tally.arm(
        "RED a missing run-order record is refused",
        gen(true),
        2,
        "run-order.txt",
    );
    let _ = fs::rename(
        guests.join("run-order.txt.bak"),
        guests.join("run-order.txt"),
    );
    // RED: a guest the run order names that is not on disk is refused, named.
    append(&guests.join("run-order.txt"), "ghost-guest\n");
    tally.arm(
        "RED a listed guest not on disk is refused, named",
        gen(true),
        2,
        "ghost-guest",
    );
    python_program(
        repo,
        DROP_GHOST,
        &[&guests.join("run-order.txt")],
        tally.report,
    );
    // RED: a guest on disk but missing from the run order never executes — refused, named.
    let _ = fs::copy(real_guests.join("smoke-trap.s"), guests.join("zz-probe.s"));
    let _ = fs::copy(
        real_guests.join("smoke-trap.expected.sexp"),
        guests.join("zz-probe.expected.sexp"),
    );
    tally.arm(
        "RED an unlisted guest on disk is refused, named",
        gen(true),
        2,
        "zz-probe",
    );
    let _ = fs::remove_file(guests.join("zz-probe.s"));
    let _ = fs::remove_file(guests.join("zz-probe.expected.sexp"));
    // The slice-(h) census arms: the gate's judging loop covers the rv64gc owner→mirror pair — pinned against the REAL
    // pair, not a synthetic one.
    tally.arm(
        "GREEN the census's rv64gc pair is in sync",
        probe(
            repo,
            false,
            "scripts/gen_guests.py",
            &[
                "--check",
                "--encoding",
                ENCODING_GC,
                "--guests-dir",
                GUESTS_DIR_GC,
                "--image-format",
                "bytes",
                "--out",
                OUT_GC,
            ],
        ),
        0,
        "matches",
    );
    let gc_fixture = t.join("gc-fixture.rs");
    let _ = fs::copy(repo.join(OUT_GC), &gc_fixture);
    append(&gc_fixture, "\n// hand edit\n");
    let gc_fixture_s = gc_fixture.display().to_string();
    tally.arm(
        "RED the census's rv64gc pair catches a hand edit",
        probe(
            repo,
            false,
            "scripts/gen_guests.py",
            &[
                "--check",
                "--encoding",
                ENCODING_GC,
                "--guests-dir",
                GUESTS_DIR_GC,
                "--image-format",
                "bytes",
                "--out",
                &gc_fixture_s,
            ],
        ),
        1,
        "DRIFT",
    );
    // The base-mirror governor arms: the mirror holds on the real tree, and the governor discriminates — a drifted pair
    // is named, a stale re-derivation record is named.
    tally.arm(
        "GREEN the base mirror holds on the real tree",
        judge_mirror(repo, Path::new(GUESTS_DIR), Path::new(GUESTS_DIR_GC), true),
        0,
        "byte-identical",
    );
    let mirror = t.join("mirror");
    copy_entries(&repo.join(GUESTS_DIR_GC), &mirror);
    append(
        &mirror.join("bound-arith.expected.sexp"),
        "\n;; silent edit\n",
    );
    tally.arm(
        "RED a drifted mirror file is named",
        judge_mirror(repo, Path::new(GUESTS_DIR), &mirror, true),
        1,
        "bound-arith",
    );
    let _ = fs::remove_file(mirror.join("bound-arith.expected.sexp"));
    let _ = fs::copy(
        repo.join(GUESTS_DIR_GC).join("bound-arith.expected.sexp"),
        mirror.join("bound-arith.expected.sexp"),
    );
    // A comment-only exception keeps valid observations. In C mode its count must remain independently derived, so this
    // arm reaches the stale-record predicate.
    python_program(
        repo,
        STALE_RECORD,
        &[
            Path::new(ENCODING_GC),
            &real_guests.join("dir-selfmod-fence.expected.sexp"),
            &mirror.join("dir-selfmod-fence.expected.sexp"),
        ],
        tally.report,
    );
    tally.arm(
        "RED a stale re-derivation record is named",
        judge_mirror(repo, Path::new(GUESTS_DIR), &mirror, true),
        1,
        "recorded re-derivation is stale after count normalization",
    );
    tally.arm(
        "GREEN mirror migration checks extents and literal fields",
        probe(repo, false, "scripts/check_gc_mirror.py", &["--self-test"]),
        0,
        "literal fields pass",
    );
    tally.arm(
        "RED mirror migration cannot ignore request counts",
        probe(
            repo,
            false,
            "scripts/check_gc_mirror.py",
            &["--self-test", "--mutation", "ignore-counts"],
        ),
        1,
        "accepted declared parcel count",
    );
    tally.arm(
        "RED mirror migration cannot exempt other bytes",
        probe(
            repo,
            false,
            "scripts/check_gc_mirror.py",
            &["--self-test", "--mutation", "ignore-noncount"],
        ),
        1,
        "accepted non-count mirror drift",
    );
    tally.arm(
        "RED mirror migration keeps source bytes exact",
        probe(
            repo,
            false,
            "scripts/check_gc_mirror.py",
            &["--self-test", "--mutation", "ignore-source"],
        ),
        1,
        "accepted source mirror is not byte-identical",
    );
    tally.arm(
        "RED parcel counts cannot preserve a stale exception",
        probe(
            repo,
            false,
            "scripts/check_gc_mirror.py",
            &["--self-test", "--mutation", "ignore-stale"],
        ),
        1,
        "accepted re-derivation is stale",
    );
    tally.arm(
        "RED source annotations require exact reviewed pins",
        probe(
            repo,
            false,
            "scripts/check_gc_mirror.py",
            &["--self-test", "--mutation", "ignore-source-pins"],
        ),
        1,
        "accepted source re-derivation pins differ",
    );
    tally.arm(
        "RED reviewed source annotations cannot change instructions",
        probe(
            repo,
            false,
            "scripts/check_gc_mirror.py",
            &["--self-test", "--mutation", "ignore-source-image"],
        ),
        1,
        "accepted source re-derivation changes assembled image",
    );
    // P4.14 a42d3a: explicit entry context through the sole expectation owner.
    tally.arm(
        "GREEN normal entry context controls",
        probe(repo, false, "scripts/probe_matched_gpr_entry.py", &[]),
        0,
        "MATCHED-GPR-ENTRY: 25 tests / 0 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted required-program",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "required-program"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 1 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted program-type",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "program-type"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 6 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted budget-cap",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "budget-cap"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 1 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted byte-bounds",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "byte-bounds"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 2 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted payload-type",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "payload-type"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 4 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted payload-forward",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "payload-forward"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 34 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted budget-forward",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "budget-forward"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 3 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted raw-schema",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "raw-schema"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 3 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted root-count",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "root-count"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 1 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted step-sequence",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "step-sequence"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 1 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted program-identity",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "program-identity"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 4 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted explicit-entry",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "explicit-entry"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 1 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted rv64-range",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "rv64-range"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 2 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted entry-forward",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "entry-forward"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 16 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted immutable",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "immutable"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 1 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED normal entry context omitted metadata-budget",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "metadata-budget"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 3 failures / 0 errors; metadata only",
    );
    tally.arm(
        "GREEN optimized entry context controls",
        probe(repo, true, "scripts/probe_matched_gpr_entry.py", &[]),
        0,
        "MATCHED-GPR-ENTRY: 25 tests / 0 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted required-program",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "required-program"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 1 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted program-type",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "program-type"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 6 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted budget-cap",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "budget-cap"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 1 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted byte-bounds",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "byte-bounds"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 2 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted payload-type",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "payload-type"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 4 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted payload-forward",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "payload-forward"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 34 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted budget-forward",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "budget-forward"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 3 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted raw-schema",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "raw-schema"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 3 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted root-count",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "root-count"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 1 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted step-sequence",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "step-sequence"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 1 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted program-identity",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "program-identity"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 4 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted explicit-entry",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "explicit-entry"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 1 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted rv64-range",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "rv64-range"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 2 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted entry-forward",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "entry-forward"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 16 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted immutable",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "immutable"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 1 failures / 0 errors; metadata only",
    );
    tally.arm(
        "RED optimized entry context omitted metadata-budget",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_entry.py",
            &["--mutation", "metadata-budget"],
        ),
        1,
        "MATCHED-GPR-ENTRY: 25 tests / 3 failures / 0 errors; metadata only",
    );
    // End P4.14 a42d3a.
    // P4.14 a42d1: complete source/image bytes, metadata-only findings and refusals.
    tally.arm(
        "GREEN complete source-image normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &[],
        ),
        0,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 0 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image image-guard normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "image-guard"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 8 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image image-bound normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "image-bound"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 1 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image empty-image normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "empty-image"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 1 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image complete-equality normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "complete-equality"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 14 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image payload-only normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "payload-only"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 9 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image source-forward normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "source-forward"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 18 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image program-forward normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "program-forward"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 8 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image entry-forward normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "entry-forward"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 17 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image unavailable-class normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "unavailable-class"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 1 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image refusal-class normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "refusal-class"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 20 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image source-fingerprint normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "source-fingerprint"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 2 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image image-fingerprint normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "image-fingerprint"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 1 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image source-retention normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "source-retention"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 3 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image frozen-result normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "frozen-result"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 1 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image frozen-facts normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "frozen-facts"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 1 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image diagnostic-echo normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "diagnostic-echo"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 20 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image broad-unavailable normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "broad-unavailable"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 1 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "GREEN complete source-image optimized",
        probe(repo, true, "scripts/probe_matched_gpr_source_image.py", &[]),
        0,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 0 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image image-guard optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "image-guard"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 8 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image image-bound optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "image-bound"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 1 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image empty-image optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "empty-image"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 1 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image complete-equality optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "complete-equality"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 14 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image payload-only optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "payload-only"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 9 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image source-forward optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "source-forward"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 18 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image program-forward optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "program-forward"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 8 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image entry-forward optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "entry-forward"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 17 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image unavailable-class optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "unavailable-class"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 1 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image refusal-class optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "refusal-class"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 20 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image source-fingerprint optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "source-fingerprint"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 2 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image image-fingerprint optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "image-fingerprint"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 1 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image source-retention optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "source-retention"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 3 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image frozen-result optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "frozen-result"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 1 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image frozen-facts optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "frozen-facts"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 1 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image diagnostic-echo optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "diagnostic-echo"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 20 failures / 0 errors; byte correspondence only",
    );
    tally.arm(
        "RED source-image broad-unavailable optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_source_image.py",
            &["--mutation", "broad-unavailable"],
        ),
        1,
        "MATCHED-GPR-SOURCE-IMAGE: 24 tests / 1 failures / 0 errors; byte correspondence only",
    );
    // P4.14 a42c: bounded source-byte construction and legacy writer access order.
    tally.arm(
        "GREEN source image normal",
        probe(repo, false, "scripts/probe_matched_gpr_image.py", &[]),
        0,
        "MATCHED-GPR-IMAGE: 33 tests / 0 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED source-type normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "source-type"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 7 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED source-bound normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "source-bound"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED program-guard normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "program-guard"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 6 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED entry-guard normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "entry-guard"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 6 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED utf8 normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "utf8"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED line-preflight normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "line-preflight"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 8 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED final-line normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "final-line"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED canonical-route normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "canonical-route"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 3 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED ialign-context normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "ialign-context"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 4 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED payload-bound normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "payload-bound"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED image-bound normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "image-bound"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED payload-type normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "payload-type"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED image-type normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "image-type"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED source-fingerprint normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "source-fingerprint"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 2 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED entry-forward normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "entry-forward"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 6 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED writer-delegation normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "writer-delegation"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED writer-order normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "writer-order"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "GREEN source image optimized",
        probe(repo, true, "scripts/probe_matched_gpr_image.py", &[]),
        0,
        "MATCHED-GPR-IMAGE: 33 tests / 0 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED source-type optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "source-type"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 7 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED source-bound optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "source-bound"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED program-guard optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "program-guard"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 6 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED entry-guard optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "entry-guard"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 6 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED utf8 optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "utf8"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED line-preflight optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "line-preflight"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 8 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED final-line optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "final-line"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED canonical-route optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "canonical-route"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 3 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED ialign-context optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "ialign-context"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 4 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED payload-bound optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "payload-bound"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED image-bound optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "image-bound"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED payload-type optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "payload-type"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED image-type optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "image-type"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED source-fingerprint optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "source-fingerprint"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 2 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED entry-forward optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "entry-forward"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 6 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED writer-delegation optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "writer-delegation"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    tally.arm(
        "RED writer-order optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_image.py",
            &["--mutation", "writer-order"],
        ),
        1,
        "MATCHED-GPR-IMAGE: 33 tests / 1 failures / 0 errors; construction only",
    );
    // P4.14 a42b: literal ELF64 fields/layout, including optimized refusal guards.
    tally.arm(
        "GREEN ELF ABI layout normal",
        probe(repo, false, "scripts/probe_elf_writer.py", &[]),
        0,
        "ELF-WRITER: 15 tests / 0 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED segment-offset normal",
        probe(
            repo,
            false,
            "scripts/probe_elf_writer.py",
            &["--mutation", "segment-offset"],
        ),
        1,
        "ELF-WRITER: 15 tests / 1 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED page-declaration normal",
        probe(
            repo,
            false,
            "scripts/probe_elf_writer.py",
            &["--mutation", "page-declaration"],
        ),
        1,
        "ELF-WRITER: 15 tests / 2 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED section-table normal",
        probe(
            repo,
            false,
            "scripts/probe_elf_writer.py",
            &["--mutation", "section-table"],
        ),
        1,
        "ELF-WRITER: 15 tests / 1 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED text-alignment normal",
        probe(
            repo,
            false,
            "scripts/probe_elf_writer.py",
            &["--mutation", "text-alignment"],
        ),
        1,
        "ELF-WRITER: 15 tests / 1 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED rvc-flag normal",
        probe(
            repo,
            false,
            "scripts/probe_elf_writer.py",
            &["--mutation", "rvc-flag"],
        ),
        1,
        "ELF-WRITER: 15 tests / 1 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED ialign-guard normal",
        probe(
            repo,
            false,
            "scripts/probe_elf_writer.py",
            &["--mutation", "ialign-guard"],
        ),
        1,
        "ELF-WRITER: 15 tests / 9 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED entry-guard normal",
        probe(
            repo,
            false,
            "scripts/probe_elf_writer.py",
            &["--mutation", "entry-guard"],
        ),
        1,
        "ELF-WRITER: 15 tests / 6 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED extent-guard normal",
        probe(
            repo,
            false,
            "scripts/probe_elf_writer.py",
            &["--mutation", "extent-guard"],
        ),
        1,
        "ELF-WRITER: 15 tests / 1 failures / 0 errors; no qualification",
    );
    tally.arm(
        "GREEN ELF ABI layout optimized",
        probe(repo, true, "scripts/probe_elf_writer.py", &[]),
        0,
        "ELF-WRITER: 15 tests / 0 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED segment-offset optimized",
        probe(
            repo,
            true,
            "scripts/probe_elf_writer.py",
            &["--mutation", "segment-offset"],
        ),
        1,
        "ELF-WRITER: 15 tests / 1 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED page-declaration optimized",
        probe(
            repo,
            true,
            "scripts/probe_elf_writer.py",
            &["--mutation", "page-declaration"],
        ),
        1,
        "ELF-WRITER: 15 tests / 2 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED section-table optimized",
        probe(
            repo,
            true,
            "scripts/probe_elf_writer.py",
            &["--mutation", "section-table"],
        ),
        1,
        "ELF-WRITER: 15 tests / 1 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED text-alignment optimized",
        probe(
            repo,
            true,
            "scripts/probe_elf_writer.py",
            &["--mutation", "text-alignment"],
        ),
        1,
        "ELF-WRITER: 15 tests / 1 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED rvc-flag optimized",
        probe(
            repo,
            true,
            "scripts/probe_elf_writer.py",
            &["--mutation", "rvc-flag"],
        ),
        1,
        "ELF-WRITER: 15 tests / 1 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED ialign-guard optimized",
        probe(
            repo,
            true,
            "scripts/probe_elf_writer.py",
            &["--mutation", "ialign-guard"],
        ),
        1,
        "ELF-WRITER: 15 tests / 9 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED entry-guard optimized",
        probe(
            repo,
            true,
            "scripts/probe_elf_writer.py",
            &["--mutation", "entry-guard"],
        ),
        1,
        "ELF-WRITER: 15 tests / 6 failures / 0 errors; no qualification",
    );
    tally.arm(
        "RED extent-guard optimized",
        probe(
            repo,
            true,
            "scripts/probe_elf_writer.py",
            &["--mutation", "extent-guard"],
        ),
        1,
        "ELF-WRITER: 15 tests / 1 failures / 0 errors; no qualification",
    );
    // P4-SYSTEM.12 d1: isolate the full C composition; the expected words and byte
    // image are hand-written spec-side fixtures, independent of the live corpus.
    tally.arm(
        "GREEN C assembler words and exact byte image",
        probe(repo, false, "scripts/probe_c_assembler.py", &[]),
        0,
        "37 spec-side words",
    );
    tally.arm(
        "RED a wrong compact-register base is caught",
        probe(
            repo,
            false,
            "scripts/probe_c_assembler.py",
            &["--mutation", "compact-base"],
        ),
        1,
        "c.addi4spn: 0x0044, expected 0x0040",
    );
    tally.arm(
        "RED word-stride labels are caught",
        probe(
            repo,
            false,
            "scripts/probe_c_assembler.py",
            &["--mutation", "label-stride"],
        ),
        1,
        "AssertionError: byte label addresses",
    );
    tally.arm(
        "RED silently padded short units are caught",
        probe(
            repo,
            false,
            "scripts/probe_c_assembler.py",
            &["--mutation", "padding"],
        ),
        1,
        "AssertionError: exact byte image",
    );
    // d2: the emitted byte fixture is consumed by the actual runner, not a second loader.
    tally.arm(
        "GREEN mixed C fixture executes through the tracked runner",
        probe(repo, false, "scripts/probe_c_guest_image.py", &[]),
        0,
        "mixed bytes, labels, writes and parcel counts passed",
    );
    tally.arm(
        "RED a padded generated image is caught",
        probe(
            repo,
            false,
            "scripts/probe_c_guest_image.py",
            &["--mutation", "padding"],
        ),
        1,
        "AssertionError: exact generated image bytes",
    );
    tally.arm(
        "RED a runner that loads at the wrong offset is caught",
        probe(
            repo,
            false,
            "scripts/probe_c_guest_image.py",
            &["--mutation", "runner-offset"],
        ),
        1,
        "mixed: step 0 writes match",
    );
    // d3a: promote the independent author, preserve its owned records, refuse reserved bits.
    tally.arm(
        "GREEN tracked author re-derives its owned corpus and refuses reserved bits",
        probe(repo, false, "scripts/probe_gc_author.py", &[]),
        0,
        "owned corpus passed",
    );
    tally.arm(
        "RED a missing OP fixed-bit guard is caught",
        probe(
            repo,
            false,
            "scripts/probe_gc_author.py",
            &["--mutation", "reserved-op"],
        ),
        1,
        "reserved word 0x04000033 accepted",
    );
    tally.arm(
        "RED a missing shift fixed-bit guard is caught",
        probe(
            repo,
            false,
            "scripts/probe_gc_author.py",
            &["--mutation", "reserved-shift"],
        ),
        1,
        "reserved word 0x04001013 accepted",
    );
    tally.arm(
        "RED division rounding away from zero changes the authored M record",
        probe(
            repo,
            false,
            "scripts/probe_gc_author.py",
            &["--mutation", "division-rounding"],
        ),
        1,
        "DRIFT — m-div",
    );
    tally.arm(
        "RED a missing SUM permission is caught",
        probe(
            repo,
            false,
            "scripts/probe_gc_author.py",
            &["--mutation", "ignore-sum"],
        ),
        1,
        "SUM=1 permits S data on U pages",
    );
    tally.arm(
        "RED a missing MXR permission is caught",
        probe(
            repo,
            false,
            "scripts/probe_gc_author.py",
            &["--mutation", "ignore-mxr"],
        ),
        1,
        "MXR=1 permits an X-only load",
    );
    tally.arm(
        "RED a missing U-mode permission gate is caught",
        probe(
            repo,
            false,
            "scripts/probe_gc_author.py",
            &["--mutation", "ignore-user"],
        ),
        1,
        "U mode cannot read an S page",
    );
    // d3b: absent ordinary rows/process output must never become reference agreement.
    tally.arm(
        "GREEN scalar reference processes, fresh output and binary pins",
        probe(repo, false, "scripts/probe_smoke_runner.py", &[]),
        0,
        "16 process/output/pin controls; three defective lifecycles rejected",
    );
    tally.arm(
        "GREEN strict Sail rows and witnessed delivery gaps",
        probe(repo, false, "scripts/probe_gc_sail.py", &[]),
        0,
        "failed processes and stale traces passed",
    );
    tally.arm(
        "RED absent ordinary no-write steps cannot agree",
        probe(
            repo,
            false,
            "scripts/probe_gc_sail.py",
            &["--mutation", "permit-missing"],
        ),
        1,
        "empty ordinary no-write trace accepted",
    );
    tally.arm(
        "RED failed reference processes cannot agree",
        probe(
            repo,
            false,
            "scripts/probe_gc_sail.py",
            &["--mutation", "ignore-status"],
        ),
        1,
        "failed reference process accepted",
    );
    tally.arm(
        "RED declared delivery gaps still need trace events",
        probe(
            repo,
            false,
            "scripts/probe_gc_sail.py",
            &["--mutation", "unwitnessed-gap"],
        ),
        1,
        "unwitnessed delivery gap accepted",
    );
    tally.arm(
        "RED stale traces cannot stand in for a new run",
        probe(
            repo,
            false,
            "scripts/probe_gc_sail.py",
            &["--mutation", "keep-stale"],
        ),
        1,
        "stale traces accepted as a new run",
    );
    tally.arm(
        "RED parcel interrupt annotations require their witnessed event",
        probe(
            repo,
            false,
            "scripts/probe_gc_sail.py",
            &["--mutation", "ignore-parcel-interrupt"],
        ),
        1,
        "missing expected step 0 (c.addi x10, 1)",
    );
    tally.arm(
        "RED Sail trace rows cannot exceed the declared budget",
        probe(
            repo,
            false,
            "scripts/probe_gc_sail.py",
            &["--mutation", "ignore-extra-rows"],
        ),
        1,
        "out-of-budget instruction row accepted",
    );
    tally.arm(
        "RED Sail witnessed deliveries cannot exceed the declared budget",
        probe(
            repo,
            false,
            "scripts/probe_gc_sail.py",
            &["--mutation", "ignore-extra-deliveries"],
        ),
        1,
        "out-of-budget interrupt delivery accepted",
    );
    // P4.14 a28: structured differences, full-tail validation, both Python modes.
    tally.arm(
        "GREEN structured Sail comparison normal",
        probe(repo, false, "scripts/probe_sail_comparison.py", &[]),
        0,
        "Ran 34 tests",
    );
    tally.arm(
        "RED Sail lose-difference normal",
        probe(
            repo,
            false,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "lose-difference"],
        ),
        1,
        "FAILED (failures=11)",
    );
    tally.arm(
        "RED Sail wrong-boundary normal",
        probe(
            repo,
            false,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "wrong-boundary"],
        ),
        1,
        "FAILED (failures=10)",
    );
    tally.arm(
        "RED Sail reverse-change-sets normal",
        probe(
            repo,
            false,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "reverse-change-sets"],
        ),
        1,
        "FAILED (failures=10)",
    );
    tally.arm(
        "RED Sail lose-extra-changes normal",
        probe(
            repo,
            false,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "lose-extra-changes"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED Sail ignore-status normal",
        probe(
            repo,
            false,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "ignore-status"],
        ),
        1,
        "FAILED (failures=3)",
    );
    tally.arm(
        "RED Sail ignore-extra-rows normal",
        probe(
            repo,
            false,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "ignore-extra-rows"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED Sail ignore-extra-deliveries normal",
        probe(
            repo,
            false,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "ignore-extra-deliveries"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED Sail bypass-wrapper normal",
        probe(
            repo,
            false,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "bypass-wrapper"],
        ),
        1,
        "FAILED (failures=2)",
    );
    tally.arm(
        "RED Sail early-gpr-return normal",
        probe(
            repo,
            false,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "early-gpr-return"],
        ),
        1,
        "FAILED (failures=2)",
    );
    tally.arm(
        "RED Sail early-delivery-return normal",
        probe(
            repo,
            false,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "early-delivery-return"],
        ),
        1,
        "FAILED (failures=2)",
    );
    tally.arm(
        "GREEN structured Sail comparison optimized",
        probe(repo, true, "scripts/probe_sail_comparison.py", &[]),
        0,
        "Ran 34 tests",
    );
    tally.arm(
        "RED Sail lose-difference optimized",
        probe(
            repo,
            true,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "lose-difference"],
        ),
        1,
        "FAILED (failures=11)",
    );
    tally.arm(
        "RED Sail wrong-boundary optimized",
        probe(
            repo,
            true,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "wrong-boundary"],
        ),
        1,
        "FAILED (failures=10)",
    );
    tally.arm(
        "RED Sail reverse-change-sets optimized",
        probe(
            repo,
            true,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "reverse-change-sets"],
        ),
        1,
        "FAILED (failures=10)",
    );
    tally.arm(
        "RED Sail lose-extra-changes optimized",
        probe(
            repo,
            true,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "lose-extra-changes"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED Sail ignore-status optimized",
        probe(
            repo,
            true,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "ignore-status"],
        ),
        1,
        "FAILED (failures=3)",
    );
    tally.arm(
        "RED Sail ignore-extra-rows optimized",
        probe(
            repo,
            true,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "ignore-extra-rows"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED Sail ignore-extra-deliveries optimized",
        probe(
            repo,
            true,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "ignore-extra-deliveries"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED Sail bypass-wrapper optimized",
        probe(
            repo,
            true,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "bypass-wrapper"],
        ),
        1,
        "FAILED (failures=2)",
    );
    tally.arm(
        "RED Sail early-gpr-return optimized",
        probe(
            repo,
            true,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "early-gpr-return"],
        ),
        1,
        "FAILED (failures=2)",
    );
    tally.arm(
        "RED Sail early-delivery-return optimized",
        probe(
            repo,
            true,
            "scripts/probe_sail_comparison.py",
            &["--mutation", "early-delivery-return"],
        ),
        1,
        "FAILED (failures=2)",
    );
    // P4.14 a29: bounded supplied-byte units, not authenticated qualification.
    tally.arm(
        "GREEN bounded GPR byte unit normal",
        probe(repo, false, "scripts/probe_matched_gpr_comparison.py", &[]),
        0,
        "Ran 52 tests",
    );
    tally.arm(
        "RED GPR byte unit byte-bounds normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "byte-bounds"],
        ),
        1,
        "FAILED (failures=6)",
    );
    tally.arm(
        "RED GPR byte unit budget-cap normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "budget-cap"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED GPR byte unit raw-schema normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "raw-schema"],
        ),
        1,
        "FAILED (failures=8)",
    );
    tally.arm(
        "RED GPR byte unit root-count normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "root-count"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED GPR byte unit step-sequence normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "step-sequence"],
        ),
        1,
        "FAILED (failures=3)",
    );
    tally.arm(
        "RED GPR byte unit rv64-range normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "rv64-range"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED GPR byte unit process-exit normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "process-exit"],
        ),
        1,
        "FAILED (failures=10)",
    );
    tally.arm(
        "RED GPR byte unit unsupported normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "unsupported"],
        ),
        1,
        "FAILED (failures=6)",
    );
    tally.arm(
        "RED GPR byte unit repeat-bytes normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "repeat-bytes"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED GPR byte unit control-bytes normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "control-bytes"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED GPR byte unit sole-value normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "sole-value"],
        ),
        1,
        "FAILED (failures=7)",
    );
    tally.arm(
        "RED GPR byte unit structured-difference normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "structured-difference"],
        ),
        1,
        "FAILED (failures=6)",
    );
    tally.arm(
        "RED GPR byte unit witness-register normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "witness-register"],
        ),
        1,
        "FAILED (failures=5)",
    );
    tally.arm(
        "RED GPR byte unit decimal-conversion normal",
        probe(
            repo,
            false,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "decimal-conversion"],
        ),
        1,
        "FAILED (failures=4)",
    );
    tally.arm(
        "GREEN bounded GPR byte unit optimized",
        probe(repo, true, "scripts/probe_matched_gpr_comparison.py", &[]),
        0,
        "Ran 52 tests",
    );
    tally.arm(
        "RED GPR byte unit byte-bounds optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "byte-bounds"],
        ),
        1,
        "FAILED (failures=6)",
    );
    tally.arm(
        "RED GPR byte unit budget-cap optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "budget-cap"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED GPR byte unit raw-schema optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "raw-schema"],
        ),
        1,
        "FAILED (failures=8)",
    );
    tally.arm(
        "RED GPR byte unit root-count optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "root-count"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED GPR byte unit step-sequence optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "step-sequence"],
        ),
        1,
        "FAILED (failures=3)",
    );
    tally.arm(
        "RED GPR byte unit rv64-range optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "rv64-range"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED GPR byte unit process-exit optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "process-exit"],
        ),
        1,
        "FAILED (failures=10)",
    );
    tally.arm(
        "RED GPR byte unit unsupported optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "unsupported"],
        ),
        1,
        "FAILED (failures=6)",
    );
    tally.arm(
        "RED GPR byte unit repeat-bytes optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "repeat-bytes"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED GPR byte unit control-bytes optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "control-bytes"],
        ),
        1,
        "FAILED (failures=1)",
    );
    tally.arm(
        "RED GPR byte unit sole-value optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "sole-value"],
        ),
        1,
        "FAILED (failures=7)",
    );
    tally.arm(
        "RED GPR byte unit structured-difference optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "structured-difference"],
        ),
        1,
        "FAILED (failures=6)",
    );
    tally.arm(
        "RED GPR byte unit witness-register optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "witness-register"],
        ),
        1,
        "FAILED (failures=5)",
    );
    tally.arm(
        "RED GPR byte unit decimal-conversion optimized",
        probe(
            repo,
            true,
            "scripts/probe_matched_gpr_comparison.py",
            &["--mutation", "decimal-conversion"],
        ),
        1,
        "FAILED (failures=4)",
    );
    // d3c: independent C parcel rules, including scatter basis and original trap bits.
    tally.arm(
        "GREEN independent C author expansions and effects",
        probe(repo, false, "scripts/probe_c_author.py", &[]),
        0,
        "37 expansions/effects",
    );
    tally.arm(
        "RED wrong C author compact registers",
        probe(
            repo,
            false,
            "scripts/probe_c_author.py",
            &["--mutation", "compact-base"],
        ),
        1,
        "c.addi4spn: C expansion mismatch",
    );
    tally.arm(
        "RED wrong C author immediate sign",
        probe(
            repo,
            false,
            "scripts/probe_c_author.py",
            &["--mutation", "signed-immediate"],
        ),
        1,
        "c.addi: C expansion mismatch",
    );
    tally.arm(
        "RED wrong C author length/link",
        probe(
            repo,
            false,
            "scripts/probe_c_author.py",
            &["--mutation", "link-length"],
        ),
        1,
        "C parcel advanced by wrong length",
    );
    tally.arm(
        "RED reserved C author parcels cannot execute",
        probe(
            repo,
            false,
            "scripts/probe_c_author.py",
            &["--mutation", "reserved-guard"],
        ),
        1,
        "reserved parcel 0x0000 accepted",
    );
    tally.arm(
        "RED a permutation of C immediate bits",
        probe(
            repo,
            false,
            "scripts/probe_c_author.py",
            &["--mutation", "scattered-bits"],
        ),
        1,
        "scattered bit 0x4000/6 misplaced",
    );
    tally.arm(
        "RED C illegal traps keep the original parcel",
        probe(
            repo,
            false,
            "scripts/probe_c_author.py",
            &["--mutation", "expanded-trap"],
        ),
        1,
        "FP illegal trap lost original C parcel",
    );
    // d3d1: independently walk and fetch only the required ILEN parcels.
    tally.arm(
        "GREEN independent Sv39 walk and exact parcel fetches",
        probe(repo, false, "scripts/probe_gc_fetch.py", &[]),
        0,
        "exact parcel schedules passed",
    );
    tally.arm(
        "RED a non-canonical Sv39 sign is caught",
        probe(
            repo,
            false,
            "scripts/probe_gc_fetch.py",
            &["--mutation", "canonical-sign"],
        ),
        1,
        "Sv39 sign bit and upper bits disagree",
    );
    tally.arm(
        "RED reserved Sv39 PTE high bits are caught",
        probe(
            repo,
            false,
            "scripts/probe_gc_fetch.py",
            &["--mutation", "reserved-pte"],
        ),
        1,
        "reserved PTE bit 54 accepted",
    );
    tally.arm(
        "RED non-leaf Sv39 reserved bits fault before descent",
        probe(
            repo,
            false,
            "scripts/probe_gc_fetch.py",
            &["--mutation", "nonleaf-bits"],
        ),
        1,
        "non-leaf reserved bit must fault before descending",
    );
    tally.arm(
        "RED a bottom-level pointer produces an architectural fault",
        probe(
            repo,
            false,
            "scripts/probe_gc_fetch.py",
            &["--mutation", "bottom-pointer"],
        ),
        1,
        "bottom-level pointer must page-fault",
    );
    tally.arm(
        "RED effective MPRV data privilege is caught",
        probe(
            repo,
            false,
            "scripts/probe_gc_fetch.py",
            &["--mutation", "mprv"],
        ),
        1,
        "MPRV data access must use MPP",
    );
    tally.arm(
        "RED a compressed fetch never probes its neighbor",
        probe(
            repo,
            false,
            "scripts/probe_gc_fetch.py",
            &["--mutation", "eager-second"],
        ),
        1,
        "compressed region-end fetch inspected its neighbor",
    );
    tally.arm(
        "RED an upper-parcel fault preserves VA and starting EPC",
        probe(
            repo,
            false,
            "scripts/probe_gc_fetch.py",
            &["--mutation", "fault-tval"],
        ),
        1,
        "second parcel lost fault VA/start EPC",
    );
    tally.arm(
        "RED a wider prefix retains all ILEN bits",
        probe(
            repo,
            false,
            "scripts/probe_gc_fetch.py",
            &["--mutation", "short-ilen"],
        ),
        1,
        "wider prefix lost ILEN bits",
    );
    tally.arm(
        "RED trap EPC always masks bit zero",
        probe(
            repo,
            false,
            "scripts/probe_gc_fetch.py",
            &["--mutation", "unaligned-epc"],
        ),
        1,
        "EPC bit zero was not masked",
    );
    // d3d2: exact byte guests have explicit boundary budgets and fresh memory fetches.
    tally.arm(
        "GREEN byte guest budgets, visibility and head boundaries",
        probe(repo, false, "scripts/probe_gc_parcel_guest.py", &[]),
        0,
        "5 legacy repairs / 176 steps",
    );
    tally.arm(
        "GREEN parcel author controls use only tracked inputs",
        probe(repo, false, "scripts/probe_gc_parcel_guest.py", &["--cold"]),
        0,
        "tracked-only inputs and no reference cache passed",
    );
    tally.arm(
        "RED source directives follow byte PCs",
        probe(
            repo,
            false,
            "scripts/probe_gc_parcel_guest.py",
            &["--mutation", "byte-directives"],
        ),
        1,
        "directives lost their byte PCs",
    );
    tally.arm(
        "RED author image padding is caught",
        probe(
            repo,
            false,
            "scripts/probe_gc_parcel_guest.py",
            &["--mutation", "padded-image"],
        ),
        1,
        "byte guest image acquired padding",
    );
    tally.arm(
        "RED explicit budgets continue past source end",
        probe(
            repo,
            false,
            "scripts/probe_gc_parcel_guest.py",
            &["--mutation", "source-end"],
        ),
        1,
        "explicit budget stopped at the source end",
    );
    tally.arm(
        "RED byte guest counts actual parcels",
        probe(
            repo,
            false,
            "scripts/probe_gc_parcel_guest.py",
            &["--mutation", "fetch-count"],
        ),
        1,
        "byte guest lost actual parcel counts",
    );
    tally.arm(
        "RED a delivered fetch fault does not retire",
        probe(
            repo,
            false,
            "scripts/probe_gc_parcel_guest.py",
            &["--mutation", "fault-retirement"],
        ),
        1,
        "fault boundary retired an instruction",
    );
    tally.arm(
        "RED pending delivery precedes guest fetch",
        probe(
            repo,
            false,
            "scripts/probe_gc_parcel_guest.py",
            &["--mutation", "head-pending"],
        ),
        1,
        "pending interrupt fetched the instruction",
    );
    tally.arm(
        "RED the next fetch observes a code patch",
        probe(
            repo,
            false,
            "scripts/probe_gc_parcel_guest.py",
            &["--mutation", "code-visibility"],
        ),
        1,
        "next parcel ignored the code patch",
    );
    tally.arm(
        "RED unknown valid vocabulary refuses by name",
        probe(
            repo,
            false,
            "scripts/probe_gc_parcel_guest.py",
            &["--mutation", "unknown-valid"],
        ),
        1,
        "unknown valid vocabulary became an illegal trap",
    );
    // e1a: the spec-side author honors fixed fields and privileged instruction legality.
    tally.arm(
        "GREEN fixed misa and privileged author legality",
        probe(repo, false, "scripts/probe_gc_privilege_author.py", &[]),
        0,
        "5 corpus repairs / 140 steps",
    );
    tally.arm(
        "RED fixed misa reset is derived from the selected set",
        probe(
            repo,
            false,
            "scripts/probe_gc_privilege_author.py",
            &["--mutation", "misa-reset"],
        ),
        1,
        "misa lost the fixed selected reset",
    );
    tally.arm(
        "RED writes retain read-only misa fields",
        probe(
            repo,
            false,
            "scripts/probe_gc_privilege_author.py",
            &["--mutation", "misa-write"],
        ),
        1,
        "misa accepted a write to read-only fields",
    );
    tally.arm(
        "RED CSR privilege failures suppress all own effects",
        probe(
            repo,
            false,
            "scripts/probe_gc_privilege_author.py",
            &["--mutation", "csr-privilege"],
        ),
        1,
        "CSR privilege fault lost its unit discipline",
    );
    tally.arm(
        "RED S-mode satp access honors TVM",
        probe(
            repo,
            false,
            "scripts/probe_gc_privilege_author.py",
            &["--mutation", "satp-tvm"],
        ),
        1,
        "S-mode satp ignored TVM",
    );
    tally.arm(
        "RED MRET requires M-mode",
        probe(
            repo,
            false,
            "scripts/probe_gc_privilege_author.py",
            &["--mutation", "mret-mode"],
        ),
        1,
        "MRET below M popped the stack",
    );
    tally.arm(
        "RED SRET refuses U-mode",
        probe(
            repo,
            false,
            "scripts/probe_gc_privilege_author.py",
            &["--mutation", "sret-mode"],
        ),
        1,
        "U-mode SRET popped the stack",
    );
    tally.arm(
        "RED S-mode SRET honors TSR",
        probe(
            repo,
            false,
            "scripts/probe_gc_privilege_author.py",
            &["--mutation", "sret-tsr"],
        ),
        1,
        "S-mode SRET ignored TSR",
    );
    tally.arm(
        "RED SFENCE.VMA refuses U-mode",
        probe(
            repo,
            false,
            "scripts/probe_gc_privilege_author.py",
            &["--mutation", "sfence-mode"],
        ),
        1,
        "U-mode SFENCE.VMA executed",
    );
    tally.arm(
        "RED S-mode SFENCE.VMA honors TVM",
        probe(
            repo,
            false,
            "scripts/probe_gc_privilege_author.py",
            &["--mutation", "sfence-tvm"],
        ),
        1,
        "S-mode SFENCE.VMA ignored TVM",
    );
    // P4-SYSTEM.13 c7a: nondelegated supervisor interrupt bits are read-only zero.
    tally.arm(
        "RED sip hides undelegated pending sources",
        probe(
            repo,
            false,
            "scripts/probe_gc_privilege_author.py",
            &["--mutation", "sip-read-delegation"],
        ),
        1,
        "sip delegation/owner read mismatch",
    );
    tally.arm(
        "RED sie hides undelegated enables",
        probe(
            repo,
            false,
            "scripts/probe_gc_privilege_author.py",
            &["--mutation", "sie-read-delegation"],
        ),
        1,
        "sie exposed an undelegated bit",
    );
    tally.arm(
        "RED sip preserves undelegated pending sources",
        probe(
            repo,
            false,
            "scripts/probe_gc_privilege_author.py",
            &["--mutation", "sip-write-delegation"],
        ),
        1,
        "sip wrote an undelegated bit",
    );
    tally.arm(
        "RED sie preserves undelegated enables",
        probe(
            repo,
            false,
            "scripts/probe_gc_privilege_author.py",
            &["--mutation", "sie-write-delegation"],
        ),
        1,
        "sie wrote an undelegated bit",
    );
    tally.arm(
        "RED sip reads its mip owner",
        probe(
            repo,
            false,
            "scripts/probe_gc_privilege_author.py",
            &["--mutation", "sip-owner"],
        ),
        1,
        "sip delegation/owner read mismatch",
    );
    // e1b1: hand-encoded integer controls precede the expanded corpus derivation.
    tally.arm(
        "GREEN base integer author vocabulary",
        probe(repo, false, "scripts/probe_gc_integer_author.py", &[]),
        0,
        "17 corpus gaps / 476 steps",
    );
    tally.arm(
        "RED SLTIU extends before unsigned comparison",
        probe(
            repo,
            false,
            "scripts/probe_gc_integer_author.py",
            &["--mutation", "sltiu-sign"],
        ),
        1,
        "SLTIU sign extension",
    );
    tally.arm(
        "RED XLEN register shifts use six count bits",
        probe(
            repo,
            false,
            "scripts/probe_gc_integer_author.py",
            &["--mutation", "xlen-count"],
        ),
        1,
        "XLEN shift count",
    );
    tally.arm(
        "RED word register shifts use five count bits",
        probe(
            repo,
            false,
            "scripts/probe_gc_integer_author.py",
            &["--mutation", "word-count"],
        ),
        1,
        "word shift count",
    );
    tally.arm(
        "RED SRAW preserves the word sign",
        probe(
            repo,
            false,
            "scripts/probe_gc_integer_author.py",
            &["--mutation", "word-sign"],
        ),
        1,
        "word arithmetic shift",
    );
    tally.arm(
        "RED SRAW independently masks its register count",
        probe(
            repo,
            false,
            "scripts/probe_gc_integer_author.py",
            &["--mutation", "sraw-count"],
        ),
        1,
        "SRAW five-bit count",
    );
    tally.arm(
        "RED SRAW truncates its source before arithmetic shift",
        probe(
            repo,
            false,
            "scripts/probe_gc_integer_author.py",
            &["--mutation", "sraw-width"],
        ),
        1,
        "word arithmetic shift",
    );
    tally.arm(
        "RED SRAIW truncates its source before arithmetic shift",
        probe(
            repo,
            false,
            "scripts/probe_gc_integer_author.py",
            &["--mutation", "sraiw-width"],
        ),
        1,
        "immediate word arithmetic shift",
    );
    tally.arm(
        "RED signed branches compare signed operands",
        probe(
            repo,
            false,
            "scripts/probe_gc_integer_author.py",
            &["--mutation", "branch-sign"],
        ),
        1,
        "branch signed/unsigned decision",
    );
    tally.arm(
        "RED narrow loads retain signed extension",
        probe(
            repo,
            false,
            "scripts/probe_gc_integer_author.py",
            &["--mutation", "load-sign"],
        ),
        1,
        "narrow load extension",
    );
    tally.arm(
        "RED byte stores preserve neighboring bytes",
        probe(
            repo,
            false,
            "scripts/probe_gc_integer_author.py",
            &["--mutation", "store-width"],
        ),
        1,
        "narrow store width",
    );
    tally.arm(
        "RED reserved W shifts have no own effect",
        probe(
            repo,
            false,
            "scripts/probe_gc_integer_author.py",
            &["--mutation", "reserved-word"],
        ),
        1,
        "reserved word shift acquired an effect",
    );
    // e1b2: selected CSR enables and every literal string retain their own rules.
    tally.arm(
        "GREEN counter permissions and literal author text",
        probe(repo, false, "scripts/probe_gc_counter_author.py", &[]),
        0,
        "3 corpus refusals / 117 steps",
    );
    tally.arm(
        "RED counter enables retain selected WARL fields",
        probe(
            repo,
            false,
            "scripts/probe_gc_counter_author.py",
            &["--mutation", "enable-mask"],
        ),
        1,
        "CSR enable legalization",
    );
    tally.arm(
        "RED menvcfg writes only STCE",
        probe(
            repo,
            false,
            "scripts/probe_gc_counter_author.py",
            &["--mutation", "stce-mask"],
        ),
        1,
        "CSR enable legalization",
    );
    tally.arm(
        "RED S stimecmp requires TM",
        probe(
            repo,
            false,
            "scripts/probe_gc_counter_author.py",
            &["--mutation", "timer-tm"],
        ),
        1,
        "stimecmp TM gate",
    );
    tally.arm(
        "RED S stimecmp requires STCE",
        probe(
            repo,
            false,
            "scripts/probe_gc_counter_author.py",
            &["--mutation", "timer-stce"],
        ),
        1,
        "stimecmp STCE gate",
    );
    tally.arm(
        "RED counter access remains gated below M",
        probe(
            repo,
            false,
            "scripts/probe_gc_counter_author.py",
            &["--mutation", "counter-enable"],
        ),
        1,
        "counter mode enable gate",
    );
    tally.arm(
        "RED U counter access requires the S enable too",
        probe(
            repo,
            false,
            "scripts/probe_gc_counter_author.py",
            &["--mutation", "u-counter-enable"],
        ),
        1,
        "counter mode enable gate",
    );
    tally.arm(
        "RED quoted annotations retain their literal text",
        probe(
            repo,
            false,
            "scripts/probe_gc_counter_author.py",
            &["--mutation", "quote-text"],
        ),
        1,
        "quoted directive lost literal text",
    );
    tally.arm(
        "RED backslash annotations retain their literal text",
        probe(
            repo,
            false,
            "scripts/probe_gc_counter_author.py",
            &["--mutation", "backslash-text"],
        ),
        1,
        "backslash directive lost literal text",
    );
    tally.arm(
        "RED STIP source follows STCE",
        probe(
            repo,
            false,
            "scripts/probe_gc_counter_author.py",
            &["--mutation", "stip-source"],
        ),
        1,
        "STIP source selection",
    );
    tally.arm(
        "RED STCE-clear software STIP is writable",
        probe(
            repo,
            false,
            "scripts/probe_gc_counter_author.py",
            &["--mutation", "stip-fallback-write"],
        ),
        1,
        "STIP write mask",
    );
    tally.arm(
        "RED STCE-enabled comparator STIP is read-only",
        probe(
            repo,
            false,
            "scripts/probe_gc_counter_author.py",
            &["--mutation", "stip-enabled-write"],
        ),
        1,
        "STIP write mask",
    );
    tally.arm(
        "RED comparator selection retains software pending",
        probe(
            repo,
            false,
            "scripts/probe_gc_counter_author.py",
            &["--mutation", "stip-retention"],
        ),
        1,
        "STIP retained software storage",
    );
    tally.arm(
        "RED a disabled Sstc witness misses the terminal trap control",
        probe(
            repo,
            false,
            "scripts/probe_gc_counter_author.py",
            &["--disable-sstc-witness"],
        ),
        1,
        "Sstc terminal control missed: disabled positive witness",
    );
    // c31a: unsupported satp.MODE ignores all fields, not only MODE.
    tally.arm(
        "RED unsupported satp MODE ignores the complete write",
        probe(
            repo,
            false,
            "scripts/probe_gc_cache_author.py",
            &["--mutation", "satp-ignore"],
        ),
        1,
        "satp unsupported MODE must ignore whole write",
    );
    tally.arm(
        "RED unsupported satp MODE preserves ASID and PPN",
        probe(
            repo,
            false,
            "scripts/probe_gc_cache_author.py",
            &["--mutation", "satp-field-only"],
        ),
        1,
        "satp unsupported MODE must ignore whole write",
    );
    // e1c1: independent selected cache policy, with no production engine oracle.
    tally.arm(
        "GREEN independent cache and cold repeat",
        probe(repo, false, "scripts/probe_gc_cache_author.py", &[]),
        0,
        "cached corpus exact and cold repeat",
    );
    tally.arm(
        "RED cached mappings stay stale until a fence",
        probe(
            repo,
            false,
            "scripts/probe_gc_cache_author.py",
            &["--mutation", "bypass-hit"],
        ),
        1,
        "cache must retain stale mapping until fence",
    );
    tally.arm(
        "RED VA scope uses register identity",
        probe(
            repo,
            false,
            "scripts/probe_gc_cache_author.py",
            &["--mutation", "fence-value"],
        ),
        1,
        "fence must use register identity and exact scope",
    );
    tally.arm(
        "RED ASID scope uses register identity",
        probe(
            repo,
            false,
            "scripts/probe_gc_cache_author.py",
            &["--mutation", "fence-asid-value"],
        ),
        1,
        "fence must use register identity and exact scope",
    );
    tally.arm(
        "RED ancestor G reaches the cached translation",
        probe(
            repo,
            false,
            "scripts/probe_gc_cache_author.py",
            &["--mutation", "global-inheritance"],
        ),
        1,
        "non-leaf G must propagate to cache entry",
    );
    tally.arm(
        "RED cache hits honor current ASID",
        probe(
            repo,
            false,
            "scripts/probe_gc_cache_author.py",
            &["--mutation", "asid-tag"],
        ),
        1,
        "ASID change must be immediately visible",
    );
    tally.arm(
        "RED hits recheck live permissions",
        probe(
            repo,
            false,
            "scripts/probe_gc_cache_author.py",
            &["--mutation", "cached-permission"],
        ),
        1,
        "cache hit must recheck live SUM",
    );
    tally.arm(
        "RED faulting translations never install",
        probe(
            repo,
            false,
            "scripts/probe_gc_cache_author.py",
            &["--mutation", "fault-install"],
        ),
        1,
        "fault must not install cache entry",
    );
    tally.arm(
        "RED hits leave FIFO age intact",
        probe(
            repo,
            false,
            "scripts/probe_gc_cache_author.py",
            &["--mutation", "fifo-hit"],
        ),
        1,
        "FIFO hit must not refresh replacement order",
    );
    tally.arm(
        "RED fences leave FIFO cursor intact",
        probe(
            repo,
            false,
            "scripts/probe_gc_cache_author.py",
            &["--mutation", "fence-cursor"],
        ),
        1,
        "fence changed FIFO cursor",
    );
    tally.arm(
        "RED selected ASID ignores high bits",
        probe(
            repo,
            false,
            "scripts/probe_gc_cache_author.py",
            &["--mutation", "asid-mask"],
        ),
        1,
        "fence must mask ASIDLEN without selecting x0 scope",
    );
    tally.arm(
        "RED ASID fences preserve globals",
        probe(
            repo,
            false,
            "scripts/probe_gc_cache_author.py",
            &["--mutation", "global-retention"],
        ),
        1,
        "fence must use register identity and exact scope",
    );
    tally.arm(
        "RED invalid VA fences have no effect",
        probe(
            repo,
            false,
            "scripts/probe_gc_cache_author.py",
            &["--mutation", "invalid-fence"],
        ),
        1,
        "invalid fence VA must have no effect",
    );
    tally.arm(
        "RED illegal fences cannot touch the cache",
        probe(
            repo,
            false,
            "scripts/probe_gc_cache_author.py",
            &["--mutation", "illegal-fence"],
        ),
        1,
        "illegal fence must not change cache",
    );
    tally.arm(
        "GREEN new author provenance and historical captures",
        probe(repo, false, "scripts/probe_gc_provenance.py", &[]),
        0,
        "GC provenance probe:",
    );
    tally.arm(
        "RED a borrowed name cannot inherit history",
        probe(
            repo,
            false,
            "scripts/probe_gc_provenance.py",
            &["--mutation", "filename-history"],
        ),
        1,
        "generic output inherited FP provenance",
    );
    tally.arm(
        "RED a parcel re-derivation cannot inherit history",
        probe(
            repo,
            false,
            "scripts/probe_gc_provenance.py",
            &["--mutation", "parcel-history"],
        ),
        1,
        "generic output inherited FP provenance",
    );
    tally.arm(
        "RED parcel provenance must name its route",
        probe(
            repo,
            false,
            "scripts/probe_gc_provenance.py",
            &["--mutation", "parcel-route"],
        ),
        1,
        "new output omitted its execution route",
    );
    tally.arm(
        "RED generic output cannot inherit FP provenance",
        probe(
            repo,
            false,
            "scripts/probe_gc_provenance.py",
            &["--mutation", "fp-fallback"],
        ),
        1,
        "generic output inherited FP provenance",
    );
    tally.arm(
        "GREEN independent count fixtures and manifest drift",
        probe(
            repo,
            false,
            "scripts/derive_gc_parcel_counts.py",
            &["--self-test"],
        ),
        0,
        "GC count self-test:",
    );
    tally.arm(
        "GREEN full historical parcel count census",
        probe(
            repo,
            false,
            "scripts/derive_gc_parcel_counts.py",
            &["--out", "target/guest-gen/parcel-counts.json"],
        ),
        0,
        "exact architectural traces;",
    );
    tally.arm(
        "RED count adoption refuses changed observations",
        probe(
            repo,
            false,
            "scripts/derive_gc_parcel_counts.py",
            &["--mutation", "observation"],
        ),
        1,
        "architectural observations differ at boundary",
    );
    tally.arm(
        "RED count adoption checks actual request log",
        probe(
            repo,
            false,
            "scripts/derive_gc_parcel_counts.py",
            &["--mutation", "extent"],
        ),
        1,
        "parcel count differs from actual request log",
    );
    tally.arm(
        "GREEN historical text survives the C extent migration",
        probe(repo, false, "scripts/probe_gc_owned_extent.py", &[]),
        0,
        "write guard and explicit route pass",
    );
    tally.arm(
        "RED fresh owned records keep declared budgets",
        probe(
            repo,
            false,
            "scripts/probe_gc_owned_extent.py",
            &["--mutation", "fresh-budget"],
        ),
        1,
        "fresh owned check",
    );
    tally.arm(
        "RED fresh owned records keep parcel provenance",
        probe(
            repo,
            false,
            "scripts/probe_gc_owned_extent.py",
            &["--mutation", "fresh-word-route"],
        ),
        1,
        "fresh owned check",
    );
    tally.arm(
        "RED historical checks cannot retain word counts with C",
        probe(
            repo,
            false,
            "scripts/probe_gc_owned_extent.py",
            &["--mutation", "old-counts"],
        ),
        1,
        "bound migrated historical check",
    );
    tally.arm(
        "RED extent migration keeps historical capture text",
        probe(
            repo,
            false,
            "scripts/probe_gc_owned_extent.py",
            &["--mutation", "parcel-prose"],
        ),
        1,
        "bound migrated historical check",
    );
    tally.arm(
        "RED historical extent reconciles actual requests",
        probe(
            repo,
            false,
            "scripts/probe_gc_owned_extent.py",
            &["--mutation", "bad-request-log"],
        ),
        1,
        "parcel extent differs from actual requests",
    );
    tally.arm(
        "RED default word route cannot overwrite a bound record",
        probe(
            repo,
            false,
            "scripts/probe_gc_owned_extent.py",
            &["--mutation", "permit-word-write"],
        ),
        1,
        "canonical word write accepted",
    );
    tally.arm(
        "GREEN independent compressed corpus staging",
        probe(repo, false, "scripts/stage_gc_c_corpus.py", &[]),
        0,
        "37 forms,",
    );
    tally.arm(
        "GREEN compressed corpus stages deterministically",
        probe(repo, false, "scripts/stage_gc_c_corpus.py", &["--check"]),
        0,
        "no production files written",
    );
    tally.arm(
        "RED staged compressed observations remain checked",
        probe(
            repo,
            false,
            "scripts/stage_gc_c_corpus.py",
            &["--mutation", "observation"],
        ),
        1,
        "staged architectural observations differ",
    );
    tally.arm(
        "RED staged compressed extent remains checked",
        probe(
            repo,
            false,
            "scripts/stage_gc_c_corpus.py",
            &["--mutation", "extent"],
        ),
        1,
        "staged extent differs from actual requests",
    );
    tally.arm(
        "GREEN pinned toolchain public selection",
        probe(repo, false, "scripts/probe_riscv_toolchain.py", &[]),
        0,
        "Toolchain probe: 20/20 controls passed",
    );
    tally.arm(
        "RED toolchain identity cannot be bypassed",
        probe(
            repo,
            false,
            "scripts/probe_riscv_toolchain.py",
            &["--mutation", "ignore-version"],
        ),
        1,
        "CONTROL-MISSED: C/wrong-clang",
    );
    let _ = fs::remove_dir_all(&t);
    // P4-SYSTEM.14 a42o: immutable source through the existing spec-side author.
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        tally.arm(
            &format!("GREEN {mode} snapshot author controls"),
            probe(repo, optimized, "scripts/probe_gc_snapshot_author.py", &[]),
            0,
            "GC-SNAPSHOT-AUTHOR: 21 tests / 0 failures / 0 errors; no reference execution",
        );
        for (mutation, failures) in SNAPSHOT_AUTHOR_CASES {
            tally.arm(&format!("RED {mode} omitted snapshot guard {mutation}"), probe(repo, optimized, "scripts/probe_gc_snapshot_author.py", &["--mutation", mutation]), 1, &format!("GC-SNAPSHOT-AUTHOR: 21 tests / {failures} failures / 0 errors; no reference execution"));
        }
    }
    // P4-SYSTEM.14 a42p: complete source-derived GPR values, never qualification.
    for (mode, optimized) in [("normal", false), ("optimized", true)] {
        tally.arm(
            &format!("GREEN source-derived GPR values {mode}"),
            probe(
                repo,
                optimized,
                "scripts/probe_matched_gpr_derivation.py",
                &[],
            ),
            0,
            "MATCHED-GPR-DERIVATION: 23 tests / 0 failures / 0 errors; no qualification",
        );
        for (mutation, losses) in SOURCE_EXPECTATION_CASES {
            tally.arm(&format!("RED source-derived GPR {mutation} {mode}"), probe(repo, optimized, "scripts/probe_matched_gpr_derivation.py", &["--mutation", mutation]), 1, &format!("MATCHED-GPR-DERIVATION: 23 tests / {losses} failures / 0 errors; no qualification"));
        }
    }
    let (pass, fail) = (tally.pass, tally.fail);
    report.out(&format!("GUEST-GEN --self-test: {pass} pass / {fail} fail"));
    fail == 0
}

/// One census pair: `gen_guests.py --check …`, its output and the verdict on stderr when it refuses or drifts, the `ok`
/// line otherwise.
fn judge_pair(
    root: &Path,
    args: &[&str],
    module: &str,
    refused: &str,
    regenerate: &str,
) -> Result<(), ExitCode> {
    let (rc, raw) = probe(root, false, "scripts/gen_guests.py", args);
    let out = captured(&raw);
    if rc == 2 {
        eprintln!("{out}");
        eprintln!("{refused}");
        return Err(ExitCode::from(2));
    }
    if rc != 0 {
        eprintln!("{out}");
        eprintln!("GUEST-GEN: FAIL — {module} is out of sync with the tracked guests and their expectations. Regenerate — never edit:\n  {regenerate}");
        return Err(ExitCode::from(1));
    }
    println!("GUEST-GEN: ok ({module} matches the tracked guests)");
    Ok(())
}

/// `cargo xtask check-guest-gen [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    // `command -v python3`
    if !on_path("python3") {
        eprintln!("GUEST-GEN: REFUSED — python3 is not on PATH; this check cannot judge.");
        return ExitCode::from(2);
    }
    if args.first().is_some_and(|arg| arg == "--self-test") {
        let mut report = Report::Terminal;
        return if self_test(root, &mut report) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    // Re-run the controls before judging, their output kept in the log: a check that no longer discriminates must
    // refuse, not pass.
    let log_path = root.join(SELF_TEST_LOG);
    if log_path
        .parent()
        .is_some_and(|d| fs::create_dir_all(d).is_err())
    {
        return ExitCode::from(2);
    }
    let Ok(log) = fs::File::create(&log_path) else {
        return ExitCode::from(2);
    };
    let mut report = Report::Log(log);
    if !self_test(root, &mut report) {
        drop(report);
        // `python3 --version >&2`: the interpreter's version line, sent to stderr as the script sent it.
        let (_, version) = merged(Command::new("python3").arg("--version"));
        eprint!("{version}");
        let text = fs::read_to_string(&log_path).unwrap_or_default();
        let lines: Vec<&str> = text.lines().collect();
        let from = lines.len().saturating_sub(80);
        for line in &lines[from..] {
            eprintln!("{line}");
        }
        eprintln!("GUEST-GEN: REFUSED — the check does not discriminate (self-test failed).");
        eprintln!("GUEST-GEN: full self-test output is in target/guest-gen/self-test.log");
        return ExitCode::from(2);
    }
    drop(report);
    if let Err(code) = judge_pair(
        root,
        &[
            "--check",
            "--encoding",
            ENCODING,
            "--guests-dir",
            GUESTS_DIR,
            "--out",
            OUT,
        ],
        OUT,
        "GUEST-GEN: REFUSED — the tracked guests could not be judged.",
        "python3 scripts/gen_guests.py",
    ) {
        return code;
    }
    // ── the census's rv64gc pair (P4-SYSTEM.2 slice h, the route flip) ─────────────────────
    if let Err(code) = judge_pair(
        root,
        &["--check", "--encoding", ENCODING_GC, "--guests-dir", GUESTS_DIR_GC, "--image-format", "bytes", "--out", OUT_GC],
        OUT_GC,
        "GUEST-GEN: REFUSED — the rv64gc tracked guests could not be judged.",
        &format!("python3 scripts/gen_guests.py --encoding {ENCODING_GC} --guests-dir {GUESTS_DIR_GC} --image-format bytes --out {OUT_GC}"),
    ) {
        return code;
    }
    // ── the base-mirror governor: `out="$(judge_mirror …)"` — stdout captured, stderr through ───────────────
    let (rc, raw) = judge_mirror(root, Path::new(GUESTS_DIR), Path::new(GUESTS_DIR_GC), false);
    let out = captured(&raw);
    if rc != 0 {
        eprintln!("{out}");
        return ExitCode::from(1);
    }
    println!("GUEST-GEN: ok ({out})");
    ExitCode::SUCCESS
}
