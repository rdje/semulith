#!/usr/bin/env python3
"""Preserve published task-archive bytes and Git modes in index and working views.

HEAD is the publishing baseline. New files may be added; first-publication
correctness and historical truth remain separate obligations. This does not
extend the finite sealed-history reader or authorize an archive transition.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = 'docs/tasks/archive/'
MAX_FILES = 96
MAX_BYTES = 3 * 1024 * 1024
MAX_FILE = 128 * 1024
OID = re.compile(rb'(?:[0-9a-f]{40}|[0-9a-f]{64})\Z')


class Changed(ValueError):
    """A published file no longer has its original identity."""


class Refused(ValueError):
    """The available inputs cannot support a preservation verdict."""


def require(condition, reason):
    if not condition:
        raise Refused(reason)


def safe_name(name):
    path = PurePosixPath(name)
    require(name.startswith(ARCHIVE) and name.endswith('.md')
            and len(name.encode('utf-8')) <= 256 and str(path) == name
            and not path.is_absolute() and '..' not in path.parts
            and '\\' not in name and all(32 <= ord(c) != 127 for c in name),
            'unsafe archive path ' + name)


def git_read(root, *arguments, data=None):
    result = subprocess.run(['git', '--no-pager', '--no-optional-locks',
                             '--no-replace-objects', '-C', str(root), *arguments],
                            input=data, capture_output=True, timeout=30)
    require(result.returncode == 0 and not result.stderr,
            f'Git read failed (rc={result.returncode}): ' + ' '.join(arguments) + ': ' +
            result.stderr.decode('utf-8', errors='replace').strip())
    return result.stdout


def git_snapshot(root, revision='HEAD'):
    staged = revision == ':'
    arguments = (['ls-files', '--stage', '-z', '--', ARCHIVE] if staged else
                 ['ls-tree', '-rz', '--full-tree', revision, '--', ARCHIVE])
    inventory = git_read(root, *arguments)
    require(len(inventory) <= MAX_FILES * 512, 'archive inventory exceeds bound')
    require(not inventory or inventory.endswith(b'\0'), 'incomplete archive inventory')
    require(staged or bool(inventory), 'empty published archive inventory')
    objects = {}
    for row in inventory.split(b'\0')[:-1]:
        metadata, separator, encoded = row.partition(b'\t')
        require(bool(separator), 'malformed archive inventory row')
        try:
            name = encoded.decode('utf-8')
        except UnicodeError as error:
            raise Refused('non-UTF-8 archive path') from error
        safe_name(name)
        fields = metadata.split()
        require(len(fields) == 3, 'malformed archive metadata ' + name)
        if staged:
            mode, oid, stage = fields
            require(stage == b'0', 'unmerged archive path ' + name)
        else:
            mode, kind, oid = fields
            require(kind == b'blob', 'non-blob archive path ' + name)
        require(mode in {b'100644', b'100755'} and OID.fullmatch(oid)
                and name not in objects, 'unsafe/duplicate archive identity ' + name)
        objects[name] = (mode.decode('ascii'), oid)
        require(len(objects) <= MAX_FILES, 'archive inventory exceeds file bound')
    if not objects:
        return {}
    requests = b''.join(oid + b'\n' for _, oid in objects.values())
    sizes = git_read(root, 'cat-file', '--batch-check', data=requests)
    require(len(sizes) <= MAX_FILES * 128, 'archive size response exceeds bound')
    require(sizes.endswith(b'\n'), 'incomplete archive size response')
    rows = sizes.splitlines()
    require(len(rows) == len(objects), 'incomplete archive size response')
    expected = []
    for (name, (mode, oid)), row in zip(objects.items(), rows):
        fields = row.split()
        require(len(fields) == 3 and fields[:2] == [oid, b'blob']
                and fields[2].isdigit() and len(fields[2]) <= 8,
                'invalid archive blob size ' + name)
        size = int(fields[2])
        require(size <= MAX_FILE, 'archive blob exceeds file bound ' + name)
        expected.append((name, mode, oid, size))
    require(sum(row[3] for row in expected) <= MAX_BYTES, 'archive snapshot exceeds byte bound')
    stream = git_read(root, 'cat-file', '--batch', data=requests)
    require(len(stream) <= MAX_BYTES + MAX_FILES * 128, 'archive blob response exceeds bound')
    result, cursor = {}, 0
    for name, mode, oid, size in expected:
        newline = stream.find(b'\n', cursor)
        header = oid + b' blob ' + str(size).encode('ascii')
        require(newline >= 0 and stream[cursor:newline] == header,
                'invalid archive blob response ' + name)
        start = newline + 1
        body = stream[start:start + size]
        require(len(body) == size and stream[start + size:start + size + 1] == b'\n',
                'incomplete archive blob ' + name)
        algorithm = hashlib.sha1 if len(oid) == 40 else hashlib.sha256
        actual = algorithm(b'blob ' + str(size).encode('ascii') + b'\0' + body).hexdigest()
        require(actual.encode('ascii') == oid, 'archive object identity differs ' + name)
        result[name] = (mode, body)
        cursor = start + size + 1
    require(cursor == len(stream), 'surplus archive blob response')
    return result


def owned_path(root, name):
    safe_name(name)
    cursor = root
    for part in PurePosixPath(name).parts:
        cursor /= part
        try:
            identity = cursor.lstat()
        except FileNotFoundError as error:
            raise Changed('working: missing published archive ' + name) from error
        require(not stat.S_ISLNK(identity.st_mode), 'symlink in archive path ' + name)
        require(identity.st_dev == root.stat().st_dev, 'off-volume archive path ' + name)
        if stat.S_ISDIR(identity.st_mode):
            marker = cursor / '.git'
            require(not marker.exists() and not marker.is_symlink(),
                    'Git boundary in archive path ' + name)
    return cursor


def working_snapshot(root, previous):
    result = {}
    for name in previous:
        path = owned_path(root, name)
        before = path.lstat()
        require(stat.S_ISREG(before.st_mode), 'nonregular working archive ' + name)
        require(before.st_size <= MAX_FILE, 'working archive exceeds file bound ' + name)
        nofollow = getattr(os, 'O_NOFOLLOW', None)
        require(nofollow is not None, 'no-follow file reads unavailable')
        descriptor = os.open(path, os.O_RDONLY | os.O_NONBLOCK | nofollow)
        with os.fdopen(descriptor, 'rb') as stream:
            opened = os.fstat(stream.fileno())
            require(stat.S_ISREG(opened.st_mode) and opened.st_dev == before.st_dev
                    and opened.st_ino == before.st_ino, 'working archive identity changed ' + name)
            body = stream.read(MAX_FILE + 1)
            after = os.fstat(stream.fileno())
        require(len(body) <= MAX_FILE, 'working archive exceeds file bound ' + name)
        fields = ('st_dev', 'st_ino', 'st_mode', 'st_size', 'st_mtime_ns')
        require(all(getattr(before, field) == getattr(after, field) for field in fields)
                and len(body) == after.st_size, 'working archive changed during read ' + name)
        mode = '100755' if after.st_mode & stat.S_IXUSR else '100644'
        result[name] = (mode, body)
    return result


def verify(previous, current, view):
    for name, identity in previous.items():
        if current.get(name) != identity:
            raise Changed(view + ': published archive changed ' + name)
    return len(previous), sum(len(body) for _, body in previous.values())


def current_head(root):
    head = git_read(root, 'rev-parse', '--verify', 'HEAD')
    require(head.endswith(b'\n') and OID.fullmatch(head[:-1]), 'invalid published HEAD identity')
    return head[:-1].decode('ascii')


def check(root):
    root = root.resolve(strict=True)
    head = current_head(root)
    previous = git_snapshot(root, head)
    proposed = git_snapshot(root, ':')
    verify(previous, proposed, 'index')
    counts = verify(previous, working_snapshot(root, previous), 'working')
    require(current_head(root) == head, 'published HEAD changed during check')
    return counts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    try:
        files, size = check(ROOT)
    except Changed as error:
        print('TASK-PRESERVATION: changed — ' + str(error))
        return 1
    except (Refused, OSError, UnicodeError, ValueError, subprocess.SubprocessError) as error:
        print('TASK-PRESERVATION: REFUSED — ' + str(error))
        return 2
    print(f'TASK-PRESERVATION: ok ({files} published files / {size} bytes; index/working exact)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
