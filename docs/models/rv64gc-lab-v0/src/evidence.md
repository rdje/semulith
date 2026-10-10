# Current processor gate

The complete generated report below is included from the canonical dossier.
G-CONTRACT measures effective version membership and realized bindings, rather
than the raw historical catalogue counts in the materials table. Registration
changes the review surface and collection census, without changing requirements,
frozen records or the acceptance decision.

{{#include ../../../../profiles/rv64gc-lab-v0/GS-REPORT.md}}

## Experiment identities

`PROFILE-CONSISTENCY` checks the existing `references.sexp` experiment grammar:
every experiment ID is unique within its dossier, every model names a declared
candidate, and a model occurs only once in an experiment. An independence row
must name two distinct candidates. These rules also apply to a one-model record;
missing a second comparator does not permit an invented first one.

For example, in a dossier whose only candidate is `sail-riscv`, this otherwise
well-shaped illustrative record is refused as `UNKNOWN EXPERIMENT MODEL`:

```lisp
(experiment (id "example-one") (program "example.s") (instructions 1)
  (models "missing-model") (verdict "AGREE") (reproduced "yes")
  (control "a wrong expected value was observed diverging"))
```

Using one ID for two conflicting experiment records is refused as
`DUPLICATE EXPERIMENT ID`. Repeating a candidate in `models` is refused as
`REPEATED EXPERIMENT MODEL`. This illustrative self-pair is refused as `BAD PAIR`:

```lisp
(independence (subsystem "example")
  (pair "sail-riscv") (pair "sail-riscv") (verdict "not-examined")
  (evidence "ancestry is unknown") (consequence "no independence credit"))
```

Run the positive and negative controls from the repository root:

```bash
bash scripts/check_profile_consistency.sh --self-test
```

A legal `not-examined` row records uncertainty. Metadata validation does not
establish adequate evidence, observed controls, current artifacts or independence.
Structured GC runs and policy-derived requirement status remain P4.14 work; the
generated gate report above remains the acceptance authority.

## Qualification contract and structured syntax

The complete declaration below is included from its authoritative decision.
Grammar/mapping and declared-edge checks exist; qualification remains closed.
The current gate report is unchanged.

{{#include ../../../decisions/decision_qualified-matched-experiment-contract.md:contract}}

## Checking identities and declared relationships

`PROFILE-CONSISTENCY` now passes each new verification experiment's raw form to
the schema checker **before mapping it**. A duplicated singular field is refused
before the dictionary could collapse its two values. Legacy records retain their
existing checks. There are no canonical v1 captures yet.

`scripts/experiment_verification.py` owns these relationship checks. The caller
supplies the parent profile's candidate inventory; requirements are filtered by
profile, and effective obligations reuse the existing contract measurement,
including inheritance and supersession. A superseded or foreign obligation cannot
be credited merely because its historical record is still in the catalogue.
This validates compatible identities, without assuming one requirement corresponds
to exactly one obligation or that naming them establishes coverage.

Every child family needs unique IDs. Producer inputs resolve; reference producers
name actual experiment candidates, one producer per candidate. Expected-result
producers keep their own identities. Shared inputs declared on a producer must be
its own inputs. Runs resolve their inputs, producers and observations, include
reference and expected producers, and include each producer's declared inputs.
Every observation belongs to exactly one run, and all observations are used.

Baseline, repeat and control kinds must all be present. A repeat names a baseline
and preserves its input and producer sets. Other run kinds cannot carry
`repeat_of`. Controls name actual control runs, mutated inputs used by that run
and existing properties. Their observed verdict must agree with the run record.
Every control run needs a control record. An honestly recorded control that
expected `DIVERGE` but observed `AGREE` remains consistent data; it earns no
adequacy credit from this checker.

Every producer pair used by a run needs an assessment. Endpoints resolve and
are distinct; a pair/subsystem cannot carry conflicting repeated assessments.
The recorded shared-input IDs must equal the intersection of the producers'
declared input IDs. This makes common inputs visible. It does not authenticate
implementation ancestry: an ancestry assessment and a common guest/source input
describe different facts, and no assessment string creates independence credit.

Paths must use canonical lexical repository-relative POSIX form. Absolute paths,
parent traversal, repeated separators, dot components, backslashes, drive syntax
and control characters are refused. Inputs and observations cannot alias one
declared path, and observation sizes cannot be negative. Filesystem resolution,
symlinks, volume identity, file existence, hashes and actual sizes remain the next
artifact verifier's responsibility.

For an otherwise complete record, these changes have distinct diagnostics:

| Edit | Refusal |
| --- | --- |
| Repeat names a missing run or another repeat | `VERIFICATION REPEAT EDGE` |
| Repeat changes its input or producer set | `VERIFICATION REPEAT INPUTS` |
| Two runs claim the same observation ID | `VERIFICATION OBSERVATION OWNER` |
| Control's observed verdict differs from its run | `VERIFICATION CONTROL VERDICT` |
| Pair hides or invents a declared shared input | `VERIFICATION PAIR SHARING` |
| Property names an obsolete or foreign obligation | `VERIFICATION OBLIGATION SCOPE` |

Run the offline controls from the repository root:

```bash
python3 scripts/probe_experiment_graph.py
bash scripts/check_profile_consistency.sh --self-test
```

The graph suite exercises 63 positive/negative cases. It checks raw duplicated and
unknown fields, current effective scope, every child identity and the declared
edge classes above. Removing a predicate must expose its intended control even
when another rule also refuses the same record.

An empty issue list from `check_experiment` means these declared relationships
are consistent. The blanket `UNQUALIFIED EXPERIMENT VERIFICATION` refusal remains
in production pending artifact/comparison evaluation. This unit does not verify
executed mutations, successful processes, invocation equivalence, complete traces,
byte-identical repeats, correct results or sufficient coverage. No CPU requirement
status, gate axis, artifact budget or retention layout changes.
