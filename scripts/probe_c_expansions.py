#!/usr/bin/env python3
"""Probe C's declaration and its generated Rust table before the engine bind.

The expected base names, register mappings and immediate limits below are hand-written
from RVI-C §27.1.3–§27.1.5 (RV64 + D). They are not derived from c.sem.sexp. This is finite
evidence for the language/generator slice, never evidence that a CPU executes C correctly.
DEF-GEN runs it on a temporary composition WITH C, including a planted wrong mapping.

Usage: probe_c_expansions.py ENCODING GENERATED_MODULE
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import gen_definition as G

REPO = Path(__file__).resolve().parent.parent
MASK = (1 << 64) - 1

# RVI-C §27.1.3.1–§27.1.5.6: instruction -> (base, register operands).
# Field values are all ones: full registers are 31, compact registers are x15.
EXPECTED = {
    "c.addi4spn": ("addi", {"rd": 15, "rs1": 2}),
    "c.fld": ("fld", {"rd": 15, "rs1": 15}),
    "c.lw": ("lw", {"rd": 15, "rs1": 15}),
    "c.ld": ("ld", {"rd": 15, "rs1": 15}),
    "c.fsd": ("fsd", {"rs1": 15, "rs2": 15}),
    "c.sw": ("sw", {"rs1": 15, "rs2": 15}),
    "c.sd": ("sd", {"rs1": 15, "rs2": 15}),
    "c.nop": ("addi", {"rd": 0, "rs1": 0}),
    "c.addi": ("addi", {"rd": 31, "rs1": 31}),
    "c.addiw": ("addiw", {"rd": 31, "rs1": 31}),
    "c.li": ("addi", {"rd": 31, "rs1": 0}),
    "c.addi16sp": ("addi", {"rd": 2, "rs1": 2}),
    "c.lui": ("lui", {"rd": 31}),
    "c.srli": ("srli", {"rd": 15, "rs1": 15}),
    "c.srai": ("srai", {"rd": 15, "rs1": 15}),
    "c.andi": ("andi", {"rd": 15, "rs1": 15}),
    "c.sub": ("sub", {"rd": 15, "rs1": 15, "rs2": 15}),
    "c.xor": ("xor", {"rd": 15, "rs1": 15, "rs2": 15}),
    "c.or": ("or", {"rd": 15, "rs1": 15, "rs2": 15}),
    "c.and": ("and", {"rd": 15, "rs1": 15, "rs2": 15}),
    "c.subw": ("subw", {"rd": 15, "rs1": 15, "rs2": 15}),
    "c.addw": ("addw", {"rd": 15, "rs1": 15, "rs2": 15}),
    "c.j": ("jal", {"rd": 0}),
    "c.beqz": ("beq", {"rs1": 15, "rs2": 0}),
    "c.bnez": ("bne", {"rs1": 15, "rs2": 0}),
    "c.slli": ("slli", {"rd": 31, "rs1": 31}),
    "c.fldsp": ("fld", {"rd": 31, "rs1": 2}),
    "c.lwsp": ("lw", {"rd": 31, "rs1": 2}),
    "c.ldsp": ("ld", {"rd": 31, "rs1": 2}),
    "c.jr": ("jalr", {"rd": 0, "rs1": 31, "imm12": 0}),
    "c.mv": ("add", {"rd": 31, "rs1": 0, "rs2": 31}),
    "c.ebreak": ("ebreak", {}),
    "c.add": ("add", {"rd": 31, "rs1": 31, "rs2": 31}),
    "c.fsdsp": ("fsd", {"rs1": 2, "rs2": 31}),
    "c.swsp": ("sw", {"rs1": 2, "rs2": 31}),
    "c.sdsp": ("sd", {"rs1": 2, "rs2": 31}),
    "c.jalr": (None, {"rd": 1, "rs1": 31}),
}

# name, bound operand, signed?, immediate width, scale (low zero bits).
# C.LUI binds the UN-SHIFTED base LUI operand; its signed six bits extend to 20.
LIMITS = [
    ("c.addi4spn", "imm12", False, 10, 2),
    *((n, "imm12", False, 8, 3) for n in ("c.fld", "c.ld", "c.fsd", "c.sd")),
    *((n, "imm12", False, 7, 2) for n in ("c.lw", "c.sw")),
    *((n, "imm12", True, 6, 0) for n in ("c.nop", "c.addi", "c.addiw", "c.li", "c.andi")),
    ("c.addi16sp", "imm12", True, 10, 4),
    ("c.lui", "imm20", True, 6, 0),
    *((n, "shamt", False, 6, 0) for n in ("c.srli", "c.srai", "c.slli")),
    ("c.j", "jimm20", True, 12, 1),
    *((n, "bimm12", True, 9, 1) for n in ("c.beqz", "c.bnez")),
    *((n, "imm12", False, 9, 3) for n in ("c.fldsp", "c.ldsp", "c.fsdsp", "c.sdsp")),
    *((n, "imm12", False, 8, 2) for n in ("c.lwsp", "c.swsp")),
]


def mask(width):
    return (1 << width) - 1


def eval_mapping(expr, fields):
    """The mapping vocabulary's value/width algebra (schema/semantics.sexp)."""
    op, *args = expr
    if op == "lit":
        return args[0] & MASK, 64
    if op in ("imm", "field"):
        return fields[args[0]]
    if op in ("add", "or", "and", "eq", "ne"):
        x, wx = eval_mapping(args[0], fields)
        y, wy = eval_mapping(args[1], fields)
        value = {"add": lambda: (x + y) & MASK, "or": lambda: x | y,
                 "and": lambda: x & y, "eq": lambda: int(x == y),
                 "ne": lambda: int(x != y)}[op]()
        return value, max(wx, wy)
    if op in ("zext", "sext", "trunc"):
        target, expr = args
        value, width = eval_mapping(expr, fields)
        if op == "sext":
            value &= mask(width)
            if value & (1 << (width - 1)):
                value -= 1 << width
        else:
            value &= mask(min(target, width))
        return value & MASK, target
    if op == "bits":
        hi, lo, expr = args
        value, _ = eval_mapping(expr, fields)
        return (value >> lo) & mask(hi - lo + 1), hi - lo + 1
    raise AssertionError(f"mapping probe cannot evaluate {op}")


