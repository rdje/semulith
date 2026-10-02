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

`P5-BOARD.11` (2026-10-02): the emission is keyed on the unit's DECLARED shape
(`unit_shape` — the vehicle route for profile-bearing units, `board.sexp` for a board):
the internal-contracts census is per-shape (`shape_contracts`), and the encoding /
reference / specification fragments carry route-honest content for shapes that have no
encoding space or reference candidates by declaration. An undeclared absence stays a
refusal.

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
# `P5-BOARD.11` (2026-10-02): the census is per-SHAPE, derived from the unit's own
# declaration (unit_shape), never from a guess. A device dossier carries expectations/
# instead of the processor's guests/ + interactions.sexp and has no encoding space at
# all; a board dossier is the canonical definition plus its narrative.
DEVICE_CONTRACTS = ("profile.sexp", "state.sexp", "requirements.sexp",
                    "contract-obligations.sexp", "expectations/")
BOARD_CONTRACTS = ("board.sexp", "DOSSIER.md")


def unit_shape(profile_dir: Path) -> str:
    """The unit's dossier shape, derived from its DECLARATION (P5-BOARD.11): a board
    dossier carries board.sexp (and no profile.sexp); any other unit's shape is its
    profile's declared vehicle route (decision_gate-applicability-by-declared-vehicle),
    defaulting to the processor shape. Public: the MATERIALS-BILL gate keys on it too."""
    if (Path(profile_dir) / "board.sexp").is_file():
        return "board"
    route = _vehicle_route(profile_dir)
    return route if route in ("sibling-crate", "device-model") else "processor"


def shape_contracts(shape: str) -> tuple[str, ...]:
    return {"device-model": DEVICE_CONTRACTS,
            "board": BOARD_CONTRACTS}.get(shape, INTERNAL_CONTRACTS)


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

def emit_specifications(profile_dir: Path) -> str:
    # P5-BOARD.11: the board unit pins its inputs in board.sexp, not a sources.sexp —
    # the processor by unit id + version + dossier digest, each device by its
    # datasheet's material id + revision + sha256 (versions, not names — P5-BOARD.1).
    board_path = profile_dir / "board.sexp"
    if board_path.is_file():
        doc = S.read_file(board_path)[0]
        proc = S.children(doc, "processor")[0]
        a = _header([board_path])
        a.append("A board has no specification of its own: it **composes** pinned units. "
                 "The canonical definition pins versions, not names — the processor by unit "
                 "id + version + the GATE-REPORT-gated dossier content digest, each device "
                 "by its datasheet's material id + revision + sha256.")
        a.append("")
        a.append("| Pin | Identity | Revision / version | sha256 |")
        a.append("| --- | --- | --- | --- |")
        a.append(f"| processor | `{S.field(proc, 'unit', board_path)}` v"
                 f"{S.field(proc, 'version', board_path)} (contract "
                 f"`{S.field(proc, 'contract', board_path)}` v"
                 f"{S.field(proc, 'contract-version', board_path)}) | the unit's dossier | "
                 f"`{S.field(proc, 'dossier-sha256', board_path)}` |")
        for d in S.children(doc, "device"):
            a.append(f"| device `{S.field(d, 'id', board_path)}` "
                     f"(unit `{S.field(d, 'unit', board_path)}`) | "
                     f"**{S.field(d, 'material', board_path)}** | "
                     f"{S.field(d, 'revision', board_path)} | "
                     f"`{S.field(d, 'sha256', board_path)}` |")
        a.append("")
        return "\n".join(a)
    doc = _load(D.load_sources, profile_dir / "sources.sexp")
    a = _header([profile_dir / "sources.sexp"])
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
    # P5-BOARD.11: shapes with no encoding space, by declaration, before any load —
    # a device has no instruction encodings (its register map is the contract), and a
    # board composes its processor's encoding rather than adding one.
    shape = unit_shape(profile_dir)
    if shape == "device-model":
        a = _header([profile_dir / "profile.sexp"])
        a.append("This unit declares its vehicle as `(route device-model)`: there is no "
                 "encoding space because a device has no instructions — its **register map** "
                 "is the contract, dossiered as requirement records with the datasheet's "
                 "locators (`profiles/` … `requirements.sexp`), and its evidence shape is "
                 "datasheet-derived register-read expectations, not encoded guest programs.")
        a.append("")
        return "\n".join(a)
    if shape == "board":
        a = _header([profile_dir / "board.sexp"])
        a.append("A board adds no encoding space: the instruction encodings a guest can "
                 "execute are exactly its processor's — pinned by unit id + version + "
                 "dossier digest in `board.sexp` and billed in the processor unit's own "
                 "book. The board's contract surface is the memory map, the device windows "
                 "and the declared absences.")
        a.append("")
        return "\n".join(a)
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


