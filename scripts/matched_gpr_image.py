"""Bounded first-method GC image construction from supplied immutable source bytes.

Caller owns source authentication, parent selection and complete current tool
adequacy. Canonical assembler construction reads project tool data, outside this
utility's supplied-artifact budgets. No source path reopens, writes, reference
processes, artifact authentication or qualification occur here.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import re

import dossier_sexp as D
import riscv_asm as A
import sexp as S

ROOT = Path(__file__).resolve().parent.parent
ENCODING_PATH = "profiles/rv64gc-lab-v0/encoding.sexp"
SOURCE_BYTES = 1024 * 1024
SOURCE_LINES = 8192
PAYLOAD_BYTES = 32 * 1024
IMAGE_BYTES = 64 * 1024
# Exact str.splitlines separators; CRLF is one boundary. Preflight precedes list allocation.
_LINE_BREAK = re.compile(r"\r\n|[\n\r\v\f\x1c-\x1e\x85\u2028\u2029]")


class ImageError(ValueError):
    """Invalid supplied source/metadata or refused construction; no image result."""


class ImageUnavailable(RuntimeError):
    """The current canonical GC assembler context cannot be constructed."""


@dataclass(frozen=True)
class GuestImage:
    program: str
    encoding_path: str
    entry: int
    ialign: int
    source_size: int
    source_sha256: str
    payload_size: int
    payload_sha256: str
    image_size: int
    image_sha256: str
    image: bytes


def _source_lines(text: str) -> list[str]:
    count = 0
    end = 0
    for boundary in _LINE_BREAK.finditer(text):
        count += 1
        if count > SOURCE_LINES:
            raise ImageError("source exceeds 8192 splitlines")
        end = boundary.end()
    if end < len(text):
        count += 1
    if count > SOURCE_LINES:
        raise ImageError("source exceeds 8192 splitlines")
    return text.splitlines()


def build_guest_image(source: bytes, *, program: str, entry: int) -> GuestImage:
    """Build at most 64 KiB of ELF from 1..1 MiB / 8192 lines of GC source.

    Exact bytes/identifier metadata are construction facts, not authentication or
    source semantics. No raw source is retained. Bounds are not exact RAM/time
    limits. ImageError diagnostics are fixed strings and never echo source text;
    unavailable/malformed canonical tools raise ImageUnavailable separately.
    """
    if type(source) is not bytes or not 1 <= len(source) <= SOURCE_BYTES:
        raise ImageError("source must be immutable bytes of 1..1048576 bytes")
    if type(program) is not str or not 1 <= len(program) <= 65536:
        raise ImageError("program must be a plain string of 1..65536 characters")
    if type(entry) is not int or not 0 <= entry < 1 << 64:
        raise ImageError("entry must be an unsigned 64-bit integer")
    try:
        text = source.decode("utf-8")
    except UnicodeError:
        raise ImageError("source must be UTF-8") from None
    lines = _source_lines(text)
    encoding = ROOT / ENCODING_PATH
    try:
        if not encoding.is_file() or encoding.resolve() != encoding:
            raise ImageUnavailable("canonical GC encoding must be an existing regular file")
        assembler = A.Assembler(encoding)
        if type(assembler.ialign) is not int or assembler.ialign != 16:
            raise ImageUnavailable("canonical GC context must declare IALIGN16")
    except (OSError, A.AsmError, D.DossierError, S.SexpError, ValueError,
            TypeError, KeyError, IndexError, RecursionError):
        raise ImageUnavailable("canonical GC assembler context is unavailable or invalid") from None
    try:
        payload = assembler.assemble_image(lines, base=entry)
        if type(payload) is not bytes:
            raise ImageError("assembler must return immutable payload bytes")
        if len(payload) > PAYLOAD_BYTES:
            raise ImageError("assembled payload exceeds 32768 bytes")
        image = A.encode_elf64(entry, payload, assembler.ialign)
        if type(image) is not bytes:
            raise ImageError("ELF encoder must return immutable image bytes")
        if len(image) > IMAGE_BYTES:
            raise ImageError("ELF image exceeds 65536 bytes")
    except (A.AsmError, ValueError, OverflowError) as exc:
        if isinstance(exc, ImageError):
            raise
        raise ImageError("source or ELF construction refuses") from None
    return GuestImage(program, ENCODING_PATH, entry, assembler.ialign,
                      len(source), hashlib.sha256(source).hexdigest(),
                      len(payload), hashlib.sha256(payload).hexdigest(),
                      len(image), hashlib.sha256(image).hexdigest(), image)
