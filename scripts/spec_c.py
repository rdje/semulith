"""Spec-side RV64C expansion, hand-authored from RVI-C 27.1 (v20260120).

The three instruction-listing diagrams supply the bit positions; the prose supplies
the expansions and reserved operands. This module reads no definition/assembler/engine
tables. It selects RV64 with D: quadrant-0/2 funct3=3/7 are LD/SD, not RV32 FLW/FSW.
HINTs execute their harmless base operations under this laboratory's declared policy.
Shared specification ancestry remains; these finite rules are not a conformance oracle.
"""
from dataclasses import dataclass


class Reserved(Exception):
    """A complete 16-bit parcel is reserved in the selected RV64C set."""


@dataclass(frozen=True)
class Expansion:
    name: str
    word: int
    source: str


def signed(value, width):
    sign = 1 << (width - 1)
    return (value ^ sign) - sign


def i_word(op, rd, rs1, imm, f3=0):
    return ((imm & 0xfff) << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op


def r_word(op, rd, rs1, rs2, f3=0, f7=0):
    return (f7 << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op


def s_word(op, rs1, rs2, imm, f3):
    return (((imm >> 5) & 0x7f) << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | ((imm & 31) << 7) | op


def decode(parcel: int) -> Expansion:
    """Expand one complete compressed parcel, or name its reserved condition.

    A wider-instruction prefix is a caller error: it needs more fetch evidence and
    must never be judged as a reserved compressed instruction.
    """
    if not isinstance(parcel, int) or not 0 <= parcel <= 0xffff or parcel & 3 == 3:
        raise ValueError('decode requires one complete 16-bit compressed parcel')
    c = parcel
    q, f3 = c & 3, c >> 13
    rd, rs2 = (c >> 7) & 31, (c >> 2) & 31
    rp, sp = 8 + ((c >> 7) & 7), 8 + ((c >> 2) & 7)
    ci = signed(((c >> 12) & 1) << 5 | ((c >> 2) & 31), 6)

    def result(name, word, section):
        return Expansion(name, word, 'RVI-C §27.1.' + section)

    if q == 0:
        if f3 == 0:
            imm = (((c >> 7) & 15) << 6 | ((c >> 11) & 3) << 4
                   | ((c >> 5) & 1) << 3 | ((c >> 6) & 1) << 2)
            if imm == 0:
                raise Reserved('C.ADDI4SPN has zero immediate')
            return result('c.addi4spn', i_word(0x13, sp, 2, imm), '5.2')
        if f3 == 4:
            raise Reserved('quadrant 0 funct3=4')
        imm = ((c >> 10) & 7) << 3
        if f3 in (2, 6):
            imm |= ((c >> 6) & 1) << 2 | ((c >> 5) & 1) << 6
        else:
            imm |= ((c >> 5) & 3) << 6
        if f3 in (1, 2, 3):
            name, op, width = {1: ('c.fld', 0x07, 3), 2: ('c.lw', 0x03, 2),
                               3: ('c.ld', 0x03, 3)}[f3]
            return result(name, i_word(op, sp, rp, imm, width), '3.2')
        name, op, width = {5: ('c.fsd', 0x27, 3), 6: ('c.sw', 0x23, 2),
                           7: ('c.sd', 0x23, 3)}[f3]
        return result(name, s_word(op, rp, sp, imm, width), '3.2')
    if q == 1:
        if f3 == 0:
            return result('c.addi' if rd else 'c.nop', i_word(0x13, rd, rd, ci), '5.2')
        if f3 == 1:
            if rd == 0:
                raise Reserved('C.ADDIW has rd=x0')
            return result('c.addiw', i_word(0x1b, rd, rd, ci), '5.2')
        if f3 == 2:
            return result('c.li', i_word(0x13, rd, 0, ci), '5.1')
        if f3 == 3:
            if ci == 0:
                raise Reserved('C.LUI/C.ADDI16SP has zero immediate')
            if rd == 2:
                imm = signed(((c >> 12) & 1) << 9 | ((c >> 6) & 1) << 4
                             | ((c >> 5) & 1) << 6 | ((c >> 3) & 3) << 7
                             | ((c >> 2) & 1) << 5, 10)
                return result('c.addi16sp', i_word(0x13, 2, 2, imm), '5.2')
            return result('c.lui', ((ci << 12) & 0xfffff000) | (rd << 7) | 0x37, '5.1')
        if f3 == 4:
            group = (c >> 10) & 3
            if group < 2:
                shamt = ((c >> 12) & 1) << 5 | ((c >> 2) & 31)
                return result(('c.srli', 'c.srai')[group],
                              i_word(0x13, rp, rp, shamt | (group << 10), 5), '5.2')
            if group == 2:
                return result('c.andi', i_word(0x13, rp, rp, ci, 7), '5.2')
            kind = (c >> 5) & 3
            if (c >> 12) & 1:
                if kind >= 2:
                    raise Reserved('quadrant 1 reserved word arithmetic')
                return result(('c.subw', 'c.addw')[kind],
                              r_word(0x3b, rp, rp, sp, f7=0x20 if kind == 0 else 0), '5.3')
            return result(('c.sub', 'c.xor', 'c.or', 'c.and')[kind],
                          r_word(0x33, rp, rp, sp, (0, 4, 6, 7)[kind],
                                 0x20 if kind == 0 else 0), '5.3')
        if f3 == 5:
            imm = signed(((c >> 12) & 1) << 11 | ((c >> 11) & 1) << 4
                         | ((c >> 9) & 3) << 8 | ((c >> 8) & 1) << 10
                         | ((c >> 7) & 1) << 6 | ((c >> 6) & 1) << 7
                         | ((c >> 3) & 7) << 1 | ((c >> 2) & 1) << 5, 12)
            word = (((imm >> 20) & 1) << 31 | ((imm >> 1) & 0x3ff) << 21
                    | ((imm >> 11) & 1) << 20 | ((imm >> 12) & 0xff) << 12 | 0x6f)
            return result('c.j', word, '4')
        imm = signed(((c >> 12) & 1) << 8 | ((c >> 10) & 3) << 3
                     | ((c >> 5) & 3) << 6 | ((c >> 3) & 3) << 1
                     | ((c >> 2) & 1) << 5, 9)
        word = (((imm >> 12) & 1) << 31 | ((imm >> 5) & 63) << 25
                | (rp << 15) | ((f3 - 6) << 12) | ((imm >> 1) & 15) << 8
                | ((imm >> 11) & 1) << 7 | 0x63)
        return result('c.beqz' if f3 == 6 else 'c.bnez', word, '4')
    if f3 == 0:
        shamt = ((c >> 12) & 1) << 5 | ((c >> 2) & 31)
        return result('c.slli', i_word(0x13, rd, rd, shamt, 1), '5.2')
    if f3 in (1, 2, 3):
        if f3 != 1 and rd == 0:
            raise Reserved('C.LWSP/C.LDSP has rd=x0')
        imm = ((c >> 12) & 1) << 5
        if f3 == 2:
            imm |= ((c >> 4) & 7) << 2 | ((c >> 2) & 3) << 6
        else:
            imm |= ((c >> 5) & 3) << 3 | ((c >> 2) & 7) << 6
        name, op, width = {1: ('c.fldsp', 0x07, 3), 2: ('c.lwsp', 0x03, 2),
                           3: ('c.ldsp', 0x03, 3)}[f3]
        return result(name, i_word(op, rd, 2, imm, width), '3.1')
    if f3 == 4:
        if rs2:
            add = (c >> 12) & 1
            return result('c.add' if add else 'c.mv',
                          r_word(0x33, rd, rd if add else 0, rs2), '5.3')
        if (c >> 12) & 1:
            if rd == 0:
                return result('c.ebreak', 0x00100073, '5.6')
            return result('c.jalr', i_word(0x67, 1, rd, 0), '4')
        if rd == 0:
            raise Reserved('C.JR has rs1=x0')
        return result('c.jr', i_word(0x67, 0, rd, 0), '4')
    if f3 == 6:
        imm = ((c >> 9) & 15) << 2 | ((c >> 7) & 3) << 6
    else:
        imm = ((c >> 10) & 7) << 3 | ((c >> 7) & 7) << 6
    name, op, width = {5: ('c.fsdsp', 0x27, 3), 6: ('c.swsp', 0x23, 2),
                       7: ('c.sdsp', 0x23, 3)}[f3]
    return result(name, s_word(op, 2, rs2, imm, width), '3.1')
