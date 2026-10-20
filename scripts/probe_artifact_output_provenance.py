#!/usr/bin/env python3
"""Output-provenance controls using fresh owned copies; never real cleanup."""
from __future__ import annotations

import argparse
from dataclasses import asdict, fields, replace
import fcntl
import hashlib
import importlib.util
import inspect
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import ModuleType
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
import probe_artifact_cleanup as P

ROOT = Path(__file__).resolve().parent.parent
OBJECT = "scripts/artifact_output_provenance.py"
MUTATION = None
SEAMS = {
    "changed-digest": ('and before.sha256 != after.sha256,', 'and True,'),
    "successful-build": ('type(item.return_code) is int and item.return_code == 0', 'True'),
    "command-root": ('tuple(item.argv) == expected', 'True'),
    "recorder-pin": ('and replace(row.after, ctime_ns=item.ctime_ns) == item and row.recorder == recorder',
                     'and replace(row.after, ctime_ns=item.ctime_ns) == item'),
    "producer-pin": ('and row.producer == sources[row.producer.object]', 'and True'),
    "current-fact": ('and replace(row.after, ctime_ns=item.ctime_ns) == item and row.recorder == recorder',
                     'and row.recorder == recorder'),
    "tracked-alias": ('key(item.path) not in tracked_keys', 'True'),
    "closed-fields": ('type(value) is dict and set(value) == {f.name for f in fields(cls)}', 'type(value) is dict'),
    "byte-bound": ('need(type(raw) is bytes and 0 < len(raw) <= MAX_BYTES,',
                   'need(type(raw) is bytes and 0 < len(raw),'),
    "root-binding": ('owned.path == ROOT', 'True'),
    "root-mapping": ('need(stat.S_ISDIR(current.st_mode) and current.st_dev == owned.device\n'
                     '         and (current.st_dev, current.st_ino) == (opened.st_dev, opened.st_ino), "root mapping changed")',
                     'need(True, "root mapping changed")'),
    "return-root": ('    _root_guard(owned)\n    return Authority(sha(raw),',
                    '    return Authority(sha(raw),'),
    "profile-binding": ('parts[0] == "debug"', 'parts[0] in {"debug", "release"}'),
    "captured-binding": ('(not require_captured or bool(row.supporting_sources))', 'True'),
    "support-pin": ('all(sources[dependency.object] == dependency for dependency in row.supporting_sources)', 'True'),
    "support-objects": ('not supporting or tuple(row.object for row in supporting) == SUPPORTING_OBJECTS', 'True'),
    "census-class": ('if leaf not in CACHE_NAMES or not stat.S_ISREG(info.st_mode):', 'if not stat.S_ISREG(info.st_mode):'),
    "observe-unchanged": ('        if old is not None and old.sha256 == item.sha256:\n            continue\n', ''),
    "observe-tracked": ('        if key(item.path) in tracked_keys or item.links != 1:', '        if item.links != 1:'),
    "publish-lock": ('                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)\n', '                pass\n'),
    "publish-pins": ('    need(all(row.recorder == sources[OBJECT] and row.producer == sources[producer]\n'
                     '             and row.supporting_sources == tuple(sources[name] for name in SUPPORTING_OBJECTS)\n'
                     '             for row in rows), "publication requires current recorder, producer and support pins")',
                     '    need(True, "publication requires current recorder, producer and support pins")'),
    "publish-readback": ('            need(check is not None and check[0] == raw, "published ledger does not read back")',
                         '            need(True, "published ledger does not read back")'),
}
TARGETS = {
    "changed-digest": "test_unchanged_unowned_inputs_cannot_establish_generation",
    "successful-build": "test_only_successful_plain_zero_return_can_establish_generation",
    "command-root": "test_command_must_bind_target_and_intermediate_roots",
    "recorder-pin": "test_stale_recorder_decodes_but_has_no_current_authority",
    "producer-pin": "test_stale_producer_decodes_but_has_no_current_authority",
    "current-fact": "test_each_changed_current_fact_loses_authority",
    "tracked-alias": "test_tracked_alias_and_output_hardlink_are_protected",
    "closed-fields": "test_unknown_fields_are_refused_even_when_named_like_dict_methods",
    "byte-bound": "test_oversize_refuses_before_json_parse",
    "root-binding": "test_wrong_runtime_root_refuses_before_ledger_read",
    "root-mapping": "test_renamed_runtime_root_cannot_borrow_the_old_descriptor",
    "return-root": "test_root_changed_during_source_read_refuses_before_authority_returns",
    "profile-binding": "test_host_test_command_cannot_claim_release_or_cross_target_outputs",
    "captured-binding": "test_legacy_bytes_stay_exact_but_cannot_supply_captured_authority",
    "support-pin": "test_each_changed_support_source_loses_authority",
    "support-objects": "test_support_sources_have_closed_names_shapes_and_order",
    "census-class": "test_census_lists_only_output_class_files_in_path_order",
    "observe-unchanged": "test_observe_records_only_new_or_changed_outputs",
    "observe-tracked": "test_observe_excludes_tracked_aliases_and_hardlinks",
    "publish-lock": "test_held_lock_refuses_concurrent_publication",
    "publish-pins": "test_publication_requires_current_pins_before_any_write",
    "publish-readback": "test_silent_rename_failure_cannot_report_publication",
}


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.fixture = P.CohortTests(methodName="runTest")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root, self.a = self.fixture.root, self.fixture.m
        source = self.root / OBJECT
        text = (ROOT / OBJECT).read_text()
        if MUTATION:
            old, new = SEAMS[MUTATION]
            if text.count(old) != 1:
                raise RuntimeError("singular omission seam required: " + MUTATION)
            text = text.replace(old, new, 1)
        source.write_text(text)
        name = "provenance_fixture_" + hashlib.sha256(str(self.root).encode()).hexdigest()
        spec = importlib.util.spec_from_file_location(name, source)
        self.m = importlib.util.module_from_spec(spec)
        sys.modules[name] = self.m
        self.addCleanup(sys.modules.pop, name)
        spec.loader.exec_module(self.m)
        self.actor = "scripts/probe_c_engine.py"
        self.fixture.file(self.actor, b"owned producer source\n")
        self.output = "target/p4-system-12/c-engine-build/debug/incremental/a/s/dep-graph.bin"
        self.fixture.file(self.output, b"newly generated owned output")

    def source(self, name):
        data = (self.root / name).read_bytes()
        return self.m.Source(name, len(data), hashlib.sha256(data).hexdigest())

    def fact(self, name=None):
        name = name or self.output
        with self.a.OwnedRoot(self.root) as owned:
            parent, leaf = name.rsplit("/", 1)
            with owned.directory(parent) as directory:
                item, _ = owned.snapshot(directory, leaf, name, self.m.FILE_BYTES)
        return self.m.Fact(**asdict(item))

    def observation(self, **changes):
        root, test_filter = self.m.PRODUCERS[self.actor]
        argv = ("cargo", "test", "--offline", "--manifest-path", "target/p4-system-12/owned-input/Cargo.toml",
                "--target-dir", root, "--config", 'build.build-dir="' + root + '"',
                "--lib", test_filter, "--", "--nocapture")
        result = self.m.Observation("2026-10-20T00:00:00+00:00", self.source(OBJECT), self.source(self.actor),
                                    argv, "cargo fixture", 0, None, self.fact())
        return replace(result, **changes)

    def raw(self, *rows):
        return self.m.encode(self.m.Ledger(self.m.FORMAT, tuple(rows)))

    def save(self, *rows):
        data = self.raw(*rows)
        self.fixture.file(self.m.LEDGER, data)
        return data

    def authorize(self, current=None, tracked=frozenset(), *, require_captured=False):
        with self.a.OwnedRoot(self.root) as owned:
            return self.m.authorize(owned, (self.fact(),) if current is None else current,
                                    tracked_paths=tracked, require_captured=require_captured)

    def captured(self):
        self.fixture.file("scripts/artifact_cargo.py", b"owned Cargo command helper\n")
        return replace(self.observation(), supporting_sources=tuple(self.source(name) for name in self.m.SUPPORTING_OBJECTS))

    def captured_raw(self, row):
        return self.m.encode(self.m.Ledger(self.m.CAPTURE_FORMAT, (row,)))

    def pins(self):
        if not (self.root / "scripts/artifact_cargo.py").exists():
            self.fixture.file("scripts/artifact_cargo.py", b"owned Cargo command helper\n")
        return tuple(self.source(name) for name in self.m.SUPPORTING_OBJECTS)

    def publish(self, rows, present=None, producer=None):
        with self.a.OwnedRoot(self.root) as owned:
            return self.m.publish(owned, rows, producer or self.actor,
                                  frozenset(row.after.path for row in rows) if present is None else present)

    def outcome(self, function, *args, **kwargs):
        try:
            return "ok", function(*args, **kwargs)
        except (self.m.ProvenanceError, self.a.CleanupError, self.a.Boundary, OSError) as error:
            return "refused", str(error)

    def guest_row(self):
        actor, output = self.actor, self.output
        self.actor = "scripts/probe_c_guest_image.py";self.fixture.file(self.actor, b"owned guest producer\n")
        self.output = "target/p4-system-12/c-guest-image-build/debug/incremental/b/t/dep-graph.bin"
        self.fixture.file(self.output, b"guest output")
        try:
            return self.observation()
        finally:
            self.actor, self.output = actor, output

    def workspace_names(self):
        path = self.root / self.m.WORKSPACE
        return sorted(item.name for item in path.iterdir()) if path.exists() else []

    def test_census_lists_only_output_class_files_in_path_order(self):
        base = self.m.PRODUCERS[self.actor][0] + "/debug/incremental"
        self.fixture.file(base + "/a/s/query-cache.bin", b"q")
        self.fixture.file(base + "/a/s/other.bin", b"not an output class")
        self.fixture.file(base + "/a/s/deeper/work-products.bin", b"too deep")
        self.fixture.file(base + "/a/work-products.bin", b"too shallow")
        self.fixture.file(self.m.PRODUCERS[self.actor][0] + "/release/incremental/a/s/dep-graph.bin", b"release")
        (self.root / base / "a/s/work-products.bin").symlink_to(self.root / base / "a/s/query-cache.bin")
        with self.a.OwnedRoot(self.root) as owned:
            facts = self.m.census(owned, self.actor)
            self.assertEqual(self.m.census(owned, "scripts/probe_c_guest_image.py"), ())
        self.assertEqual([item.path for item in facts], [base + "/a/s/dep-graph.bin", base + "/a/s/query-cache.bin"])
        self.assertEqual(facts[1].sha256, hashlib.sha256(b"q").hexdigest())
        self.assertEqual(facts, tuple(self.fact(item.path) for item in facts))

    def test_observe_records_only_new_or_changed_outputs(self):
        new = self.fact()
        changed_path = self.output.replace("dep-graph", "query-cache")
        self.fixture.file(changed_path, b"old");old = self.fact(changed_path)
        self.fixture.file(changed_path, b"new");changed = self.fact(changed_path)
        kept_path = self.output.replace("dep-graph", "work-products")
        self.fixture.file(kept_path, b"kept");kept = self.fact(kept_path)
        touched = replace(kept, mtime_ns=kept.mtime_ns + 1, ctime_ns=kept.ctime_ns + 1)
        pins, argv = self.pins(), self.observation().argv
        disposition, value = self.outcome(self.m.observe, "2026-10-20T00:00:00+00:00", self.source(OBJECT), self.source(self.actor),
                                          argv, "cargo fixture", 0, pins, (old, kept), (new, changed, touched), tracked_paths=frozenset())
        self.assertEqual(disposition, "ok", value)
        rows, unclaimed = value
        self.assertEqual(([(row.after.path, row.before) for row in rows], unclaimed), ([(self.output, None), (changed_path, old)], 0))
        self.assertTrue(all(row.supporting_sources == pins and row.after in (new, changed) for row in rows))

    def test_observe_excludes_tracked_aliases_and_hardlinks(self):
        linked_path = self.output.replace("dep-graph", "query-cache")
        target = self.fixture.file(linked_path, b"linked");os.link(target, target.parent / "shared.bin")
        pins, argv = self.pins(), self.observation().argv
        rows, unclaimed = self.m.observe("2026-10-20T00:00:00+00:00", self.source(OBJECT), self.source(self.actor), argv,
                                         "cargo fixture", 0, pins, (), (self.fact(), self.fact(linked_path)),
                                         tracked_paths=frozenset({self.output.upper()}))
        self.assertEqual(([row.after.path for row in rows], unclaimed), ([], 2))

    def test_publish_creates_a_v2_ledger_atomically_and_reads_back(self):
        row = self.captured()
        result = self.publish((row,))
        self.assertEqual((result.written, result.records, result.added, result.previous_sha256), (True, 1, 1, None))
        raw = (self.root / self.m.LEDGER).read_bytes()
        self.assertEqual((self.m.decode(raw), hashlib.sha256(raw).hexdigest(), len(raw)),
                         (self.m.Ledger(self.m.CAPTURE_FORMAT, (row,)), result.ledger_sha256, result.byte_size))
        self.assertEqual(self.workspace_names(), [self.m.NAME, self.m.LOCK_NAME])
        self.assertEqual(self.authorize(require_captured=True).approved, frozenset({self.output}))

    def test_publish_merges_replaces_retires_and_keeps_other_producer_rows(self):
        legacy_present = self.observation()
        absent_path = self.output.replace("dep-graph", "work-products");self.fixture.file(absent_path, b"gone later")
        legacy_absent = self.observation(after=self.fact(absent_path))
        guest = self.guest_row()
        self.save(legacy_present, legacy_absent, guest)
        (self.root / absent_path).unlink()  # Only this test's disposable fixture.
        self.fixture.file(self.output, b"regenerated")
        replaced = replace(self.captured(), before=legacy_present.after, after=self.fact())
        new_path = self.output.replace("dep-graph", "query-cache");self.fixture.file(new_path, b"new")
        added = replace(self.captured(), after=self.fact(new_path))
        result = self.publish((replaced, added), present=frozenset({self.output, new_path}))
        self.assertEqual((result.written, result.records, result.added, result.replaced, result.retired, result.retained),
                         (True, 3, 1, 1, 1, 1))
        ledger = self.m.decode((self.root / self.m.LEDGER).read_bytes())
        self.assertEqual(ledger.format, self.m.CAPTURE_FORMAT)
        self.assertEqual([(row.after.path, bool(row.supporting_sources)) for row in ledger.outputs],
                         [(self.output, True), (new_path, True), (guest.after.path, False)])
        self.assertEqual((ledger.outputs[0], ledger.outputs[2]), (replaced, guest))

    def test_failed_publication_preserves_previous_ledger_and_retains_partial(self):
        row = self.observation();raw = self.save(row)
        new_path = self.output.replace("dep-graph", "query-cache");self.fixture.file(new_path, b"new")
        added = replace(self.captured(), after=self.fact(new_path))
        with patch.object(self.m.os, "rename", side_effect=OSError(5, "fixture rename failure")):
            disposition, detail = self.outcome(self.publish, (added,), frozenset({self.output, new_path}))
        self.assertEqual(disposition, "refused", detail);self.assertIn("previous ledger preserved", detail)
        self.assertEqual((self.root / self.m.LEDGER).read_bytes(), raw)
        partial = [name for name in self.workspace_names() if name.endswith(".tmp")]
        self.assertEqual((len(partial), self.m.WORKSPACE + "/" + partial[0] in detail), (1, True))
        self.assertEqual(self.m.decode((self.root / self.m.WORKSPACE / partial[0]).read_bytes()).format, self.m.CAPTURE_FORMAT)
        self.assertEqual(self.authorize().approved, frozenset({self.output}))

    def test_held_lock_refuses_concurrent_publication(self):
        row = self.captured()
        lock = self.fixture.file(self.m.WORKSPACE + "/" + self.m.LOCK_NAME, b"")
        with open(lock, "r+b") as held:
            fcntl.flock(held, fcntl.LOCK_EX)
            disposition, detail = self.outcome(self.publish, (row,))
        self.assertEqual(disposition, "refused", detail);self.assertIn("another publication", detail)
        self.assertEqual(self.workspace_names(), [self.m.LOCK_NAME])
        self.assertTrue(self.publish((row,)).written)

    def test_publication_requires_current_pins_before_any_write(self):
        row = self.captured()
        self.fixture.file("scripts/probe_c_guest_image.py", b"owned guest producer\n")
        stale = [(replace(row, supporting_sources=()), None),
                 (replace(row, recorder=replace(row.recorder, sha256="0" * 64)), None),
                 (replace(row, producer=replace(row.producer, sha256="0" * 64)), None),
                 (replace(row, supporting_sources=(replace(row.supporting_sources[0], sha256="0" * 64), row.supporting_sources[1])), None),
                 (row, "scripts/probe_c_guest_image.py")]
        refused = [self.outcome(self.publish, (bad,), None, producer)[0] == "refused" for bad, producer in stale]
        self.assertEqual(refused, [True] * len(stale))
        self.assertEqual(self.workspace_names(), [])

    def test_silent_rename_failure_cannot_report_publication(self):
        row = self.captured()
        with patch.object(self.m.os, "rename") as rename:
            disposition, detail = self.outcome(self.publish, (row,))
        self.assertEqual(rename.call_count, 1)
        self.assertEqual(disposition, "refused", detail);self.assertIn("does not read back", detail)
        self.assertFalse((self.root / self.m.LEDGER).exists())

    def test_unchanged_merge_writes_nothing_and_empty_capture_creates_no_ledger(self):
        self.pins()
        self.assertFalse(self.publish((), present=frozenset()).written)
        self.assertFalse((self.root / self.m.LEDGER).exists())
        row = self.captured();first = self.publish((row,));raw = (self.root / self.m.LEDGER).read_bytes()
        second = self.publish((row,))
        self.assertEqual((second.written, second.ledger_sha256, second.previous_sha256, second.replaced, second.records),
                         (False, first.ledger_sha256, first.ledger_sha256, 1, 1))
        self.assertEqual(((self.root / self.m.LEDGER).read_bytes(), self.workspace_names()), (raw, [self.m.NAME, self.m.LOCK_NAME]))

    def test_cold_copied_publisher_writes_and_rereads_a_v2_ledger(self):
        self.pins()
        code = ('import sys,json;sys.dont_write_bytecode=True;sys.path.insert(0,sys.argv[1]);'
                'import artifact_cleanup as A,artifact_output_provenance as O;'
                'owned=A.OwnedRoot(O.ROOT)\n'
                'with owned:\n'
                ' recorder,producer=O._source(owned,O.OBJECT),O._source(owned,sys.argv[2])\n'
                ' pins=tuple(O._source(owned,name) for name in O.SUPPORTING_OBJECTS);after=O.census(owned,sys.argv[2])\n'
                ' rows,unclaimed=O.observe("2026-10-20T00:00:00+00:00",recorder,producer,json.loads(sys.argv[3]),"cargo cold",0,pins,(),after,tracked_paths=frozenset())\n'
                ' p=O.publish(owned,rows,sys.argv[2],frozenset(item.path for item in after))\n'
                ' raw,ledger=O.load(owned);print(json.dumps([p.written,p.records,len(ledger.outputs),ledger.format,unclaimed]))')
        argv = json.dumps(list(self.observation().argv))
        result = subprocess.run([sys.executable, "-B", "-c", code, str(self.root / "scripts"), self.actor, argv],
                                cwd=ROOT.parent, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
        self.assertEqual((result.returncode, result.stdout), (0, '[true, 1, 1, "artifact-output-provenance-v2", 0]\n'), result.stderr)
        self.assertEqual(self.authorize(require_captured=True).approved, frozenset({self.output}))

    def test_versioned_support_sources_roundtrip_and_match_strict_authority(self):
        row = self.captured();raw = self.captured_raw(row)
        self.fixture.file(self.m.LEDGER, raw)
        self.assertEqual(self.m.decode(raw), self.m.Ledger(self.m.CAPTURE_FORMAT, (row,)))
        result = self.authorize(require_captured=True)
        self.assertEqual(result.approved, frozenset({self.output}))
        self.assertEqual(len(result.current_sources), 4)

    def test_legacy_bytes_stay_exact_but_cannot_supply_captured_authority(self):
        row = self.observation();raw = self.save(row)
        self.assertNotIn(b"supporting_sources", raw)
        self.assertEqual(self.m.encode(self.m.decode(raw)), raw)
        self.assertEqual(self.authorize().approved, frozenset({self.output}))
        self.assertEqual(self.authorize(require_captured=True).approved, frozenset())

    def test_mixed_v2_ledger_retains_legacy_rows_without_upgrading_their_authority(self):
        legacy = self.observation()
        captured = self.captured()
        path = self.output.replace("dep-graph.bin", "query-cache.bin")
        self.fixture.file(path, b"another newly observed output")
        captured = replace(captured, after=self.fact(path))
        ledger = self.m.Ledger(self.m.CAPTURE_FORMAT, (legacy, captured))
        raw = self.m.encode(ledger)
        self.fixture.file(self.m.LEDGER, raw)
        self.assertEqual(self.m.decode(raw), ledger)
        current = (legacy.after, captured.after)
        self.assertEqual(self.authorize(current).approved, frozenset({self.output, path}))
        self.assertEqual(self.authorize(current, require_captured=True).approved, frozenset({path}))

    def test_each_changed_support_source_loses_authority(self):
        row = self.captured();self.fixture.file(self.m.LEDGER, self.captured_raw(row))
        observed = []
        for support in row.supporting_sources:
            path = self.root / support.object;before = path.read_bytes()
            try:
                path.write_bytes(before + b"\n# changed support source\n")
                observed.append(self.authorize(require_captured=True).approved)
            finally:
                path.write_bytes(before)
        self.assertEqual(observed, [frozenset(), frozenset()])

    def test_support_sources_have_closed_names_shapes_and_order(self):
        row = self.captured();value = json.loads(self.captured_raw(row))
        first, second = value["outputs"][0]["supporting_sources"]
        bad = [None, "not an array", [first], [first, second, first], [second, first],
               [first, first], [{**first, "object": "scripts/unknown.py"}, second],
               [{**first, "byte_size": True}, second], [{**first, "extra": 0}, second]]
        refused = []
        for index, supports in enumerate(bad):
            value["outputs"][0]["supporting_sources"] = supports
            raw = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
            try:
                self.m.decode(raw)
            except self.m.ProvenanceError:
                refused.append(index)
        self.assertEqual(refused, list(range(len(bad))))

    def test_legacy_cannot_hide_supports_and_selection_is_plain_boolean(self):
        row = self.captured()
        with self.assertRaises(self.m.ProvenanceError):
            self.raw(row)
        raw = self.captured_raw(row).replace(self.m.CAPTURE_FORMAT.encode(), self.m.FORMAT.encode())
        with self.assertRaises(self.m.ProvenanceError):
            self.m.decode(raw)
        for selected in (0, 1, "true", None):
            with self.assertRaises(self.m.ProvenanceError):
                self.authorize(require_captured=selected)

    def test_new_file_observation_roundtrips_and_matches_current_sources(self):
        row = self.observation();raw = self.save(row)
        self.assertEqual(self.m.decode(raw).outputs, (row,))
        result = self.authorize()
        self.assertEqual(result.approved, frozenset({self.output}))
        self.assertEqual(result.ledger_sha256, hashlib.sha256(raw).hexdigest())
        self.assertEqual(len(result.current_sources), 2)

    def test_changed_digest_can_establish_an_observation(self):
        after = self.fact();before = replace(after, sha256="0" * 64)
        row = self.observation(before=before)
        self.assertEqual(self.m.decode(self.raw(row)).outputs, (row,))

    def test_unchanged_unowned_inputs_cannot_establish_generation(self):
        after = self.fact()
        before = replace(after, mtime_ns=after.mtime_ns - 1, ctime_ns=after.ctime_ns - 1)
        with self.assertRaisesRegex(self.m.ProvenanceError, "unchanged unowned input"):
            self.m.decode(self.raw(self.observation(before=before)))

    def test_only_successful_plain_zero_return_can_establish_generation(self):
        for code in (1, -1, False, None, "0"):
            with self.assertRaises(self.m.ProvenanceError):
                self.m.observation(json.loads(self.raw(self.observation(return_code=code)))["outputs"][0])

    def test_command_must_bind_target_and_intermediate_roots(self):
        row = self.observation()
        for index in (0, 1, 2, 3, 5, 6, 7, 8, 10):
            argv = list(row.argv);argv[index] = "unbound"
            with self.assertRaises(self.m.ProvenanceError):
                self.m.observation(json.loads(self.raw(replace(row, argv=tuple(argv))))["outputs"][0])

    def test_stale_recorder_decodes_but_has_no_current_authority(self):
        row = self.observation(recorder=replace(self.source(OBJECT), sha256="0" * 64))
        raw = self.save(row)
        self.assertEqual(self.m.decode(raw).outputs, (row,))
        self.assertEqual(self.authorize().approved, frozenset())

    def test_stale_producer_decodes_but_has_no_current_authority(self):
        row = self.observation();self.save(row)
        self.fixture.file(self.actor, b"changed producer source\n")
        self.assertEqual(self.authorize().approved, frozenset())

    def test_each_changed_current_fact_loses_authority(self):
        row = self.observation();self.save(row)
        for name in ("inode", "byte_size", "mtime_ns", "sha256", "mode"):
            value = "0" * 64 if name == "sha256" else getattr(row.after, name) + 1
            self.assertEqual(self.authorize((replace(row.after, **{name: value}),)).approved, frozenset())
        drifted = replace(row.after, ctime_ns=row.after.ctime_ns + 1)
        self.assertEqual(self.authorize((drifted,)).approved, frozenset({self.output}), "ctime alone is not a change")

    def test_tracked_alias_and_output_hardlink_are_protected(self):
        row = self.observation();self.save(row)
        self.assertEqual(self.authorize(tracked=frozenset({self.output.upper()})).approved, frozenset())
        self.assertEqual(self.authorize((replace(row.after, links=2),)).approved, frozenset())

    def test_unknown_fields_are_refused_even_when_named_like_dict_methods(self):
        value = json.loads(self.raw(self.observation()));value["outputs"][0]["items"] = "not a field"
        raw = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
        with self.assertRaisesRegex(self.m.ProvenanceError, "Observation fields"):
            self.m.decode(raw)

    def test_byte_count_and_record_bounds_refuse(self):
        raw = self.raw(self.observation())
        old = self.m.MAX_BYTES;self.m.MAX_BYTES = len(raw) - 1
        try:
            with self.assertRaisesRegex(self.m.ProvenanceError, "ledger byte bound"):
                self.m.decode(raw)
        finally:self.m.MAX_BYTES = old
        self.m.MAX_RECORDS = 0
        with self.assertRaisesRegex(self.m.ProvenanceError, "count bound"):
            self.m.decode(raw)
        self.m.MAX_RECORDS = 65536;self.m.MAX_RECORD_BYTES = 1
        with self.assertRaisesRegex(self.m.ProvenanceError, "record byte bound"):
            self.m.decode(raw)

    def test_oversize_refuses_before_json_parse(self):
        raw = self.raw(self.observation());self.m.MAX_BYTES = len(raw) - 1
        with patch.object(self.m.json, "loads", wraps=json.loads) as parse:
            with self.assertRaisesRegex(self.m.ProvenanceError, "ledger byte bound"):
                self.m.decode(raw)
            self.assertEqual(parse.call_count, 0)

    def test_wrong_runtime_root_refuses_before_ledger_read(self):
        with self.a.OwnedRoot(self.root) as owned:
            self.m.ROOT = self.fixture.base
            with self.assertRaisesRegex(self.m.ProvenanceError, "runtime root differs"):
                self.m.load(owned)

    def test_absent_ledger_supplies_no_approved_outputs(self):
        self.assertEqual(self.authorize().approved, frozenset())
        self.assertIsNone(self.authorize().ledger_sha256)

    def test_renamed_runtime_root_cannot_borrow_the_old_descriptor(self):
        row = self.observation();self.save(row);moved = self.fixture.base / "moved-runtime"
        with self.a.OwnedRoot(self.root) as owned:
            self.root.rename(moved);self.root.mkdir()
            try:
                with self.assertRaisesRegex(self.m.ProvenanceError, "root mapping changed"):
                    self.m.authorize(owned, (row.after,), tracked_paths=frozenset())
            finally:
                self.root.rmdir();moved.rename(self.root)

    def test_guest_producer_matches_its_closed_debug_output_contract(self):
        self.actor = "scripts/probe_c_guest_image.py";self.fixture.file(self.actor, b"owned guest producer\n")
        self.output = "target/p4-system-12/c-guest-image-build/debug/incremental/b/t/work-products.bin"
        self.fixture.file(self.output, b"new owned guest build output");self.save(self.observation())
        self.assertEqual(self.authorize().approved, frozenset({self.output}))

    def test_root_changed_during_source_read_refuses_before_authority_returns(self):
        row = self.observation();self.save(row);moved = self.fixture.base / "moved-during-read"
        with self.a.OwnedRoot(self.root) as owned:
            original = owned.snapshot
            renamed = False
            def snapshot(*args, **kwargs):
                nonlocal renamed
                result = original(*args, **kwargs)
                if args[2] == OBJECT:
                    self.root.rename(moved);self.root.mkdir();renamed = True
                return result
            try:
                with patch.object(owned, "snapshot", side_effect=snapshot):
                    with self.assertRaisesRegex(self.m.ProvenanceError, "root mapping changed"):
                        self.m.authorize(owned, (row.after,), tracked_paths=frozenset())
            finally:
                if renamed:self.root.rmdir();moved.rename(self.root)

    def test_host_test_command_cannot_claim_release_or_cross_target_outputs(self):
        row = self.observation()
        for middle in ("release", "wasm32-unknown-unknown/debug"):
            path = self.output.replace("/debug/incremental/", "/" + middle + "/incremental/")
            with self.subTest(middle=middle), self.assertRaisesRegex(self.m.ProvenanceError, "output class"):
                self.m.decode(self.raw(replace(row, after=replace(row.after, path=path))))

    def test_arbitrary_cache_shaped_input_namespace_is_refused(self):
        row = self.observation()
        for path in ("target/retained-fixture-inputs/debug/incremental/a/s/dep-graph.bin",
                     "target/p4-system-12/c-engine-build/debug/input-fixtures/dep-graph.bin",
                     "target/p4-system-12/c-engine-build/debug/incremental/a/s/deeper/dep-graph.bin"):
            with self.subTest(path=path), self.assertRaisesRegex(self.m.ProvenanceError, "output class"):
                self.m.decode(self.raw(replace(row, after=replace(row.after, path=path))))

    def test_duplicate_noncanonical_and_nonfinite_json_refuse(self):
        raw = self.raw(self.observation())
        for data in (b'{"format":"x",' + raw[1:], b" " + raw, raw.replace(b'"return_code":0', b'"return_code":NaN')):
            with self.subTest(data=data[:30]), self.assertRaises(self.m.ProvenanceError):self.m.decode(data)

    def test_source_and_file_shapes_are_closed_and_bounded(self):
        row = self.observation()
        for changed in (replace(row, producer=replace(row.producer, object="scripts/unknown.py")),
                        replace(row, recorder=replace(row.recorder, byte_size=True)),
                        replace(row, after=replace(row.after, links=2)),
                        replace(row, after=replace(row.after, byte_size=self.m.FILE_BYTES + 1)),
                        replace(row, created_utc="2026-10-20T00:00:00")):
            with self.subTest(changed=changed), self.assertRaises(self.m.ProvenanceError):self.m.decode(self.raw(changed))

    def test_duplicate_output_or_case_alias_refuses(self):
        row = self.observation()
        with self.assertRaisesRegex(self.m.ProvenanceError, "alias collision"):self.m.decode(self.raw(row, row))
        current = (row.after, replace(row.after, path=row.after.path.upper()))
        with self.assertRaisesRegex(self.m.ProvenanceError, "current alias collision"):self.authorize(current)

    def test_cross_volume_current_fact_refuses(self):
        with self.assertRaisesRegex(self.m.ProvenanceError, "crosses volume"):
            self.authorize((replace(self.fact(), device=self.root.stat().st_dev + 1),))

    def test_ledger_symlink_is_not_followed(self):
        self.save(self.observation());path = self.root / self.m.LEDGER
        original = path.read_bytes();path.unlink();target = self.fixture.file("target/retained-ledger.bin", original)
        path.symlink_to(target)
        with self.assertRaises((self.a.CleanupError, OSError)):
            self.authorize()
        self.assertEqual(target.read_bytes(), original)

    def test_cold_copied_reader_needs_no_git_or_producer_execution(self):
        code = ('import sys;sys.dont_write_bytecode=True;sys.path.insert(0,sys.argv[1]);'
                'import artifact_cleanup as A,artifact_output_provenance as O;'
                'from pathlib import Path;'
                'owned=A.OwnedRoot(O.ROOT);'
                '\nwith owned: raw,ledger=O.load(owned);print(len(ledger.outputs))')
        for raw in (self.raw(self.observation()), self.captured_raw(self.captured())):
            self.fixture.file(self.m.LEDGER, raw)
            result = subprocess.run([sys.executable, "-B", "-c", code, str(self.root / "scripts")],
                                    cwd=ROOT.parent, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
            self.assertEqual((result.returncode, result.stdout), (0, "1\n"), result.stderr)


def cargo_contract():
    """Reproduce Cargo's container-level answer without deleting a fixture input."""
    base = ROOT / "target/artifact-provenance-controls";base.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="cargo-contract-", dir=base) as td:
        root = Path(td);(root / "src").mkdir();(root / "src/lib.rs").write_text("pub fn owned() {}\n")
        (root / "Cargo.toml").write_text('[package]\nname="cleanup-contract-fixture"\nversion="0.0.0"\nedition="2021"\n[workspace]\n')
        names = ["target/debug/incremental/a/s/dep-graph.bin", "target/debug/input-fixtures/dep-graph.bin",
                 "target/retained-fixture-inputs/debug/incremental/a/s/dep-graph.bin"]
        for name in names:
            path = root / name;path.parent.mkdir(parents=True, exist_ok=True);path.write_bytes(name.encode())
        before = {name: (root / name).read_bytes() for name in names}
        env = {k: v for k, v in os.environ.items() if not k.startswith(("CARGO_", "RUSTC_", "RUSTFLAGS", "RUSTDOC"))}
        env.update(CARGO_HOME=str(root / "cargo-home"), TMPDIR=str(ROOT / "target/tmp"), CARGO_TERM_COLOR="never")
        result = subprocess.run(["cargo", "clean", "--dry-run", "--verbose", "--offline", "--profile", "dev"],
                                cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if len(result.stdout) + len(result.stderr) > 262144:raise RuntimeError("Cargo diagnostic output bound")
        listed = {line.removeprefix(str(root) + "/") for line in result.stdout.decode().splitlines()}
        if result.returncode or not set(names[:2]) <= listed or names[2] in listed:
            raise RuntimeError("Cargo public dry-run no longer matches this recorded container observation")
        if before != {name: (root / name).read_bytes() for name in names}:raise RuntimeError("dry-run changed inputs")
        print("Cargo dry-run: cache-shaped toy and profile input listed; three inputs exact; no real cleanup")


def contract(revision, emit):
    """Report an interface of the current or an exact committed codec module."""
    import artifact_cleanup as A
    import artifact_output_provenance as O
    if revision:
        if not re.fullmatch(r"[0-9a-f]{7,40}", revision):
            raise ValueError("contract revision must be a Git object abbreviation")
        A.tracked_paths(ROOT)
        raw = A._git(ROOT, ["show", revision + ":" + OBJECT], O.SOURCE_BYTES)
        name = "codec_contract_" + hashlib.sha256(raw).hexdigest()
        module = ModuleType(name);module.__file__ = str(ROOT / OBJECT)
        sys.modules[name] = module
        try:
            exec(compile(raw, OBJECT, "exec"), module.__dict__)
            emit(module, False)
        finally:
            sys.modules.pop(name, None)
    else:
        emit(O, True)


def emit_support_contract(module, current):
    print("OUTPUT-SUPPORT: " + json.dumps(dict(
        support_field="supporting_sources" in {field.name for field in fields(module.Observation)},
        captured_selector="require_captured" in inspect.signature(module.authorize).parameters,
        fixed_sources=getattr(module, "SUPPORTING_OBJECTS", ())), sort_keys=True))


def emit_publication_contract(module, current):
    """Name the capture/publication interface; with current code, also the ledger on disk."""
    report = {name: callable(getattr(module, name, None)) for name in ("census", "observe", "merge", "publish")}
    if current:
        import artifact_cleanup as A
        with A.OwnedRoot(ROOT) as owned:
            saved = module.load(owned)
        report["ledger"] = None if saved is None else dict(
            format=saved[1].format, records=len(saved[1].outputs), byte_size=len(saved[0]),
            captured=sum(1 for row in saved[1].outputs if row.supporting_sources),
            sha256=hashlib.sha256(saved[0]).hexdigest())
    print("OUTPUT-PUBLICATION: " + json.dumps(report, sort_keys=True))


def main():
    global MUTATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(SEAMS))
    parser.add_argument("--cargo-contract", action="store_true")
    parser.add_argument("--support-contract", action="store_true")
    parser.add_argument("--publication-contract", action="store_true")
    parser.add_argument("--revision")
    args = parser.parse_args();MUTATION = args.mutation
    if args.support_contract or args.publication_contract:
        if MUTATION or args.cargo_contract or (args.support_contract and args.publication_contract):
            parser.error("an interface report cannot use another mode")
        contract(args.revision, emit_support_contract if args.support_contract else emit_publication_contract);return 0
    if args.revision:parser.error("revision requires an interface report")
    if args.cargo_contract:
        if MUTATION:parser.error("Cargo observation cannot use a source omission")
        cargo_contract();return 0
    suite = (unittest.TestSuite([ProvenanceTests(TARGETS[MUTATION])]) if MUTATION else
             unittest.defaultTestLoader.loadTestsFromTestCase(ProvenanceTests))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"output provenance: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
