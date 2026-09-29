# The method: from document to model

The materials bill says what the project *reads*; the gaps chapter says what those documents
*lack*. This chapter is the bridge: how a sentence of specification becomes, hop by hop, a
running check. The hops are the point — each one is a tracked artifact with a gate on the
seam, so the pipeline is **demonstrated, not asserted**:

```
pinned document ──► decision (authority) ──► requirement (semantic class)
      ──► obligation (positive AND negative checks) ──► guest expectation (derived,
      never copied) ──► the differential (offline on every commit, live three-way)
```

If you build your own model, this is the route to copy. And the honest part of copying it:
the route below was *not* walked cleanly the first time. The mistakes are in this chapter
because they are the instructive part — the one where the dossier was wrong and the model
right, the one where the model was wrong and the references proved it, and the two where
the gates caught the *author's* arithmetic before any model ran.

## One rule, end to end: FENCE's reserved configurations

The rule this walk follows is the FENCE reserved-configuration rule — chosen because its
chain is complete in tracked files *and* because it is the rule this project once got
wrong at hop two. Every hop below names its artifact.

### Hop 1 — the sentence

The pinned artifact `RVI-RV32I` (§1.1.7, "Table 3 Fence mode encoding" — the citation
`check_citations.py` resolves offline against the pinned bytes) says, verbatim:

> Base implementations shall treat all such reserved configurations as FENCE instructions
> (with fm=0000), and standard software shall use only non-reserved configurations.

Read it the way this project learned to read: *"shall treat … as FENCE instructions"* is a
**mandate**, addressed to base implementations, covering a *configuration of a defined
instruction*. Hold that shape; the mistake at hop 2 was misreading it.

### Hop 2 — the decision, with its authority

A sentence of specification is not yet a design decision: the same sentence can bind the
architecture, delegate to the environment, or leave the behavior free. The dossier's
decision record makes the reading explicit and **names who is deciding**:

