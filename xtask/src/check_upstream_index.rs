//! The `UPSTREAM-INDEX` doctrine's driver, ported from `scripts/check_upstream_index.sh` (`XTASK.6` slice `6ai`), which
//! is now a shim of `cargo xtask check-upstream-index`.
//!
//! Every upstream issue record (`docs/upstream/<vendor>/<id-dir>/issue.sexp`) is the authority its two indices and its
//! `REPORT.md` mirror: state and severity from the closed vocabularies, a row in both indices and a directory for every
//! row, a `verified` state earned by a pin, a captured re-run and a consumer note naming that pin, a directory named by
//! its id, `blocks` entries naming leaves a tree declares, and nothing in a subtree pointing outside it. The judge is the
//! driver's inline Python, reading the records through the pinned `sexp.py`; it runs verbatim through `python3 -`, as the
//! script ran it, and is not ported. The controls write the script's synthetic tracker (its heredocs verbatim, its four
//! Python edits as the same replacements) and print one line per arm as the script did. Each self-test arm is one
//! `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode, Stdio};

use crate::harness::scratch;

const UP: &str = "docs/upstream";
const STATES: &str = "draft reported acknowledged disputed fixed-upstream verified closed wontfix";

/// The judge, verbatim: `python3 - <root> <tracker dir> <states>`.
const JUDGE: &str = r#"import os, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(sys.argv[1]) / "scripts"))
import sexp as S

root = pathlib.Path(sys.argv[1]); up = root / sys.argv[2]
STATES = set(sys.argv[3].split()); SEV = {"high", "medium", "low"}
REQUIRED = ("id", "project", "title", "component", "severity", "state", "blocks")
# the leaf ids a `blocks` entry may name: every leaf any tracked tree owns. A blocks entry
# naming a leaf that does not exist is a lie about what is blocked (UPSTREAM-TRACK.3).
LEAF_ID = re.compile(r"^[A-Z][A-Z0-9-]*\.\d+$")
known_leaves = set()
td = root / "docs" / "tasks"
if td.is_dir():
    for t in td.glob("*.md"):
        known_leaves.update(re.findall(r"ID: `([A-Z][A-Z0-9-]*\.\d+)`", t.read_text()))
bad, checked = [], 0

if not up.is_dir():
    print("NO TRACKER  docs/upstream/ does not exist — this check cannot judge"); sys.exit(2)

