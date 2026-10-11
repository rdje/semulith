#!/usr/bin/env python3
"""Bounded syntax/identity checks for prospective Sail GPR artifact bytes.

Call with bytes from the authenticated snapshot reader. This module never opens
an artifact, authenticates a pin, executes a producer or grants method credit.
Schema loading is project-tool I/O; dossier_sexp alone owns the data mapping.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import check_sexp_schema as K
import dossier_sexp as D
from experiment_verification import is_canonical_path
import records_sexp as R
import sexp as S

ROOT = Path(__file__).resolve().parent.parent
DOCUMENT_BYTES = 64 * 1024
MANIFEST_INPUTS = 64
_OUTPUT_ROLES = frozenset({"raw-gpr", "process-stdout", "process-stderr"})


class ArtifactError(ValueError):
    """No partial document escapes a shape or identity refusal."""


@lru_cache(maxsize=2)
def _schema(family: str):
    name = {"dependencies": "matched-gpr-dependencies", "capture": "sail-gpr-capture"}[family]
    return K.load_schema(ROOT / f"schema/{name}.sexp")


def _path(value: str, where: str) -> None:
    if not isinstance(value, str) or not is_canonical_path(value):
        raise ArtifactError(f"{where}: noncanonical project path")


def _unique(records: list[dict], field: str, where: str) -> None:
    values = [record[field] for record in records]
    if len(set(values)) != len(values):
        raise ArtifactError(f"{where}: duplicate {field}")


def _document(payload: bytes, family: str, path: str) -> dict:
    # Refuse before decoding/parsing. These are payload bounds, not total RAM caps.
    if type(payload) is not bytes:
        raise ArtifactError(f"{family}: expected immutable snapshot bytes")
    if not payload or len(payload) > DOCUMENT_BYTES:
        raise ArtifactError(f"{family}: payload must contain 1..{DOCUMENT_BYTES} bytes")
    _path(path, f"{family} location")
    try:
        text = payload.decode("utf-8")
        constructs, operators = _schema(family)
        errors = K.validate_text(text, constructs, operators, path)
        if errors:
            raise ArtifactError(f"{family} shape: {errors[0]}")
        forms = [form for form in S.parse(text, path) if form[0] != "comment"]
        if len(forms) != 1 or forms[0][0] != family:
            raise ArtifactError(f"{family}: expected exactly one {family} document")
        mapper = D.dependencies_to_doc if family == "dependencies" else D.capture_to_doc
        return mapper(forms[0])
    except (UnicodeError, S.SexpError, K.SchemaError, D.DossierError,
            RecursionError, ValueError) as exc:
        if isinstance(exc, ArtifactError):
            raise
        raise ArtifactError(f"{family}: cannot decode/validate document: {exc}") from exc


def parse_dependencies(payload: bytes, *, path: str) -> dict:
    """Validate one manifest; path is its canonical repository-relative location.

    Self/nesting checks are lexical identities. Pin authentication and discovery of
    disguised manifest content belong to closure evaluation, not syntax checking.
    """
    doc = _document(payload, "dependencies", path)
    inputs = doc["input"]
    if len(inputs) > MANIFEST_INPUTS:
        raise ArtifactError(f"dependencies: more than {MANIFEST_INPUTS} inputs")
    _unique(inputs, "id", "dependencies/input")
    _unique(inputs, "path", "dependencies/input")
    for item in inputs:
        _path(item["path"], "dependencies/input")
        if item["path"] == path:
            raise ArtifactError("dependencies: self reference")
        if item["role"] == "dependency-manifest":
            raise ArtifactError("dependencies: nested manifest role")
    return doc


def parse_capture(payload: bytes, *, path: str) -> dict:
    """Validate one receipt without asserting that the recorded process ran."""
    doc = _document(payload, "capture", path)
    for family in ("input", "observation", "tool"):
        _unique(doc[family], "id", f"capture/{family}")
    inputs = {item["id"] for item in doc["input"]}
    if doc["collector_input_id"] not in inputs:
        raise ArtifactError("capture: collector input is absent from inventory")
    observations = doc["observation"]
    _unique(observations, "path", "capture/observation")
    if len(observations) != 3 or {item["role"] for item in observations} != _OUTPUT_ROLES:
        raise ArtifactError("capture: exactly one trace, stdout and stderr output required")
    for item in observations:
        _path(item["path"], "capture/observation")
        if item["path"] == path:
            raise ArtifactError("capture: receipt cannot be its own output")
        if item["byte_size"] < 0:
            raise ArtifactError("capture: negative output byte_size")
    return doc


def _encode(doc: dict, family: str, path: str) -> bytes:
    """Writer convenience; the bounded parser judges the complete serialized result.

    The caller's in-memory dictionary/render allocation is not a resource budget.
    Unknown keys and lossy/wrong-type mappings refuse instead of being published.
    """
    try:
        mapper = D.dependencies_to_form if family == "dependencies" else D.capture_to_form
        payload = R.render_forms([mapper(doc)]).encode("utf-8")
        parser = parse_dependencies if family == "dependencies" else parse_capture
        if parser(payload, path=path) != doc:
            raise ArtifactError(f"{family}: mapping would lose or change data")
        return payload
    except (D.DossierError, R.RecordRefused, TypeError, UnicodeError,
            RecursionError, ValueError) as exc:
        if isinstance(exc, ArtifactError):
            raise
        raise ArtifactError(f"{family}: cannot encode document: {exc}") from exc


def encode_dependencies(doc: dict, *, path: str) -> bytes:
    return _encode(doc, "dependencies", path)


def encode_capture(doc: dict, *, path: str) -> bytes:
    return _encode(doc, "capture", path)
