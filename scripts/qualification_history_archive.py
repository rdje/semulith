#!/usr/bin/env python3
"""Read the finite LC0041 qualification capture, without Git or extraction.

Four completed qualification records and one prior book-source snapshot retain
their exact bytes and Git identities. Every member and navigation page verifies
before output. Shared JSON/USTAR codecs belong to this repository; the separate
P4 terminal and its published contract remain unchanged.
"""
from __future__ import annotations

import argparse
import datetime
import gzip
import hashlib
import html
import io
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import stat
import sys
import tarfile
import zlib

import task_history_archive as T

PROJECT = Path(__file__).resolve().parent.parent
INDEX = 'docs/qualification-history/descriptor.json'
FRONT = 'docs/qualification-history/README.md'
MANIFEST = 'docs/qualification-history/source-manifest.json'
SOURCE = '968bc0109682628609ae6b83bc7bf42b01fc9b2c'
INDEX_SHA256 = '9d9011027eecc3ed0701fcdd886539333500b877cac0773f12e58d23756e9684'
RETIRED = tuple('docs/tasks/artifacts/live-containment/' + name + '.md' for name in
                ['book-index-consumer', 'graph-census', 'include-readers', 'orientation-indexes'])
BOOK = 'docs/book/src/working/task-trees.md'
PATHS = tuple(sorted([*RETIRED, BOOK]))
MAX_INDEX_BYTES = 8192
MAX_FRONT_BYTES = 4096
MAX_OBJECT_BYTES = 196608
MAX_TAR_BYTES = 524288
MAX_MEMBER_BYTES = 131072
FIELDS = {'schema_version', 'kind', 'source', 'source_tree_sha256', 'recorded_on',
          'authority', 'object', 'sha256', 'compressed_bytes', 'tar_bytes',
          'source_files', 'source_bytes', 'source_lines', 'manifest',
          'manifest_bytes', 'manifest_sha256', 'members'}
MEMBER_FIELDS = {'original_path', 'role', 'mode', 'git_oid', 'bytes', 'lines', 'sha256',
                 'anchors', 'stub_sha256'}
ArchiveRefused = T.ArchiveRefused
require, digest = T.require, T.digest


def owned_root(value):
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT / path
    try:
        relative = path.relative_to(PROJECT)
    except ValueError as exc:
        raise ArchiveRefused('archive root is outside this project') from exc
    require('..' not in relative.parts, 'unsafe archive root')
    cursor = PROJECT
    for part in relative.parts:
        cursor /= part
        info = cursor.lstat()
        require(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode),
                'archive root is not an owned real directory')
        require(info.st_dev == PROJECT.stat().st_dev, 'off-volume archive root')
        require(not (cursor / '.git').exists() and not (cursor / '.git').is_symlink(),
                'Git boundary in archive root')
    return path


def read_file(root, name, bound):
    """Return Git mode/bytes after bounded, stable, owned-file reads."""
    require(isinstance(name, str) and len(name.encode()) <= 256, 'unsafe archive path')
    parts = PurePosixPath(name)
    require(parts.parts and not parts.is_absolute() and '..' not in parts.parts
            and str(parts) == name and '\\' not in name
            and all(32 <= ord(c) != 127 for c in name), 'unsafe archive path')
    cursor = root
    for part in parts.parts:
        cursor /= part
        info = cursor.lstat()
        require(not stat.S_ISLNK(info.st_mode), 'symlink in archive path')
        require(info.st_dev == root.stat().st_dev, 'off-volume archive path')
        if stat.S_ISDIR(info.st_mode):
            require(not (cursor / '.git').exists() and not (cursor / '.git').is_symlink(),
                    'Git boundary in archive path')
    require(stat.S_ISREG(info.st_mode) and info.st_size <= bound, 'archive file exceeds bound or is not regular')
    require(hasattr(os, 'O_NOFOLLOW'), 'no-follow file reads unavailable')
    descriptor = os.open(cursor, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
    with os.fdopen(descriptor, 'rb') as stream:
        opened = os.fstat(stream.fileno())
        require(stat.S_ISREG(opened.st_mode) and opened.st_dev == info.st_dev
                and opened.st_ino == info.st_ino, 'archive input changed before read')
        body = stream.read(bound + 1)
        after = os.fstat(stream.fileno())
    stable = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_mode)
    require(stable(info) == stable(after) and len(body) == info.st_size <= bound,
            'archive input changed during read')
    return ('100755' if info.st_mode & stat.S_IXUSR else '100644', body)


