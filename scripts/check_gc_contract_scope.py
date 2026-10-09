#!/usr/bin/env python3
"""Run named rv64gc contract scope checks over canonical parsed declarations.

The POS check validates the selection; NEG validates it first, then requires each
violating in-memory copy to fail for its own named reason. This establishes scope
consistency, never instruction correctness. No files, engines or caches are written.
The Rust contract registry runs these checks in the ordinary test suite.
"""

from __future__ import annotations

import argparse
import copy
from pathlib import Path

import sexp as S

ROOT = Path(__file__).resolve().parent.parent
UNIT = ROOT / "profiles/rv64gc-lab-v0"
# Exact selected scope: RVI-NAMING 36.1's G, RVI-ZICNTR 6.1, RVI-C 27.1,
# RVP-SSTC 12.1 and D-SVADE. These are expectations, not a recount of the inputs.
PROFILE_EXTENSIONS = {"M", "A", "F", "D", "C", "Zicntr", "Zicsr", "Zifencei", "Sstc", "Svade"}
# Sstc/Svade are CSR/walk policy; the nine encoding fragments include system.
FRAGMENTS = {"riscv/zicsr", "riscv/zicntr", "riscv/system", "riscv/a", "riscv/zifencei",
             "riscv/f", "riscv/d", "riscv/m", "riscv/c"}


class ScopeRefused(Exception):
    """A scope declaration or a check/control does not satisfy its contract."""


def document(path: Path, name: str) -> list:
    forms = [f for f in S.read_file(path) if isinstance(f, list) and f and f[0] == name]
    if len(forms) != 1:
        raise ScopeRefused(f"DOCUMENT: {path.name} must contain exactly one {name}")
    return forms[0]


def values(form: list, name: str) -> list[str]:
    children = S.children(form, name)
    if any(len(c) != 2 or isinstance(c[1], list) for c in children):
        raise ScopeRefused(f"FIELD: {name} must contain one scalar per occurrence")
    return [str(c[1]) for c in children]


def composition(profile: list, encoding: list, mutation: str | None) -> str | None:
    """First violated predicate, with a stable reason for the negative witness."""
    if mutation != "ignore-profile":
        if S.field(profile, "base") != "RV64I" or S.field(profile, "xlen") != 64:
            return "PROFILE-BASE"
        extensions = values(profile, "extensions")
        if len(extensions) != len(PROFILE_EXTENSIONS) or set(extensions) != PROFILE_EXTENSIONS:
            return "PROFILE-EXTENSIONS"
    if mutation != "ignore-fragments":
        parts = S.children(encoding, "compose")
        if len(parts) != 1:
            return "COMPOSITION-COUNT"
        part = parts[0]
        if S.field(part, "base") != "riscv/rv64i":
            return "FRAGMENT-BASE"
        fragments = values(part, "extensions")
        if len(fragments) != len(FRAGMENTS) or set(fragments) != FRAGMENTS:
            return "FRAGMENT-EXTENSIONS"
        if S.field(part, "status") != "complete" or S.children(part, "slot"):
            return "COMPOSITION-STATUS"
    return None


def set_field(form: list, name: str, value: S.Sexp) -> None:
    fields = S.children(form, name)
    if len(fields) != 1:
        raise ScopeRefused(f"CONTROL: expected exactly one {name} to mutate")
    fields[0][1] = value


def run(check: str, mutation: str | None = None) -> str:
    if check not in {"CHK-GC-COMPOSITION-POS", "CHK-GC-COMPOSITION-NEG"}:
        raise ScopeRefused(f"UNKNOWN-CHECK: {check}")
    profile = document(UNIT / "profile.sexp", "profile")
    encoding = document(UNIT / "encoding.sexp", "encoding")
    reason = composition(profile, encoding, mutation)
    if reason is not None:
        raise ScopeRefused(f"{check}: canonical selection violates {reason}")
    if check.endswith("-POS"):
        return f"GC-CONTRACT-SCOPE: {check} holds (parsed profile and complete composition)"

    # Each fixture is isolated; no failed predicate can mask the next fixture.
    fixtures = []
    p = copy.deepcopy(profile)
    p.remove(next(c for c in S.children(p, "extensions") if c[1] == "C"))
    fixtures.append(("missing C", p, encoding, "PROFILE-EXTENSIONS"))
    p = copy.deepcopy(profile)
    p.append([S.Symbol("extensions"), "H"])
    fixtures.append(("extra H", p, encoding, "PROFILE-EXTENSIONS"))
    p = copy.deepcopy(profile)
    set_field(p, "xlen", 32)
    fixtures.append(("wrong XLEN", p, encoding, "PROFILE-BASE"))
    e = copy.deepcopy(encoding)
    part = S.children(e, "compose")[0]
    part.remove(next(c for c in S.children(part, "extensions") if c[1] == "riscv/c"))
    fixtures.append(("unbound C", profile, e, "FRAGMENT-EXTENSIONS"))
    e = copy.deepcopy(encoding)
    set_field(S.children(e, "compose")[0], "base", "riscv/rv32i")
    fixtures.append(("wrong fragment base", profile, e, "FRAGMENT-BASE"))
    e = copy.deepcopy(encoding)
    set_field(S.children(e, "compose")[0], "status", S.Symbol("partial"))
    fixtures.append(("partial composition", profile, e, "COMPOSITION-STATUS"))
    for label, p, e, expected in fixtures:
        actual = composition(p, e, mutation)
        if actual != expected:
            raise ScopeRefused(f"CONTROL-MISSED: {label}: expected {expected}, got {actual}")
    return f"GC-CONTRACT-SCOPE: {check} holds ({len(fixtures)} violating copies refused)"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", required=True)
    parser.add_argument("--mutation", choices=("ignore-profile", "ignore-fragments"),
                        help="discrimination control: deliberately disable one predicate family")
    args = parser.parse_args()
    try:
        print(run(args.check, args.mutation))
    except (ScopeRefused, S.SexpError) as error:
        print(f"GC-CONTRACT-SCOPE: REFUSED - {error}")
        return 2 if isinstance(error, ScopeRefused) and str(error).startswith("UNKNOWN-CHECK:") else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
