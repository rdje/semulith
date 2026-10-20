#!/usr/bin/env python3
"""Bounded, repository-owned artifact cohort planning and state checking.

This slice publishes plans only. It exposes no cache-deletion operation.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack, contextmanager
from dataclasses import asdict, dataclass, fields, replace
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import selectors
import stat
import subprocess
import sys
import time
import unicodedata

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = "target/artifact-cleanup"
CACHE_NAMES = frozenset({"dep-graph.bin", "query-cache.bin", "work-products.bin"})
DEFAULT_SCOPES = (".app-data", "target")
PLAN_BYTES = 16 * 1024 * 1024
SOURCE_BYTES = 1024 * 1024
PATH_BYTES = 4096
GIT_BYTES = 8 * 1024 * 1024

USAGE = """# ANCHOR: usage
### Bounded cleanup plans

The tracked instrument lists incremental cache candidates by path/name and
checks a saved cohort. Regenerable build-output ownership is pending
`ARTIFACT-CLEANUP.15` before deletion readiness. Supported cache deletion is
pending `ARTIFACT-CLEANUP.14`; this version never removes a cache. Historical
cleanup receipts keep their original scope.

From the repository root, choose a new run directory:

```sh
python3 -B scripts/artifact_cleanup.py --plan --workdir target/artifact-cleanup/review
python3 -B scripts/artifact_cleanup.py --check --workdir target/artifact-cleanup/review
```

The tracked diagnostic and its commit/CI gate use disposable on-volume copies:

```sh
python3 -B scripts/probe_artifact_cleanup.py
bash scripts/check_artifact_cleanup.sh --self-test
```

The gate requires 26 passing tests in normal and optimized Python, plus ten
targeted guard omissions per mode, each losing one assertion with zero errors.
Five additional historical-helper tests and a source-pin omission run in both
modes: 26 planning/history outcomes. Journal coverage adds26 tests and ten
omissions per mode,48 gate outcomes altogether. No real project cleanup occurs.

The original AC0067 helper is retained byte-exact as passive input in
`scripts/fixtures/artifact_cleanup_0067.py.txt`. Its 5,815 bytes retain their
original SHA-256. The tracked replay loads at most 8 KiB through descriptor
checks and executes only copies in fresh owned fixtures:

```sh
python3 -B scripts/probe_legacy_artifact_cleanup.py
```

The debug fixture completes; the release fixture reproduces the historical
defect: a cache was also labeled a retained stray, so its removal made the
post-check fail without a receipt. The replay preserves retained input bytes
and restores the caller's directory. It mocks only public Git root/inventory
reads. Those are observations of the old helper; current planning already
separates candidates and retained strays. Guarded deletion and partial-result
recovery remain separate pending work. Historical cleanup receipts keep their
original event and instrument identities.

Planning exclusively creates `plan.json`; it refuses to overwrite an old plan.
Keep run logs in the selected work directory. The reserved
`target/artifact-cleanup` namespace is excluded from the census and never
selected. Other symlinks, nested Git roots, foreign volumes and special files
are named exclusions. Neither their targets nor repository implementations are
inspected. Public Git supplies the union of HEAD and index tracked paths;
tracked files, hard links and unknown classes cannot become deletion candidates.
Case- and Unicode-normalization-equivalent tracked names are conservatively
protected too. Git metadata must remain on the repository volume.
Known foreign-device Git markers refuse before any Git query. Bounded public
path discovery precedes the indirect Git/common-directory device checks;
inventory reads follow only after those checks pass.

The default census covers `target` and `.app-data`. Repeated `--scope` options
select narrower nonoverlapping descendants of those roots. Only the three
known cache names under a `debug/incremental` or `release/incremental` path,
inside `target` or `.app-data/target`, qualify. Other `.bin` and `.log` files
are retained. Release/deps strays are a subset of retained files, so a release
incremental cache cannot occupy both populations.

Plans include immutable file identities/digests, scoped exclusions, current
instrument identity and tracked-path inventory digest. Checking re-enumerates
the complete declared cohort. `--check-after` observes that selected files are
absent and retained bytes/identities remain; it does not establish who acted.
Changed or missing cohort members cannot establish successful equality.

