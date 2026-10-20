#!/usr/bin/env python3
"""Authenticate and replay the original AC0067 helper only in owned fixtures."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from contextlib import contextmanager, redirect_stderr, redirect_stdout
import hashlib
import importlib.util
from io import StringIO
import json
import os
from pathlib import Path
import runpy
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import artifact_cleanup as A

ROOT = Path(__file__).resolve().parent.parent
SOURCE = "scripts/fixtures/artifact_cleanup_0067.py.txt"
LEGACY_BYTES = 5815
LEGACY_SHA = "0396e669f9b798f010dcbe67b5f3462497afbcff478d353c7d989b9b2bd307e9"
MUTATION = None
PIN = ('    A.need(fact.byte_size == LEGACY_BYTES and fact.sha256 == LEGACY_SHA,\n'
       '           "legacy source identity differs")\n')


def source_bytes(root: Path) -> bytes:
    """Read one bounded passive input without following an ancestor or final link."""
    with A.OwnedRoot(root) as owned, owned.directory("scripts/fixtures") as directory:
        fact, data = owned.snapshot(directory, "artifact_cleanup_0067.py.txt", SOURCE,
                                   8192, payload=True)
    A.need(fact.byte_size == LEGACY_BYTES and fact.sha256 == LEGACY_SHA,
           "legacy source identity differs")
    return data


@contextmanager
def owned_temporary(root: Path):
    """Allocate inside a verified repository-derived namespace, never the host default."""
    relative = "target/legacy-cleanup-controls"
    with A.OwnedRoot(root) as owned, owned.directory(relative, create=True):
        with TemporaryDirectory(prefix="legacy-", dir=root / relative) as name:
            yield Path(name)


def replay(root: Path, payload: bytes, *, release: bool) -> dict:
    """Execute the pinned historical bytes; all possible cache paths are newly owned."""
    A.need(len(payload) == LEGACY_BYTES and hashlib.sha256(payload).hexdigest() == LEGACY_SHA,
           "replay requires the authenticated historical payload")
    with owned_temporary(root) as fixture:
        helper = fixture / "sources/cleanup.py"
        helper.parent.mkdir(); helper.write_bytes(payload)
        work = fixture / "target/artifact-cleanup-0067"; work.mkdir(parents=True)
        mode = "release" if release else "debug"
        cache = fixture / f"target/{mode}/incremental/owned/session/dep-graph.bin"
        cache.parent.mkdir(parents=True); cache.write_bytes(b"owned cache fixture")
        retained = fixture / f"target/{mode}/reference.log"; retained.write_bytes(b"retained input")

        def public_git(command, **kwargs):
            if command == ["git", "ls-files", "-z"]: return b""
            if command == ["git", "rev-parse", "--show-toplevel"]: return str(fixture) + "\n"
            raise RuntimeError("unexpected historical subprocess")

        previous = Path.cwd()
        observations = []
        try:
            os.chdir(fixture)
            for operation in ("--plan", "--delete"):
                stream = StringIO(); error = None
                with patch("subprocess.check_output", side_effect=public_git), \
                     patch.object(sys, "argv", [str(helper), operation]), \
                     redirect_stdout(stream), redirect_stderr(stream):
                    try:
                        runpy.run_path(str(helper), run_name="__main__")
                    except RuntimeError as failure:
                        error = str(failure)
                observations.append(dict(operation=operation, error=error,
                                         cache_exists=cache.exists(),
                                         receipt_exists=(work / "result.json").exists()))
            plan = json.loads((work / "plan.json").read_bytes())
            result = json.loads((work / "result.json").read_bytes()) if (work / "result.json").exists() else None
            return dict(observations=observations, plan=plan, result=result,
                        retained=retained.read_bytes(), helper_sha256=hashlib.sha256(helper.read_bytes()).hexdigest())
        finally:
            os.chdir(previous)


class LegacyTests(unittest.TestCase):
    def setUp(self):
        self.payload = source_bytes(ROOT)
        self.allocated = owned_temporary(ROOT)
        self.base = self.allocated.__enter__()
        self.addCleanup(self.allocated.__exit__, None, None, None)
        self.root = self.base / "runtime"
        source = self.root / SOURCE; source.parent.mkdir(parents=True)
        source.write_bytes(self.payload)
        self.source = source
        copied = self.root / "scripts/probe_legacy_artifact_cleanup.py"
        text = Path(__file__).read_text()
        if MUTATION:
            if text.count(PIN) != 1: raise RuntimeError("singular source-pin guard required")
            text = text.replace(PIN, "", 1)
        copied.write_text(text)
        name = "legacy_probe_" + hashlib.sha256(str(self.root).encode()).hexdigest()
        spec = importlib.util.spec_from_file_location(name, copied)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module; self.addCleanup(sys.modules.pop, name)
        spec.loader.exec_module(module)
        self.m = module

    def test_original_bytes_are_frozen(self):
        data = self.m.source_bytes(self.root)
        self.assertEqual(len(data), LEGACY_BYTES)
        self.assertEqual(hashlib.sha256(data).hexdigest(), LEGACY_SHA)
        self.assertEqual(data, self.payload)

    def test_debug_replay_completes_without_touching_retained_input(self):
        before = Path.cwd()
        result = self.m.replay(self.root, self.payload, release=False)
        self.assertEqual(Path.cwd(), before)
        self.assertEqual([r["error"] for r in result["observations"]], [None, None])
        self.assertEqual(result["observations"][-1]["cache_exists"], False)
        self.assertEqual(result["retained"], b"retained input")
        self.assertEqual(result["result"]["deleted_files"], 1)
        self.assertEqual(result["result"]["residue"], 0)
        self.assertEqual(result["result"]["helper_sha256"], LEGACY_SHA)

    def test_release_replay_reproduces_removed_cache_without_receipt(self):
        before = Path.cwd()
        result = self.m.replay(self.root, self.payload, release=True)
        self.assertEqual(Path.cwd(), before)
        self.assertEqual(result["observations"][0]["error"], None)
        last = result["observations"][-1]
        self.assertEqual(last["error"], "post-delete census differs")
        self.assertEqual((last["cache_exists"], last["receipt_exists"]), (False, False))
        self.assertEqual(result["result"], None)
        self.assertEqual(result["retained"], b"retained input")
        candidate = result["plan"]["candidates"][0]["path"]
        self.assertIn(candidate, result["plan"]["stray_paths"])

    def test_changed_source_refuses_before_replay(self):
        changed = self.payload[:-1] + b" "
        self.assertEqual(len(changed), LEGACY_BYTES)
        self.assertNotEqual(changed, self.payload)
        self.source.write_bytes(changed)
        with self.assertRaisesRegex(A.CleanupError, "legacy source identity differs"):
            self.m.source_bytes(self.root)
        self.assertFalse((self.root / "target").exists())

    def test_unsafe_or_oversized_source_refuses(self):
        self.source.write_bytes(b"x" * 8193)
        with self.assertRaisesRegex(A.CleanupError, "file byte limit"):
            self.m.source_bytes(self.root)
        self.source.unlink()
        outside = self.base / "protected.py"; outside.write_bytes(self.payload)
        self.source.symlink_to(outside)
        with self.assertRaises(A.CleanupError): self.m.source_bytes(self.root)
        self.assertEqual(outside.read_bytes(), self.payload)
        self.source.unlink(); self.source.write_bytes(self.payload)
        marker = self.root / "scripts/.git"; marker.write_text("owned boundary fixture")
        with self.assertRaises(A.Boundary): self.m.source_bytes(self.root)


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=["source-pin"])
    MUTATION = parser.parse_args().mutation
    suite = (unittest.TestSuite([LegacyTests("test_changed_source_refuses_before_replay")])
             if MUTATION else unittest.defaultTestLoader.loadTestsFromTestCase(LegacyTests))
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    print(f"LEGACY-CLEANUP: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; pinned source, owned fixtures only")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
