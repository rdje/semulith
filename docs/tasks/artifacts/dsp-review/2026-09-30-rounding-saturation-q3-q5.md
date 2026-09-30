# DSP-REVIEW.2 evidence — rounding, saturation and sticky flags (catalog §5, questions 3–5)

Measured `2026-09-30` over the same three catalogued TI manuals' extracted text layers
(the `.1` method; `target/dsp-review/` scratch). Manuals: `TI-C64X-SPRU732J`,
`TI-C66X-SPRUGH7`, `TI-C674X-SPRUFE8B`. ⛔ No finding below is resolved by intuition —
the AMBIGUOUS ones are recorded with their quotes, per the leaf's discipline.

## Q3 — the rounding ORDER, as defined step sequences (the acceptance's exact ask)

The family pattern, per the manuals' own arithmetic: **multiply → accumulate →
round-add → shift/saturate → narrow**. Representative sequences:

- **CMPYR1** (C64x p. 188; C674x p. 219 identical): products of halfword pairs →
  subtract/accumulate → "rounded by adding 2^14" → "shifted left by 1 **with
  saturation**" → the 16 MSBs written. Saturation happens inside the shift step — AFTER
  rounding, BEFORE narrowing ("If either result saturates in the rounding or shifting
  process…").
- **DDOTPH2R** (C64x p. 195): accumulate → "+2^15" round → "saturated if appropriate" →
  msb16 narrow. The rounding term can itself push the sum into saturation range.
- **QSMPY32R1** (C66x §4.241, p. 4-512): 32×32 product → round-add (+2^30) at the 64-bit
  intermediate → >>31 (narrows) → saturation ONLY for the max-negative corner. Per lane,
  4 lanes, each formula independent.
- **DOTPNRSU2** (C64x p. 210): round-and-shift with NO saturation step — and a
  core-version split: the intermediate is 32-bit on C64x ("Overflow may occur during the
  rounding step") vs 33-bit on C64x+/C674x ("no overflow may occur"). **A profile must
  pin WHICH core** — the same instruction's intermediate width differs by core version.
- **MPYHIR/MPYIHR** (C64x p. 294–295): +2^14 then >>15, truncate — with NO saturation
  clause at all (recorded as ambiguity 5 below).

## Q4 — saturation granularity

Both models exist, and the manuals say which is which:
- **In-instruction, per lane, independently**: SADD2 ("Saturation is performed on each
  16-bit result independently", C64x p. 369 / C66x p. 4-533), SPACK2 (p. 418 /
  p. 4-592), SADDU4 per-8-bit (C66x), the S-prefixed multiplies.
- **Explicit later transfer**: SAT (40→32 saturating narrow, C64x p. 381 / C674x p. 437
  / C66x §4.256 p. 4-548).
- ⭐ **The flag side effect is per-instruction EXPLICIT, not derivable**: SADD sets CSR's
  SAT bit; SADD2/SADDSUB/ABS2 saturate but "does **not** affect the SAT bit in CSR"
  (the note is printed in each instruction's entry). Whether a saturating instruction
  sets the sticky flag is DATA on the instruction, not a consequence of saturation.

## Q5 — sticky flags' lifetime

- **CSR.SAT** (Table 2-9, §2.8.4, p. 38; same text in C66x): "Can be cleared only by the
  MVC instruction and can be set only by a functional unit… The SAT bit will not be
  modified by a conditional instruction whose condition is false." Set one cycle AFTER
  the result write (§2.8.2, p. 35) — a **delayed effect** (the catalog's C09 territory,
  `.4`'s input).
- **SSR** (C64x+ and later; §2.9.13 p. 54 / C66x §2.9.12 p. 2-30): "The bits are cleared
  only by a reset or by the MVC instruction. The bits are not cleared by the occurrence
  of a nonsaturating instruction."
- **Interrupts do not save them**: the interrupt hardware saves TSR fields only (C64x
  Table 5-3 p. 551; C66x Table 6-3 p. 6-20) — SAT/SSR survive interrupts untouched;
  software owns them.
- **Context-switch restore ORDER is documented**: the SAT bit cannot be written to 1 by
  MVC, so restoring it takes a saturating instruction, which affects SSR — therefore
  "SSR must be restored after the SAT bit has been restored" (same sections).
- "Sticky" as a word: 0 hits in all three manuals — the property is expressed as
  "cleared only by…". Measured, so nobody cites a term the manuals don't use.

## Manual defects and ambiguities — recorded, NOT resolved (the leaf's discipline)

1. **CMPYR1's execution block reuses `tmp_e` for the odd lane** where the prose defines
   `tmp_o` (C64x p. 188 AND C674x p. 219 — the same typo in both).
2. **C66x CMPY32R1/CCMPY32R1 prose order contradicts the C sequence**: prose says
   "shifted right by 31, rounded and saturated"; the functional C is
   `(sum + (1<<30)) >> 31` — round-add BEFORE the shift (§4.59/§4.37).
3. **CMPY32R1's printed formulas apply `sat(…)` to only one half** while its worked
   example shows both halves saturate (p. 4-143) — a typesetting gap.
4. **CCMPY32R1's corner case prints a seven-digit operand** (`0x8000000`) where the
   context's corner is `0x80000000` (p. 4-86).
5. **MPYHIR/MPYIHR define rounding with NO saturation clause** — whether the rounded sum
   can overflow, and what then, is unspecified in the text (C64x p. 294–295).
6. **DOTPNRSU2's intermediate width differs by core** (32-bit C64x, 33-bit C64x+/C674x)
   — documented, not a defect; it is a profile-pinning obligation.
7. **C66x's CSR table carries C674x wording** ("This field is ignored on the C674x CPU")
   — an inherited-text artifact; treat its subject as unupdated (same class as the
   §3.8.7 finding in `.1`'s evidence).

## First classification (feeds `.7`)

- **Ordering**: the abstraction's per-instruction effect trees already evaluate sequenced
  effects — the multiply→accumulate→round-add→saturate→narrow ORDER expresses today.
  The open seam is intermediate WIDTHS (33-bit intermediates; the core-version split) —
  a semantics-data concern when a DSP profile exists, not an abstraction change.
- **Flag side effects as instruction DATA** (SAT set vs not-set is per-instruction):
  expressible if the flag is architectural state — a state-census question at profile
  time, flagged now so `.4`/`.5` don't assume otherwise.
- **The one-cycle-delayed SAT update** is the delayed-effect shape this tree predicted
  (catalog C09) — an `.4` input: the scalar lab's one-instruction-complete step model
  does not represent it; whether it must, is `.4`'s measured question.
- **Interrupt-survival and context-switch ordering** are measured but OUT of the scalar
  lab's scope (no events); they become requirements when a DSP profile reopens
  `OB-ENV-EVENT-DELIVERY`.
