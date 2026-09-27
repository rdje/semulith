#!/usr/bin/env python3
"""Materialize a composition: unit parts -> one ordinary unit directory.

`MODEL-COMPOSE.5` — nesting: a composition is itself a unit. `computer -> board -> soc ->
{cpu, device}` uses ONE record shape at every level, which is only true if a board's records
are checked by the same code as a leaf unit's. That happens because the board directory is
not a new shape at all: this tool merges the parts with `merge_units(…)` — the same code the
verdicts consume — and derives an ordinary unit directory through the single mapping owners:

  requirements.sexp         records_sexp.dump  (merged, profile_ids keeping their origin units)
  contract-obligations.sexp records_sexp.dump  (merged; the discharge edges intact)
  sources.sexp              dossier_sexp.sources_to_form  (merged pins)
  encoding.sexp             derived when EXACTLY ONE part carries one

The board is then checked by the unchanged tools — merge_records self-merge,
discharge_assumptions, the UNIT-COMPOSITION read path — which is the acceptance, run: a
two-level composition checked by the same code as a one-level one.

⛔ REFUSES RATHER THAN RECONCILES. Zero parts, a missing part directory, more than one
ISA-carrying part (a multiprocessor needs the address-space operator the tree's open question
defers — refused by name until a real case earns it): each is a refusal naming the fact.

The freshness proof for a TRACKED board (manifest -> derived bytes, the gen_fragments
precedent) lands with the first tracked board; until then the derived directory is scratch
or advisory, and the ordinary gates cover it wherever it lives because it is ordinary corpus.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dossier_sexp as D                                # noqa: E402
import merge_records as M                               # noqa: E402
import records_sexp as R                                # noqa: E402
import sexp as S                                        # noqa: E402

REPO = Path(__file__).resolve().parent.parent
SCHEMA = REPO / "schema" / "composition.sexp"


class ComposeError(Exception):
    """A refusal: the manifest or the parts do not compose."""


def _schema_validate(path: Path) -> None:
    import check_sexp_schema as K
    try:
        constructs, operators = K.load_schema(SCHEMA)
        errors = K.validate_file(path, constructs, operators)
    except (K.SchemaError, S.SexpError) as exc:
        raise ComposeError(f"the composition schema itself does not read: {exc}")
    if errors:
        raise ComposeError(f"refused by schema/composition.sexp — " + "; ".join(errors))


def compose(manifest: Path, out_dir: Path) -> dict:
    """Derive the ordinary unit directory for a composition manifest. Returns a census.

    Part paths resolve against the MANIFEST's own directory, the way fragment-root
    resolves against its document — a composition names its parts relative to itself."""
    manifest = Path(manifest)
    _schema_validate(manifest)
    try:
        root = S.read_file(manifest)[0]
    except S.SexpError as exc:
        raise ComposeError(f"{manifest}: does not parse — {exc}")
    comp_id = str(S.field(root, "id"))
    # one (part …) per unit, each naming a single path: every child contributes
    parts = [str(x) for child in S.children(root, "part") for x in child[1:]]

    part_dirs = []
    for p in parts:
        d = (manifest.parent / p).resolve()
        if not d.is_dir():
            raise ComposeError(f"{manifest}: part '{p}' does not exist — a composition "
                               f"names what must be present")
        part_dirs.append(d)

    merged = M.merge_units(part_dirs)             # THE SAME CODE the verdicts consume

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    reqs = list(merged.requirements.values())
    obs = list(merged.obligations.values())
    (out / "requirements.sexp").write_text(R.dump(reqs))
    (out / "contract-obligations.sexp").write_text(R.dump(obs))
    sources_doc = {"publication": "derived: composed unit",
                   "revision": "derived",
                   "base_url": "derived",
                   "retrieved": "derived",
                   "work_dir": "derived",
                   "source": list(merged.sources.values())}
    (out / "sources.sexp").write_text(R.render_forms([D.sources_to_form(sources_doc)]))

    enc_parts = [d for d in part_dirs if (d / "encoding.sexp").is_file()]
    census = {"id": comp_id, "requirements": len(reqs), "obligations": len(obs),
              "sources": len(merged.sources), "encoding_from": None}
    if len(enc_parts) > 1:
        raise ComposeError(
            f"{manifest}: parts {', '.join(str(p) for p in enc_parts)} all "
            f"carry encoding.sexp — a multiprocessor needs the address-space assignment "
            f"operator (MODEL-COMPOSE's open question), refused until a real case earns it")
    if enc_parts:
        forms = S.read_file(enc_parts[0] / "encoding.sexp")
        enc = forms[0]
        for prof in S.children(enc, "profile"):
            prof[1] = comp_id                      # identity, not content
        (out / "encoding.sexp").write_text(R.render_forms([enc]))
        census["encoding_from"] = str(enc_parts[0])
    return census


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] == "--self-test":
        return _selftest()
    if len(argv) != 3:
        print("usage: compose_units.py <manifest.sexp> <out-dir>   |   compose_units.py "
              "--self-test", file=sys.stderr)
        return 2
    try:
        census = compose(Path(argv[1]), Path(argv[2]))
    except (ComposeError, M.MergeRefused) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    print(f"composed unit '{census['id']}': {census['requirements']} requirement(s), "
          f"{census['obligations']} obligation(s), {census['sources']} source(s)"
          + (f"; encoding derived from {census['encoding_from']}"
             if census["encoding_from"] else ""))
    print("the composition is an ordinary unit now — check it with the ordinary tools")
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
        except Exception as exc:                       # noqa: BLE001 — an arm must not abort
            print(f"  FAIL  {label}: unexpected {type(exc).__name__}: {exc}"); failed += 1
        else:
            print(f"  ok    {label}"); passed += 1

    root = Path("target/doctrine-selftest")
    root.mkdir(parents=True, exist_ok=True)
    tmp = Path(__import__("tempfile").mkdtemp(dir=root))

    def unit(name, reqs=(), obs=(), srcs=(), encoding=False):
        d = tmp / name
        d.mkdir(parents=True, exist_ok=True)
        if reqs:
            (d / "requirements.sexp").write_text(R.dump(list(reqs)))
        if obs:
            (d / "contract-obligations.sexp").write_text(R.dump(list(obs)))
        if srcs:
            (d / "sources.sexp").write_text(
                '(sources (publication "P") (revision "r") (base_url "u") (retrieved "d") '
                '(work_dir "w")\n' + "\n".join(
                    f'(source (id "{s}") (file "f.html") (title "t") (sha256 "{"a" * 64}") '
                    f'(bytes 1) (http_status 200) (supplies "s"))' for s in srcs) + ")\n")
        if encoding:
            (d / "encoding.sexp").write_text(
                '(encoding (profile "' + name + '") (ilen 32)\n'
                '  (compose (base "riscv/t-b") (extensions))\n'
                '  (fragment-root "definitions"))\n')
        return d

    def req(rid, profiles=("p",)):
        return {"id": rid, "profile_ids": list(profiles), "kind": "state", "statement": "s",
                "source_refs": [{"source_id": "S", "locator": "§1"}],
                "applicability": "included", "research_status": "resolved",
                "implementation_status": "planned",
                "source_semantics": {"category": "defined", "detail": "d"}, "risk": "low",
                "obligation_ids": [], "dependencies": [], "implementation_refs": [],
                "evidence_ids": []}

    def ob(oid, direction="cpu-guarantee", deps=()):
        return {"id": oid, "contract_id": "c", "contract_version": "0",
                "profile_ids": ["p"], "direction": direction, "statement": "s",
                "authority": "laboratory",
                "source_refs": [{"source_id": "S", "locator": "§1"}],
                "parameters": {}, "dependencies": list(deps), "required_checks": ["A-POS", "A-NEG"]}

    a = unit("cpu", reqs=[req("REQ-A")], obs=[ob("OB-G"), ob("OB-ENV", "environment-assumption",
                                                          deps=("OB-G",))], srcs=["S"],
             encoding=True)
    b = unit("dev", reqs=[req("REQ-B", profiles=("q",))], obs=[ob("OB-DEV")], srcs=["S"])

    def manifest(name, part_paths):
        p = tmp / name
        p.write_text("(composition (id \"board\") " +
                     " ".join(f'(part "{x}")' for x in part_paths) + ")\n")
        return p

    board = tmp / "board-out"

    def composes(parts):
        return compose(manifest("m.sexp", parts), board)

    arm("GREEN two parts materialize an ordinary unit dir",
        lambda: composes(["cpu", "dev"])["requirements"] == 2 or
                (_ for _ in ()).throw(AssertionError("count")))

    c = composes(["cpu", "dev"])
    arm("GREEN the census counts both parts' records",
        lambda: (_eq(c["obligations"], 3), _eq(c["sources"], 1)))

    # THE ACCEPTANCE, RUN: the derived board is checked by the same code, unmodified.
    m = M.merge_units([board, board])
    arm("GREEN the board self-merges through merge_units — the same code",
        lambda: _eq(len(m.requirements), 2))
    import discharge_assumptions as DA
    arm("GREEN the board discharges through discharge_assumptions — the same code",
        lambda: _eq(len(DA.discharge([board])), 1))
    arm("GREEN the derived encoding parses and names the composition",
        lambda: _eq(S.read_file(board / "encoding.sexp")[0][1][1], "board"))

    arm("RED   a manifest with no parts — the schema's min refuses it",
        lambda: _refuses(manifest("empty.sexp", []), board, "min is 1"))
    arm("RED   a part that does not exist",
        lambda: _refuses(manifest("ghost.sexp", ["cpu", "ghost"]), board, "'ghost' does not exist"))

    unit("cpu2", encoding=True)
    arm("RED   two ISA-carrying parts — the multiprocessor boundary, named",
        lambda: _refuses(manifest("mp.sexp", ["cpu", "cpu2"]), board,
                         "address-space assignment operator"))

    bad = tmp / "bad.sexp"
    bad.write_text("(composition (id \"x\") (widget \"y\") (part \"cpu\"))\n")
    arm("RED   an undeclared manifest field is refused by the schema layer",
        lambda: _refuses(bad, board, 'undeclared field "widget"'))

    import shutil
    shutil.rmtree(tmp)
    print(f"compose_units --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


def _refuses(manifest_path, out_dir, needle):
    try:
        compose(manifest_path, out_dir)
    except (ComposeError, M.MergeRefused) as exc:
        assert needle in str(exc), f"refused, but for the wrong reason: {exc}"
    else:
        raise AssertionError(f"composed; it must be refused ({needle})")


def _eq(got, want) -> None:
    assert got == want, f"got {got!r}, want {want!r}"


if __name__ == "__main__":
    sys.exit(main(sys.argv))
