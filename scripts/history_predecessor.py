#!/usr/bin/env python3
"""Preserve live history predecessors in working files and the proposed commit.

The pure entry module owns splitting/wrappers shared with the sharder. This guard proves
complete old entries remain an exact ordered suffix of each logical head plus
new shards. New records precede them; corrections never rewrite old records.
The existing partition judge additionally checks the complete staged corpus.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

import history_archive as H
import history_entries as S

ROOT = Path(__file__).resolve().parent.parent
HEADS = ('CHANGELOG.md', 'DEV_NOTES.md')
MAX_SNAPSHOT_BYTES = 8 * 1024 * 1024
MAX_SNAPSHOT_FILES = 1024
SHARD = re.compile(r'docs/changelog/shard-([0-9]{4,})\.md\Z')


class HistoryChanged(ValueError):
    """The proposed history does not preserve its predecessor."""


class HistoryRefused(ValueError):
    """An input/read cannot support a verdict."""


def relevant(name):
    return (name in HEADS or name == H.MANIFEST or name.startswith('docs/history/') or
            (name.startswith('docs/changelog/') and name.count('/') == 2 and name.endswith('.md')))


def safe_name(name):
    path = PurePosixPath(name)
    if (len(name.encode('utf-8')) > 256 or any(ord(c) < 32 for c in name) or
            path.is_absolute() or '..' in path.parts or str(path) != name or '\\' in name):
        raise HistoryRefused('unsafe history path ' + name)


def run_git(root, *args, input=None):
    result = subprocess.run(['git', '--no-optional-locks', '-C', str(root), *args],
                            input=input, capture_output=True)
    if result.returncode:
        raise HistoryRefused('Git read failed: ' + ' '.join(args) + ': ' +
                             result.stderr.decode('utf-8', errors='replace').strip())
    return result.stdout


def git_snapshot(root, revision='HEAD'):
    """Read a closed Git inventory and immutable blob IDs; failed reads never mean absent."""
    if revision == ':':
        inventory = run_git(root, 'ls-files', '--stage', '-z')
    else:
        inventory = run_git(root, 'ls-tree', '-rz', '--full-tree', revision)
    objects = {}
    for row in inventory.split(b'\0'):
        if not row:
            continue
        metadata, raw_name = row.split(b'\t', 1)
        name = raw_name.decode('utf-8')
        if not relevant(name):
            continue
        safe_name(name)
        fields = metadata.decode('ascii').split()
        if revision == ':':
            mode, oid, stage = fields
            if stage != '0':
                raise HistoryRefused('unmerged history path ' + name)
        else:
            mode, kind, oid = fields
            if kind != 'blob':
                raise HistoryRefused('non-blob history path ' + name)
        if mode not in {'100644', '100755'} or name in objects:
            raise HistoryRefused('unsafe/duplicate history path ' + name)
        objects[name] = oid
        if len(objects) > MAX_SNAPSHOT_FILES:
            raise HistoryRefused('history snapshot exceeds file bound')
    if not objects:
        return {}
    requests = ''.join(oid + '\n' for oid in objects.values()).encode('ascii')
    sizes = run_git(root, 'cat-file', '--batch-check', input=requests).splitlines()
    if len(sizes) != len(objects):
        raise HistoryRefused('incomplete Git size response')
    expected = []
    for (name, oid), row in zip(objects.items(), sizes):
        fields = row.decode('ascii').split()
        if len(fields) != 3 or fields[:2] != [oid, 'blob'] or not fields[2].isdigit():
            raise HistoryRefused('invalid Git blob size response ' + name)
        expected.append((name, oid, int(fields[2])))
    if sum(size for _, _, size in expected) > MAX_SNAPSHOT_BYTES:
        raise HistoryRefused('history snapshot exceeds byte bound')
    stream = run_git(root, 'cat-file', '--batch', input=requests)
    result, cursor = {}, 0
    for name, oid, size in expected:
        newline = stream.find(b'\n', cursor)
        if newline < 0 or stream[cursor:newline] != f'{oid} blob {size}'.encode('ascii'):
            raise HistoryRefused('invalid Git blob response ' + name)
        start = newline + 1
        if stream[start + size:start + size + 1] != b'\n':
            raise HistoryRefused('incomplete Git blob ' + name)
        result[name] = stream[start:start + size]
        cursor = start + size + 1
    if cursor != len(stream):
        raise HistoryRefused('surplus Git blob output')
    return result


def owned_path(root, name):
    safe_name(name)
    path = PurePosixPath(name)
    cursor = root
    for part in path.parts:
        cursor /= part
        marker = cursor / '.git'
        if cursor.is_symlink() or marker.exists() or marker.is_symlink():
            raise HistoryRefused('symlink/Git boundary in history path ' + name)
        if cursor.exists() and cursor.stat().st_dev != root.stat().st_dev:
            raise HistoryRefused('off-volume history path ' + name)
    return cursor


def working_snapshot(root):
    names = set(HEADS) | {H.MANIFEST}
    shards = owned_path(root, 'docs/changelog')
    if shards.is_dir():
        names.update(p.relative_to(root).as_posix() for p in shards.glob('*.md'))
    archive = owned_path(root, 'docs/history')
    if archive.is_dir():
        for directory, subdirs, files in os.walk(archive, followlinks=False):
            parent = Path(directory)
            owned_path(root, parent.relative_to(root).as_posix())
            for child in subdirs:
                owned_path(root, (parent / child).relative_to(root).as_posix())
            names.update((parent / f).relative_to(root).as_posix() for f in files)
    if len(names) > MAX_SNAPSHOT_FILES:
        raise HistoryRefused('history snapshot exceeds file bound')
    snapshot, consumed = {}, 0
    for name in sorted(names):
        path = owned_path(root, name)
        if not path.exists():
            continue
        if not path.is_file():
            raise HistoryRefused('history path is not a regular file ' + name)
        with path.open('rb') as stream:
            blob = stream.read(MAX_SNAPSHOT_BYTES - consumed + 1)
        consumed += len(blob)
        if consumed > MAX_SNAPSHOT_BYTES:
            raise HistoryRefused('history snapshot exceeds byte bound')
        snapshot[name] = blob
    return snapshot


def rows(snapshot):
    result = {}
    for row in snapshot.get(H.MANIFEST, b'').decode('utf-8').splitlines():
        match = H.ROW.fullmatch(row)
        if not match or match[2] in result:
            raise HistoryChanged('malformed/duplicate live manifest row')
        result[match[2]] = match[1]
    return result


def entries(blob):
    text = blob.decode('utf-8')
    if not re.search(r'^## ', text, re.M):
        return blob, []
    preamble, records = S.split_entries(text)
    return preamble.encode('utf-8'), [(key, body.encode('utf-8')) for key, body in records]


def verify(previous, current, ceilings):
    """Pure predecessor proof; the existing judge owns full partition authentication."""
    old_rows, new_rows = rows(previous), rows(current)
    moved = {head: [] for head in HEADS}
    for name in sorted(new_rows.keys() - old_rows.keys(),
                       key=lambda name: int(SHARD.fullmatch(name)[1]) if SHARD.fullmatch(name) else -1,
                       reverse=True):
        if not SHARD.fullmatch(name) or name in previous or name not in current:
            raise HistoryChanged('not a new published shard ' + name)
        blob = current[name]
        if hashlib.sha256(blob).hexdigest() != new_rows[name]:
            raise HistoryChanged('new shard digest differs ' + name)
        preamble, records = entries(blob)
        if not records:
            raise HistoryChanged('new shard has no entries ' + name)
        owner = next((head for head in HEADS if preamble.startswith(
            ('# ' + head[:-3] + ' shard — ').encode('utf-8'))), None)
        if owner is None:
            raise HistoryChanged('new shard has no declared head ' + name)
        wrapper = S.SHARD_HEADER.format(head=owner[:-3], kib=ceilings[owner] // 1024,
                                        first=records[0][0].split()[0],
                                        last=records[-1][0].split()[0]).encode('utf-8')
        if preamble != wrapper:
            raise HistoryChanged('new shard wrapper differs ' + name)
        moved[owner].extend(records)
    checked = total = 0
    for head in HEADS:
        if head not in previous:
            continue  # No predecessor is asserted for a genuinely absent closed-inventory path.
        if head not in current:
            raise HistoryChanged('removed live history head ' + head)
        before, old_entries = entries(previous[head])
        after, current_entries = entries(current[head])
        logical = current_entries + moved[head]
        if before != after:
            raise HistoryChanged('changed history preamble ' + head)
        if old_entries and (not current_entries or logical[-len(old_entries):] != old_entries):
            raise HistoryChanged('changed/missing/reordered predecessor entries ' + head)
        ids = [key for key, _ in logical]
        if len(ids) != len(set(ids)):
            raise HistoryChanged('duplicated logical head entry ' + head)
        checked += 1
        total += len(old_entries)
    return checked, total


def judge_index(previous, proposed, scratch):
    """Reuse the existing partition judge for staged manifest/shards/sealed inputs."""
    before, after = scratch / 'before', scratch / 'index'
    for directory, snapshot in [(before, previous), (after, proposed)]:
        directory.mkdir()
        for name, blob in snapshot.items():
            path = owned_path(directory, name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(blob)
    prev_index = before / H.INDEX
    prev_manifest = before / H.MANIFEST
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/check_history_partition.py'),
                             str(prev_index) if prev_index.is_file() else '', str(after),
                             'docs/changelog', H.MANIFEST,
                             str(prev_manifest) if prev_manifest.is_file() else '', *HEADS],
                            capture_output=True, text=True)
    if result.returncode == 1:
        raise HistoryChanged('staged partition: ' + result.stdout.strip())
    if result.returncode != 0:
        raise HistoryRefused('staged partition cannot judge: ' + (result.stdout + result.stderr).strip())


def main():
    if len(sys.argv) != 1:
        print('usage: history_predecessor.py', file=sys.stderr)
        return 2
    try:
        previous = git_snapshot(ROOT)
        proposed = git_snapshot(ROOT, ':')
        working = working_snapshot(ROOT)
        ceilings = {head: S.registry_ceiling(ROOT, head) for head in HEADS}
        counts = [verify(previous, snapshot, ceilings) for snapshot in [proposed, working]]
        parent = owned_path(ROOT, 'target/history-predecessor')
        parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='index-', dir=parent) as directory:
            judge_index(previous, proposed, Path(directory))
    except HistoryChanged as exc:
        print('HISTORY-PREDECESSOR: changed — ' + str(exc))
        return 1
    except (HistoryRefused, S.ShardRefused, OSError, UnicodeError, ValueError) as exc:
        print('HISTORY-PREDECESSOR: REFUSED — ' + str(exc))
        return 2
    print(f'HISTORY-PREDECESSOR: ok (index/working each {counts[0][0]} heads, '
          f'{counts[0][1]} complete predecessor entries; staged partition authenticated)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
