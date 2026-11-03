#!/usr/bin/env python3
"""Retain the licensed, source-pinned statements a matched case's properties cite, never the website shell.

A case's normative input is a retained excerpt whose wrapper names the one original page it was copied from, and that page
must be the case's source publication (`review_div_capture.check_retained_input`, `P4-SYSTEM.14` a44-2c). The M and RV64I
excerpts each have their own module (`retain_div_statement.py`, `retain_m_statements.py`, `retain_rv64i_statements.py`). This
is the one table for the cases after them (a43b-3b): an excerpt is a row of `EXCERPTS` — the page and its pin, the licence
evidence and its pin, the statements in source order, the retained path and its pin — and every row goes through the same
bounded pure transformation. Emission reads the acquired pages; verification authenticates only the retained file, without
them. Neither operation is a comparison, capture, property binding, credit or qualification.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sys

import experiment_artifacts as A

ROOT = Path(__file__).resolve().parent.parent
PAGES = ".materials/riscv/pinned-v20260120/"
SITE = "https://docs.riscv.org/reference/isa/v20260120/"
PAGE_BYTES = 262144
LICENCE_BYTES = 131072
RETAINED_BYTES = 8192
SPAN_BYTES = 1024
# The sentence both volumes' prefaces state, line breaks included (materials/RVI_M_RETENTION.md).
LICENCE_STATEMENT = (
    b"Commons Attribution 4.0 International License by the original authors,\n"
    b"and this and future versions of this document will be released under the\n"
    b"same license."
)
# A statement's markup, measured span by span before review: emphasis, code, and the manual's own cross-reference to another
# page of the same publication — kept unmodified, as the licence's reproduction asks. Any other tag or attribute refuses.
OPENING_TAGS = (re.compile(rb"<em>"), re.compile(rb"<code>"),
                re.compile(rb'<a href="[a-z0-9-]+\.html#[A-Za-z0-9_:-]+" class="xref page">'))


@dataclass(frozen=True)
class Page:
    """One pinned page of the acquired snapshot."""
    input_id: str
    file: str
    sha256: str
    label: str  # how the wrapper names it


@dataclass(frozen=True)
class Excerpt:
    input_id: str
    heading: str
    source: Page
    licence: Page
    retained_path: str
    retained_sha256: str
    statements: tuple  # (span name, section), in source order
    scope_note: str


PRIVILEGED_LICENCE = Page("RVP-PRIV-LICENCE", "priv/priv-preface.html",
                          "6e4ba2ab3ea5174ff04881c48df7dfaf9402a0d070a76805535f1c7754645e59",
                          "privileged preface to Version 1.10")
EXCERPTS = {
    "RVP-CSR-STATEMENTS": Excerpt(
        "RVP-CSR-STATEMENTS", "RVP-CSR §1.1.1: which privilege may access a CSR, and what an attempt without it does",
        Page("RVP-CSR", "priv/priv-csrs.html", "330a17314ef803231955a915748176e5175fc773469f25a8c6b5ae922c9df425",
             "RISC-V Privileged Architecture, §1.1 Control and Status Registers (CSRs)"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-csr-statements.html", "0f2d75c5e8fb85505577c62320d035680704d9afeb8aae0e978174edbc63aba6",
        (("norm:Zicsr_higher_priv", "§1.1.1"), ("norm:Zicsr_rw", "§1.1.1"), ("norm:Zicsr_access", "§1.1.1"),
         ("norm:Zicsr_illegal_mode", "§1.1.1"), ("norm:Zicsr_illegal_acc", "§1.1.1")),
        "This excerpt establishes no CSR-SET acceptance."),
}


class RetentionError(ValueError):
    """No partial retained artifact escapes a refused source transformation."""


def require(condition, reason):
    if not condition:
        raise RetentionError(reason)


def pinned(data, limit, digest, name):
    require(type(data) is bytes and 1 <= len(data) <= limit, name + " byte bound/type")
    require(hashlib.sha256(data).hexdigest() == digest, name + " pin differs")


def select_span(source: bytes, name: str) -> bytes:
    marker = b'<span id="' + name.encode() + b'">'
    start = source.find(marker)
    require(start >= 0, f"{name}: statement is absent")
    require(source.count(marker) == 1, f"{name}: statement is duplicated")
    end = source.find(b"</span>", start + len(marker))
    require(end >= 0, f"{name}: statement is unterminated")
    span = source[start: end + len(b"</span>")]
    require(len(span) <= SPAN_BYTES, f"{name}: statement exceeds bound")
    inner = span[len(marker): -len(b"</span>")]
    for tag in re.findall(rb"<[a-zA-Z0-9][^>]*>", inner):
        require(any(shape.fullmatch(tag) for shape in OPENING_TAGS), f"{name} carries unreviewed markup {tag[:40]!r}")
    span.decode("utf-8")
    return span


def retain_statements(excerpt: Excerpt, source: bytes, licence: bytes) -> bytes:
    """Copy the row's exact spans after checking both complete, frozen primary inputs."""
    pinned(source, PAGE_BYTES, excerpt.source.sha256, excerpt.source.input_id)
    pinned(licence, LICENCE_BYTES, excerpt.licence.sha256, "licence evidence")
    require(LICENCE_STATEMENT in licence, "reviewed licence statement is absent")
    spans = [(name, section, select_span(source, name)) for name, section in excerpt.statements]
    header = f"""<!doctype html>
<html lang="en"><meta charset="utf-8">
<title>Retained {excerpt.source.input_id} statements — v20260120</title>
<body>
<h1>{excerpt.heading}</h1>
<p>Copyright © RISC-V International.
Manual text by RISC-V International and the original RISC-V ISA manual authors.
The quoted statements are licensed under
<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.
Semulith adds this wrapper and retains only the named statements; all surrounding
text, diagrams and website assets are omitted. Each quoted span is unmodified.
No endorsement is implied.</p>
<p>Source: <a href="{SITE}{excerpt.source.file}">RISC-V Ratified Specifications Library,
v20260120, {excerpt.source.label}</a>.<br>
Original page SHA256: <code>{excerpt.source.sha256}</code>.<br>
Licence evidence: <a href="{SITE}{excerpt.licence.file}">{excerpt.licence.label}</a>,
whose statement also covers future manual versions.<br>
Licence-evidence page SHA256: <code>{excerpt.licence.sha256}</code>.<br>
Transformation: <code>scripts/retain_statements.py</code>.
{excerpt.scope_note}</p>
""".encode("utf-8")
    body = b"".join(f'<h2>{section}: <code>{name}</code></h2>\n<blockquote><p>'.encode("utf-8") + span
                    + b"</p></blockquote>\n" for name, section, span in spans)
    retained = header + body + b"</body></html>\n"
    require(len(retained) <= RETAINED_BYTES, "retained artifact exceeds bound")
    return retained


