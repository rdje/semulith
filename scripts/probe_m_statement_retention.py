#!/usr/bin/env python3
"""Cache-free synthetic controls for the retained M statements and Table 1 (a42bb)."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import retain_div_statement as D
import retain_m_statements as R

ROOT = Path(__file__).resolve().parent.parent
MUTATIONS = {
    "input-pins": ('    D.pinned(source, D.SOURCE_BYTES, D.SOURCE_SHA, "M source")\n', ''),
    "licence-statement": ('require(D.LICENCE_STATEMENT in licence, ', 'require(True, '),
    "unique-statement": ('require(source.count(marker) == 1, ', 'require(True, '),
    "closing-span": ('require(end >= 0, f"{name}: statement is unterminated")', 'require(True, f"{name}: statement is unterminated")'),
    "span-markup": ('    _static(inner, SPAN_TAGS, set(), name)\n', ''),
    "table-markup": ('    _static(table, TABLE_TAGS, TABLE_ATTRIBUTES, "Table 1")\n', ''),
    "style-shape": ('STYLE.fullmatch(style) is not None', 'True'),
    "table-caption": ('require(TABLE_CAPTION in table, ', 'require(True, '),
    "retained-bound": ('require(len(retained) <= RETAINED_BYTES, ', 'require(True, '),
    "retained-pin": ("digest=RETAINED_SHA", "digest=D.SOURCE_SHA"),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def span(name, text=b"synthetic <code>rs1</code> statement, unchanged whitespace\n"):
    return b'<span id="' + name.encode() + b'">' + text + b"</span>"


TABLE = (R.TABLE_MARKER + b"\n<caption class=\"title\">" + R.TABLE_CAPTION + b" L is the width.</caption>\n"
         b'<colgroup>\n<col style="width: 25%;">\n</colgroup>\n<tbody>\n<tr>\n<td class="tableblock">'
         b'<p class="tableblock"><em>x</em><br>\n-2<sup>L-1</sup></p></td>\n</tr>\n</tbody>\n</table>')


class RetentionTests(unittest.TestCase):
    def setUp(self):
        self.spans = {name: span(name) for name, _ in R.STATEMENTS}
        self.build()
        self.licence = b"synthetic preface before\n" + D.LICENCE_STATEMENT + b"\nafter"
        self.pin()

    def build(self, *, spans=None, table=TABLE, extra=b""):
        spans = self.spans if spans is None else spans
        self.source = (b"<script>excluded()</script>before" + span("norm:div_divu_op")
                       + b"between".join(spans.values()) + b"<nav>excluded</nav>" + table + extra + b"after")

    def pin(self):
        for name, value in (("SOURCE_SHA", sha(self.source)), ("LICENCE_SHA", sha(self.licence))):
            context = patch.object(D, name, value)
            context.start()
            self.addCleanup(context.stop)

    def emit(self):
        return R.retain_statements(self.source, self.licence)

    def rebuilt_emit(self, **kwargs):
        self.build(**kwargs)
        with patch.object(D, "SOURCE_SHA", sha(self.source)):
            return R.retain_statements(self.source, self.licence)

    def temporary_root(self):
        base = ROOT / "target/m-statement-retention-controls"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def install(self, root, data):
        path = root / R.RETAINED_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def test_exact_quotes_and_table_without_unselected_site_bytes(self):
        out = self.emit()
        for name, quoted in self.spans.items():
            self.assertEqual(out.count(quoted), 1, name)
        self.assertEqual(out.count(TABLE), 1)
        for excluded in (b"<script", b"excluded()", b"<nav", b"between", b"before", b"after<"):
            self.assertNotIn(excluded, out)

    def test_div_statement_is_not_repeated(self):
        self.assertNotIn(b'id="norm:div_divu_op"', self.emit())
        self.assertIn(b"retained/div-statement.html", self.emit())

    def test_attribution_and_both_original_identities(self):
        out = self.emit().decode()
        for needle in ("CC BY 4.0", "Copyright © RISC-V International", D.SOURCE_SHA, D.LICENCE_SHA,
                       "scripts/retain_m_statements.py", "establishes no M acceptance"):
            self.assertIn(needle, out)

    def test_output_is_deterministic(self):
        self.assertEqual(self.emit(), self.emit())

    def test_source_change_refuses(self):
        with self.assertRaises(D.RetentionError):
            R.retain_statements(self.source + b"x", self.licence)

    def test_missing_licence_statement_refuses_even_with_fixture_pin(self):
        licence = b"synthetic preface without the statement"
        with patch.object(D, "LICENCE_SHA", sha(licence)), self.assertRaises(R.RetentionError):
            R.retain_statements(self.source, licence)

    def test_each_missing_statement_refuses(self):
        for name in self.spans:
            with self.subTest(name=name), self.assertRaises(R.RetentionError):
                self.rebuilt_emit(spans={k: v for k, v in self.spans.items() if k != name})

    def test_duplicate_statement_refuses(self):
        name = R.STATEMENTS[0][0]
        with self.assertRaises(R.RetentionError):
            self.rebuilt_emit(extra=span(name))

    def test_unterminated_statement_refuses(self):
        """The last statement in source order with no closing span anywhere after it."""
        name = R.STATEMENTS[-1][0]
        spans = dict(self.spans); spans[name] = b'<span id="' + name.encode() + b'">no end'
        with self.assertRaises(R.RetentionError):
            self.rebuilt_emit(spans=spans)

    def test_span_bound_is_inclusive(self):
        name = R.STATEMENTS[0][0]
        overhead = len(span(name, b""))
        fits = dict(self.spans); fits[name] = span(name, b"x" * (R.SPAN_BYTES - overhead))
        self.assertIn(fits[name], self.rebuilt_emit(spans=fits))
        over = dict(self.spans); over[name] = span(name, b"x" * (R.SPAN_BYTES - overhead + 1))
        with self.assertRaises(R.RetentionError):
            self.rebuilt_emit(spans=over)

    def test_unreviewed_markup_in_a_statement_refuses(self):
        name = R.STATEMENTS[1][0]
        for bad in (b'<a href="https://example.invalid">x</a>', b"<script>x()</script>", b"<img src=x>"):
            spans = dict(self.spans); spans[name] = span(name, bad)
            with self.subTest(bad=bad), self.assertRaises(R.RetentionError):
                self.rebuilt_emit(spans=spans)

    def test_table_missing_duplicated_or_unterminated_refuses(self):
        for table, extra in ((b"", b""), (TABLE, TABLE), (TABLE[: TABLE.rfind(b"</table>")], b"")):
            with self.subTest(table=len(table), extra=len(extra)), self.assertRaises(R.RetentionError):
                self.rebuilt_emit(table=table, extra=extra)

    def test_table_unreviewed_markup_or_style_refuses(self):
        for bad in (b"<script>x()</script>", b'<td onclick="x()">', b'<a href="x">y</a>', b'<col style="background: url(x)">'):
            table = TABLE.replace(b"</tbody>", bad + b"</tbody>")
            with self.subTest(bad=bad), self.assertRaises(R.RetentionError):
                self.rebuilt_emit(table=table)

    def test_table_caption_must_match(self):
        with self.assertRaises(R.RetentionError):
            self.rebuilt_emit(table=TABLE.replace(R.TABLE_CAPTION, b"Table 1. Something else."))

    def test_retained_bound_is_inclusive(self):
        size = len(self.emit())
        with patch.object(R, "RETAINED_BYTES", size):
            self.assertEqual(len(self.emit()), size)
        with patch.object(R, "RETAINED_BYTES", size - 1), self.assertRaises(R.RetentionError):
            self.emit()

    def test_verification_needs_no_acquired_pages(self):
        root = self.temporary_root()
        data = self.emit()
        self.install(root, data)
        self.assertFalse((root / ".materials").exists())
        with patch.object(R, "RETAINED_SHA", sha(data)):
            pin = R.verify_retained(root)
        self.assertEqual((pin.disposition, pin.byte_size, pin.sha256), ("matched", len(data), sha(data)))

    def test_retained_change_is_not_success(self):
        root = self.temporary_root()
        data = self.emit()
        self.install(root, data + b"changed")
        with patch.object(R, "RETAINED_SHA", sha(data)):
            self.assertEqual(R.verify_retained(root).disposition, "mismatch")

    def test_retained_missing_is_unavailable(self):
        self.assertEqual(R.verify_retained(self.temporary_root()).disposition, "unavailable")

    def test_retained_symlink_refuses(self):
        root = self.temporary_root()
        path = self.install(root, self.emit())
        path.rename(path.with_suffix(".other"))
        path.symlink_to(path.with_suffix(".other").name)
        self.assertEqual(R.verify_retained(root).disposition, "refused")

    def test_real_tree_retained_file_verifies_offline(self):
        """The tracked excerpt authenticates by its pinned digest with no acquired page."""
        pin = R.verify_retained(ROOT)
        self.assertEqual(pin.disposition, "matched", pin.reason)
        self.assertEqual(pin.sha256, R.RETAINED_SHA)


def main():
    global R
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=sorted(MUTATIONS))
    args = parser.parse_args()
    if args.mutation:
        path = ROOT / "scripts/retain_m_statements.py"
        source = path.read_text()
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise RuntimeError("mutation no longer selects exactly one guard")
        module = types.ModuleType("mutated_m_statements")
        module.__file__ = str(path)
        exec(compile(source.replace(before, after), str(path), "exec"), module.__dict__)
        R = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(RetentionTests))
    print(f"M-STATEMENT-RETENTION: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; synthetic curation controls, no capture credit")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
