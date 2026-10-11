#!/usr/bin/env python3
"""Offline descriptor controls with owned on-volume files, never capture evidence."""
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
import matched_gpr_identity as M
import records_sexp as R


def candidate():
    return dict(id="sail-riscv", role="reference", status="obtained", kind="executable",
                origin="https://example.invalid/sail", lineage="unknown; synthetic fixture",
                binary="reference/bin/sail", binary_sha256="a" * 64)


def document(item=None):
    return dict(profile="synthetic", retrieved="2026-10-11", work_dir="reference",
                host=dict(os="fixture", kernel="fixture", arch="fixture", cxx="fixture"),
                candidate=[candidate() if item is None else item])


def encode(doc):
    return R.render_forms([D.references_to_form(doc)]).encode()


class IdentityTests(unittest.TestCase):
    def setUp(self):
        base = M.ROOT / "target/p4-system-14/a30/identity-fixtures"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.current = candidate()
        self.path = self.root / "identity.sexp"
        self.publish(encode(document()))

    def publish(self, payload):
        self.path.write_bytes(payload)
        self.record = dict(id="identity", role="reference-identity", path="identity.sexp",
                           sha256=hashlib.sha256(payload).hexdigest())

    def result(self, disposition, reason=None):
        result = M.read_reference_identity(self.root, self.record, self.current)
        self.assertEqual(result.disposition, disposition, result)
        if reason: self.assertIn(reason, result.reason)
        if disposition != "matched": self.assertEqual(result.execution_identity, ())
        return result

    def no_io_refusal(self):
        with mock.patch.object(M.A, "read_snapshot", side_effect=AssertionError("unexpected I/O")):
            self.assertIsNone(self.result("refused").pin)

    def test_positive_without_binary_cache(self):
        result = self.result("matched", "qualification pending")
        self.assertEqual(result.pin.disposition, "matched")
        self.assertEqual(result.execution_identity,
                         tuple((key, self.current[key]) for key in M.REQUIRED_FIELDS))
        self.assertFalse((self.root / self.current["binary"]).exists())

    def test_all_optional_fields_match(self):
        self.current.update(release="v1", version="1.0", source_commit="abc", asset="sail.zip",
                            asset_sha256="b" * 64)
        self.publish(encode(document(deepcopy(self.current))))
        self.assertEqual(dict(self.result("matched").execution_identity).get("asset_sha256"), "b" * 64)

    def test_required_execution_value_changes_are_stale(self):
        for field, value in dict(origin="different", kind="other", binary="other/sail",
                                 binary_sha256="b" * 64).items():
            with self.subTest(field=field):
                retained = candidate(); retained[field] = value
                self.publish(encode(document(retained)))
                self.assertEqual(self.result("stale", "differs").pin.disposition, "matched")

    def test_optional_execution_value_changes_are_stale(self):
        for field in M.OPTIONAL_FIELDS:
            with self.subTest(field=field):
                first, second = ("a" * 64, "b" * 64) if field == "asset_sha256" else ("a", "b")
                self.current = candidate(); self.current[field] = first
                retained = deepcopy(self.current); retained[field] = second
                self.publish(encode(document(retained))); self.result("stale")

    def test_optional_retained_only_is_stale(self):
        for field in M.OPTIONAL_FIELDS:
            with self.subTest(field=field):
                retained = candidate(); retained[field] = "b" * 64 if field == "asset_sha256" else "v"
                self.publish(encode(document(retained))); self.result("stale")

    def test_optional_current_only_is_stale(self):
        for field in M.OPTIONAL_FIELDS:
            with self.subTest(field=field):
                self.current = candidate(); self.current[field] = "b" * 64 if field == "asset_sha256" else "v"
                self.result("stale")

    def test_empty_optional_presence_is_not_absence(self):
        retained = candidate(); retained["version"] = ""
        self.publish(encode(document(retained))); self.result("stale")
        self.current["version"] = ""; self.result("matched")

    def test_descriptive_metadata_is_not_execution_identity(self):
        retained = candidate()
        retained.update(status="historical", role="descriptive", lineage="still unknown",
                        matched_scope="different prose", build_note="another note")
        doc = document(retained); doc.update(retrieved="older", work_dir="historical")
        doc["host"]["os"] = "older host"
        self.publish(encode(doc)); self.result("matched")

    def test_unknown_raw_field_refuses_before_mapper(self):
        self.publish(encode(document()).replace(b'(kind ', b'(invented "bad") (kind '))
        with mock.patch.object(D, "references_to_doc", side_effect=AssertionError("mapped bad shape")):
            self.result("refused", "identity shape")

    def test_duplicate_singular_refuses_before_mapper(self):
        self.publish(encode(document()).replace(b'(kind ', b'(kind "other") (kind '))
        with mock.patch.object(D, "references_to_doc", side_effect=AssertionError("mapped duplicate")):
            self.result("refused", "identity shape")

    def test_wrong_raw_type_refuses_before_mapper(self):
        self.publish(encode(document()).replace(b'(kind "executable")', b'(kind 7)'))
        with mock.patch.object(D, "references_to_doc", side_effect=AssertionError("mapped wrong type")):
            self.result("refused", "identity shape")

    def test_malformed_sexp_refuses(self):
        self.publish(b'(references'); self.result("refused")

    def test_non_utf8_refuses(self):
        self.publish(b'\xff'); self.assertEqual(self.result("refused").pin.disposition, "matched")

    def test_empty_file_refuses(self):
        self.publish(b''); self.result("refused", "immutable bytes")

    def test_comment_only_refuses(self):
        self.publish(b'(comment "only")'); self.result("refused", "one references")

    def test_comments_around_one_root_are_allowed(self):
        self.publish(b'(comment "before")\n' + encode(document()) + b'(comment "after")\n')
        self.result("matched")

    def test_two_references_roots_refuse(self):
        self.publish(encode(document()) * 2); self.result("refused", "one references")

    def test_valid_non_references_root_refuses(self):
        self.publish(R.render_forms([D.references_to_form(document())[4]]).encode())
        self.result("refused")

    def test_multiple_candidates_refuse(self):
        doc = document(); doc["candidate"].append(candidate())
        self.publish(encode(doc)); self.result("refused", "one candidate")

    def test_no_candidate_refuses(self):
        doc = document(); doc["candidate"] = []
        self.publish(encode(doc)); self.result("refused", "identity shape")

    def test_experiments_refuse(self):
        payload = encode(document()).rstrip()
        experiment = b'''(experiment (id "old") (program "old.s") (instructions 1)
          (models "sail-riscv") (verdict "AGREE") (reproduced "fixture") (control "fixture"))'''
        self.publish(payload[:-1] + experiment + b')\n')
        self.result("refused", "no experiments")

    def test_non_sail_candidate_refuses(self):
        retained = candidate(); retained["id"] = "other"
        self.publish(encode(document(retained))); self.result("refused", "sail-riscv")

    def test_schema_optional_execution_fields_are_method_required(self):
        for field in ("kind", "binary", "binary_sha256"):
            with self.subTest(field=field):
                retained = candidate(); del retained[field]
                self.publish(encode(document(retained))); self.result("refused", field)

    def test_bad_retained_digest_refuses(self):
        retained = candidate(); retained["asset_sha256"] = "B" * 64
        self.publish(encode(document(retained))); self.result("refused", "identity shape")

    def test_unsafe_retained_binary_identity_refuses(self):
        for path in ("/absolute/sail", "../sail", "a//sail", "a\\sail", "a:sail"):
            with self.subTest(path=path):
                retained = candidate(); retained["binary"] = path
                self.publish(encode(document(retained))); self.result("refused", "binary identity")

    def test_unsafe_artifact_path_refuses(self):
        self.record["path"] = "../identity.sexp"
        self.assertEqual(self.result("refused").pin.disposition, "refused")

    def test_symlink_artifact_refuses(self):
        other = self.root / "other.sexp"; self.path.rename(other); self.path.symlink_to(other.name)
        self.result("refused")

    def test_nested_git_marker_refuses(self):
        nested = self.root / "nested"; nested.mkdir(); (nested / ".git").write_text("fixture marker")
        self.path.rename(nested / self.path.name); self.record["path"] = "nested/identity.sexp"
        self.result("refused", "nested Git")

    def test_missing_artifact_is_unavailable(self):
        self.path.unlink(); self.assertEqual(self.result("unavailable").pin.disposition, "unavailable")

    def test_changed_pin_is_stale_with_no_parse(self):
        self.path.write_bytes(b"different bytes")
        with mock.patch.object(M, "_descriptor", side_effect=AssertionError("parsed unauthenticated bytes")):
            self.assertEqual(self.result("stale").pin.disposition, "mismatch")

    def test_exact_inclusive_byte_limit(self):
        payload = encode(document()); self.publish(payload + b" " * (65536 - len(payload)))
        self.result("matched")

    def test_oversized_file_refuses_before_payload_read(self):
        payload = encode(document()); self.publish(payload + b" " * (65537 - len(payload)))
        original = M.A.os.read
        reads = []
        def reading(fd, count):
            reads.append(count); return original(fd, count)
        with mock.patch.object(M.A.os, "read", side_effect=reading):
            self.result("refused")
        self.assertEqual(reads, [], "oversized descriptor must refuse before payload I/O")

    def test_one_bounded_snapshot_and_one_mapping(self):
        with mock.patch.object(M.A, "read_snapshot", wraps=M.A.read_snapshot) as reader, \
             mock.patch.object(D, "references_to_doc", wraps=D.references_to_doc) as mapper, \
             mock.patch.object(D, "load", side_effect=AssertionError("unbounded loader")):
            self.result("matched")
        reader.assert_called_once_with(self.root, "input", self.record, max_bytes=65536)
        self.assertEqual(mapper.call_count, 1)

    def test_snapshot_is_not_reopened_after_authentication(self):
        reader = M.A.read_snapshot
        def reading(*args, **kwargs):
            snapshot = reader(*args, **kwargs)
            self.path.write_bytes(b"changed after snapshot")
            return snapshot
        with mock.patch.object(M.A, "read_snapshot", side_effect=reading): self.result("matched")
        self.result("stale")

    def test_results_are_frozen_and_detached(self):
        result = self.result("matched"); original = result.execution_identity
        self.current["origin"] = "changed later"; self.record["sha256"] = "b" * 64
        self.assertEqual(result.execution_identity, original)
        with self.assertRaises(FrozenInstanceError): result.disposition = "stale"
        with self.assertRaises(FrozenInstanceError): result.pin.reason = "changed"
        self.assertTrue(all(type(pair) is tuple for pair in original))

    def test_missing_current_fields_refuse_before_io(self):
        for field in M.REQUIRED_FIELDS:
            with self.subTest(field=field):
                self.current = candidate(); del self.current[field]; self.no_io_refusal()

    def test_invalid_current_fields_refuse_before_io(self):
        for field, value in (("id", "other"), ("kind", ""), ("origin", 1), ("binary", "../sail"),
                             ("binary_sha256", "A" * 64), ("asset_sha256", "bad"), ("version", None)):
            with self.subTest(field=field, value=value):
                self.current = candidate(); self.current[field] = value; self.no_io_refusal()

    def test_invalid_request_role_or_id_refuses_before_io(self):
        original = deepcopy(self.record)
        for field, value in (("role", "collector"), ("id", "bad\n"), ("id", None)):
            with self.subTest(field=field):
                self.record = deepcopy(original); self.record[field] = value; self.no_io_refusal()

    def test_non_dictionary_request_refuses_before_io(self):
        original = self.record
        self.record = None; self.no_io_refusal()
        self.record = original; self.current = None; self.no_io_refusal()

    def test_matched_pin_without_snapshot_data_refuses(self):
        snapshot = M.A.read_snapshot(self.root, "input", self.record, max_bytes=65536)
        with mock.patch.object(M.A, "read_snapshot", return_value=replace(snapshot, data=None)):
            self.result("refused", "immutable bytes")


