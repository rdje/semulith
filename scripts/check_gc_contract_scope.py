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
import re
import subprocess
import sys
from pathlib import Path

import sexp as S
import check_extraction as E
import records_sexp as R

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
STRUCTURED = {"EXT-CLOSURE", "PRIV-REVISION", "CSR-SET", "NO-PMP", "NO-H", "SCOPE-CENSUS",
              "ABI", "SBI", "RVWMO", "PRIV-INSNS", "GC-FP-QUALIFIED-V2", "GC-DEFINITION-V2"}
# Rehashed from the public pinned v20260120 pages at P4-SYSTEM.13 b3. The check
# binds the declaration to these identities; artifact-byte verification remains
# CITATIONS' responsibility and is not inferred from the version string.
PRIVILEGE_PINS = {
    "RVP-MACHINE": "b63fe33517fef2dabe53cdbc45b05d656bf808eebf83f0af5a4ab74549617fea",
    "RVP-SUPERVISOR": "d5186efc3ead1c1f693ac2b16aeccdcab95d990264f49b559252d2dc413a651a",
}
# Rehashed public artifacts at P4-SYSTEM.13 b5. Ordinary checks bind declared
# identities, without requiring the cache or claiming a new byte verification.
ABI_SBI_PINS = {
    "RVI-PSABI": ("riscv/riscv-elf-psabi-1.0.pdf",
                  "a8d06bdcaa82a6a4567a1904dc27ef1ca1043ebaa1f523558c927a9d72bc23d9"),
    "RVI-SBI": ("riscv/riscv-sbi-2.0.pdf",
                "63084f54f382715efb340f46695d0e5cebd98965292d034d1b184b1abd3a682b"),
}
PRIVILEGED_FORMS = {"MRET", "SRET", "WFI", "SFENCE.VMA"}
BACKEND_ARTIFACT = "0.2.3+llvm-462a31f5a5ab"
BACKEND_CHECKSUM = "486c2179b4796f65bfe2ee33679acf0927ac83ecf583ad6c91c3b4570911b9ad"
QUALIFICATION_RECORDS = {"docs/decisions/decision_fp-backend-qualification.md",
                         "docs/decisions/reference_fp-model-layer-acceptance.md"}


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
    elif key == "ABI":
        declaration = str(S.field(named(profile, "decision", "D-ABI"), "statement"))
        if (not declaration.startswith("The toolchain ABI is LP64D —")
                or any(part not in declaration for part in
                       ("ELFCLASS64", "EF_RISCV_FLOAT_ABI_DOUBLE", "ABI_FLEN=64",
                        "clang/lld 21.1.8", "rv64gc target"))):
            return "ABI-CHOICE"
        fp = S.children(state, "fp_registers")
        if (S.field(profile, "xlen") != 64 or not {"D", "F"} <= extensions
                or len(fp) != 1 or S.field(fp[0], "count") != 32
                or S.field(fp[0], "width_bits") != 64 or S.field(fp[0], "ids") != "f0..f31"):
            return "ABI-STATE"
        source = named(sources, "source", "RVI-PSABI")
        if (S.field(source, "file"), S.field(source, "sha256")) != ABI_SBI_PINS["RVI-PSABI"]:
            return "ABI-SOURCE"
    elif key == "SBI":
        declaration = str(S.field(named(profile, "decision", "D-SBI"), "statement"))
        if (not declaration.startswith("The firmware contract for the Linux boot route is SBI 2.0:")
                or any(part not in declaration for part in
                       ("M-mode firmware", "S-mode kernel", "real firmware",
                        "a host-modelled SBI is a different contract, never silently substituted"))):
            return "SBI-CHOICE"
        if not {"M", "S"} <= set(values(profile, "privilege_modes")):
            return "SBI-MODES"
        source = named(sources, "source", "RVI-SBI")
        if (S.field(source, "file"), S.field(source, "sha256")) != ABI_SBI_PINS["RVI-SBI"]:
            return "SBI-SOURCE"
    elif key == "RVWMO":
        declaration = str(S.field(named(profile, "decision", "D-RVWMO"), "statement"))
        if (not declaration.startswith("The memory consistency model is RVWMO:")
                or "multicore exposure of the weak model is MC-MULTICORE's" not in declaration):
            return "RVWMO-CHOICE"
        if S.field(profile, "harts") != 1 or "A" not in extensions:
            return "RVWMO-SELECTION"
        if S.field(named(sources, "source", "RVI-RVWMO"), "chapter_version") != "2.0":
            return "RVWMO-REVISION"
    elif key == "PRIV-INSNS":
        scope = S.children(profile, "scope")[0]
        selected = values(scope, "system_privileged")
        if len(selected) != 4 or set(selected) != PRIVILEGED_FORMS:
            return "PRIVILEGED-SCOPE"
        if not {name.lower() for name in PRIVILEGED_FORMS} <= data["encoding_names"]:
            return "PRIVILEGED-ENCODING"
        declaration = str(S.field(named(profile, "decision", "D-PRIV-INSNS"), "statement"))
        if not declaration.startswith("The privileged instructions in scope are mret, sret, wfi and sfence.vma"):
            return "PRIVILEGED-CHOICE"
    elif key == "GC-FP-QUALIFIED-V2":
        params = data["record"]["parameters"]
        if (params.get("backend") != "rustc_apfloat"
                or params.get("backend_requirement") != "=0.2.3"
                or params.get("backend_artifact") != BACKEND_ARTIFACT
                or data["backend_requirement"] != ["=0.2.3"]
                or data["backend_lock"] != [(BACKEND_ARTIFACT, BACKEND_CHECKSUM)]):
            return "QUALIFIED-BACKEND-PIN"
        if (params.get("model_layer") != "crates/semulith-core/src/fp.rs"
                or not data["model_present"] or not {"F", "D"} <= extensions):
            return "QUALIFIED-MODEL-SELECTION"
        if ({params.get("qualification_record"), params.get("closing_record")} != QUALIFICATION_RECORDS
                or data["active_qualification_records"] != QUALIFICATION_RECORDS):
            return "QUALIFICATION-RECORDS"
        if params.get("sail_spike_numeric_independent") is not False:
            return "QUALIFICATION-INDEPENDENCE"
    elif key == "GC-DEFINITION-V2":
        vehicle = S.children(profile, "vehicle")
        if len(vehicle) != 1 or S.field(vehicle[0], "route") != "generated-definition":
            return "CURRENT-DEFINITION-ROUTE"
        part = S.children(data["encoding"], "compose")[0]
        if S.field(part, "status") != "complete" or S.children(part, "slot"):
            return "CURRENT-DEFINITION-COMPOSITION"
        if structured("SCOPE-CENSUS", data) is not None:
            return "CURRENT-DEFINITION-SCOPE"
        if set(data["generation_checks"]) != {"state", "definition", "guests"} or not all(
                data["generation_checks"].values()):
            return "CURRENT-DEFINITION-MIRRORS"
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

    def replace_choice(data, ident, old, new):
        decision = named(data["profile"], "decision", ident)
        statement = str(S.field(decision, "statement"))
        if old not in statement:
            raise ScopeRefused(f"CONTROL: {ident} lacks {old}")
        set_field(decision, "statement", statement.replace(old, new))

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
    elif key == "ABI":
        add("soft-float ABI", "ABI-CHOICE", lambda d: replace_choice(d, "D-ABI", "LP64D", "LP64"))
        add("wrong toolchain pin", "ABI-CHOICE",
            lambda d: replace_choice(d, "D-ABI", "21.1.8", "99.0.0"))
        add("no D", "ABI-STATE", lambda d: remove_extension(d, "D"))
        add("narrow FP file", "ABI-STATE", lambda d: set_field(
            S.children(d["state"], "fp_registers")[0], "width_bits", 32))
        add("different psABI source", "ABI-SOURCE", lambda d: set_field(
            named(d["sources"], "source", "RVI-PSABI"), "sha256", "0" * 64))
    elif key == "SBI":
        add("older SBI", "SBI-CHOICE", lambda d: replace_choice(d, "D-SBI", "SBI 2.0", "SBI 1.0"))
        add("host substitution", "SBI-CHOICE", lambda d: replace_choice(
            d, "D-SBI", "a host-modelled SBI is a different contract, never silently substituted",
            "a host-modelled SBI is substituted"))
        def no_machine(d):
            p = d["profile"]
            p.remove(next(c for c in S.children(p, "privilege_modes") if c[1] == "M"))
        add("no firmware mode", "SBI-MODES", no_machine)
        add("different SBI source", "SBI-SOURCE", lambda d: set_field(
            named(d["sources"], "source", "RVI-SBI"), "sha256", "0" * 64))
    elif key == "RVWMO":
        add("stronger model substituted", "RVWMO-CHOICE",
            lambda d: replace_choice(d, "D-RVWMO", "is RVWMO:", "is sequential consistency:"))
        add("multicore scope", "RVWMO-SELECTION", lambda d: set_field(d["profile"], "harts", 2))
        add("no atomics", "RVWMO-SELECTION", lambda d: remove_extension(d, "A"))
        add("wrong memory revision", "RVWMO-REVISION", lambda d: set_field(
            named(d["sources"], "source", "RVI-RVWMO"), "chapter_version", "1.0"))
    elif key == "PRIV-INSNS":
        def wrong_privileged(d):
            scope = S.children(d["profile"], "scope")[0]
            S.children(scope, "system_privileged")[0][1] = "HRET"
        add("same count, wrong privileged form", "PRIVILEGED-SCOPE", wrong_privileged)
        add("unresolved privileged form", "PRIVILEGED-ENCODING",
            lambda d: d["encoding_names"].remove("sfence.vma"))
        add("different privileged choice", "PRIVILEGED-CHOICE",
            lambda d: replace_choice(d, "D-PRIV-INSNS", "mret, sret, wfi and sfence.vma", "mret only"))
    elif key == "GC-FP-QUALIFIED-V2":
        add("different manifest pin", "QUALIFIED-BACKEND-PIN",
            lambda d: d.update(backend_requirement=["=0.2.4"]))
        add("different artifact checksum", "QUALIFIED-BACKEND-PIN",
            lambda d: d.update(backend_lock=[(BACKEND_ARTIFACT, "0" * 64)]))
        add("no model layer", "QUALIFIED-MODEL-SELECTION", lambda d: d.update(model_present=False))
        add("qualification withdrawn", "QUALIFICATION-RECORDS",
            lambda d: d["active_qualification_records"].remove(next(iter(QUALIFICATION_RECORDS))))
        add("shared lineage called independent", "QUALIFICATION-INDEPENDENCE",
            lambda d: d["record"]["parameters"].update(sail_spike_numeric_independent=True))
    elif key == "GC-DEFINITION-V2":
        add("old resolution vehicle", "CURRENT-DEFINITION-ROUTE", lambda d: set_field(
            S.children(d["profile"], "vehicle")[0], "route", S.Symbol("profile-resolution")))
        add("partial composition", "CURRENT-DEFINITION-COMPOSITION", lambda d: set_field(
            S.children(d["encoding"], "compose")[0], "status", S.Symbol("partial")))
        add("scope disagrees", "CURRENT-DEFINITION-SCOPE",
            lambda d: d["encoding_names"].remove("sfence.vma"))
        add("stale generated mirror", "CURRENT-DEFINITION-MIRRORS",
            lambda d: d["generation_checks"].update(definition=False))
    return fixtures


