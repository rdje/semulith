#!/usr/bin/env python3
"""Convert the profile dossier from TOML/JSON to the one format, and prove the round-trip.

`SOT-FORMAT.4` moved the profile's configuration, state and provenance documents behind the
schema layer. This tool drove that migration and owns its proof, the way `convert_records.py`
(`.3`) does for the record catalogues:

  convert_dossier.py to-sexp <src.toml|json> <out.sexp>   one migration direction
  convert_dossier.py verify  <src.toml|json> <out.sexp>   losslessness, MECHANICALLY:
      - the document re-derived from the sexp equals the TOML/JSON parse, field for field
      - the comment census: every TOML comment line survives as a comment-form string,
        in order (`SOT-FORMAT.4`: comments are first-class forms, never dropped)
      - the converted file conforms to its schema-layer schema
  convert_dossier.py --self-test

LOSSLESSNESS IS A COMPARISON, NOT A REVIEW. TOML re-dump byte-identity is deliberately NOT
claimed — these files are hand-formatted; data identity plus comment survival is the honest
claim, and both are checked here.

THE COMMENT SCANNER. `tomllib` drops comments entirely, so the scanner re-reads the source
text line by line, string-aware (a `#` inside a string is content; multi-line strings are
tracked), and records each block's anchor:

  - a block before any code is a FILE note — it becomes a top-level `(comment …)` form
  - a block before a table header attaches BEFORE that table's form
  - a block before a key attaches BEFORE that field
  - a comment trailing a value attaches AFTER that field; INDENTED comment-only lines that
    follow it with no blank line in between are its CONTINUATION lines, aligned under it
    (the profile.toml `privilege_modes` shape); a column-0 comment starts a new block
  - a trailing block at EOF lands after the last child

Anchors are resolved structurally (head + occurrence), never by line number, so a comment
cannot silently drift onto the wrong element.
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sexp as S                                # noqa: E402
import dossier_sexp as D                        # noqa: E402
import records_sexp as R                        # noqa: E402
import check_sexp_schema as K                   # noqa: E402

REPO = Path(__file__).resolve().parent.parent

WHAT = {
    "profile": "decision dossier ([profile], [state], [scope], [[decision]])",
    "state": "architectural-state document",
    "sources": "pinned specification sources",
    "references": "reference candidate dossier",
    "override": "matched-profile reference override (the Sail model reads the derived JSON)",
    "expectations": "guest expectation document",
}


class Note:
    """One comment block and its anchor.

    pos:     "file" (top level, before the root form) | "before" | "after" | "eof"
    path:    the construct path the anchor lives at, () for the root — a tuple of
             (head, occurrence) pairs, e.g. (("decision", 3),)
    anchor:  the form head (pos "before" on a table) or the field name
    """

    def __init__(self, pos: str, path: tuple, anchor, lines: list[str]):
        self.pos = pos
        self.path = path
        self.anchor = anchor
        self.lines = lines

    def __repr__(self):
        return f"Note({self.pos}, {self.path}, {self.anchor!r}, {self.lines!r})"


def _comment_form(lines: list[str]) -> list:
    return [S.Symbol("comment"), *lines]


# --------------------------------------------------------------------------- the TOML scanner

def scan_toml(text: str, source_name: str) -> list[Note]:
    notes: list[Note] = []
    pending: Note | None = None
    inline: Note | None = None
    seen_code = False
    path: tuple = ()                       # current table path, ((head, occurrence), …)
    counts: dict[str, int] = {}
    ml: str | None = None                  # None | '"""' | "'''"

    def flush(anchor_path: tuple, anchor):
        nonlocal pending
        if pending is not None:
            if pending.pos != "file":
                pending.path, pending.anchor = anchor_path, anchor
            notes.append(pending)
            pending = None

    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw
        if ml is not None:                            # inside a multi-line string
            end = line.find(ml)
            if end < 0:
                continue
            line = line[end + 3:]
            ml = None
        # split code from comment, string-aware
        code, comment = [], None
        i, n = 0, len(line)
        basic = literal = False
        while i < n:
            ch = line[i]
            if basic:
                if ch == "\\":
                    i += 2
                    continue
                if ch == '"':
                    basic = False
                i += 1
                continue
            if literal:
                if ch == "'":
                    literal = False
                i += 1
                continue
            if line.startswith('"""', i) or line.startswith("'''", i):
                ml = line[i:i + 3]
                break
            if ch == '"':
                basic = True
            elif ch == "'":
                literal = True
            elif ch == "#":
                comment = line[i + 1:]
                break
            i += 1
        code = line[:i] if comment is not None or ml is not None else line
        stripped = code.strip()
        if comment is not None:
            comment = comment.strip()
        if not stripped and comment is None:          # blank line: breaks a continuation
            inline = None
            continue
        if not stripped:                              # comment-only line
            indented = bool(line[:len(line) - len(line.lstrip())])
            if inline is not None and indented:
                inline.lines.append(comment)          # aligned under the inline comment
            else:
                if pending is None:
                    pending = Note("file" if not seen_code else "before", (), None, [])
                pending.lines.append(comment)
            continue
        m_arr = re.match(r"^\s*\[\[([A-Za-z0-9_.-]+)\]\]", code)
        m_tab = re.match(r"^\s*\[([A-Za-z0-9_.-]+)\]", code)
        if m_arr or m_tab:
            if comment is not None:
                raise SystemExit(f"{source_name}:{lineno}: a comment on a table header line "
                                 f"is not placed by this converter — give it its own line")
            head = (m_arr or m_tab).group(1)
            if m_arr:
                counts[head] = counts.get(head, 0) + 1
                ordinal = counts[head] - 1
            else:
                ordinal = 0
            flush(((head, ordinal),), head)
            path = ((head, ordinal),)
            seen_code = True
            inline = None
            continue
        m_key = re.match(r"^\s*([A-Za-z0-9_-]+)\s*=", code)
        if m_key:
            key = m_key.group(1)
            flush(path, key)
            seen_code = True
            if comment is not None:
                inline = Note("after", path, key, [comment])
                notes.append(inline)
            else:
                inline = None
            continue
        if comment is not None:
            raise SystemExit(f"{source_name}:{lineno}: a comment on a line that is neither "
                             f"a key nor a table header is not placed by this converter")
        inline = None
    if pending is not None:
        pending.pos = "eof"
        notes.append(pending)
    return notes


