#!/usr/bin/env python3
"""Generate a board's maps, wiring and hardware description from its canonical definition.

`P5-BOARD.3` — OWN-05: a board definition composes exact processor/device versions and
GENERATES consistent maps and wiring; nothing downstream of `profiles/<board>/board.sexp`
is handwritten. Boards are discovered BY DECLARATION — any `profiles/*/board.sexp` — never
from a hardcoded id (the `unit_shape` idiom). Per board, from board.sexp alone, this
generator emits seven artifacts into the board's own directory:

  composition.sexp            the manifest — the part list derived from the processor +
                              device unit pins, never a handwritten duplicate of them
  requirements.sexp           \
  contract-obligations.sexp    |  the composed catalogues, materialized by
  sources.sexp                 |  compose_units.compose_resolved — the ONE code path the
  encoding.sexp               /   composition verdicts consume, imported, never re-implemented
  hardware.sexp               the hardware description (schema hardware.sexp): every region
                              resolved with its computed end; the wiring — device ↔ region ↔
                              access-widths ↔ interrupt-state ↔ backend; the console; the
                              reset; the declared absences with their satisfies edges; the
                              composition dispositions (board decisions carrying `answers`,
                              P5-BOARD.4) mirrored for the model route
  map.md                      the human-readable generated map (the DOSSIER links to it, the
                              unit book includes it — one owner, two readers)

The generator REFUSES, by name, rather than emitting a map with a hole: an unreadable or
schema-invalid board.sexp, a duplicate region name, an overlap between regions, an mmio
region naming no device or an undeclared one, a device no region serves, a ram region
naming a device, an executable mmio region (the fetch discipline — OB-ENV-FETCH-SUPPLY),
a zero-sized region, a serial console that is not a wired device, a part unit id with no
unit directory. Measured scope note (P5-BOARD.3): the design brief's register-surface
containment check is NOT implementable — the device dossiers carry register offsets in
prose with datasheet citations, not as machine-readable data — so the refusals are scoped
to what board.sexp itself proves; machine-readable offsets arrive with the device models.

`--check` re-derives every artifact in memory and refuses DRIFT, naming the artifact —
the freshness proof `compose_units.py` defers to the first tracked board. The BOARD-GEN
doctrine (`scripts/check_board_gen.sh`) runs it on every commit.

usage: gen_board.py [--check] [--board-dir PATH] [--out-dir PATH]
  --board-dir   one board only (default: every profiles/*/board.sexp)
  --out-dir     artifact destination (default: the board dir itself; scratch use is for
                the doctrine's self-test)
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_sexp_schema as K                      # noqa: E402
import compose_units as C                          # noqa: E402
import sexp as S                                   # noqa: E402

REPO = Path(__file__).resolve().parent.parent
BOARD_SCHEMA = REPO / "schema" / "board.sexp"
HARDWARE_SCHEMA = REPO / "schema" / "hardware.sexp"
COMPOSITION_SCHEMA = REPO / "schema" / "composition.sexp"
GENERATOR = Path(__file__).resolve()

COMPOSED = ("requirements.sexp", "contract-obligations.sexp", "sources.sexp",
            "encoding.sexp")
ARTIFACTS = ("composition.sexp",) + COMPOSED + ("hardware.sexp", "map.md")


class GenError(Exception):
    """A refusal: the board definition does not generate, by the fact named."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate(path: Path, schema: Path) -> None:
    try:
        constructs, operators = K.load_schema(schema)
        errors = K.validate_file(path, constructs, operators)
    except (K.SchemaError, S.SexpError) as exc:
        raise GenError(f"{path}: the schema layer itself cannot judge — {exc}")
    if errors:
        raise GenError(f"{path}: refused by {schema.name} — " + "; ".join(errors))


# --------------------------------------------------------------------------- the board, read

def parse_hex(text: str) -> int:
    return int(text.replace("_", ""), 16)


