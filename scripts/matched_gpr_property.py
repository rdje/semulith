"""Pure source-property binding for the reviewed finite GPR cases.

Each reviewed case was reviewed against the pinned source and canonical catalogues
before collection: its program, its instruction words, its predeclared properties
and their RV64 values. A case declares one to MAX_PROPERTIES properties; the
control run discriminates exactly one of them, and every predeclared value is held
to the source derivation. A case is declared as data, `evidence/<case>/case.sexp`
(decision_case-declarations-as-data.md): `reviewed_case` reads it through
matched_gpr_case and maps it onto the records here; this module opens no file of
its own. Public graph/snapshot owners and file authentication remain
prerequisites; a finite witness never closes an obligation, and a case with many
witnesses closes none either.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib

import matched_gpr_case as Case
import matched_gpr_comparison as C
import matched_gpr_execution as E
import matched_gpr_input_review as T
import matched_gpr_manifest as M
import matched_gpr_relations as R
import records_sexp as Records


# The first captured case: the default the capture tools select when no case is named.
CASE_ID = "rv64gc-signed-div-truncation-v2"
# The M case declared in P4-SYSTEM.14 a42at, captured and retained since a42ax.
M_FORMS_CASE_ID = "rv64gc-m-forms-v3"
MAX_PROPERTIES = R.MAX_PROPERTIES
_ENTRY = 0x80000000
_PLACEHOLDER_LIMITATION = (
    "The planned record uses zero output placeholders; collection replaces sizes, "
    "hashes and exits with measurements."
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
    control_id: str | None  # the control run's id in the planned record; None in a declaration retained before a43b-2b
    control_statement: str | None  # the record's predeclared control target; None likewise
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


def _declared_case(declaration: dict) -> ReviewedPropertyCase:
    """Map a declaration's neutral data (matched_gpr_case.read_case) onto this review's records."""
    authority, control = declaration["authority"], declaration["control"]
    return ReviewedPropertyCase(
        declaration["id"],
        declaration["profile_id"],
        declaration["program"],
        declaration["instructions"],
        declaration["source_size"],
        declaration["source_sha256"],
        declaration["requirement_id"],
        declaration["obligation_ids"],
        declaration["contract_id"],
        declaration["contract_version"],
        tuple(
            ReviewedProperty(property_id, cell, statement, C.GprWitness(step, register), value)
            for property_id, cell, step, register, value, statement in declaration["properties"]
        ),
        control["property_id"],
        control["value"],
        control["reason"],
        control["id"],
        control["statement"],
        declaration["limitation"],
        declaration["steps"],
        declaration["source_id"],
        declaration["source_locator"],
        declaration["category"],
        declaration["risk"],
        declaration["coverage"],
        PropertyAuthority(
            declaration["profile_id"],
            declaration["requirement_id"],
            authority["requirement_semantic_sha256"],
            authority["obligation_id"],
            authority["obligation_semantic_sha256"],
            declaration["source_id"],
            authority["source_sha256"],
        ),
        tuple(E.InputBinding(*row) for row in declaration["required_inputs"]),
    )


def reviewed_case_ids() -> tuple[str, ...]:
    """Every case declared under evidence/, in name order."""
    return Case.declared_case_ids()


def reviewed_case(case_id: str) -> ReviewedPropertyCase:
    """Return fresh nested facts for a declared case, read from its declaration on every call."""
    _require(_text(case_id), "invalid property case ID")
    _require(case_id in reviewed_case_ids(), "no reviewed source property for selected case")
    try:
        return _declared_case(Case.read_case(case_id))
    except Case.CaseError as error:
        raise PropertyError("reviewed case declaration refused: " + str(error)) from None


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
        f"property claims require a plain tuple of 1..{MAX_PROPERTIES} claims",
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
    # An event boundary carries no word and writes nothing, and reads at most one parcel (the typed event binding, P4-SYSTEM.14 a43e-1, a49-1).
    event = numeric[2] is None and numeric[3] is None and numeric[4] in (0, 1) and writes == ()
    _require(
        all(type(value) is int for value in (numeric[:2] + numeric[4:] if event else numeric))
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
    case: ReviewedPropertyCase | None = None,
) -> SourcePropertyCheck:
    """Bind one reviewed case; authentication and complete policy stay separate.

    Every predeclared property is held to the source derivation: its witness must be an
    actual derived register change carrying exactly the reviewed value. The source-value
    finding's own witness is the control's; the other properties are read from the
    derivation it carries, so no second source read or arithmetic engine is introduced.
    A caller that already selected the reviewed case passes it and the binding opens no
    file; otherwise the case is read from its declaration here.
    """
    try:
        selected = freeze_context(
            context, profile_id=profile_id, experiment_id=experiment_id
        )
        _require(_text(case_id), "invalid property case ID")
        if case is None:
            if case_id not in reviewed_case_ids():
                return SourcePropertyCheck(
                    "unsupported", "no reviewed source property for selected case"
                )
            case = reviewed_case(case_id)
        _require(
            type(case) is ReviewedPropertyCase and case.case_id == case_id,
            "reviewed case differs from the selected case",
        )
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
