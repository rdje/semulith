#!/usr/bin/env python3
"""A requirement's statement, clause by clause: which witnesses stand for each, and what limit names the rest.

A requirement's statement says more than its forms. First drafts of the A, C, F and D cases covered every form and agreed with the
pinned reference on every step, and missed most of what their statements say; reading the 19 credited statements clause by clause then
found two more the ten legs had passed (`decision_the-window-that-carries-fetch-faults.md`). This is the record that makes such an
omission visible: `profiles/<profile>/statement-trace.sexp` splits each statement into clauses, in order, and the review holds it:

  - the clauses' words, in order, are exactly the statement's: nothing skipped, reordered or added;
  - each clause names a declared property of the case or a limit, a literal part of the case's own `limitation`;
  - every declared property stands for some clause, so a witness cannot go unread.

A trace is annotation, not proof of semantics (RULES EVD-06): it says which witness a reader should hold a clause to, and an honest
reader can still disagree. What it cannot do is leave a clause out. It grants nothing, and nothing here runs a process.

  python3 -B scripts/statement_trace.py --profile rv64gc-lab-v0
  python3 -B scripts/statement_trace.py --profile rv64gc-lab-v0 --requirement REQ-GC-C
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_sexp_schema as K  # noqa: E402  (pinned by the finite cases; read, never changed)
import sexp as S  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CATALOGUE = "statement-trace.sexp"
SCHEMA = "schema/statement-trace.sexp"
DOCUMENT_BYTES = 262144  # 47 requirements' statements, and up to 96 property names for each


class TraceRefused(ValueError):
    """The catalogue cannot be read as a trace."""


def _require(condition, reason):
    if not condition:
        raise TraceRefused(reason)


def _strings(form, name) -> list[str]:
    return [str(c[1]) for c in S.children(form, name) if len(c) == 2]


def load_trace(root: Path, profile_dir: Path) -> dict[str, list[dict]]:
    """Each traced requirement's clauses, schema-validated; an absent catalogue traces nothing. A selection's trace lives beside its record."""
    trace: dict[str, list[dict]] = {}
    for path in (Path(profile_dir) / CATALOGUE, Path(profile_dir) / "selections" / CATALOGUE):
        if path.exists():
            _read_trace(root, path, trace)
    return trace


def _read_trace(root: Path, path: Path, trace: dict[str, list[dict]]) -> None:
    _require(path.is_file() and path.stat().st_size <= DOCUMENT_BYTES, f"{path}: not a bounded regular file")
    schema = Path(root) / SCHEMA
    _require(schema.is_file(), f"{SCHEMA} is missing")
    try:
        constructs, operators = K.load_schema(schema)
        text = path.read_text("utf-8")
        errors = K.validate_text(text, constructs, operators, path.as_posix(), parse_where=str(path))
    except (K.SchemaError, S.SexpError, UnicodeError, OSError) as error:
        raise TraceRefused(f"{path}: {error}") from error
    _require(not errors, f"{path}: " + "; ".join(str(e) for e in errors[:3]))
    for form in S.parse(text, str(path)):
        if not (isinstance(form, list) and form and str(form[0]) == "trace"):
            continue
        ids = _strings(form, "requirement_id")
        _require(len(ids) == 1, f"{path}: a trace names one requirement")
        _require(ids[0] not in trace, f"{path}: {ids[0]} is traced twice")
        trace[ids[0]] = [dict(text=str(_strings(c, "text")[0]), properties=_strings(c, "properties"), limits=_strings(c, "limits"))
                         for c in S.children(form, "clause")]


def measure(statement: str, clauses: list[dict], properties: list[str], limitation: str) -> tuple[bool, str]:
    """Hold one requirement's clauses to its statement and its case: (holds, what was measured)."""
    want = statement.split()
    have = [word for clause in clauses for word in clause["text"].split()]
    if have != want:
        at = next((i for i, (a, b) in enumerate(zip(have, want)) if a != b), min(len(have), len(want)))
        return False, f"the clauses are not the statement: word {at} reads {' '.join(have[at:at + 4])!r}, the statement {' '.join(want[at:at + 4])!r}"
    named = {name for clause in clauses for name in clause["properties"]}
    unknown = sorted(named - set(properties))
    if unknown:
        return False, f"a clause names properties the case does not declare: {unknown}"
    unread = sorted(set(properties) - named)
    if unread:
        return False, f"properties stand for no clause: {unread}"
    outside = sorted({limit for clause in clauses for limit in clause["limits"] if limit not in limitation})
    if outside:
        return False, f"a clause's limit is not in the case's limitation: {outside}"
    bare = [clause["text"][:60] for clause in clauses if not clause["properties"] and not clause["limits"]]
    if bare:
        return False, f"a clause names neither a witness nor a limit: {bare}"
    limited = sum(1 for clause in clauses if clause["limits"])
    return True, (f"{len(clauses)} clauses are the statement's {len(want)} words; each names a witness or a limit ({limited} name a limit), "
                  f"and all {len(properties)} properties stand for a clause")


