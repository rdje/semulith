# DEV_NOTES shard — _(2026-09-30)_ … _(2026-09-30)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-30)_ — addressing and address spaces; the vendor-diversity filing (DSP-REVIEW.3 + DR-0087)

Q6 measured first per the acceptance: bytes on both sides, one numbering — the lab's
units answer holds for these targets. The interesting findings are the seams: AMR (a
control register carrying addressing mode — the lab has no CSR surface), the .D units
as the only address generators with cross-file routing, two L1 spaces against the lab's
identical fetch/data maps, circular addressing on a NAMED register subset. Measured
absences done right (named searches): no bit-reversed ADDRESSING (BITR is a data op), no
strided modes, no word-addressed space. The vendor sweep measured the corpus, not memory:
adi/dsp/sharc exists EMPTY, no Motorola/NXP DSP line exists — two gaps filed through the
(now two-way) channel; the C55x want dissolved (already catalogued — my first edit
duplicated its id and the materials gate refused by name; the duplicate was removed, the
gate's refusal is the recorded evidence the census exists). Four more manual defects
recorded unresolved, incl. the AMR table's row-shift and the cross-chapter alignment
precondition.

Lesson: `promotion: declined` (recorded in the leaf).

## _(2026-09-30)_ — the rounding/saturation survey (DSP-REVIEW.2)

The manuals write the ordering as inline arithmetic, so the leaf records it that way:
multiply → accumulate → round-add → shift/saturate → narrow, per instruction, quoted.
Two measurements deserve their names: the flag side effect is per-instruction DATA
(SADD2's own entry says it does NOT set the SAT bit — a model that derives "saturated ⇒
flag set" is wrong by construction), and SAT's update lands one cycle after the result
(the delayed-effect shape the tree predicted). The seven manual defects are recorded with
quotes and NOT resolved (upstream facts; our intuition is not their authority) — the
DOTPNRSU2 32-vs-33-bit intermediate split is a core-version profile-pinning obligation.
In-flight authoring slip owned: a fabricated filename went into a checklist's recorded
output block in the first draft; measured, corrected to the real pasted output, and noted
in the block itself.

Lesson: `promotion: declined` (recorded in the leaf).

## _(2026-09-30)_ — the DSP widths survey (DSP-REVIEW.1)

Method matters more than findings here: pdftotext extraction of the three catalogued TI
C6000 manuals, every fact quoted with page+section, every ABSENCE measured by named
searches (`guard` = 1 boilerplate hit; `Q15` = 0; `Q31` = exactly 1). Findings: no
accumulator/guard machinery anywhere in the family (accumulation is explicit ADDs — a
measured non-finding that stops anyone adding accumulator state speculatively); the
40-bit long/64-bit pair/128-bit quad width ladder (quads C66x-only) with the odd:even
zero-fill rule; scaling carried by instruction MNEMONICS (the S-family <<1+saturate,
MPYIHR's round), not mode bits — the opcode-map `s` bit is the A/B side-select, a trap
measured and recorded in the artifact. The classification seed for .7: register grouping
with a width+fill rule. Also fixed in passing: the tree's G1 blocker (long resolved) and
LIVE_STATUS's P2 row (stale at 8/9 from an aborted multi-file edit — its MEMORY half had
died on an assertion before writing, and only some of the files went in; measured now).

Lesson: `promotion: declined` (the method is the leaf's acceptance; the trap lives in the
artifact where the next reader meets it).

Detailed technical notes — root cause, implementation, validation — per slice. The
engineering-continuity surface (not the public docs; that's `docs/book/`). Newest first.

## _(2026-09-30)_ — the CPU-LAB report and the experimental release (P2-SCALAR.9, slice c; the tree closes)

The report's probes are all static over tracked artifacts (the generator's byte-stability
rule): the obligations census reuses G0's exact probe (concrete check ids vs tracked
executables — measured 0/72 today), the requirements census is read from the catalogue
(28 planned + 1 partial — so G-OBLIGATIONS reads open on the record's own terms), the
matrix/campaign/portability/replay axes read their tracked records (interactions.sexp,
act4.sexp, portability.sexp, the suite census). The verdict rule has no path to `passed`
over an open axis (EVD-08). The named decision: experimental release of the versioned
artifact (dossier digest in the report), the closing conditions enumerated. Defect owned:
the G0 limitation "No CPU model exists" was P0 prose, stale since the interpreter landed
— fixed in the generator, and the repair is regenerable (GATE-REPORT). MEMORY's
active-trees count sat at 6/9 across the .7/.8 commits (edited around, not in) — cosmetic
resume-pointer drift, caught and corrected at closure; TREE-CLAIMS would have caught a
contradiction at the tree's close, which is exactly what the line now does cleanly.

Lesson: `promotion: declined` (the axes' state lives in the generated report; the
decision record carries the reasoning).

