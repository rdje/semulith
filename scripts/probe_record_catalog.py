#!/usr/bin/env python3
"""Exercise catalog expansion and its public reader/schema boundaries on-volume."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import check_sexp_schema as K
import record_catalog as C
import records_sexp as R
import sexp as S

ROOT = Path(__file__).resolve().parent.parent


def record(name: str, statement: str = "Synthetic fixture") -> dict:
    return {"id": name, "contract_id": "fixture", "contract_version": "0",
            "profile_ids": ["fixture"], "direction": "cpu-guarantee",
            "statement": statement, "authority": "laboratory",
            "source_refs": [{"source_id": "SRC-FIXTURE", "locator": "§1"}],
            "parameters": {}, "dependencies": [],
            "required_checks": [f"CHK-{name}-POS", f"CHK-{name}-NEG"]}


def include(path: str) -> str:
    return f'(include-obligations (path {R.quote_string(path)}))\n'


def run(mutation: str | None) -> int:
    base = ROOT / "target/record-catalog-probe"
    base.mkdir(parents=True, exist_ok=True)
    failures, ran = [], 0
    constructs, operators = K.load_schema(ROOT / "schema/contract-obligations.sexp")
    with tempfile.TemporaryDirectory(dir=base) as scratch:
        parent = Path(scratch)

        def arm(label, fn):
            nonlocal ran
            ran += 1
            root = parent / str(ran)
            root.mkdir()
            try:
                fn(root)
            except Exception as error:  # Every failed control remains visible.
                failures.append(f"{label}: {type(error).__name__}: {error}")

        def catalog(root, source):
            p = root / "contract-obligations.sexp"
            p.write_text(source, encoding="utf-8")
            return p

        def split(root):
            a, b = R.dump([record("OB-A")]), R.dump([record("OB-B")])
            (root / "a.obligations.sexp").write_text(a)
            (root / "b.obligations.sexp").write_text(b)
            p = catalog(root, "; exact header\n" + include("a.obligations.sexp")
                        + include("b.obligations.sexp"))
            return p, "; exact header\n" + a + b

        def equal(actual, expected):
            assert actual == expected, f"expected {expected!r}, got {actual!r}"

        def refused(root, source, reason, setup=None, filename="contract-obligations.sexp"):
            p = root / filename
            p.write_text(source)
            if setup:
                setup(root)
            try:
                C.text(p, root=root)
            except C.CatalogRefused as error:
                reasons = (reason,) if isinstance(reason, str) else reason
                assert any(value in str(error) for value in reasons), str(error)
            else:
                raise AssertionError(f"accepted input requiring {reason}")

        def flat(root):
            source = "; café — intact\n" + R.dump([record("OB-A")])
            p = catalog(root, source)
            equal(C.text(p, root=root), source)
            equal(R.load(p, root=root), [record("OB-A")])

        def expansion(root):
            p, expected = split(root)
            sources = {}
            equal(C.text(p, root=root, source_texts=sources), expected)
            equal(R.load(p, root=root), [record("OB-A"), record("OB-B")])
            equal(set(sources), {p, root / "a.obligations.sexp", root / "b.obligations.sexp"})
            for origin, source in sources.items():
                equal(K.validate_text(source, constructs, operators, origin.name), [])

        def nested(root):
            p, expected = split(root)
            (root / "nested.obligations.sexp").write_text(
                include("a.obligations.sexp") + include("b.obligations.sexp"))
            p.write_text("; exact header\n" + include("nested.obligations.sexp"))
            equal(C.text(p, root=root), expected)

        def relocation(root):
            p, expected = split(root)
            dest = root / "moved"
            shutil.copytree(root, dest, ignore=shutil.ignore_patterns("moved"))
            equal(C.text(dest / p.name, root=dest), expected)

        def lexical(root):
            prose = 'café\n(include-obligations (path "absent")); text'
            source = ('; (include-obligations (path "missing"))\n'
                      + R.dump([record("OB-A", prose)]).replace('\\n', '\n'))
            p = catalog(root, source)
            equal(C.text(p, root=root), source)
            equal(R.load(p, root=root), [record("OB-A", prose)])
            for form, start, end in S.forms_with_spans(source):
                equal(S.parse(source[start:end]), [form])

        def annotations(root):
            source = '(comment "valid record annotation — café")\n' + R.dump([record("OB-A")])
            p = catalog(root, source)
            equal(K.validate_text(source, constructs, operators, p.name), [])
            equal(R.load(p, root=root), [record("OB-A")])
            assert K.validate_text('(comment 7)', constructs, operators, p.name)

        def included_schema(root):
            p, _ = split(root)
            part = root / "b.obligations.sexp"
            part.write_text(R.dump([record("OB-B")]).replace("cpu-guarantee", "unknown-direction"))
            sources = {}
            C.text(p, root=root, source_texts=sources)
            errors = [e for origin, source in sources.items()
                      for e in K.validate_text(source, constructs, operators, origin.name)]
            assert len(errors) == 1 and "b.obligations.sexp" in errors[0], errors

        def cli(root):
            p, expected = split(root)
            result = subprocess.run([sys.executable, str(ROOT / "scripts/record_catalog.py"),
                                     p.name, "--root", str(root), "--stdout"],
                                    cwd=parent, capture_output=True, check=False)
            equal(result.returncode, 0)
            equal(result.stdout, expected.encode())

        def cycle(root):
            (root / "a.obligations.sexp").write_text(include("contract-obligations.sexp"))
            refused(root, include("a.obligations.sexp"), "INCLUDE-CYCLE")

        def duplicate(root):
            (root / "a.obligations.sexp").write_text(R.dump([record("OB-A")]))
            refused(root, include("a.obligations.sexp") * 2, "DUPLICATE-PART")

        def escape(root):
            outside = parent / "outside.obligations.sexp"
            outside.write_text(R.dump([record("OB-A")]))
            (root / "link.obligations.sexp").symlink_to(outside)
            refused(root, include("link.obligations.sexp"), "INCLUDE-ESCAPE")

        def nonrecord(root):
            (root / "bad.obligations.sexp").write_text('(requirements)\n')
            refused(root, include("bad.obligations.sexp"), "PART-FORM")

        def symlink_cycle(root):
            (root / "loop.obligations.sexp").symlink_to("loop.obligations.sexp")
            # Python/platform versions detect the loop during resolve or open.
            refused(root, include("loop.obligations.sexp"), ("PATH-RESOLUTION", "UNREADABLE-PART"))

        def crlf(root):
            source = b'; intact\r\n(comment "valid")\r\n'
            p = root / "contract-obligations.sexp"
            p.write_bytes(source)
            equal(C.text(p, root=root).encode(), source)

        # A deliberate loss of expansion must make this same suite RED.
        original = C.text
        with patch.object(C, "text", (lambda path, **kw: Path(path).read_text())
                          if mutation == "ignore-includes" else original):
            arm("flat bytes and mapping", flat)
            arm("two-part exact stream, order, origins and mapping", expansion)
            arm("nested expansion", nested)
            arm("relocation", relocation)
            arm("quoted/multiline directives and comments", lexical)
            arm("reserved annotations and schema authority", annotations)
            arm("included invalid record has part origin", included_schema)
            arm("public CLI outside fixture root", cli)
            arm("missing part", lambda r: refused(r, include("absent.obligations.sexp"), "UNREADABLE-PART"))
            arm("cycle", cycle)
            arm("duplicate part", duplicate)
            arm("symlink escape", escape)
            arm("symlink cycle has a named refusal", symlink_cycle)
            arm("part contains non-record", nonrecord)
            arm("flat CRLF bytes", crlf)
            for path in ("", "../escape", "/absolute", "a/../b", "./a", "a//b", "a/",
                         "C:/windows", "a\\b", "a\nb"):
                arm(f"noncanonical path {path!r}",
                    lambda r, value=path: refused(r, include(value), "INCLUDE-PATH"))
            for source in ('(include-obligations)', '(include-obligations (path bare))',
                           '(include-obligations (path "a") (path "b"))',
                           '("include-obligations" (path "a"))',
                           '(include-obligations ("path" "a"))'):
                arm("malformed include", lambda r, value=source: refused(r, value, "INCLUDE-SHAPE"))
            arm("wrong catalog family", lambda r: refused(
                r, include("absent.obligations.sexp"), "INCLUDE-FAMILY", filename="requirements.sexp"))
        assert ran == 31, f"harness ran {ran} controls, expected 31"
    for failure in failures:
        print(f"RECORD-CATALOG-CONTROLS: CONTROL-MISSED — {failure}", file=sys.stderr)
    print(f"RECORD-CATALOG-CONTROLS: {ran - len(failures)} pass / {len(failures)} fail")
    return int(bool(failures))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=("ignore-includes",))
    sys.exit(run(parser.parse_args().mutation))