issues = {}
for d in sorted(p for p in up.glob("*/*") if p.is_dir()):
    rec = d / "issue.sexp"
    if not rec.is_file():
        bad.append(f"NO RECORD   {d.relative_to(root)} is an issue directory with no issue.sexp. "
                   f"Without one the indices have nothing to be checked against.")
        continue
    try:
        form = S.read_file(rec)[0]
        if S.head(form, str(rec)) != "issue":
            bad.append(f"BAD RECORD  {rec.relative_to(root)}: expected one (issue …) form"); continue
        f = {k: str(S.field(form, k, str(rec))) for k in REQUIRED}
    except Exception as exc:                                  # noqa: BLE001
        bad.append(f"BAD RECORD  {rec.relative_to(root)}: {exc}"); continue
    checked += 1
    if f["state"] not in STATES:
        bad.append(f"BAD STATE   {f['id']}: {f['state']!r} is not one of: {' '.join(sorted(STATES))}")
    if f["severity"] not in SEV:
        bad.append(f"BAD SEV     {f['id']}: {f['severity']!r} is not one of: {' '.join(sorted(SEV))}")
    # exposure (UPSTREAM-TRACK.3): `blocks` is required (empty = blocks nothing), and every
    # entry names a leaf that EXISTS — an exposure naming nothing is a lie about what is blocked.
    for leaf in f["blocks"].split():
        if not LEAF_ID.match(leaf):
            bad.append(f"BAD BLOCKS  {f['id']}: {leaf!r} is not a leaf id (TREE-LEAF shape)")
        elif leaf not in known_leaves:
            bad.append(f"DANGLING BLOCKS {f['id']}: blocks {leaf!r}, which no tracked tree "
                       f"declares — the exposure points at nothing")
    if f["id"] in issues:
        bad.append(f"DUP ID      {f['id']} declared by two directories")
    if not d.name.startswith(f["id"] + "-"):
        bad.append(f"NAME DRIFT  {d.relative_to(root)} does not start with its id {f['id']!r}")
    # a verified state must name what it was verified against AND carry the captured re-run
    # inside the subtree — a pin quoted from a changelog plus a result quoted from memory is
    # two claims, not evidence (leaf UPSTREAM-TRACK.2).
    if f["state"] == "verified":
        text = rec.read_text()
        events = [c for c in S.children(form, "history") for c in S.children(c, "event")]
        if "verified-against" not in text:
            bad.append(f"UNEARNED    {f['id']}: state is `verified` but the record names no "
                       f"(verified-against …) pin. A fix we have not re-run is a claim.")
        else:
            repros = [r for e in events for r in S.children(e, "repro")]
            if not repros:
                bad.append(f"UNEARNED    {f['id']}: `verified` names a pin but captures no "
                           f"(repro …) re-run output inside the subtree. The pin retires the "
                           f"changelog claim; only the captured output retires ours.")
            for r in repros:
                if len(r) != 2 or not isinstance(r[1], str):
                    bad.append(f"UNEARNED    {f['id']}: (repro …) must be a single artifact "
                               f"path, got {r!r}")
                    continue
                rp = (d / r[1]).resolve()
                if not str(rp).startswith(str(d.resolve()) + os.sep) or not rp.is_file():
                    bad.append(f"UNEARNED    {f['id']}: repro artifact {r[1]!r} is not a file "
                               f"inside the issue subtree. A maintainer copying the directory "
                               f"out must carry the evidence with it.")
            # a verified state must also tell upstream, in the same envelope (UPSTREAM-TRACK.4)
            pins = [str(c[1]) for e in events for c in S.children(e, "verified-against")
                    if len(c) == 2]
            note = d / "VERIFIED.md"
            if not note.is_file():
                bad.append(f"UNANNOUNCED {f['id']}: state is `verified` but the subtree carries "
                           f"no VERIFIED.md — the reply to upstream travels in the same "
                           f"envelope as the report it answers.")
            else:
                nt = note.read_text()
                for p in pins:
                    if p not in nt:
                        bad.append(f"UNANNOUNCED {f['id']}: VERIFIED.md does not name the pin "
                                   f"the record was verified against ({p[:12]}…); the note "
                                   f"and the record must agree.")
    f["dir"] = d
    issues[f["id"]] = f

# --- 3. REPORT.md agrees with the record beside it
for iid, f in issues.items():
    rep = f["dir"] / "REPORT.md"
    if not rep.is_file():
        bad.append(f"NO REPORT   {iid}: no REPORT.md in its subtree"); continue
    t = rep.read_text()
    for key, want in (("State", f["state"]), ("Severity", f["severity"]), ("ID", f["id"])):
        m = re.search(rf"^\|\s*\*\*{key}\*\*\s*\|(.*)$", t, re.M)
        if not m:
            bad.append(f"REPORT GAP  {iid}: REPORT.md has no **{key}** row"); continue
        if f"`{want}`" not in m.group(1):
            bad.append(f"REPORT DRIFT {iid}: REPORT.md's **{key}** row says "
                       f"{m.group(1).strip()[:40]!r}; issue.sexp says `{want}`")

# --- 4/5/6. the two indices mirror the records, both directions
def rows(path):
    if not path.is_file():
        return None
    out = {}
    for line in path.read_text().splitlines():
        m = re.match(r"\|\s*\[?`(LS-\d+|[A-Z]+-\d+)`\]?", line)
        if m:
            out[m.group(1)] = line
    return out

