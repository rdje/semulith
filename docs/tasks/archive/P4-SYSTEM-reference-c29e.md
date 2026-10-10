# P4-SYSTEM — historical reference rationale, c29e

Replaced P0/P4 overview and LIVE spans are preserved verbatim, in source order.
They contain historical internal-source observations and ancestry inferences;
they are withdrawn as a current dependency basis under the black-box boundary.
No census or implementation claim in these payloads has been revalidated here.
Current public observations and evidence limits remain in the live book.
Canonical/knowledge repairs are explicitly owned by P4-SYSTEM.14.

The source identities and exact replacement texts below permit full inverses:
authenticate every marked payload, then undo replacements in reverse order.
The result must match each committed source byte-for-byte and by SHA256.
This finite archive accepts no future additions after its commit.

```json
{
  "base": "6b37d571b3231fa5bc2ba49f6e1289405eaed8df",
  "sources": {
    "docs/book/src/plan/p0.md": {
      "bytes": 25439,
      "sha256": "3ff60eeb0bd475cebe1e9d38356de7254bd631d8bfdf24d438446ca769f6b237"
    },
    "docs/book/src/plan/p4.md": {
      "bytes": 7650,
      "sha256": "d0e4521ad9cec31d946637310594abf1155bf2a8243ccdca19bd7332e69676b7"
    },
    "LIVE_STATUS.md": {
      "bytes": 6135,
      "sha256": "c2290b994653318dc7504b00a18c0dabac74cd66cc48d19e4f6957a7a5d495d0"
    }
  },
  "spans": [
    {
      "path": "docs/book/src/plan/p0.md",
      "new": "Acquire reproducible artifacts through each reference's published build or\nrelease instructions, and **run an actual matched-profile experiment before\nmarking the reference usable**. Record versions, source and binary hashes,\neffective configurations, adapters and known gaps. Record documented expected-\nresult provenance for each compared pair and subsystem; leave unresolved\nindependence explicit.\n\nDifferent tool names and agreeing outputs do not establish independent\nsemantics. A corpus whose expected results were produced by the same comparator\nadds test inputs, but no independent expected-value derivation. Specification-\nderived expectations and deliberate failing controls are separate evidence.\nTreat dependency implementations as black boxes: use published contracts and\npublic observations, and qualify any provenance question those cannot answer.\n\n",
      "bytes": 1033,
      "sha256": "41c9c5d371a1f9dd4d0b81cfba49a97b45311e647a29af2be8ad0308c52314c8"
    },
    {
      "path": "docs/book/src/plan/p0.md",
      "new": "A candidate's name, separate artifact identity or successful comparison does\nnot establish semantic independence. Record the documented source of expected\nresults separately from observed outputs. If that source is unresolved, retain\nthat limitation rather than infer an implementation relationship.\n\nThe gate requires each candidate's `lineage` field and a per-pair/subsystem\ninventory for recorded comparisons. Those are presence and consistency checks:\nthey do not authenticate the prose or prove independence. Having the binaries\nis not having that evidence.\n\n",
      "bytes": 655,
      "sha256": "c84383043910290e0636b998b1a1f99830df831ba8ef5e050ac10d87c4fbece2"
    },
    {
      "path": "docs/book/src/plan/p0.md",
      "new": "*The public ISA strings differ.* With the tracked override, the Sail release\nreports `rv64i_zvl32b`, while Spike's selected ISA is `rv64i`. That is a measured\nconfiguration difference. The scalar guests exercise no vector instructions;\ntheir finite agreement does not establish the full decoder's extension scope or\nexplain why the extra class appears. Keep the difference explicit without\ninferring a cause inside either dependency.\n\n",
      "bytes": 439,
      "sha256": "ac63247d13c86ac18a186f7d9c9498b4e4dc96c07d41b518ce898a4a7a5e694a"
    },
    {
      "path": "docs/book/src/plan/p0.md",
      "new": "The project's assembler therefore obtains its encodings\nfrom a separately pinned machine-readable source, recorded as its own provenance.\nPublic references decoding the emitted bytes provide an observed cross-check;\nthat result does not establish their encoding ancestry or semantic independence.\nThe scalar expected values have separate, specification-side derivations.",
      "bytes": 312,
      "sha256": "9e24de0606e8c542ed72cfd52e60000676296fe5c51e42ac06d711ad49ff323d"
    },
    {
      "path": "docs/book/src/plan/p0.md",
      "new": "Agreement is evidence about the selected inputs and observed state. It does not\nreveal how a dependency implements an operation. Current work uses public\ninterfaces and authenticated artifacts; it does not infer independence from\nnames, symbols, internal source layouts or matching outputs.\n\n| Evidence route | What it establishes | Limit |\n| --- | --- | --- |\n| Scalar Sail/Spike smoke | Four programs /34 expected boundaries; three enabled comparisons /28 aligned boundaries; four repeated Sail pairs | `guest-no-device` has an explicit platform-qualified cross-model skip; no semantic-independence claim |\n| Public Sail FP guests | 24 guest pairs /927 boundaries repeat under the selected configuration | Finite instruction/state observations; agreement does not establish an independent numeric implementation |\n| Specification-side numeric fixtures | Directed and seeded expected results are computed by the project's exact-rational reference and checked against its hardware controls | A separately tested derivation with a declared scope, rather than a conclusion about reference internals |\n| Candidate and pair records | Artifact identities, declared expected-result provenance and unresolved pair/subsystem questions | Schema presence and legal verdicts do not authenticate their narrative basis |\n\nFor example, scalar arithmetic writes are derived from the instruction rules\nbefore comparison. A temporary wrong x1 expectation makes the otherwise\nsuccessful public smoke fail. FP numerical evidence is supplied by the tracked\n[qualification fixtures](p4/floating-point.md), including the exact-rational\nreference's own controls. Public trace agreement supplements those derivations.\nIt cannot replace them.\n\n### The historical inventory and its current limit\n\nP0 recorded six pair/subsystem rows across four verdict classes. Its historical\nrationale included dependency source-tree inspection and implementation ancestry\ninferences. Those are retained as history in the\n[exact-span archive](../../../tasks/archive/P4-SYSTEM-reference-c29e.md), with\nsource identities; they are withdrawn as a current dependency basis.\n\nThe canonical base dossier still has two structured experiments and six\nindependence rows. The GC dossier has no structured experiment or independence\nrows yet; its measured runs remain in acceptance receipts until `.14` registers\nthem. `P4-SYSTEM.14` owns the scheduled repair of canonical lineage/inventory\ntext, active reference decisions and maintained knowledge/plans. Their existing\nancestry verdicts are historical assertions pending that repair, and confer no\nnew current independence credit.\n\n### What the gate checks\n\n`PROFILE-CONSISTENCY` requires exactly two known candidates per inventory row,\na legal verdict, and nonempty subsystem/evidence/consequence fields. Every pair\ncompared in a structured experiment must have a row. `not-examined` is legal;\nan omitted row refuses the record. `G0` renders the declared verdicts. Neither\nconsumer independently authenticates implementation ancestry. The useful\ncurrent discipline is explicit provenance and limits, plus independent expected\nvalues and failing controls.\n\n",
      "bytes": 2989,
      "sha256": "bf49ac8ac51d89b28a7e9db7540a94efe2fb80b2a8e4ba6949c8804737fde81b"
    },
    {
      "path": "docs/book/src/plan/p0.md",
      "new": "actual evidence path works: the two recorded P0 experiments agree and reproduce\non separately identified artifacts. Differences and six pair/subsystem rows are\nenumerated. These record checks do not authenticate historical ancestry claims;\nthe current evidence limits and `.14` repair are stated above.",
      "bytes": 247,
      "sha256": "f0dfc27da47e62a72b142efef9e3a7f5d62beefe4da6b6d58a7c2ffa89a7520f"
    },
    {
      "path": "docs/book/src/plan/p4.md",
      "new": "conversions, NaN payloads and boxing; published API capabilities, artifact and\nbuild identities, documented expected-result provenance and unresolved\nindependence limits; and independently derived numeric fixtures. Qualification\nuses the public interface and measured results, without depending on a\nsubmodule's implementation details.",
      "bytes": 218,
      "sha256": "8227359e77af76968787b6756337a6f767588d316346f1c09b26a25fcb0abcb4"
    },
    {
      "path": "docs/book/src/plan/p4.md",
      "new": "That qualification and the F/D bindings are complete. The numeric basis is the\nspecification-side exact-rational fixtures and their hardware controls. Public\nreference comparisons supply finite instruction/state observations; agreement\nalone earns no claim of numeric independence. Historical ancestry assertions\nare withdrawn from this overview's current basis; `.14` owns their record sweep.",
      "bytes": 151,
      "sha256": "580fc5dbb2eab8bf1124469893031f1d29add5aa2658dc9e7f12533ea4042292"
    },
    {
      "path": "LIVE_STATUS.md",
      "new": "| Reference independence inventoried | Done | Historical 6 rows; ancestry basis withdrawn; current record sweep: `P4-SYSTEM.14` |",
      "bytes": 133,
      "sha256": "b945362f518dcc9c8c2e78891bcdf31b95990f893e425ff198e27951c857cf76"
    }
  ]
}
```

