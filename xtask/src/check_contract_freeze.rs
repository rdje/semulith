//! The `CONTRACT-FREEZE` doctrine's driver, ported from `scripts/check_contract_freeze.sh` (`XTASK.6` slice `6aj`),
//! which is now a shim of `cargo xtask check-contract-freeze`.
//!
//! A unit's contract versions (`profiles/*/contract.sexp`) own their obligation records exactly: every member names a
//! record of that version, a frozen version's members match their pins (a frozen version is superseded, never
//! rewritten), every record belongs to one version, extensions chain without gaps or cycles, supersessions name
//! inherited records and own members. The judge is the driver's inline Python over the pinned `record_catalog` and
//! `sexp`; it runs verbatim through `python3 -`, as the script ran it — from the scratch tree in the controls, where
//! the script symlinked `scripts/` — and is not ported. The controls take the real contract and its rendered
//! catalogue and apply the script's `sed` edits as the same replacements; the ancestry probe runs plain and optimized.
//! Each self-test arm is one `tally.arm(` call, the idiom the `DERIVED-COUNTS` arm total counts.

use std::fs;
use std::io::Write;
use std::path::Path;
use std::process::{Command, ExitCode, Stdio};

use crate::harness::{combined, scratch};

/// The judge, verbatim: `python3 - <root>`.
const JUDGE: &str = r#"import hashlib, re, sys
from pathlib import Path
sys.path.insert(0, "scripts")
import sexp as S
import record_catalog as C

root = Path(sys.argv[1])
findings, units, versions_seen = [], 0, 0
for cdoc in sorted(root.glob("profiles/*/contract.sexp")):
    units += 1
    unit = cdoc.parent.name
    obs = {}
    try:
        catalog = C.text(cdoc.parent / "contract-obligations.sexp", root=root)
    except (C.CatalogRefused, S.SexpError) as error:
        findings.append(f"UNREADABLE CATALOG {unit}: {error}")
        continue
    for line in catalog.splitlines():
        m = re.match(r'\(obligation \(id "([^"]+)"\) \(contract_id "([^"]+)"\) \(contract_version "([^"]+)"\)', line)
        if m:
            obs[m.group(1)] = (line, m.group(2), m.group(3))
    versions = {}
    for form in S.read_file(cdoc):
        if not isinstance(form, list) or str(form[0]) != "contract":
            continue
        f = {str(c[0]): c for c in form[1:] if isinstance(c, list)}
        vid, ver = str(f["id"][1]), str(f["version"][1])
        members = []
        for c in form[1:]:
            if isinstance(c, list) and str(c[0]) == "member":
                mf = {str(x[0]): str(x[1]) for x in c[1:]}
                members.append((mf["id"], mf.get("sha256")))
        sups = [{str(x[0]): str(x[1]) for x in c[1:]} for c in form[1:]
                if isinstance(c, list) and str(c[0]) == "supersede"]
        versions[vid] = {"version": ver, "status": str(f["status"][1]), "members": members,
                         "extends": str(f["extends"][1]) if "extends" in f else None, "sups": sups}
    versions_seen += len(versions)
    owner = {}
    for vid, v in versions.items():
        for oid, pin in v["members"]:
            if oid in owner:
                findings.append(f"RECORD IN TWO VERSIONS {unit}: {oid} is a member of {owner[oid]} and {vid}")
            owner[oid] = vid
            rec = obs.get(oid)
            if rec is None:
                findings.append(f"MEMBER WITHOUT RECORD {unit} [{vid}]: {oid} names no obligation record")
                continue
            line, cid, cver = rec
            if (cid, cver) != (vid, v["version"]):
                findings.append(f"MEMBER OF ANOTHER VERSION {unit} [{vid}]: {oid} carries contract_id "
                                f"{cid} version {cver}")
            if v["status"] == "frozen":
                if pin is None:
                    findings.append(f"FROZEN WITHOUT PIN {unit} [{vid}]: {oid} carries no sha256")
                elif hashlib.sha256(line.encode("utf-8")).hexdigest() != pin:
                    findings.append(f"FROZEN RECORD EDITED {unit} [{vid}]: {oid} no longer matches its "
                                    f"pin — a frozen version is superseded by a later one, never rewritten")
        if v["extends"] is not None:
            parent = versions.get(v["extends"])
            if parent is None:
                findings.append(f"EXTENDS NOTHING {unit} [{vid}]: no version {v['extends']}")
            elif int(parent["version"]) + 1 != int(v["version"]):
                findings.append(f"VERSION GAP {unit} [{vid}]: version {v['version']} extends "
                                f"{parent['version']}")
        inherited, p = set(), v["extends"]
        ancestry = {vid}
        while p in versions:
            if p in ancestry:
                findings.append(f"EXTENDS CYCLE {unit} [{vid}]: revisits {p}")
                break
            ancestry.add(p)
            inherited |= {oid for oid, _ in versions[p]["members"]}
            p = versions[p]["extends"]
        own = {oid for oid, _ in v["members"]}
        for s in v["sups"]:
            if s["record"] not in inherited:
                findings.append(f"SUPERSEDES NOTHING {unit} [{vid}]: {s['record']} is not inherited")
            if s["by"] not in own:
                findings.append(f"SUPERSEDED BY A STRANGER {unit} [{vid}]: {s['by']} is not this "
                                f"version's member")
    for oid in sorted(set(obs) - set(owner)):
        findings.append(f"UNVERSIONED RECORD {unit}: {oid} belongs to no version in contract.sexp")
