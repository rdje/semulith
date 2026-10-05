#!/usr/bin/env python3
"""The dossier mapping: TOML/JSON-shaped profile documents <-> S-expression forms.

SINGLE OWNER OF THE MAPPING — the `SOT-FORMAT.4` sibling of `records_sexp.py` (`.3`). The
profile dossier (decisions, architectural state, pinned sources, the reference dossier, the
matched-profile override, guest expectations) is a source of truth, so it moved behind the
schema layer like the record catalogues; every consumer that needs these documents as dicts
reads through this module. The TOML/JSON <-> form correspondence lives here, exactly once.

The mapping rules (design recorded in docs/tasks/SOT-FORMAT.md, leaf `.4`):

  table -> form, [[array]] -> repeated sibling forms; JSON objects nest the same way
  keys   -> field names verbatim — no translation table to drift
  integer -> integer atom; string -> string VERBATIM (a hex address written "0x…" stays a
             string: the data model is unchanged and the round-trip proof is exact)
  float  -> refused (none exist; the day one appears is a schema decision, not a guess)
  bool   -> (true)/(false) — the `.3` wrappers, as declared nullary marker constructs
  scalar arrays -> repeated atom fields; empty arrays -> absence (the `.3` rules); the loader
             reconstructs the empty lists the document shape promises
  arrays of objects -> repeated form fields; dynamic-keyed maps (guest `writes`, override
             `extensions`) normalize to entry forms — a schema cannot declare a hundred
             extension names, and a wildcard field would gut "undeclared is refused by name"
  `authority` (the one project-owned closed enum) -> a symbol; vocabularies the dossier merely
             RECORDS (candidate status, difference kind, mem_type…) stay strings
  (comment "…") forms are the format's annotations (`.4`): the loader skips them everywhere;
             conversion places them and `convert_dossier.py --verify` proves the census.

`load_*` returns exactly the dict `tomllib`/`json` produced for the same document — consumer
logic is untouched; only the seam moved. That data equality is what makes the leaf's
"identical verdicts" acceptance mechanical rather than hopeful.
"""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sexp as S                                # noqa: E402


class DossierError(Exception):
    """A document the mapping does not carry. Refused, never guessed."""


# --------------------------------------------------------------------------- small machinery

def _pair(name: str, value) -> list:
    return [S.Symbol(name), value]


def _sym(value: str) -> S.Symbol:
    return S.Symbol(value)


def _rep(name: str, values) -> list:
    return [_pair(name, v) for v in values]


def _bool_field(name: str, value: bool) -> list:
    if not isinstance(value, bool):
        raise DossierError(f"not a boolean: {value!r}")
    return _pair(name, _sym("true") if value else _sym("false"))


def _atom_out(value):
    """A data scalar -> its form atom: strings verbatim, bools as the marker forms."""
    if isinstance(value, bool):
        raise DossierError(f"a bare boolean is not an atom: {value!r}")
    if isinstance(value, str):
        return value
    if isinstance(value, int):
        return value
    raise DossierError(f"no S-expression value for {value!r} — a float or nested value "
                       f"needs a schema decision, not a guessed translation")


def _s(value) -> str:
    return str(value)


def _is_note(child) -> bool:
    return isinstance(child, list) and bool(child) and str(child[0]) == "comment"


def _fields(form):
    """A construct's data children, annotations skipped, order preserved."""
    return [c for c in form[1:] if isinstance(c, list) and not _is_note(c)]


def _value(child, where: str):
    if len(child) != 2:
        raise DossierError(f"{where}: ({child[0]} …) carries exactly one value, got {child!r}")
    return child[1]


def _opt(form, name: str, where: str):
    """The optional single value `(name VALUE)`, or None."""
    found = [c for c in _fields(form) if str(c[0]) == name]
    if not found:
        return None
    if len(found) > 1:
        raise DossierError(f"{where}: ({name} …) appears {len(found)} times, want at most one")
    return _value(found[0], where)


def _req(form, name: str, where: str):
    v = _opt(form, name, where)
    if v is None:
        raise DossierError(f"{where}: missing ({name} …)")
    return v


def _rep_in(form, name: str) -> list:
    """Values of repeated `(name VALUE)` children, order preserved."""
    out = []
    for c in _fields(form):
        if str(c[0]) == name:
            out.append(_value(c, f"({name} …)"))
    return out


def _child_in(form, name: str) -> list:
    """The single nested whole-list child `(name (head …) …)`."""
    found = [c for c in _fields(form) if str(c[0]) == name]
    if len(found) != 1:
        raise DossierError(f"expected exactly one ({name} (…)), found {len(found)}")
    return found[0]


def _opt_child(form, name: str):
    found = [c for c in _fields(form) if str(c[0]) == name]
    if not found:
        return None
    if len(found) > 1:
        raise DossierError(f"({name} (…)) appears {len(found)} times, want at most one")
    return found[0]


def _children_in(form, name: str) -> list:
    """Every nested whole-list child whose head is `name` (field name == head shape)."""
    return [c for c in _fields(form) if str(c[0]) == name]


def _truthy(value, where: str) -> bool:
    s = str(value)
    if s == "true":
        return True
    if s == "false":
        return False
    raise DossierError(f"{where}: expected true/false, got {value!r}")


def _bool_in(form, name: str, where: str) -> bool:
    return _truthy(_value(_child_in(form, name), where), where)


def _reset_doc(rf) -> dict:
    """One (reset …) form as a dict — the state document's shared reset construct."""
    return {"value": _s(_req(rf, "value", "reset")),
            "authority": _s(_req(rf, "authority", "reset")),
            "source": _s(_req(rf, "source", "reset")),
            "statement": _s(_req(rf, "statement", "reset"))}


def _nested_in(form, name: str, where: str):
    """The single nested form held as a field value — `(name (head …))` -> `(head …)`."""
    return _value(_child_in(form, name), where)


def _int64_in(form, name: str):
    return _nested_in(form, name, "region")


def _flag_in(form, name: str, where: str) -> bool:
    """`(name (supported true|false))` — the override's supported-flag shape."""
    return _bool_in(_child_in(form, name), "supported", where)


def _opt_bool_in(form, name: str, where: str):
    c = _opt_child(form, name)
    if c is None:
        return None
    return _truthy(_value(c, where), where)


# A flat field spec drives the record-shaped families: name -> kind.
#   "str" | "int"  scalar fields; "strs" repeated strings (empty list == absence);
#   "bool" the (true)/(false) marker form.
def _emit_flat(spec: list[tuple[str, str]], d: dict) -> list:
    out = []
    for name, kind in spec:
        if kind == "strs":
            out += _rep(name, d.get(name) or [])
        elif kind == "bool":
            if name in d:
                out.append(_bool_field(name, d[name]))
        elif name in d:
            out.append(_pair(name, _sym(d[name]) if kind == "sym" else _atom_out(d[name])))
    return out