## span-01

Source: `docs/book/src/plan/p0.md`. Historical text below is not a current dependency basis.

<!-- BEGIN span-01 bytes=1033 sha256=41c9c5d371a1f9dd4d0b81cfba49a97b45311e647a29af2be8ad0308c52314c8 -->
Acquire reproducible source or binary builds for the chosen reference path, and **run at least
one actual matched-profile experiment before marking that reference usable**. Record tool
versions, source and binary hashes, effective configurations, adapters, and known gaps. Then
establish whether a second comparator shares relevant semantic code with the first.

That last sentence is the one that does the work. Two tools with different names are not two
opinions if their expected results come from the same model. Three facts already known:

- the RISC-V architectural tests use **ACT4**, which computes expected results with a
  *configured Sail* model — valuable external tests, not a second semantics;
- **TestFloat** ordinarily obtains its expected values from **SoftFloat**, so comparing against
  SoftFloat directly is not automatically another independent numerical engine;
- **Spike** is a different implementation path, but its subsystems' independence has to be
  examined rather than inferred from the project name.


<!-- END span-01 -->

## span-02

Source: `docs/book/src/plan/p0.md`. Historical text below is not a current dependency basis.

<!-- BEGIN span-02 bytes=655 sha256=c84383043910290e0636b998b1a1f99830df831ba8ef5e050ac10d87c4fbece2 -->
The plan already warned about this and the acquisition confirmed it in writing. ACT computes its
expected results using a *configured Sail model*, so ACT agreeing with Sail is one semantics
answering twice. Spike and QEMU were written independently of Sail and of each other — *plausibly*,
which is a hypothesis, not a finding. Every candidate record carries a `lineage` field stating
what is known and what is not, and the gate **refuses a candidate that omits it**, because an
independence question nobody asked reads exactly like one that was answered.

