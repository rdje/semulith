#!/usr/bin/env python3
"""Qualify the pinned seven-book chapter TOC through public mdBook outputs.

Use a fresh --output target/PATH. Measurement completes with exit0;
--require-clean fails1 on wrong chapter data. Unjudgeable inputs refuse2.
Page-heading insertion, browser execution, search and resource loading remain
separate qualifications. No Gitlink implementation is copied or inspected.
"""
from __future__ import annotations

import argparse
import ast
import base64
import copy
import json
import lzma
import os
from pathlib import Path
import re
import subprocess
import sys
import zlib
from html.parser import HTMLParser

import collect_containment_graph as C
import qualify_book_includes as B
import qualify_book_navigation as N

ROOT = C.ROOT
SOURCE = '718bbd953bf6fd119a6a822de47d7eda75519f05'
require = C.require


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def fingerprint(value):
    body = canonical(value)
    return {'canonical_bytes': len(body), 'canonical_sha256': C.digest(body)}


def source_manifest():
    """Read the retained LC0038 baseline from this qualification's Git source.

    Git objects are required replay inputs, not an archival retention promise.
    The complete source census and bounded old metadata authenticate the view.
    """
    os.environ['GIT_NO_LAZY_FETCH'] = '1'
    source = C.source_census(SOURCE)
    require(len(source['members']) == 1466, 'complete capture source population')
    record = C.Q.git('show', SOURCE + ':docs/tasks/artifacts/live-containment/include-readers.md')
    phase = record.decode('utf-8').split('## Actual navigation consumer assessment — LC0038\n', 1)[1]
    frame = json.loads(re.search(r'^```json\n(.*?)\n```$', phase, re.M | re.S)[1])
    blob = base64.b64decode(frame['metadata_zlib_base64'], validate=True)
    require(len(blob) == frame['compressed_bytes'] and C.digest(blob) == frame['compressed_sha256'],
            'retained baseline compressed identity')
    require(type(frame['metadata_bytes']) is int and 0 < frame['metadata_bytes'] <= 524288,
            'retained baseline metadata bound')
    decoder = zlib.decompressobj()
    body = decoder.decompress(blob, frame['metadata_bytes'] + 1)
    require(decoder.eof and not decoder.unused_data and len(body) == frame['metadata_bytes']
            and C.digest(body) == frame['metadata_sha256'], 'retained baseline metadata identity')
    return source, json.loads(body)['normal']['stages']['baseline']['files']


def packed_result(raw, original):
    """Keep complete TOC metadata; fingerprint generated protocol bodies only."""
    value = copy.deepcopy(raw)
    files = value['stages']['baseline']['files']
    require(files == value['stages']['captured']['files'], 'unchanged complete capture files')
    delta = {'remove': sorted(set(original) - set(files)),
             'set': {p: sha for p, sha in files.items() if original.get(p) != sha},
             'count': len(files), **fingerprint(files)}
    value['stages']['baseline']['files'] = {'$manifest_delta': delta}
    value['stages']['captured']['files'] = {'$manifest_from': 'baseline'}

    def pack_stage(stage):
        for protocol in stage['captures'].values():
            for key in ['before', 'after']:
                protocol[key] = {'$protocol_book': fingerprint(protocol[key])}
            reads = protocol.pop('reads')
            require(not reads or all(row == reads[0] for row in reads), 'uniform registry read run')
            protocol['ordered_read_run'] = {'count': len(reads), 'record': reads[0] if reads else None}

    for stage in value['stages'].values():
        pack_stage(stage)
    for omission in value['actual_omissions']:
        stage = omission['stage']
        manifest = stage.pop('files')
        stage['files'] = {'$manifest_fingerprint': {'count': len(manifest), **fingerprint(manifest)}}
        pack_stage(stage)
    exclusions = value.pop('exclusions')
    reason = exclusions[0]['reason']
    require(all(row['reason'] == reason and files[row['path']] == row['sha256']
                for row in exclusions), 'complete exclusion inheritance')
    value['exclusions_from_baseline'] = {'paths': [row['path'] for row in exclusions], 'reason': reason}
    return value


