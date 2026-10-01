#!/usr/bin/env python3
"""Generate the per-unit model book's materials fragments (`MODEL-BOOKS.1`).

`docs/models/<unit-id>/src/materials/*.md` are GENERATED (the `gen_guests.py` /
`gate_report.py` pattern; OWN-03: generated artifacts change by regeneration, never by
direct editing, and identify their canonical inputs, generator, configuration and source
fingerprints). The generator lowers the unit's PINNED dossier into four markdown
fragments the materials chapter includes:

- `pinned-specifications.md` — the specification artifacts, from `sources.sexp`;
- `encoding-tables.md` — the encoding source and its pinned files, from
  `references.sexp`'s `encoding_source` record;
- `reference-models.md` — the reference candidates, from `references.sexp`;
- `internal-contracts.md` — the dossier's own documents, with their record counts
  DERIVED from the tracked files (a count is enumerated, never retyped).

The point of the leaf is that a digest cannot rot: every identity field in these tables
is read out of the pinned data at generation time, and the `MATERIALS-BILL` doctrine
(`scripts/check_materials_bill.sh`) regenerates in memory and refuses drift. What the
generator does NOT emit is the prose — what a material is FOR, and what it does not
supply — which is authored in `src/materials.md` around the includes.

The generator REFUSES, by name, what it cannot emit: a missing dossier document, a
record that does not map. A generator that guesses is a second definition.

usage: gen_model_book.py [--check] [--unit ID] [--profile-dir PATH] [--book-dir PATH]
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import dossier_sexp as D                           # noqa: E402
import records_sexp as R                           # noqa: E402
import sexp as S                                   # noqa: E402

REPO = Path(__file__).resolve().parent.parent
GENERATOR = Path(__file__)
FRAGMENTS = ("pinned-specifications.md", "encoding-tables.md", "reference-models.md",
             "internal-contracts.md")
# The internal contracts the bill covers — the one list, consumed by the generator AND by
# the MATERIALS-BILL gate's completeness check (a section per entry, each with its
# does-not-supply statement).
INTERNAL_CONTRACTS = ("profile.sexp", "state.sexp", "encoding.sexp", "requirements.sexp",
                      "contract-obligations.sexp", "guests/", "interactions.sexp")


class GenError(Exception):
    """A refusal: the fragments cannot be emitted from what the repository declares."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return str(path)


def _load(loader, path: Path) -> dict:
    if not path.is_file():
        raise GenError(f"{rel(path)}: the pinned document is missing")
    try:
        return loader(path)
    except D.DossierError as exc:
        raise GenError(f"{rel(path)}: does not map — {exc}") from exc


def _vehicle_route(profile_dir: Path) -> str | None:
    """The unit's declared vehicle route (P3-BREADTH.7): applicability derives from the
    declaration (`decision_gate-applicability-by-declared-vehicle`), never from a guess."""
    path = profile_dir / "profile.sexp"
    if not path.is_file():
        return None
    vehicle = _load(D.load_profile, path).get("vehicle") or {}
    route = vehicle.get("route")
    return str(route) if route is not None else None


def _bytes(n: int) -> str:
    return f"{n:,}"


def _header(inputs: list[Path]) -> list[str]:
    a = ["<!-- GENERATED — do not edit (OWN-03). Regenerate with",
         "     `python3 scripts/gen_model_book.py`; drift between this fragment and the",
         "     pinned dossier is refused by the MATERIALS-BILL doctrine",
         "     (`scripts/check_materials_bill.sh`). -->",
         "<!-- Canonical inputs (sha256):"]
    for p in inputs:
        a.append(f"     `{rel(p)}`  `{sha256(p)}`")
    a.append(f"     Generator: `scripts/gen_model_book.py` (sha256 `{sha256(GENERATOR)}`) -->")
    a.append("")
    return a


# --------------------------------------------------------------------------- the fragments

def emit_specifications(sources_path: Path) -> str:
    doc = _load(D.load_sources, sources_path)
    a = _header([sources_path])
    a.append(f"Pinned publication: **{doc['publication']}**, revision "
             f"`{doc['revision']}`, retrieved {doc['retrieved']} — explicitly NOT "
             f"{doc['not_this_publication']}.")
    a.append("")
    a.append("| ID | Document | Chapter version | Pinned artifact | sha256 | Bytes | HTTP |")
    a.append("| --- | --- | --- | --- | --- | --- | --- |")
    for s in doc["source"]:
        a.append(f"| `{s['id']}` | {s['title']} | {s.get('chapter_version', '—')} | "
                 f"`{s['file']}` | `{s['sha256']}` | {_bytes(s['bytes'])} | "
                 f"{s['http_status']} |")
    a.append("")
    a.append("What each supplies, as recorded in the pinned ledger:")
    a.append("")
    for s in doc["source"]:
        a.append(f"- **`{s['id']}`** — {s['supplies']}")
    a.append("")
    return "\n".join(a)


