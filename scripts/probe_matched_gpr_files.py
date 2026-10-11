#!/usr/bin/env python3
"""On-volume whole-declared-set budget controls; no semantic/method credit."""
from __future__ import annotations

import argparse
import ast
from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
import gc
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock
import weakref

import experiment_verification as V
import matched_gpr_files as Q
import matched_gpr_manifest as M
import probe_matched_gpr_execution as P

ROOT = Path(__file__).resolve().parent.parent


class FileSetTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/p4-system-14/a38/files-fixtures"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base); self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.experiment, self.candidate = P.fixture(); self.graph = self.experiment["verification"]
        self.manifest_record = next(item for item in self.graph["input"] if item["role"] == "dependency-manifest")
        for item in self.graph["input"]:
            if item is not self.manifest_record:
                self.write(item, ("synthetic " + item["id"]).encode())
        for item in self.graph["observation"]:
            self.write(item, b"x")
        self.child = dict(id="code dependency", role="implementation", path="source/code.py", sha256="c" * 64)
        self.write(self.child, b'("dependencies", 1)\n')
        self.document = dict(format_version="matched-gpr-dependencies-v1", input=[self.child])
        self.bind()

    def write(self, record, payload):
        path = self.root / record["path"]; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload); record["sha256"] = hashlib.sha256(payload).hexdigest()
        if "byte_size" in record:
            record["byte_size"] = len(payload)

    def bind(self):
        payload = M.F.encode_dependencies(self.document, path=self.manifest_record["path"])
        self.write(self.manifest_record, payload)
        self.manifest = M.read_dependency_manifest(self.root, experiment=self.experiment, current_candidate=self.candidate)
        self.assertEqual(self.manifest.disposition, "matched", self.manifest)

    def result(self, disposition="matched", reason=None, **kwargs):
        args = dict(manifest=self.manifest, observations=self.graph["observation"]); args.update(kwargs)
        try:
            result = Q.read_declared_files(self.root, **args)
        except (AttributeError, IndexError, KeyError, TypeError, ValueError, OSError) as exc:
            self.fail(f"file-set refusal escaped as {type(exc).__name__}")
        self.assertEqual(result.disposition, disposition, result)
        if reason:
            self.assertIn(reason, result.reason)
        if disposition != "matched":
            self.assertIsNone(result.plan)
            self.assertEqual(result.retained_bytes, 0)
            self.assertTrue(all(item.data is None for item in result.files))
        return result

    def no_read(self, reason, **kwargs):
        with mock.patch.object(Q.A, "read_snapshot", wraps=Q.A.read_snapshot) as snapshots, \
                mock.patch.object(Q.A, "read_bounded_pin", wraps=Q.A.read_bounded_pin) as pins:
            result = self.result("refused", reason, **kwargs)
            self.assertEqual((snapshots.call_count, pins.call_count), (0, 0))
        return result

    def nested(self, path=None):
        return M.F.encode_dependencies(dict(format_version="matched-gpr-dependencies-v1", input=[dict(
            id="hidden", role="implementation", path="never/read.py", sha256="c" * 64)]),
            path=path or self.child["path"])

    def total(self):
        return sum(path.stat().st_size for path in self.root.rglob("*") if path.is_file())

    def test_raw_scoped_parent_and_complete_actual_file_set(self):
        scope = V.Scope("synthetic", frozenset({"sail-riscv"}), frozenset({"REQ-synthetic"}), frozenset({"OBL-synthetic"}))
        self.assertEqual(V.check_experiment(P.raw_experiment(self.experiment, self.candidate), scope), [])
        result = self.result()
        self.assertEqual(len(result.files), 22)
        self.assertEqual((result.authenticated_bytes, result.charged_read_bytes), (self.total(), self.total()))
        self.assertEqual(result.plan, self.manifest.plan)
        self.assertIn("qualification pending", result.reason)
        self.assertEqual(result.manifest_pin, self.manifest.pin)

    def test_only_fifteen_required_payloads_are_retained(self):
        result = self.result(); payloads = [item for item in result.files if item.data is not None]
        self.assertEqual(len(payloads), 15)
        self.assertEqual(result.retained_bytes, sum(len(item.data) for item in payloads))
        self.assertEqual({item.record_id for item in payloads if item.record_kind == "input"},
                         {"reference-identity", "expectation", "mutant-expectation"})
        self.assertEqual(next(item.classification for item in result.files if item.record_id == self.child["id"]), "non-manifest")

    def test_one_read_per_file_and_manifest_is_not_reopened(self):
        with mock.patch.object(Q.A, "read_snapshot", wraps=Q.A.read_snapshot) as snapshots, \
                mock.patch.object(Q.A, "read_bounded_pin", wraps=Q.A.read_bounded_pin) as pins:
            self.result()
            calls = [*snapshots.call_args_list, *pins.call_args_list]
            ids = [(call.args[1], call.args[2]["id"]) for call in calls]
            self.assertEqual((snapshots.call_count, pins.call_count), (16, 5))
            self.assertEqual(len(ids), len(set(ids)))
            self.assertNotIn(("input", self.manifest_record["id"]), ids)

    def test_explicit_per_role_caps_reach_the_anchored_owner(self):
        with mock.patch.object(Q.A, "read_snapshot", wraps=Q.A.read_snapshot) as snapshots, \
                mock.patch.object(Q.A, "read_bounded_pin", wraps=Q.A.read_bounded_pin) as pins:
            self.result()
            for call in [*snapshots.call_args_list, *pins.call_args_list]:
                record = call.args[2]; role = record["role"]
                expected = (4 * 1024 * 1024 if role == "raw-gpr" else
                            1024 * 1024 if role == "expectation" else
                            65536 if role in {"reference-identity", "process-receipt", "process-stdout", "process-stderr"}
                            else 8 * 1024 * 1024)
                self.assertEqual(call.kwargs["max_bytes"], expected, record)

    def test_exact_read_budget_includes_manifest_and_consumed_bytes(self):
        original = Q.A.os.read; consumed = []
        def read(fd, count):
            data = original(fd, count); consumed.append(len(data)); return data
        total = self.total()
        with mock.patch.object(Q.A.os, "read", read):
            result = self.result(max_read_bytes=total)
        self.assertEqual(result.charged_read_bytes, total)
        self.assertEqual(sum(consumed) + self.manifest.pin.byte_size, total)

    def test_one_byte_read_overflow_never_consumes_past_budget(self):
        original = Q.A.os.read; consumed = []; budget = self.total() - 1
        def read(fd, count):
            self.assertLessEqual(count, budget - self.manifest.pin.byte_size - sum(consumed))
            data = original(fd, count); consumed.append(len(data)); return data
        with mock.patch.object(Q.A.os, "read", read):
            result = self.result("refused", "byte limit", max_read_bytes=budget)
        self.assertLessEqual(sum(consumed) + self.manifest.pin.byte_size, budget)
        self.assertEqual(result.charged_read_bytes, budget)

    def test_read_budget_exhaustion_before_first_child_payload(self):
        budget = self.manifest.pin.byte_size + (self.root / self.child["path"]).stat().st_size - 1
        with mock.patch.object(Q.A.os, "read", wraps=Q.A.os.read) as read:
            result = self.result("refused", "byte limit", max_read_bytes=budget)
            self.assertEqual(read.call_count, 0)
        self.assertEqual(result.charged_read_bytes, budget)

    def test_read_budget_below_known_seed_refuses_before_new_io(self):
        for limit in [0, self.manifest.pin.byte_size - 1]:
            with self.subTest(limit=limit):
                self.no_read("manifest seed", max_read_bytes=limit)

    def test_exact_retained_budget_and_one_byte_overflow(self):
        for item in self.graph["observation"]: self.write(item, b"x" * 128)
        self.bind()
        retained = self.result().retained_bytes
        self.assertGreater(retained, self.manifest.pin.byte_size)
        self.result(max_snapshot_bytes=retained)
        self.result("refused", "byte limit", max_snapshot_bytes=retained - 1)

    def test_transient_snapshot_consumption_uses_remaining_payload_budget(self):
        self.write(self.child, b";" + b"x" * 511); self.bind()
        with mock.patch.object(Q.A.os, "read", wraps=Q.A.os.read) as read:
            self.result("refused", "byte limit", max_snapshot_bytes=self.manifest.pin.byte_size)
            self.assertEqual(read.call_count, 0)

    def test_transient_leaves_precede_retained_payloads(self):
        self.write(self.child, b";" + b"x" * 511); self.bind()
        result = self.result(max_snapshot_bytes=512)
        self.assertLess(result.retained_bytes, 512)

    def test_transient_snapshot_released_before_next_read(self):
        original = Q.A.read_snapshot; previous = []
        def read(*args, **kwargs):
            if previous:
                gc.collect(); self.assertIsNone(previous[0](), "transient snapshot still retained during next read")
                previous.clear()
            result = original(*args, **kwargs)
            if args[2]["id"] == self.child["id"]:
                previous.append(weakref.ref(result))
            return result
        with mock.patch.object(Q.A, "read_snapshot", read):
            self.result()

    def test_zero_snapshot_budget_cannot_cover_nonempty_manifest(self):
        self.write(self.child, b"")
        for item in self.graph["input"]:
            if item["role"] in {"reference-identity", "expectation"}: self.write(item, b"")
        for item in self.graph["observation"]: self.write(item, b"")
        self.bind()
        self.assertGreater(self.manifest.pin.byte_size, 0)
        self.no_read("snapshot budget", max_snapshot_bytes=0)

    def test_snapshot_budget_below_known_seed_refuses_before_new_io(self):
        for limit in [0, self.manifest.pin.byte_size - 1]:
            with self.subTest(limit=limit):
                self.no_read("snapshot budget", max_snapshot_bytes=limit)

    def test_inclusive_known_manifest_peak_when_other_snapshots_empty(self):
        self.write(self.child, b"")
        for item in self.graph["input"]:
            if item["role"] in {"reference-identity", "expectation"}: self.write(item, b"")
        for item in self.graph["observation"]: self.write(item, b"")
        self.bind(); result = self.result(max_snapshot_bytes=self.manifest.pin.byte_size)
        self.assertEqual(result.retained_bytes, 0)
        self.assertEqual(sum(item.data is not None for item in result.files), 15)

    def test_invalid_aggregate_limits_refuse_before_io(self):
        for name, ceiling in [("max_read_bytes", 128 * 1024 * 1024), ("max_snapshot_bytes", 16 * 1024 * 1024)]:
            for value in [-1, True, False, None, 1.0, "1", ceiling + 1]:
                with self.subTest(name=name, value=value):
                    self.no_read("aggregate", **{name: value})

    def test_failed_manifest_findings_preserved_without_new_io(self):
        for disposition in ["stale", "unavailable", "refused", "unsupported"]:
            checked = replace(self.manifest, disposition=disposition, reason="earlier manifest finding", plan=None)
            with self.subTest(disposition=disposition), mock.patch.object(Q.A, "read_snapshot", wraps=Q.A.read_snapshot) as snapshots, \
                    mock.patch.object(Q.A, "read_bounded_pin", wraps=Q.A.read_bounded_pin) as pins:
                result = self.result(disposition, "earlier manifest finding", manifest=checked)
                self.assertEqual(result.manifest_pin, checked.pin)
                self.assertEqual((snapshots.call_count, pins.call_count), (0, 0))

    def test_malformed_manifest_finding_refuses(self):
        for checked in [None, replace(self.manifest, disposition="invented"), replace(self.manifest, pin={}),
                        replace(self.manifest, reason=[]), replace(self.manifest, plan=None)]:
            with self.subTest(kind=type(checked).__name__):
                self.no_read("manifest", manifest=checked)

    def test_child_union_and_observation_counts_before_lookup(self):
        plans = [replace(self.manifest.plan, child_input_ids=()),
                 replace(self.manifest.plan, child_input_ids=(self.child["id"],) * 65),
                 replace(self.manifest.plan, inputs=self.manifest.plan.inputs[:8]),
                 replace(self.manifest.plan, inputs=self.manifest.plan.inputs * 8)]
        for plan in plans:
            with self.subTest(children=len(plan.child_input_ids), inputs=len(plan.inputs)):
                self.no_read("counts", manifest=replace(self.manifest, plan=plan))
        for observations in [None, self.graph["observation"][:-1], self.graph["observation"] * 2]:
            with self.subTest(kind=type(observations).__name__):
                self.no_read("twelve", observations=observations)

    def test_principal_and_run_counts_before_lookup(self):
        execution = self.manifest.plan.relations.execution
        for changed in [replace(execution, common_inputs=()), replace(execution, runs=())]:
            plan = replace(self.manifest.plan, relations=replace(self.manifest.plan.relations, execution=changed))
            with self.subTest(common=len(changed.common_inputs), runs=len(changed.runs)):
                self.no_read("counts", manifest=replace(self.manifest, plan=plan))

    def test_duplicated_child_edge_refuses(self):
        plan = replace(self.manifest.plan, child_input_ids=(self.child["id"],) * 2)
        self.no_read("child identities", manifest=replace(self.manifest, plan=plan))

    def test_unknown_union_identity_refuses(self):
        original = self.manifest.plan.inputs[-1]
        for inputs in [self.manifest.plan.inputs + (replace(original, input_id="extra", path="extra/file"),),
                       tuple(replace(item, input_id="other") if item.input_id == self.child["id"] else item
                             for item in self.manifest.plan.inputs)]:
            with self.subTest(count=len(inputs)):
                self.no_read("union differs", manifest=replace(self.manifest, plan=replace(self.manifest.plan, inputs=inputs)))

    def test_duplicate_union_id_or_path_refuses(self):
        original = self.manifest.plan.inputs[-1]
        for item in [original, replace(original, input_id="new")]:
            with self.subTest(record_id=item.input_id):
                plan = replace(self.manifest.plan, inputs=self.manifest.plan.inputs + (item,))
                self.no_read("duplicated union", manifest=replace(self.manifest, plan=plan))

    def test_principal_conflict_refuses_before_io(self):
        plan = self.manifest.plan
        items = tuple(replace(item, sha256="c" * 64) if item.input_id == "guest-source" else item for item in plan.inputs)
        self.no_read("principal identity", manifest=replace(self.manifest, plan=replace(plan, inputs=items)))

    def test_manifest_self_or_nested_role_refuses(self):
        plan = self.manifest.plan
        for changed in [replace(plan, child_input_ids=(*plan.child_input_ids, plan.manifest_input_id)),
                        replace(plan, inputs=tuple(replace(item, role="dependency-manifest") if item.input_id == self.child["id"]
                                                  else item for item in plan.inputs))]:
            with self.subTest(children=changed.child_input_ids):
                self.no_read("manifest selection", manifest=replace(self.manifest, plan=changed))

    def test_manifest_seed_pin_identity_and_size_refuse(self):
        pin = self.manifest.pin
        for changed in [replace(pin, record_kind="observation"), replace(pin, record_id="other"), replace(pin, path="other/file"),
                        replace(pin, sha256="c" * 64), replace(pin, byte_size=0), replace(pin, byte_size=65537),
                        replace(pin, byte_size=True), replace(pin, disposition="mismatch")]:
            with self.subTest(pin=changed):
                self.no_read("manifest pin", manifest=replace(self.manifest, pin=changed))

    def test_observation_identity_role_and_duplicate_refuse(self):
        for key, value in [("id", "other"), ("role", "other"), ("id", self.graph["observation"][1]["id"])]:
            records = deepcopy(self.graph["observation"]); records[0][key] = value
            with self.subTest(key=key, value=value):
                self.no_read("observation", observations=records)

    def test_observation_path_duplicates_and_input_alias_refuse(self):
        for path in [self.graph["observation"][1]["path"], self.child["path"]]:
            records = deepcopy(self.graph["observation"]); records[0]["path"] = path
            with self.subTest(path=path):
                self.no_read("path", observations=records)

    def test_observation_declared_sizes_refuse_before_io(self):
        for size in [-1, True, None, 65537]:
            records = deepcopy(self.graph["observation"])
            item = next(record for record in records if record["role"] == "process-stdout"); item["byte_size"] = size
            with self.subTest(size=size):
                self.no_read("observation size", observations=records)

    def test_file_binding_paths_digests_and_strings_refuse_before_io(self):
        for key, value in [("path", "../outside"), ("sha256", "bad"), ("id", ""), ("role", None)]:
            records = deepcopy(self.graph["observation"]); records[0][key] = value
            with self.subTest(key=key):
                self.no_read("binding" if key != "sha256" else "digest", observations=records)

    def test_exact_principal_overlap_is_read_once_and_inspected(self):
        principal = self.graph["input"][0]
        self.document["input"].append(dict(principal)); self.bind()
        with mock.patch.object(Q.A, "read_snapshot", wraps=Q.A.read_snapshot) as snapshots, \
                mock.patch.object(Q.A, "read_bounded_pin", wraps=Q.A.read_bounded_pin) as pins:
            result = self.result()
            calls = [call for call in [*snapshots.call_args_list, *pins.call_args_list] if call.args[2]["id"] == principal["id"]]
            self.assertEqual(len(calls), 1)
            self.assertEqual(next(item.classification for item in result.files if item.record_id == principal["id"]), "non-manifest")
        self.assertEqual(len(result.files), 22)

    def test_retained_principal_overlap_is_inspected_and_retained_once(self):
        principal = next(item for item in self.graph["input"] if item["id"] == "expectation")
        self.document["input"].append(dict(principal)); self.bind()
        result = self.result(); selected = [item for item in result.files if item.record_id == principal["id"]]
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].classification, "non-manifest")
        self.assertEqual(selected[0].data, (self.root / principal["path"]).read_bytes())

    def test_maximum_flat_union_authenticates_all_eighty_five_files(self):
        for n in range(63):
            item = dict(id=f"extra{n}", role="implementation", path=f"source/extra{n}", sha256="c" * 64)
            self.write(item, f"synthetic child {n}".encode()); self.document["input"].append(item)
        self.bind(); result = self.result()
        self.assertEqual((len(result.plan.child_input_ids), len(result.plan.inputs), len(result.files)), (64, 73, 85))
        self.assertEqual(result.authenticated_bytes, self.total())
        self.assertEqual(sum(item.data is not None for item in result.files), 15)

    def test_coherent_failed_process_records_remain_data(self):
        for run in self.graph["run"]: run.update(process_exit=127, verdict="REFUSED")
        self.graph["control_run"][0]["observed_verdict"] = "REFUSED"
        self.bind(); result = self.result()
        self.assertEqual(result.plan.relations.control_observed_verdict, "REFUSED")

    def test_disguised_nested_child_refuses(self):
        self.write(self.child, self.nested()); self.bind()
        result = self.result("refused", "nested dependencies")
        self.assertEqual((result.files[-1].classification, result.files[-1].pin.disposition), ("manifest", "matched"))
        self.assertFalse((self.root / "never").exists())

    def test_nested_retained_principal_cannot_escape_child_inspection(self):
        principal = next(item for item in self.graph["input"] if item["id"] == "expectation")
        self.write(principal, self.nested(principal["path"]))
        self.document["input"].append(dict(principal)); self.bind()
        self.result("refused", "nested dependencies")

    def test_schema_tool_failure_stops_after_authenticated_child(self):
        with mock.patch.object(Q.F, "_schema", side_effect=OSError("missing schema")), \
                mock.patch.object(Q.A, "read_snapshot", wraps=Q.A.read_snapshot) as snapshots, \
                mock.patch.object(Q.A, "read_bounded_pin", wraps=Q.A.read_bounded_pin) as pins:
            result = self.result("unavailable", "schema unavailable")
            self.assertEqual((snapshots.call_count, pins.call_count), (1, 0))
            self.assertEqual(result.files[-1].pin.disposition, "matched")

    def test_stale_missing_and_unsafe_children_stop_new_reads(self):
        path = self.root / self.child["path"]; original = path.read_bytes()
        for kind in ["stale", "missing", "symlink"]:
            try:
                if kind == "stale": path.write_bytes(b"changed")
                elif kind == "missing": path.unlink()
                else: path.unlink(); path.symlink_to("missing")
                with self.subTest(kind=kind), mock.patch.object(Q.A, "read_snapshot", wraps=Q.A.read_snapshot) as snapshots, \
                        mock.patch.object(Q.A, "read_bounded_pin", wraps=Q.A.read_bounded_pin) as pins:
                    result = self.result({"stale": "stale", "missing": "unavailable", "symlink": "refused"}[kind])
                    self.assertEqual((snapshots.call_count, pins.call_count), (1, 0))
                    self.assertEqual(result.charged_read_bytes, self.manifest.pin.byte_size + 8 * 1024 * 1024)
            finally:
                if path.is_symlink(): path.unlink()
                path.write_bytes(original)

    def test_partial_read_failure_conservatively_charges_admitted_cap(self):
        original = Q.A.os.read; calls = []
        def read(fd, count):
            calls.append(count)
            if len(calls) == 1: return original(fd, min(count, 2))
            raise OSError("partial read fault")
        with mock.patch.object(Q.A.os, "read", read), mock.patch.object(Q.A, "read_snapshot", wraps=Q.A.read_snapshot) as snapshots:
            result = self.result("unavailable")
            self.assertEqual(snapshots.call_count, 1)
        self.assertEqual(result.charged_read_bytes, self.manifest.pin.byte_size + 8 * 1024 * 1024)
        self.assertEqual(result.authenticated_bytes, self.manifest.pin.byte_size)

    def test_nested_git_boundary_refuses_without_entering_another_repository(self):
        # Empty marker is a fixture, not a Git repository; no nested implementation is read.
        (self.root / self.child["path"]).parent.joinpath(".git").touch()
        with mock.patch.object(Q.A, "read_snapshot", wraps=Q.A.read_snapshot) as snapshots:
            self.result("refused", "nested Git")
            self.assertEqual(snapshots.call_count, 1)

    def test_close_failure_stops_batch_and_releases_all_descriptors(self):
        opened = []; open_original, close_original = Q.A.os.open, Q.A.os.close
        fault = False
        def open_fd(*args, **kwargs):
            fd = open_original(*args, **kwargs); opened.append(fd); return fd
        def close_fd(fd):
            nonlocal fault
            close_original(fd)
            if not fault:
                fault = True; raise OSError("close fault after actual close")
        with mock.patch.object(Q.A.os, "open", open_fd), mock.patch.object(Q.A.os, "close", close_fd), \
                mock.patch.object(Q.A, "read_snapshot", wraps=Q.A.read_snapshot) as snapshots:
            result = self.result("unavailable")
            self.assertEqual(snapshots.call_count, 1)
        self.assertTrue(opened)
        for fd in opened:
            with self.assertRaises(OSError): Q.A.os.fstat(fd)
        self.assertEqual(result.charged_read_bytes, self.manifest.pin.byte_size + 8 * 1024 * 1024)

    def test_late_failure_drops_all_earlier_retained_payloads(self):
        item = self.graph["observation"][-1]; (self.root / item["path"]).write_bytes(b"y")
        result = self.result("stale")
        self.assertTrue(any(item.record_id == "expectation" and item.pin.disposition == "matched" for item in result.files))
        self.assertTrue(all(item.data is None for item in result.files))

    def test_snapshot_payload_and_pin_metadata_consistency(self):
        original = Q.A.read_snapshot
        for change in [dict(data=None), dict(data=bytearray(b"mutable")), dict(data=b"wrong size"),
                       dict(pin=replace(self.manifest.pin, record_id="foreign"))]:
            def inconsistent(*args, **kwargs):
                return replace(original(*args, **kwargs), **change)
            with self.subTest(change=tuple(change)), mock.patch.object(Q.A, "read_snapshot", inconsistent):
                self.result("refused", "inconsistent authenticated")

    def test_observation_snapshot_size_must_match_frozen_declaration(self):
        original = Q.A.read_snapshot
        def inconsistent(*args, **kwargs):
            result = original(*args, **kwargs)
            if args[1] == "observation":
                data = result.data + b"x"
                return replace(result, data=data, pin=replace(result.pin, byte_size=len(data)))
            return result
        with mock.patch.object(Q.A, "read_snapshot", inconsistent):
            self.result("refused", "inconsistent authenticated")

    def test_snapshot_size_cannot_exceed_admitted_payload_cap(self):
        self.write(self.child, b";" + b"x" * 511); self.bind()
        original = Q.A.read_snapshot; limit = (self.root / self.child["path"]).stat().st_size
        def inconsistent(*args, **kwargs):
            result = original(*args, **kwargs)
            if args[2]["id"] == self.child["id"]:
                data = result.data + b"x"
                return replace(result, data=data, pin=replace(result.pin, byte_size=len(data)))
            return result
        with mock.patch.object(Q.A, "read_snapshot", inconsistent):
            self.result("refused", "inconsistent authenticated", max_snapshot_bytes=limit)

    def test_caller_observation_changes_after_first_read_do_not_rebind(self):
        original = Q.A.read_snapshot
        def changed(*args, **kwargs):
            result = original(*args, **kwargs)
            if args[2]["id"] == self.child["id"]:
                self.graph["observation"][0].update(path="absent/later", sha256="c" * 64, byte_size=0)
            return result
        with mock.patch.object(Q.A, "read_snapshot", changed):
            result = self.result()
        self.assertFalse(any(item.path == "absent/later" for item in result.files))

    def test_snapshot_not_later_path_drives_leaf_classification(self):
        original = Q.A.read_snapshot; nested = self.nested()
        def changed(*args, **kwargs):
            result = original(*args, **kwargs)
            if args[2]["id"] == self.child["id"]: (self.root / self.child["path"]).write_bytes(nested)
            return result
        with mock.patch.object(Q.A, "read_snapshot", changed):
            result = self.result()
        self.assertEqual(next(item.classification for item in result.files if item.record_id == self.child["id"]), "non-manifest")
        self.result("stale")

    def test_frozen_results_and_file_facts(self):
        result = self.result()
        with self.assertRaises(FrozenInstanceError): result.retained_bytes = 0
        with self.assertRaises(FrozenInstanceError): result.files[0].path = "other"
        with self.assertRaises(FrozenInstanceError): result.files[0].pin.sha256 = "c" * 64

    def test_binary_cache_process_legacy_and_path_reopens_are_absent(self):
        self.assertFalse((self.root / self.candidate["binary"]).exists())
        with mock.patch.object(subprocess, "run", side_effect=AssertionError("process")), \
                mock.patch.object(Q.A, "read_pinned", side_effect=AssertionError("unbounded legacy reader")), \
                mock.patch.object(Path, "read_bytes", side_effect=AssertionError("path reopened")), \
                mock.patch.object(Path, "read_text", side_effect=AssertionError("path reopened")):
            self.result()


