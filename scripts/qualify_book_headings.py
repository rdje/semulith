#!/usr/bin/env python3
"""Qualify pinned seven-book heading navigation through public browser DOMs.

Use a fresh --output target/PATH. Compile the owned nonpersistent WebKit adapter
using the read-only OS Swift/WebKit toolchain; caches/temp and captures stay on
volume. Measurement exits0, --require-clean fails1 on wrong heading contracts,
and unavailable/unsupported evidence refuses2. Visual/scroll behavior, search,
resource completeness and processor acceptance remain separate qualifications.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter
import concurrent.futures
import contextlib
from dataclasses import dataclass, field
import hashlib
from html.parser import HTMLParser
import http.server
import json
import lzma
import os
from pathlib import Path
import posixpath
import re
import shutil
import signal
import subprocess
import sys
import threading
import tomllib
from urllib.parse import quote, unquote, urlsplit

import collect_containment_graph as C
import qualify_book_includes as B
import qualify_book_navigation as N
import qualify_book_toc as T
import task_history_archive as H

ROOT = C.ROOT
SOURCE = '1226311fcbef388d92c65fdf596f39a4e06d78cb'
SOURCE_MEMBERS = 1477
require = C.require
MAX_HTML = 8 * 1024 * 1024
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'param', 'source', 'track', 'wbr'}
WITNESS = 'semulith-heading-observation'
ALLOCATOR = 'Trying to load the allocator multiple times. This is *not* supported.'
DISPLAY = re.compile(r'\[\d+:\d+:\d+/\d+\.\d+:ERROR:ui/display/mac/'
                     r'cv_display_link_mac\.mm:\d+\] '
                     r'CVDisplayLinkCreateWithCGDisplay failed\. CVReturn: -6670')
PRIORITY = re.compile(r'\[\d+:\d+:\d+/\d+\.\d+:ERROR:base/process/process_mac\.cc:\d+\] '
                      r'task_policy_set TASK_CATEGORY_POLICY: \(os/kern\) invalid argument \(4\)')

# Observational only: capture the browser's public DOM after its own listeners.
# The independent Python reader below reconciles these rows with serialized DOM.
OBSERVER = r'''<script id="semulith-heading-observer">
(() => {
    const errors = [];
    window.addEventListener('error', event => {
        if (event instanceof ErrorEvent) {
            errors.push({message: event.message, line: event.lineno, column: event.colno});
        }
    });
    function markup(nodes) {
        const result = [];
        function append(value) {
            if (typeof value === 'string' && typeof result[result.length - 1] === 'string') {
                result[result.length - 1] += value;
            } else { result.push(value); }
        }
        for (const node of nodes) {
            if (node.nodeType === Node.TEXT_NODE) { append(node.data); }
            else if (node.nodeType === Node.COMMENT_NODE) { append({comment: node.data}); }
            else if (node.nodeType === Node.ELEMENT_NODE) {
                append({tag: node.tagName.toLowerCase(),
                        attrs: [...node.attributes].map(a => [a.name, a.value]).sort(),
                        children: markup(node.childNodes)});
            } else { throw new Error('unreviewed heading node type'); }
        }
        return result;
    }
    function attrs(node) {
        return [...node.attributes].map(a => [a.name, a.value]).sort();
    }
    window.addEventListener('load', () => {
        const main = document.querySelector('main');
        const counts = new Map();
        for (const node of document.querySelectorAll('[id]')) {
            counts.set(node.id, (counts.get(node.id) || 0) + 1);
        }
        const headers = main ? [...main.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => {
            const first = h.firstElementChild;
            return {level: Number(h.tagName[1]), id: h.id, attrs: attrs(h),
                    text: h.textContent, id_count: h.id ? (counts.get(h.id) || 0) : 0,
                    first_tag: first ? first.tagName.toLowerCase() : null,
                    anchor_attrs: first && first.tagName === 'A' ? attrs(first) : null,
                    label_text: first && first.tagName === 'A' ? first.textContent : null,
                    label_markup: first && first.tagName === 'A' ? markup(first.childNodes) : null};
        }) : [];
        const regions = [...document.querySelectorAll('.on-this-page')];
        const navigation = [];
        for (const region of regions) {
            for (const a of region.querySelectorAll('a.header-in-summary')) {
                let depth = -1;
                for (let parent = a.parentElement; parent && parent !== region; parent = parent.parentElement) {
                    if (parent.tagName === 'OL') { depth++; }
                }
                navigation.push({href: a.getAttribute('href'), depth: depth,
                                 text: a.textContent, markup: markup(a.childNodes), attrs: attrs(a)});
            }
        }
        const active = [...document.querySelectorAll('#mdbook-sidebar a.active')]
            .map(a => a.getAttribute('href'));
        const bindings = regions.map(region => {
            const previous = region.previousElementSibling;
            return {parent_tag: region.parentElement.tagName.toLowerCase(),
                    parent_class: region.parentElement.getAttribute('class') || '',
                    previous_active: previous ? [...previous.querySelectorAll('a.active')]
                        .map(a => a.getAttribute('href')) : []};
        });
        const out = document.createElement('script');
        out.id = 'semulith-heading-observation';
        out.type = 'application/json';
        out.textContent = JSON.stringify({ready: true, errors: errors, headers: headers,
                                         navigation: navigation, regions: regions.length,
                                         active: active, bindings: bindings, title: document.title})
            .replace(/</g, '\\u003c');
        document.body.appendChild(out);
    });
})();
</script>'''


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


@dataclass(eq=False)
class Node:
    tag: str
    attrs: list = field(default_factory=list)
    children: list = field(default_factory=list)
    parent: Node | None = field(default=None, repr=False)

    def attribute(self, name):
        return dict(self.attrs).get(name)

    def has_class(self, name):
        return name in (self.attribute('class') or '').split()


def elements(node):
    for child in node.children:
        if isinstance(child, Node):
            yield child
            yield from elements(child)


def text_content(nodes):
    return ''.join(value if isinstance(value, str) else text_content(value.children)
                   if isinstance(value, Node) else '' for value in nodes)


def markup(nodes, *, remove_marks=False):
    result = []
    def append(value):
        if isinstance(value, str) and result and isinstance(result[-1], str):
            result[-1] += value
        else:
            result.append(value)
    for value in nodes:
        if isinstance(value, Node):
            children = markup(value.children, remove_marks=remove_marks)
            if remove_marks and value.tag == 'mark':
                for child in children:
                    append(child)
            else:
                append({'tag': value.tag, 'attrs': sorted(value.attrs), 'children': children})
        else:
            append(value)
    return result


class Document(HTMLParser):
    """Independent source/serialized-DOM reader, with complete label trees."""
    def __init__(self, body):
        require(len(body) <= MAX_HTML, 'HTML input exceeds bound')
        super().__init__(convert_charrefs=True)
        self.root = Node('#document')
        self.stack = [self.root]
        self.feed(body.decode('utf-8'))
        self.close()

    def handle_starttag(self, tag, attrs):
        require(len({k for k, v in attrs}) == len(attrs), 'duplicate HTML attribute')
        node = Node(tag, [[k, '' if v is None else v] for k, v in attrs], parent=self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)

    def handle_comment(self, data):
        self.stack[-1].children.append({'comment': data})

    def headers(self):
        all_nodes = list(elements(self.root))
        mains = [node for node in all_nodes if node.tag == 'main']
        require(len(mains) <= 1, 'ambiguous main content')
        counts = Counter(node.attribute('id') for node in all_nodes if node.attribute('id'))
        rows = []
        if not mains:
            return rows
        for node in elements(mains[0]):
            if node.tag not in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
                continue
            first = next((child for child in node.children if isinstance(child, Node)), None)
            anchor = first if first is not None and first.tag == 'a' else None
            rows.append({'level': int(node.tag[1]), 'id': node.attribute('id') or '',
                         'attrs': sorted(node.attrs), 'text': text_content(node.children),
                         'id_count': counts[node.attribute('id')] if node.attribute('id') else 0,
                         'first_tag': first.tag if first is not None else None,
                         'anchor_attrs': sorted(anchor.attrs) if anchor else None,
                         'label_text': text_content(anchor.children) if anchor else None,
                         'label_markup': markup(anchor.children) if anchor else None})
        return rows

    def navigation(self):
        all_nodes = list(elements(self.root))
        regions = [node for node in all_nodes if node.has_class('on-this-page')]
        rows = []
        for region in regions:
            for node in elements(region):
                if node.tag != 'a' or not node.has_class('header-in-summary'):
                    continue
                depth, parent = -1, node.parent
                while parent is not None and parent is not region:
                    if parent.tag == 'ol':
                        depth += 1
                    parent = parent.parent
                require(parent is region, 'heading link escaped its region')
                rows.append({'href': node.attribute('href'), 'depth': depth,
                             'text': text_content(node.children), 'markup': markup(node.children),
                             'attrs': sorted(node.attrs)})
        return len(regions), rows

    def bindings(self):
        rows = []
        for region in elements(self.root):
            if not region.has_class('on-this-page'):
                continue
            require(region.parent is not None, 'detached heading region')
            previous = None
            for sibling in region.parent.children:
                if sibling is region:
                    break
                if isinstance(sibling, Node):
                    previous = sibling
            active = [n.attribute('href') for n in elements(previous)
                      if n.tag == 'a' and n.has_class('active')] if previous else []
            rows.append({'parent_tag': region.parent.tag,
                         'parent_class': region.parent.attribute('class') or '',
                         'previous_active': active})
        return rows

    def title(self):
        titles = [node for node in elements(self.root) if node.tag == 'title']
        require(len(titles) <= 1, 'ambiguous page title')
        return text_content(titles[0].children) if titles else ''

    def witness(self):
        found = [node for node in elements(self.root) if node.attribute('id') == WITNESS]
        require(len(found) == 1 and found[0].tag == 'script'
                and found[0].attribute('type') == 'application/json', 'browser witness unavailable')
        value = json.loads(text_content(found[0].children))
        require(isinstance(value, dict) and set(value) ==
                {'ready', 'errors', 'headers', 'navigation', 'regions', 'active', 'bindings', 'title'}
                and value['ready'] is True and value['errors'] == [],
                'browser witness reports an incomplete or failed script run')
        require(value['headers'] == self.headers(), 'independent browser heading readers differ')
        regions, rows = self.navigation()
        require(value['regions'] == regions and value['navigation'] == rows,
                'independent browser navigation readers differ')
        require(value['bindings'] == self.bindings() and value['title'] == self.title(),
                'independent browser context readers differ')
        return value


def remove_marks(nodes):
    """Independent projection of recorded runtime heading markup, not producer code."""
    result = []
    def append(value):
        if isinstance(value, str) and result and isinstance(result[-1], str):
            result[-1] += value
        else:
            result.append(value)
    for node in nodes:
        if isinstance(node, dict) and 'tag' in node:
            children = remove_marks(node['children'])
            if node['tag'] == 'mark':
                for child in children:
                    append(child)
            else:
                append({**node, 'children': children})
        else:
            append(node)
    return result


def diagnostics(body):
    require(len(body) <= 65536, 'browser diagnostics exceed bound')
    counts = {'allocator_guard': 0, 'virtual_display': 0, 'process_priority': 0}
    for line in body.decode('utf-8').splitlines():
        if line == ALLOCATOR:
            counts['allocator_guard'] += 1
        elif DISPLAY.fullmatch(line):
            counts['virtual_display'] += 1
        elif PRIORITY.fullmatch(line):
            counts['process_priority'] += 1
        elif line:
            raise ValueError('unreviewed browser diagnostic: ' + line)
    return counts


def browser_flags(root):
    return ['--headless', '--dump-dom', '--disable-gpu', '--disable-software-rasterizer',
            '--disable-background-networking',
            '--disable-renderer-backgrounding', '--disable-backgrounding-occluded-windows',
            '--disable-background-timer-throttling',
            '--disable-component-update', '--disable-sync', '--disable-extensions',
            '--disable-default-apps', '--disable-breakpad', '--disable-crash-reporter',
            '--no-first-run', '--no-default-browser-check', '--password-store=basic',
            '--use-mock-keychain', '--no-proxy-server',
            '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE localhost, EXCLUDE 127.0.0.1',
            '--window-size=1024,768', '--timeout=10000', '--virtual-time-budget=1000',
            '--user-data-dir=' + str(root / 'profile'), '--disk-cache-dir=' + str(root / 'cache'),
            '--crash-dumps-dir=' + str(root / 'crash')]


def browser_run(program, root, url, *, kind='webkit'):
    relative = root.relative_to(ROOT).as_posix()
    C.Q.relative_path(relative)
    require(relative.startswith('target/') and C.U.source_path(ROOT, relative) == root
            and not root.exists(), 'fresh owned browser output required')
    root.mkdir(parents=True)
    for name in ['tmp', 'cache', 'crash']:
        (root / name).mkdir()
    require(kind in {'webkit', 'chrome'}, 'unsupported browser adapter')
    flags = browser_flags(root) if kind == 'chrome' else []
    process = subprocess.Popen([str(program), *flags, url], cwd=ROOT,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               env=dict(os.environ, TMPDIR=str(root / 'tmp'),
                                        SEMULITH_PROBE_ROOT=str(ROOT)),
                               start_new_session=True)
    try:
        try:
            stdout, stderr = process.communicate(timeout=40)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            stdout, stderr = process.communicate(timeout=10)
            (root / 'dom.html').write_bytes(stdout)
            (root / 'stderr.log').write_bytes(stderr)
            raise
    finally:
        with contextlib.suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGTERM)
    (root / 'dom.html').write_bytes(stdout)
    (root / 'stderr.log').write_bytes(stderr)
    require(process.returncode == 0, 'public browser refused')
    require(0 < len(stdout) <= MAX_HTML, 'browser DOM exceeds bound or is empty')
    if kind == 'webkit':
        require(not stderr, 'WebKit adapter emitted diagnostics')
    record = {'returncode': process.returncode, 'dom_bytes': len(stdout),
              'dom_sha256': C.digest(stdout), 'stderr_bytes': len(stderr),
              'stderr_sha256': C.digest(stderr), 'diagnostics': diagnostics(stderr), 'engine': kind}
    return stdout, record


def external_identity(path):
    """Fingerprint a supplied read-only OS tool without persisting its absolute path."""
    before = path.stat()
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for body in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(body)
    after = path.stat()
    require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
            'external browser identity changed during read')
    return {'name': path.name, 'bytes': after.st_size, 'sha256': value.hexdigest()}


def browser_identity(program, *, kind='webkit'):
    result = subprocess.run([str(program), '--version'], capture_output=True, timeout=30)
    require(result.returncode == 0 and not result.stderr, 'browser identity unavailable')
    if kind == 'webkit':
        value = json.loads(result.stdout)
        require(set(value) == {'engine', 'version', 'os', 'website_data'}
                and value['engine'] == 'WebKit' and value['website_data'] == 'nonpersistent'
                and value['version'] != 'unavailable', 'unreviewed WebKit identity')
        return {**value, 'adapter': external_identity(program),
                'access': 'owned adapter; required external OS WebKit read-only'}
    require(
            re.fullmatch(rb'(Google Chrome|Chromium) [0-9]+(?:\.[0-9]+){3}\s*', result.stdout),
            'unsupported or unavailable public browser')
    identities = [external_identity(program)]
    framework = program.parents[1] / ('Frameworks/Google Chrome Framework.framework/'
                                      'Versions/Current/Google Chrome Framework')
    if framework.is_file():
        identities.append(external_identity(framework))
    return {'version': result.stdout.decode().strip(), 'files': identities,
            'access': 'required external OS toolchain; read-only'}


def compile_webkit(output):
    directory = output / 'runtime-adapter'
    directory.mkdir()
    (directory / 'module-cache').mkdir()
    (directory / 'tmp').mkdir()
    program = directory / 'heading-probe'
    source = ROOT / 'scripts/book_headings_webkit.swift'
    before = C.file_identity(source.relative_to(ROOT).as_posix())
    compiler = shutil.which('swiftc')
    require(compiler is not None, 'public Swift compiler unavailable')
    command = [compiler, '-swift-version', '6', '-warnings-as-errors', '-parse-as-library',
               '-module-cache-path', str(directory / 'module-cache'),
               '-Xcc', '-fmodules-cache-path=' + str(directory / 'module-cache'),
               str(source), '-o', str(program)]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=180,
                            env=dict(os.environ, TMPDIR=str(directory / 'tmp')))
    (directory / 'compile.stdout').write_bytes(result.stdout)
    (directory / 'compile.stderr').write_bytes(result.stderr)
    require(result.returncode == 0 and not result.stdout and not result.stderr,
            'owned WebKit adapter did not compile cleanly')
    require(C.file_identity(source.relative_to(ROOT).as_posix()) == before,
            'WebKit adapter source changed during compilation')
    version = subprocess.run([compiler, '--version'], capture_output=True, timeout=30)
    (directory / 'compiler-version.stdout').write_bytes(version.stdout)
    (directory / 'compiler-version.stderr').write_bytes(version.stderr)
    require(version.returncode == 0 and
            re.fullmatch(rb'Apple Swift version [0-9][^\n]*\nTarget: [A-Za-z0-9_.-]+\n', version.stdout)
            and (not version.stderr or re.fullmatch(rb'swift-driver version: [0-9.]+\s*', version.stderr)),
            'Swift compiler version unavailable or malformed')
    return program, {'compiler': version.stdout.decode().strip(),
                     'driver': version.stderr.decode().strip(), 'source': before,
                     'compile_returncode': 0, 'diagnostics_bytes': 0}


def calibrate(program, output):
    """Prove script execution and an exit0 false-positive control before book use."""
    directory = output / 'calibration'
    directory.mkdir()
    pages = directory / 'pages'
    pages.mkdir()
    cases = []
    for name, body, expected in [
        ('positive', '<p id="witness">before</p><script>setTimeout(() => '
         '{document.getElementById("witness").textContent="executed";}, 50);</script>', True),
        ('script-omitted', '<p id="witness">before</p>', False),
        ('blank', '', False),
    ]:
        page = pages / (name + '.html')
        page.write_text('<!doctype html><html><head></head><body>' + body + '</body></html>')
        dom, record = browser_run(program, directory / name, page.as_uri())
        observed = b'>executed</p>' in dom
        require(observed == expected, 'browser script calibration did not discriminate')
        cases.append({'case': name, 'script_expected': expected, 'script_executed': observed,
                      'witness_verdict': 0 if observed else 1, **record})
    with serve(pages, set()) as (base, requests):
        dom, record = browser_run(program, directory / 'http-loopback', base + '/positive.html')
        require(b'>executed</p>' in dom and any(r['path'] == 'positive.html' for r in requests),
                'loopback browser script calibration did not execute')
        cases.append({'case': 'http-loopback', 'script_expected': True,
                      'script_executed': True, 'witness_verdict': 0, **record})
    return cases


@contextlib.contextmanager
def serve(site, html_paths):
    """Serve only this generated bundle; add an observer without changing its bytes."""
    allowed = B.file_set(site)
    requests, lock = [], threading.Lock()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            logical = unquote(urlsplit(self.path).path).lstrip('/')
            if logical not in allowed:
                self.send_error(404)
                return
            body = (site / logical).read_bytes()
            require(C.digest(body) == allowed[logical], 'served bundle input changed')
            if logical in html_paths:
                require(body.count(b'<head>') == 1 and WITNESS.encode() not in body,
                        'unsupported browser observer insertion')
                body = body.replace(b'<head>', b'<head>' + OBSERVER.encode(), 1)
            with lock:
                requests.append({'path': logical, 'bytes': len(body), 'sha256': C.digest(body)})
            self.send_response(200)
            self.send_header('Content-Type', self.content_type(logical))
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)

        @staticmethod
        def content_type(name):
            suffix = Path(name).suffix
            return {'.html': 'text/html; charset=utf-8', '.js': 'text/javascript',
                    '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2',
                    '.png': 'image/png'}.get(suffix, 'application/octet-stream')

        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    worker = threading.Thread(target=server.serve_forever, kwargs={'poll_interval': 0.1}, daemon=True)
    worker.start()
    try:
        yield 'http://127.0.0.1:' + str(server.server_port), requests
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=10)
        require(not worker.is_alive(), 'owned bundle server did not terminate')
        require(B.file_set(site) == allowed, 'browser serving changed generated inputs')


def source_inputs():
    """No-fetch belongs to the API boundary, including direct callers."""
    os.environ['GIT_NO_LAZY_FETCH'] = '1'
    source = C.source_census(SOURCE)
    require(len(source['members']) == SOURCE_MEMBERS, 'complete heading source population differs')
    members = {row['path']: row for row in source['members']}
    for name in ['scripts/collect_containment_graph.py', 'scripts/qualify_book_includes.py',
                 'scripts/qualify_book_navigation.py', 'scripts/qualify_book_toc.py',
                 'scripts/unit_books.py', 'scripts/book_navigation.py', 'scripts/book_includes.py']:
        row = members[name]
        require(C.file_identity(name) == {'bytes': row['bytes'], 'sha256': row['sha256'],
                                        'mode': int(row['mode'][-3:], 8)},
                'unreviewed source helper identity: ' + name)
    return source, members


def prepare(source, members, output):
    fixture, _ = B.copy_source(source, output)
    (output / 'tmp').mkdir()
    units = C.U.registered_units(fixture)
    require(not C.U.catalogue_findings(fixture, units), 'source unit catalogue differs')
    books = ['docs/book', *[unit['book'].rstrip('/') for unit in units]]
    require(len(books) == len(set(books)) == 7, 'complete seven-book population differs')
    stage = N.build_stage(fixture, output, books, 'baseline')
    site = output / 'baseline/site'
    cases, pins = [], set()
    for book in books:
        summary = book + '/src/SUMMARY.md'
        rows = T.summary_rows((fixture / summary).read_bytes(), book, members)
        chapters = [row for row in rows if row['kind'] == 'chapter']
        title = tomllib.loads((fixture / book / 'book.toml').read_text())['book']['title']
        expected = {book + '/book/' + row['path'][:-3] + '.html':
                    {'role': 'chapter', 'chapter_path': row['path'],
                     'expected_title': row['name'] + ' - ' + title} for row in chapters}
        alias = book + '/book/index.html'
        if alias not in expected:
            expected[alias] = {'role': 'index-alias', 'chapter_path': chapters[0]['path'],
                               'expected_title': chapters[0]['name'] + ' - ' + title}
        for name in ['print', 'toc', '404']:
            expected[book + '/book/' + name + '.html'] = {'role': name, 'chapter_path': None,
                                                        'expected_title': None}
        actual = {name for name in stage['files'] if name.startswith(book + '/book/') and name.endswith('.html')}
        require(actual == set(expected), 'complete page-role census differs: ' + book)
        pins.update([summary, book + '/book.toml'])
        pins.update(book + '/src/' + row['path'] for row in chapters)
        for name in sorted(expected):
            body = (site / name).read_bytes()
            document = Document(body)
            cases.append({'path': name, 'book': book, **expected[name],
                          'source_bytes': len(body), 'source_sha256': C.digest(body),
                          'source_headers': document.headers(), 'source_title': document.title()})
    require(sum(case['role'] == 'chapter' for case in cases) == 93
            and len(cases) == 120 and len(stage['files']) == 344, 'complete rendered population differs')
    B.verify_copy(source, fixture)
    cases.sort(key=lambda case: case['path'])
    return fixture, site, stage, cases, [members[name] for name in sorted(pins)]


def expected_navigation(headers, active):
    rows = []
    if active:
        for header in headers:
            if header['level'] >= 2 and header['id'] and header['first_tag'] == 'a':
                rows.append({'href': '#' + header['id'], 'depth': header['level'] - 2,
                             'text': header['label_text'], 'markup': remove_marks(header['label_markup'])})
    return rows


def assess(case, dom):
    document = Document(dom)
    observed = document.witness()
    # Highlighting may add inline markup. Preserve both trees, and independently
    # require source identity/whole text/first-anchor text before projecting DOM.
    fields = ['level', 'id', 'text', 'first_tag', 'label_text']
    projected = lambda rows: [{key: row[key] for key in fields} for row in rows]
    source_exact = projected(case['source_headers']) == projected(observed['headers'])
    active = case['role'] in {'chapter', 'index-alias'}
    expected = expected_navigation(observed['headers'], active)
    actual = [{key: row[key] for key in ['href', 'depth', 'text', 'markup']}
              for row in observed['navigation']]
    unique = all(header['id_count'] == 1 for header in observed['headers']
                 if active and header['level'] >= 2 and header['id'] and header['first_tag'] == 'a')
    context = len(observed['active']) == (1 if active else 0)
    if active and context:
        url = urlsplit(observed['active'][0])
        target = posixpath.normpath(posixpath.join(posixpath.dirname(case['path']), unquote(url.path)))
        wanted = case['book'] + '/book/' + case['chapter_path'][:-3] + '.html'
        context = not url.scheme and not url.netloc and target == wanted
    regions = observed['regions'] == (1 if expected else 0)
    bindings = all(row['parent_tag'] == 'li' and 'chapter-item' in row['parent_class'].split()
                   and row['previous_active'] == observed['active'] for row in observed['bindings'])
    title = (observed['title'] == case['source_title'] and
             (case['expected_title'] is None or observed['title'] == case['expected_title']))
    checks = {'source_headers': source_exact, 'whole_navigation': actual == expected,
              'unique_targets': unique, 'active_context': context, 'region_count': regions,
              'parent_binding': bindings, 'chapter_title': title}
    return {**case, 'browser': observed, 'expected_navigation': expected,
            'checks': checks, 'expected_contract': all(checks.values())}


def run_cases(program, site, cases, output, *, jobs):
    paths = {case['path'] for case in cases}
    with serve(site, paths) as (base, requests):
        def execute(item):
            index, case = item
            dom, record = browser_run(program, output / f'page-{index:03d}',
                                      base + '/' + quote(case['path'], safe='/'))
            return {'observation': assess(case, dom), 'process': record}
        with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
            observations = list(pool.map(execute, enumerate(cases)))
    return observations, requests


def actual_omissions(program, site, cases, output):
    """Execute three copied public producer omissions and a D78 cause control."""
    target = next(case for case in cases if case['path'] == 'docs/book/book/working/task-trees.html')
    script_paths = list((site / 'docs/book/book').glob('toc-*.js'))
    require(len(script_paths) == 1, 'ambiguous generated heading producer')
    path = script_paths[0].relative_to(site)
    original = script_paths[0].read_bytes()
    changes = [
        ('insertion', b"document.addEventListener('DOMContentLoaded', function() {\n"
         b"        const activeSection =", b"document.addEventListener('DOMContentLoaded', function() {\n"
         b"        return;\n        const activeSection ="),
        ('h2-membership', b"main.querySelectorAll('h2, h3, h4, h5, h6')",
         b"main.querySelectorAll('h3, h4, h5, h6')"),
        ('label-copy', b'filterHeader(header.children[0], a);', b'; // owned label-copy omission'),
    ]
    result = []
    for name, old, new in changes:
        directory = output / ('omit-' + name)
        copied = directory / 'site'
        shutil.copytree(site, copied)
        require(original.count(old) == 1, 'unique actual heading omission site')
        changed = original.replace(old, new, 1)
        (copied / path).write_bytes(changed)
        rows, requests = run_cases(program, copied, [target], directory / 'browser', jobs=1)
        row = rows[0]
        require(row['process']['returncode'] == 0 and not row['observation']['expected_contract'],
                'actual heading omission did not discriminate')
        result.append({'role': name, 'producer_path': path.as_posix(),
                       'original_sha256': C.digest(original), 'omitted_sha256': C.digest(changed),
                       'old': old.decode(), 'new': new.decode(), 'qualification_returncode': 1,
                       'observations': rows, 'requests': requests, 'files': B.file_set(copied)})
    # Removing the fallback diagnoses D78 but also breaks a real index alias.
    directory = output / 'cause-index-fallback'
    copied = directory / 'site'
    shutil.copytree(site, copied)
    old = (b"\n                || i === 0\n                && path_to_root === ''\n"
           b"                && current_page.endsWith('/index.html')")
    require(original.count(old) == 1, 'unique authored-index cause site')
    changed = original.replace(old, b'', 1)
    (copied / path).write_bytes(changed)
    selected = [next(case for case in cases if case['path'] == 'docs/book/book/index.html'),
                next(case for case in cases if case['role'] == 'index-alias')]
    rows, requests = run_cases(program, copied, selected, directory / 'browser', jobs=1)
    # The model-book alias uses its own separate script: apply the same real omission there.
    # Re-run it after changing that book's producer as well, with an independent fresh output.
    alias = selected[1]
    alias_scripts = list((copied / alias['book'] / 'book').glob('toc-*.js'))
    require(len(alias_scripts) == 1, 'ambiguous alias heading producer')
    alias_original = alias_scripts[0].read_bytes()
    require(alias_original.count(old) == 1, 'unique alias cause site')
    alias_scripts[0].write_bytes(alias_original.replace(old, b'', 1))
    alias_rows, alias_requests = run_cases(program, copied, [alias], directory / 'alias-browser', jobs=1)
    require(rows[0]['observation']['expected_contract'] and
            not alias_rows[0]['observation']['expected_contract'], 'D78 cause control did not discriminate')
    result.append({'role': 'index-fallback-cause', 'original_sha256': C.digest(original),
                   'omitted_sha256': C.digest(changed), 'old': old.decode(), 'new': '',
                   'observations': [rows[0], alias_rows[0]], 'alias_before_omission': rows[1],
                   'requests': requests + alias_requests, 'files': B.file_set(copied)})
    return result


def qualify(output, additions, jobs):
    require(not output.exists(), 'fresh qualification output required')
    before = C.working_snapshot(additions)
    source, members = source_inputs()
    output.mkdir(parents=True)
    program, compiler = compile_webkit(output)
    engine = browser_identity(program)
    calibration = calibrate(program, output)
    fixture, site, stage, cases, pins = prepare(source, members, output)
    rows, requests = run_cases(program, site, cases, output / 'browser', jobs=jobs)
    omissions = actual_omissions(program, site, cases, output)
    require(browser_identity(program) == engine, 'browser identity changed during qualification')
    require(B.file_set(site) == stage['files'], 'complete original bundle changed during qualification')
    B.verify_copy(source, fixture)
    after = C.working_snapshot(additions)
    require(before == after, 'actual source/index/modes changed during heading qualification')
    N.write_json(output / 'working-before.json', before)
    N.write_json(output / 'working-after.json', after)
    bad = [row['observation']['path'] for row in rows if not row['observation']['expected_contract']]
    return {'source': SOURCE, 'source_members': SOURCE_MEMBERS,
            'source_tree_sha256': source['tree_sha256'],
            'mode': 'optimized' if sys.flags.optimize else 'normal',
            'engine': engine, 'compiler': compiler, 'calibration': calibration,
            'inputs': pins, 'stage': stage, 'observations': rows, 'requests': requests,
            'actual_omissions': omissions, 'source_defects': len(bad), 'wrong_contract_paths': bad,
            'scope': 'all120 page roles/headers; DOM execution and navigation clone/context; '
                     'visual/scroll, search and resource completeness unclaimed'}


def fingerprint(value):
    body = canonical(value)
    return {'canonical_bytes': len(body), 'canonical_sha256': C.digest(body)}


def packed_result(raw):
    """Retain every header/nav/input/manifest row; HTTP streams are diagnostics."""
    value = json.loads(canonical(raw))
    def requests(rows):
        counts = Counter(row['path'] for row in rows)
        return {'count': len(rows), **fingerprint(rows),
                'footprint': [{'path': name, 'reads': counts[name]} for name in sorted(counts)]}
    value['requests'] = requests(value['requests'])
    for omission in value['actual_omissions']:
        omission['requests'] = requests(omission['requests'])
        files = omission['files']
        omission['files'] = {'count': len(files), **fingerprint(files)}
    return value


def apply_changes(value, changes):
    result = json.loads(canonical(value))
    for path, replacement in changes:
        if not path:
            result = replacement
            continue
        cursor = result
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = replacement
    return result


def validate_capture(value):
    require(isinstance(value, dict) and set(value) == {'normal', 'optimized_overrides', 'book_seams'},
            'unreviewed heading capture fields')
    source, members = source_inputs()
    summaries = sorted(name for name in members if name.startswith('docs/') and
                       name.endswith('/src/SUMMARY.md'))
    require(len(summaries) == 7, 'complete source SUMMARY population differs')
    expected_paths, expected_pins = set(), set()
    for summary in summaries:
        book = summary.removesuffix('/src/SUMMARY.md')
        body = C.Q.git('show', SOURCE + ':' + summary)
        rows = T.summary_rows(body, book, members)
        chapters = [row for row in rows if row['kind'] == 'chapter']
        expected_paths.update(book + '/book/' + row['path'][:-3] + '.html' for row in chapters)
        expected_paths.update(book + '/book/' + name + '.html' for name in ['index', 'print', 'toc', '404'])
        expected_pins.update([summary, book + '/book.toml'])
        expected_pins.update(book + '/src/' + row['path'] for row in chapters)
    optimized = apply_changes(value['normal'], value['optimized_overrides'])
    for mode, result in [('normal', value['normal']), ('optimized', optimized)]:
        require(result['source'] == SOURCE and type(result['source_members']) is int
                and result['source_members'] == SOURCE_MEMBERS and result['mode'] == mode
                and result['source_tree_sha256'] == source['tree_sha256'],
                'heading capture source identity differs')
        require(result['inputs'] == [members[name] for name in sorted(expected_pins)],
                'complete heading source pins differ')
        rows = result['observations']
        paths = [row['observation']['path'] for row in rows]
        require(paths == sorted(expected_paths) and len(paths) == 120,
                'complete heading page membership/order differs')
        bad = [row['observation']['path'] for row in rows if not row['observation']['expected_contract']]
        require(type(result['source_defects']) is int and result['source_defects'] == len(bad)
                and result['wrong_contract_paths'] == bad,
                'heading verdict ledger differs')
        require(len(result['stage']['files']) == 344 and len(result['stage']['builds']) == 7
                and len(result['actual_omissions']) == 4 and len(result['calibration']) == 4,
                'complete heading capture boundary differs')
    require(isinstance(value['book_seams'], dict), 'invalid retained book source seams')
    return value, optimized


def encode_capture(normal, optimized, book_seams):
    n, o = packed_result(normal), packed_result(optimized)
    value = {'normal': n, 'optimized_overrides': list(T.metadata_changes(n, o)),
             'book_seams': book_seams}
    validate_capture(value)
    compact = json.loads(canonical(value))
    source, _ = source_inputs()
    positions = {row['path']: index for index, row in enumerate(source['members'])}
    inputs = compact['normal']['inputs']
    indices = [positions[row['path']] for row in inputs]
    require([source['members'][index] for index in indices] == inputs, 'source-row reference differs')
    compact['normal']['inputs'] = {'$source_rows': {'indices': indices, **fingerprint(inputs)}}
    base = manifest_base()
    files = compact['normal']['stage']['files']
    compact['normal']['stage']['files'] = {'$manifest_delta': {
        'remove': sorted(set(base) - set(files)),
        'set': {name: digest for name, digest in files.items() if base.get(name) != digest},
        'base': fingerprint(base), 'count': len(files), **fingerprint(files)}}
    for row in compact['normal']['observations']:
        observation = row['observation']
        require(observation['source_sha256'] == files[observation['path']], 'page/manifest identity differs')
        require(observation['expected_navigation'] == expected_navigation(
            observation['browser']['headers'], observation['role'] in {'chapter', 'index-alias'}),
            'complete heading oracle reconstruction differs')
        del observation['source_sha256']
        del observation['expected_navigation']
    body = canonical(compact)
    require(0 < len(body) <= 8 * 1024 * 1024, 'heading metadata exceeds bound')
    blob = lzma.compress(body, format=lzma.FORMAT_XZ,
                         filters=[{'id': lzma.FILTER_LZMA2, 'preset': 6,
                                   'dict_size': 8 * 1024 * 1024}])
    return {'encoding': 'xz6/base64 canonical UTF-8 JSON', 'schema_version': 1,
            'metadata_bytes': len(body), 'metadata_sha256': C.digest(body),
            'compressed_bytes': len(blob), 'compressed_sha256': C.digest(blob),
            'metadata_xz_base64': base64.b64encode(blob).decode(),
            'producer': C.file_identity('scripts/qualify_book_headings.py'),
            'native_producer': C.file_identity('scripts/book_headings_webkit.swift')}


def manifest_base():
    """Reuse the retained LC0040 catalogue, read from this capture's immutable source."""
    os.environ['GIT_NO_LAZY_FETCH'] = '1'
    body = C.Q.git('show', SOURCE + ':docs/tasks/artifacts/live-containment/include-source-integration.md')
    phase = body.decode().split('## Chapter contents assessment — LC0040\n', 1)[1]
    match = re.search(r'^```json\n(.*?)\n```$', phase, re.M | re.S)
    require(match is not None, 'retained manifest frame unavailable')
    value = T.decode_capture(H.json_object(match[1].encode()))
    # LC0040's decoder restores its packed view; its file catalogue is a delta,
    # not an already-expanded mapping. Authenticate the predecessor, then apply it.
    _, predecessor = T.source_manifest()
    delta = value['normal']['stages']['baseline']['files']['$manifest_delta']
    files = dict(predecessor)
    require(all(name in files for name in delta['remove']), 'retained predecessor member unavailable')
    for name in delta['remove']:
        del files[name]
    files.update(delta['set'])
    require(len(files) == delta['count'] == 344 and fingerprint(files) ==
            {key: delta[key] for key in ['canonical_bytes', 'canonical_sha256']},
            'complete retained predecessor manifest differs')
    return files


