#!/usr/bin/env python3
"""Replay the closed LC0031 whole-record transition and native reader contracts.

Use --working before publication, or --revision with its introduction commit.
A fresh --output target/PATH is required. Local Git objects and the public
mdBook toolchain are read-only inputs; Gitlinks stay opaque and no fetch occurs.
"""
from __future__ import annotations

import argparse
import copy
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import collect_containment_graph as C
import qualify_book_includes as Q

ROOT = C.ROOT
SOURCE = '4e99991e231dd37fc0f42623a78dbc966237908c'
TREE = 'docs/tasks/LIVE-CONTAINMENT.md'
BOOK = 'docs/book/src/working/task-trees.md'
RECORD = 'docs/tasks/artifacts/live-containment/reader-records-retention.md'
ARCHIVE = 'docs/tasks/archive/LIVE-CONTAINMENT-readers.md'
EARLIER = 'docs/tasks/archive/LIVE-CONTAINMENT.md'
OWNED = {TREE, BOOK, 'MEMORY.md'}
require = C.require


def blob(revision, name):
    return C.Q.git('show', revision + ':' + name)


def invalid_constant(value):
    raise C.Q.Refused('nonfinite JSON constant: ' + value)


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def decode(record):
    require(len(record) <= 131072, 'oversized retained record')
    text = record.decode('utf-8')
    blocks = re.findall(r'^```json\n(.*?)\n```$', text, re.M | re.S)
    require(len(blocks) == 3, 'exact three canonical JSON blocks required')
    values = [json.loads(b, object_pairs_hook=pairs, parse_constant=invalid_constant) for b in blocks]
    require(isinstance(values[0], dict) and isinstance(values[1], list)
            and isinstance(values[2], dict), 'canonical block types')
    return values


def apply_seams(files, seams):
    require(isinstance(seams, list) and len(seams) <= 40, 'bounded owned seams')
    for seam in seams:
        require(isinstance(seam, list) and len(seam) == 3, 'owned seam arity')
        name, old, new = seam
        require(name in OWNED and isinstance(old, str) and isinstance(new, str)
                and old and len(old.encode()) <= 16384 and len(new.encode()) <= 16384,
                'owned seam contract')
        body = files[name]
        require(body.count(old.encode()) == 1, 'unique owned seam: ' + name)
        files[name] = body.replace(old.encode(), new.encode(), 1)


