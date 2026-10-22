#!/usr/bin/env python3
"""Derive each requirement's implementation_status from the evidence graph and drift-check it.

Scope: every profile whose dossier carries EVIDENCE_POLICY.md, the declaration that
requirement status is derived rather than carried ("Status and supersession"). A profile
without that declaration keeps its recorded statuses and is not judged here.

Graph inputs, tracked and bounded: the profile's requirements.sexp and effective
contract-obligations.sexp, and every evidence case evidence/<case>/ that carries
planned-experiment.sexp — with verification.json once captured, or without it while merely
declared (a declared case binds requirements and credits nothing) — (the retained declaration binding the case to
requirement/obligation ids, and the derived receipt carrying the qualification verdict).

Rules, in this order per requirement:
  not-applicable  applicability `excluded` AND source_semantics category `not-applicable` —
                  the explicit, checked inapplicability argument. One without the other is a
                  finding, never a status.
  implemented     research_status `resolved`, included, and every effective obligation the
                  requirement names has at least one CREDITED case: a verification receipt
                  whose `qualification` is true. No typed success word substitutes for it.
  partial         not implemented, but a credited case or an implementation_refs entry exists
                  (incomplete implementation or verification). An unresolved source question
                  caps a requirement here: it cannot close an included requirement.
  planned         otherwise — no credited implementation or evidence. Pending, failed, stale
                  or refused cases are reported as uncredited and never counted.
Supersession: a case naming an obligation outside the effective contract, or a requirement
outside the catalogue, is a finding; the old record and graph edge are preserved, never
credited to a successor by name alone.

Exit: 0 every derived status equals the recorded one and no finding; 1 drift or finding;
2 refused — unreadable, oversized, malformed or unbounded inputs. Read-only; no Git; no
network. `--json` prints the complete derivation table on stdout.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import records_sexp as R  # noqa: E402
import sexp as S  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
POLICY = "EVIDENCE_POLICY.md"
MAX_PROFILES = 64
MAX_REQUIREMENTS = 4096
MAX_CASES = 64
MAX_DOCUMENT_BYTES = 65536
STATUSES = ("planned", "partial", "implemented", "not-applicable")
CREDITED_FIELD = "qualification"


class Refused(ValueError):
    """The inputs cannot support a status verdict."""


def _require(condition, reason: str) -> None:
    if not condition:
        raise Refused(reason)


def _bounded_bytes(path: Path) -> bytes:
    _require(path.is_file(), f"missing input {path}")
    size = path.stat().st_size
    _require(0 < size <= MAX_DOCUMENT_BYTES, f"input outside 1..{MAX_DOCUMENT_BYTES} bytes: {path}")
    return path.read_bytes()


def _one(form, name: str):
    found = S.children(form, name)
    return str(found[0][1]) if found else None


def _strings(form, name: str) -> list[str]:
    return [str(c[1]) for c in S.children(form, name) if len(c) == 2]


def credited(receipt: dict) -> bool:
    """A case is credited only by its receipt's boolean qualification verdict."""
    return receipt.get(CREDITED_FIELD) is True


