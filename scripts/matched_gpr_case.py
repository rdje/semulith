"""A matched GPR case's declaration, read from data (P4-SYSTEM.14 a44-1; decision_case-declarations-as-data.md).

Each reviewed case is one file, `evidence/<case>/case.sexp`, validated against `schema/matched-case.sexp`:
its guest program, its predeclared properties and their RV64 values, its control, its hand-reviewed steps,
its authority and its pinned prepared inputs. This module reads that file into neutral data — a dictionary
of the schema's fields, tuples for the repeated forms — and the review owns the mapping onto its records
(`matched_gpr_property.reviewed_case`), so no record type is built here. A case without a file is refused by
name, and so is a file that does not validate or whose id disagrees with its directory. `render` writes the
canonical text, so a declaration and its rendering are one byte sequence.
"""

from __future__ import annotations

from pathlib import Path

import check_sexp_schema as Schema
import records_sexp as Records
import sexp as S

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = "schema/matched-case.sexp"
FILE = "case.sexp"
PREPARED_ROLES = ("guest-image", "reference-config", "expectation")
SCALARS = ("id", "profile_id", "program", "instructions", "source_size", "source_sha256", "requirement_id",
           "contract_id", "contract_version", "limitation", "source_id", "source_locator", "category", "risk",
           "coverage")


class CaseError(ValueError):
    """A declared case cannot be read as declared."""


def case_path(case_id: str) -> str:
    return "evidence/" + case_id + "/" + FILE


def declared_case_ids(root: Path | None = None) -> tuple[str, ...]:
    """Every case directory holding a declaration, in name order."""
    root = ROOT if root is None else root
    return tuple(sorted(path.parent.name for path in (root / "evidence").glob("*/" + FILE)))


def read_document(text: str, where: str) -> dict:
    """Validate and parse one declaration's text into neutral data.

    The result maps each scalar field to its value; `obligation_ids` is a tuple; `control` and `authority`
    are dictionaries — the control's `id` and `statement` are `None` in a declaration retained before
    P4-SYSTEM.14 a43b-2b; `second_method` and `adversarial` are dictionaries (their repeated fields tuples) or
    `None` when undeclared; `required_inputs` holds (role, id, path, sha256) rows, `prepared` (role, id, name,
    byte_size, sha256) rows, `properties` (id, cell, step_n, register, expected, statement) rows and
    `steps` (n, pc, word, length, fetches, ((register, value), ...)) rows, each in declaration order.
    """
    constructs, operators = Schema.load_schema(ROOT / SCHEMA)
    errors = Schema.validate_text(text, constructs, operators, where)
    if errors:
        raise CaseError(where + ": " + "; ".join(errors))
    forms = [form for form in S.parse(text, where) if isinstance(form, list) and form and str(form[0]) == "case"]
    if len(forms) != 1:
        raise CaseError(where + ": one case form expected")
    top = forms[0]

    def sub(form):
        return {str(child[0]): child[1] for child in form[1:] if len(child) == 2}

    def many(name):
        return [child for child in top[1:] if str(child[0]) == name]

    def single(name):
        found = many(name)
        if len(found) != 1:
            raise CaseError(f"{where}: field {name} occurs {len(found)} times")
        return found[0][1]

    declaration = {name: single(name) for name in SCALARS}
    declaration["obligation_ids"] = tuple(child[1] for child in many("obligation_ids"))
    declaration["control"] = {"id": None, "statement": None, **sub(single_form(top, "control", where))}
    declaration["second_method"] = optional_form(top, "second_method", ("producer_ids", "common_input_ids"), where)
    declaration["adversarial"] = optional_form(top, "adversarial", ("property_ids",), where)
    declaration["authority"] = sub(single_form(top, "authority", where))
    declaration["required_inputs"] = tuple((item["role"], item["id"], item["path"], item["sha256"])
                                           for item in (sub(form) for form in many("required_input")))
    declaration["prepared"] = tuple((item["role"], item["id"], item["name"], item["byte_size"], item["sha256"])
                                    for item in (sub(form) for form in many("prepared")))
    declaration["properties"] = tuple(
        (item["id"], item["cell"], item["step_n"], item["register"], item["expected"], item["statement"])
        for item in (sub(form) for form in many("property")))
    steps = []
    for form in many("step"):
        item = sub(form)
        writes = tuple((sub(write)["register"], sub(write)["value"])
                       for write in form[1:] if str(write[0]) == "write")
        steps.append((item["n"], item["pc"], item.get("word"), item.get("length"), item["fetches"], writes))
    declaration["steps"] = tuple(steps)
    for n, _pc, word, length, fetches, writes in steps:
        # A boundary with no word is an event, and writes nothing: a delivered interrupt reads no parcel, and a fetch fault reads
        # none or one, the parcel before the one that faulted (P4-SYSTEM.14 a43e-1, a49-1).
        if (word is None) != (length is None) or (word is None and (writes or fetches not in (0, 1))):
            raise CaseError(f"{where}: step {n} must fetch a word of a length, or be an event boundary that reads at most one parcel and writes nothing")
    if declaration["control"]["property_id"] not in {row[0] for row in declaration["properties"]}:
        raise CaseError(where + ": the control names no declared property")
    adversarial = declaration["adversarial"]
    if adversarial and not set(adversarial["property_ids"]) <= {row[0] for row in declaration["properties"]}:
        raise CaseError(where + ": the adversarial case names a property the case does not declare")
    if sorted(row[0] for row in declaration["prepared"]) != sorted(PREPARED_ROLES + ("expectation",)):
        raise CaseError(where + ": the prepared inputs are not one image, one configuration and two expectations")
    return declaration


