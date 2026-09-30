# Annex: building the first CPU model, step by step

This chapter walks through how `rv64i-lab-v0` — the project's first processor model — was
actually built, in the order it was actually built, so that a reader could build their own
model the same way. It is a teaching text, not a highlights reel: the mistakes are in it,
because the matched profile that matched only an instruction set and the comparator that
called a truncated trace agreement are the most instructive pages this project has.

Two mandates govern everything below, and they are worth stating before any step:

- **Production.** The model is signoff work: every claim is either re-derived, falsified by a
  test that could have failed, or honestly labelled as not yet established.
- **Teaching.** The reasoning must be recoverable, not just the result. If you are building
  your own CPU model — for school, for work, for fun — each step here names the artifact you
  would create, the mistake you would otherwise make, and the command that shows it.

The one-sentence discipline that makes the rest coherent: **a claim is only as good as the
named thing that could prove it false.** Every step below is either writing a claim down or
building the thing that could falsify it.

The fourteen steps:

0. choose a target you can actually finish
1. pin the materials — and measure what they do *not* contain
2. write the dossier: every decision gets an *authority*
3. declare the requirements and obligations before building anything
4. inventory the state — including the hidden kind
5. one canonical definition, one format
6. generate the code — never hand-edit it
7. the interpreter evaluates data; it does not contain the ISA
8. guests with expectations derived *before* any run
9. the laboratory: one observation vocabulary
10. obtain the references — and match the whole platform, not the ISA string
11. compare honestly: first divergence, and a shorter trace is never agreement
12. prove the detector: known-wrong models must be caught
13. exhaust the scope, then the boundaries, then the faults
14. the gate reads what it reads — honest verdicts only

---

## Step 0 — choose a target you can actually finish

**What you do.** Pick the *smallest* real architecture that still forces every hard problem
to show up once. For this project that was RV64I — the 64-bit base integer RISC-V — as the
profile `rv64i-lab-v0`.

**Why.** RV64I is 52 instruction forms, no privilege machinery beyond machine mode, no
atomics, no floating point, no compressed instructions. Crucially, **no RV64I instruction is
a multi-step or restartable suboperation** — each one completes or faults as a unit. That one
property is why this model's snapshot, replay and determinism stories are simple enough to be
a *first* model. It is also why the specification chapter that defines it is short enough to
read end to end, which you should do: this walk assumes you would.

The trap to avoid is picking a target whose size you cannot afford to *finish*. A model that
is 80% of a big architecture proves far less than one that is 100% of a small one — the
interesting claims (complete scope, exercised faults, measured boundaries) are all about the
last 20%.

**Feel it.**

```sh
grep -oE '\((base|rv64)_[a-z_0-9]+ "[A-Z]+"\)' profiles/rv64i-lab-v0/profile.sexp | wc -l   # 52
bash scripts/check_exercise_coverage.sh               # 52/52 forms executed by guests
```

## Step 1 — pin the materials, and measure what they do NOT contain

**What you do.** Acquire every document the model will be built from, record its *exact
identity* (locator, revision, digest, size, retrieval date), and record what each supplies —
and what it does not. Here: `materials/catalog.sexp` pins 36 primary sources, and
`profiles/rv64i-lab-v0/sources.sexp` pins the ones this unit actually reads.

**Why.** A model is only re-derivable if its inputs are. "The RISC-V spec" is not an input;
*a specific rendering, hashed* is. The project rule (SRC-03) is that availability is an
observed fact, never reputation: each pinned row was fetched and hashed on this host.

**What went wrong for real — and shaped everything after.** The pinned specification
artifacts contain **no instruction encodings**. This was measured, not noticed in passing:
`grep -cE '[01]{7}'` returns 0 over all six artifacts, because the format diagrams are
images (31 of them in the RV32I chapter alone). The bit layouts had to come from somewhere
else — `riscv-opcodes` — which is *also upstream of one of the reference models*. That
shared ancestry is recorded in `references.sexp` rather than hidden: byte-level agreement
with Spike is not an independent confirmation of the encodings, so `spike-dasm` (a second
decoder from a different codebase) was run over the emitted bytes instead. The lesson:
**measure what your primary source lacks before you discover it mid-build.**

**Feel it.**

```sh
python3 scripts/check_citations.py      # every § a semantic rule cites resolves, offline
```

## Step 2 — write the dossier: every decision gets an authority

**What you do.** Before any code, write the profile dossier: the decisions that turn "RV64I"
into *this* model. What does a misaligned load do? What is the reset state? What happens on a
reserved encoding? Each decision is a named record (`D-MISALIGN-DATA`, `D-RESERVED-DECODE`,
…) in `profiles/rv64i-lab-v0/profile.sexp`, and each carries an **authority**:
`architecture` (the specification mandates it), `execution-environment` (the spec delegates
it), or `laboratory` (this project chose it).

