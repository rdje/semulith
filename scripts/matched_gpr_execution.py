#!/usr/bin/env python3
"""Pure first-method execution bindings, before artifact or comparison checks.

The caller supplies the raw-schema/scoped-graph-validated canonical dictionary.
This unit binds selected identities and argv, never authenticates files or runs
them. Property/control/expected-derivation/pair checks remain separate, as do
complete method budgets, provenance, comparison and policy qualification.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

from experiment_verification import is_canonical_path
from matched_gpr_comparison import MAX_BOUNDARIES

COMMON_ROLES = ("guest-source", "guest-image", "reference-config", "reference-identity",
                "collector", "adapter", "dependency-manifest")
PRINCIPAL_ROLES = frozenset((*COMMON_ROLES, "expectation"))
OUTPUT_ROLES = ("raw-gpr", "process-stdout", "process-stderr", "process-receipt")
RUN_KINDS = ("baseline", "repeat", "control")


@dataclass(frozen=True)
class InputBinding:
    role: str
    input_id: str
    path: str
    sha256: str


@dataclass(frozen=True)
class RunBinding:
    kind: str
    run_id: str
    expected_producer_id: str
    expectation_id: str
    argv: tuple[str, ...]
    observations: tuple[tuple[str, str], ...]  # role / ID


@dataclass(frozen=True)
class ExecutionPlan:
    instructions: int
    binary_path: str
    binary_sha256: str
    reference_producer_id: str
    common_inputs: tuple[InputBinding, ...]
    baseline_expectation: InputBinding
    control_expectation: InputBinding
    runs: tuple[RunBinding, ...]


@dataclass(frozen=True)
class ExecutionCheck:
    disposition: str  # matched / unsupported / refused; never method success
    reason: str
    plan: ExecutionPlan | None = None


class ExecutionError(ValueError):
    """This finite execution relationship cannot be established."""


def _require(condition: bool, reason: str):
    if not condition:
        raise ExecutionError(reason)


def _text(value, where: str) -> str:
    _require(isinstance(value, str) and 0 < len(value) <= 65536, f"invalid {where}")
    return value


def _id(value, where: str) -> str:
    value = _text(value, where)
    _require(re.fullmatch(r"[A-Za-z][A-Za-z0-9._:/-]*", value) is not None, f"invalid {where}")
    return value


def _path(value, where: str) -> str:
    value = _text(value, where)
    _require(is_canonical_path(value), f"noncanonical {where}")
    return value


def _digest(value, where: str) -> str:
    value = _text(value, where)
    _require(re.fullmatch(r"[0-9a-f]{64}", value) is not None, f"invalid {where}")
    return value


def _ids(value, minimum: int, maximum: int, where: str) -> tuple[str, ...]:
    _require(type(value) in (list, tuple) and minimum <= len(value) <= maximum,
             f"{where} requires {minimum}..{maximum} IDs")
    ids = tuple(_id(rid, where) for rid in value)
    _require(len(set(ids)) == len(ids), f"duplicate {where}")
    return ids


def _index(graph: dict, family: str, count: int) -> dict:
    records = graph.get(family)
    _require(type(records) in (list, tuple) and len(records) == count,
             f"method requires {count} {family} records")
    index = {}
    for record in records:
        _require(isinstance(record, dict), f"invalid {family} record")
        rid = _id(record.get("id"), family + " id")
        _require(rid not in index, f"duplicate {family} id")
        index[rid] = record
    return index


def _input(record: dict) -> InputBinding:
    return InputBinding(_text(record.get("role"), "input role"), record["id"],
                        _path(record.get("path"), "input path"),
                        _digest(record.get("sha256"), "input sha256"))


def _plan(experiment: dict, graph: dict, candidate: dict) -> ExecutionPlan:
    count = experiment.get("instructions")
    _require(type(count) is int and 1 <= count <= MAX_BOUNDARIES,
             f"parent budget requires 1..{MAX_BOUNDARIES} boundaries")
    _require(_ids(experiment.get("models"), 1, 1, "models") == ("sail-riscv",),
             "method requires sole model sail-riscv")
    _require(isinstance(candidate, dict) and candidate.get("id") == "sail-riscv",
             "method requires current candidate sail-riscv")
    binary = _path(candidate.get("binary"), "candidate binary")
    binary_sha = _digest(candidate.get("binary_sha256"), "candidate binary_sha256")
    # Exact counts precede map construction. Caller dictionary allocation is not
    # covered by this bound; the complete method must bound the parent payload.
    inputs = {rid: _input(record) for rid, record in _index(graph, "input", 9).items()}
    observations = _index(graph, "observation", 12)
    runs = _index(graph, "run", 3)
    producers = _index(graph, "producer", 3)
    paths = [item.path for item in inputs.values()]
    for record in observations.values():
        _require(record.get("role") in OUTPUT_ROLES, "invalid output role")
        paths.append(_path(record.get("path"), "observation path"))
        _digest(record.get("sha256"), "observation sha256")
        size = record.get("byte_size")
        _require(type(size) is int and size >= 0, "invalid observation byte_size")
    _require(len(set(paths)) == len(paths), "input/output path alias")
    roles = [item.role for item in inputs.values()]
    _require(set(roles) == PRINCIPAL_ROLES and roles.count("expectation") == 2
             and all(roles.count(role) == 1 for role in COMMON_ROLES), "invalid principal input roles")
    reference = [p for p in producers.values() if p.get("role") == "reference"]
    expected = [p for p in producers.values() if p.get("role") == "expected"]
    _require(len(reference) == 1 and len(expected) == 2, "one reference/two expected producers required")
    reference = reference[0]
    _require(reference.get("candidate_id") == "sail-riscv"
             and reference.get("version") == "sha256:" + binary_sha,
             "reference candidate/version differs from binary pin")
    by_kind = {run.get("kind"): run for run in runs.values()}
    _require(set(by_kind) == set(RUN_KINDS), "one baseline/repeat/control run required")
    selected, expected_ids, owned, bindings = {}, {}, set(), []
    for kind in RUN_KINDS:
        run = by_kind[kind]
        ids = _ids(run.get("input_ids"), 8, 8, kind + " input_ids")
        _require(set(ids) <= inputs.keys(), "unknown run input")
        selected[kind] = {inputs[rid].role: inputs[rid] for rid in ids}
        _require(len(selected[kind]) == 8 and set(selected[kind]) == PRINCIPAL_ROLES,
                 "run requires one of each principal role")
        active_ids = _ids(run.get("producer_ids"), 2, 2, kind + " producer_ids")
        _require(set(active_ids) <= producers.keys() and reference["id"] in active_ids,
                 "run requires the sole reference producer")
        other = next(pid for pid in active_ids if pid != reference["id"])
        _require(producers[other].get("role") == "expected", "run requires one expected producer")
        expected_ids[kind] = other
        if kind == "repeat":
            _require(run.get("repeat_of") == by_kind["baseline"]["id"], "repeat must name baseline")
        else:
            _require("repeat_of" not in run, "spurious repeat edge")
        oids = _ids(run.get("observation_ids"), 4, 4, kind + " observation_ids")
        _require(set(oids) <= observations.keys(), "unknown run observation")
        _require(not owned.intersection(oids), "reused run observation")
        owned.update(oids)
        outputs = {observations[oid]["role"]: observations[oid] for oid in oids}
        _require(len(outputs) == 4 and set(outputs) == set(OUTPUT_ROLES), "run needs all four output roles")
        argv = (binary, "--config-override", selected[kind]["reference-config"].path,
                "--inst-limit", str(count), "--trace-instr", "--trace-gpr", "--trace-exception",
                "--trace-output", outputs["raw-gpr"]["path"], selected[kind]["guest-image"].path)
        actual = run.get("argv")
        _require(type(actual) in (list, tuple) and len(actual) == 11 and tuple(actual) == argv,
                 "run argv differs from fixed public invocation")
        bindings.append(RunBinding(kind, run["id"], other, selected[kind]["expectation"].input_id,
                                   argv, tuple((role, outputs[role]["id"]) for role in OUTPUT_ROLES)))
    # Three disjoint four-output sets exhaust the twelve declared observations.
    baseline = selected["baseline"]
    _require(selected["repeat"] == baseline and expected_ids["repeat"] == expected_ids["baseline"],
             "repeat inputs/expected producer differ from baseline")
    # Global common-role uniqueness and per-run coverage bind the same seven
    # executed input identities, including the control's configuration/image.
    _require(selected["control"]["expectation"].input_id != baseline["expectation"].input_id,
             "control needs distinct expectation input")
    _require(expected_ids["control"] != expected_ids["baseline"], "control needs distinct expected producer")
    common_ids = {baseline[role].input_id for role in COMMON_ROLES}
    reference_inputs = _ids(reference.get("input_ids"), 1, 7, "reference input_ids")
    _require(set(reference_inputs) <= common_ids, "reference producer consumes noncommon input")
    return ExecutionPlan(count, binary, binary_sha, reference["id"],
                         tuple(baseline[role] for role in COMMON_ROLES), baseline["expectation"],
                         selected["control"]["expectation"], tuple(bindings))


def bind_execution(experiment: dict, current_candidate: dict) -> ExecutionCheck:
    """Compute partial execution bindings from validated canonical context only."""
    try:
        _require(isinstance(experiment, dict), "expected canonical experiment dictionary")
        graph = experiment.get("verification")
        if graph is None:
            return ExecutionCheck("unsupported", "legacy experiment has no verification envelope")
        _require(isinstance(graph, dict), "expected canonical verification dictionary")
        _require(graph.get("format_version") == "matched-gpr-v1", "unsupported verification envelope")
        if graph.get("comparison_rule") != "sail-gpr-change-v1":
            return ExecutionCheck("unsupported", "another comparison rule needs its own execution bindings")
        plan = _plan(experiment, graph, current_candidate)
    except ExecutionError as exc:
        return ExecutionCheck("refused", str(exc))
    except (KeyError, TypeError, ValueError) as exc:
        return ExecutionCheck("refused", f"malformed selected context: {type(exc).__name__}")
    return ExecutionCheck("matched", "declared execution binds; complete method/qualification pending", plan)
