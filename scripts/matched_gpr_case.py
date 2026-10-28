"""A matched GPR case's declaration, read from data (P4-SYSTEM.14 a44-1; decision_case-declarations-as-data.md).

Each reviewed case is one file, `evidence/<case>/case.sexp`, validated against `schema/matched-case.sexp`:
its guest program, its predeclared properties and their RV64 values, its control, its hand-reviewed steps,
its authority and its pinned prepared inputs. This module reads that file and maps it onto the review's
own records (`matched_gpr_property.ReviewedPropertyCase`); a case without a file is refused by name, and so
is a file that does not validate or whose id disagrees with its directory. `render` writes the canonical
text, so a declaration and its rendering are one byte sequence.
"""

from __future__ import annotations

from pathlib import Path

import check_sexp_schema as Schema
import matched_gpr_comparison as C
import matched_gpr_execution as E
import matched_gpr_property as P
import records_sexp as Records
import sexp as S

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = "schema/matched-case.sexp"
FILE = "case.sexp"
PREPARED_ROLES = ("guest-image", "reference-config", "expectation")


class CaseError(ValueError):
    """A declared case cannot be read as declared."""


def case_path(case_id: str) -> str:
    return "evidence/" + case_id + "/" + FILE


def declared_case_ids(root: Path | None = None) -> tuple[str, ...]:
    """Every case directory holding a declaration, in name order."""
    root = ROOT if root is None else root
    return tuple(sorted(path.parent.name for path in (root / "evidence").glob("*/" + FILE)))


def read_document(text: str, where: str):
    """Validate and parse one declaration's text; returns (case, prepared rows)."""
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

    control = sub(single_form(top, "control", where))
    authority = sub(single_form(top, "authority", where))
    properties = tuple(
        P.ReviewedProperty(item["id"], item["cell"], item["statement"],
                           C.GprWitness(item["step_n"], item["register"]), item["expected"])
        for item in (sub(form) for form in many("property")))
    steps = []
    for form in many("step"):
        item = sub(form)
        writes = tuple((sub(write)["register"], sub(write)["value"])
                       for write in form[1:] if str(write[0]) == "write")
        steps.append((item["n"], item["pc"], item["word"], item["length"], item["fetches"], writes))
    required = tuple(E.InputBinding(item["role"], item["id"], item["path"], item["sha256"])
                     for item in (sub(form) for form in many("required_input")))
    prepared = tuple((item["role"], item["id"], item["name"], item["byte_size"], item["sha256"])
                     for item in (sub(form) for form in many("prepared")))
    profile_id, requirement_id, source_id = single("profile_id"), single("requirement_id"), single("source_id")
    case = P.ReviewedPropertyCase(
        single("id"), profile_id, single("program"), single("instructions"), single("source_size"),
        single("source_sha256"), requirement_id, tuple(child[1] for child in many("obligation_ids")),
        single("contract_id"), single("contract_version"), properties, control["property_id"], control["value"],
        control["reason"], single("limitation"), tuple(steps), source_id, single("source_locator"),
        single("category"), single("risk"), single("coverage"),
        P.PropertyAuthority(profile_id, requirement_id, authority["requirement_semantic_sha256"],
                            authority["obligation_id"], authority["obligation_semantic_sha256"], source_id,
                            authority["source_sha256"]),
        required)
    if case.control_property_id not in {item.property_id for item in case.properties}:
        raise CaseError(where + ": the control names no declared property")
    if sorted(role for role, *_ in prepared) != sorted(("guest-image", "reference-config", "expectation", "expectation")):
        raise CaseError(where + ": the prepared inputs are not one image, one configuration and two expectations")
    return case, prepared


def single_form(top, name, where):
    found = [child for child in top[1:] if str(child[0]) == name]
    if len(found) != 1:
        raise CaseError(f"{where}: field {name} occurs {len(found)} times")
    return found[0]


def read_case(case_id: str, root: Path | None = None):
    """The declared case and its prepared rows; a case without a declaration is refused by name."""
    root = ROOT if root is None else root
    path = root / case_path(case_id)
    if not path.is_file():
        raise CaseError("no declaration for case " + case_id + ": " + case_path(case_id) + " is absent")
    case, prepared = read_document(path.read_text(), case_path(case_id))
    if case.case_id != case_id:
        raise CaseError(case_path(case_id) + ": declares " + case.case_id + ", not its directory's " + case_id)
    return case, prepared


def _value(number: int) -> str:
    return "0x%x" % number if number >= 4096 else str(number)


def render(case, prepared) -> str:
    """The canonical declaration text of a case: one field per line, values in hex above 4095."""
    q = Records.quote_string
    a = case.authority
    lines = [
        ";; " + case_path(case.case_id) + " — the reviewed declaration of matched case " + case.case_id
        + " (schema/matched-case.sexp).",
        ";; Data, not code (decision_case-declarations-as-data.md): read by scripts/matched_gpr_case.py.",
        "(case (id " + q(case.case_id) + ") (profile_id " + q(case.profile_id) + ")",
        "  (program " + q(case.program) + ") (instructions " + str(case.instructions) + ") (source_size "
        + str(case.source_size) + ")",
        "  (source_sha256 " + q(case.source_sha256) + ")",
        "  (requirement_id " + q(case.requirement_id) + ")"
        + "".join(" (obligation_ids " + q(item) + ")" for item in case.obligation_ids),
        "  (contract_id " + q(case.contract_id) + ") (contract_version " + q(case.contract_version) + ")",
        "  (control (property_id " + q(case.control_property_id) + ") (value " + _value(case.control_value)
        + ") (reason " + q(case.control_reason) + "))",
        "  (limitation " + q(case.limitation) + ")",
        "  (source_id " + q(case.source_id) + ") (source_locator " + q(case.source_locator) + ") (category "
        + q(case.category) + ") (risk " + q(case.risk) + ")",
        "  (coverage " + q(case.coverage) + ")",
        "  (authority (requirement_semantic_sha256 " + q(a.requirement_semantic_sha256) + ") (obligation_id "
        + q(a.obligation_id) + ")",
        "    (obligation_semantic_sha256 " + q(a.obligation_semantic_sha256) + ") (source_sha256 "
        + q(a.source_sha256) + "))",
    ]
    for item in case.required_inputs:
        lines.append("  (required_input (role " + q(item.role) + ") (id " + q(item.input_id) + ") (path " + q(item.path)
                     + ") (sha256 " + q(item.sha256) + "))")
    for role, identity, name, size, digest in prepared:
        lines.append("  (prepared (role " + q(role) + ") (id " + q(identity) + ") (name " + q(name) + ") (byte_size "
                     + str(size) + ") (sha256 " + q(digest) + "))")
    for item in case.properties:
        lines.append("  (property (id " + q(item.property_id) + ") (cell " + q(item.cell) + ") (step_n "
                     + str(item.witness.step_n) + ") (register " + q(item.witness.register) + ") (expected "
                     + _value(item.expected_value) + ")")
        lines.append("    (statement " + q(item.statement) + "))")
    for n, pc, word, length, fetches, writes in case.reviewed_steps:
        lines.append("  (step (n " + str(n) + ") (pc " + _value(pc) + ") (word " + _value(word) + ") (length "
                     + str(length) + ") (fetches " + str(fetches) + ")"
                     + "".join(" (write (register " + str(reg) + ") (value " + _value(value) + "))"
                               for reg, value in writes) + ")")
    lines[-1] += ")"
    return "\n".join(lines) + "\n"
