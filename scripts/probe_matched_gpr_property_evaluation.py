#!/usr/bin/env python3
"""Finite property composition controls authenticating the actual retained excerpt."""
from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import replace
import hashlib
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock

import matched_gpr_evaluation as E
import probe_matched_gpr_evaluation as B
import probe_matched_gpr_image_evaluation as BI
import probe_matched_gpr_property as P

ROOT = Path(__file__).resolve().parent.parent


class Fixture(B.Fixture):
    """Real tracked guest/expectation/excerpt data; synthetic observations, no process."""

    def __init__(self, root):
        super().__init__(root)
        known = P.fixture()
        self.authority = known.context.authority
        self.scope = E.V.Scope(
            "rv64gc-lab-v0",
            frozenset({"sail-riscv"}),
            frozenset({"REQ-GC-M"}),
            frozenset({"OB-GC-M"}),
        )
        self.experiment.update(program="m-div.s", instructions=27)
        self.graph["property"][0].update(
            id="signed-quotient",
            requirement_id="REQ-GC-M",
            obligation_ids=["OB-GC-M"],
            statement=P.STATEMENT,
            gpr_witness=dict(step_n=2, register="x7"),
        )
        self.graph["control_run"][0]["property_ids"] = ["signed-quotient"]
        for run in self.runs.values():
            run["argv"][4] = "27"
        self.source = (ROOT / "profiles/rv64gc-lab-v0/guests/m-div.s").read_bytes()
        self.image = B.G.build_guest_image(
            self.source, program="m-div.s", entry=self.entry
        ).image
        self.write(self.inputs["guest-source"], self.source)
        self.write(self.inputs["guest-image"], self.image)
        self.base = E.D.load_expectations(
            ROOT / "profiles/rv64gc-lab-v0/guests/m-div.expected.sexp"
        )
        self.control = deepcopy(self.base)
        self.control["step"][2]["writes"]["x7"] = "0xfffffffffffffffc"
        self.write(self.inputs["expectation"], B.PC.encode(self.base))
        self.write(self.inputs["mutant-expectation"], B.PC.encode(self.control))
        lines = []
        for step in known.values.facts.derivation.steps:
            lines.append(
                f"[{step.n}] [M]: 0x{step.pc:016x} (0x{step.instruction_bits:08x}) synthetic fixture"
            )
            lines.extend(
                f"x{register} <- 0x{value:016x}" for register, value in step.writes
            )
        self.trace = ("\n".join(lines) + "\n").encode()
        for kind in self.runs:
            self.write(self.observation(kind, "raw-gpr"), self.trace)
        old_child = self.root / self.child["path"]
        self.child.update(
            role="expected-author", path=known.values.facts.derivation.author_path
        )
        self.write(
            self.child, b"# synthetic expected-author identity; never executed\n"
        )
        old_child.unlink()
        required = E.G.signed_division_case().required_inputs[0]
        self.normative = dict(
            id=required.input_id,
            role=required.role,
            path=required.path,
            sha256=required.sha256,
        )
        self.install_retained_excerpt((ROOT / required.path).read_bytes())
        self.write(
            self.inputs["dependency-manifest"],
            B.F.encode_dependencies(
                dict(
                    format_version="matched-gpr-dependencies-v1",
                    input=[self.child, self.normative],
                ),
                path=self.inputs["dependency-manifest"]["path"],
            ),
        )
        for producer in self.graph["producer"][1:]:
            producer["version"] = "sha256:" + self.child["sha256"]
        self.publish_receipts()
        inventory = E.T.InputReview(
            "rv64gc-lab-v0",
            self.experiment["id"],
            tuple(
                E.T.InputBinding(item["role"], item["id"], item["path"], item["sha256"])
                for item in [*self.graph["input"], self.child, self.normative]
            ),
        )
        self.author_review = E.U.ExpectedAuthorReview(
            inventory, self.child["id"], "snapshot-parcels-v1"
        )

    def arguments(self):
        args = super().arguments()
        args.update(
            scope=self.scope,
            author_review=self.author_review,
            property_authority=self.authority,
        )
        return args

    def refresh_manifest_and_review(self):
        self.write(
            self.inputs["dependency-manifest"],
            B.F.encode_dependencies(
                dict(
                    format_version="matched-gpr-dependencies-v1",
                    input=[self.child, self.normative],
                ),
                path=self.inputs["dependency-manifest"]["path"],
            ),
        )
        self.publish_receipts()
        inventory = E.T.InputReview(
            "rv64gc-lab-v0",
            self.experiment["id"],
            tuple(
                E.T.InputBinding(item["role"], item["id"], item["path"], item["sha256"])
                for item in [*self.graph["input"], self.child, self.normative]
            ),
        )
        self.author_review = E.U.ExpectedAuthorReview(
            inventory, self.child["id"], "snapshot-parcels-v1"
        )

    def install_retained_excerpt(self, data):
        if (
            type(data) is not bytes
            or len(data) != 1576
            or hashlib.sha256(data).hexdigest() != self.normative["sha256"]
        ):
            raise ValueError("retained excerpt does not match reviewed bytes")
        path = self.root / self.normative["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


class PropertyEvaluationTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/p4-system-14/a42u/fixtures"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.f = Fixture(Path(temporary.name))

    def evaluate(self, **changes):
        args = self.f.arguments()
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
            self.fail(
                f"source-property evaluation escaped as {type(exc).__name__}: {exc}"
            )
        self.assertEqual(checked.disposition, disposition, checked.reason)
        if reason:
            self.assertIn(reason, checked.reason)
        if finding is None:
            self.assertIsNone(checked.source_property)
        else:
            self.assertIsNotNone(
                checked.source_property, "source-property finding was dropped"
            )
            self.assertEqual(checked.source_property.disposition, finding)
        self.assertFalse(BI.has_payload(checked))
        self.assertFalse(hasattr(checked, "qualified"))
        return checked

    def test_positive_composes_finite_property_with_all_prior_findings(self):
        checked = self.outcome()
        self.assertEqual(checked.record.disposition, "valid")
        self.assertEqual(checked.authentication.disposition, "matched")
        self.assertEqual(checked.comparison.disposition, "satisfied")
        self.assertEqual(checked.source_values.disposition, "matched")
        self.assertEqual(checked.expected_author.disposition, "matched")
        self.assertEqual(
            checked.source_property.facts.observed,
            (E.G.ObservedProperty("signed-quotient", E.G.C.GprWitness(2, "x7"), (1 << 64) - 3),),
        )
        self.assertFalse((self.f.root / ".materials").exists())
        pin = next(
            item.pin
            for item in checked.authentication.files
            if item.record_id == self.f.normative["id"]
        )
        self.assertEqual(
            (pin.disposition, pin.byte_size, pin.sha256),
            ("matched", 1576, self.f.normative["sha256"]),
        )

    def test_default_preserves_old_fields_and_appends_property_finding(self):
        checked = self.outcome(finding=None, property_authority=None)
        self.assertEqual(checked.expected_author.disposition, "matched")
        self.assertEqual(checked.source_values.disposition, "matched")
        self.assertEqual(
            list(checked.__dataclass_fields__)[-2:],
            ["expected_author", "source_property"],
        )

    def test_property_requires_author_review_before_artifact_io(self):
        with mock.patch.object(
            E.M, "read_dependency_manifest", side_effect=AssertionError("artifact I/O")
        ):
            checked = self.outcome(
                "refused",
                "requires expected author review",
                finding=None,
                author_review=None,
            )
        self.assertEqual(checked.record.disposition, "valid")

    def test_malformed_current_authority_refuses_before_artifact_io(self):
        for authority in [
            {},
            object.__new__(E.G.PropertyAuthority),
            replace(self.f.authority, profile_id="other"),
            replace(self.f.authority, requirement_semantic_sha256="A" * 64),
        ]:
            with self.subTest(kind=type(authority)), mock.patch.object(
                E.M,
                "read_dependency_manifest",
                side_effect=AssertionError("artifact I/O"),
            ):
                self.outcome("refused", finding=None, property_authority=authority)

    def test_actual_raw_property_statement_cannot_be_replaced_by_authority(self):
        self.f.graph["property"][0]["statement"] = "unrelated broad property"
        checked = self.outcome("refused", "property claim", finding="refused")
        self.assertEqual(checked.source_values.disposition, "matched")
        self.assertEqual(checked.expected_author.disposition, "matched")

    def test_obligation_count_is_bounded_before_copy_and_artifact_io(self):
        obligations = ["OB-GC-M", *[f"OB-extra-{n}" for n in range(64)]]
        self.f.graph["property"][0]["obligation_ids"] = obligations
        scope = replace(self.f.scope, obligation_ids=frozenset(obligations))
        mapped = E.D.references_to_doc
        selected = []

        def capture(*args, **kwargs):
            result = mapped(*args, **kwargs)
            selected.append(
                result["experiment"][0]["verification"]["property"][0]["obligation_ids"]
            )
            return result

        def bounded_tuple(value=()):
            if any(value is item for item in selected):
                raise AssertionError("unbounded obligations copied before count guard")
            return tuple(value)

        with mock.patch.object(
            E.D, "references_to_doc", side_effect=capture
        ), mock.patch.object(
            E, "tuple", side_effect=bounded_tuple, create=True
        ), mock.patch.object(
            E.M, "read_dependency_manifest", side_effect=AssertionError("artifact I/O")
        ):
            self.outcome("refused", "1..64", finding=None, scope=scope)

    def test_actual_raw_requirement_and_obligation_are_not_labels_to_replace(self):
        scope = replace(
            self.f.scope,
            requirement_ids=frozenset({"REQ-GC-M", "REQ-other"}),
            obligation_ids=frozenset({"OB-GC-M", "OB-other"}),
        )
        prop = self.f.graph["property"][0]
        for changes in [
            dict(requirement_id="REQ-other"),
            dict(obligation_ids=["OB-other"]),
        ]:
            with self.subTest(changes=changes):
                original = deepcopy(prop)
                prop.update(changes)
                try:
                    self.outcome(
                        "refused", "property claim", finding="refused", scope=scope
                    )
                finally:
                    prop.clear()
                    prop.update(original)

    def test_actual_parent_program_is_selected_before_artifact_io(self):
        self.f.experiment["program"] = "other.s"

        def freeze(context, **kwargs):
            self.assertEqual(context.program, "other.s")
            raise E.G.PropertyError("selected actual parent program")

        with mock.patch.object(
            E.G, "freeze_context", side_effect=freeze
        ), mock.patch.object(
            E.M, "read_dependency_manifest", side_effect=AssertionError("artifact I/O")
        ):
            self.outcome("refused", "selected actual parent program", finding=None)

    def test_context_and_authority_freeze_before_artifact_reads(self):
        mapping = E.D.references_to_doc
        read = E.M.read_dependency_manifest
        mapped = []

        def capture(*args, **kwargs):
            result = mapping(*args, **kwargs)
            mapped.append(result)
            return result

        def mutate(*args, **kwargs):
            result = read(*args, **kwargs)
            for document in mapped:
                prop = document["experiment"][0]["verification"]["property"][0]
                prop["statement"] = "changed after selection"
                prop["obligation_ids"][:] = ["OB-changed"]
            object.__setattr__(self.f.authority, "source_sha256", "a" * 64)
            object.__setattr__(self.f.scope, "profile_id", "changed")
            return result

        with mock.patch.object(
            E.D, "references_to_doc", side_effect=capture
        ), mock.patch.object(E.M, "read_dependency_manifest", side_effect=mutate):
            self.outcome()

    def test_pure_owner_receives_exact_selected_context_and_existing_findings_once(
        self,
    ):
        binding = E.G.bind_source_property
        with mock.patch.object(E.G, "bind_source_property", wraps=binding) as call:
            checked = self.outcome()
        self.assertEqual(call.call_count, 1)
        context = call.call_args.args[0]
        self.assertEqual(
            (context.profile_id, context.experiment_id, context.program),
            ("rv64gc-lab-v0", self.f.experiment["id"], "m-div.s"),
        )
        self.assertEqual(len(context.claims), 1)
        self.assertEqual(context.claims[0].statement, self.f.graph["property"][0]["statement"])
        self.assertEqual(context.claims[0].witness, E.G.C.GprWitness(2, "x7"))
        self.assertEqual(context.control_property_id, self.f.graph["control_run"][0]["property_ids"][0])
        self.assertIsNot(context.authority, self.f.authority)
        self.assertIs(call.call_args.kwargs["manifest"], checked.manifest.plan)
        self.assertIs(call.call_args.kwargs["source_values"], checked.source_values)

    def test_declared_set_is_read_once_including_actual_retained_excerpt(self):
        snapshots = []
        read = E.A.read_snapshot

        def track(root, kind, record, **kwargs):
            snapshots.append(record["path"])
            return read(root, kind, record, **kwargs)

        with mock.patch.object(
            E.A, "read_snapshot", side_effect=track
        ), mock.patch.object(
            E.A, "read_bounded_pin", wraps=E.A.read_bounded_pin
        ) as pins:
            checked = E.evaluate_retained_unit(self.f.root, **self.f.arguments())
        self.assertEqual(checked.disposition, "pending", checked.reason)
        paths = [*snapshots, *[call.args[2]["path"] for call in pins.call_args_list]]
        self.assertEqual((len(paths), len(set(paths))), (23, 23))
        self.assertEqual(paths.count(self.f.normative["path"]), 1)
        self.assertLessEqual(
            checked.authentication.charged_read_bytes, 128 * 1024 * 1024
        )
        self.assertLessEqual(checked.authentication.snapshot_bytes, 16 * 1024 * 1024)

    def test_failed_retained_pin_stops_before_property_binding(self):
        path = self.f.root / self.f.normative["path"]
        data = path.read_bytes()
        for damaged, expected in [(None, "unavailable"), (data + b"changed", "stale")]:
            if damaged is None:
                path.unlink()
            else:
                path.write_bytes(damaged)
            with self.subTest(expected=expected), mock.patch.object(
                E.G,
                "bind_source_property",
                side_effect=AssertionError("property called"),
            ):
                checked = E.evaluate_retained_unit(self.f.root, **self.f.arguments())
                self.assertEqual(checked.disposition, expected, checked.reason)
                self.assertIsNone(checked.source_property)
        path.write_bytes(data)

    def test_failed_values_and_refused_author_stop_before_property(self):
        good = self.outcome().source_values
        with mock.patch.object(
            E.C,
            "compare_source_expectation",
            return_value=replace(good, disposition="failed"),
        ), mock.patch.object(
            E.G, "bind_source_property", side_effect=AssertionError("property called")
        ):
            self.outcome("failed", "source values", finding=None)
        for producer in self.f.graph["producer"][1:]:
            producer["version"] = "unreviewed"
        with mock.patch.object(
            E.G, "bind_source_property", side_effect=AssertionError("property called")
        ):
            checked = self.outcome("refused", "expected author", finding=None)
        self.assertEqual(checked.source_values.disposition, "matched")

    def test_unsupported_source_stays_pending_without_property_credit(self):
        with mock.patch.object(
            E.C,
            "compare_source_expectation",
            return_value=E.C.SourceExpectationCheck(
                "unsupported", "synthetic source scope"
            ),
        ), mock.patch.object(
            E.G, "bind_source_property", side_effect=AssertionError("property called")
        ):
            self.outcome(
                reason="source property unsupported or not reached, no credit",
                finding=None,
            )

    def test_typed_unsupported_property_is_separate_pending_finding(self):
        finding = E.G.SourcePropertyCheck("unsupported", "synthetic future property")
        with mock.patch.object(E.G, "bind_source_property", return_value=finding):
            checked = self.outcome(
                reason="source property unsupported or not reached, no credit",
                finding="unsupported",
            )
        self.assertEqual(checked.expected_author.disposition, "matched")

    def test_current_semantic_change_refuses_but_keeps_prior_findings(self):
        authority = replace(self.f.authority, requirement_semantic_sha256="a" * 64)
        checked = self.outcome(
            "refused",
            "semantic authority",
            finding="refused",
            property_authority=authority,
        )
        self.assertEqual(checked.comparison.disposition, "satisfied")
        self.assertEqual(checked.source_image.disposition, "matched")
        self.assertEqual(checked.expected_author.disposition, "matched")

    def test_invalid_property_result_shapes_are_not_retained(self):
        good = self.outcome().source_property
        for result in [
            None,
            {},
            object.__new__(E.G.SourcePropertyCheck),
            replace(good, disposition="qualified"),
            replace(good, reason=None),
            replace(good, facts=None),
            replace(good, facts={}),
            replace(good, disposition="unsupported"),
        ]:
            with self.subTest(kind=type(result)), mock.patch.object(
                E.G, "bind_source_property", return_value=result
            ):
                checked = self.outcome("refused", "invalid result", finding=None)
                self.assertEqual(checked.expected_author.disposition, "matched")

    def test_each_finding_axis_is_bound_to_actual_selected_context(self):
        good = self.outcome().source_property
        observed = good.facts.observed[0]
        for changes in [
            dict(case=None),
            dict(case=replace(good.facts.case, coverage="wrong")),
            dict(case=replace(good.facts.case, control_property_id="wrong")),
            dict(observed=(replace(observed, property_id="wrong"),)),
            dict(observed=(replace(observed, witness=E.G.C.GprWitness(2, "x8")),)),
            dict(observed=()),
            dict(observed=(observed, observed)),
            dict(observed=[observed]),
            dict(source=replace(good.facts.source, sha256="a" * 64)),
            dict(observed=(replace(observed, value=1),)),
            dict(observed=(replace(observed, value=True),)),
            dict(authority_inputs=()),
            dict(
                authority_inputs=(
                    replace(good.facts.authority_inputs[0], path="other/source.html"),
                )
            ),
        ]:
            result = replace(good, facts=replace(good.facts, **changes))
            with self.subTest(changes=changes), mock.patch.object(
                E.G, "bind_source_property", return_value=result
            ):
                checked = self.outcome("refused", "facts differ", finding=None)
                self.assertEqual(checked.source_values.disposition, "matched")

    def test_incomplete_facts_case_and_nested_records_refuse_without_escape(self):
        good = self.outcome().source_property
        cases = [
            replace(good, facts=object.__new__(E.G.SourcePropertyFacts)),
            replace(
                good,
                facts=replace(
                    good.facts, case=object.__new__(E.G.ReviewedPropertyCase)
                ),
            ),
            replace(
                good,
                facts=replace(good.facts, source=object.__new__(E.G.E.InputBinding)),
            ),
        ]
        for result in cases:
            with self.subTest(kind=type(result.facts)), mock.patch.object(
                E.G, "bind_source_property", return_value=result
            ):
                self.outcome("refused", "facts differ", finding=None)

    def test_canned_match_cannot_replace_actual_raw_statement(self):
        good = self.outcome().source_property
        self.f.graph["property"][0]["statement"] = "unrelated property"
        with mock.patch.object(E.G, "bind_source_property", return_value=good):
            self.outcome("refused", "facts differ", finding=None)

    def test_canned_property_result_cannot_outrun_the_source_witness_value(self):
        good = self.outcome()
        values = replace(
            good.source_values,
            facts=replace(good.source_values.facts, witness_value=(1 << 64) - 4),
        )
        with mock.patch.object(
            E.C, "compare_source_expectation", return_value=values
        ), mock.patch.object(
            E.G, "bind_source_property", return_value=good.source_property
        ):
            checked = self.outcome("refused", "facts differ", finding=None)
        self.assertEqual(checked.source_values.facts.witness_value, (1 << 64) - 4)
        self.assertEqual(checked.expected_author.disposition, "matched")

    def test_declared_properties_beyond_the_reviewed_case_refuse(self):
        extra = deepcopy(self.f.graph["property"][0])
        extra.update(id="remainder", statement="the remainder takes the dividend's sign",
                     gpr_witness=dict(step_n=3, register="x8"))
        self.f.graph["property"].append(extra)
        checked = self.outcome("refused", "property claim", finding="refused")
        self.assertEqual(checked.source_values.disposition, "matched")
        self.f.graph["property"] = [self.f.graph["property"][0]] + [
            dict(extra, id=f"p{n}", gpr_witness=dict(step_n=n % 27, register=f"x{8 + n // 27}"))
            for n in range(64)
        ]
        self.outcome("refused", "relations: method requires 1..64 property", finding=None)

    def test_canned_authority_pin_must_belong_to_authenticated_manifest(self):
        good = self.outcome().source_property
        previous = self.f.root / self.f.normative["path"]
        self.f.normative["path"] = "source/relocated.html"
        relocated = self.f.root / self.f.normative["path"]
        relocated.parent.mkdir(parents=True, exist_ok=True)
        previous.rename(relocated)
        self.f.refresh_manifest_and_review()
        with mock.patch.object(E.G, "bind_source_property", return_value=good):
            self.outcome("refused", "facts differ", finding=None)

    def test_unexpected_property_programming_failure_propagates(self):
        with mock.patch.object(
            E.G, "bind_source_property", side_effect=RuntimeError("programming failure")
        ), self.assertRaisesRegex(RuntimeError, "programming failure"):
            self.evaluate()


MUTATIONS = {
    "author-prerequisite": (
        'if author_context is None:\n                raise ValueError("source property requires expected author review")',
        'if False:\n                raise ValueError("source property requires expected author review")',
    ),
    "obligation-bound": (
        "if type(obligations) is not list or not 1 <= len(obligations) <= 64:",
        "if False:",
    ),
    "actual-statement": (
        'selected_property["statement"],',
        "G.signed_division_case().control().statement,",
    ),
    "actual-requirement": (
        'selected_property["requirement_id"],',
        "G.signed_division_case().requirement_id,",
    ),
    "actual-obligations": (
        "tuple(obligations),",
        "G.signed_division_case().obligation_ids,",
    ),
    "actual-program": (
        'scope.profile_id, experiment["id"], program, tuple(claims),',
        'scope.profile_id, experiment["id"], "m-div.s", tuple(claims),',
    ),
    "property-order": (
        'if property_context is not None and source_values.disposition == "matched":',
        "if property_context is not None:",
    ),
    "property-finding": (
        "result = replace(result, source_property=source_property)",
        "result = replace(result, source_property=None)",
    ),
    "property-status": ('elif property_disposition == "refused":', "elif False:"),
    "unsupported-credit": (
        'else "; source property unsupported or not reached, no credit")',
        'else "; finite source property binds")',
    ),
    "context-freeze": (
        'G.freeze_context(G.PropertyContext(\n                scope.profile_id, experiment["id"], program, tuple(claims),\n                relations.plan.control_property_id, property_authority),\n                profile_id=scope.profile_id, experiment_id=experiment["id"])',
        'G.PropertyContext(\n                scope.profile_id, experiment["id"], program, tuple(claims),\n                relations.plan.control_property_id, property_authority)',
    ),
    "property-result-shape": (
        'property_context is not None and source_values.disposition == "matched"',
        "False",
    ),
    "property-fact-binding": ("if not property_bound:", "if False:"),
    "actual-context-binding": (
        "(property_context.profile_id, property_context.program, property_context.control_property_id,\n                            property_context.claims, property_context.authority)",
        "(case.profile_id, case.program, case.control_property_id,\n                            case.claims(), case.authority)",
    ),
    "control-value": (
        "or next(item.value for item in observed if item.property_id == control.property_id)\n                           != source_values.facts.witness_value",
        "or False",
    ),
}


def retained_excerpt_smoke():
    """Unmocked, cache-free authentication; observations remain synthetic."""
    base = ROOT / "target/p4-system-14/a42aa/retained-fixtures"
    base.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=base) as directory:
        try:
            f = Fixture(Path(directory))
        except OSError as exc:
            print("RETAINED EXCERPT SMOKE: UNAVAILABLE: " + str(exc))
            return 2
        except ValueError as exc:
            print("RETAINED EXCERPT SMOKE: REFUSED: " + str(exc))
            return 1
        checked = E.evaluate_retained_unit(f.root, **f.arguments())
        if (
            checked.disposition != "pending"
            or checked.source_property is None
            or checked.source_property.disposition != "matched"
        ):
            print("RETAINED EXCERPT SMOKE: FAILED: " + checked.reason)
            return 1
        print(
            "RETAINED EXCERPT SMOKE: pending / finite property matched / "
            + str(len(checked.authentication.files))
            + " authenticated files / "
            + hex(checked.source_property.facts.observed[0].value)
            + "; no capture credit"
        )
    return 0


def main():
    global E
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    parser.add_argument("--retained-excerpt-smoke", action="store_true")
    args = parser.parse_args()
    if args.retained_excerpt_smoke:
        if args.mutation:
            parser.error("real smoke cannot use a mutation")
        return retained_excerpt_smoke()
    if args.mutation:
        source = Path(E.__file__).read_text()
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("property-evaluation mutation seam is not singular")
        module = types.ModuleType("mutated_property_evaluation")
        module.__file__ = E.__file__
        sys.modules[module.__name__] = module
        exec(
            compile(source.replace(before, after), E.__file__, "exec"), module.__dict__
        )
        E = module
    result = unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(PropertyEvaluationTests)
    )
    print(
        f"MATCHED-GPR-PROPERTY-EVALUATION: {result.testsRun} tests / {len(result.failures)} failures / "
        f"{len(result.errors)} errors; actual retained excerpt, synthetic observations, no capture credit"
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
