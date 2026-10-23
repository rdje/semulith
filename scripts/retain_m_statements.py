#!/usr/bin/env python3
"""Retain the licensed, source-pinned M statements the m-forms properties cite, never the website shell.

The DIV/DIVU statement is retained by `scripts/retain_div_statement.py` (a42z) and pinned by the
retained case; this tool retains the other eleven normative statements of RVI-M §11.1.1–§11.1.2 and
Table 1 (division by zero and overflow) from the same pinned page, under the same licence evidence,
in one attributed wrapper. Emission is a bounded pure transformation plus explicit acquired-input
reads; verification authenticates only the retained file, without those acquired pages. Neither
operation is a comparison, capture, property binding, credit or qualification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import experiment_artifacts as A
import retain_div_statement as D  # the source and licence pins have one owner (a42z)

ROOT = Path(__file__).resolve().parent.parent
RETAINED_PATH = "profiles/rv64gc-lab-v0/retained/m-statements.html"
RETAINED_SHA = "bc777ebb97814f7361ececfa0dcfc16074374df2ddfeab71cf6684597681d518"  # 6,018 B, emitted 2026-10-23 (a42bb)
RETAINED_ID = "RVI-M-STATEMENTS"
RETAINED_BYTES = 8192
SPAN_BYTES = 1024
TABLE_BYTES = 4096
# Source order; norm:div_divu_op is the a42z excerpt and is not repeated here.
STATEMENTS = (
    ("norm:mul_op", "§11.1.1"), ("norm:mulh_mulhu_mulhsu_op", "§11.1.1"), ("norm:mulw_op", "§11.1.1"),
    ("norm:rem_remu_op", "§11.1.2"), ("norm:rem_result_sign", "§11.1.2"), ("norm:divw_divuw_op", "§11.1.2"),
    ("norm:remw_remuw_op", "§11.1.2"), ("norm:remw_remuw_result_sign", "§11.1.2"),
    ("norm:div_by_zero", "§11.1.2"), ("norm:rem_by_zero", "§11.1.2"), ("norm:signed_div_overflow", "§11.1.2"),
)
TABLE_MARKER = b'<table id="divby0" class="tableblock frame-all grid-all stretch">'
TABLE_CAPTION = b"Table 1. Semantics for division by zero and division overflow."
SPAN_TAGS = {b"code"}
TABLE_TAGS = {b"table", b"caption", b"colgroup", b"col", b"thead", b"tbody", b"tr", b"th", b"td",
              b"p", b"br", b"em", b"sup"}
TABLE_ATTRIBUTES = {b"class", b"id", b"style"}
STYLE = re.compile(rb'style="width: [0-9.]+%;"')


class RetentionError(ValueError):
    """No partial retained artifact escapes a refused source transformation."""


def require(condition, reason):
    if not condition:
        raise RetentionError(reason)


def _static(fragment: bytes, tags: set, attributes: set, what: str) -> None:
    """Only the reviewed static markup; anything executable or external refuses."""
    found = set(re.findall(rb"<([a-zA-Z0-9]+)", fragment))
    require(found <= tags, f"{what} carries unreviewed markup {sorted(t.decode() for t in found - tags)}")
    named = set(re.findall(rb"\s([a-zA-Z-]+)=", fragment))
    require(named <= attributes, f"{what} carries unreviewed attributes {sorted(a.decode() for a in named - attributes)}")
    for style in re.findall(rb'style="[^"]*"', fragment):
        require(STYLE.fullmatch(style) is not None, f"{what} carries an unreviewed style")


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
    require(b"<span" not in inner, f"{name}: nested span")
    _static(inner, SPAN_TAGS, set(), name)
    span.decode("utf-8")
    return span


def select_table(source: bytes) -> bytes:
    start = source.find(TABLE_MARKER)
    require(start >= 0, "Table 1 is absent")
    require(source.count(TABLE_MARKER) == 1, "Table 1 is duplicated")
    end = source.find(b"</table>", start)
    require(end >= 0, "Table 1 is unterminated")
    table = source[start: end + len(b"</table>")]
    require(len(table) <= TABLE_BYTES, "Table 1 exceeds bound")
    require(TABLE_CAPTION in table, "Table 1 caption differs")
    require(table.count(b"<table") == 1, "Table 1 nests a table")
    _static(table, TABLE_TAGS, TABLE_ATTRIBUTES, "Table 1")
    table.decode("utf-8")
    return table


def retain_statements(source: bytes, licence: bytes) -> bytes:
    """Copy eleven exact spans and one exact table after checking both complete, frozen primary inputs."""
    D.pinned(source, D.SOURCE_BYTES, D.SOURCE_SHA, "M source")
    D.pinned(licence, D.LICENCE_BYTES, D.LICENCE_SHA, "licence evidence")
    require(D.LICENCE_STATEMENT in licence, "reviewed licence statement is absent")
    spans = [(name, section, select_span(source, name)) for name, section in STATEMENTS]
    table = select_table(source)
    header = f"""<!doctype html>
