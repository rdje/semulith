#!/usr/bin/env python3
"""A selection's record: a credit with no case, read from what the laboratory built.

Some requirements state what was selected and how it stays true. They have no behaviour of their own to run, because the behaviour is
each extension's own credit, so a case would add nothing. EVIDENCE_POLICY.md asks of them what it asks of any disposition: "an explicit
source-grounded argument and its own controls before execution". So:

  - `profiles/<profile>/dispositions.sexp` declares a `kind record` disposition before anything runs: the argument, and each fact with
    the value the statement expects;
  - `profiles/<profile>/selections/<SEL-id>.selection.sexp` is what one measurement retained: each fact as read, each named check's
    output, run twice and compared, and the identity of every input it read;
  - each read here reads every fact again and holds it to the declaration and to the record.

A record is taken once, by `--record`, and a second one is refused: a new selection is a new record and a new credit. Only `--record`
starts a process. Reading never does, so the derivation stays cheap, and the named checks and drift gates still run in every commit's
gate on their own. A fact is compared, not a file's bytes: a Cargo.lock that moves some other package does not lapse the backend's credit.

This grants nothing. `scripts/credit_records.py` reads a record through `review`, and a requirement with no current credit stays `planned`.

  python3 -B scripts/selections.py --profile rv64gc-lab-v0 --requirement REQ-D-ABI
  python3 -B scripts/selections.py --profile rv64gc-lab-v0 --requirement REQ-D-ABI --record
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
import struct
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_extraction as E  # noqa: E402
import check_sexp_schema as K  # noqa: E402  (pinned by the finite cases; read, never changed)
import dispositions as DS  # noqa: E402
import records_sexp as R  # noqa: E402
import riscv_toolchain as T  # noqa: E402
import sexp as S  # noqa: E402
import statement_trace as ST  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DIRECTORY = "selections"
SCHEMA = "schema/dispositions.sexp"
SUFFIX = ".selection.sexp"
DOCUMENT_BYTES = 65536
FACT_BYTES = 16 * 1024 * 1024


class SelectionRefused(Exception):
    """A selection record cannot be read or taken."""


@dataclass(frozen=True)
class Run:
    """One command a record retains: its argv from the repository root, and the required checks it serves."""
    argv: tuple[str, ...]
    serves: tuple[str, ...] = ()


class Reader:
    """A selection's reads, each remembered, so the record's inputs are exactly what the facts read."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.read_paths: set[str] = set()

    def bytes(self, path: str) -> bytes:
        target = self.root / path
        if target.is_symlink() or not target.is_file() or target.stat().st_size > FACT_BYTES:
            raise SelectionRefused(f"{path}: not a bounded regular file")
        self.read_paths.add(path)
        return target.read_bytes()

    def text(self, path: str) -> str:
        return self.bytes(path).decode("utf-8")

    def head(self, path: str, count: int) -> str:
        """A file's first bytes, for a generated mirror's header. The file is an input like any other."""
        target = self.root / path
        if target.is_symlink() or not target.is_file():
            raise SelectionRefused(f"{path}: not a regular file")
        self.read_paths.add(path)
        with target.open("rb") as handle:
            return handle.read(count).decode("utf-8", "replace")

    def scan(self, directory: str, suffix: str, needle: bytes) -> list[str]:
        """Every file below a directory with this suffix holding these bytes. A scan is named by the fact that makes it, not listed as inputs."""
        found = []
        for path in sorted((self.root / directory).rglob(f"*{suffix}")):
            if path.is_file() and needle in path.read_bytes():
                found.append(path.relative_to(self.root).as_posix())
        return found


@dataclass(frozen=True)
class Selection:
    """What one requirement's record reads and runs."""
    id: str
    requirement_id: str
    facts: object  # (Reader) -> dict[str, str]
    runs: tuple[Run, ...]
    limitations: tuple[str, ...]


SELECTIONS: dict[str, Selection] = {}


def record_path(profile_dir: Path, selection_id: str) -> Path:
    return Path(profile_dir) / DIRECTORY / f"{selection_id}{SUFFIX}"


def _one(form, name):
    found = S.children(form, name)
    return str(found[0][1]) if found else None


