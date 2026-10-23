#!/usr/bin/env python3
"""Measure the retained DIV case against the evidence policy's legs; measurement only, no credit.

`profiles/<profile>/EVIDENCE_POLICY.md` names, for a `defined` requirement of low or medium
risk, the evidence a credited disposition needs. This consumer measures which of those legs
the retained bytes already satisfy, from the predeclaration, the expectation file, the
derived receipt, the dependency manifest and the catalogue, on top of the finite method
review (`review_div_method`). It reads bounded tracked files, launches no process, writes
nothing, and never grants credit: `credited` is always false. A satisfied measurement is
the input a later, separately owned crediting record would cite; a pending one names the
legs still missing.

Legs (policy sections "Source-semantic dispositions", "Risk and feature obligations",
"Records, controls and currentness"):

  source-located-expectations  every expectation step carries a derivation and a source; the
                               witness step cites the requirement's source; the expected
                               producer reads no reference-only input (no model output as
                               its own expectation).
  boundary-fixtures            directed boundary rows (a step whose source cites a table row)
                               are present AND each is predeclared as a property.
  matched-reference-comparison the finite method is satisfied and the baseline agrees under
                               the declared comparison rule and named observation vocabulary.
  repeated-execution           a repeat run agrees.
  discriminating-control       the control diverges at the step and register of the one property
                               the control_run names — it fails for the stated reason (wrong
                               defined result).
  record-linkage               requirement, effective obligation, tracked runner, expectation
                               producer, receipt identity and limitations are all named.
  currentness                  the policy document is pinned by the dependency manifest and
                               its current bytes equal the pin; the method binding matched.
  risk-method                  low/medium risk needs no second method; high/critical does,
                               and no declaration vocabulary exists yet for it.
  feature-rules                the obligation's feature disposition is declared below.
  form-coverage                every form the requirement names is exercised AND predeclared.

Exit 0: measured (satisfied, pending or invalidated). Exit 1: a finding — the receipt
claims `qualification` the legs refuse, or the finite method is refused, unavailable or
unsupported (blocked). A `stale` finite method — a pinned input moved since the capture —
is the policy's currentness rule doing its work ("changes invalidate dependent evidence"):
the measurement is `invalidated`, the legs that depend on the method stay pending, the
moved input is named, and nothing is refused unless the receipt still claims qualification
(P4-SYSTEM.14 a42as, the director's ruling of 2026-10-22). An invalidated case grants
nothing and locks nothing: the next capture supersedes it.
Exit 2: refused/unavailable/unsupported (bounds, unreadable inputs, another case).
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import records_sexp as R  # noqa: E402
import sexp as S  # noqa: E402

FORMAT = "div-policy-review-v1"
CASE_ID = "rv64gc-m-forms-v3"  # the retained, captured case (a42ax); a consumer constant no case pins
DOCUMENT_BYTES = 65536
BOUNDARY_MARKER = "Table"  # an expectation step whose source cites a chapter table row is a directed boundary fixture
LOW_RISK = ("low", "medium")
# Declared feature dispositions (policy "the following feature rules apply regardless of the risk
# field"). An obligation absent here has no disposition and stays pending — never inferred.
FEATURE_DISPOSITIONS = {
    "OB-GC-M": "none applies: integer multiply/divide touches no privilege, translation, atomic, "
               "floating-point, counter, fetch or environment rule (P4-SYSTEM.14 a42aq, 2026-10-21)",
}
LEG_ORDER = ("source-located-expectations", "boundary-fixtures", "matched-reference-comparison",
             "repeated-execution", "discriminating-control", "record-linkage", "currentness",
             "risk-method", "feature-rules", "form-coverage")


class Refused(Exception):
    """The inputs cannot be measured honestly; nothing is reported as pending or satisfied."""


@dataclass(frozen=True)
class Leg:
    id: str
    disposition: str  # satisfied | pending
    measured: str


def _require(condition, reason: str) -> None:
    if not condition:
        raise Refused(reason)


def _bounded_bytes(path: Path, limit: int = DOCUMENT_BYTES) -> bytes:
    try:
        size = path.stat().st_size
    except OSError as error:
        raise Refused(f"unavailable: {path}: {type(error).__name__}") from error
    _require(0 < size <= limit, f"{path} is {size} bytes, outside 1..{limit}")
    return path.read_bytes()


def _forms(path: Path) -> list:
    try:
        return S.parse(_bounded_bytes(path).decode("utf-8"), str(path))
    except (S.SexpError, UnicodeError) as error:
        raise Refused(f"unreadable {path}: {error}") from error


def _one_form(path: Path, head: str):
    found = [f for f in _forms(path) if isinstance(f, list) and f and str(f[0]) == head]
    _require(len(found) == 1, f"exactly one ({head} …) expected in {path}")
    return found[0]


def _one(form, name):
    found = S.children(form, name)
    return found[0][1] if len(found) == 1 and len(found[0]) == 2 else None


def _strings(form, name) -> list[str]:
    return [str(c[1]) for c in S.children(form, name) if len(c) == 2]


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _leg(legs: list[Leg], leg_id: str, ok: bool, measured: str) -> None:
    legs.append(Leg(leg_id, "satisfied" if ok else "pending", measured))


def measure_policy(root: Path, *, method: dict, case_id: str = CASE_ID) -> dict:
    """The leg table for one retained case, given the finite method review's plain result."""
    root = Path(root)
    _require(isinstance(method, dict) and isinstance(method.get("disposition"), str), "method result is not a plain record")
    case_dir = root / "evidence" / case_id
    planned = _one_form(case_dir / "planned-experiment.sexp", "experiment")
    _require(_one(planned, "id") == case_id, "planned experiment id differs from the case")
    try:
        receipt = json.loads(_bounded_bytes(case_dir / "verification.json").decode("utf-8"))
    except (ValueError, UnicodeError) as error:
        raise Refused(f"unreadable receipt: {error}") from error
    _require(isinstance(receipt, dict) and receipt.get("case_id") == case_id, "receipt is not this case's object")
    profile = receipt.get("profile_id")
    _require(isinstance(profile, str) and profile, "receipt names no profile")
    _require(isinstance(receipt.get("qualification"), bool), "receipt lacks boolean qualification")
    verification = S.children(planned, "verification")
    _require(len(verification) == 1, "planned experiment needs exactly one verification form")
    properties = S.children(verification[0], "property")
    _require(1 <= len(properties) <= 64, "planned experiment declares no property, or more than 64")
    graph = verification[0]  # the scoped graph: properties, inputs, producers and observations
    inputs = {str(_one(i, "id")): i for i in S.children(graph, "input")}
    producers = {str(_one(p, "id")): p for p in S.children(graph, "producer")}
    roles = {name: str(_one(form, "role")) for name, form in inputs.items()}

    profile_dir = root / "profiles" / profile
    try:
        reqs = {r["id"]: r for r in R.load(profile_dir / "requirements.sexp", root=root)}
        obligations = {o["id"]: o for o in R.load(profile_dir / "contract-obligations.sexp", root=root)}
    except (R.RecordRefused, S.SexpError, OSError) as error:
        raise Refused(f"{profile}: unreadable catalogue: {error}") from error
    first = properties[0]
    req_id = str(_one(first, "requirement_id"))
    _require(req_id in reqs, f"property names unknown requirement {req_id}")
    requirement = reqs[req_id]
    obligation_ids = _strings(first, "obligation_ids")
    for prop in properties[1:]:
        _require(str(_one(prop, "requirement_id")) == req_id, "every property must address the one requirement")
    category = requirement["source_semantics"]["category"]
    risk = requirement["risk"]

    # Expectation steps: the source-located expected observations.
    expectation_ids = [name for name, role in roles.items() if role == "expectation" and name != "mutant-expectation"]
    _require(len(expectation_ids) == 1, "exactly one baseline expectation input expected")
    expectation_path = root / str(_one(inputs[expectation_ids[0]], "path"))
    expectations = _one_form(expectation_path, "expectations")
    steps = {}
    for step in S.children(expectations, "step"):
        n = _one(step, "n")
        _require(isinstance(n, int) and n not in steps, "expectation steps must carry unique integer n")
        steps[n] = dict(insn=str(_one(step, "insn") or ""), derivation=str(_one(step, "derivation") or ""),
                        source=str(_one(step, "source") or ""))
    _require(steps, "expectation file declares no step")
    witnesses = {}
    for prop in properties:
        gw = S.children(prop, "gpr_witness")
        _require(len(gw) == 1, "every property needs exactly one gpr_witness")
        step_n, register = _one(gw[0], "step_n"), str(_one(gw[0], "register"))
        _require(isinstance(step_n, int) and step_n in steps, "witness step is not an expectation step")
        witnesses[str(_one(prop, "id"))] = (step_n, register)
    controls = S.children(graph, "control_run")
    _require(len(controls) == 1, "planned experiment needs exactly one control_run")
    named = _strings(controls[0], "property_ids")
    _require(len(named) == 1 and named[0] in witnesses, "control_run must name one declared property")
    witness_step, witness_register = witnesses[named[0]]

    legs: list[Leg] = []
    # source-located-expectations
    unlocated = [n for n, s in steps.items() if not (s["source"].strip() and s["derivation"].strip())]
    refs = requirement["source_refs"]
    cited = any(r["source_id"] in steps[witness_step]["source"] and r["locator"] in steps[witness_step]["source"] for r in refs)
    expected = producers.get("expected")
    reference_only = {name for name, role in roles.items() if role in ("reference-config", "reference-identity")}
    expected_inputs = set(_strings(expected, "input_ids")) if expected is not None else set()
    own_output = expected is None or bool(expected_inputs & reference_only) or not (expected_inputs & set(expectation_ids))
    _leg(legs, "source-located-expectations", not unlocated and cited and not own_output,
         f"{len(steps) - len(unlocated)} of {len(steps)} steps carry derivation+source; witness step {witness_step} "
         f"{'cites' if cited else 'does not cite'} {req_id}'s source; expected producer "
         f"{'reads only its own inputs' if not own_output else 'is missing or reads reference inputs'}")
    # boundary-fixtures
    boundary_steps = sorted(n for n, s in steps.items() if BOUNDARY_MARKER in s["source"])
    declared_steps = {step for step, _ in witnesses.values()}
    undeclared = [n for n in boundary_steps if n not in declared_steps]
    _leg(legs, "boundary-fixtures", bool(boundary_steps) and not undeclared,
         f"{len(boundary_steps)} directed boundary rows present at steps {boundary_steps}; "
         f"{len(boundary_steps) - len(undeclared)} predeclared as properties")
    # runs from the receipt
    comparison = receipt.get("comparison") if isinstance(receipt.get("comparison"), dict) else {}
    runs = {r.get("run_kind"): r for r in comparison.get("runs", []) if isinstance(r, dict)}

    def verdict(kind):
        run = runs.get(kind) or {}
        inner = run.get("comparison") if isinstance(run.get("comparison"), dict) else {}
        return inner.get("verdict"), inner.get("gpr_difference")

    method_ok = (method.get("disposition") == "satisfied" and method.get("capture_binding") == "matched"
                 and method.get("record_disposition") == "valid")
    rule = str(_one(verification[0], "comparison_rule") or "")
    kinds = _strings(first, "observation_kinds")
    baseline, _ = verdict("baseline")
    _leg(legs, "matched-reference-comparison", method_ok and baseline == "AGREE" and bool(rule) and bool(kinds),
         f"method {method.get('disposition')}; baseline {baseline}; rule {rule or '(none)'}; vocabulary {kinds or '(unnamed)'}")
    repeat, _ = verdict("repeat")
    _leg(legs, "repeated-execution", repeat == "AGREE", f"repeat {repeat}")
    control, diff = verdict("control")
    diff = diff if isinstance(diff, dict) else {}
    observed = {str(pair[0]) for pair in diff.get("observed", []) if isinstance(pair, (list, tuple)) and pair}
    at_witness = diff.get("step_n") == witness_step and observed == {witness_register}
    _leg(legs, "discriminating-control", control == "DIVERGE" and at_witness,
         f"control {control} at step {diff.get('step_n')} registers {sorted(observed)}; witness step {witness_step} {witness_register}")
    # record-linkage
    unknown = [ob for ob in obligation_ids if ob not in obligations]
    unnamed = [ob for ob in obligation_ids if ob in obligations and ob not in requirement["obligation_ids"]]
    runner = any(role == "collector" for role in roles.values())
    limitations = receipt.get("limitations")
    linked = (bool(obligation_ids) and not unknown and not unnamed and runner and expected is not None
              and isinstance(limitations, list) and bool(limitations))
    _leg(legs, "record-linkage", linked,
         f"obligations {obligation_ids} ({'effective and named' if not unknown and not unnamed else 'unknown ' + str(unknown) + ' unnamed ' + str(unnamed)}); "
         f"tracked runner {'named' if runner else 'missing'}; expectation producer {'named' if expected is not None else 'missing'}; "
         f"{len(limitations) if isinstance(limitations, list) else 0} limitation(s)")
    # currentness
    manifest = _one_form(case_dir / "dependencies.sexp", "dependencies")
    policy_rel = f"profiles/{profile}/EVIDENCE_POLICY.md"
    pins = {str(_one(i, "path")): str(_one(i, "sha256")) for i in S.children(manifest, "input")}
    policy_pin = pins.get(policy_rel)
    policy_now = _digest(_bounded_bytes(root / policy_rel)) if (root / policy_rel).is_file() else None
    _leg(legs, "currentness", policy_pin is not None and policy_pin == policy_now and method_ok,
         f"policy {'pinned' if policy_pin else 'unpinned'} and {'current' if policy_pin and policy_pin == policy_now else 'changed since the pin'}; "
         f"method binding {method.get('capture_binding')}")
    # risk-method
    _leg(legs, "risk-method", risk in LOW_RISK,
         f"risk {risk}: {'no second method required' if risk in LOW_RISK else 'second method and adversarial case undeclared'}")
    # feature-rules
    feature = [FEATURE_DISPOSITIONS.get(ob) for ob in obligation_ids]
    _leg(legs, "feature-rules", bool(obligation_ids) and all(feature),
         "; ".join(f"{ob}: {d or 'feature disposition undeclared'}" for ob, d in zip(obligation_ids, feature)) or "no obligation")
    # form-coverage
    required = sorted(requirement["insns"])
    mnemonic = lambda s: s["insn"].split()[0].lower() if s["insn"].split() else ""
    exercised = sorted({mnemonic(s) for s in steps.values()} & set(required))
    predeclared = sorted({mnemonic(steps[n]) for n in declared_steps} & set(required))
    _leg(legs, "form-coverage", bool(required) and predeclared == required,
         f"{len(predeclared)} of {len(required)} forms predeclared {predeclared}; {len(exercised)} exercised {exercised}")

    assert [leg.id for leg in legs] == list(LEG_ORDER)
    missing = [leg.id for leg in legs if leg.disposition != "satisfied"]
    stale = method.get("disposition") == "stale"
    findings = []
    if receipt.get("qualification") is True and missing:
        findings.append("receipt claims qualification the policy legs refuse: " + ", ".join(missing))
    if not method_ok and not stale:
        findings.append(f"finite method not satisfied ({method.get('disposition')}); legs measured but blocked")
    if stale:
        disposition = "invalidated"
    elif not method_ok:
        disposition = "blocked"
    else:
        disposition = "satisfied" if not missing else "pending"
    return dict(format_version=FORMAT, case_id=case_id, profile_id=profile, requirement_id=req_id,
                obligation_ids=obligation_ids, category=category, risk=risk,
                method={k: method.get(k) for k in ("disposition", "reason", "capture_binding", "record_disposition",
                                                    "charged_read_bytes", "record_sha256", "planned_sha256")},
                invalidated_by=(str(method.get("reason") or "finite method stale") if stale else None),
                legs=[asdict(leg) for leg in legs], missing=missing, findings=findings,
                coverage=dict(required=required, exercised=exercised, predeclared=predeclared),
                boundary=dict(present=boundary_steps, predeclared=sorted(declared_steps & set(boundary_steps))),
                disposition=disposition, credited=False,
                limitations=["measurement of declared bytes only; grants no qualification, obligation or CPU credit",
                             "a crediting disposition is a separately owned record that cites a satisfied measurement",
                             "an invalidated measurement is superseded by the next capture, never repaired by relabelling",
                             "boundary rows and forms are read from the expectation file, not inferred from the chapter"])


