#!/usr/bin/env python3
"""Authenticate and read the finite sealed history terminal; never extract to disk.

The descriptor and content-addressed object are tracked inputs. Ordinary reads need
neither Git history nor a particular editor. Missing/changed data fails closed.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile

INDEX = 'docs/history/archives.json'
MANIFEST = 'docs/changelog/SHARDS.sha256'
MAX_INDEX_BYTES = 16384
MAX_ARCHIVES = 8
MAX_RECORD_BYTES = 2048
MAX_SOURCE_BYTES = 2097152
MAX_MEMBERS = 1024
ROW = re.compile(r'^([0-9a-f]{64})  (docs/changelog/[^/\s]+\.md)$')
FIELDS = {'object', 'sha256', 'bytes', 'capture', 'members', 'shards', 'source_bytes',
          'source_lines', 'manifest_sha256', 'manifest_bytes', 'date', 'reason'}


class ArchiveRefused(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ArchiveRefused(message)


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def relative_file(root, name):
    require(isinstance(name, str) and len(name.encode()) <= 256, 'unsafe archive path')
    path = PurePosixPath(name)
    require(not path.is_absolute() and '..' not in path.parts and str(path) == name,
            'unsafe archive path')
    full = root / name
    require(full.resolve().is_relative_to(root.resolve()) and not full.is_symlink(),
            'unsafe archive path')
    require(full.is_file(), 'missing archive object')
    require(full.stat().st_dev == root.stat().st_dev, 'off-volume archive object')
    return full


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate descriptor key')
        result[key] = value
    return result


def parse_index(blob):
    require(len(blob) <= MAX_INDEX_BYTES, 'archive index exceeds bound')
    try:
        data = json.loads(blob, object_pairs_hook=unique_object)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ArchiveRefused('malformed archive index') from exc
    require(isinstance(data, dict) and set(data) == {'schema_version', 'archives'},
            'unknown archive index fields')
    require(type(data['schema_version']) is int and data['schema_version'] == 1,
            'unknown archive schema version')
    records = data['archives']
    require(isinstance(records, list) and 1 <= len(records) <= MAX_ARCHIVES,
            'archive record count exceeds bound')
    paths = set()
    for record in records:
        require(isinstance(record, dict) and set(record) == FIELDS, 'unknown archive descriptor fields')
        require(len(json.dumps(record).encode()) <= MAX_RECORD_BYTES, 'archive record exceeds bound')
        for field in ('bytes', 'members', 'shards', 'source_bytes', 'source_lines', 'manifest_bytes'):
            require(type(record[field]) is int and record[field] > 0, 'archive counts must be positive integers')
        require(record['source_bytes'] <= MAX_SOURCE_BYTES and record['members'] <= MAX_MEMBERS,
                'archive payload exceeds bound')
        require(record['members'] == record['shards'] + 1, 'archive member counts disagree')
        require(record['bytes'] <= record['source_bytes'] + record['members'] * 1024 + 10240,
                'archive object exceeds bound')
        for field, width in (('sha256', 64), ('manifest_sha256', 64), ('capture', 40)):
            require(isinstance(record[field], str) and re.fullmatch('[0-9a-f]{'+str(width)+'}', record[field]),
                    'malformed archive identity')
        require(record['object'] == f"docs/history/sealed/{record['sha256']}.tar.gz", 'unsafe archive path')
        require(record['object'] not in paths, 'duplicate archive path')
        paths.add(record['object'])
        require(isinstance(record['date'], str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', record['date']),
                'malformed archive date')
        require(isinstance(record['reason'], str) and 1 <= len(record['reason'].encode()) <= 256,
                'archive reason exceeds bound')
    return records


def load_archives(root, previous_index=None):
    """Return immutable descriptor records and logical shard (digest, bytes) pairs."""
    index = root / INDEX
    if not index.is_file():
        require(not (root / 'docs/history').exists(), 'missing archive index')
        require(not previous_index, 'removed committed archive index')
        return [], {}
    relative_file(root, INDEX)
    front = relative_file(root, 'docs/history/README.md')
    require(front.stat().st_size <= 4096, 'archive front door exceeds bound')
    require(index.stat().st_size <= MAX_INDEX_BYTES, 'archive index exceeds bound')
    records = parse_index(index.read_bytes())
    if previous_index:
        require(previous_index.stat().st_size <= MAX_INDEX_BYTES, 'archive index exceeds bound')
        previous = parse_index(previous_index.read_bytes())
        by_path = {record['object']: record for record in records}
        for record in previous:
            require(by_path.get(record['object']) == record, 'changed or removed committed archive descriptor')
    declared = {record['object'] for record in records}
    actual = {path.relative_to(root).as_posix() for path in (root / 'docs/history/sealed').rglob('*') if path.is_file()}
    require(actual == declared, 'archive object coverage differs')
    shards = {}
    for record in records:
        full = relative_file(root, record['object'])
        require(full.stat().st_size == record['bytes'], 'archive object byte count differs')
        blob = full.read_bytes()
        require(digest(blob) == record['sha256'], 'archive object digest differs')
        bound = record['source_bytes'] + record['members'] * 1024 + 10240
        try:
            with gzip.GzipFile(fileobj=io.BytesIO(blob)) as compressed:
                raw = compressed.read(bound + 1)
            require(len(raw) <= bound, 'archive expansion exceeds bound')
            members = {}
            with tarfile.open(fileobj=io.BytesIO(raw), mode='r:') as archive:
                for member in archive:
                    require(member.isfile() and not member.issparse(), 'archive member must be a regular file')
                    require(member.name == MANIFEST or ROW.fullmatch('0'*64+'  '+member.name),
                            'unsafe archive member path')
                    require(member.name not in members, 'duplicate archive member')
                    require(0 < member.size <= record['source_bytes'], 'archive member size exceeds bound')
                    require(len(members) < record['members'], 'extra archive member')
                    members[member.name] = archive.extractfile(member).read()
        except (OSError, EOFError, tarfile.TarError) as exc:
            raise ArchiveRefused('unreadable archive object') from exc
        require(len(members) == record['members'] and MANIFEST in members, 'archive members incomplete')
        manifest = members[MANIFEST]
        require(len(manifest) == record['manifest_bytes'] and digest(manifest) == record['manifest_sha256'],
                'archived manifest identity differs')
        try:
            lines = manifest.decode('utf-8').splitlines()
        except UnicodeError as exc:
            raise ArchiveRefused('archived manifest is not UTF-8') from exc
        expected = {}
        for line in lines:
            match = ROW.fullmatch(line)
            require(match is not None, 'malformed archived manifest row')
            sha, name = match.groups()
            require(name not in expected, 'duplicate archived manifest row')
            expected[name] = sha
        require(len(expected) == record['shards'] and set(members) == set(expected) | {MANIFEST},
                'archived manifest coverage differs')
        require(sum(map(len, members.values())) == record['source_bytes'], 'archive source byte count differs')
        require(sum(blob.count(b'\n') for blob in members.values()) == record['source_lines'],
                'archive source line count differs')
        for name, sha in expected.items():
            require(digest(members[name]) == sha, 'archived shard digest differs')
            require(name not in shards, 'archived logical path duplicated')
            try:
                members[name].decode('utf-8')
            except UnicodeError as exc:
                raise ArchiveRefused('archived shard is not UTF-8') from exc
            shards[name] = (sha, members[name])
    return records, shards


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--read', metavar='FORMER_PATH')
    args = parser.parse_args()
    try:
        records, shards = load_archives(args.root)
        if args.read:
            require(args.read in shards, 'unknown archived logical path')
            sys.stdout.buffer.write(shards[args.read][1])
        else:
            print(f'HISTORY-ARCHIVE: ok ({len(records)} sealed object(s), {len(shards)} authenticated shards)')
    except (ArchiveRefused, OSError) as exc:
        print(f'HISTORY-ARCHIVE: REFUSED — {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