def metadata_changes(before, after, path=()):
    """Lossless ordered replacements of mixed dictionary/list paths."""
    if isinstance(before, dict) and isinstance(after, dict) and before.keys() == after.keys():
        for key in before:
            yield from metadata_changes(before[key], after[key], path + (key,))
    elif isinstance(before, list) and isinstance(after, list) and len(before) == len(after):
        for index, (a, b) in enumerate(zip(before, after)):
            yield from metadata_changes(a, b, path + (index,))
    elif before != after:
        yield [list(path), after]


def encode_capture(normal, optimized, book_seams):
    """Encode full metadata using authenticated source/manifest references.

    Raw protocol bodies and omission output manifests retain fingerprints, as
    declared generated diagnostics. Every TOC row, source pin and exclusion
    remains reconstructible. Standard-library XZ uses an explicit 8 MiB dictionary.
    """
    source, original = source_manifest()
    require(normal['source'] == optimized['source'] == SOURCE, 'capture source differs')
    n, o = packed_result(normal, original), packed_result(optimized, original)
    value = {'normal': n, 'optimized_overrides': list(metadata_changes(n, o)),
             'book_seams': book_seams}
    complete = fingerprint(value)
    compact = copy.deepcopy(value)
    members = source['members']
    positions = {row['path']: i for i, row in enumerate(members)}
    rows = n['inputs']
    indices = [positions[row['path']] for row in rows]
    require([members[i] for i in indices] == rows, 'complete source pin reconstruction')
    compact['normal']['inputs'] = {'$source_rows': {'indices': indices, **fingerprint(rows)}}
    files = normal['stages']['baseline']['files']
    positions = {p: i for i, p in enumerate(sorted(files))}
    excluded = compact['normal']['exclusions_from_baseline']
    excluded['indices'] = [positions[p] for p in excluded.pop('paths')]
    body = canonical(compact)
    require(0 < len(body) <= 524288 and complete['canonical_bytes'] <= 524288,
            'complete capture metadata bound')
    blob = lzma.compress(body, format=lzma.FORMAT_XZ,
                         filters=[{'id': lzma.FILTER_LZMA2, 'preset': 6,
                                   'dict_size': 8 * 1024 * 1024}])
    return {'encoding': 'lzma6/xz/base64 canonical UTF-8 JSON; source and manifest indices',
            'metadata_bytes': len(body), 'metadata_sha256': C.digest(body),
            'compressed_bytes': len(blob), 'compressed_sha256': C.digest(blob),
            'metadata_xz_base64': base64.b64encode(blob).decode('ascii'),
            'complete': complete,
            'producer': C.file_identity('scripts/qualify_book_toc.py'),
            'inventory_producer': C.file_identity('scripts/collect_containment_graph.py')}


def decode_capture(frame):
    """Bound, authenticate and restore the complete encoded metadata view."""
    try:
        return _decode_capture(frame)
    except (KeyError, TypeError, IndexError, UnicodeError, RecursionError) as exc:
        raise ValueError('capture metadata input refused') from exc