Resolving it per subsystem is a separate leaf. Having the binaries is not having the evidence.


<!-- END span-02 -->

## span-03

Source: `docs/book/src/plan/p0.md`. Historical text below is not a current dependency basis.

<!-- BEGIN span-03 bytes=439 sha256=ac63247d13c86ac18a186f7d9c9498b4e4dc96c07d41b518ce898a4a7a5e694a -->
*The Sail model cannot be configured down to exactly "no extensions."* From a default of 96
supported extensions it reaches `rv64i_zvl32b` — the base plus a vestigial minimum vector-length
class that survives because the model always instantiates a `VLEN` even with the vector unit
disabled. No vector instruction decodes, so it is believed harmless. It is recorded anyway,
because "believed harmless" and "absent" are different words.


<!-- END span-03 -->

## span-04

Source: `docs/book/src/plan/p0.md`. Historical text below is not a current dependency basis.

<!-- BEGIN span-04 bytes=312 sha256=9e24de0606e8c542ed72cfd52e60000676296fe5c51e42ac06d711ad49ff323d -->
The encodings therefore come
from a separately pinned machine-readable source, recorded as its own provenance — and that
source is upstream of both models, so "our bytes decode as expected" is *not* an independent
confirmation. It is independent for semantics, which is what the experiment is actually testing.
<!-- END span-04 -->

## span-05

Source: `docs/book/src/plan/p0.md`. Historical text below is not a current dependency basis.

<!-- BEGIN span-05 bytes=2989 sha256=bf49ac8ac51d89b28a7e9db7540a94efe2fb80b2a8e4ba6949c8804737fde81b -->
The plan warned that two tools with different names are not two opinions. With two of them now
agreeing over fifteen steps, that warning became a question to answer rather than repeat, so the
ancestry was examined per subsystem and per pair — by reading both source trees, at the exact
commit the Sail binary reports for itself.

