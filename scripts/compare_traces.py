#!/usr/bin/env python3
"""Normalize two reference models' traces and report the FIRST divergence.

Two models are only comparable once their traces are reduced to the same observation vocabulary.
This module reduces both to a sequence of steps:

    (pc, encoded_instruction_word, [(register, value), ...])

and then walks the two sequences together, stopping at the first step that differs. `EVD-02`
asks for minimized discrepancies rather than a diff of everything; a first-divergence report is
the minimal form, because every later difference may be a consequence of the first.

⛔ ALIGNMENT IS EXPLICIT, NOT ASSUMED. The two models do not start in the same place: Spike runs
a built-in reset vector before transferring to the ELF entry point, while the Sail model begins
at the entry directly. Comparing step 0 with step 0 would report a divergence that is purely a
harness difference. Both traces are therefore aligned on the first step whose `pc` equals the
declared entry, and a trace that never reaches it is an error rather than an empty match.

⚠️ HONEST LIMIT: agreement here is evidence for THESE inputs on THESE two models, and nothing
more. `docs/EVIDENCE_AND_GATES.md` is explicit that finite differential testing is tested
evidence, never universal proof — and two models that share semantic ancestry can agree while
both being wrong, which is `EVD-04` and why `P0-PROFILE.7` exists.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


class CompareError(Exception):
    """A refusal. An unparseable trace is never an empty one."""


@dataclass
class Step:
    pc: int
    word: int
    writes: list[tuple[str, int]] = field(default_factory=list)
    trap: tuple[int, int] | None = None        # (cause code, tval)

    def key(self) -> tuple:
        return (self.pc, self.word, tuple(sorted(self.writes)), self.trap)


# ---------------------------------------------------------------------------------------
# THE ADAPTER: each model's spelling of an exception -> the architectural CAUSE CODE.
#
# `EVD-05` requires a normalization to have a source-grounded justification, so the ground
# truth is not this file: it is `causes.csv` from the pinned `riscv-opcodes` tables, where
# 0x04 is "misaligned load" and 0x01 is "fetch access". The table below only says which
# words each model chose for those causes — it never invents a cause.
#
# ⛔ An unrecognised spelling RAISES. A trap that silently fails to parse is a trap that
# disappears from the comparison, and a disappearing trap reads exactly like agreement.
# ⚠️ This is a versioned adapter in the sense of `docs/EVIDENCE_AND_GATES.md` §5: it is tied
# to sail-riscv 0.14 and spike 1.1.1-dev, and a model that renames an exception must be
# re-read here rather than accommodated by a looser match.
# ---------------------------------------------------------------------------------------
TRAP_NAMES: dict[str, int] = {
    # sail-riscv 0.14 spellings
    "misaligned-load": 0x04,
    "fetch-access-fault": 0x01,
    "illegal-instruction": 0x02,
    "misaligned-store": 0x06,
    "load-access-fault": 0x05,
    "store-access-fault": 0x07,
    "m-call": 0x0B,                 # environment call from M-mode (measured, P2-SCALAR.1)
    "software-breakpoint": 0x03,    # EBREAK; tval is the ebreak's own address (measured)
    # spike 1.1.1-dev spellings
    "trap_load_address_misaligned": 0x04,
    "trap_instruction_access_fault": 0x01,
    "trap_illegal_instruction": 0x02,
    "trap_store_address_misaligned": 0x06,
    "trap_load_access_fault": 0x05,
    "trap_store_access_fault": 0x07,
    "trap_machine_ecall": 0x0B,     # measured, P2-SCALAR.1
    "trap_breakpoint": 0x03,        # measured; tval = the ebreak's address
}


def trap_cause(spelling: str, who: str) -> int:
    key = spelling.strip()
    if key not in TRAP_NAMES:
        raise CompareError(
            f"{who}: unknown exception spelling {key!r}. The adapter must be extended with its "
            f"architectural cause code from the pinned causes table — a trap this comparator "
            f"cannot name is a trap it would otherwise drop, and a dropped trap looks like "
            f"agreement.")
    return TRAP_NAMES[key]


# Semulith's own trace (`semulith run`, P1-LAB.8): the same observation vocabulary the
# reference adapters reduce to, printed directly — no spelling adapter needed, because the
# cause is emitted as the architectural code, not a model-specific name.
#   "[3] [M]: 0x000000008000000c (0x03f19213) slli"
#   "x4 <- 0x8000000000000000"
#   "trap cause=0x04 tval=0x0000000080000401"
_SEMULITH_STEP = re.compile(r"^\[\d+\] \[M\]:\s+0x([0-9a-fA-F]+)\s+\(0x([0-9a-fA-F]+)\)")
_SEMULITH_WRITE = re.compile(r"^(x\d{1,2}) <- 0x([0-9A-Fa-f]+)\s*$")
_SEMULITH_TRAP = re.compile(r"^trap cause=0x([0-9a-fA-F]+) tval=0x([0-9a-fA-F]+)\s*$")


def parse_semulith(text: str) -> list[Step]:
    """Parse `semulith run` output into the shared observation vocabulary.

    Unlike the reference adapters this parser needs no cause-name table: the laboratory's
    trap line carries the architectural cause code directly. A line that looks like a trap
    before any step is a malformed trace, not an empty match — raised, never dropped.
    """
    steps: list[Step] = []
    for line in text.splitlines():
        m = _SEMULITH_STEP.match(line.strip())
        if m:
            steps.append(Step(int(m.group(1), 16), int(m.group(2), 16)))
            continue
        m = _SEMULITH_WRITE.match(line.strip())
        if m and steps:
            steps[-1].writes.append((m.group(1), int(m.group(2), 16)))
            continue
        m = _SEMULITH_TRAP.match(line.strip())
        if m:
            if not steps:
                raise CompareError(
                    "semulith: trap record before any step — a malformed trace is not an "
                    "empty match")
            if steps[-1].trap is None:
                steps[-1].trap = (int(m.group(1), 16), int(m.group(2), 16))
    return steps


# Sail: "[0] [M]: 0x0000000080000000 (0x800000B7) lui x1, -0x80000"
#       "x1 <- 0xFFFFFFFF80000000"
_SAIL_STEP = re.compile(r"^\[\d+\]\s+\[\w+\]:\s+0x([0-9A-Fa-f]+)\s+\(0x([0-9A-Fa-f]+)\)")
_SAIL_WRITE = re.compile(r"^(x\d{1,2})\s+<-\s+0x([0-9A-Fa-f]+)\s*$")
# "handling exc#misaligned-load at priv M | tval=0x0000000080000401 | ..."
_SAIL_TRAP = re.compile(r"^handling exc#(\S+) at priv \w+ \| tval=0x([0-9A-Fa-f]+)")

# Spike full log: "core   0: exception trap_load_address_misaligned, epc 0x0000000080000008"
#                 "core   0:           tval 0x0000000080000401"
_SPIKE_TRAP = re.compile(r"^core\s+\d+:\s+exception\s+(\S+),\s+epc\s+0x([0-9a-fA-F]+)")
_SPIKE_TVAL = re.compile(r"^core\s+\d+:\s+tval\s+0x([0-9a-fA-F]+)")
# Spike `-l` disassembly form, WITHOUT the privilege digit:
#   "core   0: 0x0000000080000008 (0x40152083) lw      ra, 1025(a0)"
_SPIKE_DISASM = re.compile(r"^core\s+\d+:\s+0x([0-9a-fA-F]+)\s+\(0x([0-9a-fA-F]+)\)")

# Spike: "core   0: 3 0x0000000080000000 (0x800000b7) x1  0xffffffff80000000"
#
# ⛔ THE PRIVILEGE DIGIT IS REQUIRED, and that is what distinguishes the two log formats Spike
# emits. `--log-commits` gives the committed state change (with the digit); `-l` gives a
# disassembly line (without it). Neither alone is enough for this comparison — `-l` carries the
# exceptions and no register writes, `--log-commits` the reverse — so the documented invocation
# enables BOTH, and the two formats then interleave. Matching the disasm form as well would
# double every step. Required invocation:
#     spike --isa=rv64i --priv=m -l --log-commits --log=<file> --instructions=<n> <elf>
_SPIKE = re.compile(
    r"^core\s+\d+:\s+\d+\s+0x([0-9a-fA-F]+)\s+\(0x([0-9a-fA-F]+)\)"
    r"(?:\s+(x\d{1,2})\s+0x([0-9a-fA-F]+))?"
)


def parse_sail(text: str) -> list[Step]:
    steps: list[Step] = []
    for line in text.splitlines():
        m = _SAIL_STEP.match(line.strip())
        if m:
            steps.append(Step(int(m.group(1), 16), int(m.group(2), 16)))
            continue
        m = _SAIL_WRITE.match(line.strip())
        if m and steps:
            steps[-1].writes.append((m.group(1), int(m.group(2), 16)))
            continue
        m = _SAIL_TRAP.match(line.strip())
        if m and steps and steps[-1].trap is None:
            steps[-1].trap = (trap_cause(m.group(1), "sail"), int(m.group(2), 16))
    return steps


def parse_spike(text: str) -> list[Step]:
    """Parse Spike's interleaved `-l` + `--log-commits` output in one ordered pass.

    ⛔ SPIKE EMITS NO COMMIT RECORD FOR A TRAPPING INSTRUCTION. It prints the disassembly line,
    then the exception — and nothing else, because nothing committed. The Sail model, by
    contrast, records the trapping instruction as a step carrying the trap. The *observation* is
    the same in both ("the instruction at this pc attempted, and raised this cause with this
    tval"); only the record shape differs, so the adapter synthesizes the missing step from the
    disassembly line that immediately preceded the exception.

    This is a normalization, and per `EVD-05` it is justified rather than convenient: the pc and
    the encoded word come from Spike's own disassembly line for that instruction, the cause from
    the pinned causes table, and the tval from Spike's own report. Nothing is invented; a record
    Spike splits across two lines is reassembled into the one step both models describe.
    """
    steps: list[Step] = []
    attempted: tuple[int, int] | None = None      # (pc, word) from the most recent -l line
    for raw in text.splitlines():
        line = raw.strip()

        m = _SPIKE.match(line)                    # commit form (has the privilege digit)
        if m:
            step = Step(int(m.group(1), 16), int(m.group(2), 16))
            if m.group(3):
                step.writes.append((m.group(3), int(m.group(4), 16)))
            steps.append(step)
            continue

        m = _SPIKE_DISASM.match(line)             # -l form (no privilege digit)
        if m:
            attempted = (int(m.group(1), 16), int(m.group(2), 16))
            continue

        m = _SPIKE_TRAP.match(line)
        if m:
            cause, epc = trap_cause(m.group(1), "spike"), int(m.group(2), 16)
            if steps and steps[-1].pc == epc and steps[-1].trap is None:
                steps[-1].trap = (cause, 0)
            elif attempted is not None and attempted[0] == epc:
                steps.append(Step(epc, attempted[1], trap=(cause, 0)))
            else:
                raise CompareError(
                    f"spike: exception at epc {epc:#x} with no preceding record of that "
                    f"instruction. Enable both `-l` and `--log-commits`, or the trapping "
                    f"instruction is invisible to this comparison.")
            continue

        m = _SPIKE_TVAL.match(line)
        if m and steps and steps[-1].trap is not None:
            steps[-1].trap = (steps[-1].trap[0], int(m.group(1), 16))
    return steps


def align(steps: list[Step], entry: int, who: str) -> list[Step]:
    for i, s in enumerate(steps):
        if s.pc == entry:
            return steps[i:]
    raise CompareError(
        f"{who}: no step reaches the declared entry {entry:#x} in {len(steps)} step(s). "
        f"An unparseable or truncated trace must not be read as agreement.")


def compare(a: list[Step], b: list[Step], names: tuple[str, str]) -> tuple[bool, str]:
    """Return (agreed, report): the first differing step, or a length mismatch, or agreement.

    ⛔ A SHORTER TRACE IS NOT AGREEMENT, and this rule exists because the first cut of this
    function got it wrong on its first real input. Comparing only the overlapping prefix, it
    printed `AGREE over 2 aligned step(s)` for the misaligned-load experiment — in which one
    model raised `misaligned-load` and the other simply stopped producing commit records. The
    prefixes did agree; the observation did not, and the verdict was green.

    A length mismatch may be innocent — the two harnesses take their instruction bounds from
    different flags — but innocence is for the operator to establish, not for the comparator to
    assume. It is reported as a non-agreeing verdict that has to be explained.
    """
    if not a or not b:
        raise CompareError(f"{names[0]} has {len(a)} step(s), {names[1]} has {len(b)} — "
                           f"an empty trace is not a match")
    n = min(len(a), len(b))
    for i in range(n):
        if a[i].key() != b[i].key():
            return False, (
                f"FIRST DIVERGENCE at aligned step {i}\n"
                f"  {names[0]:12} pc={a[i].pc:#018x} insn={a[i].word:#010x} writes={a[i].writes}\n"
                f"  {names[1]:12} pc={b[i].pc:#018x} insn={b[i].word:#010x} writes={b[i].writes}")
    if len(a) != len(b):
        longer, shorter = (names[0], names[1]) if len(a) > len(b) else (names[1], names[0])
        nxt = (a if len(a) > len(b) else b)[n]
        return False, (
            f"LENGTH MISMATCH after {n} agreeing step(s): "
            f"{names[0]} produced {len(a)}, {names[1]} produced {len(b)}\n"
            f"  {longer} continues at pc={nxt.pc:#018x} insn={nxt.word:#010x}; "
            f"{shorter} stopped.\n"
            f"  The agreeing prefix is NOT a pass. Explain why one model stopped — a trap the "
            f"other reported differently, a harness instruction bound, or a genuine divergence "
            f"in control flow — before recording this run as evidence.")
    return True, (f"AGREE over {n} aligned step(s) "
                  f"({names[0]}: {len(a)} parsed, {names[1]}: {len(b)} parsed)")


SAIL_FIXTURE = """[0] [M]: 0x0000000080000000 (0x00100513) addi x10, x0, 0x1
x10 <- 0x0000000000000001
[1] [M]: 0x0000000080000004 (0x40152083) lw x1, 0x401(x10)
trapping from M to M to handle misaligned-load
handling exc#misaligned-load at priv M | tval=0x0000000080000401 | tval2=0x0 | tinst=0x0
"""

SPIKE_FIXTURE = """core   0: 0x0000000080000000 (0x00100513) li      a0, 1
core   0: 3 0x0000000080000000 (0x00100513) x10 0x0000000000000001
core   0: 0x0000000080000004 (0x40152083) lw      ra, 1025(a0)
core   0: exception trap_load_address_misaligned, epc 0x0000000080000004
core   0:           tval 0x0000000080000401
"""


def self_test() -> int:
    """RED/GREEN controls. A comparator that has only ever said AGREE is not known to disagree."""
    entry = 0x80000000
    npass = nfail = 0

    def arm(name: str, sail_text: str, spike_text: str, want_ok: bool, want_sub: str) -> None:
        nonlocal npass, nfail
        try:
            a = align(parse_sail(sail_text), entry, "sail")
            b = align(parse_spike(spike_text), entry, "spike")
            ok, report = compare(a, b, ("sail-riscv", "spike"))
        except CompareError as exc:
            ok, report = False, f"REFUSED {exc}"
        if ok != want_ok:
            nfail += 1
            print(f"compare_traces self-test MISS: {name} expected ok={want_ok} got {ok}\n{report}",
                  file=sys.stderr)
        elif want_sub not in report:
            nfail += 1
            print(f"compare_traces self-test MISS: {name} right verdict, wrong reason "
                  f"(no {want_sub!r})\n{report}", file=sys.stderr)
        else:
            npass += 1

    arm("GREEN identical observations, including the trap",
        SAIL_FIXTURE, SPIKE_FIXTURE, True, "AGREE over 2")
    arm("RED   a register value differs",
        SAIL_FIXTURE.replace("x10 <- 0x0000000000000001", "x10 <- 0x0000000000000002"),
        SPIKE_FIXTURE, False, "FIRST DIVERGENCE at aligned step 0")
    arm("RED   the trap CAUSE differs",
        SAIL_FIXTURE.replace("exc#misaligned-load", "exc#misaligned-store"),
        SPIKE_FIXTURE, False, "FIRST DIVERGENCE at aligned step 1")
    arm("RED   the trap TVAL differs",
        SAIL_FIXTURE.replace("tval=0x0000000080000401", "tval=0x00000000DEADBEEF"),
        SPIKE_FIXTURE, False, "FIRST DIVERGENCE at aligned step 1")
    arm("RED   one model stops early — a shorter trace is not agreement",
        SAIL_FIXTURE, "\n".join(SPIKE_FIXTURE.splitlines()[:2]) + "\n",
        False, "LENGTH MISMATCH")
    arm("REFUSE an exception spelling the adapter does not know",
        SAIL_FIXTURE.replace("exc#misaligned-load", "exc#brand-new-fault"),
        SPIKE_FIXTURE, False, "unknown exception spelling")
    arm("REFUSE a trace that never reaches the entry",
        SAIL_FIXTURE.replace("0x0000000080000000", "0x00000000900000AA"),
        SPIKE_FIXTURE, False, "no step reaches the declared entry")
    arm("REFUSE spike reporting an exception with no record of the instruction",
        SAIL_FIXTURE,
        "core   0: 3 0x0000000080000000 (0x00100513) x10 0x0000000000000001\n"
        "core   0: exception trap_load_address_misaligned, epc 0x00000000800000FF\n",
        False, "no preceding record of that instruction")

    print(f"compare_traces --self-test: {npass} pass / {nfail} fail")
    return 0 if nfail == 0 else 1


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] == "--self-test":
        return self_test()
    if len(argv) != 4:
        print("usage: compare_traces.py <sail-trace> <spike-log> <entry-hex>", file=sys.stderr)
        print("       compare_traces.py --self-test", file=sys.stderr)
        return 2
    entry = int(argv[3], 0)
    sail = align(parse_sail(Path(argv[1]).read_text()), entry, "sail")
    spike = align(parse_spike(Path(argv[2]).read_text()), entry, "spike")
    agreed, report = compare(sail, spike, ("sail-riscv", "spike"))
    print(report)
    return 0 if agreed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
