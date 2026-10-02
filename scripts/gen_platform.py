#!/usr/bin/env python3
"""Generate a board's platform capability manifest from its canonical inputs.

`P5-BOARD.6` — OWN-06: the read-only derived export of the accepted
processor/device/board profile and its boot contract, for a compatibility checker
(`docs/ARCHOGEN_INTEGRATION.md` §3). Derived, never handwritten: a consumer imports
facts rather than becoming a second hardware implementation. The consumer-absence
boundary is stated in the document itself — archogen is actively developed and has no
functional eADL interface today, so this export's correctness legs on our side are
derivation freshness (PLATFORM-GEN), schema conformance (`schema/platform.sexp`) and §3
content coverage, never archogen acceptance.

Boards are discovered BY DECLARATION — any `profiles/*/board.sexp` — never from a
hardcoded id (the gen_board idiom). Per board, the manifest derives from THREE canonical
inputs, all fingerprinted in the OWN-03 header:

  profiles/<board>/board.sexp                the canonical board definition (the pins,
                                             the map, the absences, the dispositions,
                                             the boot contract and the test-control
                                             surface) — read through gen_board's
                                             read_board/check_consistency, the ONE board
                                             reader, imported, never re-implemented
  profiles/<unit>/profile.sexp               the pinned processor's dossier (the ISA
                                             facts), read through dossier_sexp, the ONE
                                             dossier mapping owner
  profiles/<board>/contract-obligations.sexp the composed obligations (BOARD-GEN-fresh) —
                                             the platform-level parameters (time, events,
                                             ordering), read through records_sexp, the ONE
                                             record mapping owner

The generator REFUSES, by name, rather than emitting a manifest with a hole: an
unreadable or schema-invalid input; a STALE dossier pin — the board's `dossier-sha256`
is re-derived from the live dossier by gate_report.dossier_digest (the ONE computation;
the pin was measured display-only before this leaf, and this generator is what makes it
load-bearing); a processor profile missing a fact §3 requires (xlen, ilen, ialign,
harts, endianness — absent means undeclared at the owner, and a guessed value would be
a second source of truth); a profile id disagreeing with the pinned unit; a boot
`load-region` that is not a declared executable RAM region; a test-control claim the
wiring contradicts (console capture without a host-console TX backend, recorded
injection without a recorded RX backend, cold-reload with anything but a cold-only
reset); an obligation parameter the export derives from that is missing or carries a
value this generator cannot emit (a time source other than `none` — the fidelity of a
time-bearing platform is a declaration this generator cannot invent); a contradiction
between two owned sources (profile harts vs the ordering obligation's harts; the
declared interrupt-controller absence vs the event-delivery obligation's controller).

`--check` re-derives the manifest in memory and refuses DRIFT, naming the artifact —
the PLATFORM-GEN doctrine (`scripts/check_platform_gen.sh`) runs it on every commit.

usage: gen_platform.py [--check] [--board-dir PATH] [--out-dir PATH]
  --board-dir   one board only (default: every profiles/*/board.sexp)
  --out-dir     manifest destination (default: the board dir itself; scratch use is for
                the doctrine's self-test)
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_sexp_schema as K                    # noqa: E402
import dossier_sexp as D                         # noqa: E402
import gate_report as G                          # noqa: E402
import gen_board as B                            # noqa: E402
import records_sexp as R                         # noqa: E402
import sexp as S                                 # noqa: E402

REPO = Path(__file__).resolve().parent.parent
PLATFORM_SCHEMA = REPO / "schema" / "platform.sexp"
GENERATOR = Path(__file__).resolve()

EXPORT_VERSION = "0"
ARTIFACT = "platform.sexp"

# The obligation parameters this export derives from, and the values it can emit. A
# composed obligation missing, or carrying a value outside this table, is a refusal —
# the generator never guesses a platform fact (OWN-06: one owner; the owner is silent
# or changed = the export cannot be derived).
ENV_OBLIGATIONS = ("OB-ENV-VIRTUAL-TIME", "OB-ENV-EVENT-DELIVERY", "OB-ENV-ORDERING")


class GenError(Exception):
    """A refusal: the inputs do not generate a manifest, by the fact named."""


def _validate(path: Path, schema: Path) -> None:
    try:
        constructs, operators = K.load_schema(schema)
        errors = K.validate_file(path, constructs, operators)
    except (K.SchemaError, S.SexpError) as exc:
        raise GenError(f"{path}: the schema layer itself cannot judge — {exc}")
    if errors:
        raise GenError(f"{path}: refused by {schema.name} — " + "; ".join(errors))


# --------------------------------------------------------------------------- the inputs

def read_processor(board: dict) -> tuple[Path, dict]:
    """The pinned processor's dossier — resolved from the board's pin, never hardcoded."""
    pin = board["processor"]
    unit_dir = board["dir"].parent / pin["unit"]
    if not unit_dir.is_dir():
        unit_dir = REPO / "profiles" / pin["unit"]
    if not unit_dir.is_dir():
        raise GenError(f"unit '{pin['unit']}' has no unit directory — the board composes "
                       f"what exists")
    path = unit_dir / "profile.sexp"
    if not path.is_file():
        raise GenError(f"{path}: the pinned processor's profile dossier is missing")
    _validate(path, REPO / "schema" / "profile.sexp")
    try:
        doc = D.load_profile(path)
    except (D.DossierError, S.SexpError) as exc:
        raise GenError(f"{path}: the dossier mapping owner cannot read it — {exc}")
    prof = doc["profile"]
    if prof.get("id") != pin["unit"]:
        raise GenError(f"{path}: profile id '{prof.get('id')}' disagrees with the "
                       f"pinned unit '{pin['unit']}'")
    return unit_dir, prof


def check_pin(board: dict, unit_dir: Path) -> None:
    """The dossier-sha256 pin is LOAD-BEARING here: re-derived from the live dossier by
    the ONE computation (gate_report.dossier_digest). A stale pin means the dossier
    changed after the board pinned it — a finding, never a silent upgrade (the
    schema/board.sexp processor comment)."""
    pin = board["processor"].get("dossier_sha256")
    live = G.dossier_digest(unit_dir)
    if pin != live:
        raise GenError(
            f"dossier-sha256 pin is STALE: board.sexp pins {pin}, the live dossier "
            f"derives {live} — re-pin deliberately (the digest covers every tracked "
            f"dossier source file; GATE-REPORT regenerates the unit's GC-REPORT.md)")


def read_obligation_params(board: dict) -> dict[str, dict]:
    """The composed obligations' parameters for the platform-level facts."""
    path = board["dir"] / "contract-obligations.sexp"
    if not path.is_file():
        raise GenError(f"{path}: the composed obligations are missing — run "
                       f"python3 scripts/gen_board.py first (BOARD-GEN owns them)")
    try:
        obs = R.load(path)
    except (R.RecordRefused, S.SexpError) as exc:
        raise GenError(f"{path}: the record mapping owner cannot read it — {exc}")
    params = {}
    for oid in ENV_OBLIGATIONS:
        match = [o for o in obs if o.get("id") == oid]
        if not match:
            raise GenError(f"{path}: obligation '{oid}' is absent from the composed "
                           f"unit — the platform's {oid} facts have no owner here")
        params[oid] = match[0].get("parameters", {})
    return params