def load_cases(root: Path) -> list[dict]:
    """Every retained evidence case: its declared bindings and its verification receipt."""
    evidence = root / "evidence"
    if not evidence.is_dir():
        return []
    dirs = sorted(p for p in evidence.iterdir() if p.is_dir() and not p.name.startswith("."))
    _require(len(dirs) <= MAX_CASES, f"more than {MAX_CASES} evidence cases")
    cases = []
    for case in dirs:
        planned, receipt_path = case / "planned-experiment.sexp", case / "verification.json"
        if not planned.exists() and not receipt_path.exists():
            continue  # not an experiment case; never descended into further
        try:
            forms = S.parse(_bounded_bytes(planned).decode("utf-8"), str(planned))
        except (S.SexpError, UnicodeError) as error:
            raise Refused(f"unreadable planned experiment {planned}: {error}") from error
        experiments = [f for f in forms if isinstance(f, list) and f and str(f[0]) == "experiment"]
        _require(len(experiments) == 1, f"exactly one experiment form expected in {planned}")
        exp = experiments[0]
        # A matched-gpr record nests its properties in the (verification …) graph; a record
        # without that envelope declares them at the root. Reading only the root bound nothing
        # for either retained case until a42au measured it (0 bindings loaded for both).
        verification = S.children(exp, "verification")
        _require(len(verification) <= 1, f"more than one verification form in {planned}")
        holder = verification[0] if verification else exp
        properties = S.children(holder, "property")
        _require(properties, f"planned experiment declares no property: {planned}")
        bindings = []
        for prop in properties:
            req = _one(prop, "requirement_id")
            _require(req is not None, f"property without requirement_id in {planned}")
            bindings.append((req, tuple(_strings(prop, "obligation_ids"))))
        if not receipt_path.exists():
            # A declared case awaiting its capture (P4-SYSTEM.14 a42au): the declaration binds
            # requirements but carries no receipt, so it credits nothing. Its profile is derived
            # from the requirements it names; it is never read as a verdict.
            _require(case.name == _one(exp, "id"), f"case directory and experiment id disagree: {case.name}")
            cases.append(dict(id=case.name, profile=None, credited=False, evaluation="declared",
                              disposition="declared", bindings=bindings))
            continue
        try:
            receipt = json.loads(_bounded_bytes(receipt_path).decode("utf-8"))
        except (ValueError, UnicodeError) as error:
            raise Refused(f"unreadable verification receipt {receipt_path}: {error}") from error
        _require(isinstance(receipt, dict), f"verification receipt is not an object: {receipt_path}")
        for key in ("case_id", "profile_id", "evaluation", "disposition"):
            _require(isinstance(receipt.get(key), str), f"receipt lacks string {key}: {receipt_path}")
        _require(isinstance(receipt.get(CREDITED_FIELD), bool), f"receipt lacks boolean {CREDITED_FIELD}: {receipt_path}")
        _require(receipt["case_id"] == case.name == _one(exp, "id"),
                 f"case id, directory and experiment id disagree: {case.name}")
        cases.append(dict(id=case.name, profile=receipt["profile_id"], credited=credited(receipt),
                          evaluation=receipt["evaluation"], disposition=receipt["disposition"],
                          bindings=bindings))
    return cases


def derive_profile(root: Path, profile_dir: Path, cases: list[dict]) -> dict:
    """The derivation table for one policy-declaring profile."""
    profile = profile_dir.name
    try:
        reqs = R.load(profile_dir / "requirements.sexp", root=root)
        obligations = R.load(profile_dir / "contract-obligations.sexp", root=root)
    except (R.RecordRefused, S.SexpError, OSError) as error:
        raise Refused(f"{profile}: unreadable catalogue: {error}") from error
    _require(0 < len(reqs) <= MAX_REQUIREMENTS, f"{profile}: requirement count outside 1..{MAX_REQUIREMENTS}")
    effective = {o["id"] for o in obligations}
    by_id = {r["id"]: r for r in reqs}
    _require(len(by_id) == len(reqs), f"{profile}: duplicate requirement id")
    findings: list[str] = []
    credited_obligations: dict[str, set[str]] = {}
    uncredited: dict[str, list[str]] = {}
    def belongs(case):
        # A receipt names its profile; a declared case belongs to the profile whose catalogue
        # names every requirement it binds, and to no other.
        if case["profile"] is not None:
            return case["profile"] == profile
        return bool(case["bindings"]) and all(req_id in by_id for req_id, _ in case["bindings"])

    for case in cases:
        if not belongs(case):
            continue
        for req_id, obligation_ids in case["bindings"]:
            if req_id not in by_id:
                findings.append(f"case {case['id']} names unknown requirement {req_id}")
                continue
            for ob in obligation_ids:
                if ob not in effective:
                    findings.append(f"case {case['id']} names obligation {ob} outside the effective contract (superseded or unknown)")
                elif ob not in by_id[req_id]["obligation_ids"]:
                    findings.append(f"case {case['id']} binds {ob} to {req_id}, which does not name it")
                elif case["credited"]:
                    credited_obligations.setdefault(req_id, set()).add(ob)
                else:
                    # One entry per case and requirement, however many properties bind it.
                    entry = f"{case['id']}:{case['evaluation']}"
                    if entry not in uncredited.setdefault(req_id, []):
                        uncredited[req_id].append(entry)
    rows = []
    for r in reqs:
        excluded, argued = r["applicability"] == "excluded", r["source_semantics"]["category"] == "not-applicable"
        credited_set = credited_obligations.get(r["id"], set())
        if excluded and argued:
            derived, why = "not-applicable", "excluded with an explicit not-applicable argument"
        elif excluded != argued:
            findings.append(f"{r['id']}: applicability {r['applicability']} with source category "
                            f"{r['source_semantics']['category']} — inapplicability needs both")
            derived, why = "planned", "inapplicability argument incomplete"
        elif r["research_status"] == "resolved" and r["obligation_ids"] and set(r["obligation_ids"]) <= credited_set:
            derived, why = "implemented", f"every obligation credited ({len(credited_set)})"
        elif credited_set or r["implementation_refs"]:
            derived, why = "partial", (f"credited {sorted(credited_set)} of {r['obligation_ids']}"
                                       if credited_set else "implementation_refs without credited evidence")
            if r["research_status"] != "resolved":
                why += f"; research {r['research_status']} caps closure"
        else:
            derived, why = "planned", "no credited implementation or evidence"
        rows.append(dict(id=r["id"], recorded=r["implementation_status"], derived=derived, why=why,
                         uncredited=uncredited.get(r["id"], [])))
    drift = [row for row in rows if row["recorded"] != row["derived"]]
    counts = {s: sum(1 for row in rows if row["derived"] == s) for s in STATUSES}
    profile_cases = [c for c in cases if belongs(c)]
    return dict(profile=profile, requirements=len(rows), derived=counts, rows=rows, drift=drift,
                findings=findings, cases=len(profile_cases),
                credited_cases=sum(1 for c in profile_cases if c["credited"]),
                declared_cases=sum(1 for c in profile_cases if c["disposition"] == "declared"))


