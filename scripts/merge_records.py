#!/usr/bin/env python3
"""Record merge across a composition boundary — the thing the format split made impossible.

`SOT-FORMAT.5`. Encoding union is decidable and checked (`scripts/check_encoding_disjoint.py`);
this is the same operator for the records a unit carries: requirements, obligations, pinned
sources. A board composing two processors must merge these too, and under the retired split —
S-expressions for definitions, JSON Lines for records, TOML for sources — no rule could state
the union. One format is what makes the union definable at all.

THE MERGE RULE (design recorded in the owning leaf, `docs/tasks/SOT-FORMAT.md`, before code):

  unit      a directory carrying up to three catalogues BY NAME — requirements.sexp,
            contract-obligations.sexp, sources.sexp — read through the single mapping owners
            (`records_sexp.py`, `dossier_sexp.py`). A missing catalogue is the empty set; a
            missing directory is REFUSED (composing nothing is not composing).
  key       a record merges by its `id`; a source by its source `id`.
  collision same id in two units: every field must be equal EXCEPT `profile_ids`, which is
            membership (which units carry the record), not content — it unions by set-union.
            Any other difference is a CONFLICT, refused with the field, both values and both
            units named. Same id + different content in one composed unit is a catalogue
            lying about itself.
  sources   the same source id must pin identical bytes (sha256 and kin) — a digest difference
            means the units read different texts of "the same" specification. The document
            envelope (publication/revision/base_url/…) is per-unit metadata and is NOT part
            of the verdict; which envelope a future emitted composed ledger carries is its
            emitter's decision.
  closure   the union is closed: every `dependencies` id, every requirement `obligation_ids`
            and every `source_refs.source_id` must resolve in the union — RECORD-SCHEMA's
            rules 2/5/6 lifted from "within one file" to "within the composed unit".

THE DELIVERABLE IS THE CHECK, not a merged file — the shape of check_encoding_disjoint.py: a
verdict (`the units COMPOSE`) or a refusal naming every conflicting fact. The module is
importable (`merge_units(…)`) so MODEL-COMPOSE.3's assumption/guarantee discharge reads the
same merged view, including the direction census (cpu-guarantee vs environment-assumption) —
the assumption inventory docs/CPU_ENVIRONMENT.md §4 asks to export.

⛔ REFUSES RATHER THAN RECONCILES. There is no warning mode and no best-effort merge: two units
either compose or they do not, and a refusal names what contradicted. A merge tool that warns
is how a contradiction ships.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dossier_sexp as D                                # noqa: E402
import records_sexp as R                                # noqa: E402


class MergeRefused(Exception):
    """The units do not compose. Carries every conflicting fact, one per line."""


class UnitError(MergeRefused):
    """One unit is not composable on its own (unreadable, duplicate ids, missing)."""


# Membership, not content: the one field allowed to differ on an id collision.
_MEMBERSHIP = "profile_ids"

_CATALOGUES = (
    ("requirements", "requirements.sexp"),
    ("obligations", "contract-obligations.sexp"),
    ("sources", "sources.sexp"),
)


def _unit_label(path: Path) -> str:
    return str(path)


def load_unit(path: Path) -> dict:
    """A unit directory as three id → record tables, read through the mapping owners."""
    path = Path(path)
    if not path.is_dir():
        raise UnitError(f"unit '{path}' does not exist — composing nothing is not composing")
    unit: dict = {"label": _unit_label(path), "requirements": {}, "obligations": {},
                  "sources": {}}
    for kind, name in _CATALOGUES:
        cat = path / name
        if not cat.is_file():
            continue                                # absence is the empty set
        try:
            if kind == "sources":
                entries = D.load_sources(cat).get("source", [])
            else:
                entries = R.load(cat)
            ids = [_entry_id(e, kind, cat) for e in entries]
        except Exception as exc:                        # noqa: BLE001 — a unit we cannot read
            raise UnitError(f"unit '{path}': {name} does not map to records — {exc}")
        table = unit[kind]
        seen: dict = {}
        for entry, eid in zip(entries, ids):
            if eid in seen:
                raise UnitError(
                    f"unit '{path}': {name} carries {kind} id '{eid}' more than once — a "
                    f"catalogue that contradicts itself cannot compose")
            seen[eid] = entry
        table.update(seen)
    return unit


def _entry_id(entry: dict, kind: str, where: Path) -> str:
    eid = entry.get("id")
    if not isinstance(eid, str) or not eid:
        raise UnitError(f"{where}: a {kind} record has no usable id: {entry!r}")
    return eid


# --------------------------------------------------------------------------- the merge

class MergedUnit:
    """The composed view MODEL-COMPOSE.3 discharges against. Records in first-seen order."""

    def __init__(self, labels: list[str], requirements: dict, obligations: dict,
                 sources: dict):
        self.labels = labels
        self.requirements = requirements
        self.obligations = obligations
        self.sources = sources

    def direction_census(self) -> dict:
        census: dict = {}
        for o in self.obligations.values():
            census[o.get("direction", "?")] = census.get(o.get("direction", "?"), 0) + 1
        return census


def _content_fields(record: dict) -> dict:
    # membership and the carried-by marker are bookkeeping, not content: neither may
    # contradict on an id collision
    return {k: v for k, v in record.items() if k not in (_MEMBERSHIP, _CARRIED)}


def _absorb(merged: dict, table: dict, kind: str, unit: dict) -> list[str]:
    """Merge one unit's id → record table into the merged table. Returns conflicts."""
    conflicts: list[str] = []
    for key, rec in table.items():
        if key not in merged:
            merged[key] = rec
            continue
        base = merged[key]
        diffs = {f for f in _content_fields(rec)
                 if _content_fields(base).get(f) != rec.get(f)}
        if diffs:
            for f in sorted(diffs):
                conflicts.append(
                    f"CONFLICT {kind} '{key}' between units '{_carrier(base)}' and "
                    f"'{unit['label']}': field '{f}' differs — '{_carrier(base)}': "
                    f"{base.get(f)!r} vs '{unit['label']}': {rec.get(f)!r}")
        else:
            members = list(base.get(_MEMBERSHIP, []))
            for pid in rec.get(_MEMBERSHIP, []):
                if pid not in members:
                    members.append(pid)
            base[_MEMBERSHIP] = members
    return conflicts


