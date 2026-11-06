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

**Does not supply:** the RV64 deltas (those are the next artifact), or a
machine-readable opcode table. The authenticated HTML includes format images;
a text-only search cannot establish what those diagrams contain. This chapter's
prose grounds the semantics, while the separately pinned encoding artifacts below
record the machine-readable inputs used by this project.

### `RVI-RV64I`

The RV64I chapter, version 2.1: XLEN=64, the `*W` instruction family, the 6-bit shift
amounts, LWU/LD/SD, and the RV64I HINT table. Short enough to read end to end — which
you should, because this chapter plus the one above *is* the whole instruction
specification of this unit.

**Does not supply:** the base rules it modifies (read it with `RVI-RV32I`),
or a machine-readable opcode table. Image content cannot be ruled out by searching
HTML text. The *W forms' sign extension with a garbage upper half is derived from
the prose ("ignoring the upper 32 bits") and pinned by the `bound-arith` guest.

## The encoding tables

The machine-readable encoding artifacts have their own recorded identity.
The pinned specification's HTML includes diagrams, so zero text-search hits do
not prove that the specification lacks encodings. The table below identifies the
project's declared inputs without making an implementation-ancestry claim.

{{#include materials/encoding-tables.md}}

### `RISCV-OPCODES`

RISC-V International's machine-readable opcode tables record fixed bits and
operand lists (`rv_i`, `rv64_i`), operand positions (`arg_lut.csv`) and immediate
layout descriptors (`constants.py`). The normal assembler reads the composed
canonical `encoding.sexp`; its separate legacy table-directory route parses these
upstream artifacts. Finite word comparisons and refusal controls check the
recorded encodings and layouts (see `docs/book/src/annex/assembler.md`). They do
not guarantee that every possible encoding error is absent.

**Lineage limit.** Public artifact identities and finite decoder observations do
not establish whether Sail, Spike or this project share an implementation ancestor.
The canonical inventory now marks those ancestry questions `not-examined`; neither
agreement nor a negative text search establishes independence. The earlier
PDF investigation at `MODEL-BOOKS.2` remains dated reported history, with its two
qualifications in the gaps chapter. No fresh PDF replay or encoding re-sourcing
is claimed here.

**Does not supply:** semantics. These tables identify instruction bits, never
expected values, trap behavior or boundary rules. Nor do they prove comparator
independence. Their layout descriptors are inputs to the legacy parser; the
normal assembler uses the composed canonical encoding space.

## The reference models

The generated table records acquired implementations and the acquired ACT test
corpus. A reference is a differential partner: agreement is finite evidence for
the exercised inputs. Acquisition, configuration and observed agreement each have
their own scope; none by itself authenticates implementation ancestry.

{{#include materials/reference-models.md}}

### `sail-riscv`

The primary oracle candidate: the RISC-V International reference formal model,
release 0.14, a prebuilt binary pinned by digest. Its tracked override selects the
profile's memory regions, no CLINT and no interrupt generator. In the recorded
matched-profile control, changing only its misalignment policy to "handled
invisibly" produced a divergence against Spike. That finite control shows a
configuration-sensitive result; it proves neither general agreement nor lineage.

**Does not supply:** authenticated implementation independence. In this project's
ACT campaign, Sail produces the expected signatures (see `act4`). It also does not
emit the effective merged configuration: the recorded `--print-default-config`
probe ignores the override, so the effective configuration is represented as
release default plus tracked override. The interaction-matrix probes record a
further limit: Sail 0.14 masks access-fault tval to its 56-bit physical-address
width (`DIFF-TVAL-PHYS-MASK`).

### `spike`

The second implementation: the historical golden model, built from source at a pinned
commit. Its commit-level trace vocabulary drove the adapter's most important rule — Spike
emits *no* commit record for a trapping instruction, and reassembling that split record is
what stopped a truncated trace reading as agreement (the lesson the comparator's
length-mismatch refusal now enforces).

**Does not supply:** a matched platform. Spike bundles a board with a core-local
interruptor, PLIC and UART; the recorded public-interface investigation found no
option to remove them (`DIFF-PLATFORM-SPIKE`). Guests touching its device addresses
therefore skip the Spike comparison. Encoding agreement on exercised inputs also
supplies no authenticated ancestry conclusion; the canonical inventory marks the
implementation-lineage question `not-examined`.

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

**Does not supply:** an independent expected-result producer in this project's
recorded campaign. `scripts/run_act4_campaign.py` runs Sail and compares both Spike
and semulith signatures with Sail's signature. That is an observable dependence
of this pipeline, without a claim about every ACT configuration or implementation.
ACT supplies externally chosen tests. The dated `P2-SCALAR.5` strand-2 record
reports 51 RV64I test files and 17,017 signature slots, all passing against the
Sail-produced expectations (`profiles/rv64i-lab-v0/act4.sexp`); this correction
does not claim a fresh campaign replay.

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

The EVD-05 guest corpus uses the canonical encoding space and expected
observations derived from pinned specification prose before model comparison.
An expected value copied from model output would test self-consistency. The
offline differential checks these declared expectations; live reference runs
supply additional finite observations for their recorded inputs.

**Does not supply:** proof or authenticated implementation independence. Current
corpus counts and coverage come from the generated `G0-REPORT.md` and `GC-REPORT.md`
in `profiles/rv64i-lab-v0/`, rather than a second mutable count here. The scope
provides the coverage denominator, which `EXERCISE-COVERAGE` re-derives. Finite
agreement is not universal trace inclusion.

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
