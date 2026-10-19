#!/usr/bin/env python3
"""Authenticate and bind one declared first-method manifest, never its leaves.

Caller owns raw parent schema/scoped graph validation and trusted runtime root.
A matched result authenticates only the manifest snapshot and binds declarations;
leaf currentness, disguised nesting, aggregate budgets and qualification remain
separate requirements. No process, binary cache or child file is accessed here.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import experiment_artifacts as A
import matched_gpr_artifacts as F
from matched_gpr_execution import InputBinding
import matched_gpr_relations as R


@dataclass(frozen=True)
class ManifestPlan:
    relations: R.RelationPlan
    manifest_input_id: str
    inputs: tuple[InputBinding, ...]  # nine principals plus distinct declared leaves
    child_input_ids: tuple[str, ...]


@dataclass(frozen=True)
class ManifestCheck:
    disposition: str  # matched / stale / unavailable / refused / unsupported
    reason: str
    pin: A.PinResult | None = None
    plan: ManifestPlan | None = None


@dataclass(frozen=True)
class _Context:
    relations: R.RelationPlan
    manifest: InputBinding
    principals: tuple[InputBinding, ...]
    output_paths: frozenset[str]


class ManifestError(ValueError):
    """The flat declared file identities cannot be bound consistently."""


def _require(condition: bool, reason: str):
    if not condition:
        raise ManifestError(reason)


def _context(experiment: dict, relations: R.RelationPlan) -> _Context:
    execution = relations.execution
    principals = (*execution.common_inputs, execution.baseline_expectation, execution.control_expectation)
    manifest = next(item for item in execution.common_inputs if item.role == "dependency-manifest")
    # The public execution binder already validated exactly twelve observation
    # identities/paths before copying these used immutable strings. Freeze before I/O.
    outputs = frozenset(record["path"] for record in experiment["verification"]["observation"])
    return _Context(relations, manifest, principals, outputs)


def _bind(context: _Context, document: dict) -> ManifestPlan:
    # The public bounded codec established 1..64 unique, non-self/nested-role
    # children before this closure index; it alone owns raw schema and mapping.
    by_id = {item.input_id: item for item in context.principals}
    by_path = {item.path: item.input_id for item in context.principals}
    children = []
    for record in document["input"]:
        child = InputBinding(record["role"], record["id"], record["path"], record["sha256"])
        _require(child.path not in context.output_paths, "manifest child aliases a run output")
        if child.input_id in by_id:
            _require(child == by_id[child.input_id], "manifest child conflicts with principal identity")
        else:
            _require(child.path not in by_path, "manifest path has another input identity")
            by_id[child.input_id] = child
            by_path[child.path] = child.input_id
        children.append(child.input_id)
    return ManifestPlan(context.relations, context.manifest.input_id,
                        tuple(by_id[rid] for rid in sorted(by_id)), tuple(sorted(children)))


def read_dependency_manifest(root: Path, *, experiment: dict, current_candidate: dict,
                             max_read_bytes: int = F.DOCUMENT_BYTES) -> ManifestCheck:
    """Read one manifest within an inclusive allowance, at most the document cap.

    Invalid limits refuse before binding or I/O. Zero permits no payload bytes.
    A caller sharing a larger budget must reserve this allowance before the call;
    a failed finding does not report every possible partial read.
    """
    if type(max_read_bytes) is not int or not 0 <= max_read_bytes <= F.DOCUMENT_BYTES:
        return ManifestCheck("refused", "invalid manifest read allowance")
    relations = R.bind_relations(experiment, current_candidate)
    if relations.disposition != "matched":
        return ManifestCheck(relations.disposition, "relations: " + relations.reason)
    try:
        context = _context(experiment, relations.plan)
    except (KeyError, TypeError, ValueError, StopIteration) as exc:
        return ManifestCheck("refused", f"malformed selected context: {type(exc).__name__}")
    manifest = context.manifest
    record = dict(id=manifest.input_id, role=manifest.role, path=manifest.path, sha256=manifest.sha256)
    snapshot = A.read_snapshot(root, "input", record, max_bytes=max_read_bytes)
    pin = snapshot.pin
    if pin.disposition != "matched":
        disposition = "stale" if pin.disposition == "mismatch" else pin.disposition
        return ManifestCheck(disposition, pin.reason, pin)
    try:
        document = F.parse_dependencies(snapshot.data, path=manifest.path)
        plan = _bind(context, document)
    except OSError as exc:
        return ManifestCheck("unavailable", f"manifest schema unavailable: {exc}", pin)
    except (F.ArtifactError, ManifestError, KeyError, TypeError, ValueError) as exc:
        return ManifestCheck("refused", str(exc), pin)
    return ManifestCheck("matched", "manifest binds; leaf currentness/complete closure/qualification pending", pin, plan)
