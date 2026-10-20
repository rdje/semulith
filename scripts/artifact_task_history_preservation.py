#!/usr/bin/env python3
"""Authenticate each generation transition; preserve immutable and live history in both views.

Only this publishing gate uses Git. Published terminal identity is compared to
HEAD, so later checks work in shallow clones without fetching the source commit.
A transition adds exactly one generation: HEAD must be its source, HEAD's live task
its predecessor, every earlier object stays byte-exact and the live prefix survives.
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys

import artifact_task_history as A

WIRING = ('scripts/artifact_task_history.py',
          'scripts/artifact_task_history_preservation.py',
          'scripts/probe_artifact_task_history.py', 'scripts/check_task_history.sh',
          'doctrine/readme_routes.tsv', 'docs/book/src/working/task-trees.md',
          'docs/toolbox/artifacts.md', 'docs/doctrines/governance.md')
MAX_FILES = 32
MAX_BLOB = 262144
MAX_BYTES = 1048576
require = A.require


def git_read(root, *arguments, data=None):
    result = subprocess.run(['git', '--no-pager', '--no-optional-locks',
                             '--no-replace-objects', '-C', str(root), *arguments],
                            input=data, capture_output=True, timeout=30,
                            env=dict(os.environ, GIT_NO_LAZY_FETCH='1'))
    require(result.returncode == 0 and not result.stderr,
            'cleanup publishing Git read unavailable: ' + ' '.join(arguments))
    require(len(result.stdout) <= MAX_BYTES + MAX_FILES * 512,
            'cleanup publishing Git response exceeds bound')
    return result.stdout


def snapshot(root, revision):
    paths = [A.PREFIX, A.LIVE, *WIRING]
    staged = revision == ':'
    arguments = (['ls-files', '--stage', '-z', '--', *paths] if staged else
                 ['ls-tree', '-rz', '--full-tree', revision, '--', *paths])
    raw = git_read(root, *arguments)
    require(len(raw) <= MAX_FILES * 512 and (not raw or raw.endswith(b'\0')),
            'cleanup publishing inventory exceeds bound or is incomplete')
    identities = {}
    for item in raw.split(b'\0')[:-1]:
        metadata, separator, encoded = item.partition(b'\t')
        fields = metadata.split()
        require(separator and len(fields) == 3, 'malformed cleanup publishing inventory')
        name = encoded.decode('utf-8')
        require(name in WIRING or name == A.LIVE or name.startswith(A.PREFIX),
                'unknown cleanup publishing input')
        if staged:
            mode, oid, stage = fields
            require(stage == b'0', 'unmerged cleanup publishing input')
        else:
            mode, kind, oid = fields
            require(kind == b'blob', 'cleanup publishing input is not a blob')
        require(mode in {b'100644', b'100755'} and A.T.identity(oid.decode('ascii'), 40)
                and name not in identities, 'unsafe/duplicate cleanup publishing identity')
        identities[name] = (mode.decode('ascii'), oid)
        require(len(identities) <= MAX_FILES, 'cleanup publishing file bound exceeded')
    if not identities:
        return {}
    requests = b''.join(oid + b'\n' for _, oid in identities.values())
    raw_sizes = git_read(root, 'cat-file', '--batch-check', data=requests)
    require(raw_sizes.endswith(b'\n') and len(raw_sizes) <= MAX_FILES * 128
            and len(raw_sizes.splitlines()) == len(identities), 'incomplete cleanup publishing sizes')
    entries = []
    for (name, (mode, oid)), line in zip(identities.items(), raw_sizes.splitlines()):
        fields = line.split()
        require(len(fields) == 3 and fields[:2] == [oid, b'blob']
                and fields[2].isdigit() and len(fields[2]) <= 8,
                'malformed cleanup publishing size')
        size = int(fields[2])
        require(size <= MAX_BLOB, 'cleanup publishing blob exceeds bound')
        entries.append((name, mode, oid, size))
    require(sum(row[3] for row in entries) <= MAX_BYTES, 'cleanup publishing snapshot exceeds bound')
    stream = git_read(root, 'cat-file', '--batch', data=requests)
    result, cursor = {}, 0
    for name, mode, oid, size in entries:
        end = stream.find(b'\n', cursor)
        require(end >= 0 and stream[cursor:end] == oid + b' blob ' + str(size).encode(),
                'malformed cleanup publishing blob header')
        start = end + 1
        body = stream[start:start + size]
        require(len(body) == size and stream[start + size:start + size + 1] == b'\n',
                'incomplete cleanup publishing blob')
        actual = hashlib.sha1(b'blob ' + str(size).encode() + b'\0' + body).hexdigest()
        require(actual.encode() == oid, 'cleanup publishing blob identity differs')
        result[name] = (mode, body)
        cursor = start + size + 1
    require(cursor == len(stream), 'surplus cleanup publishing blob response')
    return result


def original_prefix(raw, entry):
    exact = A.pointer(entry)
    require(raw.count(exact) == 1, 'cleanup publishing pointer differs')
    return raw.split(exact)[0]


def first_transition(source, current, entry):
    """Everything before the retired suffix survives, except the owner's state and the frontier."""
    old = source[:entry['suffix_offset']]
    now = original_prefix(current, entry)
    pattern = rb'(- ID: `' + re.escape(entry['owner']).encode() + rb'`[^\n]*\n  Status: )[^\n]+\n'
    require(len(re.findall(pattern, now)) == 1, 'cleanup transition owner is ambiguous')
    now = re.sub(pattern, rb'\g<1>`pending`\n', now, count=1)
    start, end = b'## Current Frontier\n', b'## Decisions\n'
    require(now.count(start) == now.count(end) == old.count(start) == old.count(end) == 1,
            'cleanup transition frontier is ambiguous')
    a, b = now.index(start), now.index(end)
    require(a < b, 'cleanup transition frontier order differs')
    now = now[:a] + old[old.index(start):old.index(end)] + now[b:]
    require(now == old, 'cleanup transition lost or changed predecessor prefix')


