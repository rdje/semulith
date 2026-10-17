#!/usr/bin/env python3
"""Replay LC0043's public heading-context repair with immutable source readers.

Fresh --output target/PATH captures complete source/current seven-book DOMs.
--require-clean fails1 on current wrong contracts; unavailable evidence refuses2.
Record queries need pinned Git objects/producers; no fetch or raw-browser replay.
"""
from __future__ import annotations

import argparse
import base64
import contextlib
import json
import lzma
import os
from pathlib import Path
import posixpath
import re
import shutil
import subprocess
import sys

import qualify_book_headings as Q

C, B, N, T, H = Q.C, Q.B, Q.N, Q.T, Q.H
ROOT = C.ROOT
SOURCE = '5c72864f071b2b097a392c352d842f76c6096edf'
CONFIG = 'docs/book/book.toml'
SCRIPT = 'docs/book/theme/active-chapter.js'
PRODUCER = 'scripts/qualify_heading_repair.py'
RECORD = 'docs/tasks/artifacts/live-containment/include-source-validator.md'
MARKER = '## Authored-index context repair — LC0043\n'
SETTING = b'additional-js = ["theme/active-chapter.js"]\n'
require = C.require


def source_inputs():
    os.environ['GIT_NO_LAZY_FETCH'] = '1'
    source = C.source_census(SOURCE)
    members = {row['path']: row for row in source['members']}
    require(len(members) == 1481, 'whole repair source population differs')
    for name in ['scripts/qualify_book_headings.py',
                 'scripts/book_headings_webkit.swift', 'scripts/collect_containment_graph.py',
                 'scripts/qualify_book_includes.py', 'scripts/qualify_book_navigation.py',
                 'scripts/qualify_book_toc.py', 'scripts/unit_books.py',
                 'scripts/book_navigation.py', 'scripts/book_includes.py']:
        row = members[name]
        require(C.file_identity(name) == {'bytes': row['bytes'], 'sha256': row['sha256'],
                                        'mode': int(row['mode'][-3:], 8)},
                'unreviewed repair helper: ' + name)
    return source, members


def product_inputs():
    original = C.Q.git('show', SOURCE + ':' + CONFIG)
    old = b'no-section-label = false\n'
    require(original.count(old) == 1 and SETTING not in original, 'unique public configuration site')
    expected = original.replace(old, old + SETTING, 1)
    require((ROOT / CONFIG).read_bytes() == expected, 'repair configuration exceeds owned addition')
    return {name: C.file_identity(name) for name in [CONFIG, SCRIPT]}, expected


def mdbook_version(tmp):
    result = subprocess.run(['mdbook', '--version'], capture_output=True, timeout=10,
                            env=dict(os.environ, TMPDIR=str(tmp)))
    require(result.returncode == 0 and not result.stderr and result.stdout == b'mdbook v0.5.4\n',
            'unreviewed public mdBook version')
    return result.stdout.decode().strip()


def build(fixture, output, books):
    output.mkdir()
    (output / 'tmp').mkdir()
    # The baseline spelling selects the actual default preprocessors, not wrappers.
    stage = N.build_stage(fixture, output, books, 'baseline')
    return output / 'baseline/site', stage


def recase(site, original):
    cases = []
    for case in original:
        body = (site / case['path']).read_bytes()
        document = Q.Document(body)
        require(document.headers() == case['source_headers'] and document.title() == case['source_title'],
                'product overlay changed heading/title bytes: ' + case['path'])
        cases.append({**case, 'source_bytes': len(body), 'source_sha256': C.digest(body)})
    return cases


