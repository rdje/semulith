#!/usr/bin/env python3
"""Generate a profile's `encoding.sexp` — the instruction encodings the repository OWNS.

⛔ THE GAP THIS CLOSES, measured. Before this file existed the assembler read its encodings from
`target/refs/riscv-opcodes` — untracked and network-acquired — so `git ls-files | grep -c
riscv-opcodes` returned `0` and a fresh clone could not build a model at all. The project's own
rule is that a constant which is a function of an external document is derived or gated, never
assumed present; its own tooling was breaking that rule.

The generated file is TRACKED, so the repository owns its encodings, and `fetch_references.sh`
re-derives it against the pinned upstream whenever that upstream is present. Ownership without a
re-derivation would just be a copy.

Usage:  scripts/gen_encoding.py <profile>
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from riscv_asm import Assembler  # noqa: E402

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
UPSTREAM = ROOT / "target/refs/riscv-opcodes"
SOURCE_FILES = ("rv_i", "rv64_i", "arg_lut.csv", "constants.py")
# Only the operand fields this profile's instructions actually use are emitted: an encoding file
# listing fields nothing references would invite a reader to believe they are supported.
USED_FIELDS = ("rd", "rs1", "rs2", "imm12", "imm20", "shamtd", "shamtw",
               "imm12hi", "imm12lo", "jimm20", "bimm12hi", "bimm12lo")

HEADER = '''\
;; encoding.sexp — the instruction encodings this model OWNS.
;;
;; ⛔ DERIVED, TRACKED, AND GATED. Before this file existed the assembler read its encodings from
;; `target/refs/riscv-opcodes` — untracked and network-acquired — so a fresh clone could not build
;; a model at all, and the project's own rule (a constant that is a function of an external
;; document is derived or gated, never assumed present) was being broken by its own tooling.
;;
;; ⚠️ WHAT THIS FILE IS NOT. Encodings only: which bits name which instruction, and which fields
;; carry its operands. It says nothing about what an instruction MEANS — that is `semantics.sexp`,
;; and the two are separate because a decoder and an interpreter are separate generated artifacts.
;;
;; Regenerate with `scripts/gen_encoding.py <profile>`. Do not edit by hand.
'''


def sha256(path: Path) -> str:
    return subprocess.run(["shasum", "-a", "256", str(path)],
                          capture_output=True, text=True, check=True).stdout.split()[0]


def build(profile: str) -> str:
    asm = Assembler(UPSTREAM)
    out: list[str] = [HEADER, "(encoding", f'  (profile "{profile}")', "  (ilen 32)", "  (source",
                      '    (id "RISCV-OPCODES")',
                      '    (origin "https://github.com/riscv/riscv-opcodes")',
                      '    (license "BSD-3-Clause")']
    for f in SOURCE_FILES:
        out.append(f'    (file (name "{f}") (sha256 "{sha256(UPSTREAM / f)}"))')
    out.append('    (note "Upstream of Spike and NOT of Sail: Spike generates its encoding.h from '
               'this table, while the Sail model hand-writes 59 files of encdec mappings and never '
               'references it. So Sail decoding bytes built from this file is an independent '
               'confirmation of the encoding; Spike doing so is not."))')
    out.append("")
    out.append("  ;; ---- operand field positions, inclusive bit ranges ------------------------")
    for name in USED_FIELDS:
        hi, lo = asm.arg_lut[name]
        out.append(f"  (field (name {name}) (hi {hi}) (lo {lo}))")
    out.append("")
    out.append("  ;; ---- immediates SCATTERED across their field, most-significant piece first -")
    out.append("  ;; Read as: the field's top bits hold imm[hi:lo], then the next piece, and so on.")
    out.append("  ;; The pieces must total the field width, and the reader refuses a layout that")
    out.append("  ;; does not — a silently wrong immediate is a jump to the wrong address.")
    for name in sorted(asm.imm_layout):
        hi, lo = asm.arg_lut[name]
        pieces = " ".join(f"({h} {l})" for h, l in asm.imm_layout[name])
        out.append(f"  (scatter (name {name}) (hi {hi}) (lo {lo}) (pieces {pieces}))")
    out.append("")
    out.append(f"  ;; ---- the declared instruction scope: {len(asm.insns)} mnemonics ----------")
    for name in sorted(asm.insns):
        insn = asm.insns[name]
        fixed = " ".join(f"({h} {lo} {v:#x})" for h, lo, v in insn.fixed)
        ops = " ".join(str(o) for o in insn.operands)
        out.append(f"  (insn (name {name}) (fixed {fixed}) (operands {ops}) "
                   f'(from "{insn.source}"))')
    out.append(")")
    return "\n".join(out) + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: gen_encoding.py <profile>", file=sys.stderr)
        return 2
    if not UPSTREAM.is_dir():
        print(f"gen_encoding: {UPSTREAM} is absent — run scripts/fetch_references.sh first",
              file=sys.stderr)
        return 2
    text = build(argv[1])
    out = ROOT / "profiles" / argv[1] / "encoding.sexp"
    out.write_text(text)
    print(f"wrote {out.relative_to(ROOT)} ({len(text)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
