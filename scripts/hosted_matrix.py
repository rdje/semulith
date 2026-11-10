#!/usr/bin/env python3
"""Record the hosted two-host portability run as evidence the tree can re-read.

`docs/EVIDENCE_AND_GATES.md` §7 asks G-PORTABILITY for NATIVE x86-64 and AArch64 fixtures that agree.
The development host is arm64 and reaches x86-64 only through Rosetta 2's translation, so the native
x86-64 leg lives in the hosted `portability` workflow (`decision_release-route-x86-64-leg`): an
x86-64 runner and an arm64 runner each run `cargo test --all` and emit the digest manifest over the
unit's guests, a third job requires the two manifests byte-identical, and a fourth runs the pinned
Miri plan natively and on big-endian powerpc64.

The service keeps a run's logs and artifacts for a limited time. This tool freezes what one run
showed into `profiles/<unit>/hosted-matrix.sexp`, from the run's own files and never from a typed
number, and ties it to the tree: the run's commit and this tree hold the same engine, definitions
and guests, and both hosts reproduce the digest this host recorded. `gate.sexp` then names the
record with what it covers, so it stops being evidence when any of that moves
(`decision_recorded-evidence-states-what-it-covers`).

Usage:
  hosted_matrix.py --fetch RUN --out DIR         download the run's description, job logs and artifacts
                                                 through `gh` (the only step that needs the network);
                                                 DIR is new and under target/
  hosted_matrix.py --verify DIR --profile UNIT   judge a fetched run for one unit: exit 0 passed, 1 refused
  hosted_matrix.py --record DIR --profile UNIT   verify, tie the run to this tree, write the record and
                                                 print the gate.sexp row that names it
  hosted_matrix.py --self-test                   judge synthetic runs: complete ones pass, and each
                                                 refusal fires for its own reason
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = "portability"
# The unit's guest source, as scripts/check_portability.sh spells it (a self-test arm holds the two equal).
UNITS = {
    "rv64i-lab-v0": "crates/semulith-verify/src/guests.rs",
    "rv64gc-lab-v0": "crates/semulith-verify/src/guests_rv64gc.rs",
}
ENGINE = ("crates/semulith-core/src", "definitions")
X86_64 = ("x86_64",)
AARCH64 = ("arm64", "aarch64")
RUN_FIELDS = "databaseId,workflowName,event,headBranch,headSha,conclusion,status,createdAt,updatedAt,jobs"


class Refused(Exception):
    """The run, or its tie to the tree, does not support the record."""


def covered_paths(unit: str) -> tuple[str, ...]:
    return ENGINE + (UNITS[unit],)


# ---------------------------------------------------------------------------
# Reading one fetched run
# ---------------------------------------------------------------------------

def said(log: str) -> list[str]:
    """What a job printed, one entry per line, without the service's job, step and timestamp columns.

    A line the runner echoes from the workflow's script carries terminal colour codes, so it never
    equals the plain line the script itself prints: `echo "native: green"` is not `native: green`."""
    out = []
    for line in log.replace("﻿", "").splitlines():
        text = line.split("\t", 2)[-1]
        out.append(re.sub(r"^\d{4}-\d\d-\d\dT[\d:.]+Z ?", "", text))
    return out


def test_totals(log: str) -> tuple[int, int, int]:
    """(suites, tests passed, tests failed) over every `test result:` line; a suite that is not `ok` counts as failed."""
    rows = re.findall(r"test result: (\w+)\. (\d+) passed; (\d+) failed", log)
    failed = sum(int(f) for _, _, f in rows) + sum(1 for word, _, f in rows if word != "ok" and f == "0")
    return len(rows), sum(int(p) for _, p, _ in rows), failed


def read_manifest(path: Path) -> tuple[str, list[str], bytes]:
    """(digest, guest names, bytes) of one emitted manifest, the digest recomputed from its own lines."""
    data = path.read_bytes()
    lines = data.decode("utf-8").splitlines()
    if not lines:
        raise Refused(f"{path.parent.name}: the manifest is empty")
    stated = re.fullmatch(r"manifest sha256: ([0-9a-f]{64})  \((\d+) guests\)", lines[-1])
    rows = [re.fullmatch(r"([0-9a-f]{64})  ([a-z0-9-]+)", line) for line in lines[:-1]]
    if stated is None or not rows or any(r is None for r in rows):
        raise Refused(f"{path.parent.name}: not a digest manifest")
    names = [r.group(2) for r in rows]
    if names != sorted(set(names)):
        raise Refused(f"{path.parent.name}: the guests are not each named once, in order")
    digest = hashlib.sha256("".join(r.group(1) for r in rows).encode()).hexdigest()
    if digest != stated.group(1) or int(stated.group(2)) != len(names):
        raise Refused(f"{path.parent.name}: the manifest states {stated.group(1)[:12]} over {stated.group(2)} guests, "
                      f"and its lines give {digest[:12]} over {len(names)}")
    return digest, names, data


def verify(run_dir: Path, unit: str) -> dict:
    """The facts of one fetched run for one unit; raises `Refused` naming the first thing that does not hold."""
    if unit not in UNITS:
        raise Refused(f"unknown unit {unit} ({' | '.join(UNITS)})")
    try:
        run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise Refused(f"no readable run description: {e}") from e
    if run.get("workflowName") != WORKFLOW:
        raise Refused(f"the run is of workflow `{run.get('workflowName')}`, not `{WORKFLOW}`")
    if (run.get("status"), run.get("conclusion")) != ("completed", "success"):
        raise Refused(f"the run reads {run.get('status')}/{run.get('conclusion')}, not completed/success")
    head = str(run.get("headSha", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise Refused("the run names no commit")
    jobs = {j["name"]: j for j in run.get("jobs", [])}

    def job_log(name: str) -> list[str]:
        job = jobs.get(name)
        if job is None:
            raise Refused(f"the run has no `{name}` job")
        if job.get("conclusion") != "success":
            raise Refused(f"the `{name}` job concluded {job.get('conclusion')}")
        path = run_dir / "jobs" / f"{job['databaseId']}.log"
        if not path.is_file():
            raise Refused(f"the `{name}` job's log was not fetched")
        return said(path.read_text(encoding="utf-8", errors="replace"))

    host_jobs = sorted(n for n in jobs if re.fullmatch(rf"host \(\S+, {re.escape(unit)}\)", n))
    if len(host_jobs) != 2:
        raise Refused(f"{len(host_jobs)} host job(s) ran {unit}; the matrix is two hosts")
    hosts = []
    for name in host_jobs:
        runner = re.fullmatch(r"host \((\S+), \S+\)", name).group(1)
        lines = job_log(name)
        arch = next((m.group(1) for m in (re.fullmatch(r"== leg 1: native \((\w+)\) ==", l) for l in lines) if m), None)
        if arch is None:
            raise Refused(f"the `{name}` job names no native architecture")
        if "native: green" not in lines:
            raise Refused(f"the `{name}` job did not print `native: green`")
        log = run_dir / "artifacts" / f"portability-log-{runner}-{unit}" / "native.log"
        if not log.is_file():
            raise Refused(f"{runner}: the native test log was not uploaded")
        suites, passed, failed = test_totals(log.read_text(encoding="utf-8", errors="replace"))
        if failed or not passed:
            raise Refused(f"{runner}: {passed} test(s) passed and {failed} failed")
        manifest = run_dir / "artifacts" / f"manifest-{runner}-{unit}" / "manifest.txt"
        if not manifest.is_file():
            raise Refused(f"{runner}: the manifest was not uploaded")
        digest, names, data = read_manifest(manifest)
        rustc = next((m.group(1) for m in (re.fullmatch(r"\s*\S+ (?:installed|unchanged|updated) - (rustc .+)", l)
                                           for l in lines) if m), "unreported")
        image = next((m.group(1) for m in (re.fullmatch(r"Image: (\S+)", l) for l in lines) if m), "unreported")
        hosts.append({"runner": runner, "arch": arch, "image": image, "rustc": rustc, "suites": suites,
                      "passed": passed, "digest": digest, "names": names, "bytes": data})
    a, b = hosts
    if not (any(h["arch"] in X86_64 for h in hosts) and any(h["arch"] in AARCH64 for h in hosts)):
        raise Refused(f"the hosts are {a['arch']} and {b['arch']}; the gate needs native x86-64 and AArch64")
    if a["bytes"] != b["bytes"]:
        differing = sorted(set(a["names"]) ^ set(b["names"])) or [
            n for n, x, y in zip(a["names"], a["bytes"].splitlines(), b["bytes"].splitlines()) if x != y]
        raise Refused(f"the two hosts' manifests differ ({a['digest'][:12]} and {b['digest'][:12]}), "
                      f"first at guest {differing[0] if differing else '?'}")
    if a["passed"] != b["passed"]:
        raise Refused(f"the hosts ran different tests: {a['passed']} and {b['passed']} passed")
    job_log("agree")
    miri_lines = job_log("miri")
    legs = {}
    for leg, file in (("miri", "miri.log"), ("cross-endian", "cross.log")):
        if f"{leg}: green" not in miri_lines:
            raise Refused(f"the `miri` job did not print `{leg}: green`")
        log = run_dir / "artifacts" / "miri-logs" / file
        if not log.is_file():
            raise Refused(f"the {leg} test log was not uploaded")
        _, passed, failed = test_totals(log.read_text(encoding="utf-8", errors="replace"))
        if failed or not passed:
            raise Refused(f"{leg}: {passed} test(s) passed and {failed} failed")
        legs[leg] = passed
    return {"unit": unit, "run": str(run.get("databaseId", "")), "event": str(run.get("event", "")), "head": head,
            "completed": str(run.get("updatedAt", "")), "hosts": [{k: v for k, v in h.items() if k != "bytes"} for h in hosts],
            "digest": a["digest"], "names": a["names"], "legs": legs}


# ---------------------------------------------------------------------------
# Tying a verified run to this tree
# ---------------------------------------------------------------------------

def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    """git in `root`, an absolute existing directory: `git -C ""` acts on the caller's repository, `Path("")` is the
    current directory, and a hook's GIT_* variables would redirect it too."""
    if not root.is_absolute() or not root.is_dir():
        raise Refused(f"no such repository: {root!s}")
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, env=env)


