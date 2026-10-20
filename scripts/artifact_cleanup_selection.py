#!/usr/bin/env python3
"""Strict cohort selection: only recorded, captured generated outputs may be approved.

This module publishes a selection beside a plan. It exposes no deletion operation.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, fields
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import sys

import artifact_cleanup as A
import artifact_output_provenance as O

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
OBJECT = "scripts/artifact_cleanup_selection.py"
NAME = "selection.json"
FORMAT = "artifact-cleanup-selection-v1"
SELECTION_BYTES = 16 * 1024 * 1024
SOURCES = (OBJECT, "scripts/artifact_cleanup.py", "scripts/artifact_output_provenance.py")

USAGE = """# ANCHOR: usage
### Strict selection against the published ledger

A plan lists every cache-named untracked file by name and place. A name is not
ownership: a retained fixture or a smoke input shaped like a cache stays a
candidate in the plan. Selection closes that gap. It intersects a published
plan's candidates with the output-provenance ledger through the strict reader,
which approves a candidate only when a captured record (recorder, producer,
runner and census pins all current) matches the file's current identity.
Everything else is `unrecorded` and keeps its bytes. An absent ledger approves
nothing; a legacy row never satisfies strict selection.

```sh
python3 -B scripts/artifact_cleanup.py --plan --workdir target/artifact-cleanup/review
python3 -B scripts/artifact_cleanup_selection.py --select --workdir target/artifact-cleanup/review
python3 -B scripts/artifact_cleanup_selection.py --inspect --workdir target/artifact-cleanup/review
```

`--select` re-censuses the plan's scopes first and refuses a stale plan or a
changed tracked inventory, then exclusively creates `selection.json`: the plan
digest and time, tracked digest, ledger digest, the selector/planner/reader
source identities, and the sorted approved/unrecorded partition of the plan's
candidates with their byte totals. It never overwrites an existing selection.
`--inspect` decodes a saved selection against its plan, refuses any forged or
noncanonical record, and reports whether the pinned sources are still current.
Exit0 reports a selection; 1 a stale plan; 2 a refusal.

Selections fit16MiB. A selection grants no mutation by itself: guarded deletion
(ARTIFACT-CLEANUP.16) must bind the plan, this selection and the attempt
journal, revalidate every file immediately before unlink and require the host
census (.14). Historical plans without a selection remain readable and grant
no authority. Run the disposable-fixture controls:

```sh
python3 -B scripts/probe_artifact_cleanup_selection.py
```
# ANCHOR_END: usage
"""


def need(condition, reason, disposition="refused"):
    A.need(condition, "selection: " + reason, disposition)


def bound_root(root: Path) -> Path:
    need(ROOT == A.ROOT == O.ROOT, "selector/planner/reader roots differ")
    return A.runtime_root(root)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class Selection:
    format: str
    created_utc: str
    workdir: str
    plan_sha256: str
    plan_created_utc: str
    tracked_sha256: str
    ledger_sha256: str | None
    sources: tuple[O.Source, ...]
    approved: tuple[str, ...]
    unrecorded: tuple[str, ...]
    approved_bytes: int
    unrecorded_bytes: int


def decide(root: Path, plan: A.Plan) -> Selection:
    """Partition the plan's candidates by strict captured authority; write nothing."""
    root = bound_root(root)
    plan = A.decode_plan(A.encode_plan(plan))
    tracked = A.tracked_paths(root)
    need(digest(b"\0".join(path.encode() for path in sorted(tracked))) == plan.tracked_sha256,
         "tracked inventory differs from the plan", "stale")
    finding = A.check_plan(root, plan)
    need(finding.disposition == "matched", "plan is " + finding.disposition + ": " + finding.reason,
         "stale" if finding.disposition == "stale" else "refused")
    current = tuple(O.Fact(**asdict(item)) for item in plan.candidates)
    with A.OwnedRoot(root) as owned:
        sources = tuple(O._source(owned, name) for name in SOURCES)
        authority = O.authorize(owned, current, tracked_paths=tracked, require_captured=True)
    sizes = {item.path: item.byte_size for item in plan.candidates}
    approved = tuple(sorted(authority.approved))
    unrecorded = tuple(sorted(set(sizes) - authority.approved))
    return Selection(FORMAT, datetime.datetime.now(datetime.timezone.utc).isoformat(), plan.workdir,
                     digest(A.encode_plan(plan)), plan.created_utc, plan.tracked_sha256,
                     authority.ledger_sha256, sources, approved, unrecorded,
                     sum(sizes[path] for path in approved), sum(sizes[path] for path in unrecorded))


