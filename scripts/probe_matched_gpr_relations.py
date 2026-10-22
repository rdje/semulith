#!/usr/bin/env python3
"""Synthetic declared-method relationship controls; no capture/qualification."""
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
import matched_gpr_relations as M
import probe_matched_gpr_execution as P
import sexp as S


class RelationTests(unittest.TestCase):
    def setUp(self):
        self.experiment, self.candidate = P.fixture()
        self.graph = self.experiment["verification"]
        self.prop = self.graph["property"][0]
        self.control = self.graph["control_run"][0]
        self.base_producer, self.mutant_producer = self.graph["producer"][1:]

    def result(self, disposition, reason=None):
        result = M.bind_relations(self.experiment, self.candidate)
        self.assertEqual(result.disposition, disposition, result)
        if reason: self.assertIn(reason, result.reason)
        if disposition != "matched": self.assertIsNone(result.plan)
        return result

    def test_complete_raw_schema_scoped_graph_and_single_mapper_fixture(self):
        form = P.raw_experiment(self.experiment, self.candidate)
        scope = V.Scope("synthetic", frozenset({"sail-riscv"}), frozenset({"REQ-synthetic"}),
                        frozenset({"OBL-synthetic"}))
        self.assertEqual(V.check_experiment(form, scope), [])
        self.experiment = D.references_to_doc([S.Symbol("references"), form])["experiment"][0]
        result = self.result("matched", "qualification pending")
        self.assertEqual(result.plan.control_property_id, "property")
        self.assertEqual((result.plan.control_witness.step_n, result.plan.control_witness.register), (0, "x1"))
        self.assertEqual(result.plan.properties, (M.PropertyRelation("property", M.GprWitness(0, "x1")),))
        self.assertEqual(result.plan.control_id, "wrong-expectation")
        self.assertEqual(result.plan.expected_version, "source-derivation-v1")
        self.assertEqual(result.plan.derivation_common_input_ids,
                         ("adapter", "dependency-manifest", "guest-source"))
        self.assertEqual(len(result.plan.pairs), 2)

    def test_last_boundary_and_x31_are_supported(self):
        self.experiment["instructions"] = 4096
        for run in self.graph["run"]: run["argv"][4] = "4096"
        self.prop["gpr_witness"] = dict(step_n=4095, register="x31")
        self.result("matched")

    def test_expected_input_and_pair_order_are_unordered(self):
        expected = self.result("matched").plan
        for producer in self.graph["producer"]: producer["input_ids"].reverse()
        self.graph["producer_pair"].reverse()
        for pair in self.graph["producer_pair"]: pair["shared_input_ids"].reverse()
        self.assertEqual(self.result("matched").plan, expected)

    def test_pair_orientation_is_explicit_and_reversible(self):
        for pair in self.graph["producer_pair"]: pair["left"], pair["right"] = pair["right"], pair["left"]
        plan = self.result("matched").plan
        self.assertTrue(all(pair.right == "reference" for pair in plan.pairs))

    def test_empty_declared_intersection_is_supported(self):
        self.graph["producer"][0]["input_ids"] = ["reference-config"]
        for pair in self.graph["producer_pair"]: pair["shared_input_ids"] = []
        self.assertTrue(all(pair.shared_input_ids == () for pair in self.result("matched").plan.pairs))

    def test_coherent_failed_control_observations_remain_data(self):
        for verdict in ("AGREE", "REFUSED"):
            with self.subTest(verdict=verdict):
                self.control["observed_verdict"] = self.graph["run"][2]["verdict"] = verdict
                self.assertEqual(self.result("matched").plan.control_observed_verdict, verdict)

    def test_coherent_failed_processes_do_not_earn_success(self):
        for run in self.graph["run"]: run.update(process_exit=127, verdict="REFUSED")
        self.control["observed_verdict"] = "REFUSED"
        self.result("matched", "authentication/comparison/qualification pending")

    def test_pair_assessment_words_remain_declarations(self):
        for assessment in sorted(M.ASSESSMENTS):
            with self.subTest(assessment=assessment):
                for pair in self.graph["producer_pair"]: pair["assessment"] = assessment
                self.assertTrue(all(pair.assessment == assessment for pair in self.result("matched").plan.pairs))

    def test_actual_expectation_change_and_source_binding_are_separate(self):
        self.graph["input"][-1]["sha256"] = self.graph["input"][-2]["sha256"]
        self.experiment["program"] = "different.s"
        self.result("matched", "pending")

    def test_obligation_scope_is_not_traversed_or_copied(self):
        class NotTraversable:
            def __iter__(self): raise AssertionError("scope owner must validate obligations")
        self.prop["obligation_ids"] = NotTraversable()
        self.result("matched", "pending")

    def test_frozen_nested_facts_have_no_caller_aliases(self):
        result = self.result("matched"); original = deepcopy(result)
        self.prop["gpr_witness"]["register"] = "x2"; self.control["observed_verdict"] = "AGREE"
        self.base_producer["input_ids"].clear(); self.graph["producer_pair"][0]["evidence"] = "changed"
        self.assertEqual(result, original)
        for obj, field in ((result, "reason"), (result.plan, "control_property_id"),
                           (result.plan.control_witness, "register"), (result.plan.properties[0], "property_id"),
                           (result.plan.pairs[0], "evidence")):
            with self.subTest(field=field), self.assertRaises(FrozenInstanceError): setattr(obj, field, "changed")
        self.assertIs(type(result.plan.derivation_common_input_ids), tuple)
        self.assertIs(type(result.plan.pairs[0].shared_input_ids), tuple)

    def test_no_artifact_or_process_io(self):
        with mock.patch("builtins.open", side_effect=AssertionError("unexpected open")), \
             mock.patch("pathlib.Path.open", side_effect=AssertionError("unexpected path open")), \
             mock.patch("os.open", side_effect=AssertionError("unexpected descriptor")), \
             mock.patch("subprocess.run", side_effect=AssertionError("unexpected process")), \
             mock.patch("subprocess.Popen", side_effect=AssertionError("unexpected process")):
            self.result("matched")

    def test_execution_refusal_and_unsupported_propagate(self):
        self.graph["run"][0]["argv"][0] = "wrong/binary"; self.result("refused", "execution:")
        self.graph["comparison_rule"] = "other"; self.result("unsupported", "execution:")
        del self.experiment["verification"]; self.result("unsupported", "legacy")

    def test_exact_local_counts_before_map(self):
        for family in ("property", "control_run", "producer_pair"):
            for change in ("missing", "extra"):
                with self.subTest(family=family, change=change):
                    original = self.graph[family]
                    self.graph[family] = original[:-1] if change == "missing" else original + [None]
                    # Properties are bounded 1..64, so a surplus None is an invalid record, not a count.
                    try: self.result("refused", "record" if (family, change) == ("property", "extra") else "method requires")
                    finally: self.graph[family] = original

    def test_invalid_local_family_type_record_and_id(self):
        for family in ("property", "control_run", "producer_pair"):
            with self.subTest(family=family):
                original = self.graph[family]
                try:
                    self.graph[family] = None; self.result("refused")
                    self.graph[family] = [None] * len(original); self.result("refused", "record")
                    self.graph[family] = deepcopy(original); self.graph[family][0]["id"] = "bad\n"
                    self.result("refused", "id")
                finally: self.graph[family] = original

    def test_well_formed_extra_records_cannot_be_ignored(self):
        for family in ("property", "control_run", "producer_pair"):
            with self.subTest(family=family):
                extra = deepcopy(self.graph[family][0]); extra["id"] = "extra"
                self.graph[family].append(extra)
                # A second property is declared, never ignored: a copy repeats the witness and refuses.
                try: self.result("refused", "one observation" if family == "property" else "method requires")
                finally: self.graph[family].pop()

    def test_failed_subcases_restore_count_and_version_fixtures(self):
        families = ("property", "control_run", "producer_pair")
        counts = dict(zip(families, (1, 1, 2)))
        for method, expected in (
            ("test_exact_local_counts_before_map", [(family,) for family in families for _ in range(2)]),
            ("test_expected_version_is_nonempty_bounded_text", [(pid,) for pid in ("expected", "expected-mutant") for _ in range(4)]),
        ):
            observed = []
            def injected(experiment, candidate):
                graph = experiment["verification"]
                if "counts" in method:
                    observed.append(tuple(family for family in families if len(graph[family]) != counts[family]))
                else:
                    observed.append(tuple(producer["id"] for producer in graph["producer"][1:]
                                          if producer["version"] != "source-derivation-v1"))
                return M.RelationCheck("refused", "injected assertion failure")
            result = unittest.TestResult()
            with mock.patch.object(M, "bind_relations", side_effect=injected): RelationTests(method).run(result)
            self.assertEqual(result.errors, [])
            self.assertEqual(len(result.failures), len(expected))
            self.assertEqual(observed, expected, "a failed subcase contaminated a later fixture")

    def test_duplicate_pair_id_refuses(self):
        self.graph["producer_pair"][1]["id"] = self.graph["producer_pair"][0]["id"]
        self.result("refused", "duplicate")

    def test_exact_gpr_only_observation_kind(self):
        for kinds in ([], ["witnessed-delivery"], ["gpr-change", "witnessed-delivery"],
                      ["gpr-change"] * 2, "gpr-change"):
            with self.subTest(kinds=kinds): self.prop["observation_kinds"] = kinds; self.result("refused")

    def test_missing_wrong_or_surplus_typed_witness(self):
        for witness in (None, {}, dict(step_n=0), dict(step_n=0, register="x1", extra=1), []):
            with self.subTest(witness=witness): self.prop["gpr_witness"] = witness; self.result("refused", "typed GPR")

    def test_witness_step_is_in_parent_budget(self):
        for step in (-1, 1, 4096, True, "0", 0.0):
            with self.subTest(step=step): self.prop["gpr_witness"]["step_n"] = step; self.result("refused", "budget")

    def test_witness_register_is_canonical(self):
        for register in ("x0", "x32", "x01", "x1\n", "X1", None):
            with self.subTest(register=register): self.prop["gpr_witness"]["register"] = register; self.result("refused", "canonical")

    def test_control_names_exact_baseline_and_control(self):
        for field, value in (("baseline_id", None), ("baseline_id", "repeat"),
                             ("run_id", "base"), ("run_id", "unknown")):
            with self.subTest(field=field, value=value):
                original = self.control[field]; self.control[field] = value
                try: self.result("refused", "baseline/control")
                finally: self.control[field] = original

    def test_control_selects_exactly_one_declared_property(self):
        for ids in ([], ["other"], ["property", "other"], ["property"] * 2):
            with self.subTest(ids=ids): self.control["property_ids"] = ids; self.result("refused")

    def more_properties(self, count, register=lambda n: f"x{n}"):
        """Append synthetic properties p2.. with distinct witnesses on the one boundary."""
        for n in range(2, 2 + count):
            prop = deepcopy(self.prop); prop.update(id=f"p{n}", gpr_witness=dict(step_n=0, register=register(n)))
            self.graph["property"].append(prop)

    def test_many_properties_bind_in_record_order_and_the_control_selects_one(self):
        self.more_properties(2); self.control["property_ids"] = ["p3"]
        plan = self.result("matched").plan
        self.assertEqual([item.property_id for item in plan.properties], ["property", "p2", "p3"])
        self.assertEqual([item.witness.register for item in plan.properties], ["x1", "x2", "x3"])
        self.assertEqual((plan.control_property_id, plan.control_witness), ("p3", M.GprWitness(0, "x3")))
        self.control["property_ids"] = ["p4"]; self.result("refused", "declared property")

    def test_property_population_is_bounded_to_one_through_sixty_four(self):
        self.experiment["instructions"] = 4096
        for run in self.graph["run"]: run["argv"][4] = "4096"
        self.more_properties(63, register=lambda n: "x1")
        for n, prop in enumerate(self.graph["property"]): prop["gpr_witness"]["step_n"] = n
        self.assertEqual(len(self.graph["property"]), 64); self.result("matched")
        self.more_properties(1); self.graph["property"][-1]["gpr_witness"]["step_n"] = 64
        self.result("refused", "1..64 property")
        self.graph["property"] = []; self.result("refused", "1..64 property")

    def test_every_property_witness_is_validated_and_distinct(self):
        self.more_properties(1)
        second = self.graph["property"][1]
        for change in (dict(gpr_witness=dict(step_n=0, register="x1")), dict(gpr_witness=dict(step_n=1, register="x2")),
                       dict(gpr_witness=dict(step_n=0, register="x32")), dict(observation_kinds=["witnessed-delivery"]),
                       dict(id="property")):
            with self.subTest(change=change):
                original = deepcopy(second); second.update(change)
                try: self.result("refused")
                finally: second.clear(); second.update(original)
        self.result("matched")

    def test_control_selects_exact_mutant_expectation(self):
        for ids in ([], ["expectation"], ["adapter"], ["mutant-expectation", "adapter"]):
            with self.subTest(ids=ids): self.control["mutation_input_ids"] = ids; self.result("refused")

    def test_first_method_intends_divergence(self):
        self.control["expected_verdict"] = "REFUSED"; self.result("refused", "intended DIVERGE")

    def test_control_verdict_is_valid_and_matches_run(self):
        for value in ("AGREE", "REFUSED", "other", "DIVERGE\n", None):
            with self.subTest(value=value): self.control["observed_verdict"] = value; self.result("refused")

    def test_expected_producers_are_not_external_candidates(self):
        for producer in (self.base_producer, self.mutant_producer):
            with self.subTest(producer=producer["id"]):
                producer["candidate_id"] = "sail-riscv"
                try: self.result("refused", "external candidate")
                finally: del producer["candidate_id"]

    def test_expected_versions_must_match(self):
        self.mutant_producer["version"] = "other-derivation"
        self.result("refused", "versions differ")

    def test_expected_version_is_nonempty_bounded_text(self):
        for producer in (self.base_producer, self.mutant_producer):
            for value in (None, "", 1, "a" * 65537):
                with self.subTest(producer=producer["id"], value_type=type(value).__name__):
                    original = producer["version"]; producer["version"] = value
                    try: self.result("refused", "version")
                    finally: producer["version"] = original

    def test_expected_inputs_are_counted_unique_and_known(self):
        original = list(self.base_producer["input_ids"])
        for ids in ([], original + ["adapter"] * 5, ["adapter"] * 2, ["unknown", "expectation"]):
            with self.subTest(ids=ids): self.base_producer["input_ids"] = ids; self.result("refused")

    def test_expected_producers_consume_their_own_expectation(self):
        for producer in (self.base_producer, self.mutant_producer):
            with self.subTest(producer=producer["id"]):
                original = producer["input_ids"]
                producer["input_ids"] = ["guest-source", "adapter", "dependency-manifest"]
                try: self.result("refused", "selected expectation")
                finally: producer["input_ids"] = original

    def test_expected_producers_cannot_consume_other_expectation(self):
        for producer, wrong in ((self.base_producer, "mutant-expectation"), (self.mutant_producer, "expectation")):
            with self.subTest(producer=producer["id"]):
                producer["input_ids"].append(wrong)
                try: self.result("refused", "nonselected")
                finally: producer["input_ids"].pop()

    def test_declared_derivation_cannot_change_other_inputs(self):
        self.mutant_producer["input_ids"].remove("adapter")
        self.result("refused", "changes other inputs")

    def test_pair_must_name_actual_distinct_producers(self):
        for left, right in (("expected", "expected-mutant"), ("reference", "reference"), ("reference", "unknown")):
            with self.subTest(left=left, right=right):
                self.graph["producer_pair"][0].update(left=left, right=right)
                self.result("refused", "actual run producer pair")

    def test_both_actual_pairs_must_be_assessed_once(self):
        self.graph["producer_pair"][1]["right"] = "expected"
        self.result("refused", "actual run producer pair")

    def test_pair_sharing_is_exact_intersection(self):
        for ids in ([], ["adapter"], ["adapter", "dependency-manifest", "guest-source", "collector"], ["unknown"]):
            with self.subTest(ids=ids):
                self.graph["producer_pair"][0]["shared_input_ids"] = ids
                self.result("refused", "intersection")

    def test_pair_shared_ids_are_bounded_and_unique(self):
        for ids in (["adapter"] * 8, ["adapter"] * 2, None):
            with self.subTest(ids=ids): self.graph["producer_pair"][0]["shared_input_ids"] = ids; self.result("refused")

    def test_pair_declarations_are_required_bounded_and_typed(self):
        pair = self.graph["producer_pair"][0]
        for field in ("subsystem", "assessment", "evidence", "consequence"):
            for value in (None, "", 1, "a" * 65537):
                with self.subTest(field=field, value_type=type(value).__name__):
                    original = pair[field]; pair[field] = value
                    try: self.result("refused")
                    finally: pair[field] = original
        pair["assessment"] = "invented"; self.result("refused", "assessment")


