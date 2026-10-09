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
import check_extraction as E

ROOT = Path(__file__).resolve().parent.parent
UNIT = ROOT / "profiles/rv64gc-lab-v0"
# Exact selected scope: RVI-NAMING 36.1's G, RVI-ZICNTR 6.1, RVI-C 27.1,
# RVP-SSTC 12.1 and D-SVADE. These are expectations, not a recount of the inputs.
PROFILE_EXTENSIONS = {"M", "A", "F", "D", "C", "Zicntr", "Zicsr", "Zifencei", "Sstc", "Svade"}
# Sstc/Svade are CSR/walk policy; the nine encoding fragments include system.
FRAGMENTS = {"riscv/zicsr", "riscv/zicntr", "riscv/system", "riscv/a", "riscv/zifencei",
             "riscv/f", "riscv/d", "riscv/m", "riscv/c"}
# D-CSR-SET's committed scope, sourced by RVP-CSR, RVI-F, RVI-ZICNTR and RVP-SSTC.
# These are independent expectations; comparing two equally shortened declarations
# must not pass. CSR field behavior is evidenced by execution, not this scope check.
CSR_NAMES = set("mhartid misa mstatus mtvec medeleg mideleg mie mip mscratch mepc mcause mtval "
                "menvcfg mcounteren mcycle minstret sstatus stvec sscratch sepc scause stval "
                "sie sip scounteren satp stimecmp cycle time instret fflags frm fcsr".split())
CSR_VIEWS = {"sstatus": "mstatus", "sie": "mie", "sip": "mip", "cycle": "mcycle",
             "time": "mcycle", "instret": "minstret", "fcsr": "fflags, frm"}
STRUCTURED = {"EXT-CLOSURE", "PRIV-REVISION", "CSR-SET", "NO-PMP", "NO-H", "SCOPE-CENSUS"}
# Rehashed from the public pinned v20260120 pages at P4-SYSTEM.13 b3. The check
# binds the declaration to these identities; artifact-byte verification remains
# CITATIONS' responsibility and is not inferred from the version string.
PRIVILEGE_PINS = {
    "RVP-MACHINE": "b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea",
    "RVP-SUPERVISOR": "d5186efc3ead1c1f693ac2b16aeccdcab95d990264f49b559252d2dc413a651a",
}


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


def named(form: list, head: str, ident: str) -> list:
    found = [f for f in S.children(form, head) if S.field(f, "id") == ident]
    if len(found) != 1:
        raise ScopeRefused(f"RECORD: expected exactly one {head} {ident}")
    return found[0]


def structured(key: str, data: dict) -> str | None:
    profile, state, sources = (data[k] for k in ("profile", "state", "sources"))
    extensions = set(values(profile, "extensions"))
    csrs = S.children(state, "csr")
    names = [str(S.field(c, "id")) for c in csrs]
    if key == "EXT-CLOSURE":
        if "D" in extensions and "F" not in extensions:
            return "DEPENDENCY-D-F"
        if "F" in extensions and "Zicsr" not in extensions:
            return "DEPENDENCY-F-ZICSR"
        c = set(values(S.children(profile, "scope")[0], "c_compressed"))
        # RV64+D selects Zca+Zcd; the four D memory forms, never RV32's Zcf.
        if "C" in extensions and "D" in extensions and (
                not {"C.FLD", "C.FLDSP", "C.FSD", "C.FSDSP"} <= c
                or {"C.FLW", "C.FLWSP", "C.FSW", "C.FSWSP"} & c):
            return "DEPENDENCY-C-ZCD"
    elif key == "PRIV-REVISION":
        if (S.field(profile, "spec_revision") != "v20260120"
                or S.field(sources, "revision") != "v20260120"):
            return "PUBLICATION-REVISION"
        for ident in ("RVP-MACHINE", "RVP-SUPERVISOR"):
            source = named(sources, "source", ident)
            if S.field(source, "chapter_version") != "1.13":
                return "PRIVILEGE-REVISION"
            if S.field(source, "sha256") != PRIVILEGE_PINS[ident]:
                return "SOURCE-PIN"
    elif key == "CSR-SET":
        selected = values(S.children(profile, "state")[0], "csrs")
        if (len(names) != len(CSR_NAMES) or set(names) != CSR_NAMES
                or set(selected) != CSR_NAMES or len(selected) != len(CSR_NAMES)):
            return "CSR-SELECTION"
        views = {str(S.field(c, "id")): str(S.field(c, "view_of"))
                 for c in csrs if S.children(c, "view_of")}
        if views != CSR_VIEWS:
            return "CSR-VIEWS"
        addresses = [S.field(c, "address") for c in csrs]
        if (len(set(addresses)) != len(addresses)
                or any(type(a) is not int or not 0 <= a < 4096 for a in addresses)):
            return "CSR-ADDRESSES"
    elif key == "NO-PMP":
        if any(n.startswith("pmp") for n in names):
            return "PMP-SELECTION"
        declaration = S.field(named(profile, "decision", "D-NO-PMP"), "statement")
        if not str(declaration).startswith("PMP is excluded at v0:"):
            return "PMP-DECLARATION"
    elif key == "NO-H":
        if "H" in extensions or set(values(profile, "privilege_modes")) != {"M", "S", "U"}:
            return "H-SELECTION"
        if (set(values(S.children(state, "privilege_mode")[0], "modes")) != {"m", "s", "u"}
                or any(n.startswith("h") for n in names)):
            return "H-STATE"
        declaration = S.field(named(profile, "decision", "D-NO-H"), "statement")
        if not str(declaration).startswith("The hypervisor extension is excluded:"):
            return "H-DECLARATION"
    elif key == "SCOPE-CENSUS":
        scope = S.children(profile, "scope")[0]
        declared = E._scope_names(profile, "contract scope")
        listed = [str(n).lower() for f in scope[1:] if isinstance(f, list) and f
                  and str(f[0]) not in {"authority", "source", "comment", "note"}
                  and not str(f[0]).startswith("count_") for n in f[1:] if type(n) is str]
        if len(listed) != len(declared) or S.field(scope, "count_total") != len(declared):
            return "SCOPE-COUNT"
        if declared != data["encoding_names"]:
            return "SCOPE-SET"
    else:
        raise ScopeRefused(f"UNKNOWN-SCOPE: {key}")
    return None