def _param(params: dict[str, dict], oid: str, name: str):
    if name not in params[oid]:
        raise GenError(f"{oid}: parameter '{name}' is missing — the export derives "
                       f"from it and will not guess")
    return params[oid][name]


# --------------------------------------------------------------------------- the checks

def check_platform_facts(board: dict, prof: dict, params: dict[str, dict]) -> None:
    """Every cross-input consistency the manifest asserts, refused by name."""
    for field in ("xlen", "ilen", "ialign", "harts", "endianness"):
        if field not in prof:
            raise GenError(
                f"{prof['id']}/profile.sexp: '{field}' is absent — §3 requires the "
                f"value in the export, and its one owner is the processor dossier; "
                f"declare it there, never here")
    boot, tc = board["boot"], board["test_control"]
    regions = {r["name"]: r for r in board["regions"]}
    load = boot["load-region"]
    if load not in regions:
        raise GenError(f"boot load-region '{load}' names no declared region")
    r = regions[load]
    if r["kind"] != "ram" or not r["executable"]:
        raise GenError(f"boot load-region '{load}' is {r['kind']}, executable "
                       f"{r['executable']} — an image loads into executable RAM")
    devices = {d["id"]: d for d in board["devices"]}
    if tc["console-capture"] == "host-console":
        console = devices[board["console"]]
        if console["backend_tx"] != "host-console":
            raise GenError(f"test-control claims host-console capture but console "
                           f"device '{board['console']}' has TX backend "
                           f"'{console['backend_tx']}'")
    if tc["input-injection"] == "recorded-backends":
        if not any(d["backend_rx"].startswith("recorded") for d in devices.values()):
            raise GenError("test-control claims recorded-backend injection but no "
                           "device carries a recorded RX backend")
    if tc["reset"] == "cold-reload" and board["reset_kinds"] != ["cold"]:
        raise GenError(f"test-control claims cold-reload reset but the reset block "
                       f"declares {board['reset_kinds']}")
    if _param(params, "OB-ENV-VIRTUAL-TIME", "time_source") != "none":
        raise GenError("OB-ENV-VIRTUAL-TIME pins a time source other than 'none' — "
                       "the timing fidelity of a time-bearing platform is a "
                       "declaration this generator cannot invent")
    if not (_param(params, "OB-ENV-VIRTUAL-TIME", "csr_readable_time") is False
            and _param(params, "OB-ENV-VIRTUAL-TIME", "mmio_readable_time") is False):
        raise GenError("OB-ENV-VIRTUAL-TIME admits a readable time source — the "
                       "export's 'none' would be a lie")
    if _param(params, "OB-ENV-EVENT-DELIVERY", "asynchronous_interrupts") is not False:
        raise GenError("OB-ENV-EVENT-DELIVERY admits asynchronous interrupts — the "
                       "export's 'no' would be a lie")
    if _param(params, "OB-ENV-EVENT-DELIVERY", "synchronous_exceptions") is not True:
        raise GenError("OB-ENV-EVENT-DELIVERY does not pin synchronous exceptions — "
                       "the export's 'yes' would be a lie")
    if _param(params, "OB-ENV-EVENT-DELIVERY", "interrupt_controller") != "none":
        raise GenError("OB-ENV-EVENT-DELIVERY names an interrupt controller — "
                       "contradicts the board's declared absence")
    if any(a["element"] == "interrupt-controller" for a in board["absences"]) != \
            (_param(params, "OB-ENV-EVENT-DELIVERY", "interrupt_controller") == "none"):
        raise GenError("the board's interrupt-controller absence and "
                       "OB-ENV-EVENT-DELIVERY's controller parameter disagree")
    oharts = _param(params, "OB-ENV-ORDERING", "harts")
    if oharts != prof["harts"]:
        raise GenError(f"harts disagree: the profile declares {prof['harts']}, "
                       f"OB-ENV-ORDERING pins {oharts}")
    if _param(params, "OB-ENV-ORDERING", "execution_order") != "sequential in-order":
        raise GenError("OB-ENV-ORDERING pins an execution order this generator "
                       "cannot emit")
    if _param(params, "OB-ENV-ORDERING", "memory_model_claim") != "none":
        raise GenError("OB-ENV-ORDERING pins a memory-model claim this generator "
                       "cannot emit")


