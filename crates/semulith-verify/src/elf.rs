//! A minimal ELF64 loader for the laboratory's freestanding guests — `P1-LAB.8`.
//!
//! The tracked guests are written by `scripts/riscv_asm.py`'s `write_elf64`: one `PT_LOAD`
//! program header carrying the payload at the entry address, plus a section header table
//! the references' loader strictness requires. This loader validates the ELF header fields
//! that establish it IS that kind of file (64-bit, little-endian, RISC-V, executable) and
//! surfaces every `PT_LOAD` segment; placement into a fixture region is the caller's act,
//! with its own knowledge of the platform's memory map.
//!
//! Deliberately strict: a field this loader cannot interpret is refused with its name, not
//! guessed — the guests are the only inputs, and an input only one reader accepts is not a
//! matched experiment (DIFF-ELF-STRICTNESS in `references.sexp`).

/// Why an ELF image was refused.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ElfError(pub &'static str);

impl std::fmt::Display for ElfError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

/// One loadable segment: where it goes and which bytes of the image it carries.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Segment {
    /// Physical (== virtual for these guests) load address.
    pub paddr: u64,
    /// Offset of the segment's bytes within the image.
    pub offset: usize,
    /// How many bytes the image carries for this segment.
    pub filesz: usize,
    /// How many bytes the segment occupies in memory (the remainder is zero-filled).
    pub memsz: u64,
}

/// A parsed ELF64 executable: the entry point and its loadable segments.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Image {
    pub entry: u64,
    pub segments: Vec<Segment>,
}

const EM_RISCV: u16 = 0xF3;
const ET_EXEC: u16 = 2;
const PT_LOAD: u32 = 1;
const EHDR: usize = 64;
const PHDR: usize = 56;

fn read_u16(b: &[u8], at: usize) -> u16 {
    u16::from_le_bytes([b[at], b[at + 1]])
}

fn read_u32(b: &[u8], at: usize) -> u32 {
    u32::from_le_bytes([b[at], b[at + 1], b[at + 2], b[at + 3]])
}

fn read_u64(b: &[u8], at: usize) -> u64 {
    let mut v = [0u8; 8];
    v.copy_from_slice(&b[at..at + 8]);
    u64::from_le_bytes(v)
}

/// Parse the image. Refuses, naming the field, anything that is not a 64-bit little-endian
/// RISC-V executable with program headers this loader can walk.
pub fn parse(image: &[u8]) -> Result<Image, ElfError> {
    if image.len() < EHDR {
        return Err(ElfError("smaller than the 64-byte ELF header"));
    }
    if image[0..4] != [0x7f, b'E', b'L', b'F'] {
        return Err(ElfError("bad magic — not an ELF file"));
    }
    if image[4] != 2 {
        return Err(ElfError("not a 64-bit (ELFCLASS64) file"));
    }
    if image[5] != 1 {
        return Err(ElfError("not a little-endian (ELFDATA2LSB) file"));
    }
    if read_u16(image, 16) != ET_EXEC {
        return Err(ElfError("not an executable (ET_EXEC) file"));
    }
    if read_u16(image, 18) != EM_RISCV {
        return Err(ElfError("not a RISC-V (EM_RISCV) file"));
    }
    let entry = read_u64(image, 24);
    if !entry.is_multiple_of(4) {
        return Err(ElfError(
            "the entry address is not 4-byte aligned (IALIGN=32)",
        ));
    }
    let phoff = read_u64(image, 32) as usize;
    let phentsize = read_u16(image, 54) as usize;
    let phnum = read_u16(image, 56) as usize;
    if phentsize != PHDR {
        return Err(ElfError("program-header entry size is not 56 bytes"));
    }
    let table_end = phoff
        .checked_add(
            phnum
                .checked_mul(PHDR)
                .ok_or(ElfError("program-header count overflows"))?,
        )
        .ok_or(ElfError("program-header table extends past the image"))?;
    if table_end > image.len() {
        return Err(ElfError("program-header table extends past the image"));
    }
    let mut segments = Vec::new();
    for i in 0..phnum {
        let at = phoff + i * phentsize;
        if read_u32(image, at) != PT_LOAD {
            continue;
        }
        let offset = read_u64(image, at + 8) as usize;
        let paddr = read_u64(image, at + 24);
        let filesz = read_u64(image, at + 32) as usize;
        let memsz = read_u64(image, at + 40);
        let end = offset
            .checked_add(filesz)
            .ok_or(ElfError("segment extent overflows"))?;
        if end > image.len() {
            return Err(ElfError("a PT_LOAD segment extends past the image"));
        }
        if (filesz as u64) > memsz {
            return Err(ElfError(
                "a PT_LOAD segment carries more file bytes than memory bytes",
            ));
        }
        segments.push(Segment {
            paddr,
            offset,
            filesz,
            memsz,
        });
    }
    if segments.is_empty() {
        return Err(ElfError("no PT_LOAD segment — nothing to place in memory"));
    }
    Ok(Image { entry, segments })
}

#[cfg(test)]
mod tests;