def static_inverse(before, after, old_stage, new_stage, cases):
    old, new = old_stage['files'], new_stage['files']
    added = set(new) - set(old)
    require(set(old) <= set(new) and len(added) == 1, 'product output membership differs')
    script = added.pop()
    require(re.fullmatch(r'docs/book/book/theme/active-chapter-[0-9a-f]+\.js', script) is not None
            and (after / script).read_bytes() == (ROOT / SCRIPT).read_bytes(),
            'public renderer did not copy the owned script exactly')
    changed = []
    for name in sorted(old):
        a, b = (before / name).read_bytes(), (after / name).read_bytes()
        if a == b:
            continue
        require(name.startswith('docs/book/book/') and name.endswith('.html'),
                'non-main-HTML output changed: ' + name)
        expected = posixpath.relpath(script, posixpath.dirname(name))
        pattern = re.compile(rb'^[ \t]*<script src="' + re.escape(expected.encode())
                             + rb'"></script>\n', re.M)
        reconstructed, count = pattern.subn(b'', b)
        require(count == 1 and reconstructed == a, 'whole generated HTML insertion inverse: ' + name)
        changed.append(name)
    chapters = {case['path'] for case in cases if case['book'] == 'docs/book' and case['role'] == 'chapter'}
    require(chapters <= set(changed) and 'docs/book/book/index.html' in changed,
            'complete authored chapter integration differs')
    return {'added_script': script, 'changed_html': changed,
            'unchanged_original_outputs': len(old) - len(changed), 'whole_insertion_inverse': True}


@contextlib.contextmanager
def changed_file(path, body):
    original = path.read_bytes()
    try:
        path.write_bytes(body)
        yield
    finally:
        path.write_bytes(original)


def controls(program, fixture, books, fixed_site, fixed_stage, cases, output, script):
    index = next(case for case in cases if case['path'] == 'docs/book/book/index.html')
    summary = fixture / 'docs/book/src/SUMMARY.md'
    original_summary = summary.read_bytes()
    removed = b'[Index](index.md)\n'
    require(original_summary.count(removed) == 1, 'unique supported SUMMARY omission')
    with changed_file(summary, original_summary.replace(removed, b'', 1)):
        alias_site, alias_stage = build(fixture, output / 'alias-configuration', books)
    first = next(row for row in T.summary_rows(original_summary, 'docs/book',
                 {r['path']: r for r in C.source_census(SOURCE)['members']}) if row['kind'] == 'chapter')
    chapter = next(case for case in cases if case['book'] == 'docs/book'
                   and case['chapter_path'] == first['path'])
    body = (alias_site / index['path']).read_bytes()
    document = Q.Document(body)
    require(document.headers() == chapter['source_headers'] and document.title() == chapter['source_title'],
            'supported main index alias changed its first chapter')
    alias = {**chapter, 'path': index['path'], 'role': 'index-alias',
             'source_bytes': len(body), 'source_sha256': C.digest(body)}
    rows, requests = Q.run_cases(program, alias_site, [alias], output / 'alias-browser', jobs=1)
    require(rows[0]['observation']['expected_contract'], 'repair lost supported main-book alias')
    alias_capture = {'summary_removed': removed.decode(), 'stage': alias_stage,
                     'observations': rows, 'requests': requests}
    result = []
    original = (fixed_site / script).read_bytes()
    variants = [
        ('active-class', fixed_site, index,
         b'        link.classList.toggle("active", link === matches[0]);', b'        ;'),
        ('alias-guard', alias_site, alias,
         b'    if (matches.length !== 1) return;', b'    ;'),
    ]
    for role, site, case, old, new in variants:
        directory = output / ('omit-' + role)
        copied = directory / 'site'
        shutil.copytree(site, copied)
        require(original.count(old) == 1 and (copied / script).read_bytes() == original,
                'unique actual repair omission: ' + role)
        altered = original.replace(old, new, 1)
        (copied / script).write_bytes(altered)
        observations, requests = Q.run_cases(program, copied, [case], directory / 'browser', jobs=1)
        require(observations[0]['process']['returncode'] == 0 and
                not observations[0]['observation']['expected_contract'],
                'actual repair omission did not discriminate: ' + role)
        result.append({'role': role, 'old': old.decode(), 'new': new.decode(),
                       'original_sha256': C.digest(original), 'omitted_sha256': C.digest(altered),
                       'observations': observations, 'requests': requests, 'files': B.file_set(copied)})
    config = fixture / CONFIG
    require(config.read_bytes().count(SETTING) == 1, 'unique actual configuration omission')
    with changed_file(config, config.read_bytes().replace(SETTING, b'', 1)):
        site, stage = build(fixture, output / 'omit-configuration', books)
    body = (site / index['path']).read_bytes()
    case = {**index, 'source_bytes': len(body), 'source_sha256': C.digest(body)}
    observations, requests = Q.run_cases(program, site, [case], output / 'omit-configuration-browser', jobs=1)
    require(not observations[0]['observation']['expected_contract'],
            'actual additional-js omission did not discriminate')
    result.append({'role': 'configuration', 'old': SETTING.decode(), 'new': '',
                   'observations': observations, 'requests': requests, 'files': stage['files']})
    require(B.file_set(fixed_site) == fixed_stage['files'], 'actual controls changed the fixed bundle')
    return alias_capture, result


