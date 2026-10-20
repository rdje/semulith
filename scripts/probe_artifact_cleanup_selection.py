#!/usr/bin/env python3
"""Strict-selection controls in owned on-volume copies; no real cache deletion."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from dataclasses import asdict, replace
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

import probe_artifact_cleanup as P

ROOT = Path(__file__).resolve().parent.parent
OBJECT = "scripts/artifact_cleanup_selection.py"
MUTATION = None
SEAMS = {
    "select-strict": ("authority = O.authorize(owned, current, tracked_paths=tracked, require_captured=True)",
                      "authority = O.authorize(owned, current, tracked_paths=tracked, require_captured=False)"),
    "select-stale": ('    need(finding.disposition == "matched", "plan is " + finding.disposition + ": " + finding.reason,\n'
                     '         "stale" if finding.disposition == "stale" else "refused")\n', ''),
    "select-exclusive": ("os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC",
                         "os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW | os.O_CLOEXEC"),
    "select-binding": ('        need(value["plan_sha256"] == digest(A.encode_plan(plan)), "plan digest binding")\n', ''),
    "select-partition": ('        need(not set(groups["approved"]) & set(groups["unrecorded"])\n'
                         '             and set(groups["approved"]) | set(groups["unrecorded"]) == set(candidates),\n'
                         '             "approved/unrecorded must partition the plan\'s candidates")\n', ''),
}
TARGETS = {
    "select-strict": "test_strict_selector_denies_unbound_legacy_rows",
    "select-stale": "test_stale_plan_refuses_before_publication",
    "select-exclusive": "test_existing_selection_is_never_overwritten",
    "select-binding": "test_inspection_binds_the_plan_and_closed_shape",
    "select-partition": "test_inspection_binds_the_plan_and_closed_shape",
}


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.fixture = P.CohortTests("test_plan_is_frozen_and_census_does_not_change_data")
        self.fixture.setUp();self.addCleanup(self.fixture.doCleanups)
        self.a, self.root, self.work = self.fixture.m, self.fixture.root, self.fixture.work
        self.modules = {}
        for short in ("artifact_output_provenance", "artifact_cleanup_selection"):
            name = "scripts/" + short + ".py"
            text = (ROOT / name).read_text()
            if MUTATION and short == "artifact_cleanup_selection":
                old, new = SEAMS[MUTATION]
                if text.count(old) != 1:raise RuntimeError("singular selection guard required: " + MUTATION)
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
        self.s.A, self.s.O = self.a, self.o
        self.producer = "scripts/probe_c_engine.py"
        self.fixture.file(self.producer, b"owned producer source\n")
        self.fixture.file("scripts/artifact_cargo.py", b"owned Cargo command helper\n")
        base = self.o.PRODUCERS[self.producer][0] + "/debug/incremental"
        self.captured = base + "/a/s/dep-graph.bin"
        self.legacy = base + "/a/s/query-cache.bin"
        self.input = "target/retained-fixture-inputs/debug/incremental/a/s/dep-graph.bin"
        self.stray = "target/debug/incremental/x/y/work-products.bin"
        for name, data in ((self.captured, b"captured generated output"), (self.legacy, b"legacy recorded output"),
                           (self.input, b"retained fixture input shaped like a cache"), (self.stray, b"unknown stray cache")):
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

    def ledger(self, *rows):
        rows = tuple(sorted(rows, key=lambda row: row.after.path))
        raw = self.o.encode(self.o.Ledger(self.o.CAPTURE_FORMAT, rows))
        self.fixture.file(self.o.LEDGER, raw)
        return raw

    def plan(self):
        plan = self.fixture.plan();self.a.publish_plan(self.root, plan)
        return plan

    def outcome(self, function, *args, **kwargs):
        try:
            return "ok", function(*args, **kwargs)
        except (self.a.CleanupError, self.a.Boundary, self.o.ProvenanceError, OSError, ValueError, TypeError) as error:
            return getattr(error, "disposition", "refused"), getattr(error, "reason", str(error))

    def test_strict_selection_approves_only_captured_recorded_outputs(self):
        raw = self.ledger(self.row(self.captured, captured=True), self.row(self.legacy, captured=False))
        plan = self.plan()
        self.assertEqual({item.path for item in plan.candidates}, {self.captured, self.legacy, self.input, self.stray})
        selection = self.s.decide(self.root, plan)
        self.assertEqual((selection.approved, selection.unrecorded), ((self.captured,), tuple(sorted((self.legacy, self.input, self.stray)))))
        sizes = {item.path: item.byte_size for item in plan.candidates}
        self.assertEqual((selection.approved_bytes, selection.unrecorded_bytes),
                         (sizes[self.captured], sum(sizes[path] for path in selection.unrecorded)))
        self.assertEqual((selection.ledger_sha256, selection.plan_sha256, selection.tracked_sha256),
                         (hashlib.sha256(raw).hexdigest(), hashlib.sha256(self.a.encode_plan(plan)).hexdigest(), plan.tracked_sha256))
        self.assertEqual(tuple(row.object for row in selection.sources), self.s.SOURCES)
        self.s.publish(self.root, selection)
        saved, inspected, current = self.s.inspect(self.root, self.work)
        self.assertEqual((saved, inspected, current), (plan, selection, True))
        self.assertEqual(self.s.decode((self.root / self.work / self.s.NAME).read_bytes(), plan), selection)

    def test_absent_ledger_approves_nothing_but_still_publishes(self):
        plan = self.plan()
        selection = self.s.decide(self.root, plan)
        self.assertEqual((selection.approved, len(selection.unrecorded), selection.ledger_sha256, selection.approved_bytes),
                         ((), 4, None, 0))
        self.s.publish(self.root, selection)
        self.assertEqual(self.s.inspect(self.root, self.work)[1], selection)

    def test_strict_selector_denies_unbound_legacy_rows(self):
        self.ledger(self.row(self.captured, captured=False))
        selection = self.s.decide(self.root, self.plan())
        self.assertEqual(selection.approved, (), "a legacy row cannot satisfy strict selection")

    def test_forged_row_for_a_cache_named_input_refuses_the_whole_ledger(self):
        forged = replace(self.row(self.captured, captured=True), after=self.fact(self.input))
        value = json.loads(self.o.encode(self.o.Ledger(self.o.CAPTURE_FORMAT, (self.row(self.captured, captured=True),))))
        value["outputs"][0]["after"]["path"] = self.input
        self.fixture.file(self.o.LEDGER, (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode())
        disposition, detail = self.outcome(self.s.decide, self.root, self.plan())
        self.assertEqual(disposition, "refused", detail);self.assertIn("output class", detail)
        self.assertFalse((self.root / self.work / self.s.NAME).exists())
        del forged

    def test_stale_plan_refuses_before_publication(self):
        self.ledger(self.row(self.captured, captured=True))
        plan = self.plan()
        (self.root / self.input).write_bytes(b"changed after planning")
        disposition, detail = self.outcome(self.s.decide, self.root, plan)
        self.assertEqual(disposition, "stale", detail)
        self.assertFalse((self.root / self.work / self.s.NAME).exists())
        self.fixture.tracked.add("target/newly-tracked.bin")
        self.assertEqual(self.outcome(self.s.decide, self.root, plan)[0], "stale")

    def test_existing_selection_is_never_overwritten(self):
        self.ledger(self.row(self.captured, captured=True))
        selection = self.s.decide(self.root, self.plan())
        foreign = self.fixture.file(self.work + "/" + self.s.NAME, b"foreign selection")
        disposition, detail = self.outcome(self.s.publish, self.root, selection)
        self.assertEqual(disposition, "refused", detail)
        self.assertEqual(foreign.read_bytes(), b"foreign selection")

    def test_inspection_binds_the_plan_and_closed_shape(self):
        self.ledger(self.row(self.captured, captured=True))
        plan = self.plan();selection = self.s.decide(self.root, plan);raw = self.s.encode(selection)
        value = json.loads(raw);sizes = {item.path: item.byte_size for item in plan.candidates}
        variants = [b" " + raw, raw.replace(b'"approved_bytes":', b'"approved_bytes":0,"extra":')]
        for change in ("plan", "missing", "overlap", "bytes", "sources", "format"):
            doc = json.loads(raw)
            if change == "plan":doc["plan_sha256"] = "0" * 64
            elif change == "missing":doc["unrecorded_bytes"] -= sizes[doc["unrecorded"].pop(0)]  # byte sums stay consistent
            elif change == "overlap":
                doc["unrecorded"] = sorted(doc["unrecorded"] + doc["approved"]);doc["unrecorded_bytes"] += doc["approved_bytes"]
            elif change == "bytes":doc["approved_bytes"] += 1
            elif change == "sources":doc["sources"] = doc["sources"][::-1]
            else:doc["format"] = "artifact-cleanup-selection-v2"
            variants.append((json.dumps(doc, sort_keys=True, separators=(",", ":")) + "\n").encode())
        refused = [self.outcome(self.s.decode, data, plan)[0] == "refused" for data in variants]
        self.assertEqual(refused, [True] * len(variants))
        self.assertEqual(json.loads(self.s.encode(self.s.decode(raw, plan))), value)

    def test_ctime_drift_keeps_recorded_authority(self):
        self.ledger(self.row(self.captured, captured=True))
        target = self.root / self.captured
        os.link(target, target.parent / "seeded-by-rustc.bin");(target.parent / "seeded-by-rustc.bin").unlink()
        selection = self.s.decide(self.root, self.plan())
        self.assertEqual(selection.approved, (self.captured,), "a ctime-only change is not a changed output")

    def test_changed_recorded_output_is_unrecorded(self):
        self.ledger(self.row(self.captured, captured=True))
        (self.root / self.captured).write_bytes(b"regenerated after the record")
        self.assertEqual(self.s.decide(self.root, self.plan()).approved, ())

    def test_selection_pins_current_sources(self):
        self.ledger(self.row(self.captured, captured=True))
        self.s.publish(self.root, self.s.decide(self.root, self.plan()))
        path = self.root / OBJECT;path.write_bytes(path.read_bytes() + b"\n# changed selector\n")
        self.assertFalse(self.s.inspect(self.root, self.work)[2])

    def test_copied_cli_selects_inspects_and_has_no_delete_mode(self):
        self.ledger(self.row(self.captured, captured=True))
        self.plan()
        env = dict(os.environ, **self.fixture.fake_git())
        command = [sys.executable, *(["-O"] if sys.flags.optimize else []), "-B", str(self.root / OBJECT)]
        results = {}
        for flag, expected in (("--select", 0), ("--inspect", 0), ("--select", 2), ("--delete", 2)):
            result = subprocess.run(command + [flag, "--workdir", self.work], cwd=ROOT, env=env,
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, expected, flag + ": " + result.stdout + result.stderr)
            results.setdefault(flag, result.stdout)
        report = json.loads(results["--select"])
        self.assertEqual((report["disposition"], report["approved"], report["unrecorded"]), ("selected", 1, 3))
        self.assertEqual(json.loads(results["--inspect"])["sources_current"], True)
        self.assertEqual((self.root / self.captured).read_bytes(), b"captured generated output")


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    MUTATION = parser.parse_args().mutation
    suite = (unittest.TestSuite([SelectionTests(TARGETS[MUTATION])]) if MUTATION else
             unittest.defaultTestLoader.loadTestsFromTestCase(SelectionTests))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"artifact selection: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
