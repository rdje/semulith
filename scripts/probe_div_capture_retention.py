#!/usr/bin/env python3
"""Copied capture-retention controls; synthetic processes, no Sail or qualification."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import capture_div as A
import probe_div_command as Command
import retain_div_capture as T

ROOT = Path(__file__).resolve().parent.parent
MUTATION = None
TOOL = "scripts/retain_div_capture.py"
COMMIT = "4af5a68bbec9f1bf0922ec3787f829e029c15f29"  # a 40-hex object id; recorded by the receipt, never verified
# Each seam replaces one load-bearing predicate in the copied tool; at least one control must then fail.
SEAMS = {
    "outputs-absent": ('    _require(not present, "outputs already exist; a capture is never rerun: " + ", ".join(present))\n',
                       '    _require(True, "outputs already exist")\n'),
    "declaration-regeneration": ('        _require(snapshot.pin.disposition == "matched" and snapshot.data == payload,\n',
                                 '        _require(True,\n'),
    "binary-identity": ('    _require(snapshot.pin.disposition == "matched",\n             "reference binary differs from the retained identity: " + snapshot.pin.reason)\n',
                        '    _require(True, "reference binary differs")\n'),
    "object-id": ("OBJECT_ID.fullmatch(declaration_commit) is not None", "True"),
    "exclusive-publish": ("os.O_WRONLY | os.O_CREAT | os.O_EXCL", "os.O_WRONLY | os.O_CREAT | os.O_TRUNC"),
    "receipt-qualification": ("canonical_capture_attempted=True, complete_canonical_capture=complete, qualification=False,",
                              "canonical_capture_attempted=True, complete_canonical_capture=complete, qualification=complete,"),
    "measured-pin": ('byte_size=publications[-1]["byte_size"], sha256=publications[-1]["sha256"])',
                     'byte_size=publications[-1]["byte_size"], sha256="0" * 64)'),
}
CHILD = r'''
from pathlib import Path
from unittest.mock import patch
import hashlib, json, os, subprocess, sys
runtime = Path(sys.argv[1]); mode = sys.argv[2]; commit = sys.argv[3]
sys.path.insert(0, str(runtime / "scripts"))
import capture_div as A
import retain_div_capture as T

case = A.P.CASE_ID
directory = runtime / A.prefix(case)
for name, payload in A.declaration_files(A.prepare_capture(case)):
    (directory / name).write_bytes(payload)

def deny(*args, **kwargs):
    raise RuntimeError("unexpected process")

def files():
    return sorted(p.name for p in directory.iterdir())

def refusal(call):
    try:
        call()
    except T.RetentionRefused as error:
        return dict(refused=True, reason=str(error))
    except Exception as error:
        return dict(refused=False, escaped=type(error).__name__ + ": " + str(error))
    return dict(refused=False)

def summary(code, report):
    out = dict(code=code, disposition=report["disposition"], files=files(),
               complete=report.get("complete_canonical_capture"), publications=report.get("publications"))
    receipt = directory / "verification.json"
    if receipt.exists():
        out["receipt"] = json.loads(receipt.read_bytes())
        out["receipt_sha256"] = hashlib.sha256(receipt.read_bytes()).hexdigest()
    measured = directory / "measured-experiment.sexp"
    if measured.exists():
        data = measured.read_bytes(); out["measured"] = dict(byte_size=len(data), sha256=hashlib.sha256(data).hexdigest())
    return out

if mode == "retain":
    launched = []
    original = subprocess.Popen
    def record(args, *rest, **kwargs):
        launched.append([str(item) for item in args] if isinstance(args, (list, tuple)) else [str(args)])
        return original(args, *rest, **kwargs)
    with patch.object(subprocess, "Popen", record):
        code, report = T.retain(runtime, case, commit)
    result = summary(code, report); result["launched"] = launched
elif mode == "rerun":
    T.retain(runtime, case, commit)
    with patch.object(subprocess, "Popen", deny):
        result = refusal(lambda: T.retain(runtime, case, commit))
    result["files"] = files()
elif mode == "changed-declaration":
    path = directory / "planned-experiment.sexp"; path.write_bytes(path.read_bytes() + b"\n")
    with patch.object(subprocess, "Popen", deny):
        result = refusal(lambda: T.retain(runtime, case, commit))
    result["files"] = files()
elif mode == "changed-binary":
    binary = runtime / dict(A.review_authorities(case).reference.fields)["binary"]
    binary.write_bytes(binary.read_bytes() + b"\n")
    with patch.object(subprocess, "Popen", deny):
        result = refusal(lambda: T.retain(runtime, case, commit))
    result["files"] = files()
elif mode == "failed":
    code, report = T.retain(runtime, case, commit)
    result = summary(code, report)
    with patch.object(subprocess, "Popen", deny):
        result["rerun"] = refusal(lambda: T.retain(runtime, case, commit))
elif mode == "escaped":
    with patch.object(A, "capture", side_effect=RuntimeError("synthetic escape")):
        code, report = T.retain(runtime, case, commit)
    result = dict(code=code, disposition=report["disposition"], files=files(), has_traceback="traceback" in report)
elif mode == "publish":
    first = T.publish(runtime, case, "verification.json", b"first\n")
    second = refusal(lambda: T.publish(runtime, case, "verification.json", b"second\n"))
    result = dict(first=first, second=second, bytes=(directory / "verification.json").read_bytes().decode())
elif mode == "preflight":
    with patch.object(subprocess, "Popen", deny):
        code, report = T.retain(runtime, case, commit, preflight_only=True)
    result = dict(code=code, disposition=report["disposition"], files=files(), absent=len(report["preflight"]["absent"]),
                  binary=report["preflight"]["binary"]["sha256"] == dict(A.review_authorities(case).reference.fields)["binary_sha256"])
elif mode == "malformed":
    with patch.object(subprocess, "Popen", deny):
        result = dict(commit=refusal(lambda: T.preflight(runtime, case, "nope")),
                      unknown=refusal(lambda: T.preflight(runtime, "rv64gc-unknown", commit)))
    result["files"] = files()
elif mode == "cli":
    from contextlib import redirect_stdout
    from io import StringIO
    codes = {}
    for label, argv in (("preflight", ["--case", case, "--declaration-commit", commit, "--preflight-only", "--root", str(runtime)]),
                        ("bad-commit", ["--case", case, "--declaration-commit", "nope", "--root", str(runtime)]),
                        ("unknown", ["--case", "rv64gc-unknown", "--declaration-commit", commit, "--root", str(runtime)])):
        out = StringIO()
        with redirect_stdout(out), patch.object(subprocess, "Popen", deny):
            codes[label] = (T.main(argv), json.loads(out.getvalue())["disposition"])
    result = dict(codes=codes, files=files())
print(json.dumps(result, default=lambda value: str(value)))
'''


class RetentionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        review = A.Review.review()
        cls.paths = {row["path"] for row in review["files"]} | {row[2] for row in A.PREPARED} | {TOOL}

    def setUp(self):
        base = ROOT / "target/div-retention-controls"
        base.mkdir(parents=True, exist_ok=True)
        temporary = TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.runtime = Path(temporary.name) / "runtime"
        for relative in sorted(self.paths):
            path = self.runtime / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, path)
        if MUTATION:
            path = self.runtime / TOOL
            source = path.read_text()
            before, after = SEAMS[MUTATION]
            if source.count(before) != 1:
                raise RuntimeError("retention omission target must be singular: " + MUTATION)
            path.write_text(source.replace(before, after, 1))

    def child(self, mode, *, exit_code=0):
        Command.synthesize_reference(self.runtime, exit_code=exit_code)
        result = subprocess.run([sys.executable, *(["-O"] if sys.flags.optimize else []), "-B", "-c", CHILD,
                                 str(self.runtime), mode, COMMIT], cwd=ROOT, capture_output=True, text=True, timeout=300)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout.splitlines()[-1])

    def test_one_invocation_retains_fourteen_files_and_an_uncredited_receipt(self):
        result = self.child("retain")
        self.assertEqual((result["code"], result["disposition"], result["complete"]), (0, "pending", True))
        self.assertEqual(len(result["files"]), 4 + 3 + 12 + 2)
        self.assertEqual(len(result["launched"]), 3)
        for argv in result["launched"]:
            self.assertTrue(any(Path(item).name == "sail_riscv_sim" for item in argv), argv)
        receipt = result["receipt"]
        self.assertEqual((receipt["format_version"], receipt["case_id"], receipt["profile_id"]),
                         (T.FORMAT, A.P.CASE_ID, A.PROFILE))
        self.assertIs(receipt["qualification"], False)
        self.assertEqual((receipt["source_declaration_commit"], receipt["complete_canonical_capture"]), (COMMIT, True))
        self.assertEqual([run["kind"] for run in receipt["runs"]], ["baseline", "repeat", "control"])
        self.assertEqual({run["exit"] for run in receipt["runs"]}, {0})
        self.assertEqual(len({run["pid"] for run in receipt["runs"]}), 3)
        self.assertEqual([len(run["outputs"]) for run in receipt["runs"]], [4, 4, 4])
        # The first receipt's shape, read from the retained record itself, not from this tool's output.
        first = json.loads((ROOT / "evidence/rv64gc-signed-div-truncation-v2/verification.json").read_bytes())
        self.assertEqual(list(receipt["runs"][0]["outputs"][0]), list(first["runs"][0]["outputs"][0]))
        self.assertEqual(list(receipt["measured_experiment"]), list(first["measured_experiment"]))
        self.assertEqual(sorted(receipt), sorted(first))

        def pins(obj):  # a JSON object carrying both `path` and `sha256` is a fixture pin resolved relative to the record
            if isinstance(obj, dict):
                return int("path" in obj and "sha256" in obj) + sum(pins(v) for v in obj.values())
            return sum(pins(v) for v in obj) if isinstance(obj, list) else 0
        self.assertEqual(pins(receipt), 0)
        self.assertEqual(set(receipt["findings"].values()), {"matched", "satisfied"})
        self.assertEqual(receipt["record"]["disposition"], "valid")
        self.assertEqual([run["comparison"]["verdict"] for run in receipt["comparison"]["runs"]], ["AGREE", "AGREE", "DIVERGE"])
        self.assertEqual(receipt["measured_experiment"]["sha256"], result["measured"]["sha256"])
        self.assertEqual(receipt["measured_experiment"]["byte_size"], result["measured"]["byte_size"])
        self.assertEqual(receipt["measured_experiment"]["object"], A.PREFIX + "/measured-experiment.sexp")
        self.assertTrue(receipt["limitations"][0].startswith(A.P.reviewed_case(A.P.CASE_ID).coverage))
        self.assertLessEqual(receipt["charged_read_bytes"], receipt["combined_limit"])
        self.assertEqual([p["path"].rsplit("/", 1)[1] for p in result["publications"]], ["measured-experiment.sexp", "verification.json"])
        self.assertEqual(result["publications"][1]["sha256"], result["receipt_sha256"])

    def test_a_second_invocation_refuses_before_any_process(self):
        result = self.child("rerun")
        self.assertTrue(result["refused"], result)
        self.assertIn("outputs already exist; a capture is never rerun", result["reason"])
        self.assertEqual(len(result["files"]), 21)

    def test_a_changed_declaration_refuses_before_any_process(self):
        result = self.child("changed-declaration")
        self.assertTrue(result["refused"], result)
        self.assertIn("retained declaration differs from its regeneration: planned-experiment.sexp", result["reason"])
        self.assertEqual(len(result["files"]), 7)

    def test_a_changed_binary_refuses_before_any_process(self):
        result = self.child("changed-binary")
        self.assertTrue(result["refused"], result)
        self.assertIn("reference binary differs from the retained identity", result["reason"])
        self.assertEqual(len(result["files"]), 7)

    def test_a_failed_process_preserves_its_outputs_and_publishes_an_incomplete_receipt(self):
        result = self.child("failed", exit_code=7)
        self.assertEqual((result["code"], result["disposition"], result["complete"]), (1, "failed", False))
        self.assertNotIn("measured-experiment.sexp", result["files"])
        self.assertIn("verification.json", result["files"])
        self.assertTrue({"baseline.trace", "baseline.stdout", "baseline.stderr", "baseline.receipt.sexp"} <= set(result["files"]))
        receipt = result["receipt"]
        self.assertIs(receipt["qualification"], False)
        self.assertEqual((receipt["complete_canonical_capture"], receipt["collection"], receipt["evaluation"]), (False, "failed", None))
        self.assertEqual(receipt["runs"][0]["exit"], 7)
        self.assertTrue(result["rerun"]["refused"], result["rerun"])

    def test_an_escaped_invocation_publishes_nothing(self):
        result = self.child("escaped")
        self.assertEqual((result["code"], result["disposition"], result["has_traceback"]), (1, "escaped", True))
        self.assertEqual(len(result["files"]), 7)

    def test_publication_is_exclusive_and_never_replaces(self):
        result = self.child("publish")
        self.assertEqual(result["first"]["byte_size"], 6)
        self.assertTrue(result["second"]["refused"], result["second"])
        self.assertIn("never replaced", result["second"]["reason"])
        self.assertEqual(result["bytes"], "first\n")

    def test_preflight_only_starts_nothing_and_writes_nothing(self):
        result = self.child("preflight")
        self.assertEqual((result["code"], result["disposition"], result["absent"]), (0, "ready", 14))
        self.assertTrue(result["binary"])
        self.assertEqual(len(result["files"]), 7)

    def test_malformed_commit_and_unknown_case_refuse_before_anything(self):
        result = self.child("malformed")
        self.assertTrue(result["commit"]["refused"], result["commit"])
        self.assertIn("40-hex object id", result["commit"]["reason"])
        self.assertFalse(result["unknown"]["refused"])
        self.assertIn("PropertyError", result["unknown"]["escaped"])
        self.assertEqual(len(result["files"]), 7)

    def test_cli_exit_codes(self):
        result = self.child("cli")
        self.assertEqual(result["codes"]["preflight"], [0, "ready"])
        self.assertEqual(result["codes"]["bad-commit"], [1, "refused"])
        self.assertEqual(result["codes"]["unknown"], [1, "refused"])
        self.assertEqual(len(result["files"]), 7)

    def test_the_tool_uses_no_git_and_launches_no_process_of_its_own(self):
        import re
        source = (ROOT / TOOL).read_text()
        code = source.split('"""', 2)[2]  # the module docstring may say so in words; the code may not do it
        self.assertIsNone(re.search(r"\bgit\b", code))
        self.assertNotIn("subprocess", code)
        self.assertNotIn("os.system", code)


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    MUTATION = parser.parse_args().mutation
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(RetentionTests))
    print(f"DIV-CAPTURE-RETENTION: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; synthetic processes, no Sail or qualification")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