The fixed ceilings are 65,536 recorded files/exclusions, 262,144 directories,
4,194,304 visited entries, depth 96, 512 MiB per hashed file and 32 GiB of
cohort hashes per pass. Paths fit 4,096 UTF-8 bytes and plans fit 16 MiB.
Instrument preparation is separately limited to 1 MiB; each public Git read
accepts at most 8 MiB stdout/64 KiB stderr and has a 30-second process deadline.
Overflow detection reads at most one additional byte from each pipe.
The tool requires POSIX descriptor support, checked before use. These bounds
do not promise peak RAM, an atomic directory snapshot or loaded-code attestation.
Run against quiescent data; the actual host census remains a separate workflow
precondition for any later deletion. See Python's
[descriptor interfaces](https://docs.python.org/3.12/library/os.html#files-and-directories).
Git must support [disabling lazy fetching](https://git-scm.com/docs/git#Documentation/git.txt---no-lazy-fetch);
reads disable fetching, optional locks, paging and filesystem-monitor commands.

Exit 0 reports a published plan or matched state; 1 reports stale state;
2 refuses invalid, unavailable or unsupported inputs. No Git, reference or
dependency source is modified. All saved paths are repository-relative.
# ANCHOR_END: usage
"""


class CleanupError(ValueError):
    def __init__(self, disposition: str, reason: str):
        self.disposition = disposition
        self.reason = reason
        super().__init__(reason)


def need(condition: bool, reason: str, disposition: str = "refused"):
    if not condition:
        raise CleanupError(disposition, reason)


def relative(value: str) -> str:
    need(type(value) is str and bool(value), "expected a relative path")
    try:
        size = len(value.encode("utf-8"))
    except UnicodeError as error:
        raise CleanupError("refused", "relative path is not UTF-8") from error
    need(size <= PATH_BYTES and "\\" not in value
         and all(ord(c) >= 32 and ord(c) != 127 for c in value), "unsafe relative path")
    path = PurePosixPath(value)
    need(not path.is_absolute() and str(path) == value and "." != value
         and ".." not in path.parts and all(p.casefold() != ".git" for p in path.parts),
         "noncanonical or Git metadata path")
    return value


def beneath(path: str, parent: str) -> bool:
    return path == parent or path.startswith(parent + "/")


def runtime_root(root: Path) -> Path:
    need(isinstance(root, Path) and root.resolve() == ROOT,
         "selected root differs from this instrument's runtime root")
    return ROOT


@dataclass(frozen=True)
class Limits:
    records: int = 65536
    directories: int = 262144
    entries: int = 4194304
    depth: int = 96
    file_bytes: int = 512 * 1024 * 1024
    hash_bytes: int = 32 * 1024 * 1024 * 1024


def validate_limits(value: Limits):
    need(type(value) is Limits, "expected plain limits")
    maxima = Limits()
    for field in fields(value):
        amount = getattr(value, field.name)
        need(type(amount) is int and 0 <= amount <= getattr(maxima, field.name),
             "invalid limit: " + field.name)


@dataclass(frozen=True)
class FileFact:
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
class Source:
    object: str
    byte_size: int
    sha256: str


@dataclass(frozen=True)
class Exclusion:
    path: str
    reason: str


@dataclass(frozen=True)
class Plan:
    format: str
    created_utc: str
    workdir: str
    scopes: tuple[str, ...]
    limits: Limits
    device: int
    tracked_sha256: str
    instrument: Source
    candidates: tuple[FileFact, ...]
    retained: tuple[FileFact, ...]
    excluded: tuple[Exclusion, ...]
    strays: tuple[str, ...]


@dataclass(frozen=True)
class Finding:
    disposition: str
    reason: str
    candidates: int | None = None
    candidate_bytes: int | None = None
    retained: int | None = None
    retained_bytes: int | None = None


def _summary(plan: Plan, disposition="matched", reason="complete scoped cohort matches"):
    return Finding(disposition, reason, len(plan.candidates),
                   sum(f.byte_size for f in plan.candidates), len(plan.retained),
                   sum(f.byte_size for f in plan.retained))


def _identity(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns)


class Boundary(Exception):
    def __init__(self, path, reason):
        self.path, self.reason = path, reason


class OwnedRoot:
    """Descriptor traversal; no directory component or final symlink is followed."""

    def __init__(self, root: Path):
        need(all(hasattr(os, name) for name in ("O_DIRECTORY", "O_NOFOLLOW", "O_NONBLOCK"))
             and os.scandir in os.supports_fd and os.open in os.supports_dir_fd
             and os.stat in os.supports_dir_fd, "POSIX descriptor operations unavailable")
        self.path = root
        self.fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            self.device = os.fstat(self.fd).st_dev
        except BaseException:
            os.close(self.fd)
            raise

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        os.close(self.fd)

    @contextmanager
    def directory(self, path: str, *, create=False):
        parts = relative(path).split("/")
        need(len(parts) <= Limits().depth, "directory path depth limit exceeded")
        parents = []
        with ExitStack() as resources:
            current = self.fd
            for n, part in enumerate(parts):
                name = "/".join(parts[:n + 1])
                if create:
                    try:
                        os.mkdir(part, mode=0o700, dir_fd=current)
                    except FileExistsError:
                        pass
                before = os.stat(part, dir_fd=current, follow_symlinks=False)
                if stat.S_ISLNK(before.st_mode):
                    raise Boundary(name, "symlink")
                if before.st_dev != self.device:
                    raise Boundary(name, "volume")
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current)
                resources.callback(os.close, child)
                info = os.fstat(child)
                need((before.st_dev, before.st_ino) == (info.st_dev, info.st_ino),
                     "directory changed before open: " + name, "stale")
                if info.st_dev != self.device:
                    raise Boundary(name, "volume")
                try:
                    os.stat(".git", dir_fd=child, follow_symlinks=False)
                except FileNotFoundError:
                    pass
                else:
                    raise Boundary(name, "nested-git")
                parents.append((current, part, info.st_dev, info.st_ino, child))
                current = child
            try:
                yield current
            finally:
                for parent, part, device, inode, child in reversed(parents):
                    after = os.stat(part, dir_fd=parent, follow_symlinks=False)
                    opened = os.fstat(child)
                    need(stat.S_ISDIR(after.st_mode) and (after.st_dev, after.st_ino)
                         == (opened.st_dev, opened.st_ino) == (device, inode),
                         "directory changed after open", "stale")
                    try:
                        os.stat(".git", dir_fd=child, follow_symlinks=False)
                    except FileNotFoundError:
                        pass
                    else:
                        raise CleanupError("stale", "Git boundary appeared during operation")

    def snapshot(self, parent: int, name: str, path: str, limit: int, *, payload=False, expected=None):
        before = os.stat(name, dir_fd=parent, follow_symlinks=False)
        need(expected is None or _identity(before) == expected, "file changed before snapshot: " + path, "stale")
        need(stat.S_ISREG(before.st_mode) and before.st_dev == self.device,
             "not an owned regular file: " + path)
        need(before.st_size <= limit, "file byte limit: " + path)
        descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
        chunks = []
        digest = hashlib.sha256()
        total = 0
        try:
            need(_identity(before) == _identity(os.fstat(descriptor)), "file changed before read: " + path, "stale")
            while total < before.st_size:
                data = os.read(descriptor, min(1024 * 1024, before.st_size - total))
                if not data:
                    break
                total += len(data)
                digest.update(data)
                if payload:
                    chunks.append(data)
            after = os.fstat(descriptor)
            need(total == before.st_size and _identity(before) == _identity(after)
                 == _identity(os.stat(name, dir_fd=parent, follow_symlinks=False)),
                 "file changed during read: " + path, "stale")
        finally:
            os.close(descriptor)
        fact = FileFact(path, *_identity(before), digest.hexdigest())
        return fact, b"".join(chunks) if payload else None


def _git(root: Path, arguments: list[str], maximum=GIT_BYTES) -> bytes:
    """Bound both pipes and terminate the owned read process on timeout/overflow."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = ["git", "--no-pager", "--no-lazy-fetch", "--no-optional-locks", "--no-replace-objects", "-c", "core.fsmonitor=false",
               "-C", str(root), *arguments]
    with subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=env) as child:
        buffers = [bytearray(), bytearray()]
        deadline = time.monotonic() + 30
        try:
            with selectors.DefaultSelector() as selector:
                selector.register(child.stdout, selectors.EVENT_READ, (0, maximum))
                selector.register(child.stderr, selectors.EVENT_READ, (1, 65536))
                while selector.get_map():
                    remaining = deadline - time.monotonic()
                    need(remaining > 0, "Git read timed out", "unavailable")
                    for key, _ in selector.select(remaining):
                        index, cap = key.data
                        data = os.read(key.fd, min(65536, cap - len(buffers[index]) + 1))
                        if not data:
                            selector.unregister(key.fileobj)
                        else:
                            buffers[index].extend(data)
                            need(len(buffers[index]) <= cap, "Git output exceeds bound")
            code = child.wait(timeout=max(0.001, deadline - time.monotonic()))
            need(code == 0 and not buffers[1], "Git read failed (exit " + str(code) + ")", "unavailable")
            return bytes(buffers[0])
        finally:
            if child.poll() is None:
                child.kill()
                child.wait()


