"""Pure source-property binding for the reviewed finite GPR cases.

Each reviewed case was reviewed against the pinned source and canonical catalogues
before collection: its program, its instruction words, its predeclared properties
and their RV64 values. A case declares one to MAX_PROPERTIES properties; the
control run discriminates exactly one of them, and every predeclared value is held
to the source derivation. No file is opened here. Public graph/snapshot owners and
file authentication remain prerequisites; a finite witness never closes an
obligation, and a case with many witnesses closes none either.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib

import matched_gpr_comparison as C
import matched_gpr_execution as E
import matched_gpr_input_review as T
import matched_gpr_manifest as M
import matched_gpr_relations as R
import records_sexp as Records


# The retained case: what the method/policy reviews and the capture command select.
CASE_ID = "rv64gc-signed-div-truncation-v2"
# Declared here before its declaration record and its capture (P4-SYSTEM.14 a42at).
M_FORMS_CASE_ID = "rv64gc-m-forms-v3"
MAX_PROPERTIES = R.MAX_PROPERTIES
_ENTRY = 0x80000000
_PUBLICATION_SHA = "85e1db6c831ba6d325722d728d257b3ac9a9bf0a654ba1dc385108e99df75716"
# The curated input is authenticated separately from current publication authority.
_REQUIRED_INPUT_ROWS = (
    (
        "normative-source",
        "RVI-M-DIV-STATEMENT",
        "profiles/rv64gc-lab-v0/retained/div-statement.html",
        "bbe3ff9dd6d8e1b452589669cd676d998265327eeaf8ed370bb95fcf15af1a58",
    ),
)
_REQUIREMENT_SEMANTICS = (
    "0deea596341b2462d8c61b90c37791e566d58ccfa95c4d30beaeebcd37e30989"
)
_OBLIGATION_SEMANTICS = (
    "b441b5339cbe879ba02970b69d7a1b51ce1e548a9c5f2bfe550b39beb04c8090"
)
_PLACEHOLDER_LIMITATION = (
    "The planned record uses zero output placeholders; collection replaces sizes, "
    "hashes and exits with measurements."
)
_ONES = (1 << 64) - 1
_WORD_NEGATIVE_HALF = 0xFFFFFFFF80000000  # -2^31 as a word, sign-extended to XLEN

# m-div.s: manually reviewed words and signed operands; source annotations are not authority.
_DIV_SOURCE_SHA = "a7cbbe8c3005a7c0da68bf356a0fb6b072dbe0cdcc659eff523e465c60ae907f"
_DIV_STATEMENT = (
    "For signed DIV with x5 = -7 and x6 = 2, the x7 change at boundary 2 "
    "is -3 (rounding toward zero)."
)
_DIV_PREFIX = (
    (0, 0x80000000, 0xFF900293, 4, 2, ((5, (1 << 64) - 7),)),
    (1, 0x80000004, 0x00200313, 4, 2, ((6, 2),)),
    (2, 0x80000008, 0x0262C3B3, 4, 2, ((7, (1 << 64) - 3),)),
)

# m-forms.s: every word and every value reviewed by hand against the chapter; the probe
# re-derives each word from the encoding fields and each value from independent arithmetic.
_M_FORMS_SOURCE_SHA = "232b4d96d87125c3ab876b2ec415d250a572433df57d5696afffde6a95f8d7a6"
_M_FORMS_STEPS = (
    (0, 0x80000000, 0xFF900293, 4, 2, ((5, (1 << 64) - 7),)),
    (1, 0x80000004, 0x00200313, 4, 2, ((6, 2),)),
    (2, 0x80000008, 0xFFF00393, 4, 2, ((7, _ONES),)),
    (3, 0x8000000C, 0x00100413, 4, 2, ((8, 1),)),
    (4, 0x80000010, 0x03F41413, 4, 2, ((8, 1 << 63),)),
    (5, 0x80000014, 0x00100493, 4, 2, ((9, 1),)),
    (6, 0x80000018, 0x01F49493, 4, 2, ((9, 1 << 31),)),
    (7, 0x8000001C, 0x02628533, 4, 2, ((10, (1 << 64) - 14),)),
    (8, 0x80000020, 0x026295B3, 4, 2, ((11, _ONES),)),
    (9, 0x80000024, 0x0272A633, 4, 2, ((12, (1 << 64) - 7),)),
    (10, 0x80000028, 0x0263B6B3, 4, 2, ((13, 1),)),
    (11, 0x8000002C, 0x0292873B, 4, 2, ((14, _WORD_NEGATIVE_HALF),)),
    (12, 0x80000030, 0x0262C7B3, 4, 2, ((15, (1 << 64) - 3),)),
    (13, 0x80000034, 0x0263D833, 4, 2, ((16, (1 << 63) - 1),)),
    (14, 0x80000038, 0x0262E8B3, 4, 2, ((17, _ONES),)),
    (15, 0x8000003C, 0x0263F933, 4, 2, ((18, 1),)),
    (16, 0x80000040, 0x0264C9BB, 4, 2, ((19, 0xFFFFFFFFC0000000),)),
    (17, 0x80000044, 0x0264DA3B, 4, 2, ((20, 0x40000000),)),
    (18, 0x80000048, 0x0254EABB, 4, 2, ((21, (1 << 64) - 2),)),
    (19, 0x8000004C, 0x0254FB3B, 4, 2, ((22, _WORD_NEGATIVE_HALF),)),
    (20, 0x80000050, 0x0202CBB3, 4, 2, ((23, _ONES),)),
    (21, 0x80000054, 0x0202DC33, 4, 2, ((24, _ONES),)),
    (22, 0x80000058, 0x0202ECB3, 4, 2, ((25, (1 << 64) - 7),)),
    (23, 0x8000005C, 0x0202FD33, 4, 2, ((26, (1 << 64) - 7),)),
    (24, 0x80000060, 0x02744DB3, 4, 2, ((27, 1 << 63),)),
    (25, 0x80000064, 0x01C00E13, 4, 2, ((28, 28),)),
    (26, 0x80000068, 0x02746E33, 4, 2, ((28, 0),)),
    (27, 0x8000006C, 0x0204CEBB, 4, 2, ((29, _ONES),)),
    (28, 0x80000070, 0x0204DF3B, 4, 2, ((30, _ONES),)),
    (29, 0x80000074, 0x0204EFBB, 4, 2, ((31, _WORD_NEGATIVE_HALF),)),
    (30, 0x80000078, 0x0204F53B, 4, 2, ((10, _WORD_NEGATIVE_HALF),)),
    (31, 0x8000007C, 0x0274C5BB, 4, 2, ((11, _WORD_NEGATIVE_HALF),)),
    (32, 0x80000080, 0x0274E63B, 4, 2, ((12, 0),)),
)
# (property id, policy cell, boundary, register, predeclared RV64 value, statement)
_M_FORMS_PROPERTIES = (
    ("form-mul", "form:mul", 7, "x10", (1 << 64) - 14,
     "For MUL with x5 = -7 and x6 = 2, the x10 change at boundary 7 is -14 (the low 64 bits of the product)."),
    ("form-mulh", "form:mulh", 8, "x11", _ONES,
     "For MULH with x5 = -7 and x6 = 2, the x11 change at boundary 8 is -1 (the high 64 bits of the signed product -14)."),
    ("form-mulhsu", "form:mulhsu", 9, "x12", (1 << 64) - 7,
     "For MULHSU with x5 = -7 (signed) and x7 = 2^64 - 1 (unsigned), the x12 change at boundary 9 is -7 (the high 64 bits of -7 x 2^64 + 7)."),
    ("form-mulhu", "form:mulhu", 10, "x13", 1,
     "For MULHU with x7 = 2^64 - 1 and x6 = 2 (both unsigned), the x13 change at boundary 10 is 1 (the high 64 bits of 2^65 - 2)."),
    ("form-mulw", "form:mulw", 11, "x14", _WORD_NEGATIVE_HALF,
     "For MULW with x5 = -7 and x9 = 0x80000000, the x14 change at boundary 11 is 0xffffffff80000000 (the low 32 bits of the product, sign-extended)."),
    ("form-div", "form:div", 12, "x15", (1 << 64) - 3,
     "For DIV with x5 = -7 and x6 = 2, the x15 change at boundary 12 is -3 (rounding toward zero)."),
    ("form-divu", "form:divu", 13, "x16", (1 << 63) - 1,
     "For DIVU with x7 = 2^64 - 1 and x6 = 2 (both unsigned), the x16 change at boundary 13 is 2^63 - 1."),
    ("form-rem", "form:rem", 14, "x17", _ONES,
     "For REM with x5 = -7 and x6 = 2, the x17 change at boundary 14 is -1 (the remainder takes the dividend's sign)."),
    ("form-remu", "form:remu", 15, "x18", 1,
     "For REMU with x7 = 2^64 - 1 and x6 = 2 (both unsigned), the x18 change at boundary 15 is 1."),
    ("form-divw", "form:divw", 16, "x19", 0xFFFFFFFFC0000000,
     "For DIVW with the words -2^31 (x9) and 2 (x6), the x19 change at boundary 16 is -2^30, sign-extended."),
    ("form-divuw", "form:divuw", 17, "x20", 0x40000000,
     "For DIVUW with the unsigned words 0x80000000 (x9) and 2 (x6), the x20 change at boundary 17 is 0x40000000."),
    ("form-remw", "form:remw", 18, "x21", (1 << 64) - 2,
     "For REMW with the words -2^31 (x9) and -7 (x5), the x21 change at boundary 18 is -2 (the dividend's sign)."),
    ("form-remuw", "form:remuw", 19, "x22", _WORD_NEGATIVE_HALF,
     "For REMUW with the unsigned words 0x80000000 (x9) and 0xfffffff9 (x5), the x22 change at boundary 19 is 0x80000000 sign-extended (the whole dividend)."),
    ("table1-div-by-zero", "table1:div-by-zero", 20, "x23", _ONES,
     "For DIV with x5 = -7 and x0 = 0, the x23 change at boundary 20 is -1 (Table 1: division by zero, all bits set; no trap)."),
    ("table1-divu-by-zero", "table1:divu-by-zero", 21, "x24", _ONES,
     "For DIVU with x5 = 2^64 - 7 and x0 = 0, the x24 change at boundary 21 is 2^64 - 1 (Table 1: division by zero, all bits set)."),
    ("table1-rem-by-zero", "table1:rem-by-zero", 22, "x25", (1 << 64) - 7,
     "For REM with x5 = -7 and x0 = 0, the x25 change at boundary 22 is -7 (Table 1: the remainder of division by zero is the dividend)."),
    ("table1-remu-by-zero", "table1:remu-by-zero", 23, "x26", (1 << 64) - 7,
     "For REMU with x5 = 2^64 - 7 and x0 = 0, the x26 change at boundary 23 is 2^64 - 7 (Table 1: the dividend)."),
    ("table1-div-overflow", "table1:div-overflow", 24, "x27", 1 << 63,
     "For DIV with x8 = -2^63 and x7 = -1, the x27 change at boundary 24 is -2^63 (Table 1: signed overflow, the quotient equals the dividend; no trap)."),
    ("table1-rem-overflow", "table1:rem-overflow", 26, "x28", 0,
     "For REM with x8 = -2^63 and x7 = -1, the x28 change at boundary 26 is 0 (Table 1: the overflow remainder, replacing the sentinel 28)."),
    ("table1-divw-by-zero", "table1:divw-by-zero", 27, "x29", _ONES,
     "For DIVW with the word -2^31 (x9) and x0 = 0, the x29 change at boundary 27 is -1 (Table 1 at L = 32: all bits set, sign-extended)."),
    ("table1-divuw-by-zero", "table1:divuw-by-zero", 28, "x30", _ONES,
     "For DIVUW with the unsigned word 0x80000000 (x9) and x0 = 0, the x30 change at boundary 28 is 2^32 - 1 sign-extended (all bits set)."),
    ("table1-remw-by-zero", "table1:remw-by-zero", 29, "x31", _WORD_NEGATIVE_HALF,
     "For REMW with the word -2^31 (x9) and x0 = 0, the x31 change at boundary 29 is -2^31 sign-extended (Table 1: the dividend's word)."),
    ("table1-remuw-by-zero", "table1:remuw-by-zero", 30, "x10", _WORD_NEGATIVE_HALF,
     "For REMUW with the unsigned word 0x80000000 (x9) and x0 = 0, the x10 change at boundary 30 is 0x80000000 sign-extended (Table 1: the dividend's word), replacing the MUL result."),
    ("table1-divw-overflow", "table1:divw-overflow", 31, "x11", _WORD_NEGATIVE_HALF,
     "For DIVW with the words -2^31 (x9) and -1 (x7), the x11 change at boundary 31 is -2^31 sign-extended (Table 1: word overflow, the quotient equals the dividend), replacing the MULH result."),
    ("table1-remw-overflow", "table1:remw-overflow", 32, "x12", 0,
     "For REMW with the words -2^31 (x9) and -1 (x7), the x12 change at boundary 32 is 0 (Table 1: the word overflow remainder), replacing the MULHSU result."),
)


@dataclass(frozen=True)
class PropertyAuthority:
    profile_id: str
    requirement_id: str
    requirement_semantic_sha256: str
    obligation_id: str
    obligation_semantic_sha256: str
    source_id: str
    source_sha256: str


@dataclass(frozen=True)
class PropertyClaim:
    """One declared property as the record states it: identity, scope, words, witness."""

    property_id: str
    requirement_id: str
    obligation_ids: tuple[str, ...]
    statement: str
    witness: C.GprWitness


@dataclass(frozen=True)
class PropertyContext:
    profile_id: str
    experiment_id: str
    program: str
    claims: tuple[PropertyClaim, ...]
    control_property_id: str
    authority: PropertyAuthority


@dataclass(frozen=True)
class ReviewedProperty:
    """One reviewed predeclared property: the policy cell it serves and its RV64 value."""

    property_id: str
    cell: str  # form:<mnemonic> or table1:<row>; the policy leg the property serves
    statement: str
    witness: C.GprWitness
    expected_value: int


@dataclass(frozen=True)
class ReviewedPropertyCase:
    case_id: str
    profile_id: str
    program: str
    instructions: int
    source_size: int
    source_sha256: str
    requirement_id: str
    obligation_ids: tuple[str, ...]
    contract_id: str
    contract_version: str
    properties: tuple[ReviewedProperty, ...]
    control_property_id: str  # the property whose value the control expectation changes
    control_value: int  # the wrong value the control expectation carries there
    control_reason: str
    limitation: str  # the case's own limitation line in the planned record
    reviewed_steps: tuple[tuple, ...]  # (n, pc, word, length, fetches, writes) reviewed by hand
    source_id: str
    source_locator: str
    category: str
    risk: str
    coverage: str
    authority: PropertyAuthority
    required_inputs: tuple[E.InputBinding, ...]

    def control(self) -> ReviewedProperty:
        return next(
            item for item in self.properties if item.property_id == self.control_property_id
        )

    def claims(self) -> tuple[PropertyClaim, ...]:
        """The claims a record of this case must carry, ordered by property identity."""
        return tuple(
            PropertyClaim(
                item.property_id,
                self.requirement_id,
                self.obligation_ids,
                item.statement,
                C.GprWitness(item.witness.step_n, item.witness.register),
            )
            for item in sorted(self.properties, key=lambda item: item.property_id)
        )


@dataclass(frozen=True)
class ObservedProperty:
    property_id: str
    witness: C.GprWitness
    value: int


@dataclass(frozen=True)
class SourcePropertyFacts:
    case: ReviewedPropertyCase
    observed: tuple[ObservedProperty, ...]  # one per reviewed property, case order
    source: E.InputBinding
    authority_inputs: tuple[E.InputBinding, ...]


@dataclass(frozen=True)
class SourcePropertyCheck:
    disposition: str  # matched / refused / unsupported; never qualification
    reason: str
    facts: SourcePropertyFacts | None = None


class PropertyError(ValueError):
    """Malformed context or contradictory selected source-property facts."""


def _require(condition: bool, reason: str):
    if not condition:
        raise PropertyError(reason)


def _text(value) -> bool:
    return type(value) is str and 1 <= len(value) <= T.TEXT_CHARS


def _digest(value) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and not (set(value) - set("0123456789abcdef"))
    )


def _copy_record(value):
    # Bound plain metadata before traversing or encoding; this is not a loader.
    nodes = 0
    string_bytes = 0

    def copy(item, depth):
        nonlocal nodes, string_bytes
        nodes += 1
        _require(
            nodes <= 4096 and depth <= 16, "authority tree exceeds node/depth bounds"
        )
        if type(item) is str:
            _require(len(item) <= T.TEXT_CHARS, "authority string exceeds bound")
            string_bytes += len(item.encode("utf-8"))
            _require(string_bytes <= 1024 * 1024, "authority strings exceed byte bound")
            return item
        if item is None or type(item) is bool:
            return item
        if type(item) is int:
            _require(item.bit_length() <= 128, "authority integer exceeds bound")
            return item
        if type(item) is list:
            _require(len(item) <= 4096, "authority list exceeds bound")
            return [copy(child, depth + 1) for child in item]
        if type(item) is dict:
            _require(len(item) <= 4096, "authority dictionary exceeds bound")
            result = {}
            for key, child in item.items():
                _require(_text(key), "invalid authority key")
                result[copy(key, depth + 1)] = copy(child, depth + 1)
            return {key: result[key] for key in sorted(result)}
        raise PropertyError("authority requires plain mapped record values")

    _require(type(value) is dict, "authority requires a plain mapped record")
    return copy(value, 0)


def _semantic_digest(record: dict, family: str) -> str:
    form = Records.dict_to_form(record)
    _require(
        str(form[0]) == family and Records.form_to_dict(form) == record,
        "authority record does not round-trip through its canonical owner",
    )
    if family == "requirement":
        # These are derived outputs, not source meaning. Never apply this to file pins.
        record = dict(
            record,
            implementation_status="planned",
            implementation_refs=[],
            evidence_ids=[],
        )
    encoded = Records.render_forms([Records.dict_to_form(record)]).encode("utf-8")
    domain = b"matched-gpr-property-authority-v1\0" + family.encode("ascii") + b"\0"
    return hashlib.sha256(domain + encoded).hexdigest()


def project_authority(
    profile_id: str, *, requirement: dict, obligation: dict, source: dict
) -> PropertyAuthority:
    """Fingerprint current validated canonical records, excluding derived outputs.

    The caller selects current authority and owns raw schema validation. Exact
    artifact authentication and actual dependency impact remain unfiltered.
    """
    try:
        _require(_text(profile_id), "invalid authority profile")
        requirement, obligation, source = map(
            _copy_record, (requirement, obligation, source)
        )
        _require(
            type(requirement["profile_ids"]) is list
            and profile_id in requirement["profile_ids"]
            and type(obligation["profile_ids"]) is list
            and profile_id in obligation["profile_ids"],
            "authority records differ from selected profile",
        )
        _require(
            all(_text(record["id"]) for record in (requirement, obligation, source))
            and _digest(source["sha256"]),
            "invalid authority identity/source digest",
        )
        return PropertyAuthority(
            profile_id,
            requirement["id"],
            _semantic_digest(requirement, "requirement"),
            obligation["id"],
            _semantic_digest(obligation, "obligation"),
            source["id"],
            source["sha256"],
        )
    except PropertyError:
        raise
    except (
        Records.RecordRefused,
        AttributeError,
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        raise PropertyError(
            "canonical authority record refuses: " + type(exc).__name__
        ) from None


def _freeze_authority(
    authority: PropertyAuthority, profile_id: str
) -> PropertyAuthority:
    _require(type(authority) is PropertyAuthority, "expected a plain PropertyAuthority")
    values = tuple(
        getattr(authority, key, None)
        for key in (
            "profile_id",
            "requirement_id",
            "requirement_semantic_sha256",
            "obligation_id",
            "obligation_semantic_sha256",
            "source_id",
            "source_sha256",
        )
    )
    _require(
        all(_text(value) for value in values)
        and values[0] == profile_id
        and all(_digest(values[n]) for n in (2, 4, 6)),
        "invalid selected property authority",
    )
    return PropertyAuthority(*values)


def _m_authority() -> PropertyAuthority:
    return PropertyAuthority(
        "rv64gc-lab-v0",
        "REQ-GC-M",
        _REQUIREMENT_SEMANTICS,
        "OB-GC-M",
        _OBLIGATION_SEMANTICS,
        "RVI-M",
        _PUBLICATION_SHA,
    )


def signed_division_case() -> ReviewedPropertyCase:
    """The retained case: one signed-DIV quotient witness over m-div.s (27 boundaries)."""
    return ReviewedPropertyCase(
        CASE_ID,
        "rv64gc-lab-v0",
        "m-div.s",
        27,
        2512,
        _DIV_SOURCE_SHA,
        "REQ-GC-M",
        ("OB-GC-M",),
        "rv64gc-lab-env-v2",
        "2",
        (
            ReviewedProperty(
                "signed-quotient",
                "form:div",
                _DIV_STATEMENT,
                C.GprWitness(2, "x7"),
                (1 << 64) - 3,
            ),
        ),
        "signed-quotient",
        (1 << 64) - 4,
        "Only boundary2 x7 expectation changes from -3 to -4.",
        "One finite DIV witness; full source/risk/feature policy remains pending.",
        _DIV_PREFIX,
        "RVI-M",
        "11.1.2",
        "defined",
        "medium",
        "one signed-DIV quotient witness",
        _m_authority(),
        tuple(E.InputBinding(*row) for row in _REQUIRED_INPUT_ROWS),
    )


def m_forms_case() -> ReviewedPropertyCase:
    """The crediting case: every M form and every Table 1 cell over m-forms.s (33 boundaries).

    Declared before its declaration record and its capture. The control changes the DIV
    rounding witness (boundary 12, x15) from -3 to -4, as the retained case's control did.
    """
    return ReviewedPropertyCase(
        M_FORMS_CASE_ID,
        "rv64gc-lab-v0",
        "m-forms.s",
        33,
        3886,
        _M_FORMS_SOURCE_SHA,
        "REQ-GC-M",
        ("OB-GC-M",),
        "rv64gc-lab-env-v2",
        "2",
        tuple(
            ReviewedProperty(
                property_id, cell, statement, C.GprWitness(step, register), value
            )
            for property_id, cell, step, register, value, statement in _M_FORMS_PROPERTIES
        ),
        "form-div",
        (1 << 64) - 4,
        "Only boundary12 x15 expectation changes from -3 to -4.",
        "Twenty-five finite M witnesses, the 13 forms and the 12 Table 1 cells, predeclared; "
        "full source/risk/feature policy remains pending.",
        _M_FORMS_STEPS,
        "RVI-M",
        "11.1.1 and 11.1.2 (Table 1)",
        "defined",
        "medium",
        "thirteen M forms and twelve Table 1 cells, one finite witness each",
        _m_authority(),
        tuple(E.InputBinding(*row) for row in _REQUIRED_INPUT_ROWS),
    )


_CASES = {CASE_ID: signed_division_case, M_FORMS_CASE_ID: m_forms_case}


def reviewed_case_ids() -> tuple[str, ...]:
    return tuple(_CASES)


def reviewed_case(case_id: str) -> ReviewedPropertyCase:
    """Return fresh nested facts for a reviewed case so a caller cannot alias the constants."""
    _require(_text(case_id), "invalid property case ID")
    _require(case_id in _CASES, "no reviewed source property for selected case")
    return _CASES[case_id]()


def _freeze_witness(witness) -> C.GprWitness:
    _require(type(witness) is C.GprWitness, "expected a plain GprWitness")
    step, register = getattr(witness, "step_n", None), getattr(witness, "register", None)
    _require(
        type(step) is int
        and 0 <= step < 4096
        and type(register) is str
        and register in tuple(f"x{n}" for n in range(1, 32)),
        "invalid bounded GPR witness",
    )
    return C.GprWitness(step, register)


def _freeze_claim(claim) -> PropertyClaim:
    _require(type(claim) is PropertyClaim, "expected a plain PropertyClaim")
    values = tuple(
        getattr(claim, key, None) for key in ("property_id", "requirement_id", "statement")
    )
    _require(all(_text(value) for value in values), "invalid property text")
    obligations = getattr(claim, "obligation_ids", None)
    _require(
        type(obligations) is tuple and 1 <= len(obligations) <= 64,
        "property obligations require a plain tuple of 1..64 IDs",
    )
    _require(
        all(_text(value) for value in obligations)
        and len(set(obligations)) == len(obligations),
        "invalid or duplicate property obligations",
    )
    return PropertyClaim(
        values[0],
        values[1],
        tuple(sorted(obligations)),
        values[2],
        _freeze_witness(getattr(claim, "witness", None)),
    )


def freeze_context(
    context: PropertyContext, *, profile_id: str, experiment_id: str
) -> PropertyContext:
    """Copy bounded metadata after its owner's canonical schema/scoped checks."""
    _require(type(context) is PropertyContext, "expected a plain PropertyContext")
    values = tuple(
        getattr(context, key, None)
        for key in ("profile_id", "experiment_id", "program", "control_property_id")
    )
    _require(all(_text(value) for value in values), "invalid property text")
    _require(
        _text(profile_id)
        and values[0] == profile_id
        and _text(experiment_id)
        and values[1] == experiment_id,
        "property context differs from selected scope",
    )
    claims = getattr(context, "claims", None)
    _require(
        type(claims) is tuple and 1 <= len(claims) <= MAX_PROPERTIES,
        "property claims require a plain tuple of 1..64 claims",
    )
    frozen = tuple(_freeze_claim(claim) for claim in claims)
    identities = tuple(claim.property_id for claim in frozen)
    _require(
        len(set(identities)) == len(identities), "duplicate property claim identities"
    )
    witnesses = tuple(claim.witness for claim in frozen)
    _require(
        len(set(witnesses)) == len(witnesses), "two property claims witness one observation"
    )
    _require(values[3] in identities, "control property is not one of the claims")
    return PropertyContext(
        values[0],
        values[1],
        values[2],
        tuple(sorted(frozen, key=lambda claim: claim.property_id)),
        values[3],
        _freeze_authority(getattr(context, "authority", None), profile_id),
    )


