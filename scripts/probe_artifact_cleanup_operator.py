#!/usr/bin/env python3
"""Operator-act controls in owned on-volume copies with a stubbed host census; no real cleanup."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from dataclasses import asdict
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

import probe_artifact_cleanup as P

ROOT = Path(__file__).resolve().parent.parent
OBJECT = "scripts/artifact_cleanup_operator.py"
MUTATION = None
SEAMS = {
    "op-census-run": ('    verdict = census(root)\n', '    verdict = Census(0, VERDICT)\n'),
    "op-census-rc": ('    need(child.returncode == 0, "project work is running: " + first[:200])\n', ''),
    "op-census-verdict": ('    need(first.startswith(VERDICT), "host census gave no green verdict: " + first[:200], "unavailable")\n', ''),
}
TARGETS = {
    "op-census-run": "test_census_runs_once_immediately_before_the_core",
    "op-census-rc": "test_running_project_work_refuses_before_any_unlink",
    "op-census-verdict": "test_census_output_must_carry_the_green_verdict",
}
STUB = '''#!/usr/bin/env bash
case="$(cd "$(dirname "$0")/.." && pwd)/census-case.json"
python3 - "$case" <<'PY'
import json, sys, time
case = json.load(open(sys.argv[1]))
time.sleep(case.get("sleep", 0))
sys.stdout.write(case.get("stdout", "")); sys.stdout.flush()
sys.stderr.write(case.get("stderr", "")); sys.stderr.flush()
raise SystemExit(case.get("rc", 0))
PY
'''
GREEN = "handoff: OK — no project-owned background job is running (repo fixture)\n"


class OperatorTests(unittest.TestCase):
    def setUp(self):
        self.fixture = P.CohortTests("test_plan_is_frozen_and_census_does_not_change_data")
        self.fixture.setUp();self.addCleanup(self.fixture.doCleanups)
        self.a, self.root, self.work = self.fixture.m, self.fixture.root, self.fixture.work
        self.modules = {}
        for short in ("artifact_output_provenance", "artifact_cleanup_selection", "artifact_cleanup_journal",
                      "artifact_cleanup_guarded", "artifact_cleanup_operator"):
            name = "scripts/" + short + ".py"
            text = (ROOT / name).read_text()
            if MUTATION and short == "artifact_cleanup_operator":
                old, new = SEAMS[MUTATION]
                if text.count(old) != 1:raise RuntimeError("singular operator seam required: " + MUTATION)
                text = text.replace(old, new, 1)
            path = self.fixture.file(name, text.encode())
            module_name = short + "_" + hashlib.sha256(str(self.root).encode()).hexdigest()
            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec);sys.modules[module_name] = module
            self.addCleanup(sys.modules.pop, module_name)
            with patch.dict(sys.modules, artifact_cleanup=self.a, **self.modules):
                spec.loader.exec_module(module)
            self.modules[short] = module
        self.o, self.s = self.modules["artifact_output_provenance"], self.modules["artifact_cleanup_selection"]
        self.j, self.g = self.modules["artifact_cleanup_journal"], self.modules["artifact_cleanup_guarded"]
        self.op = self.modules["artifact_cleanup_operator"]
        stub = self.fixture.file(self.op.CENSUS, STUB.encode());stub.chmod(0o755)
        self.census()
        self.producer = "scripts/probe_c_engine.py"
        self.fixture.file(self.producer, b"owned producer source\n")
        self.fixture.file("scripts/artifact_cargo.py", b"owned Cargo command helper\n")
        base = self.o.PRODUCERS[self.producer][0] + "/debug/incremental"
        self.first, self.second = base + "/a/s/dep-graph.bin", base + "/a/s/query-cache.bin"
        self.input, self.log = "target/retained-fixture-inputs/debug/incremental/a/s/dep-graph.bin", "target/refs/reference.log"
        for name, data in ((self.first, b"first captured output"), (self.second, b"second captured output"),
                           (self.input, b"retained fixture input"), (self.log, b"retained reference log")):
            self.fixture.file(name, data)

    def census(self, rc=0, stdout=GREEN, stderr="", sleep=0):
        self.fixture.file("census-case.json", json.dumps(dict(rc=rc, stdout=stdout, stderr=stderr, sleep=sleep)).encode())

    def source(self, name):
        data = (self.root / name).read_bytes()
        return self.o.Source(name, len(data), hashlib.sha256(data).hexdigest())

    def fact(self, name):
        with self.a.OwnedRoot(self.root) as owned:
            parent, leaf = name.rsplit("/", 1)
            with owned.directory(parent) as directory:
                item, _ = owned.snapshot(directory, leaf, name, self.o.FILE_BYTES)
        return self.o.Fact(**asdict(item))

    def row(self, name):
        root, test_filter = self.o.PRODUCERS[self.producer]
        argv = ("cargo", "test", "--offline", "--manifest-path", "target/p4-system-12/owned-input/Cargo.toml",
                "--target-dir", root, "--config", 'build.build-dir="' + root + '"', "--lib", test_filter, "--", "--nocapture")
        pins = tuple(self.source(name) for name in self.o.SUPPORTING_OBJECTS)
        return self.o.Observation("2026-10-20T00:00:00+00:00", self.source(self.o.OBJECT), self.source(self.producer),
                                  argv, "cargo fixture", 0, None, self.fact(name), pins)

    def prepare(self, *, ledger=True):
        if ledger:
            rows = sorted((self.row(self.first), self.row(self.second)), key=lambda row: row.after.path)
            self.fixture.file(self.o.LEDGER, self.o.encode(self.o.Ledger(self.o.CAPTURE_FORMAT, tuple(rows))))
        plan = self.fixture.plan();self.a.publish_plan(self.root, plan)
        selection = self.s.decide(self.root, plan);self.s.publish(self.root, selection)
        return plan, selection

    def outcome(self, function, *args, **kwargs):
        try:
            return "ok", function(*args, **kwargs)
        except (self.a.CleanupError, self.a.Boundary, OSError, ValueError, TypeError) as error:
            return getattr(error, "disposition", "refused"), getattr(error, "reason", str(error))

    def untouched(self, *names):
        expected = {self.first: b"first captured output", self.second: b"second captured output",
                    self.input: b"retained fixture input", self.log: b"retained reference log"}
        for name in names:
            self.assertEqual((self.root / name).read_bytes(), expected[name], name)

    def run_main(self, *argv):
        buffer = io.StringIO()
        with patch.object(sys, "argv", [OBJECT, *argv]), patch.object(sys, "stdout", buffer):
            code = self.op.main()
        return code, json.loads(buffer.getvalue())

    def test_delete_requires_green_census_then_removes_and_receipts(self):
        plan, selection = self.prepare()
        verdict, outcome = self.op.delete(self.root, self.work)
        self.assertTrue(verdict.verdict.startswith("handoff: OK"))
        self.assertEqual((outcome.disposition, outcome.stage, outcome.removed), ("complete", "verified", 2))
        self.assertFalse((self.root / self.first).exists() or (self.root / self.second).exists())
        self.untouched(self.input, self.log)
        report = self.op.receipt(verdict, outcome)
        self.assertEqual((report["disposition"], report["removed"], report["census"]), ("complete", 2, verdict.verdict))
        inspected = self.op.inspect(self.root, self.work)
        self.assertEqual((inspected["journal"]["recorded_state"], inspected["selection"]["approved"], inspected["plan"]["candidates"]),
                         ("recorded-complete", 2, 3))

    def test_running_project_work_refuses_before_any_unlink(self):
        self.prepare()
        self.census(rc=1, stdout="handoff: 1 project-owned process(es) STILL RUNNING — not handoff-ready:\n\n  123 00:05 owned build\n")
        disposition, detail = self.outcome(self.op.delete, self.root, self.work)
        self.assertEqual(disposition, "refused", detail);self.assertIn("project work is running", detail)
        self.untouched(self.first, self.second)
        self.assertFalse((self.root / self.work / self.j.NAME).exists())

    def test_unavailable_census_refuses_as_unavailable(self):
        self.prepare()
        cases = [dict(rc=2, stderr="handoff: REFUSED — lsof census failed"), dict(rc=0, stdout=""),
                 dict(rc=0, stdout="x" * (self.op.CENSUS_BYTES + 1)), dict(rc=0, stdout=GREEN, sleep=5)]
        observed = []
        for case in cases:
            self.census(**case)
            with patch.object(self.op, "CENSUS_TIMEOUT", 0.5):
                observed.append(self.outcome(self.op.delete, self.root, self.work)[0])
        self.assertEqual(observed, ["unavailable"] * 4)
        self.untouched(self.first, self.second)
        self.assertFalse((self.root / self.work / self.j.NAME).exists())

    def test_census_output_must_carry_the_green_verdict(self):
        self.prepare()
        self.census(rc=0, stdout="handoff: something else entirely\n")
        disposition, detail = self.outcome(self.op.delete, self.root, self.work)
        self.assertEqual(disposition, "unavailable", detail);self.assertIn("no green verdict", detail)
        self.untouched(self.first, self.second)

    def test_census_runs_once_immediately_before_the_core(self):
        self.prepare()
        calls = []
        original_census, original_remove = self.op.census, self.op.G.remove
        def census(root):
            calls.append("census");return original_census(root)
        def remove(*args, **kwargs):
            calls.append("remove");return original_remove(*args, **kwargs)
        with patch.object(self.op, "census", side_effect=census), patch.object(self.op.G, "remove", side_effect=remove):
            self.op.delete(self.root, self.work)
            self.assertEqual(calls, ["census", "remove"])
            calls.clear();self.op.inspect(self.root, self.work)
        self.assertEqual(calls, [])

    def test_partial_failure_receipt_and_inspection(self):
        self.prepare()
        actual = os.unlink
        def failing(name, *args, **kwargs):
            if name == "query-cache.bin":raise PermissionError(13, "fixture refusal")
            return actual(name, *args, **kwargs)
        with patch.object(self.g.os, "unlink", side_effect=failing):
            code, report = self.run_main("--delete", "--workdir", self.work)
        self.assertEqual((code, report["disposition"], report["stage"], report["removed"], report["failure"]["errno"]),
                         (1, "failed", "unlink", 1, 13))
        self.assertFalse((self.root / self.first).exists());self.untouched(self.second)
        code, inspected = self.run_main("--inspect", "--workdir", self.work)
        self.assertEqual((code, inspected["journal"]["recorded_state"], inspected["journal"]["unresolved_intent"]), (0, "recorded-failed", 1))

    def test_interruption_exits_130_with_journal(self):
        self.prepare()
        actual = os.unlink
        def interrupt(name, *args, **kwargs):
            if name == "query-cache.bin":raise KeyboardInterrupt
            return actual(name, *args, **kwargs)
        with patch.object(self.g.os, "unlink", side_effect=interrupt):
            code, report = self.run_main("--delete", "--workdir", self.work)
        self.assertEqual((code, report["disposition"]), (130, "interrupted"))
        self.assertEqual(self.op.inspect(self.root, self.work)["journal"]["recorded_state"], "recorded-interrupted")
        self.untouched(self.second)

    def test_inspect_without_attempt_reports_no_journal(self):
        self.prepare()
        self.assertIsNone(self.op.inspect(self.root, self.work)["journal"])
        code, report = self.run_main("--inspect", "--workdir", self.work)
        self.assertEqual((code, report["disposition"], report["journal"]), (0, "inspected", None))
        self.untouched(self.first, self.second)

    def test_nothing_approved_is_a_green_receipt(self):
        self.prepare(ledger=False)
        code, report = self.run_main("--delete", "--workdir", self.work)
        self.assertEqual((code, report["disposition"], report["removed"]), (0, "nothing", 0))
        self.untouched(self.first, self.second, self.input, self.log)

    def test_cold_copied_cli_delete_inspect_and_no_plan_mode(self):
        self.prepare()
        env = dict(os.environ, **self.fixture.fake_git())
        command = [sys.executable, *(["-O"] if sys.flags.optimize else []), "-B", str(self.root / OBJECT)]
        results = {}
        for flag, expected in (("--inspect", 0), ("--delete", 0), ("--delete", 1), ("--plan", 2)):
            result = subprocess.run(command + [flag, "--workdir", self.work], cwd=ROOT, env=env,
                                    capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, expected, flag + ": " + result.stdout + result.stderr)
            results.setdefault(flag, []).append(result.stdout)
        report = json.loads(results["--delete"][0])
        self.assertEqual((report["disposition"], report["removed"], report["stage"]), ("complete", 2, "verified"))
        again = json.loads(results["--delete"][1])
        self.assertEqual(again["disposition"], "stale");self.assertIn("first gone " + self.first, again["reason"])
        self.assertFalse((self.root / self.first).exists());self.untouched(self.input, self.log)


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    MUTATION = parser.parse_args().mutation
    suite = (unittest.TestSuite([OperatorTests(TARGETS[MUTATION])]) if MUTATION else
             unittest.defaultTestLoader.loadTestsFromTestCase(OperatorTests))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"operator act: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