def _read_flat(spec: list[tuple[str, str]], form, where: str,
               skip: tuple[str, ...] = ()) -> dict:
    d: dict = {}
    kinds = {n: k for n, k in spec}
    for c in _fields(form):
        h = str(c[0])
        if h in skip:
            continue
        if h not in kinds:
            raise DossierError(f"{where}: undeclared field {h!r}")
        kind = kinds[h]
        if kind == "strs":
            d[h] = _rep_in(form, h)
        elif kind == "bool":
            d[h] = _bool_in(form, h, where)
        elif kind == "sym":
            d[h] = _s(_value(c, where))
        else:
            d[h] = _value(c, where)
    return d


# --------------------------------------------------------------------------- profile.toml

# The scope taxonomy's closed group-name set — the other place it lives is
# schema/profile.sexp's scope construct; the two are extended together. The dsp56300
# groups (P3-BREADTH.5 slice 2, case dsp56300-lab-v0: moves, alu_core, multiplies, flow,
# loops) join the scalar set; the gate readers are generic over group names, so adding a
# name here and in the schema is the whole extension. P5-BOARD.2 (2026-10-02, case
# sifive-uart-lab-v0): mmio_registers, the device register census, joins the same way.
_SCOPE_LISTS = ("base_u_type", "base_jumps", "base_branches", "base_loads", "base_stores",
                "base_op_imm", "base_op", "base_misc_mem", "base_system", "rv64_loads",
                "rv64_stores", "rv64_op_imm_32", "rv64_op_32",
                "moves", "alu_core", "multiplies", "flow", "loops",
                "mmio_registers",
                "zicsr_csrs", "system_privileged", "zicntr_counters", "a_atomics",
                "zifencei_fencei")

_PROFILE_SPEC = [("id", "str"), ("version", "str"), ("status", "str"), ("architecture", "str"),
                 ("base", "str"), ("chapter_version", "str"), ("spec_revision", "str"),
                 ("harts", "int"), ("xlen", "int"), ("ilen", "int"), ("ialign", "int"),
                 ("endianness", "sym"),
                 ("extensions", "strs"), ("privilege_modes", "strs"), ("sources", "strs")]

_STATE_SPEC = [("integer_registers", "int"), ("x0_hardwired_zero", "bool"),
               ("register_width_bits", "int"), ("program_counter", "str"),
               ("csrs", "strs"), ("authority", "sym"), ("source", "str")]

_DECISION_SPEC = [("id", "str"), ("authority", "sym"), ("statement", "str"),
                  ("source", "str"), ("note", "str")]

# P3-BREADTH.7 slice 1 (case dsp56300-lab-v0): the declared vehicle — the unit's model
# route and comparison shape; gates derive applicability from it
# (decision_gate-applicability-by-declared-vehicle).
_VEHICLE_SPEC = [("route", "sym"), ("comparison", "sym"), ("authority", "sym"),
                 ("source", "str")]


def profile_to_form(doc: dict) -> list:
    prof = doc["profile"]
    root = [S.Symbol("profile")]
    for k, v in prof.items():
        root += _rep(k, v) if isinstance(v, list) else [_pair(k, _atom_out(v))]
    if doc.get("state"):
        root.append([S.Symbol("state"), *_emit_flat(_STATE_SPEC, doc["state"])])
    if doc.get("scope"):
        root.append([S.Symbol("scope"), *_emit_flat(_SCOPE_SPEC(), doc["scope"])])
    if doc.get("vehicle"):
        root.append([S.Symbol("vehicle"), *_emit_flat(_VEHICLE_SPEC, doc["vehicle"])])
    for dec in doc.get("decision", []):
        root.append([S.Symbol("decision"), *_emit_flat(_DECISION_SPEC, dec)])
    return root


def _SCOPE_SPEC() -> list[tuple[str, str]]:
    return [("count_base", "int"), ("count_rv64i_additions", "int"), ("count_total", "int"),
            ("authority", "sym"), ("source", "str")] + [(k, "strs") for k in _SCOPE_LISTS]


def profile_to_doc(form) -> dict:
    S.head(form, "profile")
    prof = _read_flat(_PROFILE_SPEC, form, "profile", skip=("state", "scope", "decision",
                                                           "vehicle"))
    # the [profile] table always declares these lists, empty or not; absence is the empty
    # array (`.3` rule), so the fixed document shape reconstructs them
    for k in ("extensions", "privilege_modes"):
        prof.setdefault(k, [])
    state = scope = vehicle = None
    decisions = []
    for c in _fields(form):
        h = str(c[0])
        if h == "state":
            state = _read_flat(_STATE_SPEC, c, "state")
            state.setdefault("csrs", [])
        elif h == "scope":
            scope = _read_flat(_SCOPE_SPEC(), c, "scope")
        elif h == "vehicle":
            vehicle = _read_flat(_VEHICLE_SPEC, c, "vehicle")
        elif h == "decision":
            decisions.append(_read_flat(_DECISION_SPEC, c, "decision"))
    return {"profile": prof, "state": state, "scope": scope, "vehicle": vehicle,
            "decision": decisions}


# --------------------------------------------------------------------------- state.json

