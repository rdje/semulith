#!/usr/bin/env python3
"""Independent ELF64 header/layout controls; no reference or CPU qualification."""
from __future__ import annotations

import argparse
from pathlib import Path
import struct
import sys
import tempfile
import types
import unittest

import riscv_asm as A

ROOT = Path(__file__).resolve().parent.parent


class Capture:
    def __init__(self):
        self.data = None
        self.writes = 0

    def write_bytes(self, data):
        self.data = bytes(data)
        self.writes += 1
        return len(data)


def decode(data):
    """Literal ELF64 layouts, independent of the writer's constants/calculations."""
    header = struct.unpack_from("<16sHHIQQQIHHHHHH", data)
    segment = struct.unpack_from("<IIQQQQQQ", data, header[5])
    sections = tuple(struct.unpack_from("<IIQQQQIIQQ", data, header[6] + n * 64)
                     for n in range(3))
    return header, segment, sections


class ElfTests(unittest.TestCase):
    def image(self, entry=0x80000000, payload=b"\x13\0\0\0", ialign=32):
        output = Capture()
        self.assertIsNone(A.write_elf64(output, entry, payload, ialign))
        self.assertEqual(output.writes, 1)
        return output.data

    def refused(self, entry, payload, ialign, reason):
        output = Capture()
        try:
            A.write_elf64(output, entry, payload, ialign)
        except Exception as exc:
            self.assertIsInstance(exc, A.AsmError)
            self.assertIn(reason, str(exc))
        else:
            self.fail("invalid ELF input was accepted")
        self.assertEqual(output.writes, 0)

    def test_every_aligned_page_offset_is_congruent(self):
        for ialign in (16, 32):
            for offset in range(0, 4096, ialign // 8):
                entry = 0x80000000 + offset
                _, segment, _ = decode(self.image(entry, ialign=ialign))
                self.assertEqual(segment[2] % 4096, entry % 4096)
                self.assertGreaterEqual(segment[2], 120)
                self.assertLess(segment[2], 120 + 4096)

    def test_page_alignment_declaration_is_preserved(self):
        for entry in (0, 120, 4094, 0x80000002):
            _, segment, _ = decode(self.image(entry, ialign=16))
            self.assertEqual(segment[7], 4096)

    def test_section_table_is_naturally_aligned(self):
        for entry in (0x80000000, 0x80000002, 0x80000ffe):
            for length in (*range(32), 4095, 4096, 4097):
                header, _, _ = decode(self.image(entry, bytes(length), 16))
                self.assertEqual(header[5] % 8, 0)
                self.assertEqual(header[6] % 8, 0)

    def test_text_alignment_matches_profile_and_address(self):
        for entry, ialign, alignment in ((0x80000000, 32, 4), (0x80000000, 16, 2),
                                         (0x80000002, 16, 2)):
            _, _, sections = decode(self.image(entry, ialign=ialign))
            self.assertEqual(sections[1][8], alignment)
            self.assertEqual(sections[1][3] % alignment, 0)
            self.assertEqual(sections[1][4] % alignment, 0)

    def test_rvc_flag_for_halfword_instruction_alignment(self):
        for entry in (0, 0x80000000, 0x80000002):
            header, _, _ = decode(self.image(entry, ialign=16))
            self.assertEqual(header[7], 1)

    def test_base_flags_keep_soft_float_calling_convention(self):
        header, _, _ = decode(self.image())
        self.assertEqual(header[7], 0)

    def test_header_and_load_contract_fields(self):
        entry, payload = 0x80000002, b"\x01\0\x13\0\0\0"
        header, segment, sections = decode(self.image(entry, payload, 16))
        self.assertEqual(header[:5], (b"\x7fELF\x02\x01\x01" + bytes(9), 2, 243, 1, entry))
        self.assertEqual(header[5], 64)
        self.assertEqual(header[8:], (64, 56, 1, 64, 3, 2))
        self.assertEqual(segment[:2], (1, 7))
        self.assertEqual(segment[3:7], (entry, entry, len(payload), len(payload)))
        self.assertEqual(sections[0], (0,) * 10)
        self.assertEqual(sections[1][:4], (1, 1, 7, entry))
        self.assertEqual(sections[1][4:8], (segment[2], len(payload), 0, 0))
        self.assertEqual(sections[1][9], 0)
        self.assertEqual(sections[2][:4], (7, 3, 0, 0))
        self.assertEqual(sections[2][5:], (17, 0, 0, 1, 0))

    def test_payload_strings_and_padding_are_exact_and_disjoint(self):
        for entry in (0, 118, 120, 122, 4094, 4096, 0x80000002):
            for payload in (b"", b"\x01", b"\x01\0", bytes(range(256)) * 17):
                data = self.image(entry, payload, 16)
                header, segment, sections = decode(data)
                start, end = segment[2], segment[2] + segment[5]
                self.assertEqual(data[start:end], payload)
                self.assertEqual(sections[2][4], end)
                self.assertEqual(data[end:end + 17], b"\0.text\0.shstrtab\0")
                self.assertEqual(data[120:start], bytes(start - 120))
                self.assertEqual(data[end + 17:header[6]], bytes(header[6] - end - 17))
                self.assertLess(header[6] - end - 17, 8)
                self.assertEqual(len(data), header[6] + 192)

    def test_public_path_write_returns_none(self):
        parent = ROOT / "target/p4-system-14/a42b/probe"
        parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=parent) as scratch:
            path = Path(scratch) / "guest.elf"
            self.assertIsNone(A.write_elf64(path, 0x80000002, b"\x01\0", 16))
            self.assertEqual(path.read_bytes(), self.image(0x80000002, b"\x01\0", 16))

    def test_unknown_or_noninteger_ialign_refuses_before_write(self):
        for ialign in (0, 8, 24, 64, -16, True, 16.0, "16", None):
            with self.subTest(ialign=ialign):
                self.refused(0x80000000, b"", ialign, "IALIGN must be 16 or 32")

    def test_non_unsigned64_entry_refuses_before_write(self):
        for entry in (-4, 1 << 64, True, 4.0, "4", None):
            with self.subTest(entry=entry):
                self.refused(entry, b"", 32, "entry must be an unsigned 64-bit integer")

    def test_load_extent_overflow_refuses_before_write(self):
        self.refused((1 << 64) - 2, b"abc", 16, "load extent exceeds")
        self.refused((1 << 64) - 4, b"abcde", 32, "load extent exceeds")

    def test_inclusive_address_space_end_is_representable(self):
        for ialign, payload in ((16, b"ab"), (32, b"abcd")):
            entry = (1 << 64) - len(payload)
            _, segment, _ = decode(self.image(entry, payload, ialign))
            self.assertEqual(segment[3] + segment[6], 1 << 64)

    def test_misaligned_entry_refuses_before_write(self):
        for entry, ialign, reason in ((1, 16, "not 2-byte aligned"),
                                     (2, 32, "not 4-byte aligned"),
                                     (3, 32, "not 4-byte aligned")):
            self.refused(entry, b"", ialign, reason)

    def test_legacy_bytearray_payload_is_preserved(self):
        payload = bytearray(b"\x01\0\x13\0\0\0")
        data = self.image(payload=payload)
        _, segment, _ = decode(data)
        self.assertEqual(data[segment[2]:segment[2] + segment[5]], payload)
        self.assertEqual(payload, bytearray(b"\x01\0\x13\0\0\0"))


