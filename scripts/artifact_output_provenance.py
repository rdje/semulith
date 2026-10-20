#!/usr/bin/env python3
"""Closed records of changed outputs from two repository-owned Cargo producers.

This reader grants no deletion operation. Producer/plan integration is separate.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, fields
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import unicodedata

ROOT = Path(__file__).resolve().parent.parent
OBJECT = "scripts/artifact_output_provenance.py"
LEDGER = "target/artifact-cleanup/output-provenance.json"
FORMAT = "artifact-output-provenance-v1"
MAX_BYTES = 16 * 1024 * 1024
MAX_RECORDS = 65536
MAX_RECORD_BYTES = 32768
SOURCE_BYTES = 1024 * 1024
FILE_BYTES = 512 * 1024 * 1024
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
roots and debug outputs; actual producer integration is still pending. Its
command must explicitly bind both target and intermediate build directories.
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

This slice provides a record codec and anchored reader only. Actual producer
capture and planner selection remain owned by ARTIFACT-CLEANUP.17; guarded
deletion and the host-bound operator workflow follow. No cache is removed here.

Run the disposable-fixture controls:

```sh
python3 -B scripts/probe_artifact_output_provenance.py
```

The suite has25 tests normal/O and thirteen individually failing guard omissions
per mode. An optional public Cargo diagnostic preserves three owned inputs:

```sh
python3 -B scripts/probe_artifact_output_provenance.py --cargo-contract
```

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


@dataclass(frozen=True)
class Ledger:
    format: str
    outputs: tuple[Observation, ...]


@dataclass(frozen=True)
class Authority:
    ledger_sha256: str | None
    current_sources: tuple[Source, ...]
    approved: frozenset[str]


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


def observation(value):
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
    return Observation(stamp, recorder, producer, expected, item.tool_version, 0, before, after)


def encode(ledger):
    need(type(ledger) is Ledger, "plain ledger required")
    try:
        raw = (json.dumps(asdict(ledger), ensure_ascii=True, allow_nan=False,
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
        need(ledger.format == FORMAT and type(ledger.outputs) is list
             and len(ledger.outputs) <= MAX_RECORDS, "ledger format/count bound")
        outputs = []
        for row in ledger.outputs:
            need(len(json.dumps(row, ensure_ascii=True, sort_keys=True,
                                separators=(",", ":")).encode("ascii")) <= MAX_RECORD_BYTES, "record byte bound")
            outputs.append(observation(row))
        paths = [row.after.path for row in outputs]
        need(paths == sorted(paths) and len(paths) == len(set(map(key, paths))), "output order/alias collision")
        result = Ledger(FORMAT, tuple(outputs))
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


def authorize(owned, current, *, tracked_paths):
    """Match recorded observations against current sources and file facts only."""
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
    for name in sorted({row.producer.object for row in ledger.outputs}):
        sources[name] = _source(owned, name)
    observed = {row.after.path: row for row in ledger.outputs}
    approved = set()
    for item in current:
        row = observed.get(item.path)
        if (row is not None and key(item.path) not in tracked_keys and item.links == 1
                and row.after == item and row.recorder == recorder
                and row.producer == sources[row.producer.object]):
            approved.add(item.path)
    _root_guard(owned)
    return Authority(sha(raw), tuple(sources[name] for name in sorted(sources)), frozenset(approved))
