#!/usr/bin/env python3
"""Check the LC0041 first publication and preserve both publishing views thereafter.

Only this publishing gate uses Git. The separate reader needs neither history nor
Git. First publication authenticates source-tree identity and all five originals;
later checks use published HEAD, so shallow clones need no predecessor fetch.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys

import qualification_history_archive as A

PREFIX = 'docs/qualification-history/'
WIRING = ('scripts/qualification_history_archive.py',
          'scripts/qualification_history_preservation.py',
          'scripts/probe_qualification_history.py', 'scripts/check_task_history.sh',
          'scripts/check_task_history_links.py', 'doctrine/readme_routes.tsv')
MAX_FILES = 20
MAX_TOTAL = 1024 * 1024
require = A.require


def git_read(root, *args, data=None):
    environment = dict(os.environ, GIT_NO_LAZY_FETCH='1')
    result = subprocess.run(['git', '--no-pager', '--no-optional-locks',
                             '--no-replace-objects', '-C', str(root), *args],
                            input=data, capture_output=True, timeout=30, env=environment)
    require(result.returncode == 0 and not result.stderr,
            'qualification Git read unavailable: ' + ' '.join(args))
    return result.stdout


def snapshot(root, revision, paths):
    staged = revision == ':'
    args = (['ls-files', '--stage', '-z', '--', *paths] if staged else
            ['ls-tree', '-rz', '--full-tree', revision, '--', *paths])
    raw = git_read(root, *args)
    require(len(raw) <= MAX_FILES * 512 and (not raw or raw.endswith(b'\0')),
            'qualification Git inventory exceeds bound or is incomplete')
    identities = {}
    for item in raw.split(b'\0')[:-1]:
        metadata, separator, encoded = item.partition(b'\t')
        fields = metadata.split()
        require(separator and len(fields) == 3, 'malformed qualification Git inventory')
        name = encoded.decode('utf-8')
        require(name in paths or name.startswith(PREFIX), 'unexpected qualification Git path')
        if staged:
            mode, oid, stage = fields
            require(stage == b'0', 'unmerged qualification input')
        else:
            mode, kind, oid = fields
            require(kind == b'blob', 'qualification input is not a Git blob')
        require(mode in {b'100644', b'100755'} and A.T.identity(oid.decode('ascii'), 40)
                and name not in identities, 'unsafe/duplicate qualification Git identity')
        identities[name] = (mode.decode('ascii'), oid)
    require(len(identities) <= MAX_FILES, 'qualification Git inventory exceeds file bound')
    if not identities:
        return {}
    requests = b''.join(oid + b'\n' for mode, oid in identities.values())
    sizes = git_read(root, 'cat-file', '--batch-check', data=requests)
    require(len(sizes) <= MAX_FILES * 128 and sizes.endswith(b'\n')
            and len(sizes.splitlines()) == len(identities), 'incomplete qualification Git sizes')
    entries = []
    for (name, (mode, oid)), row in zip(identities.items(), sizes.splitlines()):
        fields = row.split()
        require(len(fields) == 3 and fields[:2] == [oid, b'blob']
                and fields[2].isdigit() and len(fields[2]) <= 8,
                'malformed qualification Git size')
        size = int(fields[2])
        require(size <= A.MAX_OBJECT_BYTES, 'qualification Git blob exceeds bound')
        entries.append((name, mode, oid, size))
    require(sum(e[3] for e in entries) <= MAX_TOTAL, 'qualification Git bytes exceed bound')
    wire = git_read(root, 'cat-file', '--batch', data=requests)
    require(len(wire) <= MAX_TOTAL + MAX_FILES * 128, 'qualification Git response exceeds bound')
    result, cursor = {}, 0
    for name, mode, oid, size in entries:
        end = wire.find(b'\n', cursor)
        require(end >= 0 and wire[cursor:end] == oid + b' blob ' + str(size).encode(),
                'malformed qualification Git blob header')
        start = end + 1
        body = wire[start:start + size]
        require(len(body) == size and wire[start + size:start + size + 1] == b'\n',
                'incomplete qualification Git blob')
        actual = hashlib.sha1(b'blob ' + str(size).encode() + b'\0' + body).hexdigest()
        require(actual.encode() == oid, 'qualification Git blob identity differs')
        result[name] = (mode, body)
        cursor = start + size + 1
    require(cursor == len(wire), 'surplus qualification Git blob response')
    return result


def source_check(row, members, source, tree_digest):
    require(tree_digest == row['source_tree_sha256'], 'qualification source tree differs')
    require(set(source) == set(A.PATHS), 'qualification original source coverage differs')
    for entry in row['members']:
        name = entry['original_path']
        require(source[name] == (entry['mode'], members[name]),
                'qualification original source bytes/mode differ: ' + name)


def judge(previous, proposed, working, wiring_previous, wiring_proposed, wiring_working):
    """Both independent views must pass; first publication must be atomic."""
    row, members = A.validate_view(working)
    if A.INDEX in previous:
        A.validate_view(previous)
        require(proposed == previous, 'published qualification index changed')
        require(working == previous, 'published qualification working view changed')
        return row, members, False
    changed = proposed != previous or wiring_proposed != wiring_previous
    if changed:
        A.validate_view(proposed)
        require(proposed == working, 'qualification first publication views differ')
        require(set(wiring_proposed) == set(WIRING) and wiring_proposed == wiring_working,
                'qualification first publication wiring incomplete or differs')
    return row, members, True


def check(root):
    head = git_read(root, 'rev-parse', '--verify', 'HEAD').decode().strip()
    require(A.T.identity(head, 40), 'invalid qualification publishing HEAD')
    paths = [PREFIX, *A.RETIRED, *WIRING]
    previous_all = snapshot(root, head, paths)
    proposed_all = snapshot(root, ':', paths)
    data = lambda files: {n: v for n, v in files.items() if n not in WIRING}
    wiring = lambda files: {n: v for n, v in files.items() if n in WIRING}
    row, members = A.load_terminal(root)
    working = {name: A.read_file(root, name, A.MAX_OBJECT_BYTES)
               for name in [A.INDEX, A.FRONT, row['object'], *A.RETIRED]}
    working_wiring = {name: A.read_file(root, name, A.MAX_OBJECT_BYTES) for name in WIRING}
    row, members, birth = judge(data(previous_all), data(proposed_all), working,
                               wiring(previous_all), wiring(proposed_all), working_wiring)
    if birth:
        raw_tree = git_read(root, 'ls-tree', '-rz', '--full-tree', A.SOURCE)
        require(len(raw_tree) <= MAX_TOTAL and raw_tree.endswith(b'\0'),
                'qualification source tree unavailable or exceeds bound')
        source_check(row, members, snapshot(root, A.SOURCE, A.PATHS), A.digest(raw_tree))
    require(git_read(root, 'rev-parse', '--verify', 'HEAD').decode().strip() == head,
            'qualification publishing HEAD changed during check')
    return birth


def main():
    try:
        require(len(sys.argv) == 1, 'unknown qualification publishing arguments')
        birth = check(A.PROJECT)
    except (A.ArchiveRefused, OSError, UnicodeError, subprocess.SubprocessError) as exc:
        print('QUALIFICATION-PRESERVATION: REFUSED — ' + str(exc), file=sys.stderr)
        return 2
    print('QUALIFICATION-PRESERVATION: ok (' +
          ('first publication/source exact' if birth else 'published index/working exact') + ')')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