def qualify(output, jobs):
    require(not output.exists(), 'fresh repair output required')
    additions = [PRODUCER, SCRIPT]
    before = C.working_snapshot(additions)
    source, members = source_inputs()
    products, config = product_inputs()
    output.mkdir()
    program, compiler = Q.compile_webkit(output)
    mdbook = mdbook_version(program.parent / 'tmp')
    engine = Q.browser_identity(program)
    calibration = Q.calibrate(program, output)
    fixture, baseline_site, baseline_stage, cases, pins = Q.prepare(source, members, output)
    books = [row['book'] for row in baseline_stage['builds']]
    baseline, requests = Q.run_cases(program, baseline_site, cases, output / 'source-browser', jobs=jobs)
    source_bad = [row['observation']['path'] for row in baseline if not row['observation']['expected_contract']]
    require(source_bad == ['docs/book/book/index.html'], 'immutable source D78 boundary differs')
    for name, body in [(CONFIG, config), (SCRIPT, (ROOT / SCRIPT).read_bytes())]:
        path = fixture / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
        path.chmod(products[name]['mode'])
    site, stage = build(fixture, output / 'fixed', books)
    fixed_cases = recase(site, cases)
    inverse = static_inverse(baseline_site, site, baseline_stage, stage, cases)
    fixed, fixed_requests = Q.run_cases(program, site, fixed_cases, output / 'fixed-browser', jobs=jobs)
    bad = [row['observation']['path'] for row in fixed if not row['observation']['expected_contract']]
    alias, omissions = controls(program, fixture, books, site, stage, fixed_cases, output, inverse['added_script'])
    B.verify_copy({**source, 'members': [row for row in source['members'] if row['path'] != CONFIG]}, fixture)
    require(all(C.file_identity((fixture / name).relative_to(ROOT).as_posix()) == pin
                for name, pin in products.items()), 'copied product overlay changed')
    require(B.file_set(baseline_site) == baseline_stage['files'] and B.file_set(site) == stage['files'],
            'source/current generated bundle changed')
    require(Q.browser_identity(program) == engine, 'repair engine identity changed')
    require(mdbook_version(program.parent / 'tmp') == mdbook, 'public mdBook version changed')
    require(C.working_snapshot(additions) == before, 'actual source/index/modes changed during repair capture')
    N.write_json(output / 'working-before.json', before)
    N.write_json(output / 'working-after.json', before)
    return {'source': SOURCE, 'source_members': 1481, 'source_tree_sha256': source['tree_sha256'],
            'mode': 'optimized' if sys.flags.optimize else 'normal', 'engine': engine, 'compiler': compiler,
            'calibration': calibration, 'mdbook': mdbook, 'inputs': pins, 'products': products,
            'baseline': {'stage': baseline_stage, 'observations': baseline, 'requests': requests},
            'fixed': {'stage': stage, 'observations': fixed, 'requests': fixed_requests},
            'static_inverse': inverse, 'alias': alias, 'actual_omissions': omissions,
            'source_defects': len(source_bad), 'current_defects': len(bad), 'wrong_contract_paths': bad}


def packed(raw):
    value = json.loads(Q.canonical(raw))
    def requests(rows):
        counts = Q.Counter(row['path'] for row in rows)
        return {'count': len(rows), **Q.fingerprint(rows),
                'footprint': [{'path': name, 'reads': counts[name]} for name in sorted(counts)]}
    for run in [value['baseline'], value['fixed'], value['alias'], *value['actual_omissions']]:
        run['requests'] = requests(run['requests'])
        if 'files' in run:
            run['files'] = {'count': len(run['files']), **Q.fingerprint(run['files'])}
    return value