def tracked_paths(root: Path) -> frozenset[str]:
    root = runtime_root(root)
    device = root.stat().st_dev
    try:
        marker = (root / ".git").lstat()
    except FileNotFoundError as error:
        raise CleanupError("refused", "runtime root lacks owned Git metadata") from error
    need(not stat.S_ISLNK(marker.st_mode), "Git metadata symlink refused")
    need(marker.st_dev == device, "Git marker crosses repository volume")
    top = _git(root, ["rev-parse", "--show-toplevel"], PATH_BYTES + 1)
    need(top.endswith(b"\n") and Path(top[:-1].decode()).resolve() == root,
         "Git runtime root differs; parent fallback refused")
    for option in ("--absolute-git-dir", "--git-common-dir"):
        raw = _git(root, ["rev-parse", option], PATH_BYTES + 1)
        need(raw.endswith(b"\n"), "incomplete Git metadata path")
        metadata = Path(raw[:-1].decode())
        if not metadata.is_absolute():
            metadata = root / metadata
        need(metadata.stat().st_dev == device, "Git metadata crosses repository volume")
    result = set()
    for command in (["ls-files", "--cached", "--full-name", "-z"],
                    ["ls-tree", "-r", "--name-only", "-z", "HEAD"]):
        raw = _git(root, command)
        need(not raw or raw.endswith(b"\0"), "incomplete Git inventory")
        names = [relative(row.decode("utf-8")) for row in raw.split(b"\0")[:-1]]
        need(len(names) <= Limits().records and len(names) == len(set(names)), "oversized or ambiguous Git inventory")
        result.update(names)
    return frozenset(result)