def reconstruct(record, archive, published, original):
    mapping, census, seams = decode(record)
    required = {'source_commit', 'source_bytes', 'source_sha256', 'owner_bytes',
                'owner_sha256', 'spans', 'payload_bytes', 'payload_lines', 'archive',
                'archive_bytes', 'archive_sha256', 'wrapper_bytes', 'payload_sha256',
                'proposed_root_bytes', 'proposed_root_sha256', 'D70_source_occurrences',
                'candidate_syntax'}
    require(set(mapping) == required and set(seams) == {'activation', 'extra', 'closing'},
            'exact canonical metadata keys')
    require(mapping['source_commit'] == SOURCE and mapping['archive'] == ARCHIVE,
            'reviewed source/archive required')
    require(len(original[TREE]) == mapping['source_bytes']
            and C.digest(original[TREE]) == mapping['source_sha256'], 'complete original source')
    require(len(archive) == mapping['archive_bytes']
            and C.digest(archive) == mapping['archive_sha256'], 'whole retained archive')
    files = dict(original)
    apply_seams(files, seams['activation'])
    owner = files[TREE]
    require(len(owner) == mapping['owner_bytes'] and C.digest(owner) == mapping['owner_sha256'],
            'complete pre-retirement owner root')
    spans = mapping['spans']
    require(isinstance(spans, list) and len(spans) == 10, 'exact ten complete spans')
    previous_source, previous_owner = -1, -1
    archive_offset = mapping['wrapper_bytes']
    require(type(archive_offset) is int and 0 < archive_offset < len(archive), 'archive wrapper boundary')
    bodies = []
    headings = list(re.finditer(rb'^#{2,6} .+\n', original[TREE], re.M))
    boundaries = {h.start(): (headings[i + 1].start() if i + 1 < len(headings) else len(original[TREE]))
                  for i, h in enumerate(headings)}
    for span in spans:
        require(isinstance(span, dict), 'span metadata')
        for key in ['source_offset', 'owner_offset', 'archive_offset', 'bytes', 'lines']:
            require(type(span.get(key)) is int and span[key] >= 0, 'typed finite span position')
        require(span['bytes'] > 0 and span['source_offset'] >= previous_source
                and span['owner_offset'] >= previous_owner and span['archive_offset'] == archive_offset,
                'complete ordered span boundaries')
        require(boundaries.get(span['source_offset']) == span['source_offset'] + span['bytes'],
                'whole closed unit boundary')
        body = archive[archive_offset:archive_offset + span['bytes']]
        require(len(body) == span['bytes'] and C.digest(body) == span['sha256']
                and body.count(b'\n') == span['lines'], 'retained payload identity')
        require(original[TREE][span['source_offset']:span['source_offset'] + len(body)] == body
                and owner[span['owner_offset']:span['owner_offset'] + len(body)] == body,
                'payload differs from immutable source')
        require(body.startswith((span['heading'] + '\n').encode()), 'whole original heading')
        require(isinstance(span['replacement'], str) and isinstance(span['id'], str)
                and span['replacement'].startswith(span['heading'] + '\n'), 'retained heading stub')
        previous_source = span['source_offset'] + len(body)
        previous_owner = span['owner_offset'] + len(body)
        archive_offset += len(body)
        bodies.append(body)
    payload = b''.join(bodies)
    require(archive_offset == len(archive) and len(payload) == mapping['payload_bytes']
            and payload.count(b'\n') == mapping['payload_lines']
            and C.digest(payload) == mapping['payload_sha256'], 'complete archive payload population')
    for span, body in reversed(list(zip(spans, bodies))):
        offset = span['owner_offset']
        require(files[TREE][offset:offset + len(body)] == body, 'mapped retirement span')
        files[TREE] = files[TREE][:offset] + span['replacement'].encode() + files[TREE][offset + len(body):]
    require(len(files[TREE]) == mapping['proposed_root_bytes']
            and C.digest(files[TREE]) == mapping['proposed_root_sha256'], 'complete retired root')
    start = b'<!-- LC0031 phase -->\n````text\n'
    end = b'````\n<!-- LC0031 end phase -->'
    require(record.count(start) == record.count(end) == 1, 'complete planning payload markers')
    phase = record.split(start, 1)[1].split(end, 1)[0]
    require(len(phase) == 965 and original[TREE].count(phase) == 1, 'complete original planning payload')
    apply_seams(files, seams['extra'])
    apply_seams(files, seams['closing'])
    require(all(files[name] == published[name] for name in OWNED), 'published source differs from full reconstruction')
    observed = []
    for match in re.finditer(rb'scaffold24', original[TREE], re.I):
        offset = original[TREE].rfind(b'\n', 0, match.start()) + 1
        stop = original[TREE].find(b'\n', match.start())
        text = original[TREE][offset:stop].decode()
        observed.append({'line': original[TREE][:match.start()].count(b'\n') + 1,
                         'offset': match.start(), 'text': text,
                         'kind': 'correction-metadata' if 'claims above' in text else 'historical-claim'})
    require(observed == census == mapping['D70_source_occurrences']
            and len(observed) == 8 and sum(r['kind'] == 'historical-claim' for r in observed) == 7,
            'complete case-insensitive D70 population')
    return mapping, owner


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = [], []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if 'id' in values:
            self.ids.append(values['id'])
        if tag == 'a' and 'href' in values:
            self.links.append(values['href'])