def validate(value):
    require(isinstance(value, dict) and set(value) ==
            {'normal', 'optimized_overrides', 'book_seams', 'task_seams'}, 'unreviewed repair capture fields')
    source, members = source_inputs()
    expected, pins = set(), set()
    for summary in sorted(name for name in members if name.startswith('docs/') and name.endswith('/src/SUMMARY.md')):
        book = summary.removesuffix('/src/SUMMARY.md')
        rows = T.summary_rows(C.Q.git('show', SOURCE + ':' + summary), book, members)
        chapters = [row for row in rows if row['kind'] == 'chapter']
        expected.update(book + '/book/' + row['path'][:-3] + '.html' for row in chapters)
        expected.update(book + '/book/' + name + '.html' for name in ['index', 'print', 'toc', '404'])
        pins.update([summary, book + '/book.toml'])
        pins.update(book + '/src/' + row['path'] for row in chapters)
    optimized = Q.apply_changes(value['normal'], value['optimized_overrides'])
    for mode, result in [('normal', value['normal']), ('optimized', optimized)]:
        require(result['source'] == SOURCE and type(result['source_members']) is int
                and result['source_members'] == 1481 and result['source_tree_sha256'] == source['tree_sha256']
                and result['mode'] == mode, 'repair source identity differs')
        require(result['mdbook'] == 'mdbook v0.5.4', 'recorded public mdBook version differs')
        require(result['inputs'] == [members[name] for name in sorted(pins)] and len(pins) == 107,
                'whole repair input pins differ')
        for role, count in [('baseline', 344), ('fixed', 345)]:
            run = result[role]
            paths = [row['observation']['path'] for row in run['observations']]
            require(paths == sorted(expected) and len(paths) == 120 and len(run['stage']['files']) == count
                    and len(run['stage']['builds']) == 7, 'complete repair page/output membership differs')
        baseline_bad = [row['observation']['path'] for row in result['baseline']['observations']
                        if not row['observation']['expected_contract']]
        fixed_bad = [row['observation']['path'] for row in result['fixed']['observations']
                     if not row['observation']['expected_contract']]
        require(baseline_bad == ['docs/book/book/index.html'] and type(result['source_defects']) is int
                and result['source_defects'] == 1 and type(result['current_defects']) is int
                and result['current_defects'] == len(fixed_bad) and result['wrong_contract_paths'] == fixed_bad,
                'repair verdict ledger differs')
        require(len(result['actual_omissions']) == 3 and len(result['calibration']) == 4
                and result['alias']['observations'][0]['observation']['expected_contract'] is True,
                'repair controls incomplete')
    for key in ['book_seams', 'task_seams']:
        require(isinstance(value[key], dict), 'invalid retained repair seams')
        for name, seams in value[key].items():
            C.Q.relative_path(name)
            text = C.Q.git('show', SOURCE + ':' + name).decode()
            for old, new in seams:
                require(isinstance(old, str) and isinstance(new, str) and text.count(old) == 1,
                        'retained source seam differs')
                text = text.replace(old, new, 1)
    return value