def current_guarantee_data(key: str, data: dict) -> None:
    """Read selected pins or ask the existing generators; no second generator."""
    if key == "GC-FP-QUALIFIED-V2":
        records = [r for r in R.load(UNIT / "contract-obligations.sexp") if r["id"] == "OB-" + key]
        if len(records) != 1:
            raise ScopeRefused(f"RECORD: expected exactly one OB-{key}")
        data["record"] = records[0]
        # Judge the literal forms Cargo currently owns. Cargo itself validates the
        # manifest/lock grammar; an unsupported pin spelling refuses this scope
        # predicate instead of silently guessing another TOML interpretation.
        manifest = (ROOT / "crates/semulith-core/Cargo.toml").read_text()
        data["backend_requirement"] = re.findall(r'^rustc_apfloat\s*=\s*"([^"]+)"\s*$', manifest, re.M)
        locks = []
        for block in (ROOT / "Cargo.lock").read_text().split("[[package]]"):
            if re.search(r'^name = "rustc_apfloat"$', block, re.M):
                version = re.findall(r'^version = "([^"]+)"$', block, re.M)
                checksum = re.findall(r'^checksum = "([^"]+)"$', block, re.M)
                locks.append((version[0] if len(version) == 1 else None,
                              checksum[0] if len(checksum) == 1 else None))
        data["backend_lock"] = locks
        data["model_present"] = (ROOT / "crates/semulith-core/src/fp.rs").is_file()
        data["active_qualification_records"] = {
            path for path in QUALIFICATION_RECORDS if (ROOT / path).is_file()
            and '- **Status:** `active`' in (ROOT / path).read_text()}
    elif key == "GC-DEFINITION-V2":
        data["encoding"] = document(UNIT / "encoding.sexp", "encoding")
        prefix = "profiles/rv64gc-lab-v0"
        commands = {
            "state": ["scripts/gen_state.py", "--state", f"{prefix}/state.sexp",
                      "--out", "crates/semulith-core/src/state_rv64gc.rs"],
            "definition": ["scripts/gen_definition.py", "--encoding", f"{prefix}/encoding.sexp",
                           "--state", f"{prefix}/state.sexp", "--out",
                           "crates/semulith-core/src/definition_rv64gc.rs"],
            "guests": ["scripts/gen_guests.py", "--encoding", f"{prefix}/encoding.sexp",
                       "--guests-dir", f"{prefix}/guests", "--image-format", "bytes",
                       "--out", "crates/semulith-verify/src/guests_rv64gc.rs"],
        }
        data["generation_checks"] = {}
        for name, command in commands.items():
            result = subprocess.run([sys.executable, *command, "--check"], cwd=ROOT,
                                    capture_output=True, text=True, check=False)
            data["generation_checks"][name] = result.returncode == 0
            if result.returncode:
                print(f"GC-CONTRACT-SCOPE generator {name}: {result.stdout}{result.stderr}")


def run_structured(check: str, key: str) -> str:
    data = {"profile": document(UNIT / "profile.sexp", "profile"),
            "state": document(UNIT / "state.sexp", "state"),
            "sources": document(UNIT / "sources.sexp", "sources"),
            "encoding_names": E._encoding_names(UNIT)}
    current_guarantee_data(key, data)
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