def native(output, mapping, owner, published, archive, earlier):
    require(all(re.search(rb'\{\{\s*#', body) is None
                for body in [owner, published[TREE], archive, earlier]),
            'native heading fixture cannot expand include helpers')
    fixture = output / 'fixture'
    (fixture / 'src/archive').mkdir(parents=True)
    (fixture / 'book.toml').write_text('[book]\ntitle="Native retention replay"\nsrc="src"\n')
    (fixture / 'src/SUMMARY.md').write_text('# Summary\n\n- [Live](LIVE-CONTAINMENT.md)\n'
        '- [Earlier](archive/LIVE-CONTAINMENT.md)\n- [Readers](archive/LIVE-CONTAINMENT-readers.md)\n')
    (fixture / 'src/archive/LIVE-CONTAINMENT.md').write_bytes(earlier)
    (fixture / 'src/archive/LIVE-CONTAINMENT-readers.md').write_bytes(archive)
    env = Q.environment()
    env['TMPDIR'] = str(output / 'tmp')
    for stage, body in [('before', owner), ('after', published[TREE])]:
        (fixture / 'src/LIVE-CONTAINMENT.md').write_bytes(body)
        result = subprocess.run(['mdbook', 'build', str(fixture), '-d', str(output / stage)],
                                env=env, capture_output=True)
        (output / (stage + '.stdout')).write_bytes(result.stdout)
        (output / (stage + '.stderr')).write_bytes(result.stderr)
        require(result.returncode == 0, 'actual native build failed: ' + stage)
    root = Links()
    root.feed((output / 'after/LIVE-CONTAINMENT.html').read_text())
    prior = Links()
    prior.feed((output / 'before/LIVE-CONTAINMENT.html').read_text())
    retained = Links()
    retained.feed((output / 'after/archive/LIVE-CONTAINMENT-readers.html').read_text())
    for span in mapping['spans']:
        require(prior.ids.count(span['id']) == root.ids.count(span['id']) == retained.ids.count(span['id']) == 1
                and root.links.count('archive/LIVE-CONTAINMENT-readers.html#' + span['id']) == 1,
                'actual native original heading/route differs')
    require(root.ids.count('4h--revision-pinned-task-capacity-review-active') == 1,
            'original phase anchor unavailable')
    pattern = r'window\.path_to_searchindex_js = "(\.\./searchindex-[a-f0-9]+\.js)";'
    for name in ['LIVE-CONTAINMENT', 'LIVE-CONTAINMENT-readers']:
        before = (output / 'before/archive' / (name + '.html')).read_text()
        after = (output / 'after/archive' / (name + '.html')).read_text()
        require(before.split('<main>', 1)[1].split('</main>', 1)[0] ==
                after.split('<main>', 1)[1].split('</main>', 1)[0], 'complete archived article changed')
        require(re.sub(pattern, 'SEARCH', before) == re.sub(pattern, 'SEARCH', after),
                'whole archived HTML changed beyond search resource identity')
        for stage, text in [('before', before), ('after', after)]:
            paths = re.findall(pattern, text)
            require(len(paths) == 1 and (output / stage / 'archive' / paths[0]).resolve().is_file(),
                    'generated search resource unavailable')


