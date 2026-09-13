# Introduction

**Semulith builds trustworthy CPU and DSP software models in Rust, then composes validated
processor profiles into boards and complete computers capable of running Linux.**

This book is the project's review surface. It is written to be read instead of the code: it
carries the plan, the normative contracts, the data contracts, and the discipline that decides
when a claim about a processor model is allowed to be made.

## The shape of the project

The first deliverable is **the processor** — not a boot, not a demo. One canonical executable
definition per processor, a readable reference interpreter, and reproducible evidence for a
precisely stated supported profile. A board is implemented only after the processor profile it
will use has passed its gate. A software computer follows the board.

That ordering is the whole design. An emulator that boots something is easy to produce and
almost impossible to trust; the interesting engineering is in being able to say *exactly* what
is supported, under exactly which assumptions, with evidence someone else can re-run.

## Why the discipline is in the foreground

Most of what makes a processor model trustworthy is not code. It is:

- knowing which specification revision a behaviour came from, and where;
- knowing whether a "second opinion" really is one, or shares an ancestor with the first;
- knowing that a passing test suite is *tested evidence for those cases*, never a theorem;
- knowing which evidence a change just invalidated.

So this book gives those contracts the same weight as the implementation plan, and the
repository enforces the mechanizable parts on every commit rather than trusting anyone to
remember them.

## A second consumer: archogen

Semulith is not only aimed at Linux. **archogen** generates specific-purpose operating systems
from **eADL**, its functional source of truth, and needs explicit platform contracts to execute
and validate them. eADL describes hardware and OS functionality without implementation;
archogen's engine resolves realizations; Semulith owns the executable hardware models. An
archogen OS can be a smaller, earlier system workload than Linux — with its own gate.

## How to read this book

- Start with [What is claimed, and what is not](claim-scope.md). It is short and it is the most
  important page here.
- [Current status](status.md) is included live from the repository's own tracker, so it cannot
  drift from the file the project maintains.
- The contract chapters each open with orientation and then include the canonical document
  verbatim. The book never paraphrases a contract — a paraphrase is a second owner, and this
  project's first rule is that a rule has exactly one.