def load_record(root: Path, path: Path) -> dict:
    """A retained record, schema-validated; anything else is a refusal."""
    if path.is_symlink() or not path.is_file() or path.stat().st_size > DOCUMENT_BYTES:
        raise SelectionRefused(f"{path}: not a bounded regular file")
    schema = Path(root) / SCHEMA
    try:
        constructs, operators = K.load_schema(schema)
        text = path.read_text("utf-8")
        errors = K.validate_text(text, constructs, operators, path.as_posix(), parse_where=str(path))
    except (K.SchemaError, S.SexpError, UnicodeError, OSError) as error:
        raise SelectionRefused(f"{path}: {error}") from error
    if errors:
        raise SelectionRefused(f"{path}: " + "; ".join(str(e) for e in errors[:3]))
    forms = [f for f in S.parse(text, str(path)) if isinstance(f, list) and f and str(f[0]) == "selection"]
    if len(forms) != 1:
        raise SelectionRefused(f"{path}: exactly one selection form expected")
    form = forms[0]
    return dict(id=_one(form, "id"), requirement_id=_one(form, "requirement_id"),
                obligation_ids=[str(c[1]) for c in S.children(form, "obligation_ids")],
                disposition=_one(form, "disposition"),
                runs=[dict(command=_one(r, "command"), serves=[str(c[1]) for c in S.children(r, "serves")],
                           rc=int(S.children(r, "rc")[0][1]), output=_one(r, "output"), repeated=_one(r, "repeated"))
                      for r in S.children(form, "run")],
                facts={_one(f, "id"): _one(f, "observed") for f in S.children(form, "fact")},
                limitations=[str(c[1]) for c in S.children(form, "limitation")])


def _catalogue_facts(root: Path, profile_dir: Path, requirement_id: str, obligation_ids: list[str]) -> tuple[list[str], str | None, list[dict] | None]:
    """What the catalogues say of this requirement: every required check of its obligations, its statement and its trace."""
    obligations = R.load(profile_dir / "contract-obligations.sexp", root=root)
    required = [check for o in obligations if o["id"] in obligation_ids for check in o["required_checks"]]
    statement = next((r["statement"] for r in R.load(profile_dir / "requirements.sexp", root=root) if r["id"] == requirement_id), None)
    return required, statement, ST.load_trace(root, profile_dir).get(requirement_id)


def review(root: Path, profile_dir: Path, selection_id: str, requirement_id: str, obligation_ids: list[str],
           selections: dict | None = None) -> list[str]:
    """Why this selection's record does not stand; empty when it does. Reads files; starts no process."""
    table = SELECTIONS if selections is None else selections
    root, profile_dir = Path(root), Path(profile_dir)
    path = record_path(profile_dir, selection_id)
    try:
        record = load_record(root, path)
        declared = DS.load(root, profile_dir).get(requirement_id)
        required, statement, clauses = _catalogue_facts(root, profile_dir, requirement_id, obligation_ids)
    except (SelectionRefused, DS.DispositionRefused, ST.TraceRefused, R.RecordRefused, S.SexpError, OSError) as error:
        return [f"record unreadable: {error}"]
    reasons: list[str] = []
    if record["id"] != selection_id:
        reasons.append(f"record names {record['id']}, not {selection_id}")
    if record["requirement_id"] != requirement_id:
        reasons.append(f"record answers {record['requirement_id']}, not {requirement_id}")
    if not set(obligation_ids) <= set(record["obligation_ids"]):
        reasons.append("record does not bind every credited obligation")
    if declared is None or declared["kind"] != "record":
        reasons.append(f"no kind record disposition answers {requirement_id}")
        return reasons
    if declared["id"] != record["disposition"]:
        reasons.append(f"record names disposition {record['disposition']}, the catalogue declares {declared['id']}")
    expected = declared["expect"]
    if set(expected) != set(record["facts"]):
        reasons.append(f"declared facts {sorted(expected)} differ from the record's {sorted(record['facts'])}")
    for name in sorted(set(expected) & set(record["facts"])):
        if record["facts"][name] != expected[name]:
            reasons.append(f"fact {name}: observed {record['facts'][name]!r}, the disposition expects {expected[name]!r}")
    selection = table.get(requirement_id)
    if selection is None or selection.id != selection_id:
        reasons.append(f"no reader for {selection_id}")
    else:
        try:
            live = selection.facts(Reader(root))
        except (SelectionRefused, OSError, ValueError, KeyError, IndexError) as error:
            reasons.append(f"facts cannot be read: {error}")
        else:
            for name in sorted(set(record["facts"]) | set(live)):
                if record["facts"].get(name) != live.get(name):
                    reasons.append(f"fact {name}: the tree reads {live.get(name)!r}, the record {record['facts'].get(name)!r}")
    served = {check for run in record["runs"] for check in run["serves"]}
    for check in required:
        if check not in served:
            reasons.append(f"required check {check}: no retained run serves it")
    for run in record["runs"]:
        if run["rc"] != 0:
            reasons.append(f"run {run['command']}: exit {run['rc']}")
        if run["repeated"] != "identical":
            reasons.append(f"run {run['command']}: its repeat differs")
    if clauses is None or statement is None:
        reasons.append(f"{requirement_id} has no statement trace")
    else:
        held, measured = ST.measure(statement, clauses, sorted(record["facts"]), "; ".join(record["limitations"]))
        if not held:
            reasons.append(f"statement trace: {measured}")
    return reasons