# --------------------------------------------------------------------------- the rendering

def _q(text: str) -> str:
    return '"' + text + '"'


def _fingerprint(paths: list[Path]) -> str:
    lines = (";; GENERATED — do not edit (OWN-03). Regenerate with "
             "`python3 scripts/gen_platform.py`; drift between this document and its\n"
             ";; canonical inputs is refused by the PLATFORM-GEN doctrine "
             "(scripts/check_platform_gen.sh).\n"
             ";; Canonical inputs:\n")
    for path in paths:
        lines += f";;   {B._rel(path)} (sha256 {B.sha256(path)})\n"
    lines += f";; Generator: scripts/gen_platform.py (sha256 {B.sha256(GENERATOR)})\n"
    return lines


def frozen_counter_disposition(board: dict) -> str | None:
    """The decision binding a guest-readable-time-source obligation, if one exists —
    found by the `-TIME-SOURCES` obligation-id convention (declared here, the one
    place); more than one match is ambiguous and refused."""
    hits = [d["decision"] for d in board["dispositions"]
            if any(a.endswith("-TIME-SOURCES") for a in d["answers"])]
    if len(hits) > 1:
        raise GenError(f"multiple dispositions answer a -TIME-SOURCES obligation "
                       f"({hits}) — the export cannot pick one")
    return hits[0] if hits else None


