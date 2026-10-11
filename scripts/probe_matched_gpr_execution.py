#!/usr/bin/env python3
"""Synthetic execution-binding controls; no files, execution or capture evidence."""
from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import FrozenInstanceError
from pathlib import Path
import sys
import types
import unittest
from unittest import mock

import dossier_sexp as D
import experiment_verification as V
import matched_gpr_execution as M
import probe_matched_gpr_identity as I


def fixture():
    """A complete synthetic envelope, including the separately owned graph edges."""
    candidate = I.candidate()
    roles = (*M.COMMON_ROLES, "expectation")
    inputs = [dict(id=role, role=role, path="inputs/" + role, sha256=f"{n + 1:x}" * 64)
              for n, role in enumerate(roles)]
    inputs.append(dict(id="mutant-expectation", role="expectation",
                       path="inputs/mutant-expectation", sha256="9" * 64))
    common = list(M.COMMON_ROLES)
    producers = [dict(id="reference", role="reference", candidate_id="sail-riscv",
                      version="sha256:" + candidate["binary_sha256"], input_ids=common)]
    for pid, expectation in (("expected", "expectation"), ("expected-mutant", "mutant-expectation")):
        producers.append(dict(id=pid, role="expected", version="source-derivation-v1",
                              input_ids=["guest-source", expectation, "adapter", "dependency-manifest"]))
    observations, runs = [], []
    for kind, rid in (("baseline", "base"), ("repeat", "repeat"), ("control", "control")):
        outputs = [dict(id=rid + "-" + role, role=role, path=f"outputs/{rid}.{role}",
                        sha256="b" * 64, byte_size=0) for role in M.OUTPUT_ROLES]
        observations.extend(outputs)
        run = dict(id=rid, kind=kind, input_ids=common + ["mutant-expectation" if kind == "control" else "expectation"],
                   producer_ids=["reference", "expected-mutant" if kind == "control" else "expected"],
                   observation_ids=[output["id"] for output in outputs], process_exit=0,
                   verdict="DIVERGE" if kind == "control" else "AGREE",
                   argv=[candidate["binary"], "--config-override", "inputs/reference-config",
                         "--inst-limit", "1", "--trace-instr", "--trace-gpr", "--trace-exception",
                         "--trace-output", outputs[0]["path"], "inputs/guest-image"])
        if kind == "repeat": run["repeat_of"] = "base"
        runs.append(run)
    pairs = [dict(id=pid + "-pair", left="reference", right=pid, subsystem="gpr-change",
                  assessment="not-examined", shared_input_ids=["guest-source", "adapter", "dependency-manifest"],
                  evidence="unknown; synthetic fixture", consequence="no independence credit")
             for pid in ("expected", "expected-mutant")]
    graph = dict(format_version="matched-gpr-v1", comparison_rule="sail-gpr-change-v1",
                 limitations=["synthetic; no execution or qualification"], input=inputs,
                 producer=producers, observation=observations, run=runs, producer_pair=pairs,
                 property=[dict(id="property", statement="synthetic GPR change", requirement_id="REQ-synthetic", obligation_ids=["OBL-synthetic"],
                                observation_kinds=["gpr-change"], gpr_witness=dict(step_n=0, register="x1"))],
                 control_run=[dict(id="wrong-expectation", run_id="control", baseline_id="base",
                                   property_ids=["property"], mutation_input_ids=["mutant-expectation"],
                                   expected_verdict="DIVERGE", observed_verdict="DIVERGE",
                                   reason="synthetic wrong-expectation control")])
    experiment = dict(id="synthetic", program="synthetic.s", instructions=1, models=["sail-riscv"],
                      verdict="AGREE", reproduced="synthetic fixture", control="synthetic fixture", verification=graph)
    return experiment, candidate


def raw_experiment(experiment, candidate):
    document = I.document(candidate); document["experiment"] = [experiment]
    return next(form for form in D.references_to_form(document)
                if isinstance(form, list) and form and form[0] == "experiment")


