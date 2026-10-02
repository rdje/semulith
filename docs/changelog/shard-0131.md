# DEV_NOTES shard — _(2026-10-01)_ … _(2026-10-01)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-01)_ — the bounded subset, chosen against the gaps (P3-BREADTH.4, slice 1)

Selecting a "narrow real slice" is itself measurement work, not preference. Three censuses
did the deciding: the pinned reference's `Instruction` enum (its decode is DSP56300-complete,
so coverage bounds nothing), its `LIMITATIONS.md` read in full (SA/SC/DM mode bits inert,
stack extension absent, peripheral interrupts unverified, cycle counts base-table only —
each gap became a named exclusion, because evidence cannot outrun the oracle's own honesty),
and the difftest harness's comparison contract (checkpoint-level canonical end-state:
registers, deviation-encoded X/Y windows, 15 stack slots; `steps` is the compared counter,
`cyc` informational forever — a simpler shape than the RISC-V per-instruction commit walk,
and a different one: a per-case comparator, not a first-divergence walk). The subset that
survives is `dsp56300-lab-v0` v0: non-parallel moves with the A2/B2 extension readout (F6's
named case), the immediate/register ALU core, signed `mpy`/`mac`, `nop/jmp/jsr/rts`,
`do`/`enddo`/`rep`, linear addressing. The hardest call was excluding parallel moves — the
defining DSP shape — and the honest way to exclude something load-bearing is to name it as
the first extension candidate rather than let it slip out silently. The vehicle (a sibling
crate, manual-derived, EXPERIMENTAL) followed from the tree's own routing: the pipeline
refuses a second unit by name and that generator work is `.5`'s; building the generalization
before its exercising target exists is the speculative generality P3 was created to refuse.
Two gaps surfaced and were routed, not smoothed over: the profile schema's scope taxonomy is
scalar-named (a `.5` named case), and the auto-discovering gates have never met a second,
deliberately partial profile (the dossier slice's first measurement).

## _(2026-10-01)_ — the evidence path, run for real (P3-BREADTH.3, slice 2)

A survey says a path exists; only running it proves it reproduces here. The DSP56300 route
pinned (commit `c60aeedb`, sha256-recorded tarball under `target/refs/`, the RISC-V
references' own discipline), built on-volume (31.7 s; the upstream's 1.98.1 toolchain pin
sidestepped with `RUSTUP_TOOLCHAIN=1.98.0` because installing it would write the OFF-VOLUME
rustup store — §13 applies to reference builds too), and exercised with a synthetic micro
guest: assembler rc 0, emulator rc 0, 16 steps, canonical dump. The value of the demo was in
the verification, not the run: hand arithmetic reproduced the 56-bit accumulator to the bit
(`001f253d515280`), the memory deviation dump proved the X/Y-space stores landed where
aimed, and the one value that looked wrong (`move #$5,x1` → `x1=050000`) traced to the
family manual's §3.4.1.3 (an 8-bit short immediate to X0/X1/Y0/Y1 is a fraction stored in
bits 23–16) — a reminder that on an unfamiliar ISA the FIRST reflex is "the toolchain is
wrong" and the correct one is "read the manual's move semantics". Promotion: declined in the
leaf (dated evidence; its durable output is the demonstrated path, recorded in the tree).