GUARDS = {
    "aggregate-limits": "invalid aggregate read/snapshot byte limits",
    "seed-budget": "read budget below the authenticated manifest seed",
    "seed-snapshot-peak": "snapshot budget below the authenticated manifest seed",
    "snapshot-consistency": "inconsistent authenticated file snapshot/metadata",
    "family-counts": "manifest child/union counts outside the method envelope",
    "observation-count": "expected exactly twelve observation records",
    "execution-counts": "principal/run counts outside the method envelope",
    "child-identities": "invalid or duplicated child identities",
    "union-identities": "duplicated union input identity or path",
    "union-membership": "union differs from principals and children",
    "principal-identity": "principal identity conflicts with union",
    "manifest-selection": "invalid self or nested manifest selection",
    "manifest-seed": "manifest pin does not match its selected bounded identity",
    "observation-selection": "observation identity/role not selected by a run",
    "observation-unique": "duplicated observation identity or path",
    "observation-size": "observation size outside its role bound",
    "output-alias": "input aliases an observation path",
}
MUTATIONS = {
    "read-cap": ('cap = min(request.limit, max_read_bytes - charged)', 'cap = request.limit'),
    "snapshot-cap": ('cap = min(cap, max_snapshot_bytes - retained)', 'cap = cap'),
    "seed-charge": ('authenticated = charged = manifest.pin.byte_size', 'authenticated = charged = 0'),
    "failed-charge": ('charged += cap  # Partial consumption is not exposed by every reader failure.', 'charged += 0'),
    "stop-after-failure": ('return finish(disposition, pin.reason)', 'continue'),
    "drop-failed-payloads": ('tuple(facts if disposition == "matched" else [replace(item, data=None) for item in facts])', 'tuple(facts)'),
    "transient-first": ('2 if item.retain else 0 if item.inspect else 1', '0 if item.retain else 2 if item.inspect else 1'),
    "transient-release": ('        data = None\n        if snapshot_needed:\n            snapshot = None', '        pass'),
    "nested-classification": ('F.is_dependencies_document(data, path=request.path)', 'False'),
    "immutable-result": ('@dataclass(frozen=True)\nclass FileSetCheck:', '@dataclass\nclass FileSetCheck:'),
    "immutable-facts": ('@dataclass(frozen=True)\nclass FileFact:', '@dataclass\nclass FileFact:'),
    "context-freeze": ('record = request.record()', 'record = next((item for item in observations if item["id"] == request.record_id), request.record())'),
    "manifest-reopen": ('facts = [FileFact(seed.kind, seed.record_id, seed.role, seed.path, manifest.pin)]',
                        'A.read_snapshot(root, "input", seed.record(), max_bytes=F.DOCUMENT_BYTES)\n    facts = [FileFact(seed.kind, seed.record_id, seed.role, seed.path, manifest.pin)]'),
    "legacy-pin": ('A.read_bounded_pin(root, request.kind, record, max_bytes=cap)', 'A.read_pinned(root, request.kind, record)'),
}