# --------------------------------------------------------------------------- insertion

def _walk(form, path: tuple, source_name: str):
    target = form
    for head, ordinal in path:
        matches = [c for c in target[1:] if isinstance(c, list) and str(c[0]) == head]
        if len(matches) <= ordinal:
            # the document root IS the first occurrence of its own construct ([profile] maps
            # to the root form, not to a child of it)
            if ordinal == 0 and str(target[0]) == head:
                continue
            raise SystemExit(f"{source_name}: cannot place a comment — ({head} …) occurrence "
                             f"{ordinal} not found in the converted document")
        target = matches[ordinal]
    return target


# When an inline comment annotates a field that converted to ABSENCE (an empty list is
# absent by the `.3` rule), it lands where the field would have: before the next field the
# document order declares, else at the end of the construct. The orders come from the
# mapping owner's specs — the document's canonical field order.
ORDERS: dict[str, list[str]] = {}


def insert_notes(root: list, notes: list[Note], source_name: str) -> tuple[list, list]:
    """Resolve every note into the form tree. Returns (top_level_forms, root)."""
    top: list = []
    for note in notes:
        form = _comment_form(note.lines)
        if note.pos == "file":
            top.append(form)
        elif note.pos == "eof":
            root.append(form)
        elif note.pos == "before" and note.anchor is not None and \
                note.path and note.path[-1][0] == note.anchor:
            # before a table's form: the tables of this corpus are depth-1 under the root
            parent = _walk(root, note.path[:-1], source_name)
            head, ordinal = note.path[-1]
            seen = -1
            for idx, c in enumerate(parent[1:]):
                if isinstance(c, list) and str(c[0]) == head:
                    seen += 1
                    if seen == ordinal:
                        parent.insert(idx + 1, form)
                        break
            else:
                if ordinal == 0 and str(parent[0]) == head:
                    parent.insert(1, form)   # the root form is its own first occurrence
                else:
                    raise SystemExit(f"{source_name}: cannot place a comment before ({head} …) "
                                     f"occurrence {ordinal}")
        else:
            target = _walk(root, note.path, source_name)
            hits = [i for i, c in enumerate(target[1:])
                    if isinstance(c, list) and str(c[0]) == note.anchor]
            if hits:
                # hits are indices into target[1:]; list insertion needs +1, and "after"
                # needs one more slot still
                at = hits[-1] + 2 if note.pos == "after" else hits[0] + 1
                target.insert(at, form)
                continue
            if note.pos == "after":
                order = ORDERS.get(str(target[0]), [])
                if note.anchor in order:
                    present = {str(c[0]) for c in target[1:] if isinstance(c, list)}
                    for later in order[order.index(note.anchor) + 1:]:
                        if later in present:
                            idx = next(i for i, c in enumerate(target[1:])
                                       if isinstance(c, list) and str(c[0]) == later)
                            target.insert(idx + 1, form)
                            break
                    else:
                        target.append(form)
                    continue
            raise SystemExit(f"{source_name}: cannot place a comment — field "
                             f"({note.anchor} …) not found")
    return top, root


