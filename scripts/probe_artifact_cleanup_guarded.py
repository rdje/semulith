#!/usr/bin/env python3
"""Guarded-core controls in owned on-volume copies; only fresh fixture caches are ever removed."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from dataclasses import asdict
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import unittest
from unittest.mock import patch

import probe_artifact_cleanup as P

ROOT = Path(__file__).resolve().parent.parent
OBJECT = "scripts/artifact_cleanup_guarded.py"
MUTATION = None
SEAMS = {
    "guard-revalidate": ('''                            current, _ = owned.snapshot(directory, leaf, fact.path, fact.byte_size, expected=_identity(fact))
                            need(current == fact and fact.links == 1, "file identity or digest differs before unlink")
''', ''),
    "guard-residue": ('''                            try:
                                os.stat(leaf, dir_fd=directory, follow_symlinks=False)
                            except FileNotFoundError:
                                pass
                            else:
                                problem = J.Failure("residue", None, fact.path)
                                writer.finish("failed", stage, problem)
                                return outcome("failed", problem, residue=1)
''', ''),
    "guard-postcheck": ('''            stage = "postcheck"
            detail = postcheck(root, plan, selection)
            if detail:
                problem = J.Failure("postcheck", None, detail[:2000])
                writer.finish("failed", stage, problem)
                return outcome("failed", problem)
''', ''),
    "guard-intent": ('                            writer.intent(index)\n', ''),
}
TARGETS = {
    "guard-revalidate": "test_identity_change_before_unlink_fails_at_revalidate",
    "guard-residue": "test_residue_after_unlink_is_a_failure",
    "guard-postcheck": "test_postcheck_names_a_changed_retained_file",
    "guard-intent": "test_durable_intent_precedes_every_unlink",
}


class GuardedTests(unittest.TestCase):
    def setUp(self):
        self.fixture = P.CohortTests("test_plan_is_frozen_and_census_does_not_change_data")
        self.fixture.setUp();self.addCleanup(self.fixture.doCleanups)
        self.a, self.root, self.work = self.fixture.m, self.fixture.root, self.fixture.work
        self.modules = {}
        for short in ("artifact_output_provenance", "artifact_cleanup_selection", "artifact_cleanup_journal",
                      "artifact_cleanup_guarded"):
            name = "scripts/" + short + ".py"
            text = (ROOT / name).read_text()
            if MUTATION and short == "artifact_cleanup_guarded":
                old, new = SEAMS[MUTATION]
                if text.count(old) != 1:raise RuntimeError("singular guarded seam required: " + MUTATION)
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
        self.producer = "scripts/probe_c_engine.py"
        self.fixture.file(self.producer, b"owned producer source\n")
        self.fixture.file("scripts/artifact_cargo.py", b"owned Cargo command helper\n")
        base = self.o.PRODUCERS[self.producer][0] + "/debug/incremental"
        self.first, self.second = base + "/a/s/dep-graph.bin", base + "/a/s/query-cache.bin"
        self.legacy, self.input = base + "/b/t/work-products.bin", "target/retained-fixture-inputs/debug/incremental/a/s/dep-graph.bin"
        self.log = "target/refs/reference.log"
        for name, data in ((self.first, b"first captured output"), (self.second, b"second captured output"),
                           (self.legacy, b"legacy recorded output"), (self.input, b"retained fixture input"),
                           (self.log, b"retained reference log")):
            self.fixture.file(name, data)

    def source(self, name):
        data = (self.root / name).read_bytes()
        return self.o.Source(name, len(data), hashlib.sha256(data).hexdigest())

    def fact(self, name):
        with self.a.OwnedRoot(self.root) as owned:
            parent, leaf = name.rsplit("/", 1)
            with owned.directory(parent) as directory:
                item, _ = owned.snapshot(directory, leaf, name, self.o.FILE_BYTES)
        return self.o.Fact(**asdict(item))

    def row(self, name, *, captured):
        root, test_filter = self.o.PRODUCERS[self.producer]
        argv = ("cargo", "test", "--offline", "--manifest-path", "target/p4-system-12/owned-input/Cargo.toml",
                "--target-dir", root, "--config", 'build.build-dir="' + root + '"', "--lib", test_filter, "--", "--nocapture")
        pins = tuple(self.source(name) for name in self.o.SUPPORTING_OBJECTS) if captured else ()
        return self.o.Observation("2026-10-20T00:00:00+00:00", self.source(self.o.OBJECT), self.source(self.producer),
                                  argv, "cargo fixture", 0, None, self.fact(name), pins)

    def prepare(self, *, ledger=True):
        if ledger:
            rows = sorted((self.row(self.first, captured=True), self.row(self.second, captured=True),
                           self.row(self.legacy, captured=False)), key=lambda row: row.after.path)
            self.fixture.file(self.o.LEDGER, self.o.encode(self.o.Ledger(self.o.CAPTURE_FORMAT, tuple(rows))))
        plan = self.fixture.plan();self.a.publish_plan(self.root, plan)
        selection = self.s.decide(self.root, plan);self.s.publish(self.root, selection)
        return plan, selection

    def outcome(self, function, *args, **kwargs):
        try:
            return "ok", function(*args, **kwargs)
        except (self.a.CleanupError, self.a.Boundary, self.o.ProvenanceError, OSError, ValueError, TypeError) as error:
            return getattr(error, "disposition", "refused"), getattr(error, "reason", str(error))

    def after_preflight(self, effect):
        original = self.g.preflight
        def wrapper(*args, **kwargs):
            result = original(*args, **kwargs);effect();return result
        return patch.object(self.g, "preflight", side_effect=wrapper)

    def journal(self):
        plan, finding = self.j.inspect(self.root, self.work)
        return self.j.report(plan, finding)

    def untouched(self, *names):
        expected = {self.legacy: b"legacy recorded output", self.input: b"retained fixture input",
                    self.log: b"retained reference log", self.first: b"first captured output",
                    self.second: b"second captured output"}
        for name in names:
            self.assertEqual((self.root / name).read_bytes(), expected[name], name)

    def test_remove_unlinks_only_approved_and_verifies(self):
        plan, selection = self.prepare()
        self.assertEqual(selection.approved, (self.first, self.second))
        result = self.g.remove(self.root, self.work)
        self.assertEqual((result.disposition, result.stage, result.approved, result.removed, result.residue, result.failure),
                         ("complete", "verified", 2, 2, 0, None))
        self.assertEqual(result.removed_bytes, selection.approved_bytes)
        self.assertFalse((self.root / self.first).exists() or (self.root / self.second).exists())
        self.untouched(self.legacy, self.input, self.log)
        report = self.journal()
        self.assertEqual((report["recorded_state"], report["recorded_paths"], tuple(report["header"]["approved"])),
                         ("recorded-complete", [self.first, self.second], (0, 1)))
        self.assertEqual(report["header"]["selection_sha256"], hashlib.sha256(self.s.encode(selection)).hexdigest())
        self.assertEqual(self.s.inspect(self.root, self.work)[1], selection)

    def test_stale_preflight_refuses_without_journal(self):
        self.prepare()
        (self.root / self.input).write_bytes(b"changed after selection")
        disposition, detail = self.outcome(self.g.remove, self.root, self.work)
        self.assertEqual(disposition, "stale", detail);self.assertIn("first changed " + self.input, detail)
        self.assertFalse((self.root / self.work / self.j.NAME).exists())
        self.untouched(self.first, self.second, self.legacy, self.log)
        (self.root / self.input).write_bytes(b"retained fixture input")
        with patch.object(self.g.A, "tracked_paths", return_value=frozenset({self.first})):
            self.assertEqual(self.outcome(self.g.remove, self.root, self.work)[0], "stale")
        self.untouched(self.first, self.second)

    def test_nothing_approved_attempts_nothing(self):
        plan, selection = self.prepare(ledger=False)
        self.assertEqual(selection.approved, ())
        result = self.g.remove(self.root, self.work)
        self.assertEqual((result.disposition, result.removed, result.journal), ("nothing", 0, None))
        self.assertFalse((self.root / self.work / self.j.NAME).exists())
        self.untouched(self.first, self.second, self.legacy, self.input, self.log)

    def test_identity_change_before_unlink_fails_at_revalidate(self):
        self.prepare()
        with self.after_preflight(lambda: (self.root / self.first).write_bytes(b"FIRST captured output")):
            disposition, result = self.outcome(self.g.remove, self.root, self.work)
        self.assertEqual(disposition, "ok", result)
        self.assertEqual((result.disposition, result.stage, result.removed), ("failed", "revalidate", 0))
        self.assertTrue((self.root / self.first).exists() and (self.root / self.second).exists())
        report = self.journal()
        self.assertEqual((report["recorded_state"], report["stage"], report["recorded_unlink_returns"]), ("recorded-failed", "revalidate", 0))

    def test_parent_symlink_refuses_revalidation(self):
        self.prepare()
        parent = self.root / self.first.rsplit("/", 1)[0]
        copy = self.fixture.base / "outside-copy"
        def swap():
            shutil.copytree(parent, copy);shutil.rmtree(parent);parent.symlink_to(copy, target_is_directory=True)
        with self.after_preflight(swap):
            disposition, result = self.outcome(self.g.remove, self.root, self.work)
        self.assertEqual(disposition, "ok", result)
        self.assertEqual((result.disposition, result.stage, result.removed), ("failed", "revalidate", 0))
        self.assertEqual((copy / "dep-graph.bin").read_bytes(), b"first captured output")
        self.assertEqual((copy / "query-cache.bin").read_bytes(), b"second captured output")

    def test_unlink_error_records_failure_and_partial_count(self):
        self.prepare()
        actual = os.unlink
        def failing(name, *args, **kwargs):
            if name == "query-cache.bin":raise PermissionError(13, "fixture refusal")
            return actual(name, *args, **kwargs)
        with patch.object(self.g.os, "unlink", side_effect=failing):
            result = self.g.remove(self.root, self.work)
        self.assertEqual((result.disposition, result.stage, result.removed, result.failure.errno), ("failed", "unlink", 1, 13))
        self.assertFalse((self.root / self.first).exists());self.untouched(self.second, self.legacy)
        report = self.journal()
        self.assertEqual((report["recorded_state"], report["recorded_paths"], report["unresolved_intent"]),
                         ("recorded-failed", [self.first], 1))

    def test_residue_after_unlink_is_a_failure(self):
        self.prepare()
        with patch.object(self.g.os, "unlink", side_effect=lambda *args, **kwargs: None):
            result = self.g.remove(self.root, self.work)
        self.assertEqual((result.disposition, result.stage, result.residue, result.removed), ("failed", "unlink", 1, 0))
        self.assertEqual(result.failure.kind, "residue")
        self.untouched(self.first, self.second)

    def test_postcheck_names_a_changed_retained_file(self):
        self.prepare()
        actual = os.unlink
        def unlink(name, *args, **kwargs):
            actual(name, *args, **kwargs)
            if name == "query-cache.bin":(self.root / self.log).write_bytes(b"log rewritten during the attempt")
        with patch.object(self.g.os, "unlink", side_effect=unlink):
            result = self.g.remove(self.root, self.work)
        self.assertEqual((result.disposition, result.stage, result.removed), ("failed", "postcheck", 2))
        self.assertIn("first changed " + self.log, result.failure.detail)
        self.assertEqual(self.journal()["stage"], "postcheck")

    def test_durable_intent_precedes_every_unlink(self):
        self.prepare()
        def refuse(self_writer, index):
            raise self.a.CleanupError("refused", "journal: fixture intent failure")
        with patch.object(self.j.Writer, "intent", refuse):
            disposition, result = self.outcome(self.g.remove, self.root, self.work)
        self.assertEqual(disposition, "ok", result)
        self.assertEqual((result.disposition, result.stage, result.removed, result.failure.detail),
                         ("failed", "revalidate", 0, "journal: fixture intent failure"))
        self.assertTrue((self.root / self.first).exists(), "no unlink may precede a durable intent")
        self.untouched(self.first, self.second)

    def test_interruption_records_and_propagates(self):
        self.prepare()
        actual = os.unlink
        def interrupt(name, *args, **kwargs):
            if name == "query-cache.bin":raise KeyboardInterrupt
            return actual(name, *args, **kwargs)
        with patch.object(self.g.os, "unlink", side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.g.remove(self.root, self.work)
        report = self.journal()
        self.assertEqual((report["recorded_state"], report["stage"], report["recorded_paths"], report["unresolved_intent"]),
                         ("recorded-interrupted", "unlink", [self.first], 1))
        self.untouched(self.second)

    def test_legacy_rows_and_inputs_survive_a_complete_attempt(self):
        self.prepare()
        self.g.remove(self.root, self.work)
        self.untouched(self.legacy, self.input, self.log)
        plan = self.a.load_plan(self.root, self.work)
        self.assertEqual(self.a.check_plan(self.root, plan).disposition, "stale")
        self.assertEqual(self.g.postcheck(self.root, plan, self.s.inspect(self.root, self.work)[1]), "")

    def test_dry_run_cli_reports_without_touching(self):
        self.prepare()
        env = dict(os.environ, **self.fixture.fake_git())
        command = [sys.executable, *(["-O"] if sys.flags.optimize else []), "-B", str(self.root / OBJECT)]
        result = subprocess.run(command + ["--dry-run", "--workdir", self.work], cwd=ROOT, env=env,
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual((report["disposition"], report["approved"], report["unrecorded"]), ("ready", 2, 2))
        for flag in ("--delete", "--remove"):
            refused = subprocess.run(command + [flag, "--workdir", self.work], cwd=ROOT, env=env, capture_output=True, text=True, timeout=30)
            self.assertEqual(refused.returncode, 2, flag)
        self.assertFalse((self.root / self.work / self.j.NAME).exists())
        self.untouched(self.first, self.second, self.legacy, self.input, self.log)


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    MUTATION = parser.parse_args().mutation
    suite = (unittest.TestSuite([GuardedTests(TARGETS[MUTATION])]) if MUTATION else
             unittest.defaultTestLoader.loadTestsFromTestCase(GuardedTests))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"guarded core: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
