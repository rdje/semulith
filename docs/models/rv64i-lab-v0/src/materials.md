# The materials bill

Everything `rv64i-lab-v0` is built from, in one place: every specification artifact, the
encoding tables, every reference model, and the internal contracts — each pinned by exact
identity, each with what it supplies **and what it does not**.

Two rules govern this chapter, and they are why it can be trusted:

- **The tables are generated.** `scripts/gen_model_book.py` reads the pinned dossier
  (`profiles/rv64i-lab-v0/sources.sexp` and `references.sexp`, plus the tracked contracts)
  and emits the identity tables below — digests, byte counts, versions, invocations,
  record counts. Nothing in a table is retyped, so a digest cannot rot: the
  `MATERIALS-BILL` doctrine regenerates the tables in memory on every commit and fails if
  they differ from what is committed.
- **The prose is authored, and it is where the judgement lives.** A table can say *what*
  a document is; only prose can say what it is *for* — and, crucially, what it does **not**
  supply. Every material below carries that negative statement, because a bill that lists
  only what things provide is how a project comes to believe it has information it never
  acquired.

If you are building your own model, read this chapter as a *buying list with warnings*:
each entry tells you what to acquire, exactly which it is, what you will get from it, and
the assumption you would otherwise make that it does not support.

## The pinned specification artifacts

The specification is the **RISC-V Ratified Specifications Library at docs.riscv.org**,
revision `v20260120` — and the pin is the publication, not the repository: the GitHub
`riscv-isa-manual` releases carry *different section numbering*, and this project learned
the hard way that a version string is not an identity (see
`docs/knowledge/a-version-string-is-not-an-identity.md`). Every citation in the dossier
resolves against these exact bytes, offline, via `scripts/check_citations.py`.