def controls(record, archive, published, original):
    mapping, census, seams = decode(record)
    records = []
    for mode in ['omit-span', 'truncate-span', 'reorder-spans', 'corrupt-payload', 'corrupt-phase',
                 'bad-root-target', 'missing-metadata', 'omitted-seam', 'ambiguous-stub']:
        m, s, pub, arc, rec = copy.deepcopy(mapping), copy.deepcopy(seams), dict(published), archive, record
        if mode == 'omit-span':
            m['spans'].pop()
        elif mode == 'truncate-span':
            m['spans'][0]['bytes'] -= 1
        elif mode == 'reorder-spans':
            m['spans'][:2] = reversed(m['spans'][:2])
        elif mode == 'corrupt-payload':
            span = m['spans'][0]
            start = span['archive_offset'] + len(span['heading'].encode()) + 1
            match = re.search(rb'[A-Za-z]', arc[start:span['archive_offset'] + span['bytes']])
            require(match is not None, 'payload corruption seam absent')
            at = start + match.start()
            replacement = b'X' if arc[at:at + 1] != b'X' else b'Y'
            arc = arc[:at] + replacement + arc[at + 1:]
            m['archive_sha256'] = C.digest(arc)
            span['sha256'] = C.digest(arc[span['archive_offset']:span['archive_offset'] + span['bytes']])
            m['payload_sha256'] = C.digest(arc[m['wrapper_bytes']:])
        elif mode == 'corrupt-phase':
            rec = rec.replace(b'## .4h ', b'## X4h ', 1)
        elif mode == 'bad-root-target':
            pub[TREE] = pub[TREE].replace(m['spans'][0]['id'].encode(), b'broken-target', 1)
        elif mode == 'missing-metadata':
            m.pop('source_sha256')
        elif mode == 'omitted-seam':
            s['activation'].pop(0)
        else:
            pub[TREE] += m['spans'][0]['replacement'].encode()
        if mode != 'corrupt-phase':
            blocks = iter([m, census, s])
            rec = re.sub(rb'^```json\n.*?\n```$',
                         lambda _: ('```json\n' + json.dumps(next(blocks), indent=2) + '\n```').encode(),
                         record, flags=re.M | re.S)
        try:
            reconstruct(rec, arc, pub, original)
        except C.Q.Refused as exc:
            records.append({'control': mode, 'returncode': 2, 'reason': str(exc)})
        else:
            raise C.Q.Refused('deliberate retention corruption escaped: ' + mode)
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--working', action='store_true')
    parser.add_argument('--revision', default='HEAD')
    parser.add_argument('--output', required=True)
    parser.add_argument('--addition', action='append', default=[])
    args = parser.parse_args()
    os.environ['GIT_NO_LAZY_FETCH'] = '1'
    try:
        require(args.revision == 'HEAD' or re.fullmatch(r'[0-9a-f]{40}', args.revision),
                'HEAD or exact local commit required')
        C.Q.relative_path(args.output)
        require(args.output.startswith('target/'), 'output must be repository-owned target path')
        output = C.U.source_path(ROOT, args.output)
        require(not output.exists(), 'fresh output required')
        before = C.working_snapshot(args.addition)
        output.mkdir(parents=True)
        (output / 'tmp').mkdir()
        source = C.source_census(SOURCE)
        require(len(source['members']) == 1438, 'complete reviewed source membership')
        original = {name: blob(SOURCE, name) for name in OWNED}
        if args.working:
            def read(name):
                C.file_identity(name)
                return (ROOT / name).read_bytes()
        else:
            revision = C.source_census(args.revision)['revision']
            def read(name):
                return blob(revision, name)
        published = {name: read(name) for name in OWNED}
        record, archive = read(RECORD), read(ARCHIVE)
        require(read(EARLIER) == blob(SOURCE, EARLIER), 'earlier ordinary archive changed')
        mapping, owner = reconstruct(record, archive, published, original)
        corruptions = controls(record, archive, published, original)
        native(output, mapping, owner, published, archive, read(EARLIER))
        require(before == C.working_snapshot(args.addition), 'actual source/index/modes changed')
        Q.write_json(output / 'working-before.json', before)
        Q.write_json(output / 'working-after.json', before)
        result = {'source': SOURCE, 'spans': 10, 'units': 9, 'payload_bytes': mapping['payload_bytes'],
                  'payload_lines': mapping['payload_lines'], 'archive_sha256': C.digest(archive),
                  'native_routes': 10, 'phase_anchor': True, 'archived_articles': 2,
                  'D70_claims': 7, 'controls': corruptions,
                  'mode': 'optimized' if sys.flags.optimize else 'normal'}
        Q.write_json(output / 'result.json', result)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (C.Q.Refused, C.U.BookRefused, OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
        print('READER-RETENTION: REFUSED — ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