def emit_encoding(profile_dir: Path) -> str:
    references_path = profile_dir / "references.sexp"
    doc = _load(D.load_references, references_path)
    encs = doc.get("encoding_source", [])
    if len(encs) != 1:
        # case dsp56300-lab-v0 (P3-BREADTH.6 slice 2): no encoding_source record exists
        # because the encoding's home is the sibling crate — the DECLARED vehicle. The
        # fragment says so honestly; without the declaration the refusal stands.
        if not encs and _vehicle_route(profile_dir) == "sibling-crate":
            a = _header([references_path, profile_dir / "profile.sexp"])
            a.append("This unit declares its vehicle as `(route sibling-crate)`: the "
                     "encoding space has no `encoding_source` record because it lives in "
                     "the sibling crate's hand-written decoder — every mask is cited per "
                     "form to the pinned family manual and cross-checked against the "
                     "pinned assembler (`crates/semulith-dsp56300`).")
            a.append("")
            a.append("There is no `encoding.sexp`: the encoding/definition generalization "
                     "was measured a lane, not an extension (24-bit decode emission, a DSP "
                     "fragment family, semantics as data — `P3-BREADTH.5` slice 3), and is "
                     "deferred with named reopening conditions; no current milestone "
                     "consumes it (`decision_lane-consumption`).")
            a.append("")
            return "\n".join(a)
        raise GenError(f"{rel(references_path)}: expected exactly one encoding_source "
                       f"record, found {len(encs)}")
    enc = encs[0]
    a = _header([references_path])
    a.append(f"Encoding source **`{enc['id']}`** — {enc['origin']} ({enc['license']}), "
             f"retrieved {enc['retrieved']} into `{enc['work_dir']}/`.")
    a.append("")
    a.append(f"Supplies: {enc['supplies']}")
    a.append("")
    a.append("| Pinned file | sha256 | Bytes |")
    a.append("| --- | --- | --- |")
    for f in enc["file"]:
        a.append(f"| `{f['name']}` | `{f['sha256']}` | {_bytes(f['bytes'])} |")
    a.append("")
    return "\n".join(a)


def emit_references(references_path: Path) -> str:
    doc = _load(D.load_references, references_path)
    a = _header([references_path])
    a.append("| ID | Role | Status | Kind | Version | sha256 | Terms |")
    a.append("| --- | --- | --- | --- | --- | --- | --- |")
    for c in doc["candidate"]:
        version = c.get("release") or c.get("version") or "—"
        digest = c.get("binary_sha256") or c.get("asset_sha256") or "—"
        terms = c.get("terms") or c.get("license") or "—"
        a.append(f"| `{c['id']}` | {c['role']} | {c['status']} | {c.get('kind', '—')} | "
                 f"{version} | {digest if digest == '—' else f'`{digest}`'} | {terms} |")
    a.append("")
    a.append("How each is invoked when exercised, as recorded:")
    a.append("")
    for c in doc["candidate"]:
        if c.get("invocation"):
            a.append(f"- **`{c['id']}`** — `{c['invocation']}`")
        else:
            a.append(f"- **`{c['id']}`** — not exercised; no invocation exists "
                     f"({c['status']})")
    a.append("")
    return "\n".join(a)


def _count_records(path: Path) -> int:
    if not path.is_file():
        raise GenError(f"{rel(path)}: the catalogue is missing")
    try:
        return len(R.load(path))
    except (R.RecordRefused, S.SexpError) as exc:
        raise GenError(f"{rel(path)}: does not map — {exc}") from exc