def encode(selection: Selection) -> bytes:
    need(type(selection) is Selection, "plain selection required")
    try:
        raw = (json.dumps(asdict(selection), sort_keys=True, separators=(",", ":"),
                          ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")
    except (TypeError, ValueError, RecursionError) as error:
        raise A.CleanupError("refused", "selection: unencodable record") from error
    need(len(raw) <= SELECTION_BYTES, "selection byte bound")
    return raw


def decode(raw: bytes, plan: A.Plan) -> Selection:
    """Decode a closed selection bound to exactly this plan; refuse any other shape."""
    need(type(raw) is bytes and 0 < len(raw) <= SELECTION_BYTES, "selection byte bound")
    plan = A.decode_plan(A.encode_plan(plan))

    def pairs(items):
        value = {}
        for name, item in items:
            need(name not in value, "duplicate JSON field")
            value[name] = item
        return value

    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                           parse_constant=lambda unused: need(False, "nonfinite JSON"))
        need(type(value) is dict and set(value) == {f.name for f in fields(Selection)}, "invalid Selection fields")
        need(value["format"] == FORMAT, "unsupported selection format")
        stamp = value["created_utc"]
        need(type(stamp) is str and len(stamp) <= 64
             and datetime.datetime.fromisoformat(stamp).utcoffset() == datetime.timedelta(), "UTC selection time")
        need(value["workdir"] == plan.workdir, "selection belongs to another workspace")
        need(value["plan_sha256"] == digest(A.encode_plan(plan)), "plan digest binding")
        need(value["plan_created_utc"] == plan.created_utc and value["tracked_sha256"] == plan.tracked_sha256,
             "plan time/inventory binding")
        ledger = value["ledger_sha256"]
        need(ledger is None or (type(ledger) is str and re.fullmatch("[0-9a-f]{64}", ledger)), "ledger digest")
        need(type(value["sources"]) is list and len(value["sources"]) == len(SOURCES), "source count")
        sources = tuple(O.source(row) for row in value["sources"])
        need(tuple(row.object for row in sources) == SOURCES, "source objects/order differ")
        candidates = {item.path: item.byte_size for item in plan.candidates}
        groups = {}
        for name in ("approved", "unrecorded"):
            paths = value[name]
            need(type(paths) is list and all(type(path) is str for path in paths)
                 and paths == sorted(paths) and len(paths) == len(set(paths)), "unsorted or repeated " + name)
            groups[name] = tuple(A.relative(path) for path in paths)
        need(not set(groups["approved"]) & set(groups["unrecorded"])
             and set(groups["approved"]) | set(groups["unrecorded"]) == set(candidates),
             "approved/unrecorded must partition the plan's candidates")
        for name in ("approved_bytes", "unrecorded_bytes"):
            need(type(value[name]) is int and value[name] == sum(candidates[path] for path in groups[name[:-6]]),
                 name + " differs from the plan")
        result = Selection(FORMAT, stamp, plan.workdir, value["plan_sha256"], plan.created_utc,
                           plan.tracked_sha256, ledger, sources, groups["approved"], groups["unrecorded"],
                           value["approved_bytes"], value["unrecorded_bytes"])
        need(encode(result) == raw, "noncanonical selection")
        return result
    except (TypeError, ValueError, KeyError, AttributeError, UnicodeError, RecursionError) as error:
        if isinstance(error, A.CleanupError):
            raise
        raise A.CleanupError("refused", "selection: malformed record " + type(error).__name__) from error


def publish(root: Path, selection: Selection):
    """Exclusively create the selection beside its still-identical plan; never overwrite."""
    root = bound_root(root)
    plan = A.load_plan(root, selection.workdir)
    raw = encode(decode(encode(selection), plan))
    try:
        with A.OwnedRoot(root) as owned, owned.directory(selection.workdir) as directory:
            saved, _ = owned.snapshot(directory, "plan.json", selection.workdir + "/plan.json", A.PLAN_BYTES, payload=True)
            need(saved.sha256 == selection.plan_sha256, "saved plan changed before publication", "stale")
            descriptor = os.open(NAME, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
                                 0o600, dir_fd=directory)
            try:
                cursor = 0
                while cursor < len(raw):
                    written = os.write(descriptor, raw[cursor:])
                    need(0 < written <= len(raw) - cursor, "selection write made no valid progress", "unavailable")
                    cursor += written
                O._flush(descriptor)
            finally:
                os.close(descriptor)
            os.fsync(directory)
    except A.Boundary as error:
        raise A.CleanupError("refused", "selection: unsafe workspace: " + error.reason) from error


def inspect(root: Path, workdir: str):
    """Decode the saved selection against its plan and say whether its pins are still current."""
    root = bound_root(root)
    plan = A.load_plan(root, workdir)
    try:
        with A.OwnedRoot(root) as owned, owned.directory(workdir) as directory:
            _, raw = owned.snapshot(directory, NAME, workdir + "/" + NAME, SELECTION_BYTES, payload=True)
            selection = decode(raw, plan)
            current = tuple(O._source(owned, name) for name in SOURCES)
    except A.Boundary as error:
        raise A.CleanupError("refused", "selection: unsafe workspace: " + error.reason) from error
    return plan, selection, selection.sources == current


def summary(chosen: Selection, **extra) -> dict:
    return dict(approved=len(chosen.approved), approved_bytes=chosen.approved_bytes,
                unrecorded=len(chosen.unrecorded), unrecorded_bytes=chosen.unrecorded_bytes,
                ledger_sha256=chosen.ledger_sha256, plan_sha256=chosen.plan_sha256, **extra)


def main():
    parser = argparse.ArgumentParser(description="\n".join(USAGE.splitlines()[1:-1]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--select", action="store_true")
    mode.add_argument("--inspect", action="store_true")
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()
    try:
        if args.select:
            selection = decide(ROOT, A.load_plan(ROOT, args.workdir))
            publish(ROOT, selection)
            report = summary(selection, disposition="selected", selection=args.workdir + "/" + NAME,
                             reason="strict selection published; no cache deletion")
        else:
            _, selection, current = inspect(ROOT, args.workdir)
            report = summary(selection, disposition="inspected", sources_current=current,
                             claim_scope="recorded selection only; no current authority or deletion")
    except A.CleanupError as error:
        report = dict(disposition=error.disposition, reason=error.reason)
    except A.Boundary as error:
        report = dict(disposition="refused", reason="unsafe source boundary: " + error.reason)
    except (O.ProvenanceError, UnicodeError, ValueError, RecursionError) as error:
        report = dict(disposition="refused", reason="invalid input: " + str(error))
    except OSError as error:
        report = dict(disposition="unavailable", reason="filesystem/Git operation: " + type(error).__name__)
    print(json.dumps(report, sort_keys=True))
    return 0 if report["disposition"] in {"selected", "inspected"} else 1 if report["disposition"] == "stale" else 2


if __name__ == "__main__":
    sys.exit(main())
