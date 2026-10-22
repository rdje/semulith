#!/usr/bin/env python3
"""Authenticated source-value composition controls; no execution or qualification."""
from __future__ import annotations

from copy import deepcopy
import argparse
from dataclasses import FrozenInstanceError, fields, replace
import hashlib
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock

import matched_gpr_evaluation as E
import probe_matched_gpr_evaluation as P
import probe_matched_gpr_image_evaluation as PI


ROOT = Path(__file__).resolve().parent.parent


class ValueEvaluationTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/p4-system-14/a42q/fixtures"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.f = P.Fixture(Path(temporary.name))

    def evaluate(self):
        return E.evaluate_retained_unit(self.f.root, **self.f.arguments())

    def outcome(self, disposition="pending", reason=None):
        try:
            checked = self.evaluate()
        except (
            AttributeError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
            OSError,
            AssertionError,
        ) as exc:
            self.fail(f"source-value evaluation escaped as {type(exc).__name__}: {exc}")
        self.assertEqual(checked.disposition, disposition, checked.reason)
        if disposition == "pending":
            self.assertIsNotNone(checked.source_values, "source-value finding was dropped")
        if reason:
            self.assertIn(reason, checked.reason)
        self.assertFalse(PI.has_payload(checked))
        self.assertFalse(hasattr(checked, "qualified"))
        return checked

    def repin(self, role, payload):
        self.f.write(self.f.inputs[role], payload)
        self.f.publish_receipts()

    def mixed(self):
        self.f.experiment["instructions"] = 2
        self.f.graph["property"][0]["gpr_witness"] = dict(step_n=1, register="x1")
        for run in self.f.runs.values():
            run["argv"][4] = "2"
        self.f.source = b"addi x1, x0, 1\nc.addi x1, 1\n"
        self.f.image = P.G.build_guest_image(
            self.f.source, program=self.f.experiment["program"], entry=self.f.entry
        ).image
        self.f.write(self.f.inputs["guest-source"], self.f.source)
        self.f.write(self.f.inputs["guest-image"], self.f.image)
        self.f.base = P.PC.P.expected([{"x1": "0x1"}, {"x1": "0x2"}])
        self.f.base.update(program=self.f.experiment["program"], entry=hex(self.f.entry))
        self.f.control = deepcopy(self.f.base)
        self.f.control["step"][1]["writes"]["x1"] = "0x3"
        self.f.write(self.f.inputs["expectation"], P.PC.encode(self.f.base))
        self.f.write(self.f.inputs["mutant-expectation"], P.PC.encode(self.f.control))
        self.f.trace = (
            b"[0] [M]: 0x0000000080000000 (0x00100093) addi x1, x0, 1\n"
            b"x1 <- 0x0000000000000001\n"
            b"[1] [M]: 0x0000000080000004 (0x0085) c.addi x1, 1\n"
            b"x1 <- 0x0000000000000002\n"
        )
        for kind in self.f.runs:
            self.f.write(self.f.observation(kind, "raw-gpr"), self.f.trace)
        self.f.publish_receipts()

    def test_positive_keeps_independent_source_value_finding(self):
        checked = self.evaluate()
        self.assertEqual(checked.disposition, "pending")
        finding = getattr(checked, "source_values", None)
        self.assertIsNotNone(finding, "authenticated source-value composition is absent")
        self.assertEqual(finding.disposition, "matched")
        self.assertEqual(finding.facts.witness_value, 1)

    def test_coherent_pinned_wrong_value_fails_despite_byte_agreement(self):
        self.f.base["step"][0]["writes"]["x1"] = "0x9"
        self.f.control = deepcopy(self.f.base)
        self.f.control["step"][0]["writes"]["x1"] = "0xa"
        self.f.write(self.f.inputs["expectation"], P.PC.encode(self.f.base))
        self.f.write(self.f.inputs["mutant-expectation"], P.PC.encode(self.f.control))
        trace = (
            b"[0] [M]: 0x0000000080000000 (0x00100093) addi x1, x0, 1\n"
            b"x1 <- 0x0000000000000009\n"
        )
        for kind in self.f.runs:
            self.f.write(self.f.observation(kind, "raw-gpr"), trace)
        self.f.publish_receipts()
        checked = self.evaluate()
        self.assertEqual(checked.record.disposition, "valid")
        self.assertEqual(checked.authentication.disposition, "matched")
        self.assertEqual(checked.comparison.disposition, "satisfied")
        self.assertEqual(checked.source_image.disposition, "matched")
        self.assertEqual(checked.disposition, "failed", "coherent source mismatch remains unbound")
        self.assertIsNotNone(checked.source_values, "failed source-value finding was dropped")
        self.assertEqual(checked.source_values.difference.observed, (("x1", 1),))
        self.assertEqual(checked.source_values.difference.expected, (("x1", 9),))

    def test_exact_retained_source_baseline_and_frozen_selection_reach_owner_once(self):
        self.mixed()
        source = (self.f.root / self.f.inputs["guest-source"]["path"]).read_bytes()
        baseline = (self.f.root / self.f.inputs["expectation"]["path"]).read_bytes()
        with mock.patch.object(
            E.C, "compare_source_expectation", wraps=E.C.compare_source_expectation
        ) as checking:
            checked = self.outcome()
        checking.assert_called_once_with(
            source=source,
            baseline_expectation=baseline,
            instructions=2,
            program=self.f.experiment["program"],
            witness=E.C.GprWitness(1, "x1"),
        )
        self.assertEqual(
            (checked.source_values.facts.witness.step_n, checked.source_values.facts.witness_value),
            (1, 2),
        )
        self.assertEqual(checked.source_values.facts.derivation.steps[1].instruction_bits, 0x0085)

    def test_source_and_image_metadata_agree(self):
        checked = self.outcome()
        derived, image = checked.source_values.facts.derivation, checked.source_image.facts
        for name in (
            "program",
            "entry",
            "encoding_path",
            "source_size",
            "source_sha256",
            "payload_size",
            "payload_sha256",
        ):
            with self.subTest(name=name):
                self.assertEqual(getattr(derived, name), getattr(image, name))
        self.assertEqual(derived.source_sha256, self.f.inputs["guest-source"]["sha256"])

    def test_all_old_positional_fields_keep_their_meaning(self):
        comparison = E.C.ComparisonUnit("unsupported", "example")
        image = E.F.SourceImageCheck("refused", "example")
        checked = E.EvaluationCheck(
            "pending",
            "old",
            E.RecordCheck("valid"),
            None,
            None,
            None,
            (),
            comparison,
            image,
            None,
            None,
        )
        self.assertIs(checked.comparison, comparison)
        self.assertIs(checked.source_image, image)
        self.assertIsNone(checked.source_values)
        self.assertEqual(
            [field.name for field in fields(checked)][8:12],
            ["source_image", "input_review", "impact", "source_values"],
        )

    def test_missing_stale_and_refused_inputs_precede_source_values(self):
        self.repin("guest-source", b"changed\n")
        with mock.patch.object(
            E.C, "compare_source_expectation", side_effect=AssertionError("source values called")
        ):
            checked = self.outcome("refused", "source/image")
        self.assertIsNone(checked.source_values)
        path = self.f.root / self.f.inputs["guest-source"]["path"]
        path.write_bytes(b"changed again")
        with mock.patch.object(
            E.C, "compare_source_expectation", side_effect=AssertionError("source values called")
        ):
            self.assertIsNone(self.outcome("stale", "files").source_values)
        path.unlink()
        with mock.patch.object(
            E.C, "compare_source_expectation", side_effect=AssertionError("source values called")
        ):
            self.assertIsNone(self.outcome("unavailable", "files").source_values)

    def test_failed_byte_comparison_stops_before_source_values(self):
        self.f.runs["baseline"].update(process_exit=1, verdict="REFUSED")
        self.f.publish_receipts()
        with mock.patch.object(
            E.C, "compare_source_expectation", side_effect=AssertionError("source values called")
        ):
            checked = self.outcome("failed", "comparison")
        self.assertIsNone(checked.source_image)
        self.assertIsNone(checked.source_values)

    def test_unsupported_byte_comparison_stops_before_source_values(self):
        base = deepcopy(self.f.base)
        base["cross_model"] = False
        self.repin("expectation", P.PC.encode(base))
        with mock.patch.object(
            E.C, "compare_source_expectation", side_effect=AssertionError("source values called")
        ):
            checked = self.outcome("unsupported", "comparison")
        self.assertIsNone(checked.source_values)

    def test_image_mismatch_stops_before_source_values(self):
        image = bytearray(self.f.image)
        image[-1] ^= 1
        self.repin("guest-image", bytes(image))
        with mock.patch.object(
            E.C, "compare_source_expectation", side_effect=AssertionError("source values called")
        ):
            checked = self.outcome("refused", "source/image")
        self.assertEqual(checked.comparison.disposition, "satisfied")
        self.assertIsNone(checked.source_values)

    def test_later_file_changes_do_not_replace_any_retained_snapshot(self):
        reading = E.Q.read_declared_files

        def read(*args, **kwargs):
            result = reading(*args, **kwargs)
            for fact in result.files:
                if fact.data is not None:
                    (self.f.root / fact.path).write_bytes(b"changed after authentication")
            return result

        with mock.patch.object(E.Q, "read_declared_files", side_effect=read):
            checked = self.outcome()
        self.assertEqual(checked.source_values.disposition, "matched")
        self.assertEqual(checked.source_values.facts.witness_value, 1)
        self.outcome("stale")

    def test_selected_program_budget_and_witness_freeze_before_artifact_io(self):
        self.mixed()
        reading = E.M.read_dependency_manifest

        def read(*args, **kwargs):
            result = reading(*args, **kwargs)
            parent = kwargs["experiment"]
            parent["program"] = "changed.s"
            parent["instructions"] = 1
            parent["verification"]["property"][0]["gpr_witness"] = dict(step_n=0, register="x31")
            return result

        with mock.patch.object(E.M, "read_dependency_manifest", side_effect=read):
            checked = self.outcome()
        self.assertEqual(
            (
                checked.source_values.facts.derivation.program,
                checked.source_values.facts.derivation.instructions,
            ),
            (self.f.experiment["program"], 2),
        )
        self.assertEqual(checked.source_values.facts.witness, E.C.GprWitness(1, "x1"))

    def test_no_extra_artifact_reads_after_file_set_authentication(self):
        reading = E.Q.read_declared_files
        with (
            mock.patch.object(E.A, "read_snapshot", wraps=E.A.read_snapshot) as snapshots,
            mock.patch.object(E.A, "read_bounded_pin", wraps=E.A.read_bounded_pin) as pins,
        ):

            def read(*args, **kwargs):
                result = reading(*args, **kwargs)
                snapshots.side_effect = AssertionError("artifact reopened")
                pins.side_effect = AssertionError("artifact reopened")
                return result

            with mock.patch.object(E.Q, "read_declared_files", side_effect=read):
                checked = self.outcome()
            paths = [
                call.args[2]["path"] for call in [*snapshots.call_args_list, *pins.call_args_list]
            ]
        self.assertEqual((len(paths), len(set(paths))), (22, 22))
        total = sum(path.stat().st_size for path in self.f.root.rglob("*") if path.is_file())
        self.assertEqual(
            (checked.authentication.authenticated_bytes, checked.authentication.charged_read_bytes),
            (total, total),
        )

    def test_author_unsupported_context_leaves_evaluation_pending_without_credit(self):
        self.f.entry += 2
        self.f.image = P.G.build_guest_image(
            self.f.source, program=self.f.experiment["program"], entry=self.f.entry
        ).image
        self.f.base["entry"] = self.f.control["entry"] = hex(self.f.entry)
        self.f.write(self.f.inputs["guest-image"], self.f.image)
        self.f.write(self.f.inputs["expectation"], P.PC.encode(self.f.base))
        self.f.write(self.f.inputs["mutant-expectation"], P.PC.encode(self.f.control))
        self.f.publish_receipts()
        checked = self.outcome(reason="no credit")
        self.assertEqual(checked.source_values.disposition, "unsupported")
        self.assertIsNone(checked.source_values.facts)
        self.assertEqual(checked.source_image.disposition, "matched")

    def test_known_source_failures_preserve_all_earlier_findings(self):
        for disposition in ("refused", "unavailable"):
            result = E.C.SourceExpectationCheck(disposition, "synthetic author limitation")
            with (
                self.subTest(disposition=disposition),
                mock.patch.object(E.C, "compare_source_expectation", return_value=result),
            ):
                checked = self.outcome(disposition, "source values")
                self.assertIs(checked.source_values, result)
                self.assertEqual(checked.authentication.disposition, "matched")
                self.assertEqual(
                    tuple(row.check.disposition for row in checked.receipts), ("matched",) * 3
                )
                self.assertEqual(checked.comparison.disposition, "satisfied")
                self.assertEqual(checked.source_image.disposition, "matched")

    def test_unknown_or_incomplete_source_result_refuses_without_retaining_it(self):
        good = self.outcome().source_values
        bad = [
            None,
            {"disposition": "matched"},
            replace(good, disposition="unknown"),
            replace(good, facts=None),
            replace(good, facts=replace(good.facts, derivation=None)),
            replace(good, disposition="unsupported"),
        ]
        for result in bad:
            with (
                self.subTest(result=type(result)),
                mock.patch.object(E.C, "compare_source_expectation", return_value=result),
            ):
                checked = self.outcome("refused", "source values")
                self.assertIsNone(checked.source_values)
                self.assertEqual(checked.source_image.disposition, "matched")

    def test_each_source_image_metadata_axis_is_independently_bound(self):
        good = self.outcome().source_values
        for name, value in [
            ("program", "wrong.s"),
            ("entry", 0),
            ("encoding_path", "wrong.sexp"),
            ("source_size", 0),
            ("source_sha256", "0" * 64),
            ("payload_size", 0),
            ("payload_sha256", "0" * 64),
        ]:
            changed = replace(
                good,
                facts=replace(
                    good.facts, derivation=replace(good.facts.derivation, **{name: value})
                ),
            )
            with (
                self.subTest(name=name),
                mock.patch.object(E.C, "compare_source_expectation", return_value=changed),
            ):
                checked = self.outcome("refused", "derivation differs from source/image context")
                self.assertIsNone(checked.source_values)

    def test_missing_independent_image_facts_refuse(self):
        checking = E.F.check_source_image

        def check(*args, **kwargs):
            return replace(checking(*args, **kwargs), facts=None)

        with mock.patch.object(E.F, "check_source_image", side_effect=check):
            checked = self.outcome("refused", "incomplete source/image binding facts")
        self.assertIsNone(checked.source_values)

    def test_result_and_source_facts_remain_frozen_and_payload_free(self):
        checked = self.outcome()
        for value, field in [
            (checked, "source_values"),
            (checked.source_values, "reason"),
            (checked.source_values.facts, "witness_value"),
        ]:
            with self.subTest(field=field), self.assertRaises(FrozenInstanceError):
                setattr(value, field, None)

    def test_unexpected_source_programming_failure_propagates(self):
        with (
            mock.patch.object(
                E.C,
                "compare_source_expectation",
                side_effect=RuntimeError("unexpected programming failure"),
            ),
            self.assertRaisesRegex(RuntimeError, "unexpected programming failure"),
        ):
            self.evaluate()