def _selection(workdir: str, scopes: tuple[str, ...]):
    relative(workdir)
    need(len(workdir.split("/")) <= Limits().depth, "workspace depth limit exceeded")
    need(workdir.startswith(WORKSPACE + "/"), "workdir must be a child of " + WORKSPACE)
    need(type(scopes) is tuple and 1 <= len(scopes) <= 16
         and all(type(scope) is str for scope in scopes)
         and tuple(sorted(set(scopes))) == scopes, "scopes must be a sorted distinct tuple")
    for scope in scopes:
        relative(scope)
        need(len(scope.split("/")) <= Limits().depth, "scope depth limit exceeded")
        need(any(beneath(scope, base) for base in DEFAULT_SCOPES)
             and not beneath(scope, WORKSPACE), "scope outside artifact roots or inside workspace")
    need(not any(beneath(b, a) for i, a in enumerate(scopes) for b in scopes[i + 1:]), "overlapping scopes")


def _ownership_key(path: str) -> str:
    return unicodedata.normalize("NFC", path).casefold()


def candidate(fact: FileFact, tracked_keys: frozenset[str]) -> bool:
    parts = fact.path.split("/")
    return (_ownership_key(fact.path) not in tracked_keys and fact.links == 1 and parts[-1] in CACHE_NAMES
            and (parts[0] == "target" or parts[:2] == [".app-data", "target"])
            and any(parts[n] == "incremental" and parts[n - 1] in {"debug", "release"}
                    for n in range(1, len(parts) - 1)))


def _instrument(root: OwnedRoot) -> Source:
    try:
        name = Path(__file__).resolve().relative_to(root.path).as_posix()
    except ValueError as error:
        raise CleanupError("refused", "instrument outside selected repository") from error
    relative(name)
    parent, leaf = name.rsplit("/", 1)
    with root.directory(parent) as directory:
        fact, _ = root.snapshot(directory, leaf, name, SOURCE_BYTES)
    need(fact.byte_size > 0, "instrument is empty")
    return Source(name, fact.byte_size, fact.sha256)


