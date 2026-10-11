#!/usr/bin/env python3
"""Source-byte construction controls; no authentication, execution or qualification."""
from __future__ import annotations

import argparse
from dataclasses import FrozenInstanceError, fields
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock

import matched_gpr_image as I
import probe_elf_writer as P
import riscv_asm as A

SOURCE = b"addi x1, x0, 5\nc.addi x1, 1\n"
PAYLOAD = b"\x93\0\x50\0\x85\0"
ENTRY = 0x80000002


class String(str):
    pass


class ImageTests(unittest.TestCase):
    def build(self, source=SOURCE, program="example.s", entry=ENTRY):
        return I.build_guest_image(source, program=program, entry=entry)

    def rejected(self, kind, reason, **kwargs):
        try:
            self.build(**kwargs)
        except Exception as exc:
            self.assertIsInstance(exc, kind)
            self.assertIn(reason, str(exc))
            self.assertLess(len(str(exc)), 128)
        else:
            self.fail("invalid construction was accepted")

    def preflight_refusal(self, reason, **kwargs):
        with mock.patch.object(I.Path, "is_file") as stat, mock.patch.object(I.A, "Assembler") as factory:
            self.rejected(I.ImageError, reason, **kwargs)
        stat.assert_not_called()
        factory.assert_not_called()

    def context(self, payload=PAYLOAD, ialign=16):
        return types.SimpleNamespace(ialign=ialign, assemble_image=mock.Mock(return_value=payload))

    def test_exact_hand_payload_and_halfword_load_address(self):
        result = self.build()
        header, segment, sections = P.decode(result.image)
        self.assertEqual(header[4], ENTRY)
        self.assertEqual(header[7], 1)
        self.assertEqual(segment[3:5], (ENTRY, ENTRY))
        self.assertEqual(result.image[segment[2]:segment[2] + segment[5]], PAYLOAD)
        self.assertEqual(sections[1][8], 2)

    def test_exact_frozen_metadata_fingerprints(self):
        result = self.build()
        self.assertEqual((result.program, result.encoding_path, result.entry, result.ialign),
                         ("example.s", "profiles/rv64gc-lab-v0/encoding.sexp", ENTRY, 16))
        self.assertEqual((result.source_size, result.payload_size, result.image_size), (28, 6, 4320))
        self.assertEqual(result.source_sha256, hashlib.sha256(SOURCE).hexdigest())
        self.assertEqual(result.payload_sha256, hashlib.sha256(PAYLOAD).hexdigest())
        self.assertEqual(result.image_sha256, "db3eac98c94c4e0f0f2e7e46d01948717b5ae641a8532e3a074843b46fc91fc8")
        with self.assertRaises(FrozenInstanceError):
            result.entry = 0
        self.assertIs(type(result.image), bytes)
        self.assertNotIn("source", {field.name for field in fields(result)})
        self.assertFalse(hasattr(result, "qualified"))

    def test_unicode_source_and_exact_program_label(self):
        source = "c.nop # 雪\n".encode()
        result = self.build(source, program="dir/雪.s")
        self.assertEqual(result.program, "dir/雪.s")
        self.assertEqual(result.source_size, len(source))
        self.assertEqual(result.source_sha256, hashlib.sha256(source).hexdigest())
        self.assertEqual(result.payload_sha256, hashlib.sha256(b"\x01\0").hexdigest())

    def test_inclusive_source_byte_limit(self):
        source = b"#" + b"x" * (1024 * 1024 - 1)
        result = self.build(source)
        self.assertEqual(result.source_size, 1024 * 1024)
        self.assertEqual(result.payload_size, 0)

    def test_oversized_source_before_tool_io(self):
        self.preflight_refusal("1..1048576", source=b"#" + b"x" * (1024 * 1024))

    def test_empty_source_before_tool_io(self):
        self.preflight_refusal("1..1048576", source=b"")

    def test_nonimmutable_source_types_before_tool_io(self):
        for source in (None, SOURCE.decode(), bytearray(SOURCE), memoryview(SOURCE), 1):
            with self.subTest(source=type(source).__name__):
                self.preflight_refusal("immutable bytes", source=source)

    def test_program_types_and_empty_before_tool_io(self):
        for program in ("", None, 1, b"example.s", String("example.s")):
            with self.subTest(program=repr(program)):
                self.preflight_refusal("plain string", program=program)

    def test_program_bound_before_tool_io(self):
        self.preflight_refusal("1..65536", program="x" * 65537)

    def test_inclusive_program_limit(self):
        result = self.build(program="x" * 65536)
        self.assertEqual(result.program, "x" * 65536)

    def test_entry_type_and_unsigned_bounds_before_tool_io(self):
        for entry in (True, None, 2.0, "2", -2, 1 << 64):
            with self.subTest(entry=entry):
                self.preflight_refusal("unsigned 64-bit", entry=entry)

    def test_odd_entry_refuses_without_image(self):
        self.rejected(I.ImageError, "construction refuses", entry=ENTRY + 1)

    def test_load_extent_overflow_refuses_without_image(self):
        self.rejected(I.ImageError, "construction refuses", entry=(1 << 64) - 2)

    def test_inclusive_address_space_end(self):
        result = self.build(b"c.nop", entry=(1 << 64) - 2)
        _, segment, _ = P.decode(result.image)
        self.assertEqual(segment[3] + segment[6], 1 << 64)

    def test_malformed_utf8_before_tool_io(self):
        self.preflight_refusal("UTF-8", source=b"#\xff")

    def test_every_splitlines_separator_matches_legacy(self):
        for sep in ("\n", "\r", "\r\n", "\v", "\f", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029"):
            for tail in ("", sep):
                with self.subTest(sep=repr(sep), tail=bool(tail)):
                    text = "c.nop" + sep + "# note" + sep + "c.nop" + tail
                    context = self.context()
                    with mock.patch.object(I.A, "Assembler", return_value=context):
                        self.build(text.encode())
                    context.assemble_image.assert_called_once_with(text.splitlines(), base=ENTRY)

    def test_inclusive_line_and_payload_limits(self):
        result = self.build(b".word 0\n" * 8192)
        self.assertEqual(result.payload_size, 32768)
        self.assertLessEqual(result.image_size, 65536)

    def test_excess_terminated_lines_before_tool_io(self):
        self.preflight_refusal("8192 splitlines", source=b"#\n" * 8193)

    def test_excess_unterminated_final_line_before_tool_io(self):
        self.preflight_refusal("8192 splitlines", source=b"#\n" * 8192 + b"#")

    def test_unicode_excess_lines_before_tool_io(self):
        for sep in ("\r\n", "\v", "\x1e", "\x85", "\u2028", "\u2029"):
            with self.subTest(sep=repr(sep)):
                self.preflight_refusal("8192 splitlines", source=("#" + sep).encode() * 8193)

    def test_no_path_write_source_reopen_or_process(self):
        original_open = Path.open
        def guarded_open(path, mode="r", *args, **kwargs):
            if path.name == "never-open.s":
                raise AssertionError("source path reopened")
            if any(flag in mode for flag in "wa+"):
                raise AssertionError("path write")
            return original_open(path, mode, *args, **kwargs)
        with mock.patch.object(Path, "open", new=guarded_open), \
             mock.patch.object(Path, "write_bytes", side_effect=AssertionError("path write")), \
             mock.patch.object(Path, "write_text", side_effect=AssertionError("path write")), \
             mock.patch.object(subprocess, "Popen", side_effect=AssertionError("process")):
            result = self.build(program="missing-source/never-open.s")
        self.assertEqual(result.program, "missing-source/never-open.s")

    def test_missing_directory_and_symlink_contexts_do_not_select_tables(self):
        parent = I.ROOT / "target/p4-system-14/a42c/context-fixtures"
        parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=parent) as scratch:
            root = Path(scratch)
            encoding = root / I.ENCODING_PATH
            encoding.parent.mkdir(parents=True)
            for state in ("missing", "directory", "symlink"):
                with self.subTest(state=state):
                    if state == "directory":
                        encoding.mkdir()
                    if state == "symlink":
                        encoding.rmdir()
                        other = encoding.parent / "other.sexp"
                        other.write_text("synthetic")
                        encoding.symlink_to(other.name)
                    with mock.patch.object(I, "ROOT", root), mock.patch.object(I.A, "Assembler") as factory:
                        self.rejected(I.ImageUnavailable, "existing regular file")
                    factory.assert_not_called()

    def test_context_errors_are_unavailable_with_bounded_diagnostics(self):
        for error in (OSError, I.A.AsmError, I.D.DossierError, I.S.SexpError,
                      ValueError, TypeError, KeyError, IndexError, RecursionError):
            with self.subTest(error=error.__name__), mock.patch.object(I.A, "Assembler", side_effect=error("secret" * 10000)):
                self.rejected(I.ImageUnavailable, "context is unavailable or invalid")

    def test_context_requires_plain_ialign16(self):
        for ialign in (32, 16.0, None, True):
            with self.subTest(ialign=ialign), mock.patch.object(I.A, "Assembler", return_value=self.context(ialign=ialign)):
                self.rejected(I.ImageUnavailable, "declare IALIGN16")

    def test_assembly_refusal_never_echoes_raw_source(self):
        self.rejected(I.ImageError, "construction refuses", source=b"secret" * 10000)

    def test_payload_limit_precedes_elf_encoding(self):
        with mock.patch.object(I.A, "Assembler", return_value=self.context(b"x" * 32769)), \
             mock.patch.object(I.A, "encode_elf64") as encode:
            self.rejected(I.ImageError, "payload exceeds 32768")
        encode.assert_not_called()

    def test_image_limit_refuses_without_result(self):
        with mock.patch.object(I.A, "encode_elf64", return_value=b"x" * 65537):
            self.rejected(I.ImageError, "image exceeds 65536")

    def test_mutable_payload_refuses_before_encoding(self):
        with mock.patch.object(I.A, "Assembler", return_value=self.context(bytearray(PAYLOAD))), \
             mock.patch.object(I.A, "encode_elf64") as encode:
            self.rejected(I.ImageError, "immutable payload bytes")
        encode.assert_not_called()

    def test_mutable_image_refuses_without_result(self):
        with mock.patch.object(I.A, "encode_elf64", return_value=bytearray(b"image")):
            self.rejected(I.ImageError, "immutable image bytes")

    def test_sole_encoder_receives_exact_payload_entry_and_profile(self):
        encode = I.A.encode_elf64
        with mock.patch.object(I.A, "encode_elf64", wraps=encode) as called:
            self.build()
        called.assert_called_once_with(ENTRY, PAYLOAD, 16)

    def test_legacy_writer_delegates_once_and_returns_none(self):
        encode = A.encode_elf64
        output = P.Capture()
        with mock.patch.object(A, "encode_elf64", wraps=encode) as called:
            self.assertIsNone(A.write_elf64(output, ENTRY, PAYLOAD, 16))
        called.assert_called_once_with(ENTRY, PAYLOAD, 16)
        self.assertEqual(output.data, encode(ENTRY, PAYLOAD, 16))

    def test_pure_encoder_has_no_path_or_process_effect(self):
        with mock.patch.object(Path, "write_bytes", side_effect=AssertionError("path write")), \
             mock.patch.object(subprocess, "Popen", side_effect=AssertionError("process")):
            data = A.encode_elf64(ENTRY, PAYLOAD, 16)
        header, segment, _ = P.decode(data)
        self.assertEqual(header[4], ENTRY)
        self.assertEqual(data[segment[2]:segment[2] + segment[5]], PAYLOAD)

    def test_legacy_validation_precedes_output_method_lookup(self):
        class Output:
            lookups = 0
            @property
            def write_bytes(self):
                self.lookups += 1
                raise OSError("output method lookup")
        output = Output()
        try:
            A.write_elf64(output, 1, b"\x01\0", 16)
        except Exception as exc:
            self.assertIsInstance(exc, A.AsmError)
        else:
            self.fail("invalid entry was accepted")
        self.assertEqual(output.lookups, 0)


