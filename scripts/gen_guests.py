#!/usr/bin/env python3
"""Generate the Rust guest fixture: the tracked assembly guests, assembled, with their
specification-derived expectations as data.

`crates/semulith-verify/src/guests.rs` is GENERATED (GUEST-GEN; OWN-03: generated
artifacts are changed by regeneration, never by direct editing, and identify their
canonical inputs, generator, configuration and source fingerprints). It lowers two tracked
inputs per guest into one fixture:

- `profiles/rv64i-lab-v0/guests/<name>.s` — the independently encoded program (assembled
  with the tracked assembler and the tracked encoding composition, so a fresh clone
  re-derives the identical bytes);
- `profiles/rv64i-lab-v0/guests/<name>.expected.sexp` — the observations derived from the
  pinned specification prose BEFORE any model ran (EVD-05: an expected value copied out of
  a model's output tests self-consistency and nothing else).

The verify-side tests execute each guest under the definitional interpreter
(`P1-LAB.8`) and compare the observation trace against these expectations — the commit
gate re-runs the whole first-execution-slice differential offline, no reference binary
needed. The live three-way comparison against sail-riscv is the experiment
(`scripts/run_semulith_smoke.py`), not the gate.

The generator REFUSES, by name, anything it cannot emit: a guest that does not assemble,
an expectations document it cannot reconcile, a register name outside x0..x31. A
generator that guesses is a second definition.

usage: gen_guests.py [--check] [--out PATH] [--encoding PATH] [--guests-dir PATH]
                     [--image-format words|bytes]
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from riscv_asm import Assembler, AsmError          # noqa: E402
import dossier_sexp as D                           # noqa: E402

REPO = Path(__file__).resolve().parent.parent
ENCODING = REPO / "profiles/rv64i-lab-v0/encoding.sexp"
GUESTS_DIR = REPO / "profiles/rv64i-lab-v0/guests"
OUT = REPO / "crates/semulith-verify/src/guests.rs"
GENERATOR = Path(__file__)


class GenError(Exception):
    """A refusal: the fixture cannot be emitted from what the repository declares."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    """The repository-relative name of a path, however the caller spelled it."""
    try:
        return path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return str(path)


def reg_index(name: str, where: str) -> int:
    if not name.startswith("x") or not name[1:].isdigit():
        raise GenError(f"{where}: register {name!r} is not of the x0..x31 form")
    index = int(name[1:])
    if not 0 <= index <= 31:
        raise GenError(f"{where}: register {name!r} is outside x0..x31")
    return index


def load_guest(name: str, guests_dir: Path, asm: Assembler) -> dict:
    source = guests_dir / f"{name}.s"
    expected = guests_dir / f"{name}.expected.sexp"
    if not source.is_file():
        raise GenError(f"{rel(source)}: guest source is missing")
    if not expected.is_file():
        raise GenError(f"{rel(expected)}: expectations document is missing")
    try:
        exp = D.load_expectations(expected)
    except D.DossierError as exc:
        raise GenError(f"{rel(expected)}: does not reconcile — {exc}") from exc
    entry = int(exp["entry"], 16)
    try:
        units = asm.assemble_units(source.read_text().splitlines(), base=entry)
    except AsmError as exc:
        raise GenError(f"{rel(source)}: does not assemble — {exc}") from exc
    steps = exp["instructions"]
    seen: set[int] = set()
    expectations: list[tuple[int, list[tuple[int, int]]]] = []
    for e in exp["step"]:
        n = e["n"]
        where = f"{rel(expected)} [step {n}]"
        if n in seen:
            raise GenError(f"{where}: declared twice")
        if n >= steps:
            raise GenError(
                f"{where}: step index {n} exceeds the declared {steps} executed step(s)")
        seen.add(n)
        writes = sorted(
            (reg_index(k, where), int(v, 16)) for k, v in (e.get("writes") or {}).items()
        )
        expectations.append((n, writes))
    missing = set(range(steps)) - seen
    if missing:
        raise GenError(
            f"{rel(expected)}: {len(missing)} executed step(s) carry no "
            f"expectation, starting at step {min(missing)} — a partial expectation is a "
            f"gap the check would read as 'writes nothing'")
    never = [reg_index(r, f"{rel(expected)} never_written")
             for r in (exp.get("never_written") or [])]
    # P4-SYSTEM.8 slice (c): the experiment's refusal regions — typed fault injection
    refusals = []
    for r in exp.get("refuse") or []:
        kind = r["kind"]
        if kind not in ("fetch", "load", "store", "walk"):
            raise GenError(f"{rel(expected)}: refuse kind {kind!r} — fetch, load, store or walk")
        base, size = int(r["base"], 16), int(r["size"], 16)
        if size <= 0:
            raise GenError(f"{rel(expected)}: refuse size {r['size']} — an empty region refuses nothing")
        refusals.append((kind, base, size))
    fetches = exp.get("fetches")
    if fetches is not None and (not isinstance(fetches, int) or not 0 <= fetches <= 2 * steps):
        raise GenError(
            f"{rel(expected)}: fetches {fetches!r} is not an integer within "
            f"[0, 2x the declared {steps} executed step(s)] — a step issues at most "
            f"the two parcel fetches")
    return {
        "name": name,
        "entry": entry,
        "units": units,
        "image": b"".join(u.value.to_bytes(u.length, "little") for u in units),
        "steps": steps,
        "fetches": steps if fetches is None else fetches,
        "expectations": expectations,
        "never_written": sorted(set(never)),
        "refusals": refusals,
        "cross_model": bool(exp.get("cross_model", True)),
        "sources": (source, expected),
    }


def hex64(value: int) -> str:
    return f"0x{value:016X}"


def hex32(value: int) -> str:
    return f"0x{value:08X}"


def emit(guests: list[dict], encoding: Path, image_format: str = "words",
         regeneration: str = "python3 scripts/gen_guests.py") -> str:
    if image_format not in ("words", "bytes"):
        raise GenError(f"image format {image_format!r}: wants words or bytes")
    if image_format == "words":
        for g in guests:
            if any(u.length != 4 for u in g["units"]):
                raise GenError(f"{g['name']}: short units require --image-format bytes; "
                               "word fixture refuses padding")
    a: list[str] = []
    a.append(f"//! GENERATED — do not edit (OWN-03). Regenerate with `{regeneration}`;"
             " drift between this fixture and the tracked guest sources is refused by the"
             " GUEST-GEN doctrine (`scripts/check_guest_gen.sh`). This module lowers the"
             " tracked assembly guests and their specification-derived expectations into data"
             " for the verify-side execution tests (`P1-LAB.8`): every expectation value was"
             " derived from the pinned specification prose before any model ran (EVD-05), so"
             " the commit gate re-runs the first-execution-slice differential offline.")
    a.append("//!")
    inputs: list[tuple[str, str]] = []
    for g in guests:
        for src in g["sources"]:
            inputs.append((rel(src), sha256(src)))
    inputs.append((rel(encoding), sha256(encoding)))
    a.append("//! Canonical inputs (sha256):")
    for relpath, digest in sorted(set(inputs)):
        a.append(f"//!   `{relpath}`  `{digest}`")
    gen_sha = sha256(GENERATOR)
    a.append(f"//! Generator: `scripts/gen_guests.py` (sha256 `{gen_sha}`)")
    a.append("//!")
    a.append("//! Every data array below carries `#[rustfmt::skip]`: the emission is")
    a.append("//! byte-stable by construction (one entry per line), so regeneration and the")
    a.append("//! GUEST-GEN drift check compare bytes rustfmt never reorders.")
    a.append("")
    a.append("/// The expected observations for one executed step of a guest: which register")
    a.append("/// writes the pinned specification-derived expectations declare, as")
    a.append("/// `(register index, value)` pairs ascending by index. An empty slice declares")
    a.append("/// the step writes nothing.")
    a.append("pub struct Expectation {")
    a.append("    /// The step's index in the executed trace.")
    a.append("    pub step: usize,")
    a.append("    /// The register writes the expectations declare for this step.")
    a.append("    pub writes: &'static [(u8, u64)],")
    a.append("}")
    a.append("")
    # Per-guest data arrays, each rustfmt-frozen so the emission stays byte-stable.
    for g in guests:
        name = g["name"].upper().replace("-", "_")
        a.append(f"#[rustfmt::skip]")
        if image_format == "bytes":
            a.append(f"static IMAGE_{name}: &[u8] = &[")
            for start in range(0, len(g["image"]), 16):
                a.append("    " + ", ".join(f"0x{b:02X}" for b in g["image"][start:start + 16]) + ",")
        else:
            a.append(f"static WORDS_{name}: &[u32] = &[")
            for unit in g["units"]:
                a.append(f"    {hex32(unit.value)},")
        a.append("];")
        a.append(f"#[rustfmt::skip]")
        a.append(f"static EXPECTED_{name}: &[Expectation] = &[")
        for n, writes in g["expectations"]:
            if writes:
                inner = ", ".join(f"({index}, {hex64(value)})" for index, value in writes)
                a.append(f"    Expectation {{ step: {n}, writes: &[{inner}] }},")
            else:
                a.append(f"    Expectation {{ step: {n}, writes: &[] }},")
        a.append("];")
        if g["never_written"]:
            inner = ", ".join(str(i) for i in g["never_written"])
            a.append(f"#[rustfmt::skip]")
            a.append(f"static NEVER_WRITTEN_{name}: &[u8] = &[{inner}];")
        if g["refusals"]:
            inner = ", ".join(f"Refusal {{ kind: RefusalKind::{k.capitalize()}, base: {hex64(b)}, "
                              f"size: {hex64(s)} }}" for k, b, s in g["refusals"])
            a.append(f"#[rustfmt::skip]")
            a.append(f"static REFUSALS_{name}: &[Refusal] = &[{inner}];")
        a.append("")
    a.append("/// The kind of boundary request a refusal region answers with an access fault")
    a.append("/// (P4-SYSTEM.8 slice c — typed fault injection, environment-shaped).")
    a.append("#[derive(Clone, Copy, Debug, PartialEq, Eq)]")
    a.append("pub enum RefusalKind {")
    a.append("    /// The implicit instruction read.")
    a.append("    Fetch,")
    a.append("    /// An explicit read.")
    a.append("    Load,")
    a.append("    /// An explicit write.")
    a.append("    Store,")
    a.append("    /// A page-table-walk read.")
    a.append("    Walk,")
    a.append("}")
    a.append("")
    a.append("/// One refusal region of a guest's experiment: requests of `kind` whose bytes")
    a.append("/// intersect `[base, base + size)` are answered with an access fault.")
    a.append("#[derive(Clone, Copy, Debug, PartialEq, Eq)]")
    a.append("pub struct Refusal {")
    a.append("    /// The request kind refused.")
    a.append("    pub kind: RefusalKind,")
    a.append("    /// The region's first byte.")
    a.append("    pub base: u64,")
    a.append("    /// The region's length in bytes.")
    a.append("    pub size: u64,")
    a.append("}")
    a.append("")
    a.append("/// A tracked guest program (assembled bytes) and the specification-derived")
    a.append("/// observations it must produce under the definitional interpreter.")
    a.append("pub struct Guest {")
    a.append("    /// The guest's name — the basename of its tracked sources.")
    a.append("    pub name: &'static str,")
    a.append("    /// The declared entry address (the reset vector of the laboratory).")
    a.append("    pub entry: u64,")
    if image_format == "bytes":
        a.append("    /// The exact little-endian program bytes, with no padding between units.")
        a.append("    pub image: &'static [u8],")
    else:
        a.append("    /// The guest's instruction words, little-endian sequence.")
        a.append("    pub words: &'static [u32],")
    a.append("    /// How many steps the program executes (the expectations declare it).")
    a.append("    pub executed_steps: usize,")
    a.append("    /// How many fetch requests the run must make (the expectations")
    if image_format == "bytes":
        a.append("    /// declare actual boundary requests, faulted ones included). A C-enabled")
        a.append("    /// table reads one parcel for C, two for a word; walk faults, interrupts")
        a.append("    /// and waiting can prevent requests (P4-SYSTEM.12).")
    else:
        a.append("    /// declare it — one per step, minus every step whose fetch page-faults")
        a.append("    /// in the walk and never issues a request, P4-SYSTEM.3).")
    a.append("    pub expected_fetches: usize,")
    a.append("    /// The expected register writes, one entry per executed step.")
    a.append("    pub expected: &'static [Expectation],")
    a.append("    /// Registers a correct execution must never write (the negative")
    a.append("    /// observations; a control transfer that failed to skip is invisible to")
    a.append("    /// positive checks alone).")
    a.append("    pub never_written: &'static [u8],")
    a.append("    /// The experiment's refusal regions (typed fault injection; empty for")
    a.append("    /// every guest that injects nothing).")
    a.append("    pub refusals: &'static [Refusal],")
    a.append("    /// Whether the cross-model comparison is enabled for this guest (a")
    a.append("    /// recorded platform difference may disable it; the skip is printed,")
    a.append("    /// never silent).")
    a.append("    pub cross_model: bool,")
    a.append("}")
    a.append("")
    a.append("/// The tracked guests, in the experiment's run order.")
    a.append("pub static GUESTS: &[Guest] = &[")
    for g in guests:
        name = g["name"].upper().replace("-", "_")
        never = f"NEVER_WRITTEN_{name}" if g["never_written"] else "&[]"
        refusals = f"REFUSALS_{name}" if g["refusals"] else "&[]"
        a.append("    Guest {")
        a.append(f'        name: "{g["name"]}",')
        a.append(f'        entry: {hex64(g["entry"])},')
        if image_format == "bytes":
            a.append(f"        image: IMAGE_{name},")
        else:
            a.append(f"        words: WORDS_{name},")
        a.append(f'        executed_steps: {g["steps"]},')
        a.append(f'        expected_fetches: {g["fetches"]},')
        a.append(f"        expected: EXPECTED_{name},")
        a.append(f"        never_written: {never},")
        a.append(f"        refusals: {refusals},")
        a.append(f'        cross_model: {str(g["cross_model"]).lower()},')
        a.append("    },")
    a.append("];")
    a.append("")
    return "\n".join(a)


def guest_names(guests_dir: Path) -> list[str]:
    """The corpus, DIRECTORY-DERIVED (P4-SYSTEM.2 slice d): the set is the directory's
    `*.s` files — a guest on disk the generator never saw is how a coverage hole used to
    hide — and the experiment's run order is the tracked `run-order.txt` beside them. The
    two are cross-checked both directions: a guest on disk but not listed, or listed but
    not on disk, is a refusal, named."""
    on_disk = {p.stem for p in guests_dir.glob("*.s")}
    order_path = guests_dir / "run-order.txt"
    if not order_path.is_file():
        raise GenError(f"{rel(order_path)}: missing — the run order is recorded data, "
                       f"never the directory's accident")
    order = [line for line in order_path.read_text().splitlines()
             if line and not line.startswith("#")]
    if len(order) != len(set(order)):
        raise GenError(f"{rel(order_path)}: a name repeats — the order lists each guest once")
    missing = [n for n in order if n not in on_disk]
    unlisted = sorted(on_disk - set(order))
    if missing:
        raise GenError(f"{rel(order_path)}: lists {', '.join(missing)} — not on disk")
    if unlisted:
        raise GenError(f"{rel(order_path)}: {', '.join(unlisted)} on disk but never "
                       f"listed — a guest the run order does not name never executes")
    return order


def generate(encoding: Path, guests_dir: Path, image_format: str = "words",
             regeneration: str = "python3 scripts/gen_guests.py") -> str:
    if not encoding.is_file():
        raise GenError(f"{encoding}: encoding composition is missing")
    asm = Assembler(encoding)
    names = guest_names(guests_dir)
    guests = [load_guest(name, guests_dir, asm) for name in names]
    return emit(guests, encoding, image_format, regeneration)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="regenerate in memory and report drift instead of writing")
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--encoding", type=Path, default=ENCODING)
    parser.add_argument("--guests-dir", type=Path, default=GUESTS_DIR)
    parser.add_argument("--image-format", choices=("words", "bytes"), default="words",
                        help="fixture representation; byte images preserve compressed units")
    args = parser.parse_args(argv)

    command = "python3 scripts/gen_guests.py"
    if (args.encoding.resolve(), args.guests_dir.resolve(), args.image_format) != (ENCODING, GUESTS_DIR, "words"):
        import shlex
        # Output location is not an input to the fixture. A check against a temporary
        # copy must retain the same command as the canonical module it is checking.
        canonical_out = {
            "rv64i-lab-v0": OUT,
            "rv64gc-lab-v0": REPO / "crates/semulith-verify/src/guests_rv64gc.rs",
        }.get(args.encoding.parent.name, args.out)
        command += " " + shlex.join(["--encoding", rel(args.encoding), "--guests-dir", rel(args.guests_dir),
                                     "--out", rel(canonical_out), "--image-format", args.image_format])

    try:
        text = generate(args.encoding, args.guests_dir, args.image_format, command)
    except GenError as exc:
        print(f"gen_guests: REFUSED — {exc}", file=sys.stderr)
        return 2

    if args.check:
        current = args.out.read_text() if args.out.is_file() else None
        if current != text:
            print(f"gen_guests: DRIFT — {args.out} no longer matches the tracked guest "
                  f"sources and their expectations.", file=sys.stderr)
            return 1
        print(f"gen_guests: ok ({args.out} matches the tracked guests)")
        return 0
    args.out.write_text(text)
    print(f"gen_guests: wrote {args.out} "
          f"({len(text)} bytes, {len(guest_names(args.guests_dir))} guests)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