def fmt_hex(value: int) -> str:
    """The house hex style: 0x-prefixed, underscore-grouped nibble-quads, no padding."""
    digits = f"{value:x}"
    first = len(digits) % 4
    groups = [digits[:first]] if first else []
    groups += [digits[i:i + 4] for i in range(first, len(digits), 4)]
    return "0x" + "_".join(groups)


def _rel(path: Path) -> Path:
    """Repo-relative rendering for embedded fingerprints (DOCPATH: no absolute paths)."""
    try:
        return path.resolve().relative_to(REPO)
    except ValueError:
        return path


def _strings(form, name) -> list[str]:
    """Every value of every (name …) field on a form, in declaration order."""
    return [str(v) for child in S.children(form, name) for v in child[1:]]


def read_board(board_dir: Path) -> dict:
    path = board_dir / "board.sexp"
    if not path.is_file():
        raise GenError(f"{board_dir}: no board.sexp — a board is discovered by its "
                       f"declaration, and the declaration is missing")
    _validate(path, BOARD_SCHEMA)
    doc = S.read_file(path)[0]

    proc = S.children(doc, "processor")[0]
    devices = []
    for d in S.children(doc, "device"):
        backend = S.children(d, "backend")[0]
        devices.append({
            "id": str(S.field(d, "id")),
            "unit": str(S.field(d, "unit")),
            "kind": str(S.field(d, "kind")),
            # P5-BOARD.6: the datasheet pin — the platform manifest exports device
            # identity/revision (ARCHOGEN_INTEGRATION §3); gen_board's own renderers
            # do not consume them.
            "material": str(S.field(d, "material")),
            "revision": str(S.field(d, "revision")),
            "sha256": str(S.field(d, "sha256")),
            "access_widths": [int(w) for f in S.children(d, "access-widths")
                              for w in f[1:]],
            "interrupt": str(S.field(d, "interrupt")),
            "backend_rx": str(S.field(backend, "rx")),
            "backend_tx": str(S.field(backend, "tx")),
        })
    regions = []
    for r in S.children(S.children(doc, "memory-map")[0], "region"):
        device = S.children(r, "device")
        regions.append({
            "name": str(S.field(r, "name")),
            "base": parse_hex(str(S.field(r, "base"))),
            "size": parse_hex(str(S.field(r, "size"))),
            "kind": str(S.field(r, "kind")),
            "executable": str(S.field(r, "executable")) == "true",
            "device": str(device[0][1]) if device else None,
        })
    return {
        "dir": board_dir,
        "id": str(S.field(doc, "id")),
        "version": str(S.field(doc, "version")),
        "status": str(S.field(doc, "status")),
        "processor": {"unit": str(S.field(proc, "unit")),
                      "version": str(S.field(proc, "version")),
                      "dossier_sha256": str(S.field(proc, "dossier-sha256")),
                      "contract": str(S.field(proc, "contract")),
                      "contract_version": str(S.field(proc, "contract-version"))},
        "devices": devices,
        "regions": regions,
        "reset_kinds": _strings(S.children(doc, "reset")[0], "kinds"),
        "console": str(S.field(S.children(doc, "serial-console")[0], "device")),
        "absences": [
            {"element": name,
             "satisfies": _strings(S.children(doc, name)[0], "satisfies")}
            for name in ("timers", "interrupt-controller")
            if str(S.field(S.children(doc, name)[0], "present")) == "false"],
        # P5-BOARD.4: the composition dispositions — board decisions answering device
        # obligations the dossier deferred to the board (composition_disposition
        # "required"), mirrored into hardware.sexp so the model route reads them as data.
        "dispositions": [
            {"decision": str(S.field(d, "id")),
             "answers": _strings(d, "answers"),
             "statement": str(S.field(d, "statement"))}
            for d in S.children(doc, "decision")
            if S.children(d, "answers")],
        # P5-BOARD.6: the boot contract and the test-control surface — the platform
        # capability manifest (gen_platform.py) derives from them. gen_board's own
        # renderers do not consume them; they are read here so every consumer shares
        # the ONE board reader.
        "boot": {name: str(S.field(S.children(doc, "boot")[0], name))
                 for name in ("image-format", "load-region", "entry", "register-state",
                              "argument-convention", "firmware-services", "abi",
                              "hardware-description")},
        "test_control": {name: str(S.field(S.children(doc, "test-control")[0], name))
                         for name in ("console-capture", "completion", "reset",
                                      "input-injection", "execution-budget",
                                      "trace-selection", "snapshots")},
    }