def make_plan(root: Path, *, workdir: str, scopes=DEFAULT_SCOPES, limits=Limits()) -> Plan:
    """Observe the complete selected projection; do not write files or delete caches."""
    root = runtime_root(root)
    _selection(workdir, scopes)
    validate_limits(limits)
    tracked = tracked_paths(root)
    tracked_keys = frozenset(_ownership_key(path) for path in tracked)
    selected, retained, excluded = [], [], []
    counts = {"directories": 0, "entries": 0, "records": 0, "hash_bytes": 0}

    def charge(kind, amount=1):
        counts[kind] += amount
        need(counts[kind] <= getattr(limits, kind), kind + " limit exceeded")

    with OwnedRoot(root) as owned:
        instrument = _instrument(owned)

        def visit(directory, path, depth):
            need(depth <= limits.depth, "directory depth limit exceeded")
            charge("directories")
            with os.scandir(directory) as entries:
                for entry in entries:
                    charge("entries")
                    name = relative(path + "/" + entry.name)
                    if beneath(name, WORKSPACE):
                        continue
                    info = os.stat(entry.name, dir_fd=directory, follow_symlinks=False)
                    if stat.S_ISLNK(info.st_mode):
                        charge("records"); excluded.append(Exclusion(name, "symlink")); continue
                    if info.st_dev != owned.device:
                        charge("records"); excluded.append(Exclusion(name, "volume")); continue
                    if stat.S_ISDIR(info.st_mode):
                        need(depth + 1 <= limits.depth, "directory depth limit exceeded")
                        try:
                            with owned.directory(name) as child:
                                visit(child, name, depth + 1)
                        except Boundary as error:
                            need(error.path == name, "ancestor boundary changed during census", "stale")
                            charge("records"); excluded.append(Exclusion(error.path, error.reason))
                        continue
                    if not name.endswith((".bin", ".log")):
                        continue
                    charge("records")
                    if not stat.S_ISREG(info.st_mode):
                        excluded.append(Exclusion(name, "nonregular")); continue
                    charge("hash_bytes", info.st_size)
                    fact, _ = owned.snapshot(directory, entry.name, name, min(limits.file_bytes, info.st_size),
                                             expected=_identity(info))
                    need(fact.byte_size == info.st_size, "file changed before hashing: " + name, "stale")
                    (selected if candidate(fact, tracked_keys) else retained).append(fact)

        for scope in scopes:
            need(len(scope.split("/")) <= limits.depth, "scope depth limit exceeded")
            if scope in DEFAULT_SCOPES:
                try:
                    os.stat(scope, dir_fd=owned.fd, follow_symlinks=False)
                except FileNotFoundError:
                    continue
            try:
                with owned.directory(scope) as directory:
                    visit(directory, scope, len(PurePosixPath(scope).parts))
            except Boundary as error:
                charge("records"); excluded.append(Exclusion(error.path, error.reason))
        need(_instrument(owned) == instrument, "instrument changed during census", "stale")
        need(tracked_paths(root) == tracked, "tracked inventory changed during census", "stale")
        strays = tuple(sorted(f.path for f in retained if any(beneath(f.path, prefix) for prefix in
                       ("target/release", "target/debug/deps", ".app-data/target/release", ".app-data/target/debug/deps"))))
        plan = Plan("artifact-cohort-v1", datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    workdir, scopes, limits, owned.device,
                    hashlib.sha256(b"\0".join(p.encode() for p in sorted(tracked))).hexdigest(), instrument,
                    tuple(sorted(selected, key=lambda f: f.path)), tuple(sorted(retained, key=lambda f: f.path)),
                    tuple(sorted(set(excluded), key=lambda f: (f.path, f.reason))), strays)
    encode_plan(plan)
    return plan


