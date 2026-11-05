#!/usr/bin/env python3
"""The frozen corpus GUEST-GEN's author probes judge (ruling 5, XTASK.13 slices b4 and b5).

`derive_rv64gc_expectations.py --check-owned` selects its corpus under the deriver's `REPO`, and a historical record's header depends on the same path, so
`scripts/fixtures/guest-gen/owned/` is laid out as the repository is and the probes point the module under test at it for the one call. The deriver itself is
a pinned input of every retained case and does not move. The real check, the step in GUEST-GEN's run, judges the live corpus: a damaged live record reaches it and is named.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from unittest import mock

import dossier_sexp as D

REPO = Path(__file__).resolve().parent.parent
ROOT = REPO / 'scripts/fixtures/guest-gen/owned'
GUESTS = ROOT / 'profiles/rv64gc-lab-v0/guests'
ENCODING = REPO / 'scripts/fixtures/def-gen/profiles/rv64gc-lab-v0/encoding.sexp'

# The records the author does not own and must still reproduce, register for register: each closed a gap in it (slice b5). `scripts/check_gc_mirror.py`,
# GUEST-GEN's mirror governor, derives every live guest's writes and names a damaged record for each of these, so no real-run step repeats it here.
CORPUS = REPO / 'scripts/fixtures/guest-gen/corpus'
CORPUS_GUESTS = {
    'integer': ('bound-alias', 'bound-arith', 'bound-ext', 'bound-shift', 'bound-shiftw',
                'dir-chain', 'dir-cmp-branch', 'dir-ext-matrix', 'dir-x0-writes',
                'fault-branch-nt', 'fault-hints', 'fault-shiftw-res', 'it-alias-bound',
                'scope-alu', 'scope-branch', 'scope-mem', 'smoke-arith'),
    'privilege': ('mm-readonly', 'mm-sfence', 'mm-sret', 'mm-csr-legality-s', 'mm-csr-legality-u'),
    'counter': ('a-lrsc-mustfail', 'mm-counters', 'mm-stimecmp'),
}


def image_root(image):
    """`matched_gpr_image` reads the canonical composition under its `ROOT`, and it is pinned; this patcher points that one name at DEF-GEN's frozen tree (slice b6)."""
    return mock.patch.object(image, 'ROOT', ENCODING.parents[2])


@contextmanager
def rooted(author):
    """The module under test sees the frozen tree, under DEF-GEN's frozen encoding; it is restored whatever happens."""
    saved = author.REPO, author.ENCODING
    author.REPO, author.ENCODING = ROOT, ENCODING
    try:
        yield
    finally:
        author.REPO, author.ENCODING = saved


def check_owned(author) -> int:
    """`--check-owned` over the frozen corpus."""
    with rooted(author):
        return author.main(['probe', '--check-owned'])


def judge_corpus(author, asm, group: str, label: str) -> int:
    """The steps the author derived for a group's frozen guests, each one's writes equal to its record's; the first difference raises, named."""
    total = 0
    for name in CORPUS_GUESTS[group]:
        path = CORPUS / (name + '.s')
        expected = D.load_expectations(path.with_suffix('.expected.sexp'))
        run = author.derive_parcel_guest(path, asm, expected['instructions'])
        writes = [{int(k[1:]): int(v, 16) for k, v in step['writes'].items()} for step in expected['step']]
        if [step.writes for step in run.steps] != writes:
            raise AssertionError(f'{name}: {label} architectural observations differ')
        total += len(run.steps)
    return total
