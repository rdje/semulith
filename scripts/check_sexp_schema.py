#!/usr/bin/env python3
"""Validate a source-of-truth file against a schema — both S-expressions.

The schema language is data (`schema/`): a schema declares constructs; a construct declares
its fields, their value types, whether they repeat, whether they are optional. An S-expression
reader accepts anything syntactically, so "it parses" is not validation — this is. An
undeclared construct, an undeclared field, a missing required field, a wrong arity, a wrong
value type or a duplicated single-valued field is refused BY NAME, never ignored
(`SOT-FORMAT.1`; acceptance criterion 3 of the tree).

The kernel below interprets `(construct …)` / `(field …)` declarations, and — since
`SOT-FORMAT.2` — `(operator …)` declarations for positional mini-languages the record grammar
cannot state (`(fixed (31 25 0x0) …)`, `(operands rd rs1 rs2)`, the semantics expression
forms). That interpretation is the named boundary: declaring a new CONSTRUCT or OPERATOR is
data in `schema/`; declaring a new KIND of declaration would change this kernel — the same
boundary a database draws between adding a table and adding a column type.

  python3 scripts/check_sexp_schema.py <file.sexp> <schema.sexp>   validate one file
  python3 scripts/check_sexp_schema.py --self-test                 the gate's own arms

Uniform arity rule at every level: a field instance is a child list headed by the field's
name. Atom-typed fields take exactly one value — `(name value)`. Form-typed fields take the
nested form itself, so `(child (unit (id "c")))` is the field `child` holding the form
`(unit …)`; repetition is sibling child lists with the same head, never extra elements in one
list.
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sexp as S                                   # noqa: E402

REPO = Path(__file__).resolve().parent.parent


class SchemaError(Exception):
    """A refusal. One error names the construct, the field, and the reason."""


# --------------------------------------------------------------------------- the comment form
# `SOT-FORMAT.4`: comments are FIRST-CLASS FORMS. `(comment "line" …)` is the format's reserved
# annotation head — part of its surface, like whitespace, not a domain construct. It may appear
# anywhere a form may appear (top level, inside a construct, in a schema file); validation skips
# it, and no schema may declare or forbid it. Everything else is still refused by name, and a
# typo'd `commment` is refused exactly as before. The head is reserved: a construct, operator or
# field named `comment` is refused, because the exemption would make it dead vocabulary.

def _is_comment(form) -> bool:
    return isinstance(form, list) and bool(form) and isinstance(form[0], S.Symbol) \
        and str(form[0]) == "comment"


def _check_comment(form, where: str) -> None:
    """A comment form carries one or more plain strings — nothing else."""
    if len(form) < 2:
        raise SchemaError(f"{where}: (comment …) carries at least one string, got none — "
                          f"an empty comment is silence, and silence is not annotation")
    for arg in form[1:]:
        if not isinstance(arg, str) or isinstance(arg, S.Symbol) or isinstance(arg, bool):
            raise SchemaError(f"{where}: a comment line is a plain string, got {arg!r}")



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
    """One field declaration, kernel-parsed.

    Since `SOT-FORMAT.3` a field may carry optional FACETS the record contracts already
    demanded of the JSON schemas: `(pattern "…")` and `(min-length N)` constrain string
    values (regex search, JSON-Schema `pattern` semantics; minimum length); `(min N)` and
    `(unique yes)` constrain repeated fields (at least N occurrences; no two occurrences
    equal). Facets are data in the schema file, like `(values …)` — declaring them is not a
    kernel change.
    """

    def __init__(self, where: str, form):
        g = _group(_pairs(form, where), where,
                   single=("name", "type", "repeat", "optional", "empty",
                           "pattern", "min-length", "min", "unique"),
                   multi=("head", "values"))
        if "name" not in g:
            raise SchemaError(f"{where}: a (field …) needs exactly one (name SYM)")
        name = _atom(g["name"], where)
        if not isinstance(name, S.Symbol):
            raise SchemaError(f"{where}: field name must be a bare symbol, got {name!r}")
        self.name = str(name)
        if self.name == "comment":
            raise SchemaError(f"{where}: field name 'comment' is reserved — the annotation form "
                              f"is skipped everywhere, so a field with that name is dead vocabulary")
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
        for flag in ("repeat", "optional", "empty", "unique"):
            v = g.get(flag)
            if v is None:
                setattr(self, flag, False)
                continue
            v = _atom(v, where)
            if v not in ("yes", "no"):
                raise SchemaError(f"{where}: field {self.name}: ({flag} …) is yes or no, "
                                  f"got {v!r}")
            setattr(self, flag, v == "yes")
        # facets ---------------------------------------------------------------------------------
        self.pattern = None
        if "pattern" in g:
            if self.type != "string":
                raise SchemaError(f"{where}: field {self.name}: (pattern …) constrains a "
                                  f"string field, not type {self.type!r}")
            pat = g["pattern"]
            if not isinstance(pat, str) or isinstance(pat, S.Symbol):
                raise SchemaError(f"{where}: field {self.name}: (pattern …) takes a quoted "
                                  f"regex string, got {pat!r}")
            try:
                re.compile(pat)
            except re.error as exc:
                raise SchemaError(f"{where}: field {self.name}: (pattern …) is not a valid "
                                  f"regex: {exc}") from exc
            self.pattern = pat
        self.min_length = None
        if "min-length" in g:
            if self.type != "string":
                raise SchemaError(f"{where}: field {self.name}: (min-length …) constrains a "
                                  f"string field, not type {self.type!r}")
            n = g["min-length"]
            if not isinstance(n, int) or isinstance(n, bool) or n < 0:
                raise SchemaError(f"{where}: field {self.name}: (min-length N) takes one "
                                  f"non-negative integer, got {n!r}")
            self.min_length = n
        self.min = None
        if "min" in g:
            if not self.repeat:
                raise SchemaError(f"{where}: field {self.name}: (min N) belongs to a "
                                  f"(repeat yes) field — it counts occurrences")
            n = g["min"]
            if not isinstance(n, int) or isinstance(n, bool) or n < 0:
                raise SchemaError(f"{where}: field {self.name}: (min N) takes one "
                                  f"non-negative integer, got {n!r}")
            self.min = n
        if self.unique and not self.repeat:
            raise SchemaError(f"{where}: field {self.name}: (unique yes) belongs to a "
                              f"(repeat yes) field — singularity is its own constraint")


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
    for c in children:
        if _is_comment(c):
            _check_comment(c, where)                  # annotations may annotate declarations
    children = [c for c in children if not _is_comment(c)]
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
    if c.name == "comment":
        raise SchemaError(f"{where}: construct name 'comment' is reserved for the annotation "
                          f"form — validation skips it, so a construct with that name is dead "
                          f"vocabulary")
    if c.name in constructs:
        raise SchemaError(f"{where}: construct {c.name!r} declared twice")
    constructs[c.name] = c


# --------------------------------------------------------------------------- operators
# A positional form language: `(add (reg rd) (reg rs2))` is not made of (name value) field
# pairs, and no record grammar can state it honestly. An operator declaration carries a head,
# an arity (exactly N, or variadic with a minimum), and one argument spec shared by every
# position: an atom kind (symbol|integer|string), `expr` (an atom or a nested operator form —
# the default), or a fixed-length tuple of atom kinds for one positional argument.

_ARG_KINDS = ("symbol", "integer", "string", "expr")


class Operator:
    """One (operator …) declaration, kernel-parsed like Construct/Field."""

    def __init__(self, where: str, form):
        name = fixed = variadic = min_v = arg = None          # None = not seen
        for child in form[1:]:
            if not isinstance(child, list) or isinstance(child, S.Symbol) or not child:
                raise SchemaError(f"{where}: an (operator …) holds a declaration list, got "
                                  f"{child!r}")
            if not isinstance(child[0], S.Symbol):
                raise SchemaError(f"{where}: an operator declaration is headed by a bare "
                                  f"symbol, got {child[0]!r}")
            key, arity = str(child[0]), len(child)
            if key == "name":
                if name is not None:
                    raise SchemaError(f"{where}: duplicated (name …) in an operator declaration")
                if arity != 2:
                    raise SchemaError(f"{where}: (name …) takes one symbol, got {child!r}")
                name = child[1]
            elif key == "fixed":
                if fixed is not None:
                    raise SchemaError(f"{where}: duplicated (fixed …) in an operator declaration")
                if arity != 2 or not isinstance(child[1], int) or isinstance(child[1], bool) \
                        or child[1] < 0:
                    raise SchemaError(f"{where}: (fixed N) takes one non-negative integer, got "
                                      f"{child!r}")
                fixed = child[1]
            elif key == "variadic":
                if arity != 1:
                    raise SchemaError(f"{where}: (variadic) is a bare marker, got {child!r}")
                variadic = True
            elif key == "min":
                if min_v is not None:
                    raise SchemaError(f"{where}: duplicated (min …) in an operator declaration")
                if arity != 2 or not isinstance(child[1], int) or isinstance(child[1], bool) \
                        or child[1] < 0:
                    raise SchemaError(f"{where}: (min N) takes one non-negative integer, got "
                                      f"{child!r}")
                min_v = child[1]
            elif key == "arg":
                if arg is not None:
                    raise SchemaError(f"{where}: duplicated (arg …) in an operator declaration")
                if arity != 2:
                    raise SchemaError(f"{where}: (arg SPEC) takes one spec, got {child!r}")
                arg = child[1]
            else:
                raise SchemaError(f"{where}: undeclared field {key!r} in an operator "
                                  f"declaration")
        if name is None:
            raise SchemaError(f"{where}: an (operator …) needs exactly one (name SYM)")
        if not isinstance(name, S.Symbol):
            raise SchemaError(f"{where}: operator name must be a bare symbol, got {name!r}")
        self.name = str(name)
        if (fixed is None) == (variadic is None):
            raise SchemaError(f"{where}: operator {self.name!r} declares exactly one of "
                              f"(fixed N) / (variadic)")
        self.fixed = fixed
        if min_v is not None and variadic is None:
            raise SchemaError(f"{where}: operator {self.name!r}: (min …) belongs to (variadic), "
                              f"not (fixed N)")
        self.min = 1 if min_v is None else min_v
        self.spec = "expr" if arg is None else self._spec(where, arg)

    @staticmethod
    def _spec(where: str, value):
        if isinstance(value, S.Symbol):
            if str(value) not in _ARG_KINDS:
                raise SchemaError(f"{where}: unknown argument kind {value!r} — one of "
                                  f"{list(_ARG_KINDS)}")
            return str(value)
        if isinstance(value, list) and value and not isinstance(value, S.Symbol):
            kinds = []
            for el in value:
                if not isinstance(el, S.Symbol) or str(el) not in _ARG_KINDS or str(el) == "expr":
                    raise SchemaError(f"{where}: a tuple argument spec holds atom kinds, got "
                                      f"{value!r}")
                kinds.append(str(el))
            return tuple(kinds)
        raise SchemaError(f"{where}: (arg SPEC) wants an atom kind or a list of atom kinds, "
                          f"got {value!r}")


def load_schema(path: Path) -> tuple[dict[str, Construct], dict[str, Operator]]:
    constructs: dict[str, Construct] = {}
    operators: dict[str, Operator] = {}
    for form in S.read_file(path):
        if not isinstance(form, list) or not form:
            raise SchemaError(f'{path.name}: a schema is made of (schema …)/(construct …)/'
                              f'(operator …) forms, got {form!r}')
        head = S.head(form, str(path))
        if _is_comment(form):
            _check_comment(form, str(path))
            continue
        if head == "schema":
            continue                        # the metadata form: (schema (id STRING))
        if head == "construct":
            _declare(constructs, form, f"{path.name}")
            continue
        if head == "operator":
            op = Operator(f"{path.name}", form)
            if op.name == "comment":
                raise SchemaError(f"{path.name}: operator name 'comment' is reserved for the "
                                  f"annotation form")
            if op.name in constructs:
                raise SchemaError(f"{path.name}: {op.name!r} is declared both as a construct "
                                  f"and as an operator")
            if op.name in operators:
                raise SchemaError(f"{path.name}: operator {op.name!r} declared twice")
            operators[op.name] = op
            continue
        raise SchemaError(f'{path.name}: undeclared top-level construct "{head}" in a schema — '
                          f'only (schema …), (construct …) and (operator …) may live here')
    if not constructs:
        raise SchemaError(f"{path.name}: the schema declares no constructs")
    for c in constructs.values():
        for fld in c.fields.values():
            for h in fld.heads:
                if h not in constructs and h not in operators:
                    raise SchemaError(f"{path.name}: construct {c.name!r} field {fld.name!r} "
                                      f"allows undeclared head {h!r}")
    return constructs, operators


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
        if fld.min_length is not None and len(value) < fld.min_length:
            raise SchemaError(f'{where}: field "{fld.name}" is shorter than min-length '
                              f'{fld.min_length}, got {value!r}')
        if fld.pattern is not None and not re.search(fld.pattern, value):
            raise SchemaError(f'{where}: field "{fld.name}" value {value!r} does not match '
                              f'/{fld.pattern}/')
        return
    # symbol
    if not isinstance(value, S.Symbol):
        raise SchemaError(f'{where}: field "{fld.name}" has wrong value type — want symbol, '
                          f'got {value!r}')
    if fld.values is not None and str(value) not in fld.values:
        raise SchemaError(f'{where}: field "{fld.name}": "{value}" is not one of '
                          f'{sorted(fld.values)}')


def _check_op_arg(spec, value, operators: dict[str, Operator], where: str) -> None:
    """One positional argument of an operator form, against the declared spec."""
    if isinstance(spec, tuple):
        if not isinstance(value, list) or isinstance(value, S.Symbol):
            raise SchemaError(f'{where}: wants a list of {len(spec)} value(s), got {value!r}')
        if len(value) != len(spec):
            raise SchemaError(f'{where}: wants a list of {len(spec)} value(s), got '
                              f'{len(value)} in {value!r}')
        for el, kind in zip(value, spec):
            _check_op_arg(kind, el, operators, where)
        return
    if spec == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            raise SchemaError(f'{where}: wants an integer, got {value!r}')
        return
    if spec == "symbol":
        if not isinstance(value, S.Symbol):
            raise SchemaError(f'{where}: wants a bare symbol, got {value!r}')
        return
    if spec == "string":
        if not isinstance(value, str) or isinstance(value, S.Symbol) or isinstance(value, bool):
            raise SchemaError(f'{where}: wants a string, got {value!r}')
        return
    # expr: an atom or an operator form. Which atoms are legal here is the consumer's business
    # (operand scoping needs the encoding, which the schema layer does not read).
    if isinstance(value, list) and not isinstance(value, S.Symbol):
        if not value:
            raise SchemaError(f'{where}: an empty form is not an expression')
        _validate_operator(value, operators, where)
        return
    if isinstance(value, bool) or (isinstance(value, str) and not isinstance(value, S.Symbol)):
        raise SchemaError(f'{where}: a string is not an expression — unquote it or use a '
                          f'symbol, got {value!r}')


def _validate_operator(form, operators: dict[str, Operator], where: str) -> None:
    """A positional form, validated against its operator declaration."""
    head = str(form[0]) if form and isinstance(form[0], S.Symbol) else None
    op = operators.get(head) if head else None
    if op is None:
        raise SchemaError(f'{where}: undeclared operator "{head}"')
    args = form[1:]
    if op.fixed is not None:
        if len(args) != op.fixed:
            raise SchemaError(f'{where}: ({op.name} …) takes {op.fixed} argument(s), got '
                              f'{len(args)}')
    elif len(args) < op.min:
        raise SchemaError(f'{where}: ({op.name} …) takes at least {op.min} argument(s), got '
                          f'{len(args)}')
    for a in args:
        _check_op_arg(op.spec, a, operators, where)


def validate_form(form, constructs: dict[str, Construct], operators: dict[str, Operator],
                  where: str) -> None:
    """One form, validated in place; refusals raise SchemaError with the reason.

    A child list is headed by its field's name. Atom fields take exactly one value —
    `(name value)` — or zero when declared `(empty yes)` (a marker like `(requires)`).
    Form fields come in the two house shapes: when the field name is itself one of the
    allowed heads, the whole child list IS the nested form (`(source (file …) …)`);
    otherwise the child holds one nested form as its value (`(effect (set …))`), whose
    head must be among the declared heads. Repetition is sibling child lists. A form whose
    head is an OPERATOR (a positional mini-language) is validated against its arity and
    argument spec instead.
    """
    head = str(form[0]) if form and isinstance(form[0], str) else None
    if not isinstance(form[0], S.Symbol):
        raise SchemaError(f'{where}: expected a form headed by a symbol, got {form!r}')
    if head in operators:
        _validate_operator(form, operators, where)
        return
    if head not in constructs:
        raise SchemaError(f'{where}: undeclared construct "{head}"')
    c = constructs[head]
    counts: dict[str, int] = {}
    seen: dict[str, list] = {}
    for child in form[1:]:
        if not isinstance(child, list) or isinstance(child, S.Symbol) or not child:
            raise SchemaError(f'{where}: construct "{head}": expected a (field value) child '
                              f'list, got {child!r}')
        if _is_comment(child):
            _check_comment(child, where)              # the annotation form is skipped, checked
            continue
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
                validate_form(child, constructs, operators, where)   # (source (file …) …)
                seen.setdefault(fname, []).append(child)
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
                validate_form(child[1], constructs, operators, where)  # (effect (set …))
                seen.setdefault(fname, []).append(child[1])
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
            seen.setdefault(fname, []).append(child[1])
    for fname, fld in c.fields.items():
        n = counts.get(fname, 0)
        if not fld.repeat and not fld.optional and n == 0:
            raise SchemaError(f'{where}: construct "{head}": missing required field '
                              f'"{fname}"')
        if fld.repeat and fld.min is not None and n < fld.min:
            raise SchemaError(f'{where}: construct "{head}": field "{fname}" appears {n} '
                              f'time(s), min is {fld.min} — an empty list is not a citation')
        if fld.repeat and fld.unique:
            vals = seen.get(fname, [])
            for i in range(len(vals)):
                for j in range(i + 1, len(vals)):
                    if vals[i] == vals[j]:
                        raise SchemaError(f'{where}: construct "{head}": field "{fname}" '
                                          f'repeats {vals[i]!r} — unique means written once')


def validate_file(path: Path, constructs: dict[str, Construct],
                  operators: dict[str, Operator]) -> list[str]:
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
        if _is_comment(form):
            try:
                _check_comment(form, path.name)
            except SchemaError as exc:
                errors.append(str(exc))
            continue
        try:
            validate_form(form, constructs, operators, path.name)
        except SchemaError as exc:
            errors.append(str(exc))
    return errors


def check(file: Path, schema: Path) -> int:
    try:
        constructs, operators = load_schema(schema)
    except (SchemaError, S.SexpError) as exc:
        print(f"  REFUSED the schema itself: {exc}", file=sys.stderr)
        return 1
    errors = validate_file(file, constructs, operators)
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
                constructs, operators = load_schema(s)
            except (SchemaError, S.SexpError) as exc:
                errs = [f"schema: {exc}"]
            else:
                errs = validate_file(f, constructs, operators)
            assert errs, f"no refusal for {file_text!r}"
            assert any(needle in e for e in errs), \
                f"refusal named the wrong reason — wanted {needle!r}, got {errs}"

    def refuses_schema(schema_text, needle):
        with tempfile.TemporaryDirectory(dir=REPO / "target") as td:
            s = Path(td) / "s.sexp"
            s.write_text(schema_text)
            try:
                load_schema(s)
            except (SchemaError, S.SexpError) as exc:
                assert needle in str(exc), \
                    f"refusal named the wrong reason — wanted {needle!r}, got {exc}"
            else:
                raise AssertionError(f"schema {schema_text!r} must be refused")

    def accepts(file_text, schema_text):
        with tempfile.TemporaryDirectory(dir=REPO / "target") as td:
            td = Path(td)
            f, s = td / "t.sexp", td / "s.sexp"
            f.write_text(file_text)
            s.write_text(schema_text)
            errs = validate_file(f, *load_schema(s))
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

    # --- operators: positional mini-languages (`SOT-FORMAT.2`) ---------------------------
    TOYO = """(schema (id "toyo"))