def preserve_ledger(before, after, entry):
    """New entries prepend; completed acceptance/log bytes stay exact and ordered."""
    exact = A.pointer(entry)
    previous, proposed = before.split(exact)[1], after.split(exact)[1]

    def split(raw):
        marks = list(A.NARRATIVE.finditer(raw))
        result = {}
        for index, mark in enumerate(marks):
            title = mark[0]
            key = ('acceptance' if b'Acceptance Checklist' in title else
                   'verification' if b'Verification Log' in title else
                   'commits' if b'Commit Log' in title else 'changelog')
            end = marks[index + 1].start() if index + 1 < len(marks) else len(raw)
            result[key] = result.get(key, b'') + raw[mark.start():end]
        return result

    old, new = split(previous), split(proposed)
    require(new['acceptance'].endswith(old['acceptance']), 'published cleanup acceptance history changed')
    for kind, lines in [('verification', 4), ('commits', 2), ('changelog', 2)]:
        old_lines, new_lines = old[kind].splitlines(keepends=True), new[kind].splitlines(keepends=True)
        require(new_lines[:lines] == old_lines[:lines]
                and b''.join(new_lines[lines:]).endswith(b''.join(old_lines[lines:])),
                'published cleanup ' + kind + ' history changed')
    A.preserve_graph(original_prefix(before, entry), original_prefix(after, entry))


def judge(previous, proposed, working, wiring_previous, wiring_proposed, wiring_working):
    """Return True for a generation transition, False for an ordinary published commit."""
    terminal = lambda view: {name: value for name, value in view.items() if name.startswith(A.PREFIX)}
    row, bodies = A.validate_terminal(terminal(working))
    latest, count = row['generations'][-1], len(row['generations'])
    require(A.LIVE in working and working[A.LIVE][0] == '100644',
            'working cleanup live task missing/mode differs')
    A.validate_live(working[A.LIVE][1], row, bodies)
    held = terminal(previous)
    previous_count = A.generation_count(held[A.INDEX][1]) if A.INDEX in held else 0
    require(previous_count in {count, count - 1}, 'cleanup generation count differs from the committed terminal')
    transition = previous_count == count - 1
    if not transition:
        A.validate_terminal(held)
        require(A.LIVE in previous and previous[A.LIVE][0] == '100644',
                'published cleanup live task missing/mode differs')
        A.validate_live(previous[A.LIVE][1], row, bodies)
        require(terminal(proposed) == held, 'published cleanup staged terminal changed')
        require(terminal(working) == held, 'published cleanup working terminal changed')
        for label, view in [('staged', proposed), ('working', working)]:
            require(A.LIVE in view and view[A.LIVE][0] == '100644', label + ' cleanup live task missing/mode differs')
            A.validate_live(view[A.LIVE][1], row, bodies)
            preserve_ledger(previous[A.LIVE][1], view[A.LIVE][1], latest)
    else:
        if previous_count:
            # Every earlier object is pinned by the chain the working terminal already passed.
            A.validate_terminal(held, pin=latest['predecessor_pointer'], generations=previous_count, front=False)
        require(previous.get(A.LIVE) == (latest['source_mode'], bodies[-1]['predecessor']),
                'cleanup first publication source bytes/mode differ')
        first_transition(bodies[-1]['predecessor'], working[A.LIVE][1], latest)
        changed = proposed != previous or wiring_proposed != wiring_previous
        if changed:
            require(proposed == working, 'cleanup first publication staged/working views differ')
            require(set(wiring_proposed) == set(WIRING) and wiring_proposed == wiring_working,
                    'cleanup first publication wiring incomplete or differs')
    return transition


def check(root):
    head = git_read(root, 'rev-parse', '--verify', 'HEAD').decode().strip()
    require(A.T.identity(head, 40), 'cleanup publishing HEAD is invalid')
    previous_all, proposed_all = snapshot(root, head), snapshot(root, ':')
    row, bodies, working_terminal, _ = A.load(root)
    working = {**working_terminal, A.LIVE: A.Q.read_file(root, A.LIVE, A.MAX_MEMBER)}
    working_wiring = {name: A.Q.read_file(root, name, MAX_BLOB) for name in WIRING}
    data = lambda view: {name: value for name, value in view.items() if name not in WIRING}
    wiring = lambda view: {name: value for name, value in view.items() if name in WIRING}
    transition = judge(data(previous_all), data(proposed_all), working,
                       wiring(previous_all), wiring(proposed_all), working_wiring)
    if transition:
        latest = row['generations'][-1]
        require(head == latest['source'], 'cleanup first publication source commit differs')
        require(previous_all.get(A.LIVE) == (latest['source_mode'], bodies[-1]['predecessor']),
                'cleanup committed predecessor differs')
    require(git_read(root, 'rev-parse', '--verify', 'HEAD').decode().strip() == head,
            'cleanup publishing HEAD changed during check')
    return transition


def main():
    try:
        require(len(sys.argv) == 1, 'unknown cleanup publishing arguments')
        transition = check(A.PROJECT)
    except (A.Refused, OSError, UnicodeError, ValueError, subprocess.SubprocessError) as error:
        print('CLEANUP-TASK-PRESERVATION: REFUSED — ' + str(error), file=sys.stderr)
        return 2
    print('CLEANUP-TASK-PRESERVATION: exact ' +
          ('generation transition/source/prefix' if transition else 'published terminal and both live histories'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
