#!/usr/bin/env python3
"""Authenticate the finite cleanup ledger and bounded current view before output.

The two retained products stay ordinary Markdown. Their overlap is deliberate:
one is the whole committed predecessor, the other its exact historical suffix.
No Git, network, extraction or generated cache participates in this reader.
"""
from __future__ import annotations

import argparse
import hashlib
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
SOURCE = '839e9313d79105a079ac73e2259011c761c2d5ce'
INDEX_SHA256 = '7838ebec414f4fb29cf3181da3c1e4b97658712acc78785d07ba27629f7e975f'
MAX_INDEX = 8192
MAX_FRONT = 4096
MAX_MEMBER = 131072
MAX_TERMINAL = 127271
SECTIONS = {'acceptance': 16384, 'verification': 8192,
            'commits': 4096, 'changelog': 4096}
FIELDS = {'schema_version', 'kind', 'source', 'source_path', 'source_mode',
          'source_git_oid', 'recorded_on', 'owner', 'predecessor', 'retired_suffix',
          'suffix_offset', 'unretained_bytes', 'front_sha256', 'live_path',
          'narrative_health_bytes', 'narrative_ceiling_bytes',
          'section_ceiling_bytes', 'warning_percent', 'rollover_percent'}
MEMBER_FIELDS = {'object', 'bytes', 'lines', 'sha256'}
NARRATIVE = re.compile(rb'^## (?:Acceptance Checklist[^\n]*|Verification Log|Commit Log|Changelog)\n', re.M)
Refused = T.ArchiveRefused
require, digest = T.require, T.digest


def integer(value, lower, upper):
    return type(value) is int and lower <= value <= upper


def descriptor(raw):
    require(len(raw) <= MAX_INDEX, 'cleanup descriptor exceeds bound')
    row = T.json_object(raw)
    require(isinstance(row, dict) and set(row) == FIELDS,
            'unknown cleanup descriptor fields')
    require(type(row['schema_version']) is int and row['schema_version'] == 1
            and row['kind'] == 'artifact-cleanup-ledger', 'cleanup descriptor schema differs')
    require(row['source'] == SOURCE and row['source_path'] == LIVE
            and row['live_path'] == LIVE and row['source_mode'] == '100644'
            and row['recorded_on'] == '2026-10-20'
            and row['owner'] == 'ARTIFACT-CLEANUP.19', 'cleanup capture boundary differs')
    require(T.identity(row['source_git_oid'], 40)
            and T.identity(row['front_sha256'], 64), 'malformed cleanup source identity')
    for field, label in [('predecessor', 'predecessor'), ('retired_suffix', 'ledger')]:
        entry = row[field]
        require(isinstance(entry, dict) and set(entry) == MEMBER_FIELDS,
                'unknown cleanup member fields')
        require(T.identity(entry['sha256'], 64)
                and entry['object'] == PREFIX + label + '-' + entry['sha256'] + '.md',
                'unsafe cleanup member path')
        require(integer(entry['bytes'], 1, MAX_MEMBER)
                and integer(entry['lines'], 1, MAX_MEMBER), 'cleanup member count is not a bounded integer')
    require(integer(row['suffix_offset'], 1, MAX_MEMBER)
            and integer(row['unretained_bytes'], 0, 0), 'cleanup extraction count is not a bounded integer')
    expected = {'narrative_health_bytes': 16384, 'narrative_ceiling_bytes': 32768,
                'warning_percent': 75, 'rollover_percent': 90}
    require(all(type(row[key]) is int and row[key] == value for key, value in expected.items()),
            'cleanup narrative contract differs')
    limits = row['section_ceiling_bytes']
    require(isinstance(limits, dict) and set(limits) == set(SECTIONS)
            and all(type(limits[key]) is int and limits[key] == value
                    for key, value in SECTIONS.items()), 'cleanup section contract differs')
    return row