MUTATIONS = {
    "pin-status": ('if pin.disposition != "matched":', 'if False:'),
    "read-bound": ('max_bytes=IDENTITY_BYTES)', 'max_bytes=IDENTITY_BYTES + 1)'),
    "raw-schema": ('if errors:', 'if False:'),
    "root-count": ('if len(forms) != 1 or forms[0][0] != "references":',
                   'if not forms or forms[0][0] != "references":'),
    "candidate-count": ('if len(doc.get("candidate", [])) != 1 or doc.get("experiment", []):',
                        'if not doc.get("candidate", []) or doc.get("experiment", []):'),
    "experiment-free": ('if len(doc.get("candidate", [])) != 1 or doc.get("experiment", []):',
                        'if len(doc.get("candidate", [])) != 1:'),
    "identity-equality": ('if retained != current:', 'if False:'),
    "optional-presence": ('for field in REQUIRED_FIELDS + OPTIONAL_FIELDS',
                          'for field in REQUIRED_FIELDS'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        global M
        source = Path(M.__file__).read_text(); before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1: raise SystemExit("mutation seam is not singular")
        module = types.ModuleType("mutated_gpr_identity"); module.__file__ = M.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), M.__file__, "exec"), module.__dict__)
        M = module
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(IdentityTests)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"MATCHED-GPR-IDENTITY: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; fixtures cleaned")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