def check_consistency(board: dict) -> None:
    """Every refusal a board.sexp can prove, named — never a generated map with a hole."""
    regions, devices = board["regions"], board["devices"]
    seen: set[str] = set()
    for r in regions:
        if r["name"] in seen:
            raise GenError(f"region '{r['name']}' is declared twice")
        seen.add(r["name"])
        if r["size"] <= 0:
            raise GenError(f"region '{r['name']}' has a zero size — a window that "
                           f"serves nothing")
    ordered = sorted(regions, key=lambda r: r["base"])
    for prev, nxt in zip(ordered, ordered[1:]):
        if nxt["base"] < prev["base"] + prev["size"]:
            raise GenError(f"regions '{prev['name']}' and '{nxt['name']}' overlap "
                           f"({fmt_hex(prev['base'])}–{fmt_hex(prev['base'] + prev['size'])}"
                           f" vs {fmt_hex(nxt['base'])})")
    by_device = {d["id"]: d for d in devices}
    served: dict[str, str] = {}
    for r in regions:
        if r["kind"] == "ram":
            if r["device"] is not None:
                raise GenError(f"ram region '{r['name']}' names device "
                               f"'{r['device']}' — memory serves no device")
            continue
        if r["device"] is None:
            raise GenError(f"mmio region '{r['name']}' names no device — an mmio "
                           f"window is a device's, never free-floating")
        if r["device"] not in by_device:
            raise GenError(f"mmio region '{r['name']}' names undeclared device "
                           f"'{r['device']}'")
        if r["executable"]:
            raise GenError(f"mmio region '{r['name']}' is executable — instruction "
                           f"fetch is served from RAM only (OB-ENV-FETCH-SUPPLY)")
        served[r["device"]] = r["name"]
    for d in devices:
        if d["id"] not in served:
            raise GenError(f"device '{d['id']}' has no mmio region — a wired device "
                           f"the map does not reach")
    if board["console"] not in served:
        raise GenError(f"serial console names '{board['console']}', which is not a "
                       f"wired device")


def part_dirs(board: dict) -> list[Path]:
    """The unit directories the board composes, processor first, devices in order.

    A board dir copied into scratch (the doctrine's self-test) still refers to the
    repo's units: prefer the board dir's own sibling units, fall back to the repo's
    profiles/ — and refuse by name when neither holds the unit."""
    units = [board["processor"]["unit"]] + [d["unit"] for d in board["devices"]]
    dirs = []
    for unit in units:
        for candidate in (board["dir"].parent / unit, REPO / "profiles" / unit):
            if candidate.is_dir():
                dirs.append(candidate)
                break
        else:
            raise GenError(f"unit '{unit}' has no unit directory — the board composes "
                           f"what exists")
    return dirs


# --------------------------------------------------------------------------- the renderings

def _fingerprint_sexp(board: dict) -> str:
    rel = _rel(board["dir"] / "board.sexp")
    return (f";; GENERATED — do not edit (OWN-03). Regenerate with "
            f"`python3 scripts/gen_board.py`; drift between this document and the\n"
            f";; canonical board definition is refused by the BOARD-GEN doctrine "
            f"(scripts/check_board_gen.sh).\n"
            f";; Canonical input: {rel} (sha256 {sha256(board['dir'] / 'board.sexp')})\n"
            f";; Generator: scripts/gen_board.py (sha256 {sha256(GENERATOR)})\n")


