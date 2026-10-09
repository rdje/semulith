# DEV_NOTES shard — _(2026-10-06)_ … _(2026-10-06)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-06)_ — a reference stops where its first consumer stopped (P4-SYSTEM.7 slice c5)

`scripts/specfp.py` was tracked at slice (c4) as the FP authority, and its `fma` computed
`(a×b)+c` — enough for `fp.rs`'s vectors, which exercise the backend's one fused primitive.
The corpus needs all four fused forms as the chapter writes them, and the obvious shortcut —
flip a register's sign bit and call FMADD — is exactly how the MODEL does it, so a reference
built that way would check the model against itself. The reference now forms the signed terms
exactly; the sign-flip construction became the cross-check instead (they must agree, and do,
on 464,000 cases; each of two planted mutations is caught). The staged corpus's other lesson
was procedural: the derivation tool imports `scripts/` relative to its own file, so a copy
outside the worktree read the main tree's dossier reader against the worktree's edited
profile — it refused loudly (`undeclared field 'f_single'`), and the re-derivation ran from a
copy placed inside the worktree.

- **Validation:** 464,000/0 (RED 490 and 153,438); 22/22 re-derived byte-identical; 114/114
  on the scratch engine (RED on dropped accrual); identity 103/0 + 11 RED; FP-VECTORS 176.
- Promotion: declined (recorded in the P4-SYSTEM leaf — the signed-term construction is `fma`'s docstring; the independent-construction lesson is the c4 oracle card's).

## _(2026-10-06)_ — the FP model layer, and the oracle that agreed because it shared the convention (P4-SYSTEM.7 slice c4)

`fp.rs` is the RISC-V policy over rustc_apfloat: canonical NaN, NaN-boxing, the rounding-mode
resolution, min/max/compares/class in bits, NaN→int's maximum, the FMA ∞×0 rule, and a
square root of its own (exact integer √ with a sticky remainder — the backend has none). Its
overflow and underflow come from ONE exactly-unbounded value: the same operation in a
backend format of equal precision and a 15-bit exponent, so "rounded as though the exponent
range were unbounded" (IEEE §7.4/§7.5) is computed, not approximated.

Its unit vectors came from a new spec-side reference in exact rationals. Three of 176 failed
on first run — at 2^-126·(1−2^-24), RNE/RUP/RMM, the backend raised no UF — and the cause
was not in `fp.rs`. Slice (a)'s MPFR generator judged UF on the DELIVERED result (the
backend's own convention) and OF on the EXACT magnitude (IEEE judges the unbounded ROUNDED
result): the oracle had agreed with the backend by sharing its rules. Corrected, 72 of the
recorded overflow "deviations" were the oracle's own false positives, and a third backend
deviation (underflow) appeared. SoftFloat's RISC-V specialization, read in source, takes the
IEEE side on both. The decision record carries a dated amendment; the generator and
reference are tracked (`scripts/specfp.py`, `scripts/gen_fp_vectors.py`) and gated by the new
FP-VECTORS doctrine, which also re-checks the reference against the host's hardware IEEE on
directed ties every run (a half-up mutation had survived 1,313 random cases).

- **Validation:** 176/176 spec-side vectors; `fp.rs` vs the corrected MPFR oracle 0/51,840,
  vs the exact-rational reference 0/63,480 (RED: one corrupted line caught by both); FP-VECTORS
  6/6 with the reference-mutation arm; `make check` + `make gate` green.
- Promotion: PROMOTED — docs/knowledge/an-oracle-can-share-the-convention-it-judges.md + INDEX.

## _(2026-10-06)_ — "the cargo cache stays on-volume" was true of one command (P4-SYSTEM.7 slice c4 part 1)

Slice (a) fetched `rustc_apfloat` with `CARGO_HOME=.app-data/cargo-home` and recorded the
cache as on-volume. It was — for that command. Nothing made it true for the next one: no
`.cargo/config.toml`, no `CARGO_HOME` in the Makefile, none in the shell. The workspace had
never had a registry dependency before, so every later `cargo` run silently resolved the
crate through the shared `~/.cargo` (`cargo metadata` named
`~/.cargo/registry/src/…/rustc_apfloat-…/Cargo.toml`). A locality claim about a store is a
claim about EVERY path that reads it; the acquisition path is one of them. The fix is the one
mechanism every cargo invocation in the tree obeys — `.cargo/config.toml` source replacement
to an untracked on-volume directory populated by `make vendor` — and its RED is loud: with the
store absent, cargo refuses to build rather than falling back.

