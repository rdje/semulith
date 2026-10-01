# DEV_NOTES shard — _(2026-09-30)_ … _(2026-09-30)_

> Sharded from `DEV_NOTES.md` when it crossed its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-09-30)_ — strand 3 designed: eight measured gaps, two probes, one defect (P2-SCALAR.5)

Directed-sequence design started from a census, not intuition: every candidate was checked
against the tracked guests' sources AND expectation documents, the disassembled compiled
guest, and the ACT4 testplan/bodies. Verdicts: run-off-the-end is uncovered on semulith
(the harness budget equals the expectation count, so the fall-through fetch never happens
— a harness-shape finding, not a guest gap); load→use-as-address exists nowhere (every
jalr base is materialized, never loaded — and `c-scope.c`'s "indirect jump through a
switch" was constant-folded out of its ELF: logged defect, comment corrected in-strand);
the sign-extending cross-width round-trip matrix is pinned only for same-width pairs;
store→fence→execute is unpinned (`fault-selfmod` is the no-fence shape); slt→branch
chains are unpinned (ACT4's slt is compare-and-store); no loop loads AND stores per
iteration; deepest pinned serial chain is 7–8 (single-producer); six load widths and six
*W forms lack x0-destination success-path pins. The two behavior-uncertain candidates were
probed three-way before authoring: the zero word past a program traps illegal-instruction
(0x02, tval 0, word 0) on all three models (sail `c.illegal`, spike `c.unimp`, semulith
the policy conversion — the existing adapters read all three spellings), and a patched
word stays visible through `fence rw,rw` on all three (x2 ← 7). Eight guests designed,
each with its matrix cell named; ceiling expansion pre-stated per the `.1` rule.

Lesson: `promotion: declined` — the census verdicts carry their citations in the leaf;
the probes' traces are the measurement record the guests will re-pin as tracked evidence.