def render_manifest(board: dict) -> str:
    parts = [board["processor"]["unit"]] + [d["unit"] for d in board["devices"]]
    lines = _fingerprint_sexp(board)
    lines += (f'(composition (id "{board["id"]}")\n'
              + "".join(f'  (part "../{p}")\n' for p in parts) + ")\n")
    return lines


def render_hardware(board: dict) -> str:
    out = [_fingerprint_sexp(board)]
    p = board["processor"]
    out.append(f'(hardware\n  (board "{board["id"]}")\n  (version "{board["version"]}")\n'
               f'  (processor (unit "{p["unit"]}") (version "{p["version"]}") '
               f'(contract "{p["contract"]}") (contract-version "{p["contract_version"]}"))')
    region_of = {}
    for r in board["regions"]:
        line = (f'  (region (name "{r["name"]}") (base "{fmt_hex(r["base"])}") '
                f'(size "{fmt_hex(r["size"])}") (end "{fmt_hex(r["base"] + r["size"])}") '
                f'(kind {r["kind"]}) (executable {"true" if r["executable"] else "false"})')
        if r["device"] is not None:
            line += f' (device "{r["device"]}")'
            region_of[r["device"]] = r["name"]
        out.append(line + ")")
    for d in board["devices"]:
        widths = " ".join(f"(access-widths {w})" for w in d["access_widths"])
        out.append(f'  (wiring (device "{d["id"]}") (unit "{d["unit"]}") (kind {d["kind"]})'
                   f' (region "{region_of[d["id"]]}") {widths}'
                   f' (interrupt {d["interrupt"]}) (backend-rx {d["backend_rx"]})'
                   f' (backend-tx {d["backend_tx"]}))')
    out.append(f'  (serial-console (device "{board["console"]}"))')
    out.append("  (reset" + "".join(f" (kinds {k})" for k in board["reset_kinds"]) + ")")
    for a in board["absences"]:
        sat = " ".join(f'(satisfies "{s}")' for s in a["satisfies"])
        out.append(f'  (absence (element {a["element"]}) {sat})')
    for d in board["dispositions"]:
        ans = " ".join(f'(answers "{a}")' for a in d["answers"])
        out.append(f'  (disposition (decision "{d["decision"]}") {ans} '
                   f'(statement "{d["statement"]}"))')
    out.append(")")
    return "\n".join(out) + "\n"


def _human_size(size: int) -> str:
    for unit, step in (("GiB", 1 << 30), ("MiB", 1 << 20), ("KiB", 1 << 10)):
        if size >= step and size % step == 0:
            return f"{size // step} {unit}"
    return f"{size} B"


