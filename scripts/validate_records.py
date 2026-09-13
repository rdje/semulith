#!/usr/bin/env python3
"""A JSON Schema validator for exactly the subset this project's schemas use.

WHY THIS EXISTS RATHER THAN A DEPENDENCY. `schemas/*.json` are the project's data contracts and
`EVD-01` makes them gate material, so validating them must work from a fresh clone with nothing
installed. No JSON Schema library is present on this host (`jsonschema`, `fastjsonschema` and
`pydantic` are all absent), and installing one would put a dependency store on a different volume
from the repository — which the data-locality policy forbids. Vendoring a library into `target/`
would leave the gate depending on an untracked directory.

So the validator is tracked, small, and reads its own limits out loud.

⛔ THE SOUNDNESS PROPERTY IS THE REFUSAL, NOT THE COVERAGE. A partial validator that silently
ignores a keyword it does not implement is worse than no validator: it reports `valid` for a
document it never fully checked. This one REFUSES — raises `UnsupportedSchema` — the moment it
meets a keyword outside `SUPPORTED`. Adding a keyword to a schema therefore breaks the gate
loudly instead of quietly widening what passes.

SUPPORTED is derived from a census of the three schemas actually in this repository:
    $id $schema title            annotations, ignored
    type properties required additionalProperties
    enum const pattern minLength
    items minItems uniqueItems
    allOf if then
`if`/`then` is implemented as the specification describes it: `if` is evaluated for validity
only, its errors are discarded, and `then` applies when it succeeded.

⚠️ HONEST LIMIT, stated rather than implied: this is NOT a conformant JSON Schema implementation.
It is a checker for the shapes these three files use, and it will refuse anything else. `else`,
`$ref`, `oneOf`, `anyOf`, `not`, numeric bounds and `format` are all unimplemented ON PURPOSE.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SUPPORTED = {
    "$id", "$schema", "title", "description",
    "type", "properties", "required", "additionalProperties",
    "enum", "const", "pattern", "minLength",
    "items", "minItems", "uniqueItems",
    "allOf", "if", "then",
}

TYPES = {
    "object": dict, "array": list, "string": str, "boolean": bool,
    "null": type(None), "integer": int, "number": (int, float),
}


class UnsupportedSchema(Exception):
    """A keyword this validator does not implement. Never ignored, never assumed harmless."""


def _check_keywords(schema: dict, where: str) -> None:
    unknown = sorted(set(schema) - SUPPORTED)
    if unknown:
        raise UnsupportedSchema(
            f"{where}: schema uses {unknown}, which this validator does not implement. "
            f"Implement it or stop using it — silently ignoring a keyword would report 'valid' "
            f"for a document that was never fully checked.")


def _frozen(value):
    """A hashable view of a JSON value, for uniqueItems."""
    if isinstance(value, dict):
        return ("o",) + tuple(sorted((k, _frozen(v)) for k, v in value.items()))
    if isinstance(value, list):
        return ("a",) + tuple(_frozen(v) for v in value)
    return ("v", type(value).__name__, value)


def validate(instance, schema: dict, path: str = "$", where: str = "<schema>") -> list[str]:
    """Return a list of human-readable errors. An empty list means valid."""
    _check_keywords(schema, where)
    errors: list[str] = []

    if "type" in schema:
        want = schema["type"]
        py = TYPES.get(want)
        if py is None:
            raise UnsupportedSchema(f"{where}: unknown type {want!r}")
        # JSON has no bool/int distinction in Python's type system; keep them apart explicitly.
        ok = isinstance(instance, py) and not (
            want in ("integer", "number") and isinstance(instance, bool))
        if not ok:
            errors.append(f"{path}: expected {want}, got {type(instance).__name__}")
            return errors                       # further keywords would report noise

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected the constant {schema['const']!r}, got {instance!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} is not one of {schema['enum']}")
    if isinstance(instance, str):
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"{path}: {instance!r} does not match /{schema['pattern']}/")
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: shorter than minLength {schema['minLength']}")

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: has {len(instance)} item(s), minItems is {schema['minItems']}")
        if schema.get("uniqueItems"):
            seen, dupes = set(), []
            for v in instance:
                f = _frozen(v)
                if f in seen:
                    dupes.append(v)
                seen.add(f)
            if dupes:
                errors.append(f"{path}: duplicate item(s) {dupes!r} under uniqueItems")
        if "items" in schema:
            for i, v in enumerate(instance):
                errors += validate(v, schema["items"], f"{path}[{i}]", where)

    if isinstance(instance, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: missing required property {key!r}")
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in props:
                    errors.append(f"{path}: property {key!r} is not allowed")
        for key, sub in props.items():
            if key in instance:
                errors += validate(instance[key], sub, f"{path}.{key}", where)

    for i, sub in enumerate(schema.get("allOf", [])):
        errors += validate(instance, sub, path, f"{where}/allOf[{i}]")

    if "if" in schema:
        if not validate(instance, schema["if"], path, f"{where}/if"):
            if "then" in schema:
                errors += validate(instance, schema["then"], path, f"{where}/then")

    return errors


def validate_jsonl(records_path: Path, schema_path: Path) -> list[str]:
    """Validate every line of a JSONL file. A malformed line is an error, never a skip."""
    schema = json.loads(schema_path.read_text())
    errors: list[str] = []
    n = 0
    for lineno, raw in enumerate(records_path.read_text().splitlines(), 1):
        if not raw.strip():
            continue
        n += 1
        try:
            record = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{records_path.name}:{lineno}: not valid JSON — {exc}")
            continue
        rid = record.get("id", f"<line {lineno}>") if isinstance(record, dict) else f"<line {lineno}>"
        for err in validate(record, schema, "$", schema_path.name):
            errors.append(f"{records_path.name}:{lineno} [{rid}] {err}")
    if n == 0:
        errors.append(f"{records_path.name}: contains no records — an empty file is not a valid one")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: validate_records.py <records.jsonl> <schema.json>", file=sys.stderr)
        return 2
    try:
        errors = validate_jsonl(Path(argv[1]), Path(argv[2]))
    except UnsupportedSchema as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    for e in errors:
        print(e)
    print(f"__ERRORS__ {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
