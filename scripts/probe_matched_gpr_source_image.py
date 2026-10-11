#!/usr/bin/env python3
"""Complete source/image byte controls; no authentication or qualification."""
from __future__ import annotations

import argparse
from dataclasses import FrozenInstanceError, fields
import hashlib
from pathlib import Path
import subprocess
import sys
import types
import unittest
from unittest import mock

import matched_gpr_source_image as M
import probe_elf_writer as P

SOURCE = b"addi x1, x0, 5\nc.addi x1, 1\n"
PAYLOAD = b"\x93\0\x50\0\x85\0"
ENTRY = 0x80000002
IMAGE = M.G.A.encode_elf64(ENTRY, PAYLOAD, 16)


class Text(str):
    pass


class Bytes(bytes):
    pass


class SourceImageTests(unittest.TestCase):
    def check(self, source=SOURCE, image=IMAGE, *, program="example.s", entry=ENTRY):
        try:
            return M.check_source_image(source, image, program=program, entry=entry)
        except Exception as exc:
            self.fail(f"boundary escaped as {type(exc).__name__}")

    def outcome(self, disposition, reason=None, **kwargs):
        result = self.check(**kwargs)
        self.assertEqual(result.disposition, disposition)
        if reason:
            self.assertIn(reason, result.reason)
        self.assertLess(len(result.reason), 128)
        return result

    def test_hand_encoded_image_and_complete_exact_metadata(self):
        self.assertEqual(len(IMAGE), 4320)
        self.assertEqual(hashlib.sha256(IMAGE).hexdigest(),
                         "db3eac98c94c4e0f0f2e7e46d01948717b5ae641a8532e3a074843b46fc91fc8")
        result = self.outcome("matched", "no authentication or qualification")
        fact = result.facts
        self.assertEqual((fact.program, fact.entry, fact.encoding_path, fact.ialign),
                         ("example.s", ENTRY, "profiles/rv64gc-lab-v0/encoding.sexp", 16))
        self.assertEqual((fact.source_size, fact.payload_size, fact.rebuilt_image_size, fact.image_size),
                         (28, 6, 4320, 4320))
        self.assertEqual(fact.source_sha256, hashlib.sha256(SOURCE).hexdigest())
        self.assertEqual(fact.payload_sha256, hashlib.sha256(PAYLOAD).hexdigest())
        self.assertEqual(fact.rebuilt_image_sha256, hashlib.sha256(IMAGE).hexdigest())
        self.assertEqual(fact.image_sha256, hashlib.sha256(IMAGE).hexdigest())

    def test_result_is_frozen(self):
        result = self.outcome("matched")
        with self.assertRaises(FrozenInstanceError):
            result.disposition = "qualified"

    def test_facts_are_frozen(self):
        result = self.outcome("matched")
        with self.assertRaises(FrozenInstanceError):
            result.facts.entry = 0

    def test_results_retain_only_metadata(self):
        result = self.outcome("matched")
        self.assertFalse(hasattr(result, "qualified"))
        self.assertEqual(len(fields(result.facts)), 12)
        self.assertTrue(all(type(getattr(result.facts, f.name)) in (str, int) for f in fields(result.facts)))
        self.assertFalse(any(f.name in {"source", "image", "rebuilt_image"} for f in fields(result.facts)))

    def test_all_elf_regions_are_compared_not_just_loaded_payload(self):
        header, segment, sections = P.decode(IMAGE)
        offsets = {"magic": 0, "entry": 24, "RVC": 48, "file padding": 120,
                   "loaded payload": segment[2], "strings": sections[2][4],
                   "section header": header[6] + 64}
        for name, offset in offsets.items():
            with self.subTest(region=name):
                changed = bytearray(IMAGE); changed[offset] ^= 1
                result = self.outcome("refused", "ELF bytes differ", image=bytes(changed))
                self.assertIsNotNone(result.facts)

    def test_truncation_and_extra_bytes_refuse(self):
        for image in (IMAGE[:-1], IMAGE + b"x", b"x"):
            with self.subTest(size=len(image)):
                self.outcome("refused", "ELF bytes differ", image=image)

    def test_mismatch_keeps_exact_supplied_and_rebuilt_fingerprints(self):
        image = IMAGE + b"changed"
        result = self.outcome("refused", image=image)
        self.assertEqual(result.facts.image_size, len(image))
        self.assertEqual(result.facts.image_sha256, hashlib.sha256(image).hexdigest())
        self.assertEqual(result.facts.rebuilt_image_size, len(IMAGE))
        self.assertEqual(result.facts.rebuilt_image_sha256, hashlib.sha256(IMAGE).hexdigest())
        self.assertNotEqual(result.facts.image_sha256, result.facts.rebuilt_image_sha256)

    def test_changed_source_instruction_refuses(self):
        self.outcome("refused", "ELF bytes differ", source=SOURCE.replace(b"5", b"7"))

    def test_equivalent_comments_and_spacing_match_with_their_own_source_hash(self):
        source = b"# annotation\r\n  addi x1, x0, 5\r\nc.addi x1, 1 # tail\r\n"
        result = self.outcome("matched", source=source)
        self.assertEqual(result.facts.source_size, len(source))
        self.assertEqual(result.facts.source_sha256, hashlib.sha256(source).hexdigest())
        self.assertNotEqual(result.facts.source_sha256, hashlib.sha256(SOURCE).hexdigest())

    def test_program_is_exact_selected_label_not_an_embedded_filename(self):
        result = self.outcome("matched", program="missing/雪.s")
        self.assertEqual(result.facts.program, "missing/雪.s")
        self.assertEqual(result.facts.image_sha256, hashlib.sha256(IMAGE).hexdigest())

    def test_selected_entry_is_forwarded_and_changes_complete_image(self):
        result = self.outcome("refused", "ELF bytes differ", entry=0x80000000)
        self.assertEqual(result.facts.entry, 0x80000000)
        self.assertNotEqual(result.facts.rebuilt_image_sha256, hashlib.sha256(IMAGE).hexdigest())

    def test_image_type_and_empty_refuse_before_builder(self):
        for image in (None, "image", bytearray(IMAGE), memoryview(IMAGE), Bytes(IMAGE), b"", 1):
            with self.subTest(kind=type(image).__name__), \
                 mock.patch.object(M.G, "build_guest_image", side_effect=AssertionError("builder I/O")):
                result = self.outcome("refused", "plain bytes", image=image)
                self.assertIsNone(result.facts)

    def test_image_over_bound_refuses_before_builder(self):
        with mock.patch.object(M.G, "build_guest_image", side_effect=AssertionError("builder I/O")):
            self.assertIsNone(self.outcome("refused", "1..65536", image=b"x" * 65537).facts)

    def test_inclusive_image_bound_reaches_comparison(self):
        image = b"x" * 65536
        result = self.outcome("refused", "ELF bytes differ", image=image)
        self.assertEqual(result.facts.image_size, 65536)

    def test_bad_source_refuses_before_canonical_io(self):
        for source in (None, bytearray(SOURCE), Bytes(SOURCE), b"", b"x" * 1048577, b"#\xff", b"#\n" * 8193):
            with self.subTest(kind=type(source).__name__, size=len(source) if source is not None else None), \
                 mock.patch.object(M.G.Path, "is_file", side_effect=AssertionError("canonical I/O")):
                self.assertIsNone(self.outcome("refused", "source or selected image context", source=source).facts)

    def test_bad_program_refuses_before_canonical_io(self):
        for program in (None, "", b"example.s", Text("example.s"), "x" * 65537):
            with self.subTest(kind=type(program).__name__), \
                 mock.patch.object(M.G.Path, "is_file", side_effect=AssertionError("canonical I/O")):
                self.assertIsNone(self.outcome("refused", "source or selected image context", program=program).facts)

    def test_bad_entry_refuses_before_canonical_io(self):
        for entry in (None, True, 2.0, -2, 1 << 64):
            with self.subTest(entry=entry), \
                 mock.patch.object(M.G.Path, "is_file", side_effect=AssertionError("canonical I/O")):
                self.assertIsNone(self.outcome("refused", "source or selected image context", entry=entry).facts)

    def test_odd_and_overflowing_entry_refuse_without_facts(self):
        for entry in (1, (1 << 64) - 2):
            with self.subTest(entry=entry):
                self.assertIsNone(self.outcome("refused", "source or selected image context", entry=entry).facts)

    def test_canonical_unavailability_is_separate_and_diagnostics_bounded(self):
        with mock.patch.object(M.G, "build_guest_image", side_effect=M.G.ImageUnavailable("secret" * 10000)):
            result = self.outcome("unavailable", "canonical GC image construction is unavailable")
        self.assertIsNone(result.facts)
        self.assertNotIn("secret", result.reason)

    def test_source_refusal_has_fixed_diagnostics(self):
        with mock.patch.object(M.G, "build_guest_image", side_effect=M.G.ImageError("secret" * 10000)):
            result = self.outcome("refused", "source or selected image context refuses construction")
        self.assertIsNone(result.facts)
        self.assertNotIn("secret", result.reason)

    def test_other_programming_failures_do_not_become_results(self):
        with mock.patch.object(M.G, "build_guest_image", side_effect=RuntimeError("unexpected")), \
             self.assertRaisesRegex(RuntimeError, "unexpected"):
            M.check_source_image(SOURCE, IMAGE, program="example.s", entry=ENTRY)

    def test_sole_builder_receives_exact_source_and_context_once(self):
        with mock.patch.object(M.G, "build_guest_image", wraps=M.G.build_guest_image) as build:
            self.outcome("matched")
        build.assert_called_once_with(SOURCE, program="example.s", entry=ENTRY)

    def test_empty_payload_from_nonempty_comment_source_matches(self):
        image = M.G.A.encode_elf64(ENTRY, b"", 16)
        result = self.outcome("matched", source=b"# note\n", image=image)
        self.assertEqual(result.facts.payload_size, 0)

    def test_no_source_reopen_path_write_or_process(self):
        original_open = Path.open
        def guarded_open(path, mode="r", *args, **kwargs):
            if path.name == "never-open.s" or any(flag in mode for flag in "wa+"):
                raise AssertionError("source reopen/path write")
            return original_open(path, mode, *args, **kwargs)
        with mock.patch.object(Path, "open", new=guarded_open), \
             mock.patch.object(Path, "write_bytes", side_effect=AssertionError("path write")), \
             mock.patch.object(Path, "write_text", side_effect=AssertionError("path write")), \
             mock.patch.object(subprocess, "Popen", side_effect=AssertionError("process")):
            self.outcome("matched", program="missing/never-open.s")


