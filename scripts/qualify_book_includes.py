#!/usr/bin/env python3
"""Replay the closed LC0028 include ledger, or qualify current before-links inputs.

Historical replay accepts only the reviewed LC0028 source. It copies regular
project blobs into an owned non-Git workspace; Gitlinks remain opaque. Both
modes use public mdBook builds, complete chapter captures and output comparison.
Generated evidence lives under a fresh target/ directory, never another repo.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import posixpath
import re
import shlex
import subprocess
import sys

import book_includes as I
import collect_containment_graph as C

ROOT = C.ROOT
SOURCE = 'cad73f376766572119490b157a98b69ce5ad04f7'
require = C.require


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n',
                    encoding='utf-8')


def checked_run(command, *, env):
    return subprocess.run(command, env=env, capture_output=True, check=False)


def file_set(root: Path) -> dict:
    result = {}
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'symlink in generated output')
        if path.is_file():
            result[path.relative_to(root).as_posix()] = C.digest(path.read_bytes())
    require(bool(result), 'empty generated output')
    return result


def same_files(expected: dict, actual: dict) -> None:
    require(bool(expected) and actual == expected, 'complete output population/bytes differ')


def chapters(book: dict) -> list[dict]:
    require(isinstance(book, dict) and isinstance(book.get('items'), list), 'invalid captured book')
    result = []
    stack = list(reversed(book['items']))
    while stack:
        item = stack.pop()
        if item == 'Separator' or (isinstance(item, dict) and set(item) == {'PartTitle'}):
            continue
        require(isinstance(item, dict) and set(item) == {'Chapter'}, 'unknown captured item')
        chapter = item['Chapter']
        require(isinstance(chapter, dict) and isinstance(chapter.get('source_path'), str)
                and isinstance(chapter.get('content'), str)
                and isinstance(chapter.get('sub_items'), list), 'unqualified captured chapter')
        result.append(chapter)
        stack.extend(reversed(chapter['sub_items']))
    return result


def closed_ledger(source: dict, contents: dict, books: list[str], raw: dict, expanded: dict) -> dict:
    """Reconstruct the historical whole/HTML-anchor subset independently of I.

    Unsupported/transitive selectors refuse. This is the original bounded
    LC0028 projection, not a general Markdown or mdBook implementation.
    """
    members = {r['path']: r for r in source['members']}
    require(len(members) == len(source['members']), 'duplicate source member')
    regular = {n for n, r in members.items() if r['mode'] != '160000'}
    require(regular == set(contents), 'incomplete regular source population')
    for name in regular:
        require(C.digest(contents[name]) == members[name]['sha256'], 'source body identity differs')
        if name.endswith('.md'):
            C.reconcile_includes(contents[name], [r for r in source['include_candidates']
                                                 if r['source'] == name])
    require(len(books) == len(set(books)) and set(raw) == set(expanded) == set(books),
            'incomplete consumer population')
    ledger, records, consumed, targets = [], [], set(), set()
    for book in books:
        before = chapters(raw[book])
        after = chapters(expanded[book])
        require([c['source_path'] for c in before] == [c['source_path'] for c in after],
                'chapter population/order differs')
        for original, rendered in zip(before, after):
            name = posixpath.normpath(book + '/src/' + original['source_path'])
            require(name in contents and name not in consumed, 'unknown/duplicate chapter source')
            consumed.add(name)
            text = contents[name].decode('utf-8').replace('\r\n', '\n')
            require(original['content'] == text, 'captured raw chapter differs from immutable source')
            expected = text
            candidates = [r for r in source['include_candidates'] if r['source'] == name]
            for candidate in candidates:
                marker = candidate['marker']
                match = re.fullmatch(r'\{\{#include\s+(\S+)\s*}}', marker)
                require(match is not None, 'unsupported historical include syntax')
                fields = match[1].split(':')
                require(len(fields) <= 2 and bool(fields[0]), 'unsupported historical selector')
                target = posixpath.normpath(posixpath.join(posixpath.dirname(name), fields[0]))
                require(target in contents and members[target]['mode'] in {'100644', '100755'},
                        'include target not in regular closed source')
                targets.add(target)
                body = contents[target].decode('utf-8').replace('\r\n', '\n')
                require('{{#include' not in body, 'transitive historical include needs qualification')
                selected, selector = body.removesuffix('\n'), 'whole'
                if len(fields) == 2:
                    selector = fields[1]
                    require(re.fullmatch(r'[A-Za-z_-]+', selector) is not None,
                            'unsupported historical anchor')
                    lines = body.removesuffix('\n').split('\n') if body else []
                    starts = [n for n, line in enumerate(lines)
                              if line == '<!-- ANCHOR: ' + selector + ' -->']
                    ends = [n for n, line in enumerate(lines)
                            if line == '<!-- ANCHOR_END: ' + selector + ' -->']
                    require(len(starts) == len(ends) == 1 and starts[0] < ends[0],
                            'ambiguous historical anchor')
                    selected = '\n'.join(lines[starts[0] + 1:ends[0]])
                    require('ANCHOR:' not in selected and 'ANCHOR_END:' not in selected,
                            'nested historical anchor needs qualification')
                require(expected.count(marker) == 1, 'ambiguous marker occurrence')
                expected = expected.replace(marker, selected, 1)
                ledger.append(dict(candidate, consumer=book,
                    chapter_source_oid=members[name]['oid'],
                    chapter_source_sha256=members[name]['sha256'], target=target,
                    target_mode=members[target]['mode'], target_oid=members[target]['oid'],
                    target_sha256=members[target]['sha256'], selection=selector,
                    selected_sha256=C.digest(selected.encode()), selected_bytes=len(selected.encode())))
            require(expected == rendered['content'], 'complete expanded chapter text differs')
            records.append({'consumer': book, 'source': name,
                            'source_sha256': members[name]['sha256'],
                            'expanded_sha256': C.digest(rendered['content'].encode()),
                            'include_occurrences': len(candidates)})
    unused = [r for r in source['include_candidates'] if r['source'] not in consumed]
    require(len(ledger) + len(unused) == len(source['include_candidates']) and
            not ({r['source'] for r in unused} & targets), 'include candidate partition differs')
    return {'source_revision': source['revision'], 'source_tree_sha256': source['tree_sha256'],
            'consumers': books, 'chapters': records, 'executed_occurrences': ledger,
            'unexecuted_candidates': unused, 'unique_targets': sorted(targets),
            'transitive_target_markers': 0}


def copy_source(source: dict, output: Path) -> tuple[Path, dict]:
    rows = C.Q.tree_rows(C.Q.git('ls-tree', '-rz', '--full-tree', source['revision']))
    requests = b''.join(r[2].encode() + b'\n' for r in rows.values() if r[0] != '160000')
    wire = C.Q.checked_output(subprocess.run(['git', '--no-optional-locks', '-C', str(ROOT),
                                            'cat-file', '--batch'], input=requests, capture_output=True))
    bodies = C.blob_contents(rows, wire)
    copied = output / 'source'
    copied.mkdir()
    for name, (mode, _, _) in rows.items():
        if mode == '160000':
            continue
        require(mode in {'100644', '100755'}, 'unsupported source mode')
        path = copied / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(bodies[name])
        path.chmod(0o755 if mode == '100755' else 0o644)
    verify_copy(source, copied)
    return copied, bodies


def verify_copy(source: dict, copied: Path) -> None:
    for row in source['members']:
        if row['mode'] == '160000':
            require(not (copied / row['path']).exists(), 'opaque Gitlink was materialized')
            continue
        actual = C.file_identity((copied / row['path']).relative_to(ROOT).as_posix())
        require(actual == {'sha256': row['sha256'], 'bytes': row['bytes'],
                           'mode': 0o755 if row['mode'] == '100755' else 0o644},
                'copied source bytes/mode differ: ' + row['path'])


def capture(args) -> None:
    if args.action is not None:
        require(args.action == 'supports' and args.renderer == 'html', 'unsupported capture renderer')
        return
    context, book = json.load(sys.stdin)
    path = C.U.source_path(ROOT, args.capture_output)
    require(args.capture_output.startswith('target/') and not path.exists(), 'unsafe/reused capture')
    path.parent.mkdir(parents=True, exist_ok=True)
    root = Path(context['root']).resolve().relative_to(ROOT).as_posix()
    write_json(path, {'root': root, 'renderer': context['renderer'],
                      'mdbook_version': context['mdbook_version'],
                      'config_book': context['config']['book'], 'book': book})
    json.dump(book, sys.stdout, ensure_ascii=False)


def environment() -> dict:
    # A replay uses its reviewed book configuration, not caller overrides.
    return {k: v for k, v in os.environ.items() if not k.startswith('MDBOOK_')
            and k != 'PYTHONOPTIMIZE'}


def build_pair(root: Path, output: Path, *, working: bool) -> dict:
    units = C.U.registered_units(root)
    require(not C.U.catalogue_findings(root, units), 'book catalogue refuses')
    books = ['docs/book', *[u['book'].rstrip('/') for u in units]]
    raw, expanded, reports, baseline, versions = {}, {}, {}, {}, set()
    temporary = output / 'tmp'
    temporary.mkdir()
    for stage in ['baseline', 'captured']:
        site = output / stage / 'site'
        for number, book in enumerate(books):
            env = environment()
            env['TMPDIR'] = str(temporary)
            if sys.flags.optimize:
                env['PYTHONOPTIMIZE'] = '1'
            if stage == 'captured':
                for name, when, before, after in [
                    ('raw-witness', 'raw', ['links'], []),
                    ('expanded-witness', 'expanded', ['project-record-links'], ['links'])]:
                    dest = output / 'captures' / book / (when + '.json')
                    command = shlex.join([sys.executable, str(Path(__file__).resolve()),
                                          '--capture', when, '--capture-output',
                                          dest.relative_to(ROOT).as_posix()])
                    prefix = 'MDBOOK_PREPROCESSOR__' + name.replace('-', '_').upper() + '__'
                    env[prefix + 'COMMAND'] = command
                    env[prefix + 'RENDERERS'] = '["html"]'
                    env[prefix + 'OPTIONAL'] = 'false'
                    if before:
                        env[prefix + 'BEFORE'] = json.dumps(before)
                    if after:
                        env[prefix + 'AFTER'] = json.dumps(after)
                if working:
                    prefix = 'MDBOOK_PREPROCESSOR__SOURCE_CHECK__'
                    env[prefix + 'COMMAND'] = shlex.join([sys.executable, str(ROOT / 'scripts/book_includes.py')])
                    env[prefix + 'BEFORE'] = '["links"]'
                    env[prefix + 'AFTER'] = '["raw-witness"]'
                    env[prefix + 'RENDERERS'] = '["html"]'
                    env[prefix + 'OPTIONAL'] = 'false'
            destination = site / book / 'book'
            log = output / stage
            log.mkdir(parents=True, exist_ok=True)
            result = checked_run(['mdbook', 'build', str(root / book), '-d', str(destination)], env=env)
            (log / (str(number) + '.stdout')).write_bytes(result.stdout)
            (log / (str(number) + '.stderr')).write_bytes(result.stderr)
            require(result.returncode == 0, 'public build refused: ' + book)
            if stage == 'captured':
                a = json.loads((output / 'captures' / book / 'raw.json').read_text())
                b = json.loads((output / 'captures' / book / 'expanded.json').read_text())
                expected_root = (root / book).relative_to(ROOT).as_posix()
                require(a['root'] == b['root'] == expected_root, 'capture consumer identity differs')
                versions.update([a['mdbook_version'], b['mdbook_version']])
                raw[book], expanded[book] = a['book'], b['book']
                if working:
                    context = {'root': str(root / book), 'renderer': a['renderer'],
                               'config': {'book': a['config_book']}}
                    original, report = I.preprocess(context, a['book'], ROOT)
                    require(original == a['book'], 'validator changed complete book object')
                    actual = re.findall(rb'BOOK-INCLUDES: checked ([0-9]+) chapters / ([0-9]+) include edges',
                                        result.stderr)
                    require(actual == [(str(len(report['chapters'])).encode(),
                                        str(len(report['include_edges'])).encode())],
                            'actual validator execution differs from captured input')
                    reports[book] = report
        files = file_set(site)
        if stage == 'baseline':
            baseline = files
        else:
            same_files(baseline, files)
    require(len(versions) == 1, 'ambiguous public mdbook versions')
    return {'books': books, 'raw': raw, 'expanded': expanded, 'reports': reports,
            'output_files': baseline, 'mdbook_version': next(iter(versions))}


def public_fixtures(output: Path) -> dict:
    """Check public expansion against fixture constants and actual read refusals."""
    fragment = ('before\n// ANCHOR: part\nalpha\n// ANCHOR: nested\nbeta\n'
                '// ANCHOR_END: nested\n// ANCHOR_END: part\nafter\n')
    cases = [
        ('whole-lf', '{{#include fragment.txt}}', {'fragment.txt': b'alpha\nbeta\n'}, 'alpha\nbeta'),
        ('whole-no-lf', '{{#include fragment.txt}}', {'fragment.txt': b'alpha\nbeta'}, 'alpha\nbeta'),
        ('whole-two-lfs', '{{#include fragment.txt}}', {'fragment.txt': b'alpha\n\n'}, 'alpha\n'),
        ('whole-crlf', '{{#include fragment.txt}}', {'fragment.txt': b'alpha\r\nbeta\r\n'}, 'alpha\nbeta'),
        ('anchor', '{{#include fragment.txt:part}}', {'fragment.txt': fragment.encode()}, 'alpha\nbeta'),
        ('whole-anchors', '{{#include fragment.txt}}', {'fragment.txt': fragment.encode()},
         fragment.removesuffix('\n')),
        ('range', '{{#include fragment.txt:2:4}}', {'fragment.txt': b'one\ntwo\nthree\nfour\nfive\n'},
         'two\nthree\nfour'),
        ('fenced', '```text\n{{#include fragment.txt}}\n```', {'fragment.txt': b'alpha\nbeta\n'},
         '```text\nalpha\nbeta\n```'),
        ('nested', '{{#include first.txt}}',
         {'first.txt': b'alpha\n{{#include second.txt}}\nomega\n', 'second.txt': b'beta\n'},
         'alpha\nbeta\nomega'),
        ('space-before-hash', '{{ #include fragment.txt}}', {'fragment.txt': b'contract\n'}, 'contract'),
        ('argument-spaces', '{{#include  fragment.txt }}', {'fragment.txt': b'contract\n'}, 'contract'),
        ('argument-tab', '{{#include\tfragment.txt}}', {'fragment.txt': b'contract\n'}, 'contract'),
        ('hash-space', '{{# include fragment.txt}}', {'fragment.txt': b'contract\n'}, None),
        ('hash-both-spaces', '{{ # include fragment.txt}}', {'fragment.txt': b'contract\n'}, None),
        ('missing-file', '{{#include missing.txt}}', {}, None),
        ('missing-anchor', '{{#include fragment.txt:absent}}', {'fragment.txt': fragment.encode()}, None),
        ('duplicate-anchor', '{{#include fragment.txt:part}}',
         {'fragment.txt': b'// ANCHOR: part\nfirst\n// ANCHOR_END: part\n'
                          b'// ANCHOR: part\nsecond\n// ANCHOR_END: part\n'}, None),
    ]
    temporary = output / 'tmp'
    temporary.mkdir()
    records = []
    for label, marker, files, selected in cases:
        root = output / label
        (root / 'src').mkdir(parents=True)
        (root / 'book.toml').write_text('[book]\ntitle = "Include qualification"\nsrc = "src"\n')
        (root / 'src/SUMMARY.md').write_text('# Summary\n\n- [One](one.md)\n')
        (root / 'src/one.md').write_text('START\n' + marker + '\nEND\n')
        for name, body in files.items():
            (root / 'src' / name).write_bytes(body)
        capture_path = root / 'expanded.json'
        env = environment()
        env['TMPDIR'] = str(temporary)
        if sys.flags.optimize:
            env['PYTHONOPTIMIZE'] = '1'
        env['MDBOOK_PREPROCESSOR__SOURCE_CHECK__COMMAND'] = shlex.join(
            [sys.executable, str(ROOT / 'scripts/book_includes.py'), '--root', str(root)])
        env['MDBOOK_PREPROCESSOR__SOURCE_CHECK__BEFORE'] = '["links"]'
        env['MDBOOK_PREPROCESSOR__EXPANDED_WITNESS__COMMAND'] = shlex.join(
            [sys.executable, str(Path(__file__).resolve()), '--capture', 'expanded',
             '--capture-output', capture_path.relative_to(ROOT).as_posix()])
        env['MDBOOK_PREPROCESSOR__EXPANDED_WITNESS__AFTER'] = '["links"]'
        if label.startswith('hash-'):
            bare = {k: v for k, v in env.items() if not k.startswith('MDBOOK_PREPROCESSOR__SOURCE_CHECK__')}
            plain_capture = root / 'unvalidated.json'
            bare['MDBOOK_PREPROCESSOR__EXPANDED_WITNESS__COMMAND'] = shlex.join(
                [sys.executable, str(Path(__file__).resolve()), '--capture', 'expanded',
                 '--capture-output', plain_capture.relative_to(ROOT).as_posix()])
            plain = checked_run(['mdbook', 'build', str(root), '-d', str(root / 'bare-site')], env=bare)
            (root / 'unvalidated.stderr').write_bytes(plain.stderr)
            require(plain.returncode == 0 and plain_capture.is_file(), 'public spacing baseline failed')
            found = chapters(json.loads(plain_capture.read_text())['book'])
            require(len(found) == 1 and found[0]['content'] == 'START\n' + marker + '\nEND\n',
                    'public hash spacing unexpectedly expands')
        result = checked_run(['mdbook', 'build', str(root), '-d', str(root / 'site')], env=env)
        (root / 'stdout').write_bytes(result.stdout)
        (root / 'stderr').write_bytes(result.stderr)
        if selected is None:
            diagnostic = (b'REFUSED' if label.startswith('hash-') else
                          b'missing include/source file' if label == 'missing-file'
                          else b'missing/ambiguous anchor')
            require(result.returncode != 0 and not capture_path.exists()
                    and b'BOOK-INCLUDES: ' in result.stderr and diagnostic in result.stderr,
                    'invalid public include verdict/witness differs: ' + label)
        else:
            require(result.returncode == 0 and capture_path.is_file(), 'valid public include refused: ' + label)
            found = chapters(json.loads(capture_path.read_text())['book'])
            require(len(found) == 1 and found[0]['content'] == 'START\n' + selected + '\nEND\n',
                    'public expanded fixture text differs: ' + label)
        records.append({'case': label, 'returncode': result.returncode,
                        'expanded': selected is not None})
    # Inject into owned fixture reads only. A marker proves the fault executed.
    hook = '''import os
original_open = os.open
original_fstat = os.fstat
watched = None
checks = 0
def marker():
    with open(os.environ['FAULT_LOG'], 'a') as stream:
        stream.write('1\\n')
def opened(path, flags, *args, **kwargs):
    global watched
    if os.fspath(path) == os.environ['FAULT_TARGET']:
        if os.environ['FAULT_KIND'] == 'read':
            marker()
            raise PermissionError('controlled owned source read refusal')
        watched = original_open(path, flags, *args, **kwargs)
        return watched
    return original_open(path, flags, *args, **kwargs)
def statted(fd):
    global checks
    if fd == watched:
        checks += 1
        if checks == 2:
            marker()
            with open(os.environ['FAULT_TARGET'], 'w') as stream:
                stream.write('controlled changed source\\n')
    return original_fstat(fd)
os.open = opened
os.fstat = statted
'''
    faults = []
    for role in ['chapter', 'include']:
        for kind in ['read', 'changed']:
            root = output / ('fault-' + role + '-' + kind)
            (root / 'book/src').mkdir(parents=True)
            injection = root / 'injection'
            injection.mkdir()
            (injection / 'sitecustomize.py').write_text(hook)
            chapter, fragment_path = root / 'book/src/one.md', root / 'book/src/fragment.txt'
            chapter.write_text('{{#include fragment.txt}}\n')
            fragment_path.write_text('contract\n')
            context = {'root': str(root / 'book'), 'renderer': 'html', 'config': {'book': {'src': 'src'}}}
            book = {'items': [{'Chapter': {'source_path': 'one.md', 'content': chapter.read_text(),
                                         'sub_items': []}}]}
            target = chapter if role == 'chapter' else fragment_path
            log = root / 'injections'
            env = environment()
            env.update(PYTHONPATH=str(injection), TMPDIR=str(temporary), FAULT_TARGET=str(target),
                       FAULT_LOG=str(log), FAULT_KIND=kind)
            command = [sys.executable, *(['-O'] if sys.flags.optimize else []),
                       str(ROOT / 'scripts/book_includes.py'), '--root', str(root)]
            result = subprocess.run(command, input=json.dumps([context, book]).encode(),
                                    env=env, capture_output=True, check=False)
            (root / 'stdout').write_bytes(result.stdout)
            (root / 'stderr').write_bytes(result.stderr)
            count = log.read_text().count('1\n') if log.exists() else 0
            require(result.returncode == 2 and not result.stdout and count == 1
                    and b'REFUSED' in result.stderr, 'public source fault did not refuse once')
            faults.append({'role': role, 'fault': kind, 'returncode': result.returncode,
                           'injections': count, 'stdout_bytes': len(result.stdout)})
    result = {'mode': 'optimized' if sys.flags.optimize else 'normal',
              'public_fixtures': records, 'public_faults': faults}
    write_json(output / 'fixtures-result.json', result)
    return result


def omission_controls(output: Path, additions: list[str]) -> dict:
    """Run finite copied omissions; actual working code is never patched."""
    originals = {n: (ROOT / 'scripts' / n).read_text() for n in
                 ['qualify_book_includes.py', 'book_includes.py', 'book_paths.py',
                  'probe_book_includes.py']}
    replay_prefix, replay_suffix = originals['qualify_book_includes.py'].split(
        '\ndef omission_controls(', 1)
    variants = [
        ('ledger-source-population', 'replay',
         "    require(regular == set(contents), 'incomplete regular source population')", '    pass'),
        ('ledger-source-hash', 'replay',
         "        require(C.digest(contents[name]) == members[name]['sha256'], 'source body identity differs')", '        pass'),
        ('ledger-candidate-population', 'replay',
         "            C.reconcile_includes(contents[name], [r for r in source['include_candidates']\n                                                 if r['source'] == name])", '            pass'),
        ('complete-output', 'replay',
         "    require(bool(expected) and actual == expected, 'complete output population/bytes differ')", '    pass'),
        ('skip-include-inputs', 'includes', '                    follow(destination, selector)', '                    None'),
        ('anchor-unique', 'includes', 'if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:',
         'if starts and ends and starts[0] >= ends[0]:'),
        ('hash-spacing', 'includes',
         "INCLUDE = re.compile(r'\\{\\{\\s*#include\\s+([^\\s{}]+)[ \\t]*}}')",
         "INCLUDE = re.compile(r'\\{\\{\\s*#\\s*include\\s+([^\\s{}]+)[ \\t]*}}')"),
        ('range-bounds', 'includes', 'if not 1 <= start <= end <= len(lines):', 'if False:'),
        ('source-field', 'includes', " and 'source_path' in chapter", ''),
        ('book-root-route', 'includes',
         'book_root = inputs.locate(inputs.root, book_root.relative_to(inputs.root).as_posix())',
         'book_root = source_path(inputs.root, book_root.relative_to(inputs.root).as_posix())'),
        ('nested-inputs', 'includes', '            stack.extend(reversed(children))', '            None'),
        ('final-source-stability', 'includes', '    inputs.unchanged()', '    None'),
        ('utf8', 'includes', "body.decode('utf-8')", "body.decode('utf-8', errors='replace')"),
        ('duplicate-json', 'includes', 'object_pairs_hook=unique_object,', ''),
        ('non-json-constant', 'includes', 'parse_constant=invalid_constant', 'parse_constant=None'),
        ('symlink-git-components', 'paths',
         'if cursor.is_symlink() or marker.exists() or marker.is_symlink():', 'if False:'),
        ('source-volume', 'paths',
         'if cursor.exists() and cursor.stat().st_dev != root.stat().st_dev:', 'if False:'),
    ]
    temporary = output / 'tmp'
    temporary.mkdir()
    env = environment()
    env.update(PYTHONPATH=str(ROOT / 'scripts'), TMPDIR=str(temporary))
    command_prefix = [sys.executable, *(['-O'] if sys.flags.optimize else [])]
    records = []
    for label, component, old, new in variants:
        name = {'replay': 'qualify_book_includes.py', 'includes': 'book_includes.py',
                'paths': 'book_paths.py'}[component]
        source = replay_prefix if component == 'replay' else originals[name]
        require(source.count(old) == 1, 'nonunique mutation seam: ' + label)
        mutant = source.replace(old, new, 1)
        if component == 'replay':
            mutant += '\ndef omission_controls(' + replay_suffix
        compile(mutant, name, 'exec')
        root = output / label
        root.mkdir()
        (root / name).write_text(mutant)
        if component == 'replay':
            command = command_prefix + [str(root / name), '--self-test']
        else:
            if component == 'paths':
                (root / 'book_includes.py').write_text(originals['book_includes.py'])
            (root / 'probe_book_includes.py').write_text(originals['probe_book_includes.py'])
            command = command_prefix + [str(root / 'probe_book_includes.py')]
        result = subprocess.run(command, env=env, capture_output=True, check=False, timeout=30)
        (root / 'stdout').write_bytes(result.stdout)
        (root / 'stderr').write_bytes(result.stderr)
        if component == 'replay':
            require(result.returncode == 2 and not result.stdout and b'REFUSED' in result.stderr
                    and b'accepted' in result.stderr, 'producer omission escaped its control: ' + label)
        else:
            require(result.returncode == 1 and b'FAILED (' in result.stderr
                    and b'SyntaxError' not in result.stderr and b'ImportError' not in result.stderr,
                    'component omission escaped its controls: ' + label)
        records.append({'predicate': label, 'component': component, 'returncode': result.returncode,
                        'mutant_sha256': C.digest(mutant.encode()),
                        'stderr_sha256': C.digest(result.stderr)})
    command = command_prefix + [str(ROOT / 'scripts/qualify_book_includes.py'),
                                '--revision', '0' * 40, '--output',
                                (output / 'missing-source').relative_to(ROOT).as_posix()]
    for name in additions:
        command.extend(['--addition', name])
    result = subprocess.run(command, env=env, capture_output=True, check=False, timeout=30)
    require(result.returncode == 2 and not result.stdout and b'REFUSED' in result.stderr,
            'unavailable immutable source was accepted')
    (output / 'missing-source.stderr').write_bytes(result.stderr)
    result = {'mode': 'optimized' if sys.flags.optimize else 'normal', 'omissions': records,
              'missing_source': {'returncode': result.returncode, 'stdout_bytes': len(result.stdout)}}
    write_json(output / 'omissions-result.json', result)
    return result


def self_test() -> int:
    body = b'# One\n{{#include f.txt}}\n'
    bodies = {'docs/book/src/one.md': body, 'docs/book/src/f.txt': b'contract\n',
              'docs/tasks/example.md': b'{{#include teaching}}\n'}
    members = [{'path': n, 'mode': '100644', 'kind': 'blob', 'oid': '0' * 40,
                'bytes': len(b), 'lf_lines': b.count(b'\n'), 'sha256': C.digest(b)}
               for n, b in bodies.items()]
    candidates = [r for n, b in bodies.items() if n.endswith('.md')
                  for r in C.include_candidates(n, b)]
    source = {'revision': '0' * 40, 'tree_sha256': '0' * 64,
              'members': members, 'include_candidates': candidates}
    chapter = {'source_path': 'one.md', 'content': body.decode(), 'sub_items': []}
    raw = {'docs/book': {'items': [{'Chapter': chapter}]}}
    expanded = copy.deepcopy(raw)
    expanded['docs/book']['items'][0]['Chapter']['content'] = '# One\ncontract\n'
    ledger = closed_ledger(source, bodies, ['docs/book'], raw, expanded)
    require(len(ledger['chapters']) == len(ledger['executed_occurrences']) == 1 and
            len(ledger['unexecuted_candidates']) == 1, 'positive ledger population differs')
    refused = 0
    cases = []
    a = copy.deepcopy(source)
    a['members'].pop()
    cases.append((a, bodies, ['docs/book'], raw, expanded))
    a = copy.deepcopy(source)
    a['include_candidates'].pop()
    cases.append((a, bodies, ['docs/book'], raw, expanded))
    a = copy.deepcopy(source)
    a['members'][0]['sha256'] = '0' * 64
    cases.append((a, bodies, ['docs/book'], raw, expanded))
    cases.append((source, bodies, [], raw, expanded))
    a = copy.deepcopy(expanded)
    a['docs/book']['items'] = []
    cases.append((source, bodies, ['docs/book'], raw, a))
    a = copy.deepcopy(expanded)
    a['docs/book']['items'][0]['Chapter']['content'] = 'wrong'
    cases.append((source, bodies, ['docs/book'], raw, a))
    a, b = copy.deepcopy(raw), copy.deepcopy(expanded)
    a['docs/book']['items'] *= 2
    b['docs/book']['items'] *= 2
    cases.append((source, bodies, ['docs/book'], a, b))
    for case in cases:
        try:
            closed_ledger(*case)
        except C.Q.Refused:
            refused += 1
        else:
            raise C.Q.Refused('omitted/mismatched ledger input was accepted')
    for actual in [{}, {'page': 'changed'}, {'page': 'ok', 'extra': 'ok'}]:
        try:
            same_files({'page': 'ok'}, actual)
        except C.Q.Refused:
            refused += 1
        else:
            raise C.Q.Refused('changed output files were accepted')
    require(refused == 10, 'finite control population differs')
    return refused


def qualify(args) -> dict:
    C.Q.relative_path(args.output)
    require(args.output.startswith('target/'), 'output must be under target/')
    output = C.U.source_path(ROOT, args.output)
    require(not output.exists(), 'output exists; choose a fresh evidence directory')
    before = C.working_snapshot(args.addition)
    output.mkdir(parents=True, exist_ok=False)
    if args.fixtures or args.omissions:
        result = (public_fixtures(output) if args.fixtures
                  else omission_controls(output, args.addition))
        require(before == C.working_snapshot(args.addition), 'actual source/index/modes changed')
        write_json(output / 'working-before.json', before)
        write_json(output / 'working-after.json', before)
        return result
    if args.working:
        root, source, bodies = ROOT, None, None
    else:
        source = C.source_census(args.revision)
        require(source['revision'] == SOURCE, 'only the reviewed LC0028 source is executable replay')
        root, bodies = copy_source(source, output)
        write_json(output / 'source.json', source)
    built = build_pair(root, output, working=args.working)
    if args.working:
        report = {'input_kind': 'working', 'working_inputs': before,
                  'books': built['books'], 'reports': built['reports']}
        write_json(output / 'working-report.json', report)
        count = sum(len(r['chapters']) for r in built['reports'].values())
        includes = sum(len(r['include_edges']) for r in built['reports'].values())
        ledger_sha = None
    else:
        ledger = closed_ledger(source, bodies, built['books'], built['raw'], built['expanded'])
        write_json(output / 'reader-ledger.json', ledger)
        verify_copy(source, root)
        count, includes = len(ledger['chapters']), len(ledger['executed_occurrences'])
        ledger_sha = C.digest((output / 'reader-ledger.json').read_bytes())
    require(before == C.working_snapshot(args.addition), 'actual source/index/modes changed')
    write_json(output / 'working-before.json', before)
    write_json(output / 'working-after.json', before)
    write_json(output / 'output-files.json', built['output_files'])
    result = {'input_kind': 'working' if args.working else 'immutable-source',
              'source': before['head'] if args.working else source['revision'],
              'books': len(built['books']), 'chapters': count, 'includes': includes,
              'output_files': len(built['output_files']), 'mdbook_version': built['mdbook_version'],
              'ledger_sha256': ledger_sha, 'controls': 10,
              'qualification_scope': 'finite include/complete-output evidence; full graph/adoption open'}
    write_json(output / 'result.json', result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', default=SOURCE)
    parser.add_argument('--working', action='store_true')
    parser.add_argument('--output')
    parser.add_argument('--addition', action='append', default=[])
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--fixtures', action='store_true')
    parser.add_argument('--omissions', action='store_true')
    parser.add_argument('--capture', choices=['raw', 'expanded'])
    parser.add_argument('--capture-output')
    parser.add_argument('action', nargs='?')
    parser.add_argument('renderer', nargs='?')
    args = parser.parse_args(argv)
    os.environ['GIT_NO_LAZY_FETCH'] = '1'
    try:
        if args.capture:
            capture(args)
            return 0
        require(args.action is None and args.renderer is None, 'unexpected action')
        require(sum([args.fixtures, args.working, args.omissions]) <= 1,
                '--fixtures, --omissions and --working are distinct inputs')
        controls = self_test()
        if args.self_test:
            print('book-include replay controls: ' + str(controls) + ' pass / 0 fail')
            return 0
        require(args.output is not None, 'required --output under target/')
        print(json.dumps(qualify(args), sort_keys=True))
        return 0
    except (C.Q.Refused, I.IncludeRefused, I.IncludeDefect, OSError, UnicodeError,
            ValueError, KeyError, TypeError, RecursionError) as exc:
        print('BOOK-INCLUDE-REPLAY: REFUSED — ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