<html lang="en"><meta charset="utf-8">
<title>Retained RVI-M statements and Table 1 — v20260120</title>
<body>
<h1>RVI-M §11.1.1–§11.1.2: multiplication, division and remainder statements; Table 1</h1>
<p>Copyright © RISC-V International.
Manual text by RISC-V International and the original RISC-V ISA manual authors.
The quoted statements and table are licensed under
<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.
Semulith adds this wrapper and retains only the named statements and Table 1; all
surrounding text, diagrams and website assets are omitted. Each quoted span and the
table are unmodified. No endorsement is implied.</p>
<p>Source: <a href="{D.SOURCE_URL}">RISC-V Ratified Specifications Library,
v20260120, M extension Version 2.0, §11.1</a>.<br>
Original page SHA256: <code>{D.SOURCE_SHA}</code>.<br>
Licence evidence: <a href="{D.LICENCE_URL}">unprivileged preface to Version 2.2</a>,
whose statement also covers future manual versions.<br>
Licence-evidence page SHA256: <code>{D.LICENCE_SHA}</code>.<br>
Transformation: <code>scripts/retain_m_statements.py</code>, reviewed 2026-10-23.
The DIV/DIVU statement is retained separately (<code>retained/div-statement.html</code>).
This excerpt establishes no M acceptance.</p>
""".encode("utf-8")
    body = b"".join(f'<h2>{section}: <code>{name}</code></h2>\n<blockquote><p>'.encode("utf-8") + span
                    + b"</p></blockquote>\n" for name, section, span in spans)
    body += b"<h2>\xc2\xa711.1.2: Table 1</h2>\n" + table + b"\n"
    retained = header + body + b"</body></html>\n"
    require(len(retained) <= RETAINED_BYTES, "retained artifact exceeds bound")
    return retained


def read_pin(root, *, path, digest, limit, input_id):
    return A.read_snapshot(root, "input", dict(id=input_id, path=path, sha256=digest), max_bytes=limit)


def verify_retained(root=ROOT):
    """Authenticate the curated input alone; no acquired source/cache access."""
    return read_pin(root, path=RETAINED_PATH, digest=RETAINED_SHA, limit=RETAINED_BYTES,
                    input_id=RETAINED_ID).pin


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--emit", action="store_true", help="print the retained artifact from the acquired pages")
    actions.add_argument("--verify", action="store_true", help="authenticate the tracked artifact without the acquired pages")
    args = parser.parse_args(argv)
    if args.verify:
        pin = verify_retained()
        print(json.dumps(dict(disposition=pin.disposition, reason=pin.reason, path=pin.path,
                              byte_size=pin.byte_size, sha256=pin.sha256)))
        return 0 if pin.disposition == "matched" else 2 if pin.disposition == "unavailable" else 1
    inputs = []
    for path, digest, limit, input_id in ((D.SOURCE_PATH, D.SOURCE_SHA, D.SOURCE_BYTES, "RVI-M"),
                                          (D.LICENCE_PATH, D.LICENCE_SHA, D.LICENCE_BYTES, "RVI-UNPRIV-LICENCE")):
        snapshot = read_pin(ROOT, path=path, digest=digest, limit=limit, input_id=input_id)
        if snapshot.pin.disposition != "matched":
            print(json.dumps(dict(disposition=snapshot.pin.disposition, reason=snapshot.pin.reason)), file=sys.stderr)
            return 2 if snapshot.pin.disposition == "unavailable" else 1
        inputs.append(snapshot.data)
    try:
        output = retain_statements(*inputs)
    except (RetentionError, UnicodeError) as exc:
        print(json.dumps(dict(disposition="refused", reason=str(exc))), file=sys.stderr)
        return 1
    sys.stdout.buffer.write(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