# --------------------------------------------------------------------------- conversion

def to_sexp(src: Path, dst: Path) -> None:
    fam = D.family_for(src)
    ORDERS.clear()
    if fam == "profile":
        ORDERS.update({"profile": [n for n, _ in D._PROFILE_SPEC] + ["state", "scope", "decision"],
                       "state": [n for n, _ in D._STATE_SPEC],
                       "scope": [n for n, _ in D._SCOPE_SPEC()],
                       "decision": [n for n, _ in D._DECISION_SPEC]})
    elif fam == "sources":
        ORDERS.update({"sources": [n for n, _ in D._SOURCES_TOP] + ["source"],
                       "source": [n for n, _ in D._SOURCE_SPEC]})
    elif fam == "references":
        ORDERS.update({"references": [n for n, _ in D._REFERENCES_TOP] +
                       ["host", "candidate", "attempt", "experiment", "difference",
                        "independence", "encoding_source"],
                       "candidate": [n for n, _ in D._CANDIDATE_SPEC],
                       "attempt": [n for n, _ in D._ATTEMPT_SPEC],
                       "experiment": [n for n, _ in D._EXPERIMENT_SPEC],
                       "difference": [n for n, _ in D._DIFFERENCE_SPEC],
                       "independence": [n for n, _ in D._INDEPENDENCE_SPEC],
                       "encoding_source": [n for n, _ in D._ENCODING_SOURCE_SPEC] +
                       ["file"], "enc_file": [n for n, _ in D._ENC_FILE_SPEC],
                       "host": [n for n, _ in D._HOST_SPEC]})
    elif fam == "expectations":
        ORDERS["expectations"] = ["program", "entry", "instructions", "never_written",
                                  "cross_model", "step"]
    doc = D.read_source_document(src)
    root = D._TO_FORM[fam](doc)
    notes = scan_toml(src.read_text(), src.name) if src.suffix == ".toml" else []
    top, root = insert_notes(root, notes, src.name)
    schema = D._SCHEMA_FOR[fam]
    header = (f";; {dst.name} — {WHAT[fam]}, converted from {src.name} by\n"
              f";; scripts/convert_dossier.py (SOT-FORMAT.4). One document form; validate with\n"
              f";;   python3 scripts/check_sexp_schema.py {dst.name} {schema}\n"
              f";; Round-trip: `python3 scripts/convert_dossier.py verify {src.name} {dst.name}`"
              f" — data-equal, comment census exact.\n")
    text = header + "\n" + R.render_forms(top + [root])
    dst.write_text(text)
    print(f"wrote {dst} ({fam}, {len(text.encode())} bytes, "
          f"{sum(len(n.lines) for n in notes)} comment line(s) preserved)")


def _diff(a, b, where: str):
    """First difference between two parsed documents, as a readable path."""
    if type(a) != type(b):
        return f"{where}: type {type(a).__name__} != {type(b).__name__}"
    if isinstance(a, dict):
        for k in a:
            if k not in b:
                return f"{where}.{k}: missing on the converted side"
        for k in b:
            if k not in a:
                return f"{where}.{k}: added on the converted side"
        for k in a:
            d = _diff(a[k], b[k], f"{where}.{k}")
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return f"{where}: {len(a)} element(s) != {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            d = _diff(x, y, f"{where}[{i}]")
            if d:
                return d
        return None
    return None if a == b else f"{where}: {a!r} != {b!r}"


def _census(forms) -> list[str]:
    lines: list[str] = []

    def walk(form):
        if isinstance(form, list):
            if form and str(form[0]) == "comment":
                lines.extend(str(a) for a in form[1:])
                return
            for c in form[1:]:
                if isinstance(c, list):
                    walk(c)
    for f in forms:
        walk(f)
    return lines


