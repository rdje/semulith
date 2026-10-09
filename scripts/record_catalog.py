#!/usr/bin/env python3
"""Expand explicit obligation-catalog parts without rewriting any record bytes.

Paths in include-obligations forms are repository-root-relative POSIX paths.
Only obligation catalogs may include parts; every part is used once, in order.
The canonical S-expression parser owns syntax, the schema owns record shape,
and records_sexp owns record mapping. This module owns only include expansion.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path, PurePosixPath

import sexp as S

ROOT = Path(__file__).resolve().parent.parent


class CatalogRefused(Exception):
    """A catalog include cannot be interpreted safely and exactly."""


def _resolved(path: Path) -> Path:
    try:
        return path.resolve()
    except (OSError, RuntimeError) as error:
        raise CatalogRefused(f"PATH-RESOLUTION: {path.name}: {error}") from error


def text(path: Path, *, root: Path | None = None,
         source_texts: dict[Path, str] | None = None) -> str:
    """Expand exactly; optionally collect original sources for schema validation."""
    anchor = _resolved(root or ROOT)
    seen: set[Path] = set()

    def expand(current: Path, stack: tuple[Path, ...], part: bool = False) -> str:
        current = _resolved(current)
        if current in stack:
            raise CatalogRefused(f"INCLUDE-CYCLE: {current.name}")
        if current in seen:
            raise CatalogRefused(f"DUPLICATE-PART: {current.name}")
        seen.add(current)
        try:
            with current.open(encoding="utf-8", newline="") as stream:
                source = stream.read()
        except (OSError, UnicodeError) as error:
            raise CatalogRefused(f"UNREADABLE-PART: {current.name}: {error}") from error
        if source_texts is not None:
            source_texts[current] = source
        forms = S.forms_with_spans(source, str(current))
        includes = [f for f, _, _ in forms if isinstance(f, list) and f
                    and f[0] == "include-obligations"]
        if includes and not (current.name == "contract-obligations.sexp"
                             or current.name.endswith(".obligations.sexp")):
            raise CatalogRefused(f"INCLUDE-FAMILY: {current.name} is not an obligation catalog")
        if includes or part:
            try:
                current.relative_to(anchor)
            except ValueError as error:
                raise CatalogRefused(f"CATALOG-ROOT: {current.name} is outside the selected root") from error
            for form, _, _ in forms:
                if not isinstance(form, list) or not form or form[0] not in {
                        "obligation", "comment", "include-obligations"}:
                    raise CatalogRefused(f"PART-FORM: {current.name} contains a non-obligation form")
        pieces, cursor = [], 0
        for form, start, end in forms:
            if not isinstance(form, list) or not form or form[0] != "include-obligations":
                continue
            if (not isinstance(form[0], S.Symbol) or len(form) != 2
                    or not isinstance(form[1], list) or len(form[1]) != 2
                    or not isinstance(form[1][0], S.Symbol)
                    or form[1][0] != "path" or type(form[1][1]) is not str):
                raise CatalogRefused("INCLUDE-SHAPE: expected one quoted path field")
            value = form[1][1]
            relative = PurePosixPath(value)
            if (not relative.parts or "\\" in value or any(ord(c) < 32 for c in value)
                    or relative.is_absolute()
                    or ".." in relative.parts or str(relative) != value
                    or re.match(r"^[A-Za-z]:", value)):
                raise CatalogRefused(f"INCLUDE-PATH: expected canonical repository-relative path: {value!r}")
            target = _resolved(anchor / value)
            try:
                target.relative_to(anchor)
            except ValueError as error:
                raise CatalogRefused(f"INCLUDE-ESCAPE: {value}") from error
            replacement = expand(target, (*stack, current), part=True)
            # An include normally occupies a line. Merge its existing newline
            # with the part's final newline, preserving the original stream.
            if replacement.endswith("\n") and source[end:end + 1] == "\n":
                replacement = replacement[:-1]
            pieces.extend((source[cursor:start], replacement))
            cursor = end
        pieces.append(source[cursor:])
        return "".join(pieces)

    try:
        return expand(Path(path), ())
    except RecursionError as error:
        raise CatalogRefused("INCLUDE-DEPTH: expansion exceeds the runtime recursion bound") from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--stdout", action="store_true", help="emit the exact expanded stream")
    args = parser.parse_args()
    try:
        catalog = args.catalog if args.catalog.is_absolute() else args.root / args.catalog
        expanded = text(catalog, root=args.root)
    except (CatalogRefused, S.SexpError) as error:
        print(f"RECORD-CATALOG: REFUSED — {error}", file=sys.stderr)
        return 1
    if args.stdout:
        sys.stdout.write(expanded)
    else:
        forms = S.parse(expanded)
        records = sum(isinstance(f, list) and bool(f) and f[0] == "obligation" for f in forms)
        print(f"RECORD-CATALOG: ok ({records} obligations, {len(expanded.encode())} expanded bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