def _execute(root: Path, run: Run) -> tuple[int, str]:
    done = subprocess.run(run.argv, cwd=root, capture_output=True, text=True, check=False, timeout=1800)
    return done.returncode, (done.stdout + done.stderr).replace(str(root), ".")


def _command_text(root: Path, argv: tuple[str, ...]) -> str:
    """The command as a reader would type it: `python3`, and no path outside the repository."""
    words = ["python3" if word == sys.executable else word for word in argv]
    return " ".join(word.replace(f"{root}/", "") for word in words)


def build_record(root: Path, profile_dir: Path, selection: Selection, date: str, prepare=None) -> str:
    """Run everything once and again, and render the record. `prepare`, when given, makes the retained artifacts the facts read."""
    root, profile_dir = Path(root), Path(profile_dir)
    if record_path(profile_dir, selection.id).exists():
        raise SelectionRefused(f"{selection.id} already holds a record: a new selection is a new record and a new credit")
    declared = DS.load(root, profile_dir).get(selection.requirement_id)
    if declared is None or declared["kind"] != "record":
        raise SelectionRefused(f"{selection.requirement_id}: no kind record disposition is declared, and one must be before anything runs")
    requirement = next((r for r in R.load(profile_dir / "requirements.sexp", root=root) if r["id"] == selection.requirement_id), None)
    if requirement is None:
        raise SelectionRefused(f"{selection.requirement_id}: not in this profile's requirements")
    runs = []
    for run in selection.runs:
        first, second = _execute(root, run), _execute(root, run)
        runs.append((run, first, first == second))
    reader = Reader(root)
    facts = selection.facts(reader)
    if set(facts) != set(declared["expect"]):
        raise SelectionRefused(f"{selection.id}: reads {sorted(facts)}, the disposition declares {sorted(declared['expect'])}")
    lines = [f";; {selection.id} — one measurement of a selection, taken by scripts/selections.py --record. Never edit it: the review reads it on every read.",
             f"(selection (id {R.quote_string(selection.id)}) (requirement_id {R.quote_string(selection.requirement_id)})"]
    lines += [f"  (obligation_ids {R.quote_string(o)})" for o in requirement["obligation_ids"]]
    lines.append(f"  (disposition {R.quote_string(declared['id'])}) (runner \"scripts/selections.py\") (date {R.quote_string(date)})")
    for path in sorted(reader.read_paths):
        data = (root / path).read_bytes()
        lines.append(f"  (input (path {R.quote_string(path)}) (sha256 \"{hashlib.sha256(data).hexdigest()}\") (byte_size {len(data)}))")
    for run, (rc, output), same in runs:
        serves = "".join(f" (serves {R.quote_string(c)})" for c in run.serves)
        lines.append(f"  (run (command {R.quote_string(_command_text(root, run.argv))}){serves} (rc {rc}) (output {R.quote_string(output.strip())})"
                     f" (repeated {'identical' if same else 'different'}))")
    for name in sorted(facts):
        lines.append(f"  (fact (id {R.quote_string(name)}) (observed {R.quote_string(facts[name])}))")
    lines += [f"  (limitation {R.quote_string(limit)})" for limit in selection.limitations]
    lines[-1] += ")"
    return "\n".join(lines) + "\n"


# ---- What each of the four reads (P4-SYSTEM.14 a51-12). Each statement's words decide what a fact is; the disposition declares its value.

UNIT = "profiles/rv64gc-lab-v0"
FP_SOURCE = "crates/semulith-core/src/fp.rs"
ABI_DIR = f"{UNIT}/{DIRECTORY}"
ABI_SOURCE = f"{ABI_DIR}/abi-probe.c"
ABIS = ("lp64d", "lp64", "lp64f")
ABI_FLAGS = ("--target=riscv64-unknown-elf", "-march=rv64gc", "-mno-relax", "-mcmodel=medany", "-O2", "-ffreestanding", "-fno-builtin", "-nostdlib")


