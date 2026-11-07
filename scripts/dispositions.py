#!/usr/bin/env python3
"""Declared alternative dispositions: the catalogue `profiles/<profile>/dispositions.sexp`, read and held to the catalogue.

EVIDENCE_POLICY.md: "Any alternative disposition needs an explicit source-grounded argument and its own controls before
execution." Its `source-specific` row asks the same of that category. This module reads those records. It grants nothing:
`scripts/review_div_policy.py` reads a `kind case` record as the category row of that case's comparison, and a requirement that
needs one and has none stays `planned`
(decision_the-seventeen-called.md; P4-SYSTEM.14 a51-7). Read-only; no Git; no process.
"""
from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_sexp_schema as K  # noqa: E402  (pinned by the finite cases; read, never changed)
import sexp as S  # noqa: E402

CATALOGUE = "dispositions.sexp"
SCHEMA = "schema/dispositions.sexp"
DOCUMENT_BYTES = 65536


class DispositionRefused(Exception):
    """The catalogue cannot be read as declared dispositions."""


def _one(form, name):
    found = S.children(form, name)
    return str(found[0][1]) if found else None


def load(root: Path, profile_dir: Path) -> dict[str, dict]:
    """Each declared disposition by the requirement it answers, schema-validated; no catalogue is no dispositions."""
    path = Path(profile_dir) / CATALOGUE
    if not path.exists():
        return {}
    if not path.is_file() or path.stat().st_size > DOCUMENT_BYTES:
        raise DispositionRefused(f"{path}: not a bounded regular file")
    schema = Path(root) / SCHEMA
    if not schema.is_file():
        raise DispositionRefused(f"{SCHEMA} is missing")
    try:
        constructs, operators = K.load_schema(schema)
        text = path.read_text("utf-8")
        errors = K.validate_text(text, constructs, operators, path.as_posix(), parse_where=str(path))
    except (K.SchemaError, S.SexpError, UnicodeError, OSError) as error:
        raise DispositionRefused(f"{path}: {error}") from error
    if errors:
        raise DispositionRefused(f"{path}: " + "; ".join(str(e) for e in errors[:3]))
    records: dict[str, dict] = {}
    ids: set[str] = set()
    for form in S.parse(text, str(path)):
        if not (isinstance(form, list) and form and str(form[0]) == "disposition"):
            continue
        row = dict(id=_one(form, "id"), requirement_id=_one(form, "requirement_id"), kind=_one(form, "kind"),
                   source_id=_one(form, "source_id"), source_locator=_one(form, "source_locator"), argument=_one(form, "argument"),
                   controls=[str(c[1]) for c in S.children(form, "controls")], control_property=_one(form, "control_property"),
                   walk_record=_one(form, "walk_record") == "yes",
                   expect={_one(e, "fact"): _one(e, "value") for e in S.children(form, "expect")})
        if row["id"] in ids:
            raise DispositionRefused(f"{path}: duplicate disposition id {row['id']}")
        if row["requirement_id"] in records:
            raise DispositionRefused(f"{path}: two dispositions answer {row['requirement_id']}")
        if row["kind"] == "case" and row["control_property"] is None:
            raise DispositionRefused(f"{path}: {row['id']} closes through a case and names no control_property")
        if (row["kind"] == "record") != bool(row["expect"]):
            raise DispositionRefused(f"{path}: {row['id']}: a kind record disposition declares each fact it expects, and only that kind does")
        ids.add(row["id"])
        records[row["requirement_id"]] = row
    return records
