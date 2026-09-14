#!/usr/bin/env python3
"""A minimal S-expression reader for this project's canonical-definition files.

WHY S-EXPRESSIONS, AND WHY FOR EVERY SOURCE OF TRUTH. An earlier decision split the formats per
file — S-expressions for encodings and semantics, JSON and TOML for records — on the grounds that
records are not trees. True about shape, and the wrong question. `SOT-FORMAT` supersedes it:
composition is a MERGE, and three formats are three merge semantics, so under the split a board
composing two processors could union their encodings and nothing else. One format, one merge rule,
and a construct vocabulary extended by data rather than by editing this file.

⛔ THE READER REFUSES RATHER THAN GUESSES, which is the same soundness property the JSON Schema
validator carries: a parser that silently accepts something it does not understand hands the
caller a structure that does not mean what the file says. Unterminated lists, stray closing
parens, unterminated strings and unreadable atoms are all errors, never best-effort recoveries.

⚠️ HONEST LIMIT, stated rather than implied: this is not a Lisp. There are no quotes, no dotted
pairs, no reader macros and no evaluation. It reads nested lists of atoms, and an atom is an
integer, a string, or a symbol. That is the whole language, and it is deliberately small enough
that a reader can be sure what a file means by reading this file.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

Atom = int | str
Sexp = Atom | list["Sexp"]

class SexpError(Exception):
    """A refusal. A malformed file is never read as a partially-good one."""


class Symbol(str):
    """A bare symbol, distinguished from a quoted string so a writer can round-trip it."""
    __slots__ = ()


# ⛔ THE ESCAPE TABLE IS CLOSED, AND DECODED HERE RATHER THAN BY A CODEC. The first version of
# this reader collected escape pairs raw and then ran the assembled string through
# `.encode().decode("unicode_escape")`. That codec is Latin-1: it reads the two UTF-8 bytes of
# `§` as two separate characters, so every `§` became `Â§` and every `—` became three
# characters of noise. It corrupted all 52 specification citations in this project's own
# semantics fragment, silently, because nothing compared the string it produced against the
# string the file contained. A file is UTF-8; a non-ASCII character needs no escape at all.
_ESCAPES = {'"': '"', '\\': '\\', 'n': '\n', 't': '\t', 'r': '\r'}


def _atom(text: str, line: int) -> Atom:
    if re.fullmatch(r"[+-]?\d+", text):
        return int(text)
    if re.fullmatch(r"[+-]?0[xX][0-9a-fA-F_]+", text):
        return int(text.replace("_", ""), 16)
    if re.fullmatch(r"[+-]?0[bB][01_]+", text):
        return int(text.replace("_", ""), 2)
    return Symbol(text)


def parse(text: str, where: str = "<sexp>") -> list[Sexp]:
    """Parse a whole file into a list of top-level forms.

    ⛔ SCANNED AS ONE STREAM, not line by line. A first cut stripped `;` comments per line before
    tokenizing, which is wrong in two ways that a reader would meet immediately: a `;` INSIDE a
    string truncated the string, and a string could not span lines. Generating this project's own
    `encoding.sexp` hit the second within minutes. Comments and strings have to be recognised by
    the same pass, because whether a `;` starts a comment depends on whether a string is open.
    """
    stack: list[list[Sexp]] = [[]]
    open_at: list[int] = [0]
    i, line, n = 0, 1, len(text)
    while i < n:
        ch = text[i]
        if ch == "\n":
            line += 1; i += 1; continue
        if ch.isspace():
            i += 1; continue
        if ch == ";":                                  # comment to end of line
            while i < n and text[i] != "\n":
                i += 1
            continue
        if ch == "(":
            stack.append([]); open_at.append(line); i += 1; continue
        if ch == ")":
            if len(stack) == 1:
                raise SexpError(f"{where}:{line}: ')' with no matching '('")
            done = stack.pop(); open_at.pop(); stack[-1].append(done); i += 1; continue
        if ch == '"':
            j, buf = i + 1, []
            while j < n and text[j] != '"':
                c = text[j]
                if c == "\\":
                    if j + 1 >= n:
                        raise SexpError(f"{where}:{line}: unterminated escape at end of input")
                    esc = text[j + 1]
                    if esc not in _ESCAPES:
                        raise SexpError(f"{where}:{line}: unknown escape '\\{esc}' in string. The "
                                        f"reader refuses rather than guessing what it was meant "
                                        f"to be; write the character itself, or use one of: "
                                        f"{' '.join(sorted(_ESCAPES))}")
                    buf.append(_ESCAPES[esc]); j += 2; continue
                if c == "\n":
                    line += 1
                buf.append(c); j += 1
            if j >= n:
                raise SexpError(f"{where}:{line}: unterminated string")
            stack[-1].append("".join(buf))
            i = j + 1; continue
        j = i
        while j < n and not text[j].isspace() and text[j] not in '()";':
            j += 1
        if j == i:
            raise SexpError(f"{where}:{line}: cannot read {ch!r}")
        stack[-1].append(_atom(text[i:j], line))
        i = j
    if len(stack) != 1:
        raise SexpError(f"{where}: {len(stack) - 1} unterminated list(s); the outermost opened "
                        f"on line {open_at[1]}")
    return stack[0]


def read_file(path: Path) -> list[Sexp]:
    return parse(path.read_text(), str(path))


# ---------------------------------------------------------------------------------------
# Small, explicit accessors. A canonical-definition file is read through these rather than by
# indexing, so a shape change is an error with a name instead of an IndexError somewhere later.
# ---------------------------------------------------------------------------------------
def head(form: Sexp, where: str = "") -> str:
    if not isinstance(form, list) or not form or not isinstance(form[0], str):
        raise SexpError(f"{where}: expected a list beginning with a symbol, got {form!r}")
    return str(form[0])


def children(form: Sexp, name: str) -> list[Sexp]:
    """Every direct child list whose head is `name`."""
    if not isinstance(form, list):
        raise SexpError(f"expected a list, got {form!r}")
    return [c for c in form if isinstance(c, list) and c and c[0] == name]


def field(form: Sexp, name: str, where: str = "") -> Sexp:
    """The single value of `(name value)`, refusing absence and duplication alike."""
    found = children(form, name)
    if len(found) != 1:
        raise SexpError(f"{where}: expected exactly one ({name} …), found {len(found)}")
    if len(found[0]) != 2:
        raise SexpError(f"{where}: ({name} …) must carry exactly one value, got {found[0]!r}")
    return found[0][1]



# ---------------------------------------------------------------------------------------
# Self-test. ⛔ THE READER HAD NONE, and shipped a defect that corrupted every non-ASCII
# character in every string it read — 52 specification citations in this project's own
# semantics fragment, each one the link between an expression and the sentence it came from.
# The files on disk were always right; the reader mangled them on the way in, and no tool
# downstream compared what it got against what the file said. An instrument with no arms is
# an assertion.
# ---------------------------------------------------------------------------------------
def _selftest() -> int:
    passed = failed = 0

    def arm(label: str, fn) -> None:
        nonlocal passed, failed
        try:
            fn()
        except AssertionError as exc:
            print(f"  FAIL  {label}: {exc}"); failed += 1
        except Exception as exc:                       # noqa: BLE001 — an arm must not abort the run
            print(f"  FAIL  {label}: unexpected {type(exc).__name__}: {exc}"); failed += 1
        else:
            print(f"  ok    {label}"); passed += 1

    def one(text: str):
        forms = parse(text, "<arm>")
        assert len(forms) == 1, f"expected one top-level form, got {len(forms)}"
        return forms[0]

    def refuses(text: str, needle: str) -> None:
        try:
            parse(text, "<arm>")
        except SexpError as exc:
            assert needle in str(exc), f"refused, but for the wrong reason: {exc}"
        else:
            raise AssertionError(f"accepted {text!r}; it must be refused")

    # --- what the defect was: a string is bytes the author wrote, not bytes a codec guessed
    arm("GREEN non-ASCII round-trips byte-for-byte", lambda: (
        lambda got: (_ for _ in ()).throw(AssertionError(f"got {got!r}"))
        if got != "RVI-RV64I \u00a73.1.2.1 \u2014 D-LUI" else None)(
            one('(sem (source "RVI-RV64I \u00a73.1.2.1 \u2014 D-LUI"))')[1][1]))
    arm("GREEN a citation survives the whole pipeline", lambda: (
        lambda s: (_ for _ in ()).throw(AssertionError(f"mojibake: {s!r}"))
        if "\u00c2" in s or "\u00e2" in s else None)(
            field(one('(sem (source "\u00a7 \u2014 \u00b5"))'), "source")))

    # --- escapes: decoded explicitly, never by handing the whole string to a codec
    arm("GREEN \\n is a newline", lambda: _eq(field(one(r'(x (s "a\nb"))'), "s"), "a\nb"))
    arm("GREEN \\t is a tab", lambda: _eq(field(one(r'(x (s "a\tb"))'), "s"), "a\tb"))
    arm("GREEN \\\" is a quote inside the string",
        lambda: _eq(field(one(r'(x (s "a\"b"))'), "s"), 'a"b'))
    arm("GREEN \\\\ is one backslash",
        lambda: _eq(field(one(r'(x (s "a\\b"))'), "s"), "a\\b"))
    arm("RED   an unknown escape is refused, not guessed",
        lambda: refuses(r'(x (s "a\qb"))', "unknown escape"))
    arm("RED   an unterminated escape is refused",
        lambda: refuses('(x (s "a\\', "unterminated"))

    # --- the properties the single-stream scan exists for
    arm("GREEN ';' inside a string is content, not a comment",
        lambda: _eq(field(one('(x (s "a;b"))'), "s"), "a;b"))
    arm("GREEN a string spans lines and keeps the newline",
        lambda: _eq(field(one('(x (s "a\nb"))'), "s"), "a\nb"))
    arm("GREEN a comment after a form is skipped",
        lambda: _eq(field(one('(x (s "v"))   ; trailing'), "s"), "v"))
    arm("RED   an unterminated string is refused",
        lambda: refuses('(x (s "a))', "unterminated string"))

    # --- structure
    arm("RED   a stray ')' is refused", lambda: refuses("(x))", "no matching"))
    arm("RED   an unterminated list names the line it opened on",
        lambda: refuses("(a\n (b\n  (c", "unterminated list"))

    # --- atoms
    arm("GREEN decimal, hex, binary and negative atoms read as integers",
        lambda: _eq([c for c in one("(n 12 0x1f 0b101 -3)")[1:]], [12, 31, 5, -3]))
    arm("GREEN a bare symbol is not a quoted string", lambda: _eq(
        (isinstance(one('(x sym "sym")')[1], Symbol), isinstance(one('(x sym "sym")')[2], Symbol)),
        (True, False)))

    # --- accessor soundness: absence and duplication are both errors
    arm("RED   field() refuses a duplicated field", lambda: _raises(
        lambda: field(one('(x (s "a") (s "b"))'), "s", "<arm>"), "found 2"))
    arm("RED   field() refuses a field carrying two values", lambda: _raises(
        lambda: field(one('(x (s "a" "b"))'), "s", "<arm>"), "exactly one value"))

    print(f"sexp --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


def _eq(got, want) -> None:
    assert got == want, f"got {got!r}, want {want!r}"


def _raises(fn, needle: str) -> None:
    try:
        fn()
    except SexpError as exc:
        assert needle in str(exc), f"raised, but for the wrong reason: {exc}"
    else:
        raise AssertionError(f"did not raise; it must refuse ({needle})")


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] == "--self-test":
        return _selftest()
    if len(argv) != 2:
        print("usage: sexp.py <file.sexp>   |   sexp.py --self-test   # parse and report, for checking a file by hand",
              file=sys.stderr)
        return 2
    try:
        forms = read_file(Path(argv[1]))
    except SexpError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    print(f"ok: {len(forms)} top-level form(s); heads: "
          f"{', '.join(sorted({head(f) for f in forms if isinstance(f, list)}))}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
