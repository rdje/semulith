# The method: from document to model

The route from the pinned family manual to a running, differentially agreed model was
deliberately different from the scalar unit's — and the difference is recorded, because
it is the point of the exercise.

## Why a sibling crate, decided before any code

The scalar unit's definition pipeline (`gen_definition.py`) was measured to refuse a
second unit at three named walls: the profile scope ("a second unit is generator work,
not a config knob"), the decode width (it emits a 32-bit table; the DSP fetches 24-bit
words), and the semantics corpus (the DSP's semantics would need re-expression as data
in a language that has no memory-space parameter, no accumulator parts, and no loop
state). Building that generalization first, before any exercised target demanded it,
would have been exactly the speculative generality `P3-BREADTH` exists to refuse — the
tree's own acceptance requires every schema/generator extension to name the target and
case that required it. So the vehicle was decided as a hand-written sibling crate
(`decision_dsp56300-lab-v0-subset`), keeping the gated scalar model byte-untouched, and
the encoding lane was later measured and deferred with named reopening conditions
(`P3-BREADTH.5` slice 3).

## What "hand-written" is disciplined to mean

Every decode mask and every semantic rule in `crates/semulith-dsp56300` carries a
per-form citation to the pinned FM (chapter-page), cross-checked against the pinned MIT
assembler's encodings. The model derives from the *manual*, never from the reference
emulator's decoder tables — the independence the differential needs
(`decision_dsp56300-lab-v0-subset`): Semulith-vs-emulator is a second opinion only
because the two were built from different sources.

## Evidence path first

No model code existed until the evidence path was exercised end-to-end (`P3-BREADTH.3`
slice 2): the reference pinned and built on-volume, a micro guest assembled and run
headless, and the canonical dump verified three independent ways (hand arithmetic
reproducing the 56-bit accumulator exactly, the X/Y-space memory deviations, and the
FM's own short-immediate rule explaining the one surprising value). The path
demonstration caught the project treating a surprise as a suspected defect and chasing
it to ground truth — the natural falsification probe fired, and the reference matched
the manual.

## The differential campaign, and what it caught

Form coverage was completed against the pinned sources, then six synthetic guests were
assembled and run under both engines, compared as canonical end-state dumps (51–64
fields per case; `cyc` excluded by rule). The campaign caught **five places where naive
FM readings diverge from the silicon-validated reference**, each root-caused
tools-first and recorded in the profile's decisions and the crate's module docs:

1. RTS pulls **PC only** — SR is RTI's shape (13-167/13-168), pinned by the jsr guest
   (U survives both returns).
2. Short immediates to a whole accumulator **sign-extend through A2** — the FM's
   "the remaining bits are zeroed" (13-113) does not hold for A2 (`move #$80,a` leaves
   A2=$FF).
3. **A1/B1 read raw** — the shifter/limiter sits on the whole-accumulator read path
   only (the alu guest stores $FE00FF from A1 with L clear).
4. The sticky **S bit sets on whole-accumulator bus reads only** — subset v0 decodes no
   such read, so S never leaves reset.
5. A 24-bit **keep-mask nibble-slip** in the model's own decode.

The same campaign caught two boundary defects owned and fixed at the model's edge:
accumulator-part move destinations now refuse at decode (a typed stop, not a guess),
and the NOP citation was corrected to 13-145.

## The census before the claim

Before any claim rested on the checkpoint surface, the hidden-state census (SEM-08's
method, re-run for this profile) answered 14 candidates with locators: the A2/B2
readout and A1/B1 raw reads declared and measured, the mode registers bounded at reset
by typed stops, the DO/REP loop state and the observable stale stack slots inside the
observation surface, the pending-writes window measured ABSENT for scalar issue. The
measured consequence: **the canonical end-state dump is the complete architectural
state** for subset v0 — snapshot/replay reduces to the dump fields, the same honesty
the scalar census bought on rv64i-lab-v0.
