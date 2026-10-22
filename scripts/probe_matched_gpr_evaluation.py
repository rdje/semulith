#!/usr/bin/env python3
"""Actual on-volume synthetic evaluation controls; never qualification evidence."""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock

import matched_gpr_evaluation as E
import matched_gpr_image as G
import matched_gpr_artifacts as F
import probe_matched_gpr_execution as P
import probe_matched_gpr_identity as PI
import probe_matched_gpr_receipt as PR
import probe_matched_gpr_comparison as PC

ROOT = Path(__file__).resolve().parent.parent


class Fixture:
    def __init__(self, root):
        self.root = root
        self.experiment, self.candidate = P.fixture()
        self.graph = self.experiment["verification"]
        self.inputs = {item["id"]: item for item in self.graph["input"]}
        self.outputs = {item["id"]: item for item in self.graph["observation"]}
        self.runs = {item["kind"]: item for item in self.graph["run"]}
        for item in self.graph["input"]:
            self.write(item, b"opaque synthetic principal; no source/image adequacy")
        self.entry = 0x80000000
        self.source = b"addi x1, x0, 1\n"
        self.image = G.build_guest_image(self.source, program=self.experiment["program"], entry=self.entry).image
        self.write(self.inputs["guest-source"], self.source)
        self.write(self.inputs["guest-image"], self.image)
        self.write(self.inputs["reference-identity"], PI.encode(PI.document(self.candidate)))
        self.base = PC.P.expected([{"x1": "0x1"}]); self.base["program"] = self.experiment["program"]
        self.base["entry"] = hex(self.entry)
        self.base["step"][0]["insn"] = "addi x1, x0, 1"
        self.control = deepcopy(self.base); self.control["step"][0]["writes"]["x1"] = "0x2"
        self.write(self.inputs["expectation"], PC.encode(self.base))
        self.write(self.inputs["mutant-expectation"], PC.encode(self.control))
        self.trace = (b"[0] [M]: 0x0000000080000000 (0x00100093) addi x1, x0, 1\n"
                      b"x1 <- 0x0000000000000001\n")
        for output in self.graph["observation"]:
            self.write(output, self.trace if output["role"] == "raw-gpr" else b"")
        self.child = dict(id="dependency", role="implementation", path="source/tool.py", sha256="a" * 64)
        self.write(self.child, b"# opaque synthetic implementation dependency\n")
        self.write(self.inputs["dependency-manifest"], F.encode_dependencies(
            dict(format_version="matched-gpr-dependencies-v1", input=[self.child]),
            path=self.inputs["dependency-manifest"]["path"]))
        self.publish_receipts()

    def write(self, record, payload):
        path = self.root / record["path"]; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload); record["sha256"] = hashlib.sha256(payload).hexdigest()
        if "byte_size" in record: record["byte_size"] = len(payload)

    def capture(self, kind):
        run = self.runs[kind]; outputs = [self.outputs[rid] for rid in run["observation_ids"]]
        doc = PR.P.capture()
        doc.update(run_id=run["id"], run_kind=kind, argv=list(run["argv"]), process_exit=run["process_exit"],
                   reference_binary_sha256=self.candidate["binary_sha256"],
                   input=[dict(id=rid, sha256=self.inputs[rid]["sha256"]) for rid in run["input_ids"]],
                   observation=[dict(item) for item in outputs if item["role"] != "process-receipt"])
        return doc

    def receipt(self, kind):
        return next(self.outputs[rid] for rid in self.runs[kind]["observation_ids"]
                    if self.outputs[rid]["role"] == "process-receipt")

    def publish_receipts(self):
        for kind in self.runs:
            record = self.receipt(kind)
            self.write(record, F.encode_capture(self.capture(kind), path=record["path"]))

    def observation(self, kind, role):
        return next(self.outputs[rid] for rid in self.runs[kind]["observation_ids"]
                    if self.outputs[rid]["role"] == role)

    def arguments(self):
        return dict(raw_experiment=P.raw_experiment(self.experiment, self.candidate),
                    current_candidate=self.candidate, scope=E.V.Scope("synthetic",
                        frozenset({"sail-riscv"}), frozenset({"REQ-synthetic"}), frozenset({"OBL-synthetic"})))


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/p4-system-14/a41/evaluation-fixtures"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base); self.addCleanup(temporary.cleanup)
        self.f = Fixture(Path(temporary.name))

    def outcome(self, disposition, reason=None, **overrides):
        args = self.f.arguments(); args.update(overrides)
        try:
            checked = E.evaluate_retained_unit(self.f.root, **args)
        except (AttributeError, IndexError, KeyError, TypeError, ValueError, OSError, AssertionError) as exc:
            self.fail(f"evaluation boundary escaped as {type(exc).__name__}: {exc}")
        self.assertEqual(checked.disposition, disposition, checked)
        if reason: self.assertIn(reason, checked.reason)
        if checked.authentication is not None:
            self.assertTrue(all(fact.data is None for fact in checked.authentication.files))
        return checked

    def no_artifact(self):
        stack = ExitStack()
        for name in ("read_snapshot", "read_bounded_pin", "read_pinned"):
            stack.enter_context(mock.patch.object(E.A, name, side_effect=AssertionError("artifact I/O")))
        return stack

    def test_positive_is_pending_with_three_observed_outcomes(self):
        checked = self.outcome("pending", "complete method/policy adequacy pending")
        self.assertEqual(checked.record.disposition, "valid")
        self.assertEqual(checked.authentication.disposition, "matched")
        self.assertEqual(checked.identity.disposition, "matched"); self.assertIsNone(checked.identity.pin)
        self.assertEqual(len(checked.receipts), 3)
        self.assertTrue(all(item.check.disposition == "matched" and item.check.pin is None for item in checked.receipts))
        self.assertEqual(checked.comparison.disposition, "satisfied")
        self.assertEqual(tuple(item.comparison.verdict for item in checked.comparison.runs), ("AGREE", "AGREE", "DIVERGE"))
        self.assertFalse(hasattr(checked, "qualified"))

    def test_invalid_scope_refuses_before_artifacts(self):
        with self.no_artifact():
            self.assertEqual(self.outcome("refused", "scoped", scope={}).record.disposition, "unchecked")

    def test_invalid_raw_root_refuses_before_artifacts(self):
        with self.no_artifact():
            self.assertEqual(self.outcome("refused", raw_experiment=[]).record.disposition, "refused")

    def test_duplicate_raw_field_refuses_before_mapper(self):
        args = self.f.arguments(); args["raw_experiment"].append([E.S.Symbol("instructions"), 1])
        with self.no_artifact(), mock.patch.object(E.D, "references_to_doc", side_effect=AssertionError("mapper")):
            checked = self.outcome("refused", **args)
        self.assertEqual(checked.record.disposition, "refused")

    def test_scoped_missing_requirement_refuses_before_artifacts(self):
        args = self.f.arguments(); args["scope"] = replace(args["scope"], requirement_ids=frozenset())
        with self.no_artifact(): self.assertEqual(self.outcome("refused", **args).record.disposition, "refused")

    def test_schema_tool_io_leaves_record_unchecked(self):
        with self.no_artifact(), mock.patch.object(E.V, "_schema", side_effect=OSError("synthetic schema I/O")):
            self.assertEqual(self.outcome("unavailable", "schema").record.disposition, "unchecked")

    def test_invalid_current_candidate_is_separate_from_valid_record(self):
        args = self.f.arguments(); args["current_candidate"] = dict(self.f.candidate, binary_sha256="bad")
        with self.no_artifact(): self.assertEqual(self.outcome("refused", **args).record.disposition, "valid")

    def test_unsupported_rule_is_separate_from_valid_record(self):
        self.f.graph["comparison_rule"] = "another-rule"
        with self.no_artifact(): self.assertEqual(self.outcome("unsupported").record.disposition, "valid")

    def test_method_input_count_refuses_before_artifacts(self):
        self.f.graph["input"].append(dict(id="extra", role="extra", path="extra", sha256="a" * 64))
        with self.no_artifact(): self.assertEqual(self.outcome("refused", "relations").record.disposition, "valid")

    def test_complete_set_read_once_and_manifest_seed_not_reopened(self):
        with mock.patch.object(E.A, "read_snapshot", wraps=E.A.read_snapshot) as snapshots, \
                mock.patch.object(E.A, "read_bounded_pin", wraps=E.A.read_bounded_pin) as pins:
            checked = self.outcome("pending")
        calls = [*snapshots.call_args_list, *pins.call_args_list]
        paths = [call.args[2]["path"] for call in calls]
        self.assertEqual(len(paths), 22); self.assertEqual(len(set(paths)), 22)
        self.assertEqual(paths.count(self.f.inputs["dependency-manifest"]["path"]), 1)
        total = sum(path.stat().st_size for path in self.f.root.rglob("*") if path.is_file())
        self.assertEqual((checked.authentication.authenticated_bytes, checked.authentication.charged_read_bytes), (total, total))
        self.assertGreater(checked.authentication.snapshot_bytes, 0)
        self.assertTrue(all(0 <= call.kwargs["max_bytes"] <= 8 * 1024 * 1024 for call in calls))

    def test_no_legacy_identity_receipt_pins_binary_or_process(self):
        with mock.patch.object(E.I, "read_reference_identity", side_effect=AssertionError("legacy identity")), \
                mock.patch.object(E.R, "read_run_receipt", side_effect=AssertionError("legacy receipt")), \
                mock.patch.object(E.A, "read_pinned", side_effect=AssertionError("legacy pin")), \
                mock.patch.object(subprocess, "run", side_effect=AssertionError("process")):
            self.assertFalse((self.f.root / self.f.candidate["binary"]).exists())
            self.outcome("pending")

    def test_missing_manifest_is_unavailable_before_set_reads(self):
        (self.f.root / self.f.inputs["dependency-manifest"]["path"]).unlink()
        with mock.patch.object(E.Q, "read_declared_files", side_effect=AssertionError("file set")):
            checked = self.outcome("unavailable", "manifest")
        self.assertEqual(checked.record.disposition, "valid"); self.assertIsNone(checked.authentication)

    def test_changed_manifest_is_stale_before_set_reads(self):
        (self.f.root / self.f.inputs["dependency-manifest"]["path"]).write_bytes(b"changed")
        with mock.patch.object(E.Q, "read_declared_files", side_effect=AssertionError("file set")):
            self.outcome("stale", "manifest")

    def test_pinned_invalid_manifest_refuses_with_matched_pin(self):
        self.f.write(self.f.inputs["dependency-manifest"], b"(dependencies (unknown 1))")
        self.f.publish_receipts()
        checked = self.outcome("refused", "manifest")
        self.assertEqual(checked.manifest.pin.disposition, "matched"); self.assertIsNone(checked.authentication)

    def test_nested_child_refuses_before_identity(self):
        self.f.write(self.f.child, F.encode_dependencies(dict(format_version="matched-gpr-dependencies-v1",
            input=[dict(id="hidden", role="implementation", path="hidden", sha256="a" * 64)]), path=self.f.child["path"]))
        self.f.write(self.f.inputs["dependency-manifest"], F.encode_dependencies(
            dict(format_version="matched-gpr-dependencies-v1", input=[self.f.child]), path=self.f.inputs["dependency-manifest"]["path"]))
        self.f.publish_receipts()
        with mock.patch.object(E.I, "check_reference_identity_bytes", side_effect=AssertionError("identity")):
            checked = self.outcome("refused", "files")
        self.assertEqual(checked.authentication.snapshot_bytes, 0)

    def test_missing_dependency_is_unavailable_before_consumers(self):
        (self.f.root / self.f.child["path"]).unlink()
        with mock.patch.object(E.I, "check_reference_identity_bytes", side_effect=AssertionError("identity")):
            checked = self.outcome("unavailable", "files")
        self.assertEqual(checked.record.disposition, "valid"); self.assertEqual(checked.receipts, ())

    def test_changed_dependency_is_stale_before_consumers(self):
        (self.f.root / self.f.child["path"]).write_bytes(b"changed")
        with mock.patch.object(E.C, "compare_unit", side_effect=AssertionError("comparison")):
            self.outcome("stale", "files")

    def test_current_identity_change_is_stale_after_file_authentication(self):
        self.f.candidate["version"] = "new"
        with mock.patch.object(E.R, "check_receipt_bytes", side_effect=AssertionError("receipt")):
            checked = self.outcome("stale", "identity")
        self.assertEqual(checked.authentication.disposition, "matched"); self.assertIsNone(checked.identity.pin)

    def test_pinned_malformed_identity_refuses_after_authentication(self):
        self.f.write(self.f.inputs["reference-identity"], b"(references (unknown 1))"); self.f.publish_receipts()
        with mock.patch.object(E.C, "compare_unit", side_effect=AssertionError("comparison")):
            checked = self.outcome("refused", "identity")
        self.assertEqual(checked.authentication.disposition, "matched")

    def test_identity_payload_cap_remains_enforced(self):
        self.f.write(self.f.inputs["reference-identity"], b" " * 65537); self.f.publish_receipts()
        with mock.patch.object(E.I, "check_reference_identity_bytes", side_effect=AssertionError("identity")):
            self.outcome("refused", "files")

    def test_identity_schema_io_preserves_existing_refusal(self):
        with mock.patch.object(E.I, "_schema", side_effect=OSError("identity schema unavailable")):
            checked = self.outcome("refused", "identity")
        self.assertEqual(checked.authentication.disposition, "matched"); self.assertEqual(checked.record.disposition, "valid")

    def test_changed_receipt_pin_is_stale_before_byte_checks(self):
        (self.f.root / self.f.receipt("repeat")["path"]).write_bytes(b"changed")
        with mock.patch.object(E.I, "check_reference_identity_bytes", side_effect=AssertionError("identity")):
            self.outcome("stale", "files")

    def test_receipt_contradiction_stops_before_comparison(self):
        doc = self.f.capture("repeat"); doc["argv"][0] = "wrong/binary"
        self.f.write(self.f.receipt("repeat"), F.encode_capture(doc, path=self.f.receipt("repeat")["path"]))
        with mock.patch.object(E.C, "compare_unit", side_effect=AssertionError("comparison")):
            checked = self.outcome("refused", "receipt")
        self.assertEqual(len(checked.receipts), 2); self.assertEqual(checked.authentication.disposition, "matched")

    def test_receipt_schema_io_is_unavailable_after_authenticated_identity(self):
        schema = F._schema
        def unavailable(family):
            if family == "capture": raise OSError("capture schema unavailable")
            return schema(family)
        with mock.patch.object(F, "_schema", side_effect=unavailable): checked = self.outcome("unavailable", "receipt")
        self.assertEqual(checked.identity.disposition, "matched"); self.assertEqual(len(checked.receipts), 1)

    def test_coherent_failed_baseline_is_valid_failed_evidence(self):
        self.f.runs["baseline"].update(process_exit=1, verdict="REFUSED"); self.f.publish_receipts()
        checked = self.outcome("failed")
        self.assertEqual(checked.record.disposition, "valid")
        self.assertEqual(checked.receipts[0].check.facts.process_exit, 1)
        self.assertIsNone(checked.comparison.runs[0].comparison)
        self.assertIsNotNone(checked.comparison.runs[0].refusal)

    def test_coherent_signaled_control_is_valid_failed_evidence(self):
        self.f.runs["control"].update(process_exit=-9, verdict="REFUSED")
        self.f.graph["control_run"][0]["observed_verdict"] = "REFUSED"; self.f.publish_receipts()
        checked = self.outcome("failed"); self.assertEqual(checked.record.disposition, "valid")
        self.assertEqual(checked.receipts[2].check.facts.process_exit, -9)

    def test_unchanged_control_is_failed_with_coherent_recorded_agreement(self):
        self.f.write(self.f.inputs["mutant-expectation"], PC.encode(self.f.base))
        self.f.runs["control"]["verdict"] = "AGREE"
        self.f.graph["control_run"][0]["observed_verdict"] = "AGREE"; self.f.publish_receipts()
        self.assertEqual(self.outcome("failed").comparison.runs[2].comparison.verdict, "AGREE")

    def test_malformed_trace_with_recorded_refusal_is_valid_failed_evidence(self):
        self.f.write(self.f.observation("baseline", "raw-gpr"), b"malformed trace")
        self.f.runs["baseline"]["verdict"] = "REFUSED"; self.f.publish_receipts()
        checked = self.outcome("failed"); self.assertEqual(checked.record.disposition, "valid")

    def test_repeat_raw_difference_fails_even_with_observed_agreement(self):
        self.f.write(self.f.observation("repeat", "raw-gpr"), self.f.trace + b"\n"); self.f.publish_receipts()
        checked = self.outcome("failed"); self.assertEqual(checked.comparison.runs[1].comparison.verdict, "AGREE")

    def test_control_raw_difference_fails_even_with_observed_divergence(self):
        self.f.write(self.f.observation("control", "raw-gpr"), self.f.trace + b"\n"); self.f.publish_receipts()
        checked = self.outcome("failed"); self.assertEqual(checked.comparison.runs[2].comparison.verdict, "DIVERGE")

    def test_recorded_verdict_must_match_computed_outcome(self):
        for kind in ("baseline", "repeat"):
            original = self.f.runs[kind]["verdict"]
            try:
                self.f.runs[kind]["verdict"] = "DIVERGE"
                checked = self.outcome("refused", "recorded verdict")
                self.assertEqual(checked.comparison.disposition, "satisfied")
            finally: self.f.runs[kind]["verdict"] = original

    def test_cross_model_exclusion_is_unsupported_with_a_valid_record(self):
        base = deepcopy(self.f.base); base["cross_model"] = False
        self.f.write(self.f.inputs["expectation"], PC.encode(base)); self.f.publish_receipts()
        checked = self.outcome("unsupported"); self.assertEqual(checked.record.disposition, "valid")
        self.assertEqual(checked.comparison.runs, ())

    def test_malformed_expectation_refuses_after_binding(self):
        self.f.write(self.f.inputs["expectation"], b"(expectations (unknown 1))"); self.f.publish_receipts()
        checked = self.outcome("refused", "comparison")
        self.assertEqual(len(checked.receipts), 3); self.assertIsNone(checked.comparison)

    def test_returned_facts_are_frozen_and_payload_free(self):
        checked = self.outcome("pending")
        for value, field in ((checked, "reason"), (checked.record, "issues"),
                             (checked.authentication, "files"), (checked.receipts[0], "declared_verdict")):
            with self.subTest(field=field), self.assertRaises(FrozenInstanceError): setattr(value, field, ())
        self.assertIs(type(checked.receipts), tuple); self.assertIs(type(checked.authentication.files), tuple)
        self.assertTrue(all(fact.data is None for fact in checked.authentication.files))

    def test_caller_context_mutation_during_first_read_does_not_change_bindings(self):
        args = self.f.arguments(); original = deepcopy(args); reader = E.A.read_snapshot; changed = False
        def reading(*a, **kw):
            nonlocal changed
            snapshot = reader(*a, **kw)
            if not changed:
                changed = True; args["raw_experiment"].clear(); args["current_candidate"].clear()
            return snapshot
        try:
            with mock.patch.object(E.A, "read_snapshot", side_effect=reading): self.outcome("pending", **args)
        finally:
            args["raw_experiment"][:] = original["raw_experiment"]
            args["current_candidate"].clear(); args["current_candidate"].update(original["current_candidate"])

    def test_all_receipt_and_identity_contexts_precede_first_artifact_read(self):
        reader = E.A.read_snapshot
        with mock.patch.object(E.I, "bind_reference_identity", wraps=E.I.bind_reference_identity) as identity, \
                mock.patch.object(E.R, "bind_receipt_context", wraps=E.R.bind_receipt_context) as receipts:
            def reading(*args, **kwargs):
                self.assertEqual((identity.call_count, receipts.call_count), (1, 3))
                return reader(*args, **kwargs)
            with mock.patch.object(E.A, "read_snapshot", side_effect=reading): self.outcome("pending")

    def test_candidate_execution_fields_freeze_before_component_callbacks(self):
        binding = E.B.bind_relations; original = deepcopy(self.f.candidate); changed = False
        def bound(*args, **kwargs):
            nonlocal changed
            result = binding(*args, **kwargs)
            if not changed:
                changed = True; self.f.candidate["binary_sha256"] = "e" * 64
            return result
        try:
            with mock.patch.object(E.B, "bind_relations", side_effect=bound): self.outcome("pending")
        finally:
            self.f.candidate.clear(); self.f.candidate.update(original)

    def test_observation_records_freeze_before_manifest_read(self):
        reading = E.M.read_dependency_manifest; captured = []
        def read(*args, **kwargs):
            result = reading(*args, **kwargs); graph = kwargs["experiment"]["verification"]
            captured.append((graph, deepcopy(graph["observation"])))
            for output in graph["observation"]: output["path"] = "changed/" + output["path"]
            return result
        try:
            with mock.patch.object(E.M, "read_dependency_manifest", side_effect=read): self.outcome("pending")
        finally:
            for graph, original in captured: graph["observation"][:] = original

    def test_declared_verdicts_freeze_before_manifest_read(self):
        reading = E.M.read_dependency_manifest; captured = []
        def read(*args, **kwargs):
            result = reading(*args, **kwargs); graph = kwargs["experiment"]["verification"]
            captured.append((graph, deepcopy(graph["run"])))
            for run in graph["run"]: run["verdict"] = "AGREE" if run["kind"] == "control" else "DIVERGE"
            return result
        try:
            with mock.patch.object(E.M, "read_dependency_manifest", side_effect=read):
                checked = self.outcome("pending")
            self.assertEqual(tuple(item.declared_verdict for item in checked.receipts), ("AGREE", "AGREE", "DIVERGE"))
        finally:
            for graph, original in captured: graph["run"][:] = original

    def test_later_path_changes_do_not_replace_authenticated_payloads(self):
        reading = E.Q.read_declared_files
        def authenticated(*a, **kw):
            bundle = reading(*a, **kw)
            for fact in bundle.files:
                if fact.data is not None: (self.f.root / fact.path).write_bytes(b"changed later")
            return bundle
        with mock.patch.object(E.Q, "read_declared_files", side_effect=authenticated): self.outcome("pending")
        self.outcome("stale")

    def test_incomplete_or_unknown_comparison_results_refuse(self):
        comparing = E.C.compare_unit
        for mode in ("missing", "reordered", "unknown"):
            def incomplete(**kwargs):
                result = comparing(**kwargs)
                if mode == "missing": return replace(result, runs=result.runs[:2])
                if mode == "reordered": return replace(result, runs=tuple(reversed(result.runs)))
                return replace(result, disposition="unrecognized")
            with self.subTest(mode=mode), mock.patch.object(E.C, "compare_unit", side_effect=incomplete):
                self.outcome("refused", "complete ordered run set")

    def test_manifest_must_reuse_frozen_relation_identity(self):
        reading = E.M.read_dependency_manifest
        def changed(*args, **kwargs):
            result = reading(*args, **kwargs)
            plan = replace(result.plan, relations=replace(result.plan.relations, control_property_id="different"))
            return replace(result, plan=plan)
        with mock.patch.object(E.M, "read_dependency_manifest", side_effect=changed), \
                mock.patch.object(E.Q, "read_declared_files", side_effect=AssertionError("file set")):
            self.outcome("refused", "frozen relations")


