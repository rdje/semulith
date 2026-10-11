#!/usr/bin/env python3
"""On-volume manifest binding controls; declared child files deliberately absent."""
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
import experiment_verification as V
import matched_gpr_manifest as M
import probe_matched_gpr_execution as P

ROOT = Path(__file__).resolve().parent.parent


class ManifestTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/p4-system-14/a34/manifest-fixtures"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base); self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.experiment, self.candidate = P.fixture(); self.graph = self.experiment["verification"]
        self.record = next(item for item in self.graph["input"] if item["role"] == "dependency-manifest")
        self.path = self.root / self.record["path"]; self.path.parent.mkdir()
        self.doc = dict(format_version="matched-gpr-dependencies-v1",
                        input=[dict(id="code dependency", role="implementation", path="source/code.py", sha256="c" * 64)])
        self.publish()

    def publish(self, payload=None):
        if payload is None: payload = M.F.encode_dependencies(self.doc, path=self.record["path"])
        self.path.write_bytes(payload); self.record["sha256"] = hashlib.sha256(payload).hexdigest()

    def result(self, disposition, reason=None):
        try:
            result = M.read_dependency_manifest(self.root, experiment=self.experiment, current_candidate=self.candidate)
        except OSError as exc:
            self.fail(f"schema-tool I/O escaped manifest consumer: {exc}")
        self.assertEqual(result.disposition, disposition, result)
        if reason: self.assertIn(reason, result.reason)
        if disposition != "matched": self.assertIsNone(result.plan)
        return result

    def test_complete_scoped_parent_and_authenticated_manifest(self):
        scope = V.Scope("synthetic", frozenset({"sail-riscv"}), frozenset({"REQ-synthetic"}),
                        frozenset({"OBL-synthetic"}))
        self.assertEqual(V.check_experiment(P.raw_experiment(self.experiment, self.candidate), scope), [])
        result = self.result("matched", "complete closure/qualification pending")
        self.assertEqual(result.pin.disposition, "matched")
        self.assertEqual(result.plan.manifest_input_id, "dependency-manifest")
        self.assertEqual(result.plan.child_input_ids, ("code dependency",))
        self.assertEqual(len(result.plan.inputs), 10)

    def test_children_binary_and_outputs_are_not_read(self):
        self.assertFalse((self.root / "source").exists())
        self.assertFalse((self.root / "outputs").exists())
        self.assertFalse((self.root / self.candidate["binary"]).exists())
        with mock.patch("subprocess.run", side_effect=AssertionError("unexpected process")), \
             mock.patch("subprocess.Popen", side_effect=AssertionError("unexpected process")):
            self.result("matched")

    def test_coherent_failed_controls_remain_data(self):
        self.graph["run"][2].update(process_exit=127, verdict="REFUSED")
        self.graph["control_run"][0]["observed_verdict"] = "REFUSED"
        self.assertEqual(self.result("matched").plan.relations.control_observed_verdict, "REFUSED")

    def test_exact_principal_overlap_is_counted_once(self):
        self.doc["input"] = [deepcopy(self.graph["input"][0])]; self.publish()
        plan = self.result("matched").plan
        self.assertEqual(len(plan.inputs), 9)
        self.assertEqual(plan.child_input_ids, ("guest-source",))

    def test_manifest_children_are_unordered(self):
        self.doc["input"].append(dict(id="other", role="definition", path="definitions/example.sexp", sha256="d" * 64))
        self.publish(); first = self.result("matched").plan
        self.doc["input"].reverse(); self.publish(); second = self.result("matched").plan
        # Manifest bytes/pin change with order; all other file/child declarations do not.
        def nonmanifest(plan): return tuple(item for item in plan.inputs if item.role != "dependency-manifest")
        self.assertEqual(nonmanifest(first), nonmanifest(second))
        self.assertEqual(first.child_input_ids, second.child_input_ids)

    def test_inclusive_64_children_and_73_union(self):
        self.doc["input"] = [dict(id=f"leaf-{n}", role="definition", path=f"deps/{n}", sha256="c" * 64) for n in range(64)]
        self.publish(); self.assertEqual(len(self.result("matched").plan.inputs), 73)

    def test_65_children_refuse(self):
        self.doc["input"] = [dict(id=f"leaf-{n}", role="definition", path=f"deps/{n}", sha256="c" * 64) for n in range(65)]
        self.publish(M.F.R.render_forms([D.dependencies_to_form(self.doc)]).encode())
        self.result("refused", "more than 64")

    def test_principal_identity_conflicts_refuse(self):
        original = deepcopy(self.graph["input"][0])
        for field, value in (("role", "other"), ("path", "other/source.s"), ("sha256", "d" * 64)):
            with self.subTest(field=field):
                self.doc["input"] = [dict(original, **{field: value})]; self.publish()
                self.result("refused", "principal identity")

    def test_principal_path_cannot_gain_another_id(self):
        self.doc["input"][0]["path"] = "inputs/guest-source"; self.publish()
        self.result("refused", "another input identity")

    def test_manifest_child_cannot_alias_output(self):
        self.doc["input"][0]["path"] = self.graph["observation"][0]["path"]; self.publish()
        self.result("refused", "run output")

    def test_self_path_refuses(self):
        self.doc["input"][0]["path"] = self.record["path"]
        self.publish(M.F.R.render_forms([D.dependencies_to_form(self.doc)]).encode())
        self.result("refused", "self reference")

    def test_self_id_with_other_path_refuses(self):
        self.doc["input"][0]["id"] = self.record["id"]; self.publish()
        self.result("refused", "principal identity")

    def test_lexical_nested_manifest_role_refuses(self):
        self.doc["input"][0]["role"] = "dependency-manifest"
        self.publish(M.F.R.render_forms([D.dependencies_to_form(self.doc)]).encode())
        self.result("refused", "nested manifest role")

    def test_duplicate_child_ids_and_paths_refuse(self):
        original = deepcopy(self.doc["input"][0])
        for field in ("id", "path"):
            with self.subTest(field=field):
                other = dict(id="other", role="definition", path="deps/other", sha256="d" * 64)
                other[field] = original[field]; self.doc["input"] = [original, other]
                self.publish(M.F.R.render_forms([D.dependencies_to_form(self.doc)]).encode())
                self.result("refused", "duplicate")

    def test_noncanonical_child_path_refuses(self):
        for path in ("../code", "/code", "a//code", "a\\code", "a:code"):
            with self.subTest(path=path):
                self.doc["input"][0]["path"] = path
                self.publish(M.F.R.render_forms([D.dependencies_to_form(self.doc)]).encode())
                self.result("refused", "noncanonical")

    def test_unknown_raw_field_refuses_before_mapping(self):
        payload = self.path.read_bytes().replace(b'(role ', b'(invented "bad") (role ')
        self.publish(payload)
        with mock.patch.object(D, "dependencies_to_doc", wraps=D.dependencies_to_doc) as mapper:
            self.result("refused")
        self.assertEqual(mapper.call_count, 0, "invalid raw shape reached the mapper")

    def test_wrong_raw_type_and_digest_refuse(self):
        original = self.path.read_bytes()
        for bad in (original.replace(b'(role "implementation")', b'(role 7)'),
                    original.replace(b'"' + b'c' * 64 + b'"', b'"bad"')):
            with self.subTest(payload=bad): self.publish(bad); self.result("refused")

    def test_empty_malformed_non_utf8_and_multiple_roots_refuse(self):
        original = self.path.read_bytes()
        for payload in (b'', b'(', b'\xff', original * 2):
            with self.subTest(payload=payload[:20]): self.publish(payload); self.result("refused")

    def test_comments_around_one_manifest_are_allowed(self):
        self.publish(b'(comment "before")\n' + self.path.read_bytes() + b'(comment "after")\n')
        self.result("matched")

    def test_inclusive_64k_payload(self):
        payload = self.path.read_bytes(); self.publish(payload + b' ' * (65536 - len(payload)))
        self.result("matched")

    def test_oversized_refuses_before_payload_io(self):
        payload = self.path.read_bytes(); self.publish(payload + b' ' * (65537 - len(payload)))
        original = M.A.os.read; reads = []
        def reading(fd, count): reads.append(count); return original(fd, count)
        with mock.patch.object(M.A.os, "read", side_effect=reading): self.result("refused")
        self.assertEqual(reads, [], "oversized manifest must refuse before payload I/O")

    def test_changed_pin_is_stale_without_parse(self):
        self.path.write_bytes(b'changed')
        with mock.patch.object(M.F, "parse_dependencies", side_effect=AssertionError("parsed unpinned bytes")):
            self.assertEqual(self.result("stale").pin.disposition, "mismatch")

    def test_missing_manifest_is_unavailable(self):
        self.path.unlink(); self.assertEqual(self.result("unavailable").pin.disposition, "unavailable")

    def test_symlink_manifest_refuses(self):
        other = self.path.with_name("other"); self.path.rename(other); self.path.symlink_to(other.name)
        self.result("refused")

    def test_nested_git_boundary_refuses(self):
        (self.path.parent / ".git").write_text("fixture marker")
        self.result("refused", "nested Git")

    def test_bad_parent_refuses_before_io(self):
        self.graph["run"][0]["argv"][0] = "wrong/binary"
        with mock.patch.object(M.A, "read_snapshot", side_effect=AssertionError("unexpected I/O")):
            self.assertIsNone(self.result("refused", "relations:").pin)

    def test_legacy_and_other_rule_are_unsupported_before_io(self):
        with mock.patch.object(M.A, "read_snapshot", side_effect=AssertionError("unexpected I/O")):
            self.graph["comparison_rule"] = "other"; self.result("unsupported")
            del self.experiment["verification"]; self.result("unsupported")

    def test_one_bounded_snapshot_one_mapping_and_no_loader(self):
        with mock.patch.object(M.A, "read_snapshot", wraps=M.A.read_snapshot) as reader, \
             mock.patch.object(D, "dependencies_to_doc", wraps=D.dependencies_to_doc) as mapper, \
             mock.patch.object(D, "load", side_effect=AssertionError("unexpected loader")):
            self.result("matched")
        reader.assert_called_once_with(self.root, "input", self.record, max_bytes=65536)
        self.assertEqual(mapper.call_count, 1)

    def test_snapshot_is_not_reopened(self):
        original = M.A.read_snapshot
        def reading(*args, **kwargs):
            snapshot = original(*args, **kwargs); self.path.write_bytes(b'later change'); return snapshot
        with mock.patch.object(M.A, "read_snapshot", side_effect=reading): self.result("matched")
        self.result("stale")

    def test_parent_context_is_frozen_before_io(self):
        original = M.A.read_snapshot
        def reading(*args, **kwargs):
            snapshot = original(*args, **kwargs)
            self.graph["observation"][0]["path"] = self.doc["input"][0]["path"]
            self.graph["input"][0]["sha256"] = "f" * 64
            self.candidate["binary"] = "changed/later"
            return snapshot
        with mock.patch.object(M.A, "read_snapshot", side_effect=reading):
            result = self.result("matched")
        self.assertEqual(result.plan.relations.execution.binary_path, "reference/bin/sail")

    def test_results_and_all_nested_bindings_are_frozen(self):
        result = self.result("matched"); original = deepcopy(result)
        self.doc["input"][0]["path"] = "changed"; self.record["sha256"] = "f" * 64
        self.assertEqual(result, original)
        for obj, field in ((result, "reason"), (result.pin, "sha256"), (result.plan, "manifest_input_id"),
                           (result.plan.inputs[0], "path"), (result.plan.relations.witness, "register")):
            with self.subTest(field=field), self.assertRaises(FrozenInstanceError): setattr(obj, field, "changed")
        self.assertIs(type(result.plan.inputs), tuple); self.assertIs(type(result.plan.child_input_ids), tuple)

    def test_schema_tool_io_is_unavailable_with_matched_pin(self):
        with mock.patch.object(M.F, "parse_dependencies", side_effect=OSError("schema fixture")):
            self.assertEqual(self.result("unavailable", "schema unavailable").pin.disposition, "matched")

    def test_matched_pin_without_data_refuses(self):
        snapshot = M.A.read_snapshot(self.root, "input", self.record, max_bytes=65536)
        with mock.patch.object(M.A, "read_snapshot", return_value=replace(snapshot, data=None)):
            self.result("refused", "immutable")


