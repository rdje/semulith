# The method: from a specification to a checkable model definition

This document is the method this project uses to turn a processor specification into a model
definition an engine can be built from. It is written to be carried: a reader with a different
ISA, different tools, and none of this repository's files should be able to apply it. Where the
method is mechanical, it says so and names the instrument shape; where it is a judgement, it
says so and names what the judgement turns on. A method that hides its judgement calls teaches
the reader to trust where they should think.

The spine is five steps, run in order:

```
document → decision → requirement → obligation → check
```

Each step answers one question, and the order is load-bearing — a later step assumes the
earlier one's answer exists. The rejected alternatives are kept at each step, because the
rejection is part of the method.

## Step 0 — pin the document before reading it (non-mechanical: choosing the publication)

Everything downstream cites the specification. A version string is not an identity: the same
specification is published in multiple renderings that number their sections differently, and
two publications of one revision are different documents for citation purposes. The judgement
call: choose the PUBLICATION, pin it with a digest, and record why that publication — the
`sha256` of a fetched page pins the bytes, the `revision` plus the chapter's own version carry
the normative identity, and a digest mismatch is an instruction to RE-READ, not proof of a
semantic change.

Rejected: pinning a version string alone (ambiguity has already cost real work — a tag
matching no public build); pinning the source repository's HEAD (it moves); citing without
pinning (a locator into a document nobody acquired is not a citation).

## Step 1 — document: state the facts with a source, classed honestly

Read the pinned document and write down what it says — one fact per record, every fact with
the locator it came from and a semantic class. The class vocabulary is small and each word
means something checkable:

- **defined** — the specification states it outright; the model has no latitude.
- **implementation-defined** — the specification delegates the choice to the execution
  environment; the profile chooses, and a reference that chose differently is a profile
  difference, not a defect.
- **unspecified** — the architecture permits a range of behaviours; the laboratory may adopt a
  policy, and the model must still be able to report that the case WAS unspecified.
- **reserved** — the encoding space is reserved; the current revision's rule applies, and the
  revision history matters.

The judgement call at this step is the class, and it is the sharpest one in the method: a
**laboratory** policy over an `unspecified` case must never be recorded as if the architecture
had defined it. Misclassifying upward turns a defect into an unfalsifiable "profile
difference"; misclassifying downward discards a real choice the profile was entitled to make.
When the class is honestly `implementation-defined` or `unspecified`, the model owes the reader
a way to learn that — which is what step 4's negative checks are for.

Rejected: recording facts without the class (silently mixing architecture and policy);
recording the class but not the locator (a claim nobody can re-derive).

## Step 2 — decision: the profile chooses, with an authority on every choice

Every `implementation-defined` or `unspecified` case, and every boundary the harness itself
imposes, becomes a decision. Every decision carries an **authority** — `architecture`,
`execution-environment`, or `laboratory` — and the authority is the load-bearing field: it
records WHOSE choice this was. The rule that protects the whole method: *a laboratory decision
can never override an architectural one*, and labelling an architectural fact as a laboratory
choice is the one misclassification the gates must refuse mechanically, because it is how a
defect becomes untestable.

Rejected: decisions without authority (untestable); one "authority" for everything (the word
stops discriminating); deferring the choice to "whatever the reference does" (the reference's
defaults are ITS profile, not yours — a QEMU-virt platform under a correct ISA string is not a
matched profile).

## Step 3 — requirement and obligation: one fact, one owner, mirrored under governance

Each decision becomes a requirement; each requirement that touches the execution environment
becomes an obligation in both directions — what the CPU guarantees, and what the environment
assumes. Two rules keep this honest:

- **One fact, one owner.** The decision is stated once; the requirement and the obligation are
  *derived mirrors* of it, and every mirror pair is governed — a gate refuses the day a mirror
  drifts from its source. A fact stated in two places with no governor between them is how a
  definition quietly becomes two definitions.
- **Coverage is data, not prose.** A requirement that commits to specific instructions NAMES
  them; then a mechanical check can ask whether the declared set, the encoded set, the
  semantics set, and the requirement set are the SAME set. An instruction with an encoding and
  semantics but no requirement is a fact the engine cannot extract.

The judgement call: what granularity a requirement owns (one instruction, a family, a
boundary). Choose the granularity the checks can falsify.

## Step 4 — check: positive AND negative, derived not copied, refusing rather than warning

Every obligation owes at least two checks: a positive fixture that must behave as declared, and
a negative fixture that must be reported — a contract violation, an illegal instruction, a
profile difference — rather than silently succeed. Positive-only checks are how a contract
comes to describe only the cases that already work.

An expected value in a check is **derived**, not copied: the check re-derives the value from
the pinned source (assemble the instruction from the encoding table; compute the result from
the semantics; re-fetch the document and hash it) rather than carrying a number someone typed.
A carried constant that is a function of the repository is a claim nothing re-proves.

And the checks REFUSE rather than warn. A check that cannot judge (no document, no cache, no
reference) says it cannot judge and stands down; it never reports green over an absence. A
check whose verdict is "yes, but" is a check whose verdict is yes.

Rejected: sampled checks where the answer must be exhaustive (a sampled collision check is an
impression, not a decision); warnings at outward-facing boundaries (read after the bytes have
left); a check that runs nowhere (capability without a re-runner regresses silently).

## Step 5 — disagreement: defect, or profile difference? (non-mechanical: the classification)

When the model and a reference disagree, the classification turns on step 1's class and step
2's authority: a disagreement inside an `architecture`-authority fact is a DEFECT in somebody;
inside an `implementation-defined` or `unspecified` case it is a PROFILE DIFFERENCE, recorded
as such with both choices named. The classification is a judgement — but a bounded one: the
earlier steps have already done the work of making the boundary visible.

## One rule, end to end, by name

Take the shift-amount rule: *SLLI/SRLI/SRAI take a 6-bit shift amount from the I-immediate;
SLL/SRL/SRA use the low 6 bits of rs2; SLLIW/SRLIW/SRAIW take 5 bits, and SLLW/SRLW/SRAW use
rs2[4:0].* — **documented** from the pinned RV64I §3.1.2.1/§3.1.2.2 with the `defined` class;
the **decision** `D-SHAMT` carries `architecture` authority (the specification states it — no
latitude); the **requirement** `REQ-D-SHAMT` names the eleven instructions and states the same
fact; the **obligation** `OB-SHAMT` mirrors the requirement's statement and owes both a positive
check (a shift by 6 bits wraps the amount correctly per width) and a negative one (an SLLIW
with imm[5]≠0 is RESERVED in this revision, reported as such); the **check** derives the
encodings from the pinned table and the expected results from the semantics forms, and the
mirrors are governed — a drift between any two refuses at the gate. Every step is mechanical
except two: classing the fact (it could have been `implementation-defined` — it is not) and
writing the check's expected values honestly (derived from the pinned semantics, not typed
from the reference's output).

## The steps no gate can take for you

Named honestly, because a method that pretends otherwise produces confident errors:

1. **Choosing the publication** (step 0) — which rendering of which revision is YOUR source.
2. **Classing the fact** (step 1) — defined, implementation-defined, unspecified, reserved.
3. **Judging the authority** (step 2) — whose choice this boundary was.
4. **Classifying the disagreement** (step 5) — defect or profile difference.

Everything else — coverage, mirror drift, extraction sufficiency, citation resolution,
duplicate ids, format conformance — is mechanical, and the method's discipline is to keep it
mechanical: a rule a human must remember is a rule a gate must carry.