- **Validation:** cargo metadata's path before/after; the shared cache's stat snapshot
  unchanged by a full build; the missing-store failure; `make check` + `make gate` green.
- Promotion: PROMOTED — docs/knowledge/a-locality-claim-covers-every-reader-of-the-store.md + INDEX.

## _(2026-10-06)_ — a move census that reuses the mover's filter cannot see what the filter drops (LIVE-CONTAINMENT.3)

Partitioning TOOLBOX.md's 76-row table, the mover selected rows by `startswith("| \`")`
— and the census that "proved" the move used the same predicate, so it reported 75 of
75 moved, exactly once. One row starts `| any project check's \`--self-test\` |`: no
backtick in its first cell, invisible to both. A second census selecting rows by
POSITION (every table line after the header and separator) found 76 and named the
missing one; the move was re-run from HEAD with the positional selector. The doctrine
partition had the same latent shape (it happened to have no such row). REGISTRY-MIRROR
now also judges the doctrine families' union, so a long-form row lost in a future move
is a gate failure, not an accident of census design.

- **Validation:** 35 + 76 rows each exactly once (positional census); REGISTRY-MIRROR
  13/13 and RED on a removed row; `make gate` green.
- Promotion: declined — the existing card a-survey-that-found-things-can-still-have-missed-things.md
  states the lesson; this entry records its instance.

## _(2026-10-06)_ — a registered pressure control nothing enforces is a wish (LIVE-CONTAINMENT.1)

`docs/TASK_TREE.md`'s registry row has said "one row per active tree; completed trees
leave the index" since SEMULITH-TREES.4 — and the index carried 22 completed trees (of
31) at 8,172 / 8,192 B. Nothing had ever applied the control, and the reason was
mechanical: FRONTIER-SYNC's CLOSURE rule demanded an index row for EVERY tree file, so
obeying the registry would have failed the gate. The two rules contradicted each other
and the enforced one won by default. Now the completed rows live verbatim in
`docs/TASK_TREE_CLOSED.md` (registered, bounded), and FRONTIER-SYNC gates both files:
one row per tree by its status, a completed tree left in the index refused (22 such
findings against the real pre-move index), the leaf-count checks running on the
register too. The book includes both anchors live.

- **Validation:** FRONTIER-SYNC 20/20 (4 new arms); RED 22× on the real pre-move index;
  the move census exact; README-ROUTING-CLOSURE, TREE-CLAIMS, DERIVED-COUNTS green;
  `make book` rc=0; `make gate` green.
- Promotion: declined (mechanized — FRONTIER-SYNC refuses the state this lesson describes).

## _(2026-10-06)_ — a locator that resolves can still name the wrong section (CITATION-ACCURACY.1)

`P4-SYSTEM.7` slice (c3) part 1 found the rv64gc FP-CSR content cited `RVI-F §20.1.1`
(the F register state — real, and wrong: the fcsr is §20.1.2), with every gate green.
The measurement of WHY nothing saw it: `check_citations.py` globs the semantics files
only and asks whether the cited section EXISTS — a wrong-but-real locator passes it by
construction, and no gate read a quote at all. The new tool reads every string atom of
every tracked `.sexp`, attributes a quoted phrase only when the attribution is decidable
(R1 adjacency, R2 a source's leading locator, R3 an expectation step's source, R4 a
single-locator string — 24 of 108 quotes today; the rest counted, never guessed at), and
checks the phrase against the cited section in order, ellipses honoured. Two renderings
of the pinned HTML had to be measured before matching was honest: code literals arrive
quoted (`('pc'+4)`) and dash ranges carry zero-width spaces (`7—\u200b5`). Run against
the real pre-fix files it reports six misses and, for each, the section that does hold
the sentence (§20.1.2) — the refusal names the cure.

- **Validation:** the doctrine's 14 controls pass on synthetic pages; a mutation (the
  matcher forced to always-match) turns 6 RED arms red; HEAD judges 24 quotes, 0
  findings; the pre-fix corpus 6 misses; DERIVED-COUNTS 431 → 445 arms, 34 → 35
  doctrines; `make gate` green.
- Promotion: declined — the lesson is mechanized: the CITATION-QUOTES row in
  DOCTRINE_ENFORCEMENT.md is its retrievable statement, and the gate enforces it.
