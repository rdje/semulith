#!/usr/bin/env python3
"""gen_state.py — generate `semulith-core`'s architectural-state module from the profile's
state descriptor (P1-LAB.3; OWN-01/OWN-03).

The state accessors and inspection metadata DERIVE from `state.sexp` — the descriptor is
the authority (docs/ARCHITECTURE.md §2), the generated module is its derived mirror, and
the pair is governed by the STATE-GEN doctrine (`scripts/check_state_gen.sh`): drift is
`regenerate and diff`, never a hand edit. Emission is byte-deterministic — the same
descriptor bytes always yield the same module bytes, and the input's sha256 rides in the
module header so a reviewer can name the exact bytes the code derives from.

The generator REFUSES (exit 2, naming the construct) on any descriptor shape it does not
know how to emit: a profile id outside its two scoped units, a register family / memory
space / hardware stack (the `P3-BREADTH.5` constructs), a missing xlen, a non-64 width, a
special register it has no mapping for, a missing reset, an alias outside x1..x31, a CSR
shape it cannot legalize (P4-SYSTEM.2 slice c1). A descriptor that grew is generator work,
never silently guessed — that is how "generated" stays a claim instead of a hope.

TWO PROFILES, ONE GENERATOR (P4-SYSTEM.2 slice c1): rv64i-lab-v0's module is the committed
`crates/semulith-core/src/state.rs` (byte-identical re-derivation, gated by STATE-GEN).
rv64gc-lab-v0's descriptor landed tracked at the route flip (P4-SYSTEM.2 slice h) and its
module is the committed `crates/semulith-core/src/state_rv64gc.rs`, gated by the same
STATE-GEN census — both modules regenerate from their tracked descriptors.

Usage:
  python3 scripts/gen_state.py                 # regenerate the committed module
  python3 scripts/gen_state.py --check         # exit 0 iff the committed module is current
  python3 scripts/gen_state.py --state S --arith A --out O   # explicit paths (self-tests)
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import dossier_sexp as D                                # noqa: E402

PROFILE = "rv64i-lab-v0"
PROFILES = ("rv64i-lab-v0", "rv64gc-lab-v0")
STATE = ROOT / "profiles" / PROFILE / "state.sexp"
ARITH = ROOT / "crates" / "semulith-core" / "src" / "arith.rs"
OUT = ROOT / "crates" / "semulith-core" / "src" / "state.rs"

# The one executable owner of XLEN is `arith::XLEN` (REQ-D-XLEN, P1-LAB.2). The generator
# binds the descriptor to it at generation time; the STATE-GEN doctrine then refuses the
# day the two could drift apart in the generated mirror.
XLEN_RE = re.compile(r"pub const XLEN: u32 = (\d+);")
SUPPORTED_WIDTH = 64


class Refusal(Exception):
    """The descriptor (or the arith owner) says something this generator cannot emit."""


def snake(role: str) -> str:
    ident = re.sub(r"[^A-Za-z0-9]+", "_", role).strip("_").upper()
    if not ident or not ident[0].isalpha():
        raise Refusal(f"alias role {role!r} yields no legal constant identifier")
    return ident


def rust_str(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def load_checked(state_path: Path, arith_path: Path) -> tuple[dict, int]:
    doc = D.load_state(state_path)
    m = XLEN_RE.search(arith_path.read_text(encoding="utf-8"))
    if not m:
        raise Refusal(f"{arith_path.name}: no `pub const XLEN: u32 = N;` — the generator "
                      "cannot bind the descriptor to the one XLEN owner")
    arith_xlen = int(m.group(1))
    xlen = doc.get("xlen")
    if xlen is None:
        raise Refusal("no xlen — this generator binds the descriptor to arith::XLEN, the "
                      "one executable owner (REQ-D-XLEN); a descriptor without xlen is "
                      "generator work (P3-BREADTH.5), never a guessed default")
    if xlen != arith_xlen:
        raise Refusal(f"xlen mismatch: state.sexp declares {xlen}, arith::XLEN is "
                      f"{arith_xlen} — one fact, one owner; resolve the descriptor, do not "
                      "pick a side in the generator")
    return doc, arith_xlen


def validate(doc: dict, arith_xlen: int) -> tuple[list[dict], list[dict], dict]:
    if doc["profile_id"] not in PROFILES:
        raise Refusal(f"profile_id {doc['profile_id']!r} — this generator is scoped to "
                      f"{PROFILES!r}; another profile is generator work, not a config knob")
    if doc["profile_id"] == "rv64gc-lab-v0":
        return validate_gc(doc, arith_xlen)
    # P3-BREADTH.5 slice 1: the schema declares these constructs (the exercised target is
    # dsp56300-lab-v0; the census record names the cases) — emitting them is generator
    # work, so a descriptor carrying one is refused BY NAME, never silently dropped.
    if doc.get("register_family"):
        raise Refusal("register_family declared — emitting register families with masked "
                      "widths and part readouts is generator work (P3-BREADTH.5; case "
                      "dsp56300-lab-v0, F1), not silently assumed")
    if doc.get("memory_spaces"):
        raise Refusal("memory_spaces declared — emitting distinct memory spaces is "
                      "generator work (P3-BREADTH.5; case dsp56300-lab-v0, F3), not "
                      "silently assumed")
    if "hardware_stack" in doc:
        raise Refusal("hardware_stack declared — emitting the hardware stack is generator "
                      "work (P3-BREADTH.5; case dsp56300-lab-v0, the census's candidates "
                      "4/6), not silently assumed")
    if doc.get("csr") or "privilege_mode" in doc:
        raise Refusal("csr / privilege_mode declared under rv64i-lab-v0 — the privileged "
                      "constructs belong to rv64gc-lab-v0's descriptor (P4-SYSTEM.2 slice "
                      "c1); emitting them for this profile is generator work, never guessed")
    ir = doc.get("integer_registers")
    if ir is None:
        raise Refusal("no integer_registers — this generator emits the x0-anchored "
                      "integer file; a descriptor with only register families is generator "
                      "work (P3-BREADTH.5), not silently assumed")
    count = ir["count"]
    if ir["width_bits"] != SUPPORTED_WIDTH:
        raise Refusal(f"integer_registers width_bits {ir['width_bits']} — masked fixed-width "
                      "storage for nonstandard widths is generator work "
                      "(docs/ARCHITECTURE.md §4), not silently assumed")
    if ir["ids"] != f"x0..x{count - 1}":
        raise Refusal(f"integer_registers ids {ir['ids']!r} do not enumerate x0..x{count - 1}")
    if not ir["x0"]["hardwired_zero"]:
        raise Refusal("x0 is not declared hardwired_zero — the emitted read/write discipline "
                      "assumes the descriptor's x0 rule; emit something else instead")
    if "reset" not in ir:
        raise Refusal("integer_registers has no reset — REQ-D-ENTRY-STATE is unowned")
    regs = doc["special_registers"]
    for r in regs:
        if r["id"] != "pc":
            raise Refusal(f"special register {r['id']!r} has no emission mapping — extend "
                          "the generator behind the schema layer, never guess")
        if r["width_bits"] != SUPPORTED_WIDTH:
            raise Refusal(f"special register {r['id']!r} width_bits {r['width_bits']} — "
                          "same refusal as the integer file")
    if not regs:
        raise Refusal("no special registers declared — pc is required (RVI-RV32I §1.1.1)")
    census = doc.get("hidden_state_census")
    if census is None:
        raise Refusal("no hidden_state_census (SEM-08) — the universal claim that no hidden "
                      "state exists must be earned by the census, not inferred from silence")
    named = []
    seen: set[str] = set()
    for n in ir["named_by_the_isa_chapter"]:
        m = re.fullmatch(r"x(\d+)", n["reg"])
        if not m or not 1 <= int(m.group(1)) < count:
            raise Refusal(f"named register {n['reg']!r} is not x1..x{count - 1} — aliasing "
                          "outside the integer file has no emission mapping")
        ident = snake(n["role"])
        if ident in seen:
            raise Refusal(f"alias role {n['role']!r} collides after naming — rename in the "
                          "descriptor, not by hand here")
        seen.add(ident)
        named.append({"index": int(m.group(1)), "ident": ident, **n})
    return named, regs, census


def emit(doc: dict, named: list[dict], regs: list[dict], census: dict,
         state_sha: str) -> str:
    ir = doc["integer_registers"]
    count = ir["count"]
    width = ir["width_bits"]
    x0_source = ir["x0"]["source"]
    pc = regs[0]

    w = []
    a = w.append
    a("//! GENERATED — do not edit (OWN-03). Regenerate with `python3 scripts/gen_state.py`;")
    a("//! drift between this module and the descriptor it derives from is refused by the")
    a("//! STATE-GEN doctrine (`scripts/check_state_gen.sh`). The state accessors and")
    a("//! inspection metadata derive from the state/alias descriptors (docs/ARCHITECTURE.md")
    a("//! §2), never maintained by hand.")
    a(f"//! Source: `profiles/{PROFILE}/state.sexp` (sha256 `{state_sha}`).")
    a("//!")
    a(f"//! Architectural state of `{PROFILE}`: {count} × {width}-bit integer registers")
    a("//! (x0 hardwired to zero) and the 64-bit program counter. — REQ-D-XLEN,")
    a("//! REQ-D-ENTRY-STATE (RVI-RV32I §1.1.1; RVI-RV64I §3.1.1)")
    a("")
    a(f"/// Number of integer registers in the architectural register file. — REQ-D-XLEN")
    a(f"pub const INTEGER_COUNT: usize = {count};")
    a("")
    for n in sorted(named, key=lambda d: d["index"]):
        a(f"/// x{n['index']} — alias view, {rust_str(n['role'])} (software convention named")
        a(f"/// by the ISA chapter; authority {n['authority']} — {n['source']}).")
        a("/// Aliases are views over ONE storage: a value written through one name is visible")
        a("/// through every other (catalog C02).")
        a(f"pub const {n['ident']}: u8 = {n['index']};")
        a("")
    a("/// The architectural register file and program counter: one fixed-width storage,")
    a("/// every alias a view over it. 33 × 8 bytes inline, no heap — common scalar execution")
    a("/// takes no per-access allocation (RUST-03).")
    a("pub struct ArchitecturalState {")
    a("    regs: [u64; INTEGER_COUNT],")
    a("    pc: u64,")
    a("}")
    a("")
    a("impl ArchitecturalState {")
    a("    /// Fresh state at the laboratory reset for `entry` (REQ-D-ENTRY-STATE).")
    a("    #[must_use]")
    a("    pub fn zeroed_at(entry: u64) -> Self {")
    a("        Self {")
    a("            regs: [0; INTEGER_COUNT],")
    a("            pc: entry,")
    a("        }")
    a("    }")
    a("")
    a("    /// The laboratory reset (REQ-D-ENTRY-STATE, OB-ENV-RESET): x1..x31 = 0 — a harness")
    a("    /// declaration the base ISA leaves to the execution environment, not an")
    a("    /// architectural guarantee — and pc = the loaded image's declared entry address,")
    a("    /// supplied by the environment. x0 needs no action: it is hardwired to zero.")
    a("    pub fn reset(&mut self, entry: u64) {")
    a("        self.regs = [0; INTEGER_COUNT];")
    a("        self.pc = entry;")
    a("    }")
    a("")
    a("    /// Architectural read of `x(index)`. x0 reads as 0, always — hardwired zero,")
    a("    /// \"a write to it is discarded; a read of it yields 0\" (RVI-RV32I §1.1.1).")
    a("    /// Contract: `index < INTEGER_COUNT`; an out-of-range index is a model error")
    a("    /// (SEM-01) and panics rather than silently reading another register.")
    a("    #[must_use]")
    a("    pub fn read_x(&self, index: u8) -> u64 {")
    a("        debug_assert!(")
    a("            index < INTEGER_COUNT as u8,")
    a("            \"read_x: index {index} out of range\"")
    a("        );")
    a("        if index == 0 {")
    a("            0")
    a("        } else {")
    a("            self.regs[index as usize]")
    a("        }")
    a("    }")
    a("")
    a("    /// Architectural write of `x(index)`; a write to x0 is discarded (hardwired zero).")
    a("    /// Same index contract as [`Self::read_x`].")
    a("    pub fn write_x(&mut self, index: u8, value: u64) {")
    a("        debug_assert!(")
    a("            index < INTEGER_COUNT as u8,")
    a("            \"write_x: index {index} out of range\"")
    a("        );")
    a("        if index != 0 {")
    a("            self.regs[index as usize] = value;")
    a("        }")
    a("    }")
    a("")
    a("    /// The program counter: the address of the current instruction (RVI-RV32I §1.1.1).")
    a("    /// Compositions that advance it (pc+4 sequencing, taken targets) are instruction-")
    a("    /// layer rules; they land with the interpreter slice (P1-LAB.8).")
    a("    #[must_use]")
    a("    pub fn pc(&self) -> u64 {")
    a("        self.pc")
    a("    }")
    a("")
    a("    /// Set the program counter (a control transfer's target).")
    a("    pub fn set_pc(&mut self, value: u64) {")
    a("        self.pc = value;")
    a("    }")
    a("}")
    a("")
    a("/// Static inspection metadata for one architectural state element — what observers,")
    a("/// divergence reports and the gate report read. Values, not storage: reading this")
    a("/// table never touches architectural state and never allocates.")
    a("pub struct StateElement {")
    a("    pub name: &'static str,")
    a("    pub width_bits: u32,")
    a("    pub class: StateClass,")
    a("    /// Software-convention role the ISA chapter itself names; `None` where the")
    a("    /// descriptor records none (ABI names are a calling convention, not")
    a("    /// architecture — see the descriptor's note).")
    a("    pub role: Option<&'static str>,")
    a("    pub source: &'static str,")
    a("}")
    a("")
    a("/// Which kind of state an element is; the class set is descriptor-driven, so it is")
    a("/// generated with the elements rather than hand-extended.")
    a("#[derive(Clone, Copy, Debug, PartialEq, Eq)]")
    a("pub enum StateClass {")
    a("    IntegerRegister,")
    a("    SpecialRegister,")
    a("}")
    a("")
    roles = {n["index"]: n["role"] for n in named}
    a(f"/// The {count} integer registers followed by the special registers, in descriptor")
    a("/// order: one row per state element, the observer's whole view of the file.")
    a(f"pub const ELEMENTS: [StateElement; {count + len(regs)}] = [")
    for i in range(count):
        role = roles.get(i)
        source = x0_source if i == 0 else ir["source"]
        a("    StateElement {")
        a(f"        name: {rust_str(f'x{i}')},")
        a(f"        width_bits: {width},")
        a("        class: StateClass::IntegerRegister,")
        a(f"        role: {f'Some({rust_str(role)})' if role else 'None'},")
        a(f"        source: {rust_str(source)},")
        a("    },")
    for r in regs:
        a("    StateElement {")
        a(f"        name: {rust_str(r['id'])},")
        a(f"        width_bits: {r['width_bits']},")
        a("        class: StateClass::SpecialRegister,")
        a("        role: None,")
        a(f"        source: {rust_str(r['source'])},")
        a("    },")
    a("];")
    a("")
    a("/// SEM-08: required state includes hidden or pending information that can influence")
    a("/// future supported observations. This profile's census answers NO — per candidate,")
    a("/// with the reason — and the answer is carried as data so the interpreter, the gate")
    a("/// report and the reviewer read the same sentence. Every extension added later")
    a("/// reopens the census (the descriptor's own consequence).")
    a("pub struct HiddenStateCandidate {")
    a("    pub candidate: &'static str,")
    a("    pub present: bool,")
    a("    pub why: &'static str,")
    a("}")
    a("")
    a("pub struct HiddenStateCensus {")
    a("    pub question: &'static str,")
    a("    pub answer: &'static str,")
    a("    pub candidates: &'static [HiddenStateCandidate],")
    a("    pub consequence: &'static str,")
    a("}")
    a("")
    a("pub const HIDDEN_STATE_CENSUS: HiddenStateCensus = HiddenStateCensus {")
    a(f"    question: {rust_str(census['question'])},")
    a(f"    answer: {rust_str(census['answer'])},")
    a("    candidates: &[")
    for c in census["candidates_checked"]:
        a("        HiddenStateCandidate {")
        a(f"            candidate: {rust_str(c['candidate'])},")
        a(f"            present: {'true' if c['present'] else 'false'},")
        a(f"            why: {rust_str(c['why'])},")
        a("        },")
    a("    ],")
    a(f"    consequence: {rust_str(census['consequence'])},")
    a("};")
    a("")
    a("#[cfg(test)]")
    a("mod tests;")
    a("")
    return "\n".join(w)


# ---------------------------------------------------------------------------------------
# rv64gc-lab-v0 (P4-SYSTEM.2 slice c1): the privileged-state branch — same integer file,
# plus the current privilege mode and the 33 CSRs with their field tables.
# ---------------------------------------------------------------------------------------
MODE_CODES = {"u": 0, "s": 1, "m": 3}


def _int(value: str, where: str) -> int:
    try:
        return int(str(value), 0)
    except ValueError:
        raise Refusal(f"{where}: reset value {value!r} is not an integer the generator can "
                      f"emit — record the number and carry the prose in the statement")


def _composed_reset(csr: dict) -> int:
    """A CSR's reset, composed from its per-field resets — and checked against the
    csr-level declared value when that value is numeric. The two statements of one fact
    must agree; a disagreement is a descriptor defect, named, never adjudicated here."""
    value = 0
    for f in csr.get("fields", []):
        fv = _int(f["reset"], f"{csr['id']}.{f['id']}")
        width = f["bit_hi"] - f["bit_lo"] + 1
        if fv >= (1 << width):
            raise Refusal(f"{csr['id']}.{f['id']}: reset {fv:#x} does not fit "
                          f"[{f['bit_hi']}:{f['bit_lo']}]")
        value |= fv << f["bit_lo"]
    raw = csr["reset"]["value"]
    try:
        declared = int(str(raw), 0)
    except ValueError:
        return value                       # prose reset (a view's) — nothing to cross-check
    if csr.get("fields") and declared != value:
        raise Refusal(f"{csr['id']}: the per-field resets compose to {value:#x} but the "
                      f"csr-level reset declares {declared:#x} — one reset, one value")
    return declared


def validate_gc(doc: dict, arith_xlen: int) -> tuple[list[dict], list[dict], dict]:
    # The same construct refusals the rv64i path carries (P4-SYSTEM.3 slice a: the hole
    # the .3 brief's pre-condition 6 names — these constructs were silently IGNORED here,
    # so a descriptor carrying one would have lost data without a word):
    if doc.get("register_family"):
        raise Refusal("register_family declared — emitting register families with masked "
                      "widths and part readouts is generator work (P3-BREADTH.5; case "
                      "dsp56300-lab-v0, F1), not silently assumed")
    if doc.get("memory_spaces"):
        raise Refusal("memory_spaces declared — emitting distinct memory spaces is "
                      "generator work (P3-BREADTH.5; case dsp56300-lab-v0, F3), not "
                      "silently assumed")
    if "hardware_stack" in doc:
        raise Refusal("hardware_stack declared — emitting the hardware stack is generator "
                      "work (P3-BREADTH.5; case dsp56300-lab-v0, the census's candidates "
                      "4/6), not silently assumed")
    ir = doc.get("integer_registers")
    if ir is None or ir["width_bits"] != SUPPORTED_WIDTH or ir["ids"] != "x0..x31":
        raise Refusal("rv64gc-lab-v0: the integer file must be the RV64I x0..x31 file at "
                      "64 bits — anything else is generator work")
    if not ir["x0"]["hardwired_zero"]:
        raise Refusal("rv64gc-lab-v0: x0 is not declared hardwired_zero")
    regs = doc["special_registers"]
    if [r["id"] for r in regs] != ["pc"] or regs[0]["width_bits"] != SUPPORTED_WIDTH:
        raise Refusal("rv64gc-lab-v0: special registers must be exactly pc at 64 bits")
    pm = doc.get("privilege_mode")
    if pm is None:
        raise Refusal("rv64gc-lab-v0: no privilege_mode element — the current mode is hart "
                      "state the mode-matrix corpus observes through; it is not optional")
    if not pm["modes"] or set(pm["modes"]) - set(MODE_CODES):
        raise Refusal(f"rv64gc-lab-v0: privilege modes {pm['modes']!r} — the generator "
                      f"emits codes for {sorted(MODE_CODES)} only")
    if pm["reset"]["value"] not in pm["modes"]:
        raise Refusal(f"rv64gc-lab-v0: mode reset {pm['reset']['value']!r} is not one of "
                      f"the declared modes {pm['modes']!r}")
    csrs = doc.get("csr") or []
    if not csrs:
        raise Refusal("rv64gc-lab-v0: no csr elements — a privileged profile without its "
                      "CSR state is not extractable")
    ids = [c["id"] for c in csrs]
    if len(ids) != len(set(ids)):
        raise Refusal("rv64gc-lab-v0: duplicate csr id in the descriptor")
    addrs = [c["address"] for c in csrs]
    if len(addrs) != len(set(addrs)):
        raise Refusal("rv64gc-lab-v0: duplicate csr address in the descriptor")
    if any(not 0 <= a <= 0xFFF for a in addrs):
        raise Refusal("rv64gc-lab-v0: a csr address lies outside the 12-bit space")
    for c in csrs:
        if c["width_bits"] != SUPPORTED_WIDTH:
            raise Refusal(f"csr {c['id']!r} width_bits {c['width_bits']} — non-64 storage "
                          f"is generator work, as for the integer file")
        for v in c.get("view_of", "").split(","):
            v = v.strip()
            if v and v not in ids:
                raise Refusal(f"csr {c['id']!r} is a view of {v!r}, which the descriptor "
                              f"does not declare — a view of nothing has no storage to read")
        if "reset" not in c:
            raise Refusal(f"csr {c['id']!r}: carries no (reset …) — an engine cannot "
                          f"extract where this element starts")
        spans = sorted((f["bit_lo"], f["bit_hi"]) for f in c.get("fields", []))
        prev = -1
        for lo, hi in spans:
            if not 0 <= lo <= hi < c["width_bits"]:
                raise Refusal(f"csr {c['id']!r}: field range [{hi}:{lo}] outside the register")
            if lo <= prev:
                raise Refusal(f"csr {c['id']!r}: fields overlap at bit {lo}")
            prev = hi
        if c.get("fields") and sum(hi - lo + 1 for lo, hi in spans) != c["width_bits"]:
            raise Refusal(f"csr {c['id']!r}: the field table leaves bits unaccounted — a "
                          f"legalization table with a hole guesses at the hole")
        for f in c.get("fields", []):
            lg = f.get("legalize")
            if f["discipline"] in ("warl", "wlrl") and lg is None:
                raise Refusal(f"csr {c['id']!r}.{f['id']!r}: {f['discipline']} without a "
                              f"(legalize …) — WARL/WLRL name what they do NOT define; the "
                              f"legal rule is the field's to state")
            if f["discipline"] == "wpri" and lg is not None:
                raise Refusal(f"csr {c['id']!r}.{f['id']!r}: a WPRI field carries no "
                              f"legalize — the discipline itself is the whole rule")
            if lg and lg["kind"] == "read-only" and _int(f["reset"], c["id"]) != lg["value"]:
                raise Refusal(f"csr {c['id']!r}.{f['id']!r}: read-only {lg['value']} but "
                              f"reset {f['reset']} — one constant, stated once")
        c["_reset"] = _composed_reset(c)
    census = doc.get("hidden_state_census")
    if census is None:
        raise Refusal("rv64gc-lab-v0: no hidden_state_census (SEM-08) — the re-earned "
                      "census for the privileged state is the point of the document")
    # The carried hart state the census must ACCOUNT FOR before the generator will emit
    # its storage — a descriptor silent about one is an incomplete census, refused by
    # name (P4-SYSTEM.3 slice d's TLB gate, generalised at P4-SYSTEM.4 slice c).
    for cand, label, why in REQUIRED_CENSUS_CANDIDATES:
        found = [c for c in census.get("candidates_checked", [])
                 if c.get("candidate") == cand and c.get("present")]
        if not found:
            raise Refusal(f"rv64gc-lab-v0: the hidden-state census does not declare a "
                          f"present {label} candidate — {why}")
    named = []
    for n in ir["named_by_the_isa_chapter"]:
        m = re.fullmatch(r"x(\d+)", n["reg"])
        named.append({"index": int(m.group(1)), "ident": snake(n["role"]), **n})
    return named, regs, census


# The census must ACCOUNT FOR each piece of optional hart state the module carries,
# before the generator will emit its storage — a descriptor silent about one is an
# incomplete census, refused by name. P4-SYSTEM.3 slice (d) introduced the gate for the
# TLB; P4-SYSTEM.4 slice (c) generalised it when the reservation joined the carried
# state: (the census's candidate name, the refusal's short label, the owning slice).
REQUIRED_CENSUS_CANDIDATES = (
    ("address-translation caches (TLBs)", "translation-cache",
     "the TLB is hart state the census must account for before the module can carry it "
     "(P4-SYSTEM.3 slice d)"),
    ("reservation set (LR/SC)", "reservation",
     "the reservation is hart state the census must account for before the module can "
     "carry it (P4-SYSTEM.4 slice c)"),
)


def emit_gc(doc: dict, named: list[dict], regs: list[dict], census: dict,
            state_sha: str, state_rel: str) -> str:
    ir = doc["integer_registers"]
    count = ir["count"]
    pm = doc["privilege_mode"]
    csrs = doc["csr"]
    storage = [c for c in csrs if "view_of" not in c]
    index_of = {c["id"]: i for i, c in enumerate(storage)}

    w = []
    a = w.append
    a("//! GENERATED — do not edit (OWN-03). Regenerate with `python3 scripts/gen_state.py`;")
    a("//! drift between this module and the descriptor it derives from is refused by the")
    a("//! STATE-GEN doctrine (`scripts/check_state_gen.sh`).")
    a(f"//! Source: `{state_rel}` (sha256 `{state_sha}`).")
    a("//!")
    a("//! Architectural state of `rv64gc-lab-v0`: 32 × 64-bit integer registers (x0")
    a("//! hardwired), the program counter, the current privilege mode, and the 33 CSRs of")
    a("//! D-CSR-SET with their per-field WPRI/WARL/WLRL tables as DATA — legalization is")
    a("//! applied by the engine at lowering (P4-SYSTEM.2 slices c2/d), never by hand here.")
    a("")
    a("/// Number of integer registers in the architectural register file. — REQ-D-XLEN")
    a(f"pub const INTEGER_COUNT: usize = {count};")
    a("")
    for n in sorted(named, key=lambda d: d["index"]):
        a(f"/// x{n['index']} — alias view, {rust_str(n['role'])} (software convention).")
        a(f"pub const {n['ident']}: u8 = {n['index']};")
        a("")
    a("/// The current privilege mode (hart state, not a CSR): the engine's vocabulary type")
    a("/// — the codes are the architecture's own (the pinned encoding.h's PRV_U/PRV_S/PRV_M).")
    a("pub use crate::privilege::{CsrMeta, FieldDiscipline, FieldMeta, Legalize, PrivilegeMode};")
    a("")
    a(f"/// Number of CSRs with storage ({len(storage)} of {len(csrs)}; the rest are views —")
    a("/// a view declares no storage: sstatus/sie/sip restrict mstatus/mie/mip, the")
    a("/// counters shadow their machine registers).")
    a(f"pub const CSR_COUNT: usize = {len(storage)};")
    a("")
    for i, c in enumerate(storage):
        a(f"/// Storage index of `{c['id']}` (address {c['address']:#05x}).")
        a(f"pub const CSR_{c['id'].upper()}: usize = {i};")
        a("")
    a("/// The architectural register file, program counter, current mode and CSR storage:")
    a("/// fixed-width inline, no heap (RUST-03).")
    a("pub struct ArchitecturalState {")
    a("    regs: [u64; INTEGER_COUNT],")
    a("    pc: u64,")
    a("    mode: PrivilegeMode,")
    a("    csrs: [u64; CSR_COUNT],")
    # P4-SYSTEM.3 decision 2: the TLB is hart state, emitted because the descriptor's
    # SEM-08 census declares it (the translation-cache candidate, present true —
    # validate_gc refuses a descriptor that does not account for it).
    a("    tlb: crate::translation::Tlb,")
    # P4-SYSTEM.4 decision 2: the LR/SC reservation is hart state, emitted on the same
    # discipline (the census's reservation candidate, the gate at
    # REQUIRED_CENSUS_CANDIDATES).
    a("    reservation: crate::reservation::Reservation,")
    a("}")
    a("")
    a("impl ArchitecturalState {")
    a("    /// Fresh state at the reset for `entry`: the architectural resets of RVP-MACHINE")
    a("    /// §2.1.4, the laboratory's stated values everywhere §2.1.4 says UNSPECIFIED (the")
    a("    /// descriptor's reset rows are the authority).")
    a("    #[must_use]")
    a("    pub fn zeroed_at(entry: u64) -> Self {")
    a("        Self {")
    a("            regs: [0; INTEGER_COUNT],")
    a("            pc: entry,")
    a(f"            mode: PrivilegeMode::{pm['reset']['value'].upper()},")
    # one reset per line: the rustfmt-stable shape (cargo fmt must leave the generated
    # module byte-identical — STATE-GEN's --check compares against regeneration, not
    # against a formatter's second opinion)
    a("            csrs: [")
    for c in storage:
        a(f"                {c['_reset']:#x},")
    a("            ],")
    a("            tlb: crate::translation::Tlb::new(),")
    a("            reservation: crate::reservation::Reservation::new(),")
    a("        }")
    a("    }")
    a("")
    a("    /// The laboratory reset (REQ-D-ENTRY-STATE, OB-ENV-RESET).")
    a("    pub fn reset(&mut self, entry: u64) {")
    a("        *self = Self::zeroed_at(entry);")
    a("    }")
    a("")
    a("    /// Architectural read of `x(index)`. x0 reads as 0, always (RVI-RV32I §1.1.1).")
    a("    #[must_use]")
    a("    pub fn read_x(&self, index: u8) -> u64 {")
    a("        if index == 0 {")
    a("            0")
    a("        } else {")
    a("            self.regs[index as usize]")
    a("        }")
    a("    }")
    a("")
    a("    /// Architectural write of `x(index)`; a write to x0 is discarded.")
    a("    pub fn write_x(&mut self, index: u8, value: u64) {")
    a("        if index != 0 {")
    a("            self.regs[index as usize] = value;")
    a("        }")
    a("    }")
    a("")
    a("    /// The program counter (RVI-RV32I §1.1.1).")
    a("    #[must_use]")
    a("    pub fn pc(&self) -> u64 {")
    a("        self.pc")
    a("    }")
    a("")
    a("    /// Set the program counter (a control transfer's target).")
    a("    pub fn set_pc(&mut self, value: u64) {")
    a("        self.pc = value;")
    a("    }")
    a("")
    a("    /// The current privilege mode (hart state — RVP-INTRO; reset M, §2.1.4).")
    a("    #[must_use]")
    a("    pub fn mode(&self) -> PrivilegeMode {")
    a("        self.mode")
    a("    }")
    a("")
    a("    /// Set the current privilege mode (trap delivery and xret's concern — the")
    a("    /// engine's, slice (d); accessors stay raw here).")
    a("    pub fn set_mode(&mut self, mode: PrivilegeMode) {")
    a("        self.mode = mode;")
    a("    }")
    a("")
    a("    /// Raw read of CSR storage by index. The permission model, view masking and")
    a("    /// WARL/WLRL legalization are the ENGINE's, applied at lowering (slices c2/d) —")
    a("    /// this layer stores and reports, it never adjudicates.")
    a("    #[must_use]")
    a("    pub fn read_csr(&self, index: usize) -> u64 {")
    a("        self.csrs[index]")
    a("    }")
    a("")
    a("    /// Raw write of CSR storage by index; same layering as [`Self::read_csr`].")
    a("    pub fn write_csr(&mut self, index: usize, value: u64) {")
    a("        self.csrs[index] = value;")
    a("    }")
    a("")
    a("    /// The storage index of a csr ADDRESS, or None for an address the profile does")
    a("    /// not implement (an access there is the permission model's illegal instruction,")
    a("    /// decided by the engine).")
    a("    #[must_use]")
    a("    pub fn csr_index(address: u16) -> Option<usize> {")
    a("        match address {")
    for i, c in enumerate(storage):
        a(f"            {c['address']:#05x} => Some(CSR_{c['id'].upper()}),")
    a("            _ => None,")
    a("        }")
    a("    }")
    a("}")
    a("")
    a("/// Every CSR the profile implements, in descriptor order (views included) — the")
    a("/// engine's `CsrMeta` vocabulary (`crate::privilege`), the descriptor's data.")
    a(f"pub const CSR_ELEMENTS: [CsrMeta; {len(csrs)}] = [")
    for c in csrs:
        view = f"Some({rust_str(c['view_of'])})" if "view_of" in c else "None"
        a("    CsrMeta {")
        a(f"        name: {rust_str(c['id'])},")
        a(f"        address: {c['address']:#05x},")
        a(f"        view_of: {view},")
        a("    },")
    a("];")
    a("")

    def legalize(lg) -> str:
        if lg["kind"] == "any":
            return "Legalize::Any"
        if lg["kind"] == "read-only":
            return f"Legalize::ReadOnly({lg['value']})"
        if lg["kind"] == "one-of":
            vals = ", ".join(str(v) for v in lg["values"])
            return f"Legalize::OneOf(&[{vals}])"
        return "Legalize::Computed"

    nfields = sum(len(c.get("fields", [])) for c in csrs)
    a(f"/// The per-field tables of the {len(csrs)} CSRs, in descriptor order — the")
    a("/// legalization rules as DATA (`crate::privilege::FieldMeta`); the engine applies")
    a("/// them at lowering, this table never adjudicates.")
    a(f"pub const CSR_FIELDS: [FieldMeta; {nfields}] = [")
    for c in csrs:
        for f in c.get("fields", []):
            legal = f"Some({legalize(f['legalize'])})" if "legalize" in f else "None"
            a("    FieldMeta {")
            a(f"        csr: {rust_str(c['id'])},")
            a(f"        name: {rust_str(f['id'])},")
            a(f"        bit_hi: {f['bit_hi']},")
            a(f"        bit_lo: {f['bit_lo']},")
            a(f"        discipline: FieldDiscipline::{f['discipline'].capitalize()},")
            a(f"        legalize: {legal},")
            a(f"        reset: {_int(f['reset'], c['id'] + '.' + f['id'])},")
            a("    },")
    a("];")
    a("")
    a("/// The engine's privileged-state surface (`crate::privilege::PrivilegedHart`),")
    a("/// implemented over this module's storage and tables — the trait's rules are the")
    a("/// engine's; the data they read is the descriptor's.")
    a("impl crate::privilege::PrivilegedHart for ArchitecturalState {")
    a("    fn mode(&self) -> PrivilegeMode {")
    a("        self.mode")
    a("    }")
    a("    fn set_mode(&mut self, mode: PrivilegeMode) {")
    a("        self.mode = mode;")
    a("    }")
    a("    fn csr_raw(&self, index: usize) -> u64 {")
    a("        self.csrs[index]")
    a("    }")
    a("    fn csr_write_raw(&mut self, index: usize, value: u64) {")
    a("        self.csrs[index] = value;")
    a("    }")
    a("    fn csr_index(&self, address: u16) -> Option<usize> {")
    a("        Self::csr_index(address)")
    a("    }")
    a("    fn csr_meta(&self) -> &'static [CsrMeta] {")
    a("        &CSR_ELEMENTS")
    a("    }")
    a("    fn csr_fields(&self) -> &'static [FieldMeta] {")
    a("        &CSR_FIELDS")
    a("    }")
    a("    fn tlb(&mut self) -> &mut crate::translation::Tlb {")
    a("        &mut self.tlb")
    a("    }")
    a("    fn reservation(&mut self) -> &mut crate::reservation::Reservation {")
    a("        &mut self.reservation")
    a("    }")
    a("}")
    a("")
    a("/// SEM-08: the hidden-state census, re-earned for the privileged state — carried as")
    a("/// data so the interpreter, the gate report and the reviewer read the same sentence.")
    a("pub struct HiddenStateCandidate {")
    a("    pub candidate: &'static str,")
    a("    pub present: bool,")
    a("    pub why: &'static str,")
    a("}")
    a("")
    a("pub struct HiddenStateCensus {")
    a("    pub question: &'static str,")
    a("    pub answer: &'static str,")
    a("    pub candidates: &'static [HiddenStateCandidate],")
    a("    pub consequence: &'static str,")
    a("}")
    a("")
    a("pub const HIDDEN_STATE_CENSUS: HiddenStateCensus = HiddenStateCensus {")
    a(f"    question: {rust_str(census['question'])},")
    a(f"    answer: {rust_str(census['answer'])},")
    a("    candidates: &[")
    for c in census["candidates_checked"]:
        a("        HiddenStateCandidate {")
        a(f"            candidate: {rust_str(c['candidate'])},")
        a(f"            present: {'true' if c['present'] else 'false'},")
        a(f"            why: {rust_str(c['why'])},")
        a("        },")
    a("    ],")
    a(f"    consequence: {rust_str(census['consequence'])},")
    a("};")
    a("")
    return "\n".join(w)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--state", type=Path, default=STATE)
    ap.add_argument("--arith", type=Path, default=ARITH)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--check", action="store_true",
                    help="exit 0 iff the committed module already matches regeneration")
    args = ap.parse_args(argv)

    try:
        doc, arith_xlen = load_checked(args.state, args.arith)
        named, regs, census = validate(doc, arith_xlen)
        state_sha = hashlib.sha256(args.state.read_bytes()).hexdigest()
        if doc["profile_id"] == "rv64gc-lab-v0":
            text = emit_gc(doc, named, regs, census, state_sha,
                           str(args.state))
        else:
            text = emit(doc, named, regs, census, state_sha)
    except (Refusal, D.DossierError) as exc:
        print(f"gen_state: REFUSED — {exc}", file=sys.stderr)
        return 2

    if args.check:
        committed = args.out.read_text(encoding="utf-8") if args.out.exists() else ""
        if committed == text:
            return 0
        diff = "\n".join(difflib.unified_diff(
            committed.splitlines(), text.splitlines(),
            fromfile=str(args.out), tofile=f"{args.out} (regenerated)", n=2))
        print(f"gen_state: DRIFT — {args.out} no longer matches {args.state}:\n"
              f"{diff}\n"
              f"Regenerate — never edit: python3 scripts/gen_state.py", file=sys.stderr)
        return 1

    args.out.write_text(text, encoding="utf-8")
    print(f"gen_state: wrote {args.out} ({len(text)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