def fields_at(data, insn, word):
    out = {}
    for name, hi, lo, pieces in data["fields"]:
        if name not in insn.operands:
            continue
        value = (word >> lo) & mask(hi - lo + 1)
        width = hi - lo + 1
        if pieces:
            bits, value, remaining = value, 0, width
            for top, bottom in pieces:
                n = top - bottom + 1
                remaining -= n
                value |= ((bits >> remaining) & mask(n)) << bottom
            width = max(top for top, _ in pieces) + 1
        out[name] = value, width
    return out


def probe(data):
    expansions = data["expansions"]
    assert set(expansions) == set(EXPECTED), "compressed form census differs from the RV64+D selection"
    checks = 0
    compiled_cases = []
    for name, (expected_base, expected_regs) in EXPECTED.items():
        base, binds, _ = expansions[name]
        assert base == expected_base, f"{name}: base {base!r}, expected {expected_base!r}"
        insn = data["insns"][name]
        fixed_mask, fixed_value = G.fixed_mask(name, insn.fixed)
        word = fixed_value | (0xffff & ~fixed_mask)
        fields = fields_at(data, insn, word)
        values = {n: eval_mapping(v, fields)[0] for n, v in binds}
        for n, expected in expected_regs.items():
            assert values[n] == expected, f"{name}: {n}={values[n]}, expected {expected}"
            compiled_cases.append((name, word, n, expected, False))
        checks += 1
    for name, operand, signed, width, scale in LIMITS:
        insn = data["insns"][name]
        _, binds, reserved = expansions[name]
        expr = dict(binds)[operand]
        immediate_mask = 0
        for fname, hi, lo, pieces in data["fields"]:
            if fname in insn.operands and pieces:
                immediate_mask |= mask(hi - lo + 1) << lo
        # RVI-C's signed immediates ALL place the sign at parcel bit 12.
        maximum = ((1 << (width - int(signed))) - 1) & ~mask(scale)
        cases = [(0, 0), (immediate_mask & ~(0x1000 if signed else 0), maximum)]
        if signed:
            cases.append((0x1000, -(1 << (width - 1))))
        for bits, expected in cases:
            fixed_mask, fixed_value = G.fixed_mask(name, insn.fixed)
            word = ((fixed_value | (0xffff & ~fixed_mask)) & ~immediate_mask) | bits
            fields = fields_at(data, insn, word)
            value, value_width = eval_mapping(expr, fields)
            # Interpret at the width the BASE rule receives (including C.LUI's 20 bits).
            value &= mask(value_width)
            if signed and value & (1 << (value_width - 1)):
                value -= 1 << value_width
            assert value == expected, f"{name}: {operand}={value}, expected {expected}"
            compiled_cases.append((name, word, operand, expected, signed))
            if name in ("c.addi4spn", "c.addi16sp", "c.lui"):
                assert bool(eval_mapping(reserved, fields)[0]) == (expected == 0), \
                    f"{name}: wrong zero-immediate reservation"
            checks += 1
    for name, field in (("c.addiw", "rd_rs1_n0"), ("c.lwsp", "rd_n0"),
                        ("c.ldsp", "rd_n0"), ("c.jr", "rs1_n0")):
        fields = fields_at(data, data["insns"][name], 0xffff)
        fields[field] = (0, 5)
        assert eval_mapping(expansions[name][2], fields)[0] == 1, f"{name}: zero register must be reserved"
        checks += 1
    # The source's explicit exception: read target before writing x1, link = old pc+2.
    assert data["rules"]["c.jalr"][1] == ["seq", ["set-pc", ["and", ["reg", "rs1"], ["lit", -2]]],
        ["set", ["reg", "rd"], ["add", ["pc"], ["lit", 2]]]], "C.JALR must link at pc+2"
    return checks + 1, compiled_cases


