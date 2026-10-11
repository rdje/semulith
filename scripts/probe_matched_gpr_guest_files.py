#!/usr/bin/env python3
"""Real-file source/image retention controls; authentication is not image validity."""
from __future__ import annotations

import argparse
from dataclasses import FrozenInstanceError, replace
import gc
from pathlib import Path
import subprocess
import sys
import types
import unittest
from unittest import mock
import weakref

import matched_gpr_files as Q
import probe_matched_gpr_files as P


class GuestFileTests(unittest.TestCase):
    # Reuse only the public-graph/on-volume fixture authoring, not its reader oracle.
    setUp = P.FileSetTests.setUp
    write = P.FileSetTests.write
    bind = P.FileSetTests.bind
    total = P.FileSetTests.total
    nested = P.FileSetTests.nested

    def inputs(self):
        return {item["role"]: item for item in self.graph["input"] if item["role"] != "expectation"}

    def result(self, disposition="matched", reason=None, **kwargs):
        args = dict(manifest=self.manifest, observations=self.graph["observation"], retain_source_image=True)
        args.update(kwargs)
        try:
            checked = Q.read_declared_files(self.root, **args)
        except (AttributeError, IndexError, KeyError, TypeError, ValueError, OSError) as exc:
            self.fail(f"reader escaped as {type(exc).__name__}")
        self.assertEqual(checked.disposition, disposition, checked)
        if reason:
            self.assertIn(reason, checked.reason)
        if disposition != "matched":
            self.assertIsNone(checked.plan)
            self.assertEqual(checked.retained_bytes, 0)
            self.assertTrue(all(item.data is None for item in checked.files))
        return checked

    def no_read(self, reason, **kwargs):
        with mock.patch.object(Q.A, "read_snapshot", wraps=Q.A.read_snapshot) as snapshots, \
                mock.patch.object(Q.A, "read_bounded_pin", wraps=Q.A.read_bounded_pin) as pins:
            checked = self.result("refused", reason, **kwargs)
            self.assertEqual((snapshots.call_count, pins.call_count), (0, 0))
        return checked

    def empty_snapshots(self):
        for item in self.graph["input"]:
            if item["role"] in {"guest-source", "guest-image", "reference-identity", "expectation"}:
                self.write(item, b"")
        for item in self.graph["observation"]:
            self.write(item, b"")
        self.write(self.child, b""); self.bind()

    def test_default_and_explicit_false_keep_fifteen_and_same_facts(self):
        implicit = Q.read_declared_files(self.root, manifest=self.manifest, observations=self.graph["observation"])
        explicit = self.result(retain_source_image=False)
        self.assertEqual(implicit, explicit)
        self.assertEqual(sum(item.data is not None for item in implicit.files), 15)
        self.assertTrue(all(item.data is None for item in implicit.files if item.role in {"guest-source", "guest-image"}))

    def test_opt_in_returns_exact_seventeen_payloads_without_qualification(self):
        checked = self.result(); payloads = [item for item in checked.files if item.data is not None]
        self.assertEqual(len(payloads), 17)
        self.assertEqual(len(checked.files), 22)
        self.assertEqual(checked.retained_bytes, sum(len(item.data) for item in payloads))
        self.assertIn("qualification pending", checked.reason)
        for role in ("guest-source", "guest-image"):
            fact = next(item for item in payloads if item.role == role)
            self.assertEqual(fact.data, ("synthetic " + self.inputs()[role]["id"]).encode())
            self.assertEqual(fact.pin.sha256, self.inputs()[role]["sha256"])

    def test_one_read_per_file_and_no_manifest_reopen(self):
        with mock.patch.object(Q.A, "read_snapshot", wraps=Q.A.read_snapshot) as snapshots, \
                mock.patch.object(Q.A, "read_bounded_pin", wraps=Q.A.read_bounded_pin) as pins:
            self.result()
        calls = [*snapshots.call_args_list, *pins.call_args_list]
        ids = [(call.args[1], call.args[2]["id"]) for call in calls]
        self.assertEqual((snapshots.call_count, pins.call_count), (18, 3))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertNotIn(("input", self.manifest_record["id"]), ids)

    def test_exact_reader_role_caps_and_default_pin_caps(self):
        for opt_in in (False, True):
            with self.subTest(opt_in=opt_in), \
                    mock.patch.object(Q.A, "read_snapshot", wraps=Q.A.read_snapshot) as snapshots, \
                    mock.patch.object(Q.A, "read_bounded_pin", wraps=Q.A.read_bounded_pin) as pins:
                self.result(retain_source_image=opt_in)
                for call in [*snapshots.call_args_list, *pins.call_args_list]:
                    role = call.args[2]["role"]
                    cap = (4 * 1024 * 1024 if role == "raw-gpr" else
                           1024 * 1024 if role == "expectation" or (opt_in and role == "guest-source") else
                           65536 if role in {"reference-identity", "process-receipt", "process-stdout", "process-stderr"}
                           or (opt_in and role == "guest-image") else 8 * 1024 * 1024)
                    self.assertEqual(call.kwargs["max_bytes"], cap, role)

    def test_all_seventeen_maxima_and_rebuild_room_fit_fixed_ceiling(self):
        for item in self.graph["input"]:
            size = (1024 * 1024 if item["role"] in {"guest-source", "expectation"} else
                    65536 if item["role"] in {"guest-image", "reference-identity"} else None)
            if size is not None:
                self.write(item, b"x" * size)
        for item in self.graph["observation"]:
            self.write(item, b"x" * (4 * 1024 * 1024 if item["role"] == "raw-gpr" else 65536))
        self.bind(); checked = self.result(max_snapshot_bytes=16515072)
        self.assertEqual(checked.retained_bytes, 16449536)  # 15.6875 MiB, independently literal.
        self.assertLess(checked.retained_bytes + 65536, 16 * 1024 * 1024)
        self.assertEqual((checked.authenticated_bytes, checked.charged_read_bytes), (self.total(), self.total()))
        self.result("refused", "byte limit", max_snapshot_bytes=16515071)

    def oversized(self, role, size):
        item = self.inputs()[role]; self.write(item, b"x" * size); self.bind()
        original = Q.A.read_snapshot; reads = []
        def snapshot(*args, **kwargs):
            if args[2]["id"] == item["id"]:
                with mock.patch.object(Q.A.os, "read", wraps=Q.A.os.read) as read:
                    result = original(*args, **kwargs)
                reads.append(read.call_count); return result
            return original(*args, **kwargs)
        with mock.patch.object(Q.A, "read_snapshot", snapshot):
            self.result("refused", "byte limit")
        self.assertEqual(reads, [0], "oversized selected file must refuse before payload I/O")

    def test_source_one_byte_over_bound_refuses_before_its_payload_read(self):
        self.oversized("guest-source", 1048577)

    def test_image_one_byte_over_bound_refuses_before_its_payload_read(self):
        self.oversized("guest-image", 65537)

    def test_empty_source_image_is_authenticated_without_content_credit(self):
        for role in ("guest-source", "guest-image"):
            self.write(self.inputs()[role], b"")
        self.bind(); checked = self.result()
        self.assertEqual([item.data for item in checked.files if item.role in {"guest-source", "guest-image"}], [b"", b""])
        self.assertEqual(sum(item.data is not None for item in checked.files), 17)

    def test_non_boolean_flag_refuses_before_io_even_with_failed_manifest(self):
        failed = replace(self.manifest, disposition="unavailable", reason="earlier manifest", plan=None)
        for flag in (0, 1, None, "true", [], {}, 0.0):
            with self.subTest(flag=repr(flag)):
                self.no_read("plain boolean", retain_source_image=flag)
                self.no_read("plain boolean", retain_source_image=flag, manifest=failed)

    def test_reservation_floor_refuses_before_new_io(self):
        for size in (0, 65535):
            with self.subTest(size=size):
                self.no_read("rebuild reservation", max_snapshot_bytes=size)
        self.no_read("manifest seed", max_snapshot_bytes=65536)

    def test_seed_peak_plus_reservation_is_inclusive(self):
        self.empty_snapshots(); peak = self.manifest.pin.byte_size + 65536
        checked = self.result(max_snapshot_bytes=peak)
        self.assertEqual(checked.retained_bytes, 0)
        self.assertEqual(sum(item.data is not None for item in checked.files), 17)
        self.no_read("manifest seed", max_snapshot_bytes=peak - 1)

    def test_retained_peak_plus_reservation_is_inclusive(self):
        for item in self.graph["observation"]:
            self.write(item, b"x" * 128)
        self.bind(); retained = self.result().retained_bytes
        self.assertGreater(retained, self.manifest.pin.byte_size)
        self.result(max_snapshot_bytes=retained + 65536)
        self.result("refused", "byte limit", max_snapshot_bytes=retained + 65535)

    def test_transient_peak_also_leaves_rebuild_room_and_precedes_retention(self):
        self.write(self.child, b";" + b"x" * 511); self.bind()
        checked = self.result(max_snapshot_bytes=65536 + 512)
        self.assertLess(checked.retained_bytes, 512)
        with mock.patch.object(Q.A.os, "read", wraps=Q.A.os.read) as read:
            self.result("refused", "byte limit", max_snapshot_bytes=65536 + 511)
        self.assertEqual(read.call_count, 0)

    def test_transient_snapshot_is_released_before_next_read(self):
        original = Q.A.read_snapshot; previous = []
        def read(*args, **kwargs):
            if previous:
                gc.collect(); self.assertIsNone(previous.pop()(), "transient snapshot carried into next read")
            snapshot = original(*args, **kwargs)
            if args[2]["id"] == self.child["id"]:
                previous.append(weakref.ref(snapshot))
            return snapshot
        with mock.patch.object(Q.A, "read_snapshot", read):
            self.result()

    def test_exact_read_budget_still_charges_manifest_once(self):
        original = Q.A.os.read; consumed = []
        def read(fd, count):
            data = original(fd, count); consumed.append(len(data)); return data
        total = self.total()
        with mock.patch.object(Q.A.os, "read", read):
            checked = self.result(max_read_bytes=total)
        self.assertEqual(sum(consumed) + self.manifest.pin.byte_size, total)
        self.assertEqual(checked.charged_read_bytes, total)

    def test_read_overflow_never_consumes_past_shared_budget(self):
        original = Q.A.os.read; consumed = []; budget = self.total() - 1
        def read(fd, count):
            self.assertLessEqual(count, budget - self.manifest.pin.byte_size - sum(consumed))
            data = original(fd, count); consumed.append(len(data)); return data
        with mock.patch.object(Q.A.os, "read", read):
            checked = self.result("refused", "byte limit", max_read_bytes=budget)
        self.assertLessEqual(sum(consumed) + self.manifest.pin.byte_size, budget)
        self.assertEqual(checked.charged_read_bytes, budget)

    def test_late_failure_drops_source_image_and_every_other_payload(self):
        with mock.patch.object(Q.A, "read_snapshot", wraps=Q.A.read_snapshot) as reads:
            self.result()
        last = reads.call_args_list[-1].args[2]
        (self.root / last["path"]).write_bytes(b"changed after declaration")
        checked = self.result("stale")
        self.assertTrue(all(item.pin.disposition == "matched" for item in checked.files
                            if item.role in {"guest-source", "guest-image"}))
        self.assertEqual(checked.files[-1].record_id, last["id"])

    def test_source_image_unavailable_and_stale_remain_separate_terminal_facts(self):
        for role in ("guest-source", "guest-image"):
            item = self.inputs()[role]; path = self.root / item["path"]
            payload = path.read_bytes(); path.unlink()
            self.result("unavailable")
            path.write_bytes(b"changed"); self.result("stale")
            path.write_bytes(payload)

    def test_selected_child_overlaps_use_one_strict_snapshot(self):
        self.document["input"] += [self.inputs()[role].copy() for role in ("guest-source", "guest-image")]
        self.bind()
        with mock.patch.object(Q.A, "read_snapshot", wraps=Q.A.read_snapshot) as snapshots:
            checked = self.result()
        for role, cap in (("guest-source", 1048576), ("guest-image", 65536)):
            calls = [call for call in snapshots.call_args_list if call.args[2]["role"] == role]
            self.assertEqual(len(calls), 1); self.assertEqual(calls[0].kwargs["max_bytes"], cap)
            self.assertEqual(next(item.classification for item in checked.files if item.role == role), "non-manifest")

    def test_selected_child_overlap_still_refuses_nested_document(self):
        item = self.inputs()["guest-source"]; self.write(item, self.nested(item["path"]))
        self.document["input"].append(item.copy()); self.bind()
        checked = self.result("refused", "nested dependencies")
        self.assertEqual(checked.files[-1].classification, "manifest")

    def test_frozen_source_image_facts_and_payloads(self):
        checked = self.result(); fact = next(item for item in checked.files if item.role == "guest-source")
        with self.assertRaises(FrozenInstanceError):
            checked.retained_bytes = 0
        with self.assertRaises(FrozenInstanceError):
            fact.data = b"changed"
        self.assertIs(type(fact.data), bytes)
        original = fact.data; (self.root / fact.path).write_bytes(b"later path change")
        self.assertEqual(fact.data, original)

    def test_unused_reservation_is_not_reported_as_retained_payload(self):
        default = self.result(retain_source_image=False); extended = self.result()
        payloads = [item.data for item in extended.files if item.role in {"guest-source", "guest-image"}]
        self.assertEqual(len(payloads), 2)
        self.assertTrue(all(type(data) is bytes for data in payloads))
        extra = sum(len(data) for data in payloads)
        self.assertEqual(extended.retained_bytes, default.retained_bytes + extra)
        self.assertEqual(extended.authenticated_bytes, default.authenticated_bytes)

    def test_no_builder_process_legacy_reader_or_path_writes(self):
        with mock.patch.object(Q.G, "build_guest_image", side_effect=AssertionError("reader built an image")), \
                mock.patch.object(Q.A, "read_pinned", side_effect=AssertionError("legacy unbounded reader")), \
                mock.patch.object(subprocess, "run", side_effect=AssertionError("process launched")), \
                mock.patch.object(Path, "write_bytes", side_effect=AssertionError("path written")):
            self.result()

    def test_opt_in_does_not_change_later_default_calls(self):
        self.result(); checked = self.result(retain_source_image=False)
        self.assertEqual(sum(item.data is not None for item in checked.files), 15)


