# A probe's unexpected exception refuses; a self-test judges frozen fixture copies, never live data

- **Type:** `decision`
- **Date:** `2026-10-28`
- **Status:** `active`
- **Owner / source:** the director, 2026-10-28, answering the doctrine-owner questions 6r, 6u and 6x of the XTASK
  leaf ([`decision_director-rulings-2026-10-28.md`](decision_director-rulings-2026-10-28.md)). Authority `director`.
answers: What should a doctrine do when its availability probe crashes, or when its self-test's controls copy live data that is wrong?

## The fact / decision

1. `CITATION-QUOTES` (6r): the availability probe exits 2 — a refusal — on any exception outside the cases it
   names; only a recognised absence is a named skip.
2. `BOARD-VERDICT` (6u) and `STATE-GEN` (6x): the controls run over frozen fixture copies tracked with the
   driver, so a wrong live board or a hand-edited live rv64gc pair fails by name (exit 1) instead of making
   the check refuse as non-discriminating (exit 2).

## Why

A crash that exits 1 reads as an absence (`docs/knowledge/a-crash-that-exits-one-reads-as-an-absence.md`); a
self-test whose controls depend on the live data cannot tell a broken check from broken data.

## How to apply

- One doctrine per unit, each change fired RED: the crashing manifest refuses; the live board rejected and the
  live pair edited each fail by name while the frozen controls stay green. Executed in the `XTASK` tree, whose
  Open Questions carry the three.