def _form(reader: Reader, path: str, head: str) -> list:
    forms = [f for f in S.parse(reader.text(path), path) if isinstance(f, list) and f and str(f[0]) == head]
    if len(forms) != 1:
        raise SelectionRefused(f"{path}: exactly one {head} form expected")
    return forms[0]


def _elf_fact(data: bytes) -> str:
    """A relocatable object's class, machine, flags and `.text`, from its own section table."""
    if data[:4] != b"\x7fELF" or data[4] != 2 or data[5] != 1:
        return "not a little-endian ELFCLASS64 file"
    machine, flags = struct.unpack("<H", data[18:20])[0], struct.unpack("<I", data[48:52])[0]
    shoff = struct.unpack("<Q", data[40:48])[0]
    shentsize, shnum, shstrndx = struct.unpack("<HHH", data[58:64])
    sections = [struct.unpack("<IIQQQQIIQQ", data[shoff + i * shentsize:shoff + i * shentsize + 64]) for i in range(shnum)]
    names = data[sections[shstrndx][4]:sections[shstrndx][4] + sections[shstrndx][5]]
    text = [s for s in sections if names[s[0]:names.index(b"\0", s[0])] == b".text"]
    if len(text) != 1:
        return f"{len(text)} .text sections"
    return f"ELFCLASS64 machine={machine} flags={flags:#x} text={data[text[0][4]:text[0][4] + text[0][5]].hex()}"


def abi_facts(reader: Reader) -> dict[str, str]:
    campaign = reader.text("scripts/run_workload_campaign.py")
    flags = re.search(r"^CFLAGS = \[(.*?)\]", campaign, re.M | re.S)
    words = re.findall(r'"(-m(?:arch|abi)=[^"]+)"', flags[1]) if flags else []
    pinned = re.findall(r'^LLVM_VERSION = "([^"]+)"$', reader.text("scripts/riscv_toolchain.py"), re.M)
    facts = {f"object-{abi}": _elf_fact(reader.bytes(f"{ABI_DIR}/abi-{abi}.o")) for abi in ABIS}
    facts["workload-flags"] = " ".join(words)
    facts["toolchain-pin"] = " ".join(pinned)
    return facts


def build_abi_objects(root: Path) -> str:
    """The fixture under each ABI, by the pinned toolchain. Each object is retained, and its bytes are what a fact reads."""
    tools = T.select(Path(root) / "target/selections", require_nm=False)
    directory = Path(root) / ABI_DIR
    identity = subprocess.run([tools.clang, "--version"], capture_output=True, text=True, check=True).stdout.splitlines()[0]
    lines = [identity]
    for abi in ABIS:
        out = directory / f"abi-{abi}.o"
        subprocess.run([tools.clang, *ABI_FLAGS, f"-mabi={abi}", "-c", ABI_SOURCE, "-o", str(out.relative_to(root))],
                       cwd=root, check=True, capture_output=True, text=True)
        lines.append(f"abi-{abi}.o {hashlib.sha256(out.read_bytes()).hexdigest()}")
    return "\n".join(lines)


