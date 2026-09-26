#!/usr/bin/env python3
"""Validate a source-of-truth file against a schema — both S-expressions.

The schema language is data (`schema/`): a schema declares constructs; a construct declares
its fields, their value types, whether they repeat, whether they are optional. An S-expression
reader accepts anything syntactically, so "it parses" is not validation — this is. An
undeclared construct, an undeclared field, a missing required field, a wrong arity, a wrong
value type or a duplicated single-valued field is refused BY NAME, never ignored
(`SOT-FORMAT.1`; acceptance criterion 3 of the tree).

The kernel below interprets `(construct …)` / `(field …)` declarations. That interpretation
is the named boundary: declaring a new CONSTRUCT is data in `schema/`; declaring a new KIND of
declaration would change this kernel — the same boundary a database draws between adding a
table and adding a column type.

  python3 scripts/check_sexp_schema.py <file.sexp> <schema.sexp>   validate one file
  python3 scripts/check_sexp_schema.py --self-test                 the gate's own arms

Uniform arity rule at every level: a field instance is a child list headed by the field's
name. Atom-typed fields take exactly one value — `(name value)`. Form-typed fields take the
nested form itself, so `(child (unit (id "c")))` is the field `child` holding the form
`(unit …)`; repetition is sibling child lists with the same head, never extra elements in one
list.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sexp as S                                   # noqa: E402

REPO = Path(__file__).resolve().parent.parent


class SchemaError(Exception):
    """A refusal. One error names the construct, the field, and the reason."""


# --------------------------------------------------------------------------- schema loading
# The kernel: it understands exactly three forms — schema, construct, field — and nothing
# else. A schema file that abuses them is refused here, at the meta level, before any target
# file is judged against it.

def _atom(form, where: str) -> S.Atom:
    if not isinstance(form, S.Atom) or isinstance(form, bool):
        raise SchemaError(f"{where}: expected an atom, got {form!r}")
    return form


def _group(pairs: list[tuple[str, object]], where: str,
           single: tuple[str, ...], multi: tuple[str, ...]) -> dict[str, object]:
    """Group (name value) pairs by name: `single` keys at most once, `multi` keys collect."""
    out: dict[str, object] = {}
    for name, value in pairs:
        if name in single:
            if name in out:
                raise SchemaError(f"{where}: duplicated field {name!r}")
            out[name] = value
        elif name in multi:
            out.setdefault(name, [])
            assert isinstance(out[name], list)
            out[name].append(value)                     # noqa: PERF401
        else:
            raise SchemaError(f"{where}: undeclared field {name!r} in a field declaration")
    return out


def _pairs(form, where: str) -> list[tuple[str, object]]:
    """The children of a declaration form as (name value) pairs, strictly two elements each."""
    pairs = []
    for el in form[1:]:
        if not isinstance(el, list) or isinstance(el, S.Symbol) or not el:
            raise SchemaError(f"{where}: expected a (name value) pair, got {el!r}")
        if len(el) != 2:
            raise SchemaError(f"{where}: wrong arity — a field is a two-element (name value) "
                              f"pair, got {len(el)} element(s) in {el!r}")
        if not isinstance(el[0], S.Symbol):
            raise SchemaError(f"{where}: a field name must be a bare symbol, got {el[0]!r}")
        pairs.append((str(el[0]), el[1]))
    return pairs


class Field:
    """One field declaration, kernel-parsed."""

    def __init__(self, where: str, form):
        g = _group(_pairs(form, where), where,
                   single=("name", "type", "repeat", "optional", "empty"),
                   multi=("head", "values"))
        if "name" not in g:
            raise SchemaError(f"{where}: a (field …) needs exactly one (name SYM)")
        name = _atom(g["name"], where)
        if not isinstance(name, S.Symbol):
            raise SchemaError(f"{where}: field name must be a bare symbol, got {name!r}")
        self.name = str(name)
        if "type" not in g:
            if g.get("empty") != "yes":
                raise SchemaError(f"{where}: field {self.name!r} has no (type …) — a marker "
                                  f"field declares (empty yes) instead")
            self.type = None                       # a pure marker: (name) and nothing else
        else:
            self.type = _atom(g["type"], where)
        if self.type is not None and self.type not in ("symbol", "string", "integer", "form"):
            raise SchemaError(f"{where}: field {self.name}: unknown type {self.type!r} — one "
                              f"of symbol string integer form")
        self.heads = [str(_atom(h, where)) for h in g.get("head", [])]
        self.values = ({str(_atom(v, where)) for v in g["values"]}
                       if "values" in g else None)
        if self.type == "form":
            if not self.heads:
                raise SchemaError(f"{where}: field {self.name} is (type form) but names no "
                                  f"(head SYM) — which constructs may it be?")
            if self.values:
                raise SchemaError(f"{where}: field {self.name} declares (values …) but is not "
                                  f"(type symbol)")
        elif self.heads:
            raise SchemaError(f"{where}: field {self.name} declares (head …) but is not "
                              f"(type form)")
        if "empty" in g and self.type == "form":
            raise SchemaError(f"{where}: field {self.name}: (empty yes) is for atom fields — "
                              f"a form field's emptiness is its construct's business")
        for flag in ("repeat", "optional", "empty"):
            v = g.get(flag)
            if v is None:
                setattr(self, flag, False)
                continue
            v = _atom(v, where)
            if v not in ("yes", "no"):
                raise SchemaError(f"{where}: field {self.name}: ({flag} …) is yes or no, "
                                  f"got {v!r}")
            setattr(self, flag, v == "yes")


class Construct:
    def __init__(self, where: str, name, field_forms: list):
        if not isinstance(name, S.Symbol):
            raise SchemaError(f"{where}: construct name must be a bare symbol, got {name!r}")
        self.name = str(name)
        self.fields: dict[str, Field] = {}
        for f in field_forms:
            fld = Field(f"{where} construct {self.name}", f)
            if fld.name in self.fields:
                raise SchemaError(f"{where}: construct {self.name} declares field "
                                  f"{fld.name!r} twice")
            self.fields[fld.name] = fld


def _declare(constructs: dict[str, Construct], form, where: str) -> None:
    children = [c for c in form[1:] if isinstance(c, list) and c]
    name_forms = [c for c in children if c[0] == "name"]
    field_forms = [c for c in children if isinstance(c[0], str) and c[0] == "field"]
    stray = [c for c in children
             if not (c[0] == "name" or (isinstance(c[0], str) and c[0] == "field"))]
    if stray:
        raise SchemaError(f"{where}: a (construct …) holds something that is not (name …) or "
                          f"(field …): {stray[0]!r}")
    if len(name_forms) != 1:
        raise SchemaError(f"{where}: a (construct …) needs exactly one (name SYM), got "
                          f"{len(name_forms)}")
    c = Construct(where, name_forms[0][1], field_forms)
    if c.name in constructs:
        raise SchemaError(f"{where}: construct {c.name!r} declared twice")
    constructs[c.name] = c


def load_schema(path: Path) -> dict[str, Construct]:
    constructs: dict[str, Construct] = {}
    for form in S.read_file(path):
        if not isinstance(form, list) or not form:
            raise SchemaError(f'{path.name}: a schema is made of (schema …)/(construct …) '
                              f'forms, got {form!r}')
        head = S.head(form, str(path))
        if head == "schema":
            continue                        # the metadata form: (schema (id STRING))
        if head == "construct":
            _declare(constructs, form, f"{path.name}")
            continue
        raise SchemaError(f'{path.name}: undeclared top-level construct "{head}" in a schema — '
                          f'only (schema …) and (construct …) may live here')
    if not constructs:
        raise SchemaError(f"{path.name}: the schema declares no constructs")
    for c in constructs.values():
        for fld in c.fields.values():
            for h in fld.heads:
                if h not in constructs:
                    raise SchemaError(f"{path.name}: construct {c.name!r} field {fld.name!r} "
                                      f"allows undeclared head {h!r}")
    return constructs


# --------------------------------------------------------------------------- validation

def _check_atom(fld: Field, value, where: str) -> None:
    if fld.type == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            raise SchemaError(f'{where}: field "{fld.name}" has wrong value type — want '
                              f'integer, got {value!r}')
        return
    if fld.type == "string":
        if not isinstance(value, str) or isinstance(value, S.Symbol) or isinstance(value, bool):
            raise SchemaError(f'{where}: field "{fld.name}" has wrong value type — want '
                              f'string, got {value!r}')
        return
    # symbol
    if not isinstance(value, S.Symbol):
        raise SchemaError(f'{where}: field "{fld.name}" has wrong value type — want symbol, '
                          f'got {value!r}')
    if fld.values is not None and str(value) not in fld.values:
        raise SchemaError(f'{where}: field "{fld.name}": "{value}" is not one of '
                          f'{sorted(fld.values)}')


def validate_form(form, constructs: dict[str, Construct], where: str) -> None:
    """One form, validated in place; refusals raise SchemaError with the reason.

    A child list is headed by its field's name. Atom fields take exactly one value —
    `(name value)` — or zero when declared `(empty yes)` (a marker like `(requires)`).
    Form fields come in the two house shapes: when the field name is itself one of the
    allowed heads, the whole child list IS the nested form (`(source (file …) …)`);
    otherwise the child holds one nested form as its value (`(effect (set …))`), whose
    head must be among the declared heads. Repetition is sibling child lists.
    """
    head = str(form[0]) if form and isinstance(form[0], str) else None
    if not isinstance(form[0], S.Symbol) or head not in constructs:
        raise SchemaError(f'{where}: undeclared construct "{head}"')
    c = constructs[head]
    counts: dict[str, int] = {}
    for child in form[1:]:
        if not isinstance(child, list) or isinstance(child, S.Symbol) or not child:
            raise SchemaError(f'{where}: construct "{head}": expected a (field value) child '
                              f'list, got {child!r}')
        if not isinstance(child[0], S.Symbol):
            raise SchemaError(f'{where}: construct "{head}": a field name must be a bare '
                              f'symbol, got {child[0]!r}')
        fname = str(child[0])
        if fname not in c.fields:
            raise SchemaError(f'{where}: construct "{head}": undeclared field "{fname}"')
        fld = c.fields[fname]
        counts[fname] = counts.get(fname, 0) + 1
        if not fld.repeat and counts[fname] > 1:
            raise SchemaError(f'{where}: construct "{head}": duplicated single-valued field '
                              f'"{fname}"')
        if fld.type == "form":
            if fname in fld.heads:
                validate_form(child, constructs, where)            # (source (file …) …)
            else:
                if len(child) != 2 or not isinstance(child[1], list) \
                        or isinstance(child[1], S.Symbol):
                    raise SchemaError(f'{where}: construct "{head}" field "{fname}": wrong '
                                      f'arity — expects one nested form headed one of '
                                      f'{sorted(fld.heads)}, got {child!r}')
                inner = str(child[1][0]) \
                    if child[1] and isinstance(child[1][0], str) else None
                if inner not in fld.heads:
                    raise SchemaError(f'{where}: construct "{head}" field "{fname}": form '
                                      f'head "{inner}" is not one of {sorted(fld.heads)}')
                validate_form(child[1], constructs, where)         # (effect (set …))
        else:
            if len(child) == 1:
                if fld.type is None or fld.empty:
                    continue                        # the marker form: (name)
                raise SchemaError(f'{where}: construct "{head}" field "{fname}": wrong '
                                  f'arity — (name) with no value, and the field is not '
                                  f'declared (empty yes)')
            if fld.type is None:
                raise SchemaError(f'{where}: construct "{head}" field "{fname}": wrong arity '
                                  f'— a marker field is written (name) with no value, got '
                                  f'{child!r}')
            if len(child) != 2:
                raise SchemaError(f'{where}: construct "{head}" field "{fname}": wrong arity '
                                  f'— an atom field is (name value), got {len(child)} '
                                  f'element(s) in {child!r}')
            _check_atom(fld, child[1], f'{where}: construct "{head}"')
    for fname, fld in c.fields.items():
        if not fld.repeat and not fld.optional and counts.get(fname, 0) == 0:
            raise SchemaError(f'{where}: construct "{head}": missing required field '
                              f'"{fname}"')


def validate_file(path: Path, constructs: dict[str, Construct]) -> list[str]:
    """Every refusal, by name. An empty list is the pass verdict."""
    try:
        forms = S.read_file(path)
    except S.SexpError as exc:
        return [f"{path.name}: does not even parse: {exc}"]
    errors: list[str] = []
    for form in forms:
        if not isinstance(form, list) or not form:
            errors.append(f"{path.name}: top level holds a non-form {form!r}")
            continue
        try:
            validate_form(form, constructs, path.name)
        except SchemaError as exc:
            errors.append(str(exc))
    return errors


def check(file: Path, schema: Path) -> int:
    try:
        constructs = load_schema(schema)
    except (SchemaError, S.SexpError) as exc:
        print(f"  REFUSED the schema itself: {exc}", file=sys.stderr)
        return 1
    errors = validate_file(file, constructs)
    for e in errors:
        print(f"  REFUSED {e}", file=sys.stderr)
    if errors:
        print(f"check_sexp_schema: {len(errors)} refusal(s) against {schema}", file=sys.stderr)
        return 1
    print(f"check_sexp_schema: ok — {file} conforms to {schema.name}")
    return 0


# --------------------------------------------------------------------------- self-test

def _selftest() -> int:
    passed = failed = 0

    def arm(label, fn):
        nonlocal passed, failed
        try:
            fn()
        except AssertionError as exc:
            print(f"  FAIL  {label}: {exc}"); failed += 1
        except Exception as exc:                        # noqa: BLE001
            print(f"  FAIL  {label}: unexpected {type(exc).__name__}: {exc}"); failed += 1
        else:
            print(f"  ok    {label}"); passed += 1

    def eq(x, y): assert x == y, f"got {x!r}, want {y!r}"

    def refuses(file_text, schema_text, needle):
        with tempfile.TemporaryDirectory(dir=REPO / "target") as td:
            td = Path(td)
            f, s = td / "t.sexp", td / "s.sexp"
            f.write_text(file_text)
            s.write_text(schema_text)
            try:
                constructs = load_schema(s)
            except (SchemaError, S.SexpError) as exc:
                errs = [f"schema: {exc}"]
            else:
                errs = validate_file(f, constructs)
            assert errs, f"no refusal for {file_text!r}"
            assert any(needle in e for e in errs), \
                f"refusal named the wrong reason — wanted {needle!r}, got {errs}"

    def accepts(file_text, schema_text):
        with tempfile.TemporaryDirectory(dir=REPO / "target") as td:
            td = Path(td)
            f, s = td / "t.sexp", td / "s.sexp"
            f.write_text(file_text)
            s.write_text(schema_text)
            errs = validate_file(f, load_schema(s))
            assert not errs, f"unexpected refusals: {errs}"

    TOY = """(schema (id "toy"))

