"""Bounded complete ELF correspondence from supplied source/image snapshots.

Caller owns authentication, selected parent program/entry, current tool adequacy
and aggregate reservation before I/O. This unit neither reads artifact paths nor
proves source-grounded expected properties or qualification. Canonical tool reads
belong to the public builder; its temporary rebuilt ELF is at most 64 KiB.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib

import matched_gpr_image as G


@dataclass(frozen=True)
class SourceImageFacts:
    program: str
    entry: int
    encoding_path: str
    ialign: int
    source_size: int
    source_sha256: str
    payload_size: int
    payload_sha256: str
    rebuilt_image_size: int
    rebuilt_image_sha256: str
    image_size: int
    image_sha256: str


@dataclass(frozen=True)
class SourceImageCheck:
    disposition: str  # matched / refused / unavailable; no authentication credit
    reason: str
    facts: SourceImageFacts | None = None  # Metadata only, including on byte mismatch.


def check_source_image(source: bytes, image: bytes, *, program: str,
                       entry: int) -> SourceImageCheck:
    """Compare all supplied ELF bytes with the sole bounded GC reconstruction.

    Validate the image before canonical I/O; builder preflights source/metadata.
    Results retain no supplied or reconstructed bytes. Input/output bounds are
    payload bounds, not exact RAM/time limits. Program is a caller-selected label,
    not a filename embedded in ELF or evidence of source semantics.
    """
    if type(image) is not bytes or not 1 <= len(image) <= G.IMAGE_BYTES:
        return SourceImageCheck("refused", "image must be plain bytes of 1..65536 bytes")
    try:
        built = G.build_guest_image(source, program=program, entry=entry)
    except G.ImageUnavailable:
        return SourceImageCheck("unavailable", "canonical GC image construction is unavailable")
    except G.ImageError:
        return SourceImageCheck("refused", "source or selected image context refuses construction")
    facts = SourceImageFacts(
        built.program, built.entry, built.encoding_path, built.ialign,
        built.source_size, built.source_sha256, built.payload_size, built.payload_sha256,
        built.image_size, built.image_sha256, len(image), hashlib.sha256(image).hexdigest())
    if image != built.image:
        return SourceImageCheck("refused", "supplied ELF bytes differ from rebuilt source", facts)
    return SourceImageCheck("matched", "complete source/image bytes match; no authentication or qualification", facts)
