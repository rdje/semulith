#!/usr/bin/env python3
"""Finite signed-DIV property controls; synthetic metadata, no capture credit."""
from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from types import SimpleNamespace
import sys
import types
import unittest
from unittest import mock

import dossier_sexp as D
import experiment_verification as V
import matched_gpr_property as G
import probe_matched_gpr_execution as P
import records_sexp as Records

ROOT = Path(__file__).resolve().parent.parent
STATEMENT = (
    "For signed DIV with x5 = -7 and x6 = 2, the x7 change at boundary 2 "
    "is -3 (rounding toward zero)."
)


def fixture():
    """Construct public-owner facts, not authenticated artifact or process evidence."""
    requirement = next(
        r
        for r in Records.load(ROOT / "profiles/rv64gc-lab-v0/requirements.sexp")
        if r["id"] == "REQ-GC-M"
    )
    obligation = next(
        r
        for r in Records.load(ROOT / "profiles/rv64gc-lab-v0/contract-obligations.sexp")
        if r["id"] == "OB-GC-M"
    )
    source = next(
        r
        for r in D.load_sources(ROOT / "profiles/rv64gc-lab-v0/sources.sexp")["source"]
        if r["id"] == "RVI-M"
    )
    authority = G.project_authority(
        "rv64gc-lab-v0", requirement=requirement, obligation=obligation, source=source
    )
    values = G.C.compare_source_expectation(
        source=(ROOT / "profiles/rv64gc-lab-v0/guests/m-div.s").read_bytes(),
        baseline_expectation=(
            ROOT / "profiles/rv64gc-lab-v0/guests/m-div.expected.sexp"
        ).read_bytes(),
        program="m-div.s",
        instructions=27,
        witness=G.C.GprWitness(2, "x7"),
    )
    if values.disposition != "matched":
        raise RuntimeError(
            "canonical signed-DIV source fixture no longer matches: " + values.reason
        )
    experiment, candidate = P.fixture()
    experiment.update(program="m-div.s", instructions=27)
    graph = experiment["verification"]
    prop = graph["property"][0]
    prop.update(
        requirement_id="REQ-GC-M",
        obligation_ids=["OB-GC-M"],
        statement=STATEMENT,
        gpr_witness=dict(step_n=2, register="x7"),
    )
    for run in graph["run"]:
        run["argv"][4] = "27"
    for item in graph["input"]:
        if item["role"] == "guest-source":
            item["sha256"] = values.facts.derivation.source_sha256
        if item["role"] == "expectation":
            item["sha256"] = values.facts.expectation_sha256
    relations = G.R.bind_relations(experiment, candidate)
    if relations.disposition != "matched":
        raise RuntimeError(
            "canonical property metadata fixture refuses: " + relations.reason
        )
    execution = relations.plan.execution
    normative = G.E.InputBinding(
        "normative-source",
        "RVI-M-DIV-STATEMENT",
        "profiles/rv64gc-lab-v0/retained/div-statement.html",
        "bbe3ff9dd6d8e1b452589669cd676d998265327eeaf8ed370bb95fcf15af1a58",
    )
    manifest = G.M.ManifestPlan(
        relations.plan,
        "dependency-manifest",
        (
            *execution.common_inputs,
            execution.baseline_expectation,
            execution.control_expectation,
            normative,
        ),
        (normative.input_id,),
    )
    context = G.PropertyContext(
        "rv64gc-lab-v0",
        experiment["id"],
        "m-div.s",
        prop["id"],
        "REQ-GC-M",
        ("OB-GC-M",),
        STATEMENT,
        G.C.GprWitness(2, "x7"),
        authority,
    )
    return SimpleNamespace(
        context=context,
        manifest=manifest,
        values=values,
        requirement=requirement,
        obligation=obligation,
        source=source,
        experiment=experiment,
        candidate=candidate,
    )


class PropertyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = fixture()

    def setUp(self):
        self.f = deepcopy(self.template)

    def project(self, **changes):
        args = dict(
            requirement=self.f.requirement,
            obligation=self.f.obligation,
            source=self.f.source,
        )
        args.update(changes)
        return G.project_authority("rv64gc-lab-v0", **args)

    def freeze(self, context=None, **scope):
        args = dict(
            profile_id="rv64gc-lab-v0", experiment_id=self.f.context.experiment_id
        )
        args.update(scope)
        return G.freeze_context(self.f.context if context is None else context, **args)

    def refuses(self, call):
        try:
            call()
        except G.PropertyError:
            pass
        except (
            AttributeError,
            KeyError,
            TypeError,
            ValueError,
            AssertionError,
            RecursionError,
        ) as exc:
            self.fail(f"bounded property input escaped as {type(exc).__name__}: {exc}")
        else:
            self.fail("invalid property authority/context accepted")

    def outcome(self, disposition="matched", reason=None, **changes):
        args = dict(
            profile_id="rv64gc-lab-v0",
            experiment_id=self.f.context.experiment_id,
            manifest=self.f.manifest,
            source_values=self.f.values,
        )
        args.update(changes)
        try:
            checked = G.bind_source_property(self.f.context, **args)
        except (
            AttributeError,
            KeyError,
            TypeError,
            ValueError,
            AssertionError,
            OSError,
        ) as exc:
            self.fail(f"finite property binding escaped as {type(exc).__name__}: {exc}")
        self.assertEqual(checked.disposition, disposition, checked.reason)
        if reason:
            self.assertIn(reason, checked.reason)
        if disposition == "matched":
            self.assertIsNotNone(
                checked.facts, "finite source-property facts were dropped"
            )
        else:
            self.assertIsNone(checked.facts)
        self.assertFalse(hasattr(checked, "qualified"))
        return checked

    def test_canonical_source_witness_has_independently_reviewed_meaning(self):
        checked = self.outcome()
        case = checked.facts.case
        self.assertEqual(case.statement, STATEMENT)
        self.assertEqual(
            (case.requirement_id, case.obligation_ids), ("REQ-GC-M", ("OB-GC-M",))
        )
        self.assertEqual(
            (case.contract_id, case.contract_version), ("rv64gc-lab-env-v2", "2")
        )
        self.assertEqual(
            (case.source_id, case.source_locator, case.category, case.risk),
            ("RVI-M", "11.1.2", "defined", "medium"),
        )
        self.assertEqual(case.coverage, "one signed-DIV quotient witness")
        self.assertEqual((case.witness.step_n, case.witness.register), (2, "x7"))
        self.assertEqual(
            (case.expected_value, case.control_value), ((1 << 64) - 3, (1 << 64) - 4)
        )
        self.assertEqual(checked.facts.observed_value, (1 << 64) - 3)

    def test_raw_fixture_is_valid_in_the_selected_canonical_scope(self):
        raw = P.raw_experiment(self.f.experiment, self.f.candidate)
        scope = V.Scope(
            "rv64gc-lab-v0",
            frozenset({"sail-riscv"}),
            frozenset({"REQ-GC-M"}),
            frozenset({"OB-GC-M"}),
        )
        self.assertEqual(V.check_experiment(raw, scope), [])

    def test_v2_separates_retained_input_from_original_publication_authority(self):
        checked = self.outcome()
        case = checked.facts.case
        self.assertEqual(case.case_id, "rv64gc-signed-div-truncation-v2")
        self.assertEqual(case.authority.source_id, "RVI-M")
        self.assertEqual(
            case.authority.source_sha256,
            "85e1db6c831ba6d325722d728d257b3ac9a9bf0a654ba1dc385108e99df75716",
        )
        self.assertEqual(
            case.required_inputs,
            (
                G.E.InputBinding(
                    "normative-source",
                    "RVI-M-DIV-STATEMENT",
                    "profiles/rv64gc-lab-v0/retained/div-statement.html",
                    "bbe3ff9dd6d8e1b452589669cd676d998265327eeaf8ed370bb95fcf15af1a58",
                ),
            ),
        )
        self.assertNotEqual(
            case.authority.source_sha256, case.required_inputs[0].sha256
        )
        self.assertEqual(checked.facts.authority_inputs, case.required_inputs)
        self.outcome("unsupported", case_id="rv64gc-signed-div-truncation-v1")

    def test_original_full_page_cannot_substitute_for_the_curated_input(self):
        old = G.E.InputBinding(
            "normative-source",
            "RVI-M",
            ".materials/riscv/pinned-v20260120/unpriv/m-st-ext.html",
            self.f.source["sha256"],
        )
        self.outcome(
            "refused",
            "pins",
            manifest=replace(
                self.f.manifest,
                inputs=(*self.f.manifest.inputs[:-1], old),
                child_input_ids=(old.input_id,),
            ),
        )

    def test_prefix_words_independently_encode_operands_and_signed_div(self):
        steps = self.f.values.facts.derivation.steps
        self.assertEqual(
            steps[0].instruction_bits, ((-7 & 0xFFF) << 20) | (5 << 7) | 0x13
        )
        self.assertEqual(steps[1].instruction_bits, (2 << 20) | (6 << 7) | 0x13)
        self.assertEqual(
            steps[2].instruction_bits,
            (1 << 25) | (6 << 20) | (5 << 15) | (4 << 12) | (7 << 7) | 0x33,
        )
        quotient = -(7 // 2)
        remainder = -7 - 2 * quotient
        self.assertEqual((quotient, remainder), (-3, -1))
        self.assertEqual(steps[2].writes, ((7, quotient & ((1 << 64) - 1)),))

    def test_publishing_derived_status_and_links_does_not_change_semantic_authority(
        self,
    ):
        for changes in [
            dict(implementation_status="partial"),
            dict(implementation_status="implemented"),
            dict(
                implementation_refs=[
                    dict(artifact_id="implementation", locator="public interface")
                ],
                evidence_ids=["evidence"],
            ),
        ]:
            with self.subTest(changes=changes):
                requirement = deepcopy(self.f.requirement)
                requirement.update(changes)
                authority = self.project(requirement=requirement)
                self.assertEqual(authority, self.f.context.authority)
                self.f.context = replace(self.f.context, authority=authority)
                self.outcome()

    def test_semantic_requirement_changes_are_not_masked(self):
        variants = [
            dict(statement="different source claim"),
            dict(risk="high"),
            dict(
                source_semantics=dict(
                    category="unspecified", detail="different source latitude"
                )
            ),
            dict(dependencies=["REQ-D-RVWMO"]),
            dict(obligation_ids=["OB-other"]),
        ]
        for change in variants:
            with self.subTest(change=change):
                requirement = deepcopy(self.f.requirement)
                requirement.update(change)
                authority = self.project(requirement=requirement)
                self.assertNotEqual(authority, self.template.context.authority)
                self.f.context = replace(self.template.context, authority=authority)
                self.outcome("refused", "semantic authority")

    def test_effective_obligation_source_and_profile_changes_need_review(self):
        for change in [
            dict(contract_version="3"),
            dict(statement="different guarantee"),
            dict(required_checks=["CHK-other"]),
        ]:
            with self.subTest(change=change):
                obligation = deepcopy(self.f.obligation)
                obligation.update(change)
                authority = self.project(obligation=obligation)
                self.assertNotEqual(authority, self.template.context.authority)
                self.f.context = replace(self.template.context, authority=authority)
                self.outcome("refused", "semantic authority")
        source = dict(self.f.source, sha256="a" * 64)
        self.f.context = replace(
            self.template.context, authority=self.project(source=source)
        )
        self.outcome("refused", "semantic authority")
        self.refuses(
            lambda: self.project(
                requirement=dict(self.f.requirement, profile_ids=["other"])
            )
        )

    def test_canonical_owner_roundtrip_rejects_unknown_record_fields(self):
        self.refuses(
            lambda: self.project(
                requirement=dict(self.f.requirement, future_semantic_field="unknown")
            )
        )
        self.refuses(
            lambda: self.project(
                obligation=dict(self.f.obligation, future_semantic_field="unknown")
            )
        )

    def test_authority_plain_tree_string_integer_and_node_bounds(self):
        for requirement in [
            False,
            {},
            dict(self.f.requirement, statement="x" * 65537),
            dict(self.f.requirement, insns=["div"] * 4090),
            dict(self.f.requirement, insns=["d" * 2000] * 1000),
        ]:
            with self.subTest(kind=type(requirement)):
                self.refuses(lambda: self.project(requirement=requirement))
        for source in [
            dict(self.f.source, bytes=1 << 129),
            dict(self.f.source, bytes=object()),
        ]:
            with self.subTest(kind=type(source["bytes"])):
                self.refuses(lambda: self.project(source=source))
        nested = "value"
        for _ in range(17):
            nested = [nested]
        self.refuses(lambda: self.project(source=dict(self.f.source, extra=nested)))

    def test_authority_missing_wrong_and_noncanonical_fields_refuse(self):
        for source in [
            {},
            dict(self.f.source, id=False),
            dict(self.f.source, sha256="A" * 64),
        ]:
            with self.subTest(source=str(source)[:40]):
                self.refuses(lambda: self.project(source=source))
        self.refuses(lambda: self.project(obligation={}))

    def test_projection_dictionary_order_is_irrelevant_and_no_caller_record_is_changed(
        self,
    ):
        before = deepcopy((self.f.requirement, self.f.obligation, self.f.source))
        reverse = {key: self.f.requirement[key] for key in reversed(self.f.requirement)}
        self.assertEqual(self.project(requirement=reverse), self.f.context.authority)
        self.assertEqual(before, (self.f.requirement, self.f.obligation, self.f.source))

    def test_context_and_authority_types_text_and_scope_refuse_before_binding(self):
        for context in [
            {},
            object.__new__(G.PropertyContext),
            replace(self.f.context, program=""),
            replace(self.f.context, statement="x" * 65537),
            replace(self.f.context, authority={}),
            replace(
                self.f.context,
                authority=replace(
                    self.f.context.authority, requirement_semantic_sha256="A" * 64
                ),
            ),
        ]:
            with self.subTest(kind=type(context)):
                self.refuses(lambda: self.freeze(context))
        self.refuses(lambda: self.freeze(profile_id="other"))
        self.refuses(lambda: self.freeze(experiment_id="other"))

    def test_context_obligation_and_witness_domains_are_bounded_and_plain(self):
        for obligations in [[], (), ("OB-GC-M",) * 2, ("x",) * 65, (False,)]:
            with self.subTest(obligations=obligations):
                self.refuses(
                    lambda: self.freeze(
                        replace(self.f.context, obligation_ids=obligations)
                    )
                )
        for witness in [
            None,
            G.C.GprWitness(True, "x7"),
            G.C.GprWitness(4096, "x7"),
            G.C.GprWitness(2, "x0"),
            G.C.GprWitness(2, "x07"),
        ]:
            with self.subTest(witness=witness):
                self.refuses(
                    lambda: self.freeze(replace(self.f.context, witness=witness))
                )

    def test_context_copy_survives_caller_changes(self):
        frozen = self.freeze()
        self.assertIsNot(frozen, self.f.context)
        self.assertIsNot(frozen.witness, self.f.context.witness)
        self.assertIsNot(frozen.authority, self.f.context.authority)
        object.__setattr__(self.f.context.witness, "step_n", 0)
        object.__setattr__(
            self.f.context.authority, "requirement_semantic_sha256", "a" * 64
        )
        self.assertEqual(
            (frozen.witness.step_n, frozen.authority.requirement_semantic_sha256),
            (2, self.template.context.authority.requirement_semantic_sha256),
        )

    def test_claim_statement_requirement_obligation_program_and_witness_must_match_case(
        self,
    ):
        for change in [
            dict(statement="unrelated property"),
            dict(requirement_id="REQ-other"),
            dict(obligation_ids=("OB-other",)),
            dict(program="other.s"),
            dict(witness=G.C.GprWitness(2, "x8")),
        ]:
            with self.subTest(change=change):
                self.f.context = replace(self.template.context, **change)
                self.outcome("refused", "property claim")

    def test_actual_relation_property_and_witness_are_bound(self):
        for change in [
            dict(property_id="other"),
            dict(witness=G.C.GprWitness(1, "x7")),
        ]:
            with self.subTest(change=change):
                self.outcome(
                    "refused",
                    "relation",
                    manifest=replace(
                        self.f.manifest,
                        relations=replace(self.f.manifest.relations, **change),
                    ),
                )

    def test_normative_pin_identity_role_path_digest_and_child_membership_are_exact(
        self,
    ):
        original = self.f.manifest.inputs
        for change in [
            dict(role="implementation"),
            dict(input_id="RVI-M"),
            dict(path="source/wrong.html"),
            dict(sha256="a" * 64),
        ]:
            with self.subTest(change=change):
                inputs = tuple(
                    (
                        replace(item, **change)
                        if item.input_id == "RVI-M-DIV-STATEMENT"
                        else item
                    )
                    for item in original
                )
                self.outcome(
                    "refused", "pins", manifest=replace(self.f.manifest, inputs=inputs)
                )
        self.outcome(
            "refused",
            "pins",
            manifest=replace(self.f.manifest, child_input_ids=("other",)),
        )

    def test_same_size_source_comment_change_requires_new_review(self):
        source = (ROOT / "profiles/rv64gc-lab-v0/guests/m-div.s").read_bytes()
        changed = source.replace(b"dividend", b"numerand", 1)
        self.assertNotEqual(changed, source)
        self.assertEqual(len(changed), len(source))
        values = G.C.compare_source_expectation(
            source=changed,
            baseline_expectation=(
                ROOT / "profiles/rv64gc-lab-v0/guests/m-div.expected.sexp"
            ).read_bytes(),
            program="m-div.s",
            instructions=27,
            witness=G.C.GprWitness(2, "x7"),
        )
        self.assertEqual(values.disposition, "matched", values.reason)
        sha = values.facts.derivation.source_sha256
        execution = self.f.manifest.relations.execution
        common = tuple(
            replace(item, sha256=sha) if item.role == "guest-source" else item
            for item in execution.common_inputs
        )
        inputs = tuple(
            replace(item, sha256=sha) if item.role == "guest-source" else item
            for item in self.f.manifest.inputs
        )
        manifest = replace(
            self.f.manifest,
            inputs=inputs,
            relations=replace(
                self.f.manifest.relations,
                execution=replace(execution, common_inputs=common),
            ),
        )
        self.outcome(
            "refused", "reviewed guest", manifest=manifest, source_values=values
        )

    def test_selected_baseline_and_exact_numeric_witness_are_bound(self):
        good = self.f.values
        for changes in [
            dict(expectation_sha256="a" * 64),
            dict(witness_value=(1 << 64) - 4),
            dict(witness=G.C.GprWitness(2, "x8")),
        ]:
            with self.subTest(changes=changes):
                self.outcome(
                    "refused",
                    source_values=replace(good, facts=replace(good.facts, **changes)),
                )

    def test_program_route_entry_source_identity_and_parent_budget_are_exact(self):
        for change in [
            dict(program="other.s"),
            dict(route="word"),
            dict(entry=0),
            dict(source_size=0),
            dict(source_sha256="a" * 64),
            dict(instructions=26),
        ]:
            with self.subTest(change=change):
                values = replace(
                    self.f.values,
                    facts=replace(
                        self.f.values.facts,
                        derivation=replace(self.f.values.facts.derivation, **change),
                    ),
                )
                self.outcome("refused", source_values=values)
        execution = replace(self.f.manifest.relations.execution, instructions=28)
        self.outcome(
            "refused",
            "budget",
            manifest=replace(
                self.f.manifest,
                relations=replace(self.f.manifest.relations, execution=execution),
            ),
        )

    def test_each_reviewed_prefix_axis_and_operand_change_is_detected(self):
        derived = self.f.values.facts.derivation
        for index, change in [
            (0, dict(n=False)),
            (1, dict(pc=0)),
            (2, dict(instruction_bits=0)),
            (0, dict(instruction_length=2)),
            (1, dict(fetches=1)),
            (0, dict(writes=((5, 7),))),
            (1, dict(writes=((6, 3),))),
            (2, dict(writes=((7, (1 << 64) - 4),))),
        ]:
            with self.subTest(index=index, change=change):
                steps = list(derived.steps)
                steps[index] = replace(steps[index], **change)
                self.outcome(
                    "refused",
                    "prefix",
                    source_values=replace(
                        self.f.values,
                        facts=replace(
                            self.f.values.facts,
                            derivation=replace(derived, steps=tuple(steps)),
                        ),
                    ),
                )

    def test_source_labels_do_not_create_semantic_authority(self):
        derived = self.f.values.facts.derivation
        steps = tuple(
            replace(step, source="untrusted label", derivation="untrusted explanation")
            for step in derived.steps
        )
        self.outcome(
            source_values=replace(
                self.f.values,
                facts=replace(
                    self.f.values.facts, derivation=replace(derived, steps=steps)
                ),
            )
        )

    def test_unknown_case_and_unsupported_source_have_no_facts_or_credit(self):
        self.outcome("unsupported", case_id="future-case")
        self.outcome(
            "unsupported",
            source_values=G.C.SourceExpectationCheck("unsupported", "scope"),
        )
        self.outcome(
            "refused", source_values=replace(self.f.values, disposition="unsupported")
        )

    def test_incomplete_public_facts_and_plans_refuse_without_tracebacks(self):
        for manifest in [
            None,
            {},
            object.__new__(G.M.ManifestPlan),
            replace(self.f.manifest, relations=None),
        ]:
            with self.subTest(kind=type(manifest)):
                self.outcome("refused", manifest=manifest)
        for values in [
            None,
            {},
            object.__new__(G.C.SourceExpectationCheck),
            replace(self.f.values, facts=None),
            replace(self.f.values, disposition="failed"),
        ]:
            with self.subTest(kind=type(values)):
                self.outcome("refused", source_values=values)
        derived = self.f.values.facts.derivation
        self.outcome(
            "refused",
            source_values=replace(
                self.f.values,
                facts=replace(
                    self.f.values.facts,
                    derivation=replace(derived, steps=derived.steps[:-1]),
                ),
            ),
        )

    def test_frozen_case_context_and_result_copy_nested_caller_bindings(self):
        checked = self.outcome()
        values = [
            (deepcopy(self.f.context), "statement"),
            (deepcopy(self.f.context.authority), "source_id"),
            (G.signed_division_case(), "coverage"),
            (checked, "reason"),
            (checked.facts, "observed_value"),
        ]
        for value, field in values:
            with self.subTest(field=field), self.assertRaises(FrozenInstanceError):
                setattr(value, field, None)
        checked = self.outcome()
        original = next(
            item for item in self.f.manifest.inputs if item.role == "guest-source"
        )
        self.assertIsNot(checked.facts.source, original)
        object.__setattr__(original, "sha256", "a" * 64)
        self.assertEqual(
            checked.facts.source.sha256, self.f.values.facts.derivation.source_sha256
        )
        normative = next(
            item
            for item in self.f.manifest.inputs
            if item.input_id == "RVI-M-DIV-STATEMENT"
        )
        self.assertIsNot(checked.facts.authority_inputs[0], normative)
        object.__setattr__(normative, "sha256", "a" * 64)
        self.assertEqual(
            checked.facts.authority_inputs[0].sha256,
            "bbe3ff9dd6d8e1b452589669cd676d998265327eeaf8ed370bb95fcf15af1a58",
        )
        first = G.signed_division_case()
        object.__setattr__(first.required_inputs[0], "sha256", "a" * 64)
        self.assertNotEqual(
            G.signed_division_case().required_inputs[0].sha256, "a" * 64
        )

    def test_pure_projection_and_binding_open_no_files_or_processes(self):
        with mock.patch(
            "builtins.open", side_effect=AssertionError("file I/O")
        ), mock.patch(
            "pathlib.Path.open", side_effect=AssertionError("path I/O")
        ), mock.patch(
            "os.open", side_effect=AssertionError("descriptor I/O")
        ), mock.patch(
            "subprocess.run", side_effect=AssertionError("process I/O")
        ):
            self.assertEqual(self.project(), self.f.context.authority)
            self.outcome()

    def test_unexpected_programming_failures_propagate(self):
        with mock.patch.object(
            G.T, "freeze_review", side_effect=RuntimeError("programming failure")
        ), self.assertRaisesRegex(RuntimeError, "programming failure"):
            G.bind_source_property(
                self.f.context,
                profile_id="rv64gc-lab-v0",
                experiment_id=self.f.context.experiment_id,
                manifest=self.f.manifest,
                source_values=self.f.values,
            )
        with mock.patch.object(
            G.Records, "dict_to_form", side_effect=RuntimeError("programming failure")
        ), self.assertRaisesRegex(RuntimeError, "programming failure"):
            self.project()


MUTATIONS = {
    "publication-authority": (
        "            _PUBLICATION_SHA,",
        "            _REQUIRED_INPUT_ROWS[0][3],",
    ),
    "record-roundtrip": (
        '_require(\n        str(form[0]) == family and Records.form_to_dict(form) == record,\n        "authority record does not round-trip through its canonical owner",\n    )',
        "_require(True, 'authority record does not round-trip through its canonical owner')",
    ),
    "authority-string-bound": (
        '_require(len(item) <= T.TEXT_CHARS, "authority string exceeds bound")',
        "_require(True, 'authority string exceeds bound')",
    ),
    "authority-byte-bound": (
        '_require(string_bytes <= 1024 * 1024, "authority strings exceed byte bound")',
        "_require(True, 'authority strings exceed byte bound')",
    ),
    "context-scope": (
        '_require(\n        _text(profile_id)\n        and values[0] == profile_id\n        and _text(experiment_id)\n        and values[1] == experiment_id,\n        "property context differs from selected scope",\n    )',
        "_require(True, 'property context differs from selected scope')",
    ),
    "authority-shape": (
        '_require(\n        all(_text(value) for value in values)\n        and values[0] == profile_id\n        and all(_digest(values[n]) for n in (2, 4, 6)),\n        "invalid selected property authority",\n    )',
        "_require(True, 'invalid selected property authority')",
    ),
    "claim-binding": (
        '_require(\n            (\n                selected.profile_id,\n                selected.program,\n                selected.requirement_id,\n                selected.obligation_ids,\n                selected.statement,\n                selected.witness,\n            )\n            == (\n                case.profile_id,\n                case.program,\n                case.requirement_id,\n                case.obligation_ids,\n                case.statement,\n                case.witness,\n            ),\n            "property claim differs from reviewed finite case",\n        )',
        "_require(True, 'property claim differs from reviewed finite case')",
    ),
    "semantic-authority": (
        '_require(\n            selected.authority == case.authority,\n            "current semantic authority differs from reviewed case",\n        )',
        "_require(True, 'current semantic authority differs from reviewed case')",
    ),
    "relation-binding": (
        '_require(\n            relations.property_id == selected.property_id\n            and relations.witness == selected.witness,\n            "selected relation differs from property context",\n        )',
        "_require(True, 'selected relation differs from property context')",
    ),
    "normative-pin": (
        '_require(\n            all(\n                inputs.get(pin.input_id) == pin\n                and pin.input_id in manifest.child_input_ids\n                for pin in case.required_inputs\n            ),\n            "reviewed normative source pins differ or are not children",\n        )',
        "_require(True, 'reviewed normative source pins differ or are not children')",
    ),
    "guest-source": (
        '_require(\n            inputs.get(principal.input_id) == principal\n            and principal.sha256 == _SOURCE_SHA,\n            "selected source differs from reviewed guest",\n        )',
        "_require(True, 'selected source differs from reviewed guest')",
    ),
    "baseline-binding": (
        '_require(\n            facts.expectation_sha256 == execution.baseline_expectation.sha256,\n            "source finding differs from selected baseline expectation",\n        )',
        "_require(True, 'source finding differs from selected baseline expectation')",
    ),
    "witness-value": (
        '_require(\n            facts.witness == selected.witness\n            and type(facts.witness_value) is int\n            and facts.witness_value == case.expected_value,\n            "source witness differs from reviewed quotient",\n        )',
        "_require(True, 'source witness differs from reviewed quotient')",
    ),
    "budget-binding": (
        '_require(\n            type(execution.instructions) is int\n            and execution.instructions == case.instructions\n            and type(derived.instructions) is int\n            and derived.instructions == case.instructions,\n            "reviewed property requires the complete 27-boundary budget",\n        )',
        "_require(True, 'reviewed property requires the complete 27-boundary budget')",
    ),
    "source-identity": (
        '_require(\n            derived.program == case.program\n            and derived.route == "snapshot-parcels-v1"\n            and type(derived.entry) is int\n            and derived.entry == 0x80000000\n            and type(derived.source_size) is int\n            and derived.source_size == 2512\n            and derived.source_sha256 == principal.sha256,\n            "source derivation differs from reviewed program/entry/identity",\n        )',
        "_require(True, 'source derivation differs from reviewed program/entry/identity')",
    ),
    "prefix-proof": (
        '_require(\n                all(type(value) is int for value in numeric)\n                and type(writes) is tuple\n                and len(writes) == 1\n                and type(writes[0]) is tuple\n                and len(writes[0]) == 2\n                and all(type(value) is int for value in writes[0])\n                and (*numeric, writes) == expected,\n                "snapshot prefix differs from reviewed words/operands/quotient",\n            )',
        "_require(True, 'snapshot prefix differs from reviewed words/operands/quotient')",
    ),
    "authority-node-bound": (
        '_require(\n            nodes <= 4096 and depth <= 16, "authority tree exceeds node/depth bounds"\n        )',
        "_require(depth <= 16, 'authority tree exceeds node/depth bounds')",
    ),
    "authority-depth-bound": (
        '_require(\n            nodes <= 4096 and depth <= 16, "authority tree exceeds node/depth bounds"\n        )',
        "_require(nodes <= 4096, 'authority tree exceeds node/depth bounds')",
    ),
    "derived-status": (
        'implementation_status="planned"',
        'implementation_status=record["implementation_status"]',
    ),
    "derived-links": (
        'record = dict(\n            record,\n            implementation_status="planned",\n            implementation_refs=[],\n            evidence_ids=[],\n        )',
        'record = dict(\n            record,\n            implementation_status="planned",\n            implementation_refs=record["implementation_refs"],\n            evidence_ids=record["evidence_ids"],\n        )',
    ),
    "requirement-meaning": (
        '_semantic_digest(requirement, "requirement")',
        "_REQUIREMENT_SEMANTICS",
    ),
    "obligation-meaning": (
        '_semantic_digest(obligation, "obligation")',
        "_OBLIGATION_SEMANTICS",
    ),
    "context-copy": (
        'return PropertyContext(\n        values[0],\n        values[1],\n        values[2],\n        values[3],\n        values[4],\n        tuple(sorted(obligations)),\n        values[5],\n        C.GprWitness(step, register),\n        _freeze_authority(getattr(context, "authority", None), profile_id),\n    )',
        "return context",
    ),
    "source-fact-copy": ("inputs[principal.input_id],", "principal,"),
    "authority-fact-copy": (
        "tuple(inputs[pin.input_id] for pin in case.required_inputs)",
        "tuple(next(item for item in manifest.inputs if item.input_id == pin.input_id) for pin in case.required_inputs)",
    ),
    "case-selection": ("if case_id != CASE_ID:", "if False:"),
    "source-unsupported": (
        'if source_values.disposition == "unsupported":',
        "if False:",
    ),
    "frozen-results": ("@dataclass(frozen=True)", "@dataclass(frozen=False)"),
    "finite-finding": (
        'return SourcePropertyCheck(\n        "matched",\n        "reviewed finite source property binds; authentication/collection/qualification separate",\n        result,\n    )',
        'return SourcePropertyCheck(\n        "matched",\n        "reviewed finite source property binds; authentication/collection/qualification separate",\n        None,\n    )',
    ),
}


def main():
    global G
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        source = Path(G.__file__).read_text()
        before, after = MUTATIONS[args.mutation]
        expected = 5 if args.mutation == "frozen-results" else 1
        if source.count(before) != expected:
            raise RuntimeError("property mutation seam count differs")
        module = types.ModuleType("mutated_source_property")
        module.__file__ = G.__file__
        sys.modules[module.__name__] = module
        exec(
            compile(source.replace(before, after), G.__file__, "exec"), module.__dict__
        )
        G = module
    result = unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(PropertyTests)
    )
    print(
        f"MATCHED-GPR-PROPERTY: {result.testsRun} tests / {len(result.failures)} failures / "
        f"{len(result.errors)} errors; synthetic metadata, finite source witness only"
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
