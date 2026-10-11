#!/usr/bin/env python3
"""Synthetic on-volume receipt binding controls; no process/capture evidence."""
from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
import hashlib
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock

import dossier_sexp as D
import matched_gpr_artifacts as F
import matched_gpr_receipt as M
import probe_matched_gpr_artifacts as P
import probe_matched_gpr_identity as I

ROOT = Path(__file__).resolve().parent.parent


def fixture():
    candidate = I.candidate()
    roles = ("guest-source", "guest-image", "reference-config", "reference-identity",
             "expectation", "collector", "adapter", "dependency-manifest")
    inputs = [dict(id=role, role=role, path=f"inputs/{role}", sha256=f"{n + 1:x}" * 64)
              for n, role in enumerate(roles)]
    doc = P.capture()
    doc.update(reference_binary_sha256=candidate["binary_sha256"],
               input=[dict(id=item["id"], sha256=item["sha256"]) for item in inputs],
               argv=[candidate["binary"], "--config-override", "inputs/reference-config",
                     "--inst-limit", "1", "--trace-instr", "--trace-gpr", "--trace-exception",
                     "--trace-output", "outputs/base.trace", "inputs/guest-image"])
    for item, suffix in zip(doc["observation"], ("trace", "stdout", "stderr")):
        item["path"] = "outputs/base." + suffix
    observations = deepcopy(doc["observation"]) + [dict(
        id="receipt", role="process-receipt", path="outputs/base.receipt.sexp", byte_size=0, sha256="0" * 64)]
    run = dict(id="base", kind="baseline", argv=list(doc["argv"]),
               input_ids=[item["id"] for item in inputs], producer_ids=["reference", "expected"],
               process_exit=0, verdict="AGREE", observation_ids=[item["id"] for item in observations])
    return doc, dict(run=run, inputs=inputs, observations=observations, current_candidate=candidate)


