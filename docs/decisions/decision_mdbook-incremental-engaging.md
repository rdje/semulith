# The mdBook builds up incrementally and keeps both audiences reading

- **Type:** `decision`
- **Date:** `2026-10-02`
- **Status:** `active`
- **Owner / source:** director directive `2026-10-02`, recorded under `BOOK-APPARATUS`; it
  binds every book this repository writes — the project book (`docs/book/`) and the per-unit
  model books (`docs/models/`) alike, because both are teaching texts
  (`decision_dual-mandate-production-and-teaching`).

## The decision

The mdBook's content **builds up incrementally** — each chapter assumes only what earlier
chapters established — and is written to **keep the reader engaged**. The two failure modes are
named against both audiences: it must not be **too dry**, scaring off students and newcomers,
and not **too slow or too boring** for experts, who must be able to move at their own speed.

## Consequences

- A chapter introduces a term before it leans on it; forward references name where the reader
  can skip ahead. The [Index](../book/src/index.md) and the glossary are the navigation aids
  that make skipping safe for an expert and orientation possible for a newcomer.
- Motivation comes before mechanism: a chapter opens with *why this exists and what breaks
  without it*, then the contract, then the machinery. The measured incident — what actually
  failed — stays in the text, because it is the engaging part and the instructive part alike.
- Density is layered, not averaged: the readable narrative lives in the chapters, and what is
  too technical for a normal chapter lives in an annex (the `2026-10-02` apparatus directive,
  `BOOK-APPARATUS.1`) rather than being diluted into the main line or dropped.
- Every new or revised chapter is reviewed against this record. `BOOK-APPARATUS.2` owns the
  first audit pass over the existing chapters.