def structured_fixtures(key: str, original: dict) -> list[tuple[str, dict, str]]:
    fixtures = []

    def add(label, reason, edit):
        data = copy.deepcopy(original)
        edit(data)
        fixtures.append((label, data, reason))

    def remove_extension(data, ext):
        p = data["profile"]
        p.remove(next(c for c in S.children(p, "extensions") if c[1] == ext))

    if key == "EXT-CLOSURE":
        add("D without F", "DEPENDENCY-D-F", lambda d: remove_extension(d, "F"))
        add("F without Zicsr", "DEPENDENCY-F-ZICSR", lambda d: remove_extension(d, "Zicsr"))
        def no_zcd(d):
            scope = S.children(d["profile"], "scope")[0]
            scope.remove(next(f for f in S.children(scope, "c_compressed") if f[1] == "C.FLD"))
        add("D+C without FLD", "DEPENDENCY-C-ZCD", no_zcd)
    elif key == "PRIV-REVISION":
        add("wrong publication", "PUBLICATION-REVISION",
            lambda d: set_field(d["sources"], "revision", "v20240411"))
        for ident in ("RVP-MACHINE", "RVP-SUPERVISOR"):
            add(ident, "PRIVILEGE-REVISION",
                lambda d, ident=ident: set_field(
                    named(d["sources"], "source", ident), "chapter_version", "1.12"))
        add("different valid pin", "SOURCE-PIN", lambda d: set_field(
            named(d["sources"], "source", "RVP-MACHINE"), "sha256", "0" * 64))
    elif key == "CSR-SET":
        def shortened(d):
            state, p = d["state"], d["profile"]
            state.remove(named(state, "csr", "fcsr"))
            declared = S.children(S.children(p, "state")[0], "csrs")
            S.children(p, "state")[0].remove(next(c for c in declared if c[1] == "fcsr"))
        add("both censuses shortened", "CSR-SELECTION", shortened)
        add("time has another owner", "CSR-VIEWS", lambda d: set_field(
            named(d["state"], "csr", "time"), "view_of", "minstret"))
        add("duplicate CSR address", "CSR-ADDRESSES", lambda d: set_field(
            named(d["state"], "csr", "stimecmp"), "address", 0x300))
    elif key == "NO-PMP":
        add("PMP register selected", "PMP-SELECTION", lambda d: set_field(
            named(d["state"], "csr", "mscratch"), "id", "pmpcfg0"))
        add("PMP inclusion declared", "PMP-DECLARATION", lambda d: set_field(
            named(d["profile"], "decision", "D-NO-PMP"), "statement", "PMP is included."))
    elif key == "NO-H":
        add("H extension selected", "H-SELECTION", lambda d: d["profile"].append([S.Symbol("extensions"), "H"]))
        add("hypervisor CSR", "H-STATE", lambda d: set_field(
            named(d["state"], "csr", "mscratch"), "id", "hstatus"))
        add("H inclusion declared", "H-DECLARATION", lambda d: set_field(
            named(d["profile"], "decision", "D-NO-H"), "statement",
            "The hypervisor extension is included."))
    elif key == "SCOPE-CENSUS":
        add("wrong total", "SCOPE-COUNT", lambda d: set_field(
            S.children(d["profile"], "scope")[0], "count_total", 1))
        def wrong_name(d):
            scope = S.children(d["profile"], "scope")[0]
            S.children(scope, "c_compressed")[0][1] = "C.UNKNOWN"
        add("same count, wrong name", "SCOPE-SET", wrong_name)
    return fixtures


def run_structured(check: str, key: str) -> str:
    data = {"profile": document(UNIT / "profile.sexp", "profile"),
            "state": document(UNIT / "state.sexp", "state"),
            "sources": document(UNIT / "sources.sexp", "sources"),
            "encoding_names": E._encoding_names(UNIT)}
    reason = structured(key, data)
    if reason is not None:
        raise ScopeRefused(f"{check}: canonical declaration violates {reason}")
    if check.endswith("-POS"):
        return f"GC-CONTRACT-SCOPE: {check} holds (canonical structured declarations)"
    fixtures = structured_fixtures(key, data)
    if not fixtures:
        raise ScopeRefused(f"CONTROL-MISSING: {check}")
    for label, fixture, expected in fixtures:
        actual = structured(key, fixture)
        if actual != expected:
            raise ScopeRefused(f"CONTROL-MISSED: {label}: expected {expected}, got {actual}")
    return f"GC-CONTRACT-SCOPE: {check} holds ({len(fixtures)} violating copies refused)"


def run(check: str, mutation: str | None = None) -> str:
    key, _, polarity = check.removeprefix("CHK-").rpartition("-")
    if check.startswith("CHK-") and key in STRUCTURED and polarity in {"POS", "NEG"}:
        if mutation is not None:
            raise ScopeRefused("MUTATION-SCOPE: disabled-predicate controls target composition only")
        return run_structured(check, key)
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
    except (ScopeRefused, S.SexpError, E.ExtractionRefused) as error:
        print(f"GC-CONTRACT-SCOPE: REFUSED - {error}")
        return 2 if isinstance(error, ScopeRefused) and str(error).startswith("UNKNOWN-CHECK:") else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