MUTATIONS = {
    "scope": ('if type(scope) is not V.Scope:', 'if False:'),
    "raw-check": ('issues = tuple(V.check_experiment(raw_experiment, scope))', 'issues = ()'),
    "raw-findings": ('if issues:', 'if False:'),
    "schema-tool": ('except OSError as exc:\n        return EvaluationCheck("unavailable", f"record schema unavailable: {exc}", RecordCheck("unchecked"))',
                    'except OSError:\n        raise'),
    "candidate-freeze": ('candidate = dict(identity_context.fields)', 'candidate = current_candidate'),
    "relations-status": ('if relations.disposition != "matched":', 'if False:'),
    "observation-freeze": ('observations = tuple(dict(item) for item in graph["observation"])',
                           'observations = graph["observation"]'),
    "receipt-context": ('run=run, inputs=', 'run=dict(run, process_exit=0), inputs='),
    "manifest-status": ('if manifest.disposition != "matched":', 'if False:'),
    "manifest-relations": ('if manifest.plan.relations != relations.plan:', 'if False:'),
    "manifest-reopen": ('files = Q.read_declared_files(root, manifest=manifest, observations=observations,\n                                  max_read_bytes=max_read_bytes, retain_source_image=True)',
                        'manifest = M.read_dependency_manifest(root, experiment=experiment, current_candidate=candidate, max_read_bytes=min(max_read_bytes, Artifacts.DOCUMENT_BYTES))\n    files = Q.read_declared_files(root, manifest=manifest, observations=observations,\n                                  max_read_bytes=max_read_bytes, retain_source_image=True)'),
    "file-status": ('if files.disposition != "matched":', 'if False:'),
    "payload-release": ('tuple(replace(fact, data=None) for fact in files.files)', 'files.files'),
    "snapshot-account": ('files.retained_bytes)', '0)'),
    "identity-status": ('if identity.disposition != "matched":', 'if False:'),
    "identity-reopen": ('identity = I.check_reference_identity_bytes(_payload(files, "input", identity_input.input_id),\n                                               path=identity_input.path, context=identity_context)',
                        'identity = I.read_reference_identity(root, dict(id=identity_input.input_id, role="reference-identity", path=identity_input.path, sha256=identity_input.sha256), candidate)'),
    "receipt-status": ('if checked.disposition != "matched":', 'if False:'),
    "receipt-reopen": ('checked = R.check_receipt_bytes(_payload(files, "observation", receipt_id), context=context.receipt)',
                       'checked = R.read_run_receipt(root, run=runs[context.run_id], inputs=[inputs[rid] for rid in runs[context.run_id]["input_ids"]], observations=[outputs[rid] for rid in runs[context.run_id]["observation_ids"]], current_candidate=candidate)'),
    "process-facts": ('receipt.check.facts.process_exit)', '0)'),
    "control-selection": ('control_expectation=_payload(files, "input", execution.control_expectation.input_id),',
                          'control_expectation=_payload(files, "input", execution.baseline_expectation.input_id),'),
    "comparison-refusal": ('except C.UnitError as exc:\n        return finish("refused", "comparison: " + str(exc), identity=identity, receipts=tuple(receipts))',
                           'except C.UnitError:\n        raise'),
    "comparison-completeness": ('if (comparison.disposition not in ("satisfied", "failed", "unsupported") or\n            (comparison.disposition != "unsupported" and\n             tuple(run.run_kind for run in comparison.runs) != tuple(run.kind for run in contexts))):', 'if False:'),
    "verdict-binding": ('if declaration.verdict != verdict:', 'if False:'),
    "comparison-status": ('if comparison.disposition != "satisfied":', 'if False:'),
    "qualification": ('return finish("pending", "authenticated byte comparison binds;',
                      'return finish("satisfied", "authenticated byte comparison binds;'),
    "result-frozen": ('@dataclass(frozen=True)\nclass EvaluationCheck:', '@dataclass\nclass EvaluationCheck:'),
    "record-frozen": ('@dataclass(frozen=True)\nclass RecordCheck:', '@dataclass\nclass RecordCheck:'),
    "authentication-frozen": ('@dataclass(frozen=True)\nclass AuthenticationSummary:', '@dataclass\nclass AuthenticationSummary:'),
    "receipt-frozen": ('@dataclass(frozen=True)\nclass ReceiptBinding:', '@dataclass\nclass ReceiptBinding:'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS); args = parser.parse_args()
    if args.mutation:
        global E
        before, after = MUTATIONS[args.mutation]; source = Path(E.__file__).read_text()
        if source.count(before) != 1: raise SystemExit("mutation seam is not singular")
        module = types.ModuleType("mutated_gpr_evaluation"); module.__file__ = E.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), E.__file__, "exec"), module.__dict__); E = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(EvaluationTests))
    print(f"MATCHED-GPR-EVALUATION: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; synthetic only")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