def _decode_capture(frame):
    require(isinstance(frame, dict) and {'encoding', 'metadata_bytes', 'metadata_sha256',
            'compressed_bytes', 'compressed_sha256', 'metadata_xz_base64', 'complete',
            'producer', 'inventory_producer'} <= frame.keys(), 'capture frame fields')
    require(C.file_identity('scripts/qualify_book_toc.py') == frame['producer']
            and C.file_identity('scripts/collect_containment_graph.py') == frame['inventory_producer'],
            'pinned capture producers unavailable')
    require(frame['encoding'] == 'lzma6/xz/base64 canonical UTF-8 JSON; source and manifest indices',
            'unreviewed capture encoding')
    for key, limit in [('metadata_bytes', 524288), ('compressed_bytes', 131072)]:
        require(type(frame[key]) is int and 0 < frame[key] <= limit, 'capture bound: ' + key)
    require(isinstance(frame['metadata_xz_base64'], str)
            and len(frame['metadata_xz_base64']) <= 174764, 'encoded capture bound')
    blob = base64.b64decode(frame['metadata_xz_base64'], validate=True)
    require(len(blob) == frame['compressed_bytes'] and C.digest(blob) == frame['compressed_sha256'],
            'compressed capture identity')
    try:
        decoder = lzma.LZMADecompressor(format=lzma.FORMAT_XZ, memlimit=64 * 1024 * 1024)
        body = decoder.decompress(blob, max_length=frame['metadata_bytes'] + 1)
    except lzma.LZMAError as exc:
        raise ValueError('capture XZ input refused') from exc
    require(decoder.eof and not decoder.unused_data and len(body) == frame['metadata_bytes']
            and C.digest(body) == frame['metadata_sha256'], 'complete encoded capture identity')
    value = json.loads(body)
    require(isinstance(value, dict) and isinstance(value.get('normal'), dict),
            'capture metadata objects')
    normal = value['normal']
    require(normal['source'] == SOURCE, 'capture source differs')
    source, original = source_manifest()
    require(normal['source_tree_sha256'] == source['tree_sha256'], 'complete capture source tree')

    def selected(indices, population, count):
        require(isinstance(indices, list) and len(indices) == count
                and all(type(i) is int and 0 <= i < len(population) for i in indices)
                and len(set(indices)) == len(indices), 'complete unique capture indices')
        return [population[i] for i in indices]

    reference = normal['inputs']['$source_rows']
    rows = selected(reference['indices'], source['members'], 107)
    require(fingerprint(rows) == {key: reference[key] for key in
                                 ['canonical_bytes', 'canonical_sha256']}, 'complete source pin identity')
    normal['inputs'] = rows
    delta = normal['stages']['baseline']['files']['$manifest_delta']
    files = dict(original)
    require(isinstance(delta, dict) and isinstance(delta['set'], dict)
            and isinstance(delta['remove'], list) and len(set(delta['remove'])) == len(delta['remove'])
            and all(p in files for p in delta['remove']), 'baseline removed member population')
    for name in delta['remove']:
        del files[name]
    for name, sha in delta['set'].items():
        C.Q.relative_path(name)
        require(isinstance(sha, str) and re.fullmatch(r'[0-9a-f]{64}', sha), 'baseline file digest')
        files[name] = sha
    require(len(files) == delta['count'] == 344 and fingerprint(files) ==
            {key: delta[key] for key in ['canonical_bytes', 'canonical_sha256']},
            'complete baseline manifest identity')
    excluded = normal['exclusions_from_baseline']
    excluded['paths'] = selected(excluded.pop('indices'), sorted(files), 330)
    require(isinstance(frame['complete'], dict) and set(frame['complete']) ==
            {'canonical_bytes', 'canonical_sha256'} and type(frame['complete']['canonical_bytes']) is int
            and 0 < frame['complete']['canonical_bytes'] <= 524288
            and fingerprint(value) == frame['complete'], 'complete reconstructed capture identity')
    return value


def summary_rows(body, book, members):
    """Independent oracle for this source's closed, plain-label SUMMARY grammar.

    Only blank lines, the opening Summary, root part titles and literal chapter
    links are accepted. Four-space nested bullet lists supply numbered chapters;
    unbulleted root links are unnumbered. Unsupported syntax refuses qualification.
    """
    text = body.decode('utf-8')
    require(text.startswith('# Summary\n'), 'unreviewed SUMMARY heading')
    rows, numbers, parents, seen = [], [], [], set()
    for line_number, line in enumerate(text.splitlines()[1:], 2):
        if not line.strip():
            continue
        if line.startswith('# '):
            title = line[2:]
            require(bool(title) and title == title.strip(), 'invalid plain part title')
            rows.append({'kind': 'part', 'name': title, 'depth': 0})
            parents = []
            continue
        match = re.fullmatch(r'( *)(- )?\[([^\[\]`]+)\]\(([^\s()]+\.md)\)', line)
        require(match is not None, f'unsupported SUMMARY line {book}:{line_number}')
        spaces, bullet, name, path = match.groups()
        require(len(spaces) % 4 == 0 and name == name.strip(), 'invalid SUMMARY indentation/label')
        depth = len(spaces) // 4
        C.Q.relative_path(path)
        require(path not in seen and book + '/src/' + path in members,
                'missing or repeated SUMMARY chapter')
        seen.add(path)
        if bullet:
            require(depth <= len(numbers) and depth <= len(parents), 'SUMMARY hierarchy jumps')
            numbers = numbers[:depth + 1]
            if len(numbers) == depth:
                numbers.append(0)
            numbers[depth] += 1
            number = list(numbers)
            parents = parents[:depth]
        else:
            require(depth == 0, 'nested unnumbered SUMMARY chapter')
            number, parents = None, []
        rows.append({'kind': 'chapter', 'name': name, 'path': path,
                     'source_path': path, 'number': number,
                     'parent_names': list(parents), 'depth': depth})
        parents.append(name)
    require(bool(seen), 'empty SUMMARY chapter population')
    return rows


