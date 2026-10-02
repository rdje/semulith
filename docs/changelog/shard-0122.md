# DEV_NOTES shard — _(2026-09-30)_ … _(2026-09-30)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-30)_ — TI's absences are TI's (DSP-REVIEW.8)

The review extracted three TI manuals first, and the absence facts it pinned (no
accumulator, no guard bits, no bit-reversed addressing) were one lazy reading away from
becoming "DSPs don't have accumulators". The two manuals the chipdoc channel answered
the same day measured the opposite: DSP56300 has two 56-bit accumulators with 8-bit
extension registers, SHARC has 80-bit accumulators and prints the words "guard bits",
and both have bit-reversed addressing. The `.4` break — the execute packet and the
delayed visible writeback — is now scoped where it belongs: TI-family-shaped, not
DSP-shaped, with SHARC's interlocked five-stage pipeline as the printed counterexample.
A finding's scope is only ever as wide as the corpus measured so far; the tree's own
rule (a TI absence is never restated as a DSP absence) is now armed for `.7`'s report.
Also recorded, fourth time this day: an unmeasured number composed into a checklist
(9 and 11 written where the tool said 14) — caught pre-commit, again. The practiced
rule holds: paste real output, never compose it.

## _(2026-09-30)_ — the packet and the delayed writeback (DSP-REVIEW.4)

The tree named this leaf "the single most likely place the scalar abstraction breaks"
and the measurement agreed — twice. The packet: ≤8 instructions, all operands read at E1
simultaneously (Table 3-3's read cycles are all "i"), one functional unit each — so two
stores to one address have a joint outcome that instruction-stepping miscomputes. The
delayed writeback: load results land at i+4, interlocks are eliminated BY DESIGN ("no
stall is introduced if the register being read has data placed by a load"), and the
manual's own §5.7.1 worked example shows an interrupt inside the window producing
incorrect results — the exact delayed-effect shape .2's SAT measurement fed in. The
third unmeasured-number slip of the day happened in this leaf's checklist (101 measured
after 21 was composed) — the practiced rule is now "paste real output, never compose",
and it is written into the leaf's own checklist block where the next author sees it.

Lesson: `promotion: declined` (the breaks are the artifact's own section).

## _(2026-09-30)_ — the synthetic boundary fixture (DSP-REVIEW.6)

The design question was what "through the real API" means, and the answer was measured:
gen_state.py's refusal list is the boundary's own documentation (the unknown dossier
name, the XLEN owner split, the second profile id, the nonstandard width — each refused
by name), and the schema layer refuses the packet/space/delayed-effect shapes the same
way. The fixture pins the REFUSALS — green while the boundary stands, RED the day a
shape becomes supported (the fixture measures the boundary moving, which is its whole
purpose). The packet descriptor was reduced until its ONLY refusal is `packet` itself
(the kind/requires/source fields satisfied first, so the pin measures the construct,
not descriptor hygiene). The vendor gaps filed with .3 were answered same-day (the
2026-09-30 DSP batch) and their channel contract now lives in
`docs/knowledge/the-chipdoc-channel.md` (adopted per Policy 12: the content copied in,
never depended on externally).

Lesson: `promotion: declined` (recorded in the leaf; the channel contract is the
knowledge card's).

## _(2026-09-30)_ — the loop/restart survey (DSP-REVIEW.5)

The measured content: SPLOOP's full state census (buffer + hidden LBC ×2 + ILC + RILC +
SPLX), the drain-vs-no-drain asymmetry between interrupts and exceptions (§7.13.1 vs
§7.13.3 — the leaf's load-bearing fact: a restart model treating them alike is wrong by
construction), the not-interruptible formula for short loops, and restart as
re-execution under modified rules. The SEM-04 framing (the acceptance): per-instruction
completion holds across interrupts; the persistent loop state is exactly ILC + refill;
the .4 break stands beside it. MFENCE measured C66x-only (0/34/0 hits); its violated
restrictions are undefined-by-omission. DMA ordering is out of ALL three CPU manuals by
their own deferral — the catalog's answer must cite the programmer's guide; recorded so.

Lesson: `promotion: declined` (recorded in the leaf).