for label, path in (("VENDOR", up / "linkedspec" / "README.md"), ("TOP", up / "README.md")):
    r = rows(path)
    if r is None:
        bad.append(f"NO INDEX    {label}: {path.relative_to(root)} is missing"); continue
    for iid in issues:
        if iid not in r:
            bad.append(f"MISSING ROW {label}: {path.relative_to(root)} lists no row for {iid}")
    for iid in r:
        if iid not in issues:
            bad.append(f"ORPHAN ROW  {label}: {path.relative_to(root)} lists {iid}, which has no "
                       f"issue directory")
    for iid, f in issues.items():
        if iid in r and f"`{f['state']}`" not in r[iid]:
            bad.append(f"STATE DRIFT {label}: the row for {iid} does not carry its state "
                       f"`{f['state']}`")
        if iid in r and f"`{f['severity']}`" not in r[iid]:
            bad.append(f"SEV DRIFT   {label}: the row for {iid} does not carry `{f['severity']}`")

# --- 7. self-containment: nothing in a subtree may point outside it
ESCAPE = re.compile(r"(\.\./\.\./|/Volumes/|/Users/|\bdocs/tasks/|\bscripts/|\bprofiles/|\bdefinitions/)")
for iid, f in issues.items():
    for p in sorted(f["dir"].rglob("*")):
        if not p.is_file() or p.suffix in (".patch",):
            continue
        for n, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
            m = ESCAPE.search(line)
            if m and "docs/.../" not in line:
                bad.append(f"NOT CONTAINED {iid}: {p.relative_to(root)}:{n} references "
                           f"{m.group(1)!r} — outside its own subtree. A maintainer who copies "
                           f"this directory out would get a broken issue.")
                break

for b in bad:
    print(f"  {b}")
print(f"__CHECKED__ {checked}")
sys.exit(1 if bad else 0)
"#;

/// `scan <root> <up> <states> 2>&1`: the judge on stdin, stdout and stderr together.
fn scan(repo: &Path, root: &Path, both: bool) -> (i32, String) {
    let mut command = Command::new("python3");
    command
        .arg("-")
        .arg(root)
        .arg(UP)
        .arg(STATES)
        .current_dir(repo)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(if both {
            Stdio::piped()
        } else {
            Stdio::inherit()
        });
    let Ok(mut child) = command.spawn() else {
        return (-1, "cannot run python3".to_owned());
    };
    if let Some(mut stdin) = child.stdin.take() {
        let _ = stdin.write_all(JUDGE.as_bytes());
    }
    match child.wait_with_output() {
        Ok(o) => {
            let mut text = String::from_utf8_lossy(&o.stdout).into_owned();
            text.push_str(&String::from_utf8_lossy(&o.stderr));
            (o.status.code().unwrap_or(-1), text)
        }
        Err(e) => (-1, e.to_string()),
    }
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

/// `t.replace(a, b)` on a file, every occurrence, as the script's Python edits did.
fn replace_in(path: &Path, from: &str, to: &str) {
    if let Ok(text) = fs::read_to_string(path) {
        let _ = fs::write(path, text.replace(from, to));
    }
}

struct Tally<'a> {
    repo: &'a Path,
    root: &'a Path,
    pass: u32,
    fail: u32,
}

impl Tally<'_> {
    /// One arm, printed as the script printed it: `  ok    <label>` or `  FAIL  <label>: …` with the first output line.
    fn arm(&mut self, label: &str, want_rc: i32, needle: &str) {
        let (rc, out) = scan(self.repo, self.root, true);
        let out = captured(&out);
        let first = out.lines().next().unwrap_or("");
        if rc != want_rc {
            println!("  FAIL  {label}: exit {rc}, expected {want_rc} — {first}");
            self.fail += 1;
            return;
        }
        if !needle.is_empty() && !out.contains(needle) {
            println!("  FAIL  {label}: right exit, wrong reason — wanted '{needle}', got: {first}");
            self.fail += 1;
            return;
        }
        println!("  ok    {label}");
        self.pass += 1;
    }
}

