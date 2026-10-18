#!/usr/bin/env python3
"""Synthetic input-review controls; no canonical review or reference execution."""
from __future__ import annotations

import argparse
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock

import matched_gpr_input_review as T
import matched_gpr_evaluation as E
import matched_gpr_artifacts as F
import probe_matched_gpr_evaluation as P

ROOT = Path(__file__).resolve().parent.parent


def pins(count=10):
    return tuple(T.InputBinding("implementation", f"pin {i}", f"source/{i}.py", "a" * 64)
                 for i in range(count))


def review(inputs=None):
    return T.InputReview("synthetic", "unit", pins() if inputs is None else inputs)


class ReviewTests(unittest.TestCase):
    def freeze(self, value, **changes):
        selected = dict(profile_id="synthetic", experiment_id="unit"); selected.update(changes)
        return T.freeze_review(value, **selected)

    def refused(self, value, reason=None, **changes):
        try:
            self.freeze(value, **changes)
        except T.ReviewError as exc:
            if reason: self.assertIn(reason, str(exc))
        except (AttributeError, TypeError, ValueError, AssertionError) as exc:
            self.fail(f"malformed review escaped as {type(exc).__name__}: {exc}")
        else:
            self.fail("malformed review accepted")

    def test_order_and_existing_space_containing_child_ids_are_preserved(self):
        value = self.freeze(review(tuple(reversed(pins()))))
        checked = T.compare_inputs(value, pins())
        self.assertEqual(checked.disposition, "matched")
        self.assertEqual((checked.reviewed_count, checked.declared_count), (10, 10))
        self.assertEqual((checked.profile_id, checked.experiment_id), ("synthetic", "unit"))
        self.assertEqual((checked.missing_ids, checked.unreviewed_ids, checked.changed_ids), ((), (), ()))

    def test_missing_and_unreviewed_ids_have_separate_findings(self):
        value = self.freeze(review())
        missing = T.compare_inputs(value, pins()[:-1])
        self.assertEqual((missing.disposition, missing.missing_ids), ("refused", ("pin 9",)))
        self.assertEqual(missing.unreviewed_ids, ())
        extra = T.compare_inputs(value, pins() + (T.InputBinding("source", "extra", "source/extra.py", "a" * 64),))
        self.assertEqual((extra.disposition, extra.unreviewed_ids), ("refused", ("extra",)))
        self.assertEqual(extra.missing_ids, ())
        renamed = T.compare_inputs(value, (replace(pins()[0], input_id="renamed"), *pins()[1:]))
        self.assertEqual((renamed.disposition, renamed.missing_ids, renamed.unreviewed_ids),
                         ("refused", ("pin 0",), ("renamed",)))

    def test_role_path_and_digest_changes_each_refuse(self):
        value = self.freeze(review())
        for change in [dict(role="configuration"), dict(path="source/other.py"), dict(sha256="b" * 64)]:
            with self.subTest(change=change):
                supplied = (replace(pins()[0], **change), *pins()[1:])
                checked = T.compare_inputs(value, supplied)
                self.assertEqual((checked.disposition, checked.changed_ids), ("refused", ("pin 0",)))
                self.assertEqual((checked.missing_ids, checked.unreviewed_ids), ((), ()))

    def test_profile_and_parent_are_bound_to_selected_authority(self):
        self.refused(replace(review(), profile_id="other"), "profile")
        self.refused(replace(review(), experiment_id="other"), "experiment")
        self.refused(review(), "selected", profile_id=False)
        self.refused(review(), "selected", experiment_id="")

    def test_plain_review_and_binding_types_and_incomplete_objects_refuse(self):
        class Subclass(T.InputReview): pass
        for value in [False, {}, Subclass("synthetic", "unit", pins()), object.__new__(T.InputReview)]:
            with self.subTest(value=type(value)): self.refused(value)
        for item in [False, {}, object.__new__(T.InputBinding)]:
            self.refused(review((item, *pins()[1:])))

    def test_binding_field_shapes_and_paths_are_checked(self):
        for change in [dict(role=""), dict(input_id=False), dict(input_id="x" * (T.TEXT_CHARS + 1)),
                       dict(path="../outside"), dict(path="/absolute"), dict(path="x" * 4097),
                       dict(sha256="A" * 64), dict(sha256="0" * 63), dict(sha256=False)]:
            with self.subTest(change=str(change)[:80]):
                self.refused(review((replace(pins()[0], **change), *pins()[1:])))

    def test_duplicate_ids_and_paths_refuse(self):
        self.refused(review((replace(pins()[0], input_id=pins()[1].input_id), *pins()[1:])), "ID")
        self.refused(review((replace(pins()[0], path=pins()[1].path), *pins()[1:])), "path")

    def test_count_bounds_and_plain_container_precede_members(self):
        for count in [9, 73]:
            self.assertEqual(len(self.freeze(review(pins(count))).inputs), count)
        for count in [0, 8, 74]: self.refused(review(pins(count)), "tuple")
        class TrapTuple(tuple):
            def __len__(self): raise AssertionError("subclass length inspected")
        for value in [list(pins()), TrapTuple(pins())]: self.refused(review(value), "tuple")
        self.refused(review((object(),) * 74), "tuple")

    def test_review_and_results_are_frozen_and_bindings_are_copied(self):
        source = review(); frozen = self.freeze(source)
        checked = T.compare_inputs(frozen, pins())
        for value, field in [(source, "inputs"), (frozen, "profile_id"), (checked, "reason")]:
            with self.subTest(field=field), self.assertRaises(FrozenInstanceError): setattr(value, field, ())
        # A failed immutability subtest can mutate its local objects under an omission.
        # Use fresh objects for the independent copy witness to avoid a cascade.
        source = review(); frozen = self.freeze(source)
        self.assertIsNot(frozen.inputs[0], source.inputs[0])
        object.__setattr__(source.inputs[0], "sha256", "b" * 64)
        self.assertEqual(frozen.inputs[0].sha256, "a" * 64)
        self.assertEqual(T.compare_inputs(frozen, pins()).disposition, "matched")

    def test_declared_inventory_has_the_same_strict_boundary(self):
        value = self.freeze(review())
        for supplied in [list(pins()), pins(8), pins(74),
                         (replace(pins()[0], path="../bad"), *pins()[1:])]:
            try: T.compare_inputs(value, supplied)
            except T.ReviewError: pass
            except (AttributeError, TypeError, ValueError, AssertionError) as exc:
                self.fail(f"declared inventory escaped as {type(exc).__name__}: {exc}")
            else: self.fail("malformed declared inventory accepted")

    def test_pure_binding_performs_no_file_or_process_operations(self):
        with mock.patch("builtins.open", side_effect=AssertionError("file I/O")), \
             mock.patch.object(Path, "open", side_effect=AssertionError("path I/O")), \
             mock.patch("subprocess.run", side_effect=AssertionError("process")):
            self.assertEqual(T.compare_inputs(self.freeze(review()), pins()).disposition, "matched")


class EvaluationReviewTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/p4-system-14/a42m/review-fixtures"; base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base); self.addCleanup(temporary.cleanup)
        self.f = P.Fixture(Path(temporary.name))
        values = [*self.f.inputs.values(), self.f.child]
        # Separate synthetic authority, saved before each test mutates declarations.
        self.review = T.InputReview("synthetic", self.f.experiment["id"], tuple(
            T.InputBinding(item["role"], item["id"], item["path"], item["sha256"]) for item in values))

    def outcome(self, disposition, **changes):
        args = self.f.arguments(); args["reviewed_inputs"] = self.review; args.update(changes)
        try: checked = E.evaluate_retained_unit(self.f.root, **args)
        except (AttributeError, KeyError, IndexError, TypeError, ValueError, OSError, AssertionError) as exc:
            self.fail(f"evaluation escaped as {type(exc).__name__}: {exc}")
        self.assertEqual(checked.disposition, disposition, checked.reason)
        return checked

    def manifest(self, children):
        row = self.f.inputs["dependency-manifest"]
        self.f.write(row, F.encode_dependencies(dict(format_version="matched-gpr-dependencies-v1", input=children), path=row["path"]))
        self.f.publish_receipts()
        # Refresh only the manifest's own pin to isolate leaf coverage controls.
        self.review = replace(self.review, inputs=tuple(replace(item, sha256=row["sha256"])
            if item.input_id == row["id"] else item for item in self.review.inputs))

    def test_positive_and_legacy_paths_remain_pending_and_payload_free(self):
        checked = self.outcome("pending")
        self.assertIsNotNone(checked.input_review)
        self.assertEqual(checked.input_review.disposition, "matched")
        self.assertEqual(checked.authentication.disposition, "matched")
        self.assertTrue(all(item.data is None for item in checked.authentication.files))
        self.assertIsNone(self.outcome("pending", reviewed_inputs=None).input_review)

    def test_unreviewed_extra_with_valid_pins_refuses_before_file_set_reads(self):
        extra = dict(id="extra", role="implementation", path="source/extra.py", sha256="a" * 64)
        self.f.write(extra, b"# valid pinned but unreviewed\n"); self.manifest([self.f.child, extra])
        self.assertEqual(self.outcome("pending", reviewed_inputs=None).authentication.disposition, "matched")
        with mock.patch.object(E.Q, "read_declared_files", side_effect=AssertionError("file set read")):
            checked = self.outcome("refused")
        self.assertIsNotNone(checked.input_review)
        self.assertEqual(checked.input_review.unreviewed_ids, ("extra",))
        self.assertIsNone(checked.authentication)

    def test_missing_required_child_with_other_valid_manifest_leaf_refuses(self):
        self.manifest([self.f.inputs["guest-source"]])
        self.assertEqual(self.outcome("pending", reviewed_inputs=None).authentication.disposition, "matched")
        checked = self.outcome("refused")
        self.assertIsNotNone(checked.input_review)
        self.assertEqual(checked.input_review.missing_ids, ("dependency",))

    def test_changed_child_role_with_valid_files_refuses(self):
        self.manifest([{**self.f.child, "role": "configuration"}])
        self.assertEqual(self.outcome("pending", reviewed_inputs=None).authentication.disposition, "matched")
        checked = self.outcome("refused")
        self.assertIsNotNone(checked.input_review)
        self.assertEqual(checked.input_review.changed_ids, ("dependency",))

    def test_invalid_authority_refuses_before_artifact_io(self):
        for value in [False, replace(self.review, experiment_id="other"), replace(self.review, profile_id="other")]:
            with self.subTest(value=type(value)), mock.patch.object(E.A, "read_snapshot", side_effect=AssertionError("artifact read")):
                self.assertEqual(self.outcome("refused", reviewed_inputs=value).record.disposition, "valid")

    def test_authority_and_its_bindings_freeze_before_first_artifact_read(self):
        original = self.review; reading = E.A.read_snapshot; changed = False
        def read(*args, **kwargs):
            nonlocal changed
            value = reading(*args, **kwargs)
            if not changed:
                changed = True
                object.__setattr__(original, "experiment_id", "changed")
                object.__setattr__(original.inputs[0], "sha256", "e" * 64)
            return value
        with mock.patch.object(E.A, "read_snapshot", side_effect=read): checked = self.outcome("pending")
        self.assertTrue(changed); self.assertIsNotNone(checked.input_review)
        self.assertEqual(checked.input_review.experiment_id, self.f.experiment["id"])

    def test_metadata_review_is_independent_of_later_file_staleness(self):
        (self.f.root / self.f.child["path"]).write_bytes(b"# changed after declarations\n")
        checked = self.outcome("stale")
        self.assertIsNotNone(checked.input_review)
        self.assertEqual(checked.input_review.disposition, "matched")
        self.assertIsNone(checked.comparison)

    def test_reviewed_inventory_does_not_turn_a_failed_process_into_success(self):
        self.f.runs["repeat"].update(process_exit=1, verdict="REFUSED"); self.f.publish_receipts()
        checked = self.outcome("failed")
        self.assertIsNotNone(checked.input_review)
        self.assertEqual(checked.input_review.disposition, "matched")
        self.assertEqual(checked.record.disposition, "valid")

    def test_manifest_failure_keeps_review_finding_absent(self):
        (self.f.root / self.f.inputs["dependency-manifest"]["path"]).unlink()
        checked = self.outcome("unavailable")
        self.assertIsNone(checked.input_review)