def verify(src: Path, dst: Path) -> int:
    fam = D.family_for(src)
    try:
        want_doc = D.read_source_document(src)
    except D.DossierError as exc:
        print(f"VERIFY FAIL: {exc}")
        return 1
    try:
        forms = S.read_file(dst)
        roots = [f for f in forms if not (isinstance(f, list) and f and str(f[0]) == "comment")]
        if len(roots) != 1:
            print(f"VERIFY FAIL: {dst.name}: expected exactly one document form (annotations "
                  f"aside), found {len(roots)}")
            return 1
        got_doc = D._TO_DOC[fam](roots[0])
    except (S.SexpError, D.DossierError) as exc:
        print(f"VERIFY FAIL: {dst}: does not re-derive — {exc}")
        return 1
    diff = _diff(want_doc, got_doc, src.stem)
    if diff:
        print(f"VERIFY FAIL: data drift — {diff}")
        return 1
    got_notes = _census(forms)
    if src.suffix == ".toml":
        want_notes = [l for n in scan_toml(src.read_text(), src.name) for l in n.lines]
        if got_notes != want_notes:
            for i, (a, b) in enumerate(zip(want_notes, got_notes)):
                if a != b:
                    print(f"VERIFY FAIL: comment census drift at line {i + 1}:\n"
                          f"  src: {a!r}\n  got: {b!r}")
                    return 1
            print(f"VERIFY FAIL: comment census drift — {len(want_notes)} source line(s), "
                  f"{len(got_notes)} in {dst.name}")
            return 1
    elif got_notes:
        print(f"VERIFY FAIL: {dst.name} carries {len(got_notes)} comment line(s); the JSON "
              f"source has none")
        return 1
    schema = REPO / D._SCHEMA_FOR[fam]
    try:
        constructs, operators = K.load_schema(schema)
        errors = K.validate_file(dst, constructs, operators)
    except (K.SchemaError, S.SexpError) as exc:
        print(f"VERIFY FAIL: the schema itself: {exc}")
        return 1
    if errors:
        for e in errors:
            print(f"VERIFY FAIL: schema: {e}")
        return 1
    n = sum(1 for _ in scan_toml(src.read_text(), src.name)) if src.suffix == ".toml" else 0
    print(f"round-trip ok: {fam} — document field-for-field equal, {len(got_notes)} comment "
          f"line(s) in {n} block(s) exact, conforms to {schema.name}")
    return 0


# --------------------------------------------------------------------------- self-test

