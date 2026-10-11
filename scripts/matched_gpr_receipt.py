#!/usr/bin/env python3
"""Authenticate and bind one retained Sail receipt to selected canonical records.

The caller owns raw parent-schema/graph validation and reference-identity checks.
This finite boundary never authenticates the other declared files, runs a process
or qualifies an experiment. Context dictionaries are already caller-owned; their
memory is outside the retained receipt's 64 KiB payload bound.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import experiment_artifacts as A
from experiment_verification import is_canonical_path
import matched_gpr_artifacts as F

RECEIPT_BYTES = 64 * 1024
MAX_INPUTS = 8
MAX_ARGV = 11
OUTPUT_ROLES = frozenset({"raw-gpr", "process-stdout", "process-stderr", "process-receipt"})


@dataclass(frozen=True)
class ReceiptFacts:
    run_id: str
    run_kind: str
    argv: tuple[str, ...]
    process_exit: int
    host: tuple[tuple[str, str], ...]
    tools: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class ReceiptCheck:
    disposition: str  # matched / stale / unavailable / refused; not process success
    reason: str
    pin: A.PinResult | None = None
    facts: ReceiptFacts | None = None


@dataclass(frozen=True)
class _Context:
    run_id: str
    run_kind: str
    argv: tuple[str, ...]
    process_exit: int
    candidate_id: str
    binary_sha256: str
    collector_id: str
    inputs: tuple[tuple[str, str], ...]
    outputs: tuple[tuple[str, str, str, int, str], ...]
    receipt: tuple[tuple[str, str | int], ...]


class BindingError(ValueError):
    """Invalid selected context; no artifact read is needed to refuse it."""


def _text(value, where: str, *, empty: bool = False) -> str:
    # Bound used context text before regex/path work. This request bound is
    # independent of receipt bytes and caller dictionary allocation.
    if not isinstance(value, str) or len(value) > RECEIPT_BYTES or (not empty and not value):
        raise BindingError(f"invalid {where}")
    return value


def _id(value, where: str) -> str:
    value = _text(value, where)
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9._:/-]*", value) is None:
        raise BindingError(f"invalid {where}")
    return value


def _digest(value, where: str) -> str:
    value = _text(value, where)
    if re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise BindingError(f"invalid {where}")
    return value


def _sequence(value, minimum: int, maximum: int, where: str):
    if type(value) not in (list, tuple) or not minimum <= len(value) <= maximum:
        raise BindingError(f"{where} requires {minimum}..{maximum} entries")
    return value


def _unique(values, where: str):
    if len(values) != len(set(values)):
        raise BindingError(f"duplicate {where}")


def _records(records, *, observation: bool):
    _sequence(records, 4 if observation else 1, 4 if observation else MAX_INPUTS,
              "observations" if observation else "inputs")
    copied = []
    for record in records:
        if not isinstance(record, dict):
            raise BindingError("expected a selected record dictionary")
        item = {field: _text(record.get(field), field) for field in ("role", "path")}
        item["id"] = _id(record.get("id"), "record id")
        item["sha256"] = _digest(record.get("sha256"), "record sha256")
        if not is_canonical_path(item["path"]):
            raise BindingError("noncanonical selected record path")
        if observation:
            size = record.get("byte_size")
            if type(size) is not int or size < 0:
                raise BindingError("invalid observation byte_size")
            item["byte_size"] = size
        copied.append(item)
    _unique([item["id"] for item in copied], "selected record id")
    _unique([item["path"] for item in copied], "selected record path")
    return copied


def _context(run, inputs, observations, candidate) -> _Context:
    if not isinstance(run, dict) or not isinstance(candidate, dict):
        raise BindingError("expected canonical run/candidate dictionaries")
    run_id = _id(run.get("id"), "run id")
    kind = run.get("kind")
    if kind not in ("baseline", "repeat", "control"):
        raise BindingError("invalid run kind")
    argv = tuple(_text(arg, "argv entry", empty=True)
                 for arg in _sequence(run.get("argv"), 1, MAX_ARGV, "argv"))
    status = run.get("process_exit")
    if type(status) is not int:
        raise BindingError("invalid process_exit")
    candidate_id = _text(candidate.get("id"), "candidate id")
    if candidate_id != "sail-riscv":
        raise BindingError("this method requires candidate sail-riscv")
    binary_sha = _digest(candidate.get("binary_sha256"), "candidate binary_sha256")
    inputs = _records(inputs, observation=False)
    observations = _records(observations, observation=True)
    _unique([item["path"] for item in inputs + observations], "input/output path")
    for field, records, maximum in (("input_ids", inputs, MAX_INPUTS),
                                    ("observation_ids", observations, 4)):
        ids = tuple(_id(rid, field) for rid in _sequence(run.get(field), 1, maximum, field))
        _unique(ids, field)
        if set(ids) != {item["id"] for item in records}:
            raise BindingError(f"selected records differ from run {field}")
    if {item["role"] for item in observations} != OUTPUT_ROLES:
        raise BindingError("expected four distinct run output roles")
    collectors = [item["id"] for item in inputs if item["role"] == "collector"]
    if len(collectors) != 1:
        raise BindingError("expected one collector input")
    receipt = next(item for item in observations if item["role"] == "process-receipt")
    return _Context(run_id, kind, argv, status, candidate_id, binary_sha, collectors[0],
                    tuple(sorted((item["id"], item["sha256"]) for item in inputs)),
                    tuple(sorted((item["id"], item["role"], item["path"], item["byte_size"],
                                  item["sha256"]) for item in observations if item is not receipt)),
                    tuple(receipt.items()))


def read_run_receipt(root: Path, *, run: dict, inputs: list[dict],
                     observations: list[dict], current_candidate: dict) -> ReceiptCheck:
    """Bind one authenticated receipt, preserving coherent failed-process data.

    Context selection/parent graph and current reference identity are caller
    prerequisites. Exact eight principal roles, fixed invocation, producers,
    other-file authentication and aggregate method budgets remain separate.
    """
    try:
        context = _context(run, inputs, observations, current_candidate)
    except BindingError as exc:
        return ReceiptCheck("refused", str(exc))
    record = dict(context.receipt)
    snapshot = A.read_snapshot(root, "observation", record, max_bytes=RECEIPT_BYTES)
    pin = snapshot.pin
    if pin.disposition != "matched":
        disposition = "stale" if pin.disposition == "mismatch" else pin.disposition
        return ReceiptCheck(disposition, pin.reason, pin)
    try:
        doc = F.parse_capture(snapshot.data, path=record["path"])
    except F.ArtifactError as exc:
        return ReceiptCheck("refused", str(exc), pin)
    except OSError as exc:
        return ReceiptCheck("unavailable", f"receipt schema unavailable: {exc}", pin)
    for field, expected in (("run_id", context.run_id), ("run_kind", context.run_kind),
                            ("process_exit", context.process_exit),
                            ("reference_candidate_id", context.candidate_id),
                            ("reference_binary_sha256", context.binary_sha256),
                            ("collector_input_id", context.collector_id)):
        if doc[field] != expected:
            return ReceiptCheck("refused", f"receipt differs from canonical {field}", pin)
    if tuple(doc["argv"]) != context.argv:
        return ReceiptCheck("refused", "receipt differs from ordered canonical argv", pin)
    inventory = tuple(sorted((item["id"], item["sha256"]) for item in doc["input"]))
    if inventory != context.inputs:
        return ReceiptCheck("refused", "receipt differs from canonical input inventory", pin)
    outputs = tuple(sorted((item["id"], item["role"], item["path"], item["byte_size"], item["sha256"])
                           for item in doc["observation"]))
    if outputs != context.outputs:
        return ReceiptCheck("refused", "receipt differs from canonical output inventory", pin)
    facts = ReceiptFacts(doc["run_id"], doc["run_kind"], tuple(doc["argv"]), doc["process_exit"],
                         tuple(sorted(doc["host"].items())),
                         tuple((tool["id"], tool["version"]) for tool in doc["tool"]))
    return ReceiptCheck("matched", "authenticated receipt binds; process/method credit pending", pin, facts)
