#!/usr/bin/env python3
"""Synthetic reviewed-author metadata controls; no capture or qualification."""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from dataclasses import FrozenInstanceError, replace
import hashlib
from pathlib import Path
import sys
import types
import unittest
from unittest import mock

import matched_gpr_expected_author as A
import probe_matched_gpr_execution as P


class ExpectedAuthorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = b"addi x1, x0, 1\n"
        cls.snapshot = A.Author.derive_snapshot(
            cls.source, program="unit.s", instructions=1
        )

    def setUp(self):
        experiment, candidate = P.fixture()
        graph = experiment["verification"]
        for item in graph["input"]:
            if item["role"] == "guest-source":
                item["sha256"] = hashlib.sha256(self.source).hexdigest()
        self.author = A.E.InputBinding(
            "expected-author", "author leaf", self.snapshot.author_path, "b" * 64
        )
        for producer in graph["producer"][1:]:
            producer["version"] = "sha256:" + self.author.sha256
        result = A.R.bind_relations(experiment, candidate)
        self.assertEqual(result.disposition, "matched", result)
        execution = result.plan.execution
        inputs = (
            *execution.common_inputs,
            execution.baseline_expectation,
            execution.control_expectation,
            self.author,
        )
        self.manifest = A.M.ManifestPlan(
            result.plan, "dependency-manifest", inputs, (self.author.input_id,)
        )
        self.review = A.ExpectedAuthorReview(
            A.T.InputReview("synthetic", "unit", inputs),
            self.author.input_id,
            "snapshot-parcels-v1",
        )
        self.derivation = self.snapshot

    def freeze(self, review=None, **scope):
        args = dict(profile_id="synthetic", experiment_id="unit")
        args.update(scope)
        return A.freeze_review(self.review if review is None else review, **args)

    def freeze_refuses(self, review, **scope):
        try:
            self.freeze(review, **scope)
        except A.AuthorReviewError:
            pass
        except (AttributeError, TypeError, ValueError, AssertionError) as exc:
            self.fail(f"authority escaped as {type(exc).__name__}: {exc}")
        else:
            self.fail("malformed authority accepted")

    def outcome(self, disposition="matched", reason=None, **changes):
        args = dict(
            profile_id="synthetic",
            experiment_id="unit",
            manifest=self.manifest,
            derivation=self.derivation,
        )
        args.update(changes)
        try:
            checked = A.bind_expected_author(self.review, **args)
        except (
            AttributeError,
            KeyError,
            TypeError,
            ValueError,
            AssertionError,
            OSError,
        ) as exc:
            self.fail(f"author binding escaped as {type(exc).__name__}: {exc}")
        self.assertEqual(checked.disposition, disposition, checked.reason)
        if reason:
            self.assertIn(reason, checked.reason)
        if disposition == "refused":
            self.assertIsNone(checked.facts)
        else:
            self.assertIsNotNone(checked.facts, "selected author finding was dropped")
        return checked

    def test_positive_carries_selected_frozen_metadata_without_credit(self):
        checked = self.outcome()
        self.assertEqual(checked.facts.author, self.author)
        self.assertEqual(checked.facts.source.role, "guest-source")
        self.assertEqual(checked.facts.manifest.input_id, "dependency-manifest")
        self.assertEqual(
            (checked.facts.version, checked.facts.route, checked.facts.instructions),
            ("sha256:" + "b" * 64, "snapshot-parcels-v1", 1),
        )
        self.assertIn("authentication/attestation pending", checked.reason)
        self.assertFalse(hasattr(checked, "qualified"))

    def test_input_order_is_irrelevant(self):
        expected = self.outcome()
        self.review = replace(
            self.review,
            inventory=replace(
                self.review.inventory,
                inputs=tuple(reversed(self.review.inventory.inputs)),
            ),
        )
        self.manifest = replace(
            self.manifest, inputs=tuple(reversed(self.manifest.inputs))
        )
        self.assertEqual(self.outcome(), expected)

    def test_plain_review_and_inventory_types_refuse(self):
        class Subclass(A.ExpectedAuthorReview):
            pass

        for value in [
            False,
            {},
            object.__new__(A.ExpectedAuthorReview),
            Subclass(self.review.inventory, self.author.input_id, self.review.route),
            replace(self.review, inventory={}),
        ]:
            with self.subTest(kind=type(value)):
                self.freeze_refuses(value)

    def test_selected_scope_is_not_taken_from_review(self):
        for scope in [
            dict(profile_id="other"),
            dict(experiment_id="other"),
            dict(profile_id=False),
            dict(experiment_id=""),
        ]:
            with self.subTest(scope=scope):
                self.freeze_refuses(self.review, **scope)
                self.outcome("refused", **scope)

    def test_invalid_author_id_and_route_refuse(self):
        for changes in [
            dict(author_input_id=False),
            dict(author_input_id=""),
            dict(author_input_id="x" * (A.T.TEXT_CHARS + 1)),
            dict(author_input_id="not selected"),
            dict(route=False),
            dict(route="snapshot-parcels-v1\n"),
            dict(route="word"),
        ]:
            with self.subTest(changes=str(changes)[:80]):
                self.freeze_refuses(replace(self.review, **changes))

    def test_author_selection_requires_exactly_one_expected_author_role(self):
        for inputs in [
            tuple(
                replace(item, role="implementation") if item == self.author else item
                for item in self.review.inventory.inputs
            ),
            (
                *self.review.inventory.inputs,
                A.E.InputBinding(
                    "expected-author", "second", "source/second.py", "c" * 64
                ),
            ),
        ]:
            with self.subTest(count=len(inputs)):
                self.freeze_refuses(
                    replace(
                        self.review,
                        inventory=replace(self.review.inventory, inputs=inputs),
                    )
                )

    def test_inventory_shape_duplicates_paths_and_hashes_use_existing_owner(self):
        original = self.review.inventory.inputs
        malformed = [
            list(original),
            original[:8],
            (object(),) * 74,
            (*original[:-1], replace(self.author, path="../outside")),
            (*original[:-1], replace(self.author, sha256="B" * 64)),
            (*original, self.author),
        ]
        for inputs in malformed:
            with self.subTest(count=len(inputs)):
                self.freeze_refuses(
                    replace(
                        self.review,
                        inventory=replace(self.review.inventory, inputs=inputs),
                    )
                )

    def test_freeze_copies_every_caller_binding_before_future_io(self):
        frozen = self.freeze()
        original = next(
            item for item in self.review.inventory.inputs if item == self.author
        )
        copied = next(
            item
            for item in frozen.inventory.inputs
            if item.input_id == original.input_id
        )
        self.assertIsNot(frozen.inventory, self.review.inventory)
        self.assertIsNot(copied, original)
        object.__setattr__(original, "sha256", "c" * 64)
        self.assertEqual(copied.sha256, "b" * 64)

    def test_direct_binding_revalidates_authority(self):
        self.review = replace(self.review, route="word")
        self.outcome("refused", "route")

    def test_complete_inventory_coverage_is_required(self):
        original = self.manifest
        for inputs in [
            original.inputs[:-1],
            (
                *original.inputs,
                A.E.InputBinding(
                    "implementation", "extra", "source/extra.py", "c" * 64
                ),
            ),
            (*original.inputs[:-1], replace(self.author, role="implementation")),
            (*original.inputs[:-1], replace(self.author, path="source/other.py")),
            (*original.inputs[:-1], replace(self.author, sha256="c" * 64)),
        ]:
            with self.subTest(count=len(inputs)):
                self.outcome(
                    "refused", "inventory", manifest=replace(original, inputs=inputs)
                )

    def test_author_must_be_a_bounded_flat_child(self):
        for children in [
            (),
            [self.author.input_id],
            ("other",),
            (self.author.input_id,) * 65,
        ]:
            with self.subTest(children=str(children)[:60]):
                self.outcome(
                    "refused",
                    "flat manifest child",
                    manifest=replace(self.manifest, child_input_ids=children),
                )

    def test_source_manifest_and_author_cannot_change_principal_identity(self):
        original = self.manifest.relations.execution
        for common in [
            original.common_inputs[:-1],
            tuple(
                replace(item, sha256="c" * 64) if item.role == "guest-source" else item
                for item in original.common_inputs
            ),
            tuple(
                (
                    replace(item, sha256="c" * 64)
                    if item.role == "dependency-manifest"
                    else item
                )
                for item in original.common_inputs
            ),
        ]:
            with self.subTest(count=len(common)):
                execution = replace(original, common_inputs=common)
                manifest = replace(
                    self.manifest,
                    relations=replace(self.manifest.relations, execution=execution),
                )
                self.outcome("refused", manifest=manifest)
        self.outcome(
            "refused",
            "identities",
            manifest=replace(self.manifest, manifest_input_id="wrong"),
        )

    def test_expected_version_requires_reviewed_digest_with_explicit_prefix(self):
        for version in [
            "source-derivation-v1",
            "b" * 64,
            "sha256:" + "c" * 64,
            "sha256:" + "b" * 64 + "\n",
        ]:
            with self.subTest(version=version):
                manifest = replace(
                    self.manifest,
                    relations=replace(
                        self.manifest.relations, expected_version=version
                    ),
                )
                self.outcome("refused", "version", manifest=manifest)

    def test_both_source_and_manifest_must_be_declared_consumed(self):
        original = self.manifest.relations.derivation_common_input_ids
        for removed in ["guest-source", "dependency-manifest"]:
            with self.subTest(removed=removed):
                relation = replace(
                    self.manifest.relations,
                    derivation_common_input_ids=tuple(
                        rid for rid in original if rid != removed
                    ),
                )
                self.outcome(
                    "refused",
                    "consume",
                    manifest=replace(self.manifest, relations=relation),
                )

    def test_snapshot_path_and_route_must_match_review(self):
        for changes in [
            dict(author_path="scripts/other.py"),
            dict(route="word"),
            dict(route=False),
        ]:
            with self.subTest(changes=changes):
                self.outcome(
                    "refused",
                    "path/route",
                    derivation=replace(self.derivation, **changes),
                )

    def test_snapshot_source_hash_must_match_selected_source(self):
        self.outcome(
            "refused",
            "source",
            derivation=replace(self.derivation, source_sha256="c" * 64),
        )

    def test_snapshot_budget_is_exact_plain_integer(self):
        for instructions in [False, 2, 0, 4097]:
            with self.subTest(instructions=instructions):
                self.outcome(
                    "refused",
                    "budget",
                    derivation=replace(self.derivation, instructions=instructions),
                )

    def test_public_plan_shapes_refuse_without_tracebacks(self):
        for manifest in [
            None,
            {},
            object.__new__(A.M.ManifestPlan),
            replace(self.manifest, relations=None),
            replace(
                self.manifest,
                relations=replace(self.manifest.relations, execution=None),
            ),
        ]:
            with self.subTest(manifest=type(manifest)):
                self.outcome("refused", manifest=manifest)
        for snapshot in [None, {}, object.__new__(A.Author.SnapshotDerivation)]:
            with self.subTest(snapshot=type(snapshot)):
                self.outcome("refused", derivation=snapshot)

    def test_freeze_check_and_facts_are_frozen_and_not_aliases(self):
        checked = self.outcome()
        for value, field in [
            (self.freeze(), "route"),
            (checked, "reason"),
            (checked.facts, "version"),
        ]:
            with self.subTest(field=field), self.assertRaises(FrozenInstanceError):
                setattr(value, field, None)
        for role in ["expected-author", "guest-source", "dependency-manifest"]:
            with self.subTest(role=role):
                checked = self.outcome()
                original = next(
                    item for item in self.review.inventory.inputs if item.role == role
                )
                fact = {
                    "expected-author": checked.facts.author,
                    "guest-source": checked.facts.source,
                    "dependency-manifest": checked.facts.manifest,
                }[role]
                digest = fact.sha256
                self.assertIsNot(fact, original)
                object.__setattr__(original, "sha256", "c" * 64)
                self.assertEqual(fact.sha256, digest)
                object.__setattr__(original, "sha256", digest)

    def test_pure_binding_never_opens_artifacts_or_starts_processes(self):
        with ExitStack() as stack:
            for name in [
                "builtins.open",
                "pathlib.Path.open",
                "os.open",
                "subprocess.run",
                "subprocess.Popen",
            ]:
                stack.enter_context(
                    mock.patch(name, side_effect=AssertionError("unexpected I/O"))
                )
            self.outcome()

    def test_unexpected_programming_failure_propagates(self):
        with mock.patch.object(
            A.T, "compare_inputs", side_effect=RuntimeError("programming failure")
        ), self.assertRaisesRegex(RuntimeError, "programming failure"):
            A.bind_expected_author(
                self.review,
                profile_id="synthetic",
                experiment_id="unit",
                manifest=self.manifest,
                derivation=self.derivation,
            )


