#!/usr/bin/env python3
"""Authenticated author-review composition controls; no reference execution."""
from __future__ import annotations

import argparse
from dataclasses import fields, replace
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock

import matched_gpr_evaluation as E
import probe_matched_gpr_evaluation as P
import probe_matched_gpr_image_evaluation as PI
import probe_matched_gpr_impact as PH

ROOT = Path(__file__).resolve().parent.parent


class AuthorEvaluationTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/p4-system-14/a42s/fixtures"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.f = P.Fixture(Path(temporary.name))
        snapshot = E.U.Author.derive_snapshot(
            self.f.source, program=self.f.experiment["program"], instructions=1
        )
        old_child = self.f.root / self.f.child["path"]
        self.f.child.update(role="expected-author", path=snapshot.author_path)
        self.f.write(
            self.f.child, b"# opaque synthetic expected author; never executed\n"
        )
        old_child.unlink()
        self.publish_manifest()
        self.set_version("sha256:" + self.f.child["sha256"])
        inputs = tuple(
            E.U.E.InputBinding(item["role"], item["id"], item["path"], item["sha256"])
            for item in [*self.f.graph["input"], self.f.child]
        )
        self.review = E.U.ExpectedAuthorReview(
            E.T.InputReview("synthetic", self.f.experiment["id"], inputs),
            self.f.child["id"],
            snapshot.route,
        )
        self.scope = self.f.arguments()["scope"]

    def publish_manifest(self):
        self.f.write(
            self.f.inputs["dependency-manifest"],
            P.F.encode_dependencies(
                dict(
                    format_version="matched-gpr-dependencies-v1", input=[self.f.child]
                ),
                path=self.f.inputs["dependency-manifest"]["path"],
            ),
        )
        self.f.publish_receipts()

    def set_version(self, value):
        for producer in self.f.graph["producer"][1:]:
            producer["version"] = value

    def evaluate(self, **changes):
        args = self.f.arguments()
        args.update(scope=self.scope, author_review=self.review)
        args.update(changes)
        return E.evaluate_retained_unit(self.f.root, **args)

    def outcome(self, disposition="pending", reason=None, finding="matched", **changes):
        try:
            checked = self.evaluate(**changes)
        except (
            AttributeError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
            OSError,
            AssertionError,
        ) as exc:
            self.fail(f"author evaluation escaped as {type(exc).__name__}: {exc}")
        self.assertEqual(checked.disposition, disposition, checked.reason)
        if reason:
            self.assertIn(reason, checked.reason)
        if finding is None:
            self.assertIsNone(checked.expected_author)
        else:
            self.assertIsNotNone(
                checked.expected_author, "expected-author finding was dropped"
            )
            self.assertEqual(checked.expected_author.disposition, finding)
            self.assertIsNotNone(
                checked.input_review, "current inventory finding was dropped"
            )
        self.assertFalse(PI.has_payload(checked))
        self.assertFalse(hasattr(checked, "qualified"))
        return checked

    def test_positive_preserves_all_independent_findings_and_pending_status(self):
        checked = self.outcome(reason="complete method/policy adequacy pending")
        self.assertEqual(checked.input_review.disposition, "matched")
        self.assertEqual(checked.authentication.disposition, "matched")
        self.assertEqual(checked.identity.disposition, "matched")
        self.assertEqual(
            tuple(row.check.disposition for row in checked.receipts), ("matched",) * 3
        )
        self.assertEqual(checked.comparison.disposition, "satisfied")
        self.assertEqual(checked.source_image.disposition, "matched")
        self.assertEqual(checked.source_values.disposition, "matched")
        self.assertEqual(
            checked.expected_author.facts.author.sha256, self.f.child["sha256"]
        )

    def test_legacy_default_and_positional_fields_keep_meaning(self):
        checked = self.outcome(finding=None, author_review=None)
        self.assertIsNone(checked.input_review)
        self.assertEqual(checked.source_values.disposition, "matched")
        self.assertEqual(
            [field.name for field in fields(checked)][:12],
            [
                "disposition",
                "reason",
                "record",
                "manifest",
                "authentication",
                "identity",
                "receipts",
                "comparison",
                "source_image",
                "input_review",
                "impact",
                "source_values",
            ],
        )
        self.assertEqual(fields(checked)[12].name, "expected_author")

    def test_author_supplies_current_inventory_and_agrees_with_explicit_review(self):
        checked = self.outcome(
            reviewed_inputs=replace(
                self.review.inventory,
                inputs=tuple(reversed(self.review.inventory.inputs)),
            )
        )
        self.assertEqual(checked.input_review.reviewed_count, 10)

    def test_author_inventory_can_supply_the_current_impact_review(self):
        checked = self.outcome(impact_review=PH.authority(self.review.inventory))
        self.assertIsNotNone(checked.impact)
        self.assertEqual(checked.impact.disposition, "matched")

    def test_dual_review_disagreement_refuses_before_artifact_io(self):
        inputs = (
            *self.review.inventory.inputs[:-1],
            replace(self.review.inventory.inputs[-1], sha256="c" * 64),
        )
        with P.EvaluationTests.no_artifact(self):
            self.outcome(
                "refused",
                "author review differs",
                finding=None,
                reviewed_inputs=replace(self.review.inventory, inputs=inputs),
            )

    def test_malformed_author_review_refuses_before_artifact_io(self):
        for review in [
            {},
            replace(self.review, route="word"),
            replace(
                self.review,
                inventory=replace(self.review.inventory, profile_id="other"),
            ),
        ]:
            with self.subTest(kind=type(review)), P.EvaluationTests.no_artifact(self):
                self.outcome("refused", finding=None, author_review=review)

    def test_manifest_inventory_disagreement_refuses_before_file_set(self):
        changed = tuple(
            (
                replace(item, sha256="c" * 64)
                if item.input_id == self.f.child["id"]
                else item
            )
            for item in self.review.inventory.inputs
        )
        review = replace(
            self.review, inventory=replace(self.review.inventory, inputs=changed)
        )
        with mock.patch.object(
            E.Q, "read_declared_files", side_effect=AssertionError("file set")
        ):
            checked = self.outcome(
                "refused", "input review", finding=None, author_review=review
            )
        self.assertEqual(checked.input_review.changed_ids, (self.f.child["id"],))

    def test_unreviewed_version_refuses_after_values_and_keeps_findings(self):
        self.set_version("unreviewed-version")
        checked = self.outcome("refused", "version", finding="refused")
        self.assertEqual(checked.source_values.disposition, "matched")
        self.assertEqual(checked.source_image.disposition, "matched")
        self.assertEqual(checked.comparison.disposition, "satisfied")
        self.assertEqual(len(checked.receipts), 3)
        self.assertIsNone(checked.expected_author.facts)

    def test_binding_uses_exact_frozen_plan_scope_and_source_derivation_once(self):
        binding = E.U.bind_expected_author
        with mock.patch.object(E.U, "bind_expected_author", wraps=binding) as call:
            checked = self.outcome()
        self.assertEqual(call.call_count, 1)
        self.assertIs(call.call_args.kwargs["manifest"], checked.manifest.plan)
        self.assertIs(
            call.call_args.kwargs["derivation"], checked.source_values.facts.derivation
        )
        self.assertEqual(
            (
                call.call_args.kwargs["profile_id"],
                call.call_args.kwargs["experiment_id"],
            ),
            ("synthetic", self.f.experiment["id"]),
        )
        self.assertIsNot(call.call_args.args[0], self.review)

    def test_caller_authority_and_scope_changes_during_read_cannot_replace_selection(
        self,
    ):
        read = E.M.read_dependency_manifest

        def mutate(*args, **kwargs):
            result = read(*args, **kwargs)
            object.__setattr__(self.review, "route", "word")
            object.__setattr__(self.scope, "profile_id", "other")
            object.__setattr__(self.review.inventory.inputs[-1], "sha256", "c" * 64)
            return result

        with mock.patch.object(E.M, "read_dependency_manifest", side_effect=mutate):
            self.outcome()

    def test_artifact_files_are_authenticated_once_with_unchanged_budgets(self):
        with mock.patch.object(
            E.A, "read_snapshot", wraps=E.A.read_snapshot
        ) as snapshots, mock.patch.object(
            E.A, "read_bounded_pin", wraps=E.A.read_bounded_pin
        ) as pins:
            checked = self.outcome()
        paths = [
            call.args[2]["path"]
            for call in [*snapshots.call_args_list, *pins.call_args_list]
        ]
        self.assertEqual(len(paths), 22)
        self.assertEqual(len(set(paths)), 22)
        self.assertLessEqual(
            checked.authentication.charged_read_bytes, 128 * 1024 * 1024
        )
        self.assertLessEqual(checked.authentication.snapshot_bytes, 16 * 1024 * 1024)

    def test_stale_author_file_stops_before_binding(self):
        (self.f.root / self.f.child["path"]).write_bytes(b"changed author\n")
        with mock.patch.object(
            E.U, "bind_expected_author", side_effect=AssertionError("author called")
        ):
            self.outcome("stale", finding=None)

    def test_failed_source_values_stop_before_binding(self):
        good = self.outcome().source_values
        with mock.patch.object(
            E.C,
            "compare_source_expectation",
            return_value=replace(good, disposition="failed"),
        ), mock.patch.object(
            E.U, "bind_expected_author", side_effect=AssertionError("author called")
        ):
            checked = self.outcome("failed", "source values", finding=None)
        self.assertEqual(checked.source_values.disposition, "failed")

    def test_unsupported_source_stays_pending_without_author_credit(self):
        with mock.patch.object(
            E.C,
            "compare_source_expectation",
            return_value=E.C.SourceExpectationCheck(
                "unsupported", "synthetic source scope"
            ),
        ), mock.patch.object(
            E.U, "bind_expected_author", side_effect=AssertionError("author called")
        ):
            checked = self.outcome(
                reason="author binding not reached, no credit", finding=None
            )
        self.assertEqual(checked.source_values.disposition, "unsupported")

    def test_source_budget_contradiction_reaches_pure_owner_and_refuses(self):
        good = self.outcome().source_values
        for instructions in [True, 2]:
            with self.subTest(instructions=instructions), mock.patch.object(
                E.C,
                "compare_source_expectation",
                return_value=replace(
                    good,
                    facts=replace(
                        good.facts,
                        derivation=replace(
                            good.facts.derivation, instructions=instructions
                        ),
                    ),
                ),
            ):
                self.outcome("refused", "budget", finding="refused")

    def test_invalid_author_result_shapes_refuse_without_retaining_them(self):
        good = self.outcome().expected_author
        for result in [
            None,
            {},
            object.__new__(E.U.ExpectedAuthorCheck),
            replace(good, disposition="qualified"),
            replace(good, reason=None),
            replace(good, facts=None),
            replace(good, facts={}),
            replace(good, disposition="refused"),
        ]:
            with self.subTest(result=type(result)), mock.patch.object(
                E.U, "bind_expected_author", return_value=result
            ):
                checked = self.outcome("refused", "invalid result", finding=None)
                self.assertEqual(checked.source_values.disposition, "matched")

    def test_each_author_fact_axis_is_bound_to_frozen_selection(self):
        good = self.outcome().expected_author
        changes = [
            dict(author=replace(good.facts.author, sha256="c" * 64)),
            dict(source=replace(good.facts.source, path="source/wrong.s")),
            dict(manifest=replace(good.facts.manifest, input_id="wrong")),
            dict(version="wrong"),
            dict(route="word"),
            dict(instructions=2),
            dict(instructions=True),
            dict(author=None),
        ]
        for change in changes:
            result = replace(good, facts=replace(good.facts, **change))
            with self.subTest(change=change), mock.patch.object(
                E.U, "bind_expected_author", return_value=result
            ):
                checked = self.outcome("refused", "facts differ", finding=None)
                self.assertEqual(checked.source_values.disposition, "matched")

    def test_incomplete_author_facts_refuse_without_traceback(self):
        good = self.outcome().expected_author
        result = replace(good, facts=object.__new__(E.U.ExpectedAuthorFacts))
        with mock.patch.object(E.U, "bind_expected_author", return_value=result):
            self.outcome("refused", "facts differ", finding=None)

    def test_unexpected_author_programming_failure_propagates(self):
        with mock.patch.object(
            E.U, "bind_expected_author", side_effect=RuntimeError("programming failure")
        ), self.assertRaisesRegex(RuntimeError, "programming failure"):
            self.evaluate()