MUTATIONS = {
    "source-values-selection": ("source=source_bytes,", 'source=b"addi x1, x0, 9\\n",'),
    "baseline-values-selection": (
        'baseline_expectation=_payload(files, "input", execution.baseline_expectation.input_id),\n        instructions=execution.instructions, program=image_context.program,',
        'baseline_expectation=_payload(files, "input", execution.control_expectation.input_id),\n        instructions=execution.instructions, program=image_context.program,',
    ),
    "source-values-reopen": (
        "source=source_bytes,",
        "source=(root / source_input.path).read_bytes(),",
    ),
    "budget-forward": (
        "instructions=execution.instructions, program=image_context.program,",
        "instructions=1, program=image_context.program,",
    ),
    "witness-forward": (
        "witness=relations.plan.control_witness)\n    if (type(source_values)",
        'witness=C.GprWitness(0, "x31"))\n    if (type(source_values)',
    ),
    "program-forward": (
        "instructions=execution.instructions, program=image_context.program,",
        'instructions=execution.instructions, program="wrong.s",',
    ),
    "source-result-shape": (
        'if (type(source_values) is not C.SourceExpectationCheck\n            or source_values.disposition not in ("matched", "failed", "refused", "unavailable", "unsupported")\n            or (source_values.disposition not in ("matched", "failed") and source_values.facts is not None)):',
        "if False:",
    ),
    "source-binding-shape": (
        "if (type(source_values.facts) is not C.SourceExpectationFacts\n                or type(source_values.facts.derivation) is not C.Author.SnapshotDerivation\n                or type(source_image.facts) is not F.SourceImageFacts):",
        "if False:",
    ),
    "source-context-binding": (
        "if ((derived.program, derived.entry, derived.encoding_path, derived.source_size,\n             derived.source_sha256, derived.payload_size, derived.payload_sha256) !=\n                (image_facts.program, image_facts.entry, image_facts.encoding_path, image_facts.source_size,\n                 image_facts.source_sha256, image_facts.payload_size, image_facts.payload_sha256)):",
        "if False:",
    ),
    "source-status": (
        'if source_values.disposition in ("failed", "refused", "unavailable"):',
        "if False:",
    ),
    "unsupported-credit": (
        'if source_values.disposition in ("failed", "refused", "unavailable"):',
        'if source_values.disposition in ("failed", "refused", "unavailable", "unsupported"):',
    ),
    "source-finding": (
        "return replace(result, source_values=source_values)",
        "return replace(result, source_values=None)",
    ),
}


def main():
    global E
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        source = Path(E.__file__).read_text()
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("mutation seam is not singular")
        module = types.ModuleType("mutated_value_evaluation")
        module.__file__ = E.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), E.__file__, "exec"), module.__dict__)
        E = module
    result = unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(ValueEvaluationTests)
    )
    print(
        f"MATCHED-GPR-VALUE-EVALUATION: {result.testsRun} tests / {len(result.failures)} failures / "
        f"{len(result.errors)} errors; synthetic only"
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
