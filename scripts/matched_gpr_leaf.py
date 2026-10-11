#!/usr/bin/env python3
"""Inspect one declared dependency leaf, without whole-closure or method credit."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import experiment_artifacts as A
import matched_gpr_artifacts as F
import matched_gpr_manifest as M

LEAF_BYTES = 8 * 1024 * 1024


@dataclass(frozen=True)
class LeafCheck:
    disposition: str  # matched / stale / unavailable / refused
    reason: str
    pin: A.PinResult | None = None
    classification: str | None = None  # non-manifest / manifest; never source validation


class LeafError(ValueError):
    """A selected dependency cannot be safely inspected under this contract."""


def _require(condition: bool, reason: str):
    if not condition:
        raise LeafError(reason)


def _record(manifest: M.ManifestPlan, input_id: str) -> dict:
    _require(isinstance(manifest, M.ManifestPlan), "expected a bound manifest plan")
    _require(isinstance(input_id, str) and bool(input_id), "expected a nonempty child ID")
    _require(1 <= len(manifest.child_input_ids) <= F.MANIFEST_INPUTS and
             9 <= len(manifest.inputs) <= 9 + F.MANIFEST_INPUTS,
             "manifest child/union counts outside the method envelope")
    _require(manifest.child_input_ids.count(input_id) == 1,
             "selected child edge absent or duplicated")
    selected = tuple(item for item in manifest.inputs if item.input_id == input_id)
    _require(len(selected) == 1, "selected child binding absent or duplicated")
    binding = selected[0]
    _require(binding.input_id != manifest.manifest_input_id and binding.role != "dependency-manifest",
             "selected child is the manifest itself or declares a nested manifest role")
    record = dict(id=binding.input_id, role=binding.role, path=binding.path, sha256=binding.sha256)
    _require(all(isinstance(value, str) and bool(value) for value in record.values()),
             "malformed selected child binding")
    return record


def _classification(data: bytes, path: str) -> str:
    return "manifest" if F.is_dependencies_document(data, path=path) else "non-manifest"


def inspect_dependency_leaf(root: Path, *, manifest: M.ManifestPlan, input_id: str,
                            max_bytes: int = LEAF_BYTES) -> LeafCheck:
    """Authenticate and classify one selected child from a validated manifest plan.

    The caller first validates the raw parent/schema/scoped graph and obtains
    the plan through read_dependency_manifest. This helper releases its payload;
    the caller owns aggregate read/snapshot budgets and complete method evaluation.
    """
    if type(max_bytes) is not int or not 0 <= max_bytes <= LEAF_BYTES:
        return LeafCheck("refused", "dependency leaf byte limit must be an integer in 0..8MiB")
    try:
        record = _record(manifest, input_id)
    except LeafError as exc:
        return LeafCheck("refused", str(exc))
    except (AttributeError, IndexError, TypeError, ValueError) as exc:
        return LeafCheck("refused", f"malformed selected context: {type(exc).__name__}")
    snapshot = A.read_snapshot(root, "input", record, max_bytes=max_bytes)
    pin = snapshot.pin
    if pin.disposition != "matched":
        disposition = "stale" if pin.disposition == "mismatch" else pin.disposition
        return LeafCheck(disposition, pin.reason, pin)
    data = snapshot.data
    if type(data) is not bytes or len(data) > max_bytes or pin.byte_size != len(data):
        return LeafCheck("refused", "inconsistent authenticated leaf snapshot payload", pin)
    try:
        classification = _classification(data, record["path"])
    except (F.ArtifactToolError, OSError) as exc:
        return LeafCheck("unavailable", str(exc), pin)
    except F.ArtifactError as exc:
        return LeafCheck("refused", str(exc), pin)
    if classification == "manifest":
        return LeafCheck("refused", "dependency leaf declares a nested dependencies document", pin, classification)
    return LeafCheck("matched", "leaf authenticated; aggregate closure/method qualification pending", pin, classification)