MUTATIONS = {
    "family-counts": ('type(records) in (list, tuple) and len(records) == count,', 'type(records) in (list, tuple),'),
    "gpr-only": ('_ids(prop.get("observation_kinds"), 1, 1, "observation_kinds") == ("gpr-change",),', 'True,'),
    "witness-budget": ('type(step) is int and 0 <= step < execution.instructions,', 'True,'),
    "witness-register": ('isinstance(register, str) and re.fullmatch(r"x([1-9]|[12][0-9]|3[01])", register) is not None,', 'True,'),
    "control-runs": ('control.get("baseline_id") == baseline.run_id and control.get("run_id") == control_run.run_id,', 'True,'),
    "control-property": ('selected in properties,', 'True,'),
    "property-count": ('type(records) in (list, tuple) and minimum <= len(records) <= maximum,', 'type(records) in (list, tuple),'),
    "witness-unique": ('(step, register) not in witnessed,', 'True,'),
    "control-mutation": ('_ids(control.get("mutation_input_ids"), 1, 1, "control mutation_input_ids") == (control_run.expectation_id,),', 'True,'),
    "control-intent": ('control.get("expected_verdict") == "DIVERGE",', 'True,'),
    "control-observed": ('observed == raw_control.get("verdict"),', 'True,'),
    "expected-version": ('_text(mutant_producer.get("version"), "mutant expected version") == version,', 'True,'),
    "expected-selection": ('base_inputs <= common | {baseline.expectation_id}\n             and mutant_inputs <= common | {control_run.expectation_id},', 'True,'),
    "expected-consumes": ('baseline.expectation_id in base_inputs and control_run.expectation_id in mutant_inputs,', 'True,'),
    "expected-common": ('derivation_inputs == mutant_inputs - {control_run.expectation_id},', 'True,'),
    "pair-endpoints": ('endpoints in needed and endpoints not in actual,', 'True,'),
    "pair-sharing": ('set(shared) == reference_inputs & expected_inputs,', 'True,'),
    "fixture-count-cleanup": ('                    finally: self.graph[family] = original\n',
                              '                    finally: pass\n                    self.graph[family] = original\n'),
    "fixture-version-cleanup": ('                    finally: producer["version"] = original\n',
                                '                    finally: pass\n                    producer["version"] = original\n'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    test_class = RelationTests
    if args.mutation:
        global M
        filename = __file__ if args.mutation.startswith("fixture-") else M.__file__
        source = Path(filename).read_text(); before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1: raise SystemExit("mutation seam is not singular")
        module = types.ModuleType("mutated_gpr_relations"); module.__file__ = filename
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), filename, "exec"), module.__dict__)
        if args.mutation.startswith("fixture-"): test_class = module.RelationTests
        else: M = module
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"MATCHED-GPR-RELATIONS: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; synthetic only")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
