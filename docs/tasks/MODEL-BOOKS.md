# MODEL-BOOKS: one reviewable book per processor model — its materials, and its methodology

## Metadata

- Tree ID: `MODEL-BOOKS`
- Status: `active`
- Roadmap lane: cross-cutting deliverable class; applies to every model from `P0` onward
- Gate: none of its own — it is the surface every other gate's result is read through
- Depends on: `P0-PROFILE` (the first model must exist before it can be documented)
- Unlocks: a reviewer who can judge a model without reading TOML
- Created: `2026-09-14`
- Owner: repo-local workflow

## Goal

Give **every CPU/DSP model its own mdBook**, which does two things the project cannot currently
do for a reader:

1. **States the complete, detailed list of materials** used to specify that model's functionality
   — every specification document, encoding table, reference model and internal contract — each
   pinned by exact identity, with what it supplies **and what it does not**.
2. **Explains the methodology**: how the project got from those initial documents to the model.
   Document → decision → requirement → obligation → check, in prose a reviewer can follow.

Explanation stays **essentially prose**. Code and data snippets appear only where they make a
point faster than a paragraph would; tables are used for the materials list, where a list is the
honest form.

⭐ **And the book carries a second mandate: it is a teaching text.**
`decision_dual-mandate-production-and-teaching` makes every model both signoff production work and
material a student can learn to build production models from — including models capable of running
real compiled code. Concretely, for this tree: the reasoning is recoverable and not just the
result; **the mistakes stay in**, because a matched profile that matched only an instruction set
and a comparator that called a truncated trace agreement are the most instructive pages available;
the *order* of the work is justified rather than listed; and each chapter is written so a reader
could **build** from it rather than only agree with it.

## Why this is a gap, stated as a measurement

Everything a reviewer needs about `rv64i-lab-v0` already exists — and exists as **13 files of
TOML, JSONL and reference prose** inside `profiles/rv64i-lab-v0/`. The project-wide book
(`docs/book/`) narrates the *plan* and the *working practices*; it has no chapter that answers
*"what documents define this processor, and how did you get from them to a model?"*

A materials list that lives only in `sources.toml` is a list the reviewer will not read, and a
methodology that lives only in nine task-tree leaves is a methodology nobody can follow end to end.

## Non-Goals

- **Not a second owner of any fact.** The book renders what `profiles/<id>/` already holds; where
  it states a pinned digest, a count or a verdict, that content is **generated or gated**, never
  retyped. `docs/book/` learned this lesson already — the contracts are included verbatim there so
  the book cannot drift from them.
- **Not a replacement for the project book.** `docs/book/` keeps the plan, the milestones and the
  working practices. A model book is about **one model**.
- **Not documentation of an implementation.** No CPU code exists. A model book documents the
  *specification of the model* and the *route from documents to it* — and must say plainly where
  the route stops.

## Acceptance Criteria

1. Every directory under `profiles/` has a book, and a gate says so — a model without one is a
   model whose materials are unreviewable.
2. The materials list is **complete**: every document that contributed to the model appears, with
   its exact identity (locator, revision, digest, size, retrieval date), what it supplies, what it
   does **not** supply, and its terms. Generated from the pinned data and gated against it.
3. The methodology chapter follows at least one rule **end to end** — from the sentence in the
   source document to the check that will test it — so the pipeline is demonstrated, not asserted.
4. `make book` builds every book, and the project book routes to each model book.
5. Prose dominates. A chapter that is mostly listing is a chapter that has not been written yet.
6. ⭐ Each chapter passes the teaching test: **could a reader build something from this, or only
   agree with it?** Where the project got something wrong, the book says what the wrong instrument
   reported and why it was believed — removing that to look competent removes the lesson.
7. The model's ability to run real compiled code is stated with its **limits**, derived from the
   extension set rather than asserted: no `M` means runtime multiply calls, no `A` means no
   atomics, no `F`/`D` means a soft-float ABI.

## Task Tree

- ID: `MODEL-BOOKS.1` — **the book structure, and the complete materials bill**
  Status: `pending`
  Goal: establish `docs/models/<profile-id>/` as the per-model book (repeatable for every future
  model), and write the materials chapter: every specification artifact, encoding table, reference
  model and internal contract, generated from `sources.toml` / `references.toml` so a digest cannot
  rot, with prose around each explaining its role.
  Acceptance: the generated material tables agree with the pinned data and a gate fails if not;
  every material states what it does NOT supply; `mdbook build` renders it.

- ID: `MODEL-BOOKS.2` — **what the materials do not contain**
  Status: `pending`
  Goal: the chapter a specification bill usually omits. This project measured that its pinned
  artifacts contain **no instruction encodings** (the format diagrams are images), which forced a
  second provenance whose ancestry is shared with one comparator and not the other.
  ⭐ Includes a real investigation: the official specification is also published as **PDF**, and
  whether *that* rendering carries the instruction-format tables as selectable text is unknown. If
  it does, encodings can be re-sourced from the primary document and the shared-ancestry problem
  shrinks. If it does not, the finding is stronger and is recorded as such.
  Acceptance: the PDF is fetched and examined with a tool, not assumed; the outcome is recorded
  either way with the command that established it.

