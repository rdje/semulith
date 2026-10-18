"""Bounded Sail GPR byte comparisons; no artifact I/O or qualification.

The caller supplies immutable snapshots and recorded process exits. This unit
does not authenticate those inputs, receipts, producers or execution provenance.
Schema loading is project-tool I/O; dossier_sexp owns expectation mapping.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
import hashlib
from pathlib import Path
import re

import derive_rv64gc_expectations as Author
import check_sexp_schema as K
import dossier_sexp as D
import matched_gpr_image as G
import run_rv64gc_sail as Sail
import sexp as S

EXPECTATION_BYTES = 1024 * 1024
TRACE_BYTES = 4 * 1024 * 1024
MAX_BOUNDARIES = 4096
_REGISTER = re.compile(r"x([1-9]|[12][0-9]|3[01])\Z")
_HEX = re.compile(r"0[xX][0-9a-fA-F]+\Z")


class UnitError(ValueError):
    """The supplied byte unit refuses; this is not a record-validity verdict."""


@dataclass(frozen=True)
class ExpectationImageContext:
    program: str
    instructions: int
    entry: int


@dataclass(frozen=True)
class GprWitness:
    step_n: int
    register: str


@dataclass(frozen=True)
class RunBytes:
    trace: bytes
    process_exit: int


@dataclass(frozen=True)
class RunComparison:
    run_kind: str
    comparison: Sail.Comparison | None
    refusal: str | None


@dataclass(frozen=True)
class ComparisonUnit:
    disposition: str
    reason: str
    runs: tuple[RunComparison, ...] = ()


def _bounded(payload: bytes, limit: int, where: str, *, empty: bool) -> None:
    if type(payload) is not bytes:
        raise UnitError(f"{where}: immutable snapshot bytes required")
    if len(payload) > limit or (not empty and not payload):
        raise UnitError(f"{where}: payload outside {0 if empty else 1}..{limit} bytes")


def _parent_context(instructions: int, program: str | None) -> None:
    if program is not None and (type(program) is not str or not 1 <= len(program) <= 65536):
        raise UnitError("parent program must be a plain string of 1..65536 characters")
    if type(instructions) is not int or not 1 <= instructions <= MAX_BOUNDARIES:
        raise UnitError(f"parent budget must contain 1..{MAX_BOUNDARIES} boundaries")


@lru_cache(maxsize=1)
def _schema():
    return K.load_schema(Path(__file__).resolve().parent.parent / "schema/expectations.sexp")


def _rv64(value: str, where: str) -> int:
    if not _HEX.fullmatch(value) or len(value[2:].lstrip("0")) > 16:
        raise UnitError(f"{where}: hexadecimal RV64 value required")
    return int(value, 16)


def _expectation(payload: bytes, instructions: int, where: str) -> dict:
    try:
        text = payload.decode("utf-8")
        constructs, operators = _schema()
        errors = K.validate_text(text, constructs, operators, where)
        if errors:
            raise UnitError(f"{where} shape: {errors[0]}")
        forms = [form for form in S.parse(text, where) if form[0] != "comment"]
        if len(forms) != 1 or forms[0][0] != "expectations":
            raise UnitError(f"{where}: exactly one expectations document required")
        doc = D.expectations_to_doc(forms[0])
        if doc.get("instructions") != instructions:
            raise UnitError(f"{where}: instruction budget differs from parent")
        if len(doc["step"]) != instructions or [s["n"] for s in doc["step"]] != list(range(instructions)):
            raise UnitError(f"{where}: steps must cover the complete ordered budget")
        for step in doc["step"]:
            for register, value in step["writes"].items():
                if not _REGISTER.fullmatch(register):
                    raise UnitError(f"{where}: change register must be canonical x1..x31")
                _rv64(value, f"{where}/step{step['n']}/{register}")
        return doc
    except (UnicodeError, S.SexpError, K.SchemaError, D.DossierError,
            RecursionError, ValueError, OSError) as exc:
        if isinstance(exc, UnitError):
            raise
        raise UnitError(f"{where}: cannot decode/validate expectations: {exc}") from exc


def _compare(kind: str, run: RunBytes, expected: dict) -> RunComparison:
    try:
        result = Sail.compare_observations(expected, run.trace.decode("utf-8"), run.process_exit)
        return RunComparison(kind, result, None)
    except (UnicodeError, Sail.SailError) as exc:
        return RunComparison(kind, None, str(exc))


def expectation_image_context(payload: bytes, *, instructions: int,
                              program: str) -> ExpectationImageContext:
    """Bind explicit RV64 entry metadata through the sole expectation decoder.

    This new consumer requires entry; generic expectations and legacy byte
    comparisons keep their existing optional-entry contract. Source/image
    correspondence, alignment, authentication, tool adequacy and qualification
    are separate. Unsupported expectation flags grant no credit here. Schema
    loading is project-tool I/O; no artifact paths, builds or processes are used.
    """
    if program is None:
        raise UnitError("image context requires an explicit parent program")
    _parent_context(instructions, program)
    _bounded(payload, EXPECTATION_BYTES, "image expectation", empty=False)
    doc = _expectation(payload, instructions, "image expectation")
    if doc["program"] != program:
        raise UnitError("expectation program differs from parent")
    entry = doc.get("entry")
    if type(entry) is not str:
        raise UnitError("image expectation requires an explicit string entry")
    return ExpectationImageContext(program, instructions, _rv64(entry, "image expectation entry"))


def compare_unit(*, instructions: int, witness: GprWitness,
                 baseline_expectation: bytes, control_expectation: bytes,
                 baseline: RunBytes, repeat: RunBytes, control: RunBytes,
                 program: str | None = None) -> ComparisonUnit:
    """Compute a finite three-run byte comparison, never method qualification.

    Bounds are payload limits, not exact RAM caps. All five payloads are checked
    before decoding/parsing; full authentication and aggregate method budgets
    belong to orchestration. Invalid method inputs raise UnitError. Unsupported
    expectations and valid failed comparisons return separate dispositions.
    An optional parent program binds both expectation identifiers exactly; omitted
    context preserves the legacy pure-unit boundary. This is not source/image proof.
    """
    _parent_context(instructions, program)
    if (not isinstance(witness, GprWitness) or type(witness.step_n) is not int
            or not 0 <= witness.step_n < instructions or not isinstance(witness.register, str)
            or not _REGISTER.fullmatch(witness.register)):
        raise UnitError("witness must name an in-budget boundary and canonical x1..x31")
    _bounded(baseline_expectation, EXPECTATION_BYTES, "baseline expectation", empty=False)
    _bounded(control_expectation, EXPECTATION_BYTES, "control expectation", empty=False)
    for kind, run in (("baseline", baseline), ("repeat", repeat), ("control", control)):
        if not isinstance(run, RunBytes) or type(run.process_exit) is not int:
            raise UnitError(f"{kind}: typed run and actual integer process exit required")
        _bounded(run.trace, TRACE_BYTES, f"{kind} trace", empty=True)
    base = _expectation(baseline_expectation, instructions, "baseline expectation")
    changed = _expectation(control_expectation, instructions, "control expectation")
    if program is not None and (base["program"] != program or changed["program"] != program):
        raise UnitError("expectation program differs from parent")
    for doc in (base, changed):
        if doc.get("cross_model") is False or "expect_divergence" in doc or "refuse" in doc:
            return ComparisonUnit(
                "unsupported", "cross-model exclusions, profile differences and fault injection need another method")
    runs = (_compare("baseline", baseline, base), _compare("repeat", repeat, base),
            _compare("control", control, changed))

    def failed(reason: str) -> ComparisonUnit:
        return ComparisonUnit("failed", reason, runs)

    for run in runs:
        if run.refusal is not None:
            return failed(f"{run.run_kind} comparison refused: {run.refusal}")
    if any(run.comparison.verdict != "AGREE" for run in runs[:2]):
        return failed("baseline and repeat must both agree")
    if repeat.trace != baseline.trace:
        return failed("repeat raw bytes differ from baseline")
    if control.trace != baseline.trace:
        return failed("control raw bytes differ from baseline")
    n, register = witness.step_n, witness.register
    base_writes, control_writes = base["step"][n]["writes"], changed["step"][n]["writes"]
    if register not in base_writes or register not in control_writes:
        return failed("witness must declare the register change in both expectations")
    if int(base_writes[register], 16) == int(control_writes[register], 16):
        return failed("control must change the witnessed RV64 value")
    restored = deepcopy(changed)
    restored["step"][n]["writes"][register] = base_writes[register]
    if restored != base:
        return failed("control expectation changes data outside the sole witnessed value")
    result = runs[2].comparison
    difference = result.gpr_difference
    observed = tuple(sorted((reg, int(value, 16)) for reg, value in base_writes.items()))
    expected = tuple(sorted((reg, int(value, 16)) for reg, value in control_writes.items()))
    if (result.verdict != "DIVERGE" or difference is None or difference.step_n != n
            or difference.observed != observed or difference.expected != expected):
        return failed("control must diverge at exactly the witnessed complete GPR change sets")
    return ComparisonUnit(
        "satisfied", "finite supplied-byte comparison satisfied; authentication and qualification pending", runs)


@dataclass(frozen=True)
class SourceExpectationFacts:
    derivation: Author.SnapshotDerivation
    expectation_size: int
    expectation_sha256: str
    witness: GprWitness
    witness_value: int | None


@dataclass(frozen=True)
class SourceExpectationCheck:
    disposition: str  # matched / failed / refused / unavailable / unsupported
    reason: str
    facts: SourceExpectationFacts | None = None
    difference: Sail.GprDifference | None = None


def compare_source_expectation(*, source: bytes, baseline_expectation: bytes,
                               instructions: int, program: str,
                               witness: GprWitness) -> SourceExpectationCheck:
    """Bind complete supplied GPR expectations to the existing snapshot author.

    This ordinary-fetched-boundary consumer checks values and a typed witness.
    Authentication, producer/property review, event binding and qualification are
    separate. Canonical schema/tool reads remain explicit; no artifact is reopened.
    """
    try:
        if program is None:
            raise UnitError("source expectation requires an explicit parent program")
        _parent_context(instructions, program)
        _bounded(source, G.SOURCE_BYTES, "source", empty=False)
        _bounded(baseline_expectation, EXPECTATION_BYTES, "baseline expectation", empty=False)
        if (type(witness) is not GprWitness or type(witness.step_n) is not int
                or not 0 <= witness.step_n < instructions or type(witness.register) is not str
                or _REGISTER.fullmatch(witness.register) is None):
            raise UnitError("witness must name an in-budget boundary and canonical x1..x31")
        selected = GprWitness(witness.step_n, witness.register)
        G.prepare_guest_source(source, program=program, entry=Author.ENTRY)
    except UnitError as exc:
        return SourceExpectationCheck("refused", str(exc))
    except G.ImageError:
        return SourceExpectationCheck("refused", "source preflight refuses")
    try:
        doc = _expectation(baseline_expectation, instructions, "baseline expectation")
        if doc["program"] != program:
            raise UnitError("expectation program differs from parent")
        if type(doc.get("entry")) is not str:
            raise UnitError("source expectation requires an explicit string entry")
        entry = _rv64(doc["entry"], "source expectation entry")
    except UnitError as exc:
        return SourceExpectationCheck("refused", str(exc))
    if entry != Author.ENTRY:
        return SourceExpectationCheck("unsupported", "entry exceeds the snapshot author's fixed cold context")
    excluded = doc.get("cross_model") is False or "expect_divergence" in doc or "refuse" in doc
    if excluded:
        return SourceExpectationCheck("unsupported", "expectation exclusions need another method")
    if any(step["insn"].startswith("<") or Sail.LEGACY_FETCH.fullmatch(step["insn"])
           or Sail.DECLARED_INTERRUPT.match(step["derivation"]) for step in doc["step"]):
        return SourceExpectationCheck("unsupported", "declared event boundaries need typed event binding")
    try:
        derived = Author.derive_snapshot(source, program=program, instructions=instructions)
    except Author.SnapshotUnsupported:
        return SourceExpectationCheck("unsupported", "source exceeds the snapshot author's supported semantics")
    except Author.SnapshotUnavailable:
        return SourceExpectationCheck("unavailable", "canonical snapshot author context is unavailable")
    except Author.SnapshotError:
        return SourceExpectationCheck("refused", "source derivation refuses")
    if (type(derived) is not Author.SnapshotDerivation or derived.program != program
            or type(derived.instructions) is not int or derived.instructions != instructions
            or derived.entry != entry or derived.source_size != len(source)
            or derived.source_sha256 != hashlib.sha256(source).hexdigest()
            or type(derived.steps) is not tuple or len(derived.steps) != instructions
            or any(type(step) is not Author.SnapshotStep or type(step.n) is not int or step.n != n
                   for n, step in enumerate(derived.steps))):
        return SourceExpectationCheck("refused", "snapshot author result differs from requested context")
    if any(step.instruction_bits is None or step.instruction_length is None for step in derived.steps):
        return SourceExpectationCheck("unsupported", "unfetched boundaries need typed event binding")
    value = dict(derived.steps[selected.step_n].writes).get(int(selected.register[1:]))
    facts = SourceExpectationFacts(derived, len(baseline_expectation),
                                   hashlib.sha256(baseline_expectation).hexdigest(), selected, value)
    for step, expected in zip(derived.steps, doc["step"]):
        observed = tuple(sorted((f"x{reg}", val) for reg, val in step.writes))
        wanted = tuple(sorted((reg, int(val, 16)) for reg, val in expected["writes"].items()))
        if observed != wanted:
            return SourceExpectationCheck(
                "failed", f"baseline GPR changes differ from source at step {step.n}", facts,
                Sail.GprDifference(step.n, observed, wanted))
    if value is None:
        return SourceExpectationCheck("failed", "witness is not an actual derived register change", facts)
    return SourceExpectationCheck(
        "matched", "complete source-derived GPR changes and witness match; qualification pending", facts)