def encode_capture(normal, optimized, book_seams, task_seams):
    n, o = packed(normal), packed(optimized)
    value = {'normal': n, 'optimized_overrides': list(T.metadata_changes(n, o)),
             'book_seams': book_seams, 'task_seams': task_seams}
    validate(value)
    compact = json.loads(Q.canonical(value))
    source, _ = source_inputs()
    positions = {row['path']: index for index, row in enumerate(source['members'])}
    inputs = compact['normal']['inputs']
    indices = [positions[row['path']] for row in inputs]
    require([source['members'][index] for index in indices] == inputs, 'repair source-row reference differs')
    compact['normal']['inputs'] = {'$source_rows': {'indices': indices, **Q.fingerprint(inputs)}}
    for role in ['baseline', 'fixed']:
        run = compact['normal'][role]
        for row in run['observations']:
            observation = row['observation']
            require(observation['source_sha256'] == run['stage']['files'][observation['path']],
                    'repair page/manifest identity differs')
            require(observation['expected_navigation'] == Q.expected_navigation(
                observation['browser']['headers'], observation['role'] in {'chapter', 'index-alias'}),
                'repair oracle reconstruction differs')
            del observation['source_sha256']
            del observation['expected_navigation']
    compact['normal']['fixed'] = {'$baseline_changes': list(T.metadata_changes(
        compact['normal']['baseline'], compact['normal']['fixed']))}
    body = Q.canonical(compact)
    require(0 < len(body) <= 8 * 1024 * 1024, 'repair metadata exceeds bound')
    blob = lzma.compress(body, format=lzma.FORMAT_XZ,
                         filters=[{'id': lzma.FILTER_LZMA2, 'preset': 6, 'dict_size': 8 * 1024 * 1024}])
    return {'schema_version': 1, 'encoding': 'xz6/base64 canonical UTF-8 JSON',
            'metadata_bytes': len(body), 'metadata_sha256': C.digest(body),
            'compressed_bytes': len(blob), 'compressed_sha256': C.digest(blob),
            'metadata_xz_base64': base64.b64encode(blob).decode(), 'producer': C.file_identity(PRODUCER)}


def expand(value):
    source, _ = source_inputs()
    reference = value['normal']['inputs']['$source_rows']
    indices = reference['indices']
    require(isinstance(indices, list) and all(type(index) is int and 0 <= index < len(source['members'])
            for index in indices) and len(indices) == len(set(indices)), 'invalid repair source-row indices')
    inputs = [source['members'][index] for index in indices]
    require(Q.fingerprint(inputs) == {key: reference[key] for key in ['canonical_bytes', 'canonical_sha256']},
            'expanded repair source pins differ')
    value['normal']['inputs'] = inputs
    value['normal']['fixed'] = Q.apply_changes(value['normal']['baseline'],
        value['normal']['fixed']['$baseline_changes'])
    for role in ['baseline', 'fixed']:
        run = value['normal'][role]
        for row in run['observations']:
            observation = row['observation']
            require('source_sha256' not in observation and 'expected_navigation' not in observation,
                    'ambiguous reconstructed repair fields')
            observation['source_sha256'] = run['stage']['files'][observation['path']]
            observation['expected_navigation'] = Q.expected_navigation(
                observation['browser']['headers'], observation['role'] in {'chapter', 'index-alias'})
    return value


def decode_capture(frame):
    try:
        require(isinstance(frame, dict) and set(frame) == {'schema_version', 'encoding', 'metadata_bytes',
                'metadata_sha256', 'compressed_bytes', 'compressed_sha256', 'metadata_xz_base64', 'producer'},
                'unreviewed repair frame fields')
        require(type(frame['schema_version']) is int and frame['schema_version'] == 1
                and frame['encoding'] == 'xz6/base64 canonical UTF-8 JSON'
                and frame['producer'] == C.file_identity(PRODUCER), 'repair frame/producer identity differs')
        require(type(frame['metadata_bytes']) is int and 0 < frame['metadata_bytes'] <= 8 * 1024 * 1024
                and type(frame['compressed_bytes']) is int and 0 < frame['compressed_bytes'] <= 1024 * 1024
                and H.identity(frame['metadata_sha256'], 64) and H.identity(frame['compressed_sha256'], 64),
                'repair frame identity/bound differs')
        require(isinstance(frame['metadata_xz_base64'], str)
                and len(frame['metadata_xz_base64']) <= 2 * frame['compressed_bytes'], 'repair base64 exceeds bound')
        blob = base64.b64decode(frame['metadata_xz_base64'], validate=True)
        require(len(blob) == frame['compressed_bytes'] and C.digest(blob) == frame['compressed_sha256'],
                'repair compressed identity differs')
        decoder = lzma.LZMADecompressor(format=lzma.FORMAT_XZ, memlimit=64 * 1024 * 1024)
        body = decoder.decompress(blob, max_length=frame['metadata_bytes'] + 1)
        require(decoder.eof and not decoder.unused_data and len(body) == frame['metadata_bytes']
                and C.digest(body) == frame['metadata_sha256'], 'repair expansion identity/bound differs')
        return validate(expand(H.json_object(body)))
    except (KeyError, TypeError, IndexError, UnicodeError, RecursionError, lzma.LZMAError) as exc:
        raise ValueError('repair capture refused') from exc