def expand_capture(value):
    source, _ = source_inputs()
    reference = value['normal']['inputs']['$source_rows']
    indices = reference['indices']
    require(isinstance(indices, list) and all(type(index) is int and
            0 <= index < len(source['members']) for index in indices)
            and len(indices) == len(set(indices)), 'invalid source-row indices')
    inputs = [source['members'][index] for index in indices]
    require(fingerprint(inputs) == {k: reference[k] for k in ['canonical_bytes', 'canonical_sha256']},
            'restored source-row identity differs')
    value['normal']['inputs'] = inputs
    delta = value['normal']['stage']['files']['$manifest_delta']
    base = manifest_base()
    require(delta['base'] == fingerprint(base), 'retained manifest base differs')
    files = dict(base)
    require(isinstance(delta['remove'], list) and len(delta['remove']) == len(set(delta['remove']))
            and all(name in files for name in delta['remove']), 'invalid manifest removals')
    for name in delta['remove']:
        del files[name]
    require(isinstance(delta['set'], dict), 'invalid manifest replacements')
    files.update(delta['set'])
    require(len(files) == delta['count'] and fingerprint(files) ==
            {k: delta[k] for k in ['canonical_bytes', 'canonical_sha256']},
            'restored complete manifest differs')
    value['normal']['stage']['files'] = files
    for row in value['normal']['observations']:
        observation = row['observation']
        require('source_sha256' not in observation and 'expected_navigation' not in observation,
                'ambiguous reconstructed heading fields')
        observation['source_sha256'] = files[observation['path']]
        observation['expected_navigation'] = expected_navigation(
            observation['browser']['headers'], observation['role'] in {'chapter', 'index-alias'})
    return value