`D-FENCE` (`profiles/rv64i-lab-v0/profile.sexp`) — *"FENCE is decoded and must not trap. …
The remaining fm, pred and succ configurations are reserved, and the architecture SPECIFIES
their behavior: base implementations shall treat all such reserved configurations as FENCE
instructions (with fm = 0000) … They do NOT fall under D-RESERVED-DECODE."* — authority
**execution-environment**, because the observable half of the rule ("with one hart, no
devices and an in-order model, FENCE has no observable effect") is the laboratory
environment's to state, while the mandated half is quoted from the architecture. The
decision carries a `note` recording that it was **corrected** — the earlier wording sent
reserved `fm` values to illegal-instruction. Corrections are recorded, not smoothed over;
the note is the second correction of this shape in the dossier (`D-MAIN-VS-IO` was first).

### Hop 3 — the requirement, with its semantic class

`REQ-D-FENCE` (`profiles/rv64i-lab-v0/requirements.sexp`) restates the decision —
**identically**, and the identity is enforced, not hoped for: `RECORD-SCHEMA` fails the
commit if a requirement's statement drifts from its decision's. (It fired during the
correction: the first rewording of `D-FENCE` and `REQ-D-FENCE` disagreed, and the gate
said so.) The requirement adds what the decision does not carry: a **semantic class** —
`implementation-defined` — and a research status that cannot read `resolved` while an open
question is attached (the same gate's sharpest rule, written after exactly that pair was
found convenient to hold).

### Hop 4 — the obligation, with positive AND negative checks

`OB-FENCE` (`profiles/rv64i-lab-v0/contract-obligations.sexp`) is the contract half: a
`cpu-guarantee` direction, and required checks `CHK-FENCE-POS` **and** `CHK-FENCE-NEG` — a
contract with only positive checks describes the cases that already work, so the negative
fixture is mandatory. The obligation names its requirement (`parameters.requirement_id`),
and the pair must state the same fact verbatim — an obligation is a derived mirror, and a
mirror that drifts is one fact stated two ways (the MIRROR check, same doctrine).

**The honest gap, said here because the chapter would be a lie without it:** those check
ids are *declared*, and gate `G0`'s report measures exactly this — 72 declared checks, 0
implemented — which is why `G0` reads `incomplete`. What tests the rule *today* is the
guest corpus at the next hop; the named-check layer is the release gate's skeleton, not
yet flesh. The walk continues through what exists.

### Hop 5 — the guest, with expectations derived before any run

`fault-fence` (`profiles/rv64i-lab-v0/guests/fault-fence.s` + `.expected.sexp`): an
ordinary write, then six FENCE configurations — the reserved `fm=1`, FENCE.TSO, the
ignored `rs1`/`rd` fields, the HINT code points — then a landing write. Every expected
observation in the `.expected.sexp` was derived from the pinned sentence *before the
program was run* (EVD-05 — an expected value copied from a model's output tests
self-consistency and nothing else), and the behaviors were **measured on both references
first**: sail-riscv 0.14 and spike 1.1.1-dev execute every one as a nop, exactly as the
corrected dossier says. The expectations declare the empty writes table per fence — a nop
writes nothing — and the run retires into the budget.

### Hop 6 — the differentials that keep it true

Offline, on every commit: the generated fixture (`GUEST-GEN` — the fixture is a byte-exact
function of the tracked guest and its expectations) runs under the definitional
interpreter in the suite `fault_fence_retires_every_reserved_configuration_as_a_fence`
(`crates/semulith-verify/src/run/tests.rs`), asserting the step count, the stop reason
(`Stop::Budget`), and no trap on any step. Live: `scripts/run_semulith_smoke.py` runs the
same guest against both pinned references in the one observation vocabulary — three-way
agreement, byte-identical reproduction. And `EXERCISE-COVERAGE` keeps FENCE inside the
52/52 denominator, so the rule cannot silently drop out of the exercised set.

Six hops, every one inspectable: a sentence, a decision, a requirement, an obligation, an
expectation document, two differentials. That is the whole method — the rest of this
chapter is the two judgement calls the hops do *not* make for you, and the mistakes.

## The judgement call the schema cannot make: semantic class

A requirement's class answers: **what kind of freedom does the source grant here?** The
vocabulary (`schema/requirements.sexp`) is the specification's own: `defined`,
`implementation-defined`, `unspecified`, `undefined`, `reserved`, `unpredictable`,
`source-specific`, `not-applicable`. Today's 28 requirements span four of them. The
judgement is a *reading*, not a lookup: the reserved-FENCE case is `implementation-defined`
because the architecture defines the shape and delegates the effect; `D-SHIFTW-RESERVED`'s
class is `reserved` because the revision marks the encodings reserved outright. Misreading
the class is not a typo-class error — it changes who is allowed to decide, which is the
next axis. The class is checkable for *presence* and *consistency*, never for *correctness*;
that is why the reading gets a citation and the citation gets a resolver.

## The judgement call with teeth: authority

A decision's authority answers: **who is deciding** — `architecture` (the specification
decides; the dossier records), `execution-environment` (the specification delegates to the
EEI; this laboratory states its choice), or `laboratory` (the case is UNSPECIFIED and the
harness adopts a policy — `D-RESERVED-DECODE` is the canonical one). The axis has a
mechanical edge, and it bites in the direction that matters: an obligation whose
requirement is architecturally `defined` must itself carry authority `architecture`
(`RECORD-SCHEMA`'s AUTHORITY check) — **laboratory policy cannot override an architectural
rule**, because mislabelling one is how a defect becomes an unfalsifiable "profile
difference". The DEFECT-A correction below is exactly this axis misread: a reserved
*configuration* (architecture-specified) was read as a reserved *instruction*
(UNSPECIFIED), and the wrong authority reached for the wrong policy.

## The mistakes stay in

### DEFECT-A — the dossier was wrong, the model was right

`P2-SCALAR.1` logged: a FENCE with a reserved `fm` value executes as a nop where `D-FENCE`
then said it must raise illegal-instruction. Read as a model defect, it would have been
"fixed" by making the model trap. The `P2-SCALAR.3` probe suite measured the case against
the pinned text *and* both references before touching anything — and **inverted** the
defect: §1.1.7 mandates the nop verbatim, both references execute the probe word exactly
as the model does, and the dossier's sentence was the wrong artifact. What the wrong
instrument reported: a checklist reading of the word "reserved" had reached for
`D-RESERVED-DECODE` without reading the rest of the sentence. Why it was believed: it
*looked* like the reserved-instruction case, and nothing forced the re-read — the probe
discipline (measure before you fix) is what forced it. The correction is in the record at
`D-FENCE`'s note, and `fault-fence` pins the corrected behavior three-way.

### DEFECT-B — the model was wrong, the references proved it

A misaligned `jal`/`jalr` wrote its link register *before* trapping; spike emits no commit
record for the jump and sail shows no write — an instruction that raises a synchronous
exception retires nothing, and the model retired a write. The fix is the part worth
copying: it landed in semantics **data** (`definitions/riscv/rv64i.sem.sexp` — the
`jal`/`jalr` effect trees now evaluate `set-pc` first), never in the evaluator, because the
definition is the execution authority. `fault-jal-mis` / `fault-jalr-mis` pin it with the
negative observation `never_written x5` — the suite names a register that must stay
unwritten, so a regression cannot hide behind the trap. (The offline suites:
`fault_jal_mis_traps_on_the_jump_and_never_writes_the_link` and its `jalr` sibling.)

### The two authoring REDs — the gates catching the *author*

The measured-first pipeline catches the model; the gates also catch the person writing the
evidence. Twice in these leaves: the `bound-alias` overlap-composition constant was
hand-assembled wrong *twice* (`P2-SCALAR.2` — each time the pinned expectation failed RED
against the real model, and the correction was re-derived from the spec rule: SH stores the
low 16 bits, little-endian — the rule computes the value, never the author); and all
eighteen `P2-SCALAR.3` expectation documents carried one systematic trailing paren, which
the schema check refused on all eighteen before any guest ran. Neither was a model defect.
The lesson the gates enforce: an expectation the spec rule does not compute cannot be
committed, and a document the schema cannot parse does not exist.

## Build it yourself

For your own unit, in this order:

1. **Pin the materials** — publication + revision + digest, per artifact. A version string
   without its publication is not an identity.
2. **Enumerate the scope with its denominator** — the count must equal the enumeration, or
   the dossier contradicts itself.
3. **Write the decisions before any code** — each with its authority; the authority is a
   reading of the source, so cite the section.
4. **Declare the requirements with their semantic class** — and let the statement-identity
   gate hold decision and requirement verbatim.
5. **Write the obligations with positive AND negative checks** — the negative one is the
   half that fails when the model cheats.
6. **Derive the expected values before any run** — from the pinned prose, with the
   derivation written down; then *measure* the references before pinning a fault case.
7. **Let the gates catch you** — they will, and that is the method working, not failing.