def review_policy(root: Path, *, case_id: str = CASE_ID) -> dict:
    """Compose the finite method review on the real tree, then measure the legs."""
    import review_div_method as Method
    _require(Path(root).resolve() == Method.ROOT.resolve(), "the finite method review is bound to the repository root")
    _require(case_id == CASE_ID, f"unsupported: no reviewed capture for {case_id}")
    return measure_policy(root, method=asdict(Method.review_method(case_id=case_id)), case_id=case_id)


def summary(table: dict) -> tuple[int, str]:
    satisfied = sum(1 for leg in table["legs"] if leg["disposition"] == "satisfied")
    line = (f"DIV-POLICY: {table['disposition']} — {satisfied} of {len(table['legs'])} legs satisfied"
            + (f"; missing {', '.join(table['missing'])}" if table["missing"] else "")
            + (f"; invalidated by {table['invalidated_by']}" if table.get("invalidated_by") else "")
            + (f"; FINDING {'; '.join(table['findings'])}" if table["findings"] else "")
            + "; no qualification credit")
    return (1 if table["findings"] else 0), line


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Measure the retained DIV case against the policy legs.")
    parser.add_argument("--root", default=str(HERE.parent))
    parser.add_argument("--case", default=CASE_ID)
    parser.add_argument("--method-json", help="a plain method result file instead of running the finite method review")
    parser.add_argument("--json", action="store_true", help="the leg table on stdout, the summary on stderr")
    args = parser.parse_args(argv)
    try:
        if args.method_json:
            try:
                method = json.loads(_bounded_bytes(Path(args.method_json)).decode("utf-8"))
            except (ValueError, UnicodeError) as error:
                raise Refused(f"unreadable method result: {error}") from error
            table = measure_policy(Path(args.root), method=method, case_id=args.case)
        else:
            table = review_policy(Path(args.root), case_id=args.case)
    except Refused as error:
        print(f"DIV-POLICY: refused — {error}", file=sys.stderr)
        return 2
    code, line = summary(table)
    if args.json:
        payload = json.dumps(table, indent=2) + "\n"
        _require(len(payload.encode()) <= DOCUMENT_BYTES, "leg table exceeds the 64 KiB document bound")
        sys.stdout.write(payload)
        print(line, file=sys.stderr)
    else:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
