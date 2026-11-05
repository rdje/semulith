#!/usr/bin/env python3
"""Controls for `scripts/artifact_cleanup_orphans.py` on an owned scratch tree; no real cache is touched and no census runs (`ARTIFACT-CLEANUP.29`)."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys
import tempfile
import types
import unittest

import artifact_cleanup_orphans as O

REPO = Path(__file__).resolve().parent.parent
MUTATIONS = {
    "anchor": ("    if newest >= anchor:\n        return None\n", ""),
    "shape": ("if not CRATE.fullmatch(crate.name) or not entries or not all(SESSION.fullmatch(name) for name in entries):", "if False:"),
    "kind": ("if info.st_dev != device or not (stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)):", "if False:"),
    "tracked": ("if relative in tracked:", "if False:"),
    "recheck": ('if current is None or current.identity != row["identity"]:', "if False:"),
    "census": ("    verdict = host_census(root)\n", '    verdict = type("V", (), {"verdict": "skipped"})\n'),
    "fixtures": ("if here.relative_to(root).as_posix().startswith(OWNED_FIXTURES):", "if False:"),
}
M = O
RECORD = "# ARTIFACT CLEANUP — last run\n\n- `2026-11-05T00:16Z`: removed things.\n"
ANCHOR = 1793837760  # 2026-11-05T00:16:00Z
OLD, NEW = ANCHOR - 86400, ANCHOR + 60
WORK = "target/artifact-cleanup/AC"


class Green:
    verdict = "handoff: OK"


def green(_root):
    return Green


def stopped(_root):
    raise M.Refused("project work is running")


class OrphanTests(unittest.TestCase):
    def setUp(self):
        parent = REPO / "target/tmp"
        parent.mkdir(parents=True, exist_ok=True)
        self.scratch = tempfile.TemporaryDirectory(prefix="orphans-", dir=parent)
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name).resolve()
        (self.root / "docs").mkdir()
        (self.root / "docs/ARTIFACT_CLEANUP.md").write_text(RECORD)
        (self.root / "target").mkdir()

    def crate(self, relative="target/debug/incremental/core-abc123", when=OLD):
        """A crate-hash directory of cargo's shape: one finished session and its lock, every member dated `when`."""
        crate = self.root / relative
        session = crate / "s-hb0ad-working"
        session.mkdir(parents=True)
        for name, data in (("dep-graph.bin", b"bin"), ("0abc.o", b"object"), ("metadata.rmeta", b"meta")):
            (session / name).write_bytes(data)
        (crate / "s-hb0ad-working.lock").write_bytes(b"")
        self.date(crate, when)
        return crate

    def date(self, crate, when):
        for current, directories, names in os.walk(crate, topdown=False):
            for name in names + directories:
                os.utime(Path(current) / name, (when, when), follow_symlinks=False)
        os.utime(crate, (when, when))

    def planned(self, tracked=frozenset()):
        return M.plan(self.root, WORK, tracked)

    def test_the_anchor_is_the_last_recorded_act(self):
        self.assertEqual(M.anchor_ns(self.root), ANCHOR * 1_000_000_000)

    def test_an_unreadable_record_refuses(self):
        (self.root / "docs/ARTIFACT_CLEANUP.md").write_text("no act here\n")
        with self.assertRaises(M.Refused):
            M.anchor_ns(self.root)

    def test_an_orphan_goes_whole_files_locks_and_directories(self):
        crate = self.crate()
        report = self.planned()
        self.assertEqual((report["orphans"], report["files"], report["bytes"]), (1, 4, 13))
        done = M.delete(self.root, WORK, frozenset(), green)
        self.assertEqual((done["disposition"], done["removed"], done["removed_bytes"], done["residue"], done["kept"]), ("complete", 1, 13, 0, []))
        self.assertFalse(crate.exists())
        self.assertTrue(crate.parent.is_dir())

    def test_one_member_younger_than_the_act_keeps_the_directory(self):
        crate = self.crate()
        os.utime(crate / "s-hb0ad-working/0abc.o", (NEW, NEW))
        self.date(crate / "s-hb0ad-working", OLD)
        os.utime(crate / "s-hb0ad-working/0abc.o", (NEW, NEW))
        self.assertEqual(self.planned()["orphans"], 0)

    def test_a_directory_not_of_cargos_shape_is_not_the_class(self):
        crate = self.crate()
        (crate / "notes.txt").write_text("someone's")
        self.date(crate, OLD)
        self.assertEqual(self.planned()["orphans"], 0)

    def test_a_symlink_inside_keeps_the_directory(self):
        crate = self.crate()
        os.symlink("/nonexistent", crate / "s-hb0ad-working/link")
        os.utime(crate / "s-hb0ad-working/link", (OLD, OLD), follow_symlinks=False)
        self.date(crate / "s-hb0ad-working", OLD)
        self.assertEqual(self.planned()["orphans"], 0)

    def test_a_tracked_member_keeps_the_directory(self):
        self.crate()
        tracked = frozenset({"target/debug/incremental/core-abc123/s-hb0ad-working/0abc.o"})
        self.assertEqual(self.planned(tracked)["orphans"], 0)

    def test_the_cleanup_tools_own_fixtures_are_not_a_cargo_root(self):
        self.crate("target/artifact-cleanup-0070/smoke-inputs/debug/incremental/core-abc123")
        self.assertEqual(self.planned()["orphans"], 0)

    def test_a_build_after_the_plan_keeps_the_directory_and_names_it(self):
        crate = self.crate()
        self.planned()
        (crate / "s-hb0ad-working/0abc.o").write_bytes(b"rebuilt, larger")
        os.utime(crate / "s-hb0ad-working/0abc.o", (OLD, OLD))
        done = M.delete(self.root, WORK, frozenset(), green)
        self.assertEqual((done["removed"], done["kept"]), (0, ["target/debug/incremental/core-abc123"]))
        self.assertTrue(crate.exists())

    def test_running_work_refuses_before_anything_goes(self):
        crate = self.crate()
        self.planned()
        with self.assertRaises(M.Refused):
            M.delete(self.root, WORK, frozenset(), stopped)
        self.assertTrue(crate.exists())
        self.assertFalse((self.root / WORK / M.JOURNAL).exists())

    def test_a_plan_is_never_reused(self):
        self.crate()
        self.planned()
        with self.assertRaises(FileExistsError):
            self.planned()
        M.delete(self.root, WORK, frozenset(), green)
        with self.assertRaises(M.Refused):
            M.delete(self.root, WORK, frozenset(), green)

    def test_the_work_directory_stays_where_the_tools_keep_theirs(self):
        with self.assertRaises(M.Refused):
            M.plan(self.root, "target/elsewhere", frozenset())
        with self.assertRaises(M.Refused):
            M.plan(self.root, "target/artifact-cleanup/../escape", frozenset())


def main():
    global M
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(MUTATIONS))
    args = parser.parse_args()
    if args.mutation:
        path = REPO / "scripts/artifact_cleanup_orphans.py"
        source = path.read_text()
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("mutation no longer selects exactly one guard")
        module = types.ModuleType("mutated_artifact_cleanup_orphans")
        module.__file__ = str(path)
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), str(path), "exec"), module.__dict__)
        M = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(OrphanTests))
    print(f"ARTIFACT-ORPHANS: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; owned scratch tree, no real cache and no census")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
