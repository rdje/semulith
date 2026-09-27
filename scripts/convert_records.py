#!/usr/bin/env python3
"""Convert record catalogues between JSON Lines and the one format, and prove the round-trip.

`SOT-FORMAT.3` moved the profile's requirement and obligation catalogues behind the schema
layer. This tool drove that migration and owns its proof:

  convert_records.py --to-sexp  <records.jsonl> <out.sexp>   # one migration direction
  convert_records.py --to-jsonl <records.sexp> <out.jsonl>   # the other
  convert_records.py --verify   <records.jsonl> <records.sexp>
                               # losslessness, MECHANICALLY: the sexp re-derived to JSONL must
                               # equal the source file byte for byte (keys, order, values)

LOSSLESSNESS IS A COMPARISON, NOT A REVIEW. `--verify` re-dumps every record with the canonical
serializer (`json.dumps(..., ensure_ascii=False)`, the shape these files already had) and diffs
bytes; a field dropped, renamed, reordered or retyped fails here before any gate could.

Usage: the <records.jsonl> kind is taken from its basename (requirements / contract-obligations);
the output carries a header comment naming the schema that governs it.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sexp as S                                # noqa: E402
import records_sexp as R                        # noqa: E402

REPO = Path(__file__).resolve().parent.parent

HEADERS = {
    "requirements": ("requirements.sexp", "schema/requirements.sexp",
                     "the requirement catalogue"),
    "contract-obligations": ("contract-obligations.sexp", "schema/contract-obligations.sexp",
                             "the CPU/environment contract obligation catalogue"),
}


def _kind(path: Path) -> str:
    for stem in HEADERS:
        if path.name == f"{stem}.jsonl" or path.name == f"{stem}.sexp":
            return stem
    raise SystemExit(f"REFUSED: {path.name} is not a known record file "
                     f"({', '.join(HEADERS)})")


def _read_jsonl(path: Path) -> list[dict]:
    records = []
    for lineno, raw in enumerate(path.read_text().splitlines(), 1):
        if not raw.strip():
            continue
        try:
            records.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"REFUSED: {path}:{lineno}: not valid JSON — {exc}")
    if not records:
        raise SystemExit(f"REFUSED: {path} holds no records")
    return records


def _to_sexp(src: Path, out: Path) -> None:
    kind = _kind(src)
    records = _read_jsonl(src)
    _, schema_rel, what = HEADERS[kind]
    header = (f";; {HEADERS[kind][0]} — {what}, converted from {src.name} by\n"
              f";; scripts/convert_records.py (SOT-FORMAT.3). One record per form; validate with\n"
              f";;   python3 scripts/check_sexp_schema.py {HEADERS[kind][0]} {schema_rel}\n"
              f";; Round-trip losslessness: `convert_records.py --verify {src.name} "
              f"{HEADERS[kind][0]}`.\n")
    text = header + "\n" + R.dump(records)
    out.write_text(text)
    print(f"wrote {out} ({len(records)} record(s), {len(text.encode())} bytes)")


def _to_jsonl(src: Path, out: Path) -> None:
    _kind(src)
    try:
        forms = S.read_file(src)
    except S.SexpError as exc:
        raise SystemExit(f"REFUSED: {src}: does not parse — {exc}")
    if not forms:
        raise SystemExit(f"REFUSED: {src} holds no forms")
    try:
        records = [R.form_to_dict(f) for f in forms]
    except (R.RecordRefused, S.SexpError) as exc:
        raise SystemExit(f"REFUSED: {src}: {exc}")
    lines = [json.dumps(r, ensure_ascii=False) for r in records]
    out.write_text("".join(l + "\n" for l in lines))
    print(f"wrote {out} ({len(records)} record(s))")


def _verify(jsonl: Path, sexp: Path) -> int:
    kind = _kind(jsonl)
    source = jsonl.read_text()
    records = _read_jsonl(jsonl)
    try:
        forms = S.read_file(sexp)
        back = [R.form_to_dict(f) for f in forms]
        re_dumped = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in back)
    except (S.SexpError, R.RecordRefused) as exc:
        print(f"ROUND-TRIP FAIL: {sexp}: {exc}")
        return 1
    if len(back) != len(records):
        print(f"ROUND-TRIP FAIL: {len(records)} record(s) in {jsonl.name}, "
              f"{len(back)} form(s) in {sexp.name}")
        return 1
    for i, (a, b) in enumerate(zip(records, back)):
        if a != b:
            for key in a:
                if a.get(key) != b.get(key):
                    print(f"ROUND-TRIP FAIL: record {i} ({a.get('id')}): field {key!r}: "
                          f"{a.get(key)!r} != {b.get(key)!r}")
                    return 1
            print(f"ROUND-TRIP FAIL: record {i}: fields added: "
                  f"{sorted(set(b) - set(a))}")
            return 1
    if re_dumped != source:
        for i, (a, b) in enumerate(zip(source.splitlines(), re_dumped.splitlines())):
            if a != b:
                print(f"ROUND-TRIP FAIL: byte drift at line {i + 1}:\n  src: {a}\n  got: {b}")
                return 1
        print("ROUND-TRIP FAIL: byte counts differ "
              f"({len(source.splitlines())} vs {len(re_dumped.splitlines())} lines)")
        return 1
    print(f"round-trip ok: {len(records)} {kind} record(s), "
          f"field-by-field equal and byte-identical on re-dump")
    return 0


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

    REQ = {"id": "REQ-T", "profile_ids": ["p"], "kind": "state", "statement": "S",
           "source_refs": [{"source_id": "SRC", "locator": "§1"}],
           "applicability": "included", "research_status": "resolved",
           "implementation_status": "planned",
           "source_semantics": {"category": "defined", "detail": "d"},
           "risk": "low", "obligation_ids": ["OB-T"], "dependencies": [],
           "implementation_refs": [], "evidence_ids": []}
    OB = {"id": "OB-T", "contract_id": "c", "contract_version": "0", "profile_ids": ["p"],
          "direction": "cpu-guarantee", "statement": "S", "authority": "architecture",
          "source_refs": [{"source_id": "SRC", "locator": "§1"}],
          "parameters": {"ints_p": [8, 16], "strs_p": ["cold"], "empty": [], "n": 0,
                         "s": "2^64", "t": True, "f": False, "z": None},
          "dependencies": [], "required_checks": ["CHK-T-POS", "CHK-T-NEG"]}

    def eq(x, y): assert x == y, f"got {x!r}, want {y!r}"

    arm("GREEN a requirement round-trips through form and back",
        lambda: eq(R.form_to_dict(R.dict_to_form(REQ)), REQ))
    arm("GREEN an obligation round-trips, heterogeneous parameters intact",
        lambda: eq(R.form_to_dict(R.dict_to_form(OB)), OB))
    arm("GREEN empty lists become absence and return as empty lists",
        lambda: (
            eq(all(not (isinstance(c, list) and c and c[0] == "dependencies")
                   for c in R.dict_to_form(REQ)[1:]), True),
            eq(R.form_to_dict(R.dict_to_form(REQ))["dependencies"], []),
            eq(R.form_to_dict(R.dict_to_form(OB))["parameters"]["empty"], [])))
    arm("GREEN rendering escapes quotes, backslashes and newlines, and re-parses equal",
        lambda: (
            (lambda line: (
                eq('\\"' in line, True), eq("\\\\" in line, True), eq("\\n" in line, True),
                eq(S.parse(line), [R.dict_to_form({**REQ, "statement": 'a"b\\c\nd'})])))(
                R.render_forms([R.dict_to_form({**REQ, "statement": 'a"b\\c\nd'})]))))
    arm("GREEN dict key order survives — re-dumped JSONL is byte-identical",
        lambda: (
            eq(json.dumps(R.form_to_dict(R.dict_to_form(REQ)), ensure_ascii=False),
               json.dumps(REQ, ensure_ascii=False)),
            eq(json.dumps(R.form_to_dict(R.dict_to_form(OB)), ensure_ascii=False),
               json.dumps(OB, ensure_ascii=False))))
    arm("RED   a float parameter is refused, not truncated",
        lambda: (_raised(lambda: R.dict_to_form({**OB, "parameters": {"x": 1.5}})),
                 None)[1])
    arm("RED   a mixed list parameter is refused by name",
        lambda: (_raised(lambda: R.dict_to_form({**OB, "parameters": {"x": [1, "a"]}})),
                 None)[1])
    arm("RED   a nested value is refused by name",
        lambda: (_raised(lambda: R.dict_to_form({**OB, "parameters": {"x": {"y": 1}}})), None)[1])
    arm("RED   an unknown record dict is refused",
        lambda: (_raised(lambda: R.dict_to_form({"mystery": 1})), None)[1])

    print(f"convert_records --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


def _raised(fn) -> None:
    try:
        fn()
    except R.RecordRefused:
        return
    raise AssertionError("expected RecordRefused, got none")


def main(argv: list[str]) -> int:
    if "--self-test" in argv[1:]:
        return _selftest()
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("to-sexp", "to-jsonl", "verify"):
        sp = sub.add_parser(name)
        sp.add_argument("src")
        sp.add_argument("dst")
    args = ap.parse_args(argv[1:])
    src, dst = Path(args.src), Path(args.dst)
    if args.cmd == "to-sexp":
        _to_sexp(src, dst)
        return 0
    if args.cmd == "to-jsonl":
        _to_jsonl(src, dst)
        return 0
    return _verify(src, dst)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
