#!/usr/bin/env python3
"""Pure first-method property/control/declared-derivation/pair bindings.

Caller owns complete raw parent schema and scoped graph validation. These frozen
facts describe declarations; artifact currentness, actual expected derivation,
byte comparison and full method/policy qualification remain separate owners.
A case declares one to MAX_PROPERTIES GPR-change properties, each with its own
typed witness; the control run names exactly one of them, and that property's
witness is the witness the three-run byte comparison discriminates.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

from matched_gpr_comparison import GprWitness
import matched_gpr_execution as E

ASSESSMENTS = frozenset(("shared", "not-shared", "no-evidence-of-sharing", "not-examined"))
VERDICTS = frozenset(("AGREE", "DIVERGE", "REFUSED"))
MAX_PROPERTIES = 64  # predeclared properties per case; the m-forms case declares 25 (P4-SYSTEM.14 a42at)


@dataclass(frozen=True)
class PairBinding:
    pair_id: str
    left: str
    right: str
    subsystem: str
    assessment: str
    shared_input_ids: tuple[str, ...]
    evidence: str
    consequence: str


@dataclass(frozen=True)
class PropertyRelation:
    property_id: str
    witness: GprWitness


@dataclass(frozen=True)
class RelationPlan:
    execution: E.ExecutionPlan
    properties: tuple[PropertyRelation, ...]  # every declared property, in record order
    control_property_id: str  # the one property the control run discriminates
    control_witness: GprWitness  # its witness: the three-run byte comparison's witness
    control_id: str
    control_observed_verdict: str  # declaration, never computed method success
    expected_version: str
    derivation_common_input_ids: tuple[str, ...]
    pairs: tuple[PairBinding, ...]


@dataclass(frozen=True)
class RelationCheck:
    disposition: str  # matched / unsupported / refused; never method success
    reason: str
    plan: RelationPlan | None = None


class RelationError(ValueError):
    """The selected finite declared relationship cannot be established."""


def _require(condition: bool, reason: str):
    if not condition:
        raise RelationError(reason)


def _text(value, where: str) -> str:
    _require(isinstance(value, str) and 0 < len(value) <= 65536, f"invalid {where}")
    return value


def _id(value, where: str) -> str:
    value = _text(value, where)
    _require(re.fullmatch(r"[A-Za-z][A-Za-z0-9._:/-]*", value) is not None, f"invalid {where}")
    return value


def _ids(value, minimum: int, maximum: int, where: str) -> tuple[str, ...]:
    _require(type(value) in (list, tuple) and minimum <= len(value) <= maximum,
             f"{where} requires {minimum}..{maximum} IDs")
    ids = tuple(_id(item, where) for item in value)
    _require(len(set(ids)) == len(ids), f"duplicate {where}")
    return ids


def _records(graph: dict, family: str, count: int) -> dict:
    records = graph.get(family)
    _require(type(records) in (list, tuple) and len(records) == count,
             f"method requires {count} {family} records")
    return _index(records, family)


def _bounded_records(graph: dict, family: str, minimum: int, maximum: int) -> dict:
    records = graph.get(family)
    _require(type(records) in (list, tuple) and minimum <= len(records) <= maximum,
             f"method requires {minimum}..{maximum} {family} records")
    return _index(records, family)


def _index(records, family: str) -> dict:
    result = {}
    for record in records:
        _require(isinstance(record, dict), f"invalid {family} record")
        rid = _id(record.get("id"), family + " id")
        _require(rid not in result, f"duplicate {family} id")
        result[rid] = record
    return result


def _plan(graph: dict, execution: E.ExecutionPlan) -> RelationPlan:
    properties = _bounded_records(graph, "property", 1, MAX_PROPERTIES)
    controls = _records(graph, "control_run", 1)
    pairs = _records(graph, "producer_pair", 2)
    declared, witnessed = [], set()
    for prop in properties.values():
        _require(_ids(prop.get("observation_kinds"), 1, 1, "observation_kinds") == ("gpr-change",),
                 "method supports only GPR-change properties")
        witness = prop.get("gpr_witness")
        _require(isinstance(witness, dict) and len(witness) == 2
                 and set(witness) == {"step_n", "register"}, "method requires typed GPR witness")
        step, register = witness["step_n"], witness["register"]
        _require(type(step) is int and 0 <= step < execution.instructions, "witness outside parent budget")
        _require(isinstance(register, str) and re.fullmatch(r"x([1-9]|[12][0-9]|3[01])", register) is not None,
                 "witness requires canonical x1..31")
        _require((step, register) not in witnessed, "two properties witness one observation")
        witnessed.add((step, register))
        declared.append(PropertyRelation(prop["id"], GprWitness(step, register)))
    baseline, _repeat, control_run = execution.runs
    control = next(iter(controls.values()))
    _require(control.get("baseline_id") == baseline.run_id and control.get("run_id") == control_run.run_id,
             "control must name sole baseline/control runs")
    selected = _ids(control.get("property_ids"), 1, 1, "control property_ids")[0]
    _require(selected in properties,
             "control must name one declared property")
    control_witness = next(item.witness for item in declared if item.property_id == selected)
    _require(_ids(control.get("mutation_input_ids"), 1, 1, "control mutation_input_ids") == (control_run.expectation_id,),
             "control must name sole mutant expectation")
    _require(control.get("expected_verdict") == "DIVERGE", "method requires intended DIVERGE control")
    observed = _text(control.get("observed_verdict"), "control observed_verdict")
    _require(observed in VERDICTS, "invalid control observed_verdict")
    # Execution already bounded/identified these three runs; verdicts remain data.
    raw_control = next(run for run in graph["run"] if run["id"] == control_run.run_id)
    _require(observed == raw_control.get("verdict"), "control recorded verdict differs from run")

    producers = {record["id"]: record for record in graph["producer"]}
    base_producer = producers[baseline.expected_producer_id]
    mutant_producer = producers[control_run.expected_producer_id]
    _require("candidate_id" not in base_producer and "candidate_id" not in mutant_producer,
             "expected producer is not an external candidate")
    version = _text(base_producer.get("version"), "expected version")
    _require(_text(mutant_producer.get("version"), "mutant expected version") == version,
             "expected producer versions differ")
    base_inputs = set(_ids(base_producer.get("input_ids"), 1, 8, "baseline expected input_ids"))
    mutant_inputs = set(_ids(mutant_producer.get("input_ids"), 1, 8, "mutant expected input_ids"))
    common = {item.input_id for item in execution.common_inputs}
    _require(base_inputs <= common | {baseline.expectation_id}
             and mutant_inputs <= common | {control_run.expectation_id},
             "expected producer consumes nonselected input")
    _require(baseline.expectation_id in base_inputs and control_run.expectation_id in mutant_inputs,
             "expected producer must consume selected expectation")
    derivation_inputs = base_inputs - {baseline.expectation_id}
    _require(derivation_inputs == mutant_inputs - {control_run.expectation_id},
             "expected derivation changes other inputs")

    reference_id = execution.reference_producer_id
    reference_inputs = set(producers[reference_id]["input_ids"])
    needed = {frozenset((reference_id, baseline.expected_producer_id)),
              frozenset((reference_id, control_run.expected_producer_id))}
    actual, bindings = set(), []
    for pair in pairs.values():
        left, right = _id(pair.get("left"), "pair left"), _id(pair.get("right"), "pair right")
        endpoints = frozenset((left, right))
        _require(endpoints in needed and endpoints not in actual, "pair must assess each actual run producer pair once")
        actual.add(endpoints)
        expected_inputs = base_inputs if baseline.expected_producer_id in endpoints else mutant_inputs
        shared = _ids(pair.get("shared_input_ids"), 0, 7, "pair shared_input_ids")
        _require(set(shared) == reference_inputs & expected_inputs, "pair sharing differs from declared input intersection")
        assessment = _text(pair.get("assessment"), "pair assessment")
        _require(assessment in ASSESSMENTS, "invalid pair assessment")
        bindings.append(PairBinding(pair["id"], left, right, _text(pair.get("subsystem"), "pair subsystem"),
                                    assessment, tuple(sorted(shared)), _text(pair.get("evidence"), "pair evidence"),
                                    _text(pair.get("consequence"), "pair consequence")))
    # Exactly two distinct members of the two needed endpoints establish coverage.
    return RelationPlan(execution, tuple(declared), selected, control_witness, control["id"], observed,
                        version, tuple(sorted(derivation_inputs)), tuple(sorted(bindings, key=lambda pair: pair.pair_id)))


def bind_relations(experiment: dict, current_candidate: dict) -> RelationCheck:
    """Bind declarations only; matched is neither authenticated nor qualified."""
    execution = E.bind_execution(experiment, current_candidate)
    if execution.disposition != "matched":
        return RelationCheck(execution.disposition, "execution: " + execution.reason)
    try:
        plan = _plan(experiment["verification"], execution.plan)
    except RelationError as exc:
        return RelationCheck("refused", str(exc))
    except (KeyError, TypeError, ValueError, StopIteration) as exc:
        return RelationCheck("refused", f"malformed selected context: {type(exc).__name__}")
    return RelationCheck("matched", "declared method relations bind; authentication/comparison/qualification pending", plan)