MUTATIONS = {
    "pin-status": ('if pin.disposition != "matched":', 'if False:'),
    "read-bound": ('max_bytes=F.DOCUMENT_BYTES)', 'max_bytes=F.DOCUMENT_BYTES + 1)'),
    "manifest-codec": ('document = F.parse_dependencies(snapshot.data, path=manifest.path)',
                       'document = _unchecked_manifest(snapshot.data, manifest.path)'),
    "principal-overlap": ('child == by_id[child.input_id],', 'True,'),
    "path-alias": ('child.path not in by_path,', 'True,'),
    "output-alias": ('child.path not in context.output_paths,', 'True,'),
    "context-freeze": ('plan = _bind(context, document)', 'plan = _bind(_context(experiment, relations.plan), document)'),
    "schema-tool": ('return ManifestCheck("unavailable", f"manifest schema unavailable: {exc}", pin)', 'raise'),
}


def unchecked_manifest(payload, path):
    """Deliberately omit codec checks, retaining only exception normalization.

    This test mutant still uses the single mapper; it cannot earn a RED merely
    by crashing on malformed bytes or mishandling harmless surrounding comments.
    """
    try:
        forms = [form for form in M.F.S.parse(payload.decode(), path) if form[0] != "comment"]
        return D.dependencies_to_doc(forms[0])
    except (M.F.S.SexpError, D.DossierError, UnicodeError, IndexError, TypeError,
            AttributeError, ValueError) as exc:
        raise M.F.ArtifactError(f"unchecked mutant document: {exc}") from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        global M
        source = Path(M.__file__).read_text(); before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1: raise SystemExit("mutation seam is not singular")
        module = types.ModuleType("mutated_gpr_manifest"); module.__file__ = M.__file__
        sys.modules[module.__name__] = module
        module.__dict__["_unchecked_manifest"] = unchecked_manifest
        exec(compile(source.replace(before, after), M.__file__, "exec"), module.__dict__)
        M = module
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ManifestTests)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"MATCHED-GPR-MANIFEST: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; fixtures cleaned")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