MUTATIONS = {
    "flag-type": ('if type(retain_source_image) is not bool:', 'if False:'),
    "default": ('retain_source_image: bool = False) -> FileSetCheck:', 'retain_source_image: bool = True) -> FileSetCheck:'),
    "forward": ('_requests(manifest, observations, retain_source_image=retain_source_image)',
                '_requests(manifest, observations, retain_source_image=False)'),
    "retain-source": ('retained_roles.update({"guest-source", "guest-image"})', 'retained_roles.update({"guest-image"})'),
    "retain-image": ('retained_roles.update({"guest-source", "guest-image"})', 'retained_roles.update({"guest-source"})'),
    "source-cap": ('G.SOURCE_BYTES if item.role == "guest-source" and retain else', 'L.LEAF_BYTES if item.role == "guest-source" and retain else'),
    "image-cap": ('G.IMAGE_BYTES if item.role == "guest-image" and retain else', 'L.LEAF_BYTES if item.role == "guest-image" and retain else'),
    "reserve": ('reserve = G.IMAGE_BYTES if retain_source_image else 0', 'reserve = 0'),
    "reserve-debit": ('max_snapshot_bytes -= reserve', 'max_snapshot_bytes -= 0'),
    "seed-peak": ('_require(manifest.pin.byte_size <= max_snapshot_bytes, "snapshot budget below the authenticated manifest seed")',
                  '_require(manifest.pin.byte_size <= max_snapshot_bytes + reserve, "snapshot budget below the authenticated manifest seed")'),
    "snapshot-cap": P.MUTATIONS["snapshot-cap"],
    "read-cap": P.MUTATIONS["read-cap"],
    "drop-failed-payloads": P.MUTATIONS["drop-failed-payloads"],
    "immutable-facts": P.MUTATIONS["immutable-facts"],
    "immutable-result": P.MUTATIONS["immutable-result"],
    "reservation-counter": ('retained if disposition == "matched" else 0)', 'retained + reserve if disposition == "matched" else 0)'),
}


def main():
    global Q
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        source = Path(Q.__file__).read_text(); before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("mutation site count changed")
        module = types.ModuleType("guest_file_mutant"); module.__file__ = Q.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), Q.__file__, "exec"), module.__dict__); Q = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(GuestFileTests))
    print(f"MATCHED-GPR-GUEST-FILES: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; fixtures cleaned")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
