#!/usr/bin/env python3
"""Synthetic parent-program controls; identifier equality is not source/image proof."""
from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock

import dossier_sexp as D
import matched_gpr_comparison as C
import matched_gpr_evaluation as E
import probe_matched_gpr_comparison as PC
import probe_matched_gpr_evaluation as PE
import sexp as S

ROOT = Path(__file__).resolve().parent.parent


class String(str):
    pass


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.args = PC.fixture()

    def change(self, role, **fields):
        doc = D.expectations_to_doc(S.parse(self.args[role].decode())[0])
        doc.update(fields)
        self.args[role] = PC.encode(doc)

    def refused(self, program, reason):
        with self.assertRaises(C.UnitError) as caught:
            C.compare_unit(program=program, **self.args)
        self.assertIn(reason, str(caught.exception))

    def test_exact_program_binds(self):
        self.assertEqual(C.compare_unit(program="fixture.s", **self.args).disposition, "satisfied")

    def test_legacy_omitted_context_preserves_pure_unit(self):
        for role in ("baseline_expectation", "control_expectation"):
            self.change(role, program="other.s")
        self.assertEqual(C.compare_unit(**self.args).disposition, "satisfied")
        self.assertEqual(C.compare_unit(program=None, **self.args).disposition, "satisfied")

    def test_both_consistently_wrong_programs_refuse(self):
        for role in ("baseline_expectation", "control_expectation"):
            self.change(role, program="other.s")
        self.refused("fixture.s", "expectation program differs from parent")

    def test_only_baseline_wrong_refuses(self):
        self.change("baseline_expectation", program="other.s")
        self.refused("fixture.s", "expectation program differs from parent")

    def test_only_control_wrong_refuses(self):
        self.change("control_expectation", program="other.s")
        self.refused("fixture.s", "expectation program differs from parent")

    def test_program_identity_is_exact_without_path_inference(self):
        for value in ("Fixture.s", "dir/fixture.s", "fixture.s ", "./fixture.s"):
            with self.subTest(value=value):
                self.refused(value, "expectation program differs from parent")

    def test_non_plain_parent_types_refuse_before_payload_validation(self):
        for value in (1, True, b"fixture.s", ["fixture.s"], String("fixture.s")):
            with self.subTest(value=repr(value)):
                self.refused(value, "parent program must be a plain string")

    def test_empty_program_refuses(self):
        self.refused("", "parent program must be a plain string")

    def test_inclusive_program_limit_matches(self):
        program = "x" * 65536
        for role in ("baseline_expectation", "control_expectation"):
            self.change(role, program=program)
        self.assertEqual(C.compare_unit(program=program, **self.args).disposition, "satisfied")

    def test_oversized_program_refuses_before_payload_validation(self):
        self.args["baseline_expectation"] = object()
        self.refused("x" * 65537, "parent program must be a plain string")

    def test_wrong_program_refuses_before_unsupported_expectation(self):
        self.change("baseline_expectation", program="other.s", cross_model=False)
        self.change("control_expectation", program="other.s", cross_model=False)
        self.refused("fixture.s", "expectation program differs from parent")

    def test_correct_program_preserves_unsupported_disposition(self):
        self.change("baseline_expectation", cross_model=False)
        self.change("control_expectation", cross_model=False)
        self.assertEqual(C.compare_unit(program="fixture.s", **self.args).disposition, "unsupported")


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        parent = ROOT / "target/p4-system-14/a42a/program-fixtures"
        parent.mkdir(parents=True, exist_ok=True)
        scratch = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(scratch.cleanup)
        self.fixture = PE.Fixture(Path(scratch.name))

    def change(self, role, **fields):
        doc = deepcopy(self.fixture.base if role == "expectation" else self.fixture.control)
        doc.update(fields)
        self.fixture.write(self.fixture.inputs[role], PC.encode(doc))

    def check(self):
        return E.evaluate_retained_unit(self.fixture.root, **self.fixture.arguments())

    def refused(self):
        result = self.check()
        self.assertEqual(result.disposition, "refused", result)
        self.assertEqual(result.record.disposition, "valid")
        self.assertEqual(result.authentication.disposition, "matched")
        self.assertEqual(result.identity.disposition, "matched")
        self.assertEqual(len(result.receipts), 3)
        self.assertIsNone(result.comparison)
        self.assertIn("expectation program differs from parent", result.reason)
        return result

    def test_ordinary_composition_remains_pending(self):
        self.assertEqual(self.check().disposition, "pending")

    def test_repinned_consistently_wrong_programs_refuse_after_authentication(self):
        for role in ("expectation", "mutant-expectation"):
            self.change(role, program="other.s")
        self.fixture.publish_receipts()
        self.refused()

    def test_repinned_wrong_baseline_refuses(self):
        self.change("expectation", program="other.s")
        self.fixture.publish_receipts()
        self.refused()

    def test_repinned_wrong_control_refuses(self):
        self.change("mutant-expectation", program="other.s")
        self.fixture.publish_receipts()
        self.refused()

    def test_changed_parent_program_refuses_with_unchanged_retained_bytes(self):
        self.fixture.experiment["program"] = "other.s"
        self.refused()

    def test_unsupported_wrong_program_still_refuses(self):
        for role in ("expectation", "mutant-expectation"):
            self.change(role, program="other.s", cross_model=False)
        self.fixture.publish_receipts()
        self.refused()

    def test_unsupported_rule_retains_classification_before_program_bound(self):
        self.fixture.experiment["program"] = "x" * 65537
        self.fixture.graph["comparison_rule"] = "another-rule"
        with mock.patch.object(E.M, "read_dependency_manifest", wraps=E.M.read_dependency_manifest) as manifest:
            result = self.check()
        self.assertEqual(result.disposition, "unsupported", result)
        self.assertEqual(result.record.disposition, "valid")
        self.assertIsNone(result.authentication)
        manifest.assert_not_called()

    def test_parent_program_bound_precedes_artifact_reads(self):
        self.fixture.experiment["program"] = "x" * 65537
        with mock.patch.object(E.M, "read_dependency_manifest", wraps=E.M.read_dependency_manifest) as manifest:
            result = self.check()
        self.assertEqual(result.disposition, "refused", result)
        self.assertEqual(result.record.disposition, "valid")
        self.assertIsNone(result.authentication)
        self.assertIn("parent program outside", result.reason)
        manifest.assert_not_called()

    def test_inclusive_parent_program_bound_binds(self):
        program = "x" * 65536
        self.fixture.experiment["program"] = program
        for role in ("expectation", "mutant-expectation"):
            self.change(role, program=program)
        self.fixture.publish_receipts()
        self.assertEqual(self.check().disposition, "pending")

    def test_canonical_program_change_during_manifest_read_uses_frozen_context(self):
        read = E.M.read_dependency_manifest
        changed = []
        def mutate(root, **kwargs):
            experiment = kwargs["experiment"]
            changed.append((experiment, experiment["program"]))
            experiment["program"] = "changed-after-binding.s"
            return read(root, **kwargs)
        try:
            with mock.patch.object(E.M, "read_dependency_manifest", side_effect=mutate):
                self.assertEqual(self.check().disposition, "pending")
        finally:
            for experiment, program in changed:
                experiment["program"] = program
        self.assertEqual(len(changed), 1)

    def test_accepted_mapped_string_context_normalizes_to_plain_value(self):
        mapping = E.D.references_to_doc
        def mapped(*args, **kwargs):
            doc = mapping(*args, **kwargs)
            for experiment in doc.get("experiment", []):
                experiment["program"] = String(experiment["program"])
            return doc
        with mock.patch.object(E.D, "references_to_doc", side_effect=mapped):
            self.assertEqual(self.check().disposition, "pending")


