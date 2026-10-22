#!/usr/bin/env python3
"""Finite GPR property controls for the reviewed cases; synthetic metadata, no capture credit."""
from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import FrozenInstanceError, asdict, replace
import hashlib
from pathlib import Path
import re
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
GUESTS = ROOT / "profiles/rv64gc-lab-v0/guests"
STATEMENT = (
    "For signed DIV with x5 = -7 and x6 = 2, the x7 change at boundary 2 "
    "is -3 (rounding toward zero)."
)
M64 = (1 << 64) - 1
# Independent of the author and the assembler: the encoding fields of the chapter's forms.
FUNCT3 = dict(
    mul=0, mulh=1, mulhsu=2, mulhu=3, div=4, divu=5, rem=6, remu=7,
    mulw=0, divw=4, divuw=5, remw=6, remuw=7,
)
INSTRUCTION = re.compile(r"\s*(\w+)\s+x(\d+),\s*x(\d+),\s*(-?\w+)")


def encode(line: str) -> int:
    """Encode one m-forms instruction from its fields (I-type addi/slli, R-type M forms)."""
    op, rd, rs1, third = INSTRUCTION.match(line).groups()
    rd, rs1 = int(rd), int(rs1)
    if op == "addi":
        return ((int(third) & 0xFFF) << 20) | (rs1 << 15) | (rd << 7) | 0x13
    if op == "slli":
        return (int(third) << 20) | (rs1 << 15) | (1 << 12) | (rd << 7) | 0x13
    rs2, opcode = int(third[1:]), 0x3B if op.endswith("w") else 0x33
    return (1 << 25) | (rs2 << 20) | (rs1 << 15) | (FUNCT3[op] << 12) | (rd << 7) | opcode


def _signed(value: int, bits: int) -> int:
    value &= (1 << bits) - 1
    return value - (1 << bits) if value >> (bits - 1) else value


def _truncating_quotient(a: int, b: int) -> int:
    quotient = abs(a) // abs(b)
    return -quotient if (a < 0) != (b < 0) else quotient


