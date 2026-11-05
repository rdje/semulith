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
PAGE_BYTES = 524288  # the longest pinned page a row names: priv/machine.html, 271,851 B
LICENCE_BYTES = 131072
RETAINED_BYTES = 8192
SPAN_BYTES = 1024
OPENING = "opening:"
PARAGRAPH = b'<div class="paragraph">\n<p>'
PARAGRAPH_END = b"</p>\n</div>"
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
UNPRIVILEGED_LICENCE = Page("RVI-LICENCE", "unpriv/colophon.html",
                            "7f48c2cb52c7d325520b00a02153222492bd5c4ffa0ae02adecda7ecc4c2a25c",
                            "the unprivileged volume's preface")
EXCERPTS = {
    "RVP-CSR-STATEMENTS": Excerpt(
        "RVP-CSR-STATEMENTS", "RVP-CSR §1.1.1: which privilege may access a CSR, and what an attempt without it does",
        Page("RVP-CSR", "priv/priv-csrs.html", "330a17314ef803231955a915748176e5175fc773469f25a8c6b5ae922c9df425",
             "RISC-V Privileged Architecture, §1.1 Control and Status Registers (CSRs)"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-csr-statements.html", "0f2d75c5e8fb85505577c62320d035680704d9afeb8aae0e978174edbc63aba6",
        (("norm:Zicsr_higher_priv", "§1.1.1"), ("norm:Zicsr_rw", "§1.1.1"), ("norm:Zicsr_access", "§1.1.1"),
         ("norm:Zicsr_illegal_mode", "§1.1.1"), ("norm:Zicsr_illegal_acc", "§1.1.1")),
        "This excerpt establishes no CSR-SET acceptance."),
    "RVI-ZICNTR-STATEMENTS": Excerpt(
        "RVI-ZICNTR-STATEMENTS", "RVI-ZICNTR §6.1: the counters are read-only CSRs, and what each of the base three counts",
        Page("RVI-ZICNTR", "unpriv/counters.html", "8d619d6ef71d6cd87415342782aa615a0aff121a537342e4497658947f4fa81c",
             "RISC-V Unprivileged Architecture, §6.1 \"Zicntr\" and \"Zihpm\" Extensions for Counters, Version 2.0"),
        UNPRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvi-zicntr-statements.html", "ee5bca84e2b9cc3be2c797535adcf701892967687e379c5d4df3738e7e4aad49",
        (("norm:zihpm_op_sz_mode_acc_count", "§6.1"), ("norm:zihpm_op_sz_mode_acc_priv", "§6.1"),
         ("norm:zihpm_op_sz_mode_acc_partition", "§6.1"), ("norm:zicntr_rdcycle_op", "§6.1.1"),
         ("norm:zicntr_rdtime_op", "§6.1.1"), ("norm:zicntr_rdinstret_op", "§6.1.1")),
        "This excerpt establishes no ZICNTR acceptance."),
    "RVP-COUNTEREN-STATEMENTS": Excerpt(
        "RVP-COUNTEREN-STATEMENTS", "RVP-MACHINE §2.1.1.11: what mcounteren gates, and what a read it refuses does",
        Page("RVP-MACHINE", "priv/machine.html", "b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea",
             "RISC-V Privileged Architecture, §2.1 Machine-Level ISA, Version 1.13"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-counteren-statements.html", "a47ba18329dd6d7d4079f2f37c96619a8cb4347b4e973d37cc80e10ede27890a",
        (("norm:mcounteren_op", "§2.1.1.11"), ("norm:mcounteren_inc_inaccessible", "§2.1.1.11"),
         ("norm:mcounteren_clr_ill_inst_exc", "§2.1.1.11"), ("norm:mcounteren_set_nxt_priv", "§2.1.1.11")),
        "This excerpt establishes no ZICNTR acceptance; the scounteren statement has no anchor to select in its own page, so it is cited, not retained."),
    "RVP-SSTC-STATEMENTS": Excerpt(
        "RVP-SSTC-STATEMENTS", "RVP-SSTC §12.1: why supervisor mode has its own timer, and what the extension adds",
        Page("RVP-SSTC", "priv/sstc.html", "30bea862eee800d485ce34636b2824bf9909a4676b39d2c5734e92fba14216e1",
             "RISC-V Privileged Architecture, §12.1 \"Sstc\" Extension for Supervisor-mode Timer Interrupts, Version 1.0"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-sstc-statements.html", "8032b3fff7e2861adf58a2965f5cca55025242b9ae46f3f034c24677cbf3e7a6",
        (("opening:This extension serves", "§12.1"), ("opening:The extension name is", "§12.1")),
        "This excerpt establishes no SSTC acceptance; the chapter anchors none of its text, so each paragraph is selected by the words it opens with."),
    "RVP-STIMECMP-STATEMENTS": Excerpt(
        "RVP-STIMECMP-STATEMENTS", "RVP-SUPERVISOR §11.1.1.3 and §11.1.1.12: when a supervisor interrupt traps, and what stimecmp makes pending",
        Page("RVP-SUPERVISOR", "priv/supervisor.html", "d5186efc3ead1c1f693ac2b16aeccdcab95d990264f49b559252d2dc413a651a",
             "RISC-V Privileged Architecture, §11.1 Supervisor-Level ISA, Version 1.13"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-stimecmp-statements.html", "7f2362b1cc60afb3281c82e50e244b6dd4b971e13eae25c0aac46e3601d3b6e3",
        (("norm:sie_sip_supervisor_strap", "§11.1.1.3"), ("norm:sie_sip_strap_time_constraint", "§11.1.1.3"),
         ("norm:sip-stip_sie-stie", "§11.1.1.3"), ("norm:stimecmp-stimecmph_sz_acc", "§11.1.1.12"), ("norm:mip_sip-stip_op", "§11.1.1.12")),
        "This excerpt establishes no SSTC acceptance."),
    "RVP-STCE-STATEMENTS": Excerpt(
        "RVP-STCE-STATEMENTS", "RVP-MACHINE §2.1.1.9 and §2.1.1.18: how stimecmp drives STIP, and what menvcfg.STCE gates",
        Page("RVP-MACHINE", "priv/machine.html", "b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea",
             "RISC-V Privileged Architecture, §2.1 Machine-Level ISA, Version 1.13"),
        PRIVILEGED_LICENCE, "profiles/rv64gc-lab-v0/retained/rvp-stce-statements.html", "dd8a425e87b394c6bc655c98724debc3875f690c903685f8a3f84eb504306c15",
        (("norm:mip_stip_stimecmp_acc", "§2.1.1.9"), ("norm:mip_stip_stimecmp_op2", "§2.1.1.9"), ("norm:mip_stip_stimecmp_clr", "§2.1.1.9"),
         ("norm:menvcfg_stce_op1", "§2.1.1.18"), ("norm:menvcfg_stce_op2", "§2.1.1.18")),
        "This excerpt establishes no SSTC acceptance."),
}


class RetentionError(ValueError):
    """No partial retained artifact escapes a refused source transformation."""


def require(condition, reason):
    if not condition:
        raise RetentionError(reason)


def pinned(data, limit, digest, name):
    require(type(data) is bytes and 1 <= len(data) <= limit, name + " byte bound/type")
    require(hashlib.sha256(data).hexdigest() == digest, name + " pin differs")


def statement_marks(source: bytes, name: str) -> tuple[bytes, bytes, bytes]:
    """What opens and closes a row's statement, and what opens its quoted bytes.

    A statement is a span by its anchor, as most are. The manual also anchors a whole paragraph, and the Sstc chapter anchors nothing, so `opening:<words>`
    selects the one paragraph that opens with exactly those words. A span is quoted with its own tags; a paragraph is quoted from inside its `<p>`.
    """
    if name.startswith(OPENING):
        words = name[len(OPENING):].encode()
        return PARAGRAPH + words, PARAGRAPH_END, words
    span, anchored = b'<span id="' + name.encode() + b'">', b'<div id="' + name.encode() + b'" class="paragraph">\n<p>'
    if span not in source and anchored in source:
        return anchored, PARAGRAPH_END, b""
    return span, b"</span>", span


def select_span(source: bytes, name: str) -> bytes:
    marker, closing, quoted = statement_marks(source, name)
    start = source.find(marker)
    require(start >= 0, f"{name}: statement is absent")
    require(source.count(marker) == 1, f"{name}: statement is duplicated")
    end = source.find(closing, start + len(marker))
    require(end >= 0, f"{name}: statement is unterminated")
    first = start + len(marker) - len(quoted)
    tagged = closing == b"</span>"
    span = source[first: end + len(closing)] if tagged else source[first: end]
    require(len(span) <= SPAN_BYTES, f"{name}: statement exceeds bound")
    inner = span[len(marker): -len(closing)] if tagged else span
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