PROGRAM_CONTEXT = '        program = str(experiment["program"])\n        if not 1 <= len(program) <= 65536:\n            raise ValueError("parent program outside 1..65536 characters")\n'


MUTATIONS = {
    "program-type": ("comparison", 'if program is not None and (type(program) is not str or not 1 <= len(program) <= 65536):', 'if False:'),
    "program-binding": ("comparison", 'if program is not None and (base["program"] != program or changed["program"] != program):', 'if False:'),
    "program-forward": ("evaluation", 'program=program,', 'program=None,'),
    "program-freeze": ("evaluation", 'program=program,', 'program=str(experiment["program"]),'),
    "program-bound": ("evaluation", 'if not 1 <= len(program) <= 65536:', 'if False:'),
    "program-plain": ("evaluation", 'program = str(experiment["program"])', 'program = experiment["program"]'),
    "program-selection": ("evaluation", PROGRAM_CONTEXT, ""),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        global C, E
        owner, before, after = MUTATIONS[args.mutation]
        original = C if owner == "comparison" else E
        source = Path(original.__file__).read_text()
        if source.count(before) != 1:
            raise SystemExit("mutation seam is not singular")
        module = types.ModuleType("mutated_program_" + owner)
        module.__file__ = original.__file__
        sys.modules[module.__name__] = module
        source = source.replace(before, after)
        if args.mutation == "program-selection":
            marker = '        identity_context = I.bind_reference_identity(current_candidate)\n'
            if source.count(marker) != 1:
                raise SystemExit("selection mutation seam is not singular")
            source = source.replace(marker, PROGRAM_CONTEXT + marker, 1)
        exec(compile(source, original.__file__, "exec"), module.__dict__)
        if owner == "comparison":
            # Omit only the new guard; preserve the public pre-existing value types.
            for name in ("GprWitness", "RunBytes", "RunComparison", "ComparisonUnit"):
                setattr(module, name, getattr(C, name))
            C = module
            E.C = C
        else:
            E = module
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(cls)
                               for cls in (ComparisonTests, EvaluationTests))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"MATCHED-GPR-PROGRAM: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; synthetic only")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