def single_form(top, name, where):
    found = [child for child in top[1:] if str(child[0]) == name]
    if len(found) != 1:
        raise CaseError(f"{where}: field {name} occurs {len(found)} times")
    return found[0]


def optional_form(top, name, repeated, where):
    """An optional nested form as a dictionary — its `repeated` fields as tuples in order — or `None`."""
    found = [child for child in top[1:] if str(child[0]) == name]
    if not found:
        return None
    if len(found) != 1:
        raise CaseError(f"{where}: field {name} occurs {len(found)} times")
    form = found[0]
    data = {key: tuple(child[1] for child in form[1:] if str(child[0]) == key) for key in repeated}
    data.update({str(child[0]): child[1] for child in form[1:] if str(child[0]) not in repeated})
    return data


def read_case(case_id: str, root: Path | None = None) -> dict:
    """The declared case as neutral data; a case without a declaration is refused by name."""
    root = ROOT if root is None else root
    path = root / case_path(case_id)
    if not path.is_file():
        raise CaseError("no declaration for case " + case_id + ": " + case_path(case_id) + " is absent")
    declaration = read_document(path.read_text(), case_path(case_id))
    if declaration["id"] != case_id:
        raise CaseError(case_path(case_id) + ": declares " + declaration["id"] + ", not its directory's " + case_id)
    return declaration


def _value(number: int) -> str:
    return "0x%x" % number if number >= 4096 else str(number)


def render(declaration: dict) -> str:
    """The canonical declaration text of a case: one field per line, values in hex above 4095."""
    q = Records.quote_string
    d = declaration
    a, control = d["authority"], d["control"]
    lines = [
        ";; " + case_path(d["id"]) + " — the reviewed declaration of matched case " + d["id"]
        + " (schema/matched-case.sexp).",
        ";; Data, not code (decision_case-declarations-as-data.md): read by scripts/matched_gpr_case.py.",
        "(case (id " + q(d["id"]) + ") (profile_id " + q(d["profile_id"]) + ")",
        "  (program " + q(d["program"]) + ") (instructions " + str(d["instructions"]) + ") (source_size "
        + str(d["source_size"]) + ")",
        "  (source_sha256 " + q(d["source_sha256"]) + ")",
        "  (requirement_id " + q(d["requirement_id"]) + ")"
        + "".join(" (obligation_ids " + q(item) + ")" for item in d["obligation_ids"]),
        "  (contract_id " + q(d["contract_id"]) + ") (contract_version " + q(d["contract_version"]) + ")",
        "  (control (property_id " + q(control["property_id"]) + ") (value " + _value(control["value"])
        + ") (reason " + q(control["reason"]) + ")" + ("" if control.get("id") is None else " (id " + q(control["id"]) + ")")
        + ("" if control.get("statement") is None else "\n    (statement " + q(control["statement"]) + ")") + ")",
        "  (limitation " + q(d["limitation"]) + ")",
        "  (source_id " + q(d["source_id"]) + ") (source_locator " + q(d["source_locator"]) + ") (category "
        + q(d["category"]) + ") (risk " + q(d["risk"]) + ")",
        "  (coverage " + q(d["coverage"]) + ")",
    ]
    method, adversarial = d.get("second_method"), d.get("adversarial")
    if method is not None:
        lines.append("  (second_method (kind " + q(method["kind"]) + ")"
                     + "".join(" (producer_ids " + q(item) + ")" for item in method["producer_ids"])
                     + "".join(" (common_input_ids " + q(item) + ")" for item in method["common_input_ids"]))
        lines.append("    (independently_derived " + q(method["independently_derived"]) + "))")
    if adversarial is not None:
        lines.append("  (adversarial" + "".join(" (property_ids " + q(item) + ")" for item in adversarial["property_ids"]))
        lines.append("    (failure_mode " + q(adversarial["failure_mode"]) + "))")
    lines += [
        "  (authority (requirement_semantic_sha256 " + q(a["requirement_semantic_sha256"]) + ") (obligation_id "
        + q(a["obligation_id"]) + ")",
        "    (obligation_semantic_sha256 " + q(a["obligation_semantic_sha256"]) + ") (source_sha256 "
        + q(a["source_sha256"]) + "))",
    ]
    for role, identity, path, digest in d["required_inputs"]:
        lines.append("  (required_input (role " + q(role) + ") (id " + q(identity) + ") (path " + q(path)
                     + ") (sha256 " + q(digest) + "))")
    for role, identity, name, size, digest in d["prepared"]:
        lines.append("  (prepared (role " + q(role) + ") (id " + q(identity) + ") (name " + q(name) + ") (byte_size "
                     + str(size) + ") (sha256 " + q(digest) + "))")
    for identity, cell, step_n, register, expected, statement in d["properties"]:
        lines.append("  (property (id " + q(identity) + ") (cell " + q(cell) + ") (step_n " + str(step_n)
                     + ") (register " + q(register) + ") (expected " + _value(expected) + ")")
        lines.append("    (statement " + q(statement) + "))")
    for n, pc, word, length, fetches, writes in d["steps"]:
        fetched = "" if word is None else " (word " + _value(word) + ") (length " + str(length) + ")"  # an event boundary retires no word
        lines.append("  (step (n " + str(n) + ") (pc " + _value(pc) + ")" + fetched + " (fetches " + str(fetches) + ")"
                     + "".join(" (write (register " + str(reg) + ") (value " + _value(value) + "))"
                               for reg, value in writes) + ")")
    lines[-1] += ")"
    return "\n".join(lines) + "\n"