(construct (name unit)
  (field (name id) (type string))
  (field (name width) (type integer))
  (field (name body) (type form)
         (head bump) (head pair) (head many) (head any) (head triple) (repeat yes) (optional yes)))

(operator (name bump) (fixed 1) (arg symbol))
(operator (name pair) (fixed 2))
(operator (name many) (variadic) (arg integer))
(operator (name any) (variadic) (min 0))
(operator (name triple) (variadic) (arg (integer integer integer)))"""

    # A faithful miniature of the fragment mini-languages: fixed triples, bare-symbol operands.
    TOYF = TOYO + """

(construct (name insn)
  (field (name name) (type symbol))
  (field (name fixed) (type form) (head fixed))
  (field (name operands) (type form) (head operands)))

(operator (name fixed) (variadic) (arg (integer integer integer)))
(operator (name operands) (variadic) (min 0) (arg symbol))"""

    GOOD = ('(unit (id "u") (width 32) '
            '(body (pair (bump rd) (pair a b))) (body (triple (1 2 3) (4 5 6))) '
            '(body (many 1 2 3)) (body (any)) (body (any x 7)))')
    arm("GREEN operator forms validate — fixed arity, nesting, variadic min, arg kinds",
        lambda: accepts(GOOD, TOYO))
    arm("GREEN the fragment shapes are operators — fixed triples and bare-symbol operands",
        lambda: accepts(GOOD + ' (insn (name add) (fixed (31 25 0x0) (14 12 0xc)) '
                               '(operands rd rs1 rs2)) '
                               '(insn (name ecall) (fixed (31 20 0x0)) (operands))', TOYF))
    arm("RED   an undeclared operator head is refused by name",
        lambda: refuses('(unit (id "u") (width 32) (body (pair a (widget x))))', TOYO,
                        'undeclared operator "widget"'))
    arm("RED   a fixed-arity operator with the wrong count is refused",
        lambda: refuses('(unit (id "u") (width 32) (body (pair a)))', TOYO,
                        "takes 2 argument(s), got 1"))
    arm("RED   a variadic operator below its minimum is refused",
        lambda: refuses('(unit (id "u") (width 32) (body (many)))', TOYO,
                        "takes at least 1 argument(s), got 0"))
    arm("RED   an integer argument slot refuses a symbol",
        lambda: refuses('(unit (id "u") (width 32) (body (many 1 rs)))', TOYO,
                        "wants an integer"))
    arm("RED   a symbol argument slot refuses an integer",
        lambda: refuses('(unit (id "u") (width 32) (body (bump 7)))', TOYO,
                        "wants a bare symbol"))
    arm("RED   a tuple argument spec refuses a wrong length",
        lambda: refuses('(unit (id "u") (width 32) (body (triple (1 2))))', TOYO,
                        "wants a list of 3 value(s), got 2"))
    arm("RED   a tuple argument spec refuses a wrong element kind",
        lambda: refuses('(unit (id "u") (width 32) (body (triple (1 rs 3))))', TOYO,
                        "wants an integer"))
    arm("RED   an expression argument refuses a quoted string",
        lambda: refuses('(unit (id "u") (width 32) (body (pair "a" b)))', TOYO,
                        "is not an expression"))
    arm("RED   the operator meta-level refuses fixed and variadic together",
        lambda: refuses_schema(TOYO + "\n(operator (name bad) (fixed 1) (variadic))",
                               "exactly one of"))
    arm("RED   the operator meta-level refuses (min …) without (variadic)",
        lambda: refuses_schema(TOYO + "\n(operator (name bad) (fixed 1) (min 0))", "(min …)"))
    arm("RED   the operator meta-level refuses an unknown argument kind",
        lambda: refuses_schema(TOYO + "\n(operator (name bad) (fixed 1) (arg number))",
                               "unknown argument kind"))
    arm("RED   the operator meta-level refuses a duplicated declaration",
        lambda: refuses_schema(TOYO + "\n(operator (name bump) (fixed 2))", "declared twice"))
    arm("RED   a name declared as both construct and operator is refused",
        lambda: refuses_schema('(schema (id "s"))\n(construct (name dual) '
                               '(field (name x) (type string)))\n(operator (name dual) (fixed 1))',
                               "both as a construct"))

    # --- facets: the record contracts' discriminating power, as data (`SOT-FORMAT.3`) ----------
    TOYFAC = """(schema (id "toyfac"))