/// The script's `mk <dir> <id> <state> <severity>`: an issue record and its report.
fn mk(tmp: &Path, dir: &str, id: &str, state: &str, severity: &str) -> PathBuf {
    let d = tmp.join("docs/upstream/linkedspec").join(dir);
    write(
        &d.join("issue.sexp"),
        &format!("(issue (id \"{id}\") (project \"linkedspec\") (title \"t\") (component \"c\")\n       (severity {severity}) (state {state}) (blocks \"\"))\n"),
    );
    write(
        &d.join("REPORT.md"),
        &format!("| | |\n| --- | --- |\n| **ID** | `{id}` |\n| **Severity** | `{severity}` |\n| **State** | `{state}` |\n"),
    );
    d
}

/// The script's `idx <top-row> <vendor-row>`.
fn idx(tmp: &Path, top: &str, vendor: &str) {
    let _ = fs::create_dir_all(tmp.join("docs/upstream/linkedspec"));
    write(
        &tmp.join("docs/upstream/README.md"),
        &format!("| ID |\n| --- |\n{top}\n"),
    );
    write(
        &tmp.join("docs/upstream/linkedspec/README.md"),
        &format!("| ID |\n| --- |\n{vendor}\n"),
    );
}

/// The script's `reset`.
fn reset(tmp: &Path) {
    let _ = fs::remove_dir_all(tmp.join("docs"));
    let _ = fs::create_dir_all(tmp.join("docs/upstream/linkedspec"));
}

/// A verified record with the given history tail, and the one-line report the script wrote beside it.
fn verified_record(d: &Path, pin: &str, repro: Option<&str>) {
    let repro_form = repro.map_or(String::new(), |r| {
        format!("\n                       (repro \"{r}\")")
    });
    write(
        &d.join("issue.sexp"),
        &format!("(issue (id \"LS-001\") (project \"linkedspec\") (title \"t\") (component \"c\")\n       (severity high) (state verified) (blocks \"\")\n       (history (event (date \"2026-09-26\") (state verified)\n                       (verified-against \"{pin}\"){repro_form})))\n"),
    );
}

const VERIFIED_ROW: &str = "| [`LS-001`](x) | t | `high` | `verified` |";
const LN: &str = "| [`LS-001`](x) | t | `high` | `draft` |";