def render_platform(board: dict, prof: dict, params: dict[str, dict],
                    prof_path: Path) -> str:
    p = board["processor"]
    # The ISA string in canonical order (RVI naming chapter): the base lowered, the
    # single-letter extensions concatenated in the profile's declared order, then the
    # multi-letter extensions underscore-joined in declared order. Sorting would
    # destroy the canonical order (measured against the GC profile's declaration).
    exts = prof.get("extensions", [])
    single = "".join(e.lower() for e in exts if len(e) == 1)
    multi = "_".join(e.lower() for e in exts if len(e) > 1)
    isa = prof["base"].lower() + single + ("_" + multi if multi else "")
    out = [_fingerprint([board["dir"] / "board.sexp", prof_path,
                         board["dir"] / "contract-obligations.sexp"])]
    out.append(
        f'(platform\n  (id "{board["id"]}") (version "{board["version"]}") '
        f'(export-version "{EXPORT_VERSION}") (status {board["status"]})')
    extensions = (" (extensions)" if not prof.get("extensions") else
                  " (extensions " + " ".join(_q(e) for e in prof["extensions"]) + ")")
    out.append(
        f'  (processor (unit "{p["unit"]}") (version "{p["version"]}")\n'
        f'    (dossier-sha256 "{p["dossier_sha256"]}") (contract "{p["contract"]}") '
        f'(contract-version "{p["contract_version"]}")\n'
        f'    (architecture "{prof["architecture"]}") (isa "{isa}") '
        f'(xlen {prof["xlen"]}) (ilen {prof["ilen"]}) (ialign {prof["ialign"]}) '
        f'(harts {prof["harts"]})\n'
        f'    (privilege-modes {" ".join(_q(m) for m in prof["privilege_modes"])})'
        f'{extensions} (endianness {prof["endianness"]})\n'
        f'    (spec (chapter-version "{prof["chapter_version"]}") '
        f'(revision "{prof["spec_revision"]}")))')
    region_of = {}
    out.append("  (memory")
    for r in board["regions"]:
        line = (f'    (region (name "{r["name"]}") (base "{B.fmt_hex(r["base"])}") '
                f'(size "{B.fmt_hex(r["size"])}") '
                f'(end "{B.fmt_hex(r["base"] + r["size"])}") (kind {r["kind"]}) '
                f'(executable {"true" if r["executable"] else "false"})')
        if r["device"] is not None:
            line += f' (device "{r["device"]}")'
            region_of[r["device"]] = r["name"]
        out.append(line + " (presence offered))")
    out[-1] += ")"
    for d in board["devices"]:
        widths = " ".join(str(w) for w in d["access_widths"])
        out.append(
            f'  (device (id "{d["id"]}") (unit "{d["unit"]}") (kind {d["kind"]}) '
            f'(material "{d["material"]}") (revision "{d["revision"]}") '
            f'(sha256 "{d["sha256"]}")\n'
            f'    (region "{region_of[d["id"]]}") (access-widths {widths}) '
            f'(interrupt {d["interrupt"]}) (backend-rx {d["backend_rx"]}) '
            f'(backend-tx {d["backend_tx"]}) (presence offered))')
    for a in board["absences"]:
        sat = " ".join(f'(satisfies "{s}")' for s in a["satisfies"])
        out.append(f'  (absence (element {a["element"]}) (presence absent-by-contract) '
                   f'{sat})')
    for d in board["dispositions"]:
        ans = " ".join(f'(answers "{a}")' for a in d["answers"])
        out.append(f'  (disposition (decision "{d["decision"]}") {ans} '
                   f'(statement "{d["statement"]}"))')
    b = board["boot"]
    out.append(
        f'  (boot (image-format {b["image-format"]}) (load-region "{b["load-region"]}") '
        f'(entry {b["entry"]}) (register-state {b["register-state"]})\n'
        f'    (argument-convention {b["argument-convention"]}) '
        f'(firmware-services {b["firmware-services"]}) (abi {b["abi"]}) '
        f'(hardware-description {b["hardware-description"]}) (presence offered))')
    frozen = frozen_counter_disposition(board)
    time_line = ('  (time (time-source none)'
                 + (f' (frozen-counter-disposition "{frozen}")' if frozen else "")
                 + ' (timing-fidelity functional-only) (presence absent-by-contract))')
    out.append(time_line)
    out.append('  (events (synchronous-exceptions yes) (requested-traps yes) '
               '(asynchronous-interrupts no) (interrupt-controller none) '
               '(presence limited))')
    out.append(f'  (ordering (harts {prof["harts"]}) (execution sequential-in-order) '
               f'(memory-model-claim none) (scheduling-policies none))')
    t = board["test_control"]
    out.append(
        f'  (test-control (console-capture {t["console-capture"]}) '
        f'(completion {t["completion"]}) (reset {t["reset"]}) '
        f'(input-injection {t["input-injection"]})\n'
        f'    (execution-budget {t["execution-budget"]}) '
        f'(trace-selection {t["trace-selection"]}) (snapshots {t["snapshots"]}) '
        f'(presence offered))')
    widths = sorted({w for d in board["devices"] for w in d["access_widths"]})
    limitations = [
        f'EXPERIMENTAL: the platform inherits its processor\'s status ({p["unit"]} '
        f'v{p["version"]}); every claim is conditional on the CPU\'s acceptance '
        f'trajectory — the composition can never outrank its processor',
        *('{} absent by contract ({}); no such facility exists for a guest'.format(
            a["element"].replace("-", " "), ", ".join(a["satisfies"]))
          for a in board["absences"]),
        'drivers poll: no asynchronous event is deliverable, so nothing wakes a '
        'waiting guest',
        'MMIO accesses honour exactly the declared widths ('
        + "/".join(str(w) for w in widths)
        + '-bit on this board); any other width is a board-reported contract '
        'violation, never silently serviced',
        'no firmware services and no environment ABI: ECALL/EBREAK are typed '
        'requested-trap outcomes reported to the harness',
    ]
    if frozen:
        limitations.append(
            f'guest-readable device counters are frozen ({frozen}): constant values '
            f'carry no time information — a guest busy-waiting on one hangs; poll for '
            f'data, never for time')
    out.append("  (limitations")
    out += [f'    (limitation "{line}")' for line in limitations]
    out[-1] += ")"
    out.append("  (non-claims")
    out += [
        '    (non-claim "a compatible manifest proves neither that an OS is correct '
        'nor that this manifest matches the implementation '
        '(docs/ARCHOGEN_INTEGRATION.md §3)")',
        '    (non-claim "no archogen eADL interface exists today — archogen is '
        'actively developed; this export is validated by derivation freshness, schema '
        'conformance and ARCHOGEN_INTEGRATION §3 coverage, never by archogen '
        'acceptance")',
        '    (non-claim "test-control capabilities are the platform package\'s '
        'declaration, evidenced by the runner\'s own suites — not by this document")',
    ]
    out[-1] += ")"
    out.append(")")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- the derivation

