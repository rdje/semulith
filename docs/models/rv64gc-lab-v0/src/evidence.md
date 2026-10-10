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

## Prospective qualification contract

The complete declaration below is included from its authoritative decision.
Its implementation status is explicit; the current gate report is unchanged.

{{#include ../../../decisions/decision_qualified-matched-experiment-contract.md:contract}}