def _selftest() -> int:
    passed = failed = 0

    def arm(label: str, fn) -> None:
        nonlocal passed, failed
        try:
            fn()
        except AssertionError as exc:
            print(f"  FAIL  {label}: {exc}"); failed += 1
        except Exception as exc:                        # noqa: BLE001
            print(f"  FAIL  {label}: unexpected {type(exc).__name__}: {exc}"); failed += 1
        else:
            print(f"  ok    {label}"); passed += 1

    def eq(x, y):
        assert x == y, f"got {x!r}, want {y!r}"

    TOY = """# file header
# second header line
[unit]
id = "u"        # inline one
                # inline continuation
# before width
width = 32
# trailing eof comment
"""
    NOTES = ("file header", "second header line", "inline one", "inline continuation",
             "before width", "trailing eof comment")

    def scan_notes(text=TOY):
        return scan_toml(text, "<arm>")

    arm("GREEN a file-header block anchors to the file", lambda: (
        eq([(n.pos, n.anchor, n.lines) for n in scan_notes()][:1],
           [("file", None, ["file header", "second header line"])])))
    arm("GREEN an inline comment anchors after its field, continuations joined",
        lambda: (lambda ns: eq((ns[1].pos, ns[1].path, ns[1].anchor, ns[1].lines),
                               ("after", (("unit", 0),), "id", ["inline one",
                                "inline continuation"])))(scan_notes()))
    arm("GREEN a block before a key anchors before that field",
        lambda: (lambda ns: eq((ns[2].pos, ns[2].path, ns[2].anchor, ns[2].lines),
                               ("before", (("unit", 0),), "width", ["before width"])))(
            scan_notes()))
    arm("GREEN a trailing block anchors at EOF",
        lambda: eq(scan_notes()[-1].pos, "eof"))
    arm("GREEN # and quotes inside strings are not comments",
        lambda: eq(scan_toml('a = "x # y ; z"  # real\nb = "q\\"q" # after\n', "<arm>")[-1]
                   .lines, ["after"]))
    arm("GREEN a multi-line string hides its # until close", lambda: eq(
        scan_toml('a = """\n# hidden\n"""\nb = 1 # seen\n', "<arm>")[-1].lines, ["seen"]))
    arm("GREEN a # on a bare line inside a ML string stays hidden", lambda: eq(
        len(scan_toml('a = """x\n# hidden\n"""\n', "<arm>")), 0))
    arm("RED   a comment on a table header line is refused, not misplaced", lambda: (
        _raised(SystemExit, lambda: scan_toml("[t] # nope\n", "<arm>"), "table header")))
    arm("RED   a comment on a non-key line is refused, not misplaced", lambda: (
        _raised(SystemExit, lambda: scan_toml('a = [1,\n2] # nope\n', "<arm>"), "neither")))

    def insert_arm():
        root = [S.Symbol("profile"), [S.Symbol("id"), "p"], [S.Symbol("state")],
                [S.Symbol("scope")]]
        notes = [Note("file", (), None, ["header"]),
                 Note("before", (("state", 0),), "state", ["why state"]),
                 Note("before", (), "id", ["why id"]),
                 Note("after", (), "id", ["id provenance"]),
                 Note("eof", (), None, ["tail"])]
        top, root = insert_notes(root, notes, "<arm>")
        eq(top, [[S.Symbol("comment"), "header"]])
        eq(root, [S.Symbol("profile"), [S.Symbol("comment"), "why id"],
                  [S.Symbol("id"), "p"], [S.Symbol("comment"), "id provenance"],
                  [S.Symbol("comment"), "why state"], [S.Symbol("state")],
                  [S.Symbol("scope")], [S.Symbol("comment"), "tail"]])
    arm("GREEN notes land in the tree — file top, before forms, before fields, eof",
        insert_arm)

    def roundtrip_arm():
        with tempfile.TemporaryDirectory(dir=REPO / "target") as td:
            td = Path(td)
            src, dst = td / "guests.smoke.expected.toml", td / "smoke.expected.sexp"
            src.write_text('program = "g.s"\nentry = "0x80000000"\ninstructions = 1\n'
                           '# header policy\n[[step]]\nn = 0\ninsn = "addi x1, x0, 1"\n'
                           'writes = { x1 = "0x0000000000000001" }  # the write\n'
                           'derivation = "d"\nsource = "s"\n')
            to_sexp(src, dst)
            eq(verify(src, dst), 0)
    arm("GREEN a guest fixture converts and verifies end to end", roundtrip_arm)

    def drift_arm():
        with tempfile.TemporaryDirectory(dir=REPO / "target") as td:
            td = Path(td)
            src, dst = td / "guests.x.expected.toml", td / "x.expected.sexp"
            src.write_text('program = "g.s"\nentry = "0x80000000"\ninstructions = 1\n'
                           '# header policy\n[[step]]\nn = 0\ninsn = "i"\nwrites = {}\n'
                           'derivation = "d"\nsource = "s"\n')
            to_sexp(src, dst)
            text = dst.read_text()
            dst.write_text(text.replace('(comment "header policy")', "", 1))
            _eq1(verify(src, dst))
    arm("RED   a dropped comment line fails the census", drift_arm)

    print(f"convert_dossier --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


def _raised(want, fn, needle: str) -> None:
    try:
        fn()
    except want as exc:
        assert not needle or needle in str(exc), f"raised, wrong reason: {exc}"
        return
    raise AssertionError(f"expected {want.__name__}; none raised")


def _eq1(v):
    assert v == 1, f"verify returned {v}, want 1"


def main(argv: list[str]) -> int:
    if "--self-test" in argv[1:]:
        return _selftest()
    if len(argv) != 4 or argv[1] not in ("to-sexp", "verify"):
        print("usage: convert_dossier.py to-sexp <src.toml|json> <out.sexp> | "
              "convert_dossier.py verify <src.toml|json> <out.sexp> | --self-test",
              file=sys.stderr)
        return 2
    src, dst = Path(argv[2]), Path(argv[3])
    if argv[1] == "to-sexp":
        to_sexp(src, dst)
        return 0
    return verify(src, dst)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
