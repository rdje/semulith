#!/usr/bin/env python3
"""The frozen owned corpus GUEST-GEN's author probes judge (ruling 5, XTASK.13 slice b4).

`derive_rv64gc_expectations.py --check-owned` selects its corpus under the deriver's `REPO`, and a historical record's header depends on the same path, so
`scripts/fixtures/guest-gen/owned/` is laid out as the repository is and the probes point the module under test at it for the one call. The deriver itself is
a pinned input of every retained case and does not move. The real check, the step in GUEST-GEN's run, judges the live corpus: a damaged live record reaches it and is named.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROOT = REPO / 'scripts/fixtures/guest-gen/owned'
GUESTS = ROOT / 'profiles/rv64gc-lab-v0/guests'
ENCODING = REPO / 'scripts/fixtures/def-gen/profiles/rv64gc-lab-v0/encoding.sexp'


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