# Each merged record remembers which unit carried it, so a conflict names both sides.
_CARRIED = "__carried_by__"


def _carried(table: dict, unit: dict) -> dict:
    for key, rec in table.items():
        rec[_CARRIED] = unit["label"]
    return table


def _carrier(rec: dict) -> str:
    return rec.get(_CARRIED, "?")


def merge_units(unit_dirs) -> MergedUnit:
    """The union of N units, or MergeRefused naming every conflicting fact."""
    units = []
    for d in unit_dirs:
        u = load_unit(Path(d))
        for kind, _name in _CATALOGUES:
            _carried(u[kind], u)
        units.append(u)

    merged_reqs: dict = {}
    merged_obs: dict = {}
    merged_srcs: dict = {}
    problems: list[str] = []
    for u in units:
        problems += _absorb(merged_reqs, u["requirements"], "requirement", u)
        problems += _absorb(merged_obs, u["obligations"], "obligation", u)
        problems += _absorb(merged_srcs, u["sources"], "source", u)

    problems += _closure(units, merged_reqs, merged_obs, merged_srcs)

    if problems:
        raise MergeRefused("\n".join(problems))

    for table in (merged_reqs, merged_obs, merged_srcs):
        for rec in table.values():
            rec.pop(_CARRIED, None)
    return MergedUnit([u["label"] for u in units], merged_reqs, merged_obs, merged_srcs)


def _closure(units, reqs: dict, obs: dict, srcs: dict) -> list[str]:
    """Every reference resolves in the union — RECORD-SCHEMA 2/5/6 across the boundary."""
    problems: list[str] = []
    for rid, r in reqs.items():
        for dep in r.get("dependencies", []):
            if dep not in reqs:
                problems.append(
                    f"DANGLING DEP requirement '{rid}' (unit '{_carrier(r)}') depends on "
                    f"'{dep}', which no unit provides")
        for oid in r.get("obligation_ids", []):
            if oid not in obs:
                problems.append(
                    f"UNDEFINED OBLIGATION requirement '{rid}' (unit '{_carrier(r)}') names "
                    f"'{oid}', which no unit's contract defines")
        for sr in r.get("source_refs", []):
            if sr["source_id"] not in srcs:
                problems.append(
                    f"UNPINNED SOURCE requirement '{rid}' (unit '{_carrier(r)}') cites "
                    f"'{sr['source_id']}', which no unit's sources.sexp pins")
    for oid, o in obs.items():
        for dep in o.get("dependencies", []):
            # The corpus writes both kinds: a cpu-guarantee depends on its requirement
            # (OB-XLEN -> REQ-D-XLEN), an environment-assumption on the guarantees it
            # assumes the environment will satisfy (OB-ENV-RESET -> OB-ENTRY-STATE). An
            # obligation's dependency therefore resolves against EITHER table.
            if dep not in reqs and dep not in obs:
                problems.append(
                    f"DANGLING DEP obligation '{oid}' (unit '{_carrier(o)}') depends on "
                    f"'{dep}', which no unit provides")
        for sr in o.get("source_refs", []):
            if sr["source_id"] not in srcs:
                problems.append(
                    f"UNPINNED SOURCE obligation '{oid}' (unit '{_carrier(o)}') cites "
                    f"'{sr['source_id']}', which no unit's sources.sexp pins")
    return problems