def decode_capture(frame):
    try:
        require(isinstance(frame, dict) and set(frame) ==
                {'encoding', 'schema_version', 'metadata_bytes', 'metadata_sha256',
                 'compressed_bytes', 'compressed_sha256', 'metadata_xz_base64',
                 'producer', 'native_producer'}, 'unreviewed heading frame fields')
        require(type(frame['schema_version']) is int and frame['schema_version'] == 1
                and frame['encoding'] == 'xz6/base64 canonical UTF-8 JSON', 'unsupported heading encoding')
        require(frame['producer'] == C.file_identity('scripts/qualify_book_headings.py')
                and frame['native_producer'] == C.file_identity('scripts/book_headings_webkit.swift'),
                'heading producer identity differs')
        require(type(frame['metadata_bytes']) is int and 0 < frame['metadata_bytes'] <= 8 * 1024 * 1024
                and type(frame['compressed_bytes']) is int and 0 < frame['compressed_bytes'] <= 1024 * 1024
                and H.identity(frame['metadata_sha256'], 64) and H.identity(frame['compressed_sha256'], 64),
                'heading metadata identity/bound differs')
        require(isinstance(frame['metadata_xz_base64'], str)
                and len(frame['metadata_xz_base64']) <= 2 * frame['compressed_bytes'],
                'heading encoded input exceeds bound')
        blob = base64.b64decode(frame['metadata_xz_base64'], validate=True)
        require(len(blob) == frame['compressed_bytes'] and C.digest(blob) == frame['compressed_sha256'],
                'heading compressed identity differs')
        decoder = lzma.LZMADecompressor(format=lzma.FORMAT_XZ, memlimit=64 * 1024 * 1024)
        body = decoder.decompress(blob, max_length=frame['metadata_bytes'] + 1)
        require(decoder.eof and not decoder.unused_data and len(body) == frame['metadata_bytes']
                and C.digest(body) == frame['metadata_sha256'], 'heading expansion identity/bound differs')
        return validate_capture(expand_capture(H.json_object(body)))[0]
    except (KeyError, TypeError, IndexError, UnicodeError, RecursionError, lzma.LZMAError) as exc:
        raise ValueError('heading capture refused') from exc