def derive(board_dir: Path, scratch: Path) -> bytes:
    """Derive one board's manifest into `scratch`; return its bytes."""
    board = B.read_board(board_dir)
    B.check_consistency(board)
    unit_dir, prof = read_processor(board)
    check_pin(board, unit_dir)
    params = read_obligation_params(board)
    check_platform_facts(board, prof, params)
    text = render_platform(board, prof, params, unit_dir / "profile.sexp")
    mpath = scratch / ARTIFACT
    mpath.write_text(text)
    _validate(mpath, PLATFORM_SCHEMA)
    return mpath.read_bytes()


def run(board_dirs: list[Path], out_dir: Path | None, check: bool) -> int:
    drift: list[str] = []
    for board_dir in board_dirs:
        dest = out_dir if out_dir is not None else board_dir
        (REPO / "target").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=REPO / "target") as tmp:
            content = derive(board_dir, Path(tmp))
        if check:
            got = dest / ARTIFACT
            if not got.is_file():
                drift.append(f"{dest / ARTIFACT}: missing (never generated)")
            elif got.read_bytes() != content:
                drift.append(f"{dest / ARTIFACT}: DRIFT — not what the canonical "
                             f"inputs derive")
        else:
            dest.mkdir(parents=True, exist_ok=True)
            (dest / ARTIFACT).write_bytes(content)
            print(f"{dest}: {ARTIFACT} generated from {board_dir / 'board.sexp'}")
    if drift:
        for line in drift:
            print(line, file=sys.stderr)
        print("Regenerate — never edit: python3 scripts/gen_platform.py",
              file=sys.stderr)
        return 1
    if check:
        print(f"gen_platform --check: ok ({len(board_dirs)} board(s), byte-exact)")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="re-derive and byte-compare; refuse drift, naming the artifact")
    ap.add_argument("--board-dir", type=Path,
                    help="one board directory (default: every profiles/*/board.sexp)")
    ap.add_argument("--out-dir", type=Path,
                    help="manifest destination (default: the board dir itself)")
    args = ap.parse_args(argv[1:])

    if args.board_dir is not None:
        board_dirs = [args.board_dir]
    else:
        board_dirs = sorted(p.parent for p in (REPO / "profiles").glob("*/board.sexp"))
        if not board_dirs:
            print("gen_platform: no board declares itself (profiles/*/board.sexp) — "
                  "nothing to generate", file=sys.stderr)
            return 2
    try:
        return run(board_dirs, args.out_dir, args.check)
    except (GenError, B.GenError, S.SexpError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