def state_to_form(doc: dict) -> list:
    root = [S.Symbol("state"),
            _pair("profile_id", doc["profile_id"])]
    if "xlen" in doc:
        root.append(_pair("xlen", doc["xlen"]))
    root.append(_pair("note", doc["note"]))
    if "integer_registers" in doc:
        ir = doc["integer_registers"]
        reg = [S.Symbol("integer_registers"),
               _pair("count", ir["count"]),
               _pair("width_bits", ir["width_bits"]),
               _pair("ids", ir["ids"]),
               _pair("authority", _sym(ir["authority"])),
               _pair("source", ir["source"]),
               [S.Symbol("x0"),
                _bool_field("hardwired_zero", ir["x0"]["hardwired_zero"]),
                _pair("authority", _sym(ir["x0"]["authority"])),
                _pair("source", ir["x0"]["source"]),
                _pair("statement", ir["x0"]["statement"])]]
        for n in ir.get("named_by_the_isa_chapter", []):
            reg.append([S.Symbol("named_by_the_isa_chapter"),
                        [S.Symbol("named-register"),
                         _pair("reg", n["reg"]),
                         _pair("role", n["role"]),
                         _pair("authority", _sym(n["authority"])),
                         _pair("source", n["source"])]])
        if "reset" in ir:
            r = ir["reset"]
            reg.append([S.Symbol("reset"),
                        _pair("value", r["value"]),
                        _pair("authority", _sym(r["authority"])),
                        _pair("source", r["source"]),
                        _pair("statement", r["statement"])])
        root.append(reg)
    for fam in doc.get("register_family", []):
        ff = [S.Symbol("register_family"),
              _pair("id", fam["id"]),
              _pair("count", fam["count"]),
              _pair("width_bits", fam["width_bits"]),
              _pair("ids", fam["ids"]),
              _pair("authority", _sym(fam["authority"])),
              _pair("source", fam["source"])]
        for p in fam.get("parts", []):
            ff.append([S.Symbol("parts"),
                       [S.Symbol("part"),
                        _pair("id", p["id"]),
                        _pair("bit_hi", p["bit_hi"]),
                        _pair("bit_lo", p["bit_lo"]),
                        _pair("readout", p["readout"]),
                        _pair("authority", _sym(p["authority"])),
                        _pair("source", p["source"])]])
        if "reset" in fam:
            r = fam["reset"]
            ff.append([S.Symbol("reset"),
                       _pair("value", r["value"]),
                       _pair("authority", _sym(r["authority"])),
                       _pair("source", r["source"]),
                       _pair("statement", r["statement"])])
        root.append(ff)
    for s in doc.get("special_registers", []):
        root.append([S.Symbol("special_registers"),
                     [S.Symbol("register"),
                      _pair("id", s["id"]),
                      _pair("width_bits", s["width_bits"]),
                      _pair("holds", s["holds"]),
                      _pair("authority", _sym(s["authority"])),
                      _pair("source", s["source"]),
                      _pair("reset", s["reset"]),
                      _pair("reset_authority", _sym(s["reset_authority"]))]])
    if "privilege_mode" in doc:
        p = doc["privilege_mode"]
        pf = [S.Symbol("privilege_mode")]
        for m in p["modes"]:
            pf.append(_pair("modes", _sym(m)))
        pf += [_pair("authority", _sym(p["authority"])),
               _pair("source", p["source"]),
               [S.Symbol("reset"),
                _pair("value", p["reset"]["value"]),
                _pair("authority", _sym(p["reset"]["authority"])),
                _pair("source", p["reset"]["source"]),
                _pair("statement", p["reset"]["statement"])]]
        root.append(pf)
    for c in doc.get("csr", []):
        cf = [S.Symbol("csr"),
              _pair("id", c["id"]),
              _pair("address", c["address"]),
              _pair("width_bits", c["width_bits"])]
        if "view_of" in c:
            cf.append(_pair("view_of", c["view_of"]))
        cf += [_pair("authority", _sym(c["authority"])),
               _pair("source", c["source"])]
        for f in c.get("fields", []):
            ff = [S.Symbol("field"),
                  _pair("id", f["id"]),
                  _pair("bit_hi", f["bit_hi"]),
                  _pair("bit_lo", f["bit_lo"]),
                  _pair("discipline", _sym(f["discipline"]))]
            if "legalize" in f:
                lg = f["legalize"]
                if lg["kind"] == "any":
                    form = [S.Symbol("any")]
                elif lg["kind"] == "read-only":
                    form = [S.Symbol("read-only"), lg["value"]]
                elif lg["kind"] == "one-of":
                    form = [S.Symbol("one-of"), *lg["values"]]
                else:
                    form = [S.Symbol("computed")]
                ff.append([S.Symbol("legalize"), form])
            ff += [_pair("reset", f["reset"]),
                   _pair("reset_authority", _sym(f["reset_authority"])),
                   _pair("authority", _sym(f["authority"])),
                   _pair("source", f["source"])]
            cf.append(ff)
        r = c["reset"]
        cf.append([S.Symbol("reset"),
                   _pair("value", r["value"]),
                   _pair("authority", _sym(r["authority"])),
                   _pair("source", r["source"]),
                   _pair("statement", r["statement"])])
        root.append(cf)
    for sp in doc.get("memory_spaces", []):
        root.append([S.Symbol("memory_spaces"),
                     [S.Symbol("space"),
                      _pair("id", sp["id"]),
                      _pair("word_bits", sp["word_bits"]),
                      _pair("authority", _sym(sp["authority"])),
                      _pair("source", sp["source"])]])
    if "hardware_stack" in doc:
        h = doc["hardware_stack"]
        root.append([S.Symbol("hardware_stack"),
                     _pair("levels", h["levels"]),
                     _pair("width_bits", h["width_bits"]),
                     _pair("indexing", h["indexing"]),
                     _bool_field("stale_slots_observable", h["stale_slots_observable"]),
                     _pair("authority", _sym(h["authority"])),
                     _pair("source", h["source"])])
    if "hidden_state_census" in doc:
        c = doc["hidden_state_census"]
        census = [S.Symbol("hidden_state_census"),
                  _pair("question", c["question"]),
                  _pair("answer", c["answer"])]
        for cd in c.get("candidates_checked", []):
            census.append([S.Symbol("candidates"),
                           [S.Symbol("checked"),
                            _pair("candidate", cd["candidate"]),
                            _bool_field("present", cd["present"]),
                            _pair("why", cd["why"])]])
        census.append(_pair("consequence", c["consequence"]))
        root.append(census)
    return root


