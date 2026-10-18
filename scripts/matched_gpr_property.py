"""Pure source-property binding for one reviewed signed-DIV observation.

The fixed case was reviewed against the pinned source and canonical catalogues
before collection. No file is opened here. Public graph/snapshot owners and file
authentication remain prerequisites; a finite witness never closes an obligation.
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


CASE_ID = "rv64gc-signed-div-truncation-v1"
_SOURCE_SHA = "a7cbbe8c3005a7c0da68bf356a0fb6b072dbe0cdcc659eff523e465c60ae907f"
_STATEMENT = (
    "For signed DIV with x5 = -7 and x6 = 2, the x7 change at boundary 2 "
    "is -3 (rounding toward zero)."
)
_AUTHORITY_ROWS = (
    (
        "normative-source",
        "RVI-M",
        ".materials/riscv/pinned-v20260120/unpriv/m-st-ext.html",
        "85e1db6c831ba6d325722d728d257b3ac9a9bf0a654ba1dc385108e99df75716",
    ),
)
_REQUIREMENT_SEMANTICS = (
    "0deea596341b2462d8c61b90c37791e566d58ccfa95c4d30beaeebcd37e30989"
)
_OBLIGATION_SEMANTICS = (
    "b441b5339cbe879ba02970b69d7a1b51ce1e548a9c5f2bfe550b39beb04c8090"
)
# Manually reviewed words and signed operands; source annotations are not authority.
_PREFIX = (
    (0, 0x80000000, 0xFF900293, 4, 2, ((5, (1 << 64) - 7),)),
    (1, 0x80000004, 0x00200313, 4, 2, ((6, 2),)),
    (2, 0x80000008, 0x0262C3B3, 4, 2, ((7, (1 << 64) - 3),)),
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
class PropertyContext:
    profile_id: str
    experiment_id: str
    program: str
    property_id: str
    requirement_id: str
    obligation_ids: tuple[str, ...]
    statement: str
    witness: C.GprWitness
    authority: PropertyAuthority


@dataclass(frozen=True)
class ReviewedPropertyCase:
    case_id: str
    profile_id: str
    program: str
    instructions: int
    requirement_id: str
    obligation_ids: tuple[str, ...]
    contract_id: str
    contract_version: str
    statement: str
    witness: C.GprWitness
    expected_value: int
    control_value: int
    source_id: str
    source_locator: str
    category: str
    risk: str
    coverage: str
    authority: PropertyAuthority
    required_inputs: tuple[E.InputBinding, ...]


@dataclass(frozen=True)
class SourcePropertyFacts:
    case: ReviewedPropertyCase
    property_id: str
    source: E.InputBinding
    authority_inputs: tuple[E.InputBinding, ...]
    observed_value: int


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


def signed_division_case() -> ReviewedPropertyCase:
    """Return fresh nested facts so a caller cannot alias the reviewed constants."""
    return ReviewedPropertyCase(
        CASE_ID,
        "rv64gc-lab-v0",
        "m-div.s",
        27,
        "REQ-GC-M",
        ("OB-GC-M",),
        "rv64gc-lab-env-v2",
        "2",
        _STATEMENT,
        C.GprWitness(2, "x7"),
        (1 << 64) - 3,
        (1 << 64) - 4,
        "RVI-M",
        "11.1.2",
        "defined",
        "medium",
        "one signed-DIV quotient witness",
        PropertyAuthority(
            "rv64gc-lab-v0",
            "REQ-GC-M",
            _REQUIREMENT_SEMANTICS,
            "OB-GC-M",
            _OBLIGATION_SEMANTICS,
            "RVI-M",
            _AUTHORITY_ROWS[0][3],
        ),
        tuple(E.InputBinding(*row) for row in _AUTHORITY_ROWS),
    )


def freeze_context(
    context: PropertyContext, *, profile_id: str, experiment_id: str
) -> PropertyContext:
    """Copy bounded metadata after its owner's canonical schema/scoped checks."""
    _require(type(context) is PropertyContext, "expected a plain PropertyContext")
    values = tuple(
        getattr(context, key, None)
        for key in (
            "profile_id",
            "experiment_id",
            "program",
            "property_id",
            "requirement_id",
            "statement",
        )
    )
    _require(all(_text(value) for value in values), "invalid property text")
    _require(
        _text(profile_id)
        and values[0] == profile_id
        and _text(experiment_id)
        and values[1] == experiment_id,
        "property context differs from selected scope",
    )
    obligations = getattr(context, "obligation_ids", None)
    _require(
        type(obligations) is tuple and 1 <= len(obligations) <= 64,
        "property obligations require a plain tuple of 1..64 IDs",
    )
    _require(
        all(_text(value) for value in obligations)
        and len(set(obligations)) == len(obligations),
        "invalid or duplicate property obligations",
    )
    witness = getattr(context, "witness", None)
    _require(type(witness) is C.GprWitness, "expected a plain GprWitness")
    step, register = getattr(witness, "step_n", None), getattr(
        witness, "register", None
    )
    _require(
        type(step) is int
        and 0 <= step < 4096
        and type(register) is str
        and register in tuple(f"x{n}" for n in range(1, 32)),
        "invalid bounded GPR witness",
    )
    return PropertyContext(
        values[0],
        values[1],
        values[2],
        values[3],
        values[4],
        tuple(sorted(obligations)),
        values[5],
        C.GprWitness(step, register),
        _freeze_authority(getattr(context, "authority", None), profile_id),
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
    """Bind one reviewed case; authentication and complete policy stay separate."""
    try:
        selected = freeze_context(
            context, profile_id=profile_id, experiment_id=experiment_id
        )
        _require(_text(case_id), "invalid property case ID")
        if case_id != CASE_ID:
            return SourcePropertyCheck(
                "unsupported", "no reviewed source property for selected case"
            )
        case = signed_division_case()
        _require(
            (
                selected.profile_id,
                selected.program,
                selected.requirement_id,
                selected.obligation_ids,
                selected.statement,
                selected.witness,
            )
            == (
                case.profile_id,
                case.program,
                case.requirement_id,
                case.obligation_ids,
                case.statement,
                case.witness,
            ),
            "property claim differs from reviewed finite case",
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
            relations.property_id == selected.property_id
            and relations.witness == selected.witness,
            "selected relation differs from property context",
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
            and principal.sha256 == _SOURCE_SHA,
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
            facts.witness == selected.witness
            and type(facts.witness_value) is int
            and facts.witness_value == case.expected_value,
            "source witness differs from reviewed quotient",
        )
        _require(
            type(execution.instructions) is int
            and execution.instructions == case.instructions
            and type(derived.instructions) is int
            and derived.instructions == case.instructions,
            "reviewed property requires the complete 27-boundary budget",
        )
        _require(
            derived.program == case.program
            and derived.route == "snapshot-parcels-v1"
            and type(derived.entry) is int
            and derived.entry == 0x80000000
            and type(derived.source_size) is int
            and derived.source_size == 2512
            and derived.source_sha256 == principal.sha256,
            "source derivation differs from reviewed program/entry/identity",
        )
        _require(
            type(derived.steps) is tuple and len(derived.steps) == case.instructions,
            "source derivation lacks the complete bounded steps",
        )
        for step, expected in zip(derived.steps[:3], _PREFIX):
            _require(type(step) is C.Author.SnapshotStep, "invalid snapshot prefix row")
            numeric = tuple(
                getattr(step, key, None)
                for key in (
                    "n",
                    "pc",
                    "instruction_bits",
                    "instruction_length",
                    "fetches",
                )
            )
            writes = step.writes
            _require(
                all(type(value) is int for value in numeric)
                and type(writes) is tuple
                and len(writes) == 1
                and type(writes[0]) is tuple
                and len(writes[0]) == 2
                and all(type(value) is int for value in writes[0])
                and (*numeric, writes) == expected,
                "snapshot prefix differs from reviewed words/operands/quotient",
            )
        result = SourcePropertyFacts(
            case,
            selected.property_id,
            inputs[principal.input_id],
            tuple(inputs[pin.input_id] for pin in case.required_inputs),
            facts.witness_value,
        )
    except (
        PropertyError,
        T.ReviewError,
        AttributeError,
        KeyError,
        TypeError,
        ValueError,
        StopIteration,
    ) as exc:
        return SourcePropertyCheck("refused", "source property: " + str(exc))
    return SourcePropertyCheck(
        "matched",
        "reviewed finite source property binds; authentication/collection/qualification separate",
        result,
    )
