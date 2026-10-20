#!/usr/bin/env python3
"""Attempt-journal controls in owned copies; no cache deletion."""
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
import stat
import subprocess
import unittest
from unittest.mock import patch

import probe_artifact_cleanup as P

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "scripts/artifact_cleanup_journal.py"
MUTATION = None
SEAMS = {
    "plan-binding": ('        need(record["plan_sha256"] == digest(A.encode_plan(plan)), "plan digest binding")\n', ''),
    "intent-sequence": ('            need(progress.pending is None and index == expected, "intent sequence")\n', ''),
    "terminal": ('''        need(progress.pending is None and progress.removed == total and record["stage"] == "verified"
             and record["failure"] is None, "incomplete terminal success")
''', ''),
    "approved-range": ('''            need(type(approved) is list and 0 < len(approved) <= MAX_APPROVED
                 and all(type(index) is int and 0 <= index < count for index in approved)
                 and approved == sorted(set(approved)), "approved index set")
''', ''),
    "exclusive": ('os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_APPEND',
                  'os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW | os.O_APPEND'),
    "parent": ('''        current = self._owned.path.lstat()
        opened = os.fstat(self._owned.fd)
        need(stat.S_ISDIR(current.st_mode) and (current.st_dev, current.st_ino)
             == (opened.st_dev, opened.st_ino), "root mapping changed")
        with self._owned.directory(self._plan.workdir) as fresh:
            now, held = os.fstat(fresh), os.fstat(self._parent)
            need((now.st_dev, now.st_ino) == (held.st_dev, held.st_ino), "workspace mapping changed")
            yield fresh
''', '        yield self._parent\n'),
    "file": ('                self._file_guard(parent)\n', ''),
    "barrier": ('                _flush(self._descriptor)\n', ''),
    "poison": ('            self._broken = True\n', ''),
    "byte-bound": ('    need(type(raw) is bytes and len(raw) <= JOURNAL_BYTES, "journal byte bound")\n', ''),
    "terminal-tail": ('        need(progress.result is None or not tail, "tail after terminal")\n', ''),
}
TARGETS = {
    "plan-binding": "test_changed_plan_digest_refuses",
    "intent-sequence": "test_skipped_intent_refuses",
    "terminal": "test_incomplete_success_refuses",
    "exclusive": "test_existing_empty_journal_is_preserved",
    "parent": "test_renamed_workspace_refuses_before_append",
    "file": "test_external_file_change_refuses_before_append",
    "barrier": "test_each_accepted_record_has_a_flush_barrier",
    "poison": "test_zero_write_failure_poison_prevents_retry",
    "byte-bound": "test_oversized_bytes_refuse_before_framing",
    "terminal-tail": "test_tail_after_terminal_is_not_success",
    "approved-range": "test_selection_bound_begin_shape_refuses",
}


