#!/usr/bin/env python3
"""A minimal S-expression reader for this project's canonical-definition files.

WHY S-EXPRESSIONS LIVE HERE AND NOWHERE ELSE. `decision_canonical-definition-input` settles the
format question per file: records stay JSON and TOML, because they are records and are already
gated by instruments that have been fired RED. Two files are not records — `encoding.sexp` and
`semantics.sexp` — because an instruction's encoding is a small tree and its meaning is a bigger
one, and JSON renders a tree as punctuation. The ISA-formalism tradition converged on this shape
for the same reason.

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
                if text[j] == "\\" and j + 1 < n:
                    buf.append(text[j:j + 2]); j += 2
                else:
                    if text[j] == "\n":
                        line += 1
                    buf.append(text[j]); j += 1
            if j >= n:
                raise SexpError(f"{where}:{line}: unterminated string")
            stack[-1].append("".join(buf).encode().decode("unicode_escape"))
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


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: sexp.py <file.sexp>   # parse and report, for checking a file by hand",
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