def derive(root: Path, profiles: list[str] | None = None) -> list[dict]:
    base = root / "profiles"
    dirs = sorted(p for p in base.iterdir() if p.is_dir()) if base.is_dir() else []
    _require(len(dirs) <= MAX_PROFILES, f"more than {MAX_PROFILES} profiles")
    selected = [p for p in dirs if (p / POLICY).is_file() and (profiles is None or p.name in profiles)]
    if profiles is not None:
        missing = set(profiles) - {p.name for p in selected}
        _require(not missing, f"no policy-declaring profile named {sorted(missing)}")
    cases = load_cases(root)
    return [derive_profile(root, p, cases) for p in selected]


def report(tables: list[dict]) -> tuple[int, str, list[str]]:
    """(exit code, one summary line, detail lines)."""
    if not tables:
        return 0, "REQUIREMENT-STATUS: ok (no policy-declaring profile; recorded statuses stand)", []
    details, bad = [], False
    parts = []
    for t in tables:
        for row in t["drift"]:
            details.append(f"  drift {t['profile']} {row['id']}: recorded `{row['recorded']}` derived `{row['derived']}` — {row['why']}")
        for f in t["findings"]:
            details.append(f"  finding {t['profile']}: {f}")
        bad = bad or bool(t["drift"]) or bool(t["findings"])
        summary = ", ".join(f"{n} {s}" for s, n in t["derived"].items() if n)
        parts.append(f"{t['profile']}: {t['requirements']} requirements derived {summary}; "
                     f"{t['cases']} case(s), {t['credited_cases']} credited, {t.get('declared_cases', 0)} declared; "
                     f"{len(t['drift'])} drift, {len(t['findings'])} finding(s)")
    verdict = "drift or finding" if bad else "ok"
    return (1 if bad else 0), f"REQUIREMENT-STATUS: {verdict} ({'; '.join(parts)})", details


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="derive and drift-check requirement statuses")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--profile", action="append", help="limit to a policy-declaring profile id")
    parser.add_argument("--json", action="store_true", help="print the derivation table")
    args = parser.parse_args(argv)
    try:
        tables = derive(args.root.resolve(), args.profile)
    except Refused as error:
        print(f"REQUIREMENT-STATUS: REFUSED — {error}", file=sys.stderr)
        return 2
    code, line, details = report(tables)
    if args.json:
        print(json.dumps(tables, indent=2))
        print(line, file=sys.stderr)
    else:
        print(line)
    for d in details:
        print(d, file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