/// The RED/GREEN controls over the script's synthetic tracker.
fn self_test(repo: &Path) -> bool {
    let Ok(tmp) = scratch(repo, "target/tmp", "check_upstream_index") else {
        return false;
    };
    let _ = fs::create_dir_all(tmp.join("scripts"));
    let _ = fs::copy(repo.join("scripts/sexp.py"), tmp.join("scripts/sexp.py"));
    let mut tally = Tally {
        repo,
        root: &tmp,
        pass: 0,
        fail: 0,
    };
    let issue = tmp.join("docs/upstream/linkedspec/LS-001-a/issue.sexp");
    let report = tmp.join("docs/upstream/linkedspec/LS-001-a/REPORT.md");
    reset(&tmp);
    mk(&tmp, "LS-001-a", "LS-001", "draft", "high");
    idx(&tmp, LN, LN);
    tally.arm("GREEN a consistent tracker passes", 0, "__CHECKED__ 1");
    reset(&tmp);
    mk(&tmp, "LS-001-a", "LS-001", "reported", "high");
    idx(&tmp, LN, LN);
    tally.arm("RED   the index carries a stale STATE", 1, "STATE DRIFT");
    reset(&tmp);
    mk(&tmp, "LS-001-a", "LS-001", "draft", "medium");
    idx(&tmp, LN, LN);
    tally.arm("RED   the index carries a stale SEVERITY", 1, "SEV DRIFT");
    reset(&tmp);
    mk(&tmp, "LS-001-a", "LS-001", "draft", "high");
    idx(&tmp, LN, "| x |");
    tally.arm(
        "RED   an issue with no row in the vendor index",
        1,
        "MISSING ROW VENDOR",
    );
    reset(&tmp);
    mk(&tmp, "LS-001-a", "LS-001", "draft", "high");
    idx(&tmp, "| [`LS-009`](x) | t | `high` | `draft` |", LN);
    tally.arm(
        "RED   an index row with no issue directory",
        1,
        "ORPHAN ROW",
    );
    reset(&tmp);
    mk(&tmp, "LS-001-a", "LS-001", "invented", "high");
    idx(&tmp, LN, LN);
    tally.arm(
        "RED   a state outside the vocabulary is refused",
        1,
        "BAD STATE",
    );
    reset(&tmp);
    mk(&tmp, "LS-001-a", "LS-001", "draft", "catastrophic");
    idx(&tmp, LN, LN);
    tally.arm(
        "RED   a severity outside the vocabulary is refused",
        1,
        "BAD SEV",
    );
    reset(&tmp);
    mk(&tmp, "LS-001-a", "LS-001", "draft", "high");
    let _ = fs::remove_file(&issue);
    idx(&tmp, LN, LN);
    tally.arm("RED   an issue directory with no record", 1, "NO RECORD");
    reset(&tmp);
    mk(&tmp, "LS-001-a", "LS-001", "draft", "high");
    idx(&tmp, LN, LN);
    let mut text = fs::read_to_string(&report).unwrap_or_default();
    text.push_str("| **State** | `closed` |\n");
    // `sed -i.bak 's/| \*\*State\*\* | `draft` |//'`: the first occurrence on each line emptied (the `.bak` copy kept).
    let _ = fs::write(
        tmp.join("docs/upstream/linkedspec/LS-001-a/REPORT.md.bak"),
        &text,
    );
    let edited: String = text
        .split_inclusive('\n')
        .map(|l| l.replacen("| **State** | `draft` |", "", 1))
        .collect();
    let _ = fs::write(&report, edited);
    tally.arm(
        "RED   REPORT.md disagrees with the record beside it",
        1,
        "REPORT DRIFT",
    );
    reset(&tmp);
    mk(&tmp, "LS-001-a", "LS-001", "draft", "high");
    idx(&tmp, LN, LN);
    write(
        &tmp.join("docs/upstream/linkedspec/LS-001-a/VALIDATE.md"),
        "see scripts/sexp.py for details\n",
    );
    tally.arm(
        "RED   a file pointing OUTSIDE its own subtree",
        1,
        "NOT CONTAINED",
    );
    reset(&tmp);
    mk(&tmp, "LS-001-a", "LS-001", "verified", "high");
    idx(&tmp, VERIFIED_ROW, VERIFIED_ROW);
    tally.arm(
        "RED   `verified` without the pin it was verified against",
        1,
        "UNEARNED",
    );
    reset(&tmp);
    let d = mk(&tmp, "LS-001-a", "LS-001", "verified", "high");
    verified_record(&d, "a8d34c845", None);
    write(&report, "| **State** | `verified` |\n");
    idx(&tmp, VERIFIED_ROW, VERIFIED_ROW);
    tally.arm(
        "RED   `verified` with a pin but no captured re-run artifact",
        1,
        "captures no",
    );
    reset(&tmp);
    let d = mk(&tmp, "LS-001-a", "LS-001", "verified", "high");
    verified_record(&d, "a8d34c845", Some("evidence/missing.txt"));
    write(&report, "| **State** | `verified` |\n");
    idx(&tmp, VERIFIED_ROW, VERIFIED_ROW);
    tally.arm(
        "RED   `verified` whose repro artifact does not exist",
        1,
        "not a file inside",
    );
    reset(&tmp);
    let d = mk(&tmp, "LS-001-a", "LS-001", "verified", "high");
    verified_record(&d, "a8d34c845", Some("../outside.txt"));
    write(&report, "| **State** | `verified` |\n");
    idx(&tmp, VERIFIED_ROW, VERIFIED_ROW);
    tally.arm(
        "RED   `verified` whose repro artifact escapes the subtree",
        1,
        "not a file inside",
    );
    reset(&tmp);
    let d = mk(&tmp, "LS-001-a", "LS-001", "verified", "high");
    verified_record(&d, "a8d34c845", Some("evidence/verified.txt"));
    write(&d.join("evidence/verified.txt"), "8 matched / 0 differed\n");
    write(
        &report,
        "| **ID** | `LS-001` |\n| **Severity** | `high` |\n| **State** | `verified` |\n",
    );
    write(&d.join("VERIFIED.md"), "verified against a8d34c84595d46c24cd1820d5fc0414261706412 by re-running the reproduction\n");
    idx(&tmp, VERIFIED_ROW, VERIFIED_ROW);
    tally.arm(
        "GREEN `verified` with a pin, the captured re-run and the consumer note",
        0,
        "__CHECKED__ 1",
    );
    reset(&tmp);
    let d = mk(&tmp, "LS-001-a", "LS-001", "verified", "high");
    verified_record(
        &d,
        "a8d34c84595d46c24cd1820d5fc0414261706412",
        Some("evidence/verified.txt"),
    );
    write(&d.join("evidence/verified.txt"), "8 matched / 0 differed\n");
    write(
        &report,
        "| **ID** | `LS-001` |\n| **Severity** | `high` |\n| **State** | `verified` |\n",
    );
    write(
        &d.join("VERIFIED.md"),
        "verified against 9999999999999999999999999999999999999999 which is not the record pin\n",
    );
    idx(&tmp, VERIFIED_ROW, VERIFIED_ROW);
    tally.arm(
        "RED   `verified` whose VERIFIED.md names a different pin than the record",
        1,
        "does not name the pin",
    );
    reset(&tmp);
    mk(&tmp, "wrongly-named-dir", "LS-001", "draft", "high");
    idx(&tmp, LN, LN);
    tally.arm(
        "RED   a directory whose name does not carry its id",
        1,
        "NAME DRIFT",
    );
    // UPSTREAM-TRACK.3: `blocks` is required, and every entry names a leaf that EXISTS.
    reset(&tmp);
    mk(&tmp, "LS-001-a", "LS-001", "draft", "high");
    idx(&tmp, LN, LN);
    write(
        &tmp.join("docs/tasks/SOT-FORMAT.md"),
        "- ID: `SOT-FORMAT.9`\n",
    );
    replace_in(&issue, "(blocks \"\")", "(blocks \"SOT-FORMAT.9\")");
    tally.arm(
        "GREEN a blocks entry naming a real leaf",
        0,
        "__CHECKED__ 1",
    );
    replace_in(
        &issue,
        "(blocks \"SOT-FORMAT.9\")",
        "(blocks \"SOT-FORMAT.99\")",
    );
    tally.arm(
        "RED   a blocks entry naming a leaf no tree declares",
        1,
        "DANGLING BLOCKS",
    );
    replace_in(
        &issue,
        "(blocks \"SOT-FORMAT.99\")",
        "(blocks \"not-a-leaf\")",
    );
    tally.arm(
        "RED   a blocks entry that is not a leaf id",
        1,
        "BAD BLOCKS",
    );
    replace_in(&issue, " (blocks \"not-a-leaf\")", "");
    tally.arm(
        "RED   a record with no blocks field at all",
        1,
        "BAD RECORD",
    );
    let _ = fs::remove_dir_all(&tmp);
    println!(
        "UPSTREAM-INDEX --self-test: {} pass / {} fail",
        tally.pass, tally.fail
    );
    tally.fail == 0
}

/// `cargo xtask check-upstream-index [--self-test]`: the shell driver's lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    let _ = fs::create_dir_all(root.join("target/tmp"));
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    let (rc, out) = scan(root, root, true);
    let out = captured(&out);
    let n = out
        .lines()
        .find_map(|l| l.strip_prefix("__CHECKED__ "))
        .unwrap_or("0");
    if rc != 0 {
        eprintln!("UPSTREAM-INDEX: an index disagrees with the issues it lists.");
        for line in out.lines().filter(|l| !l.starts_with("__CHECKED__")) {
            eprintln!("{line}");
        }
        eprintln!(
            "  The ISSUE RECORD is authoritative. Fix the index, never the record to match it."
        );
        return ExitCode::from(u8::try_from(rc).unwrap_or(1));
    }
    println!("UPSTREAM-INDEX: ok ({n} issue record(s) mirrored by both indices)");
    ExitCode::SUCCESS
}
