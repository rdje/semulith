# DEV_NOTES shard — _(2026-10-01)_ … _(2026-10-01)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-01)_ — the census as a harvest, not a rewrite (P3-BREADTH.1, the F6 leg)

F6 is the finding that the hidden-state census reopens per profile; the live question was
what "re-run" means when this profile's `state.sexp` is deferred to `.5`. Answer: the
census lands as a measured record, not a schema document — `.5`'s named cases (special
registers, F1 widths, F3 spaces) harvest it. The substantive content was already earned by
the differential campaign: the A2/B2 sign-extended readout, the A1/B1 raw reads, S's
absent writer, the stale popped stack slots that are hidden from the programmer but inside
the dump. The census's own contribution is the surface-completeness argument — before
asking "is anything hidden?", prove the observation surface covers every mutable cell:
stack slot 0 is unwritable by the pre-incremented SP, P below the deviation window is
constant because subset v0 decodes no P-space write, and the harness's private X window is
excluded by the harness's own contract on both engines. With that argument in place the
6/6 agreement becomes a completeness measurement, not just an equality measurement. The
scalar census's seven candidates were re-asked verbatim; three flipped to "absent
architecturally" (no reservation mechanism, no FP, no vector unit exist in the family to
hide), and the fetch-cache answer came out one step stronger than rv64's — the DSP56300
has no instruction cache at all.

## _(2026-10-01)_ — where the manual and the silicon part ways (P3-BREADTH.4 slice 4)

Form-coverage completion for `semulith-dsp56300` was a decode exercise plus a semantics
arbitration exercise. The decode side was routine in the good way: FM figures give the
shapes, the pinned assembler's probe words confirm every mask (one probe misalignment on
my side — reading the lod two lines off — caught instantly by the pinned decode test).
The semantics side is where the differential campaign earned its keep: first smoke run
was 2 agree / 4 fail, and every failure was a real model defect with a distinct root
cause. RTS restores PC only, not SR (FM 13-168 was right; my 56000-style assumption was
wrong — the jsr guest pins it: the U bit survives both returns). A short immediate to an
accumulator sign-extends through A2, falsifying the FM's "remaining bits are zeroed"
prose. A1/B1 memory reads are raw — the shifter/limiter lives on the whole-accumulator
read path (my FM-derived limiter on A1 was an over-application, refuted by a stored
$FE00FF). The S bit sets only on accumulator bus reads, so no subset-v0 path sets it at
all (an ASR of a negative accumulator proved it). And a keep-mask nibble-slip
(`0xFF00…` for `0x00FF…`) zeroed A2 on the 24-bit logical ops — the kind of bug the
reference's b2=$FE dump line makes instantly visible. Guest-side lesson: the assembler
will shorten `move #$000002,x1` to the fractional short form; `#>` forces the long form,
and the model's typed OutOfWindow stop is what caught the runaway. The reference's emit
source was used to LOCATE mechanisms (TOOLBOX); every rule's evidence is the dump
agreement, so EVD-04's independence ledger is unchanged and the claim stays
EXPERIMENTAL.