def execute(regs: list, line: str) -> tuple[int, int]:
    """Evaluate one m-forms instruction with plain integer arithmetic and the chapter's Table 1."""
    op, rd, rs1, third = INSTRUCTION.match(line).groups()
    rd, a = int(rd), regs[int(rs1)]
    if op == "addi":
        value = (a + int(third)) & M64
    elif op == "slli":
        value = (a << int(third)) & M64
    else:
        b = regs[int(third[1:])]
        sa, sb = _signed(a, 64), _signed(b, 64)
        wa, wb, ua, ub = _signed(a, 32), _signed(b, 32), a & 0xFFFFFFFF, b & 0xFFFFFFFF
        word = lambda v: _signed(v, 32) & M64  # noqa: E731  sign-extend a 32-bit result
        overflow, word_overflow = sa == -(1 << 63) and sb == -1, wa == -(1 << 31) and wb == -1
        value = {
            "mul": lambda: (a * b) & M64,
            "mulh": lambda: ((sa * sb) >> 64) & M64,
            "mulhsu": lambda: ((sa * b) >> 64) & M64,
            "mulhu": lambda: ((a * b) >> 64) & M64,
            "mulw": lambda: word(a * b),
            "div": lambda: M64 if sb == 0 else (a if overflow else _truncating_quotient(sa, sb) & M64),
            "divu": lambda: M64 if b == 0 else a // b,
            "rem": lambda: a if sb == 0 else (0 if overflow else (sa - sb * _truncating_quotient(sa, sb)) & M64),
            "remu": lambda: a if b == 0 else a % b,
            "divw": lambda: M64 if wb == 0 else word(ua if word_overflow else _truncating_quotient(wa, wb)),
            "divuw": lambda: M64 if ub == 0 else word(ua // ub),
            "remw": lambda: word(ua) if wb == 0 else word(0 if word_overflow else wa - wb * _truncating_quotient(wa, wb)),
            "remuw": lambda: word(ua) if ub == 0 else word(ua % ub),
        }[op]()
    regs[rd] = value
    regs[0] = 0
    return rd, value


def authority():
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
    return requirement, obligation, source, G.project_authority(
        "rv64gc-lab-v0", requirement=requirement, obligation=obligation, source=source
    )


def fixture(case_id: str = G.CASE_ID):
    """Construct public-owner facts for a reviewed case, not authenticated artifact or process evidence."""
    case = G.reviewed_case(case_id)
    requirement, obligation, source, selected_authority = authority()
    values = G.C.compare_source_expectation(
        source=(GUESTS / case.program).read_bytes(),
        baseline_expectation=(GUESTS / (Path(case.program).stem + ".expected.sexp")).read_bytes(),
        program=case.program,
        instructions=case.instructions,
        witness=case.control().witness,
    )
    if values.disposition != "matched":
        raise RuntimeError(
            "canonical source fixture no longer matches " + case_id + ": " + values.reason
        )
    experiment, candidate = P.fixture()
    experiment.update(program=case.program, instructions=case.instructions)
    graph = experiment["verification"]
    graph["property"] = [
        dict(
            id=item.property_id,
            statement=item.statement,
            requirement_id=case.requirement_id,
            obligation_ids=list(case.obligation_ids),
            observation_kinds=["gpr-change"],
            gpr_witness=asdict(item.witness),
        )
        for item in case.properties
    ]
    graph["control_run"][0]["property_ids"] = [case.control_property_id]
    for run in graph["run"]:
        run["argv"][4] = str(case.instructions)
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
    normative = G.E.InputBinding(*G._REQUIRED_INPUT_ROWS[0])
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
    witnesses = {item.property_id: item.witness for item in relations.plan.properties}
    claims = tuple(
        G.PropertyClaim(
            prop["id"],
            prop["requirement_id"],
            tuple(prop["obligation_ids"]),
            prop["statement"],
            witnesses[prop["id"]],
        )
        for prop in graph["property"]
    )
    context = G.PropertyContext(
        "rv64gc-lab-v0",
        experiment["id"],
        case.program,
        claims,
        relations.plan.control_property_id,
        selected_authority,
    )
    return SimpleNamespace(
        case_id=case_id,
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
        cls.m_template = fixture(G.M_FORMS_CASE_ID)

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

    def outcome(self, disposition="matched", reason=None, fixture=None, **changes):
        f = self.f if fixture is None else fixture
        args = dict(
            profile_id="rv64gc-lab-v0",
            experiment_id=f.context.experiment_id,
            manifest=f.manifest,
            source_values=f.values,
            case_id=f.case_id,
        )
        args.update(changes)
        try:
            checked = G.bind_source_property(f.context, **args)
        except (
            AttributeError,
            KeyError,
            IndexError,
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

    def claim(self, **changes):
        """The retained case's one claim with a change; the context carries it alone."""
        return replace(self.f.context, claims=(replace(self.f.context.claims[0], **changes),))

    def test_canonical_source_witness_has_independently_reviewed_meaning(self):
        checked = self.outcome()
        case = checked.facts.case
        control = case.control()
        self.assertEqual(control.statement, STATEMENT)
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
        self.assertEqual((control.witness.step_n, control.witness.register), (2, "x7"))
        self.assertEqual(
            (control.expected_value, case.control_value), ((1 << 64) - 3, (1 << 64) - 4)
        )
        self.assertEqual(
            checked.facts.observed,
            (G.ObservedProperty("signed-quotient", G.C.GprWitness(2, "x7"), (1 << 64) - 3),),
        )
        self.assertEqual(case.properties, (control,))

    def test_raw_fixture_is_valid_in_the_selected_canonical_scope(self):
        scope = V.Scope(
            "rv64gc-lab-v0",
            frozenset({"sail-riscv"}),
            frozenset({"REQ-GC-M"}),
            frozenset({"OB-GC-M"}),
        )
        for f in (self.f, self.m_template):
            with self.subTest(case=f.case_id):
                raw = P.raw_experiment(f.experiment, f.candidate)
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

    def test_m_forms_case_declares_every_form_and_every_table1_cell(self):
        case = G.m_forms_case()
        self.assertEqual(G.reviewed_case_ids(), (G.CASE_ID, G.M_FORMS_CASE_ID))
        self.assertEqual(case.case_id, "rv64gc-m-forms-v3")
        self.assertEqual((case.program, case.instructions), ("m-forms.s", 33))
        source = (GUESTS / case.program).read_bytes()
        self.assertEqual(
            (len(source), hashlib.sha256(source).hexdigest()),
            (case.source_size, case.source_sha256),
        )
        self.assertEqual(len(case.properties), 25)
        self.assertEqual(len({item.property_id for item in case.properties}), 25)
        self.assertEqual(len({item.witness for item in case.properties}), 25)
        expectations = D.load_expectations(GUESTS / "m-forms.expected.sexp")
        steps = {step["n"]: step for step in expectations["step"]}
        forms = {
            steps[item.witness.step_n]["insn"].split()[0]
            for item in case.properties
            if item.cell.startswith("form:")
        }
        self.assertEqual(forms, set(self.f.requirement["insns"]))
        self.assertEqual(len(forms), 13)
        table1 = sorted(
            item.witness.step_n for item in case.properties if item.cell.startswith("table1:")
        )
        self.assertEqual(table1, sorted(n for n, step in steps.items() if "Table 1" in step["source"]))
        self.assertEqual(len(table1), 12)
        for item in case.properties:
            with self.subTest(property=item.property_id):
                step = steps[item.witness.step_n]
                self.assertEqual(
                    step["writes"], {item.witness.register: f"0x{item.expected_value:016x}"}
                )
                self.assertEqual(item.cell.split(":")[1].split("-")[0], step["insn"].split()[0])
        control = case.control()
        self.assertEqual(
            (control.property_id, control.witness, control.expected_value, case.control_value),
            ("form-div", G.C.GprWitness(12, "x15"), (1 << 64) - 3, (1 << 64) - 4),
        )
        self.assertEqual([row[0] for row in case.reviewed_steps], list(range(33)))
        self.assertEqual((case.requirement_id, case.obligation_ids, case.authority),
                         ("REQ-GC-M", ("OB-GC-M",), G.signed_division_case().authority))
        self.assertEqual(case.required_inputs, G.signed_division_case().required_inputs)
        self.refuses(lambda: G.reviewed_case("rv64gc-m-forms-v2"))

    def test_m_forms_words_and_values_are_independently_derived(self):
        case = G.m_forms_case()
        lines = [
            line for line in (GUESTS / case.program).read_text().splitlines() if line.strip()
        ]
        self.assertEqual(len(lines), 33)
        regs = [0] * 32
        for n, line in enumerate(lines):
            rd, value = execute(regs, line)
            with self.subTest(boundary=n):
                self.assertEqual(
                    case.reviewed_steps[n],
                    (n, 0x80000000 + 4 * n, encode(line), 4, 2, ((rd, value),)),
                )
        by_step = {row[0]: row[5][0] for row in case.reviewed_steps}
        for item in case.properties:
            self.assertEqual(
                by_step[item.witness.step_n],
                (int(item.witness.register[1:]), item.expected_value),
                item.property_id,
            )
        derived = self.m_template.values.facts.derivation
        self.assertEqual(
            tuple(
                (s.n, s.pc, s.instruction_bits, s.instruction_length, s.fetches, s.writes)
                for s in derived.steps
            ),
            case.reviewed_steps,
        )

    def test_m_forms_case_binds_every_predeclared_value_to_the_source_derivation(self):
        checked = self.outcome(fixture=self.m_template)
        case = checked.facts.case
        self.assertEqual(case.case_id, G.M_FORMS_CASE_ID)
        self.assertEqual(len(checked.facts.observed), 25)
        self.assertEqual(
            checked.facts.observed,
            tuple(
                G.ObservedProperty(item.property_id, item.witness, item.expected_value)
                for item in case.properties
            ),
        )
        control = next(
            item for item in checked.facts.observed if item.property_id == case.control_property_id
        )
        self.assertEqual(control.value, self.m_template.values.facts.witness_value)
        self.assertEqual(checked.facts.source.sha256, case.source_sha256)
        self.assertEqual(checked.facts.authority_inputs, case.required_inputs)

    def test_each_predeclared_value_is_held_to_the_derivation_beyond_the_reviewed_words(self):
        f = deepcopy(self.m_template)
        derived = f.values.facts.derivation
        target = next(item for item in G.m_forms_case().properties if item.property_id == "table1-remw-overflow")
        reviewed = G.m_forms_case()
        prefix_only = lambda: replace(reviewed, reviewed_steps=reviewed.reviewed_steps[:3])  # noqa: E731
        with mock.patch.dict(G._CASES, {G.M_FORMS_CASE_ID: prefix_only}):
            self.outcome(fixture=f)
            for writes, expected in [
                (((12, 0x1234),), "predeclared value differs from the source derivation: table1-remw-overflow"),
                (((13, 0),), "predeclared value differs from the source derivation: table1-remw-overflow"),
                ((), "predeclared value differs from the source derivation: table1-remw-overflow"),
            ]:
                steps = list(derived.steps)
                steps[target.witness.step_n] = replace(steps[target.witness.step_n], writes=writes)
                with self.subTest(writes=writes):
                    self.outcome(
                        "refused",
                        expected,
                        fixture=f,
                        source_values=replace(
                            f.values,
                            facts=replace(f.values.facts, derivation=replace(derived, steps=tuple(steps))),
                        ),
                    )

    def test_m_forms_claims_must_match_the_case_exactly(self):
        f = deepcopy(self.m_template)
        claims = f.context.claims
        first, second = claims[0], claims[1]
        for context, reason in [
            (replace(f.context, claims=claims[:-1]), "property claim"),
            (replace(f.context, claims=(*claims[1:], replace(first, property_id="renamed"))), "property claim"),
            (replace(f.context, claims=(*claims[2:], replace(first, witness=second.witness), replace(second, witness=first.witness))), "property claim"),
            (replace(f.context, control_property_id=second.property_id if second.property_id != f.context.control_property_id else first.property_id), "property claim"),
            (replace(f.context, control_property_id="form-mulhu"), "property claim"),
            (replace(f.context, control_property_id="not-a-claim"), "control property is not one of the claims"),
            (replace(f.context, claims=(*claims, replace(first, property_id="extra", witness=G.C.GprWitness(0, "x5")))), "property claim"),
        ]:
            with self.subTest(reason=reason):
                self.outcome("refused", reason, fixture=SimpleNamespace(**{**vars(f), "context": context}))

    def test_claim_order_is_irrelevant(self):
        f = deepcopy(self.m_template)
        relations = f.manifest.relations
        reordered = SimpleNamespace(
            **vars(f),
        )
        reordered.context = replace(f.context, claims=tuple(reversed(f.context.claims)))
        reordered.manifest = replace(
            f.manifest, relations=replace(relations, properties=tuple(reversed(relations.properties)))
        )
        checked = self.outcome(fixture=reordered)
        self.assertEqual(len(checked.facts.observed), 25)

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
            replace(self.f.context, control_property_id=""),
            self.claim(statement="x" * 65537),
            self.claim(property_id=""),
            self.claim(requirement_id=5),
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

    def test_context_claim_obligation_and_witness_domains_are_bounded_and_plain(self):
        one = self.f.context.claims[0]
        for index, claims in enumerate([
            (),
            [one],
            (one,) * 2,
            (one, *[replace(one, property_id=f"p{n}", witness=G.C.GprWitness(n, "x1")) for n in range(64)]),
            (one, replace(one, property_id="other")),
            (one, replace(one, witness=G.C.GprWitness(3, "x8"))),
            (asdict(one),),
            (object.__new__(G.PropertyClaim),),
        ]):
            with self.subTest(index=index):
                self.refuses(
                    lambda: self.freeze(replace(self.f.context, claims=claims))
                )
        self.refuses(
            lambda: self.freeze(replace(self.f.context, control_property_id="absent"))
        )
        for obligations in [[], (), ("OB-GC-M",) * 2, ("x",) * 65, (False,)]:
            with self.subTest(obligations=obligations):
                self.refuses(
                    lambda: self.freeze(self.claim(obligation_ids=obligations))
                )
        for witness in [
            None,
            G.C.GprWitness(True, "x7"),
            G.C.GprWitness(4096, "x7"),
            G.C.GprWitness(2, "x0"),
            G.C.GprWitness(2, "x07"),
        ]:
            with self.subTest(witness=witness):
                self.refuses(lambda: self.freeze(self.claim(witness=witness)))

    def test_context_copy_survives_caller_changes(self):
        frozen = self.freeze()
        self.assertIsNot(frozen, self.f.context)
        self.assertIsNot(frozen.claims, self.f.context.claims)
        self.assertIsNot(frozen.claims[0], self.f.context.claims[0])
        self.assertIsNot(frozen.claims[0].witness, self.f.context.claims[0].witness)
        self.assertIsNot(frozen.authority, self.f.context.authority)
        object.__setattr__(self.f.context.claims[0].witness, "step_n", 0)
        object.__setattr__(self.f.context.claims[0], "statement", "changed")
        object.__setattr__(
            self.f.context.authority, "requirement_semantic_sha256", "a" * 64
        )
        self.assertEqual(
            (
                frozen.claims[0].witness.step_n,
                frozen.claims[0].statement,
                frozen.authority.requirement_semantic_sha256,
            ),
            (2, STATEMENT, self.template.context.authority.requirement_semantic_sha256),
        )
        frozen = self.freeze(self.m_template.context)
        self.assertEqual(
            [claim.property_id for claim in frozen.claims],
            sorted(claim.property_id for claim in self.m_template.context.claims),
        )

    def test_claim_statement_requirement_obligation_program_and_witness_must_match_case(
        self,
    ):
        for context in [
            self.claim(statement="unrelated property"),
            self.claim(requirement_id="REQ-other"),
            self.claim(obligation_ids=("OB-other",)),
            replace(self.claim(property_id="other-quotient"), control_property_id="other-quotient"),
            replace(self.f.context, program="other.s"),
            self.claim(witness=G.C.GprWitness(2, "x8")),
            replace(
                self.f.context,
                claims=(
                    self.f.context.claims[0],
                    replace(self.f.context.claims[0], property_id="remainder", witness=G.C.GprWitness(3, "x8")),
                ),
            ),
        ]:
            with self.subTest(context=context):
                self.f.context = context
                self.outcome("refused", "property claim")

    def test_actual_relation_properties_and_control_are_bound(self):
        relations = self.f.manifest.relations
        for change in [
            dict(control_property_id="other"),
            dict(control_witness=G.C.GprWitness(1, "x7")),
            dict(properties=()),
            dict(properties=(G.R.PropertyRelation("signed-quotient", G.C.GprWitness(1, "x7")),)),
            dict(properties=(*relations.properties, G.R.PropertyRelation("extra", G.C.GprWitness(3, "x8")))),
            dict(properties=list(relations.properties)),
        ]:
            with self.subTest(change=change):
                self.outcome(
                    "refused",
                    "relation",
                    manifest=replace(
                        self.f.manifest,
                        relations=replace(relations, **change),
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
        source = (GUESTS / "m-div.s").read_bytes()
        changed = source.replace(b"dividend", b"numerand", 1)
        self.assertNotEqual(changed, source)
        self.assertEqual(len(changed), len(source))
        values = G.C.compare_source_expectation(
            source=changed,
            baseline_expectation=(GUESTS / "m-div.expected.sexp").read_bytes(),
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

    def test_selected_baseline_and_exact_numeric_control_value_are_bound(self):
        good = self.f.values
        for changes in [
            dict(expectation_sha256="a" * 64),
            dict(witness_value=(1 << 64) - 4),
            dict(witness_value=True),
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

    def test_each_reviewed_word_axis_and_operand_change_is_detected(self):
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
            (2, dict(writes=((7, (1 << 64) - 3), (8, 1)))),
        ]:
            with self.subTest(index=index, change=change):
                steps = list(derived.steps)
                steps[index] = replace(steps[index], **change)
                self.outcome(
                    "refused",
                    "reviewed words",
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
        self.outcome("refused", case_id=G.M_FORMS_CASE_ID)
        self.outcome("refused", fixture=self.m_template, case_id=G.CASE_ID)
        self.outcome(
            "unsupported",
            source_values=G.C.SourceExpectationCheck("unsupported", "scope"),
        )
        self.outcome(
            "refused", source_values=replace(self.f.values, disposition="unsupported")
        )
        self.outcome("refused", case_id="")

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
            (deepcopy(self.f.context), "program"),
            (deepcopy(self.f.context.claims[0]), "statement"),
            (deepcopy(self.f.context.authority), "source_id"),
            (G.signed_division_case(), "coverage"),
            (G.m_forms_case().properties[0], "expected_value"),
            (checked, "reason"),
            (checked.facts, "observed"),
            (checked.facts.observed[0], "value"),
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
        for builder in (G.signed_division_case, G.m_forms_case):
            first = builder()
            object.__setattr__(first.required_inputs[0], "sha256", "a" * 64)
            object.__setattr__(first.properties[0], "expected_value", 0)
            self.assertNotEqual(builder().required_inputs[0].sha256, "a" * 64)
            self.assertNotEqual(builder().properties[0].expected_value, 0)

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
            self.outcome(fixture=self.m_template)

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
        "        _PUBLICATION_SHA,\n",
        "        _REQUIRED_INPUT_ROWS[0][3],\n",
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
    "claim-count": (
        "type(claims) is tuple and 1 <= len(claims) <= MAX_PROPERTIES,",
        "type(claims) is tuple,",
    ),
    "claim-identity": (
        'len(set(identities)) == len(identities), "duplicate property claim identities"',
        "True, 'duplicate property claim identities'",
    ),
    "claim-witness": (
        'len(set(witnesses)) == len(witnesses), "two property claims witness one observation"',
        "True, 'two property claims witness one observation'",
    ),
    "control-claim": (
        '_require(values[3] in identities, "control property is not one of the claims")',
        "_require(True, 'control property is not one of the claims')",
    ),
    "claim-binding": (
        '_require(\n            (\n                selected.profile_id,\n                selected.program,\n                selected.control_property_id,\n                selected.claims,\n            )\n            == (case.profile_id, case.program, case.control_property_id, case.claims()),\n            "property claims differ from reviewed finite case",\n        )',
        "_require(True, 'property claims differ from reviewed finite case')",
    ),
    "semantic-authority": (
        '_require(\n            selected.authority == case.authority,\n            "current semantic authority differs from reviewed case",\n        )',
        "_require(True, 'current semantic authority differs from reviewed case')",
    ),
    "relation-binding": (
        '_require(\n            type(relations.properties) is tuple\n            and relations.control_property_id == selected.control_property_id\n            and relations.control_witness == control.witness\n            and tuple(sorted(relations.properties, key=lambda item: item.property_id))\n            == tuple(\n                R.PropertyRelation(claim.property_id, claim.witness)\n                for claim in selected.claims\n            ),\n            "selected relations differ from property context",\n        )',
        "_require(True, 'selected relations differ from property context')",
    ),
    "normative-pin": (
        '_require(\n            all(\n                inputs.get(pin.input_id) == pin\n                and pin.input_id in manifest.child_input_ids\n                for pin in case.required_inputs\n            ),\n            "reviewed normative source pins differ or are not children",\n        )',
        "_require(True, 'reviewed normative source pins differ or are not children')",
    ),
    "guest-source": (
        '_require(\n            inputs.get(principal.input_id) == principal\n            and principal.sha256 == case.source_sha256,\n            "selected source differs from reviewed guest",\n        )',
        "_require(True, 'selected source differs from reviewed guest')",
    ),
    "baseline-binding": (
        '_require(\n            facts.expectation_sha256 == execution.baseline_expectation.sha256,\n            "source finding differs from selected baseline expectation",\n        )',
        "_require(True, 'source finding differs from selected baseline expectation')",
    ),
    "witness-value": (
        '_require(\n            facts.witness == control.witness\n            and type(facts.witness_value) is int\n            and facts.witness_value == control.expected_value,\n            "source witness differs from reviewed control value",\n        )',
        "_require(True, 'source witness differs from reviewed control value')",
    ),
    "budget-binding": (
        '_require(\n            type(execution.instructions) is int\n            and execution.instructions == case.instructions\n            and type(derived.instructions) is int\n            and derived.instructions == case.instructions,\n            "reviewed case requires its complete boundary budget",\n        )',
        "_require(True, 'reviewed case requires its complete boundary budget')",
    ),
    "source-identity": (
        '_require(\n            derived.program == case.program\n            and derived.route == "snapshot-parcels-v1"\n            and type(derived.entry) is int\n            and derived.entry == _ENTRY\n            and type(derived.source_size) is int\n            and derived.source_size == case.source_size\n            and derived.source_sha256 == principal.sha256,\n            "source derivation differs from reviewed program/entry/identity",\n        )',
        "_require(True, 'source derivation differs from reviewed program/entry/identity')",
    ),
    "reviewed-words": (
        '        and (*numeric, writes) == expected,\n        "snapshot steps differ from reviewed words/operands/values",\n    )',
        '        and True,\n        "snapshot steps differ from reviewed words/operands/values",\n    )',
    ),
    "claim-values": (
        '_require(\n                type(value) is int and value == item.expected_value,\n                "predeclared value differs from the source derivation: " + item.property_id,\n            )',
        "_require(True, 'predeclared value differs from the source derivation: ' + item.property_id)",
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
        'return PropertyContext(\n        values[0],\n        values[1],\n        values[2],\n        tuple(sorted(frozen, key=lambda claim: claim.property_id)),\n        values[3],\n        _freeze_authority(getattr(context, "authority", None), profile_id),\n    )',
        "return context",
    ),
    "claim-copy": (
        'return PropertyClaim(\n        values[0],\n        values[1],\n        tuple(sorted(obligations)),\n        values[2],\n        _freeze_witness(getattr(claim, "witness", None)),\n    )',
        "return claim",
    ),
    "source-fact-copy": ("inputs[principal.input_id],", "principal,"),
    "authority-fact-copy": (
        "tuple(inputs[pin.input_id] for pin in case.required_inputs)",
        "tuple(next(item for item in manifest.inputs if item.input_id == pin.input_id) for pin in case.required_inputs)",
    ),
    "case-selection": ("if case_id not in _CASES:", "if False:"),
    "source-unsupported": (
        'if source_values.disposition == "unsupported":',
        "if False:",
    ),
    "frozen-results": ("@dataclass(frozen=True)", "@dataclass(frozen=False)"),
    "finite-finding": (
        'return SourcePropertyCheck(\n        "matched",\n        "reviewed finite source properties bind; authentication/collection/qualification separate",\n        result,\n    )',
        'return SourcePropertyCheck(\n        "matched",\n        "reviewed finite source properties bind; authentication/collection/qualification separate",\n        None,\n    )',
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
        expected = 8 if args.mutation == "frozen-results" else 1
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
        f"{len(result.errors)} errors; synthetic metadata, finite source witnesses only"
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