def tie_tree(root: Path, head: str, paths: tuple[str, ...]) -> None:
    """The run's commit is here, and the tree holds what that commit held on every covered path."""
    if _git(root, "cat-file", "-e", f"{head}^{{commit}}").returncode != 0:
        raise Refused(f"the run's commit {head[:12]} is not in this repository")
    moved = _git(root, "diff", "--name-only", head, "--", *paths)
    if moved.returncode != 0:
        raise Refused(f"cannot compare with the run's commit: {moved.stderr.strip()}")
    if moved.stdout.split():
        raise Refused(f"the run measured another tree: {moved.stdout.split()[0]} moved since {head[:12]}")


def local_manifest(text: str) -> tuple[str, int]:
    """(digest, guests) of the fixture-digest-manifest leg a unit's portability.sexp records."""
    m = re.search(r'\(leg \(id "fixture-digest-manifest"\).*?\(evidence "sha256 ([0-9a-f]{64}) over the (\d+) tracked guests',
                  text, re.S)
    if m is None:
        raise Refused("this host's portability record states no manifest digest")
    return m.group(1), int(m.group(2))


def tie_records(facts: dict, portability: str, guests_source: str) -> None:
    """Both hosts reproduce the digest this host recorded, over exactly the guests the tree tracks."""
    digest, count = local_manifest(portability)
    if (digest, count) != (facts["digest"], len(facts["names"])):
        raise Refused(f"this host recorded {digest[:12]} over {count} guests; the hosted hosts give "
                      f"{facts['digest'][:12]} over {len(facts['names'])}")
    tracked = sorted(set(re.findall(r'name: "([a-z0-9-]+)"', guests_source)))
    if tracked != facts["names"]:
        odd = sorted(set(tracked) ^ set(facts["names"]))
        raise Refused(f"the tree tracks {len(tracked)} guests and the manifest names {len(facts['names'])}: {odd[0]}")