def state_to_doc(form) -> dict:
    S.head(form, "state")
    doc = {"profile_id": _s(_req(form, "profile_id", "state")),
           "note": _s(_req(form, "note", "state")),
           "special_registers": [
               {"id": _s(_req(r, "id", "register")),
                "width_bits": _req(r, "width_bits", "register"),
                "holds": _s(_req(r, "holds", "register")),
                "authority": _s(_req(r, "authority", "register")),
                "source": _s(_req(r, "source", "register")),
                "reset": _s(_req(r, "reset", "register")),
                "reset_authority": _s(_req(r, "reset_authority", "register"))}
               for r in (_child_in(c, "register") for c in _children_in(form, "special_registers"))],
           "hidden_state": []}
    xv = _opt(form, "xlen", "state")
    if xv is not None:
        doc["xlen"] = xv
    irf = _opt_child(form, "integer_registers")
    if irf is not None:
        ir = {"count": _req(irf, "count", "integer_registers"),
              "width_bits": _req(irf, "width_bits", "integer_registers"),
              "ids": _s(_req(irf, "ids", "integer_registers")),
              "authority": _s(_req(irf, "authority", "integer_registers")),
              "source": _s(_req(irf, "source", "integer_registers"))}
        x0f = _child_in(irf, "x0")
        ir["x0"] = {"hardwired_zero": _bool_in(x0f, "hardwired_zero", "x0"),
                    "authority": _s(_req(x0f, "authority", "x0")),
                    "source": _s(_req(x0f, "source", "x0")),
                    "statement": _s(_req(x0f, "statement", "x0"))}
        ir["named_by_the_isa_chapter"] = [
            {"reg": _s(_req(n, "reg", "named-register")),
             "role": _s(_req(n, "role", "named-register")),
             "authority": _s(_req(n, "authority", "named-register")),
             "source": _s(_req(n, "source", "named-register"))}
            for n in (_child_in(c, "named-register") for c in _children_in(irf, "named_by_the_isa_chapter"))]
        rf = _opt_child(irf, "reset")
        if rf is not None:
            ir["reset"] = {"value": _s(_req(rf, "value", "reset")),
                           "authority": _s(_req(rf, "authority", "reset")),
                           "source": _s(_req(rf, "source", "reset")),
                           "statement": _s(_req(rf, "statement", "reset"))}
        doc["integer_registers"] = ir
    # P3-BREADTH.5 slice 1: the mapping owner CARRIES the dsp56300-lab-v0 constructs —
    # a declared form must reach the generator as data, never be silently dropped here.
    fams = []
    for ff in _children_in(form, "register_family"):
        fam = {"id": _s(_req(ff, "id", "register_family")),
               "count": _req(ff, "count", "register_family"),
               "width_bits": _req(ff, "width_bits", "register_family"),
               "ids": _s(_req(ff, "ids", "register_family")),
               "authority": _s(_req(ff, "authority", "register_family")),
               "source": _s(_req(ff, "source", "register_family"))}
        parts = [{"id": _s(_req(p, "id", "part")),
                  "bit_hi": _req(p, "bit_hi", "part"),
                  "bit_lo": _req(p, "bit_lo", "part"),
                  "readout": _s(_req(p, "readout", "part")),
                  "authority": _s(_req(p, "authority", "part")),
                  "source": _s(_req(p, "source", "part"))}
                 for p in (_child_in(c, "part") for c in _children_in(ff, "parts"))]
        if parts:
            fam["parts"] = parts
        rf = _opt_child(ff, "reset")
        if rf is not None:
            fam["reset"] = {"value": _s(_req(rf, "value", "reset")),
                            "authority": _s(_req(rf, "authority", "reset")),
                            "source": _s(_req(rf, "source", "reset")),
                            "statement": _s(_req(rf, "statement", "reset"))}
        fams.append(fam)
    if fams:
        doc["register_family"] = fams
    spaces = [{"id": _s(_req(sp, "id", "space")),
               "word_bits": _req(sp, "word_bits", "space"),
               "authority": _s(_req(sp, "authority", "space")),
               "source": _s(_req(sp, "source", "space"))}
              for sp in (_child_in(c, "space") for c in _children_in(form, "memory_spaces"))]
    if spaces:
        doc["memory_spaces"] = spaces
    hf = _opt_child(form, "hardware_stack")
    if hf is not None:
        doc["hardware_stack"] = {
            "levels": _req(hf, "levels", "hardware_stack"),
            "width_bits": _req(hf, "width_bits", "hardware_stack"),
            "indexing": _s(_req(hf, "indexing", "hardware_stack")),
            "stale_slots_observable": _bool_in(hf, "stale_slots_observable", "hardware_stack"),
            "authority": _s(_req(hf, "authority", "hardware_stack")),
            "source": _s(_req(hf, "source", "hardware_stack"))}
    pf = _opt_child(form, "privilege_mode")
    if pf is not None:
        prf = _child_in(pf, "reset")
        doc["privilege_mode"] = {
            "modes": [_s(m) for m in _rep_in(pf, "modes")],
            "authority": _s(_req(pf, "authority", "privilege_mode")),
            "source": _s(_req(pf, "source", "privilege_mode")),
            "reset": _reset_doc(prf)}
    csrs = []
    for cf in _children_in(form, "csr"):
        c = {"id": _s(_req(cf, "id", "csr")),
             "address": _req(cf, "address", "csr"),
             "width_bits": _req(cf, "width_bits", "csr"),
             "authority": _s(_req(cf, "authority", "csr")),
             "source": _s(_req(cf, "source", "csr"))}
        vo = _opt(cf, "view_of", "csr")
        if vo is not None:
            c["view_of"] = _s(vo)
        fields = []
        for ff in _children_in(cf, "field"):
            f = {"id": _s(_req(ff, "id", "field")),
                 "bit_hi": _req(ff, "bit_hi", "field"),
                 "bit_lo": _req(ff, "bit_lo", "field"),
                 "discipline": _s(_req(ff, "discipline", "field")),
                 "reset": _s(_req(ff, "reset", "field")),
                 "reset_authority": _s(_req(ff, "reset_authority", "field")),
                 "authority": _s(_req(ff, "authority", "field")),
                 "source": _s(_req(ff, "source", "field"))}
            lg = _opt_child(ff, "legalize")
            if lg is not None:
                body = _value(lg, "legalize")
                head = str(body[0])
                if head == "any":
                    f["legalize"] = {"kind": "any"}
                elif head == "read-only":
                    f["legalize"] = {"kind": "read-only", "value": int(body[1])}
                elif head == "one-of":
                    f["legalize"] = {"kind": "one-of", "values": [int(v) for v in body[1:]]}
                elif head == "computed":
                    f["legalize"] = {"kind": "computed"}
                else:
                    raise DossierError(f"field: unknown legalize form ({head} …)")
            fields.append(f)
        if fields:
            c["fields"] = fields
        c["reset"] = _reset_doc(_child_in(cf, "reset"))
        csrs.append(c)
    if csrs:
        doc["csr"] = csrs
    cf = _opt_child(form, "hidden_state_census")
    if cf is not None:
        doc["hidden_state_census"] = {
            "question": _s(_req(cf, "question", "hidden_state_census")),
            "answer": _s(_req(cf, "answer", "hidden_state_census")),
            "candidates_checked": [
                {"candidate": _s(_req(c, "candidate", "checked")),
                 "present": _bool_in(c, "present", "checked"),
                 "why": _s(_req(c, "why", "checked"))}
                for c in (_child_in(e, "checked") for e in _children_in(cf, "candidates"))],
            "consequence": _s(_req(cf, "consequence", "hidden_state_census"))}
    return doc


# --------------------------------------------------------------------------- sources.toml

_SOURCE_SPEC = [("id", "str"), ("file", "str"), ("title", "str"), ("chapter_version", "str"),
                ("sha256", "str"), ("bytes", "int"), ("http_status", "int"), ("supplies", "str")]

_SOURCES_TOP = [("publication", "str"), ("not_this_publication", "str"), ("revision", "str"),
                ("base_url", "str"), ("retrieved", "str"), ("work_dir", "str")]


def sources_to_form(doc: dict) -> list:
    root = [S.Symbol("sources"), *_emit_flat(_SOURCES_TOP, doc)]
    for s in doc.get("source", []):
        root.append([S.Symbol("source"), *_emit_flat(_SOURCE_SPEC, s)])
    return root


def sources_to_doc(form) -> dict:
    S.head(form, "sources")
    d = _read_flat(_SOURCES_TOP, form, "sources", skip=("source",))
    d["source"] = [_read_flat(_SOURCE_SPEC, c, "source") for c in _children_in(form, "source")]
    return d


# --------------------------------------------------------------------------- references.toml

_CANDIDATE_SPEC = [(k, "str") for k in (
    "id", "role", "status", "kind", "origin", "release", "released", "asset", "asset_sha256",
    "binary", "binary_sha256", "build_info", "invocation", "trace_granularity", "injection",
    "matched_config", "matched_isa_string", "matched_isa_string_source", "matched_scope",
    "terms", "lineage", "version", "source_commit", "source_authored", "release_assets",
    "build_prefix", "build_note", "default_branch", "tag_shape", "status_reason", "license",
    "cross_volume", "redirect_note", "last_pushed")] + [("asset_bytes", "int"), ("http_status", "int"), ("tags_listed", "int")]

_ATTEMPT_SPEC = [("what", "str"), ("command", "str"), ("outcome", "str"), ("consequence", "str")]

_EXPERIMENT_SPEC = [("id", "str"), ("program", "str"), ("instructions", "int"),
                    ("models", "strs"), ("sail_invocation", "str"), ("spike_invocation", "str"),
                    ("elf_sha256", "str"), ("verdict", "str"), ("expectations", "str"),
                    ("reproduced", "str"), ("exercises", "str"), ("control", "str")]

_DIFFERENCE_SPEC = [("id", "str"), ("kind", "str"), ("observed", "str"), ("resolution", "str")]

_INDEPENDENCE_SPEC = [("subsystem", "str"), ("pair", "strs"), ("verdict", "str"),
                      ("evidence", "str"), ("consequence", "str")]