MUTATIONS = {
    "authority-shape": (
        "_require(type(review) is ExpectedAuthorReview,",
        "_require(True,",
    ),
    "authority-scope": (
        "                                    profile_id=profile_id, experiment_id=experiment_id)",
        "                                    profile_id=review.inventory.profile_id, experiment_id=review.inventory.experiment_id)",
    ),
    "authority-copy": (
        "return ExpectedAuthorReview(inventory, selected, route)",
        "return review",
    ),
    "author-selection": (
        "len(authors) == 1 and authors[0].input_id == selected,",
        "True,",
    ),
    "review-route": ("type(route) is str and route == SNAPSHOT_ROUTE,", "True,"),
    "inventory-binding": ('coverage.disposition == "matched",', "True,"),
    "child-membership": ("and author.input_id in manifest.child_input_ids,", ","),
    "principal-binding": (
        "source in frozen.inventory.inputs and dependency in frozen.inventory.inputs\n                 and author not in execution.common_inputs\n                 and manifest.manifest_input_id == dependency.input_id,",
        "True,",
    ),
    "producer-version": (
        'relations.expected_version == "sha256:" + author.sha256,',
        "True,",
    ),
    "source-consumption": (
        "and source.input_id in consumed and dependency.input_id in consumed,",
        "and dependency.input_id in consumed,",
    ),
    "manifest-consumption": (
        "and source.input_id in consumed and dependency.input_id in consumed,",
        "and source.input_id in consumed,",
    ),
    "snapshot-author": (
        "derivation.author_path == author.path and derivation.route == frozen.route,",
        "True,",
    ),
    "snapshot-source": ("derivation.source_sha256 == source.sha256,", "True,"),
    "snapshot-budget": (
        "type(execution.instructions) is int and 1 <= execution.instructions <= 4096\n                 and type(derivation.instructions) is int\n                 and derivation.instructions == execution.instructions,",
        "True,",
    ),
    "frozen-results": ("@dataclass(frozen=True)", "@dataclass(frozen=False)"),
    "metadata-finding": (
        '"expected author metadata binds; authentication/attestation pending", facts)',
        '"expected author metadata binds; authentication/attestation pending", None)',
    ),
}


def main():
    global A
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        source = Path(A.__file__).read_text()
        before, after = MUTATIONS[args.mutation]
        count = 3 if args.mutation == "frozen-results" else 1
        if source.count(before) != count:
            raise RuntimeError(
                "mutation seam is not singular or the declared three dataclasses"
            )
        module = types.ModuleType("mutated_expected_author")
        module.__file__ = A.__file__
        sys.modules[module.__name__] = module
        exec(
            compile(source.replace(before, after), A.__file__, "exec"), module.__dict__
        )
        A = module
    result = unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(ExpectedAuthorTests)
    )
    print(
        f"MATCHED-GPR-EXPECTED-AUTHOR: {result.testsRun} tests / {len(result.failures)} failures / "
        f"{len(result.errors)} errors; synthetic only"
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
