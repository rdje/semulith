#!/usr/bin/env python3
"""Offline shape/mapping controls for the prospective matched-GPR capture graph.

These synthetic pins and observations are not execution evidence. No artifacts are
read or created. DOSSIER-SCHEMA owns the outer named arms; qualification stays closed
in PROFILE-CONSISTENCY pending separate comparison and policy evaluation.
"""
from __future__ import annotations

import argparse
import copy
from pathlib import Path

import check_sexp_schema as K
import dossier_sexp as D
import records_sexp as R
import sexp as S

ROOT = Path(__file__).resolve().parent.parent
CASES = ("complete", "roundtrip", "legacy", "unknown", "type", "arity", "duplicate",
         "missing", "collection", "digest", "version", "unique", "vocabulary",
         "mapper-refusal")
REPEATED_SCALARS = {"limitations", "obligation_ids", "observation_kinds", "input_ids",
                    "shared_input_ids", "argv", "producer_ids", "observation_ids",
                    "mutation_input_ids", "property_ids"}
OPTIONAL_SCALARS = {"candidate_id", "repeat_of", "shared_input_ids"}


def fixture() -> dict:
    """Exercise every field, multiple records per child and ordered repeated argv."""
    graph = {
        "format_version": "matched-gpr-v1", "comparison_rule": "fixture-gpr-and-delivery",
        "limitations": ["synthetic structure only", "no architectural equivalence claim"],
        "property": [], "input": [], "producer": [], "observation": [], "run": [],
        "control_run": [], "producer_pair": [],
    }
    for n in (1, 2):
        graph["property"].append({
            "id": f"property-{n}", "requirement_id": f"REQ-{n}",
            "obligation_ids": [f"OBL-{n}a", f"OBL-{n}b"],
            "observation_kinds": ["gpr-change", "witnessed-delivery"],
            "statement": f"fixture property {n}",
        })
        graph["input"].append({"id": f"input-{n}", "role": f"fixture-role-{n}",
                               "path": f"target/fixture/input-{n}", "sha256": str(n) * 64})
        graph["producer"].append({
            "id": f"producer-{n}", "role": "reference" if n == 1 else "expected",
            "version": f"fixture-{n}", "input_ids": [f"input-{n}"],
            "shared_input_ids": ["input-1"],
            **({"candidate_id": "c1"} if n == 1 else {}),
        })
        for kind in ("baseline", "repeat", "control"):
            rid = f"{kind}-{n}"
            verdict = "DIVERGE" if kind == "control" else "AGREE"
            graph["observation"].append({
                "id": f"observation-{rid}", "role": "raw-gpr", "byte_size": n,
                "path": f"target/fixture/{rid}.trace", "sha256": str(n) * 64,
            })
            graph["run"].append({
                "id": rid, "kind": kind, "argv": ["fixture-runner", "same", "", "same"],
                "input_ids": ["input-1", "input-2"],
                "producer_ids": ["producer-1", "producer-2"],
                "process_exit": 0, "verdict": verdict,
                "observation_ids": [f"observation-{rid}"],
                **({"repeat_of": f"baseline-{n}"} if kind == "repeat" else {}),
            })
        graph["control_run"].append({
            "id": f"control-record-{n}", "run_id": f"control-{n}",
            "mutation_input_ids": [f"input-{n}"], "property_ids": [f"property-{n}"],
            "expected_verdict": "DIVERGE", "observed_verdict": "DIVERGE",
            "reason": f"synthetic wrong value {n}",
        })
        graph["producer_pair"].append({
            "id": f"pair-{n}", "left": "producer-1", "right": "producer-2",
            "subsystem": f"fixture-{n}", "assessment": "not-examined",
            "shared_input_ids": ["input-1"], "evidence": "ancestry unknown",
            "consequence": "no independence credit",
        })
    return {
        "profile": "p1", "retrieved": "fixture", "work_dir": "target/fixture",
        "host": {"os": "fixture", "kernel": "fixture", "arch": "fixture", "cxx": "fixture"},
        "candidate": [{"id": "c1", "role": "reference", "status": "not obtained",
                       "origin": "fixture", "lineage": "unknown"}],
        "experiment": [{"id": "e1", "program": "fixture.s", "instructions": 1,
                        "models": ["c1"], "verdict": "AGREE", "reproduced": "fixture",
                        "control": "synthetic only", "verification": graph}],
    }


def only(form, head):
    children = S.children(form, head)
    if len(children) != 1:
        raise ValueError(f"fixture expected one {head}, got {len(children)}")
    return children[0]


def graph(form):
    return only(only(form, "experiment"), "verification")


