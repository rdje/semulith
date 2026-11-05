#!/usr/bin/env python3
"""The effective contract's measure: what a unit declares, and what its registry realizes.

Its own module since `P4-SYSTEM.14` a43e-1 (`decision_dossier-copies-retire-at-the-next-window.md`). `experiment_verification.py` needs this one computation, and importing it from
`gate_report.py` made a report generator a pinned input of every retained experiment, so editing a report lapsed evidence.
"""
from __future__ import annotations

from pathlib import Path
import re

import sexp as S

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# The G-CONTRACT measure (`P4-SYSTEM.10` slice a) — ONE computation, every builder.
# ⛔ The third wrong cut, after the two recorded in `build()`: an implemented check was any id a
# tracked executable under `scripts/`/`crates/` NAMES — across the whole tree. MIRROR-DERIVE makes
# 26 check ids identical across rv64i's and rv64gc's contracts (13 base mirrors, field-equal by
# enforcement), so realizing one for rv64gc credited rv64i with a check nothing of rv64i's runs.
# And the denominator counted every record, including those a later contract version SUPERSEDED.
# The measure is now the unit's own: a check is implemented for a unit exactly when THAT unit's
# registry — named by its contract document, its every entry run by `cargo test` — realizes it
# under the obligation that declares it; the denominator is the EFFECTIVE contract.
# ---------------------------------------------------------------------------

_ENTRY = re.compile(r'\bContractCheck\s*\{\s*id:\s*"([^"]+)",\s*obligation:\s*"([^"]+)",')
_OPENED = re.compile(r'(?<!struct )\bContractCheck\s*\{')


def _registry_pairs(path: Path) -> set[tuple[str, str]]:
    """The (obligation, check) pairs a registry realizes — read EXACTLY: an entry this
    reader cannot parse is a refusal, never a silent miss (a miss would deflate the count)."""
    text = path.read_text(encoding="utf-8")
    entries = _ENTRY.findall(text)
    opened = len(_OPENED.findall(text))
    if len(entries) != opened:
        raise SystemExit(f"effective_contract: {path.relative_to(ROOT)}: {opened} ContractCheck "
                         f"entries, {len(entries)} read exactly — the registry's shape changed "
                         f"and this measure cannot judge it")
    return {(ob, chk) for chk, ob in entries}


def contract_measure(d: Path, obs: list[dict]) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """(the EFFECTIVE contract's declared (obligation, check) pairs, the ones THIS unit's
    registry realizes). The effective contract is the latest version's members and everything
    it inherits, minus every record a version in that chain supersedes; a unit with no
    contract document (rv64i) is all of its records. A unit whose contract names no registry
    realizes nothing."""
    by_id = {o["id"]: o for o in obs}
    cdoc = d / "contract.sexp"
    effective, registry = list(obs), None
    if cdoc.is_file():
        versions, regs = {}, []
        for form in S.read_file(cdoc):
            if not isinstance(form, list) or not form:
                continue
            head = str(form[0])
            if head == "registry":
                regs.append(str(S.field(form, "path", cdoc.name)))
            if head != "contract":
                continue
            f = {str(c[0]): c for c in form[1:] if isinstance(c, list)}
            versions[str(f["id"][1])] = {
                "version": int(str(f["version"][1])),
                "extends": str(f["extends"][1]) if "extends" in f else None,
                "members": [str(S.field(c, "id", cdoc.name)) for c in S.children(form, "member")],
                "sups": {str(S.field(c, "record", cdoc.name)) for c in S.children(form, "supersede")}}
        numbers = sorted(v["version"] for v in versions.values())
        if not numbers or len(numbers) != len(set(numbers)) or len(regs) > 1:
            raise SystemExit(f"effective_contract: {cdoc.relative_to(ROOT)}: the versions {numbers} and "
                             f"{len(regs)} registry form(s) do not name one latest version and at "
                             f"most one registry — this measure cannot judge it")
        v = next(v for v in versions.values() if v["version"] == numbers[-1])
        members, superseded = [], set()
        ancestry = set()
        while v is not None:
            # Version numbers were checked unique above; a repeated number
            # therefore revisits the same version rather than adding ancestry.
            if v["version"] in ancestry:
                raise SystemExit(f"effective_contract: {cdoc.relative_to(ROOT)}: CONTRACT CYCLE: "
                                 f"revisits version {v['version']}")
            ancestry.add(v["version"])
            members += v["members"]
            superseded |= v["sups"]
            v = versions.get(v["extends"]) if v["extends"] else None
        effective = [by_id[m] for m in members if m not in superseded]
        registry = ROOT / regs[0] if regs else None
    declared = [(o["id"], c) for o in effective for c in o["required_checks"]]
    realized = _registry_pairs(registry) if registry is not None else set()
    return declared, [pair for pair in declared if pair in realized]
