# The materials bill

Everything `dsp56300-lab-v0` is built from, in one place: the pinned specification, the
reference candidate and its legs, and the internal contracts — each pinned by exact
identity, each with what it supplies **and what it does not**.

Two rules govern this chapter, and they are why it can be trusted:

- **The tables are generated.** `scripts/gen_model_book.py` reads the pinned dossier
  (`profiles/dsp56300-lab-v0/sources.sexp` and `references.sexp`, plus the tracked
  contracts) and emits the identity tables below — digests, byte counts, invocations,
  record counts. Nothing in a table is retyped, so a digest cannot rot: the
  `MATERIALS-BILL` doctrine regenerates the tables in memory on every commit and fails if
  they differ from what is committed.
- **The prose is authored, and it is where the judgement lives.** A table can say *what*
  a document is; only prose can say what it is *for* — and, crucially, what it does **not**
  supply. Every material below carries that negative statement, because a bill that lists
  only what things provide is how a project comes to believe it has information it never
  acquired.

## The pinned specification artifact

One document carries the whole architecture the subset is drawn from — and the pin is
NXP's own reference-manual locator, not a third-party mirror, because a publication is
part of the identity (the manual's cover names the family "16-Bit" — a historical
marketing name; the datapath this unit models is 24-bit, and the title is recorded
verbatim because an identity is not edited for sense).

