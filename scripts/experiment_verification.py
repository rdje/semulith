#!/usr/bin/env python3
"""Identity and declared-edge checks for matched-GPR capture records.

The public entrypoint receives a raw experiment form: schema validation precedes
the single dossier mapping, so duplicate fields cannot disappear before checking.
An empty issue list means these relationships are consistent, never qualification.
Artifact authentication, execution/comparison and policy adequacy remain separate.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from pathlib import Path, PurePosixPath

import check_sexp_schema as K
import dossier_sexp as D
import records_sexp as R
import sexp as S

ROOT = Path(__file__).resolve().parent.parent
FAMILIES = ("property", "input", "producer", "observation", "run", "control_run", "producer_pair")


@dataclass(frozen=True)
class Scope:
    profile_id: str
    candidate_ids: frozenset[str]
    requirement_ids: frozenset[str]
    obligation_ids: frozenset[str]


def load_scope(directory: Path, profile_id: str, candidate_ids: set[str]) -> Scope:
    """Use the existing public effective-contract measurement, with profile filtering.

    Catalogue/contract shape and integrity are owned by RECORD-SCHEMA and
    CONTRACT-FREEZE. Missing/unreadable scope is an error, never an empty success.
    """
    from gate_report import contract_measure

    requirements = R.load(directory / "requirements.sexp")
    obligations = R.load(directory / "contract-obligations.sexp")
    declared, _ = contract_measure(directory, obligations)
    effective = {oid for oid, _ in declared}
    return Scope(profile_id, frozenset(candidate_ids),
                 frozenset(r["id"] for r in requirements if profile_id in r["profile_ids"]),
                 frozenset(o["id"] for o in obligations
                           if o["id"] in effective and profile_id in o["profile_ids"]))


@lru_cache(maxsize=1)
def _schema():
    return K.load_schema(ROOT / "schema/references.sexp")


def is_canonical_path(raw: str) -> bool:
    path = PurePosixPath(raw)
    return (bool(raw) and not path.is_absolute() and path.as_posix() == raw
            and raw != "." and ".." not in path.parts and "\\" not in raw
            and ":" not in raw and not any(ord(c) < 32 or 127 <= ord(c) <= 159 for c in raw))


def check_experiment(form: list, scope: Scope) -> list[str]:
    """Return deterministic named shape/identity/edge findings for one raw form."""
    if not isinstance(form, list) or not form or form[0] != "experiment":
        return ["VERIFICATION SHAPE: expected an experiment form"]
    constructs, operators = _schema()
    errors = K.validate_text(R.render_forms([form]), constructs, operators,
                             "experiment", parse_where="experiment")
    if errors:
        return ["VERIFICATION SHAPE: " + error for error in errors]
    experiment = D.references_to_doc([S.Symbol("references"), form])["experiment"][0]
    if "verification" not in experiment:
        return []
    graph = experiment["verification"]
    issues: list[str] = []

    def issue(code: str, detail: str):
        issues.append(f"VERIFICATION {code}: {detail}")

    indexes = {}
    for family in FAMILIES:
        index = {}
        for record in graph[family]:
            rid = record["id"]
            if rid in index:
                issue("DUPLICATE ID", f"{family}/{rid}")
            index[rid] = record
        indexes[family] = index
    if issues:
        return issues  # A conflicting identity has no well-defined endpoint.

    def resolve(ids, index, edge):
        for rid in ids:
            if rid not in index:
                issue("UNKNOWN EDGE", f"{edge} -> {rid}")

    properties, inputs = indexes["property"], indexes["input"]
    producers, observations = indexes["producer"], indexes["observation"]
    runs = indexes["run"]
    models = set(experiment["models"])
    if len(models) != len(experiment["models"]) or not models <= scope.candidate_ids:
        issue("MODEL SCOPE", "models must be distinct declared candidates")
    for prop in properties.values():
        if prop["requirement_id"] not in scope.requirement_ids:
            issue("REQUIREMENT SCOPE", prop["id"] + " -> " + prop["requirement_id"])
        for oid in prop["obligation_ids"]:
            if oid not in scope.obligation_ids:
                issue("OBLIGATION SCOPE", prop["id"] + " -> " + oid)
        witness = prop.get("gpr_witness")
        if witness is not None:
            if not 0 <= witness["step_n"] < experiment["instructions"]:
                issue("GPR WITNESS BUDGET", prop["id"] + ": step outside declared budget")
            if "gpr-change" not in prop["observation_kinds"]:
                issue("GPR WITNESS KIND", prop["id"] + ": needs gpr-change observation")

    paths = {}
    for family in ("input", "observation"):
        for record in indexes[family].values():
            raw = record["path"]
            if not is_canonical_path(raw):
                issue("PATH", f"{family}/{record['id']}: noncanonical relative path {raw!r}")
            if raw in paths:
                issue("PATH ALIAS", f"{family}/{record['id']} and {paths[raw]}: {raw}")
            paths[raw] = family + "/" + record["id"]
            if family == "observation" and record["byte_size"] < 0:
                issue("BYTE SIZE", record["id"] + ": negative size")

    reference_candidates = []
    for producer in producers.values():
        pid = producer["id"]
        resolve(producer["input_ids"], inputs, "producer/" + pid)
        shared = set(producer.get("shared_input_ids", []))
        if not shared <= set(producer["input_ids"]):
            issue("PRODUCER SHARING", pid + ": shared inputs must be own inputs")
        if producer["role"] == "reference":
            candidate = producer.get("candidate_id")
            if candidate not in models:
                issue("PRODUCER CANDIDATE", pid + ": reference must name an experiment model")
            reference_candidates.append(candidate)
        elif "candidate_id" in producer:
            issue("PRODUCER CANDIDATE", pid + ": expected producer is not an external candidate")
    if set(reference_candidates) != models or len(reference_candidates) != len(models):
        issue("REFERENCE COVERAGE", "each experiment model needs exactly one reference producer")

    observation_owners = {}
    required_pairs = set()
    for run in runs.values():
        rid = run["id"]
        resolve(run["input_ids"], inputs, "run/" + rid + "/input")
        resolve(run["producer_ids"], producers, "run/" + rid + "/producer")
        resolve(run["observation_ids"], observations, "run/" + rid + "/observation")
        active = [producers[p] for p in run["producer_ids"] if p in producers]
        if {p["role"] for p in active} != {"reference", "expected"}:
            issue("RUN PRODUCERS", rid + ": needs reference and expected producers")
        for producer in active:
            if not set(producer["input_ids"]) <= set(run["input_ids"]):
                issue("RUN INPUTS", rid + ": missing producer inputs for " + producer["id"])
        required_pairs.update(frozenset(pair) for pair in combinations(run["producer_ids"], 2))
        for oid in run["observation_ids"]:
            if oid in observation_owners:
                issue("OBSERVATION OWNER", oid + ": reused by " + observation_owners[oid] + "/" + rid)
            observation_owners[oid] = rid
        parent = run.get("repeat_of")
        if run["kind"] == "repeat":
            baseline = runs.get(parent)
            if baseline is None or baseline["kind"] != "baseline":
                issue("REPEAT EDGE", rid + ": must name a baseline")
            elif (set(run["input_ids"]) != set(baseline["input_ids"])
                  or set(run["producer_ids"]) != set(baseline["producer_ids"])):
                issue("REPEAT INPUTS", rid + ": baseline inputs/producers differ")
        elif parent is not None:
            issue("REPEAT EDGE", rid + ": only a repeat may carry repeat_of")
    if {r["kind"] for r in runs.values()} != {"baseline", "repeat", "control"}:
        issue("RUN KINDS", "baseline, repeat and control runs are required")
    for oid in sorted(observations.keys() - observation_owners.keys()):
        issue("OBSERVATION OWNER", oid + ": no run produces it")

    controlled_runs = set()
    for control in indexes["control_run"].values():
        cid = control["id"]
        if "baseline_id" in control:
            control_baseline = runs.get(control["baseline_id"])
            if control_baseline is None or control_baseline["kind"] != "baseline":
                issue("CONTROL BASELINE", cid + ": must name a baseline run")
        run = runs.get(control["run_id"])
        if run is None or run["kind"] != "control":
            issue("CONTROL EDGE", cid + ": must name a control run")
        else:
            controlled_runs.add(run["id"])
            if not set(control["mutation_input_ids"]) <= set(run["input_ids"]):
                issue("CONTROL INPUTS", cid + ": mutations must be run inputs")
            if control["observed_verdict"] != run["verdict"]:
                issue("CONTROL VERDICT", cid + ": recorded verdict differs from run")
        resolve(control["mutation_input_ids"], inputs, "control/" + cid + "/mutation")
        resolve(control["property_ids"], properties, "control/" + cid + "/property")
    for rid in sorted(r["id"] for r in runs.values() if r["kind"] == "control"):
        if rid not in controlled_runs:
            issue("CONTROL EDGE", rid + ": no control record")

    examined, assessments = set(), set()
    for pair in indexes["producer_pair"].values():
        left, right = pair["left"], pair["right"]
        resolve((left, right), producers, "pair/" + pair["id"])
        endpoints = frozenset((left, right))
        if len(endpoints) != 2:
            issue("PAIR EDGE", pair["id"] + ": needs distinct producers")
        key = (pair["subsystem"], endpoints)
        if key in assessments:
            issue("PAIR DUPLICATE", pair["id"] + ": pair/subsystem already assessed")
        assessments.add(key)
        examined.add(endpoints)
        if left in producers and right in producers:
            overlap = set(producers[left]["input_ids"]) & set(producers[right]["input_ids"])
            if set(pair.get("shared_input_ids", [])) != overlap:
                issue("PAIR SHARING", pair["id"] + ": must record the declared input intersection")
    for pair in sorted(required_pairs - examined, key=lambda p: sorted(p)):
        issue("PAIR MISSING", "/".join(sorted(pair)))
    return issues