def encode_plan(plan: Plan) -> bytes:
    need(type(plan) is Plan, "expected a plain plan")
    try:
        raw = (json.dumps(asdict(plan), sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode()
    except (TypeError, ValueError, RecursionError) as error:
        raise CleanupError("refused", "invalid plan serialization: " + type(error).__name__) from error
    need(len(raw) <= PLAN_BYTES, "plan JSON exceeds bound")
    return raw


def decode_plan(raw: bytes) -> Plan:
    need(type(raw) is bytes and 0 < len(raw) <= PLAN_BYTES, "invalid bounded plan bytes")

    def pairs(items):
        value = {}
        for key, item in items:
            need(key not in value, "duplicate JSON field")
            value[key] = item
        return value

    def record(cls, value):
        need(type(value) is dict and set(value) == {f.name for f in fields(cls)}, "invalid " + cls.__name__ + " fields")
        return cls(**value)

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                           parse_constant=lambda unused: need(False, "nonfinite JSON value"))
        need(type(value) is dict and set(value) == {f.name for f in fields(Plan)}, "invalid Plan fields")
        for name in ("scopes", "candidates", "retained", "excluded", "strays"):
            need(type(value[name]) is list and len(value[name]) <= Limits().records, "invalid plan collection")
        value["limits"] = record(Limits, value["limits"])
        validate_limits(value["limits"])
        value["instrument"] = record(Source, value["instrument"])
        for name in ("candidates", "retained"):
            value[name] = tuple(record(FileFact, f) for f in value[name])
        value["excluded"] = tuple(record(Exclusion, f) for f in value["excluded"])
        value["scopes"], value["strays"] = tuple(value["scopes"]), tuple(value["strays"])
        plan = record(Plan, value)
        need(plan.format == "artifact-cohort-v1", "unsupported plan format")
        _selection(plan.workdir, plan.scopes)
        need(type(plan.created_utc) is str and len(plan.created_utc) <= 64
             and datetime.datetime.fromisoformat(plan.created_utc).utcoffset() == datetime.timedelta(), "invalid UTC time")
        need(type(plan.device) is int and 0 <= plan.device < 2 ** 64, "invalid repository device")
        need(type(plan.tracked_sha256) is str and re.fullmatch("[0-9a-f]{64}", plan.tracked_sha256), "invalid tracked digest")
        relative(plan.instrument.object)
        need(type(plan.instrument.byte_size) is int and 0 < plan.instrument.byte_size <= SOURCE_BYTES
             and type(plan.instrument.sha256) is str and re.fullmatch("[0-9a-f]{64}", plan.instrument.sha256), "invalid instrument identity")
        all_paths = []
        for group in (plan.candidates, plan.retained):
            need(tuple(sorted(group, key=lambda f: f.path)) == group, "unordered file facts")
            for fact in group:
                relative(fact.path)
                need(len(fact.path.split("/")) <= plan.limits.depth + 1,
                     "file path depth exceeds plan limit")
                need(any(beneath(fact.path, scope) for scope in plan.scopes)
                     and not beneath(fact.path, WORKSPACE) and fact.path.endswith((".bin", ".log")), "file outside selected projection")
                for name in ("device", "inode", "mode", "links", "byte_size", "mtime_ns", "ctime_ns"):
                    number = getattr(fact, name)
                    lower = -(2 ** 63) if name in {"mtime_ns", "ctime_ns"} else 0
                    need(type(number) is int and lower <= number < 2 ** 64, "invalid file identity integer")
                need(fact.device == plan.device and stat.S_ISREG(fact.mode) and fact.links >= 1
                     and fact.byte_size <= plan.limits.file_bytes and type(fact.sha256) is str
                     and re.fullmatch("[0-9a-f]{64}", fact.sha256), "invalid file identity")
                all_paths.append(fact.path)
        need(len(all_paths) == len(set(all_paths)), "repeated file identity")
        need(all(candidate(f, frozenset()) for f in plan.candidates), "invalid cache candidate class")
        need(tuple(sorted(plan.excluded, key=lambda f: (f.path, f.reason))) == plan.excluded, "unordered exclusions")
        for item in plan.excluded:
            relative(item.path)
            need(item.reason in {"symlink", "volume", "nested-git", "nonregular"}
                 and any(beneath(scope, item.path) or beneath(item.path, scope) for scope in plan.scopes)
                 and not beneath(item.path, WORKSPACE), "invalid scoped exclusion")
        excluded_paths = [item.path for item in plan.excluded]
        excluded_set = set(excluded_paths)
        need(len(excluded_paths) == len(excluded_set)
             and not any("/".join(path.split("/")[:n]) in excluded_set
                         for path in all_paths for n in range(1, len(path.split("/")) + 1)),
             "overlapping excluded and file populations")
        need(len(all_paths) + len(plan.excluded) <= plan.limits.records
             and sum(f.byte_size for f in (*plan.candidates, *plan.retained)) <= plan.limits.hash_bytes, "plan totals exceed limits")
        need(tuple(sorted(set(plan.strays))) == plan.strays
             and set(plan.strays) <= {f.path for f in plan.retained}, "strays must be distinct retained files")
        return plan
    except (TypeError, ValueError, KeyError, AttributeError, UnicodeError, RecursionError) as error:
        if isinstance(error, CleanupError):
            raise
        raise CleanupError("refused", "invalid plan: " + type(error).__name__) from error


def check_plan(root: Path, plan: Plan, *, phase="before") -> Finding:
    try:
        need(phase in {"before", "after"}, "invalid check phase")
        plan = decode_plan(encode_plan(plan))
        fresh = make_plan(root, workdir=plan.workdir, scopes=plan.scopes, limits=plan.limits)
        if phase == "before":
            matched = replace(fresh, created_utc=plan.created_utc) == plan
        else:
            matched = (not fresh.candidates and fresh.retained == plan.retained and fresh.excluded == plan.excluded
                       and fresh.device == plan.device and fresh.tracked_sha256 == plan.tracked_sha256
                       and fresh.instrument == plan.instrument and fresh.strays == plan.strays)
        need(matched, "scoped cohort or authority changed", "stale")
        return _summary(plan, reason="scoped " + phase + " state matches; no process attribution")
    except CleanupError as error:
        return Finding(error.disposition, error.reason)
    except Boundary as error:
        return Finding("refused", "unsafe source boundary: " + error.reason)
    except subprocess.TimeoutExpired:
        return Finding("unavailable", "Git read timed out")
    except OSError as error:
        return Finding("unavailable", "filesystem/Git read: " + type(error).__name__ + " errno=" + str(error.errno))


def publish_plan(root: Path, plan: Plan):
    """Exclusive bounded publication under the reserved workspace; preserve failed files."""
    plan = decode_plan(encode_plan(plan))
    root = runtime_root(root)
    tracked = tracked_paths(root)
    need(hashlib.sha256(b"\0".join(p.encode() for p in sorted(tracked))).hexdigest() == plan.tracked_sha256,
         "tracked inventory changed before publication", "stale")
    raw = encode_plan(plan)
    try:
        with OwnedRoot(root) as owned:
            need(owned.device == plan.device and _instrument(owned) == plan.instrument,
                 "plan authority changed before publication", "stale")
            with owned.directory(plan.workdir, create=True) as directory:
                descriptor = os.open("plan.json", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                     0o600, dir_fd=directory)
                try:
                    cursor = 0
                    while cursor < len(raw):
                        written = os.write(descriptor, raw[cursor:])
                        need(written > 0, "plan write made no progress", "unavailable")
                        cursor += written
                    os.fsync(descriptor)
                finally:
                    os.close(descriptor)
    except Boundary as error:
        raise CleanupError("refused", "unsafe workspace: " + error.reason) from error


def load_plan(root: Path, workdir: str) -> Plan:
    root = runtime_root(root)
    _selection(workdir, DEFAULT_SCOPES)
    try:
        with OwnedRoot(root) as owned, owned.directory(workdir) as directory:
            _, raw = owned.snapshot(directory, "plan.json", workdir + "/plan.json", PLAN_BYTES, payload=True)
        plan = decode_plan(raw)
        need(plan.workdir == workdir, "plan belongs to another workspace")
        return plan
    except Boundary as error:
        raise CleanupError("refused", "unsafe workspace: " + error.reason) from error


def main():
    parser = argparse.ArgumentParser(description="\n".join(USAGE.splitlines()[1:-1]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--plan", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--check-after", action="store_true")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--scope", action="append")
    args = parser.parse_args()
    try:
        if args.plan:
            scopes = tuple(sorted(args.scope)) if args.scope else DEFAULT_SCOPES
            plan = make_plan(ROOT, workdir=args.workdir, scopes=scopes)
            publish_plan(ROOT, plan)
            report = asdict(_summary(plan, "planned", "exclusive plan published; no cache deletion"))
            report["plan"] = args.workdir + "/plan.json"
        else:
            need(not args.scope, "check uses the saved scopes")
            result = check_plan(ROOT, load_plan(ROOT, args.workdir), phase="after" if args.check_after else "before")
            report = asdict(result)
    except CleanupError as error:
        report = dict(disposition=error.disposition, reason=error.reason)
    except Boundary as error:
        report = dict(disposition="refused", reason="unsafe source boundary: " + error.reason)
    except (OSError, subprocess.TimeoutExpired) as error:
        report = dict(disposition="unavailable", reason="filesystem/Git operation: " + type(error).__name__)
    except (UnicodeError, ValueError, RecursionError) as error:
        report = dict(disposition="refused", reason="invalid input: " + type(error).__name__)
    print(json.dumps(report, sort_keys=True))
    return 0 if report["disposition"] in {"planned", "matched"} else 1 if report["disposition"] == "stale" else 2


if __name__ == "__main__":
    sys.exit(main())