def render_map(board: dict) -> str:
    rel = _rel(board["dir"] / "board.sexp")
    out = ["<!-- GENERATED — do not edit (OWN-03). Regenerate with\n"
           "     `python3 scripts/gen_board.py`; drift between this map and the canonical\n"
           "     board definition is refused by the BOARD-GEN doctrine\n"
           "     (`scripts/check_board_gen.sh`). -->\n"
           f"<!-- Canonical input: `{rel}` "
           f"(sha256 `{sha256(board['dir'] / 'board.sexp')}`)\n"
           f"     Generator: `scripts/gen_board.py` (sha256 `{sha256(GENERATOR)}`) -->\n",
           f"# The generated map — `{board['id']}` v{board['version']}\n",
           "Derived from the canonical board definition; the DOSSIER narrates it. "
           "Region ends are exclusive (base + size).\n",
           "## Address map\n",
           "| Region | Base | End | Size | Kind | Executable | Device |",
           "| --- | --- | --- | --- | --- | --- | --- |"]
    region_of = {}
    for r in board["regions"]:
        device = f"`{r['device']}`" if r["device"] else "—"
        if r["device"]:
            region_of[r["device"]] = r["name"]
        out.append(f"| `{r['name']}` | `{fmt_hex(r['base'])}` | "
                   f"`{fmt_hex(r['base'] + r['size'])}` | {_human_size(r['size'])} "
                   f"(`{fmt_hex(r['size'])}`) | {r['kind'].upper()} | "
                   f"{'yes' if r['executable'] else 'no'} | {device} |")
    out += ["", "## Wiring\n",
            "| Device | Unit | Kind | Region | Access widths | Interrupt | RX backend | TX backend |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for d in board["devices"]:
        widths = "/".join(str(w) for w in d["access_widths"])
        out.append(f"| `{d['id']}` | `{d['unit']}` | {d['kind']} | `{region_of[d['id']]}` "
                   f"| {widths}-bit | {d['interrupt']} | {d['backend_rx']} | {d['backend_tx']} |")
    out += ["", f"Serial console: `{board['console']}`. Reset: "
            + ", ".join(board["reset_kinds"]) + " only.\n",
            "## Declared absences\n",
            "| Element | Present | Satisfies |", "| --- | --- | --- |"]
    for a in board["absences"]:
        out.append(f"| {a['element'].replace('-', ' ')} | no — absent by contract | "
                   + ", ".join(f"`{s}`" for s in a["satisfies"]) + " |")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- the derivation

def derive(board_dir: Path, scratch: Path) -> dict[str, bytes]:
    """Derive every artifact for one board into `scratch`; return name -> bytes."""
    board = read_board(board_dir)
    check_consistency(board)

    manifest = render_manifest(board)
    mpath = scratch / "composition.sexp"
    mpath.write_text(manifest)
    _validate(mpath, COMPOSITION_SCHEMA)

    census = C.compose_resolved(board["id"], part_dirs(board), scratch)
    if census["id"] != board["id"]:
        raise GenError(f"composition id '{census['id']}' disagrees with the board id "
                       f"'{board['id']}'")

    hardware = render_hardware(board)
    hpath = scratch / "hardware.sexp"
    hpath.write_text(hardware)
    _validate(hpath, HARDWARE_SCHEMA)

    (scratch / "map.md").write_text(render_map(board))
    return {name: (scratch / name).read_bytes() for name in ARTIFACTS}


def run(board_dirs: list[Path], out_dir: Path | None, check: bool) -> int:
    drift: list[str] = []
    for board_dir in board_dirs:
        dest = out_dir if out_dir is not None else board_dir
        (REPO / "target").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=REPO / "target") as tmp:
            derived = derive(board_dir, Path(tmp))
        if check:
            for name, want in derived.items():
                got = dest / name
                if not got.is_file():
                    drift.append(f"{dest / name}: missing (never generated)")
                elif got.read_bytes() != want:
                    drift.append(f"{dest / name}: DRIFT — not what board.sexp derives")
        else:
            dest.mkdir(parents=True, exist_ok=True)
            for name, content in derived.items():
                (dest / name).write_bytes(content)
            print(f"{dest}: {len(derived)} artifact(s) generated from "
                  f"{board_dir / 'board.sexp'}")
    if drift:
        for line in drift:
            print(line, file=sys.stderr)
        print("Regenerate — never edit: python3 scripts/gen_board.py", file=sys.stderr)
        return 1
    if check:
        print(f"gen_board --check: ok ({len(board_dirs)} board(s), "
              f"{len(ARTIFACTS)} artifact(s) each, byte-exact)")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="re-derive and byte-compare; refuse drift, naming the artifact")
    ap.add_argument("--board-dir", type=Path,
                    help="one board directory (default: every profiles/*/board.sexp)")
    ap.add_argument("--out-dir", type=Path,
                    help="artifact destination (default: the board dir itself)")
    args = ap.parse_args(argv[1:])

    if args.board_dir is not None:
        board_dirs = [args.board_dir]
    else:
        board_dirs = sorted(p.parent for p in (REPO / "profiles").glob("*/board.sexp"))
        if not board_dirs:
            print("gen_board: no board declares itself (profiles/*/board.sexp) — "
                  "nothing to generate", file=sys.stderr)
            return 2
    try:
        return run(board_dirs, args.out_dir, args.check)
    except (GenError, C.ComposeError, S.SexpError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
