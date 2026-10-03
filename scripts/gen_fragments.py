#!/usr/bin/env python3
"""Generate the reusable definition FRAGMENTS the repository owns.

A fragment is a complete, independently checkable description of one thing — an ISA base, an
extension — and lives under `definitions/` because it is shared by every unit that composes it.
A unit's `encoding.sexp` names fragments; it never carries a copy of an instruction.

⛔ THE GAP THIS CLOSES, measured. Before this file existed the assembler read its encodings from
`target/refs/riscv-opcodes` — untracked and network-acquired — so `git ls-files | grep -c
riscv-opcodes` returned `0` and a fresh clone could not build a model at all. The project's own
rule is that a constant which is a function of an external document is derived or gated, never
assumed present; its own tooling was breaking that rule.

The generated file is TRACKED, so the repository owns its encodings, and `fetch_references.sh`
re-derives it against the pinned upstream whenever that upstream is present. Ownership without a
re-derivation would just be a copy.

Usage:  scripts/gen_fragments.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
UPSTREAM = ROOT / "target/refs/riscv-opcodes"
SOURCE_FILES = ("rv_i", "rv64_i", "arg_lut.csv", "constants.py")
# Only the operand fields this profile's instructions actually use are emitted: an encoding file
# listing fields nothing references would invite a reader to believe they are supported. `fm`,
# `pred` and `succ` are FENCE's (`P2-SCALAR.1`: a guest assembles `fence`, and the fields come
# from the pinned `arg_lut.csv` like every other — derived, never typed).
USED_FIELDS = ("rd", "rs1", "rs2", "imm12", "imm20", "shamtd", "shamtw",
               "imm12hi", "imm12lo", "jimm20", "bimm12hi", "bimm12lo",
               "fm", "pred", "succ")

def sha256(path: Path) -> str:
    return subprocess.run(["shasum", "-a", "256", str(path)],
                          capture_output=True, text=True, check=True).stdout.split()[0]


FRAGMENTS = (
    # (output, fragment id, kind, tables, requires, fields, scatter, pseudo, note)
    # requires: the fragment ids this one depends on, one (requires "…") form each — an
    #          empty tuple emits the bare `(requires)` marker.
    # fields:  the operand fields THIS fragment owns (positions from the pinned arg_lut.csv,
    #          derived never typed) — a base defines the formats its extensions reuse; an
    #          extension owns the fields its instructions introduce.
    # scatter: emit the scrambled-immediate layouts (the base's B/J formats).
    # pseudo:  also emit the tables' $pseudo_op rows as (pseudo …) assembler spellings —
    #          only for a fragment whose selected forms exist upstream ONLY as pseudo-ops
    #          (Zicntr's counter reads; measured at the P4-SYSTEM.2 re-pin).
    ("definitions/riscv/rv64i.sexp", "riscv/rv64i", "isa-base", ("rv_i", "rv64_i"), (),
     USED_FIELDS, True, False,
     "The RV64I base: the 52 instructions every RV64 profile starts from. Carries the operand "
     "field table and the scattered-immediate layouts, because a base defines the formats its "
     "extensions reuse."),
    ("definitions/riscv/m.sexp", "riscv/m", "isa-extension", ("rv_m", "rv64_m"),
     ("riscv/rv64i",), (), False, False,
     "The M extension: integer multiply and divide. REQUIRES a base, because it reuses the base's "
     "R-type operand fields and defines none of its own — a fragment with a hidden dependency is a "
     "fragment that composes by luck."),
    ("definitions/riscv/zicsr.sexp", "riscv/zicsr", "isa-extension", ("rv_zicsr",),
     ("riscv/rv64i",), ("csr", "zimm5"), False, False,
     "The Zicsr extension: the CSR access instructions csrrw/csrrs/csrrc and their immediate "
     "forms. It OWNS the csr and zimm5 operand fields (the base's field table predates them, and "
     "a field nothing owns is a field nobody can check); csr shares bits 31..20 with imm12 and "
     "the pinned arg_lut.csv distinguishes them by field name. REQUIRES a base: it reuses rd/rs1 "
     "from it (P4-SYSTEM.2 slice a)."),
    ("definitions/riscv/zicntr.sexp", "riscv/zicntr", "isa-extension", ("rv_zicntr",),
     ("riscv/rv64i", "riscv/zicsr"), (), False, True,
     "The Zicntr extension: the base counter reads rdcycle/rdtime/rdinstret. It adds NO new "
     "encodings — upstream carries the three only as $pseudo_op rows of Zicsr's csrrs, each "
     "fully fixed by its row — so the fragment carries them as (pseudo …) assembler spellings "
     "and the encoding space is untouched. It REQUIRES Zicsr by name (the pinned rows say "
     "rv_zicsr::csrrs — the realizing instruction lives there), not only the base "
     "(P4-SYSTEM.2 slice a)."),
    ("definitions/riscv/system.sexp", "riscv/system", "isa-extension", ("rv_system", "rv_s"),
     ("riscv/rv64i",), (), False, False,
     "The privileged system instructions: mret and wfi (rv_system), sret and sfence.vma (rv_s) "
     "— the profile's selection from RVP-INSNS 18.1 (D-PRIV-INSNS). REQUIRES a base, because "
     "ecall/ebreak own the neighbouring fixed points of the SYSTEM opcode (P4-SYSTEM.2 "
     "slice a)."),
)


def regenerate() -> int:
    from riscv_asm import AsmError, load_arg_lut, load_encodings, load_immediate_layout, \
        load_pseudo_ops
    arg_lut = load_arg_lut(UPSTREAM / "arg_lut.csv")
    layout = load_immediate_layout(UPSTREAM / "constants.py", arg_lut)
    for rel, fid, kind, tables, requires, fields, scatter, pseudo, note in FRAGMENTS:
        insns = load_encodings([UPSTREAM / t for t in tables], allow_empty=pseudo)
        pseudos = load_pseudo_ops([UPSTREAM / t for t in tables]) if pseudo else {}
        if not insns and not pseudos:
            raise AsmError(f"{rel}: the pinned tables yielded neither instructions nor "
                           f"pseudo-ops — an empty fragment is not a valid one")
        L = [f";; {Path(rel).name} — a reusable definition FRAGMENT ({kind}).", ";;",
             ";; A fragment is a complete, independently checkable description of ONE thing. It",
             ";; lives here rather than inside a profile because a base ISA is shared by every",
             ";; profile that composes it — copying it per profile would be the duplication the",
             ";; composition model exists to avoid. A unit COMPOSES fragments;",
             ";; `scripts/check_encoding_disjoint.py` decides whether a composition is legal.", ";;",
             f";; {note}", ";;",
             ";; Generated by `scripts/gen_fragments.py`. Do not edit by hand.", "",
             "(fragment", f'  (id "{fid}")', f"  (kind {kind})"]
        if requires:
            L += [f'  (requires "{r}")' for r in requires]
        else:
            L.append("  (requires)")
        L.append("  (source")
        for t in tables:
            L.append(f'    (file (name "{t}") (sha256 "{sha256(UPSTREAM / t)}"))')
        L += ['    (origin "https://github.com/riscv/riscv-opcodes")',
              '    (license "BSD-3-Clause"))', ""]
        if fields:
            L.append("  ;; ---- operand field positions, inclusive bit ranges ------------------")
            for n in fields:
                hi, lo = arg_lut[n]
                L.append(f"  (field (name {n}) (hi {hi}) (lo {lo}))")
            L.append("")
        if scatter:
            L.append("  ;; ---- immediates SCATTERED across their field, MSB piece first -------")
            for n in sorted(layout):
                hi, lo = arg_lut[n]
                pieces = " ".join(f"({h} {l})" for h, l in layout[n])
                L.append(f"  (scatter (name {n}) (hi {hi}) (lo {lo}) (pieces {pieces}))")
            L.append("")
        L.append(f"  ;; ---- {len(insns)} instruction(s) ----")
        for name in sorted(insns):
            i = insns[name]
            fixed = " ".join(f"({h} {lo} {v:#x})" for h, lo, v in i.fixed)
            ops = " ".join(str(o) for o in i.operands)
            L.append(f'  (insn (name {name}) (fixed {fixed}) (operands {ops}) (from "{i.source}"))')
        if pseudos:
            L += ["",
                  "  ;; ---- pseudo-instruction(s): assembler spellings, NOT new encodings ------",
                  "  ;; Each row's fixed bits specialize a real instruction's (the `of` base), so",
                  "  ;; the word it assembles is already in the encoding space.",
                  ]
            for name in sorted(pseudos):
                i = pseudos[name]
                fixed = " ".join(f"({h} {lo} {v:#x})" for h, lo, v in i.fixed)
                ops = " ".join(str(o) for o in i.operands)
                L.append(f'  (pseudo (name {name}) (of "{i.of}") (fixed {fixed}) '
                         f'(operands {ops}) (from "{i.source}"))')
        L.append(")")
        (ROOT / rel).write_text("\n".join(L) + "\n")
    return len(FRAGMENTS)


def main(argv: list[str]) -> int:
    if not UPSTREAM.is_dir():
        print(f"gen_fragments: {UPSTREAM} is absent — run scripts/fetch_references.sh first",
              file=sys.stderr)
        return 2
    n = regenerate()
    print(f"regenerated {n} fragment(s) under definitions/")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