def protocol_rows(book):
    """Read complete captured chapter metadata independently of the oracle."""
    require(isinstance(book, dict) and isinstance(book.get('items'), list), 'invalid captured book')
    pending = [(item, 0) for item in reversed(book['items'])]
    result = []
    while pending:
        item, depth = pending.pop()
        require(isinstance(item, dict) and len(item) == 1, 'unsupported captured item')
        if 'PartTitle' in item:
            require(depth == 0 and isinstance(item['PartTitle'], str), 'invalid captured part')
            result.append({'kind': 'part', 'name': item['PartTitle'], 'depth': depth})
            continue
        require('Chapter' in item and isinstance(item['Chapter'], dict), 'invalid captured chapter')
        chapter = item['Chapter']
        require(set(chapter) == {'name', 'number', 'sub_items', 'path', 'source_path',
                                 'parent_names', 'content'}, 'unreviewed captured chapter fields')
        require(isinstance(chapter['sub_items'], list) and isinstance(chapter['content'], str),
                'invalid captured chapter data')
        result.append({'kind': 'chapter', **{key: chapter[key] for key in
                       ['name', 'path', 'source_path', 'number', 'parent_names']}, 'depth': depth})
        pending.extend((child, depth + 1) for child in reversed(chapter['sub_items']))
    return result


def expected_toc(rows):
    result = []
    for row in rows:
        if row['kind'] == 'part':
            result.append(dict(row))
        else:
            number = '.'.join(map(str, row['number'])) + '.' if row['number'] else ''
            result.append({'kind': 'chapter', 'name': row['name'], 'depth': row['depth'],
                           'href': row['path'][:-3] + '.html', 'number': number})
    return result


class Contents(HTMLParser):
    """Extract ordered chapter/part rows from the generated contents list.

    List depth supplies hierarchy; strong text supplies displayed numbering.
    Complete original attributes are retained alongside the compared rows.
    """
    def __init__(self, text, iframe):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.anchor = None
        self.part = None
        self.strong = 0
        self.rows, self.attributes = [], []
        self.iframe = iframe
        self.feed(text)
        self.close()
        require(self.depth == 0 and self.anchor is None and self.part is None,
                'unfinished generated TOC structure')

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        require(len(values) == len(attrs), 'duplicate generated TOC attribute')
        if tag == 'ol':
            require(values.get('class') == ('chapter' if self.depth == 0 else 'section'),
                    'unreviewed generated TOC list')
            self.depth += 1
        elif tag == 'li' and values.get('class') == 'part-title':
            require(self.depth == 1 and self.part is None, 'invalid generated part')
            self.part = []
        elif tag == 'a':
            require(self.depth > 0 and self.anchor is None, 'anchor outside chapter contents')
            wanted = {'href', 'target'} if self.iframe else {'href'}
            require(set(values) == wanted and (not self.iframe or values['target'] == '_parent'),
                    'unreviewed chapter TOC anchor attributes')
            self.anchor = {'href': values['href'], 'depth': self.depth - 1,
                           'name': [], 'number': []}
            self.attributes.append(values)
        elif tag == 'strong' and self.anchor is not None:
            require(values == {'aria-hidden': 'true'} and self.strong == 0,
                    'unreviewed chapter numbering')
            self.strong = 1

    def handle_data(self, data):
        if self.anchor is not None:
            self.anchor['number' if self.strong else 'name'].append(data)
        elif self.part is not None:
            self.part.append(data)

    def handle_endtag(self, tag):
        if tag == 'strong' and self.anchor is not None:
            self.strong = 0
        elif tag == 'a':
            require(self.anchor is not None and self.strong == 0, 'unfinished chapter anchor')
            row = self.anchor
            self.rows.append({'kind': 'chapter', 'href': row['href'], 'depth': row['depth'],
                              'name': ''.join(row['name']).strip(),
                              'number': ''.join(row['number']).strip()})
            self.anchor = None
        elif tag == 'li' and self.part is not None:
            self.rows.append({'kind': 'part', 'name': ''.join(self.part).strip(), 'depth': 0})
            self.part = None
        elif tag == 'ol':
            require(self.depth > 0, 'unbalanced chapter contents list')
            self.depth -= 1


