#!/usr/bin/env python3
"""Closed records of changed outputs from two repository-owned Cargo producers.

This module records and publishes observations; it grants no deletion operation.
Plan selection against the published ledger is separate.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, fields
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import time
import unicodedata

ROOT = Path(__file__).resolve().parent.parent
OBJECT = "scripts/artifact_output_provenance.py"
WORKSPACE = "target/artifact-cleanup"
NAME = "output-provenance.json"
LOCK_NAME = "output-provenance.lock"
LEDGER = WORKSPACE + "/" + NAME
FORMAT = "artifact-output-provenance-v1"
CAPTURE_FORMAT = "artifact-output-provenance-v2"
SUPPORTING_OBJECTS = ("scripts/artifact_cargo.py", "scripts/artifact_cleanup.py")
MAX_BYTES = 16 * 1024 * 1024
MAX_RECORDS = 65536
MAX_RECORD_BYTES = 32768
SOURCE_BYTES = 1024 * 1024
FILE_BYTES = 512 * 1024 * 1024
MAX_ENTRIES = 4 * MAX_RECORDS
PRODUCERS = {
    "scripts/probe_c_engine.py": ("target/p4-system-12/c-engine-build", "c_engine::"),
    "scripts/probe_c_guest_image.py": ("target/p4-system-12/c-guest-image-build", "run_rv64gc::tests::"),
}
CACHE_NAMES = frozenset({"dep-graph.bin", "query-cache.bin", "work-products.bin"})

USAGE = """# ANCHOR: usage
### Output provenance before deletion readiness

Cache names, Cargo metadata and `cargo clean --dry-run` cannot establish that
each file was generated. An owned fixture's dry run lists an input inside a
profile directory too. The provenance reader instead requires a successful
bound Cargo invocation, recorder/producer source identities and exact per-file
before/after observations. Only a new file or changed digest can be recorded;
touching an unchanged unowned input cannot establish generation.

The record protocol covers the C-engine and C-guest-image producers' existing
roots and debug outputs. Its command must explicitly bind both target and
intermediate build directories.
Unknown roots, aliases, tracked names and stale source/file
identities cannot gain current authority. Records describe observations under
caller quiescence; they do not attest loaded code or exclude every race.
The caller supplies current file facts from its anchored census; this reader
reopens the ledger and sources, not each supplied output. The guarded core must
revalidate files immediately before any later mutation. Root pathname/device/
inode mapping is checked around reads and before authority returns.

The ledger fits16MiB/65,536 unique sorted outputs, each record32KiB. Source
snapshots fit1MiB and each observed file fits512MiB. These are input bounds,
not a peak-memory promise. Absent provenance supplies no approved outputs;
malformed or unsafe provenance refuses rather than silently authorizing files.
Historical records can still be decoded after a source changes, but stale
records cannot match current authority.

Version 1 retains its exact serialized shape. Version 2 adds a closed tuple
binding `scripts/artifact_cargo.py` and `scripts/artifact_cleanup.py`, the
command runner and census support. Historical rows may remain explicitly
unbound in a mixed v2 ledger. The reader's `require_captured=True` selector
requires both current support pins; legacy read-only matching remains available
without that selector. This checks record shape and current source/file facts;
it does not independently attest that an invocation occurred.

Capture pairs an anchored census of one producer's `debug/incremental` cache
files taken immediately before and after the bound invocation. A file that is
new, or whose digest changed, becomes one v2 record carrying the recorder,
producer and both support pins; an unchanged file, a tracked alias or a
hard-linked file receives no record. A failed build publishes nothing.

Publication serializes on `target/artifact-cleanup/output-provenance.lock`
(a held lock refuses rather than waits, because quiescence is a caller
precondition), merges into the current ledger under read-only pins, writes a
uniquely named temporary file, synchronizes it, renames it over the ledger
and reads the result back. Same-path rows are replaced, this producer's rows
for files absent from the fresh census are retired, every other row is kept
unchanged, and legacy rows stay unbound. The previous ledger is never opened
for writing: a build, source, census, bound or write failure leaves it exact
and retains the partial temporary file under its reported name as evidence.