MUTATIONS = {
    "source-type": ("image", "if type(source) is not bytes or not 1 <= len(source) <= SOURCE_BYTES:", "if False:"),
    "source-bound": ("image", "SOURCE_BYTES = 1024 * 1024", "SOURCE_BYTES = 2 * 1024 * 1024"),
    "program-guard": ("image", "if type(program) is not str or not 1 <= len(program) <= 65536:", "if False:"),
    "entry-guard": ("image", "if type(entry) is not int or not 0 <= entry < 1 << 64:", "if False:"),
    "utf8": ("image", 'source.decode("utf-8")', 'source.decode("utf-8", errors="replace")'),
    "line-preflight": ("image", "lines = _source_lines(text)", "lines = text.splitlines()"),
    "final-line": ("image", "if end < len(text):", "if False:"),
    "canonical-route": ("image", "if not encoding.is_file() or encoding.resolve() != encoding:", "if False:"),
    "ialign-context": ("image", "if type(assembler.ialign) is not int or assembler.ialign != 16:", "if False:"),
    "payload-bound": ("image", "if len(payload) > PAYLOAD_BYTES:", "if False:"),
    "image-bound": ("image", "if len(image) > IMAGE_BYTES:", "if False:"),
    "payload-type": ("image", "if type(payload) is not bytes:", "if False:"),
    "image-type": ("image", "if type(image) is not bytes:", "if False:"),
    "source-fingerprint": ("image", "hashlib.sha256(source).hexdigest()", "hashlib.sha256(payload).hexdigest()"),
    "entry-forward": ("image", "A.encode_elf64(entry, payload, assembler.ialign)", "A.encode_elf64(0x80000000, payload, assembler.ialign)"),
    "writer-delegation": ("assembler", "path.write_bytes(image)", 'path.write_bytes(b"bypass")'),
    "writer-order": ("assembler", "    image = encode_elf64(entry, payload, ialign)\n    path.write_bytes(image)\n", "    path.write_bytes(encode_elf64(entry, payload, ialign))\n"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        global I, A
        owner, before, after = MUTATIONS[args.mutation]
        original = I if owner == "image" else A
        source = Path(original.__file__).read_text()
        if source.count(before) != 1:
            raise SystemExit("mutation seam is not singular")
        module = types.ModuleType("mutated_source_" + owner)
        module.__file__ = original.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after, 1), original.__file__, "exec"), module.__dict__)
        if owner == "image":
            I = module
        else:
            A = module
            I.A = A
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(ImageTests))
    print(f"MATCHED-GPR-IMAGE: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; construction only")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