**Why the authority field is the load-bearing one.** A *laboratory* policy over an
unspecified case must never read as an *architectural* rule — because when a reference model
later chooses differently, that is a **profile difference**, not a defect. This project has
exactly such a case: the spec leaves code-visibility (self-modifying code without `fence.i`)
to the implementation; the laboratory re-reads memory every fetch; a caching reference would
be equally legal, so a divergence there must be reported as a difference, not a bug
(`D-CODE-VISIBILITY`).

**What measuring looks like here.** Are register reset values architectural? The string
`reset` appears **0 times** in the RV32I chapter and **0 times** in the RV64I chapter —
measured. The unprivileged spec says the environment defines the initial state, so zeroed
registers are a *laboratory* declaration a guest may not rely on elsewhere. A decision that
is checked against the source text is a different object from one that sounds right.

**Feel it.**

```sh
bash scripts/check_profile_consistency.sh   # declared counts == enumeration; every decision cited
```

## Step 3 — declare the requirements and obligations before building anything

**What you do.** Turn the dossier into machine-checkable records: `requirements.sexp` (28
requirements, one per decision, each with a *predeclared* verification policy) and
`contract-obligations.sexp` (36 obligations — 28 CPU guarantees, 8 environment assumptions —
each with positive **and negative** required checks).

**Why *predeclared* (rule EVD-03).** If you write the verification policy after the
implementation exists, the policy quietly becomes "whatever the implementation does". Writing
"this obligation needs a differential test *and* a negative fixture" before any model runs is
what stops the evidence from being fit to the answer. The sharpest record in this layer is
the negative check: `guest-no-device` exists to fail if a device becomes reachable — a
positive test cannot prove an absence.

**Feel it.**

```sh
bash scripts/check_requirements.sh   # the record schema, the cross-references, the graph
```

## Step 4 — inventory the state, including the hidden kind

**What you do.** Write `state.sexp`: 32 integer registers of 64 bits, `x0` hardwired, `pc` —
and then the part that matters: **enumerate seven candidates for hidden state and show each
absent**. CSRs, the reservation set, floating-point state, vector state, privilege/trap
state, instruction-fetch cache state, pending or partially committed effects.

**Why.** An empty list with no census is an unearned claim. Two of the seven are worth
reading carefully, because they are where a first model usually lies to itself:

- *Fetch-cache state* is absent **only because** of the laboratory's code-visibility choice —
  a caching implementation would have hidden state here and would still be legal. The absence
  is a *decision*, not a fact of nature, and the census says so.
- *Pending effects* are absent because no base instruction is restartable — which is exactly
  why this is a good first experiment, and why the file warns: **every extension added later
  reopens this census.**

## Step 5 — one canonical definition, one format

**What you do.** Write the model down exactly once, as data: `definitions/riscv/rv64i.sexp`
(the encoding fragment — fixed bits and operand fields per instruction) and
`definitions/riscv/rv64i.sem.sexp` (the semantics — an effect tree per instruction). The
unit's `encoding.sexp` *composes* fragments; it never copies an instruction.

**Why one format.** Every source of truth in this project is an S-expression
(`decision_one-format-every-source-of-truth`), read by one reader (`scripts/sexp.py`), so
"the definition" is never three files that might disagree. The format split this replaced had
the same fact in TOML, JSON and JSONL at once — a structure that guarantees drift, and did.

**Why data, not code.** If the ISA lives in a programming language, the only way to ask
questions of it is to run it. As data it can be *checked*: the EXTRACTION gate proves every
declared instruction has an encoding **and** semantics **and** a requirement — one set, four
ways — before any engine exists.

**Feel it.**

```sh
bash scripts/check_extraction.sh   # is the definition sufficient for an engine?
```

## Step 6 — generate the code, never hand-edit it

**What you do.** Generate the Rust: `scripts/gen_state.py` lowers `state.sexp` to
`crates/semulith-core/src/state.rs`; `scripts/gen_definition.py` lowers the composed
definition to `definition.rs` (decode tables + semantics trees). Then gate it: STATE-GEN and
DEF-GEN regenerate and compare, so the checked-in module is a **byte-exact function** of the
tracked descriptor.

**Why.** "Generated" must be a governed claim. Two properties do the governing: drift is
refused with the regeneration command (never "please re-sync"), and the generator itself
**refuses — naming the construct — any shape it cannot emit**. A generator that guesses is a
second, unaudited definition. Both gates were fired RED against a hand-edited module before
they were registered; a gate that has never been observed red is not known to work.

**Feel it.**

```sh
bash scripts/check_definition_gen.sh   # refuses drift with the exact regeneration command
```

## Step 7 — the interpreter evaluates data; it does not contain the ISA

