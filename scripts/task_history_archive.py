#!/usr/bin/env python3
"""Verify/read the approved finite P4 history seal, without Git or extraction.

This is a closed capture, not an appendable archive service. Both the immutable
descriptor and every original member authenticate before any bytes reach stdout.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tarfile
import zlib

INDEX = 'docs/task-history/descriptor.json'
FRONT = 'docs/task-history/README.md'
MANIFEST = 'docs/history/task-history-manifest.json'  # Original sealed member name.
INDEX_SHA256 = 'befe1401d3e8b80abc824dc1ec0c6eb5c5d2d12ae00f46221e5bdc3eb29e6516'
PATHS = ('docs/tasks/archive/P4-SYSTEM.md',) + tuple(
    f'docs/tasks/archive/P4-SYSTEM-{n}.md' for n in range(2, 13))
MAX_INDEX_BYTES = 8192
MAX_FRONT_BYTES = 4096
MAX_OBJECT_BYTES = 400000
MAX_TAR_BYTES = 2 * 1024 * 1024
MAX_MEMBER_BYTES = 131072
FIELDS = {'schema_version', 'kind', 'capture', 'approved_on', 'object', 'sha256',
          'compressed_bytes', 'tar_bytes', 'source_files', 'source_bytes',
          'source_lines', 'manifest', 'manifest_bytes', 'manifest_sha256', 'anchors'}


class ArchiveRefused(ValueError):
    """The terminal cannot supply authenticated original bytes."""


def require(condition, reason):
    if not condition:
        raise ArchiveRefused(reason)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def json_object(data):
    try:
        return json.loads(data, object_pairs_hook=unique_object)
    except ArchiveRefused:
        raise
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise ArchiveRefused('malformed archive JSON') from exc


def identity(value, width):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{' + str(width) + '}', value)


def positive(value, bound):
    return type(value) is int and 0 < value <= bound


def parse_descriptor(data):
    require(len(data) <= MAX_INDEX_BYTES, 'descriptor exceeds bound')
    row = json_object(data)
    require(isinstance(row, dict) and set(row) == FIELDS, 'unknown descriptor fields')
    require(type(row['schema_version']) is int and row['schema_version'] == 1
            and row['kind'] == 'sealed-task-history', 'unsupported descriptor schema')
    for name, width in (('capture', 40), ('sha256', 64), ('manifest_sha256', 64)):
        require(identity(row[name], width), 'malformed descriptor identity')
    require(row['approved_on'] == '2026-10-10', 'unknown approval boundary')
    require(row['object'] == f"docs/task-history/sealed/{row['sha256']}.tar.gz",
            'unsafe archive object path')
    require(row['manifest'] == MANIFEST, 'unknown manifest path')
    for name, bound in (('compressed_bytes', MAX_OBJECT_BYTES), ('tar_bytes', MAX_TAR_BYTES),
                        ('source_files', len(PATHS)), ('source_bytes', MAX_TAR_BYTES),
                        ('source_lines', MAX_TAR_BYTES), ('manifest_bytes', MAX_INDEX_BYTES)):
        require(positive(row[name], bound), 'descriptor count exceeds bound or is not an integer')
    require(row['source_files'] == len(PATHS), 'finite capture count differs')
    anchors = row['anchors']
    require(isinstance(anchors, dict) and set(anchors) <= set(PATHS), 'unknown navigation path')
    for values in anchors.values():
        require(isinstance(values, list) and len(values) <= 32, 'navigation anchors exceed bound')
        require(all(isinstance(v, str) and re.fullmatch(r'[a-z0-9-]{1,80}', v) for v in values),
                'unsafe navigation anchor')
        require(len(values) == len(set(values)), 'duplicate navigation anchor')
    return row


def read_file(root, name, bound):
    """Read only a bounded regular file on the repository volume; no symlink hops."""
    require(isinstance(name, str), 'unsafe filesystem path')
    parts = PurePosixPath(name)
    require(not parts.is_absolute() and '..' not in parts.parts and str(parts) == name,
            'unsafe filesystem path')
    path = root
    volume = root.stat().st_dev
    for part in parts.parts:
        path = path / part
        mode = path.lstat()
        require(not stat.S_ISLNK(mode.st_mode), 'symlink in archive path')
        require(mode.st_dev == volume, 'off-volume archive path')
    require(stat.S_ISREG(mode.st_mode), 'archive path is not a regular file')
    require(mode.st_size <= bound, 'archive file exceeds bound')
    with path.open('rb') as stream:
        data = stream.read(bound + 1)
    require(len(data) <= bound, 'archive file exceeds bound')
    return data


def canonical_tar(items):
    """The documented USTAR encoding also rejects hidden headers/trailing data."""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w', format=tarfile.USTAR_FORMAT) as archive:
        for name, data in items:
            member = tarfile.TarInfo(name)
            member.size, member.mode = len(data), 0o644
            archive.addfile(member, io.BytesIO(data))
    return buffer.getvalue()


def inspect_object(blob, row):
    require(len(blob) == row['compressed_bytes'], 'object byte count differs')
    require(digest(blob) == row['sha256'], 'object digest differs')
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(blob)) as compressed:
            raw = compressed.read(row['tar_bytes'] + 1)
        require(len(raw) <= row['tar_bytes'], 'archive expansion exceeds bound')
        require(len(raw) == row['tar_bytes'], 'tar byte count differs')
        members = {}
        with tarfile.open(fileobj=io.BytesIO(raw), mode='r:') as archive:
            for member in archive:
                require(member.name in (*PATHS, MANIFEST), 'unknown or unsafe archive member')
                require(member.name not in members, 'duplicate archive member')
                require(member.type == tarfile.REGTYPE and not member.issparse()
                        and not member.pax_headers, 'archive member must be a plain regular file')
                require(positive(member.size, MAX_MEMBER_BYTES), 'archive member exceeds bound')
                require(len(members) < len(PATHS) + 1, 'extra archive member')
                members[member.name] = archive.extractfile(member).read()
    except (OSError, EOFError, tarfile.TarError, zlib.error) as exc:
        raise ArchiveRefused('unreadable archive object') from exc
    require(set(members) == set(PATHS) | {MANIFEST}, 'archive member census differs')
    require(raw == canonical_tar(members.items()), 'noncanonical tar encoding')
    manifest = members.pop(MANIFEST)
    require(len(manifest) == row['manifest_bytes'] and digest(manifest) == row['manifest_sha256'],
            'manifest identity differs')
    data = json_object(manifest)
    require(isinstance(data, dict) and set(data) == {'schema_version', 'kind', 'capture', 'members'},
            'unknown manifest fields')
    require(type(data['schema_version']) is int and data['schema_version'] == 1
            and data['kind'] == 'task-history-review' and data['capture'] == row['capture'],
            'manifest capture differs')
    rows = data['members']
    require(isinstance(rows, list) and len(rows) == len(PATHS), 'manifest member count differs')
    seen = set()
    for entry in rows:
        require(isinstance(entry, dict) and set(entry) == {'path', 'sha256', 'bytes', 'lines'},
                'unknown manifest member fields')
        name = entry['path']
        require(isinstance(name, str) and name in PATHS, 'unknown manifest member path')
        require(name not in seen, 'duplicate manifest member')
        seen.add(name)
        require(identity(entry['sha256'], 64) and positive(entry['bytes'], MAX_MEMBER_BYTES)
                and positive(entry['lines'], MAX_MEMBER_BYTES), 'malformed manifest member identity')
        original = members[name]
        require(len(original) == entry['bytes'] and original.count(b'\n') == entry['lines']
                and digest(original) == entry['sha256'], f'original member identity differs: {name}')
        try:
            original.decode('utf-8')
        except UnicodeError as exc:
            raise ArchiveRefused('original member is not UTF-8') from exc
    require(sum(map(len, members.values())) == row['source_bytes'], 'source byte count differs')
    require(sum(b.count(b'\n') for b in members.values()) == row['source_lines'],
            'source line count differs')
    return rows, members


def navigation_stub(entry, row):
    name = entry['path']
    text = (f'# Sealed P4 task history — {PurePosixPath(name).name}\n\n'
            'The complete original narrative is preserved in the '
            '[verified history archive](../../task-history/README.md).\n'
            'This page retains its former path and incoming section anchors.\n\n'
            'Read the original from the repository root:\n\n```sh\n'
            f'python3 scripts/task_history_archive.py --read {name}\n```\n\n'
            f"Capture: `{row['capture']}`. Original: {entry['bytes']} bytes / "
            f"{entry['lines']} lines. SHA-256:\n`{entry['sha256']}`.\n")
    for anchor in row['anchors'].get(name, []):
        text += (f'\n<a id="{anchor}"></a>\n\n'
                 f'Original `{anchor}` section: read the complete logical file above.\n')
    return text.encode()


def terminal_files(root):
    """Census bounded to this finite terminal; directories cannot hide extra files."""
    found = set()
    stack = [root / 'docs/task-history']
    entries = 0
    while stack:
        for path in stack.pop().iterdir():
            entries += 1
            require(entries <= 4, 'finite terminal coverage differs')
            mode = path.lstat()
            require(not stat.S_ISLNK(mode.st_mode), 'symlink in archive terminal')
            require(mode.st_dev == root.stat().st_dev, 'off-volume archive terminal')
            if stat.S_ISDIR(mode.st_mode):
                require(path == root / 'docs/task-history/sealed', 'unknown terminal directory')
                stack.append(path)
            else:
                require(stat.S_ISREG(mode.st_mode), 'terminal path is not a regular file')
                found.add(path.relative_to(root).as_posix())
    return found


def load_terminal(root, previous=None):
    root = root.resolve()
    encoded = read_file(root, INDEX, MAX_INDEX_BYTES)
    row = parse_descriptor(encoded)
    require(digest(encoded) == INDEX_SHA256, 'approved descriptor identity differs')
    if previous is not None:
        require(encoded == previous, 'changed committed descriptor')
    read_file(root, FRONT, MAX_FRONT_BYTES)
    require(terminal_files(root) == {INDEX, FRONT, row['object']}, 'finite terminal coverage differs')
    rows, members = inspect_object(read_file(root, row['object'], MAX_OBJECT_BYTES), row)
    for entry in rows:
        require(read_file(root, entry['path'], MAX_FRONT_BYTES) == navigation_stub(entry, row),
                f'navigation stub differs: {entry["path"]}')
    return row, rows, members


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--read', metavar='FORMER_PATH')
    action.add_argument('--list', action='store_true', help='list authenticated logical paths')
    parser.add_argument('--previous', type=Path, help='gate-only committed descriptor comparison')
    args = parser.parse_args()
    try:
        previous = None
        if args.previous is not None:
            try:
                relative = args.previous.absolute().relative_to(args.root.resolve()).as_posix()
            except ValueError as exc:
                raise ArchiveRefused('previous descriptor is outside repository') from exc
            previous = read_file(args.root.resolve(), relative, MAX_INDEX_BYTES)
        row, rows, members = load_terminal(args.root, previous)
        if args.read is not None:
            require(args.read in members, 'unknown archived logical path')
            sys.stdout.buffer.write(members[args.read])
        elif args.list:
            print('\n'.join(entry['path'] for entry in rows))
        else:
            print(f'TASK-HISTORY: ok ({len(members)} originals, {row["source_bytes"]} authenticated bytes)')
    except (ArchiveRefused, OSError) as exc:
        print(f'TASK-HISTORY: REFUSED — {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
