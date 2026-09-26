#!/usr/bin/env python3
"""Do this project's S-expression readers agree on every tracked `.sexp` file?

Two readers of one format that disagree is the defect `SOT-FORMAT` exists to prevent, and it is a
defect that hides: each reader is self-consistent, each passes its own tests, and the disagreement
only ever shows up as a model that behaves differently depending on which tool built it.

  A  scripts/sexp.py                  the Python tooling's reader — strict, refuses on malformed input
  B  LinkedSpec `specs/Lispish.spec`  the historical extraction route, via examples/.../lispish_file
  C  LinkedSpec `specs/SExprDocumentV1.spec`  the document grammar, via examples/.../sexpr_file

⛔ THEY DO NOT AGREE BY CONSTRUCTION, and this tool exists to say exactly where. The published
integration guide is explicit that Lispish "extracts the first parenthesized form. It can skip
malformed or extra text. A successful value does not establish that the complete file is valid",
and that applications "requiring strict document validation or multiple top-level forms need an
explicit grammar/contract for those requirements." The document grammar IS that contract, and the
comparison runs it as a separate layer.

So the comparison is deliberately layered, because collapsing it would hide the real finding
behind a pile of expected ones:

  STRUCTURE  the tree shape and the atoms, after applying the SAME numeric interpretation to both.
             This is the layer that must be identical, and a difference here is a genuine defect.
  CLASS (B only)  differences that follow from what reader B is FOR, enumerated rather than counted.
             Lispish returns atoms as text and discards the symbol/quoted-string distinction, so
             `0x0` and `(name rd)` reach it as strings. Applying sexp.py's own `_atom` to Lispish's
             text is what makes the two comparable without pretending the difference is absent.

             Two families are enumerated, both of them consequences of Lispish's PUBLISHED
             extraction contract (docs/linkedspec-book/src/public-api/integration-rust.md), not
             defects, and both surfaced in materials/catalog.sexp only once LS-001 was fixed:

             quoted-numeric   a string that QUOTES a numeric spelling (`"20260911"`) reaches
                              Lispish as text; `_atom` then types it as int. sexp.py kept it a
                              string because it saw the quotes. Same bytes, same token — the
                              quote-kind Lispish discards (tracked upstream as LS-002) is the only
                              information lost. Class iff `sexp._atom(A_text) == B` exactly, so a
                              different number (`20260912`) can never be masked.
             escape-retention Lispish retains escape sequences verbatim (`\\"` stays backslash +
                              quote — the guide documents exactly this); sexp.py decodes them per
                              the format's table (`\\"` -> `"`). Class iff decoding B with
                              sexp.py's OWN escape table reproduces A exactly; anything that does
                              not decode (or decodes differently) stays a REAL difference, loud.

  DOCUMENT (C)  reader C keeps token kinds and RAW lexemes — no number conversion, no escape
             decoding, every form in the file. Both CLASS families die by construction: a quoted
             number arrives tagged `string`, so the quote-kind is never lost; a string's escapes
             are decoded on OUR side with sexp.py's own table, so interpretation is anchored to
             the canonical reader. This layer compares EVERY top-level form (B compares the
             first, per its contract) and has no CLASS layer: lexeme-level equality is exact or
             it is a defect. It is also the read path the engine will adopt, so a green sweep
             here is evidence for that decision, not just hygiene.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sexp as _sexp                                                   # noqa: E402

REPO = Path(__file__).resolve().parent.parent
BIN = REPO / ".app-data/target/debug/lispish_file"
# ⛔ Overridable so a CANDIDATE FIX can be tested against the real corpus without touching the
# pinned submodule. A grammar edit inside vendor/ would make the submodule dirty, and a dirty
# submodule is how a pin quietly becomes a fork.
GRAMMAR = Path(os.environ.get("LISPISH_GRAMMAR", REPO / "vendor/linkedspec/specs/Lispish.spec"))
BIN_C = REPO / ".app-data/target/debug/sexpr_file"
GRAMMAR_C = REPO / "vendor/linkedspec/specs/SExprDocumentV1.spec"


class CompareError(Exception):
    """A refusal. An absent reader is never reported as an agreeing one."""


def normalise_a(form) -> object:
    """sexp.py's tree, with Symbol and str collapsed to text and ints kept as ints."""
    if isinstance(form, list):
        return [normalise_a(c) for c in form]
    if isinstance(form, bool):
        raise CompareError("unexpected bool")
    if isinstance(form, int):
        return form
    return str(form)