MUTATIONS = {
    "author-freeze": (
        'U.freeze_review(author_review, profile_id=scope.profile_id,\n                                          experiment_id=experiment["id"])',
        "author_review",
    ),
    "current-inventory": (
        "review_context = author_context.inventory",
        "review_context = None",
    ),
    "review-agreement": (
        "elif review_context != author_context.inventory:",
        "elif False:",
    ),
    "frozen-scope": (
        "profile_id=author_context.inventory.profile_id,",
        "profile_id=scope.profile_id,",
    ),
    "author-scope": (
        "experiment_id=author_context.inventory.experiment_id,\n            manifest=manifest.plan,",
        'experiment_id="wrong", manifest=manifest.plan,',
    ),
    "manifest-reopen": (
        "experiment_id=author_context.inventory.experiment_id,\n            manifest=manifest.plan,",
        "experiment_id=author_context.inventory.experiment_id, manifest=M.read_dependency_manifest(root, experiment=experiment, current_candidate=candidate).plan,",
    ),
    "derivation-selection": (
        "manifest=manifest.plan, derivation=source_values.facts.derivation)",
        "manifest=manifest.plan, derivation=replace(source_values.facts.derivation))",
    ),
    "author-order": (
        'if author_context is not None and source_values.disposition == "matched":',
        "if author_context is not None:",
    ),
    "author-result-shape": (
        '        if (type(expected_author) is not U.ExpectedAuthorCheck\n                or type(getattr(expected_author, "reason", None)) is not str\n                or author_disposition not in ("matched", "refused")\n                or (author_disposition == "refused" and author_facts is not None)\n                or (author_disposition == "matched" and type(author_facts) is not U.ExpectedAuthorFacts)):',
        "        if False:",
    ),
    "author-fact-binding": (
        '            if (any(type(item) is not U.E.InputBinding for item in metadata[:3])\n                    or type(metadata[3]) is not str or type(metadata[4]) is not str\n                    or type(metadata[5]) is not int\n                    or metadata != (selected_author, source_input, principals["dependency-manifest"],\n                                    relations.plan.expected_version, author_context.route, execution.instructions)):',
        "            if False:",
    ),
    "author-status": (
        '        else:\n            return finish("refused", "expected author: " + expected_author.reason,',
        '        elif False:\n            return finish("refused", "expected author: " + expected_author.reason,',
    ),
    "author-finding": (
        "result = replace(result, expected_author=expected_author)",
        "result = replace(result, expected_author=None)",
    ),
    "unsupported-credit": (
        'else "; author binding not reached, no credit")',
        'else "; reviewed author metadata binds")',
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
        module = types.ModuleType("mutated_author_evaluation")
        module.__file__ = E.__file__
        sys.modules[module.__name__] = module
        exec(
            compile(source.replace(before, after), E.__file__, "exec"), module.__dict__
        )
        E = module
    result = unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(AuthorEvaluationTests)
    )
    print(
        f"MATCHED-GPR-AUTHOR-EVALUATION: {result.testsRun} tests / {len(result.failures)} failures / "
        f"{len(result.errors)} errors; synthetic only"
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
