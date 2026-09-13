# A worked example

The fixtures under `examples/` describe **SYN16**, an invented 16-bit arithmetic machine. It is
not RISC-V, it is not a DSP, and it represents no physical processor. Its purpose is to exercise
the record shapes end to end while being impossible to mistake for a result.

## The fixture's own specification

```markdown
## A1 — Addition
Inputs `a` and `b` are unsigned 16-bit values. The result is `(a + b) modulo 65536`, also an
unsigned 16-bit value. There are no status flags, exceptions, memory effects, or time claims.
The host's overflow behavior has no bearing on this definition.

## E1 — Input contract
The fixture environment supplies `a` and `b` in the inclusive range 0 through 65535. Input
outside this range is a malformed fixture and must be rejected by the harness before invoking
the arithmetic operation. It is not a guest architectural exception.
```

Note what E1 does: it makes *"the harness was handed something illegal"* a different outcome
from *"the guest did something that traps"*. That distinction is `SEM-01` in miniature, and
getting it wrong is how a model reports its own bugs as target behaviour.

## The requirement

```json
{"id": "SYN16-ADD-001", "profile_ids": ["synthetic-u16-v1"], "kind": "numeric",
 "statement": "Return (a + b) modulo 65536 for valid unsigned 16-bit operands.",
 "source_refs": [{"source_id": "SRC-SYN16", "locator": "A1"}],
 "applicability": "included", "research_status": "resolved", "implementation_status": "planned",
 "source_semantics": {"category": "defined",
   "detail": "Explicitly self-defined synthetic fixture; no real ISA claim."},
 "risk": "medium", "obligation_ids": ["OB-SYN16-ADD"],
 "dependencies": [], "implementation_refs": [], "evidence_ids": ["EV-SYN16-ADD"]}
```

`research_status: resolved` and `implementation_status: planned` together say something a single
status field could not: *we know what this must do, and we have not built it.*

## The evidence

```json
{"id": "EV-SYN16-ADD", "method": "directed-test", "status": "planned",
 "producer": {"id": "PLANNED-SYN16-CHECKS", "version": "not-implemented", "kind": "test-runner",
   "provenance_refs": ["SRC-SYN16"], "shared_dependencies": [],
   "independence": {"classification": "unknown", "scope": "SYN16-ADD-001",
     "justification": "Implementation and test provenance must be established when these planned checks exist."}},
 "inputs": [], "artifacts": [],
 "limitations": ["Planned example only: no CPU code, test execution, or successful evidence."]}
```

Every evidence record in this repository is `planned`, with an empty `inputs` and `artifacts`
and an explicit limitation. The schema would *reject* a `passed` record shaped like this — which
is the point: the fixture cannot be edited into a false result by changing one word.

Its `independence.classification` is `unknown`, not `independently-derived`. Unknown is an
honest answer and a much more common one than projects admit; `EVD-04` requires recording known
ancestry **and** unknown ancestry rather than assuming either independence or correlation.

## The source ledger, and the gate on it

```json
{"fixture_only": true,
 "sources": [{"id": "SRC-SYN16", "path": "synthetic-spec.md", "version": "1",
              "sha256": "12787d5932eba395a8904c347db55f22501fe889f73d5533726b4864502ca43f"}]}
```

That hash is a claim about the working tree, so it is gated rather than trusted. Appending a
single byte to `examples/synthetic-spec.md` produces:

```
FIXTURE-FINGERPRINT: a record pins a fingerprint that no longer describes the tree.
  DRIFTED   examples/sources.json:1 — 'synthetic-spec.md'
      pinned  12787d5932eba395a8904c347db55f22501fe889f73d5533726b4864502ca43f
      current 80e347f44e975f2c4e813f648225f3b5ba604dc6d1051ee4f403fc191cd9eedc
```

A carried constant that is a function of the repository is derived or gated, never trusted —
see [What "checked" means](../working/claim-verification.md).