- ID: `MODEL-BOOKS.3` — **the methodology: from document to model**
  Status: `pending`
  Goal: the prose chapter that explains the pipeline — how a sentence of specification becomes a
  decision with an *authority*, how a decision becomes a requirement record with a *semantic
  class*, how a requirement becomes an obligation with positive **and negative** checks, and how an
  expected value is *derived* rather than copied.
  Acceptance: one rule is followed end to end, by name, from its sentence to its check; the
  chapter explains the judgement calls (authority vs semantic class) that are not mechanical.

- ID: `MODEL-BOOKS.4` — **the references, their configuration, and what agreement is worth**
  Status: `pending`
  Goal: how each reference model was obtained, how it was configured to match the profile, what
  the matched-profile control demonstrated, and the independence inventory — in prose, including
  why three models is not three opinions.
  Acceptance: the configuration story is told through the control that changed the observation,
  not through a configuration file listing.

- ID: `MODEL-BOOKS.5` — **the evidence, the gate, and the traceability walk**
  Status: `pending`
  Goal: what has actually been demonstrated, the gate verdict and why it is `incomplete`, and a
  walk a reviewer can repeat: pick a rule, follow it to its requirement, its obligation, its
  declared checks and the experiment that touches it.
  Acceptance: the walk names real ids at every hop and ends at something re-runnable.

- ID: `MODEL-BOOKS.6` — **wiring: every model has a book, and every book builds**
  Status: `pending`
  Goal: `make book` builds the project book and every model book; the project book and `README.md`
  route to each; `doctrine/readme_routes.tsv` governs the new family; a gate requires a book per
  profile directory.
  Acceptance: adding a profile without a book fails the gate; `make book` builds all books.

## Current Frontier

| Order | Leaf | Status | Why next |
| --- | --- | --- | --- |
| 1 | `MODEL-BOOKS.1` | `pending` | the structure has to exist before any chapter can live in it, and the materials bill is the deliverable the reviewer asked for first |
| 2 | `MODEL-BOOKS.2` | `pending` | the honest counterpart to the bill, and it carries a real investigation that may change where encodings come from |
| 3 | `MODEL-BOOKS.3` | `pending` | the methodology, once the materials it operates on are documented |

## Decisions

- `2026-09-14`: a model book lives at **`docs/models/<profile-id>/`**, beside the project book
  rather than inside `profiles/`. `profiles/<id>/` stays machine-readable data that gates consume;
  `docs/models/<id>/` is the narrative a human reads. Putting the book inside the profile directory
  would have mixed the two and pushed a prose tree under bounds calibrated for data files.
- `2026-09-14`: the book **generates or gates** every fact it restates from the profile. This tree
  exists because `MIRROR-DRIFT` had to be written four times over; a new prose surface that retypes
  digests and counts would be a fifth mirror, created deliberately after learning why not to.

## Open Questions

- Does the specification's **PDF** rendering contain the instruction-format tables as text? Owner:
  `MODEL-BOOKS.2`. It decides whether encodings can be re-sourced from the primary document, which
  would materially improve the independence position recorded in `references.toml`.
- Should a DSP model book differ in structure? Deferred until `P3-BREADTH` selects a real DSP
  target; the structure here is built to be repeated, and a second model is what will test that.

## Blockers

- ✅ **Unblocked.** `P0-PROFILE.10` landed: the platform is now matched, four refuted claims are
  corrected at source, and the two irreducible reference differences are enumerated. The materials
  bill is now worth writing, and it has one more thing to say — that a "matched profile" is
  matched on its platform as well as its instruction set.

## Acceptance Checklist (current leaf — `MODEL-BOOKS.1`)

- [ ] **ROOT CAUSE (WHY + WHERE)** — pending
- [ ] **ADDRESSED (verified)** — pending
- [ ] **NO REGRESSION** — pending
- [ ] **FIX** — pending
- [ ] **LOCKSTEP** — pending

## Verification Log

| Date | Leaf | Checks | Result |
| --- | --- | --- | --- |
| `2026-09-14` | `MODEL-BOOKS.1` | `pending` | `pending` |

## Commit Log

| Leaf | Commit subject or reference | Notes |
| --- | --- | --- |
| `MODEL-BOOKS.1` | `pending` | `pending` |

## Changelog

- `2026-09-14`: Created. A model's materials and the methodology that turned them into a model had
  no reviewable home: the facts existed as 13 files of TOML/JSONL under `profiles/rv64i-lab-v0/`,
  and the single project book narrates the plan rather than any one model.