MUTATIONS = {
    "missing": ('missing = tuple(sorted(expected.keys() - actual.keys()))', 'missing = ()'),
    "unreviewed": ('unreviewed = tuple(sorted(actual.keys() - expected.keys()))', 'unreviewed = ()'),
    "changed": ('changed = tuple(sorted(key for key in expected.keys() & actual.keys() if expected[key] != actual[key]))', 'changed = ()'),
    "profile": ('_text(selected_profile) and selected_profile == profile_id', 'True'),
    "experiment": ('_text(selected_experiment) and selected_experiment == experiment_id', 'True'),
    "bindings-copy": ('result.append(InputBinding(role, rid, path, digest))', 'result.append(item)'),
    "input-bound": ('type(value) is tuple and MIN_INPUTS <= len(value) <= MAX_INPUTS', 'type(value) is tuple'),
    "input-type": ('type(value) is tuple and MIN_INPUTS <= len(value) <= MAX_INPUTS', 'MIN_INPUTS <= len(value) <= MAX_INPUTS'),
    "id-unique": ('_require(rid not in ids, "duplicate input ID")', '_require(True, "duplicate input ID")'),
    "path-unique": ('_require(path not in paths, "duplicate input path")', '_require(True, "duplicate input path")'),
    "result-frozen": ('@dataclass(frozen=True)\nclass InputReviewCheck:', '@dataclass\nclass InputReviewCheck:'),
    "review-frozen": ('@dataclass(frozen=True)\nclass InputReview:', '@dataclass\nclass InputReview:'),
    "declared-validation": ('supplied = _inputs(declared)', 'supplied = declared'),
    "plan-binding": ('if input_review.disposition != "matched":', 'if False:'),
    "review-freeze": ('T.freeze_review(reviewed_inputs, profile_id=scope.profile_id,\n                                          experiment_id=experiment["id"])', 'reviewed_inputs'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        global T, E
        before, after = MUTATIONS[args.mutation]
        target = E if args.mutation in ("plan-binding", "review-freeze") else T
        source = Path(target.__file__).read_text()
        if source.count(before) != 1: raise SystemExit("mutation seam is not singular")
        module = types.ModuleType("mutated_input_review_" + target.__name__); module.__file__ = target.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after), target.__file__, "exec"), module.__dict__)
        if target is T: T = module; E.T = module
        else: E = module
    suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(ReviewTests),
                               unittest.defaultTestLoader.loadTestsFromTestCase(EvaluationReviewTests)])
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"MATCHED-GPR-INPUT-REVIEW: {result.testsRun} tests / {len(result.failures)} failures / {len(result.errors)} errors; synthetic only")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__": raise SystemExit(main())
