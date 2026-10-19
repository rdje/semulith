#!/usr/bin/env python3
"""Bind and emit bounded retained Sail descriptors without accessing the binary.

Readers authenticate one input or consume its already authenticated bytes. The
emitter uses frozen selected fields and explicit descriptor metadata. Callers own
raw parent-schema/graph validation and wider dependency currentness. The 64 KiB
descriptor ceiling is an artifact bound, not a total process-memory guarantee.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import re

import check_sexp_schema as K
import dossier_sexp as D
import experiment_artifacts as A
import records_sexp as R
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


@dataclass(frozen=True)
class ReferenceIdentity:
    """Selected canonical identity, frozen by bind_reference_identity before I/O."""

    fields: tuple[tuple[str, str], ...]


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


def bind_reference_identity(current_candidate: dict) -> ReferenceIdentity:
    """Freeze used execution fields/presence; raise IdentityError without file I/O."""
    fields = _execution_identity(current_candidate)
    return ReferenceIdentity(tuple((field, str(value)) for field, value in fields))


def _check_identity(payload: bytes, path: str, current: tuple[tuple[str, str], ...],
                    pin: A.PinResult | None = None) -> IdentityCheck:
    try:
        retained = _descriptor(payload, path)
    except (IdentityError, UnicodeError, S.SexpError, K.SchemaError,
            D.DossierError, RecursionError, ValueError, OSError) as exc:
        return IdentityCheck("refused", f"cannot use retained identity: {exc}", pin)
    if retained != current:
        return IdentityCheck("stale", "retained execution identity differs from current candidate", pin)
    return IdentityCheck("matched", "retained execution identity matches; qualification pending",
                         pin, retained)


def check_reference_identity_bytes(payload: bytes, *, path: str,
                                   context: ReferenceIdentity) -> IdentityCheck:
    """Bind immutable descriptor bytes to a context frozen before authentication.

    This pure consumer never reads an artifact or authenticates a pin. The caller
    supplies the exact authenticated snapshot and owns parent schema/graph checks.
    Descriptive candidate metadata remains outside this finite execution identity.
    """
    if (type(context) is not ReferenceIdentity or not isinstance(path, str) or
            not is_canonical_path(path)):
        return IdentityCheck("refused", "expected frozen identity context and canonical path")
    fields = context.fields
    if (type(fields) is not tuple or not len(REQUIRED_FIELDS) <= len(fields) <=
            len(REQUIRED_FIELDS) + len(OPTIONAL_FIELDS) or
            any(type(pair) is not tuple or len(pair) != 2 or
                any(type(value) is not str for value in pair) for pair in fields)):
        return IdentityCheck("refused", "invalid frozen identity fields")
    try:
        if _execution_identity(dict(fields)) != fields:
            raise IdentityError("noncanonical frozen identity fields")
    except IdentityError as exc:
        return IdentityCheck("refused", str(exc))
    return _check_identity(payload, path, fields)


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
    return _check_identity(snapshot.data, record["path"], current, pin)


def encode_reference_identity(context: ReferenceIdentity, *, profile: str,
                              retrieved: str, work_dir: str, host: dict,
                              path: str) -> bytes:
    """Emit one bounded selected descriptor, never a parent catalogue or artifact.

    Metadata describes this descriptor, not execution attestation. Freeze explicit
    metadata and the canonical execution fields before serialization/schema I/O.
    Descriptor value text totals at most 65536 characters; encoded output is at
    most 65536 bytes. The diagnostic path has a separate 65536-character bound.
    Caller allocation, escaping and parsed objects are separate RAM costs.
    IdentityError refuses invalid/unverifiable output. No partial bytes escape.
    """
    if type(context) is not ReferenceIdentity or type(context.fields) is not tuple:
        raise IdentityError("expected a frozen reference identity")
    fields = context.fields
    if (not len(REQUIRED_FIELDS) <= len(fields) <=
            len(REQUIRED_FIELDS) + len(OPTIONAL_FIELDS) or
            any(type(pair) is not tuple or len(pair) != 2 or
                any(type(value) is not str for value in pair) for pair in fields)):
        raise IdentityError("invalid descriptor execution fields")
    if any(key not in REQUIRED_FIELDS + OPTIONAL_FIELDS for key, _ in fields):
        raise IdentityError("unknown descriptor execution field")
    if (type(host) is not dict or not 4 <= len(host) <= 5 or
            any(type(key) is not str for key in host) or
            not {"os", "kernel", "arch", "cxx"} <= set(host) <=
            {"os", "kernel", "arch", "cxx", "note"}):
        raise IdentityError("expected explicit bounded descriptor host metadata")
    metadata = dict(profile=profile, retrieved=retrieved, work_dir=work_dir,
                    host=dict(host))
    required_text = (profile, retrieved, work_dir,
                     *(metadata["host"][key] for key in ("os", "kernel", "arch", "cxx")))
    if any(type(value) is not str or not value for value in required_text):
        raise IdentityError("descriptor metadata requires nonempty plain strings")
    note = metadata["host"].get("note", "")
    if type(note) is not str:
        raise IdentityError("descriptor host note requires a plain string")
    text = (*required_text, note, *(value for _, value in fields))
    if sum(len(value) for value in text) > IDENTITY_BYTES:
        raise IdentityError("descriptor input text exceeds 65536 characters")
    if (type(path) is not str or not 1 <= len(path) <= IDENTITY_BYTES or
            not is_canonical_path(path) or not is_canonical_path(work_dir)):
        raise IdentityError("descriptor paths must be canonical and repository-relative")
    if bind_reference_identity(dict(fields)) != context:
        raise IdentityError("noncanonical descriptor execution fields")
    selected = dict(fields)
    selected.update(role="selected execution identity", status="retained descriptor",
                    lineage="unexamined; no ancestry or independence credit")
    document = dict(metadata, candidate=[selected])
    try:
        payload = R.render_forms([D.references_to_form(document)]).encode("utf-8")
    except (UnicodeError, D.DossierError, ValueError, TypeError, RecursionError) as exc:
        raise IdentityError(f"cannot encode descriptor: {exc}") from exc
    if not 1 <= len(payload) <= IDENTITY_BYTES:
        raise IdentityError("encoded descriptor exceeds 65536 bytes")
    checked = check_reference_identity_bytes(payload, path=path, context=context)
    if checked.disposition != "matched":
        raise IdentityError("emitted descriptor cannot bind: " + checked.reason)
    return payload