class ExecutionTests(unittest.TestCase):
    def setUp(self):
        self.experiment, self.candidate = fixture()
        self.graph = self.experiment["verification"]
        self.base, self.repeat, self.control = self.graph["run"]

    def result(self, disposition, reason=None):
        result = M.bind_execution(self.experiment, self.candidate)
        self.assertEqual(result.disposition, disposition, result)
        if reason: self.assertIn(reason, result.reason)
        if disposition != "matched": self.assertIsNone(result.plan)
        return result

    def test_complete_fixture_passes_raw_schema_and_scoped_graph(self):
        scope = V.Scope("synthetic", frozenset({"sail-riscv"}), frozenset({"REQ-synthetic"}),
                        frozenset({"OBL-synthetic"}))
        self.assertEqual(V.check_experiment(raw_experiment(self.experiment, self.candidate), scope), [])
        plan = self.result("matched", "qualification pending").plan
        self.assertEqual(plan.reference_producer_id, "reference")
        self.assertEqual(tuple(item.role for item in plan.common_inputs), M.COMMON_ROLES)
        self.assertEqual(tuple(run.kind for run in plan.runs), M.RUN_KINDS)
        self.assertEqual(plan.runs[0].argv, tuple(self.base["argv"]))

    def test_inclusive_maximum_budget(self):
        self.experiment["instructions"] = 4096
        for run in self.graph["run"]: run["argv"][4] = "4096"
        self.assertEqual(self.result("matched").plan.instructions, 4096)

    def test_collections_and_memberships_are_unordered(self):
        expected = self.result("matched").plan
        for family in ("input", "observation", "producer", "run"): self.graph[family].reverse()
        for run in self.graph["run"]:
            for field in ("input_ids", "producer_ids", "observation_ids"): run[field].reverse()
        self.assertEqual(self.result("matched").plan, expected)

    def test_coherent_failed_processes_are_data(self):
        for run in self.graph["run"]: run.update(process_exit=127, verdict="REFUSED")
        self.graph["control_run"][0]["observed_verdict"] = "REFUSED"
        self.result("matched", "complete method/qualification pending")

    def test_property_control_pair_semantics_are_separate(self):
        for family in ("property", "control_run", "producer_pair"): self.graph[family] = []
        self.result("matched", "pending")

    def test_expected_derivation_and_value_change_are_separate(self):
        self.graph["producer"][2]["version"] = "unrelated"
        self.graph["input"][-1]["sha256"] = self.graph["input"][-2]["sha256"]
        self.result("matched", "pending")

    def test_plan_is_frozen_and_detached(self):
        result = self.result("matched"); original = deepcopy(result)
        self.candidate["binary"] = "changed"
        self.graph["input"][0]["path"] = "changed"
        self.base["argv"][0] = "changed"; self.base["observation_ids"].clear()
        self.assertEqual(result, original)
        for obj, field in ((result, "reason"), (result.plan, "instructions"),
                           (result.plan.common_inputs[0], "path"), (result.plan.runs[0], "argv")):
            with self.subTest(field=field), self.assertRaises(FrozenInstanceError): setattr(obj, field, "changed")
        self.assertIs(type(result.plan.runs[0].argv), tuple)
        self.assertTrue(all(type(pair) is tuple for pair in result.plan.runs[0].observations))

    def test_no_artifact_io_or_execution(self):
        with mock.patch("builtins.open", side_effect=AssertionError("unexpected open")), \
             mock.patch("pathlib.Path.open", side_effect=AssertionError("unexpected path open")), \
             mock.patch("os.open", side_effect=AssertionError("unexpected descriptor")), \
             mock.patch("subprocess.run", side_effect=AssertionError("unexpected process")), \
             mock.patch("subprocess.Popen", side_effect=AssertionError("unexpected process")):
            self.result("matched")

    def test_legacy_and_other_rule_are_unsupported(self):
        del self.experiment["verification"]; self.result("unsupported", "legacy")
        self.experiment["verification"] = self.graph
        self.graph["comparison_rule"] = "other"; self.result("unsupported", "another")

    def test_malformed_context_and_version_refuse(self):
        self.experiment = None; self.result("refused")
        self.experiment = {"verification": []}; self.result("refused")
        self.experiment = {"verification": {"format_version": "other"}}; self.result("refused")

    def test_budget_refuses_bool_zero_surplus_and_wrong_type(self):
        for value in (True, 0, -1, 4097, "1", None):
            with self.subTest(value=value): self.experiment["instructions"] = value; self.result("refused", "budget")

    def test_models_are_sole_sail(self):
        for value in ([], ["other"], ["sail-riscv", "other"], ["sail-riscv"] * 2, "sail-riscv"):
            with self.subTest(value=value): self.experiment["models"] = value; self.result("refused")

    def test_current_candidate_is_sail(self):
        self.candidate["id"] = "other"; self.result("refused", "current candidate")
        self.candidate = None; self.result("refused", "current candidate")

    def test_candidate_path_and_digest_refuse(self):
        for field, value in (("binary", "../sail"), ("binary", "/sail"), ("binary", "a//sail"),
                             ("binary", "a\\sail"), ("binary", "a:sail"), ("binary", "a\n"),
                             ("binary_sha256", "A" * 64), ("binary_sha256", "a" * 64 + "\n")):
            with self.subTest(field=field, value=value):
                original = self.candidate[field]; self.candidate[field] = value
                self.result("refused"); self.candidate[field] = original

    def test_family_counts_refuse_before_indexing(self):
        for family in ("input", "observation", "run", "producer"):
            for change in ("missing", "extra"):
                with self.subTest(family=family, change=change):
                    original = self.graph[family]
                    self.graph[family] = original[:-1] if change == "missing" else original + [None]
                    # A bad excess element cannot be visited before the count refusal.
                    self.result("refused", "method requires")
                    self.graph[family] = original

    def test_family_type_and_duplicate_ids_refuse(self):
        for family in ("input", "observation", "run", "producer"):
            with self.subTest(family=family):
                original = self.graph[family]; self.graph[family] = {}; self.result("refused")
                self.graph[family] = deepcopy(original)
                self.graph[family][-1]["id"] = self.graph[family][0]["id"]
                self.result("refused", "duplicate"); self.graph[family] = original

    def test_invalid_record_and_id_refuse(self):
        self.graph["input"][0] = None; self.result("refused", "record")
        self.graph["input"][0] = dict(id="bad\n"); self.result("refused", "id")

    def test_used_string_length_is_bounded(self):
        self.graph["input"][0]["id"] = "a" * 65537; self.result("refused", "id")

    def test_input_paths_and_digests_refuse(self):
        for field, value in (("path", "../source"), ("sha256", "B" * 64), ("sha256", "b" * 64 + "\n")):
            with self.subTest(field=field):
                original = self.graph["input"][0][field]; self.graph["input"][0][field] = value
                self.result("refused"); self.graph["input"][0][field] = original

    def test_observation_paths_digests_sizes_and_roles_refuse(self):
        for field, value in (("path", "a//trace"), ("sha256", "b" * 63), ("byte_size", -1),
                             ("byte_size", True), ("byte_size", "0"), ("role", "other")):
            with self.subTest(field=field, value=value):
                original = self.graph["observation"][0][field]; self.graph["observation"][0][field] = value
                self.result("refused"); self.graph["observation"][0][field] = original

    def test_input_output_path_aliases_refuse(self):
        self.graph["observation"][0]["path"] = self.graph["input"][0]["path"]
        self.result("refused", "alias")

    def test_duplicate_common_or_missing_principal_roles_refuse(self):
        self.graph["input"][0]["role"] = "guest-image"; self.result("refused", "principal input roles")

    def test_reference_expected_role_counts_refuse(self):
        self.graph["producer"][2]["role"] = "reference"; self.result("refused", "one reference")

    def test_reference_candidate_binding_refuses(self):
        self.graph["producer"][0]["candidate_id"] = "other"; self.result("refused", "binary pin")

    def test_reference_binary_version_binding_refuses(self):
        self.graph["producer"][0]["version"] = "sha256:" + "c" * 64; self.result("refused", "binary pin")

    def test_missing_reference_version_refuses(self):
        del self.graph["producer"][0]["version"]; self.result("refused", "binary pin")

    def test_reference_inputs_must_be_common(self):
        self.graph["producer"][0]["input_ids"] = ["expectation"]
        self.result("refused", "noncommon")

    def test_reference_input_count_and_duplicates_refuse(self):
        for value in ([], list(M.COMMON_ROLES) + ["expectation"], ["guest-image"] * 2):
            with self.subTest(value=value):
                self.graph["producer"][0]["input_ids"] = value; self.result("refused")

    def test_run_kind_coverage_refuses(self):
        self.control["kind"] = "repeat"; self.result("refused", "baseline/repeat/control")

    def test_run_input_counts_duplicates_unknowns_and_coverage_refuse(self):
        for value in (self.base["input_ids"][:-1], self.base["input_ids"] + ["mutant-expectation"],
                      ["unknown"] + self.base["input_ids"][1:], ["guest-image"] * 8,
                      self.base["input_ids"][1:] + ["mutant-expectation"]):
            with self.subTest(value=value): self.base["input_ids"] = value; self.result("refused")

    def test_run_producer_counts_and_unknowns_refuse(self):
        for value in (["reference"], ["reference", "expected", "expected-mutant"],
                      ["reference"] * 2, ["reference", "unknown"]):
            with self.subTest(value=value): self.base["producer_ids"] = value; self.result("refused")

    def test_run_must_select_reference(self):
        self.base["producer_ids"] = ["expected", "expected-mutant"]
        self.result("refused", "sole reference")

    def test_repeat_must_name_baseline(self):
        for value in (None, "control", "missing"):
            with self.subTest(value=value): self.repeat["repeat_of"] = value; self.result("refused", "name baseline")

    def test_spurious_repeat_edges_refuse(self):
        for run in (self.base, self.control):
            with self.subTest(kind=run["kind"]):
                run["repeat_of"] = "base"; self.result("refused", "spurious"); del run["repeat_of"]

    def test_repeat_expectation_must_match_baseline(self):
        self.repeat["input_ids"][-1] = "mutant-expectation"
        self.result("refused", "repeat inputs/expected producer")

    def test_repeat_expected_producer_must_match_baseline(self):
        self.repeat["producer_ids"][-1] = "expected-mutant"
        self.result("refused", "repeat inputs/expected producer")

    def test_control_expectation_must_differ(self):
        self.control["input_ids"][-1] = "expectation"
        self.result("refused", "distinct expectation")

    def test_control_expected_producer_must_differ(self):
        self.control["producer_ids"][-1] = "expected"
        self.result("refused", "distinct expected producer")

    def test_run_observation_counts_duplicates_unknowns_refuse(self):
        for value in (self.base["observation_ids"][:-1], self.base["observation_ids"] + ["repeat-raw-gpr"],
                      ["base-raw-gpr"] * 4, ["unknown"] + self.base["observation_ids"][1:]):
            with self.subTest(value=value): self.base["observation_ids"] = value; self.result("refused")

    def test_run_observations_have_unique_owners(self):
        self.repeat["observation_ids"] = list(self.base["observation_ids"])
        self.repeat["argv"][9] = self.base["argv"][9]
        self.result("refused", "reused")

    def test_run_requires_all_four_output_roles(self):
        self.graph["observation"][1]["role"] = "raw-gpr"
        self.result("refused", "all four")

    def test_each_argv_position_is_fixed(self):
        for run in self.graph["run"]:
            for n in range(11):
                with self.subTest(kind=run["kind"], position=n):
                    original = run["argv"][n]; run["argv"][n] = "changed"
                    self.result("refused", "fixed public invocation"); run["argv"][n] = original

    def test_argv_type_count_order_and_empty_arguments_refuse(self):
        original = list(self.base["argv"])
        for value in (None, "shell command", original[:-1], original + ["extra"],
                      list(reversed(original)), original[:5] + [""] + original[6:]):
            with self.subTest(value=value): self.base["argv"] = value; self.result("refused", "fixed public invocation")

    def test_argv_budget_is_parent_budget(self):
        self.experiment["instructions"] = 2; self.result("refused", "fixed public invocation")

    def test_argv_uses_selected_config_and_image(self):
        for role in ("reference-config", "guest-image"):
            with self.subTest(role=role):
                item = next(item for item in self.graph["input"] if item["role"] == role)
                original = item["path"]; item["path"] = "inputs/changed"
                self.result("refused", "fixed public invocation"); item["path"] = original

    def test_argv_uses_current_binary(self):
        self.candidate["binary"] = "reference/bin/another-sail"
        self.result("refused", "fixed public invocation")

    def test_argv_uses_this_runs_trace(self):
        self.control["argv"][9] = self.base["argv"][9]
        self.result("refused", "fixed public invocation")