MUTATIONS = {
    "image-guard": ('if type(image) is not bytes or not 1 <= len(image) <= G.IMAGE_BYTES:', 'if False:'),
    "image-bound": ('len(image) <= G.IMAGE_BYTES:', 'len(image) <= 2 * G.IMAGE_BYTES:'),
    "empty-image": ('not 1 <= len(image)', 'not 0 <= len(image)'),
    "complete-equality": ('if image != built.image:', 'if False:'),
    "payload-only": ('if image != built.image:', 'if image[4098:4104] != built.image[4098:4104]:'),
    "source-forward": ('G.build_guest_image(source, program=program, entry=entry)', 'G.build_guest_image(b"c.nop", program=program, entry=entry)'),
    "program-forward": ('G.build_guest_image(source, program=program, entry=entry)', 'G.build_guest_image(source, program="wrong", entry=entry)'),
    "entry-forward": ('G.build_guest_image(source, program=program, entry=entry)', 'G.build_guest_image(source, program=program, entry=0x80000000)'),
    "unavailable-class": ('SourceImageCheck("unavailable",', 'SourceImageCheck("refused",'),
    "refusal-class": ('SourceImageCheck("refused", "source or selected', 'SourceImageCheck("matched", "source or selected'),
    "source-fingerprint": ('built.source_size, built.source_sha256,', 'built.source_size, built.image_sha256,'),
    "image-fingerprint": ('hashlib.sha256(image).hexdigest()', 'built.image_sha256'),
    "source-retention": ('built.source_size, built.source_sha256,', 'built.source_size, source,'),
    "frozen-result": ('@dataclass(frozen=True)\nclass SourceImageCheck:', '@dataclass\nclass SourceImageCheck:'),
    "frozen-facts": ('@dataclass(frozen=True)\nclass SourceImageFacts:', '@dataclass\nclass SourceImageFacts:'),
    "diagnostic-echo": ('except G.ImageError:\n        return SourceImageCheck("refused", "source or selected image context refuses construction")', 'except G.ImageError as exc:\n        return SourceImageCheck("refused", str(exc))'),
    "broad-unavailable": ('except G.ImageUnavailable:', 'except RuntimeError:'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()
    if args.mutation:
        global M
        before, after = MUTATIONS[args.mutation]
        source = Path(M.__file__).read_text()
        if source.count(before) != 1:
            raise SystemExit("mutation seam is not singular")
        module = types.ModuleType("mutated_source_image")
        module.__file__ = M.__file__
        sys.modules[module.__name__] = module
        exec(compile(source.replace(before, after, 1), M.__file__, "exec"), module.__dict__)
        M = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(SourceImageTests))
    print(f"MATCHED-GPR-SOURCE-IMAGE: {result.testsRun} tests / {len(result.failures)} failures / "
          f"{len(result.errors)} errors; byte correspondence only")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