def generated_toc(site, book):
    directory = site / book / 'book'
    scripts = list(directory.glob('toc-*.js'))
    require(len(scripts) == 1 and re.fullmatch(r'toc-[0-9a-f]{8}\.js', scripts[0].name),
            'unreviewed chapter TOC script population')
    script = scripts[0].read_bytes()
    literals = re.findall(r"this\.innerHTML = ('(?:[^'\\]|\\.)*');", script.decode('utf-8'))
    require(len(literals) == 1, 'unreviewed chapter TOC JavaScript data framing')
    data = ast.literal_eval(literals[0])
    require(isinstance(data, str), 'non-string chapter TOC data')
    page = directory / 'toc.html'
    html_body = page.read_bytes()
    native, iframe = Contents(data, False), Contents(html_body.decode('utf-8'), True)
    return {'javascript': {'path': scripts[0].relative_to(site).as_posix(),
                          'bytes': len(script), 'sha256': C.digest(script),
                          'data_bytes': len(data.encode()), 'data_sha256': C.digest(data.encode()),
                          'rows': native.rows, 'attributes': native.attributes},
            'html': {'path': page.relative_to(site).as_posix(), 'bytes': len(html_body),
                     'sha256': C.digest(html_body), 'rows': iframe.rows,
                     'attributes': iframe.attributes}}


def assess(book, expected, capture, generated):
    before, after = protocol_rows(capture['before']), protocol_rows(capture['after'])
    wanted = expected_toc(expected)
    return {'book': book, 'expected': expected, 'protocol_before': before,
            'protocol_after': after, 'generated': generated,
            'checks': {'protocol': before == after == expected,
                       'javascript': generated['javascript']['rows'] == wanted,
                       'html': generated['html']['rows'] == wanted},
            'expected_contract': before == after == expected
                and all(value['rows'] == wanted for value in generated.values())}