(construct (name rec)
  (field (name id) (type string) (pattern "^[A-Z][A-Z0-9-]*$"))
  (field (name title) (type string) (min-length 1))
  (field (name tag) (type symbol) (repeat yes) (min 1) (unique yes)
         (values red) (values blue))
  (field (name alias) (type string) (repeat yes) (unique yes) (optional yes)))"""

    arm("GREEN facets hold — pattern, min-length, min and unique all satisfied",
        lambda: accepts('(rec (id "REQ-X") (title "t") (tag red) (tag blue) '
                        '(alias "a") (alias "b"))', TOYFAC))
    arm("RED   a pattern mismatch is refused by name",
        lambda: refuses('(rec (id "req-x") (title "t") (tag red))', TOYFAC,
                        "does not match"))
    arm("RED   a min-length violation is refused by name",
        lambda: refuses('(rec (id "REQ-X") (title "") (tag red))', TOYFAC,
                        "shorter than min-length"))
    arm("RED   a repeat below its min is refused — an empty list is not a citation",
        lambda: refuses('(rec (id "REQ-X") (title "t"))', TOYFAC, "min is 1"))
    arm("RED   a unique repeat refusing a duplicated value",
        lambda: refuses('(rec (id "REQ-X") (title "t") (tag red) (tag red))', TOYFAC,
                        "unique"))
    arm("RED   a unique string repeat refusing a duplicated value",
        lambda: refuses('(rec (id "REQ-X") (title "t") (tag red) (alias "a") '
                        '(alias "a"))', TOYFAC, "unique"))
    arm("RED   the meta-level refuses a pattern on a non-string field",
        lambda: refuses_schema(TOYFAC + '\n(construct (name bad) '
                               '(field (name n) (type integer) (pattern "^x$")))',
                               "(pattern …) constrains a string"))
    arm("RED   the meta-level refuses min-length on a non-string field",
        lambda: refuses_schema(TOYFAC + '\n(construct (name bad) '
                               '(field (name n) (type integer) (min-length 1)))',
                               "(min-length …) constrains a string"))
    arm("RED   the meta-level refuses min on a non-repeating field",
        lambda: refuses_schema(TOYFAC + '\n(construct (name bad) '
                               '(field (name n) (type string) (min 1)))',
                               "(min N) belongs to a (repeat yes)"))
    arm("RED   the meta-level refuses unique on a non-repeating field",
        lambda: refuses_schema(TOYFAC + '\n(construct (name bad) '
                               '(field (name n) (type string) (unique yes)))',
                               "(unique yes) belongs to a (repeat yes)"))
    arm("RED   the meta-level refuses an invalid regex",
        lambda: refuses_schema(TOYFAC + '\n(construct (name bad) '
                               '(field (name n) (type string) (pattern "^[(")))',
                               "not a valid regex"))
    arm("RED   the meta-level refuses a non-integer min-length",
        lambda: refuses_schema(TOYFAC + '\n(construct (name bad) '
                               '(field (name n) (type string) (min-length one)))',
                               "(min-length N) takes one non-negative integer"))

    # --- the comment form: first-class annotations (`SOT-FORMAT.4`) ---------------------------
    arm("GREEN a comment form is allowed anywhere — top level and inside a construct",
        lambda: accepts('(comment "why this file exists") '
                        '(unit (id "u") (width 32) (comment "why 32"))', TOY))
    arm("RED   an empty comment is refused — silence is not annotation",
        lambda: refuses('(comment)', TOY, "at least one string"))
    arm("RED   a comment line that is not a string is refused",
        lambda: refuses('(comment 42)', TOY, "plain string"))
    arm("RED   a comment holding a nested form is refused",
        lambda: refuses('(unit (id "u") (width 32) (comment (why)))', TOY, "plain string"))
    arm("RED   the typo commment is still refused by name",
        lambda: refuses('(unit (id "u") (width 32) (commment "why"))', TOY,
                        'undeclared field "commment"'))
    arm("RED   a construct named comment is refused — the head is reserved",
        lambda: refuses_schema(TOY + '\n(construct (name comment) (field (name x) (type string)))',
                               "reserved"))
    arm("RED   a field named comment is refused — the head is reserved",
        lambda: refuses_schema(TOY + '\n(construct (name unit2) '
                               '(field (name comment) (type string)))', "reserved"))

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