MUTATIONS = {
    "budget": ('type(count) is int and 1 <= count <= MAX_BOUNDARIES,', 'True,'),
    "family-counts": ('type(records) in (list, tuple) and len(records) == count,', 'type(records) in (list, tuple),'),
    "reference-pin": ('reference.get("candidate_id") == "sail-riscv"\n             and reference.get("version") == "sha256:" + binary_sha,', 'True,'),
    "run-reference": ('set(active_ids) <= producers.keys() and reference["id"] in active_ids,', 'set(active_ids) <= producers.keys(),'),
    "repeat-edge": ('run.get("repeat_of") == by_kind["baseline"]["id"],', 'True,'),
    "spurious-repeat": ('"repeat_of" not in run,', 'True,'),
    "output-ownership": ('not owned.intersection(oids),', 'True,'),
    "fixed-argv": ('type(actual) in (list, tuple) and len(actual) == 11 and tuple(actual) == argv,', 'True,'),
    "repeat-selection": ('selected["repeat"] == baseline and expected_ids["repeat"] == expected_ids["baseline"],', 'True,'),
    "control-expectation": ('selected["control"]["expectation"].input_id != baseline["expectation"].input_id,', 'True,'),
    "control-producer": ('expected_ids["control"] != expected_ids["baseline"],', 'True,'),
    "reference-inputs": ('set(reference_inputs) <= common_ids,', 'True,'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        global M
        source = Path(M.__file__).read_text(); before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1: raise SystemExit("mutation seam is not singular")
        module = types.ModuleType("mutated_gpr_execution"); module.__file__ = M.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), M.__file__, "exec"), module.__dict__)
        M = module
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ExecutionTests)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"MATCHED-GPR-EXECUTION: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; synthetic only")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