def compiled_probe(module, cases):
    # Literal parcels independently name the specialization, including both general rows.
    # This runs the ACTUAL generated decoder, not the generator's Python ordering helper.
    pairs = [(0x0001, "c.nop"), (0x8082, "c.jr"), (0x9082, "c.jalr"),
             (0x9002, "c.ebreak"), (0x6105, "c.addi16sp"), (0x6185, "c.lui"),
             (0x8086, "c.mv"), (0x9086, "c.add")]
    subprocess.run(["rustfmt", "--check", "--color", "never", str(module)],
                   check=True, capture_output=True, text=True)
    with tempfile.TemporaryDirectory(dir=REPO / "target") as d:
        d = Path(d)
        import json
        code = '#[allow(dead_code)]\n#[path=' + json.dumps(str(module.resolve())) + ']\nmod def;\n'
        code += r'''
fn mask(w: u32) -> u64 { if w == 64 { u64::MAX } else { (1u64 << w) - 1 } }
fn field(name: &str, word: u32) -> (u64, u32) {
    let f = def::FIELDS.iter().find(|f| f.name == name).unwrap();
    let mut width = u32::from(f.hi - f.lo + 1);
    let raw = (u64::from(word) >> f.lo) & mask(width);
    if f.scatter.is_empty() { return (raw, width); }
    let mut value = 0;
    for &(hi, lo) in f.scatter {
        let n = u32::from(hi - lo + 1);
        width -= n;
        value |= ((raw >> width) & mask(n)) << lo;
    }
    (value, u32::from(f.scatter.iter().map(|&(hi, _)| hi).max().unwrap()) + 1)
}
fn eval(e: &def::Sem, word: u32) -> (u64, u32) {
    use def::Sem;
    match e {
        Sem::Lit(v) => (*v, 64),
        Sem::Field(n) | Sem::Imm(n) => field(n, word),
        Sem::Add(a, b) | Sem::Or(a, b) | Sem::And(a, b) | Sem::Eq(a, b) | Sem::Ne(a, b) => {
            let (x, wx) = eval(a, word); let (y, wy) = eval(b, word);
            let v = match e { Sem::Add(..) => x.wrapping_add(y), Sem::Or(..) => x | y,
                Sem::And(..) => x & y, Sem::Eq(..) => u64::from(x == y),
                Sem::Ne(..) => u64::from(x != y), _ => unreachable!() };
            (v, wx.max(wy))
        }
        Sem::Sext(w, e) => { let (v, from) = eval(e, word);
            ((((v << (64 - from)) as i64) >> (64 - from)) as u64, *w as u32) }
        Sem::Zext(w, e) | Sem::Trunc(w, e) => { let (v, from) = eval(e, word);
            (v & mask(from.min(*w as u32)), *w as u32) }
        Sem::Bits(hi, lo, e) => { let (v, _) = eval(e, word);
            let w = u32::from(hi - lo + 1); ((v >> lo) & mask(w), w) }
        _ => panic!("not a mapping expression: {e:?}"),
    }
}
fn binding(name: &str, operand: &str, word: u32, signed: bool) -> i128 {
    let insn = def::INSNS.iter().find(|i| i.name == name).unwrap();
    let b = insn.expansion.unwrap().bindings.iter().find(|b| b.name == operand).unwrap();
    let (v, w) = eval(b.value, word); let v = v & mask(w);
    if signed && v & (1 << (w - 1)) != 0 { i128::from(v) - (1i128 << w) }
    else { i128::from(v) }
}
#[test] fn emitted_expansions() {
'''
        for name, word, operand, expected, signed in cases:
            code += (f'assert_eq!(binding("{name}", "{operand}", {word}, '
                     f'{str(signed).lower()}), {expected}, "{name} {operand}");\n')
        for name, (base, _) in EXPECTED.items():
            if base is not None:
                code += (f'let c = def::INSNS.iter().find(|i| i.name == "{name}").unwrap();\n'
                         f'let b = def::INSNS.iter().find(|i| i.name == "{base}").unwrap();\n'
                         f'assert_eq!(c.expansion.unwrap().base, Some("{base}"));\n'
                         'assert_eq!(format!("{:?}", c.effect), format!("{:?}", b.effect));\n')
        code += r'''
let c = def::INSNS.iter().find(|i| i.name == "c.jalr").unwrap();
let expected = def::Sem::Seq(&[
    &def::Sem::SetPc(&def::Sem::And(&def::Sem::Reg("rs1"), &def::Sem::Lit(u64::MAX - 1))),
    &def::Sem::Set(&def::Sem::Reg("rd"), &def::Sem::Add(&def::Sem::Pc, &def::Sem::Lit(2))),
]);
assert_eq!(format!("{:?}", c.effect), format!("{:?}", expected));
'''
        for name, word, reserved in [("c.addi4spn", 0, True), ("c.addi16sp", 0x6101, True),
                ("c.lui", 0x6181, True), ("c.addiw", 0x2001, True), ("c.lwsp", 0x4002, True),
                ("c.ldsp", 0x6002, True), ("c.jr", 0x8002, True),
                ("c.addi", 0x0081, False), ("c.li", 0x4005, False), ("c.slli", 0x0082, False),
                ("c.mv", 0x8006, False), ("c.add", 0x9006, False), ("c.nop", 0x0005, False)]:
            code += (f'let i = def::INSNS.iter().find(|i| i.name == "{name}").unwrap();\n'
                     f'assert_eq!(i.expansion.unwrap().reserved.is_some_and(|e| eval(e, {word}).0 != 0), '
                     f'{str(reserved).lower()}, "{name} reserved/HINT");\n')
        code += '}\n'
        code += '#[test] fn specialization_decode() {\n'
        for word, name in pairs:
            code += f'assert_eq!(def::decode({word}).unwrap().name, "{name}");\n'
        code += 'assert_eq!(def::decode(0x13).unwrap().length, 4);\n'
        code += 'assert_eq!(def::decode(1).unwrap().length, 2);\n'
        code += 'assert_eq!(def::INSNS.iter().filter(|i| i.expansion.is_some()).count(), 37);\n}\n'
        (d / "probe.rs").write_text(code)
        subprocess.run(["rustc", "--edition=2021", "--test", str(d / "probe.rs"),
                        "-o", str(d / "probe")], check=True, capture_output=True, text=True)
        subprocess.run([str(d / "probe")], check=True, capture_output=True, text=True)


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        data = G.load_inputs(Path(sys.argv[1]), REPO / "profiles/rv64gc-lab-v0/state.sexp")
        checks, cases = probe(data)
        compiled_probe(Path(sys.argv[2]), cases)
        print(f"C expansion probe: {len(EXPECTED)} forms, {checks} spec-side checks; compiled decoder 8/8")
        return 0
    except (AssertionError, G.Refusal, subprocess.CalledProcessError) as exc:
        print(f"C expansion probe: FAIL — {exc}", file=sys.stderr)
        if isinstance(exc, subprocess.CalledProcessError):
            print(exc.stdout + exc.stderr, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
