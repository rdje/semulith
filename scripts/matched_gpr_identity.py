#!/usr/bin/env python3
"""Authenticate a retained Sail execution descriptor, without opening its binary.

This finite dependency of the future method evaluator checks one input, not an
experiment. The caller owns raw parent-schema/graph validation and currentness of
the wider dependency closure. Candidate dictionaries are already caller-owned;
the 64 KiB bound applies to the retained descriptor, not total process memory.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import re

import check_sexp_schema as K
import dossier_sexp as D
import experiment_artifacts as A
from experiment_verification import is_canonical_path
import sexp as S

ROOT = Path(__file__).resolve().parent.parent
IDENTITY_BYTES = 64 * 1024
REQUIRED_FIELDS = ("id", "origin", "kind", "binary", "binary_sha256")
OPTIONAL_FIELDS = ("release", "version", "source_commit", "asset", "asset_sha256")


@dataclass(frozen=True)
class IdentityCheck:
    disposition: str  # matched / stale / unavailable / refused; never qualification
    reason: str
    pin: A.PinResult | None = None  # None if the request refuses before file I/O.
    execution_identity: tuple[tuple[str, str], ...] = ()  # Only on a current match.


class IdentityError(ValueError):
    """The request or retained descriptor cannot supply this method's identity."""


@lru_cache(maxsize=1)
def _schema():
    return K.load_schema(ROOT / "schema/references.sexp")


def _execution_identity(candidate: dict) -> tuple[tuple[str, str], ...]:
    if not isinstance(candidate, dict):
        raise IdentityError("expected a candidate dictionary")
    for field in REQUIRED_FIELDS:
        if not isinstance(candidate.get(field), str) or not candidate[field]:
            raise IdentityError(f"missing/invalid execution field {field}")
    for field in OPTIONAL_FIELDS:
        if field in candidate and not isinstance(candidate[field], str):
            raise IdentityError(f"invalid execution field {field}")
    if candidate["id"] != "sail-riscv":
        raise IdentityError("this method requires candidate sail-riscv")
    if not is_canonical_path(candidate["binary"]):
        raise IdentityError("noncanonical relative binary identity")
    for field in ("binary_sha256", "asset_sha256"):
        if field in candidate and re.fullmatch(r"[0-9a-f]{64}", candidate[field]) is None:
            raise IdentityError(f"invalid execution digest {field}")
    return tuple((field, candidate[field]) for field in REQUIRED_FIELDS + OPTIONAL_FIELDS
                 if field in candidate)


def _descriptor(payload: bytes, path: str) -> tuple[tuple[str, str], ...]:
    # Defense in depth: the public reader enforces this bound before artifact I/O.
    if type(payload) is not bytes or not 1 <= len(payload) <= IDENTITY_BYTES:
        raise IdentityError("identity requires 1..65536 immutable bytes")
    text = payload.decode("utf-8")
    constructs, operators = _schema()
    errors = K.validate_text(text, constructs, operators, path)
    if errors:
        raise IdentityError(f"identity shape: {errors[0]}")
    forms = [form for form in S.parse(text, path) if form[0] != "comment"]
    if len(forms) != 1 or forms[0][0] != "references":
        raise IdentityError("expected exactly one references document")
    doc = D.references_to_doc(forms[0])
    if len(doc.get("candidate", [])) != 1 or doc.get("experiment", []):
        raise IdentityError("identity requires one candidate and no experiments")
    return _execution_identity(doc["candidate"][0])


def read_reference_identity(root: Path, record: dict, current_candidate: dict) -> IdentityCheck:
    """Read one reference-identity input once; preserve independent pin findings.

    A matched pin with invalid syntax refuses. Changed pins or execution fields
    are stale; absent/unreadable data stays unavailable. Excluded descriptive
    metadata is not execution identity; wider relevant changes need closure checks.
    A match grants no receipt, process, replay, ancestry or qualification credit.
    """
    try:
        if not isinstance(record, dict) or record.get("role") != "reference-identity":
            raise IdentityError("expected a reference-identity input")
        if not isinstance(record.get("id"), str) or re.fullmatch(
                r"[A-Za-z][A-Za-z0-9._:/-]*", record["id"]) is None:
            raise IdentityError("invalid reference-identity input id")
        current = _execution_identity(current_candidate)
    except IdentityError as exc:
        return IdentityCheck("refused", str(exc))

    snapshot = A.read_snapshot(root, "input", record, max_bytes=IDENTITY_BYTES)
    pin = snapshot.pin
    if pin.disposition != "matched":
        disposition = "stale" if pin.disposition == "mismatch" else pin.disposition
        return IdentityCheck(disposition, pin.reason, pin)
    try:
        retained = _descriptor(snapshot.data, record["path"])
    except (IdentityError, UnicodeError, S.SexpError, K.SchemaError,
            D.DossierError, RecursionError, ValueError, OSError) as exc:
        return IdentityCheck("refused", f"cannot use retained identity: {exc}", pin)
    if retained != current:
        return IdentityCheck("stale", "retained execution identity differs from current candidate", pin)
    return IdentityCheck("matched", "retained execution identity matches; qualification pending",
                         pin, retained)