def main():
    global Q
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=[*GUARDS, *MUTATIONS])
    args = parser.parse_args()
    if args.mutation:
        source = Path(Q.__file__).read_text()
        if args.mutation in GUARDS:
            reason = GUARDS[args.mutation]
            sites = [node for node in ast.walk(ast.parse(source)) if isinstance(node, ast.Call) and
                     isinstance(node.func, ast.Name) and node.func.id == "_require" and len(node.args) == 2 and
                     isinstance(node.args[1], ast.Constant) and node.args[1].value == reason]
            if sites:
                if len(sites) != 1: raise RuntimeError("guard mutation site count changed")
                before = ast.get_source_segment(source, sites[0]); after = f"_require(True, {reason!r})"
            else:
                sites = [node for node in ast.walk(ast.parse(source)) if isinstance(node, ast.If) and
                         any(isinstance(statement, ast.Return) and isinstance(statement.value, ast.Call) and
                             len(statement.value.args) >= 2 and isinstance(statement.value.args[1], ast.Constant) and
                             statement.value.args[1].value == reason for statement in node.body)]
                if len(sites) != 1: raise RuntimeError("conditional mutation site count changed")
                before = ast.get_source_segment(source, sites[0].test); after = "False"
        else:
            before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1: raise RuntimeError("mutation site count changed")
        module = types.ModuleType("file_set_mutant"); module.__file__ = Q.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), Q.__file__, "exec"), module.__dict__)
        Q = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(FileSetTests))
    print(f"MATCHED-GPR-FILES: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; fixtures cleaned")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