def fp_facts(reader: Reader) -> dict[str, str]:
    manifest = reader.text("crates/semulith-core/Cargo.toml")
    lock = [block for block in reader.text("Cargo.lock").split("[[package]]") if re.search(r'^name = "rustc_apfloat"$', block, re.M)]
    locked = [" ".join(re.findall(r'^(?:version|checksum) = "([^"]+)"$', block, re.M)) for block in lock]
    consumers = []
    for path in reader.scan("crates", ".rs", b"rustc_apfloat") + reader.scan("xtask", ".rs", b"rustc_apfloat"):
        code = [line.split("//", 1)[0] for line in (reader.root / path).read_text("utf-8").splitlines()]
        kinds = {"re-exports" if re.search(r"\bpub use rustc_apfloat\b", line) else "uses"
                 for line in code if re.search(r"\b(?:use rustc_apfloat\b|rustc_apfloat::)", line)}
        consumers += [f"{path} {kind}" for kind in sorted(kinds)]
    profile = _form(reader, f"{UNIT}/profile.sexp", "profile")
    selected = sorted({str(c[1]) for c in S.children(profile, "extensions")} & {"F", "D"})
    requirement = next(f for f in S.parse(reader.text(f"{UNIT}/requirements.sexp"), "requirements") if isinstance(f, list) and f
                       and str(f[0]) == "requirement" and str(S.field(f, "id")) == "REQ-D-FP-DEFER")
    status = lambda path: re.findall(r"^- \*\*Status:\*\* `([^`]+)`$", reader.text(path), re.M)
    decisions = "docs/decisions/"
    closing = reader.text(f"{decisions}reference_fp-model-layer-acceptance.md")
    return {"backend-requirement": " ".join(re.findall(r'^rustc_apfloat\s*=\s*"([^"]+)"\s*$', manifest, re.M)),
            "backend-artifact": " | ".join(locked),
            "model-layer": FP_SOURCE if (reader.root / FP_SOURCE).is_file() else "absent",
            "backend-consumers": "; ".join(consumers),
            "f-and-d-selected": " ".join(selected),
            "needs-the-abi": " ".join(str(c[1]) for c in S.children(requirement, "dependencies")),
            "qualification-status": " ".join(status(f"{decisions}decision_fp-backend-qualification.md") + status(f"{decisions}reference_fp-model-layer-acceptance.md")),
            "flag-corrections-recorded": "overflow/underflow" if "overflow/underflow" in closing else "not named",
            "shared-ancestry-status": " ".join(status(f"{decisions}reference_softfloat-shared-ancestry.md"))}


def definition_facts(reader: Reader) -> dict[str, str]:
    profile = _form(reader, f"{UNIT}/profile.sexp", "profile")
    encoding = _form(reader, f"{UNIT}/encoding.sexp", "encoding")
    part = S.children(encoding, "compose")[0]
    owners = [line.split("\t") for line in reader.text("doctrine/fact_ownership.tsv").splitlines() if line and not line.startswith("#")]
    mirrors = {"state": "crates/semulith-core/src/state_rv64gc.rs", "definition": "crates/semulith-core/src/definition_rv64gc.rs",
               "guests": "crates/semulith-verify/src/guests_rv64gc.rs"}
    facts = {"vehicle": str(S.field(S.children(profile, "vehicle")[0], "route")),
             "composition": f"{S.field(part, 'status')}, {len(S.children(part, 'slot'))} unbound slots, base {S.field(part, 'base')}"}
    for name, mirror in mirrors.items():
        header = reader.head(mirror, 200).split("\n", 1)[0]
        generator = re.search(r"python3 (scripts/gen_[a-z]+\.py)", header)
        gates = sorted({row[3] for row in owners if len(row) >= 4 and row[2] == mirror})
        facts[f"mirror-{name}"] = f"{'GENERATED' if header.startswith('//! GENERATED') else 'not marked generated'}, {generator[1] if generator else 'no generator'}, {' '.join(gates)}"
    registered = reader.text("scripts/check_doctrines.project.sh")
    facts["drift-gates"] = " ".join(sorted(g for g in ("DEF-GEN", "GUEST-GEN", "STATE-GEN") if f'"{g}|' in registered))
    return facts


def _scope(reader: Reader, unit: str) -> tuple[list, list[str]]:
    scope = S.children(_form(reader, f"profiles/{unit}/profile.sexp", "profile"), "scope")[0]
    names = [str(n).lower() for fam in scope[1:] if isinstance(fam, list) and fam and str(fam[0]).startswith(("base_", "rv64_")) for n in fam[1:] if type(n) is str]
    return scope, names


def census_facts(reader: Reader) -> dict[str, str]:
    scope, base = _scope(reader, "rv64gc-lab-v0")
    other, reference = _scope(reader, "rv64i-lab-v0")
    declared = E._scope_names(_form(reader, f"{UNIT}/profile.sexp", "profile"), "selection")
    reader.text(f"{UNIT}/encoding.sexp")
    resolved = E._encoding_names(reader.root / UNIT)
    source = str(S.field(scope, "source"))
    return {"base-census": f"{len(base)} forms, {S.field(scope, 'count_base')} base and {S.field(scope, 'count_rv64i_additions')} RV64I additions",
            "same-enumeration-as-rv64i": f"{len(set(base) & set(reference))} shared, {len(set(base) ^ set(reference))} differ",
            "same-source-as-rv64i": "yes" if source.startswith(str(S.field(other, "source"))) else "no",
            "total": f"{S.field(scope, 'count_total')} stated, {len(declared)} enumerated",
            "grows-with-its-fragments": f"{len(declared & resolved)} resolved in the composition, {len(declared ^ resolved)} differ"}