def read_pin(root, *, path, digest, limit, input_id):
    return A.read_snapshot(root, "input", dict(id=input_id, path=path, sha256=digest), max_bytes=limit)


def verify_retained(excerpt: Excerpt, root=ROOT):
    """Authenticate the curated input alone; no acquired source/cache access."""
    return read_pin(root, path=excerpt.retained_path, digest=excerpt.retained_sha256, limit=RETAINED_BYTES,
                    input_id=excerpt.input_id).pin


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--emit", metavar="INPUT_ID", choices=sorted(EXCERPTS),
                         help="print one retained artifact from the acquired pages")
    actions.add_argument("--verify", action="store_true", help="authenticate every tracked excerpt without the acquired pages")
    args = parser.parse_args(argv)
    if args.verify:
        worst = 0
        for excerpt in EXCERPTS.values():
            pin = verify_retained(excerpt)
            print(json.dumps(dict(id=excerpt.input_id, disposition=pin.disposition, reason=pin.reason, path=pin.path,
                                  byte_size=pin.byte_size, sha256=pin.sha256)))
            worst = max(worst, 0 if pin.disposition == "matched" else 2 if pin.disposition == "unavailable" else 1)
        return worst
    excerpt = EXCERPTS[args.emit]
    inputs = []
    for page, limit in ((excerpt.source, PAGE_BYTES), (excerpt.licence, LICENCE_BYTES)):
        snapshot = read_pin(ROOT, path=PAGES + page.file, digest=page.sha256, limit=limit, input_id=page.input_id)
        if snapshot.pin.disposition != "matched":
            print(json.dumps(dict(disposition=snapshot.pin.disposition, reason=snapshot.pin.reason)), file=sys.stderr)
            return 2 if snapshot.pin.disposition == "unavailable" else 1
        inputs.append(snapshot.data)
    try:
        output = retain_statements(excerpt, *inputs)
    except (RetentionError, UnicodeError) as exc:
        print(json.dumps(dict(disposition="refused", reason=str(exc))), file=sys.stderr)
        return 1
    sys.stdout.buffer.write(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
