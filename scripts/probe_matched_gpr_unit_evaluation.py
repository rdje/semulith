#!/usr/bin/env python3
"""Fresh synthetic processes and actual reads; no Sail/canonical/qualification credit."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import matched_gpr_identity as Identity
import matched_gpr_unit_collector as U
import probe_matched_gpr_property_evaluation as PropertyFixture
import records_sexp as R

ROOT = Path(__file__).resolve().parent.parent
CHILD = '''import json,pathlib,sys
config=json.loads(pathlib.Path(sys.argv[2]).read_text())
pathlib.Path(sys.argv[9]).write_bytes(bytes.fromhex(config["trace"]))
sys.exit(7 if config.get("fail") else 0)
'''


class Fixture(PropertyFixture.Fixture):
    def __init__(self, root):
        super().__init__(root)
        binary = root / "reference"
        binary.write_text("#!" + sys.executable + " -B\n" + CHILD)
        binary.chmod(0o755)
        self.candidate.update(binary="reference", binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest())
        for producer in self.graph["producer"]:
            if producer["role"] == "reference":
                producer["version"] = "sha256:" + self.candidate["binary_sha256"]
        for run in self.runs.values():
            run["argv"][0] = "reference"
        self.configuration()
        self.write(self.inputs["reference-identity"], Identity.encode_reference_identity(
            Identity.bind_reference_identity(self.candidate), profile=self.scope.profile_id,
            retrieved="synthetic", work_dir="inputs",
            host=dict(os="fixture", kernel="fixture", arch="fixture", cxx="fixture"),
            path=self.inputs["reference-identity"]["path"]))
        self.refresh_manifest_and_review()
        self.clear()

    def configuration(self, **changes):
        self.write(self.inputs["reference-config"], json.dumps(dict(trace=self.trace.hex(), **changes)).encode())

    def clear(self):
        for record in self.graph["observation"]:
            path = self.root / record["path"]
            if path.exists():
                path.unlink()

    def combined_arguments(self):
        args = super().arguments()
        args["planned_experiment"] = R.render_forms([args.pop("raw_experiment")]).encode()
        return args


class CombinedTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/p4-system-14/a42ad/controls"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.f = Fixture(Path(temporary.name))

    @contextmanager
    def reads(self):
        original, observed = os.read, []
        def read(fd, count):
            data = original(fd, count)
            observed.append(len(data))
            return data
        with patch.object(U.C.A.os, "read", side_effect=read):
            yield observed

    def run_unit(self, expected="pending", arguments=None, **changes):
        args = self.f.combined_arguments() if arguments is None else dict(arguments)
        args.update(changes)
        try:
            result = U.capture_and_evaluate(self.f.root, **args)
        except Exception as exc:
            self.fail("combined boundary escaped as " + type(exc).__name__ + ": " + str(exc))
        self.assertEqual(result.disposition, expected, result.reason)
        self.assertIs(type(result.charged_read_bytes), int)
        limit = args.get("max_read_bytes", U.C.TOTAL_BYTES)
        if type(limit) is int and 0 <= limit <= U.C.TOTAL_BYTES:
            self.assertLessEqual(result.charged_read_bytes, limit)
        self.assertGreaterEqual(result.charged_read_bytes, 0)
        self.assertFalse(hasattr(result, "qualified"))
        return result

    def test_fresh_three_processes_bind_actual_metadata_and_read_totals(self):
        with self.reads() as actual:
            result = self.run_unit()
        self.assertEqual(sum(actual), result.charged_read_bytes)
        self.assertEqual(result.charged_read_bytes,
                         result.collection.charged_read_bytes + result.evaluation.authentication.charged_read_bytes)
        self.assertEqual(len({r.process.pid for r in result.collection.runs}), 3)
        self.assertEqual(result.evaluation.source_property.disposition, "matched")
        self.assertLessEqual(result.evaluation.authentication.snapshot_bytes, U.Evaluation.Q.MAX_SNAPSHOT_BYTES)
        self.assertTrue(all(f.data is None for f in result.evaluation.authentication.files))
        self.assertIs(type(result.experiment), bytes)
        forms = U.S.parse(result.experiment.decode(), "measured")
        self.assertEqual(U.V.check_experiment(forms[0], self.f.scope), [])
        document = U.D.references_to_doc([U.S.Symbol("references"), forms[0]])["experiment"][0]
        for record in document["verification"]["observation"]:
            payload = (self.f.root / record["path"]).read_bytes()
            self.assertEqual((record["byte_size"], record["sha256"]),
                             (len(payload), hashlib.sha256(payload).hexdigest()))

    def test_exact_and_one_byte_short_share_both_stages(self):
        first = self.run_unit()
        needed = first.charged_read_bytes
        self.f.clear()
        with self.reads() as actual:
            exact = self.run_unit(max_read_bytes=needed)
        self.assertEqual((sum(actual), exact.charged_read_bytes), (needed, needed))
        self.f.clear()
        with self.reads() as actual:
            short = self.run_unit("refused", max_read_bytes=needed - 1)
        self.assertIsNotNone(short.collection)
        self.assertEqual(short.collection.disposition, "recorded")
        self.assertIsNotNone(short.evaluation)
        self.assertEqual(short.evaluation.disposition, "refused")
        self.assertEqual(short.charged_read_bytes, needed - 1)
        self.assertLessEqual(sum(actual), needed - 1)

    def test_collection_exhaustion_stops_before_evaluation(self):
        first = self.run_unit()
        self.f.clear()
        limit = first.collection.charged_read_bytes - 1
        with self.reads() as actual, patch.object(U.Evaluation, "evaluate_retained_unit",
                                                side_effect=AssertionError("evaluation reached")):
            result = self.run_unit("refused", max_read_bytes=limit)
        self.assertIsNone(result.evaluation)
        self.assertEqual(result.charged_read_bytes, limit)
        self.assertLessEqual(sum(actual), limit)

    def test_zero_reads_no_payload_and_never_evaluates(self):
        with self.reads() as actual, patch.object(U.Evaluation, "evaluate_retained_unit",
                                                side_effect=AssertionError("evaluation reached")):
            result = self.run_unit("refused", max_read_bytes=0)
        self.assertEqual(sum(actual), 0)
        self.assertEqual(result.charged_read_bytes, 0)
        self.assertIsNone(result.experiment)
        self.assertFalse(any(run.process and run.process.pid for run in result.collection.runs))

    def test_invalid_allowance_refuses_before_parsing_or_collection(self):
        class Integer(int):
            pass
        for value in [False, True, -1, U.C.TOTAL_BYTES + 1, 1 << 100000, None, "0", 0.0, Integer(1)]:
            with self.subTest(kind=type(value)), patch.object(U.S, "parse", side_effect=AssertionError("parse")):
                result = self.run_unit("refused", max_read_bytes=value)
                self.assertEqual(result.charged_read_bytes, 0)
                self.assertIsNone(result.collection)

    def test_bad_planned_bytes_refuse_before_parsing(self):
        for value in [None, "record", [], bytearray(b"record"), memoryview(b"record"), b"", b"x" * 65537]:
            with self.subTest(kind=type(value)), patch.object(U.S, "parse", side_effect=AssertionError("parse")):
                result = self.run_unit("refused", planned_experiment=value)
                self.assertEqual(result.charged_read_bytes, 0)
                self.assertIsNone(result.collection)

    def test_malformed_or_multiple_records_never_collect(self):
        original = self.f.combined_arguments()["planned_experiment"]
        for value in [b"\xff", b"(experiment", b'(comment "only")', b'(unknown "x")', original * 2]:
            with self.subTest(length=len(value)), patch.object(U, "capture_unit", side_effect=AssertionError("collection")):
                result = self.run_unit("refused", planned_experiment=value)
                self.assertEqual(result.charged_read_bytes, 0)

    def test_raw_schema_precedes_mapping_and_processes(self):
        raw = self.f.combined_arguments()["planned_experiment"]
        for value in [raw.replace(b"(instructions 27)", b"(instructions 27) (instructions 27)", 1),
                      raw.replace(b"(instructions 27)", b'(instructions "27")', 1)]:
            with patch.object(U.D, "references_to_doc", side_effect=AssertionError("mapped invalid raw record")), \
                    patch.object(U, "capture_unit", side_effect=AssertionError("collection")):
                result = self.run_unit("refused", planned_experiment=value)
                self.assertEqual(result.charged_read_bytes, 0)

    def test_schema_unavailability_before_collection_has_no_artifact_charge(self):
        with patch.object(U.V, "_schema", side_effect=OSError("schema missing")), \
                patch.object(U, "capture_unit", side_effect=AssertionError("collection")):
            result = self.run_unit("unavailable")
        self.assertEqual(result.charged_read_bytes, 0)
        self.assertIsNone(result.collection)

    def test_failed_process_keeps_reservation_and_stops_after_first_run(self):
        self.f.configuration(fail=True)
        self.f.refresh_manifest_and_review()
        self.f.clear()
        with patch.object(U.Evaluation, "evaluate_retained_unit", side_effect=AssertionError("evaluation")):
            result = self.run_unit("failed")
        self.assertEqual(result.charged_read_bytes, U.C.TOTAL_BYTES)
        self.assertEqual(len(result.collection.runs), 1)
        self.assertEqual(result.collection.runs[0].process.process_exit, 7)
        self.assertIsNone(result.experiment)

    def test_stale_input_stops_collection_without_evaluation(self):
        path = self.f.root / self.f.inputs["reference-config"]["path"]
        path.write_bytes(path.read_bytes() + b" ")
        with patch.object(U.Evaluation, "evaluate_retained_unit", side_effect=AssertionError("evaluation")):
            result = self.run_unit("stale")
        self.assertEqual(result.charged_read_bytes, U.C.TOTAL_BYTES)
        self.assertIsNone(result.experiment)

    def test_unsupported_rule_is_distinct_before_collection(self):
        payload = self.f.combined_arguments()["planned_experiment"].replace(
            b"sail-gpr-change-v1", b"unsupported-rule", 1)
        with patch.object(U, "capture_unit", side_effect=AssertionError("collection")):
            result = self.run_unit("unsupported", planned_experiment=payload)
        self.assertEqual(result.charged_read_bytes, 0)
        self.assertIsNone(result.collection)

    def test_invalid_collection_findings_are_not_returned_as_typed_components(self):
        for value in [object(), U.UnitCapture("invented", "bad"), U.UnitCapture("recorded", None),
                      U.UnitCapture("refused", "bad", charged_read_bytes=True)]:
            with self.subTest(kind=type(value)), patch.object(U, "capture_unit", return_value=value), \
                    patch.object(U.Evaluation, "evaluate_retained_unit", side_effect=AssertionError("evaluation")):
                result = self.run_unit("refused")
                self.assertEqual(result.charged_read_bytes, U.C.TOTAL_BYTES)
                self.assertIsNone(result.collection)
                self.assertIsNone(result.evaluation)

    def test_invalid_scopes_refuse_before_parsing(self):
        scope = self.f.scope
        for value in [None, object(), replace(scope, candidate_ids=["sail-riscv"]),
                      replace(scope, profile_id=False),
                      replace(scope, obligation_ids=frozenset({False})),
                      replace(scope, requirement_ids=frozenset(str(n) for n in range(U.SCOPE_IDS + 1)))]:
            with self.subTest(kind=type(value)), patch.object(U.S, "parse", side_effect=AssertionError("parse")):
                result = self.run_unit("refused", scope=value)
                self.assertEqual(result.charged_read_bytes, 0)
                self.assertIsNone(result.collection)

    def test_invalid_candidate_and_authorities_never_collect(self):
        for changes in [dict(current_candidate=dict(self.f.candidate, binary="/outside")),
                        dict(author_review=replace(self.f.author_review, route="unknown")),
                        dict(author_review=None),
                        dict(property_authority=replace(self.f.authority, source_sha256="wrong")),
                        dict(case_id="rv64gc-unknown"),
                        dict(reviewed_inputs=replace(self.f.author_review.inventory, experiment_id="other")),
                        dict(impact_review=object())]:
            with self.subTest(keys=tuple(changes)), patch.object(U, "capture_unit", side_effect=AssertionError("collection")):
                result = self.run_unit("refused", **changes)
                self.assertEqual(result.charged_read_bytes, 0)
                self.assertIsNone(result.collection)

    def test_the_capture_names_the_case_it_binds(self):
        """The retained case is the default; naming the m-forms case over this record collects, then refuses by name."""
        result = self.run_unit("refused", case_id=U.Property.M_FORMS_CASE_ID)
        self.assertIn("property claim", result.reason)
        self.assertEqual(result.collection.disposition, "recorded")
        self.assertEqual(result.evaluation.source_values.disposition, "matched")
        self.assertEqual(result.evaluation.source_property.disposition, "refused")

    def test_explicit_inventory_and_author_agree(self):
        result = self.run_unit(reviewed_inputs=self.f.author_review.inventory)
        self.assertEqual(result.evaluation.input_review.disposition, "matched")
        self.assertEqual(result.evaluation.expected_author.disposition, "matched")

    def test_scope_candidate_and_property_authority_freeze_before_collection(self):
        args = self.f.combined_arguments()
        capture = U.capture_unit
        def mutate(root, **kwargs):
            self.f.candidate["binary_sha256"] = "b" * 64
            self.f.graph["property"][0]["statement"] = "changed caller statement"
            object.__setattr__(self.f.scope, "profile_id", "changed caller profile")
            object.__setattr__(self.f.authority, "source_sha256", "b" * 64)
            object.__setattr__(self.f.author_review.inventory.inputs[0], "sha256", "b" * 64)
            return capture(root, **kwargs)
        with patch.object(U, "capture_unit", side_effect=mutate):
            result = self.run_unit(arguments=args)
        self.assertEqual(result.evaluation.source_property.disposition, "matched")
        self.assertEqual(result.evaluation.expected_author.disposition, "matched")

    def test_structured_comments_and_unmeasured_fields_survive(self):
        args = self.f.combined_arguments()
        forms = U.S.parse(args["planned_experiment"].decode(), "plan")
        raw = forms[0]
        raw.append([U.S.Symbol("comment"), "inside parent"])
        graph = U.S.children(raw, "verification")[0]
        graph.append([U.S.Symbol("comment"), "inside graph"])
        forms.insert(0, [U.S.Symbol("comment"), "outer annotation"])
        args["planned_experiment"] = R.render_forms(forms).encode()
        original = args["planned_experiment"]
        result = self.run_unit(arguments=args)
        actual = U.S.parse(result.experiment.decode(), "measured")
        for phrase in [b"outer annotation", b"inside parent", b"inside graph"]:
            self.assertIn(phrase, result.experiment)
        self.assertEqual(args["planned_experiment"], original)
        current_raw = next(form for form in actual if form[0] == "experiment")
        current_graph = U.S.children(current_raw, "verification")[0]
        for name in ["input", "producer", "property", "producer_pair", "control_run", "comment"]:
            self.assertEqual(U.S.children(current_graph, name), U.S.children(graph, name))
        self.assertEqual([part for part in current_raw if not isinstance(part, list) or not part or part[0] != "verification"],
                         [part for part in raw if not isinstance(part, list) or not part or part[0] != "verification"])

    def test_inclusive_planned_payload_ceiling(self):
        args = self.f.combined_arguments()
        args["planned_experiment"] += b" " * (U.EXPERIMENT_BYTES - len(args["planned_experiment"]))
        self.assertEqual(len(args["planned_experiment"]), U.EXPERIMENT_BYTES)
        result = self.run_unit(arguments=args)
        self.assertLessEqual(len(result.experiment), U.EXPERIMENT_BYTES)

    def test_measured_record_growth_is_bounded_before_evaluation(self):
        args = self.f.combined_arguments()
        forms = U.S.parse(args["planned_experiment"].decode(), "plan")
        graph = U.S.children(forms[0], "verification")[0]
        for observation in U.S.children(graph, "observation"):
            U.S.children(observation, "byte_size")[0][1] = 0
        note = [U.S.Symbol("comment"), ""]
        forms.append(note)
        base = R.render_forms(forms).encode()
        note[1] = "x" * (U.EXPERIMENT_BYTES - len(base))
        args["planned_experiment"] = R.render_forms(forms).encode()
        self.assertEqual(len(args["planned_experiment"]), U.EXPERIMENT_BYTES)
        with self.reads() as actual, patch.object(U.Evaluation, "evaluate_retained_unit",
                                                side_effect=AssertionError("evaluation reached")):
            result = self.run_unit("refused", arguments=args)
        self.assertEqual(result.collection.disposition, "recorded")
        self.assertIsNone(result.experiment)
        self.assertIsNone(result.evaluation)
        self.assertEqual(result.charged_read_bytes, result.collection.charged_read_bytes)
        self.assertEqual(sum(actual), result.charged_read_bytes)

    def test_existing_outputs_are_preserved_without_another_process(self):
        self.run_unit()
        paths = [self.f.root / item["path"] for item in self.f.graph["observation"]]
        before = [path.read_bytes() for path in paths]
        with self.reads() as actual, patch.object(U.C, "capture_run_with_receipt",
                                                side_effect=AssertionError("another process")):
            result = self.run_unit("refused")
        self.assertEqual(sum(actual), 0)
        self.assertEqual(result.charged_read_bytes, U.C.TOTAL_BYTES)
        self.assertEqual([path.read_bytes() for path in paths], before)
        self.assertIsNone(result.evaluation)

    def test_invalid_complete_collection_metadata_never_evaluates(self):
        complete = self.run_unit().collection
        published = complete.runs[0]
        process = published.process
        output = process.outputs[0]
        zero_runs = tuple(replace(item, charged_read_bytes=0,
                          process=replace(item.process, charged_read_bytes=0))
                          for item in complete.runs)
        variants = [replace(complete, charged_read_bytes=0),
                    replace(complete, charged_read_bytes=complete.charged_read_bytes + 1),
                    replace(complete, charged_read_bytes=0, runs=zero_runs),
                    replace(complete, runs=(complete.runs[0], replace(complete.runs[1],
                        process=replace(complete.runs[1].process, pid=process.pid)), complete.runs[2])),
                    replace(complete, runs=complete.runs[:2]),
                    replace(complete, runs=(published, published, complete.runs[2])),
                    replace(complete, runs=(replace(published, process=replace(process, process_exit=7)), *complete.runs[1:])),
                    replace(complete, runs=(replace(published, receipt=None), *complete.runs[1:])),
                    replace(complete, runs=(replace(published, charged_read_bytes=True), *complete.runs[1:])),
                    replace(complete, runs=(replace(published, process=replace(process, outputs=(replace(output, path="other/path"), *process.outputs[1:]))), *complete.runs[1:])),
                    replace(complete, runs=(replace(published, process=replace(process, outputs=(replace(output, byte_size=True), *process.outputs[1:]))), *complete.runs[1:]))]
        for value in variants:
            with self.subTest(kind=type(value)), patch.object(U, "capture_unit", return_value=value), \
                    patch.object(U.Evaluation, "evaluate_retained_unit", side_effect=AssertionError("evaluation")):
                result = self.run_unit("refused")
                self.assertEqual(result.charged_read_bytes, U.C.TOTAL_BYTES)
                self.assertIsNone(result.collection)
                self.assertIsNone(result.evaluation)

    def test_invalid_evaluation_headers_never_escape_in_typed_result(self):
        complete = self.run_unit().collection
        record = U.Evaluation.RecordCheck("valid")
        values = [None, object(), U.Evaluation.EvaluationCheck("invented", "bad", record),
                  U.Evaluation.EvaluationCheck("pending", None, record),
                  U.Evaluation.EvaluationCheck("pending", "bad", None)]
        for value in values:
            with self.subTest(kind=type(value)), patch.object(U, "capture_unit", return_value=complete), \
                    patch.object(U.Evaluation, "evaluate_retained_unit", return_value=value):
                result = self.run_unit("refused")
                self.assertEqual(result.charged_read_bytes, U.C.TOTAL_BYTES)
                self.assertIsNone(result.evaluation)

    def test_pending_counters_must_include_seed_and_fit_remainder(self):
        good = self.run_unit()
        result, auth, manifest = good.evaluation, good.evaluation.authentication, good.evaluation.manifest
        remaining = U.C.TOTAL_BYTES - good.collection.charged_read_bytes
        variants = [replace(result, authentication=None),
                    replace(result, manifest=None),
                    replace(result, authentication=replace(auth, charged_read_bytes=False)),
                    replace(result, authentication=replace(auth, authenticated_bytes=True)),
                    replace(result, authentication=replace(auth, charged_read_bytes=0, authenticated_bytes=0)),
                    replace(result, authentication=replace(auth, charged_read_bytes=remaining + 1)),
                    replace(result, authentication=replace(auth, snapshot_bytes=U.Evaluation.Q.MAX_SNAPSHOT_BYTES + 1)),
                    replace(result, authentication=replace(auth, manifest_pin=None)),
                    replace(result, manifest=replace(manifest, pin=replace(manifest.pin, path="other/manifest")))]
        for value in variants:
            with self.subTest(kind=type(value)), patch.object(U, "capture_unit", return_value=good.collection), \
                    patch.object(U.Evaluation, "evaluate_retained_unit", return_value=value):
                checked = self.run_unit("refused")
                self.assertEqual(checked.charged_read_bytes, U.C.TOTAL_BYTES)
                self.assertIsNone(checked.evaluation)

    def test_real_preledger_zero_charge_keeps_entire_evaluation_reservation(self):
        evaluate = U.Evaluation.evaluate_retained_unit
        def preflight(root, **kwargs):
            graph = U.S.children(kwargs["raw_experiment"], "verification")[0]
            output = U.S.children(graph, "observation")[0]
            U.S.children(output, "byte_size")[0][1] = U.Evaluation.C.TRACE_BYTES + 1
            return evaluate(root, **kwargs)
        with self.reads() as actual, patch.object(U.Evaluation, "evaluate_retained_unit", side_effect=preflight):
            result = self.run_unit("refused")
        self.assertEqual(result.evaluation.manifest.disposition, "matched")
        self.assertEqual(result.evaluation.authentication.charged_read_bytes, 0)
        self.assertGreater(sum(actual), result.collection.charged_read_bytes)
        self.assertEqual(result.charged_read_bytes, U.C.TOTAL_BYTES)

    def test_evaluation_failure_stops_without_retry_or_budget_reset(self):
        evaluate = U.Evaluation.evaluate_retained_unit
        calls = []
        def stale(root, **kwargs):
            calls.append(kwargs["max_read_bytes"])
            path = root / self.f.normative["path"]
            data = path.read_bytes()
            path.write_bytes(bytes([data[0] ^ 1]) + data[1:])
            return evaluate(root, **kwargs)
        with patch.object(U.Evaluation, "evaluate_retained_unit", side_effect=stale):
            result = self.run_unit("stale")
        self.assertEqual(calls, [U.C.TOTAL_BYTES - result.collection.charged_read_bytes])
        self.assertEqual(result.charged_read_bytes, U.C.TOTAL_BYTES)

    def test_os_failures_retain_the_active_stage_reservation(self):
        with patch.object(U, "capture_unit", side_effect=OSError("collector unavailable")):
            result = self.run_unit("unavailable")
        self.assertEqual(result.charged_read_bytes, U.C.TOTAL_BYTES)
        self.assertIsNone(result.collection)
        with patch.object(U.Evaluation, "evaluate_retained_unit", side_effect=OSError("evaluation unavailable")):
            result = self.run_unit("unavailable")
        self.assertEqual(result.charged_read_bytes, U.C.TOTAL_BYTES)
        self.assertIsNone(result.evaluation)

    def test_impact_graphs_and_change_context_freeze_before_collection(self):
        projection = U.Impact.project_inputs(self.f.author_review.inventory)
        profile = self.f.scope.profile_id
        node = U.Impact.I.DependencyNode(projection.evidence_key, "evidence", (profile,), "a" * 64)
        graph = U.Impact.I.DependencyGraph((profile,), (node, *projection.nodes),
                    tuple((node.key, item.key) for item in projection.nodes))
        review = U.Impact.ImpactReview(profile, self.f.experiment["id"], graph, graph)
        capture = U.capture_unit
        def mutate(root, **kwargs):
            object.__setattr__(node, "fingerprint", "b" * 64)
            object.__setattr__(review, "changed_paths", ("unknown/change",))
            object.__setattr__(review, "uncertain", True)
            return capture(root, **kwargs)
        with patch.object(U, "capture_unit", side_effect=mutate):
            result = self.run_unit(impact_review=review)
        self.assertEqual(result.evaluation.impact.disposition, "matched")

    def test_unexpected_programming_failure_propagates(self):
        with patch.object(U, "capture_unit", side_effect=RuntimeError("programming failure")), \
                self.assertRaisesRegex(RuntimeError, "programming failure"):
            U.capture_and_evaluate(self.f.root, **self.f.combined_arguments())


MUTATIONS = {
    "planned-bound": ('0 < len(payload) <= EXPERIMENT_BYTES,\n            "planned experiment',
                      'True,\n            "planned experiment'),
    "scope-envelope": ('type(values) is frozenset and len(values) <= SCOPE_IDS', 'True'),
    "scope-freeze": ('return V.Scope(scope.profile_id, *groups)', 'return scope'),
    "raw-schema": ('C._need(not issues, "planned record shape/identities/edges refuse")',
                   'C._need(True, "planned record shape/identities/edges refuse")'),
    "candidate-freeze": ('candidate = dict(Identity.bind_reference_identity(candidate).fields)',
                         'Identity.bind_reference_identity(candidate)'),
    "author-freeze": ('author = None if author is None else Author.freeze_review(author, **selected)',
                      'author = author'),
    "property-freeze": ('authority = context.authority', 'authority = authority'),
    "case-forward": ('author_review=plan.author, case_id=plan.case_id,', 'author_review=plan.author,'),
    "impact-freeze": ('impact = Impact.ImpactReview(frozen.profile_id, frozen.experiment_id,\n                                    frozen.previous, frozen.current, paths, uncertain)',
                      'impact = impact'),
    "collection-limit": ('captured = capture_unit(root, request=plan.request, max_read_bytes=reserved)',
                         'captured = capture_unit(root, request=plan.request, max_read_bytes=C.TOTAL_BYTES)'),
    "collection-debit": ('remaining = reserved - captured.charged_read_bytes', 'remaining = reserved'),
    "captured-pid": ('process.pid not in pids', 'True'),
    "captured-output": ('== (target.role, target.observation_id, target.path),',
                        '== (target.role, target.observation_id, target.path) or True,'),
    "captured-charge": ('C._need(charges == result.charged_read_bytes\n            and sum(item.byte_size for item in observations) <= charges,',
                        'C._need(True,'),
    "measured-bound": ('C._need(0 < len(payload) <= EXPERIMENT_BYTES, "measured experiment exceeds65536 bytes")',
                       'C._need(True, "measured experiment exceeds65536 bytes")'),
    "evaluation-limit": ('property_authority=plan.authority, max_read_bytes=reserved)',
                         'property_authority=plan.authority, max_read_bytes=C.TOTAL_BYTES)'),
    "evaluation-debit": ('remaining = reserved - charged', 'remaining = reserved'),
    "seed-accounting": ('pin.byte_size <= summary.authenticated_bytes', '0 <= summary.authenticated_bytes'),
    "evaluation-envelope": ('<= summary.charged_read_bytes <= allowance', '<= summary.charged_read_bytes'),
    "snapshot-envelope": ('0 <= summary.snapshot_bytes <= Evaluation.Q.MAX_SNAPSHOT_BYTES',
                          '0 <= summary.snapshot_bytes'),
    "failed-collection-refund": ('collection = captured\n            return finish(captured.disposition,',
                                 'collection = captured\n            remaining = reserved - captured.charged_read_bytes\n            return finish(captured.disposition,'),
    "failed-evaluation-refund": ('evaluation = checked\n            return finish(checked.disposition,',
                                 'evaluation = checked\n            remaining = reserved - (checked.authentication.charged_read_bytes if checked.authentication else 0)\n            return finish(checked.disposition,'),
    "attach-invalid-collection": ('C._need(type(captured) is UnitCapture and type(captured.reason) is str',
                                  'collection = captured\n        C._need(type(captured) is UnitCapture and type(captured.reason) is str'),
    "attach-invalid-evaluation": ('C._need(type(checked) is Evaluation.EvaluationCheck',
                                  'evaluation = checked\n        C._need(type(checked) is Evaluation.EvaluationCheck'),
    "structured-comments": ('Records.render_forms(plan.forms)', 'Records.render_forms([plan.raw])'),
    "unsupported-finding": ('return finish(exc.disposition, str(exc))', 'return finish("refused", str(exc))'),
}


def main():
    global U
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        source = Path(U.__file__).read_text()
        start = source.index("\n\n@dataclass(frozen=True)\nclass UnitEvaluation:")
        selected = source[start:]
        before, after = MUTATIONS[args.mutation]
        if selected.count(before) != 1:
            raise RuntimeError("combined mutation seam not singular: " + args.mutation)
        module = types.ModuleType("mutated_unit_evaluation")
        module.__file__ = U.__file__
        sys.modules[module.__name__] = module
        exec(compile(source[:start] + selected.replace(before, after, 1),
                     module.__file__, "exec"), module.__dict__)
        U = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(CombinedTests))
    print(f"MATCHED-GPR-UNIT-EVALUATION: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; actual synthetic processes/read bytes, qualification closed")
    return int(not result.wasSuccessful())


if __name__ == "__main__":
    sys.exit(main())
