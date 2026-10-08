#!/usr/bin/env python3
"""Positive/negative controls for finite history identity, retrieval and partition."""
import argparse
import copy
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import tarfile

import history_archive as H
from shard_history import next_shard_name

ROOT = Path(__file__).resolve().parent.parent
NAME = 'docs/changelog/shard-0042.md'
BODY = b'# shard\n\n## old-entry\nkept exactly\n'


def pack(root, entries, raw_override=None):
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode='w', format=tarfile.USTAR_FORMAT) as archive:
        for name, blob in entries:
            info = tarfile.TarInfo(name)
            info.size = len(blob)
            info.mode = 0o644
            archive.addfile(info, io.BytesIO(blob))
    blob = gzip.compress(raw.getvalue() if raw_override is None else raw_override, mtime=0)
    sha = H.digest(blob)
    path = f'docs/history/sealed/{sha}.tar.gz'
    (root / path).parent.mkdir(parents=True, exist_ok=True)
    (root / path).write_bytes(blob)
    (root / 'docs/history/README.md').write_text('# Retrieval\n')
    manifest = next(blob for name, blob in entries if name == H.MANIFEST)
    return dict(object=path, sha256=sha, bytes=len(blob), capture='a'*40,
                members=len(entries), shards=len(entries)-1,
                source_bytes=sum(len(blob) for _, blob in entries),
                source_lines=sum(blob.count(b'\n') for _, blob in entries),
                manifest_sha256=H.digest(manifest), manifest_bytes=len(manifest),
                date='2026-10-08', reason='finite test capture')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutation', default='green', choices=['green', 'missing-object',
        'object-digest', 'unknown-field', 'unsafe-path', 'string-count', 'duplicate-key',
        'oversized-index', 'duplicate-member', 'extra-member', 'unsafe-member',
        'shard-digest', 'expansion-bound', 'missing-index', 'previous-descriptor',
        'duplicate-heading', 'duplicate-location'])
    args = parser.parse_args()
    parent = ROOT / 'target/doctrine-selftest'
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=parent, prefix='history-archive-') as td:
        root = Path(td)
        (root / 'docs/changelog').mkdir(parents=True)
        (root / H.MANIFEST).write_text('')  # all old rows moved into authenticated terminal
        (root / 'CHANGELOG.md').write_text('# live\n\n## new-entry\nnew\n')
        (root / 'DEV_NOTES.md').write_text('# notes\n')
        manifest = f'{H.digest(BODY)}  {NAME}\n'.encode()
        entries = [(NAME, BODY), (H.MANIFEST, manifest)]
        if args.mutation == 'duplicate-member':
            entries.insert(1, (NAME, BODY))
        elif args.mutation == 'extra-member':
            entries.append(('docs/changelog/extra.md', BODY))
        elif args.mutation == 'unsafe-member':
            entries[0] = ('docs/changelog/../escape.md', BODY)
        elif args.mutation == 'shard-digest':
            entries[0] = (NAME, BODY+b'changed')
        record = pack(root, entries)
        if args.mutation == 'extra-member':
            record['members'], record['shards'] = 2, 1
        elif args.mutation == 'expansion-bound':
            bound = record['source_bytes'] + record['members']*1024 + 10240
            old = root / record['object']
            record = pack(root, entries, b'\0'*(bound+1))
            old.unlink()
        index = {'schema_version': 1, 'archives': [record]}
        previous = copy.deepcopy(index)
        previous_path = None
        if args.mutation == 'missing-object':
            (root / record['object']).unlink()
        elif args.mutation == 'object-digest':
            path = root / record['object']
            blob = path.read_bytes(); path.write_bytes(blob[:-1]+bytes([blob[-1]^1]))
        elif args.mutation == 'unknown-field':
            record['extra'] = 1
        elif args.mutation == 'unsafe-path':
            record['object'] = '../outside.tar.gz'
        elif args.mutation == 'string-count':
            record['source_bytes'] = str(record['source_bytes'])
        elif args.mutation == 'previous-descriptor':
            previous_path = root / 'previous.json'
            previous_path.write_text(json.dumps(previous))
            record['reason'] = 'rewritten committed descriptor'
        path = root / H.INDEX
        path.write_text(json.dumps(index))
        if args.mutation == 'duplicate-key':
            path.write_text(path.read_text()[:-1]+',"schema_version":1}')
        elif args.mutation == 'oversized-index':
            path.write_text(path.read_text()+' '*(H.MAX_INDEX_BYTES+1))
        elif args.mutation == 'missing-index':
            path.unlink()
        try:
            records, shards = H.load_archives(root, previous_path)
            assert shards[NAME] == (H.digest(BODY), BODY), 'retrieved bytes differ'
            if args.mutation in ('duplicate-heading', 'duplicate-location'):
                if args.mutation == 'duplicate-heading':
                    (root / 'CHANGELOG.md').write_bytes(BODY)
                else:
                    (root / NAME).write_bytes(BODY)
                    (root / H.MANIFEST).write_bytes(manifest)
            prev = root / 'previous.sha256'
            prev.write_bytes(manifest)
            judged = subprocess.run(['python3', str(ROOT/'scripts/check_history_partition.py'),
                '', str(root), 'docs/changelog', H.MANIFEST, str(prev),
                'CHANGELOG.md', 'DEV_NOTES.md'], capture_output=True, text=True)
            if judged.returncode:
                print(judged.stdout, end='')
                return judged.returncode
            assert '__CHECKED__ 1' in judged.stdout, 'predecessor archive row not authenticated'
            assert next_shard_name(root/'docs/changelog', root) == 'shard-0043.md', 'retired shard name reused'
            query = subprocess.run(['python3', str(ROOT/'scripts/history_archive.py'),
                '--root', str(root), '--read', NAME], capture_output=True)
            assert query.returncode == 0 and query.stdout == BODY, 'tool-neutral retrieval differs'
            assert args.mutation == 'green', 'mutation escaped'
            print('HISTORY-ARCHIVE probe: identity/retrieval/predecessor/numbering passed')
        except H.ArchiveRefused as exc:
            print(f'HISTORY-ARCHIVE: REFUSED — {exc}')
            return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