def validate_terminal(files):
    """Judge one complete, bounded mapping of relative path to (Git mode, bytes)."""
    require(INDEX in files, 'missing cleanup descriptor')
    mode, raw = files[INDEX]
    require(mode == '100644', 'cleanup descriptor mode differs')
    row = descriptor(raw)
    require(digest(raw) == INDEX_SHA256, 'immutable cleanup descriptor differs')
    names = {INDEX, FRONT, row['predecessor']['object'], row['retired_suffix']['object']}
    require(set(files) == names, 'finite cleanup terminal coverage differs')
    require(sum(len(body) for _, body in files.values()) <= MAX_TERMINAL,
            'cleanup terminal exceeds byte bound')
    require(all(mode == '100644' for mode, _ in files.values()), 'cleanup terminal mode differs')
    front = files[FRONT][1]
    require(len(front) <= MAX_FRONT and digest(front) == row['front_sha256'],
            'cleanup retention page differs')
    bodies = {}
    for role in ['predecessor', 'retired_suffix']:
        entry = row[role]
        body = files[entry['object']][1]
        require(len(body) == entry['bytes'] and body.count(b'\n') == entry['lines']
                and digest(body) == entry['sha256'], 'cleanup original identity differs: ' + role)
        try:
            body.decode('utf-8')
        except UnicodeError as error:
            raise Refused('cleanup original is not UTF-8') from error
        bodies[role] = body
    source, suffix = bodies['predecessor'], bodies['retired_suffix']
    offset = row['suffix_offset']
    require(source.find(b'## Acceptance Checklist') == offset
            and source[offset:] == suffix, 'cleanup suffix is not the exact predecessor suffix')
    oid = hashlib.sha1(b'blob ' + str(len(source)).encode() + b'\0' + source).hexdigest()
    require(oid == row['source_git_oid'], 'cleanup source Git identity differs')
    return row, bodies


def read_terminal(root):
    """Census exactly four regular owned files; reject unknown directories first."""
    directory = Q.owned_root(root / PREFIX)
    info = directory.lstat()
    require(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode)
            and info.st_dev == root.stat().st_dev, 'unsafe cleanup terminal directory')
    require(not (directory / '.git').exists() and not (directory / '.git').is_symlink(),
            'Git boundary in cleanup terminal')
    found = []
    for child in directory.iterdir():
        require(len(found) < 4, 'finite cleanup terminal coverage differs')
        child_info = child.lstat()
        require(stat.S_ISREG(child_info.st_mode) and not stat.S_ISLNK(child_info.st_mode)
                and child_info.st_dev == root.stat().st_dev,
                'unsafe cleanup terminal member')
        found.append(PREFIX + child.name)
    require(len(found) == 4 and INDEX in found, 'finite cleanup terminal coverage differs')
    files = {name: Q.read_file(root, name, MAX_INDEX if name == INDEX else
                               MAX_FRONT if name == FRONT else MAX_MEMBER) for name in found}
    row, bodies = validate_terminal(files)
    return row, bodies, files


def pointer(row):
    predecessor = Path(row['predecessor']['object']).name
    ledger = Path(row['retired_suffix']['object']).name
    return (f'<!-- ARTIFACT-CLEANUP-LEDGER: {INDEX_SHA256} -->\n'
            f'Completed checklists/logs: [exact ledger](../artifact-cleanup-history/{ledger}).\n'
            f'The [whole predecessor](../artifact-cleanup-history/{predecessor}) and\n'
            '[retention contract](../artifact-cleanup-history/README.md) remain directly readable.\n'
            '<!-- /ARTIFACT-CLEANUP-LEDGER -->\n\n').encode()


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


def validate_live(raw, row, source):
    require(len(raw) <= MAX_MEMBER, 'cleanup live task exceeds file bound')
    try:
        raw.decode('utf-8')
    except UnicodeError as error:
        raise Refused('cleanup live task is not UTF-8') from error
    exact = pointer(row)
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
        nodes = preserve_graph(source[:row['suffix_offset']], prefix)
    except (UnicodeError, task_source.TaskSourceError) as error:
        raise Refused('cleanup task graph unavailable: ' + str(error)) from error
    return {'narrative_bytes': len(ledger), 'sections': sizes, 'nodes': nodes,
            'warning': len(ledger) * 100 >= row['narrative_health_bytes'] * row['warning_percent']}


def load(root):
    row, bodies, files = read_terminal(root)
    mode, raw = Q.read_file(root, LIVE, MAX_MEMBER)
    require(mode == '100644', 'cleanup live task mode differs')
    usage = validate_live(raw, row, bodies['predecessor'])
    return row, bodies, files, usage


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--read', choices=['ledger', 'predecessor'])
    parser.add_argument('--root', default='.', help='owned project-relative fixture root')
    arguments = parser.parse_args()
    try:
        root = Q.owned_root(arguments.root)
        row, bodies, _, usage = load(root)
        if arguments.read:
            sys.stdout.buffer.write(bodies['retired_suffix' if arguments.read == 'ledger' else 'predecessor'])
        else:
            print('CLEANUP-TASK-HISTORY: exact predecessor/suffix, unique live pointer and complete graph; '
                  f"{usage['narrative_bytes']} live narrative bytes; "
                  + ('warning: owned rollover due' if usage['warning'] else 'within health target'))
    except (Refused, OSError, UnicodeError, task_source.TaskSourceError) as error:
        print('CLEANUP-TASK-HISTORY: REFUSED — ' + str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
