#!/usr/bin/env python3
"""Artifact cohort controls in owned on-volume copies; no real cache deletion."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from dataclasses import FrozenInstanceError, replace
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unicodedata
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "scripts/artifact_cleanup.py"
MUTATION = None
SEAMS = {
    "git-volume-before-read": ('    need(marker.st_dev == device, "Git marker crosses repository volume")\n', ''),
    "volume-before-open": ('                if before.st_dev != self.device:\n                    raise Boundary(name, "volume")\n', ''),
    "release-strays": ('f.path for f in retained if any(beneath(f.path, prefix)',
                        'f.path for f in (*retained, *selected) if any(beneath(f.path, prefix)'),
    "tracked-ownership": ('_ownership_key(fact.path) not in tracked_keys', 'True'),
    "hash-budget": ('                    charge("hash_bytes", info.st_size)\n', ''),
    "root-binding": ('isinstance(root, Path) and root.resolve() == ROOT', 'isinstance(root, Path)'),
    "plan-shape": ('            need(key not in value, "duplicate JSON field")\n', ''),
    "exclusive-output": ('os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW',
                          'os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW'),
    "head-inventory": ('''for command in (["ls-files", "--cached", "--full-name", "-z"],
                    ["ls-tree", "-r", "--name-only", "-z", "HEAD"]):''',
                       '''for command in (["ls-files", "--cached", "--full-name", "-z"],):'''),
    "directory-recheck": ('''                for parent, part, device, inode, child in reversed(parents):
                    after = os.stat(part, dir_fd=parent, follow_symlinks=False)
                    opened = os.fstat(child)
                    need(stat.S_ISDIR(after.st_mode) and (after.st_dev, after.st_ino)
                         == (opened.st_dev, opened.st_ino) == (device, inode),
                         "directory changed after open", "stale")
                    try:
                        os.stat(".git", dir_fd=child, follow_symlinks=False)
                    except FileNotFoundError:
                        pass
                    else:
                        raise CleanupError("stale", "Git boundary appeared during operation")
''', '                pass\n'),
}
TARGETS = {
    "git-volume-before-read": "test_foreign_git_marker_refuses_before_public_git_reads",
    "volume-before-open": "test_declared_foreign_scope_is_refused_before_directory_open",
    "release-strays": "test_release_cache_is_not_a_retained_stray",
    "tracked-ownership": "test_tracked_case_equivalent_paths_and_hardlinks_are_retained",
    "hash-budget": "test_each_census_limit_refuses_without_publication",
    "root-binding": "test_foreign_runtime_root_refuses_before_git_read_or_write",
    "plan-shape": "test_closed_plan_codec_rejects_malformed_data",
    "exclusive-output": "test_exclusive_publication_preserves_existing_foreign_bytes",
    "head-inventory": "test_git_head_and_index_union_and_environment_isolation",
    "directory-recheck": "test_directory_rename_during_read_never_publishes_a_plan",
}

FAKE_GIT = '''#!/usr/bin/env python3
import os,sys,time
from pathlib import Path
root=Path(os.environ['CLEANUP_TEST_ROOT']);args=sys.argv[1:]
if any(k.startswith('GIT_') for k in os.environ):raise SystemExit(98)
mode=os.environ.get('CLEANUP_TEST_GIT_MODE','normal')
if mode=='overflow':sys.stdout.write('x'*100000);raise SystemExit(0)
if mode=='stderr':sys.stderr.write('fixture warning');raise SystemExit(0)
if mode=='wait':time.sleep(3);raise SystemExit(0)
if 'rev-parse' in args:
 if '--show-toplevel' in args:print(root)
 elif '--absolute-git-dir' in args:print(root/'.git')
 elif '--git-common-dir' in args:print('.git')
 else:raise SystemExit(9)
elif 'ls-files' in args:sys.stdout.buffer.write((root/'fixture-index').read_bytes())
elif 'ls-tree' in args:sys.stdout.buffer.write((root/'fixture-head').read_bytes())
else:raise SystemExit(9)
'''


class CohortTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/artifact-cleanup-controls"
        base.mkdir(parents=True, exist_ok=True)
        self.temporary = TemporaryDirectory(dir=base)
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "runtime"
        self.source = self.root / "scripts/artifact_cleanup.py"
        self.source.parent.mkdir(parents=True)
        text = SOURCE.read_text()
        if MUTATION:
            before, after = SEAMS[MUTATION]
            if text.count(before) != 1:
                raise RuntimeError("singular guard target required: " + MUTATION)
            text = text.replace(before, after, 1)
        self.source.write_text(text)
        module_name = "cleanup_fixture_" + hashlib.sha256(str(self.root).encode()).hexdigest()
        spec = importlib.util.spec_from_file_location(module_name, self.source)
        self.m = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = self.m
        self.addCleanup(sys.modules.pop, module_name)
        spec.loader.exec_module(self.m)
        self.real_inventory = self.m.tracked_paths
        self.tracked = set()
        self.inventory_patch = patch.object(self.m, "tracked_paths", side_effect=lambda root: frozenset(self.tracked))
        self.inventory_patch.start()
        self.addCleanup(self.inventory_patch.stop)
        self.work = "target/artifact-cleanup/review"

    def file(self, path, data=b"fixture"):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return target

    def plan(self, **kwargs):
        return self.m.make_plan(self.root, workdir=self.work, **kwargs)

    def outcome(self, function, *args, **kwargs):
        try:
            return "ok", function(*args, **kwargs)
        except (self.m.CleanupError, self.m.Boundary, OSError) as error:
            return "refused", str(error)

    def fake_git(self):
        (self.root / ".git").mkdir(exist_ok=True)
        self.file("fixture-index", b"")
        self.file("fixture-head", b"")
        executable = self.base / "bin/git"
        executable.parent.mkdir(exist_ok=True)
        executable.write_text(FAKE_GIT)
        executable.chmod(0o755)
        return {"PATH": str(executable.parent) + os.pathsep + os.environ["PATH"],
                "CLEANUP_TEST_ROOT": str(self.root)}

    def test_named_cache_class_and_unknown_inputs_are_separate(self):
        selected = {
            "target/debug/incremental/a/s/dep-graph.bin",
            "target/release/incremental/b/s/query-cache.bin",
            ".app-data/target/wasm32/debug/incremental/c/s/work-products.bin",
        }
        retained = {
            ".app-data/cargo-home/source/tests/data.bin",
            "target/debug/incremental/a/s/unknown.bin",
            "target/debug/deps/reference.log",
            "target/release/result.bin",
            "target/refs/retained.log",
        }
        for name in selected | retained:
            self.file(name)
        p = self.plan()
        self.assertEqual({f.path for f in p.candidates}, selected)
        self.assertEqual({f.path for f in p.retained}, retained)
        self.assertEqual(p.strays, ("target/debug/deps/reference.log", "target/release/result.bin"))
        self.assertEqual(self.m.check_plan(self.root, p).disposition, "matched")

    def test_release_cache_is_not_a_retained_stray(self):
        cache = "target/release/incremental/a/s/dep-graph.bin"
        log = "target/release/compiler.log"
        self.file(cache); self.file(log)
        p = self.plan()
        self.assertEqual(p.strays, (log,))
        self.assertEqual(tuple(f.path for f in p.candidates), (cache,))

    def test_plan_is_frozen_and_census_does_not_change_data(self):
        self.file("target/debug/incremental/a/s/dep-graph.bin")
        before = {p.relative_to(self.root).as_posix(): p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        p = self.plan()
        with self.assertRaises(FrozenInstanceError):
            p.device = 0
        with self.assertRaises(FrozenInstanceError):
            p.candidates[0].sha256 = "0" * 64
        self.assertEqual(self.m.decode_plan(self.m.encode_plan(p)), p)
        after = {p.relative_to(self.root).as_posix(): p.read_bytes()
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_closed_plan_codec_rejects_malformed_data(self):
        path = "target/debug/incremental/a/s/dep-graph.bin"
        self.file(path)
        raw = self.m.encode_plan(self.plan())
        valid = json.loads(raw)
        variants = [bytearray(raw), b"", b"x" * (self.m.PLAN_BYTES + 1),
                    raw.replace(b'"artifact-cohort-v1"', b'"artifact-cohort-v1", "format":"artifact-cohort-v1"', 1)]
        for change in ("extra", "boolean", "absolute", "overlap", "missing"):
            doc = json.loads(raw)
            if change == "extra": doc["unknown"] = True
            elif change == "boolean": doc["candidates"][0]["byte_size"] = True
            elif change == "absolute": doc["candidates"][0]["path"] = "/outside.bin"
            elif change == "overlap": doc["retained"] = doc["candidates"]
            else: del doc["instrument"]
            variants.append(json.dumps(doc).encode())
        for n, value in enumerate(variants):
            with self.subTest(case=n):
                with self.assertRaises(self.m.CleanupError): self.m.decode_plan(value)
        self.assertEqual(json.loads(self.m.encode_plan(self.m.decode_plan(raw))), valid)

    def test_changed_and_new_data_make_saved_cohort_stale(self):
        cache = self.file("target/debug/incremental/a/s/dep-graph.bin", b"old")
        retained = self.file("target/refs/reference.log", b"reference")
        p = self.plan()
        cache.write_bytes(b"different")
        self.assertEqual(self.m.check_plan(self.root, p).disposition, "stale")
        p = self.plan(); retained.write_bytes(b"changed")
        self.assertEqual(self.m.check_plan(self.root, p).disposition, "stale")
        p = self.plan(); self.file("target/debug/incremental/a/s/query-cache.bin")
        self.assertEqual(self.m.check_plan(self.root, p).disposition, "stale")

    def test_stale_reason_names_the_first_differing_member(self):
        cache = self.file("target/debug/incremental/a/s/dep-graph.bin", b"old")
        retained = self.file("target/refs/reference.log", b"reference")
        p = self.plan(); retained.write_bytes(b"changed!!")
        finding = self.m.check_plan(self.root, p)
        self.assertEqual(finding.disposition, "stale")
        self.assertIn("retained: 0 gone, 0 new, 1 changed; first changed target/refs/reference.log (", finding.reason)
        self.assertIn("sha256", finding.reason)
        cache.unlink()  # Only this test's disposable fixture; the instrument has no delete API.
        self.assertIn("candidates: 1 gone, 0 new, 0 changed; first gone target/debug/incremental/a/s/dep-graph.bin",
                      self.m.check_plan(self.root, p).reason)
        self.assertEqual(self.m.difference(p, p), "")

    def test_after_state_observes_fixture_removal_without_attribution(self):
        cache = self.file("target/release/incremental/a/s/dep-graph.bin")
        retained = self.file("target/release/reference.log")
        p = self.plan()
        cache.unlink()  # Only this test's disposable fixture; the instrument has no delete API.
        result = self.m.check_plan(self.root, p, phase="after")
        self.assertEqual(result.disposition, "matched")
        self.assertIn("no process attribution", result.reason)
        retained.unlink()
        self.assertEqual(self.m.check_plan(self.root, p, phase="after").disposition, "stale")

    def test_tracked_case_equivalent_paths_and_hardlinks_are_retained(self):
        name = "target/caché/debug/incremental/a/s/dep-graph.bin"
        self.file(name)
        self.tracked.add(unicodedata.normalize("NFD", name.upper()))
        self.assertEqual(self.plan().candidates, ())
        path = self.file("target/debug/incremental/b/s/query-cache.bin")
        os.link(path, path.parent / "shared.bin")
        self.assertEqual(self.plan().candidates, ())

    def test_symlinks_and_nested_git_are_exclusions(self):
        outside = self.base / "outside.bin"; outside.write_bytes(b"protected")
        link = self.root / "target/link.bin"; link.parent.mkdir(parents=True); link.symlink_to(outside)
        self.file("target/nested/.git", b"fixture marker, not a repository")
        self.file("target/nested/debug/incremental/a/s/dep-graph.bin")
        p = self.plan()
        self.assertEqual(p.candidates, ())
        self.assertEqual({(e.path, e.reason) for e in p.excluded},
                         {("target/link.bin", "symlink"), ("target/nested", "nested-git")})
        self.assertEqual(outside.read_bytes(), b"protected")

    def test_foreign_volume_is_not_traversed(self):
        folder = self.root / "target/foreign"; folder.mkdir(parents=True)
        inode = folder.stat().st_ino
        actual = os.stat
        def changed(*args, **kwargs):
            info = actual(*args, **kwargs)
            if info.st_ino != inode: return info
            names = ("st_dev", "st_ino", "st_mode", "st_nlink", "st_size", "st_mtime_ns", "st_ctime_ns")
            values = {name: getattr(info, name) for name in names}; values["st_dev"] += 1
            return SimpleNamespace(**values)
        with patch.object(self.m.os, "stat", side_effect=changed) as wrapped, \
             patch.object(self.m.os, "supports_dir_fd", self.m.os.supports_dir_fd | {wrapped}):
            p = self.plan()
        self.assertEqual(p.excluded, (self.m.Exclusion("target/foreign", "volume"),))

    def test_deep_scope_symlink_never_reads_target_metadata(self):
        outside = self.base / "outside-data/subdir"; outside.mkdir(parents=True)
        protected = outside / "reference.log"; protected.write_bytes(b"protected input")
        link = self.root / "target/alias"; link.parent.mkdir(parents=True)
        link.symlink_to(outside.parent, target_is_directory=True)
        actual = os.stat
        unsafe_calls = []
        def observed(path, *args, **kwargs):
            if isinstance(path, str) and path.startswith("target/alias/") and kwargs.get("dir_fd") is not None:
                unsafe_calls.append(path)
            return actual(path, *args, **kwargs)
        with patch.object(self.m.os, "stat", side_effect=observed) as wrapped, \
             patch.object(self.m.os, "supports_dir_fd", self.m.os.supports_dir_fd | {wrapped}):
            p = self.plan(scopes=("target/alias/subdir",))
        self.assertEqual(unsafe_calls, [])
        self.assertEqual(p.excluded, (self.m.Exclusion("target/alias", "symlink"),))
        self.assertEqual(protected.read_bytes(), b"protected input")

    def test_declared_foreign_scope_is_refused_before_directory_open(self):
        folder = self.root / "target/foreign"; folder.mkdir(parents=True)
        inode = folder.stat().st_ino
        actual_stat, actual_open = os.stat, os.open
        foreign_opens = []
        def foreign(*args, **kwargs):
            info = actual_stat(*args, **kwargs)
            if info.st_ino != inode: return info
            names = ("st_dev", "st_ino", "st_mode", "st_nlink", "st_size", "st_mtime_ns", "st_ctime_ns")
            values = {name: getattr(info, name) for name in names}; values["st_dev"] += 1
            return SimpleNamespace(**values)
        def observed(path, *args, **kwargs):
            if path == "foreign": foreign_opens.append(path)
            return actual_open(path, *args, **kwargs)
        with patch.object(self.m.os, "stat", side_effect=foreign) as wrapped_stat, \
             patch.object(self.m.os, "open", side_effect=observed) as wrapped_open, \
             patch.object(self.m.os, "supports_dir_fd", self.m.os.supports_dir_fd | {wrapped_stat, wrapped_open}):
            disposition, value = self.outcome(self.plan, scopes=("target/foreign",))
        self.assertEqual(foreign_opens, [])
        self.assertEqual(disposition, "ok", value)
        self.assertEqual(value.excluded, (self.m.Exclusion("target/foreign", "volume"),))

    def test_disjoint_scopes_share_one_ancestor_exclusion(self):
        outside = self.base / "outside-data"; outside.mkdir()
        link = self.root / "target/alias"; link.parent.mkdir(parents=True)
        link.symlink_to(outside, target_is_directory=True)
        p = self.plan(scopes=("target/alias/one", "target/alias/two"))
        self.assertEqual(p.excluded, (self.m.Exclusion("target/alias", "symlink"),))
        self.assertEqual(self.m.decode_plan(self.m.encode_plan(p)), p)
        self.assertEqual(list(outside.iterdir()), [])

    def test_bad_scopes_and_workspace_symlink_cannot_write_elsewhere(self):
        self.file("target/debug/incremental/a/s/dep-graph.bin")
        for scopes in (("../outside",), ("target//bad",), ("target", "target/data"),
                       ("target/artifact-cleanup/review",)):
            with self.subTest(scopes=scopes), self.assertRaises(self.m.CleanupError):
                self.plan(scopes=scopes)
        with self.assertRaises(self.m.CleanupError):
            self.m.make_plan(self.root, workdir="target/debug")
        p = self.plan()
        outside = self.base / "outside-work"; outside.mkdir()
        (self.root / "target/artifact-cleanup").symlink_to(outside, target_is_directory=True)
        self.assertEqual(self.outcome(self.m.publish_plan, self.root, p)[0], "refused")
        self.assertEqual(list(outside.iterdir()), [])

    def test_descriptors_close_even_if_one_close_reports_error(self):
        (self.root / "target/data").mkdir(parents=True)
        actual_open, actual_close = os.open, os.close
        opened, closed = set(), set()
        failed = False
        def observed_open(*args, **kwargs):
            descriptor = actual_open(*args, **kwargs); opened.add(descriptor); return descriptor
        def observed_close(descriptor):
            nonlocal failed
            actual_close(descriptor); closed.add(descriptor)
            if not failed:
                failed = True
                raise OSError("fixture close failure after close")
        with patch.object(self.m.os, "open", side_effect=observed_open) as wrapped, \
             patch.object(self.m.os, "supports_dir_fd", self.m.os.supports_dir_fd | {wrapped}), \
             patch.object(self.m.os, "close", side_effect=observed_close):
            with self.assertRaises(OSError):
                with self.m.OwnedRoot(self.root) as owned, owned.directory("target/data"):
                    pass
        self.assertTrue(failed)
        self.assertEqual(opened, closed)

    def test_depth_refuses_before_traversal_or_workspace_creation(self):
        self.file("target/data/subdir/reference.log")
        deep = "target/artifact-cleanup/" + "/".join(["x"] * 95)
        for operation in (
            lambda: self.m.make_plan(self.root, workdir=deep),
            lambda: self.plan(scopes=("target/" + "/".join(["x"] * 96),)),
        ):
            with patch.object(self.m, "tracked_paths") as inventory:
                with self.assertRaises(self.m.CleanupError): operation()
                inventory.assert_not_called()
        with self.m.OwnedRoot(self.root) as owned, patch.object(self.m.os, "mkdir") as mkdir:
            with self.assertRaises(self.m.CleanupError):
                with owned.directory(deep, create=True): pass
            mkdir.assert_not_called()
        opened = []
        original = self.m.OwnedRoot.directory
        def observed(owner, path, **kwargs):
            opened.append(path)
            return original(owner, path, **kwargs)
        with patch.object(self.m.OwnedRoot, "directory", new=observed):
            with self.assertRaises(self.m.CleanupError):
                self.plan(scopes=("target/data",), limits=replace(self.m.Limits(), depth=2))
        self.assertNotIn("target/data/subdir", opened)
        self.assertFalse((self.root / "target/artifact-cleanup").exists())

    def test_unserializable_api_plan_is_refused_before_io(self):
        p = self.plan()
        invalid = replace(p, device=object())
        with patch.object(self.m, "make_plan") as census:
            self.assertEqual(self.m.check_plan(self.root, invalid).disposition, "refused")
            census.assert_not_called()

    def test_each_census_limit_refuses_without_publication(self):
        cache = self.file("target/debug/incremental/a/s/dep-graph.bin", b"two")
        for name, value in (("records", 0), ("directories", 0), ("entries", 0),
                            ("depth", 0), ("file_bytes", 1), ("hash_bytes", 1)):
            with self.subTest(limit=name):
                result = self.outcome(self.plan, limits=replace(self.m.Limits(), **{name: value}))
                self.assertEqual(result[0], "refused", result)
        self.assertEqual(cache.read_bytes(), b"two")
        self.assertFalse((self.root / self.work).exists())
        with self.assertRaises(self.m.CleanupError):
            self.plan(limits=replace(self.m.Limits(), records=True))

    def test_disappearing_file_is_not_silently_an_empty_default_scope(self):
        name = "target/debug/incremental/a/s/dep-graph.bin"
        cache = self.file(name)
        original = self.m.OwnedRoot.snapshot
        def disappear(owner, parent, leaf, path, *args, **kwargs):
            if path == name: cache.unlink()
            return original(owner, parent, leaf, path, *args, **kwargs)
        with patch.object(self.m.OwnedRoot, "snapshot", new=disappear):
            self.assertEqual(self.outcome(self.plan)[0], "refused")

    def test_directory_rename_during_read_never_publishes_a_plan(self):
        name = "target/data/observed.log"
        self.file(name)
        original = self.m.OwnedRoot.snapshot
        def rename(owner, parent, leaf, path, *args, **kwargs):
            result = original(owner, parent, leaf, path, *args, **kwargs)
            if path == name: (self.root / "target/data").rename(self.root / "target/moved")
            return result
        with patch.object(self.m.OwnedRoot, "snapshot", new=rename):
            result = self.outcome(self.plan, scopes=("target/data",))
        self.assertEqual(result[0], "refused", result)

    def test_exclusive_publication_preserves_existing_foreign_bytes(self):
        self.file("target/debug/incremental/a/s/dep-graph.bin")
        p = self.plan()
        foreign = self.file(self.work + "/plan.json", b"foreign plan")
        result = self.outcome(self.m.publish_plan, self.root, p)
        self.assertEqual(result[0], "refused", result)
        self.assertEqual(foreign.read_bytes(), b"foreign plan")

    def test_plan_publication_roundtrip_and_source_drift(self):
        self.file("target/debug/incremental/a/s/dep-graph.bin")
        p = self.plan(); self.m.publish_plan(self.root, p)
        saved = self.m.load_plan(self.root, self.work)
        self.assertEqual(saved, p)
        self.assertEqual(self.m.check_plan(self.root, saved).disposition, "matched")
        self.source.write_bytes(self.source.read_bytes() + b"\n# changed fixture source\n")
        self.assertEqual(self.m.check_plan(self.root, saved).disposition, "stale")

    def test_foreign_runtime_root_refuses_before_git_read_or_write(self):
        elsewhere = self.base / "other"; elsewhere.mkdir()
        with patch.object(self.m, "tracked_paths", return_value=frozenset()) as inventory:
            self.outcome(self.m.make_plan, elsewhere, workdir=self.work)
            self.assertEqual(inventory.call_count, 0)
        self.assertFalse((elsewhere / "target").exists())

    def test_git_head_and_index_union_and_environment_isolation(self):
        env = self.fake_git()
        index, head = "target/index.bin", "target/head.bin"
        self.file("fixture-index", (index + "\0").encode())
        self.file("fixture-head", (head + "\0").encode())
        with patch.dict(os.environ, {**env, "GIT_DIR": "poisoned", "GIT_INDEX_FILE": "poisoned"}):
            self.assertEqual(self.real_inventory(self.root), frozenset({index, head}))

    def test_foreign_git_marker_refuses_before_public_git_reads(self):
        self.fake_git()
        original = Path.lstat
        def foreign(path, *args, **kwargs):
            info = original(path, *args, **kwargs)
            if path == self.root / ".git":
                return SimpleNamespace(st_mode=info.st_mode, st_dev=info.st_dev + 1)
            return info
        with patch.object(Path, "lstat", new=foreign), patch.object(self.m, "_git", return_value=b"") as public:
            disposition, detail = self.outcome(self.real_inventory, self.root)
        self.assertEqual(public.call_count, 0)
        self.assertEqual(disposition, "refused", detail)
        self.assertIn("Git marker crosses repository volume", detail)

    def test_bounded_git_reads_refuse_overflow_stderr_and_timeout(self):
        env = self.fake_git()
        for mode in ("overflow", "stderr"):
            with self.subTest(mode=mode), patch.dict(os.environ, {**env, "CLEANUP_TEST_GIT_MODE": mode}):
                self.assertEqual(self.outcome(self.m._git, self.root, ["rev-parse"], 16)[0], "refused")
        with patch.dict(os.environ, {**env, "CLEANUP_TEST_GIT_MODE": "wait"}), \
             patch.object(self.m.time, "monotonic", side_effect=[0, 31]):
            self.assertEqual(self.outcome(self.m._git, self.root, ["rev-parse"])[0], "refused")

    def test_copied_cli_binds_its_root_and_has_no_delete_mode(self):
        cache = self.file("target/debug/incremental/a/s/dep-graph.bin")
        command = [sys.executable, *( ["-O"] if sys.flags.optimize else []), "-B", str(self.source)]
        unavailable = subprocess.run(command + ["--plan", "--workdir", self.work], cwd=ROOT,
                                     capture_output=True, text=True, timeout=20)
        self.assertEqual(unavailable.returncode, 2, unavailable.stdout + unavailable.stderr)
        self.assertIn("runtime root lacks", unavailable.stdout)
        env = dict(os.environ, **self.fake_git())
        for flag, expected in (("--plan", 0), ("--check", 0), ("--check-after", 1), ("--delete", 2)):
            with self.subTest(flag=flag):
                result = subprocess.run(command + [flag, "--workdir", self.work], cwd=ROOT,
                                        env=env, capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        self.assertEqual(cache.read_bytes(), b"fixture")


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    MUTATION = parser.parse_args().mutation
    if set(TARGETS) != set(SEAMS): raise RuntimeError("every guard needs its own control")
    suite = (unittest.TestSuite([CohortTests(TARGETS[MUTATION])]) if MUTATION else
             unittest.defaultTestLoader.loadTestsFromTestCase(CohortTests))
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    print(f"ARTIFACT-COHORT: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; owned fixtures, no real cleanup")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