def record_frame(path):
    C.Q.relative_path(path)
    source = C.U.source_path(ROOT, path)
    require(source.is_file() and source.stat().st_size <= 131072, 'bounded heading record required')
    text = source.read_text()
    marker = '## Heading navigation assessment — LC0042\n'
    require(text.count(marker) == 1, 'unique heading capture phase required')
    match = re.search(r'^```json\n(.*?)\n```$', text.split(marker, 1)[1], re.M | re.S)
    require(match is not None, 'heading capture frame unavailable')
    return H.json_object(match[1].encode())


def codec_controls(frame):
    """Damage outer and authenticated inner legs; actual decoder must refuse each."""
    original = decode_capture(frame)
    blob = base64.b64decode(frame['metadata_xz_base64'])
    compact = H.json_object(lzma.decompress(blob))
    controls = []
    for name in ['compressed-sha', 'bool-bound', 'trailing-xz', 'source-tree',
                 'missing-page', 'duplicate-source-index', 'producer', 'string-count', 'bool-ledger']:
        changed = json.loads(canonical(frame))
        value = json.loads(canonical(compact))
        inner = False
        if name == 'compressed-sha':
            changed['compressed_sha256'] = '0' * 64
        elif name == 'bool-bound':
            changed['metadata_bytes'] = True
        elif name == 'producer':
            changed['producer']['sha256'] = '0' * 64
        elif name == 'trailing-xz':
            extra = blob + b'trailing'
            changed.update(compressed_bytes=len(extra), compressed_sha256=C.digest(extra),
                           metadata_xz_base64=base64.b64encode(extra).decode())
        elif name == 'source-tree':
            value['normal']['source_tree_sha256'] = '0' * 64
            inner = True
        elif name == 'missing-page':
            value['normal']['observations'].pop()
            inner = True
        elif name == 'duplicate-source-index':
            indices = value['normal']['inputs']['$source_rows']['indices']
            indices[0] = indices[1]
            inner = True
        elif name == 'string-count':
            value['normal']['source_members'] = str(SOURCE_MEMBERS)
            inner = True
        elif name == 'bool-ledger':
            value['normal']['source_defects'] = True
            inner = True
        if inner:
            body = canonical(value)
            encoded = lzma.compress(body, format=lzma.FORMAT_XZ,
                                   filters=[{'id': lzma.FILTER_LZMA2, 'preset': 6,
                                             'dict_size': 8 * 1024 * 1024}])
            changed.update(metadata_bytes=len(body), metadata_sha256=C.digest(body),
                           compressed_bytes=len(encoded), compressed_sha256=C.digest(encoded),
                           metadata_xz_base64=base64.b64encode(encoded).decode())
        try:
            decode_capture(changed)
        except ValueError as exc:
            controls.append({'case': name, 'refused': True, 'reason': str(exc)})
        else:
            raise ValueError('heading decoder control accepted: ' + name)
    require(decode_capture(frame) == original, 'codec controls changed their original capture')
    return controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output')
    parser.add_argument('--addition', action='append', default=[])
    parser.add_argument('--jobs', type=int, default=2, choices=[1, 2])
    parser.add_argument('--require-clean', action='store_true')
    parser.add_argument('--record', default='docs/tasks/artifacts/live-containment/include-source-integration.md')
    parser.add_argument('--verify-record', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    try:
        if args.verify_record or args.self_test:
            require(args.output is None and not args.addition and not args.require_clean,
                    'record query does not accept capture arguments')
            frame = record_frame(args.record)
            value = decode_capture(frame)
            controls = codec_controls(frame) if args.self_test else []
            print(json.dumps({'source': SOURCE, 'pages': len(value['normal']['observations']),
                              'source_defects': value['normal']['source_defects'],
                              'codec_controls': len(controls)}, sort_keys=True))
            return 0
        require(args.output is not None, 'fresh --output required')
        C.Q.relative_path(args.output)
        require(args.output.startswith('target/'), 'owned target output required')
        output = C.U.source_path(ROOT, args.output)
        result = qualify(output, args.addition, args.jobs)
        N.write_json(output / 'result.json', result)
        print(json.dumps({'source': SOURCE, 'pages': len(result['observations']),
                          'source_headers': sum(len(row['observation']['source_headers'])
                                                for row in result['observations']),
                          'source_defects': result['source_defects'],
                          'actual_omissions': len(result['actual_omissions'])}, sort_keys=True))
        return 1 if args.require_clean and result['source_defects'] else 0
    except (ValueError, OSError, UnicodeError, subprocess.SubprocessError) as exc:
        print('BOOK-HEADINGS: REFUSED — ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