def _scope_check(check: str) -> Run:
    return Run((sys.executable, "-B", "scripts/check_gc_contract_scope.py", "--check", check), (check,))


SELECTIONS.update({
    "REQ-D-ABI": Selection(
        "SEL-ABI", "REQ-D-ABI", abi_facts,
        (_scope_check("CHK-ABI-POS"), _scope_check("CHK-ABI-NEG"),
         Run((sys.executable, "-B", "scripts/selections.py", "--profile", "rv64gc-lab-v0", "--requirement", "REQ-D-ABI", "--build"))),
        ("the assembler's own guests carry no calling convention and are tagged soft-float by design (scripts/probe_elf_writer.py), so this reads what the pinned compiler builds, not those",
         "the ACT suites assemble under -mabi=lp64 for the same reason: they make no calls across the ABI",
         "one function shows the convention, and it does not exercise the whole of the psABI")),
    "REQ-D-FP-DEFER": Selection(
        "SEL-FP-DEFER", "REQ-D-FP-DEFER", fp_facts,
        (_scope_check("CHK-GC-FP-QUALIFIED-V3-POS"), _scope_check("CHK-GC-FP-QUALIFIED-V3-NEG"),
         Run(("cargo", "tree", "--locked", "--offline", "-p", "semulith-core", "-e", "normal", "--depth", "1", "--prefix", "none")),
         Run(("bash", "scripts/check_fp_vectors.sh"))),
        ("the numeric and instruction guarantees are REQ-GC-F's and REQ-GC-D's own credits: this reads which backend was selected and how it is held",
         "the qualification decision and the closing measurement are read as active records, and their finite evidence is theirs")),
    "REQ-D-ROUTE-FLIP": Selection(
        "SEL-ROUTE-FLIP", "REQ-D-ROUTE-FLIP", definition_facts,
        (_scope_check("CHK-GC-DEFINITION-V3-POS"), _scope_check("CHK-GC-DEFINITION-V3-NEG")),
        ("selection and generated-route consistency are scope evidence: instruction behavior is established separately by executable checks",
         "a read here does not run the generators: their drift gates run in every commit's gate, and the record retains one run of each through the named check")),
    "REQ-D-SCOPE-CENSUS": Selection(
        "SEL-SCOPE-CENSUS", "REQ-D-SCOPE-CENSUS", census_facts,
        (_scope_check("CHK-SCOPE-CENSUS-POS"), _scope_check("CHK-SCOPE-CENSUS-NEG")),
        ("the census is compared with the composition and with rv64i-lab-v0's enumeration; that each form is executed is EXERCISE-COVERAGE's, and that it behaves is each extension's credit",
         "the listings themselves are the citations' to hold (scripts/check_citations.py)")),
})


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--profile", required=True)
    parser.add_argument("--requirement", required=True)
    parser.add_argument("--record", action="store_true", help="take this selection's one record, then read it")
    parser.add_argument("--date", help="the record's date, with --record")
    parser.add_argument("--build", action="store_true", help="REQ-D-ABI's objects, as its record's run asks")
    args = parser.parse_args(argv)
    if args.build:
        if args.requirement != "REQ-D-ABI":
            parser.error("--build is REQ-D-ABI's")
        print(build_abi_objects(ROOT))
        return 0
    profile_dir = ROOT / "profiles" / args.profile
    selection = SELECTIONS.get(args.requirement)
    if selection is None:
        print(f"SELECTIONS: refused: no selection answers {args.requirement}", file=sys.stderr)
        return 2
    if args.record:
        if not args.date:
            parser.error("--record needs --date")
        try:
            text = build_record(ROOT, profile_dir, selection, args.date)
        except SelectionRefused as error:
            print(f"SELECTIONS: refused: {error}", file=sys.stderr)
            return 3
        path = record_path(profile_dir, selection.id)
        path.parent.mkdir(exist_ok=True)
        path.write_text(text, "utf-8")
    requirement = next((r for r in R.load(profile_dir / "requirements.sexp", root=ROOT) if r["id"] == args.requirement), None)
    obligations = requirement["obligation_ids"] if requirement else []
    reasons = review(ROOT, profile_dir, selection.id, args.requirement, obligations)
    for reason in reasons:
        print(f"  {reason}")
    if reasons:
        print(f"SELECTIONS: {selection.id}: does not stand; read only, nothing granted")
        return 1
    print(f"SELECTIONS: {selection.id}: stands; read only, nothing granted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
