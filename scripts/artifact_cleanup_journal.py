#!/usr/bin/env python3
"""Bounded cleanup-attempt records. This module never unlinks a cache."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import asdict, dataclass, replace
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

import artifact_cleanup as A

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
OBJECT = "scripts/artifact_cleanup_journal.py"
NAME = "attempt.jsonl"
FORMAT = "artifact-cleanup-journal-v1"
JOURNAL_BYTES = 16 * 1024 * 1024
RECORD_BYTES = 32768
EVENT_BYTES = 64
STAGES = frozenset({"preflight", "revalidate", "unlink", "postcheck", "finalize", "interrupt", "verified"})

USAGE = """# ANCHOR: usage
### Read cleanup-attempt records

The journal module reserves one `attempt.jsonl` beside a published `plan.json`.
Its writer API records intent and caller-reported unlink returns; it performs
no cache operation. Guarded deletion and the host-bound operator CLI remain
pending. A fresh attempt can never overwrite or resume an existing journal.

Each record is one canonical JSON line. A begin record binds the canonical
plan digest, candidate count, current recorder and actor source identities.
Candidate indices follow the plan's sorted list. The allowed sequence is:

```text
begin → intent(0) → removed(0) → intent(1) → removed(1) → finish
```

Only a finish claiming `complete` after all recorded returns and a `verified`
stage can produce `recorded-complete`. Failed/interrupted attempts retain
their stage and bounded error. A valid prefix without a finish is incomplete;
a durable intent without a recorded return stays unresolved. A torn final
line is retained as a byte count/digest, never interpreted as success.

Inspect a saved attempt from the repository root:

```sh
python3 -B scripts/artifact_cleanup_journal.py --workdir target/artifact-cleanup/review
```

The metadata writer/reader has26 tests in normal and optimized Python plus ten
targeted guard omissions per mode,22 journal outcomes in the focused gate:

```sh
python3 -B scripts/probe_artifact_cleanup_journal.py
```

Exit0 means inspection completed, including an incomplete recorded attempt;
exit2 means the input or read was refused/unavailable. These are recorded
observations, not evidence of current absence or independent actor attestation.
Inspection does not invoke Git, execute a producer or touch a cache. It can
read historical source identities after the current recorder has changed.

