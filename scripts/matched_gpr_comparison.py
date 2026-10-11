"""Bounded Sail GPR byte comparisons; no artifact I/O or qualification.

The caller supplies immutable snapshots and recorded process exits. This unit
does not authenticate those inputs, receipts, producers or execution provenance.
Schema loading is project-tool I/O; dossier_sexp owns expectation mapping.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import re

import check_sexp_schema as K
import dossier_sexp as D
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
    if program is not None and (type(program) is not str or not 1 <= len(program) <= 65536):
        raise UnitError("parent program must be a plain string of 1..65536 characters")
    if type(instructions) is not int or not 1 <= instructions <= MAX_BOUNDARIES:
        raise UnitError(f"parent budget must contain 1..{MAX_BOUNDARIES} boundaries")
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
