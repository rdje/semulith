#!/usr/bin/env python3
"""Adversarial controls for the finite history reader; all fixtures stay in target/."""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile

import task_history_archive as history
from check_task_history_links import check_links

ROOT = Path(__file__).resolve().parent.parent
CASES = (
    'green', 'missing-descriptor', 'unknown-field', 'duplicate-key', 'oversized-descriptor',
    'string-count', 'bool-count', 'unsafe-object', 'changed-descriptor', 'previous-descriptor',
    'missing-object', 'object-digest', 'extra-file', 'terminal-symlink', 'parent-symlink',
    'changed-stub', 'missing-stub', 'unknown-read', 'escaping-read', 'expansion-bound',
    'truncated-gzip', 'nonregular-member', 'duplicate-member', 'extra-member', 'unsafe-member',
    'missing-member', 'oversized-member', 'noncanonical-tar', 'manifest-identity',
    'member-identity', 'source-bytes', 'source-lines', 'manifest-fields',
    'manifest-duplicate', 'manifest-path', 'manifest-string-count', 'malformed-json',
    'non-utf8', 'manifest-capture', 'oversized-json-integer', 'front-bound', 'extra-directory',
    'corrupt-read',
    'links-green', 'links-anchor', 'links-include',
)


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def tar_bytes(items, special=None):
    # Independent fixture encoder; the reader's canonical encoder is not used.
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w', format=tarfile.USTAR_FORMAT) as archive:
        for name, value in items:
            member = tarfile.TarInfo(name)
            member.size, member.mode = len(value), 0o644
            if special:
                special(member)
            archive.addfile(member, io.BytesIO(value))
    return buffer.getvalue()


def reseal(items, descriptor, special=None):
    raw = tar_bytes(items, special)
    blob = gzip.compress(raw, mtime=0)
    row = copy.deepcopy(descriptor)
    row['sha256'] = hashlib.sha256(blob).hexdigest()
    row['compressed_bytes'], row['tar_bytes'] = len(blob), len(raw)
    return blob, row