(construct (name unit)
  (field (name id) (type string))
  (field (name width) (type integer))
  (field (name mode) (type symbol) (values on) (values off) (optional yes))
  (field (name note) (type string) (repeat yes) (optional yes))
  (field (name meta) (empty yes) (optional yes))
  (field (name data) (type form) (head data) (repeat yes) (optional yes))
  (field (name effect) (type form) (head bump) (optional yes)))

(construct (name data)
  (field (name item) (type string) (repeat yes)))

(construct (name bump)
  (field (name by) (type integer)))"""

    arm("GREEN a conforming file validates — markers, repeats, both form shapes, recursion",
        lambda: accepts('(unit (id "u") (width 32) (mode on) (meta) '
                        '(note "a") (note "b") '
                        '(data (item "x") (item "y")) (data (item "z")) '
                        '(effect (bump (by 1))))', TOY))
    arm("RED   an undeclared construct is refused by name",
        lambda: refuses('(sourcs (id "u") (width 32))', TOY, 'undeclared construct "sourcs"'))
    arm("RED   an undeclared field is refused by name",
        lambda: refuses('(unit (id "u") (width 32) (widht 8))', TOY, 'undeclared field "widht"'))
    arm("RED   a missing required field is refused by name",
        lambda: refuses('(unit (id "u"))', TOY, 'missing required field "width"'))
    arm("RED   wrong arity — an atom field with two values",
        lambda: refuses('(unit (id "u" "v") (width 32))', TOY, "wrong arity"))
    arm("RED   wrong arity — an atom where a child list belongs",
        lambda: refuses('(unit (id "u") stray (width 32))', TOY, "expected a (field value) child"))
    arm("RED   wrong arity — a marker where the field is not declared (empty yes)",
        lambda: refuses('(unit (id "u") (width 32) (mode))', TOY, "not declared (empty yes)"))
    arm("RED   wrong value type — a string where a symbol belongs",
        lambda: refuses('(unit (id "u") (width 32) (mode "on"))', TOY, "want symbol"))
    arm("RED   wrong value type — a bare atom is not an integer",
        lambda: refuses('(unit (id "u") (width 1.5))', TOY, "want integer"))
    arm("RED   a duplicated single-valued field is refused by name",
        lambda: refuses('(unit (id "u") (id "v") (width 32))', TOY,
                        'duplicated single-valued field "id"'))
    arm("RED   a values restriction is enforced",
        lambda: refuses('(unit (id "u") (width 32) (mode maybe))', TOY, "is not one of"))
    arm("RED   a form value with the wrong head is refused",
        lambda: refuses('(unit (id "u") (width 32) (effect (widget (by 1))))', TOY,
                        'form head "widget"'))
    arm("RED   a nested form is validated recursively, not just its head",
        lambda: refuses('(unit (id "u") (width 32) (effect (bump (by "lots"))))', TOY,
                        "want integer"))
    arm("RED   the schema itself abusing the meta-level is refused (construct, no name)",
        lambda: refuses('(unit (id "u") (width 32))',
                        '(construct (field (name x) (type string)))', "needs exactly one"))
    arm("RED   a schema allowing an undeclared form head is refused",
        lambda: refuses('(unit (id "u") (width 32))',
                        '(schema (id "s"))\n'
                        '(construct (name unit) (field (name id) (type string))\n'
                        ' (field (name child) (type form) (head widget) (optional yes)))',
                        "allows undeclared head"))
    arm("GREEN the fixpoint: schema.sexp validates under itself",
        lambda: accepts((REPO / "schema/schema.sexp").read_text(),
                        (REPO / "schema/schema.sexp").read_text()))

    print(f"check_sexp_schema --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] == "--self-test":
        return _selftest()
    if len(argv) != 3:
        print("usage: check_sexp_schema.py <file.sexp> <schema.sexp> | --self-test",
              file=sys.stderr)
        return 2
    return check(Path(argv[1]), Path(argv[2]))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