_ENCODING_SOURCE_SPEC = [("id", "str"), ("origin", "str"), ("license", "str"),
                         ("retrieved", "str"), ("work_dir", "str"), ("supplies", "str"),
                         ("note", "str")]

_ENC_FILE_SPEC = [("name", "str"), ("sha256", "str"), ("bytes", "int")]

_REFERENCES_TOP = [("profile", "str"), ("retrieved", "str"), ("work_dir", "str")]

_HOST_SPEC = [("os", "str"), ("kernel", "str"), ("arch", "str"), ("cxx", "str"), ("note", "str")]


def references_to_form(doc: dict) -> list:
    root = [S.Symbol("references"), *_emit_flat(_REFERENCES_TOP, doc)]
    if "host" in doc:
        root.append([S.Symbol("host"), *_emit_flat(_HOST_SPEC, doc["host"])])
    for key, head, spec in (("candidate", "candidate", _CANDIDATE_SPEC),
                            ("attempt", "attempt", _ATTEMPT_SPEC),
                            ("experiment", "experiment", _EXPERIMENT_SPEC),
                            ("difference", "difference", _DIFFERENCE_SPEC),
                            ("independence", "independence", _INDEPENDENCE_SPEC),
                            ("encoding_source", "encoding_source", _ENCODING_SOURCE_SPEC)):
        for rec in doc.get(key, []):
            form = [S.Symbol(head), *_emit_flat(spec, rec)]
            if key == "encoding_source":
                for f in rec.get("file", []):
                    form.append([S.Symbol("file"), *_emit_flat(_ENC_FILE_SPEC, f)])
            root.append(form)
    return root


def references_to_doc(form) -> dict:
    S.head(form, "references")
    d = _read_flat(_REFERENCES_TOP, form, "references",
                   skip=("host", "candidate", "attempt", "experiment", "difference",
                         "independence", "encoding_source"))
    host = _opt_child(form, "host")
    if host is not None:
        d["host"] = _read_flat(_HOST_SPEC, host, "host")
    for key, spec, extra in (("candidate", _CANDIDATE_SPEC, None),
                             ("attempt", _ATTEMPT_SPEC, None),
                             ("experiment", _EXPERIMENT_SPEC, None),
                             ("difference", _DIFFERENCE_SPEC, None),
                             ("independence", _INDEPENDENCE_SPEC, None),
                             ("encoding_source", _ENCODING_SOURCE_SPEC, "file")):
        recs = []
        for c in _children_in(form, key):
            rec = _read_flat(spec, c, key, skip=(extra,) if extra else ())
            if extra:
                rec[extra] = [_read_flat(_ENC_FILE_SPEC, f, extra)
                              for f in _children_in(c, extra)]
            recs.append(rec)
        if recs:
            d[key] = recs
    return d


# --------------------------------------------------------------------------- the Sail override

def _some_none_to_form(value) -> list:
    if set(value) == {"Some"}:
        return [S.Symbol("some"), _pair("value", value["Some"])]
    if set(value) == {"None"}:
        return [S.Symbol("none")]
    raise DossierError(f"not an option shape: {value!r}")


def _some_none_to_doc(form) -> dict:
    h = S.head(form, "option")
    if h == "some":
        return {"Some": _s(_req(form, "value", "some"))}
    if h == "none":
        return {"None": None}
    raise DossierError(f"expected (some …)/(none), got {form!r}")


def _supported_flag(value: bool) -> list:
    return _bool_field("supported", value)


def _extension_to_form(name: str, e: dict) -> list:
    ef = [S.Symbol("extension"), _pair("name", name)]
    if "supported" in e:
        ef.append(_supported_flag(e["supported"]))
    for k in ("support_level", "vlen_exp", "elen_exp", "max_index_eew_exp"):
        if k in e:
            ef.append(_pair(k, _atom_out(e[k])))
    for k, v in e.items():
        if isinstance(v, dict):                    # a nested group (Stateen.Smstateen)
            ef.append(_extension_to_form(k, v))
    return ef


def override_to_form(doc: dict) -> list:
    mstatus = doc["base"]["mstatus"]
    base = [S.Symbol("base"),
            [S.Symbol("mstatus"),
             _pair("fs_legal_states", mstatus["fs_legal_states"]),
             _pair("vs_legal_states", mstatus["vs_legal_states"])]]
    # P4-SYSTEM.2 slice h: the rv64gc override's extra base keys — emitted only when the
    # document carries them (the rv64i override predates them; absence round-trips).
    for k in ("privileged_isa_version", "writable_misa", "medeleg", "mideleg"):
        if k in doc["base"]:
            if k in ("medeleg", "mideleg"):
                bits = doc["base"][k]["delegatable_bits"]
                base.append([S.Symbol(k),
                             [S.Symbol("delegatable_bits"),
                              [S.Symbol("int64"), _pair("len", bits["len"]),
                               _pair("value", bits["value"])]]])
            elif k == "writable_misa":
                base.append(_bool_field(k, doc["base"][k]))
            else:
                base.append(_pair(k, _atom_out(doc["base"][k])))
    plat = doc["platform"]
    machine = plat["interrupts"]["machine"]
    platform = [S.Symbol("platform"),
                [S.Symbol("clint"), _supported_flag(plat["clint"]["supported"])],
                [S.Symbol("simple_interrupt_generator"),
                 _supported_flag(plat["simple_interrupt_generator"]["supported"])],
                [S.Symbol("interrupts"),
                 [S.Symbol("machine"),
                  [S.Symbol("software"), _supported_flag(machine["software"]["supported"])],
                  [S.Symbol("external"), _supported_flag(machine["external"]["supported"])],
                  [S.Symbol("timer"), _supported_flag(machine["timer"]["supported"])]]]]
    for k in ("wfi_is_nop", "wfi_available_to_user_mode"):
        if k in plat:
            platform.append(_bool_field(k, plat[k]))
    mem = doc["memory"]
    region_forms = []
    for r in mem["regions"]:
        a = r["attributes"]
        me = a["misaligned_exceptions"]
        region_forms.append(
            [S.Symbol("region"),
             [S.Symbol("base"),
              [S.Symbol("int64"), _pair("len", r["base"]["len"]), _pair("value", r["base"]["value"])]],
             [S.Symbol("size"),
              [S.Symbol("int64"), _pair("len", r["size"]["len"]), _pair("value", r["size"]["value"])]],
             [S.Symbol("attributes"),
              _pair("mem_type", a["mem_type"]),
              _bool_field("cacheable", a["cacheable"]),
              _bool_field("coherent", a["coherent"]),
              _bool_field("executable", a["executable"]),
              _bool_field("readable", a["readable"]),
              _bool_field("writable", a["writable"]),
              _bool_field("read_idempotent", a["read_idempotent"]),
              _bool_field("write_idempotent", a["write_idempotent"]),
              [S.Symbol("misaligned_exceptions"),
               [S.Symbol("load_store"), _some_none_to_form(me["load_store"])],
               [S.Symbol("vector"), _some_none_to_form(me["vector"])],
               _pair("amo", me["amo"]),
               _pair("lrsc", me["lrsc"])],
              _pair("atomic_support", a["atomic_support"]),
              _pair("misaligned_atomicity_granule_size_exp", a["misaligned_atomicity_granule_size_exp"]),
              _pair("vector_misaligned_atomicity_granule_size_exp",
                   a["vector_misaligned_atomicity_granule_size_exp"]),
              _pair("reservability", a["reservability"]),
              _bool_field("supports_cbo_zero", a["supports_cbo_zero"]),
              _bool_field("supports_pte_read", a["supports_pte_read"]),
              _bool_field("supports_pte_write", a["supports_pte_write"])],
             _bool_field("include_in_device_tree", r["include_in_device_tree"])])
    memory = [S.Symbol("memory"),
              [S.Symbol("misaligned"),
               [S.Symbol("exceptions"),
                [S.Symbol("load_store"),
                 _some_none_to_form(mem["misaligned"]["exceptions"]["load_store"])]]],
              [S.Symbol("regions"), *region_forms]]
    if "pmp" in mem:
        p = mem["pmp"]
        memory.append([S.Symbol("pmp"),
                       _pair("grain", p["grain"]), _pair("count", p["count"]),
                       _pair("usable_count", p["usable_count"]),
                       _bool_field("tor_supported", p["tor_supported"]),
                       _bool_field("na4_supported", p["na4_supported"]),
                       _bool_field("napot_supported", p["napot_supported"])])
    extensions = [S.Symbol("extensions")]
    for name in doc["extensions"]:
        extensions.append(_extension_to_form(name, doc["extensions"][name]))
    return [S.Symbol("override"), base, platform, memory, extensions]