def _reviewed_step(step, expected) -> None:
    _require(type(step) is C.Author.SnapshotStep, "invalid snapshot step row")
    numeric = tuple(
        getattr(step, key, None)
        for key in ("n", "pc", "instruction_bits", "instruction_length", "fetches")
    )
    writes = step.writes
    _require(
        all(type(value) is int for value in numeric)
        and type(writes) is tuple
        and all(
            type(write) is tuple
            and len(write) == 2
            and all(type(value) is int for value in write)
            for write in writes
        )
        and (*numeric, writes) == expected,
        "snapshot steps differ from reviewed words/operands/values",
    )


def bind_source_property(
    context: PropertyContext,
    *,
    profile_id: str,
    experiment_id: str,
    manifest: M.ManifestPlan,
    source_values: C.SourceExpectationCheck,
    case_id: str = CASE_ID,
) -> SourcePropertyCheck:
    """Bind one reviewed case; authentication and complete policy stay separate.

    Every predeclared property is held to the source derivation: its witness must be an
    actual derived register change carrying exactly the reviewed value. The source-value
    finding's own witness is the control's; the other properties are read from the
    derivation it carries, so no second source read or arithmetic engine is introduced.
    """
    try:
        selected = freeze_context(
            context, profile_id=profile_id, experiment_id=experiment_id
        )
        _require(_text(case_id), "invalid property case ID")
        if case_id not in _CASES:
            return SourcePropertyCheck(
                "unsupported", "no reviewed source property for selected case"
            )
        case = reviewed_case(case_id)
        control = case.control()
        _require(
            (
                selected.profile_id,
                selected.program,
                selected.control_property_id,
                selected.claims,
            )
            == (case.profile_id, case.program, case.control_property_id, case.claims()),
            "property claims differ from reviewed finite case",
        )
        _require(
            selected.authority == case.authority,
            "current semantic authority differs from reviewed case",
        )
        _require(
            type(manifest) is M.ManifestPlan
            and type(manifest.relations) is R.RelationPlan,
            "expected public manifest/relation plans",
        )
        relations = manifest.relations
        execution = relations.execution
        _require(type(execution) is E.ExecutionPlan, "expected a public execution plan")
        _require(
            type(relations.properties) is tuple
            and relations.control_property_id == selected.control_property_id
            and relations.control_witness == control.witness
            and tuple(sorted(relations.properties, key=lambda item: item.property_id))
            == tuple(
                R.PropertyRelation(claim.property_id, claim.witness)
                for claim in selected.claims
            ),
            "selected relations differ from property context",
        )
        inventory = T.freeze_review(
            T.InputReview(profile_id, experiment_id, manifest.inputs),
            profile_id=profile_id,
            experiment_id=experiment_id,
        )
        inputs = {item.input_id: item for item in inventory.inputs}
        _require(
            type(manifest.child_input_ids) is tuple
            and 1 <= len(manifest.child_input_ids) <= T.MANIFEST_INPUTS,
            "invalid flat manifest children",
        )
        _require(
            all(
                inputs.get(pin.input_id) == pin
                and pin.input_id in manifest.child_input_ids
                for pin in case.required_inputs
            ),
            "reviewed normative source pins differ or are not children",
        )
        _require(
            type(execution.common_inputs) is tuple
            and len(execution.common_inputs) == len(E.COMMON_ROLES),
            "invalid common principals",
        )
        principal = next(
            item for item in execution.common_inputs if item.role == "guest-source"
        )
        _require(
            inputs.get(principal.input_id) == principal
            and principal.sha256 == case.source_sha256,
            "selected source differs from reviewed guest",
        )
        _require(
            type(source_values) is C.SourceExpectationCheck,
            "expected a public source-value finding",
        )
        if source_values.disposition == "unsupported":
            _require(
                source_values.facts is None, "unsupported source finding carries facts"
            )
            return SourcePropertyCheck(
                "unsupported", "source-value scope cannot ground this property"
            )
        _require(
            source_values.disposition == "matched"
            and type(source_values.facts) is C.SourceExpectationFacts,
            "source values must match before property binding",
        )
        facts = source_values.facts
        derived = facts.derivation
        _require(
            type(derived) is C.Author.SnapshotDerivation,
            "expected a public source derivation",
        )
        _require(
            facts.expectation_sha256 == execution.baseline_expectation.sha256,
            "source finding differs from selected baseline expectation",
        )
        _require(
            facts.witness == control.witness
            and type(facts.witness_value) is int
            and facts.witness_value == control.expected_value,
            "source witness differs from reviewed control value",
        )
        _require(
            type(execution.instructions) is int
            and execution.instructions == case.instructions
            and type(derived.instructions) is int
            and derived.instructions == case.instructions,
            "reviewed case requires its complete boundary budget",
        )
        _require(
            derived.program == case.program
            and derived.route == "snapshot-parcels-v1"
            and type(derived.entry) is int
            and derived.entry == _ENTRY
            and type(derived.source_size) is int
            and derived.source_size == case.source_size
            and derived.source_sha256 == principal.sha256,
            "source derivation differs from reviewed program/entry/identity",
        )
        _require(
            type(derived.steps) is tuple and len(derived.steps) == case.instructions,
            "source derivation lacks the complete bounded steps",
        )
        for expected in case.reviewed_steps:
            _reviewed_step(derived.steps[expected[0]], expected)
        observed = []
        for item in case.properties:
            step = derived.steps[item.witness.step_n]
            _require(type(step) is C.Author.SnapshotStep, "invalid snapshot step row")
            value = dict(step.writes).get(int(item.witness.register[1:]))
            _require(
                type(value) is int and value == item.expected_value,
                "predeclared value differs from the source derivation: " + item.property_id,
            )
            observed.append(
                ObservedProperty(
                    item.property_id,
                    C.GprWitness(item.witness.step_n, item.witness.register),
                    value,
                )
            )
        result = SourcePropertyFacts(
            case,
            tuple(observed),
            inputs[principal.input_id],
            tuple(inputs[pin.input_id] for pin in case.required_inputs),
        )
    except (
        PropertyError,
        T.ReviewError,
        AttributeError,
        KeyError,
        IndexError,
        TypeError,
        ValueError,
        StopIteration,
    ) as exc:
        return SourcePropertyCheck("refused", "source property: " + str(exc))
    return SourcePropertyCheck(
        "matched",
        "reviewed finite source properties bind; authentication/collection/qualification separate",
        result,
    )
