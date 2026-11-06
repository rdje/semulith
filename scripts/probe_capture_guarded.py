#!/usr/bin/env python3
"""Controls for the capture guard (`capture_guarded.py`, P4-SYSTEM.14 a50-c2).

A scratch repository stands in for the tree, and stand-ins for the host, the preflight and the capture record what ran, so no
reference process runs here. One test reads the real manifests.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest

import capture_guarded as M

ROOT = Path(__file__).resolve().parent.parent
COMMIT_MESSAGE = ["-c", "user.name=scratch", "-c", "user.email=scratch@invalid", "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", "scratch"]
MUTATIONS = {
    "object-id": ("if OBJECT_ID.fullmatch(commit) is None:", "if False:"),
    "ancestor": ('if _git(root, "merge-base", "--is-ancestor", commit, "HEAD").returncode != 0:', "if False:"),
    "clean": ('if status.returncode != 0 or status.stdout.strip():', "if False:"),
    "moved": ("    if moved:\n", "    if False:\n"),
    "views": ("paths = set(AUTHORITY_VIEWS)", "paths = set()"),
    "empty-manifest": ("        if not named:\n", "        if False:\n"),
    "own-gate": ("        if gate(root):\n", "        if False:\n"),
    "already": ('if (root / "evidence" / case / "verification.json").exists():', "if False:"),
    "unfit-host": ("if not check_only and not host(log):", "if False:"),
    "judged-again": ("            require_fit_tree(root, cases, commit)\n            ready(root, case, commit)", "            ready(root, case, commit)"),
    "preflight": ("            ready(root, case, commit)\n", ""),
    "first-nonzero": ("        if code != 0:\n", "        if False:\n"),
    "check-captures": ("        if check_only:\n", "        if False:\n"),
    "limit": ("if current < LOAD_LIMIT:", "if True:"),
    "spawn": ("                spawn()\n", "                pass\n"),
    "spawn-refusal": ("                log(f\"spawn probe refused at load {current:.2f}: {error}\")\n", "                return True\n"),
    "deadline": ("        if clock() >= deadline:\n            return False\n", ""),
}


class Clock:
    """Time that moves only when the guard sleeps."""

    def __init__(self, limit: int = 100):
        self.now, self.slept, self.limit = 0.0, 0, limit

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.now += seconds; self.slept += 1
        if self.slept > self.limit:
            raise TimeoutError("the guard never gave up")


class GuardTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / "target" / "tmp"
        scratch.mkdir(parents=True, exist_ok=True)
        self.td = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.td.name).resolve()
        self.git("init", "-q")
        (self.root / "src").mkdir()
        (self.root / "src/pinned.txt").write_text("pinned\n")
        (self.root / "src/other.txt").write_text("other\n")
        for case in ("c1", "c2"):
            (self.root / "evidence" / case).mkdir(parents=True)
            (self.root / "evidence" / case / "dependencies.sexp").write_text('(dependencies (input (id "i") (path "src/pinned.txt")))\n')
        self.commit()
        self.declared = self.git("rev-parse", "HEAD").stdout.strip()
        self.ran, self.lines = [], []

    def tearDown(self):
        self.td.cleanup()

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, text=True, check=True)

    def commit(self):
        self.git("add", "-A"); self.git(*COMMIT_MESSAGE)

    def take(self, root, case, commit, out):
        self.ran.append(case)
        return 0

    def run_guard(self, cases=("c1", "c2"), commit=None, **kwargs):
        kwargs.setdefault("host", lambda log: True)
        kwargs.setdefault("ready", lambda root, case, commit: None)
        kwargs.setdefault("take", self.take)
        kwargs.setdefault("gate", lambda root: False)
        return M.run(self.root, cases, commit or self.declared, self.root / "out", self.lines.append, **kwargs)

    def test_each_case_captured_once_in_order(self):
        self.assertEqual(self.run_guard(), 0)
        self.assertEqual(self.ran, ["c1", "c2"])
        self.assertEqual(self.lines, ["c1 capture rc=0", "c2 capture rc=0"])

    def test_a_commit_that_is_not_an_object_id_is_refused(self):
        self.assertEqual(self.run_guard(commit="HEAD"), 3)
        self.assertEqual(self.ran, [])

    def test_a_commit_that_is_not_an_ancestor_is_refused(self):
        self.git("checkout", "-q", "-b", "side")
        (self.root / "src/other.txt").write_text("side\n"); self.commit()
        side = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("checkout", "-q", "-")
        self.assertEqual(self.run_guard(commit=side), 3)
        self.assertIn("not an ancestor", self.lines[-1])

    def test_a_dirty_tree_is_refused(self):
        (self.root / "src/other.txt").write_text("dirty\n")
        self.assertEqual(self.run_guard(), 3)
        self.assertEqual((self.ran, self.lines), ([], ["refused: the tracked tree is not clean"]))

    def test_an_untracked_output_does_not_dirty_the_tree(self):
        (self.root / "evidence/c1/baseline.trace").write_text("an earlier case's output\n")
        self.assertEqual(self.run_guard(), 0)

    def test_a_pinned_path_moved_since_the_declaration_is_refused(self):
        (self.root / "src/pinned.txt").write_text("moved\n"); self.commit()
        self.assertEqual(self.run_guard(), 3)
        self.assertEqual(self.ran, [])
        self.assertIn("src/pinned.txt", self.lines[-1])

    def test_an_authority_view_moved_since_the_declaration_is_refused(self):
        view = self.root / M.AUTHORITY_VIEWS[0]
        view.parent.mkdir(parents=True, exist_ok=True); view.write_text("moved\n"); self.commit()
        self.assertEqual(self.run_guard(), 3)
        self.assertIn(M.AUTHORITY_VIEWS[0], self.lines[-1])

    def test_an_unpinned_path_may_move(self):
        (self.root / "src/other.txt").write_text("moved\n"); self.commit()
        self.assertEqual(self.run_guard(), 0)
        self.assertEqual(self.ran, ["c1", "c2"])

    def test_a_manifest_pinning_nothing_is_refused(self):
        (self.root / "evidence/c1/dependencies.sexp").write_text("(dependencies)\n"); self.commit()
        self.assertEqual(self.run_guard(), 3)
        self.assertIn("pins nothing", self.lines[-1])

    def test_a_missing_manifest_is_refused(self):
        self.assertEqual(self.run_guard(cases=("c1", "absent")), 3)
        self.assertEqual(self.ran, [])

    def test_this_checkouts_own_gate_refuses(self):
        self.assertEqual(self.run_guard(gate=lambda root: True), 3)
        self.assertEqual(self.ran, [])

    def test_a_captured_case_is_skipped_and_never_run_again(self):
        (self.root / "evidence/c1/verification.json").write_text("{}\n")
        self.assertEqual(self.run_guard(), 0)
        self.assertEqual(self.ran, ["c2"])
        self.assertEqual(self.lines[0], "c1: already captured; never run again")

    def test_the_first_nonzero_capture_stops_the_run(self):
        def fails(root, case, commit, out):
            self.ran.append(case)
            return 7
        self.assertEqual(self.run_guard(take=fails), 7)
        self.assertEqual(self.ran, ["c1"])

    def test_a_refused_preflight_stops_with_nothing_captured(self):
        def refuses(root, case, commit):
            raise M.Refused(f"{case}: preflight refused")
        self.assertEqual(self.run_guard(ready=refuses), 3)
        self.assertEqual(self.ran, [])

    def test_an_unfit_host_spends_nothing(self):
        self.assertEqual(self.run_guard(host=lambda log: False), 4)
        self.assertEqual(self.ran, [])

    def test_a_tree_moved_during_the_hold_is_refused(self):
        def host(log):
            (self.root / "src/other.txt").write_text("moved during the hold\n")
            return True
        self.assertEqual(self.run_guard(host=host), 3)
        self.assertEqual(self.ran, [])

    def test_check_captures_nothing_and_asks_the_host_nothing(self):
        def host(log):
            self.fail("--check does not hold on the host")
        self.assertEqual(self.run_guard(check_only=True, host=host), 0)
        self.assertEqual((self.ran, self.lines), ([], ["c1: ready", "c2: ready"]))

    def test_the_host_holds_above_the_limit_then_gives_up(self):
        clock = Clock(); spawned = []
        self.assertFalse(M.host_ready(self.lines.append, load=lambda: M.LOAD_LIMIT, spawn=lambda: spawned.append(1), sleep=clock.sleep, clock=clock))
        self.assertEqual(spawned, [])
        self.assertEqual(clock.now, M.HOLD_SECONDS)
        self.assertIn("holding", self.lines[0])

    def test_the_host_is_ready_when_the_load_falls(self):
        clock = Clock(); loads = iter([M.LOAD_LIMIT + 1, M.LOAD_LIMIT - 1])
        self.assertTrue(M.host_ready(self.lines.append, load=lambda: next(loads), spawn=lambda: None, sleep=clock.sleep, clock=clock))
        self.assertEqual(clock.slept, 1)
        self.assertIn("host ready", self.lines[-1])

    def test_the_spawn_probe_refusing_holds_the_host(self):
        clock = Clock()
        def refuses():
            raise PermissionError(1, "Operation not permitted")
        self.assertFalse(M.host_ready(self.lines.append, load=lambda: 1.0, spawn=refuses, sleep=clock.sleep, clock=clock))
        self.assertIn("Operation not permitted", self.lines[0])

    def test_the_real_spawn_probe_reaps_what_it_spawns(self):
        M.spawn_probe(3)

    def test_the_real_manifests_pin_what_the_capture_reads(self):
        paths = M.frozen_paths(ROOT, ["rv64gc-svade-v1"])
        self.assertLessEqual({"scripts/capture_div.py", "scripts/derive_rv64gc_expectations.py", "profiles/rv64gc-lab-v0/state.sexp"}, paths)
        self.assertLessEqual(set(M.AUTHORITY_VIEWS), paths)
        self.assertFalse(any(path == "scripts/capture_guarded.py" for path in paths), "the guard is no input of what it guards")


def main():
    global M
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(MUTATIONS))
    args = parser.parse_args()
    if args.mutation:
        path = ROOT / "scripts/capture_guarded.py"
        source = path.read_text()
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("mutation no longer selects exactly one guard")
        module = types.ModuleType("mutated_capture_guarded")
        module.__file__ = str(path)
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), str(path), "exec"), module.__dict__)
        M = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(GuardTests))
    print(f"CAPTURE-GUARD: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; "
          "stand-in host and capture, no capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
