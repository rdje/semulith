#!/usr/bin/env python3
"""Shared-reader refusal and optimization controls; fixtures stay on-volume."""
from __future__ import annotations

import argparse
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import sexp as S

ROOT = Path(__file__).resolve().parent.parent


class ReaderTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / "target/p4-system-14/a35/reader-fixtures"
        base.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def refusal(self, text, needle):
        try:
            S.parse(text, "fixture.sexp")
        except S.SexpError as exc:
            self.assertIn(needle, str(exc))
            return str(exc)
        except (ValueError, OSError, UnicodeError) as exc:
            self.fail(f"expected named parser refusal, got {type(exc).__name__}")
        self.fail("invalid integer accepted")

    def cli(self, path, rc, needle):
        out, err = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                got = S.main(["sexp.py", str(path)])
        except (S.SexpError, ValueError, OSError, UnicodeError) as exc:
            self.fail(f"expected CLI refusal, escaped {type(exc).__name__}")
        self.assertEqual(got, rc)
        self.assertIn(needle, err.getvalue() if rc else out.getvalue())
        self.assertNotIn("Traceback", err.getvalue())
        if rc:
            self.assertEqual(out.getvalue(), "")
        else:
            self.assertEqual(err.getvalue(), "")

    def test_hex_without_digits(self):
        self.refusal("(n 0x_)", "unreadable base-16 integer")

    def test_binary_without_digits(self):
        self.refusal("(n -0b___)", "unreadable base-2 integer")

    def test_host_decimal_limit(self):
        original = sys.get_int_max_str_digits()
        limit = sys.int_info.str_digits_check_threshold
        try:
            # Exercise a real conversion refusal even when the caller disabled its limit.
            sys.set_int_max_str_digits(limit)
            text = "7" * (limit + 1)
            reason = self.refusal("(n\n " + text + ")", "fixture.sexp:2:")
            self.assertIn(f"({len(text)} characters)", reason)
            self.assertLess(len(reason), 160)
            self.assertNotIn("7" * 32, reason)
            self.assertEqual(sys.get_int_max_str_digits(), limit)
        finally:
            sys.set_int_max_str_digits(original)
        self.assertEqual(sys.get_int_max_str_digits(), original)

    def test_conversion_valueerror_independent_of_host_limit(self):
        with patch.object(S, "int", side_effect=ValueError("conversion failed"), create=True):
            self.refusal("(n 12)", "unreadable base-10 integer")

    def test_valid_integer_spellings(self):
        self.assertEqual(S.parse("(n +12 -3 +0X_1_f_ -0B_1_0_ ٠١٢)"),
                         [["n", 12, -3, 31, -2, 12]])

    def test_large_power_of_two_integers(self):
        self.assertEqual(S.parse("(n 0x" + "f" * 5000 + ")")[0][1], (1 << 20000) - 1)
        self.assertEqual(S.parse("(n 0b" + "1" * 5000 + ")")[0][1], (1 << 5000) - 1)

    def test_symbols_and_strings_unchanged(self):
        got = S.parse('(n 0x 0xg 0b2 1_2 "12" sym)')[0][1:]
        self.assertEqual(got, ["0x", "0xg", "0b2", "1_2", "12", "sym"])
        self.assertEqual([isinstance(x, S.Symbol) for x in got], [True] * 4 + [False, True])

    def test_atom_two_argument_consumers(self):
        self.assertEqual(S._atom("0x10", 0), 16)

    def test_spans_still_validate_and_preserve_text(self):
        text = '; preface\n(n 12) "§;x"'
        spans = S.forms_with_spans(text)
        self.assertEqual([text[a:b] for _, a, b in spans], ['(n 12)', '"§;x"'])
        try:
            S.forms_with_spans("(n 0x_)")
        except S.SexpError:
            pass
        except ValueError:
            self.fail("span validation leaked an integer conversion error")
        else:
            self.fail("span validation accepted an unreadable integer")

    def test_cli_success(self):
        path = self.root / "good.sexp"
        path.write_text('(z) (a) (a) "literal" 12\n')
        self.cli(path, 0, "ok: 5 top-level form(s); heads: a, z\n")

    def test_cli_empty_list(self):
        path = self.root / "empty.sexp"; path.write_text("()")
        self.cli(path, 1, "REFUSED:")

    def test_cli_nested_head(self):
        path = self.root / "head.sexp"; path.write_text("((a))")
        self.cli(path, 1, "expected a list beginning with a symbol")

    def test_cli_malformed_integer(self):
        path = self.root / "integer.sexp"; path.write_text("(n 0x_)")
        self.cli(path, 1, "unreadable base-16 integer")

    def test_cli_large_hex_head(self):
        path = self.root / "hex-head.sexp"
        path.write_text("(0x" + "f" * 5000 + ")")
        self.cli(path, 1, "list beginning with int")

    def test_head_large_integer(self):
        try:
            S.head([1 << 20000], "fixture.sexp")
        except S.SexpError as exc:
            self.assertIn("list beginning with int", str(exc))
        except ValueError:
            self.fail("head diagnostic leaked integer display error")
        else:
            self.fail("integer list head accepted")

    def test_head_diagnostic_bounded(self):
        try:
            S.head([[], *range(10000)], "fixture.sexp")
        except S.SexpError as exc:
            self.assertLess(len(str(exc)), 160)
            self.assertIn("list beginning with list", str(exc))
        else:
            self.fail("nested list head accepted")

    def test_cli_missing_file(self):
        self.cli(self.root / "missing.sexp", 1, "REFUSED:")

    def test_cli_directory(self):
        self.cli(self.root, 1, "REFUSED:")

    def test_cli_invalid_encoding(self):
        path = self.root / "invalid.sexp"; path.write_bytes(b"\xff")
        self.cli(path, 1, "REFUSED:")

    def test_cli_other_os_error(self):
        with patch.object(S.Path, "read_text", side_effect=PermissionError("denied")):
            self.cli(self.root / "denied.sexp", 1, "denied")

    def test_cli_unicode_error(self):
        with patch.object(S.Path, "read_text", side_effect=UnicodeError("cannot decode")):
            self.cli(self.root / "decode.sexp", 1, "cannot decode")

    def test_library_io_contract(self):
        with self.assertRaises(FileNotFoundError):
            S.read_file(self.root / "missing.sexp")
        with patch.object(S.Path, "read_text", side_effect=UnicodeError("decode")):
            with self.assertRaises(UnicodeError):
                S.read_file(self.root / "decode.sexp")

    def test_usage(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(S.main(["sexp.py"]), 2)

    def selftest(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return S._selftest()

    def test_selftest_healthy(self):
        self.assertEqual(self.selftest(), 0)

    def test_selftest_rejects_wrong_integer(self):
        atom = S._atom
        def wrong(text, line, where="<sexp>"):
            return 13 if text == "12" else atom(text, line, where)
        with patch.object(S, "_atom", wrong):
            self.assertEqual(self.selftest(), 1)

    def test_equality_guard(self):
        with self.assertRaises(AssertionError):
            S._eq(12, 13)

    def test_selftest_rejects_extra_form(self):
        parse = S.parse
        def extra(text, where="<sexp>"):
            forms = parse(text, where)
            return forms + [S.Symbol("extra")] if text.startswith("(n 12") else forms
        with patch.object(S, "parse", extra):
            self.assertEqual(self.selftest(), 1)

    def test_selftest_rejects_wrong_refusal_reason(self):
        parse = S.parse
        def wrong(text, where="<sexp>"):
            if text == "(x))":
                raise S.SexpError("unrelated error")
            return parse(text, where)
        with patch.object(S, "parse", wrong):
            self.assertEqual(self.selftest(), 1)

    def test_accessor_reason_guard(self):
        def wrong():
            raise S.SexpError("unrelated error")
        with self.assertRaises(AssertionError):
            S._raises(wrong, "duplicate")


MUTATIONS = {
    "integer-refusal": ("except ValueError as exc:", "except OverflowError as exc:"),
    "cli-head": ('        heads = sorted({head(f, argv[1]) for f in forms if isinstance(f, list)})\n', ''),
    "head-diagnostic": ('got {shape}', 'got {form!r}'),
    "cli-io": ("(SexpError, OSError, UnicodeError)", "(SexpError, UnicodeError)"),
    "cli-decode": ("(SexpError, OSError, UnicodeError)", "(SexpError, OSError)"),
    "selftest-equality": ("    if got != want:", "    if False:"),
    "selftest-arity": ("        if len(forms) != 1:", "        if False:"),
    "selftest-reason": ("if needle not in str(exc):", "if False:"),
}


def main():
    global S
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        source = Path(S.__file__).read_text()
        before, after = MUTATIONS[args.mutation]
        expected = 2 if args.mutation == "selftest-reason" else 1
        if source.count(before) != expected:
            raise RuntimeError("mutation site count changed")
        source = source.replace(before, after)
        if args.mutation == "cli-head":
            source = source.replace('    print(f"ok: {len(forms)}',
                                    before[4:] + '    print(f"ok: {len(forms)}', 1)
        module = types.ModuleType("sexp_mutant"); module.__file__ = S.__file__
        exec(compile(source, S.__file__, "exec"), module.__dict__)
        S = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(ReaderTests))
    print(f"SEXP-REFUSALS: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; fixtures cleaned")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