def normalise_b(value) -> object:
    """Lispish's application value, with sexp.py's OWN atom rule applied to each text atom.

    ⛔ This is the one interpretive step, and it is applied in the direction that cannot invent
    agreement: Lispish hands back `"0x0"`, and `_atom` turns it into the same 0 that sexp.py
    produced from the same three characters. If the two readers had genuinely read different
    tokens, no amount of re-interpretation would make them equal.
    """
    if isinstance(value, list):
        return [normalise_b(v) for v in value]
    if value is None:
        return []
    return _sexp._atom(str(value), 0)


def read_b(path: Path) -> object:
    if not BIN.exists():
        raise CompareError(
            f"the LinkedSpec consumer is not built at {BIN.relative_to(REPO)}. Build it as its "
            f"integration guide prescribes — vendor/linkedspec/docs/linkedspec-book/src/"
            f"public-api/integration-rust.md — then re-run. An unbuilt reader is not an agreeing "
            f"reader.")
    if not GRAMMAR.exists():
        raise CompareError(f"the grammar is missing at {GRAMMAR.relative_to(REPO)}; is the "
                           f"submodule initialised?")
    r = subprocess.run([str(BIN), "--grammar", str(GRAMMAR), str(path)],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise CompareError(f"{path.relative_to(REPO)}: the LinkedSpec reader exited "
                           f"{r.returncode}: {r.stderr.strip()[:200]}")
    out = r.stdout.strip()
    if not out:
        raise CompareError(f"{path.relative_to(REPO)}: the LinkedSpec reader returned no value")
    return json.loads(out)


def read_c(path: Path) -> object:
    """The document grammar's value for one file: every top-level form, tagged and raw."""
    if not BIN_C.exists():
        raise CompareError(
            f"the document consumer is not built at {BIN_C.relative_to(REPO)}. Build it as the "
            f"integration guide prescribes — vendor/linkedspec/docs/linkedspec-book/src/"
            f"public-api/integration-rust.md — then re-run. An unbuilt reader is not an agreeing "
            f"reader.")
    if not GRAMMAR_C.exists():
        raise CompareError(f"the document grammar is missing at {GRAMMAR_C.relative_to(REPO)}; "
                           f"is the submodule initialised?")
    r = subprocess.run([str(BIN_C), "--grammar", str(GRAMMAR_C), str(path)],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise CompareError(f"{path.relative_to(REPO)}: the document reader exited "
                           f"{r.returncode}: {r.stderr.strip()[:200]}")
    line = r.stdout.strip()
    if not line:
        raise CompareError(f"{path.relative_to(REPO)}: the document reader returned no value")
    obj = json.loads(line)
    if obj.get("format") != "linkedspec-sexpr-v1" or "forms" not in obj:
        raise CompareError(f"{path.relative_to(REPO)}: not a document-grammar value: {line[:120]}")
    return obj["forms"]


def normalise_c(node) -> object:
    """The document grammar's tagged node -> sexp.py's value, using ONLY sexp.py's own tables.

    Kinds and raw lexemes do the work: a quoted number arrives tagged `string` and stays one
    (the quoted-numeric family cannot arise); a string's escapes are decoded here with
    sexp.py's `_ESCAPES`, not by the reader (escape-retention cannot arise); number/symbol
    lexemes pass through `_atom` exactly as sexp.py types the same bare text.
    """
    if not isinstance(node, dict) or "kind" not in node:
        raise CompareError(f"unexpected document node {node!r}")
    kind = node["kind"]
    if kind == "list":
        return [normalise_c(i) for i in node.get("items", [])]
    lexeme = node.get("lexeme")
    if not isinstance(lexeme, str):
        raise CompareError(f"a {kind} token without a string lexeme: {node!r}")
    if kind == "string":
        if len(lexeme) < 2 or not lexeme.startswith('"') or not lexeme.endswith('"'):
            raise CompareError(f"a string lexeme must keep its quotes: {lexeme!r}")
        try:
            return _decode_escapes(lexeme[1:-1])
        except ValueError as exc:
            raise CompareError(f"a string lexeme sexp.py itself would refuse: {exc}") from exc
    if kind in ("number", "symbol"):
        return _sexp._atom(lexeme, 0)
    raise CompareError(f"unknown token kind {kind!r}")


def first_difference(a, b, path: str = "") -> str | None:
    if isinstance(a, list) != isinstance(b, list):
        return f"{path or '<root>'}: A is {type(a).__name__}, B is {type(b).__name__} — {a!r} vs {b!r}"
    if isinstance(a, list):
        if len(a) != len(b):
            return (f"{path or '<root>'}: A has {len(a)} element(s), B has {len(b)}. "
                    f"A[{min(len(a), len(b))}:]={a[len(b):]!r} B[...]={b[len(a):]!r}")
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_difference(x, y, f"{path}[{i}]")
            if d:
                return d
        return None
    return None if a == b else f"{path or '<root>'}: A={a!r}  B={b!r}"


def _decode_escapes(text: str) -> str:
    """sexp.py's escape table applied to retained text. Raises ValueError on anything the
    canonical reader would refuse (unknown escape, trailing backslash) — those stay REAL."""
    out, i, n = [], 0, len(text)
    while i < n:
        if text[i] != "\\":
            out.append(text[i]); i += 1; continue
        if i + 1 >= n:
            raise ValueError("unterminated escape")
        esc = text[i + 1]
        if esc not in _sexp._ESCAPES:
            raise ValueError(f"unknown escape \\{esc}")
        out.append(_sexp._ESCAPES[esc]); i += 2
    return "".join(out)


def classify_atom(a: object, b: object) -> str | None:
    """A documented CLASS family label, or None for a REAL value difference.

    Both families follow from Lispish's published extraction contract, not from a defect;
    both are anchored to exact byte meaning so they cannot mask a genuine difference:
    quoted-numeric requires sexp._atom(A's text) == B's int EXACTLY, escape-retention
    requires decoding B with sexp.py's own table to reproduce A EXACTLY.
    """
    if isinstance(a, str) and isinstance(b, int) and not isinstance(b, bool) \
            and _sexp._atom(a, 0) == b:
        return "quoted-numeric (Lispish discards quote-kind; upstream LS-002)"
    if isinstance(a, str) and isinstance(b, str) and "\\" in b:
        try:
            if _decode_escapes(b) == a:
                return "escape-retention (Lispish retains escapes verbatim; sexp.py decodes)"
        except ValueError:
            return None
    return None


def differences(a: object, b: object, path: str = ""):
    """Every differing position as (path, kind, a_val, b_val); kind is "shape" (structural,
    always a defect) or "atom" (same shape, differing value — then classified by the caller)."""
    if isinstance(a, list) != isinstance(b, list):
        yield (path or "<root>", "shape", a, b); return
    if isinstance(a, list):
        if len(a) != len(b):
            yield (path or "<root>", "shape",
                   f"A has {len(a)} element(s), B has {len(b)}", ""); return
        for i, (x, y) in enumerate(zip(a, b)):
            yield from differences(x, y, f"{path}[{i}]")
        return
    if a != b:
        yield (path or "<root>", "atom", a, b)


def compare(paths: list[Path]) -> int:
    bad = 0
    for p in paths:
        try:
            a_forms = _sexp.read_file(p)
            a = normalise_a(a_forms[0])                # layer B: the first form, per Lispish
            b = normalise_b(read_b(p))
            a_all = [normalise_a(f) for f in a_forms]  # layer C: every form, tagged lexemes
            c = [normalise_c(f) for f in read_c(p)]
        except (CompareError, _sexp.SexpError) as exc:
            print(f"  REFUSED {p.relative_to(REPO)}: {exc}", file=sys.stderr); bad += 1; continue
        n = sum(1 for _ in _walk(a))
        n_all = sum(1 for _ in _walk(a_all))
        ok = True
        diffs = list(differences(a, b))
        structural = [d for d in diffs if d[1] == "shape"]
        classes, real = [], []
        for d in diffs:
            if d[1] == "shape":
                continue
            label = classify_atom(d[2], d[3])
            (classes if label else real).append((d, label))
        if structural or real:
            d = first_difference(a, b)
            print(f"  DIFFER  {p.relative_to(REPO)}  ({n} nodes, lispish)\n            {d}",
                  file=sys.stderr)
            ok = False
        c_diff = first_difference(a_all, c)
        if c_diff:
            print(f"  DIFFER  {p.relative_to(REPO)}  ({n_all} nodes, document)\n"
                  f"            {c_diff}", file=sys.stderr)
            ok = False
        if not ok:
            bad += 1
        else:
            print(f"  agree   {str(p.relative_to(REPO)):44} {n:>6} nodes identical "
                  f"[lispish]; {n_all} nodes, {len(a_all)} form(s) [document]")
            for d, label in classes:
                print(f"  class   {p.relative_to(REPO)} {d[0]}: A={d[2]!r} B={d[3]!r} — {label}")
    print(f"\ncompare_readers: {len(paths) - bad} of {len(paths)} file(s) agree")
    return 1 if bad else 0


def _walk(x):
    yield x
    if isinstance(x, list):
        for c in x:
            yield from _walk(c)


# ⛔ `docs/upstream/` holds DELIBERATELY PATHOLOGICAL inputs — the case files of bug reports
# raised against other projects. They exist to make a reader misbehave, so comparing the two
# readers on them would report the very defect the report already documents, as a failure of this
# repository. A corpus and a bug-report fixture are different things and must not share a sweep.
EXCLUDED_PREFIXES = ("docs/upstream/",)


def tracked_sexp() -> list[Path]:
    out = subprocess.run(["git", "-C", str(REPO), "ls-files", "*.sexp"],
                         capture_output=True, text=True, check=True)
    return [REPO / line for line in out.stdout.split()
            if line and not line.startswith(EXCLUDED_PREFIXES)]


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "--self-test":
        return _selftest()
    paths = [Path(a).resolve() for a in argv[1:]] or tracked_sexp()
    if not paths:
        print("REFUSED: no tracked .sexp file found; nothing to compare", file=sys.stderr)
        return 1
    try:
        return compare(paths)
    except CompareError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr); return 1


def _selftest() -> int:
    passed = failed = 0

    def arm(label, fn):
        nonlocal passed, failed
        try:
            fn()
        except AssertionError as exc:
            print(f"  FAIL  {label}: {exc}"); failed += 1
        except Exception as exc:                        # noqa: BLE001
            print(f"  FAIL  {label}: unexpected {type(exc).__name__}: {exc}"); failed += 1
        else:
            print(f"  ok    {label}"); passed += 1

    def eq(x, y): assert x == y, f"got {x!r}, want {y!r}"
    def diff(a, b, needle):
        d = first_difference(a, b)
        assert d is not None, f"no difference reported between {a!r} and {b!r}"
        assert needle in d, f"difference reported for the wrong reason: {d}"
    def agrees(a, b):
        assert first_difference(a, b) is None, f"{a!r} != {b!r}"
    def refuses_c(node, needle):
        try:
            normalise_c(node)
        except CompareError as exc:
            assert needle in str(exc), f"refused for the wrong reason: {exc}"
        else:
            raise AssertionError(f"no refusal for {node!r}")

    arm("GREEN document layer: a quoted number stays a string — the LS-002 class cannot arise",
        lambda: agrees(normalise_a(['tag', '20260911']),
                       normalise_c({'kind': 'list', 'items': [
                           {'kind': 'symbol', 'lexeme': 'tag'},
                           {'kind': 'string', 'lexeme': '"20260911"'}]})))
    arm("GREEN document layer: escapes decode with sexp.py's own table",
        lambda: eq(normalise_c({'kind': 'string', 'lexeme': '"a\\"q"'}), 'a"q'))
    arm("GREEN document layer: number and symbol lexemes type through sexp.py's _atom",
        lambda: (eq(normalise_c({'kind': 'number', 'lexeme': '0x10'}), 16),
                 eq(normalise_c({'kind': 'symbol', 'lexeme': '0b1010'}), 10)))
    arm("RED   document layer: differing lexemes refuse — no interpretive escape hatch",
        lambda: diff(normalise_a(['tag', '20260911']),
                     normalise_c({'kind': 'list', 'items': [
                         {'kind': 'symbol', 'lexeme': 'tag'},
                         {'kind': 'string', 'lexeme': '"20260912"'}]}),
                     "A='20260911'"))
    arm("RED   document layer: a lexeme sexp.py would refuse is refused, not guessed",
        lambda: refuses_c({'kind': 'string', 'lexeme': '"a\\qb"'}, "would refuse"))
    arm("GREEN document layer: EVERY form is compared, not the first",
        lambda: agrees([normalise_a(f) for f in _sexp.parse('(v 1 "1") (done)')],
                       [normalise_c(f) for f in [
                           {'kind': 'list', 'items': [
                               {'kind': 'symbol', 'lexeme': 'v'},
                               {'kind': 'number', 'lexeme': '1'},
                               {'kind': 'string', 'lexeme': '"1"'}]},
                           {'kind': 'list', 'items': [
                               {'kind': 'symbol', 'lexeme': 'done'}]}]]))
    arm("RED   an unbuilt document consumer refuses instead of reporting agreement", lambda: (
        lambda saved: (_try_read_c_missing(),
                       globals().__setitem__("BIN_C", saved))[0])(BIN_C))

    arm("GREEN identical trees report no difference",
        lambda: eq(first_difference(["a", ["b", 1]], ["a", ["b", 1]]), None))
    arm("RED   a differing atom is located by path",
        lambda: diff(["a", ["b", 1]], ["a", ["b", 2]], "[1][1]"))
    arm("RED   a differing LENGTH is reported, not silently zipped",
        lambda: diff(["a", "b"], ["a"], "A has 2 element(s), B has 1"))
    arm("RED   an extra element on B is reported",
        lambda: diff(["a"], ["a", "b"], "A has 1 element(s), B has 2"))
    arm("RED   atom-vs-list at the same position is reported",
        lambda: diff(["a", "b"], ["a", ["b"]], "A is str, B is list"))
    arm("GREEN Lispish's text atoms normalise through sexp.py's OWN rule",
        lambda: eq(normalise_b(["ilen", "32"]), ["ilen", 32]))
    arm("GREEN a hex atom normalises to the same int both readers mean",
        lambda: eq(normalise_b(["fixed", ["31", "25", "0x0"]]), ["fixed", [31, 25, 0]]))
    arm("GREEN Lispish's null (empty list) becomes an empty list",
        lambda: eq(normalise_b(["extensions", None]), ["extensions", []]))
    arm("GREEN sexp.py's Symbol and str collapse to the same text",
        lambda: eq(normalise_a([_sexp.Symbol("rd"), "rd"]), ["rd", "rd"]))
    arm("RED   normalisation cannot invent agreement between different tokens",
        lambda: diff(normalise_a([_sexp.Symbol("rd")]), normalise_b(["rs1"]), "A='rd'"))
    arm("GREEN a quoted numeric string classifies as quote-kind loss (LS-002)",
        lambda: eq(classify_atom("20260911", 20260911),
                   "quoted-numeric (Lispish discards quote-kind; upstream LS-002)"))
    arm("GREEN a hex-quoted numeric string classifies the same way",
        lambda: eq(classify_atom("0x10", 16),
                   "quoted-numeric (Lispish discards quote-kind; upstream LS-002)"))
    arm("RED   a DIFFERENT number is not class — the rule cannot mask a real value change",
        lambda: eq(classify_atom("20260911", 20260912), None))
    arm("RED   a non-numeric string against an int is not class",
        lambda: eq(classify_atom("v0.2", 2), None))
    arm("GREEN an escape-retained string classifies when decoding B reproduces A exactly",
        lambda: eq(classify_atom('says "hi"', 'says \\"hi\\"'),
                   "escape-retention (Lispish retains escapes verbatim; sexp.py decodes)"))
    arm("RED   retained text that does NOT decode to A stays a REAL difference",
        lambda: eq(classify_atom('says "hi"', 'says \\q"hi\\"'), None))
    arm("RED   a trailing backslash cannot decode and stays REAL",
        lambda: eq(classify_atom("x", "x\\"), None))
    arm("RED   two unequal plain strings are a REAL difference",
        lambda: eq(classify_atom("abc", "abd"), None))
    arm("GREEN differences() reports every position, shape and atom, not just the first", lambda: (
        eq([(d[0], d[1]) for d in differences(["a", ["b", 1], ["c", 2]], ["a", ["b", 1], ["c", 3]])],
           [("[2][1]", "atom")]),
        eq([d[1] for d in differences(["a"], ["a", "b"])], ["shape"])))
    arm("RED   an unbuilt consumer refuses instead of reporting agreement", lambda: (
        lambda saved: (_try_read_b_missing(), globals().__setitem__("BIN", saved))[0])(BIN))

    def excludes_reports() -> None:
        files = [str(p.relative_to(REPO)) for p in tracked_sexp()]
        bad = [f for f in files if f.startswith("docs/upstream/")]
        assert not bad, f"bug-report fixtures leaked into the corpus sweep: {bad[:3]}"
        assert files, "the sweep found nothing at all, so it proves nothing"
    arm("GREEN the sweep excludes bug-report fixtures but is not empty", excludes_reports)

    print(f"compare_readers --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


def _try_read_b_missing():
    global BIN
    BIN = REPO / ".app-data/target/debug/does-not-exist"
    try:
        read_b(REPO / "profiles/rv64i-lab-v0/encoding.sexp")
    except CompareError as exc:
        assert "not built" in str(exc), f"refused for the wrong reason: {exc}"
    else:
        raise AssertionError("an unbuilt consumer was not refused")


def _try_read_c_missing():
    global BIN_C
    BIN_C = REPO / ".app-data/target/debug/does-not-exist"
    try:
        read_c(REPO / "profiles/rv64i-lab-v0/encoding.sexp")
    except CompareError as exc:
        assert "not built" in str(exc), f"refused for the wrong reason: {exc}"
    else:
        raise AssertionError("an unbuilt document consumer was not refused")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