def run(case, fixture):
    original_index = (ROOT / history.INDEX).read_bytes()
    row = json.loads(original_index)
    blob = (ROOT / row['object']).read_bytes()
    with tarfile.open(fileobj=io.BytesIO(blob), mode='r:gz') as archive:
        items = [(member.name, archive.extractfile(member).read()) for member in archive]
    originals = dict(items)
    manifest = json.loads(originals[history.MANIFEST])
    for name in (history.INDEX, history.FRONT, row['object']):
        dest = fixture / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((ROOT / name).read_bytes())
    for entry in manifest['members']:
        dest = fixture / entry['path']
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(history.navigation_stub(entry, row))
    index = fixture / history.INDEX
    obj = fixture / row['object']
    stub = fixture / history.PATHS[-1]
    previous = None
    inner = False

    if case == 'green':
        _, rows, got = history.load_terminal(fixture, original_index)
        # Review is a separate, committed source of the historical identities.
        review = (ROOT / 'docs/decisions/decision_task-history-seal-review.md').read_text()
        expected = json.loads(review.split('<!-- capture-manifest -->\n```json\n', 1)[1].split('```', 1)[0])
        assert rows == expected['members']
        assert len(got) == 12 and sum(map(len, got.values())) == 1144703
        reader = fixture / 'scripts/task_history_archive.py'
        reader.parent.mkdir()
        reader.write_bytes((ROOT / 'scripts/task_history_archive.py').read_bytes())
        work = fixture / 'unrelated-working-directory'
        work.mkdir()
        before = {p.relative_to(fixture).as_posix(): p.read_bytes()
                  for p in fixture.rglob('*') if p.is_file()}
        tar = shutil.which('tar')
        assert tar, 'ordinary tar is required for the independent retrieval control'
        for entry in rows:
            name = entry['path']
            # PATH deliberately contains no Git; checkout has no .git directory.
            result = subprocess.run([sys.executable, str(reader), '--read', name],
                                    env={'PATH': ''}, cwd=work, capture_output=True)
            other = subprocess.run([tar, '-xOf', str(obj), name], capture_output=True)
            assert result.returncode == other.returncode == 0
            assert result.stdout == other.stdout == got[name] == originals[name]
            assert not result.stderr
        assert before == {p.relative_to(fixture).as_posix(): p.read_bytes()
                          for p in fixture.rglob('*') if p.is_file()}
        print('TASK-HISTORY-PROBE: all12 Python/tar originals exact; no Git/extraction; navigation/freeze exact')
        return
    if case.startswith('links-'):
        target = history.PATHS[-1]
        fragment = 'commits' if case == 'links-green' else 'not-retained'
        source = f'[history]({target}#{fragment})\n'.encode()
        if case == 'links-include':
            source = ('{{#include ' + target + '}}\n').encode()
        check_links(fixture, {'docs/consumer.md': source}, row, originals)
        if case != 'links-green':
            raise AssertionError('bad incoming consumer accepted')
        print('TASK-HISTORY-PROBE: incoming history path/anchor resolves')
        return
    if case == 'missing-descriptor':
        index.unlink()
    elif case == 'unknown-field':
        changed = copy.deepcopy(row); changed['unexpected'] = 1; index.write_bytes(encode(changed))
    elif case == 'duplicate-key':
        index.write_bytes(original_index[:-2] + b',"schema_version":1}\n')
    elif case == 'oversized-descriptor':
        index.write_bytes(original_index + b' ' * history.MAX_INDEX_BYTES)
    elif case in ('string-count', 'bool-count'):
        changed = copy.deepcopy(row)
        changed['source_bytes'] = '1144703' if case == 'string-count' else True
        index.write_bytes(encode(changed))
    elif case == 'unsafe-object':
        changed = copy.deepcopy(row); changed['object'] = '../outside'; index.write_bytes(encode(changed))
    elif case == 'changed-descriptor':
        changed = copy.deepcopy(row); changed['capture'] = '0' * 40; index.write_bytes(encode(changed))
    elif case == 'previous-descriptor':
        previous = b'changed predecessor'
    elif case == 'missing-object':
        obj.unlink()
    elif case == 'object-digest':
        changed = bytearray(blob); changed[-1] ^= 1; obj.write_bytes(changed)
    elif case == 'extra-file':
        (fixture / 'docs/task-history/extra').write_text('extra')
    elif case == 'terminal-symlink':
        obj.unlink(); obj.symlink_to(ROOT / row['object'])
    elif case == 'parent-symlink':
        path = fixture / 'docs/tasks/archive'; path.rename(fixture / 'saved-archive')
        path.symlink_to(fixture / 'saved-archive', target_is_directory=True)
    elif case == 'changed-stub':
        stub.write_bytes(stub.read_bytes().replace(b'id="commits"', b'id="lost"'))
    elif case == 'missing-stub':
        stub.unlink()
    elif case in ('unknown-read', 'escaping-read', 'corrupt-read'):
        name = 'docs/tasks/archive/UNKNOWN.md' if case == 'unknown-read' else '../outside'
        reason = 'unknown archived logical path'
        if case == 'corrupt-read':
            name, reason = history.PATHS[-1], 'object digest differs'
            changed = bytearray(blob); changed[-1] ^= 1; obj.write_bytes(changed)
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/task_history_archive.py'),
                                 '--root', str(fixture), '--read', name], capture_output=True)
        assert result.returncode == 1 and result.stdout == b'', result
        print(result.stderr.decode(), end='')
        assert reason in result.stderr.decode()
        raise history.ArchiveRefused(reason)
    elif case == 'front-bound':
        (fixture / history.FRONT).write_bytes(b'x' * (history.MAX_FRONT_BYTES + 1))
    elif case == 'extra-directory':
        (fixture / 'docs/task-history/unknown').mkdir()
    else:
        # Reseal the outer digest in these controls to exercise the inner defenses.
        # Production reads always require the separate immutable descriptor pin.
        inner = True
        if case == 'expansion-bound':
            row['tar_bytes'] = 1024
        elif case == 'truncated-gzip':
            blob = blob[:-8]; row['compressed_bytes'] = len(blob); row['sha256'] = history.digest(blob)
        elif case == 'nonregular-member':
            def symlink(member):
                if member.name == history.PATHS[0]:
                    member.type, member.linkname = tarfile.SYMTYPE, '../outside'
            blob, row = reseal(items, row, symlink)
        elif case == 'duplicate-member':
            blob, row = reseal(items[:1] + items, row)
        elif case in ('extra-member', 'unsafe-member'):
            name = 'docs/tasks/archive/UNKNOWN.md' if case == 'extra-member' else '../outside'
            blob, row = reseal(items + [(name, b'x\n')], row)
        elif case == 'missing-member':
            blob, row = reseal(items[1:], row)
        elif case == 'oversized-member':
            blob, row = reseal([(items[0][0], b'x' * (history.MAX_MEMBER_BYTES + 1))] + items[1:], row)
        elif case == 'noncanonical-tar':
            blob, row = reseal(items, row, lambda member: setattr(member, 'mtime', 1))
        elif case == 'manifest-identity':
            blob, row = reseal(items[:-1] + [(history.MANIFEST, originals[history.MANIFEST] + b' ')], row)
        elif case == 'member-identity':
            value = items[0][1].replace(b'P4', b'Q4', 1)
            assert value != items[0][1]
            blob, row = reseal([(items[0][0], value)] + items[1:], row)
        elif case == 'source-bytes':
            row['source_bytes'] += 1
        elif case == 'source-lines':
            row['source_lines'] += 1
        else:
            if case == 'manifest-fields':
                manifest['unknown'] = 1
            elif case == 'manifest-duplicate':
                manifest['members'][1] = copy.deepcopy(manifest['members'][0])
            elif case == 'manifest-path':
                manifest['members'][0]['path'] = '../outside'
            elif case == 'manifest-string-count':
                manifest['members'][0]['bytes'] = str(manifest['members'][0]['bytes'])
            elif case == 'manifest-capture':
                manifest['capture'] = '0' * 40
            elif case == 'non-utf8':
                value = b'\xff' + items[0][1][1:]
                items[0] = (items[0][0], value)
                manifest['members'][0]['sha256'] = history.digest(value)
            elif case not in ('malformed-json', 'oversized-json-integer'):
                raise AssertionError(f'unimplemented control: {case}')
            encoded = encode(manifest)
            if case == 'malformed-json':
                encoded = b'{'
            elif case == 'oversized-json-integer':
                encoded = b'{"schema_version":' + b'1' * 5000 + b'}'
            row['manifest_bytes'], row['manifest_sha256'] = len(encoded), history.digest(encoded)
            blob, row = reseal(items[:-1] + [(history.MANIFEST, encoded)], row)
    if inner:
        history.inspect_object(blob, row)
    else:
        history.load_terminal(fixture, previous)
    raise AssertionError(f'negative control unexpectedly accepted: {case}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', required=True, choices=CASES)
    args = parser.parse_args()
    scratch = ROOT / 'target/doctrine-selftest'
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='task-history-', dir=scratch) as temp:
        try:
            run(args.case, Path(temp))
        except (history.ArchiveRefused, OSError) as exc:
            print(f'TASK-HISTORY-PROBE: REFUSED — {exc}')
            return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
