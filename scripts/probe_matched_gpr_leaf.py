#!/usr/bin/env python3
"""On-volume selected-leaf controls; other declared files deliberately absent."""
from __future__ import annotations

import argparse
import ast
from dataclasses import FrozenInstanceError, replace
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock

import experiment_verification as V
import matched_gpr_leaf as L
import matched_gpr_manifest as M
import probe_matched_gpr_execution as P

ROOT = Path(__file__).resolve().parent.parent


class LeafTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/p4-system-14/a37/leaf-fixtures"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base); self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.experiment, self.candidate = P.fixture()
        self.manifest_record = next(item for item in self.experiment["verification"]["input"]
                                    if item["role"] == "dependency-manifest")
        self.manifest_path = self.root / self.manifest_record["path"]
        self.manifest_path.parent.mkdir(parents=True)
        self.child = dict(id="code dependency", role="implementation", path="source/leaf.dat", sha256="c" * 64)
        self.path = self.root / self.child["path"]; self.path.parent.mkdir()
        self.document = dict(format_version="matched-gpr-dependencies-v1", input=[self.child])
        self.publish(b'(source (name "synthetic"))')

    def bind(self):
        payload = M.F.encode_dependencies(self.document, path=self.manifest_record["path"])
        self.manifest_path.write_bytes(payload)
        self.manifest_record["sha256"] = hashlib.sha256(payload).hexdigest()
        result = M.read_dependency_manifest(self.root, experiment=self.experiment, current_candidate=self.candidate)
        self.assertEqual(result.disposition, "matched", result)
        self.plan = result.plan

    def publish(self, payload):
        self.path.write_bytes(payload); self.child["sha256"] = hashlib.sha256(payload).hexdigest()
        self.bind()

    def nested(self):
        doc = dict(format_version="matched-gpr-dependencies-v1", input=[dict(
            id="unread child", role="implementation", path="never/read.rs", sha256="c" * 64)])
        return M.F.encode_dependencies(doc, path=self.child["path"])

    def result(self, disposition, classification=None, reason=None, **kwargs):
        args = dict(manifest=self.plan, input_id=self.child["id"]); args.update(kwargs)
        try:
            result = L.inspect_dependency_leaf(self.root, **args)
        except (AttributeError, IndexError, TypeError, ValueError, OSError) as exc:
            self.fail(f"selected-leaf refusal escaped as {type(exc).__name__}")
        self.assertEqual(result.disposition, disposition, result)
        self.assertEqual(result.classification, classification, result)
        if reason:
            self.assertIn(reason, result.reason)
        return result

    def no_read(self, reason, **kwargs):
        with mock.patch.object(L.A, "read_snapshot", wraps=L.A.read_snapshot) as read:
            result = self.result("refused", reason=reason, **kwargs)
            self.assertIsNone(result.pin)
            self.assertEqual(read.call_count, 0)

    def test_complete_raw_scoped_parent_and_selected_leaf(self):
        scope = V.Scope("synthetic", frozenset({"sail-riscv"}), frozenset({"REQ-synthetic"}), frozenset({"OBL-synthetic"}))
        self.assertEqual(V.check_experiment(P.raw_experiment(self.experiment, self.candidate), scope), [])
        result = self.result("matched", "non-manifest")
        self.assertEqual((result.pin.record_id, result.pin.path, result.pin.sha256),
                         (self.child["id"], self.child["path"], self.child["sha256"]))
        self.assertIn("qualification pending", result.reason)

    def test_empty_file(self):
        self.publish(b""); result = self.result("matched", "non-manifest")
        self.assertEqual(result.pin.byte_size, 0)

    def test_binary_is_non_manifest(self):
        self.publish(b"\x00\xff"); self.result("matched", "non-manifest")

    def test_undecodable_syntax_is_non_manifest(self):
        self.publish(b"(unfinished"); self.result("matched", "non-manifest")

    def test_unreadable_numeric_atom_is_non_manifest(self):
        self.publish(b"(source 0x_)"); self.result("matched", "non-manifest")

    def test_large_hexadecimal_atom_is_non_manifest(self):
        self.publish(b"(0x" + b"f" * 5000 + b")"); self.result("matched", "non-manifest")

    def test_comment_marker_is_not_a_manifest(self):
        self.publish(b"; (dependencies (unknown 1))\n(source)"); self.result("matched", "non-manifest")

    def test_quoted_marker_is_not_a_manifest(self):
        self.publish(b'"(dependencies (unknown 1))"'); self.result("matched", "non-manifest")

    def test_nested_field_is_not_a_document(self):
        self.publish(b"(source (dependencies (name example)))"); self.result("matched", "non-manifest")

    def test_schema_declaration_is_not_a_document(self):
        self.publish(b"(construct (name dependencies) (field (name input)))"); self.result("matched", "non-manifest")

    def test_disguised_valid_manifest_refuses(self):
        self.publish(self.nested()); result = self.result("refused", "manifest", "nested dependencies")
        self.assertEqual(result.pin.disposition, "matched")
        self.assertFalse((self.root / "never/read.rs").exists())

    def test_bad_manifest_fields_are_not_a_document(self):
        self.publish(b"(dependencies (unknown 1))"); self.result("matched", "non-manifest")

    def test_multiple_roots_are_not_one_document(self):
        self.publish(b"(source) (dependencies) (source)"); self.result("matched", "non-manifest")

    def test_invalid_quoted_head_is_not_a_document(self):
        self.publish(b'("dependencies" (unknown 1))'); self.result("matched", "non-manifest")

    def test_manifest_header_after_comments_refuses(self):
        self.publish(b'; heading\n(comment "annotation") ' + self.nested()); self.result("refused", "manifest")

    def test_oversize_content_cannot_be_a_bounded_document(self):
        self.publish(b'(dependencies (unknown "' + b"x" * M.F.DOCUMENT_BYTES + b'"))')
        with mock.patch.object(L.F, "_document", wraps=L.F._document) as decode:
            self.result("matched", "non-manifest")
            self.assertEqual(decode.call_count, 0)

    def test_valid_python_root_name_is_not_a_manifest(self):
        payload = b'("dependencies", 1)\n'
        ast.parse(payload.decode("utf-8"))
        self.publish(payload); self.result("matched", "non-manifest")

    def test_raw_schema_refusal_precedes_mapper(self):
        payload = self.nested().replace(b"(dependencies", b"(dependencies (unknown 1)", 1)
        self.publish(payload)
        with mock.patch.object(L.F.D, "dependencies_to_doc", wraps=L.F.D.dependencies_to_doc) as mapper:
            self.result("matched", "non-manifest")
            self.assertEqual(mapper.call_count, 0)

    def test_document_uses_single_canonical_mapping(self):
        self.publish(self.nested())
        with mock.patch.object(L.F.D, "dependencies_to_doc", wraps=L.F.D.dependencies_to_doc) as mapper:
            self.result("refused", "manifest")
            self.assertEqual(mapper.call_count, 1)

    def test_semantically_bad_manifest_edges_still_declare_document(self):
        for path, role in [(self.child["path"], "implementation"), ("never/read.rs", "dependency-manifest")]:
            doc = dict(format_version="matched-gpr-dependencies-v1", input=[
                dict(id="nested", role=role, path=path, sha256="c" * 64)])
            payload = M.F.R.render_forms([M.F.D.dependencies_to_form(doc)]).encode("utf-8")
            self.publish(payload)
            with self.subTest(path=path, role=role):
                self.result("refused", "manifest")

    def test_format_cap_is_inclusive(self):
        document = self.nested(); padding = M.F.DOCUMENT_BYTES - len(document) - 2
        payload = b";" + b"x" * padding + b"\n" + document
        self.assertEqual(len(payload), M.F.DOCUMENT_BYTES)
        self.publish(payload); self.result("refused", "manifest")

    def test_known_non_document_sizes_need_no_schema_tools(self):
        for payload in [b"", b"x" * (M.F.DOCUMENT_BYTES + 1)]:
            self.publish(payload)
            with self.subTest(size=len(payload)), mock.patch.object(L.F, "_schema", side_effect=OSError("unavailable")) as tool:
                self.result("matched", "non-manifest")
                self.assertEqual(tool.call_count, 0)

    def test_missing_schema_tool_is_unavailable(self):
        with mock.patch.object(L.F, "_schema", side_effect=OSError("missing schema")):
            result = self.result("unavailable", reason="schema unavailable")
            self.assertEqual(result.pin.disposition, "matched")

    def test_invalid_schema_tool_is_unavailable(self):
        for error in [L.F.K.SchemaError("bad schema"), L.F.S.SexpError("bad schema syntax"), UnicodeError("bad schema text")]:
            with self.subTest(error=type(error).__name__), mock.patch.object(L.F, "_schema", side_effect=error):
                result = self.result("unavailable", reason="schema unavailable")
                self.assertEqual(result.pin.disposition, "matched")

    def test_public_classifier_tool_error_is_distinct(self):
        payload = self.nested()
        for error in [OSError("missing"), L.F.K.SchemaError("bad"), L.F.S.SexpError("bad"), UnicodeError("bad")]:
            with self.subTest(error=type(error).__name__), mock.patch.object(L.F, "_schema", side_effect=error):
                try:
                    L.F.is_dependencies_document(payload, path=self.child["path"])
                except L.F.ArtifactToolError:
                    pass
                except (OSError, L.F.K.SchemaError, L.F.S.SexpError, ValueError) as exc:
                    self.fail(f"public classifier tool error escaped as {type(exc).__name__}")
                else:
                    self.fail("tool failure was classified as content")

    def test_public_classifier_requires_bytes_and_canonical_path(self):
        for payload in [None, bytearray(b"mutable")]:
            with self.subTest(kind=type(payload).__name__), self.assertRaises(L.F.ArtifactError):
                L.F.is_dependencies_document(payload, path=self.child["path"])
        with self.assertRaises(L.F.ArtifactError):
            L.F.is_dependencies_document(b"(source)", path="../outside")

    def test_stale_pin_never_parses(self):
        self.path.write_bytes(self.nested())
        with mock.patch.object(L.F.S, "parse", wraps=L.F.S.parse) as parse:
            result = self.result("stale")
            self.assertEqual(result.pin.disposition, "mismatch")
            self.assertEqual(result.reason, result.pin.reason)
            self.assertEqual(parse.call_count, 0)

    def test_missing_file(self):
        self.path.unlink(); result = self.result("unavailable")
        self.assertEqual(result.reason, result.pin.reason)

    def test_symlink_refuses(self):
        self.path.unlink(); other = self.path.with_name("other"); other.write_bytes(b"data")
        self.path.symlink_to("other"); result = self.result("refused")
        self.assertEqual(result.reason, result.pin.reason)

    def test_nested_git_marker_refuses(self):
        (self.path.parent / ".git").touch(); result = self.result("refused", reason="nested Git")
        self.assertEqual(result.reason, result.pin.reason)

    def test_inclusive_eight_mib_limit(self):
        self.publish(b";" + b"x" * (L.LEAF_BYTES - 1))
        with mock.patch.object(L.A, "read_snapshot", wraps=L.A.read_snapshot) as read:
            result = self.result("matched", "non-manifest")
            self.assertEqual(result.pin.byte_size, L.LEAF_BYTES)
            self.assertEqual(read.call_args.kwargs["max_bytes"], L.LEAF_BYTES)

    def test_oversize_refuses_before_payload_or_parse(self):
        self.publish(b"x" * (L.LEAF_BYTES + 1))
        with mock.patch.object(L.A.os, "read", wraps=L.A.os.read) as read, \
                mock.patch.object(L.F.S, "parse", wraps=L.F.S.parse) as parse:
            self.result("refused", reason="byte limit")
            self.assertEqual(read.call_count, 0); self.assertEqual(parse.call_count, 0)

    def test_custom_limit_bounds_actual_consumption(self):
        self.publish(b";xx"); original = L.A.os.read; consumed = []; remaining = 3
        def read(descriptor, count):
            nonlocal remaining
            self.assertLessEqual(count, remaining)
            data = original(descriptor, count); consumed.append(len(data)); remaining -= len(data)
            return data
        with mock.patch.object(L.A.os, "read", read), \
                mock.patch.object(L.A, "read_snapshot", wraps=L.A.read_snapshot) as snapshots:
            self.result("matched", "non-manifest", max_bytes=3)
            self.assertEqual(snapshots.call_args.kwargs["max_bytes"], 3)
        self.assertEqual(sum(consumed), 3)

    def test_custom_limit_oversize_refuses_before_read(self):
        self.publish(b"four")
        with mock.patch.object(L.A.os, "read", wraps=L.A.os.read) as read:
            self.result("refused", reason="byte limit", max_bytes=3)
            self.assertEqual(read.call_count, 0)

    def test_zero_limit_empty_file(self):
        self.publish(b"")
        with mock.patch.object(L.A.os, "read", wraps=L.A.os.read) as read, \
                mock.patch.object(L.A, "read_snapshot", wraps=L.A.read_snapshot) as snapshots:
            self.result("matched", "non-manifest", max_bytes=0)
            self.assertEqual(read.call_count, 0)
            self.assertEqual(snapshots.call_args.kwargs["max_bytes"], 0)

    def test_zero_limit_nonempty_file(self):
        with mock.patch.object(L.A.os, "read", wraps=L.A.os.read) as read:
            self.result("refused", reason="byte limit", max_bytes=0)
            self.assertEqual(read.call_count, 0)

    def test_invalid_limits_do_not_open(self):
        for limit in [-1, True, False, L.LEAF_BYTES + 1, 1.0, None, "3"]:
            with self.subTest(limit=limit):
                self.no_read("byte limit", max_bytes=limit)

    def test_child_and_union_counts_before_lookup(self):
        for plan in [replace(self.plan, child_input_ids=()),
                     replace(self.plan, child_input_ids=(self.child["id"],) * 65),
                     replace(self.plan, inputs=self.plan.inputs[:8]),
                     replace(self.plan, inputs=(self.plan.inputs[0],) * 74)]:
            with self.subTest(plan_lengths=(len(plan.child_input_ids), len(plan.inputs))):
                self.no_read("counts", manifest=plan)

    def test_selected_edge_absent_or_duplicated(self):
        cases = [dict(input_id=self.plan.relations.execution.common_inputs[0].input_id),
                 dict(manifest=replace(self.plan, child_input_ids=(self.child["id"],) * 2))]
        for index, args in enumerate(cases):
            with self.subTest(case=index):
                self.no_read("selected child edge", **args)

    def test_selected_binding_absent_or_duplicated(self):
        binding = next(item for item in self.plan.inputs if item.input_id == self.child["id"])
        for items in [tuple(item for item in self.plan.inputs if item != binding), (*self.plan.inputs, binding)]:
            with self.subTest(count=len(items)):
                self.no_read("selected child binding", manifest=replace(self.plan, inputs=items))

    def test_manifest_cannot_be_selected_as_child(self):
        plan = replace(self.plan, child_input_ids=(self.plan.manifest_input_id,))
        self.no_read("manifest itself", manifest=plan, input_id=plan.manifest_input_id)

    def test_declared_nested_role_cannot_be_selected(self):
        items = tuple(replace(item, role="dependency-manifest") if item.input_id == self.child["id"] else item
                      for item in self.plan.inputs)
        self.no_read("nested manifest role", manifest=replace(self.plan, inputs=items))

    def test_maximum_union_reads_only_selected_child(self):
        self.document["input"] += [dict(id=f"ghost{n}", role="implementation", path=f"absent/{n}", sha256="c" * 64)
                                   for n in range(63)]
        self.bind(); self.assertEqual((len(self.plan.inputs), len(self.plan.child_input_ids)), (73, 64))
        with mock.patch.object(L.A, "read_snapshot", wraps=L.A.read_snapshot) as read:
            self.result("matched", "non-manifest")
            self.assertEqual(read.call_count, 1)
            self.assertEqual(read.call_args.args[2]["path"], self.child["path"])
        self.assertFalse((self.root / "absent").exists())

    def test_declared_exact_principal_overlap_is_a_child(self):
        principal = next(item for item in self.experiment["verification"]["input"] if item["role"] == "guest-source")
        path = self.root / principal["path"]; path.write_bytes(b"; synthetic source")
        principal["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.document["input"].append(dict(principal)); self.bind()
        self.assertEqual(len(self.plan.inputs), 10)
        self.result("matched", "non-manifest", input_id=principal["id"])

    def test_one_snapshot_no_legacy_reopen_codec_or_process(self):
        with mock.patch.object(L.A, "read_snapshot", wraps=L.A.read_snapshot) as read, \
                mock.patch.object(L.A, "read_pinned", wraps=L.A.read_pinned) as legacy, \
                mock.patch.object(L.A, "read_bounded_pin", wraps=L.A.read_bounded_pin) as pin, \
                mock.patch.object(Path, "read_bytes", autospec=True, side_effect=Path.read_bytes) as reopen, \
                mock.patch.object(Path, "read_text", autospec=True, side_effect=Path.read_text) as text, \
                mock.patch.object(M.F, "parse_dependencies", wraps=M.F.parse_dependencies) as mapper, \
                mock.patch.object(subprocess, "run", wraps=subprocess.run) as process:
            self.result("matched", "non-manifest")
            self.assertEqual(read.call_count, 1)
            self.assertEqual((legacy.call_count, pin.call_count, reopen.call_count, text.call_count, mapper.call_count, process.call_count), (0,) * 6)

    def test_snapshot_not_later_changed_path_drives_classification(self):
        read = L.A.read_snapshot
        def changed(*args, **kwargs):
            result = read(*args, **kwargs); self.path.write_bytes(self.nested()); return result
        with mock.patch.object(L.A, "read_snapshot", changed):
            self.result("matched", "non-manifest")
        self.result("stale")

    def test_snapshot_manifest_cannot_be_hidden_by_later_path(self):
        self.publish(self.nested()); read = L.A.read_snapshot
        def changed(*args, **kwargs):
            result = read(*args, **kwargs); self.path.write_bytes(b"(source)"); return result
        with mock.patch.object(L.A, "read_snapshot", changed):
            self.result("refused", "manifest", "nested dependencies")

    def test_inconsistent_payload_refuses_before_parse(self):
        read = L.A.read_snapshot
        for data in [None, bytearray(b"mutable"), b"different-size"]:
            def inconsistent(*args, **kwargs):
                return replace(read(*args, **kwargs), data=data)
            with self.subTest(kind=type(data).__name__), mock.patch.object(L.A, "read_snapshot", inconsistent), \
                    mock.patch.object(L.F.S, "parse", wraps=L.F.S.parse) as parse:
                self.result("refused", reason="snapshot payload")
                self.assertEqual(parse.call_count, 0)

    def test_inconsistent_payload_limit_refuses_before_parse(self):
        read = L.A.read_snapshot
        def inconsistent(*args, **kwargs):
            result = read(*args, **kwargs); data = b"(source)"
            return replace(result, data=data, pin=replace(result.pin, byte_size=len(data)))
        self.publish(b"")
        with mock.patch.object(L.A, "read_snapshot", inconsistent), mock.patch.object(L.F.S, "parse", wraps=L.F.S.parse) as parse:
            self.result("refused", reason="snapshot payload", max_bytes=0)
            self.assertEqual(parse.call_count, 0)

    def test_result_is_frozen_and_retains_no_payload(self):
        result = self.result("matched", "non-manifest")
        with self.assertRaises(FrozenInstanceError):
            result.classification = "forged"
        with self.assertRaises(FrozenInstanceError):
            result.pin.sha256 = "0" * 64
        self.assertFalse(hasattr(result, "data"))


MUTATIONS = {
    "family-counts": ('_require(1 <= len(manifest.child_input_ids) <= F.MANIFEST_INPUTS and\n'
                      '             9 <= len(manifest.inputs) <= 9 + F.MANIFEST_INPUTS,', '_require(True,'),
    "selected-edge": ('_require(manifest.child_input_ids.count(input_id) == 1,', '_require(True,'),
    "selected-binding": ('_require(len(selected) == 1,', '_require(True,'),
    "manifest-selection": ('_require(binding.input_id != manifest.manifest_input_id and binding.role != "dependency-manifest",', '_require(True,'),
    "byte-limit": ('if type(max_bytes) is not int or not 0 <= max_bytes <= LEAF_BYTES:', 'if False:'),
    "read-bound": ('record, max_bytes=max_bytes)', 'record, max_bytes=LEAF_BYTES)'),
    "pin-status": ('if pin.disposition != "matched":', 'if False:'),
    "payload-consistency": ('if type(data) is not bytes or len(data) > max_bytes or pin.byte_size != len(data):', 'if False:'),
    "document-classification": ('F.is_dependencies_document(data, path=path)', 'False'),
    "no-nesting": ('if classification == "manifest":', 'if False:'),
    "snapshot-reopen": ('data = snapshot.data', 'data = (root / record["path"]).read_bytes()'),
    "immutable-result": ('@dataclass(frozen=True)', '@dataclass'),
}


ARTIFACT_MUTATIONS = {
    "document-bound": ('if not payload or len(payload) > DOCUMENT_BYTES:', 'if False:'),
    "schema-preflight": ('_schema("dependencies")', 'pass'),
    "schema-before-map": ('if errors:', 'if False:'),
}


def main():
    global L
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=[*MUTATIONS, *ARTIFACT_MUTATIONS])
    args = parser.parse_args()
    if args.mutation in ARTIFACT_MUTATIONS:
        source = Path(L.F.__file__).read_text()
        before, after = ARTIFACT_MUTATIONS[args.mutation]
        if args.mutation != "schema-before-map":
            start = source.index("def is_dependencies_document(")
            end = source.index("\n\ndef parse_capture(", start)
            prefix, selected, suffix = source[:start], source[start:end], source[end:]
        else:
            prefix, selected, suffix = "", source, ""
        if selected.count(before) != 1:
            raise RuntimeError("artifact mutation site count changed")
        module = types.ModuleType("leaf_artifact_mutant"); module.__file__ = L.F.__file__
        sys.modules[module.__name__] = module
        exec(compile(prefix + selected.replace(before, after) + suffix, L.F.__file__, "exec"), module.__dict__)
        L.F = module
    elif args.mutation:
        source = Path(L.__file__).read_text(); before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("mutation site count changed")
        module = types.ModuleType("leaf_mutant"); module.__file__ = L.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), L.__file__, "exec"), module.__dict__)
        L = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(LeafTests))
    print(f"MATCHED-GPR-LEAF: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; fixtures cleaned")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
