#!/usr/bin/env python3
"""The record mapping: JSON-shaped record dicts <-> S-expression forms.

SINGLE OWNER OF THE MAPPING. `SOT-FORMAT.3` converted the profile's requirement and
contract-obligation catalogues from JSON Lines to the one format; every consumer that needs
records as dictionaries (the RECORD-SCHEMA gate, the gate report) reads through this module,
so the JSON key <-> field name correspondence lives in exactly one place and cannot drift
between reader and writer.

The mapping is deliberately boring:
  JSON string (prose / identifier) -> quoted string     (id, statement, locator, …)
  JSON string (closed enum)        -> bare symbol       (kind, risk, authority, …)
  JSON integer                     -> integer atom
  JSON boolean / null              -> (true) / (false) / (null)      [obligation parameters]
  JSON list of scalars             -> repeated sibling field lists   (record top level)
  JSON list (parameters)           -> (ints …) / (strs …)            (homogeneous, typed)
  empty JSON list                  -> the field's absence (repeat fields may appear zero times)

Round-trip losslessness is not asserted here; `scripts/convert_records.py --verify` re-derives
the source JSONL from the converted file and compares bytes. Values the corpus does not write
(a float, a heterogeneous or nested list) are REFUSED with the parameter named — the
S-expression side has no atom for them, and a guessed translation would be a fork of meaning.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sexp as S                                # noqa: E402


class RecordRefused(Exception):
    """A value the mapping does not carry. Refused, never guessed."""


# --------------------------------------------------------------------------- form -> dict

def _s(value) -> str:
    return str(value)


def _refs(children, key_id, key_locator):
    return [{key_id: _s(S.field(f, key_id)), key_locator: _s(S.field(f, key_locator))}
            for f in children]


def _strings(forms, name):
    """Values of repeated `(name VALUE)` atom-field children, order preserved."""
    out = []
    for f in forms:
        if len(f) != 2 or f[0] != name:
            raise S.SexpError(f"({name} …) must carry exactly one value, got {f!r}")
        out.append(_s(f[1]))
    return out


def _one(form, name):
    """The single child list headed `name` — the whole-list form-field shape."""
    found = S.children(form, name)
    if len(found) != 1:
        raise S.SexpError(f"expected exactly one ({name} …), found {len(found)}")
    return found[0]


def requirement_to_dict(form) -> dict:
    S.head(form, "requirement")
    src = S.children(form, "source_refs")
    impl = S.children(form, "implementation_refs")
    sem = _one(form, "source_semantics")
    return {
        "id": _s(S.field(form, "id")),
        "profile_ids": _strings(S.children(form, "profile_ids"), "profile_ids"),
        "kind": _s(S.field(form, "kind")),
        "statement": _s(S.field(form, "statement")),
        "insns": _strings(S.children(form, "insns"), "insns"),
        "source_refs": _refs(src, "source_id", "locator"),
        "applicability": _s(S.field(form, "applicability")),
        "research_status": _s(S.field(form, "research_status")),
        "implementation_status": _s(S.field(form, "implementation_status")),
        "source_semantics": {"category": _s(S.field(sem, "category")),
                             "detail": _s(S.field(sem, "detail"))},
        "risk": _s(S.field(form, "risk")),
        "obligation_ids": _strings(S.children(form, "obligation_ids"), "obligation_ids"),
        "dependencies": _strings(S.children(form, "dependencies"), "dependencies"),
        "implementation_refs": _refs(impl, "artifact_id", "locator"),
        "evidence_ids": _strings(S.children(form, "evidence_ids"), "evidence_ids"),
    }


def _value_to_json(form):
    head = S.head(form, "param value")
    if len(form) < 1:
        raise RecordRefused(f"empty parameter value form {form!r}")

    def one():
        if len(form) != 2:
            raise RecordRefused(f"({head} …) takes exactly one value, got {form!r}")
        return form[1]

    if head == "int":
        return one()
    if head == "str":
        return _s(one())
    if head == "true":
        if len(form) != 1:
            raise RecordRefused(f"(true) is nullary, got {form!r}")
        return True
    if head == "false":
        if len(form) != 1:
            raise RecordRefused(f"(false) is nullary, got {form!r}")
        return False
    if head == "null":
        if len(form) != 1:
            raise RecordRefused(f"(null) is nullary, got {form!r}")
        return None
    if head == "ints":
        return [int(a) for a in form[1:]]
    if head == "strs":
        return [_s(a) for a in form[1:]]
    raise RecordRefused(f"unknown parameter value form {form!r}")


def obligation_to_dict(form) -> dict:
    S.head(form, "obligation")
    src = S.children(form, "source_refs")
    params = _one(form, "parameters")
    out = {
        "id": _s(S.field(form, "id")),
        "contract_id": _s(S.field(form, "contract_id")),
        "contract_version": _s(S.field(form, "contract_version")),
        "profile_ids": _strings(S.children(form, "profile_ids"), "profile_ids"),
        "direction": _s(S.field(form, "direction")),
        "statement": _s(S.field(form, "statement")),
        "authority": _s(S.field(form, "authority")),
        "source_refs": _refs(src, "source_id", "locator"),
        "parameters": {},
        "dependencies": _strings(S.children(form, "dependencies"), "dependencies"),
        "required_checks": _strings(S.children(form, "required_checks"), "required_checks"),
    }
    for p in S.children(params, "param"):
        name = _s(S.field(p, "name"))
        out["parameters"][name] = _value_to_json(S.field(p, "value"))
    return out


def unit_to_dict(form) -> dict:
    S.head(form, "unit")
    out = {"id": _s(S.field(form, "id")),
           "kind": _s(S.field(form, "kind")),
           "layer": _s(S.field(form, "layer")),
           "book": _s(S.field(form, "book"))}
    req = S.children(form, "requires")
    if req:
        out["requires"] = [_s(x) for x in req[0][1:]]
    return out


def category_need_to_dict(form) -> dict:
    S.head(form, "category-need")
    out = {"category": _s(S.field(form, "category")),
           "layer": _s(S.field(form, "layer")),
           "kind": _s(S.field(form, "kind")),
           "unit": _s(S.field(form, "unit")),
           "disposition": _s(S.field(form, "disposition"))}
    reason = S.children(form, "reason")
    if reason:
        out["reason"] = _s(reason[0][1])
    material = S.children(form, "material")
    if material:
        out["material"] = _s(material[0][1])
    return out


def form_to_dict(form) -> dict:
    head = S.head(form)
    if head == "requirement":
        return requirement_to_dict(form)
    if head == "obligation":
        return obligation_to_dict(form)
    if head == "unit":
        return unit_to_dict(form)
    if head == "category-need":
        return category_need_to_dict(form)
    raise RecordRefused(f"not a record form: {form!r}")


# --------------------------------------------------------------------------- dict -> form

def _pair(name, value):
    return [S.Symbol(name), value]


def _repeated(name, values):
    return [_pair(name, v) for v in values]


def _ref_forms(key, refs, key_id, key_locator):
    return [[S.Symbol(key), _pair(key_id, r[key_id]), _pair(key_locator, r[key_locator])]
            for r in refs]


def _json_to_value(name, v):
    if isinstance(v, bool):
        return [S.Symbol("true")] if v else [S.Symbol("false")]
    if v is None:
        return [S.Symbol("null")]
    if isinstance(v, int):
        return [S.Symbol("int"), v]
    if isinstance(v, str):
        return [S.Symbol("str"), v]
    if isinstance(v, list):
        if all(isinstance(x, int) and not isinstance(x, bool) for x in v):
            return [S.Symbol("ints"), *v]
        if all(isinstance(x, str) for x in v):
            return [S.Symbol("strs"), *v]
        raise RecordRefused(f"parameter {name!r}: a list must be all-integer or all-string, "
                            f"got {v!r}")
    raise RecordRefused(f"parameter {name!r}: no S-expression value for {v!r} — a float or "
                        f"nested value needs a schema decision, not a guessed translation")


def dict_to_form(rec: dict):
    """The record dict -> its form. Field order follows the dict, i.e. the JSON key order."""
    if "book" in rec:                                    # a modelled-unit registry row
        form = [S.Symbol("unit"),
                _pair("id", rec["id"]),
                _pair("kind", S.Symbol(rec["kind"])),
                _pair("layer", S.Symbol(rec["layer"])),
                _pair("book", rec["book"])]
        if rec.get("requires"):
            form += _repeated("requires", rec["requires"])
        return form
    if "disposition" in rec:                             # a category-need row
        form = [S.Symbol("category-need"),
                _pair("category", rec["category"]),
                _pair("layer", S.Symbol(rec["layer"])),
                _pair("kind", rec["kind"]),
                _pair("unit", rec["unit"]),
                _pair("disposition", S.Symbol(rec["disposition"]))]
        if rec.get("reason"):
            form.append(_pair("reason", rec["reason"]))
        if rec.get("material"):
            form.append(_pair("material", rec["material"]))
        return form
    if "kind" in rec:                                    # a requirement
        return [S.Symbol("requirement"),
                _pair("id", rec["id"]),
                *_repeated("profile_ids", rec["profile_ids"]),
                _pair("kind", S.Symbol(rec["kind"])),
                _pair("statement", rec["statement"]),
                *_repeated("insns", rec.get("insns") or []),
                *_ref_forms("source_refs", rec["source_refs"], "source_id", "locator"),
                _pair("applicability", S.Symbol(rec["applicability"])),
                _pair("research_status", S.Symbol(rec["research_status"])),
                _pair("implementation_status", S.Symbol(rec["implementation_status"])),
                [S.Symbol("source_semantics"),
                 _pair("category", S.Symbol(rec["source_semantics"]["category"])),
                 _pair("detail", rec["source_semantics"]["detail"])],
                _pair("risk", S.Symbol(rec["risk"])),
                *_repeated("obligation_ids", rec["obligation_ids"]),
                *_repeated("dependencies", rec["dependencies"]),
                *_ref_forms("implementation_refs", rec["implementation_refs"],
                            "artifact_id", "locator"),
                *_repeated("evidence_ids", rec["evidence_ids"])]
    if "direction" in rec:                               # an obligation
        return [S.Symbol("obligation"),
                _pair("id", rec["id"]),
                _pair("contract_id", rec["contract_id"]),
                _pair("contract_version", rec["contract_version"]),
                *_repeated("profile_ids", rec["profile_ids"]),
                _pair("direction", S.Symbol(rec["direction"])),
                _pair("statement", rec["statement"]),
                _pair("authority", S.Symbol(rec["authority"])),
                *_ref_forms("source_refs", rec["source_refs"], "source_id", "locator"),
                [S.Symbol("parameters"),
                 *[[S.Symbol("param"), _pair("name", S.Symbol(name)), _pair("value", _json_to_value(name, v))]
                   for name, v in rec["parameters"].items()]],
                *_repeated("dependencies", rec["dependencies"]),
                *_repeated("required_checks", rec["required_checks"])]
    raise RecordRefused(f"not a record dict: keys {sorted(rec)!r}")


# --------------------------------------------------------------------------- rendering

_ESCAPES = {"\\": "\\\\", '"': '\\"', "\n": "\\n", "\t": "\\t", "\r": "\\r"}


def _render(form) -> str:
    out = []
    for el in form:
        if isinstance(el, list) and not isinstance(el, S.Symbol):
            out.append(_render(el))
        elif isinstance(el, S.Symbol):
            out.append(str(el))
        elif isinstance(el, bool):
            raise RecordRefused(f"a bare boolean is not a value: {el!r}")
        elif isinstance(el, int):
            out.append(str(el))
        elif isinstance(el, str):
            out.append('"' + "".join(_ESCAPES.get(c, c) for c in el) + '"')
        else:
            raise RecordRefused(f"cannot render {el!r}")
    return "(" + " ".join(out) + ")"


def render_forms(forms) -> str:
    """One form per line — the compact shape that keeps the dossier under its per-part bound."""
    return "".join(_render(f) + "\n" for f in forms)


# --------------------------------------------------------------------------- files

def load(path: Path) -> list[dict]:
    """A converted record file as JSON-shaped dicts, in file order."""
    return [form_to_dict(f) for f in S.read_file(Path(path))]


def dump(records: list[dict]) -> str:
    return render_forms([dict_to_form(r) for r in records])