def emit_contracts(profile_dir: Path) -> str:
    profile_path = profile_dir / "profile.sexp"
    reqs_path = profile_dir / "requirements.sexp"
    obs_path = profile_dir / "contract-obligations.sexp"
    enc_path = profile_dir / "encoding.sexp"
    inputs = [profile_dir / n for n in INTERNAL_CONTRACTS if not n.endswith("/")]
    # case dsp56300-lab-v0 (P3-BREADTH.6 slice 2): encoding.sexp is the ONE document a
    # unit may lack — the encoding generalization is a deferred lane and the sibling
    # crate is the declared vehicle. The table ROW below names the absence; any other
    # missing document stays a refusal.
    for p in inputs:
        if not p.is_file() and not (p.name == "encoding.sexp"
                                    and _vehicle_route(profile_dir) == "sibling-crate"):
            raise GenError(f"{rel(p)}: the dossier document is missing")
    inputs = [p for p in inputs if p.is_file()]
    prof = _load(D.load_profile, profile_path)
    state = _load(D.load_state, profile_dir / "state.sexp")
    iregs = state.get("integer_registers")
    hidden = state.get("hidden_state_census", {}).get("answer", "—")
    composed: list[str] = []
    if enc_path.is_file():
        enc = S.read_file(enc_path)[0]
        comp = S.children(enc, "compose")
        if len(comp) != 1:
            raise GenError(f"{rel(enc_path)}: expected one compose form")
        base = str(S.field(comp[0], "base", "encoding.sexp"))
        ext = S.children(comp[0], "extensions")
        composed = [base] + [str(x) for x in (ext[0][1:] if ext else [])]
    n_reqs = _count_records(reqs_path)
    obs = R.load(obs_path)
    n_checks = sum(len(o["required_checks"]) for o in obs)
    interactions = S.read_file(profile_dir / "interactions.sexp")[0]
    n_cells = len(S.children(interactions, "cell"))
    n_axes = len(S.children(interactions, "axis"))
    guests = sorted((profile_dir / "guests").glob("*.expected.sexp"))
    steps = sum(len(D.load_expectations(g)["step"]) for g in guests)
    guests_a56 = sorted((profile_dir / "guests").glob("*.a56"))
    forms = prof["scope"]["count_total"]

    a = _header(inputs)
    a.append("| Document | Role | Derived contents |")
    a.append("| --- | --- | --- |")
    a.append(f"| `profile.sexp` | the unit's declaration: scope, decisions, authorities | "
             f"{len(prof['decision'])} decisions, {forms} declared instruction forms |")
    if iregs is not None:
        a.append(f"| `state.sexp` | the architectural-state census, including the hidden-state "
                 f"census | {iregs['count']} integer registers, XLEN {iregs['width_bits']}, "
                 f"hidden state: {hidden} |")
    else:
        # case dsp56300-lab-v0: the register census is families with masked widths and
        # per-part readouts, not an x0-anchored integer file (P3-BREADTH.5 slice 1).
        families = len(state.get("register_family", []))
        spaces = len(state.get("memory_spaces", []))
        stack = ("the hardware stack declared" if state.get("hardware_stack")
                 else "no hardware stack")
        a.append(f"| `state.sexp` | the architectural-state census, including the hidden-state "
                 f"census | {families} register families (masked widths, per-part readouts), "
                 f"{spaces} memory spaces, {stack}, hidden state: {hidden} |")
    if enc_path.is_file():
        a.append(f"| `encoding.sexp` | the composed encoding space (fragments resolved, "
                 f"collision-free, gated by UNIT-COMPOSITION) | composes "
                 f"{', '.join(f'`{c}`' for c in composed)} |")
    else:
        a.append("| `encoding.sexp` | DEFERRED — the encoding/definition generalization was "
                 "measured a lane, not an extension (`P3-BREADTH.5` slice 3); the sibling "
                 "crate is the declared, exercised vehicle | no document — the reopening "
                 "conditions are named in the tree |")
    a.append(f"| `requirements.sexp` | the predeclared requirements, one per decision "
             f"(RECORD-SCHEMA cross-checks the statements verbatim) | {n_reqs} requirements |")
    a.append(f"| `contract-obligations.sexp` | the environment contract "
             f"(`{obs[0]['contract_id']}`): every obligation with positive AND negative "
             f"checks | "
             f"{len(obs)} obligations, {n_checks} declared checks |")
    if guests:
        a.append(f"| `guests/` | the EVD-05 guest corpus: independently encoded programs and "
                 f"specification-derived expectations | {len(guests)} guests, "
                 f"{steps} expected steps |")
    else:
        # case dsp56300-lab-v0: the corpus is checkpoint-compared .a56 guests (canonical
        # end-state dumps), not per-step expectation documents.
        a.append(f"| `guests/` | the synthetic guest corpus: checkpoint-compared `.a56` "
                 f"programs, canonical end-state dumps against the pinned reference "
                 f"(`cyc` never compared) | {len(guests_a56)} guests |")
    a.append(f"| `interactions.sexp` | the declared interaction matrix (P2-SCALAR.4), "
             f"gated by INTERACTION-MATRIX | {n_cells} cells over {n_axes} axes |")
    a.append("")
    return "\n".join(a)


EMITTERS = {
    "pinned-specifications.md": lambda pd: emit_specifications(pd / "sources.sexp"),
    "encoding-tables.md": emit_encoding,
    "reference-models.md": lambda pd: emit_references(pd / "references.sexp"),
    "internal-contracts.md": emit_contracts,
}


def generate(profile_dir: Path) -> dict[str, str]:
    return {name: emitter(profile_dir) for name, emitter in EMITTERS.items()}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="regenerate in memory and report drift instead of writing")
    parser.add_argument("--unit", default="rv64i-lab-v0")
    parser.add_argument("--profile-dir", type=Path, default=None)
    parser.add_argument("--book-dir", type=Path, default=None)
    args = parser.parse_args(argv)

    profile_dir = args.profile_dir or REPO / "profiles" / args.unit
    book_dir = args.book_dir or REPO / "docs" / "models" / args.unit
    try:
        fragments = generate(profile_dir)
    except (GenError, S.SexpError) as exc:
        print(f"gen_model_book: REFUSED — {exc}", file=sys.stderr)
        return 2

    out_dir = book_dir / "src" / "materials"
    if args.check:
        stale = [name for name, text in fragments.items()
                 if not (out_dir / name).is_file() or (out_dir / name).read_text() != text]
        if stale:
            print(f"gen_model_book: DRIFT — {', '.join(sorted(stale))} no longer match "
                  f"the pinned dossier.", file=sys.stderr)
            return 1
        print(f"gen_model_book: ok ({len(fragments)} fragments match the pinned dossier)")
        return 0
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, text in fragments.items():
        (out_dir / name).write_text(text)
    print(f"gen_model_book: wrote {len(fragments)} fragments under {rel(out_dir)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