| Subsystem | Sail vs Spike | Evidence |
| --- | --- | --- |
| Instruction encoding | **not shared** | Spike generates `encoding.h` from `riscv-opcodes`; the Sail model hand-writes 59 files of `encdec` mappings and never mentions `riscv-opcodes` under `model/` |
| Floating point | **shared** | both vendor Berkeley SoftFloat; **184 of the 199 files present in both copies are byte-identical** |
| Integer semantics | no evidence of sharing | no textual reference in either direction |
| ACT vs Sail | **shared** | ACT computes its expected results with a configured Sail model |
| QEMU pairs | **not examined** | nobody has looked; recorded rather than omitted |

### The floating-point row

Both models vendor Berkeley SoftFloat — Sail Release 3e, Spike Release 3d — and `f64_add.c`
differs between the two copies by **one line**: the release number in a comment. For 184 of the
199 overlapping files, a differential floating-point test between these two models would execute
*one implementation twice* and report agreement. The agreement would be real, reproducible, and
worthless as independent evidence.

Nothing currently held is affected: this profile declares no floating point, and the experiment
compares integer semantics only. So the finding is routed forward to the milestone that
introduces floating point, with its measurement attached, rather than acted on here.

### The encoding row cuts the other way

This was not anticipated. The project's own assembler takes its encodings from `riscv-opcodes` —
the same source Spike generates from, and a source the Sail model does not use. So when Sail
decodes the emitted bytes as intended that is a genuinely independent confirmation of the
encoding, and when Spike does, it is not. **Independence is a property of a pair and a subsystem,
never of a tool.**

### "Not examined" is written down

Two pairs involving QEMU have no measurement at all, and they appear in the inventory saying so.
An omitted pair reads exactly like an independent one, and the distinction between *looked and
found nothing* and *never looked* is the whole value of the exercise. For the same reason, the
integer-semantics row says **no evidence of sharing** rather than *not shared*: no textual
reference in either direction rules out one model importing the other, and says nothing about
two authors having read the same third specification — which, for an ISA model, is the normal case.

The gate now enforces the discipline rather than trusting it: an experiment record that compares
two models is refused unless an independence record examines that pair. `not-examined` is a legal
verdict; silence is not.


<!-- END span-05 -->

## span-06

Source: `docs/book/src/plan/p0.md`. Historical text below is not a current dependency basis.

<!-- BEGIN span-06 bytes=247 sha256=f0dfc27da47e62a72b142efef9e3a7f5d62beefe4da6b6d58a7c2ffa89a7520f -->
actual evidence path works: two experiments, two independently built models, agreeing and
reproduced. Differences are enumerated: four recorded, plus six independence records across four
verdict classes — including the pairs nobody has examined.
<!-- END span-06 -->

## span-07

Source: `docs/book/src/plan/p4.md`. Historical text below is not a current dependency basis.

<!-- BEGIN span-07 bytes=218 sha256=8227359e77af76968787b6756337a6f767588d316346f1c09b26a25fcb0abcb4 -->
conversions, NaN payloads and boxing; the ancestry inventory (shared SoftFloat lineage, target
specialization, thread-local versus global status handling, exact compiler and features); and
independent numeric fixtures.
<!-- END span-07 -->

## span-08

Source: `docs/book/src/plan/p4.md`. Historical text below is not a current dependency basis.

<!-- BEGIN span-08 bytes=151 sha256=580fc5dbb2eab8bf1124469893031f1d29add5aa2658dc9e7f12533ea4042292 -->
That qualification and the F/D bindings are complete. Sail-versus-Spike remains one
SoftFloat implementation twice, never independent numeric evidence.
<!-- END span-08 -->

## span-09

Source: `LIVE_STATUS.md`. Historical text below is not a current dependency basis.

<!-- BEGIN span-09 bytes=133 sha256=b945362f518dcc9c8c2e78891bcdf31b95990f893e425ff198e27951c857cf76 -->
| Reference independence inventoried | Done | 6 pairs, 4 verdicts; FP **shared** (184/199 files identical), routed to `P4-SYSTEM.7` |
<!-- END span-09 -->
