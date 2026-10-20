#!/usr/bin/env python3
"""Authenticate the finite cleanup ledger generations and bounded current view before output.

Each generation retains two ordinary Markdown products whose overlap is deliberate:
the whole committed predecessor and its exact historical suffix. A later generation's
suffix begins with the previous generation's pointer, and its retained entry re-derives
the superseded descriptor byte-exactly, so the chain authenticates itself.
No Git, network, extraction or generated cache participates in this reader.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import sys

import qualification_history_archive as Q
import task_history_archive as T
import task_source

PROJECT = Path(__file__).resolve().parent.parent
PREFIX = 'docs/artifact-cleanup-history/'
INDEX = PREFIX + 'descriptor.json'
FRONT = PREFIX + 'README.md'
LIVE = 'docs/tasks/ARTIFACT-CLEANUP.md'
INDEX_SHA256 = '6776eca32531dcb5bd1e4e8fa030b290c4fcfeb3a8eb8811b0a1dffd5c0d481d'
CAPTURES = (('839e9313d79105a079ac73e2259011c761c2d5ce', '2026-10-20', 'ARTIFACT-CLEANUP.19'),
            ('b18971eeea61fdcce6f428693916f4f00b145ba6', '2026-10-20', 'ARTIFACT-CLEANUP.23'))
MAX_GENERATIONS = 8
MAX_INDEX = 8192
MAX_FRONT = 4096
MAX_MEMBER = 131072
SECTIONS = {'acceptance': 16384, 'verification': 8192,
            'commits': 4096, 'changelog': 4096}
CONTRACT = {'narrative_health_bytes': 16384, 'narrative_ceiling_bytes': 32768,
            'warning_percent': 75, 'rollover_percent': 90}
FIELDS = {'schema_version', 'kind', 'live_path', 'generations', 'section_ceiling_bytes', *CONTRACT}
GENERATION_ORDER = ('source', 'source_path', 'source_mode', 'source_git_oid', 'recorded_on',
                    'owner', 'predecessor', 'retired_suffix', 'suffix_offset', 'unretained_bytes',
                    'front_sha256')
GENERATION_FIELDS = {*GENERATION_ORDER, 'predecessor_pointer'}
LEGACY_FIELDS = {'schema_version', 'kind', *GENERATION_ORDER, 'live_path',
                 'section_ceiling_bytes', *CONTRACT}
MEMBER_ORDER = ('object', 'bytes', 'lines', 'sha256')
NARRATIVE = re.compile(rb'^## (?:Acceptance Checklist[^\n]*|Verification Log|Commit Log|Changelog)\n', re.M)
Refused = T.ArchiveRefused
require, digest = T.require, T.digest


def integer(value, lower, upper):
    return type(value) is int and lower <= value <= upper


def member(entry, label):
    require(isinstance(entry, dict) and set(entry) == set(MEMBER_ORDER),
            'unknown cleanup member fields')
    require(T.identity(entry['sha256'], 64)
            and entry['object'] == PREFIX + label + '-' + entry['sha256'] + '.md',
            'unsafe cleanup member path')
    require(integer(entry['bytes'], 1, MAX_MEMBER)
            and integer(entry['lines'], 1, MAX_MEMBER), 'cleanup member count is not a bounded integer')


def generation(entry, index, capture):
    require(isinstance(entry, dict) and set(entry) == GENERATION_FIELDS,
            'unknown cleanup generation fields')
    source, recorded_on, owner = capture
    require(entry['source'] == source and entry['source_path'] == LIVE
            and entry['source_mode'] == '100644' and entry['recorded_on'] == recorded_on
            and entry['owner'] == owner, 'cleanup capture boundary differs')
    require(T.identity(entry['source_git_oid'], 40) and T.identity(entry['front_sha256'], 64),
            'malformed cleanup source identity')
    for field, label in [('predecessor', 'predecessor'), ('retired_suffix', 'ledger')]:
        member(entry[field], label)
    require(integer(entry['suffix_offset'], 1, MAX_MEMBER)
            and integer(entry['unretained_bytes'], 0, 0), 'cleanup extraction count is not a bounded integer')
    pointer_pin = entry['predecessor_pointer']
    require(pointer_pin is None if index == 0 else T.identity(pointer_pin, 64),
            'cleanup generation chain differs')


def contract(row):
    require(all(type(row[key]) is int and row[key] == value for key, value in CONTRACT.items()),
            'cleanup narrative contract differs')
    limits = row['section_ceiling_bytes']
    require(isinstance(limits, dict) and set(limits) == set(SECTIONS)
            and all(type(limits[key]) is int and limits[key] == value
                    for key, value in SECTIONS.items()), 'cleanup section contract differs')


def generation_count(raw):
    """Count the generations a committed descriptor declares, before validating it."""
    require(len(raw) <= MAX_INDEX, 'cleanup descriptor exceeds bound')
    row = T.json_object(raw)
    require(isinstance(row, dict), 'unknown cleanup descriptor fields')
    if set(row) == LEGACY_FIELDS:
        return 1
    require(set(row) == FIELDS and isinstance(row['generations'], list),
            'unknown cleanup descriptor fields')
    return len(row['generations'])


def descriptor(raw, generations=len(CAPTURES)):
    require(len(raw) <= MAX_INDEX, 'cleanup descriptor exceeds bound')
    row = T.json_object(raw)
    require(isinstance(row, dict), 'unknown cleanup descriptor fields')
    if set(row) == LEGACY_FIELDS:
        require(generations == 1, 'cleanup generation count differs')
        require(row['schema_version'] == 1, 'cleanup descriptor schema differs')
        entry = {name: row[name] for name in GENERATION_ORDER}
        row = {name: value for name, value in row.items() if name not in entry}
        row = {**row, 'schema_version': 2, 'generations': [{**entry, 'predecessor_pointer': None}]}
    require(set(row) == FIELDS, 'unknown cleanup descriptor fields')
    require(type(row['schema_version']) is int and row['schema_version'] == 2
            and row['kind'] == 'artifact-cleanup-ledger', 'cleanup descriptor schema differs')
    require(row['live_path'] == LIVE, 'cleanup capture boundary differs')
    chain = row['generations']
    require(isinstance(chain, list) and len(chain) == generations
            and 1 <= generations <= min(MAX_GENERATIONS, len(CAPTURES)), 'cleanup generation count differs')
    for index, (entry, capture) in enumerate(zip(chain, CAPTURES)):
        generation(entry, index, capture)
    contract(row)
    return row


def encoding(row, generations):
    """Exact descriptor bytes for the first generations; version 1 bytes for exactly one."""
    chain = row['generations'][:generations]
    members = lambda entry: {role: {name: entry[role][name] for name in MEMBER_ORDER}
                             for role in ('predecessor', 'retired_suffix')}
    narrative = {'narrative_health_bytes': row['narrative_health_bytes'],
                 'narrative_ceiling_bytes': row['narrative_ceiling_bytes'],
                 'section_ceiling_bytes': {name: row['section_ceiling_bytes'][name] for name in SECTIONS},
                 'warning_percent': row['warning_percent'], 'rollover_percent': row['rollover_percent']}
    if generations == 1:
        entry = chain[0]
        value = {'schema_version': 1, 'kind': 'artifact-cleanup-ledger',
                 **{name: members(entry).get(name, entry[name]) for name in GENERATION_ORDER},
                 'live_path': LIVE, **narrative}
    else:
        value = {'schema_version': 2, 'kind': 'artifact-cleanup-ledger', 'live_path': LIVE,
                 'generations': [{**{name: members(entry).get(name, entry[name]) for name in GENERATION_ORDER},
                                  'predecessor_pointer': entry['predecessor_pointer']} for entry in chain],
                 **narrative}
    return (json.dumps(value, indent=2) + '\n').encode()


def pointer(entry, pin=None):
    pin = INDEX_SHA256 if pin is None else pin
    predecessor = Path(entry['predecessor']['object']).name
    ledger = Path(entry['retired_suffix']['object']).name
    return (f'<!-- ARTIFACT-CLEANUP-LEDGER: {pin} -->\n'
            f'Completed checklists/logs: [exact ledger](../artifact-cleanup-history/{ledger}).\n'
            f'The [whole predecessor](../artifact-cleanup-history/{predecessor}) and\n'
            '[retention contract](../artifact-cleanup-history/README.md) remain directly readable.\n'
            '<!-- /ARTIFACT-CLEANUP-LEDGER -->\n\n').encode()


def validate_terminal(files, *, pin=None, generations=len(CAPTURES), front=True):
    """Judge one complete, bounded mapping of relative path to (Git mode, bytes)."""
    pin = INDEX_SHA256 if pin is None else pin
    require(INDEX in files, 'missing cleanup descriptor')
    mode, raw = files[INDEX]
    require(mode == '100644', 'cleanup descriptor mode differs')
    row = descriptor(raw, generations)
    require(digest(raw) == pin, 'immutable cleanup descriptor differs')
    require(encoding(row, generations) == raw, 'noncanonical cleanup descriptor')
    chain = row['generations']
    objects = [entry[role]['object'] for entry in chain for role in ('predecessor', 'retired_suffix')]
    names = {INDEX, FRONT, *objects}
    require(len(names) == 2 + len(objects) and set(files) == names,
            'finite cleanup terminal coverage differs')
    declared = sum(entry[role]['bytes'] for entry in chain for role in ('predecessor', 'retired_suffix'))
    require(sum(len(body) for _, body in files.values()) <= MAX_INDEX + MAX_FRONT + declared,
            'cleanup terminal exceeds byte bound')
    require(all(mode == '100644' for mode, _ in files.values()), 'cleanup terminal mode differs')
    page = files[FRONT][1]
    require(len(page) <= MAX_FRONT and (not front or digest(page) == chain[-1]['front_sha256']),
            'cleanup retention page differs')
    bodies, previous = [], None
    for index, entry in enumerate(chain):
        originals = {}
        for role in ['predecessor', 'retired_suffix']:
            item = entry[role]
            body = files[item['object']][1]
            require(len(body) == item['bytes'] and body.count(b'\n') == item['lines']
                    and digest(body) == item['sha256'], 'cleanup original identity differs: ' + role)
            try:
                body.decode('utf-8')
            except UnicodeError as error:
                raise Refused('cleanup original is not UTF-8') from error
            originals[role] = body
        source, suffix = originals['predecessor'], originals['retired_suffix']
        offset = entry['suffix_offset']
        if index == 0:
            boundary = b'## Acceptance Checklist'
        else:
            require(digest(encoding(row, index)) == entry['predecessor_pointer'],
                    'cleanup generation chain differs')
            boundary = pointer(chain[index - 1], entry['predecessor_pointer'])
            require(source.count(boundary) == 1 and not NARRATIVE.search(source[:offset]),
                    'cleanup generation chain differs')
            try:
                preserve_graph(previous[0][:previous[1]], source[:offset])
            except (UnicodeError, task_source.TaskSourceError) as error:
                raise Refused('cleanup generation graph unavailable: ' + str(error)) from error
        require(source.find(boundary) == offset
                and source[offset:] == suffix, 'cleanup suffix is not the exact predecessor suffix')
        oid = hashlib.sha1(b'blob ' + str(len(source)).encode() + b'\0' + source).hexdigest()
        require(oid == entry['source_git_oid'], 'cleanup source Git identity differs')
        bodies.append(originals)
        previous = (source, offset)
    return row, bodies


def read_terminal(root, generations=len(CAPTURES)):
    """Census exactly two files per generation plus descriptor/front; reject unknown directories first."""
    directory = Q.owned_root(root / PREFIX)
    info = directory.lstat()
    require(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode)
            and info.st_dev == root.stat().st_dev, 'unsafe cleanup terminal directory')
    require(not (directory / '.git').exists() and not (directory / '.git').is_symlink(),
            'Git boundary in cleanup terminal')
    limit = 2 + 2 * generations
    found = []
    for child in directory.iterdir():
        require(len(found) < limit, 'finite cleanup terminal coverage differs')
        child_info = child.lstat()
        require(stat.S_ISREG(child_info.st_mode) and not stat.S_ISLNK(child_info.st_mode)
                and child_info.st_dev == root.stat().st_dev,
                'unsafe cleanup terminal member')
        found.append(PREFIX + child.name)
    require(len(found) == limit and INDEX in found, 'finite cleanup terminal coverage differs')
    files = {name: Q.read_file(root, name, MAX_INDEX if name == INDEX else
                               MAX_FRONT if name == FRONT else MAX_MEMBER) for name in found}
    row, bodies = validate_terminal(files, generations=generations)
    return row, bodies, files


def graph(text):
    """Use the published numeric-leaf reader; bind structural child groups too."""
    leaves = task_source.direct_leaves('ARTIFACT-CLEANUP', text)
    require(bool(leaves), 'cleanup live graph is empty')
    groups, owner = {}, None
    for line in text.splitlines():
        if line.startswith('- ID:'):
            match = re.fullmatch(r'- ID: `([A-Za-z0-9._-]+)`(?:.*)', line)
            require(match is not None, 'unsupported cleanup node spelling')
            owner = match[1]
        elif line.startswith('### '):
            owner = line
        elif line.startswith('## '):
            owner = None
        if line.startswith('  Children:'):
            require(owner is not None and owner not in groups, 'ambiguous cleanup child group')
            children = re.findall(r'`([^`]+)`', line)
            require(children and len(children) == len(set(children))
                    and all(child in leaves for child in children), 'cleanup child closure differs')
            groups[owner] = set(children)
    require(groups.get('ARTIFACT-CLEANUP') == set(leaves), 'cleanup root child closure differs')
    return leaves, groups


def preserve_graph(before, after):
    original, old_groups = graph(before.decode('utf-8'))
    current, groups = graph(after.decode('utf-8'))
    require(list(current)[:len(original)] == list(original), 'cleanup live node order/population differs')
    require(all(current[name] == 'done' for name, status in original.items() if status == 'done'),
            'completed cleanup node status regressed')
    require(all(name in groups and children <= groups[name] for name, children in old_groups.items()),
            'cleanup structural child group was lost')
    return len(current)


def validate_live(raw, row, bodies):
    require(len(raw) <= MAX_MEMBER, 'cleanup live task exceeds file bound')
    try:
        raw.decode('utf-8')
    except UnicodeError as error:
        raise Refused('cleanup live task is not UTF-8') from error
    latest, source = row['generations'][-1], bodies[-1]['predecessor']
    exact = pointer(latest)
    require(raw.count(b'<!-- ARTIFACT-CLEANUP-LEDGER:') == 1 and raw.count(exact) == 1,
            'cleanup live history pointer differs or is not unique')
    prefix, ledger = raw.split(exact)
    require(not NARRATIVE.search(prefix), 'cleanup narrative precedes its history pointer')
    require(len(ledger) <= row['narrative_ceiling_bytes'], 'cleanup live narrative exceeds ceiling')
    headers = list(NARRATIVE.finditer(ledger))
    require(headers and headers[0].start() == 0, 'cleanup live ledger has unclassified prefix')
    kinds = []
    sizes = dict.fromkeys(SECTIONS, 0)
    for index, heading in enumerate(headers):
        name = heading[0]
        kind = ('acceptance' if b'Acceptance Checklist' in name else
                'verification' if b'Verification Log' in name else
                'commits' if b'Commit Log' in name else 'changelog')
        end = headers[index + 1].start() if index + 1 < len(headers) else len(ledger)
        sizes[kind] += end - heading.start()
        kinds.append(kind)
    require(set(kinds) == set(SECTIONS) and kinds.count('verification') == 1
            and kinds.count('commits') == 1 and kinds.count('changelog') == 1,
            'cleanup live ledger section coverage differs')
    require(kinds == ['acceptance'] * kinds.count('acceptance')
            + ['verification', 'commits', 'changelog'], 'cleanup live ledger section order differs')
    require(all(sizes[key] <= SECTIONS[key] for key in sizes), 'cleanup live section exceeds ceiling')
    require(len(ledger) * 100 < row['narrative_health_bytes'] * row['rollover_percent'],
            'cleanup live narrative requires owned rollover before ordinary growth')
    try:
        nodes = preserve_graph(source[:latest['suffix_offset']], prefix)
    except (UnicodeError, task_source.TaskSourceError) as error:
        raise Refused('cleanup task graph unavailable: ' + str(error)) from error
    return {'narrative_bytes': len(ledger), 'sections': sizes, 'nodes': nodes,
            'warning': len(ledger) * 100 >= row['narrative_health_bytes'] * row['warning_percent']}


def load(root):
    row, bodies, files = read_terminal(root)
    mode, raw = Q.read_file(root, LIVE, MAX_MEMBER)
    require(mode == '100644', 'cleanup live task mode differs')
    usage = validate_live(raw, row, bodies)
    return row, bodies, files, usage


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--read', choices=['ledger', 'predecessor'])
    parser.add_argument('--generation', type=int, help='1-based generation to read; default latest')
    parser.add_argument('--root', default='.', help='owned project-relative fixture root')
    arguments = parser.parse_args()
    try:
        root = Q.owned_root(arguments.root)
        row, bodies, _, usage = load(root)
        count = len(bodies)
        if arguments.read:
            index = count if arguments.generation is None else arguments.generation
            require(integer(index, 1, count), 'unknown cleanup generation')
            sys.stdout.buffer.write(bodies[index - 1]['retired_suffix' if arguments.read == 'ledger'
                                                      else 'predecessor'])
        else:
            require(arguments.generation is None, 'generation selects a read')
            print('CLEANUP-TASK-HISTORY: exact predecessor/suffix, unique live pointer and complete graph; '
                  f"{count} generations; {usage['narrative_bytes']} live narrative bytes; "
                  + ('warning: owned rollover due' if usage['warning'] else 'within health target'))
    except (Refused, OSError, UnicodeError, task_source.TaskSourceError) as error:
        print('CLEANUP-TASK-HISTORY: REFUSED — ' + str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