def override_to_doc(form) -> dict:
    S.head(form, "override")
    bf = _child_in(form, "base")
    mstatus = _child_in(bf, "mstatus")
    pf = _child_in(form, "platform")
    machine = _child_in(_child_in(pf, "interrupts"), "machine")
    mf = _child_in(form, "memory")
    regions = []
    for rf in _children_in(_child_in(mf, "regions"), "region"):
        af = _child_in(rf, "attributes")
        mef = _child_in(af, "misaligned_exceptions")
        base = _int64_in(rf, "base")
        size = _int64_in(rf, "size")
        regions.append({
            "base": {"len": _req(base, "len", "base"), "value": _s(_req(base, "value", "base"))},
            "size": {"len": _req(size, "len", "size"), "value": _s(_req(size, "value", "size"))},
            "attributes": {
                "mem_type": _s(_req(af, "mem_type", "attributes")),
                "cacheable": _bool_in(af, "cacheable", "attributes"),
                "coherent": _bool_in(af, "coherent", "attributes"),
                "executable": _bool_in(af, "executable", "attributes"),
                "readable": _bool_in(af, "readable", "attributes"),
                "writable": _bool_in(af, "writable", "attributes"),
                "read_idempotent": _bool_in(af, "read_idempotent", "attributes"),
                "write_idempotent": _bool_in(af, "write_idempotent", "attributes"),
                "misaligned_exceptions": {
                    "load_store": _some_none_to_doc(_nested_in(mef, "load_store", "misaligned_exceptions")),
                    "vector": _some_none_to_doc(_nested_in(mef, "vector", "misaligned_exceptions")),
                    "amo": _s(_req(mef, "amo", "misaligned_exceptions")),
                    "lrsc": _s(_req(mef, "lrsc", "misaligned_exceptions"))},
                "atomic_support": _s(_req(af, "atomic_support", "attributes")),
                "misaligned_atomicity_granule_size_exp":
                    _req(af, "misaligned_atomicity_granule_size_exp", "attributes"),
                "vector_misaligned_atomicity_granule_size_exp":
                    _req(af, "vector_misaligned_atomicity_granule_size_exp", "attributes"),
                "reservability": _s(_req(af, "reservability", "attributes")),
                "supports_cbo_zero": _bool_in(af, "supports_cbo_zero", "attributes"),
                "supports_pte_read": _bool_in(af, "supports_pte_read", "attributes"),
                "supports_pte_write": _bool_in(af, "supports_pte_write", "attributes")},
            "include_in_device_tree": _bool_in(rf, "include_in_device_tree", "region")})
    def _extension_to_doc(ef):
        e = {}
        sup = _opt_child(ef, "supported")
        if sup is not None:
            e["supported"] = _value(sup, "extension") == "true"
        for k in ("support_level", "vlen_exp", "elen_exp", "max_index_eew_exp"):
            v = _opt(ef, k, "extension")
            if v is not None:
                e[k] = v
        for sub in _children_in(ef, "extension"):
            e[_s(_req(sub, "name", "extension"))] = _extension_to_doc(sub)
        return e

    extensions = {}
    exf = _child_in(form, "extensions")
    for ef in _children_in(exf, "extension"):
        extensions[_s(_req(ef, "name", "extension"))] = _extension_to_doc(ef)
    exceptions = _child_in(_child_in(mf, "misaligned"), "exceptions")
    memory = {"misaligned": {"exceptions": {"load_store": _some_none_to_doc(
                  _nested_in(exceptions, "load_store", "exceptions"))}},
              "regions": regions}
    pmp_f = _opt_child(mf, "pmp")
    if pmp_f is not None:
        memory["pmp"] = {"grain": _req(pmp_f, "grain", "pmp"),
                         "count": _req(pmp_f, "count", "pmp"),
                         "usable_count": _req(pmp_f, "usable_count", "pmp"),
                         "tor_supported": _bool_in(pmp_f, "tor_supported", "pmp"),
                         "na4_supported": _bool_in(pmp_f, "na4_supported", "pmp"),
                         "napot_supported": _bool_in(pmp_f, "napot_supported", "pmp")}
    platform = {"clint": {"supported": _flag_in(pf, "clint", "platform")},
                "simple_interrupt_generator":
                    {"supported": _flag_in(pf, "simple_interrupt_generator",
                                          "platform")},
                "interrupts": {"machine": {
                    "software": {"supported": _flag_in(machine, "software",
                                                      "interrupts")},
                    "external": {"supported": _flag_in(machine, "external",
                                                      "interrupts")},
                    "timer": {"supported": _flag_in(machine, "timer", "interrupts")}}}}
    for k in ("wfi_is_nop", "wfi_available_to_user_mode"):
        if _opt(pf, k, "platform") is not None:
            platform[k] = _opt(pf, k, "platform") == "true"
    base = {"mstatus": {"fs_legal_states": _s(_req(mstatus, "fs_legal_states",
                                                   "mstatus")),
                        "vs_legal_states": _s(_req(mstatus, "vs_legal_states",
                                                   "mstatus"))}}
    for k in ("privileged_isa_version", "writable_misa", "medeleg", "mideleg"):
        if k in ("medeleg", "mideleg"):
            kf = _opt_child(bf, k)
            if kf is not None:
                bits = _int64_in(kf, "delegatable_bits")
                base[k] = {"delegatable_bits": {"len": _req(bits, "len", "delegatable_bits"),
                                                "value": _s(_req(bits, "value",
                                                                 "delegatable_bits"))}}
        elif _opt(bf, k, "base") is not None:
            v = _opt(bf, k, "base")
            base[k] = (v == "true") if k == "writable_misa" else v
    return {"base": base, "platform": platform, "memory": memory,
            "extensions": extensions}