The writer exclusively creates a same-volume regular file and validates the
root, parent, file and saved plan before every append. It synchronizes the
plan and ancestor directories before yielding a writer, then flushes each
complete frame before reporting it accepted. Darwin also requires
`F_FULLFSYNC`; missing or failed barriers refuse further use. See
[Python's fsync interface](https://docs.python.org/3.14/library/os.html#os.fsync)
and [Apple's write-order contract](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/fsync.2.html).
These calls are tested in owned fixtures; hardware power failure is not tested.
Quiescent ownership remains a caller precondition, not a filesystem transaction.

Journals fit16MiB, frames32KiB and at most two events per candidate plus begin/
finish; plans retain their separate16MiB bound. Each recorder/actor snapshot
fits1MiB. Errors fit2KiB UTF-8. Reader memory and hardware durability are not
attested. A failed/partial write poisons that writer; retain its bytes and
inspect the prefix rather than appending another result to damaged framing.
# ANCHOR_END: usage
"""


def need(condition, reason):
    A.need(condition, "journal: " + reason)


def bound_root(root: Path) -> Path:
    need(ROOT == A.ROOT, "recorder/planner roots differ")
    return A.runtime_root(root)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encode(record: dict) -> bytes:
    try:
        raw = (json.dumps(record, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")
    except (TypeError, ValueError, RecursionError) as error:
        raise A.CleanupError("refused", "journal: unencodable record") from error
    need(len(raw) <= RECORD_BYTES, "frame byte bound")
    return raw


def fields(value, names):
    need(type(value) is dict and set(value) == set(names.split()), "record fields differ")


def source(value) -> A.Source:
    fields(value, "object byte_size sha256")
    name = A.relative(value["object"])
    need(name.startswith("scripts/") and name.endswith(".py"), "source object outside script namespace")
    need(type(value["byte_size"]) is int and 0 < value["byte_size"] <= A.SOURCE_BYTES,
         "source byte bound")
    need(type(value["sha256"]) is str and re.fullmatch("[0-9a-f]{64}", value["sha256"]), "source digest")
    return A.Source(**value)


@dataclass(frozen=True)
class Failure:
    kind: str
    errno: int | None
    detail: str


def failure(value) -> Failure:
    fields(value, "kind errno detail")
    need(type(value["kind"]) is str and re.fullmatch("[A-Za-z_][A-Za-z0-9_.]{0,127}", value["kind"]),
         "failure kind")
    need(value["errno"] is None or type(value["errno"]) is int and -(2 ** 31) <= value["errno"] < 2 ** 31,
         "failure errno")
    need(type(value["detail"]) is str and len(value["detail"].encode("utf-8")) <= 2048, "failure detail bound")
    return Failure(**value)


@dataclass(frozen=True)
class Header:
    created_utc: str
    plan_sha256: str
    candidates: int
    recorder: A.Source
    actor: A.Source


@dataclass(frozen=True)
class Progress:
    header: Header | None = None
    removed: int = 0
    pending: int | None = None
    result: str | None = None
    stage: str | None = None
    failure: Failure | None = None


@dataclass(frozen=True)
class Inspection:
    progress: Progress
    tail_bytes: int
    tail_sha256: str | None


def transition(progress: Progress, record: dict, plan: A.Plan) -> Progress:
    need(progress.result is None, "record after terminal")
    need(type(record) is dict and type(record.get("kind")) is str, "record kind")
    kind = record["kind"]
    count = len(plan.candidates)
    if progress.header is None:
        fields(record, "kind format created_utc plan_sha256 candidates recorder actor")
        need(kind == "begin" and record["format"] == FORMAT, "begin format")
        stamp = record["created_utc"]
        need(type(stamp) is str and len(stamp) <= 64
             and datetime.datetime.fromisoformat(stamp).utcoffset() == datetime.timedelta(), "begin UTC time")
        need(type(record["candidates"]) is int and record["candidates"] == count, "candidate count binding")
        need(record["plan_sha256"] == digest(A.encode_plan(plan)), "plan digest binding")
        recorder, actor = source(record["recorder"]), source(record["actor"])
        need(recorder.object == OBJECT, "recorder object")
        return replace(progress, header=Header(stamp, record["plan_sha256"], count, recorder, actor))
    if kind in {"intent", "removed"}:
        fields(record, "kind index")
        index = record["index"]
        need(type(index) is int and 0 <= index < count, "candidate index")
        need(len(encode(record)) <= EVENT_BYTES, "event byte bound")
        if kind == "intent":
            need(progress.pending is None and index == progress.removed, "intent sequence")
            return replace(progress, pending=index)
        need(progress.pending == index, "return without matching intent")
        return replace(progress, removed=progress.removed + 1, pending=None)
    fields(record, "kind result stage failure")
    need(kind == "finish" and record["result"] in {"complete", "failed", "interrupted"}, "terminal result")
    need(type(record["stage"]) is str and record["stage"] in STAGES, "terminal stage")
    if record["result"] == "complete":
        need(progress.pending is None and progress.removed == count and record["stage"] == "verified"
             and record["failure"] is None, "incomplete terminal success")
        problem = None
    else:
        need(record["stage"] != "verified", "failure marked verified")
        problem = failure(record["failure"])
    return replace(progress, result=record["result"], stage=record["stage"], failure=problem)


def decode(raw: bytes, plan: A.Plan) -> Inspection:
    """Parse framed observations; do not infer a return from a partial tail."""
    need(type(raw) is bytes and len(raw) <= JOURNAL_BYTES, "journal byte bound")
    plan = A.decode_plan(A.encode_plan(plan))
    pieces = raw.split(b"\n")
    lines, tail = pieces[:-1], pieces[-1]
    need(len(lines) <= 2 * len(plan.candidates) + 2, "record count bound")
    need(len(tail) < RECORD_BYTES, "tail byte bound")
    progress = Progress()

    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "duplicate JSON field")
            result[key] = value
        return result

    try:
        for line in lines:
            need(0 < len(line) < RECORD_BYTES, "frame byte bound")
            value = json.loads(line.decode("ascii"), object_pairs_hook=pairs,
                               parse_constant=lambda unused: need(False, "nonfinite JSON value"))
            need(encode(value) == line + b"\n", "noncanonical frame")
            progress = transition(progress, value, plan)
        need(progress.result is None or not tail, "tail after terminal")
        return Inspection(progress, len(tail), digest(tail) if tail else None)
    except (TypeError, ValueError, KeyError, AttributeError, UnicodeError, RecursionError) as error:
        if isinstance(error, A.CleanupError): raise
        raise A.CleanupError("refused", "journal: malformed record " + type(error).__name__) from error


def _source(owned: A.OwnedRoot, name: str) -> A.Source:
    A.relative(name)
    need(name.startswith("scripts/") and name.endswith(".py"), "actor outside script namespace")
    parent, leaf = name.rsplit("/", 1)
    with owned.directory(parent) as directory:
        fact, _ = owned.snapshot(directory, leaf, name, A.SOURCE_BYTES)
    need(fact.byte_size > 0, "empty source")
    return A.Source(name, fact.byte_size, fact.sha256)


def _full_sync(descriptor: int):
    if sys.platform == "darwin":
        flag = getattr(fcntl, "F_FULLFSYNC", None)
        need(type(flag) is int, "F_FULLFSYNC unavailable")
        fcntl.fcntl(descriptor, flag)


def _flush(descriptor: int):
    os.fsync(descriptor)
    _full_sync(descriptor)


def _sync_namespace(owned: A.OwnedRoot, workdir: str):
    parts = workdir.split("/")
    for length in range(len(parts), 0, -1):
        with owned.directory("/".join(parts[:length])) as directory:
            os.fsync(directory)
    os.fsync(owned.fd)


def _fact_identity(fact: A.FileFact):
    return (fact.device, fact.inode, fact.mode, fact.links, fact.byte_size,
            fact.mtime_ns, fact.ctime_ns)


class Writer:
    """One open metadata attempt. It has no cache-unlink method."""

    def __init__(self, owned, parent, descriptor, plan, plan_fact):
        self._owned, self._parent, self._descriptor = owned, parent, descriptor
        self._plan, self._plan_fact = plan, plan_fact
        self._known = A._identity(os.fstat(descriptor))
        self._progress = Progress()
        self._bytes = 0
        self._broken = False
        self._closed = False

    @property
    def progress(self):
        return self._progress

    @contextmanager
    def _parent_guard(self):
        current = self._owned.path.lstat()
        opened = os.fstat(self._owned.fd)
        need(stat.S_ISDIR(current.st_mode) and (current.st_dev, current.st_ino)
             == (opened.st_dev, opened.st_ino), "root mapping changed")
        with self._owned.directory(self._plan.workdir) as fresh:
            now, held = os.fstat(fresh), os.fstat(self._parent)
            need((now.st_dev, now.st_ino) == (held.st_dev, held.st_ino), "workspace mapping changed")
            yield fresh

    def _file_guard(self, parent):
        opened = os.fstat(self._descriptor)
        located = os.stat(NAME, dir_fd=parent, follow_symlinks=False)
        need(A._identity(opened) == A._identity(located) == self._known
             and stat.S_ISREG(opened.st_mode) and opened.st_nlink == 1
             and opened.st_dev == self._owned.device, "journal file changed")
        current = os.stat("plan.json", dir_fd=parent, follow_symlinks=False)
        need(A._identity(current) == _fact_identity(self._plan_fact), "saved plan changed")

    def _append(self, record):
        need(not self._closed and not self._broken, "writer closed or poisoned")
        after = transition(self._progress, record, self._plan)
        raw = encode(record)
        need(self._bytes + len(raw) <= JOURNAL_BYTES, "journal byte bound")
        try:
            with self._parent_guard() as parent:
                self._file_guard(parent)
                cursor = 0
                while cursor < len(raw):
                    written = os.write(self._descriptor, raw[cursor:])
                    need(0 < written <= len(raw) - cursor, "write made no valid progress")
                    cursor += written
                _flush(self._descriptor)
                info = os.fstat(self._descriptor)
                need(info.st_size == self._bytes + len(raw) and info.st_nlink == 1,
                     "journal changed while appending")
                known = A._identity(info)
            self._known, self._bytes, self._progress = known, self._bytes + len(raw), after
        except BaseException:
            self._broken = True
            raise

    def intent(self, index: int):
        self._append(dict(kind="intent", index=index))

    def removed(self, index: int):
        self._append(dict(kind="removed", index=index))

    def finish(self, result: str, stage: str, problem: Failure | None = None):
        need(problem is None or type(problem) is Failure, "expected plain failure")
        self._append(dict(kind="finish", result=result, stage=stage,
                          failure=asdict(problem) if problem is not None else None))


@contextmanager
def start(root: Path, workdir: str, *, actor_object: str):
    """Reserve once, persist the plan/path/frame, then yield a metadata-only writer."""
    root = bound_root(root)
    A._selection(workdir, A.DEFAULT_SCOPES)
    with A.OwnedRoot(root) as owned, owned.directory(workdir) as parent:
        plan_fact, raw = owned.snapshot(parent, "plan.json", workdir + "/plan.json", A.PLAN_BYTES, payload=True)
        plan = A.decode_plan(raw)
        need(plan.workdir == workdir, "plan workspace differs")
        begin = dict(kind="begin", format=FORMAT,
                     created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                     plan_sha256=digest(A.encode_plan(plan)), candidates=len(plan.candidates),
                     recorder=asdict(_source(owned, OBJECT)), actor=asdict(_source(owned, actor_object)))
        need(len(encode(begin)) + 2 * len(plan.candidates) * EVENT_BYTES + RECORD_BYTES <= JOURNAL_BYTES,
             "planned journal exceeds bound")
        plan_fd = os.open("plan.json", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
        try:
            need(A._identity(os.fstat(plan_fd)) == _fact_identity(plan_fact), "plan changed before barrier")
            os.fsync(plan_fd)
            _sync_namespace(owned, workdir)
            _full_sync(plan_fd)
        finally:
            os.close(plan_fd)
        descriptor = os.open(NAME, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_APPEND,
                             0o600, dir_fd=parent)
        writer = None
        try:
            writer = Writer(owned, parent, descriptor, plan, plan_fact)
            writer._append(begin)
            _sync_namespace(owned, workdir)
            _flush(descriptor)
            yield writer
        finally:
            if writer is not None: writer._closed = True
            os.close(descriptor)


def inspect(root: Path, workdir: str) -> tuple[A.Plan, Inspection]:
    root = bound_root(root)
    plan = A.load_plan(root, workdir)
    with A.OwnedRoot(root) as owned, owned.directory(workdir) as parent:
        _, raw = owned.snapshot(parent, NAME, workdir + "/" + NAME, JOURNAL_BYTES, payload=True)
    return plan, decode(raw, plan)


def report(plan: A.Plan, finding: Inspection) -> dict:
    progress = finding.progress
    state = ("unestablished" if progress.header is None else
             "incomplete" if progress.result is None else "recorded-" + progress.result)
    return dict(recorded_state=state, binding_established=progress.header is not None,
                header=asdict(progress.header) if progress.header is not None else None,
                recorded_unlink_returns=progress.removed,
                recorded_paths=[f.path for f in plan.candidates[:progress.removed]],
                planned_bytes_for_recorded_returns=sum(f.byte_size for f in plan.candidates[:progress.removed]),
                unresolved_intent=progress.pending, stage=progress.stage,
                failure=asdict(progress.failure) if progress.failure is not None else None,
                tail_bytes=finding.tail_bytes, tail_sha256=finding.tail_sha256,
                claim_scope="recorded observations only; current state and actor not attested")


def main():
    parser = argparse.ArgumentParser(description="\n".join(USAGE.splitlines()[1:-1]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()
    try:
        plan, finding = inspect(ROOT, args.workdir)
        output = json.dumps(report(plan, finding), sort_keys=True, ensure_ascii=True)
        need(len(output.encode()) <= JOURNAL_BYTES, "report byte bound")
        print(output)
        return 0
    except (A.CleanupError, A.Boundary, OSError, ValueError, TypeError, UnicodeError, RecursionError) as error:
        reason = error.reason if isinstance(error, A.CleanupError) else type(error).__name__
        print(json.dumps(dict(disposition="refused", reason=reason), sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