Strict planner selection against the published ledger remains owned by
ARTIFACT-CLEANUP.17; guarded deletion and the host-bound operator workflow
follow. No cache is removed here.

Run the disposable-fixture controls:

```sh
python3 -B scripts/probe_artifact_output_provenance.py
```

The suite has 42 tests normal/O and twenty-two individually failing guard
omissions per mode. An optional public Cargo diagnostic preserves three owned
inputs:

```sh
python3 -B scripts/probe_artifact_output_provenance.py --cargo-contract
```

Inspect the support-source and publication interfaces, including a committed
predecessor, and the current ledger's presence:

```sh
python3 -B scripts/probe_artifact_output_provenance.py --support-contract
python3 -B scripts/probe_artifact_output_provenance.py --support-contract --revision 43f07ab
python3 -B scripts/probe_artifact_output_provenance.py --publication-contract
python3 -B scripts/probe_artifact_output_provenance.py --publication-contract --revision 47d69ef
```

The revision diagnostics load only this repository's bounded codec source
initializer through read-only Git; they perform no build or capture and need
that local object. Ordinary current/v1/v2 readers need no Git history.

Public contracts: [Cargo build directories](https://doc.rust-lang.org/cargo/reference/build-cache.html),
[Cargo metadata](https://doc.rust-lang.org/cargo/commands/cargo-metadata.html),
and [Cargo clean dry runs](https://doc.rust-lang.org/cargo/commands/cargo-clean.html).
# ANCHOR_END: usage
"""


class ProvenanceError(ValueError):
    pass


def need(condition, reason):
    if not condition:
        raise ProvenanceError(reason)


def relative(value):
    need(type(value) is str and value, "invalid bounded path")
    try:
        size = len(value.encode("utf-8"))
    except UnicodeError as error:
        raise ProvenanceError("path is not UTF-8") from error
    need(size <= 4096, "invalid bounded path")
    path = PurePosixPath(value)
    need(not path.is_absolute() and str(path) == value and value != "."
         and ".." not in path.parts and "\\" not in value
         and all(part.casefold() != ".git" for part in path.parts)
         and all(ord(char) >= 32 and ord(char) != 127 for char in value), "unsafe path")
    return value


def key(path):
    return unicodedata.normalize("NFC", path).casefold()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class Source:
    object: str
    byte_size: int
    sha256: str


@dataclass(frozen=True)
class Fact:
    path: str
    device: int
    inode: int
    mode: int
    links: int
    byte_size: int
    mtime_ns: int
    ctime_ns: int
    sha256: str


@dataclass(frozen=True)
class Observation:
    created_utc: str
    recorder: Source
    producer: Source
    argv: tuple[str, ...]
    tool_version: str
    return_code: int
    before: Fact | None
    after: Fact
    supporting_sources: tuple[Source, ...] = ()


@dataclass(frozen=True)
class Ledger:
    format: str
    outputs: tuple[Observation, ...]


@dataclass(frozen=True)
class Authority:
    ledger_sha256: str | None
    current_sources: tuple[Source, ...]
    approved: frozenset[str]


@dataclass(frozen=True)
class Publication:
    ledger_sha256: str | None
    previous_sha256: str | None
    written: bool
    records: int
    byte_size: int
    added: int
    replaced: int
    retired: int
    retained: int


def record(cls, value):
    need(type(value) is dict and set(value) == {f.name for f in fields(cls)},
         "invalid " + cls.__name__ + " fields")
    return cls(**value)


def source(value):
    item = record(Source, value)
    relative(item.object)
    need(type(item.byte_size) is int and 0 < item.byte_size <= SOURCE_BYTES,
         "source byte bound")
    need(type(item.sha256) is str and re.fullmatch("[0-9a-f]{64}", item.sha256), "source digest")
    return item


def fact(value):
    item = record(Fact, value)
    relative(item.path)
    for name in ("device", "inode", "mode", "links", "byte_size", "mtime_ns", "ctime_ns"):
        number = getattr(item, name)
        lower = -(2 ** 63) if name in {"mtime_ns", "ctime_ns"} else 0
        need(type(number) is int and lower <= number < 2 ** 64, "file identity integer")
    need(stat.S_ISREG(item.mode) and item.links >= 1 and item.byte_size <= FILE_BYTES,
         "regular bounded file required")
    need(type(item.sha256) is str and re.fullmatch("[0-9a-f]{64}", item.sha256), "file digest")
    return item


def output_class(item, producer):
    root, _ = PRODUCERS[producer]
    prefix = root + "/"
    if not item.path.startswith(prefix):
        return False
    parts = item.path[len(prefix):].split("/")
    return (len(parts) == 5 and parts[0] == "debug"
            and parts[1] == "incremental" and parts[-1] in CACHE_NAMES)


def observation(value, version=FORMAT):
    need(type(version) is str and version in {FORMAT, CAPTURE_FORMAT}, "unsupported observation format")
    if version == FORMAT:
        need(type(value) is dict and "supporting_sources" not in value,
             "invalid Observation fields")
        value = {**value, "supporting_sources": []}
    item = record(Observation, value)
    stamp = item.created_utc
    need(type(stamp) is str and len(stamp) <= 64
         and datetime.datetime.fromisoformat(stamp).utcoffset() == datetime.timedelta(), "UTC observation time")
    recorder, producer = source(item.recorder), source(item.producer)
    need(recorder.object == OBJECT and producer.object in PRODUCERS, "unbound producer/recorder")
    after = fact(item.after)
    before = None if item.before is None else fact(item.before)
    need(after.links == 1 and output_class(after, producer.object), "unowned output class")
    need(before is None or before.path == after.path and before.device == after.device
         and before.sha256 != after.sha256, "unchanged unowned input is not generation")
    need(type(item.return_code) is int and item.return_code == 0, "unsuccessful build")
    need(type(item.tool_version) is str and 0 < len(item.tool_version.encode("utf-8")) <= 1024
         and "\n" not in item.tool_version and "\r" not in item.tool_version, "tool version bound")
    need(type(item.argv) is list and len(item.argv) == 13
         and all(type(arg) is str and len(arg.encode("utf-8")) <= 4096 for arg in item.argv), "command shape")
    manifest = relative(item.argv[4])
    root, test_filter = PRODUCERS[producer.object]
    need(manifest.startswith("target/p4-system-12/") and manifest.endswith("/Cargo.toml")
         and not manifest.startswith(root + "/"), "manifest outside owned input namespace")
    expected = ("cargo", "test", "--offline", "--manifest-path", manifest,
                "--target-dir", root, "--config", 'build.build-dir="' + root + '"',
                "--lib", test_filter, "--", "--nocapture")
    need(tuple(item.argv) == expected, "build command/root binding")
    need(type(item.supporting_sources) is list and len(item.supporting_sources) in {0, 2},
         "support source count/type bound")
    supporting = tuple(source(row) for row in item.supporting_sources)
    need(not supporting or tuple(row.object for row in supporting) == SUPPORTING_OBJECTS,
         "support source objects/order differ")
    return Observation(stamp, recorder, producer, expected, item.tool_version, 0, before, after, supporting)


def encode(ledger):
    need(type(ledger) is Ledger, "plain ledger required")
    need(type(ledger.format) is str and ledger.format in {FORMAT, CAPTURE_FORMAT}, "unsupported ledger format")
    try:
        value = asdict(ledger)
        if ledger.format == FORMAT:
            need(all(not row.supporting_sources for row in ledger.outputs),
                 "legacy format cannot store support sources")
            for row in value["outputs"]:
                del row["supporting_sources"]
        raw = (json.dumps(value, ensure_ascii=True, allow_nan=False,
                          sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")
    except (TypeError, ValueError, RecursionError) as error:
        raise ProvenanceError("unencodable ledger") from error
    need(0 < len(raw) <= MAX_BYTES, "ledger byte bound")
    return raw


def decode(raw):
    need(type(raw) is bytes and 0 < len(raw) <= MAX_BYTES, "ledger byte bound")

    def pairs(items):
        value = {}
        for name, item in items:
            need(name not in value, "duplicate JSON field")
            value[name] = item
        return value

    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                           parse_constant=lambda unused: need(False, "nonfinite JSON"))
        ledger = record(Ledger, value)
        need(ledger.format in {FORMAT, CAPTURE_FORMAT} and type(ledger.outputs) is list
             and len(ledger.outputs) <= MAX_RECORDS, "ledger format/count bound")
        outputs = []
        for row in ledger.outputs:
            need(len(json.dumps(row, ensure_ascii=True, sort_keys=True,
                                separators=(",", ":")).encode("ascii")) <= MAX_RECORD_BYTES, "record byte bound")
            outputs.append(observation(row, ledger.format))
        paths = [row.after.path for row in outputs]
        need(paths == sorted(paths) and len(paths) == len(set(map(key, paths))), "output order/alias collision")
        result = Ledger(ledger.format, tuple(outputs))
        need(encode(result) == raw, "noncanonical ledger")
        return result
    except (TypeError, ValueError, KeyError, AttributeError, UnicodeError, RecursionError) as error:
        if isinstance(error, ProvenanceError):
            raise
        raise ProvenanceError("malformed ledger: " + type(error).__name__) from error


def _source(owned, name):
    parent, leaf = name.rsplit("/", 1)
    with owned.directory(parent) as directory:
        item, _ = owned.snapshot(directory, leaf, name, SOURCE_BYTES)
    return Source(name, item.byte_size, item.sha256)


def _root_guard(owned):
    need(owned.path == ROOT, "reader/runtime root differs")
    current, opened = ROOT.lstat(), os.fstat(owned.fd)
    need(stat.S_ISDIR(current.st_mode) and current.st_dev == owned.device
         and (current.st_dev, current.st_ino) == (opened.st_dev, opened.st_ino), "root mapping changed")


def load(owned):
    """Read through the caller's anchored root; absence supplies no authority."""
    _root_guard(owned)
    parent, leaf = LEDGER.rsplit("/", 1)
    try:
        with owned.directory(parent) as directory:
            _, raw = owned.snapshot(directory, leaf, LEDGER, MAX_BYTES, payload=True)
    except FileNotFoundError:
        _root_guard(owned)
        return None
    _root_guard(owned)
    return raw, decode(raw)


def authorize(owned, current, *, tracked_paths, require_captured=False):
    """Match recorded observations against current sources and file facts only."""
    need(type(require_captured) is bool, "plain captured-observation selection required")
    need(type(current) is tuple and len(current) <= MAX_RECORDS
         and all(type(item) is Fact for item in current), "bounded plain current facts required")
    need(type(tracked_paths) is frozenset and len(tracked_paths) <= MAX_RECORDS,
         "bounded tracked inventory required")
    tracked_keys = frozenset(key(relative(path)) for path in tracked_paths)
    paths = [item.path for item in current]
    need(len(paths) == len(set(map(key, paths))), "current alias collision")
    for item in current:
        fact(asdict(item))
        need(item.device == owned.device, "current file crosses volume")
    saved = load(owned)
    recorder = _source(owned, OBJECT)
    if saved is None:
        _root_guard(owned)
        return Authority(None, (recorder,), frozenset())
    raw, ledger = saved
    sources = {OBJECT: recorder}
    dependencies = {row.producer.object for row in ledger.outputs}
    dependencies.update(source.object for row in ledger.outputs for source in row.supporting_sources)
    for name in sorted(dependencies):
        sources[name] = _source(owned, name)
    observed = {row.after.path: row for row in ledger.outputs}
    approved = set()
    for item in current:
        row = observed.get(item.path)
        if (row is not None and key(item.path) not in tracked_keys and item.links == 1
                and row.after == item and row.recorder == recorder
                and row.producer == sources[row.producer.object]
                and (not require_captured or bool(row.supporting_sources))
                and all(sources[dependency.object] == dependency for dependency in row.supporting_sources)):
            approved.add(item.path)
    _root_guard(owned)
    return Authority(sha(raw), tuple(sources[name] for name in sorted(sources)), frozenset(approved))


def census(owned, producer):
    """Observe every current output-class file under one producer's root, in path order."""
    need(type(producer) is str and producer in PRODUCERS, "unknown Cargo producer")
    _root_guard(owned)
    base = PRODUCERS[producer][0] + "/debug/incremental"
    facts, entries = [], 0

    def listing(directory):
        nonlocal entries
        rows = []
        with os.scandir(directory) as scan:
            for entry in scan:
                entries += 1
                need(entries <= MAX_ENTRIES, "output census entry bound")
                rows.append((entry.name, os.stat(entry.name, dir_fd=directory, follow_symlinks=False)))
        return sorted(rows)

    try:
        os.stat(base, dir_fd=owned.fd, follow_symlinks=False)
    except FileNotFoundError:
        _root_guard(owned)
        return ()
    with owned.directory(base) as incremental:
        for crate, info in listing(incremental):
            if not stat.S_ISDIR(info.st_mode):
                continue
            with owned.directory(base + "/" + crate) as sessions:
                for session, info in listing(sessions):
                    if not stat.S_ISDIR(info.st_mode):
                        continue
                    path = base + "/" + crate + "/" + session
                    with owned.directory(path) as outputs:
                        for leaf, info in listing(outputs):
                            if leaf not in CACHE_NAMES or not stat.S_ISREG(info.st_mode):
                                continue
                            item, _ = owned.snapshot(outputs, leaf, path + "/" + leaf, FILE_BYTES)
                            facts.append(fact(asdict(item)))
                            need(len(facts) <= MAX_RECORDS, "output census record bound")
    _root_guard(owned)
    paths = [item.path for item in facts]
    need(len(paths) == len(set(map(key, paths))), "output alias collision")
    return tuple(sorted(facts, key=lambda item: item.path))


def observe(stamp, recorder, producer, argv, tool_version, return_code, supporting, before, after, *, tracked_paths):
    """Pair anchored before/after facts; only a new file or a changed digest becomes a record."""
    need(type(before) is tuple and type(after) is tuple and all(type(item) is Fact for item in (*before, *after))
         and type(tracked_paths) is frozenset and len(tracked_paths) <= MAX_RECORDS, "plain bounded census facts required")
    tracked_keys = frozenset(key(relative(path)) for path in tracked_paths)
    prior = {item.path: item for item in before}
    rows, unclaimed = [], 0
    for item in after:
        if key(item.path) in tracked_keys or item.links != 1:
            unclaimed += 1
            continue
        old = prior.get(item.path)
        if old is not None and old.sha256 == item.sha256:
            continue
        row = Observation(stamp, recorder, producer, tuple(argv), tool_version, return_code, old, item, tuple(supporting))
        rows.append(observation(json.loads(json.dumps(asdict(row))), CAPTURE_FORMAT))
    need(all(row.supporting_sources for row in rows), "captured observations require support pins")
    return tuple(rows), unclaimed


def merge(previous, rows, producer, present):
    """Replace same-path rows, retire this producer's rows absent from the fresh census, keep the rest."""
    root = PRODUCERS[producer][0] + "/"
    fresh = {row.after.path for row in rows}
    kept, counts = [], dict(added=0, replaced=0, retired=0, retained=0)
    for row in (previous.outputs if previous is not None else ()):
        if row.after.path in fresh:
            counts["replaced"] += 1
        elif row.after.path.startswith(root) and row.after.path not in present:
            counts["retired"] += 1
        else:
            kept.append(row)
            counts["retained"] += 1
    counts["added"] = len(rows) - counts["replaced"]
    ledger = Ledger(CAPTURE_FORMAT, tuple(sorted((*kept, *rows), key=lambda row: row.after.path)))
    return decode(encode(ledger)), counts


def _flush(descriptor):
    os.fsync(descriptor)
    if sys.platform == "darwin":
        flag = getattr(fcntl, "F_FULLFSYNC", None)
        need(type(flag) is int, "F_FULLFSYNC unavailable")
        fcntl.fcntl(descriptor, flag)


def publish(owned, rows, producer, present):
    """Serialize one bounded merge and replace the current ledger atomically; never rewrite it in place."""
    need(type(rows) is tuple and all(type(row) is Observation for row in rows) and type(present) is frozenset
         and all(type(path) is str for path in present), "plain captured rows and census paths required")
    need(type(producer) is str and producer in PRODUCERS, "unknown Cargo producer")
    _root_guard(owned)
    sources = {name: _source(owned, name) for name in (OBJECT, producer, *SUPPORTING_OBJECTS)}
    need(all(row.recorder == sources[OBJECT] and row.producer == sources[producer]
             and row.supporting_sources == tuple(sources[name] for name in SUPPORTING_OBJECTS)
             for row in rows), "publication requires current recorder, producer and support pins")
    with owned.directory(WORKSPACE, create=True) as directory:
        lock = os.open(LOCK_NAME, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600, dir_fd=directory)
        try:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                raise ProvenanceError("another publication holds the ledger lock") from error
            held = os.fstat(lock)
            need(stat.S_ISREG(held.st_mode) and held.st_dev == owned.device, "ledger lock is not an owned regular file")
            saved = load(owned)
            previous_raw, previous = saved if saved is not None else (None, None)
            previous_sha = None if previous_raw is None else sha(previous_raw)
            if not rows and previous is None:
                return Publication(None, None, False, 0, 0, 0, 0, 0, 0)
            ledger, counts = merge(previous, rows, producer, present)
            raw = encode(ledger)
            if previous_raw == raw:
                return Publication(previous_sha, previous_sha, False, len(ledger.outputs), len(raw), **counts)
            temp = NAME + "." + str(os.getpid()) + "." + str(time.monotonic_ns()) + ".tmp"
            descriptor = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
                                 0o600, dir_fd=directory)
            try:
                cursor = 0
                while cursor < len(raw):
                    written = os.write(descriptor, raw[cursor:])
                    need(0 < written <= len(raw) - cursor, "ledger write made no valid progress")
                    cursor += written
                _flush(descriptor)
                opened = os.fstat(descriptor)
                located = os.stat(temp, dir_fd=directory, follow_symlinks=False)
                need(opened.st_size == len(raw) and opened.st_nlink == 1 and opened.st_dev == owned.device
                     and (opened.st_dev, opened.st_ino) == (located.st_dev, located.st_ino),
                     "temporary ledger changed before publication")
                _root_guard(owned)
                os.rename(temp, NAME, src_dir_fd=directory, dst_dir_fd=directory)
            except Exception as error:
                raise ProvenanceError("publication failed; previous ledger preserved, partial retained as "
                                      + WORKSPACE + "/" + temp) from error
            finally:
                os.close(descriptor)
            os.fsync(directory)
            check = load(owned)
            need(check is not None and check[0] == raw, "published ledger does not read back")
        finally:
            os.close(lock)
    _root_guard(owned)
    return Publication(sha(raw), previous_sha, True, len(ledger.outputs), len(raw), **counts)