for f in findings:
    print("  " + f)
print(f"CONTRACT-FREEZE: {'FAIL' if findings else 'ok'} ({units} versioned unit(s), "
      f"{versions_seen} version(s), {len(findings)} finding(s))")
sys.exit(1 if findings else 0)
"#;

/// `judge <root>` run from `cwd` (the script's `cd "$t" && judge "$t"` in the controls, the root in the main run),
/// stdout and stderr together.
fn judge(cwd: &Path, root: &Path) -> (i32, String) {
    let mut command = Command::new("python3");
    command
        .arg("-")
        .arg(root)
        .current_dir(cwd)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());
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

/// `sed -i '0,/^PREFIX/s/FROM/TO/'`: the first occurrence replaced on every line up to and including the first line
/// that starts with the prefix.
fn sed_until(path: &Path, prefix: &str, from: &str, to: &str) {
    let text = fs::read_to_string(path).unwrap_or_default();
    let mut out = String::with_capacity(text.len());
    let mut in_range = true;
    for line in text.split_inclusive('\n') {
        if in_range {
            out.push_str(&line.replacen(from, to, 1));
            if line.starts_with(prefix) {
                in_range = false;
            }
        } else {
            out.push_str(line);
        }
    }
    let _ = fs::write(path, out);
}

/// `sed -i '/TEXT/d'`: every line containing the text removed.
fn sed_delete(path: &Path, text: &str) {
    let content = fs::read_to_string(path).unwrap_or_default();
    let out: String = content
        .split_inclusive('\n')
        .filter(|l| !l.contains(text))
        .collect();
    let _ = fs::write(path, out);
}

/// `sed -i 's/FROM/TO/'`: the first occurrence replaced on every line.
fn sed_all_lines(path: &Path, from: &str, to: &str) {
    let text = fs::read_to_string(path).unwrap_or_default();
    let out: String = text
        .split_inclusive('\n')
        .map(|l| l.replacen(from, to, 1))
        .collect();
    let _ = fs::write(path, out);
}

fn append(path: &Path, text: &str) {
    let mut bytes = fs::read(path).unwrap_or_default();
    bytes.extend_from_slice(text.as_bytes());
    let _ = fs::write(path, bytes);
}

struct Tally {
    pass: u32,
    fail: u32,
    verbose: bool,
}

impl Tally {
    /// One arm: the run's exit status must be `expected` and its output must contain `want`.
    fn arm(&mut self, name: &str, rc: i32, expected: i32, out: &str, want: &str) {
        if rc == expected && out.contains(want) {
            self.pass += 1;
        } else {
            self.fail += 1;
            if self.verbose {
                eprintln!("CONTRACT-FREEZE self-test MISS: {name} — expected rc={expected} (reason: {want}), got rc={rc}\n{out}");
            }
        }
    }
}