{{#include materials/pinned-specifications.md}}

### `RVI-INTRO`

The introduction to the unprivileged library. This is where the *vocabulary of honesty*
comes from: the execution-environment interface (EEI) and hart definitions, the four
effects a trap can have, and — load-bearing for everything this laboratory does with
reserved encodings — the meaning of **UNSPECIFIED**. When a reference model and this model
legitimately disagree (the `fence.i` case), it is this document's UNSPECIFIED rule that
makes the disagreement legal.

**Does not supply:** a single instruction's semantics or encoding. It defines the frame —
what a hart is, what a trap may do, what "unspecified" permits — and no instruction's
behavior. A model built from this document alone would execute nothing.

### `RVI-RV32I`

The base integer instruction set, chapter 1.1, version 2.1 — the semantic heart of the
model: register state, the instruction formats, control transfer, load/store, FENCE,
ECALL/EBREAK, and the HINT tables. RV64I is written as a *set of deltas* against this
chapter, so nearly every rule in the dossier cites it. Its prose is where every guest
expectation value is derived from before any model runs (EVD-05).

**Does not supply:** the RV64 deltas (those are the next artifact), and — measured, not
assumed — **any instruction encodings**. The format diagrams in this chapter are *images*:
`grep -cE '[01]{7}'` over the pinned bytes returns 0. The semantics are all present in
prose; the bit layouts are simply not in the document. That measurement is what forced
the second provenance below.

### `RVI-RV64I`

The RV64I chapter, version 2.1: XLEN=64, the `*W` instruction family, the 6-bit shift
amounts, LWU/LD/SD, and the RV64I HINT table. Short enough to read end to end — which
you should, because this chapter plus the one above *is* the whole instruction
specification of this unit.

**Does not supply:** the base rules it modifies (it is a delta document — read it
together with `RVI-RV32I`, never alone), and again no encodings, for the same measured
reason. It also does not say how the *W forms' sign extension interacts with a garbage
upper half — that rule is derived from its prose ("ignoring the upper 32 bits") and is
pinned by the `bound-arith` guest, not quoted from a table.

## The encoding tables

The one place this model's definition comes from somewhere other than the specification —
and this section is the honest account of that, because the project first *recorded it
wrong* and then corrected itself.

**The measured gap.** The three pinned artifacts above contain no instruction encodings
(the format diagrams are images; the measurement is the grep above, run over all six
pinned artifacts at acquisition time). Semantics in prose, encodings nowhere. So the bit
layouts had to come from somewhere else, and that somewhere is recorded as its own
provenance rather than blurred into "the specification":

{{#include materials/encoding-tables.md}}

### `RISCV-OPCODES`

RISC-V International's machine-readable opcode tables: the fixed bits and operand lists
per instruction (`rv_i`, `rv64_i`), the operand field positions (`arg_lut.csv`), and the
B/J scrambled-immediate layouts (`constants.py`) — which the pinned specification renders
only as images. The project's assembler *parses* these files and refuses any immediate
layout whose accounted bits do not total the field width; it carries no opcode constant of
its own, so a typo cannot invent an instruction (see the project book's assembler annex,
`docs/book/src/annex/assembler.md`).

⭐ **The shared-ancestry statement, plainly.** This source is *upstream of Spike* — whose
`encoding.h` declares itself generated from it — and **not** of the Sail model, which
hand-writes 59 files of `encdec` mappings and never mentions it. So when Sail decodes the
project's guest bytes as intended, that is a genuinely *independent* confirmation of the
encoding; when Spike does, it is not — it is the same table answering twice. The project
initially recorded "our encodings are confirmed by the references" without this
distinction; the independence inventory in `references.sexp` is the correction, and it is
why the differential's encoding leg rests on Sail alone. The follow-up question — does the
official specification's **PDF** rendering carry the format tables as selectable text,
which would let encodings be re-sourced from the primary document — was investigated with
a tool at `MODEL-BOOKS.2` and answered **yes** (same publication, same revision; the
evidence and its two qualifications are in the gaps chapter). The re-sourcing itself is
future, reviewed work, not done today.

**Does not supply:** semantics. These tables say which bits mean *which instruction*,
never what the instruction *does* — no expected value, no trap behavior, no boundary rule
is ever derived from here. It also does not supply the B/J immediate layouts as prose:
`constants.py` states them as descriptors the assembler must parse and self-check, and a
layout it cannot reconcile is one it will not use.

## The reference models

Three obtained implementations and one deliberately-unacquired test corpus. A reference
here is a *differential partner*, never a source of truth: agreement is tested evidence
for these inputs, and the dossier records what each model actually is — including the two
that were tried and rejected as routes, and the one whose independence is unexamined.

{{#include materials/reference-models.md}}

### `sail-riscv`

The primary oracle candidate: the RISC-V International reference formal model, release
0.14, a prebuilt binary pinned by digest. It is the reference that can be *configured to
match this profile's whole platform* — memory regions, no CLINT, no interrupt generator —
via the tracked override, and it is the encoding-independent comparator (above). The
matched-profile control that demonstrated what configuration is worth: flipping its
misaligned policy back to "handled invisibly", changing nothing else, produced a real
divergence against Spike — the two models agree *because* the profile is matched.

**Does not supply:** an independence guarantee for expected-value derivation (ACT's
signatures are computed by a configured Sail model — see `act4`), nor the *effective
merged configuration* — measured: the model will not emit it (`--print-default-config`
ignores the override), so the effective configuration is recorded as (release default) +
(tracked override), and the merge is ours, not the model's report. And notably it does not
supply a 64-bit-wide access-fault tval: measured at the interaction-matrix design probes,
sail 0.14 masks it to its 56-bit physical-address width (`DIFF-TVAL-PHYS-MASK`).

### `spike`

The second implementation: the historical golden model, built from source at a pinned
commit. Its commit-level trace vocabulary drove the adapter's most important rule — Spike
emits *no* commit record for a trapping instruction, and reassembling that split record is
what stopped a truncated trace reading as agreement (the lesson the comparator's
length-mismatch refusal now enforces).

**Does not supply:** a matched platform. Spike bundles a *board* with its CPU — a
core-local interruptor, a PLIC, a UART — and offers no option to remove them
(`DIFF-PLATFORM-SPIKE`), so guests touching its device addresses disable the Spike
comparison and print the skip. Nor does it supply encoding independence: its encodings
are generated from the same riscv-opcodes tables this project parses, so Spike agreeing
with our bytes is the same table agreeing with itself.

### `qemu`

The third implementation, obtained as a pre-existing host binary and never exercised:
no matched configuration, no ISA string read back (QEMU emits none), and its independence
from both comparators is **unexamined** — recorded as `not-examined` rather than omitted,
because an omitted pair reads exactly like an independent one.

**Does not supply:** anything this project currently rests on. No evidence names it. It is
on the bill precisely so that "we have three models" is never misread as "we have three
opinions" — and so that whichever leaf first proposes QEMU as a comparator must do the
independence examination *before* its agreement counts.

### `act4`

The RISC-V architectural test corpus — a set of tests somebody else chose, located, and
**acquired as a sparse partial** (`2026-09-30`, `P2-SCALAR.5` strand 2): a blobless clone
pinned at commit `e2216915…` holding only `tests/env/`, `tests/rv64i/I/` and `config/`
(45 MB of the ~672 MB tree — the RV64I campaign needs nothing else), standing untracked at
`target/refs/riscv-arch-test/` beside the reference binaries. The docs and test-plan half
remains the catalogued material `RISCV-ARCH-TEST-ACT4`.

**Does not supply:** a second opinion, ever. ACT computes its expected results using a
*configured Sail model*, so ACT agreeing with sail-riscv is one semantics answering twice
— the single most important lineage fact in the dossier. ACT's value, as `P2-SCALAR.5`
takes it up, is *external tests*, which is a different kind of value from independence.

## The internal contracts

The materials above are acquired; these are *authored* — the project's own documents,
tracked and gated, that turn the external materials into a buildable definition. They are
on the bill because a reviewer must be able to see the whole chain: the specification
says, the dossier decides, the contract obliges, the guests pin. The counts below are
derived from the tracked files at generation time; `RECORD-SCHEMA`, `PROFILE-CONSISTENCY`
and the generation gates keep the documents themselves honest.

{{#include materials/internal-contracts.md}}

### `profile.sexp`

The unit's declaration: the scope (52 instruction forms, enumerated — the count is
re-derived against the enumeration by `EXERCISE-COVERAGE`), and every design decision
with its *authority* — `architecture`, `execution-environment` or `laboratory` — so a
laboratory policy over an UNSPECIFIED case can never read as an architectural rule.

**Does not supply:** the source text of any rule — the dossier *cites* the pinned
artifacts by section, it does not quote them; a decision without its citation is refused
by `PROFILE-CONSISTENCY`. Nor does it supply evidence that any decision is *implemented*.

### `state.sexp`

The architectural-state census: the 32 integer registers, x0 hardwired, the program
counter — and the **hidden-state census**, the explicit answer to "is there state this
list does not show?" (for this profile: *no*, and only because of what the profile
excludes). The generated Rust state module is a byte-exact function of this document
(`STATE-GEN`).

**Does not supply:** behavior. The census says what state *exists* and its reset values;
what an instruction does to that state lives in the semantics fragments, not here. And it
does not supply the hidden-state answer for any *other* profile — the "no" is this
profile's, earned by its exclusions, not a reusable constant.

### `encoding.sexp`

The composed encoding space: which fragments the unit composes (`riscv/rv64i`), resolved
through the one shared resolver, collision-free, with the composition decided
(`UNIT-COMPOSITION`). This is the document that makes "52 instructions" an enumerable set
rather than a claim — the same set the decoder, the requirements and the guests are all
checked against.

**Does not supply:** semantics, again — the encoding space says which words decode to
which instruction; the effect of each instruction is the semantics fragment's fact
(`definitions/riscv/rv64i.sem.sexp`), and `EXTRACTION` refuses a unit where the two sets
diverge.

### `requirements.sexp`

The predeclared requirements — one per profile decision, each with a source locator, a
semantic class (`defined` / `undefined` / …), and a research status that cannot read
`resolved` while carrying an open question (the `RECORD-SCHEMA` rule written after exactly
that pair was found convenient to hold).

**Does not supply:** evidence. A requirement records what the source *says* and where;
that the model *does* it is the guests' and gates' job. A requirements catalogue is a
promise with citations, and this one is gated to stay that way rather than drifting into
a claim.

### `contract-obligations.sexp`

The environment contract (`rv64i-lab-env-v0`): what the laboratory around the model owes
— fetch supply, partial progress, event delivery, boundary answers — each obligation
carrying a positive **and** a negative required check, because a contract that only
describes the cases that already work is how a laboratory quietly stops testing the hard
half.

**Does not supply:** the checks' existence as running code. The obligations *declare* the
checks; whether any executable names them is what gate `G0` measures — and it reads
`incomplete` today, which this book states rather than papers over.

### `guests/`

The EVD-05 guest corpus: independently encoded programs whose every expected observation
was derived from the pinned specification prose *before any model ran* — an expected value
copied from a model's output tests self-consistency and nothing else. The guests are the
executable half of the bill: the offline differential re-runs them against these
expectations on every commit, and the live smoke runs them against both references.

**Does not supply:** proof. Forty guests and 492 aligned steps is finite, tested evidence
— explicitly not universal trace inclusion, and the two references can agree while both
are wrong where they share ancestry. The corpus also does not supply its own coverage
claim: the denominator lives in the profile's scope, and `EXERCISE-COVERAGE` re-derives
the ratio.

### `interactions.sexp`

The declared interaction matrix (P2-SCALAR.4): the six axes — fault, alias, boundary,
event, progress, restart — and the 21-cell upper triangle, each cell dispositioned to
guests, a mechanism, or a degenerate-with-reason. Declared first as data, then exercised;
the `INTERACTION-MATRIX` gate re-derives the cells from the axes and refuses an omitted
one by name.

**Does not supply:** the executions themselves — the matrix is the *declaration* of what
must be exercised; the guests and the determinism suite are the exercise. Nor does it
supply the axis definitions' authority: the axes are grounded in the dossier's own layers
(the `.2`/`.3` evidence layers, the environment contract's obligations), stated in the
document's preamble.

## What this bill deliberately records as *not* routes

Three acquisition routes were tried and rejected, and they stay on the record
(`references.sexp`, "attempts that did NOT work out") so the next reader does not retry
them blind: `brew install sail` is a *different project* (a WordPress provisioning CLI —
the name matched, the software did not); building Sail from source was *not needed* once
the prebuilt 0.14 binary was pinned; and dumping Sail's effective merged configuration is
*not supported* — the dump ignores the override, a real limitation with evidential weight,
recorded rather than worked around. `SRC-02` makes an honest "no route" a legitimate
result that bounds a claim; this bill would be incomplete without them.
