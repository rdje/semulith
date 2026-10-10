#!/usr/bin/env python3
"""Offline identity/edge controls; synthetic records earn no qualification."""
from __future__ import annotations

import argparse
import copy
from pathlib import Path
import sys
import types

import dossier_sexp as D
import experiment_verification as V
import probe_experiment_verification as P
import sexp as S


def fixture():
    document = P.fixture()
    block = document["experiment"][0]["verification"]
    for producer in block["producer"]:
        producer["input_ids"] = ["input-1", "input-2"]
        producer["shared_input_ids"] = ["input-1", "input-2"]
    for pair in block["producer_pair"]:
        pair["shared_input_ids"] = ["input-1", "input-2"]
    return document


SCOPE = V.Scope("p1", frozenset({"c1"}), frozenset({"REQ-1", "REQ-2"}),
                frozenset({"OBL-1a", "OBL-1b", "OBL-2a", "OBL-2b"}))


def form(document):
    return S.children(D.references_to_form(document), "experiment")[0]


def run_controls() -> int:
    passed = failed = 0

    def judge(name, findings, reason=None):
        nonlocal passed, failed
        good = not findings if reason is None else any(reason in f for f in findings)
        if good:
            passed += 1
        else:
            failed += 1
            print(f"GRAPH MISS {name}: expected {reason or 'no issues'}, got {findings}")

    def mutation(name, change, reason):
        document = copy.deepcopy(fixture())
        change(document["experiment"][0]["verification"])
        judge(name, V.check_experiment(form(document), SCOPE), reason)

    def remove_baselines(graph):
        for run in graph["run"]:
            if run["kind"] == "baseline":
                run["kind"] = "control"

    def unused_mutation(graph):
        graph["input"].append({**graph["input"][0], "id": "unused-mutation",
                               "path": "target/fixture/unused"})
        graph["control_run"][0]["mutation_input_ids"] = ["unused-mutation"]

    def remove_assessments(graph):
        for pair in graph["producer_pair"]:
            pair.update(left="producer-1", right="producer-1")

    judge("complete declared graph", V.check_experiment(form(fixture()), SCOPE))
    document = fixture()
    graph = document["experiment"][0]["verification"]
    graph["property"][0]["gpr_witness"] = {"step_n": 0, "register": "x1"}
    graph["control_run"][0]["baseline_id"] = "baseline-1"
    judge("typed witness and control baseline", V.check_experiment(form(document), SCOPE))
    document["experiment"][0]["instructions"] = 9
    graph["property"][0]["gpr_witness"] = {"step_n": 8, "register": "x31"}
    judge("last declared witness boundary", V.check_experiment(form(document), SCOPE))
    graph["control_run"][0]["baseline_id"] = "baseline-2"
    judge("generic baseline edge may select another baseline", V.check_experiment(form(document), SCOPE))
    for step in (-1, 1, 2):
        mutation("witness step " + str(step), lambda g, n=step: g["property"][0].update(
            gpr_witness={"step_n": n, "register": "x1"}), "GPR WITNESS BUDGET")
    document = fixture()
    document["experiment"][0]["instructions"] = 0
    document["experiment"][0]["verification"]["property"][0]["gpr_witness"] = {
        "step_n": 0, "register": "x1"}
    judge("witness cannot fit empty budget", V.check_experiment(form(document), SCOPE),
          "GPR WITNESS BUDGET")
    mutation("GPR witness without GPR observation", lambda g: g["property"][0].update(
        observation_kinds=["witnessed-delivery"], gpr_witness={"step_n": 0, "register": "x1"}),
        "GPR WITNESS KIND")
    for baseline in ("missing", "control-1", "repeat-1"):
        mutation("control baseline " + baseline,
                 lambda g, b=baseline: g["control_run"][0].update(baseline_id=b), "CONTROL BASELINE")
    # A failed control remains honestly recordable. Adequacy is a later evaluation.
    document = fixture()
    graph = document["experiment"][0]["verification"]
    graph["control_run"][0]["observed_verdict"] = "AGREE"
    next(r for r in graph["run"] if r["id"] == "control-1")["verdict"] = "AGREE"
    judge("failed control is consistent data", V.check_experiment(form(document), SCOPE))
    # An ancestry assessment and shared experiment inputs describe different facts.
    document = fixture()
    document["experiment"][0]["verification"]["producer_pair"][0]["assessment"] = "not-shared"
    judge("shared inputs are explicit alongside ancestry assessment",
          V.check_experiment(form(document), SCOPE))

    for family in V.FAMILIES:
        mutation("duplicate " + family,
                 lambda g, f=family: g[f].append({**g[f][0], "id": g[f][0]["id"]}),
                 "DUPLICATE ID")
    mutation("foreign requirement", lambda g: g["property"][0].update(requirement_id="foreign"),
             "REQUIREMENT SCOPE")
    mutation("superseded or foreign obligation",
             lambda g: g["property"][0].update(obligation_ids=["old-obligation"]), "OBLIGATION SCOPE")
    mutation("unknown producer input", lambda g: g["producer"][0].update(input_ids=["missing"]),
             "UNKNOWN EDGE: producer/")
    mutation("invented candidate", lambda g: g["producer"][0].update(candidate_id="missing"),
             "PRODUCER CANDIDATE")
    mutation("expected producer disguised as candidate",
             lambda g: g["producer"][1].update(candidate_id="c1"), "PRODUCER CANDIDATE")
    mutation("two wrappers for one reference",
             lambda g: g["producer"].append({**g["producer"][0], "id": "wrapper"}),
             "REFERENCE COVERAGE")
    mutation("producer invents shared input",
             lambda g: g["producer"][0].update(shared_input_ids=["missing"]), "PRODUCER SHARING")
    for path in ("/foreign/file", "../file", "a/../file", "a//file", "a/./file", ".",
                 "C:/file", "a\\file", "a\nfile", "a\x85file"):
        mutation("unsafe path " + repr(path), lambda g, p=path: g["input"][0].update(path=p), "PATH:")
    mutation("input/output alias", lambda g: g["observation"][0].update(path=g["input"][0]["path"]),
             "PATH ALIAS")
    mutation("negative artifact size", lambda g: g["observation"][0].update(byte_size=-1), "BYTE SIZE")
    mutation("unknown run input", lambda g: g["run"][0].update(input_ids=["missing"]),
             "UNKNOWN EDGE: run/baseline-1/input")
    mutation("unknown run producer", lambda g: g["run"][0].update(producer_ids=["missing"]),
             "UNKNOWN EDGE: run/baseline-1/producer")
    mutation("no expected producer", lambda g: g["run"][0].update(producer_ids=["producer-1"]),
             "RUN PRODUCERS")
    mutation("run omits producer input", lambda g: g["run"][0].update(input_ids=["input-1"]),
             "RUN INPUTS")
    mutation("unknown observation", lambda g: g["run"][0].update(observation_ids=["missing"]),
             "UNKNOWN EDGE: run/baseline-1/observation")
    mutation("reused observation", lambda g: g["run"][1].update(
        observation_ids=g["run"][0]["observation_ids"]),
        "OBSERVATION OWNER: observation-baseline-1: reused")
    mutation("orphan observation", lambda g: g["observation"].append({
        **g["observation"][0], "id": "orphan", "path": "target/fixture/orphan.trace"}),
        "OBSERVATION OWNER: orphan")
    mutation("missing repeat parent", lambda g: g["run"][1].pop("repeat_of"), "REPEAT EDGE")
    mutation("self repeat", lambda g: g["run"][1].update(repeat_of="repeat-1"), "REPEAT EDGE")
    mutation("repeat names a control", lambda g: g["run"][1].update(repeat_of="control-1"), "REPEAT EDGE")
    mutation("baseline carries repeat edge", lambda g: g["run"][0].update(repeat_of="baseline-2"),
             "REPEAT EDGE")
    mutation("repeat changes input set", lambda g: g["run"][1].update(input_ids=["input-1"]),
             "REPEAT INPUTS")
    mutation("repeat changes producer set", lambda g: g["run"][1].update(producer_ids=["producer-1"]),
             "REPEAT INPUTS")
    mutation("no baseline kind", remove_baselines, "RUN KINDS")
    mutation("control names baseline", lambda g: g["control_run"][0].update(run_id="baseline-1"),
             "CONTROL EDGE: control-record-1: must name a control run")
    mutation("control names missing run", lambda g: g["control_run"][0].update(run_id="missing"),
             "CONTROL EDGE: control-record-1: must name a control run")
    mutation("unknown mutated input",
             lambda g: g["control_run"][0].update(mutation_input_ids=["missing"]),
             "UNKNOWN EDGE: control/")
    mutation("mutation is not run input", unused_mutation, "CONTROL INPUTS")
    mutation("unknown controlled property",
             lambda g: g["control_run"][0].update(property_ids=["missing"]),
             "UNKNOWN EDGE: control/")
    mutation("control verdict differs from run",
             lambda g: g["control_run"][0].update(observed_verdict="REFUSED"), "CONTROL VERDICT")
    mutation("control run has no record", lambda g: g["control_run"].pop(),
             "CONTROL EDGE: control-2: no control record")
    mutation("unknown pair endpoint", lambda g: g["producer_pair"][0].update(left="missing"),
             "UNKNOWN EDGE: pair/")
    mutation("pair refers to itself", lambda g: g["producer_pair"][0].update(right="producer-1"),
             "PAIR EDGE")
    mutation("conflicting pair identity", lambda g: g["producer_pair"].append({
        **g["producer_pair"][0], "id": "second-assessment", "assessment": "shared"}),
        "PAIR DUPLICATE")
    mutation("pair hides shared inputs", lambda g: g["producer_pair"][0].update(shared_input_ids=[]),
             "PAIR SHARING")
    mutation("pair invents shared input",
             lambda g: g["producer_pair"][0].update(shared_input_ids=["missing"]), "PAIR SHARING")
    mutation("actual pair has no assessment", remove_assessments, "PAIR MISSING")

    raw = form(fixture())
    block = S.children(raw, "verification")[0]
    first_input = S.children(block, "input")[0]
    first_input.append([S.Symbol("id"), "different-id"])
    judge("raw duplicate field before mapping", V.check_experiment(raw, SCOPE), "VERIFICATION SHAPE")
    raw = form(fixture())
    S.children(raw, "verification")[0].append([S.Symbol("unknown"), "bad"])
    judge("raw unknown field before mapping", V.check_experiment(raw, SCOPE), "VERIFICATION SHAPE")
    raw = form(fixture())
    S.children(raw, "models")[0][1] = "foreign"
    judge("experiment model scope", V.check_experiment(raw, SCOPE), "MODEL SCOPE")
    raw = form(fixture())
    raw[:] = [c for c in raw if not isinstance(c, list) or c[0] != "verification"]
    judge("legacy experiment unchanged", V.check_experiment(raw, SCOPE))

    directory = Path(__file__).resolve().parent.parent / "profiles/rv64gc-lab-v0"
    references = D.load_references(directory / "references.sexp")
    current = V.load_scope(directory, "rv64gc-lab-v0", {c["id"] for c in references["candidate"]})
    judge("canonical scope is nonempty", [] if current.requirement_ids and current.obligation_ids else ["empty scope"])
    judge("canonical scope selects effective FP successor",
          [] if "OB-FP-DEFER" not in current.obligation_ids
          and "OB-GC-FP-QUALIFIED-V2" in current.obligation_ids else ["wrong contract version"])
    judge("scope filters another profile", [] if not V.load_scope(directory, "foreign", set()).requirement_ids
          and not V.load_scope(directory, "foreign", set()).obligation_ids else ["cross-profile IDs"])
    print(f"EXPERIMENT-GRAPH: {passed} pass / {failed} fail")
    return 1 if failed else 0


def main():
    global V
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=("ignore-witness-budget", "ignore-witness-kind",
                                               "ignore-control-baseline"))
    args = parser.parse_args()
    if args.mutation:
        root = Path(__file__).resolve().parent.parent
        path = root / "scripts/experiment_verification.py"
        source = path.read_text()
        span = {"ignore-witness-budget": 'if not 0 <= witness["step_n"] < experiment["instructions"]:',
                "ignore-witness-kind": 'if "gpr-change" not in prop["observation_kinds"]:',
                "ignore-control-baseline": 'if control_baseline is None or control_baseline["kind"] != "baseline":'}[args.mutation]
        if source.count(span) != 1:
            raise ValueError("graph mutation must match exactly once: " + args.mutation)
        module = types.ModuleType("experiment_graph_mutant")
        module.__file__ = str(path)
        sys.modules[module.__name__] = module
        exec(compile(source.replace(span, "if False:"), str(path), "exec"), module.__dict__)
        V = module
    return run_controls()


if __name__ == "__main__":
    raise SystemExit(main())