def parse_descriptor(body):
    require(len(body) <= MAX_INDEX_BYTES, 'descriptor exceeds bound')
    row = T.json_object(body)
    require(isinstance(row, dict) and set(row) == FIELDS, 'unknown qualification descriptor fields')
    require(type(row['schema_version']) is int and row['schema_version'] == 1
            and row['kind'] == 'sealed-qualification-history', 'unsupported qualification schema')
    require(row['source'] == SOURCE and T.identity(row['source_tree_sha256'], 64),
            'unknown qualification capture')
    require(row['authority'] == 'director-session-archive-delegation', 'unknown archive authority')
    require(isinstance(row['recorded_on'], str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', row['recorded_on']),
            'invalid archive record date')
    try:
        datetime.date.fromisoformat(row['recorded_on'])
    except ValueError as exc:
        raise ArchiveRefused('invalid archive record date') from exc
    require(T.identity(row['sha256'], 64) and T.identity(row['manifest_sha256'], 64),
            'malformed archive identity')
    require(row['object'] == f"docs/qualification-history/sealed/{row['sha256']}.tar.gz",
            'unsafe qualification object path')
    require(row['manifest'] == MANIFEST, 'unknown qualification manifest')
    for name, bound in [('compressed_bytes', MAX_OBJECT_BYTES), ('tar_bytes', MAX_TAR_BYTES),
                        ('source_files', len(PATHS)), ('source_bytes', MAX_TAR_BYTES),
                        ('source_lines', MAX_TAR_BYTES), ('manifest_bytes', MAX_INDEX_BYTES)]:
        require(T.positive(row[name], bound), 'archive count exceeds bound or is not an integer')
    require(row['source_files'] == len(PATHS), 'finite qualification count differs')
    members = row['members']
    require(isinstance(members, list) and len(members) == len(PATHS), 'qualification member count differs')
    for name, entry in zip(PATHS, members):
        require(isinstance(entry, dict) and set(entry) == MEMBER_FIELDS, 'unknown qualification member fields')
        require(entry['original_path'] == name and entry['mode'] == '100644', 'qualification member path/mode differs')
        require(T.identity(entry['git_oid'], 40) and T.identity(entry['sha256'], 64)
                and T.positive(entry['bytes'], MAX_MEMBER_BYTES)
                and T.positive(entry['lines'], MAX_MEMBER_BYTES), 'malformed original identity')
        require(entry['role'] == ('qualification' if name in RETIRED else 'book-source-snapshot'),
                'unknown qualification member role')
        anchors = entry['anchors']
        require(isinstance(anchors, list) and len(anchors) <= 64
                and all(isinstance(v, str) and re.fullmatch(r'[a-z0-9_-]{1,160}', v) for v in anchors)
                and len(set(anchors)) == len(anchors), 'invalid original heading aliases')
        require((name in RETIRED and bool(anchors) and T.identity(entry['stub_sha256'], 64))
                or (name == BOOK and not anchors and entry['stub_sha256'] is None),
                'qualification navigation role differs')
    return row


def navigation_stub(entry, row):
    name = entry['original_path']
    front = posixpath.relpath(FRONT, str(PurePosixPath(name).parent))
    text = (f'# Sealed qualification record — {PurePosixPath(name).name}\n\n'
            f'The complete original is retained in the [qualification archive]({front}).\n'
            'This is a navigation page, not the historical record. From the repository root:\n\n'
            '```sh\n'
            f'python3 scripts/qualification_history_archive.py --read {name}\n```\n\n'
            f"Capture: `{row['source']}`. Original: {entry['bytes']} bytes / {entry['lines']} LF lines.\n"
            f"SHA-256: `{entry['sha256']}`. Git mode: `{entry['mode']}`.\n")
    for anchor in entry['anchors']:
        text += (f'\n<a id="{html.escape(anchor, quote=True)}"></a>\n\n'
                 f'Original `{anchor}` section: retrieve the complete record above.\n')
    return text.encode()


def inspect_object(blob, row):
    require(len(blob) == row['compressed_bytes'] and digest(blob) == row['sha256'],
            'qualification object identity differs')
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(blob)) as compressed:
            raw = compressed.read(row['tar_bytes'] + 1)
        require(len(raw) == row['tar_bytes'], 'qualification expansion differs or exceeds bound')
        members = {}
        with tarfile.open(fileobj=io.BytesIO(raw), mode='r:') as archive:
            for item in archive:
                require(item.name in (*PATHS, MANIFEST), 'unknown or unsafe qualification member')
                require(item.name not in members, 'duplicate qualification member')
                require(item.type == tarfile.REGTYPE and not item.issparse() and not item.pax_headers,
                        'qualification member is not a plain regular file')
                require(T.positive(item.size, MAX_MEMBER_BYTES), 'qualification member exceeds bound')
                require(len(members) < len(PATHS) + 1, 'extra qualification member')
                members[item.name] = archive.extractfile(item).read()
    except (OSError, EOFError, zlib.error, tarfile.TarError) as exc:
        raise ArchiveRefused('unreadable qualification object') from exc
    require(list(members) == [*PATHS, MANIFEST], 'complete qualification member order/census differs')
    require(raw == T.canonical_tar(members.items()), 'noncanonical qualification tar encoding')
    manifest = members.pop(MANIFEST)
    require(len(manifest) == row['manifest_bytes'] and digest(manifest) == row['manifest_sha256'],
            'qualification manifest identity differs')
    expected = {'schema_version': 1, 'kind': 'qualification-history-source', 'source': row['source'],
                'source_tree_sha256': row['source_tree_sha256'], 'members': row['members']}
    require(T.json_object(manifest) == expected, 'complete qualification manifest differs')
    for entry in row['members']:
        body = members[entry['original_path']]
        require(len(body) == entry['bytes'] and body.count(b'\n') == entry['lines']
                and digest(body) == entry['sha256'], 'original qualification identity differs')
        oid = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        require(oid == entry['git_oid'], 'original Git blob identity differs')
        try:
            body.decode('utf-8')
        except UnicodeError as exc:
            raise ArchiveRefused('original qualification is not UTF-8') from exc
    require(sum(map(len, members.values())) == row['source_bytes'], 'qualification source bytes differ')
    require(sum(body.count(b'\n') for body in members.values()) == row['source_lines'],
            'qualification source lines differ')
    return members