class ReceiptTests(unittest.TestCase):
    def setUp(self):
        parent = ROOT / "target/p4-system-14/a31/receipt-fixtures"
        parent.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=parent); self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.doc, self.args = fixture()
        self.path = self.root / "outputs/base.receipt.sexp"; self.path.parent.mkdir()
        self.publish()

    def publish(self, payload=None):
        payload = P.raw(self.doc, "capture") if payload is None else payload
        self.path.write_bytes(payload)
        self.args["observations"][-1].update(byte_size=len(payload), sha256=hashlib.sha256(payload).hexdigest())

    def result(self, disposition, reason=None):
        result = M.read_run_receipt(self.root, **self.args)
        self.assertEqual(result.disposition, disposition, result)
        if reason: self.assertIn(reason, result.reason)
        if disposition != "matched": self.assertIsNone(result.facts)
        return result

    def no_io_refusal(self, reason=None):
        with mock.patch.object(M.A, "read_snapshot", side_effect=AssertionError("unexpected I/O")):
            self.assertIsNone(self.result("refused", reason).pin)

    def test_positive_full_selected_inventory(self):
        result = self.result("matched", "process/method credit pending")
        self.assertEqual(result.pin.disposition, "matched")
        self.assertEqual(result.facts.argv, tuple(self.doc["argv"]))
        self.assertEqual((result.facts.run_id, result.facts.run_kind, result.facts.process_exit), ("base", "baseline", 0))
        self.assertEqual(result.facts.host, tuple(sorted(self.doc["host"].items())))
        self.assertEqual(result.facts.tools, tuple((item["id"], item["version"]) for item in self.doc["tool"]))

    def test_other_declared_files_and_binary_are_not_opened(self):
        self.assertFalse((self.root / "inputs").exists())
        self.assertFalse((self.root / self.args["current_candidate"]["binary"]).exists())
        self.result("matched")

    def test_coherent_failed_processes_remain_bound_data(self):
        for status in (-9, 1, 127):
            for kind in ("baseline", "repeat", "control"):
                with self.subTest(status=status, kind=kind):
                    self.doc.update(process_exit=status, run_kind=kind)
                    self.args["run"].update(process_exit=status, kind=kind, verdict="REFUSED")
                    self.publish()
                    self.assertEqual(self.result("matched").facts.process_exit, status)

    def test_inventories_are_unordered(self):
        self.doc["input"].reverse(); self.doc["observation"].reverse(); self.publish()
        self.args["inputs"].reverse(); self.args["run"]["input_ids"].reverse()
        self.args["run"]["observation_ids"].reverse()
        self.result("matched")

    def test_exact_argv_can_include_repeated_empty_unicode_arguments(self):
        argv = ["reference/bin/sail", "repeat", "", "repeat", "λ"]
        self.doc["argv"] = argv; self.args["run"]["argv"] = list(argv); self.publish()
        self.assertEqual(self.result("matched").facts.argv, tuple(argv))

    def test_short_context_does_not_claim_principal_method_coverage(self):
        self.args["inputs"] = [item for item in self.args["inputs"] if item["role"] == "collector"]
        self.args["run"]["input_ids"] = ["collector"]
        self.doc["input"] = [item for item in self.doc["input"] if item["id"] == "collector"]
        self.publish(); self.result("matched", "method credit pending")

    def test_scalar_binding_fields_must_match(self):
        original = deepcopy(self.doc)
        for field, value in (("run_id", "other"), ("run_kind", "control"), ("process_exit", -9),
                             ("reference_candidate_id", "other"), ("reference_binary_sha256", "b" * 64),
                             ("collector_input_id", "adapter")):
            with self.subTest(field=field):
                self.doc = deepcopy(original); self.doc[field] = value; self.publish()
                self.assertEqual(self.result("refused", field).pin.disposition, "matched")

    def test_argv_order_must_match(self):
        self.doc["argv"][1:3] = reversed(self.doc["argv"][1:3]); self.publish()
        self.result("refused", "ordered canonical argv")

    def test_argv_entry_must_match(self):
        self.doc["argv"][0] = "different/binary"; self.publish(); self.result("refused", "argv")

    def test_input_digest_must_match(self):
        self.doc["input"][0]["sha256"] = "b" * 64; self.publish(); self.result("refused", "input inventory")

    def test_input_ids_must_match(self):
        self.doc["input"][0]["id"] = "other"; self.publish(); self.result("refused", "input inventory")

    def test_missing_input_refuses(self):
        self.doc["input"].pop(0); self.publish(); self.result("refused", "input inventory")

    def test_extra_input_refuses(self):
        self.doc["input"].append(dict(id="extra", sha256="a" * 64)); self.publish()
        self.result("refused", "input inventory")

    def test_each_output_field_must_match(self):
        original = deepcopy(self.doc)
        for field, value in (("id", "other"), ("path", "outputs/other.trace"), ("byte_size", 99), ("sha256", "b" * 64)):
            with self.subTest(field=field):
                self.doc = deepcopy(original); self.doc["observation"][0][field] = value
                self.publish(); self.result("refused", "output inventory")

    def test_swapped_output_roles_refuse(self):
        outputs = self.doc["observation"]; outputs[0]["role"], outputs[1]["role"] = outputs[1]["role"], outputs[0]["role"]
        self.publish(); self.result("refused", "output inventory")

    def test_raw_unknown_field_refuses_before_mapping(self):
        self.publish(P.raw(self.doc, "capture").replace(b'(run_id ', b'(invented "bad") (run_id '))
        with mock.patch.object(D, "capture_to_doc", side_effect=AssertionError("mapped invalid raw shape")):
            self.result("refused", "shape")

    def test_duplicate_raw_singular_refuses_before_mapping(self):
        self.publish(P.raw(self.doc, "capture").replace(b'(process_exit ', b'(process_exit 1) (process_exit '))
        with mock.patch.object(D, "capture_to_doc", side_effect=AssertionError("mapped duplicate")):
            self.result("refused", "shape")

    def test_malformed_or_non_utf8_receipt_refuses(self):
        for payload in (b'(capture', b'\xff', b'', P.raw(self.doc, "capture") * 2):
            with self.subTest(payload=payload[:12]):
                self.publish(payload); self.assertEqual(self.result("refused").pin.disposition, "matched")

    def test_changed_bytes_are_stale_without_parsing(self):
        self.path.write_bytes(b"changed")
        with mock.patch.object(F, "parse_capture", side_effect=AssertionError("parsed unauthenticated bytes")):
            self.assertEqual(self.result("stale").pin.disposition, "mismatch")

    def test_changed_hash_same_size_is_stale(self):
        payload = self.path.read_bytes(); self.path.write_bytes(payload.replace(b'"base"', b'"fake"', 1))
        self.result("stale", "SHA256")

    def test_missing_receipt_is_unavailable(self):
        self.path.unlink(); self.result("unavailable")

    def test_symlink_receipt_refuses(self):
        other = self.path.with_name("other"); self.path.rename(other); self.path.symlink_to(other.name)
        self.result("refused")

    def test_exact_inclusive_receipt_bound(self):
        payload = P.raw(self.doc, "capture"); self.publish(payload + b' ' * (65536 - len(payload)))
        self.result("matched")

    def test_oversize_refuses_before_payload_read(self):
        payload = P.raw(self.doc, "capture"); self.publish(payload + b' ' * (65537 - len(payload)))
        original = M.A.os.read; reads = []
        def reading(fd, count):
            reads.append(count); return original(fd, count)
        with mock.patch.object(M.A.os, "read", side_effect=reading): self.result("refused")
        self.assertEqual(reads, [])

    def test_one_bounded_snapshot_and_one_mapper(self):
        with mock.patch.object(M.A, "read_snapshot", wraps=M.A.read_snapshot) as reader, \
             mock.patch.object(D, "capture_to_doc", wraps=D.capture_to_doc) as mapper, \
             mock.patch.object(D, "load", side_effect=AssertionError("unbounded loader")):
            self.result("matched")
        reader.assert_called_once_with(self.root, "observation", self.args["observations"][-1], max_bytes=65536)
        self.assertEqual(mapper.call_count, 1)

    def test_snapshot_is_not_reopened(self):
        reader = M.A.read_snapshot
        def reading(*args, **kwargs):
            snapshot = reader(*args, **kwargs); self.path.write_bytes(b"changed later"); return snapshot
        with mock.patch.object(M.A, "read_snapshot", side_effect=reading): self.result("matched")
        self.result("stale")

    def test_context_is_frozen_before_read(self):
        reader = M.A.read_snapshot
        def reading(*args, **kwargs):
            self.args["run"]["argv"].append("changed later")
            self.args["inputs"][0]["sha256"] = "b" * 64
            self.args["observations"][-1]["path"] = "changed/path"
            self.args["current_candidate"]["binary_sha256"] = "b" * 64
            return reader(*args, **kwargs)
        with mock.patch.object(M.A, "read_snapshot", side_effect=reading):
            result = self.result("matched")
        self.assertEqual(result.facts.argv, tuple(self.doc["argv"]))

    def test_result_and_provenance_are_immutable_and_detached(self):
        result = self.result("matched"); original = result.facts
        self.doc["host"]["os"] = "changed"; self.args["run"]["argv"].clear()
        self.assertEqual(result.facts, original)
        self.assertTrue(all(type(pair) is tuple for pair in result.facts.host + result.facts.tools))
        with self.assertRaises(FrozenInstanceError): result.disposition = "stale"
        with self.assertRaises(FrozenInstanceError): result.facts.process_exit = 1

    def test_selected_input_count_limits_before_io(self):
        for count in (0, 9):
            with self.subTest(count=count):
                self.doc, self.args = fixture()
                self.args["inputs"] = self.args["inputs"][:count] if not count else self.args["inputs"] + [dict(
                    id="extra", role="other", path="inputs/extra", sha256="a" * 64)]
                self.args["run"]["input_ids"] = [item["id"] for item in self.args["inputs"]]
                self.no_io_refusal()

    def test_selected_observation_count_limits_before_io(self):
        for count in (3, 5):
            with self.subTest(count=count):
                self.doc, self.args = fixture()
                self.args["observations"] = self.args["observations"][:count] if count == 3 else self.args["observations"] + [dict(
                    id="extra", role="extra", path="outputs/extra", byte_size=0, sha256="a" * 64)]
                self.no_io_refusal()

    def test_argv_count_limits_before_io(self):
        for argv in ([], ["x"] * 12):
            with self.subTest(count=len(argv)):
                self.args["run"]["argv"] = argv; self.no_io_refusal()

    def test_wrong_context_types_before_io(self):
        original = deepcopy(self.args)
        for field, value in (("run", None), ("current_candidate", None), ("inputs", {}), ("observations", None)):
            with self.subTest(field=field):
                self.args = deepcopy(original); self.args[field] = value; self.no_io_refusal()

    def test_invalid_used_run_fields_before_io(self):
        original = deepcopy(self.args)
        for field, value in (("id", "bad\n"), ("kind", "other"), ("process_exit", True),
                             ("argv", [1]), ("argv", ["x" * 65537]), ("input_ids", [None]), ("observation_ids", [])):
            with self.subTest(field=field):
                self.args = deepcopy(original); self.args["run"][field] = value; self.no_io_refusal()

    def test_candidate_fields_before_io(self):
        for field, value in (("id", "other"), ("binary_sha256", "A" * 64), ("binary_sha256", None)):
            with self.subTest(field=field):
                self.args["current_candidate"] = I.candidate(); self.args["current_candidate"][field] = value
                self.no_io_refusal()

    def test_selected_records_are_canonical_before_io(self):
        original = deepcopy(self.args)
        for family, field, value in (("inputs", "id", "bad\n"), ("inputs", "role", ""),
                                    ("inputs", "path", "../escape"), ("inputs", "sha256", "bad"),
                                    ("observations", "byte_size", -1), ("observations", "byte_size", True)):
            with self.subTest(family=family, field=field):
                self.args = deepcopy(original); self.args[family][0][field] = value; self.no_io_refusal()

    def test_duplicate_selected_ids_or_paths_before_io(self):
        original = deepcopy(self.args)
        for family in ("inputs", "observations"):
            for field in ("id", "path"):
                with self.subTest(family=family, field=field):
                    self.args = deepcopy(original)
                    self.args[family][1][field] = self.args[family][0][field]; self.no_io_refusal()

    def test_input_output_path_alias_before_io(self):
        self.args["inputs"][0]["path"] = self.args["observations"][0]["path"]; self.no_io_refusal()

    def test_run_membership_must_match_selected_context_before_io(self):
        original = deepcopy(self.args)
        for field in ("input_ids", "observation_ids"):
            with self.subTest(field=field):
                self.args = deepcopy(original); self.args["run"][field][0] = "other"; self.no_io_refusal()

    def test_duplicate_run_edges_before_io(self):
        for field in ("input_ids", "observation_ids"):
            with self.subTest(field=field):
                self.doc, self.args = fixture(); self.args["run"][field][1] = self.args["run"][field][0]
                self.no_io_refusal()

    def test_exact_four_output_roles_before_io(self):
        self.args["observations"][0]["role"] = "other"; self.no_io_refusal()

    def test_one_collector_role_before_io(self):
        original = deepcopy(self.args)
        for role in ("other", "collector"):
            with self.subTest(role=role):
                self.args = deepcopy(original)
                self.args["inputs"][5 if role == "other" else 0]["role"] = role
                self.no_io_refusal()

    def test_unavailable_schema_tool_preserves_authenticated_pin(self):
        with mock.patch.object(F, "_schema", side_effect=OSError("synthetic schema I/O failure")):
            try:
                result = self.result("unavailable", "schema")
            except OSError as exc:
                self.fail(f"schema I/O escaped the receipt boundary: {exc}")
            self.assertEqual(result.pin.disposition, "matched")

    def test_matched_pin_without_data_refuses(self):
        reader = M.A.read_snapshot
        def reading(*args, **kwargs): return replace(reader(*args, **kwargs), data=None)
        with mock.patch.object(M.A, "read_snapshot", side_effect=reading): self.result("refused", "immutable")