def omissions(source, output, expected):
    """Execute actual public builds after three supported SUMMARY mutations."""
    book = 'docs/book'
    relative = book + '/src/SUMMARY.md'
    seams = [('chapter', '- [Current status](status.md)\n', ''),
             ('label', '[Current status](status.md)', '[LC0040 changed status](status.md)'),
             ('hierarchy', '    - [P0 — profile and evidence access](plan/p0.md)',
              '- [P0 — profile and evidence access](plan/p0.md)')]
    records = []
    for name, old, new in seams:
        directory = output / ('omit-' + name)
        directory.mkdir()
        fixture, _ = B.copy_source(source, directory)
        path = fixture / relative
        body = path.read_bytes()
        require(body.count(old.encode()) == 1, 'unique supported SUMMARY omission')
        changed = body.replace(old.encode(), new.encode(), 1)
        path.write_bytes(changed)
        stage = N.build_stage(fixture, directory, [book], 'captured')
        capture = stage['captures'][book]
        observed = assess(book, expected[book], capture,
                          generated_toc(directory / 'captured/site', book))
        require(not observed['expected_contract'] and capture['returncode'] == 0,
                'actual supported TOC omission did not discriminate')
        require(path.read_bytes() == changed, 'omitted SUMMARY changed during build')
        path.write_bytes(body)
        B.verify_copy(source, fixture)
        records.append({'role': name, 'source': relative, 'old': old, 'new': new,
                        'changed_source_sha256': C.digest(changed), 'stage': stage,
                        'observation': observed, 'qualification_returncode': 1})
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--addition', action='append', default=[])
    parser.add_argument('--require-clean', action='store_true')
    args = parser.parse_args()
    os.environ['GIT_NO_LAZY_FETCH'] = '1'
    try:
        C.Q.relative_path(args.output)
        require(args.output.startswith('target/'), 'on-volume target output required')
        output = C.U.source_path(ROOT, args.output)
        require(not output.exists(), 'fresh output required')
        before = C.working_snapshot(args.addition)
        source = C.source_census(SOURCE)
        require(len(source['members']) == 1466, 'whole immutable source population')
        output.mkdir(parents=True)
        (output / 'tmp').mkdir()
        fixture, bodies = B.copy_source(source, output)
        units = C.U.registered_units(fixture)
        require(not C.U.catalogue_findings(fixture, units), 'source unit catalogue differs')
        books = ['docs/book', *[u['book'].rstrip('/') for u in units]]
        require(len(books) == 7 and len(set(books)) == 7, 'seven distinct source books')
        expected = {book: summary_rows(bodies[book + '/src/SUMMARY.md'], book, bodies)
                    for book in books}
        require(sum(row['kind'] == 'chapter' for rows in expected.values() for row in rows) == 93,
                'complete source chapter population')
        stages = {name: N.build_stage(fixture, output, books, name)
                  for name in ['baseline', 'captured']}
        require(stages['baseline']['files'] == stages['captured']['files'],
                'capture changed complete output population/bytes')
        observations = []
        for book in books:
            capture = stages['captured']['captures'][book]
            require(capture['root'] == book and capture['mdbook_version'] == '0.5.4'
                    and capture['returncode'] == 0, 'public consumer identity/verdict differs')
            observations.append(assess(book, expected[book], capture,
                                      generated_toc(output / 'captured/site', book)))
        actual_omissions = omissions(source, output, expected)
        selected = {book + '/src/SUMMARY.md' for book in books}
        selected.update(book + '/book.toml' for book in books)
        selected.update(book + '/src/' + row['path'] for book, rows in expected.items()
                        for row in rows if row['kind'] == 'chapter')
        inputs = [row for row in source['members'] if row['path'] in selected]
        require(len(inputs) == 107, 'seven summaries/configs and93 chapter source pins')
        consumed = {value['path'] for row in observations for value in row['generated'].values()}
        exclusions = [{'path': path, 'sha256': sha,
                       'reason': 'outside-chapter-TOC; page headings/search/resources remain open'}
                      for path, sha in stages['baseline']['files'].items() if path not in consumed]
        B.verify_copy(source, fixture)
        require(before == C.working_snapshot(args.addition), 'actual source/index/modes changed')
        defects = sum(not row['expected_contract'] for row in observations)
        result = {'source': SOURCE, 'source_members': 1466, 'source_tree_sha256': source['tree_sha256'],
                  'mode': 'optimized' if sys.flags.optimize else 'normal', 'books': books,
                  'inputs': inputs, 'stages': stages, 'observations': observations,
                  'actual_omissions': actual_omissions, 'exclusions': exclusions,
                  'source_defects': defects}
        N.write_json(output / 'result.json', result)
        print(json.dumps({'source': SOURCE, 'books': len(books),
                          'chapters': 93, 'inputs': len(inputs),
                          'files': len(stages['baseline']['files']), 'toc_files': len(consumed),
                          'exclusions': len(exclusions), 'source_defects': defects,
                          'actual_omissions': len(actual_omissions)}))
        return 1 if args.require_clean and defects else 0
    except (ValueError, OSError, UnicodeError, TypeError, RecursionError,
            subprocess.SubprocessError, KeyError, SyntaxError) as exc:
        print('qualify_book_toc: REFUSED — ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
