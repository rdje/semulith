# DEV_NOTES shard — _(2026-10-01)_ … _(2026-10-01)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-01)_ — the oracle question, answered by census (P3-BREADTH.3, slice 1)

The tree carried an open question — "whether any real DSP oracle becomes available at all" —
and the honest way to answer it was enumeration, not memory: one survey per measured family
over the same enumerator (QEMU/MAME/gem5/GDB-sim/binutils/LLVM/vendor tools/dedicated
projects), one URL per claim, then the two load-bearing positives re-fetched from primary
sources. The answer inverted the tree's prior assumption for two of three families: DSP56300
has a STRONG path (an MIT toolkit whose authors already built the exact differential harness
this project would need, silicon-sealed), SHARC-2106x a PARTIAL one (MAME's BSD-3 core, but
the assembler leg is unbuildable-as-licensed), and only TI C6000 is truly oracle-less (the
vendor discontinued its simulator in 2014). The slice decision — DSP56300 — follows from
RK08's rule (evidence path, not manual convenience) and fits the findings' conditioning: it
activates F1/F3/F6 and leaves F4/F5/F2 unbuilt, recorded rather than lost. Promotion:
declined in the leaf (the survey is dated evidence; its durable output is the decision).

## _(2026-10-01)_ — a dead justification camouflaged a live silent path (P3-BREADTH.2)

The hook audit's only silent escape hatch survived review precisely because it carried a
plausible justification: `extract_operands`' `_` arm skipped operands naming no field,
"because FENCE's `fm`/`pred`/`succ` have no field ranges" — true when written, false since
`P2-SCALAR.1` gave all three fields, leaving the arm unreachable for real data but live for
any future unfielded operand, with enforcement only in a test ratchet whose own whitelist
comment had gone stale in the same way. The fix put the invariant where ARCHITECTURE §2 says
it lives: generation time. `gen_definition.py` now refuses an unfielded operand by name
(rc 2; the DEF-GEN self-test's new RED arm feeds `add` an `rs9` operand and demands the
refusal), the runtime arm returns `ModelError::InvalidDescription` instead of skipping, and
the ratchet is strict. Wider census result: no opaque hooks anywhere — the three seams that
exist (`Environment`, `step_over`, bench `Observer`) are typed contracts that cannot reach
instruction behaviour. Lesson promoted to
`docs/knowledge/a-dead-justification-camouflages-a-silent-path.md` — census the SHAPES
silence takes, then re-measure each justification's premise; never read the comment as the
check.