# ---------------------------------------------------------------------------
# The record, and the row that names it
# ---------------------------------------------------------------------------

def q(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def render(facts: dict, recorded: str) -> str:
    unit, run = facts["unit"], facts["run"]
    hosts = "\n".join(
        f'    (host (runner "{q(h["runner"])}") (arch "{q(h["arch"])}") (image "{q(h["image"])}") (rustc "{q(h["rustc"])}")\n'
        f'          (tests "{h["passed"]} passed, 0 failed, in {h["suites"]} suites")\n'
        f'          (manifest "sha256 {h["digest"]} over {len(h["names"])} guests"))' for h in facts["hosts"])
    return f""";; hosted-matrix.sexp — the recorded hosted run of {unit}'s portability matrix: G-PORTABILITY's native
;; x86-64 and arm64 legs, on the service's own hardware. Frozen from one run's description, job logs and
;; artifacts by `scripts/hosted_matrix.py --record`, never typed. The service keeps those files for a
;; limited time; this record is what stays. `gate.sexp` names it with what it covers.
;; Re-derive, while the service still holds the run:
;;   python3 -B scripts/hosted_matrix.py --fetch {run} --out target/hosted-matrix/{run}
;;   python3 -B scripts/hosted_matrix.py --verify target/hosted-matrix/{run} --profile {unit}

(hosted-matrix
  (for-gate G-PORTABILITY)
  (unit "{unit}")
  (recorded "{recorded}")
  (recorded-by "scripts/hosted_matrix.py --record DIR --profile {unit}")
  (run (id "{run}") (workflow "{WORKFLOW}") (event "{q(facts["event"])}") (head "{facts["head"]}") (completed "{q(facts["completed"])}"))
  (verdict "passed")
  (hosts
{hosts})
  (agreement "the two hosts' manifests are byte-identical, and equal the digest profiles/{unit}/portability.sexp records over the same guests")
  (miri (verdict "green") (tests "{facts["legs"]["miri"]} passed, 0 failed"))
  (cross-endian (verdict "green") (tests "{facts["legs"]["cross-endian"]} passed, 0 failed")))
"""


def gate_row(facts: dict) -> str:
    sys.path.insert(0, str(ROOT / "scripts"))
    import gate_report                                   # the one definition of what a row covers
    unit = facts["unit"]
    tracked = gate_report._tracked()
    covers = "\n".join(f'  (covers (path "{p}") (sha256 "{gate_report._covered_digest(p, tracked)}"))'
                       for p in covered_paths(unit))
    x86 = next(h for h in facts["hosts"] if h["arch"] in X86_64)
    arm = next(h for h in facts["hosts"] if h["arch"] in AARCH64)
    return (f'(evidence (axis G-PORTABILITY) (kind x86-64) (record "profiles/{unit}/hosted-matrix.sexp")\n{covers}\n'
            f'  (statement "The hosted portability run {facts["run"]} on commit {facts["head"][:12]}: `cargo test --all` natively on '
            f'{x86["runner"]} ({x86["arch"]}) and {arm["runner"]} ({arm["arch"]}), {x86["passed"]} tests passed on each, and the digest '
            f'manifest over the unit\'s {len(facts["names"])} guests byte-identical on both and equal to this host\'s record; Miri and '
            f'big-endian powerpc64 green in the same run. Frozen from the run\'s own files by scripts/hosted_matrix.py --record."))')


# ---------------------------------------------------------------------------
# The acts
# ---------------------------------------------------------------------------

def fetch(run: str, out: Path) -> Path:
    if not re.fullmatch(r"\d+", run):
        raise Refused(f"not a run id: {run}")
    out = out if out.is_absolute() else ROOT / out
    target = (ROOT / "target").resolve()
    if target not in out.resolve().parents:
        raise Refused(f"{out} is not under target/: fetched files stay on the repository's volume, untracked")
    if out.exists():
        raise Refused(f"{out} exists: a fetch writes a new directory")

    def gh(*args: str) -> str:
        done = subprocess.run(["gh", *args], capture_output=True, text=True, cwd=ROOT)
        if done.returncode != 0:
            raise Refused(f"gh {' '.join(args[:3])} failed: {done.stderr.strip()[:300]}")
        return done.stdout

    description = gh("run", "view", run, "--json", RUN_FIELDS)
    (out / "jobs").mkdir(parents=True)
    (out / "run.json").write_text(description, encoding="utf-8")
    for job in json.loads(description).get("jobs", []):
        (out / "jobs" / f"{job['databaseId']}.log").write_text(
            gh("run", "view", run, "--log", "--job", str(job["databaseId"])), encoding="utf-8")
    gh("run", "download", run, "--dir", str(out / "artifacts"))
    return out


def summary(facts: dict) -> str:
    hosts = " and ".join(f"{h['runner']} ({h['arch']})" for h in facts["hosts"])
    return (f"run {facts['run']} on {facts['head'][:12]}: {hosts} agree on {facts['digest'][:12]} over "
            f"{len(facts['names'])} guests, {facts['hosts'][0]['passed']} tests each; miri {facts['legs']['miri']}, "
            f"cross-endian {facts['legs']['cross-endian']}")


def record(run_dir: Path, unit: str) -> None:
    facts = verify(run_dir, unit)
    tie_tree(ROOT, facts["head"], covered_paths(unit))
    tie_records(facts, (ROOT / "profiles" / unit / "portability.sexp").read_text(encoding="utf-8"),
                (ROOT / UNITS[unit]).read_text(encoding="utf-8"))
    path = ROOT / "profiles" / unit / "hosted-matrix.sexp"
    path.write_text(render(facts, datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")), encoding="utf-8")
    print(f"hosted_matrix: recorded {summary(facts)}")
    print(f"hosted_matrix: wrote {path.relative_to(ROOT)}; the row for profiles/{unit}/gate.sexp:")
    print(gate_row(facts))


# ---------------------------------------------------------------------------
# Controls
# ---------------------------------------------------------------------------

def _selftest() -> int:
    base = ROOT / "target" / "doctrine-selftest"
    base.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="hosted-matrix.", dir=base))
    unit = "rv64gc-lab-v0"
    ok_log = "running 2 tests\ntest result: ok. 2 passed; 0 failed; 0 ignored\ntest result: ok. 3 passed; 0 failed; 0 ignored\n"
    passed, missed, ran = 0, [], 0

    def manifest(rows: dict[str, str]) -> str:
        lines = [f"{hashlib.sha256(v.encode()).hexdigest()}  {k}" for k, v in sorted(rows.items())]
        digest = hashlib.sha256("".join(l.split()[0] for l in lines).encode()).hexdigest()
        return "\n".join(lines + [f"manifest sha256: {digest}  ({len(rows)} guests)"]) + "\n"

    def stamp(job: str, lines: list[str]) -> str:
        return "".join(f"{job}\tUNKNOWN STEP\t2026-01-01T00:00:00.0000000Z {l}\n" for l in lines)

    def make(name: str, edit=None) -> Path:
        """A complete synthetic run; `edit(spec)` damages exactly one thing before it is written."""
        guests = {"a-one": "x", "b-two": "y", "c-three": "z"}
        spec = {
            "run": {"databaseId": 7, "workflowName": WORKFLOW, "event": "push", "headSha": "a" * 40,
                    "status": "completed", "conclusion": "success", "updatedAt": "2026-01-01T01:00:00Z"},
            "jobs": {
                f"host (ubuntu-latest, {unit})": ["success", ["Image: ubuntu-24.04", "  stable-x86_64-unknown-linux-gnu installed - rustc 1.0.0 (0 2026-01-01)",
                                                             "== leg 1: native (x86_64) ==", "native: green"]],
                f"host (macos-latest, {unit})": ["success", ["Image: macos-26-arm64", "== leg 1: native (arm64) ==", "native: green"]],
                "host (ubuntu-latest, rv64i-lab-v0)": ["success", ["== leg 1: native (x86_64) ==", "native: green"]],
                "miri": ["success", ["miri: green", "cross-endian: green"]],
                "agree": ["success", ["portability matrix: agreed"]],
            },
            "files": {
                f"manifest-ubuntu-latest-{unit}/manifest.txt": manifest(guests),
                f"manifest-macos-latest-{unit}/manifest.txt": manifest(guests),
                f"portability-log-ubuntu-latest-{unit}/native.log": ok_log,
                f"portability-log-macos-latest-{unit}/native.log": ok_log,
                "miri-logs/miri.log": ok_log, "miri-logs/cross.log": ok_log,
            },
            "guests": guests, "manifest": manifest,
        }
        if edit:
            edit(spec)
        d = tmp / name
        (d / "jobs").mkdir(parents=True)
        jobs = []
        for i, (job, (conclusion, lines)) in enumerate(spec["jobs"].items(), start=100):
            jobs.append({"name": job, "conclusion": conclusion, "databaseId": i})
            (d / "jobs" / f"{i}.log").write_text(stamp(job, lines), encoding="utf-8")
        (d / "run.json").write_text(json.dumps({**spec["run"], "jobs": jobs}), encoding="utf-8")
        for rel, text in spec["files"].items():
            (d / "artifacts" / rel).parent.mkdir(parents=True, exist_ok=True)
            (d / "artifacts" / rel).write_text(text, encoding="utf-8")
        return d

    def arm(label, fn):
        nonlocal passed, ran
        ran += 1
        try:
            fn()
            passed += 1
        except Exception as e:                           # noqa: BLE001 — every miss is reported
            missed.append(f"{label}: {type(e).__name__}: {e}")

    def refuses(fn, needle: str):
        try:
            fn()
        except Refused as e:
            assert needle in str(e), f"refused for another reason: {e}"
            return
        raise AssertionError("accepted")

    def red(label: str, needle: str, edit):
        arm(f"RED {label}", lambda: refuses(lambda: verify(make(f"red{ran}", edit), unit), needle))

    def green():
        facts = verify(make("green"), unit)
        assert (len(facts["names"]), facts["hosts"][0]["passed"], facts["legs"]) == (3, 5, {"miri": 5, "cross-endian": 5}), facts
        assert sorted(h["arch"] for h in facts["hosts"]) == ["arm64", "x86_64"], facts["hosts"]
        assert facts["hosts"][1]["rustc"] == "rustc 1.0.0 (0 2026-01-01)" and facts["hosts"][0]["rustc"] == "unreported", facts["hosts"]

    mac, ubu = f"host (macos-latest, {unit})", f"host (ubuntu-latest, {unit})"
    try:
        arm("GREEN a complete run passes, and its facts are the run's", green)
        red("the two hosts' manifests differ by one guest", "manifests differ", lambda s: s["files"].__setitem__(
            f"manifest-macos-latest-{unit}/manifest.txt", s["manifest"]({**s["guests"], "b-two": "other"})))
        red("a manifest states a digest its lines do not give", "its lines give", lambda s: s["files"].__setitem__(
            f"manifest-ubuntu-latest-{unit}/manifest.txt",
            re.sub(r"manifest sha256: [0-9a-f]{64}", "manifest sha256: " + "0" * 64, s["manifest"](s["guests"]))))
        red("a manifest names a guest twice", "named once", lambda s: s["files"].__setitem__(
            f"manifest-ubuntu-latest-{unit}/manifest.txt", s["manifest"](s["guests"]).replace("b-two", "a-one")))
        red("a host uploaded no manifest", "manifest was not uploaded",
            lambda s: s["files"].pop(f"manifest-macos-latest-{unit}/manifest.txt"))
        red("both hosts are arm64: no native x86-64", "needs native x86-64",
            lambda s: s["jobs"][ubu][1].__setitem__(2, "== leg 1: native (arm64) =="))
        red("a host job failed", "concluded failure", lambda s: s["jobs"][mac].__setitem__(0, "failure"))
        red("a host only echoed its script's `native: green`", "did not print `native: green`",
            lambda s: s["jobs"][mac][1].__setitem__(2, '\x1b[36;1mecho "native: green"\x1b[0m'))
        red("a test failed on one host", "1 failed", lambda s: s["files"].__setitem__(
            f"portability-log-macos-latest-{unit}/native.log", ok_log + "test result: FAILED. 4 passed; 1 failed; 0 ignored\n"))
        red("the hosts ran different numbers of tests", "different tests", lambda s: s["files"].__setitem__(
            f"portability-log-macos-latest-{unit}/native.log", ok_log + "test result: ok. 1 passed; 0 failed; 0 ignored\n"))
        red("only one host ran the unit", "the matrix is two hosts", lambda s: s["jobs"].pop(mac))
        red("the big-endian leg did not report green", "`cross-endian: green`",
            lambda s: s["jobs"]["miri"][1].remove("cross-endian: green"))
        red("a Miri test failed", "miri: 5 test(s) passed and 2 failed", lambda s: s["files"].__setitem__(
            "miri-logs/miri.log", ok_log + "test result: FAILED. 0 passed; 2 failed; 0 ignored\n"))
        red("the agreement job is absent", "no `agree` job", lambda s: s["jobs"].pop("agree"))
        red("the run did not succeed", "not completed/success", lambda s: s["run"].__setitem__("conclusion", "failure"))
        red("the run is of another workflow", "not `portability`", lambda s: s["run"].__setitem__("workflowName", "rust"))
        red("the run names no commit", "names no commit", lambda s: s["run"].__setitem__("headSha", "main"))
        red("a manifest is empty", "the manifest is empty",
            lambda s: s["files"].__setitem__(f"manifest-ubuntu-latest-{unit}/manifest.txt", ""))
        red("a manifest is some other file", "not a digest manifest",
            lambda s: s["files"].__setitem__(f"manifest-ubuntu-latest-{unit}/manifest.txt", "404: Not Found\n"))
        red("a host job names no native architecture", "names no native architecture",
            lambda s: s["jobs"][ubu][1].remove("== leg 1: native (x86_64) =="))
        red("a host uploaded no test log", "native test log was not uploaded",
            lambda s: s["files"].pop(f"portability-log-ubuntu-latest-{unit}/native.log"))
        red("the big-endian test log was not uploaded", "cross-endian test log was not uploaded",
            lambda s: s["files"].pop("miri-logs/cross.log"))

        def unfetched():
            d = make("unfetched")
            next(f for f in (d / "jobs").iterdir() if "miri: green" in f.read_text()).unlink()
            refuses(lambda: verify(d, unit), "`miri` job's log was not fetched")
        arm("RED a job's log was not fetched", unfetched)
        arm("RED an unknown unit is refused", lambda: refuses(lambda: verify(make("unknown-unit"), "rv32-lab-v9"), "unknown unit rv32-lab-v9"))

        facts = verify(make("ties"), unit)
        source = "".join(f'Guest {{ name: "{n}", }}\n' for n in facts["names"])
        local = f'(leg (id "fixture-digest-manifest") (verdict "green")\n (evidence "sha256 {facts["digest"]} over the 3 tracked guests\' demo outputs"))'
        arm("GREEN the hosted digest is this host's, over the tracked guests", lambda: tie_records(facts, local, source))
        arm("RED this host recorded another digest", lambda: refuses(
            lambda: tie_records(facts, local.replace(facts["digest"], "f" * 64), source), "this host recorded ffffffffffff"))
        arm("RED the tree tracks a guest the run never saw", lambda: refuses(
            lambda: tie_records(facts, local, source + 'Guest { name: "d-four", }\n'), "tracks 4 guests and the manifest names 3: d-four"))
        arm("RED this host's record states no digest", lambda: refuses(
            lambda: tie_records(facts, '(leg (id "native-arm64"))', source), "states no manifest digest"))

        repo = tmp / "repo"
        (repo / "engine").mkdir(parents=True)
        (repo / "engine" / "core.rs").write_text("one\n")
        (repo / "notes.md").write_text("one\n")
        for args in (("init", "-q"), ("add", "-A"),
                     ("-c", "user.name=t", "-c", "user.email=t@invalid", "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", "one")):
            done = _git(repo, *args)
            assert done.returncode == 0, done.stderr
        head = _git(repo, "rev-parse", "HEAD").stdout.strip()
        assert _git(repo, "rev-parse", "--show-toplevel").stdout.strip() == str(repo.resolve()), "the scratch repository is not its own"
        (repo / "notes.md").write_text("two\n")
        arm("GREEN a tree that moved only outside the covered paths is the run's tree", lambda: tie_tree(repo, head, ("engine",)))
        arm("RED the run's commit is not in the repository", lambda: refuses(
            lambda: tie_tree(repo, "b" * 40, ("engine",)), "is not in this repository"))
        (repo / "engine" / "core.rs").write_text("two\n")
        arm("RED a covered path moved since the run's commit", lambda: refuses(
            lambda: tie_tree(repo, head, ("engine",)), "another tree: engine/core.rs moved"))
        arm("RED an empty repository path is refused, never run in the caller's", lambda: refuses(
            lambda: _git(Path(""), "status"), "no such repository"))
        arm("RED a comparison git cannot make refuses, and is never read as nothing moved", lambda: refuses(
            lambda: tie_tree(repo, head, ("../outside",)), "cannot compare with the run's commit"))

        # --fetch, with a stub `gh` serving a synthetic run: the self-test never reaches the network.
        served, stub = make("served"), tmp / "bin"
        stub.mkdir()
        (stub / "gh").write_text(
            '#!/bin/sh\n[ -n "$HOSTED_MATRIX_STUB_FAIL" ] && { echo "HTTP 404: Not Found" >&2; exit 1; }\n'
            'case "$1 $2 $4" in\n'
            '  "run view --json") cat "$HOSTED_MATRIX_STUB_RUN/run.json";;\n'
            '  "run view --log") cat "$HOSTED_MATRIX_STUB_RUN/jobs/$6.log";;\n'
            '  "run download --dir") cp -R "$HOSTED_MATRIX_STUB_RUN/artifacts" "$5";;\n'
            '  *) echo "stub gh: unexpected $*" >&2; exit 2;;\nesac\n', encoding="utf-8")
        (stub / "gh").chmod(0o755)
        saved = {k: os.environ.get(k) for k in ("PATH", "HOSTED_MATRIX_STUB_RUN", "HOSTED_MATRIX_STUB_FAIL")}
        os.environ.update(PATH=f"{stub}{os.pathsep}{saved['PATH']}", HOSTED_MATRIX_STUB_RUN=str(served))
        try:
            def fetched():
                fetch("7", tmp / "fetched")
                assert verify(tmp / "fetched", unit)["digest"] == facts["digest"], "the fetched run is not the served one"
            arm("GREEN a fetched run is laid out as the judge reads it", fetched)
            arm("RED a fetch into an existing directory is refused", lambda: refuses(lambda: fetch("7", tmp / "fetched"), "exists: a fetch writes a new directory"))
            arm("RED a fetch outside target/ is refused", lambda: refuses(lambda: fetch("7", ROOT / "docs" / "hosted-run"), "is not under target/"))
            arm("RED a run id that is not a number is refused", lambda: refuses(lambda: fetch("7; rm", tmp / "x"), "not a run id"))

            def service_fails():
                os.environ["HOSTED_MATRIX_STUB_FAIL"] = "1"
                refuses(lambda: fetch("7", tmp / "failed"), "gh run view 7 failed: HTTP 404")
                assert not (tmp / "failed").exists(), "a failed fetch left a directory"
            arm("RED a service failure refuses and leaves nothing", service_fails)
        finally:
            for k, v in saved.items():
                os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)

        def reads_back():
            text = render(facts, "2026-01-01")
            assert re.search(r'\(verdict "([a-z]+)"\)', text).group(1) == "passed", "the first verdict a reader meets is not the record's"
            assert text.count('(arch "x86_64")') == 1 and f'(head "{"a" * 40}")' in text and '"5 passed, 0 failed, in 2 suites"' in text
        arm("the record's first verdict is its own, and it names the run", reads_back)

        def units_agree():
            script = (ROOT / "scripts" / "check_portability.sh").read_text(encoding="utf-8")
            assert dict(re.findall(r'^\s*([a-z0-9-]+)\)\s+GUESTS_RS="([^"]+)"', script, re.M)) == UNITS, "the unit table left check_portability.sh's"
        arm("the units and their guest sources are check_portability.sh's", units_agree)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for m in missed:
        print(f"hosted_matrix --self-test MISS: {m}", file=sys.stderr)
    want = 40
    if ran != want:
        print(f"hosted_matrix --self-test HARNESS: {ran} arm(s) ran, {want} declared", file=sys.stderr)
        return 2
    print(f"hosted_matrix --self-test: {passed} pass / {ran - passed} fail")
    return 0 if passed == ran else 1


def main(argv: list[str]) -> int:
    args = argv[1:]
    try:
        if args == ["--self-test"]:
            return _selftest()
        if len(args) == 4 and args[0] == "--fetch" and args[2] == "--out":
            print(f"hosted_matrix: fetched run {args[1]} into {fetch(args[1], Path(args[3])).relative_to(ROOT)}")
            return 0
        if len(args) == 4 and args[0] in ("--verify", "--record") and args[2] == "--profile":
            run_dir = Path(args[1]) if Path(args[1]).is_absolute() else ROOT / args[1]
            if args[0] == "--record":
                record(run_dir, args[3])
            else:
                print(f"hosted_matrix: passed — {summary(verify(run_dir, args[3]))}")
            return 0
    except Refused as e:
        print(f"hosted_matrix: REFUSED — {e}", file=sys.stderr)
        return 1
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
