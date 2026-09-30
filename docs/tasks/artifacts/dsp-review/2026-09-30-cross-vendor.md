# DSP-REVIEW.8 evidence — the cross-vendor contrast (catalog §5, over NXP DSP56300 + ADI SHARC)

Measured `2026-09-30` over the two manuals the channel answered with
(`NXP-DSP56300-FAMILY-MANUAL`, `ADI-SHARC-PRM-2.4`; adopted `SEMULITH-DR-0092`), the
same questions and method as `.1`–`.5`. The point of the contrast: the TI family's two
measured ABSENCES were never DSP facts — they are TI facts.

## The headline inversion

**Accumulators and guard bits exist — as other vendors' core structures.**
- **DSP56300** (§3.1, p. 3-1/3-3): two 56-bit accumulators A/B, each three registers —
  `A2:A1:A0` — with the 8-bit **extension register** in A2/B2 ("The 8-bit EXT is stored
  in A2 or B2"). 24-bit operands, 48-bit product, "right-justified into 56 bits and
  added to the 56-bit contents of either accumulator". The fractional representation is
  the architecture's own ("The DSP56300 core uses a fractional data representation for
  all data ALU operations", §3.2.1) — weights 2^0…2^-23, never named "Q" (measured).
  Saturation is split in two by name: the SM bit's **arithmetic saturation** (to 48
  bits at accumulate) vs **transfer saturation** (limiting at the accumulator READ) —
  a per-operation vs per-transfer granularity contrast no TI manual makes.
- **SHARC** (§3, p. 3-13–3-15): fixed-point multiplies "produce 80-bit results" into
  MRF/MRB = MR2 (16 bits) + MR1 + MR0 — and the manual calls them **guard bits**
  outright ("Data read from MR2F (guard bits) is sign-extended to 32 bits"). Signed
  fractional inputs auto-shift the result left one bit (the redundant sign bit).
  Saturation is a separate instruction (SAT MRx); ALU saturation is a MODE bit
  (ALUSAT).

**Bit-reversed addressing exists — twice.**
- **DSP56300**: the reverse-carry modifier (`Mn = $000000`), hardware carry from MSB to
  LSB, "useful for 2k-point FFT addressing … up to 16,777,216 points" (§4.5.2, p. 4-10).
- **SHARC**: `BR0`/`BR8` in MODE1 bit-reverse the I0/I8 address OUTPUTS (§6, p. 6-25).
  And its circular buffers need **no alignment** ("located at arbitrary boundaries",
  §1 p. 1-6/1-7) — against TI's align-to-block-size and DSP56300's 2^k-aligned base.
  Three alignment rules for one concept, all measured.

## The unit-shape variety (SEM-05's question, answered wider)

Three distinct address-unit shapes across four vendors: TI's 32-bit bytes (matches the
lab's units); **DSP56300's 24-bit WORDS in THREE spaces** (P/X/Y — "to feed two operands
simultaneously to the Data ALU", §11.1, p. 11-1; address +1 = one 24-bit word); **SHARC's
word-addressed spaces whose WIDTH VARIES BY SPACE** (NW 32/48, SW 16, LW 64). A byte
model expresses none of the three without unit metadata on the address itself.

## The execution-model variety

TI's VLIW packets against two scalars: **DSP56300** is one instruction/cycle in a
seven-stage pipeline ("essentially invisible to the programmer" — yet §3.4.2/§3.5
document arithmetic/status/transfer stalls; recorded unresolved) with REP's
not-interruptible repeats; **SHARC** is one instruction/cycle in a **five-stage
INTERLOCKED** pipeline ("All possible hazards are controlled by hardware", §4, p. 4-5 —
the exact negation of TI's printed "eliminating pipeline interlocks"), optional SIMD via
the PEYEN bit, and delayed branches that are ATOMIC against interrupts. So the `.4`
break is TI-family-shaped, not DSP-shaped: the delayed-effects question is per-vendor.

## Sticky flags and loops, across vendors

- DSP56300's S (FFT scaling) and L (limit) bits are called "sticky" by the manual
  ("remains set until explicitly cleared"); the whole SR stacks on long-interrupt entry
  and restores on RTI — but entry CLEARS the loop flag and scaling mode bits, restored
  on return (§2, p. 2-14).
- SHARC's STKYx/y: "Once set, a sticky flag remains high until explicitly cleared";
  ASTATx/y + MODE1 auto-stack for IRQ0-2/timer ONLY — whether STKYx/y need software
  saves elsewhere is NOT stated (measured absence, not an asserted rule).
- Loops: DSP56300's stack-based DO (7 deep, interruptible) vs **REP (never
  interruptible — fetches suspend)**; SHARC's 6-deep loop stack with the termination
  test four instructions early and CURLCNTR frozen 4 fetch cycles on ISR return; TI's
  SPLOOP (drain-to-boundary, not-interruptible-if-small). Three loop models, three
  interrupt rules.

## Defects/ambiguities recorded (not resolved)

DSP56300: (1) the 8-bit EXT is never called "guard" (`guard` = JTAG hits only) — the
mapping is functional, stated as such; (2) the "invisible pipeline" claim vs the
documented stalls; (3) "Q1.23" is inference from bit weights, not the manual's term.
SHARC: (5) "The bit **reserve** mode" (p. 6-25, probable typo); (6) Table 3-4's
saturation values extract column-scrambled (do not trust from the text layer without a
visual check); (7) Listing 6-7's `IO` letter/digit confusion; (8) Table 1-1's extraction
scramble; (9) the STKY auto-save question above.