def nodes(form):
    block = graph(form)
    return [block, *[child for child in block[1:]
                     if isinstance(child, list) and child[0] in {
                         "property", "input", "producer", "observation", "run",
                         "control_run", "producer_pair"}]]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_case(case: str):
    constructs, operators = K.load_schema(ROOT / "schema/references.sexp")
    form = D.references_to_form(fixture())

    def errors(changed):
        return K.validate_text(R.render_forms([changed]), constructs, operators,
                               "verification-fixture", parse_where="verification-fixture")

    def refuses(changed, reason):
        found = errors(changed)
        require(any(reason in item for item in found),
                f"expected refusal {reason!r}, got {found}")

    if case == "complete":
        require(not errors(form), f"complete fixture refused: {errors(form)}")
    elif case == "roundtrip":
        # Compare the independently constructed data, not the writer with itself.
        parsed = S.parse(R.render_forms([form]))[0]
        require(D.references_to_doc(parsed) == fixture(), "nested data lost or changed")
    elif case == "legacy":
        count = experiments = 0
        for path in sorted((ROOT / "profiles").glob("*/references.sexp")):
            original = D.load_references(path)
            if "experiment" in original:
                original["experiment"] = [x for x in original["experiment"]
                                           if "verification" not in x]
                experiments += len(original["experiment"])
                if not original["experiment"]:
                    del original["experiment"]
            reread = D.references_to_doc(S.parse(R.render_forms([
                D.references_to_form(original)]))[0])
            require(reread == original, f"legacy dictionary changed: {path.relative_to(ROOT)}")
            count += 1
        require(count > 0 and experiments > 0, "legacy experiment corpus is empty")
    elif case == "unknown":
        for index, node in enumerate(nodes(form)):
            changed = copy.deepcopy(form)
            target = nodes(changed)[index]
            target.append([S.Symbol("unexpected_capture_field"), "bad"])
            refuses(changed, 'undeclared field "unexpected_capture_field"')
    elif case in {"type", "arity", "duplicate", "missing"}:
        # Independent contract vocabulary: all repeated/optional scalar fields.
        for index, node in enumerate(nodes(form)):
            seen = set()
            for field_index, original in enumerate(node[1:], 1):
                head = original[0]
                if len(original) != 2 or isinstance(original[1], list) or head in seen:
                    continue
                seen.add(head)
                if case == "duplicate" and head in REPEATED_SCALARS:
                    continue
                if case == "missing" and (head in REPEATED_SCALARS or head in OPTIONAL_SCALARS):
                    continue
                changed = copy.deepcopy(form)
                target = nodes(changed)[index]
                field = target[field_index]
                if case == "type":
                    field[1] = "bad-integer" if isinstance(original[1], int) else 123
                    reason = "want integer" if isinstance(original[1], int) else "want string"
                elif case == "arity":
                    field.append("extra")
                    reason = "wrong arity"
                elif case == "duplicate":
                    target.append(copy.deepcopy(field))
                    reason = "duplicated single-valued field"
                else:
                    target.remove(field)
                    reason = "missing required field"
                refuses(changed, reason)
    elif case == "collection":
        for head in ("property", "input", "producer", "observation", "run",
                     "control_run", "producer_pair", "limitations"):
            changed = copy.deepcopy(form)
            block = graph(changed)
            block[:] = [c for c in block if not isinstance(c, list) or c[0] != head]
            refuses(changed, f'field "{head}"')
        for index, node in enumerate(nodes(form)):
            for head in sorted({c[0] for c in node[1:]} &
                               (REPEATED_SCALARS - OPTIONAL_SCALARS)):
                changed = copy.deepcopy(form)
                target = nodes(changed)[index]
                target[:] = [c for c in target if not isinstance(c, list) or c[0] != head]
                refuses(changed, f'field "{head}"')
    elif case == "digest":
        for head in ("input", "observation"):
            changed = copy.deepcopy(form)
            only(S.children(graph(changed), head)[0], "sha256")[1] = "bad"
            refuses(changed, "does not match")
    elif case == "version":
        only(graph(form), "format_version")[1] = "matched-gpr-v999"
        refuses(form, "does not match")
    elif case == "unique":
        for index, node in enumerate(nodes(form)):
            for field in sorted({c[0] for c in node[1:]} & (REPEATED_SCALARS - {"argv"})):
                changed = copy.deepcopy(form)
                target = nodes(changed)[index]
                target.append(copy.deepcopy(S.children(target, field)[0]))
                refuses(changed, "unique means written once")
    elif case == "vocabulary":
        for head, field in (("property", "observation_kinds"), ("producer", "role"),
                            ("run", "kind"), ("run", "verdict"),
                            ("control_run", "expected_verdict"),
                            ("control_run", "observed_verdict"),
                            ("producer_pair", "assessment")):
            changed = copy.deepcopy(form)
            target = S.children(graph(changed), head)[0]
            S.children(target, field)[0][1] = "unsupported"
            refuses(changed, "does not match")
    elif case == "mapper-refusal":
        for index in range(len(nodes(form))):
            changed = copy.deepcopy(form)
            nodes(changed)[index].append([S.Symbol("unexpected_capture_field"), "bad"])
            try:
                D.references_to_doc(changed)
            except D.DossierError as error:
                require("unexpected_capture_field" in str(error), str(error))
            else:
                raise ValueError("mapper ignored an unknown nested field")
        experiment = only(form, "experiment")
        experiment.append(copy.deepcopy(graph(form)))
        try:
            D.references_to_doc(form)
        except D.DossierError as error:
            require("appears 2 times" in str(error), str(error))
        else:
            raise ValueError("mapper ignored duplicate verification blocks")
    else:
        raise ValueError(f"unknown case: {case}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--case", choices=CASES)
    mode.add_argument("--emit-experiment", action="store_true")
    args = parser.parse_args()
    try:
        if args.emit_experiment:
            print(R.render_forms(S.children(D.references_to_form(fixture()), "experiment")), end="")
        else:
            check_case(args.case)
            print(f"VERIFICATION {args.case}: ok")
    except (ValueError, D.DossierError, K.SchemaError, S.SexpError) as error:
        print(f"VERIFICATION {args.case}: FAILED: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