# --------------------------------------------------------------------------- guest expectations

def expectations_to_form(doc: dict) -> list:
    root = [S.Symbol("expectations"),
            _pair("program", doc["program"])]
    # P5-BOARD.2 (case sifive-uart-lab-v0): entry/instructions are optional — a device
    # register-read-expectation has no program entry or instruction count; both emit
    # only when the document carries them. P4-SYSTEM.3: `fetches` likewise (the
    # no-extraneous-fetch witness for a guest whose fetch can page-fault).
    for k in ("entry", "instructions", "fetches"):
        if k in doc:
            root.append(_pair(k, doc[k]))
    root += _rep("never_written", doc.get("never_written") or [])
    if "cross_model" in doc:
        root.append(_bool_field("cross_model", doc["cross_model"]))
    if "expect_divergence" in doc:
        ed = doc["expect_divergence"]
        root.append([S.Symbol("expect_divergence"),
                     _pair("difference", ed["difference"]),
                     _pair("at_step", ed["at_step"])])
    for s in doc.get("step", []):
        sf = [S.Symbol("step"),
              _pair("n", s["n"]),
              _pair("insn", s["insn"]),
              [S.Symbol("writes"),
               *[[S.Symbol("write"), _pair("reg", reg), _pair("value", val)]
                 for reg, val in (s.get("writes") or {}).items()]],
              _pair("derivation", s["derivation"]),
              _pair("source", s["source"])]
        if "limit" in s:
            sf.append(_pair("limit", s["limit"]))
        root.append(sf)
    return root


def expectations_to_doc(form) -> dict:
    S.head(form, "expectations")
    doc = {"program": _s(_req(form, "program", "expectations")),
           "cross_model": _opt_bool_in(form, "cross_model", "expectations"),
           "step": []}
    # P5-BOARD.2 (case sifive-uart-lab-v0): entry/instructions reconstruct only when the
    # document declares them — an absent program shape is not a zero one
    entry = _opt(form, "entry", "expectations")
    if entry is not None:
        doc["entry"] = _s(entry)
    instructions = _opt(form, "instructions", "expectations")
    if instructions is not None:
        doc["instructions"] = instructions
    fetches = _opt(form, "fetches", "expectations")
    if fetches is not None:
        doc["fetches"] = fetches
    edf = _opt_child(form, "expect_divergence")
    if edf is not None:
        doc["expect_divergence"] = {
            "difference": _s(_req(edf, "difference", "expect_divergence")),
            "at_step": _req(edf, "at_step", "expect_divergence")}
    # never_written reconstructs only when the document declares it — an absent negative
    # observation is not the same as an empty one
    if any(str(c[0]) == "never_written" for c in _fields(form)):
        doc["never_written"] = [_s(v) for v in _rep_in(form, "never_written")]
    for sf in _children_in(form, "step"):
        writes = {}
        wf = _child_in(sf, "writes")
        for w in _children_in(wf, "write"):
            writes[_s(_req(w, "reg", "write"))] = _s(_req(w, "value", "write"))
        step = {"n": _req(sf, "n", "step"),
                "insn": _s(_req(sf, "insn", "step")),
                "writes": writes,
                "derivation": _s(_req(sf, "derivation", "step")),
                "source": _s(_req(sf, "source", "step"))}
        limit = _opt(sf, "limit", "step")
        if limit is not None:
            step["limit"] = _s(limit)
        doc["step"].append(step)
    if doc["cross_model"] is None:
        del doc["cross_model"]
    return doc


# --------------------------------------------------------------------------- files

FAMILIES = ("profile", "state", "sources", "references", "override", "expectations")

_TO_FORM = {"profile": profile_to_form, "state": state_to_form, "sources": sources_to_form,
            "references": references_to_form, "override": override_to_form,
            "expectations": expectations_to_form}
_TO_DOC = {"profile": profile_to_doc, "state": state_to_doc, "sources": sources_to_doc,
           "references": references_to_doc, "override": override_to_doc,
           "expectations": expectations_to_doc}
_SCHEMA_FOR = {"profile": "schema/profile.sexp", "state": "schema/state.sexp",
               "sources": "schema/sources.sexp", "references": "schema/references.sexp",
               "override": "schema/override.sexp", "expectations": "schema/expectations.sexp"}


def family_for(path: Path) -> str:
    n = path.name
    if n == "profile.toml" or n == "profile.sexp":
        return "profile"
    if n == "state.json" or n == "state.sexp":
        return "state"
    if n == "sources.toml" or n == "sources.sexp":
        return "sources"
    if n == "references.toml" or n == "references.sexp":
        return "references"
    if n.endswith(".override.json") or n.endswith(".override.sexp"):
        return "override"
    if n.endswith(".expected.toml") or n.endswith(".expected.sexp"):
        return "expectations"
    raise DossierError(f"{n}: not a dossier document I know ({', '.join(FAMILIES)})")


def _root_form(path: Path):
    forms = [f for f in S.read_file(path) if not _is_note(f)]
    if len(forms) != 1:
        raise DossierError(f"{path.name}: expected exactly one document form (annotations "
                           f"aside), found {len(forms)}")
    return forms[0]


def load(path: Path) -> dict:
    """A converted dossier document as the dict tomllib/json produced for it."""
    path = Path(path)
    fam = family_for(path)
    try:
        return _TO_DOC[fam](_root_form(path))
    except S.SexpError as exc:
        raise DossierError(f"{path.name}: does not parse — {exc}") from exc


def load_profile(path: Path) -> dict:
    return load(path)


def load_state(path: Path) -> dict:
    return load(path)


def load_sources(path: Path) -> dict:
    return load(path)


def load_references(path: Path) -> dict:
    return load(path)


def load_override(path: Path) -> dict:
    return load(path)


def load_expectations(path: Path) -> dict:
    return load(path)


def read_source_document(path: Path) -> dict:
    """The tracked TOML/JSON source document, parsed (the converter's input side)."""
    path = Path(path)
    try:
        if path.suffix == ".toml":
            return tomllib.loads(path.read_text())
        if path.suffix == ".json":
            return json.loads(path.read_text())
    except (tomllib.TOMLDecodeError, json.JSONDecodeError) as exc:
        raise DossierError(f"{path.name}: {exc}") from exc
    raise DossierError(f"{path.name}: not a .toml/.json source document")


def materialize_sail_override(repo: Path, profile: str = "rv64i-lab-v0") -> Path:
    """Derive the matched-profile JSON the Sail model reads from the tracked override.sexp.

    The `.sexp` is the source of truth; the JSON is a foreign-tool input, materialized
    untracked under target/refs/ (repo volume) — the same pattern as the fetched artifacts.
    """
    doc = load(repo / "profiles" / profile / "reference" / f"sail-{profile}.override.sexp")
    out = repo / "target" / "refs" / f"sail-{profile}.override.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=2) + "\n")
    return out


# --------------------------------------------------------------------------- self-test