class JournalTests(unittest.TestCase):
    def setUp(self):
        self.fixture = P.CohortTests("test_plan_is_frozen_and_census_does_not_change_data")
        self.fixture.setUp(); self.addCleanup(self.fixture.doCleanups)
        self.a = self.fixture.m
        self.root = self.fixture.root
        self.work = self.fixture.work
        self.object = "scripts/artifact_cleanup_journal.py"
        copied = self.root / self.object
        text = SOURCE.read_text()
        if MUTATION:
            before, after = SEAMS[MUTATION]
            if text.count(before) != 1: raise RuntimeError("singular journal guard required: " + MUTATION)
            text = text.replace(before, after, 1)
        copied.write_text(text)
        name = "journal_fixture_" + hashlib.sha256(str(self.root).encode()).hexdigest()
        spec = importlib.util.spec_from_file_location(name, copied)
        self.j = importlib.util.module_from_spec(spec)
        sys.modules[name] = self.j; self.addCleanup(sys.modules.pop, name)
        spec.loader.exec_module(self.j)
        self.j.A = self.a
        for leaf in ("dep-graph.bin", "query-cache.bin"):
            self.fixture.file("target/debug/incremental/owned/session/" + leaf, b"retained fixture cache")
        self.plan = self.fixture.plan()
        self.a.publish_plan(self.root, self.plan)
        self.path = self.root / self.work / self.j.NAME

    def start(self):
        return self.j.start(self.root, self.work, actor_object=self.object)

    def outcome(self, function, *args, **kwargs):
        try: return "ok", function(*args, **kwargs)
        except (self.a.CleanupError, self.a.Boundary, OSError, ValueError, TypeError) as error:
            return "refused", getattr(error, "reason", str(error))

    def frames(self):
        if not self.path.exists():
            with self.start(): pass
        return [json.loads(line) for line in self.path.read_bytes().splitlines()]

    def raw(self, records):
        return b"".join(self.j.encode(record) for record in records)

    def parsed(self):
        return self.j.inspect(self.root, self.work)[1]

    def test_complete_records_do_not_attest_or_remove_actual_files(self):
        with self.start() as writer:
            for index in range(len(self.plan.candidates)):
                writer.intent(index); writer.removed(index)
            writer.finish("complete", "verified")
        result = self.parsed()
        report = self.j.report(self.plan, result)
        self.assertEqual(report["recorded_state"], "recorded-complete")
        self.assertEqual(report["recorded_unlink_returns"], 2)
        self.assertEqual(report["recorded_paths"], [f.path for f in self.plan.candidates])
        self.assertIn("not attested", report["claim_scope"])
        for fact in self.plan.candidates:
            self.assertEqual((self.root / fact.path).read_bytes(), b"retained fixture cache")

    def test_selection_bound_attempt_follows_approved_indices_only(self):
        binding = ("ab" * 32, (1,))
        with self.j.start(self.root, self.work, actor_object=self.object, selection=binding) as writer:
            self.assertEqual(self.outcome(writer.intent, 0)[0], "refused")
            writer.intent(1); writer.removed(1)
            self.assertEqual(self.outcome(writer.intent, 0)[0], "refused")
            writer.finish("complete", "verified")
        result = self.parsed()
        report = self.j.report(self.plan, result)
        self.assertEqual((result.progress.header.selection_sha256, result.progress.header.approved), ("ab" * 32, (1,)))
        self.assertEqual((report["recorded_state"], report["recorded_paths"], report["recorded_unlink_returns"]),
                         ("recorded-complete", [self.plan.candidates[1].path], 1))
        self.assertEqual(report["planned_bytes_for_recorded_returns"], self.plan.candidates[1].byte_size)
        for fact in self.plan.candidates:
            self.assertEqual((self.root / fact.path).read_bytes(), b"retained fixture cache")

    def test_selection_bound_begin_shape_refuses(self):
        begin = json.loads(json.dumps(self.frames()[0]))
        begin.update(format=self.j.SELECTED_FORMAT, selection_sha256="ab" * 32, approved=[0, 1])
        self.assertEqual(self.outcome(self.j.decode, self.raw([begin]), self.plan)[0], "ok")
        variants = []
        for tag in ("digest", "empty", "range", "order", "duplicate", "type", "legacy-fields"):
            record = json.loads(json.dumps(begin))
            if tag == "digest": record["selection_sha256"] = "bad"
            elif tag == "empty": record["approved"] = []
            elif tag == "range": record["approved"] = [0, 2]
            elif tag == "order": record["approved"] = [1, 0]
            elif tag == "duplicate": record["approved"] = [0, 0]
            elif tag == "type": record["approved"] = [0, True]
            else: record["format"] = self.j.FORMAT
            variants.append(self.outcome(self.j.decode, self.raw([record]), self.plan)[0])
        self.assertEqual(variants, ["refused"] * 7)

    def test_selection_bound_complete_requires_every_approved_return(self):
        begin = json.loads(json.dumps(self.frames()[0]))
        begin.update(format=self.j.SELECTED_FORMAT, selection_sha256="ab" * 32, approved=[0, 1])
        raw = self.raw([begin, dict(kind="intent", index=0), dict(kind="removed", index=0),
                        dict(kind="finish", result="complete", stage="verified", failure=None)])
        self.assertEqual(self.outcome(self.j.decode, raw, self.plan)[0], "refused")
        raw = self.raw([begin, dict(kind="intent", index=0), dict(kind="removed", index=0),
                        dict(kind="intent", index=1), dict(kind="removed", index=1),
                        dict(kind="finish", result="complete", stage="verified", failure=None)])
        self.assertEqual(self.j.decode(raw, self.plan).progress.result, "complete")

    def test_pending_intent_and_missing_finish_remain_incomplete(self):
        with self.start() as writer: writer.intent(0)
        result = self.parsed()
        self.assertEqual((result.progress.removed, result.progress.pending, result.progress.result), (0, 0, None))
        self.assertEqual(self.j.report(self.plan, result)["recorded_state"], "incomplete")

    def test_failed_and_interrupted_records_keep_stage_and_error(self):
        begin = self.frames()
        for kind in ("failed", "interrupted"):
            raw = self.raw([*begin, dict(kind="intent", index=0),
                            dict(kind="finish", result=kind, stage="unlink",
                                 failure=dict(kind="OSError", errno=5, detail="owned fixture failure"))])
            result = self.j.decode(raw, self.plan)
            self.assertEqual((result.progress.result, result.progress.stage), (kind, "unlink"))
            self.assertEqual(result.progress.failure.errno, 5)
            self.assertEqual(result.progress.pending, 0)

    def test_empty_and_torn_begin_have_no_established_binding(self):
        for raw in (b"", b'{"kind":"beg'):
            result = self.j.decode(raw, self.plan)
            self.assertIsNone(result.progress.header)
            self.assertEqual(result.tail_bytes, len(raw))
            self.assertEqual(self.j.report(self.plan, result)["recorded_state"], "unestablished")

    def test_torn_return_is_not_counted(self):
        raw = self.raw([*self.frames(), dict(kind="intent", index=0)]) + b'{"index":0,"kind":"remov'
        result = self.j.decode(raw, self.plan)
        self.assertEqual((result.progress.removed, result.progress.pending), (0, 0))
        self.assertGreater(result.tail_bytes, 0)
        self.assertEqual(result.tail_sha256, hashlib.sha256(raw.rsplit(b"\n", 1)[1]).hexdigest())

    def test_changed_plan_digest_refuses(self):
        records = self.frames(); records[0]["plan_sha256"] = "0" * 64
        self.assertEqual(self.outcome(self.j.decode, self.raw(records), self.plan)[0], "refused")

    def test_skipped_intent_refuses(self):
        raw = self.raw([*self.frames(), dict(kind="intent", index=1)])
        self.assertEqual(self.outcome(self.j.decode, raw, self.plan)[0], "refused")

    def test_incomplete_success_refuses(self):
        raw = self.raw([*self.frames(), dict(kind="finish", result="complete", stage="verified", failure=None)])
        self.assertEqual(self.outcome(self.j.decode, raw, self.plan)[0], "refused")

    def test_tail_after_terminal_is_not_success(self):
        records = self.frames()
        for index in range(len(self.plan.candidates)):
            records += [dict(kind="intent", index=index), dict(kind="removed", index=index)]
        records.append(dict(kind="finish", result="complete", stage="verified", failure=None))
        self.assertEqual(self.outcome(self.j.decode, self.raw(records) + b"unexplained", self.plan)[0], "refused")

    def test_closed_canonical_records_reject_malformed_inputs(self):
        begin = self.frames()[0]
        variants = []
        for tag in ("extra", "count-bool", "source-path", "source-digest", "time", "format"):
            record = json.loads(json.dumps(begin))
            if tag == "extra": record["extra"] = 1
            elif tag == "count-bool": record["candidates"] = True
            elif tag == "source-path": record["actor"]["object"] = "../foreign.py"
            elif tag == "source-digest": record["actor"]["sha256"] = "bad"
            elif tag == "time": record["created_utc"] = "not-time"
            else: record["format"] = "unknown"
            variants.append(self.raw([record]))
        variants += [b'{"kind":"begin","kind":"begin"}\n', b"\xff\n", b"{}\n", b"NaN\n",
                     json.dumps(begin, sort_keys=True).encode() + b"\n", b"\n"]
        for raw in variants:
            with self.subTest(raw=raw[:40]):
                self.assertEqual(self.outcome(self.j.decode, raw, self.plan)[0], "refused")

    def test_illegal_sequences_fail_before_any_append(self):
        with self.start() as writer:
            before = self.path.read_bytes()
            for function, args in ((writer.intent, (True,)), (writer.intent, (-1,)), (writer.intent, (2,)),
                                   (writer.removed, (0,)), (writer.intent, (1,)),
                                   (writer.finish, ("complete", "verified"))):
                with self.subTest(function=function.__name__, args=args):
                    self.assertEqual(self.outcome(function, *args)[0], "refused")
                    self.assertEqual(self.path.read_bytes(), before)
            writer.intent(0)
            before = self.path.read_bytes()
            self.assertEqual(self.outcome(writer.intent, 0)[0], "refused")
            self.assertEqual(self.outcome(writer.removed, 1)[0], "refused")
            self.assertEqual(self.path.read_bytes(), before)

    def test_existing_empty_journal_is_preserved(self):
        self.path.write_bytes(b"")
        def attempt():
            with self.start(): pass
        self.assertEqual(self.outcome(attempt)[0], "refused")
        self.assertEqual(self.path.read_bytes(), b"")

    def test_renamed_workspace_refuses_before_append(self):
        current = self.path.parent; moved = current.parent / "moved"
        manager = self.start(); writer = manager.__enter__()
        before = self.path.read_bytes()
        try:
            current.rename(moved); current.mkdir()
            result = self.outcome(writer.intent, 0)
            observed = (moved / self.j.NAME).read_bytes()
        finally:
            current.rmdir(); moved.rename(current)
            manager.__exit__(None, None, None)
        self.assertEqual(result[0], "refused", result)
        self.assertEqual(observed, before)

    def test_external_file_change_refuses_before_append(self):
        with self.start() as writer:
            with self.path.open("ab") as stream: stream.write(b"foreign append")
            before = self.path.read_bytes()
            self.assertEqual(self.outcome(writer.intent, 0)[0], "refused")
            self.assertEqual(self.path.read_bytes(), before)

    def test_plan_change_and_hardlink_refuse_before_append(self):
        with self.start() as writer:
            alias = self.fixture.base / "shared-journal"
            os.link(self.path, alias)
            before = self.path.read_bytes()
            self.assertEqual(self.outcome(writer.intent, 0)[0], "refused")
            self.assertEqual(alias.read_bytes(), before)
        alias.unlink()
        self.path.unlink()  # Metadata-only owned fixture; no cache path.
        with self.start() as writer:
            plan_path = self.path.parent / "plan.json"
            plan_path.write_bytes(plan_path.read_bytes() + b" ")
            before = self.path.read_bytes()
            self.assertEqual(self.outcome(writer.intent, 0)[0], "refused")
            self.assertEqual(self.path.read_bytes(), before)

    def test_each_accepted_record_has_a_flush_barrier(self):
        actual = os.fsync; calls = []
        with self.start() as writer:
            def observed(fd): calls.append(fd); return actual(fd)
            with patch.object(self.j.os, "fsync", side_effect=observed): writer.intent(0)
            self.assertGreater(len(calls), 0)
            self.assertEqual(writer.progress.pending, 0)

    def test_short_writes_finish_one_frame(self):
        actual = os.write
        with self.start() as writer:
            with patch.object(self.j.os, "write", side_effect=lambda fd, data: actual(fd, data[:3])):
                writer.intent(0)
        self.assertEqual(self.parsed().progress.pending, 0)

    def test_zero_write_failure_poison_prevents_retry(self):
        with self.start() as writer:
            before = self.path.read_bytes()
            with patch.object(self.j.os, "write", side_effect=OSError(5, "owned write failure")):
                self.assertEqual(self.outcome(writer.intent, 0)[0], "refused")
            self.assertEqual(self.outcome(writer.intent, 0)[0], "refused")
            self.assertEqual(self.path.read_bytes(), before)

    def test_partial_write_preserves_torn_prefix(self):
        actual = os.write; calls = 0
        with self.start() as writer:
            def partial(fd, data):
                nonlocal calls
                calls += 1
                if calls == 1: return actual(fd, data[:5])
                raise OSError(5, "owned partial write")
            with patch.object(self.j.os, "write", side_effect=partial):
                self.assertEqual(self.outcome(writer.intent, 0)[0], "refused")
        result = self.parsed()
        self.assertEqual(result.progress.removed, 0)
        self.assertEqual(result.tail_bytes, 5)

    def test_fsync_failure_and_interruption_preserve_recorded_prefix(self):
        with self.start() as writer:
            with patch.object(self.j.os, "fsync", side_effect=OSError(5, "owned barrier failure")):
                self.assertEqual(self.outcome(writer.intent, 0)[0], "refused")
            self.assertEqual(writer.progress.pending, None)
        self.assertEqual(self.parsed().progress.pending, 0)  # Present bytes are not an fsync attestation.
        self.path.unlink()
        with self.assertRaises(KeyboardInterrupt):
            with self.start() as writer:
                writer.intent(0)
                raise KeyboardInterrupt()
        self.assertEqual(self.parsed().progress.pending, 0)

    def test_darwin_requires_full_fsync_and_propagates_failure(self):
        calls = []
        with patch.object(self.j.sys, "platform", "darwin"), \
             patch.object(self.j.fcntl, "F_FULLFSYNC", 12345, create=True), \
             patch.object(self.j.fcntl, "fcntl", side_effect=lambda fd, flag: calls.append((fd, flag))):
            with self.start() as writer: writer.intent(0)
        self.assertTrue(calls)
        self.assertTrue(all(flag == 12345 for _, flag in calls))
        self.path.unlink()
        with patch.object(self.j.sys, "platform", "darwin"), \
             patch.object(self.j.fcntl, "F_FULLFSYNC", None, create=True):
            self.assertEqual(self.outcome(lambda: self.start().__enter__())[0], "refused")
        with self.start() as writer:
            with patch.object(self.j.sys, "platform", "darwin"), \
                 patch.object(self.j.fcntl, "F_FULLFSYNC", 12345, create=True), \
                 patch.object(self.j.fcntl, "fcntl", side_effect=OSError(5, "owned full-sync failure")):
                self.assertEqual(self.outcome(writer.intent, 0)[0], "refused")
            self.assertIsNone(writer.progress.pending)
            self.assertEqual(self.outcome(writer.intent, 0)[0], "refused")

    def test_close_error_still_closes_every_owned_descriptor(self):
        actual_open, actual_close = os.open, os.close
        active = {}; generation = 0; selected = None; failed = False
        def opened(path, *args, **kwargs):
            nonlocal generation, selected
            descriptor = actual_open(path, *args, **kwargs)
            generation += 1; active[descriptor] = generation
            if path == self.j.NAME: selected = generation
            return descriptor
        def closed(descriptor):
            nonlocal failed
            token = active.pop(descriptor)
            actual_close(descriptor)
            if token == selected and not failed:
                failed = True
                raise OSError(5, "owned close failure after close")
        def attempt():
            with self.start(): pass
        with patch.object(self.j.os, "open", side_effect=opened) as wrapper, \
             patch.object(self.j.os, "supports_dir_fd", self.j.os.supports_dir_fd | {wrapper}), \
             patch.object(self.j.os, "close", side_effect=closed):
            result = self.outcome(attempt)
        self.assertEqual(result[0], "refused", result)
        self.assertTrue(failed)
        self.assertEqual(active, {})

    def test_frame_and_record_population_bounds_are_named(self):
        begin = self.raw(self.frames())
        variants = [(begin + b"x" * self.j.RECORD_BYTES, "tail byte bound"),
                    (b"x" * self.j.RECORD_BYTES + b"\n", "frame byte bound"),
                    (begin * (2 * len(self.plan.candidates) + 3), "record count bound")]
        for raw, reason in variants:
            with self.subTest(reason=reason):
                result = self.outcome(self.j.decode, raw, self.plan)
                self.assertEqual(result[0], "refused")
                self.assertIn(reason, result[1])

    def test_oversized_bytes_refuse_before_framing(self):
        raw = self.raw(self.frames()) + b"x" * self.j.JOURNAL_BYTES
        result = self.outcome(self.j.decode, raw, self.plan)
        self.assertEqual(result[0], "refused")
        self.assertIn("journal byte bound", result[1])

    def test_reader_does_not_invoke_git_or_require_current_actor_source(self):
        with self.start() as writer:
            writer.finish("failed", "preflight", self.j.Failure("CleanupError", None, "observed refusal"))
        (self.root / self.object).unlink()  # Historical recorder identity remains in the record.
        with patch.object(self.j.A, "_git", side_effect=AssertionError("reader must not invoke Git")), \
             patch.object(subprocess, "Popen", side_effect=AssertionError("reader must not launch")):
            result = self.parsed()
        self.assertEqual(result.progress.result, "failed")

    def test_cli_reads_copied_runtime_from_valid_parent_without_git(self):
        with self.start() as writer: writer.intent(0)
        cold = self.fixture.base / "cold"
        for name in ("scripts/artifact_cleanup.py", self.object, self.work + "/plan.json", self.work + "/" + self.j.NAME):
            target = cold / name; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self.root / name, target)
        self.assertFalse((cold / ".git").exists())
        result = subprocess.run([sys.executable, *(["-O"] if sys.flags.optimize else []), "-B",
                                 str(cold / self.object), "--workdir", self.work], cwd=ROOT,
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual((report["recorded_state"], report["unresolved_intent"]), ("incomplete", 0))
        self.assertIn("not attested", report["claim_scope"])


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    MUTATION = parser.parse_args().mutation
    if set(TARGETS) != set(SEAMS): raise RuntimeError("each guard needs a targeted control")
    suite = (unittest.TestSuite([JournalTests(TARGETS[MUTATION])]) if MUTATION else
             unittest.defaultTestLoader.loadTestsFromTestCase(JournalTests))
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(suite)
    print(f"CLEANUP-JOURNAL: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; metadata only, no cache unlink")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
