//! Tests for the ELF loader: every refusal names the field, and the writer the guests use
//! round-trips through parse into the same entry and payload.

use super::*;

/// The same writer shape `scripts/riscv_asm.py`'s `write_elf64` emits: EHDR + one PHDR +
/// payload + shstrtab + three SHDRs. The loader reads only what it validates.
fn write_elf64(entry: u64, payload: &[u8]) -> Vec<u8> {
    let shstrtab = b"\0.text\0.shstrtab\0";
    let phoff = EHDR;
    let text_off = phoff + PHDR;
    let shstr_off = text_off + payload.len();
    let shoff = shstr_off + shstrtab.len();
    let mut out = Vec::new();
    out.extend_from_slice(&0x7fu64.to_le_bytes()[..1]);
    out.extend_from_slice(b"ELF");
    out.push(2); // ELFCLASS64
    out.push(1); // ELFDATA2LSB
    out.push(1); // EV_CURRENT
    out.push(0); // ABI SysV
    out.push(0);
    out.extend_from_slice(&[0u8; 7]);
    out.extend_from_slice(&ET_EXEC.to_le_bytes());
    out.extend_from_slice(&EM_RISCV.to_le_bytes());
    out.extend_from_slice(&1u32.to_le_bytes());
    out.extend_from_slice(&entry.to_le_bytes());
    out.extend_from_slice(&(phoff as u64).to_le_bytes());
    out.extend_from_slice(&(shoff as u64).to_le_bytes());
    out.extend_from_slice(&0u32.to_le_bytes());
    out.extend_from_slice(&(EHDR as u16).to_le_bytes());
    out.extend_from_slice(&(PHDR as u16).to_le_bytes());
    out.extend_from_slice(&1u16.to_le_bytes());
    out.extend_from_slice(&64u16.to_le_bytes());
    out.extend_from_slice(&3u16.to_le_bytes());
    out.extend_from_slice(&2u16.to_le_bytes());
    // PT_LOAD, R|W|X, offset, vaddr = paddr = entry, filesz = memsz = payload, align 0x1000.
    out.extend_from_slice(&PT_LOAD.to_le_bytes());
    out.extend_from_slice(&7u32.to_le_bytes());
    out.extend_from_slice(&(text_off as u64).to_le_bytes());
    out.extend_from_slice(&entry.to_le_bytes());
    out.extend_from_slice(&entry.to_le_bytes());
    out.extend_from_slice(&(payload.len() as u64).to_le_bytes());
    out.extend_from_slice(&(payload.len() as u64).to_le_bytes());
    out.extend_from_slice(&0x1000u64.to_le_bytes());
    out.extend_from_slice(payload);
    out.extend_from_slice(shstrtab);
    out.extend_from_slice(&[0u8; 3 * 64]);
    out
}

#[test]
fn the_writer_round_trips_through_parse() {
    let entry = 0x8000_0000u64;
    let payload: [u8; 8] = [0x93, 0x00, 0x50, 0x00, 0x13, 0x81, 0xf0, 0xff];
    let image = write_elf64(entry, &payload);
    let parsed = parse(&image, 32).unwrap();
    assert_eq!(parsed.entry, entry);
    assert_eq!(parsed.segments.len(), 1);
    let seg = parsed.segments[0];
    assert_eq!(seg.paddr, entry);
    assert_eq!(seg.filesz, payload.len());
    assert_eq!(seg.memsz, payload.len() as u64);
    assert_eq!(image[seg.offset..seg.offset + seg.filesz], payload);
}

#[test]
fn refusals_name_the_field() {
    let entry = 0x8000_0000u64;
    let good = write_elf64(entry, &[0u8; 4]);

    let mut bad = good.clone();
    bad[0] = 0x7e;
    assert_eq!(
        parse(&bad, 32).unwrap_err(),
        ElfError("bad magic — not an ELF file")
    );

    let mut bad = good.clone();
    bad[4] = 1;
    assert_eq!(
        parse(&bad, 32).unwrap_err(),
        ElfError("not a 64-bit (ELFCLASS64) file")
    );

    let mut bad = good.clone();
    bad[5] = 2;
    assert_eq!(
        parse(&bad, 32).unwrap_err(),
        ElfError("not a little-endian (ELFDATA2LSB) file")
    );

    let mut bad = good.clone();
    bad[16] = 3; // ET_DYN
    assert_eq!(
        parse(&bad, 32).unwrap_err(),
        ElfError("not an executable (ET_EXEC) file")
    );

    let mut bad = good.clone();
    bad[18] = 0x28; // EM_AARCH64
    assert_eq!(
        parse(&bad, 32).unwrap_err(),
        ElfError("not a RISC-V (EM_RISCV) file")
    );

    let mut bad = good.clone();
    bad[24] = 0x02; // entry 0x...02, misaligned
    assert_eq!(
        parse(&bad, 32).unwrap_err(),
        ElfError("the entry address is not 4-byte aligned (IALIGN=32)")
    );

    assert_eq!(
        parse(&good[..32], 32).unwrap_err(),
        ElfError("smaller than the 64-byte ELF header")
    );

    let mut bad = good.clone();
    let phnum_at = 56;
    bad[phnum_at] = 0xff; // 255 program headers: table runs past the image
    assert_eq!(
        parse(&bad, 32).unwrap_err(),
        ElfError("program-header table extends past the image")
    );

    let mut bad = good;
    // filesz (phdr+32) larger than the image allows.
    let filesz_at = EHDR + 32;
    bad[filesz_at] = 0xff;
    assert_eq!(
        parse(&bad, 32).unwrap_err(),
        ElfError("a PT_LOAD segment extends past the image")
    );
}