def emit_references(profile_dir: Path) -> str:
    # P5-BOARD.11: devices and boards pin no reference candidates — recorded by
    # declaration, not by an absent file discovered mid-load.
    shape = unit_shape(profile_dir)
    if shape == "device-model":
        a = _header([profile_dir / "profile.sexp"])
        a.append("This unit pins **no reference models**: it declares `(comparison "
                 "register-expectations)` — the comparison surface is the dossier's own "
                 "datasheet-derived register-read expectations (`expectations/`), recorded "
                 "before any model exists (EVD-05 at the device layer). A reference that "
                 "shares an ancestor with the datasheet would not be a second opinion; an "
                 "independent implementation may be pinned here the day one is acquired "
                 "through the materials channel.")
        a.append("")
        return "\n".join(a)
    if shape == "board":
        a = _header([profile_dir / "board.sexp"])
        a.append("A board pins no reference models of its own: the references that matter "
                 "are its processor's, standing behind the pinned dossier digest "
                 "(`board.sexp`), and its devices' datasheets, pinned as materials. The "
                 "composition's own evidence is `.4`'s verdict and `.5`'s probes — never a "
                 "reference implementation's say-so.")
        a.append("")
        return "\n".join(a)
    references_path = profile_dir / "references.sexp"
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
    # P5-BOARD.11: the census follows the unit's DECLARED shape — a device dossier and a
    # board dossier carry different documents than a processor dossier, and the table
    # says so honestly rather than refusing or pretending.
    shape = unit_shape(profile_dir)
    if shape == "device-model":
        return _emit_contracts_device(profile_dir)
    if shape == "board":
        return _emit_contracts_board(profile_dir)
    return _emit_contracts_processor(profile_dir)


def _emit_contracts_device(profile_dir: Path) -> str:
    profile_path = profile_dir / "profile.sexp"
    inputs = [profile_dir / n for n in DEVICE_CONTRACTS if not n.endswith("/")]
    for p in inputs:
        if not p.is_file():
            raise GenError(f"{rel(p)}: the dossier document is missing")
    inputs.append(profile_dir / "sources.sexp")
    prof = _load(D.load_profile, profile_path)
    state_root = S.read_file(profile_dir / "state.sexp")[0]
    n_regs = sum(len(S.children(sr, "register"))
                 for sr in S.children(state_root, "special_registers"))
    n_fams = len(S.children(state_root, "register_family"))
    census = S.children(state_root, "hidden_state_census")
    hidden = str(S.field(census[0], "answer", "state.sexp")) if census else "—"
    n_reqs = _count_records(profile_dir / "requirements.sexp")
    obs = R.load(profile_dir / "contract-obligations.sexp")
    n_checks = sum(len(o["required_checks"]) for o in obs)
    exp = sorted((profile_dir / "expectations").glob("*.expected.sexp"))
    steps = sum(len(D.load_expectations(g)["step"]) for g in exp)
    forms = prof["scope"]["count_total"]

    a = _header(inputs)
    a.append("| Document | Role | Derived contents |")
    a.append("| --- | --- | --- |")
    a.append(f"| `profile.sexp` | the unit's declaration: scope, decisions, authorities | "
             f"{len(prof['decision'])} decisions, {forms} declared scope registers |")
    a.append(f"| `state.sexp` | the device-state census, including the hidden-state "
             f"census | {n_regs} registers, {n_fams} FIFO families, hidden state: {hidden} |")
    a.append(f"| `requirements.sexp` | the predeclared requirements, one per decision "
             f"(RECORD-SCHEMA cross-checks the statements verbatim) | {n_reqs} requirements |")
    a.append(f"| `contract-obligations.sexp` | the device contract "
             f"(`{obs[0]['contract_id']}`): every obligation with positive AND negative "
             f"checks | {len(obs)} obligations, {n_checks} declared checks |")
    a.append(f"| `expectations/` | the EVD-05 register-read corpus: datasheet-derived "
             f"expectations recorded before any model exists | {len(exp)} documents, "
             f"{steps} expected steps |")
    a.append("")
    a.append("This unit declares `(route device-model)`: it carries no `encoding.sexp` "
             "(a device has no instruction encodings), no `guests/` corpus "
             "(the expectations are the corpus) and no `interactions.sexp` "
             "(INTERACTION-MATRIX derives the route from the declaration — the matrix "
             "attaches with the probe corpus, P5-BOARD.5). The absences are the shape, "
             "not gaps.")
    a.append("")
    return "\n".join(a)


def _emit_contracts_board(profile_dir: Path) -> str:
    board_path = profile_dir / "board.sexp"
    dossier_path = profile_dir / "DOSSIER.md"
    for p in (board_path, dossier_path):
        if not p.is_file():
            raise GenError(f"{rel(p)}: the dossier document is missing")
    doc = S.read_file(board_path)[0]
    proc = S.children(doc, "processor")[0]
    devices = S.children(doc, "device")
    mmap = S.children(doc, "memory-map")
    regions = S.children(mmap[0], "region") if mmap else []
    n_decisions = len(S.children(doc, "decision"))

    a = _header([board_path, dossier_path])
    a.append("| Document | Role | Derived contents |")
    a.append("| --- | --- | --- |")
    a.append(f"| `board.sexp` | the canonical board definition (schema `board.sexp`): "
             f"composition pins, memory map, reset, declared absences | processor "
             f"`{S.field(proc, 'unit', board_path)}` v{S.field(proc, 'version', board_path)}, "
             f"{len(devices)} devices, {len(regions)} memory regions, "
             f"{n_decisions} recorded board decisions |")
    a.append(f"| `DOSSIER.md` | the board's narrative — what the definition means and "
             f"what it does not claim | {_bytes(dossier_path.stat().st_size)} bytes |")
    a.append("")
    a.append("A board dossier carries no profile/requirements/obligations of its own: "
             "the CPU contract it must satisfy is its processor's, the device guarantees "
             "it relies on are its devices'. The composition verdict that matches them "
             "(`COMPOSITION-VERDICT.md`, P5-BOARD.4) is the unit's evidence — decided by "
             "the BOARD-VERDICT doctrine and included in the book's verdict chapter.")
    a.append("")
    return "\n".join(a)


def _emit_contracts_processor(profile_dir: Path) -> str:
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
    "pinned-specifications.md": emit_specifications,
    "encoding-tables.md": emit_encoding,
    "reference-models.md": emit_references,
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