def terminal_files(root):
    found, pending, count = set(), [root / 'docs/qualification-history'], 0
    while pending:
        for path in pending.pop().iterdir():
            count += 1
            require(count <= 4, 'finite qualification terminal coverage differs')
            info = path.lstat()
            require(not stat.S_ISLNK(info.st_mode) and info.st_dev == root.stat().st_dev,
                    'symlink or off-volume qualification terminal')
            if stat.S_ISDIR(info.st_mode):
                require(path == root / 'docs/qualification-history/sealed', 'unknown qualification directory')
                require(not (path / '.git').exists(), 'Git boundary in qualification terminal')
                pending.append(path)
            else:
                require(stat.S_ISREG(info.st_mode), 'qualification terminal path is not regular')
                found.add(path.relative_to(root).as_posix())
    return found


def validate_view(files):
    """Authenticate either filesystem or staged byte/mode inputs, without Git."""
    require(INDEX in files and files[INDEX][0] == '100644', 'qualification descriptor unavailable or mode differs')
    encoded = files[INDEX][1]
    row = parse_descriptor(encoded)
    require(digest(encoded) == INDEX_SHA256, 'captured qualification descriptor identity differs')
    require(set(files) == {INDEX, FRONT, row['object'], *RETIRED}, 'qualification view coverage differs')
    require(all(mode == '100644' for mode, body in files.values()), 'qualification view Git mode differs')
    require(len(files[FRONT][1]) <= MAX_FRONT_BYTES, 'qualification front door exceeds bound')
    members = inspect_object(files[row['object']][1], row)
    for entry in row['members']:
        if entry['original_path'] in RETIRED:
            expected = navigation_stub(entry, row)
            require(files[entry['original_path']][1] == expected and digest(expected) == entry['stub_sha256'],
                    'qualification navigation differs: ' + entry['original_path'])
    return row, members


def load_terminal(root):
    root = owned_root(root)
    encoded_file = read_file(root, INDEX, MAX_INDEX_BYTES)
    encoded = encoded_file[1]
    row = parse_descriptor(encoded)
    require(terminal_files(root) == {INDEX, FRONT, row['object']}, 'finite qualification terminal coverage differs')
    files = {INDEX: encoded_file}
    for name in [FRONT, row['object'], *RETIRED]:
        bound = MAX_OBJECT_BYTES if name == row['object'] else MAX_FRONT_BYTES
        files[name] = read_file(root, name, bound)
    return validate_view(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=PROJECT)
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--read', metavar='ORIGINAL_PATH')
    action.add_argument('--list', action='store_true')
    args = parser.parse_args()
    try:
        row, members = load_terminal(args.root)
        if args.read is not None:
            require(args.read in members, 'unknown archived qualification path')
            sys.stdout.buffer.write(members[args.read])
        elif args.list:
            print('\n'.join(entry['original_path'] for entry in row['members']))
        else:
            print(f'QUALIFICATION-HISTORY: ok (4 records, 1 book snapshot; {row["source_bytes"]} authenticated bytes)')
    except (ArchiveRefused, OSError) as exc:
        print('QUALIFICATION-HISTORY: REFUSED — ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