def record_frame(path):
    C.Q.relative_path(path)
    source = C.U.source_path(ROOT, path)
    require(source.is_file() and source.stat().st_size <= 131072, 'bounded repair record required')
    text = source.read_text()
    require(text.count(MARKER) == 1, 'unique repair capture phase required')
    match = re.search(r'^```json\n(.*?)\n```$', text.split(MARKER, 1)[1], re.M | re.S)
    require(match is not None, 'repair capture frame unavailable')
    return H.json_object(match[1].encode())


def codec_controls(frame):
    original = decode_capture(frame)
    compact = H.json_object(lzma.decompress(base64.b64decode(frame['metadata_xz_base64'])))
    controls = []
    for name in ['sha', 'bool-bound', 'trailing-xz', 'tree', 'missing-page', 'bool-verdict', 'source-seam']:
        changed = json.loads(Q.canonical(frame))
        value = json.loads(Q.canonical(compact))
        inner = False
        if name == 'sha':
            changed['compressed_sha256'] = '0' * 64
        elif name == 'bool-bound':
            changed['metadata_bytes'] = True
        elif name == 'trailing-xz':
            blob = base64.b64decode(changed['metadata_xz_base64']) + b'trailing'
            changed.update(compressed_bytes=len(blob), compressed_sha256=C.digest(blob),
                           metadata_xz_base64=base64.b64encode(blob).decode())
        elif name == 'tree':
            value['normal']['source_tree_sha256'] = '0' * 64
            inner = True
        elif name == 'missing-page':
            value['normal']['baseline']['observations'].pop()
            inner = True
        elif name == 'bool-verdict':
            value['normal']['current_defects'] = False
            inner = True
        elif name == 'source-seam':
            value['task_seams'] = {'docs/tasks/LIVE-CONTAINMENT.md': [['absent source seam', 'replacement']]}
            inner = True
        if inner:
            body = Q.canonical(value)
            blob = lzma.compress(body, format=lzma.FORMAT_XZ,
                                 filters=[{'id': lzma.FILTER_LZMA2, 'preset': 6, 'dict_size': 8 * 1024 * 1024}])
            changed.update(metadata_bytes=len(body), metadata_sha256=C.digest(body), compressed_bytes=len(blob),
                           compressed_sha256=C.digest(blob), metadata_xz_base64=base64.b64encode(blob).decode())
        try:
            decode_capture(changed)
        except ValueError as exc:
            controls.append({'case': name, 'refused': True, 'reason': str(exc)})
        else:
            raise ValueError('repair decoder accepted control: ' + name)
    require(decode_capture(frame) == original, 'repair controls changed original capture')
    return controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output')
    parser.add_argument('--jobs', type=int, choices=[1, 2], default=2)
    parser.add_argument('--require-clean', action='store_true')
    parser.add_argument('--record', default=RECORD)
    parser.add_argument('--verify-record', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    try:
        if args.verify_record or args.self_test:
            require(args.output is None and not args.require_clean, 'repair query does not accept capture options')
            frame = record_frame(args.record)
            value = decode_capture(frame)
            controls = codec_controls(frame) if args.self_test else []
            print(json.dumps({'source': SOURCE, 'pages': len(value['normal']['fixed']['observations']),
                              'current_defects': value['normal']['current_defects'], 'controls': len(controls)}))
            return 0
        require(args.output is not None, 'fresh repair output required')
        C.Q.relative_path(args.output)
        require(args.output.startswith('target/'), 'owned target repair output required')
        output = C.U.source_path(ROOT, args.output)
        value = qualify(output, args.jobs)
        N.write_json(output / 'result.json', value)
        print(json.dumps({'source': SOURCE, 'pages': len(value['fixed']['observations']),
                          'source_defects': value['source_defects'], 'current_defects': value['current_defects'],
                          'actual_omissions': len(value['actual_omissions'])}))
        return 1 if args.require_clean and value['current_defects'] else 0
    except (ValueError, OSError, UnicodeError, subprocess.SubprocessError) as exc:
        print('HEADING-REPAIR: REFUSED — ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