MUTATIONS = {
    "schema-tool": ('except OSError as exc:\n        return ReceiptCheck("unavailable", f"receipt schema unavailable: {exc}", pin)',
                    'except OSError:\n        raise'),
    "pin-status": ('if pin.disposition != "matched":', 'if False:'),
    "read-bound": ('max_bytes=RECEIPT_BYTES)', 'max_bytes=RECEIPT_BYTES + 1)'),
    "context-counts": ('or not minimum <= len(value) <= maximum:', 'or len(value) < minimum:'),
    "context-edges": ('if set(ids) != {item["id"] for item in records}:', 'if False:'),
    "scalar-binding": ('if doc[field] != expected:', 'if False:'),
    "argv-binding": ('if tuple(doc["argv"]) != context.argv:', 'if False:'),
    "input-binding": ('if inventory != context.inputs:', 'if False:'),
    "output-binding": ('if outputs != context.outputs:', 'if False:'),
    "output-roles": ('if {item["role"] for item in observations} != OUTPUT_ROLES:', 'if False:'),
    "collector-role": ('if len(collectors) != 1:', 'if len(collectors) < 1:'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS); args = parser.parse_args()
    if args.mutation:
        global M
        source = Path(M.__file__).read_text(); before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1: raise SystemExit("mutation seam is not singular")
        module = types.ModuleType("mutated_gpr_receipt"); module.__file__ = M.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), M.__file__, "exec"), module.__dict__); M = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(ReceiptTests))
    print(f"MATCHED-GPR-RECEIPT: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; fixtures cleaned")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
