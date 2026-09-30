# DSP-REVIEW.3 evidence — addressing and address spaces (catalog §5, questions 6–8)

Measured `2026-09-30` over the same three catalogued TI manuals' extracted text layers
(the `.1`/`.2` method). Manuals: `TI-C64X-SPRU732J`, `TI-C66X-SPRUGH7`,
`TI-C674X-SPRUFE8B`. The vendor-diversity measurement also landed today: the base is one
vendor's one family, and the corpus cannot widen it yet — two gaps filed
(`GAP-DSP56K-FAMILY-MANUAL`, `GAP-ADI-SHARC-PRM`, `SEMULITH-DR-0087`); the C55x want
dissolved on measurement (already catalogued).

## Q6 — units: instruction and data addresses

**The same units: bytes, one 32-bit numbering, both spaces.** "The C64x and C64x+ DSP
have a 32-bit, byte-addressable address space" (C64x §1.4.2, p. 23; C66x §1.2.2, p. 1-6;
C674x §1.3.2, p. 23). The branch displacement is a byte offset scaled by 4 only in its
ENCODING ("cst21 = (label − PCE1) >> 2", B, C64x p. 131). ⛔ Measured absence: no
word-addressed space exists — every `word address` hit is an ADDAB/ADDAH/ADDAW offset
*scaling* note or an alignment note, never an address space's unit. This MATCHES the
lab's byte-addressed model (SEM-05's units answer: same unit on both sides); the width
differs (32-bit, not 64).

Fetch has structure data lacks: "Instructions are always fetched eight words at a time…
fetch packets are aligned on 256-bit (8-word) boundaries" (C64x §3.4, p. 64–65). The
program counter is the PFC and it names bytes; fetch granularity is 256 bits.

## Q7 — memory spaces and address generators

- **Two architecturally distinct spaces at L1** (Harvard shape), unified later:
  "Internal (on-chip) memory is organized in separate data and program spaces. When
  off-chip memory is used, these spaces are unified on most devices … via the external
  memory interface" (C64x §1.4.2, p. 23). C66x is sharper: "L1 … separate data and
  program spaces, with unified memory for L2 and higher" (§1.2.2, p. 1-6). Ports differ
  by direction: a read-only 256-bit program port + two 256-bit data ports (C66x §1.2.2).
- **The .D units ARE the address generators** — no separate AGU: "The data address paths
  (DA1 and DA2) are each connected to the .D units in both data paths" (C64x §2.6,
  p. 31), and cross-file routing is decoupled (`LDW .D1T2 *A0[3],B1` — the .D1 unit
  generates the address, the DA2 path places the data in the B file, §2.6 p. 31).
- No separate I/O space: peripherals are memory-mapped (C64x §1.4.3, p. 23). One
  instruction never addresses two spaces (load/store architecture, C64x §3.8.3, p. 79).

## Q8 — modulo / circular / strided / bit-reversed modes

- **Circular: yes, via the AMR** (Addressing Mode Register, §2.8.3, p. 36 in C64x and
  C674x; §2.8.3, p. 2-12 in C66x): eight registers only (A4–A7, B4–B7) can be circular; a
  2-bit field per register selects linear / circular-with-BK0 / circular-with-BK1;
  "Block size (in bytes) = 2^(N+1)" for the 5-bit BK field; "the buffer must be aligned
  on a byte boundary equal to the block size". Wrap mechanics: "only … bits N through 0
  of the result [are] updated, leaving bits 31 through N+1 unchanged" (C64x §3.8.2,
  p. 77) — and the AMR buffer size "is not scaled" by data size.
- **A measured core-version split**: nonaligned circular access is "at least as large as
  the data size" on C64x but "at least 32 bytes" on C64x+/C66x/C674x (§3.8.2.3 p. 77–78
  vs §3.9.2.3 p. 3-26 / p. 87) — a profile-pinning obligation, same class as `.2`'s
  DOTPNRSU2 split.
- **Bit-reversed addressing: measured ABSENT as an addressing mode** — `bit-rev`/`bitrev`
  has exactly one hit per manual: BITR, a DATA operation ("reverses the order of bits in
  a 32-bit word", C64x p. 144). **Strided: measured absent** (0 hits, all three); the
  only stride-like mechanism is the scaled offset (shift 0–3 by data size). "Modulo"
  hits are Galois-field arithmetic and the SPLOOP loop buffer — NOT address arithmetic;
  recorded so the catalog doesn't conflate them.

## Fit against the flat 64-bit byte-addressed lab model (the acceptance's exact check)

- **Units: compatible** — bytes on both sides (Q6).
- **Does NOT fit**: the 32-bit space (the lab is 64-bit); two L1 spaces with a
  program-only fetch path (the lab's D-FETCH-MAP declares fetch and data maps
  IDENTICAL); fetch-packet alignment structure; addressing state in a CONTROL REGISTER
  (AMR) rather than in operands — the lab has no CSR surface at all; and circular
  addressing restricted to a named register subset (A4–A7/B4–B7) — a per-register
  capability the lab's uniform register file lacks.
- The `.7` classification input: address generation as a UNIT-BOUND capability (the .D
  units) + side-state (AMR) + per-register capability bits — three distinct seams, each
  measured here.

## Manual defects / ambiguities recorded (not resolved)

1. **C66x §1.2.2 garble** (p. 1-6): "L1 memory for each DSP CPU memory is organized…" —
   an editing artifact; the intended subject is L1 memory per DSP CPU.
2. **AMR Table 2-7 row-shift** (C64x p. 36–37, C674x same, C66x Table 2-7 p. 2-12): the
   Value/Description rows are offset by one in places (readable from Figure 2-3; the
   table rows alone misalign).
3. **The wrap formula's alignment precondition lives in a different chapter** (§2.8.3's
   alignment rule vs §3.8.2's wrap arithmetic) with no cross-reference — easy to miss;
   recorded so a future model states the precondition AT the rule.
4. **"Modulo" is overloaded** in these manuals (Galois field; SPLOOP "modulo loop") —
   only AMR circular addressing is modulo ADDRESSING.