def _declared_cases(root: Path, profile: str) -> dict[str, list[tuple[str, list[str], str]]]:
    """The declared cases in the tree, by the requirement each binds: id, properties and limitation, newest last. An older case stays in
    the tree as history, and a requirement's trace need hold only for the case that answers it."""
    found: dict[str, list[tuple[str, list[str], str]]] = {}
    for path in sorted((Path(root) / "evidence").glob("*/case.sexp")):
        forms = [f for f in S.parse(path.read_text("utf-8"), str(path)) if isinstance(f, list) and f and str(f[0]) == "case"]
        if len(forms) != 1 or _strings(forms[0], "profile_id") != [profile]:
            continue
        ids = [str(_strings(p, "id")[0]) for p in S.children(forms[0], "property")]
        found.setdefault(_strings(forms[0], "requirement_id")[0], []).append((path.parent.name, ids, _strings(forms[0], "limitation")[0]))
    return found


def _declared_selections(root: Path, profile_dir: Path) -> dict[str, list[tuple[str, list[str], str]]]:
    """A selection's facts stand as a case's properties do, and its limitations as a case's limitation (decision_a-credit-with-no-case.md)."""
    found: dict[str, list[tuple[str, list[str], str]]] = {}
    for path in sorted((Path(profile_dir) / "selections").glob("*.selection.sexp")):
        forms = [f for f in S.parse(path.read_text("utf-8"), str(path)) if isinstance(f, list) and f and str(f[0]) == "selection"]
        _require(len(forms) == 1, f"{path}: exactly one selection form expected")
        facts = sorted(str(_strings(f, "id")[0]) for f in S.children(forms[0], "fact"))
        found.setdefault(_strings(forms[0], "requirement_id")[0], []).append((_strings(forms[0], "id")[0], facts, "; ".join(_strings(forms[0], "limitation"))))
    return found


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--profile", required=True)
    parser.add_argument("--requirement")
    args = parser.parse_args(argv)
    profile_dir = ROOT / "profiles" / args.profile
    try:
        trace = load_trace(ROOT, profile_dir)
    except TraceRefused as error:
        print(f"STATEMENT-TRACE: refused: {error}", file=sys.stderr)
        return 2
    statements = {}
    for form in S.parse((profile_dir / "requirements.sexp").read_text("utf-8"), "requirements.sexp"):
        if isinstance(form, list) and form and str(form[0]) == "requirement":
            statements[_strings(form, "id")[0]] = _strings(form, "statement")[0]
    cases = _declared_cases(ROOT, args.profile)
    for requirement, rows in _declared_selections(ROOT, profile_dir).items():
        cases.setdefault(requirement, []).extend(rows)
    if args.requirement:
        clauses = trace.get(args.requirement)
        if clauses is None:
            print(f"STATEMENT-TRACE: {args.requirement} is not traced", file=sys.stderr)
            return 1
        for clause in clauses:
            print(clause["text"])
            for name in clause["properties"]:
                print(f"    witness: {name}")
            for limit in clause["limits"]:
                print(f"    limit: {limit}")
        return 0
    failed = 0
    for requirement in sorted(cases):
        if requirement not in trace:
            print(f"{requirement} ({cases[requirement][-1][0]}): not traced")
            failed += 1
            continue
        results = [(case, *measure(statements[requirement], trace[requirement], properties, limitation))
                   for case, properties, limitation in cases[requirement]]
        case, holds, measured = next((row for row in results if row[1]), results[-1])
        failed += not holds
        print(f"{requirement} ({case}): {measured}")
    print(f"STATEMENT-TRACE: {args.profile}: {len(cases) - failed} of {len(cases)} requirements with a declared trace; annotation, not proof of semantics")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