def _selftest() -> int:
    import copy
    passed = failed = 0

    def arm(label: str, fn) -> None:
        nonlocal passed, failed
        try:
            fn()
        except AssertionError as exc:
            print(f"  FAIL  {label}: {exc}"); failed += 1
        except Exception as exc:                        # noqa: BLE001
            print(f"  FAIL  {label}: unexpected {type(exc).__name__}: {exc}"); failed += 1
        else:
            print(f"  ok    {label}"); passed += 1

    def eq(x, y):
        assert x == y, f"got {x!r}, want {y!r}"

    def refused(fn, needle: str) -> None:
        try:
            fn()
        except DossierError as exc:
            assert needle in str(exc), f"refused, but for the wrong reason: {exc}"
        else:
            raise AssertionError(f"accepted; it must be refused ({needle})")

    # `vehicle` reconstructs as None when the document does not declare it (the mapping's
    # shape since P3-BREADTH.7 slice 1) — the fixture carries the key so the round-trip
    # compares equal.
    PROF = {"profile": {"id": "p1", "xlen": 64, "extensions": [], "privilege_modes": [],
                     "sources": ["S-A"]},
            "state": {"integer_registers": 32, "x0_hardwired_zero": True, "csrs": [],
                      "authority": "laboratory", "source": "§1"},
            "scope": {"count_base": 2, "count_rv64i_additions": 1, "count_total": 3,
                      "authority": "architecture", "source": "§1", "base_op": ["ADD"]},
            "vehicle": None,
            "decision": [{"id": "D-1", "authority": "architecture", "statement": "s",
                          "source": "§1"}]}
    EXP = {"program": "g.s", "entry": "0x80000000", "instructions": 1,
           "never_written": ["x1"], "cross_model": False,
           "step": [{"n": 0, "insn": "addi x1, x0, 1", "writes": {"x1": "0x0000000000000001"},
                     "derivation": "d", "source": "§1"}]}
    OVR = {"base": {"mstatus": {"fs_legal_states": "ExtContext_Off",
                                "vs_legal_states": "ExtContext_Off"}},
           "platform": {"clint": {"supported": False},
                        "simple_interrupt_generator": {"supported": False},
                        "interrupts": {"machine": {"software": {"supported": False},
                                                   "external": {"supported": False},
                                                   "timer": {"supported": False}}}},
           "memory": {"misaligned": {"exceptions": {"load_store": {"Some": "AlignmentException"}}},
                      "regions": [{"base": {"len": 64, "value": "0x80000000"},
                                   "size": {"len": 64, "value": "0x80000000"},
                                   "attributes": {
                                       "mem_type": "MainMemory", "cacheable": True,
                                       "coherent": True, "executable": True, "readable": True,
                                       "writable": True, "read_idempotent": True,
                                       "write_idempotent": True,
                                       "misaligned_exceptions": {"load_store": {"None": None},
                                                                 "vector": {"None": None},
                                                                 "amo": "AccessFault",
                                                                 "lrsc": "AccessFault"},
                                       "atomic_support": "AMOCASQ",
                                       "misaligned_atomicity_granule_size_exp": 4,
                                       "vector_misaligned_atomicity_granule_size_exp": 4,
                                       "reservability": "RsrvEventual",
                                       "supports_cbo_zero": True, "supports_pte_read": True,
                                       "supports_pte_write": True},
                                   "include_in_device_tree": True}]},
           "extensions": {"A": {"supported": False}, "Zicsr": {"supported": False},
                          "V": {"support_level": "Disabled", "vlen_exp": 5, "elen_exp": 5,
                                "max_index_eew_exp": 5}}}

    arm("GREEN a profile document round-trips, empty lists as absence and back",
        lambda: eq(profile_to_doc(profile_to_form(PROF)), PROF))
    arm("GREEN a profile keeps a decision's note and a scope's empty lists",
        lambda: eq(profile_to_doc(profile_to_form({**PROF, "decision": [
            {"id": "D-1", "authority": "architecture", "statement": "s", "source": "§1",
             "note": "n"}]}))["decision"][0]["note"], "n"))
    arm("GREEN guest expectations round-trip, dynamic write keys as entry forms",
        lambda: eq(expectations_to_doc(expectations_to_form(EXP)), EXP))
    arm("GREEN a device register-read-expectation (no entry/instructions) round-trips "
        "(P5-BOARD.2, case sifive-uart-lab-v0)",
        lambda: eq(expectations_to_doc(expectations_to_form(
            {k: v for k, v in EXP.items() if k not in ("entry", "instructions")})),
            {k: v for k, v in EXP.items() if k not in ("entry", "instructions")}))
    arm("GREEN a device scope's mmio_registers census round-trips (P5-BOARD.2)",
        lambda: eq(profile_to_doc(profile_to_form(
            {**PROF, "scope": {**PROF["scope"],
                               "mmio_registers": ["UART_RXDATA", "UART_TXDATA"]}}))["scope"]
            ["mmio_registers"], ["UART_RXDATA", "UART_TXDATA"]))
    arm("GREEN the override round-trips — options, regions, dynamic extensions",
        lambda: eq(override_to_doc(override_to_form(OVR)), OVR))
    arm("GREEN an empty writes table becomes a marker form and returns as {}",
        lambda: eq(expectations_to_doc(expectations_to_form(
            {**EXP, "step": [{**EXP["step"][0], "writes": {}}]}))["step"][0]["writes"], {}))
    arm("GREEN a document with annotations maps as if they were not there",
        lambda: eq(expectations_to_doc(
            [S.Symbol("expectations"), _pair("program", "g.s"), _pair("entry", "0x1"),
             _pair("instructions", 1),
             [S.Symbol("step"), _pair("n", 0), _pair("insn", "i"),
              [S.Symbol("writes")], _pair("derivation", "d"), _pair("source", "s"),
              [S.Symbol("comment"), "why"]]]),
            {"program": "g.s", "entry": "0x1", "instructions": 1,
             "step": [{"n": 0, "insn": "i", "writes": {}, "derivation": "d",
                       "source": "s"}]}))
    arm("GREEN authority travels as a symbol and returns as the same string",
        lambda: eq(profile_to_doc(profile_to_form(PROF))["state"]["authority"],
                   "laboratory"))
    arm("GREEN an expected-divergence declaration round-trips (P2-SCALAR.4)",
        lambda: eq(expectations_to_doc(expectations_to_form(
            {**EXP, "expect_divergence": {"difference": "DIFF-X", "at_step": 1}})),
            {**EXP, "expect_divergence": {"difference": "DIFF-X", "at_step": 1}}))
    arm("RED   a float is refused, not truncated",
        lambda: refused(lambda: _pair("x", _atom_out(1.5)), "float"))
    arm("RED   a nested value where a scalar belongs is refused",
        lambda: refused(lambda: _atom_out({"y": 1}), "no S-expression value"))
    arm("RED   an undeclared field in a flat record is refused by name",
        lambda: refused(lambda: profile_to_doc([
            S.Symbol("profile"), _pair("id", "p1"), _pair("widht", 64)]), "widht"))
    arm("RED   a bool field holding a bare symbol is refused",
        lambda: refused(lambda: _truthy(S.Symbol("maybe"), "arm"), "expected true/false"))

    print(f"dossier_sexp --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_selftest())
