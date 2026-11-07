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
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_sexp_schema as K  # noqa: E402  (pinned by the finite cases; read, never changed)
import dispositions as DS  # noqa: E402
import records_sexp as R  # noqa: E402
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


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--profile", required=True)
    parser.add_argument("--requirement", required=True)
    parser.add_argument("--record", action="store_true", help="take this selection's one record, then read it")
    parser.add_argument("--date", help="the record's date, with --record")
    args = parser.parse_args(argv)
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