/// The RED/GREEN controls over the real contract and its rendered catalogue, then the ancestry probe plain and optimized.
fn self_test(repo: &Path, verbose: bool) -> bool {
    let Ok(t) = scratch(repo, "target/doctrine-selftest", "contractfreeze") else {
        eprintln!("CONTRACT-FREEZE self-test: cannot create a scratch directory under target/doctrine-selftest");
        return false;
    };
    let u = t.join("profiles/u");
    let fresh = || {
        let _ = fs::remove_dir_all(t.join("profiles"));
        let _ = fs::create_dir_all(&u);
        let _ = fs::copy(
            repo.join("profiles/rv64gc-lab-v0/contract.sexp"),
            u.join("contract.sexp"),
        );
        let rendered = Command::new("python3")
            .args([
                "scripts/record_catalog.py",
                "profiles/rv64gc-lab-v0/contract-obligations.sexp",
                "--stdout",
            ])
            .current_dir(repo)
            .stdin(Stdio::null())
            .stderr(Stdio::inherit())
            .output()
            .map(|o| o.stdout)
            .unwrap_or_default();
        let _ = fs::write(u.join("contract-obligations.sexp"), rendered);
        let _ = fs::remove_file(t.join("scripts"));
        #[cfg(unix)]
        let _ = std::os::unix::fs::symlink(repo.join("scripts"), t.join("scripts"));
    };
    let mut tally = Tally {
        pass: 0,
        fail: 0,
        verbose,
    };
    fresh();
    let (rc, out) = judge(&t, &t);
    tally.arm(
        "GREEN the real contract and its records agree",
        rc,
        0,
        captured(&out),
        "0 finding(s)",
    );
    fresh();
    sed_until(
        &u.join("contract-obligations.sexp"),
        "(obligation (id \"OB-SV39\")",
        "selects the minimal",
        "selects the MINIMAL",
    );
    let (rc, out) = judge(&t, &t);
    tally.arm(
        "RED an edited frozen record is refused",
        rc,
        1,
        captured(&out),
        "FROZEN RECORD EDITED",
    );
    fresh();
    sed_delete(&u.join("contract.sexp"), "(member (id \"OB-SVADE\")");
    let (rc, out) = judge(&t, &t);
    tally.arm(
        "RED a record dropped from every version is refused",
        rc,
        1,
        captured(&out),
        "UNVERSIONED RECORD",
    );
    fresh();
    sed_all_lines(
        &u.join("contract.sexp"),
        "(member (id \"OB-SVADE\")",
        "(member (id \"OB-NOWHERE\")",
    );
    let (rc, out) = judge(&t, &t);
    tally.arm(
        "RED a member naming no record is refused",
        rc,
        1,
        captured(&out),
        "MEMBER WITHOUT RECORD",
    );
    fresh();
    sed_until(
        &u.join("contract-obligations.sexp"),
        "(obligation (id \"OB-SV39\")",
        "(contract_version \"0\")",
        "(contract_version \"1\")",
    );
    let (rc, out) = judge(&t, &t);
    tally.arm(
        "RED a member of another version is refused",
        rc,
        1,
        captured(&out),
        "MEMBER OF ANOTHER VERSION",
    );
    fresh();
    append(&u.join("contract.sexp"), "(contract (id \"rv64gc-lab-env-v1\") (version \"1\") (profile_ids \"u\") (extends \"rv64gc-lab-env-v7\") (status open) (statement \"x\") (member (id \"OB-X\")) (supersede (record \"OB-NOT-INHERITED\") (by \"OB-X\") (why \"y\")))\n");
    append(
        &u.join("contract-obligations.sexp"),
        "(obligation (id \"OB-X\") (contract_id \"rv64gc-lab-env-v1\") (contract_version \"1\"))\n",
    );
    let (rc, out) = judge(&t, &t);
    let out = captured(&out).to_owned();
    tally.arm(
        "RED an extension of no version is refused",
        rc,
        1,
        &out,
        "EXTENDS NOTHING",
    );
    tally.arm(
        "RED a supersession of a record not inherited is refused",
        rc,
        1,
        &out,
        "SUPERSEDES NOTHING",
    );
    for mode in ["normal", "optimized"] {
        let probe = |mutation: Option<&str>| {
            let mut command = Command::new("python3");
            if mode == "optimized" {
                command.arg("-O");
            }
            command.arg("scripts/probe_contract_ancestry.py");
            if let Some(m) = mutation {
                command.args(["--mutation", m]);
            }
            combined(command.current_dir(repo))
        };
        let (rc, out) = probe(None);
        tally.arm(
            &format!("GREEN bounded real contract ancestry {mode}"),
            rc,
            0,
            captured(&out),
            "CONTRACT-ANCESTRY: 4 tests / 0 failures / 0 errors; finite contract owners, no capture credit",
        );
        for mutation in ["freeze-cycle", "scope-cycle"] {
            let (rc, out) = probe(Some(mutation));
            tally.arm(
                &format!("RED omitted contract ancestry {mutation} {mode}"),
                rc,
                1,
                captured(&out),
                "CONTRACT-ANCESTRY: 4 tests / 3 failures / 0 errors; finite contract owners, no capture credit",
            );
        }
    }
    let _ = fs::remove_dir_all(&t);
    if verbose {
        println!(
            "CONTRACT-FREEZE --self-test: {} pass / {} fail",
            tally.pass, tally.fail
        );
    }
    tally.fail == 0
}

/// `cargo xtask check-contract-freeze [--self-test]`: the shell driver's verdict lines and exit statuses.
pub fn run(root: &Path, args: &[String]) -> ExitCode {
    if args.first().is_some_and(|arg| arg == "--self-test") {
        return if self_test(root, true) {
            ExitCode::SUCCESS
        } else {
            ExitCode::from(1)
        };
    }
    // Judge FIRST: a finding is a verdict on its own; only a PASS needs the controls' proof.
    let (rc, out) = judge(root, root);
    let out = captured(&out);
    if rc != 0 {
        eprintln!("{out}");
        return ExitCode::from(1);
    }
    if !self_test(root, false) {
        eprintln!("CONTRACT-FREEZE: REFUSED — the check does not discriminate (self-test failed).");
        return ExitCode::from(2);
    }
    println!("{out}");
    ExitCode::SUCCESS
}