MUTATIONS = {
    "segment-offset": ("text_off = header_end + (entry - header_end) % ELF_PAGE_ALIGN", "text_off = header_end"),
    "page-declaration": ("ELF_PAGE_ALIGN = 4096", "ELF_PAGE_ALIGN = 1"),
    "section-table": ("shoff = (shstr_end + 7) & ~7", "shoff = shstr_end"),
    "text-alignment": ("entry, text_off, len(payload), ialign // 8)", "entry, text_off, len(payload), 4)"),
    "rvc-flag": ("EF_RISCV_RVC if ialign == 16 else 0", "0"),
    "ialign-guard": ("if type(ialign) is not int or ialign not in (16, 32):", "if False:"),
    "entry-guard": ("if type(entry) is not int or not 0 <= entry < 1 << 64:", "if False:"),
    "extent-guard": ("if len(payload) > (1 << 64) - entry:", "if False:"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        global A
        source = Path(A.__file__).read_text()
        before, after = MUTATIONS[args.mutation]
        if source.count(before) != 1:
            raise SystemExit("mutation seam is not singular")
        module = types.ModuleType("mutated_elf_writer")
        module.__file__ = A.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after, 1), A.__file__, "exec"), module.__dict__)
        A = module
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ElfTests)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"ELF-WRITER: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; no qualification")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
