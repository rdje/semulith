#!/usr/bin/env python3
"""Authenticate the declared method file set under one read/snapshot budget.

Caller owns raw parent/schema/scoped validation and the public manifest check.
These are read-time file facts, not closure adequacy, source/program relationships,
process execution, comparison, cross-file atomic currentness or qualification.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import re

import experiment_artifacts as A
from experiment_verification import is_canonical_path
import matched_gpr_artifacts as F
import matched_gpr_comparison as C
import matched_gpr_execution as E
import matched_gpr_identity as I
import matched_gpr_image as G
import matched_gpr_leaf as L
import matched_gpr_manifest as M

MAX_READ_BYTES = 128 * 1024 * 1024
MAX_SNAPSHOT_BYTES = 16 * 1024 * 1024


@dataclass(frozen=True)
class FileFact:
    record_kind: str
    record_id: str
    role: str
    path: str
    pin: A.PinResult
    data: bytes | None = None
    classification: str | None = None  # Only declared children; not source validity.


@dataclass(frozen=True)
class FileSetCheck:
    disposition: str  # matched / stale / unavailable / refused / unsupported
    reason: str
    files: tuple[FileFact, ...] = ()
    manifest_pin: A.PinResult | None = None
    plan: M.ManifestPlan | None = None  # Only after the complete declared set matches.
    authenticated_bytes: int = 0
    charged_read_bytes: int = 0  # Conservative upper bound after a failed reader call.
    retained_bytes: int = 0


@dataclass(frozen=True)
class _Request:
    kind: str
    record_id: str
    role: str
    path: str
    sha256: str
    byte_size: int | None
    limit: int
    retain: bool
    inspect: bool

    def record(self) -> dict:
        result = dict(id=self.record_id, role=self.role, path=self.path, sha256=self.sha256)
        if self.kind == "observation":
            result["byte_size"] = self.byte_size
        return result


class FileSetError(ValueError):
    """The finite context or budget cannot safely supply this declared set."""


def _require(condition: bool, reason: str):
    if not condition:
        raise FileSetError(reason)


def _identity(record_id, role, path, sha256):
    _require(all(isinstance(value, str) and bool(value) for value in (record_id, role, path, sha256)),
             "file binding requires nonempty strings")
    _require(is_canonical_path(path), "file binding requires a canonical project path")
    _require(re.fullmatch(r"[0-9a-f]{64}", sha256) is not None, "invalid declared file digest")


def _requests(manifest: M.ManifestCheck, observations, *,
              retain_source_image: bool = False) -> tuple[_Request, tuple[_Request, ...]]:
    plan, pin = manifest.plan, manifest.pin
    _require(isinstance(plan, M.ManifestPlan) and isinstance(pin, A.PinResult),
             "expected an authenticated manifest plan and pin")
    _require(isinstance(plan.child_input_ids, tuple) and 1 <= len(plan.child_input_ids) <= F.MANIFEST_INPUTS and
             isinstance(plan.inputs, tuple) and 9 <= len(plan.inputs) <= 9 + F.MANIFEST_INPUTS,
             "manifest child/union counts outside the method envelope")
    _require(isinstance(observations, (list, tuple)) and len(observations) == 12,
             "expected exactly twelve observation records")
    execution = plan.relations.execution
    _require(isinstance(execution.common_inputs, tuple) and len(execution.common_inputs) == 7 and
             isinstance(execution.runs, tuple) and len(execution.runs) == 3,
             "principal/run counts outside the method envelope")
    children = plan.child_input_ids
    _require(all(isinstance(value, str) and bool(value) for value in children) and
             len(set(children)) == len(children), "invalid or duplicated child identities")
    principals = (*execution.common_inputs, execution.baseline_expectation, execution.control_expectation)
    _require(all(isinstance(item, E.InputBinding) for item in (*plan.inputs, *principals)),
             "expected immutable input bindings")
    _require({item.role for item in execution.common_inputs} == set(E.COMMON_ROLES) and
             execution.baseline_expectation.role == execution.control_expectation.role == "expectation",
             "principal roles differ from the method")
    principal_ids = {item.input_id for item in principals}
    _require(len(principal_ids) == 9, "duplicated principal identities")
    for item in plan.inputs:
        _identity(item.input_id, item.role, item.path, item.sha256)
    by_id = {item.input_id: item for item in plan.inputs}
    _require(len(by_id) == len(plan.inputs) and len({item.path for item in plan.inputs}) == len(plan.inputs),
             "duplicated union input identity or path")
    _require(set(by_id) == principal_ids | set(children), "union differs from principals and children")
    _require(all(by_id.get(item.input_id) == item for item in principals), "principal identity conflicts with union")
    selected = by_id.get(plan.manifest_input_id)
    _require(selected is not None and selected.role == "dependency-manifest" and
             selected.input_id not in children and
             all(item.role != "dependency-manifest" for item in plan.inputs if item != selected),
             "invalid self or nested manifest selection")
    _require(pin.disposition == "matched" and
             (pin.record_kind, pin.record_id, pin.path, pin.sha256) ==
             ("input", selected.input_id, selected.path, selected.sha256) and
             type(pin.byte_size) is int and 1 <= pin.byte_size <= F.DOCUMENT_BYTES,
             "manifest pin does not match its selected bounded identity")
    retained_roles = {"reference-identity", "expectation"}
    if retain_source_image:
        retained_roles.update({"guest-source", "guest-image"})
    requests = []
    for item in plan.inputs:
        retain = item.input_id in principal_ids and item.role in retained_roles
        limit = (I.IDENTITY_BYTES if item.role == "reference-identity" and retain else
                 C.EXPECTATION_BYTES if item.role == "expectation" and retain else
                 G.SOURCE_BYTES if item.role == "guest-source" and retain else
                 G.IMAGE_BYTES if item.role == "guest-image" and retain else L.LEAF_BYTES)
        requests.append(_Request("input", item.input_id, item.role, item.path, item.sha256,
                                 None, limit, retain, item.input_id in children))
    expected = []
    for run in execution.runs:
        _require(len(run.observations) == 4 and {role for role, _ in run.observations} == set(E.OUTPUT_ROLES),
                 "run output roles differ from the method")
        expected.extend((record_id, role) for role, record_id in run.observations)
    _require(len({record_id for record_id, _ in expected}) == 12, "duplicated selected observation identity")
    output_ids, output_paths = set(), set()
    for record in observations:
        _require(isinstance(record, dict), "expected observation dictionaries")
        record_id, role, path, digest = (record.get(key) for key in ("id", "role", "path", "sha256"))
        _identity(record_id, role, path, digest)
        _require((record_id, role) in expected, "observation identity/role not selected by a run")
        _require(record_id not in output_ids and path not in output_paths, "duplicated observation identity or path")
        output_ids.add(record_id); output_paths.add(path)
        limit = C.TRACE_BYTES if role == "raw-gpr" else F.DOCUMENT_BYTES
        size = record.get("byte_size")
        _require(type(size) is int and 0 <= size <= limit, "observation size outside its role bound")
        requests.append(_Request("observation", record_id, role, path, digest, size, limit, True, False))
    _require(not output_paths.intersection(item.path for item in plan.inputs), "input aliases an observation path")
    seed = next(item for item in requests if item.kind == "input" and item.record_id == selected.input_id)
    remaining = [item for item in requests if item != seed]
    # Transient child payloads are released before retained comparison inputs accumulate.
    remaining.sort(key=lambda item: (2 if item.retain else 0 if item.inspect else 1,
                                     item.kind, item.record_id))
    return seed, tuple(remaining)


def read_declared_files(root: Path, *, manifest: M.ManifestCheck, observations,
                        max_read_bytes: int = MAX_READ_BYTES,
                        max_snapshot_bytes: int = MAX_SNAPSHOT_BYTES,
                        retain_source_image: bool = False) -> FileSetCheck:
    """Read one complete declared set once, including the earlier manifest charge.

    Both limits must cover the known manifest seed, including its earlier snapshot
    peak. Released seed bytes leave current snapshot room available. Limits include
    transient payload while it exists; parsed objects/chunks/copies add RAM. A failure
    ends the batch, drops all payloads and cannot retry inside a reset budget.
    Later path changes require another evaluation; these are individual read facts.

    Opt-in source/image retention uses the builder's 1 MiB/64 KiB caps and reserves
    another 64 KiB inside the snapshot limit for later reconstruction. This unused
    room is deducted before new reads, also constraining the earlier manifest peak
    and transient payloads. retained_bytes excludes it. No reconstruction occurs
    here; empty authenticated bytes are allowed and need separate content checks.
    """
    if type(retain_source_image) is not bool:
        return FileSetCheck("refused", "source/image retention requires a plain boolean")
    if (type(max_read_bytes) is not int or not 0 <= max_read_bytes <= MAX_READ_BYTES or
            type(max_snapshot_bytes) is not int or not 0 <= max_snapshot_bytes <= MAX_SNAPSHOT_BYTES):
        return FileSetCheck("refused", "invalid aggregate read/snapshot byte limits")
    if not isinstance(manifest, M.ManifestCheck):
        return FileSetCheck("refused", "expected the public manifest check")
    if (not isinstance(manifest.reason, str) or
            (manifest.pin is not None and not isinstance(manifest.pin, A.PinResult))):
        return FileSetCheck("refused", "malformed manifest finding")
    if manifest.disposition != "matched":
        if manifest.disposition not in {"stale", "unavailable", "refused", "unsupported"}:
            return FileSetCheck("refused", "unknown manifest disposition")
        return FileSetCheck(manifest.disposition, manifest.reason, manifest_pin=manifest.pin)
    try:
        seed, requests = _requests(manifest, observations, retain_source_image=retain_source_image)
        reserve = G.IMAGE_BYTES if retain_source_image else 0
        _require(reserve <= max_snapshot_bytes, "snapshot budget below source/image rebuild reservation")
        max_snapshot_bytes -= reserve
        _require(manifest.pin.byte_size <= max_read_bytes, "read budget below the authenticated manifest seed")
        _require(manifest.pin.byte_size <= max_snapshot_bytes, "snapshot budget below the authenticated manifest seed")
    except (FileSetError, AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
        return FileSetCheck("refused", f"cannot bind declared file set: {exc}", manifest_pin=manifest.pin)
    facts = [FileFact(seed.kind, seed.record_id, seed.role, seed.path, manifest.pin)]
    authenticated = charged = manifest.pin.byte_size
    retained = 0

    def finish(disposition: str, reason: str) -> FileSetCheck:
        files = tuple(facts if disposition == "matched" else [replace(item, data=None) for item in facts])
        return FileSetCheck(disposition, reason, files, manifest.pin,
                            manifest.plan if disposition == "matched" else None,
                            authenticated, charged, retained if disposition == "matched" else 0)

    for request in requests:
        snapshot_needed = request.retain or request.inspect
        cap = min(request.limit, max_read_bytes - charged)
        if snapshot_needed:
            cap = min(cap, max_snapshot_bytes - retained)
        record = request.record()
        if snapshot_needed:
            snapshot = A.read_snapshot(root, request.kind, record, max_bytes=cap)
            pin, data = snapshot.pin, snapshot.data
        else:
            pin = A.read_bounded_pin(root, request.kind, record, max_bytes=cap)
            data = None
        fact = FileFact(request.kind, request.record_id, request.role, request.path, pin)
        facts.append(fact)
        if pin.disposition != "matched":
            charged += cap  # Partial consumption is not exposed by every reader failure.
            disposition = "stale" if pin.disposition == "mismatch" else pin.disposition
            if disposition not in {"stale", "unavailable", "refused"}:
                disposition = "refused"
            return finish(disposition, pin.reason)
        if (type(pin.byte_size) is not int or not 0 <= pin.byte_size <= cap or
                (pin.record_kind, pin.record_id, pin.path, pin.sha256) !=
                (request.kind, request.record_id, request.path, request.sha256) or
                (request.kind == "observation" and pin.byte_size != request.byte_size) or
                (snapshot_needed and (type(data) is not bytes or len(data) != pin.byte_size))):
            charged += cap
            return finish("refused", "inconsistent authenticated file snapshot/metadata")
        authenticated += pin.byte_size
        charged += pin.byte_size
        if request.inspect:
            try:
                classification = "manifest" if F.is_dependencies_document(data, path=request.path) else "non-manifest"
            except (F.ArtifactToolError, OSError) as exc:
                return finish("unavailable", str(exc))
            except F.ArtifactError as exc:
                return finish("refused", str(exc))
            fact = replace(fact, classification=classification)
            facts[-1] = fact
            if classification == "manifest":
                return finish("refused", "declared child contains a nested dependencies document")
        if request.retain:
            retained += len(data)
            facts[-1] = replace(fact, data=data)
        # Do not carry a transient snapshot into the next iteration's read.
        data = None
        if snapshot_needed:
            snapshot = None
    return finish("matched", "declared files authenticated; closure adequacy/method qualification pending")