# --------------------------------------------------------------------------- CLI

def _census(table: dict) -> str:
    return f"{len(table)} record(s)"


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] == "--self-test":
        return _selftest()
    if len(argv) < 2:
        print("usage: merge_records.py <unit-dir>…   |   merge_records.py --self-test\n"
              "       A unit directory carries requirements.sexp / contract-obligations.sexp /\n"
              "       sources.sexp by name (any subset). Verdict on stdout; conflicts too;",
              file=sys.stderr)
        return 2
    try:
        merged = merge_units(argv[1:])
    except UnitError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    except MergeRefused as exc:
        print("REJECTED — these units do not compose:", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1
    census = merged.direction_census()
    directions = ", ".join(f"{v} {k}" for k, v in sorted(census.items())) or "none"
    print(f"composed: {len(merged.requirements)} requirement(s), "
          f"{len(merged.obligations)} obligation(s) ({directions}), "
          f"{len(merged.sources)} source(s) from {len(merged.labels)} unit(s)")
    print("the units COMPOSE")
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

    def unit(name: str, reqs=(), obs=(), srcs=()) -> Path:
        d = tmp / name
        d.mkdir(parents=True, exist_ok=True)
        if reqs:
            (d / "requirements.sexp").write_text(R.dump(list(reqs)))
        if obs:
            (d / "contract-obligations.sexp").write_text(R.dump(list(obs)))
        if srcs:
            (d / "sources.sexp").write_text(
                "(sources (publication \"P\") (revision \"r\") (base_url \"u\") "
                "(retrieved \"d\") (work_dir \"w\")\n" +
                "\n".join(
                    f'(source (id "{s["id"]}") (file "{s.get("file", "f.html")}") '
                    f'(title "t") (sha256 "{s["sha256"]}") (bytes {s.get("bytes", 1)}) '
                    f'(http_status 200) (supplies "s"))' for s in srcs) + ")\n")
        return d

    H = "a" * 64
    H2 = "b" * 64

    def req(rid, stmt="S", deps=(), obs_=(), srcs_=("SRC-A",), profiles=("p",), **kw):
        return {"id": rid, "profile_ids": list(profiles), "kind": "state", "statement": stmt,
                "source_refs": [{"source_id": s, "locator": "§1"} for s in srcs_],
                "applicability": "included", "research_status": "resolved",
                "implementation_status": "planned",
                "source_semantics": {"category": "defined", "detail": "d"},
                "risk": kw.get("risk", "low"), "obligation_ids": list(obs_),
                "dependencies": list(deps), "implementation_refs": [], "evidence_ids": []}

    def ob(oid, direction="cpu-guarantee", authority="architecture", contract="c",
           stmt="S", deps=(), srcs_=("SRC-A",), profiles=("p",), checks=("CHK-POS", "CHK-NEG")):
        return {"id": oid, "contract_id": contract, "contract_version": "0",
                "profile_ids": list(profiles), "direction": direction, "statement": stmt,
                "authority": authority,
                "source_refs": [{"source_id": s, "locator": "§1"} for s in srcs_],
                "parameters": {}, "dependencies": list(deps), "required_checks": list(checks)}

    def src(sid, sha=H):
        return {"id": sid, "sha256": sha}

    def composes(*dirs):
        try:
            return merge_units(dirs)
        except MergeRefused as exc:
            raise AssertionError(f"should compose, refused: {exc}")

    def refuses(dirs, needle):
        try:
            merge_units(dirs)
        except MergeRefused as exc:
            assert needle in str(exc), f"refused, but for the wrong reason: {exc}"
        else:
            raise AssertionError(f"composed; it must be refused ({needle})")

    # --- the union itself
    a = unit("a", reqs=[req("REQ-A")], obs=[ob("OB-A")], srcs=[src("SRC-A")])
    b = unit("b", reqs=[req("REQ-B", profiles=("q",))], obs=[ob("OB-B", contract="c2")],
             srcs=[src("SRC-B", sha=H2)])
    m = composes(a, b)
    arm("GREEN two disjoint units compose; counts add", lambda: (
        _eq(len(m.requirements), 2), _eq(len(m.obligations), 2), _eq(len(m.sources), 2)))

    m2 = composes(a, a)
    arm("GREEN idempotent self-merge — every record collides equal", lambda: (
        _eq(len(m2.requirements), 1), _eq(len(m2.obligations), 1), _eq(len(m2.sources), 1)))

    c = unit("c", reqs=[req("REQ-A", profiles=("c",))])     # same content, other membership
    m3 = composes(a, c)
    arm("GREEN a shared record unions profile_ids, kept once", lambda: (
        _eq(len(m3.requirements), 1),
        _eq(sorted(m3.requirements["REQ-A"]["profile_ids"]), ["c", "p"])))

    ext = unit("ext", reqs=[req("REQ-M", deps=("REQ-A",), profiles=("ext",))])
    arm("GREEN a cross-boundary dependency resolves in the union",
        lambda: _eq("REQ-M" in composes(a, ext).requirements, True))

    env_dep = unit("envdep", obs=[ob("OB-ENV", direction="environment-assumption",
                                      deps=("OB-A",))], srcs=[src("SRC-A")])
    arm("GREEN an environment-assumption may depend on the guarantee it discharges",
        lambda: _eq("OB-ENV" in composes(a, env_dep).obligations, True))

    env_ghost = unit("envghost", obs=[ob("OB-ENV2", direction="environment-assumption",
                                         deps=("OB-GHOST",))], srcs=[src("SRC-A")])
    arm("RED   an obligation depending on a record no unit provides",
        lambda: refuses([a, env_ghost], "DANGLING DEP"))

    m4 = composes(a, b)
    arm("GREEN the direction census is the .3 hook", lambda: (
        _eq(m4.direction_census(), {"cpu-guarantee": 2})))
    env = unit("env", obs=[ob("OB-ENV", direction="environment-assumption")], srcs=[src("SRC-A")])
    m5 = composes(a, env)
    arm("GREEN environment-assumptions count beside cpu-guarantees", lambda: (
        _eq(m5.direction_census(), {"cpu-guarantee": 1, "environment-assumption": 1})))

    same_src = unit("same", srcs=[src("SRC-A")])            # identical pins collapse
    m6 = composes(a, same_src)
    arm("GREEN the same source with identical pins merges to one", lambda: (
        _eq(len(m6.sources), 1)))

    # --- contradictions, each named
    bad = unit("bad", reqs=[req("REQ-A", stmt="a different statement")])
    arm("RED   same id, different statement — the conflicting fact named",
        lambda: refuses([a, bad], "field 'statement' differs"))

    bad_risk = unit("badrisk", reqs=[req("REQ-A", risk="critical")])
    arm("RED   same id, different risk — content fields all bite",
        lambda: refuses([a, bad_risk], "field 'risk' differs"))

    bad_src = unit("badsrc", srcs=[src("SRC-A", sha=H2)])
    arm("RED   same source id, different digest — two texts of one specification",
        lambda: refuses([a, bad_src], "field 'sha256' differs"))

    bad_ob = unit("badob", obs=[ob("OB-A", authority="laboratory")])
    arm("RED   same obligation id, different authority",
        lambda: refuses([a, bad_ob], "field 'authority' differs"))

    ghost = unit("ghost", reqs=[req("REQ-G", deps=("REQ-GHOST",))])
    arm("RED   a dependency resolving in no unit is named with its unit",
        lambda: refuses([a, ghost], "DANGLING DEP"))

    no_ob = unit("noob", reqs=[req("REQ-N", obs_=("OB-GHOST",))])
    arm("RED   an obligation id no unit's contract defines",
        lambda: refuses([a, no_ob], "UNDEFINED OBLIGATION"))

    no_src = unit("nosrc", reqs=[req("REQ-S", srcs_=("SRC-GHOST",))])
    arm("RED   a source no unit pins",
        lambda: refuses([a, no_src], "UNPINNED SOURCE"))

    dup = unit("dup", reqs=[req("REQ-D"), req("REQ-D", risk="critical")])
    arm("RED   a unit whose own catalogue repeats an id is refused",
        lambda: refuses([dup], "more than once"))

    arm("RED   a unit directory that does not exist",
        lambda: refuses([tmp / "nowhere"], "does not exist"))

    import shutil
    shutil.rmtree(tmp)
    print(f"merge_records --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


def _eq(got, want) -> None:
    assert got == want, f"got {got!r}, want {want!r}"


if __name__ == "__main__":
    sys.exit(main(sys.argv))