**What you do.** Write the executor (`semulith-core`'s `exec`) as a *generic evaluator* of
the semantics trees: registers, memory requests through an environment boundary, typed
outcomes. The ISA is entirely in the data from step 5.

**Why this separation pays — measured, not argued.** During the fault campaign the model was
caught writing the link register of a misaligned `jal` *before* the trap, where both
reference models suppress the write. The defect was in the `jal` effect tree — it evaluated
the link write before the target check. The fix **reordered the data**; the evaluator did not
change by one line. When "the model is wrong" can mean "edit a data file and regenerate",
correctness work stops touching the machinery that everything else depends on.

## Step 8 — guests with expectations derived BEFORE any run

**What you do.** Write small guest programs (`profiles/rv64i-lab-v0/guests/*.s`) and, for
each step of each one, the expected observation: which registers change to which values —
with a `derivation` (the arithmetic, in words) and a `source` (the spec section), computed
**from the specification prose before any model ran** (rule EVD-05). Then generate the
fixture (`gen_guests.py` → `guests.rs`) and let the commit gate re-run every guest against
those expectations on every build.

**Why.** An expected value copied out of a model's output is the model grading itself. The
derivation-before-run discipline is what makes a failure *mean* something: either the model
is wrong, or your reading of the spec is — and both are worth knowing.

**What went wrong for real.** The gate failed twice on **authoring** mistakes, never on the
model: an overlap-composition constant was hand-assembled wrong (0x4CD's high byte is 0x04,
not 0x4C). Each time the pinned expectation failed red against the real model, the derivation
was re-done from the spec rule, and the corrected value is what *the rule* computes. The
instrument discriminated in exactly the direction it was built for — including against its
author.

One practical rule the guests taught: the observation vocabulary is the *visible register
change*, so an expected result of 0 (or an identity operation) proves nothing unless the
destination was pre-written to a different value. Several guests pre-write registers for
exactly this reason.

**Feel it.**

```sh
cargo test -p semulith-verify          # the offline differential: every guest, every step
```

## Step 9 — the laboratory: one observation vocabulary

**What you do.** Build the runner (`semulith-verify`'s `run.rs`): drive the interpreter over
a memory environment and record, per executed step, one observation —
`(pc, instruction word, register writes, trap)`. Runs stop *typed*: `Budget`, `Trap`,
`FetchFault`, `Failed`, `Undefined`.

**Why one vocabulary.** The two reference models print utterly different traces; the only
honest way to compare is to reduce every model — including your own — to the same shape and
compare *that*. Deliberate absences define the shape: the word is `Option`, because a failed
fetch supplies no word and inventing one would put a fiction in the comparison; a write to
`x0` never appears, because the architecture discards it.

**Why the stops are typed.** "The guest asked the environment for something" (an `ecall`) is
not "the model cannot do this" (a crash) is not "the source leaves this unspecified" (a
reserved encoding). The laboratory's reserved-decode policy is instructive: the *interpreter*
reports the case as the unspecified case it is, and the *harness* — one layer up, explicitly —
converts it to the illegal-instruction observation both references were measured to produce.
The classification is never laundered: the stop reason keeps it.

## Step 10 — obtain the references, and match the whole platform

**What you do.** Acquire the reference models (`scripts/fetch_references.sh` pins Sail 0.14
and a Spike source build, hashed), configure them to the profile, and compare *the
configuration*, with `scripts/compare_platforms.py`.

**What went wrong for real — the most instructive defect in the project.** The first
"matched" configuration matched the **instruction set and nothing else**. The ISA string read
`rv64i_zvl32b`, which was taken as "matched" — but underneath, the reference kept its default
platform: a core-local interruptor with a live `mtime`. Measured by probe: a guest load from
`0x0200_BFF8` returned a value that *advanced across reads* (2, then 3) — an invisible device
sitting inside a "matched" experiment. The fix was to configure the platform (devices off,
one memory region), and `guest-no-device` is kept as the negative fixture that fails if a
device ever becomes reachable again. **An ISA string describes an instruction set. Reading it
as a whole-configuration verdict is how a device hides in your control group.**

## Step 11 — compare honestly: first divergence, and a shorter trace is never agreement

**What you do.** Normalize each reference's trace through a small adapter with *measured*
spellings (an unknown exception name raises — a trap the adapter cannot parse is a trap that
disappears, and a disappearing trap reads as agreement), align both traces on the entry
point, and walk them together (`scripts/compare_traces.py`): report the **first** divergence,
because every later difference may be its consequence.

**What went wrong for real.** The first comparator compared only the overlapping prefix — and
printed `AGREE over 2 aligned step(s)` for a run in which one model trapped and the other
simply stopped producing records. The prefixes agreed; the observation did not; the verdict
was green. Now: a length mismatch is a non-agreeing verdict that must be explained, and the
comparator's self-test carries that exact case as a red arm. **Any comparator you build
should be forced to disagree before you trust it to agree** — this project's comparator has
twelve self-test arms, most of them red on purpose.

**Feel it.**

```sh
python3 scripts/compare_traces.py --self-test   # a comparator forced to disagree, 12 arms
python3 scripts/run_semulith_smoke.py           # the live three-way differential
```

## Step 12 — prove the detector: known-wrong models must be caught

**What you do.** Mutate the model deliberately (`semulith-verify`'s `mutate.rs` builds
one-row-wrong definition tables) and require the differential to catch each mutant. A
mutation that is *not* caught is a finding about the tests, not about the model.

**Why.** A validator that has only ever said "agree" is not known to detect anything. The
mutation suite is the detector's own test evidence, and it is pinned the same way as the
model: the census of boundary crossings each guest produces is recorded with per-line
justifications, so a mutant that changes *nothing observable* is impossible to confuse with a
mutant that was caught.

**Feel it.**

```sh
cargo run -p semulith-cli -- demo --guest=smoke-arith --mutate=zext-addi
```

## Step 13 — exhaust the scope, then the boundaries, then the faults

**What you do.** Three campaigns, each gated:

1. **Scope.** Every declared form must *execute* in a guest — coverage reported **with its
   denominator**. Measured when the gate was built: 15/52 forms had ever run; the gate named
   all 37 missing ones, and has read 52/52 since.
2. **Boundaries.** The *tractable* domains are exhausted outright — the 6-bit shift-amount
   field by a 64-point sweep, the 5-bit one by 32 — and the intractable ones (2^64 data
   values) are probed at their discriminating structure: sign edges, wrap points, the
   register-amount corners (`rs2 = 64` reads as 0). A 256-point byte sweep was considered and
   rejected with the reason recorded: the edge pair discriminates everything it would, at
   1/40 the cost.
3. **Faults.** Every failure behaviour was *measured against both references by throwaway
   probes before any guest was written* — and two of the measurements rewrote the plan: a
   dossier "defect" turned out to be the spec mandating the model's behaviour verbatim
   (reserved-`fm` FENCE nops; the *dossier* was corrected), and a real model defect (the
   misaligned-jump link write) was fixed in semantics data. **Measure the references before
   you pin expectations about them** — every fault guest in this project exists because a
   probe told the truth first.

**Feel it.**

```sh
bash scripts/check_exercise_coverage.sh          # 52/52, with the denominator
cargo run -p semulith-cli -- run <elf> --steps=N # watch any guest under the laboratory
```

## Step 14 — the gate reads what it reads: honest verdicts

**What you do.** Generate the gate report (`scripts/gate_report.py`) from tracked inputs and
gate the report itself for staleness — so the verdict cannot be reached with an editor. For
most of this project's life the verdicts were `incomplete`, and that was the system
*working*: criterion 6 of the laboratory gate (a compiled-C guest) was genuinely unmet, so
the report said so and named the owning leaf. When the guest landed (`P2-SCALAR.5`,
`2026-09-30`), the SAME instrument read `passed` — the verdict moved because the inputs did,
never because anyone reached for an editor.

**Why.** The release rules make a missing required check yield `incomplete`, never `passed`,
and the generator has no code path to `passed` while any criterion stands unmet. A verdict
you could edit is a verdict no one can build on; a verdict that is a pure function of tracked
inputs is one a reviewer can re-run in a fresh clone.

**Feel it.**

```sh
scripts/gate_report.py rv64i-lab-v0 --gate G1 --stdout   # the honest gate, regenerated
make check && make gate                                  # the full offline proof
```

---

## What this walk did not cover

The model you just walked through runs in the browser as well (`make bench`, then serve
`bench/` — the engine compiles to WebAssembly on every commit, so a host-only API cannot
slip in unnoticed), and it boots nothing: no privilege modes, no devices, no OS. Those are
later milestones with their own gates (see *P4 — the Linux CPU profile* onward), and each
reopens censuses this walk closed — the hidden-state census first of all.

And the standing limit, stated once here rather than fourteen times: finite differential
testing is **tested evidence, never proof**. What this walk produces is a model whose every
claim names the thing that could falsify it — which is the strongest kind of statement an
executable model can honestly make, and the only kind this project ships.

## Try it, end to end

```sh
make check                                   # the offline differential: 32 guests, every step
python3 scripts/run_semulith_smoke.py        # the live three-way run (needs target/refs/)
make bench && (cd bench && python3 -m http.server 8000)   # the same engine in a browser
```

The per-unit book (`MODEL-BOOKS`'s future leaves) will re-tell this route centered on the
unit's own materials bill; this chapter stays the pipeline-level walk, and the two reference
each other rather than repeat — the project's first documentation rule is that no fact gets
two owners.