{{#include materials/pinned-specifications.md}}

### `DSP56300FM`

The DSP56300 Family Manual, Rev. 5 (April 2005): the architectural state (§3, §5), the
addressing spaces and AGU, the data ALU and its condition codes, the DO/REP loop
machinery, and the per-instruction forms of §13 that every decode mask and semantic rule
in the crate cites. Two acquisition routes — the materials corpus (via the chipdoc
channel) and a fresh fetch from the pinned locator — were verified byte-equal, so the
corpus copy is the offline fallback and the fetch ledger is the re-derivation route.

**Does not supply:** ground truth where its prose over-applies. The differential campaign
measured five places where naive FM readings diverge from the silicon-validated
reference — the A1/B1 raw reads (the limiter is whole-accumulator-only), the A2
short-immediate sign extension (the FM's "remaining bits are zeroed" does not hold for
A2), RTS pulling PC only, the S bit setting on bus reads only, and a keep-mask
nibble-slip.
Each correction is recorded in the profile's decisions and the crate's module docs — the
FM is the source of the *questions*, and in these five places the measured reference
supplied the answers. Nor does the FM supply any timing this unit may rely on: `cyc` is
informational and never compared.

## The encoding tables

This unit's encoding has a different home than the scalar unit's — declared, not
defaulted:

{{#include materials/encoding-tables.md}}

### `encoding.sexp`

There is **no such document in this unit**, and the absence is a measured decision, not
an oversight. The encoding/definition generalization was measured a lane, not an
extension (`P3-BREADTH.5` slice 3): the pipeline's decode emission is 32-bit-shaped (the
DSP fetches 24-bit words), its semantics language has no memory-space parameter and no
loop state, and no current milestone consumes the work (`decision_lane-consumption`).
The reopening conditions are named: a corpus extension beyond subset v0 (the
parallel-move dual feed), a third unit arriving, or a landing leaf choosing the
machinery route.

**Does not supply:** anything — the document does not exist. What supplies the encodings
instead is the sibling crate's hand-written decoder, every mask cited per form to the FM
and cross-checked against the pinned MIT assembler, whose own encoding leg is upstream's
exhaustive roundtrip against Motorola's official `asm56300` (an upstream proof artifact —
EVD-04, not re-run here).

## The reference candidate and its legs

One candidate, obtained and built on-volume — and the honest warning that **one candidate
is not one opinion**: its assembler and emulator legs share one repository, one author,
one crate workspace. The independent confirmations are upstream's own proof artifacts
(the asm56300 roundtrip; the silicon-sealed difftest corpus), recorded as such rather
than borrowed.

{{#include materials/reference-models.md}}

### `dsp56300`

The primary oracle: `mborgerson/dsp56300` at commit `c60aeedb`, MIT-licensed, built
on-volume from the pinned tarball. Its `difftest` runner produces the canonical
end-state dump this unit's comparison is defined over — registers, deviation-encoded
X/Y/P memory windows, 15 hardware stack slots; steps compared, `cyc` never. The
reference's own `LIMITATIONS.md` bounds every claim axis: SA/SC/DM mode bits stored but
inert, stack extension unimplemented, cache operations NOPs, pipeline interlocks
unmodelled, peripheral-interrupt shapes unverified. Subset v0's exclusions map
one-to-one onto those gaps, which is what makes the subset honest rather than
convenient.

**Does not supply:** a second opinion on its own semantics — the emulator and the
assembler are one project (the independence inventory records the shared lineage), so
Semulith's model derives from the FM, never from this project's decoder tables,
precisely so that Semulith-vs-emulator *is* a second opinion. Nor does it supply an
exact-toolchain-pinned build yet: the upstream pins Rust 1.98.1 and the demonstrated
build ran under the host's 1.98.0 (the crate's `rust-version` floor) to keep the rustup
store off the repository volume — an open item, owned by this profile's model slice, to
resolve before the reference becomes evidence-bearing beyond the demonstrated path.

### `dsp56300-asm`

The assembler leg: turns a guest's tracked `.a56` source into the `.lod` image the
executor consumes. Registered as a first-class candidate (obtained, invoked, digested)
so the compared pair names candidates, not dangling labels.

**Does not supply:** an independent encoding confirmation *for this project* — its
roundtrip against Motorola's `asm56300` v6.3.15 across the full encoding space is
upstream's proof artifact; Semulith has not re-run it (`asm56300` is proprietary and
unpinnable). It supplies the injection route, not the evidence.

### `dsp56300-emu`

The emulator leg: the `difftest` corpus runner that executes a `.lod` image plus a case
meta (load base, stop pc, step budget) and prints the canonical end-state dump.

**Does not supply:** timing evidence (its cycle counts are base-table values —
LIMITATIONS §4 — which is why `cyc` is never compared), nor any per-instruction trace:
the comparison surface is per-CASE end state, and this unit's claim is shaped to exactly
that surface.

### `gearmulator`

The family's second implementation (dsp56300/gearmulator, "The Usual Suspects") —
recorded as a first-class candidate with status **not obtained**: GPL-3.0, which this
project's pinning discipline does not vendor, and its source has not been read.

**Does not supply:** anything this project rests on, today. It is on the bill so that
"the family has a second implementation" is never misread as "we have a second opinion"
— the independence pair (dsp56300 ↔ gearmulator) is recorded `not-examined`, and
whichever leaf first proposes it as an oracle must do that examination first.

## The internal contracts

The materials above are acquired; these are *authored* — the project's own documents,
tracked and gated, that turn the external materials into a reviewable definition.

{{#include materials/internal-contracts.md}}

### `profile.sexp`

The unit's declaration: the subset scope (19 forms in five groups — moves, alu_core,
multiplies, flow, loops — each enumerated and re-derived against the guest corpus by
`EXERCISE-COVERAGE`), the seven decisions with their authorities (architecture vs
laboratory, so a laboratory boundary never reads as an architectural rule), and the
`vehicle` block the gates derive applicability from
(`decision_gate-applicability-by-declared-vehicle`).

**Does not supply:** the source text of any rule — the dossier *cites* the FM by section,
it does not quote it. Nor does it supply evidence that any decision is *implemented*;
that is the crate's and the gates' job.

### `state.sexp`

The architectural-state census carried as data: the five register families with masked
widths and per-part readouts (the A2/B2 sign-extended readout included), the three
memory spaces, the 16-level hardware stack with its observable stale slots, the 12
special registers — and the 14-candidate hidden-state census, whose measured answer is
that **the canonical end-state dump is the complete architectural state** for subset
v0. That answer is what makes checkpoint-level comparison honest here.

**Does not supply:** behavior — the census says what state *exists*; what an instruction
does to it lives in the crate's semantics, cited per form. And the hidden-state "no" is
this subset's, earned by its exclusions: every exclusion reopens its candidate row.

### `requirements.sexp`

The predeclared requirements, one per profile decision, each statement byte-identical to
its decision (the `RECORD-SCHEMA` COVERAGE rule), each with its FM locator and semantic
class.

**Does not supply:** evidence. A requirement records what the source *says* and where;
that the model *does* it is the guests' and gates' job.

### `contract-obligations.sexp`

The environment contract (`dsp56300-lab-env-v0`): the seven decision mirrors plus six
environment-assumptions — no guest-reachable time source, sequential scalar issue, cold
reset, 24-bit P-space fetch supply, no asynchronous events, instruction-level atomicity
— each carrying a positive **and** a negative required check.

**Does not supply:** the checks' existence as running code. The 26 checks are declared;
no milestone has routed their fixtures, which this book states rather than papers over.

### `guests/`

The synthetic guest corpus: six `.a56` programs plus their case metas, each assembled by
the pinned assembler and run under both the model and the reference, compared as
canonical end-state dumps. Synthetic means exactly that: evidence about the *path* and
the *model*, never about any real DSP program.

**Does not supply:** proof. Six guests is finite, tested evidence (EVD-01) — and the
corpus does not supply its own coverage claim: the denominator lives in the profile's
scope, and `EXERCISE-COVERAGE` re-derives the 19/19 ratio at every commit.

### `interactions.sexp`

The declared interaction matrix for subset v0: six axes — progress, stop, loop, stack,
alias, state — and 21 cells, each dispositioned to a mechanism or a degenerate-with-
reason (the corpus is checkpoint-compared, so no guest cells). The `INTERACTION-MATRIX`
gate re-derives every cell from the axes and refuses an omitted one by name.

**Does not supply:** the executions themselves — the matrix is the *declaration* of what
must be exercised; the smoke driver and the crate's tests are the exercise.
